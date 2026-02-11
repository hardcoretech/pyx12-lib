import json
from typing import Iterable

from pyx12lib.core.grammar.element import (
    USAGE_MANDATORY,
    ELEMENT_TYPE_DECIMAL,
    ELEMENT_TYPE_NUMERIC,
    CompositeElement,
)


class ParsedElement:
    """Represents a parsed element with its value and grammar metadata."""

    def __init__(self, grammar, value):
        self._grammar = grammar
        self._value = value

    @property
    def grammar(self):
        return self._grammar

    @property
    def value(self):
        return self._value

    def to_dict(self):
        return {
            'reference_designator': self._grammar.reference_designator,
            'name': self._grammar.name,
            'value': self._value,
            'type': self._grammar.type,
            'usage': self._grammar.usage,
        }

    def is_valid(self):
        ele = self._grammar
        value = self._value

        if not isinstance(value, str):
            return False

        if ele.usage == USAGE_MANDATORY and value == '':
            return False

        if value != '':
            if not (ele.minimum <= len(value) <= ele.maximum):
                return False

            if ele.type == ELEMENT_TYPE_DECIMAL:
                stripped_sign = value.lstrip('-')
                if not stripped_sign or not stripped_sign.replace('.', '', 1).isdigit():
                    return False
            elif ele.type.startswith(ELEMENT_TYPE_NUMERIC):
                stripped_sign = value.lstrip('-')
                if not stripped_sign or not stripped_sign.isdigit():
                    return False

        return True

    def is_empty(self):
        return not bool(self._value)


class ParsedComponent(ParsedElement):
    """Represents a parsed component within a composite element."""
    pass


class ParsedCompositeElement:
    """Represents a parsed composite element containing components."""

    def __init__(self, grammar: CompositeElement, components: Iterable[ParsedComponent]) -> None:
        self._grammar = grammar
        self._components = components

    @property
    def grammar(self):
        return self._grammar

    @property
    def components(self):
        return self._components

    def to_dict(self):
        return {
            'reference_designator': self._grammar.reference_designator,
            'name': self._grammar.name,
            'components': [c.to_dict() for c in self._components],
        }

    def is_valid(self):
        if self.is_empty():
            if self._grammar.usage == USAGE_MANDATORY:
                return False
            return True
        return all(c.is_valid() for c in self._components)

    def is_empty(self):
        return all(c.is_empty() for c in self._components)


class ParsedSegment:
    """Represents a fully parsed segment with all its elements."""

    def __init__(self, grammar, elements):
        self._grammar = grammar
        self._elements = elements

    @property
    def grammar(self):
        return self._grammar

    @property
    def elements(self):
        return self._elements

    @property
    def segment_id(self):
        return self._grammar.segment_id

    def to_dict(self):
        return {
            'segment_id': self._grammar.segment_id,
            'elements': [e.to_dict() for e in self._elements],
        }

    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)

    def is_valid(self):
        if self.is_empty():
            if self._grammar.usage == USAGE_MANDATORY:
                return False
            return True
        return all(e.is_valid() for e in self._elements)

    def is_empty(self):
        return all(e.is_empty() for e in self._elements)


class ParsedLoop:
    """Represents a hierarchical loop of parsed segments."""

    def __init__(self, loop_id, segments=None):
        self.loop_id = loop_id
        self.segments = segments or []
        self.child_loops = []

    def add_segment(self, segment):
        self.segments.append(segment)

    def add_child_loop(self, loop):
        self.child_loops.append(loop)

    def to_dict(self):
        result = {
            'loop_id': self.loop_id,
            'segments': [s.to_dict() for s in self.segments],
        }
        if self.child_loops:
            result['child_loops'] = [c.to_dict() for c in self.child_loops]
        return result

    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)
