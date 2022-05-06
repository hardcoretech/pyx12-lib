import collections
import copy

import six

from pyx12lib.core import exceptions
from pyx12lib.core.base import RenderedElement, RenderedSegment, RenderedComponent, RenderedCompositeElement
from pyx12lib.core.grammar.element import (
    COMPONENT_DELIMITER,
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

    _rendered_segment = None

    def __init__(self, data, **kwargs):
        super(SegmentRenderer, self).__init__(**kwargs)

        self._data = data

    def get_element_value_getter(self, ref_des):
        if self.element_value_getters is None:
            raise NotImplementedError('element_value_getters should be defined.')
        return self.element_value_getters.get(ref_des, NotUsedElement.value_getter)

    def _get_rendered_segment(self):
        if self._rendered_segment is None:
            self.build()
        return self._rendered_segment

    def count(self):
        return 1 if not self._get_rendered_segment().is_empty() else 0

    def build(self):
        render_stat = collections.OrderedDict()

        elements = []
        for ele in self.grammar.elements:
            value = self.get_element_value_getter(ele.reference_designator)(ele, self._data, render_stat)
            render_stat[ele.reference_designator] = value
            elements.append(RenderedElement(ele=ele, value=value))

        self._rendered_segment = RenderedSegment(
            grammar=self.grammar,
            elements=elements,
            segment_terminator=self._segment_terminator,
            element_delimiter=self._element_delimiter,
        )

    def render(self):
        rendered_segment = self._get_rendered_segment()

        rendered_segment.is_valid()

        if rendered_segment.is_empty():
            return ''

        return rendered_segment.to_string()


class CompositeElementRenderer(SegmentRenderer):
    def get_component_values(self, ele, data, stat, value_getters):
        local_stat = copy.deepcopy(stat)

        comp_values = {}
        components = []
        for comp in ele.components:
            value = value_getters.get(comp.reference_designator, NotUsedElement.value_getter)(comp, data, local_stat)
            comp_values[comp.reference_designator] = value
            components.append(RenderedComponent(component=comp, value=value))

            local_stat.update(comp_values)

        composite_ele = RenderedCompositeElement(
            composite_ele=ele,
            components=components,
            component_delimiter=self._component_delimiter,
        )

        composite_ele.is_valid()

        return composite_ele.to_string()


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
