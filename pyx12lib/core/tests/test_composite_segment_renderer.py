from unittest import TestCase

from pyx12lib.core import exceptions
from pyx12lib.core.grammar import BaseSegment, Element, NotUsedElement, element, segment, CompositeElement, Component
from pyx12lib.core.renderer import CompositeElementRenderer, SegmentRenderer


class _TestCompositeSegment(BaseSegment):
    segment_id = "TEST"
    usage = segment.USAGE_MANDATORY
    max_use = 1
    elements = (
        NotUsedElement(reference_designator="TEST01"),
        Element(
            reference_designator="TEST02",
            name="Test Element",
            usage=element.USAGE_OPTIONAL,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=2,
            maximum=3,
        ),
        CompositeElement(
            reference_designator='TEST03',
            name='Composite Element',
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_COMPOSITE,
            minimum=1,
            maximum=35,
            components=(
                Component(
                    reference_designator='C04001',
                    name='Composite Test 1',
                    usage=element.USAGE_MANDATORY,
                    element_type=element.ELEMENT_TYPE_ID,
                    minimum=1,
                    maximum=1,
                ),
                Component(
                    reference_designator='C04002',
                    name='Composite Test 1',
                    usage=element.USAGE_OPTIONAL,
                    element_type=element.ELEMENT_TYPE_STRING,
                    minimum=1,
                    maximum=5,
                ),
            ),
        ),
        Element(
            reference_designator="TEST04",
            name="Test Element",
            usage=element.USAGE_OPTIONAL,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=30,
        ),
    )


class TestCompositeElementRenderer(TestCase):
    def test_test_mandatory_composite_element_raises_error(self):
        # arrange
        data = {}

        class _TestCompositeElementRenderer(CompositeElementRenderer):
            grammar = _TestCompositeSegment

            @property
            def element_value_getters(self):
                return {
                    'TEST03': self.test03,
                }

            def test03(self, ele, data, stat):
                value_getters = {
                    'C04001': lambda _comp, _data, _stat: '',
                    'C04002': lambda _comp, _data, _stat: 'TEST',
                }

                return self.get_component_values(ele, data, stat, value_getters)

        # action & assert
        renderer = _TestCompositeElementRenderer(data)
        with self.assertRaises(exceptions.MandatoryComponentException):
            renderer.render()

    def test_test_mandatory_composite_component_raises_error(self):
        # arrange
        data = {}

        class _TestCompositeElementRenderer(CompositeElementRenderer):
            grammar = _TestCompositeSegment

            @property
            def element_value_getters(self):
                return {
                    'TEST03': self.test03,
                }

            def test03(self, ele, data, stat):
                value_getters = {
                    'C04001': lambda _comp, _data, _stat: '',
                    'C04002': lambda _comp, _data, _stat: '',
                }

                return self.get_component_values(ele, data, stat, value_getters)

        # action & assert
        renderer = _TestCompositeElementRenderer(data)
        with self.assertRaises(exceptions.MandatoryCompositeElementException):
            renderer.render()

    def test_composite_element(self):
        # arrange
        expect_data = (
            'TEST***A^BCD*TRAILING ELE~'
        )
        data = {
            "test_data_composite": ['A', 'BCD'],
        }

        class _TestCompositeElementRenderer(CompositeElementRenderer):
            grammar = _TestCompositeSegment

            @property
            def element_value_getters(self):
                return {
                    'TEST03': self.test03,
                    'TEST04': lambda ele, data, stat: 'TRAILING ELE',
                }

            def test03(self, ele, data, stat):
                value_getters = {
                    'C04001': lambda _comp, _data, _stat: _data['test_data_composite'][0],
                    'C04002': lambda _comp, _data, _stat: _data['test_data_composite'][1],
                }

                return self.get_component_values(ele, data, stat, value_getters)

        # action
        renderer = _TestCompositeElementRenderer(data)
        result = renderer.render()

        # assert
        self.assertEqual(expect_data, result)
