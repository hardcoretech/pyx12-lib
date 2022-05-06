import six

from pyx12lib.core import exceptions
from pyx12lib.core.grammar import element, segment


class RenderedSegment:
    def __init__(self, grammar, elements, segment_terminator, element_delimiter):
        self._grammar = grammar
        self._elements = elements
        self._segment_terminator = segment_terminator
        self._element_delimiter = element_delimiter

    def is_valid(self):
        # Check empty segment
        if self.is_empty():
            if self._grammar.usage == segment.USAGE_MANDATORY:
                raise exceptions.MandatorySegmentException(self._grammar)
            if self._grammar.usage in (segment.USAGE_OPTIONAL, segment.USAGE_CONDITIONAL):
                return True

        # Check each element
        return all(ele.is_valid() for ele in self._elements)

    def is_empty(self):
        return all(e.is_empty() for e in self._elements)

    def to_string(self):
        ele_values = self._element_delimiter.join(
            (self._grammar.segment_id, *(e.to_string() for e in self._elements))
        )
        return ele_values.rstrip(self._element_delimiter) + self._segment_terminator


class RenderedElement:
    def __init__(self, ele, value):
        self._element = ele
        self._value = value

    def is_valid(self):
        ele = self._element
        value = self.to_string()

        # Skip NotUsedElement
        if isinstance(ele, element.NotUsedElement):
            if value != '':
                raise exceptions.NotUsedElementException(ele, value)
            return True

        # Check string type
        if not isinstance(value, six.string_types):
            raise exceptions.NotStringException(ele, value)

        # Check mandatory
        if ele.usage == element.USAGE_MANDATORY and value == '':
            raise exceptions.MandatoryElementException(ele, value)

        if value != '':
            # Check width
            if not (ele.minimum <= len(value) <= ele.maximum):
                raise exceptions.LengthException(ele, value)

            # Check type
            if ele.type == element.ELEMENT_TYPE_DECIMAL or ele.type.startswith(element.ELEMENT_TYPE_NUMERIC):
                try:
                    float(value)
                except ValueError:
                    raise exceptions.NotDecimalError(ele, value)

            if ele.type.startswith(element.ELEMENT_TYPE_NUMERIC):
                decimal_places = int(ele.type[1])
                try:
                    if len(value.split('.')[1]) != decimal_places:
                        raise exceptions.DecimalPlaceNotMatchError(ele, value)
                except IndexError:
                    if decimal_places > 0:
                        raise exceptions.DecimalPlaceNotMatchError(ele, value)

        return True

    def is_empty(self):
        return not bool(self._value)

    def to_string(self):
        return self._value


class RenderedCompositeElement:
    def __init__(self, composite_ele, components, component_delimiter):
        self._composite_element = composite_ele
        self._components = components
        self._component_delimiter = component_delimiter

    def is_valid(self):
        # Check empty composite element
        if self.is_empty():
            if self._composite_element.usage == element.USAGE_MANDATORY:
                raise exceptions.MandatoryCompositeElementException(
                    self._composite_element
                )
            if self._composite_element.usage in (
                element.USAGE_OPTIONAL,
                element.USAGE_CONDITIONAL,
            ):
                return True

        # Check each component
        return all(comp.is_valid() for comp in self._components)

    def is_empty(self):
        return all(comp.is_empty() for comp in self._components)

    def to_string(self):
        return self._component_delimiter.join(
            (comp.to_string() for comp in self._components)
        ).rstrip(self._component_delimiter)


class RenderedComponent:
    def __init__(self, component, value):
        self._component = component
        self._value = value

    def is_valid(self):
        component = self._component
        value = self.to_string()

        # Skip NotUsedElement
        if isinstance(component, element.NotUsedElement):
            if value != '':
                raise exceptions.NotUsedElementException(component, value)
            return True

        # Check data type
        if not isinstance(value, six.string_types):
            raise exceptions.NotStringException(component, value)

        # Check mandatory
        if component.usage == element.USAGE_MANDATORY and value == '':
            raise exceptions.MandatoryComponentException(component, value)

        if value != '':
            # Check width
            if not (component.minimum <= len(value) <= component.maximum):
                raise exceptions.LengthException(component, value)

        return True

    def is_empty(self):
        return not bool(self._value)

    def to_string(self):
        return self._value
