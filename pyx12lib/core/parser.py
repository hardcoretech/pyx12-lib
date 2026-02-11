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

    def parse(self):
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


class X12Parser(BaseSegmentParser):
    """Parse a complete X12 string containing multiple segments.

    Uses a GrammarRegistry to auto-detect segment types by their ID.
    Unknown segments (not in the registry) are skipped.

    If auto_detect_delimiters is True and the string starts with ISA,
    delimiters are automatically detected from the ISA header.
    """

    def __init__(self, x12_string, registry=None, auto_detect_delimiters=True, **kwargs):
        self._x12_string = x12_string

        if auto_detect_delimiters and x12_string.lstrip().startswith('ISA'):
            detected = detect_delimiters(x12_string)
            kwargs.setdefault('segment_terminator', detected.segment_terminator)
            kwargs.setdefault('element_delimiter', detected.element_delimiter)
            kwargs.setdefault('component_delimiter', detected.component_delimiter)

        super(X12Parser, self).__init__(**kwargs)

        if registry is None:
            registry = create_default_registry()
        self._registry = registry
        self._parsed_segments = None

    def parse(self):
        if self._parsed_segments is not None:
            return self._parsed_segments

        flat_segments = []
        raw_segments = self._x12_string.split(self._segment_terminator)

        for raw in raw_segments:
            raw = raw.strip()
            if not raw:
                continue

            segment_id = raw.split(self._element_delimiter)[0]
            grammar = self._registry.get(segment_id)
            if grammar is None:
                continue

            parser = SegmentParser(
                raw + self._segment_terminator,
                grammar=grammar,
                segment_terminator=self._segment_terminator,
                element_delimiter=self._element_delimiter,
                component_delimiter=self._component_delimiter,
            )
            flat_segments.append(parser.parse())

        if self._registry.has_loops:
            self._parsed_segments = self._organize_into_loops(flat_segments)
        else:
            self._parsed_segments = flat_segments

        return self._parsed_segments

    def _organize_into_loops(self, flat_segments):
        """Group flat segments into ParsedLoop objects based on registry loop definitions."""
        result = []
        current_loop = None
        current_loop_def = None

        for segment in flat_segments:
            seg_id = segment.segment_id
            loop_def = self._registry.get_loop(seg_id)

            if loop_def is not None:
                # This segment starts a new loop.
                if current_loop is not None:
                    result.append(current_loop)
                current_loop = ParsedLoop(loop_id=loop_def.loop_id)
                current_loop.add_segment(segment)
                current_loop_def = loop_def

            elif current_loop is not None and current_loop_def.is_child(seg_id):
                current_loop.add_segment(segment)

            else:
                if current_loop is not None:
                    result.append(current_loop)
                    current_loop = None
                    current_loop_def = None
                result.append(segment)

        if current_loop is not None:
            result.append(current_loop)

        return result

    def to_dict(self):
        return {
            'segments': [s.to_dict() for s in self.parse()],
        }

    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)
