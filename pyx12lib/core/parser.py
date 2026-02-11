import json

from pyx12lib.core.parsed import (
    ParsedElement,
    ParsedComponent,
    ParsedCompositeElement,
    ParsedLoop,
    ParsedSegment,
)
from pyx12lib.core.grammar.element import (
    CompositeElement,
    NotUsedElement,
    COMPONENT_DELIMITER,
)
from pyx12lib.core.grammar.segment import (
    ELEMENT_DELIMITER,
    SEGMENT_TERMINATOR,
)
from pyx12lib.core.delimiters import detect_delimiters
from pyx12lib.core.registry import create_default_registry


class BaseSegmentParser(object):
    def __init__(
        self,
        segment_terminator=SEGMENT_TERMINATOR,
        element_delimiter=ELEMENT_DELIMITER,
        component_delimiter=COMPONENT_DELIMITER,
    ):
        self._segment_terminator = segment_terminator
        self._element_delimiter = element_delimiter
        self._component_delimiter = component_delimiter

    def parse(self, x12_string: str):
        raise NotImplementedError


class SegmentParser(BaseSegmentParser):
    """Parse a single X12 segment string using a grammar definition."""

    def __init__(self, segment_string, grammar, **kwargs):
        super(SegmentParser, self).__init__(**kwargs)
        self._segment_string = segment_string.rstrip(self._segment_terminator)
        self._grammar = grammar
        self._parsed_segment = None

    def parse(self):
        if self._parsed_segment is not None:
            return self._parsed_segment

        parts = self._segment_string.split(self._element_delimiter)
        segment_id = parts[0]

        if segment_id != self._grammar.segment_id:
            raise ValueError(
                "Segment ID mismatch: expected '{}', got '{}'".format(
                    self._grammar.segment_id, segment_id
                )
            )

        element_values = parts[1:]
        elements = []

        for i, ele_grammar in enumerate(self._grammar.elements):
            if isinstance(ele_grammar, NotUsedElement):
                continue

            value = element_values[i] if i < len(element_values) else ''

            if isinstance(ele_grammar, CompositeElement):
                parsed = self._parse_composite(ele_grammar, value)
            else:
                parsed = ParsedElement(grammar=ele_grammar, value=value)

            elements.append(parsed)

        self._parsed_segment = ParsedSegment(
            grammar=self._grammar,
            elements=elements,
        )

        return self._parsed_segment

    def _parse_composite(self, grammar, value):
        component_values = value.split(self._component_delimiter) if value else []
        components = []

        for i, comp_grammar in enumerate(grammar.components):
            if isinstance(comp_grammar, NotUsedElement):
                continue
            comp_value = component_values[i] if i < len(component_values) else ''
            components.append(ParsedComponent(grammar=comp_grammar, value=comp_value))

        return ParsedCompositeElement(grammar=grammar, components=components)

    def to_dict(self):
        return self.parse().to_dict()

    def to_json(self, indent=2):
        return self.parse().to_json(indent=indent)


class X12ParseResult(object):
    """Result of parsing an X12 string."""

    def __init__(self, segments):
        self._segments = segments

    @property
    def segments(self):
        return self._segments

    def to_dict(self):
        return {
            'segments': [s.to_dict() for s in self._segments],
        }

    def to_json(self, indent=None):
        return json.dumps(self.to_dict(), indent=indent)


class X12Parser(BaseSegmentParser):
    """Parse complete X12 strings containing multiple segments.

    Uses a GrammarRegistry to auto-detect segment types by their ID.
    Unknown segments (not in the registry) are skipped.

    If auto_detect_delimiters is True and the string starts with ISA,
    delimiters are automatically detected from the ISA header.
    """

    def __init__(self, registry=None, auto_detect_delimiters=True, **kwargs):
        super(X12Parser, self).__init__(**kwargs)

        if registry is None:
            registry = create_default_registry()
        self._registry = registry
        self._auto_detect_delimiters = auto_detect_delimiters

    def parse(self, x12_string):
        segment_terminator = self._segment_terminator
        element_delimiter = self._element_delimiter
        component_delimiter = self._component_delimiter

        if self._auto_detect_delimiters and x12_string.lstrip().startswith('ISA'):
            detected = detect_delimiters(x12_string)
            segment_terminator = detected.segment_terminator
            element_delimiter = detected.element_delimiter
            component_delimiter = detected.component_delimiter

        flat_segments = []
        raw_segments = x12_string.split(segment_terminator)

        for raw in raw_segments:
            raw = raw.strip()
            if not raw:
                continue

            segment_id = raw.split(element_delimiter)[0]
            grammar = self._registry.get(segment_id)
            if grammar is None:
                continue

            parser = SegmentParser(
                raw + segment_terminator,
                grammar=grammar,
                segment_terminator=segment_terminator,
                element_delimiter=element_delimiter,
                component_delimiter=component_delimiter,
            )
            flat_segments.append(parser.parse())

        if self._registry.has_loops:
            segments = self._organize_into_loops(flat_segments)
        else:
            segments = flat_segments

        return X12ParseResult(segments)

    def _organize_into_loops(self, flat_segments):
        """Group flat segments into ParsedLoop objects based on registry loop definitions.

        Single O(n) pass. Maintains two pieces of state:
        - current_loop: the ParsedLoop being built (None when not inside a loop)
        - current_loop_def: the LoopDefinition that governs valid children

        For each segment, exactly one of three cases applies:
        1. Segment starts a new loop (its ID matches a registered LoopDefinition).
        2. Segment is a child of the currently open loop.
        3. Segment is unrelated — emitted flat, closing any open loop first.

        Examples (N1 loop with N2 child):
          [A, N1, N2, B]       → [A, Loop(N1,N2), B]
          [N1*CA, N1*SH, N2]   → [Loop(N1*CA), Loop(N1*SH, N2)]
          [N2, N1, N2]         → [N2, Loop(N1, N2)]   (orphan N2 emitted flat)
        """
        result = []
        current_loop = None
        current_loop_def = None

        for segment in flat_segments:
            seg_id = segment.segment_id
            loop_def = self._registry.get_loop(seg_id)

            if loop_def is not None:
                # Case 1: This segment starts a new loop.
                # Finalize the previous loop if one is open, then start fresh.
                # This also handles consecutive starts (e.g. N1*CA then N1*SH)
                # — each start closes the prior loop.
                if current_loop is not None:
                    result.append(current_loop)
                current_loop = ParsedLoop(loop_id=loop_def.loop_id)
                current_loop.add_segment(segment)
                current_loop_def = loop_def

            elif current_loop is not None and current_loop_def is not None and current_loop_def.is_child(seg_id):
                # Case 2: Segment belongs to the currently open loop.
                # is_child() checks against the LoopDefinition's child_segment_ids
                # (direct children only, not nested loop members).
                current_loop.add_segment(segment)

            else:
                # Case 3: Segment is not a loop start and not a child.
                # If a loop is open, it's terminated by this unrelated segment.
                # The segment itself is emitted as a flat ParsedSegment.
                if current_loop is not None:
                    result.append(current_loop)
                    current_loop = None
                    current_loop_def = None
                result.append(segment)

        # Flush any loop still open after the last segment.
        if current_loop is not None:
            result.append(current_loop)

        return result
