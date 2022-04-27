# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import collections
import copy
from builtins import object, zip

import six

from pyx12lib.core import exceptions
from pyx12lib.core.grammar.element import (
    COMPONENT_DELIMITER,
    ELEMENT_TYPE_DECIMAL,
    ELEMENT_TYPE_NUMERIC,
    NotUsedElement,
)
from pyx12lib.core.grammar.segment import (
    ELEMENT_DELIMITER,
    SEGMENT_TERMINATOR,
    USAGE_CONDITIONAL,
    USAGE_MANDATORY,
    USAGE_OPTIONAL,
)

WEIGHT_MAX_DIGITS = 3
MEASURE_MAX_DIGITS = 4


class BaseSegmentRenderer(object):
    def __init__(
        self,
        segment_terminator=SEGMENT_TERMINATOR,
        element_delimiter=ELEMENT_DELIMITER,
        component_delimiter=COMPONENT_DELIMITER,
    ):
        self._segment_terminator = segment_terminator
        self._element_delimiter = element_delimiter
        self._component_delimiter = component_delimiter

    def count(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError


class SegmentRenderer(BaseSegmentRenderer):
    grammar = None
    element_value_getters = None

    _element_values = None

    def __init__(self, data, **kwargs):
        super(SegmentRenderer, self).__init__(**kwargs)

        self._data = data

    def get_element_value_getter(self, ref_des):
        if self.element_value_getters is None:
            raise NotImplementedError('element_value_getters should be defined.')
        return self.element_value_getters.get(ref_des, NotUsedElement.value_getter)

    @staticmethod
    def _is_element_valid(element, value):
        # Skip NotUsedElement
        if isinstance(element, NotUsedElement):
            if value != '':
                raise exceptions.NotUsedElementException(element, value)
            return True

        # Check string type
        if not isinstance(value, six.string_types):
            raise exceptions.NotStringException(element, value)

        # Check mandatory
        if element.usage == USAGE_MANDATORY and value == '':
            raise exceptions.MandatoryElementException(element, value)

        if value != '':
            # Check width
            if not (element.minimum <= len(value) <= element.maximum):
                raise exceptions.LengthException(element, value)

            # Check type
            if element.type == ELEMENT_TYPE_DECIMAL or element.type.startswith(ELEMENT_TYPE_NUMERIC):
                try:
                    float(value)
                except ValueError:
                    raise exceptions.NotDecimalError(element, value)

            if element.type.startswith(ELEMENT_TYPE_NUMERIC):
                decimal_places = int(element.type[1])
                try:
                    if len(value.split('.')[1]) != decimal_places:
                        raise exceptions.DecimalPlaceNotMatchError(element, value)
                except IndexError:
                    if decimal_places > 0:
                        raise exceptions.DecimalPlaceNotMatchError(element, value)

        return True

    def is_valid(self):
        # Check empty segment
        if not any(self._element_values.values()):
            if self.grammar.usage == USAGE_MANDATORY:
                raise exceptions.MandatorySegmentException(self.grammar)
            if self.grammar.usage in (USAGE_OPTIONAL, USAGE_CONDITIONAL):
                return True

        # Check each elements
        return all(
            self._is_element_valid(ele, self._element_values[ele.reference_designator]) for ele in self.grammar.elements
        )

    def count(self):
        return 1 if any(self._element_values.values()) else 0

    def build(self):
        self._element_values = collections.OrderedDict()

        for ele in self.grammar.elements:
            ref_des = ele.reference_designator
            value_getter = self.get_element_value_getter(ref_des)
            self._element_values[ref_des] = value_getter(ele, self._data, self._element_values)

        return self._element_values

    def render(self):
        ele_values_dict = self._element_values if self._element_values is not None else self.build()

        self.is_valid()

        if not any(ele_values_dict.values()):
            return ''

        ele_values_list = list(ele_values_dict.values())
        ele_values_list.insert(0, self.grammar.segment_id)
        segment_value = (
            self._element_delimiter.join(ele_values_list).rstrip(self._element_delimiter) + self._segment_terminator
        )

        return segment_value


class ComponentSegmentRenderer(SegmentRenderer):
    def is_composite_element_valid(self, element, comp_values_tuple):
        # Check empty composite element
        if not any(val for ele, val in comp_values_tuple):
            if element.usage == USAGE_MANDATORY:
                raise exceptions.MandatoryCompositeElementException(element)
            if element.usage in (USAGE_OPTIONAL, USAGE_CONDITIONAL):
                return True

        # Check each components
        return all(self.is_component_valid(element, value) for element, value in comp_values_tuple)

    @staticmethod
    def is_component_valid(component, value):
        # Skip NotUsedElement
        if isinstance(component, NotUsedElement):
            if value != '':
                raise exceptions.NotUsedElementException(component, value)
            return True

        # Check data type
        if not isinstance(value, six.string_types):
            raise exceptions.NotStringException(component, value)

        # Check mandatory
        if component.usage == USAGE_MANDATORY and value == '':
            raise exceptions.MandatoryComponentException(component, value)

        if value != '':
            # Check width
            if not (component.minimum <= len(value) <= component.maximum):
                raise exceptions.LengthException(component, value)

        return True

    def get_component_values(self, ele, data, stat, value_getters):
        local_stat = copy.deepcopy(stat)

        comp_values = {}
        for comp in ele.components:
            ref_des = comp.reference_designator
            value_getter = value_getters.get(ref_des, NotUsedElement.value_getter)
            comp_values[ref_des] = value_getter(comp, data, local_stat)

            local_stat.update(comp_values)

        comp_values_list = [comp_values[comp.reference_designator] for comp in ele.components]
        self.is_composite_element_valid(ele, list(zip(ele.components, comp_values_list)))

        return self._component_delimiter.join(comp_values_list).rstrip(self._component_delimiter)


class SegmentRendererLoop(BaseSegmentRenderer):
    loop_id = None
    renderer_class_list = None

    _count = 0
    _renderer_list = None

    def __init__(self, data, **kwargs):
        super(SegmentRendererLoop, self).__init__(**kwargs)

        self._data_list = self.preprocess_data(data)

        assert isinstance(self._data_list, list)
        assert all(
            issubclass(renderer, (SegmentRenderer, SegmentRendererLoop)) for renderer in self.renderer_class_list
        )

    def build_data(self, **kwargs):
        return collections.namedtuple(self.loop_id + 'LoopData', list(kwargs.keys()))(**kwargs)

    def preprocess_data(self, data):
        """
        :param data: data from outer loop
        :return: list of processed data
        """
        return [data]

    def count(self):
        return self._count

    def build(self):
        self._renderer_list = []
        for data in self._data_list:
            for renderer_class in self.renderer_class_list:
                renderer = renderer_class(data)
                renderer.build()
                self._renderer_list.append(renderer)

        self._count = sum(r.count() for r in self._renderer_list)

        return self._renderer_list

    def render(self):
        """
        traverse the loop to get data from each Segments, validation is done by each SegmentRenderer
        :return: values of all segments inside the loop
        """
        renderer_list = self._renderer_list if self._renderer_list is not None else self.build()

        return ''.join(r.render() for r in renderer_list if r.count())
