from unittest import TestCase

from pyx12lib.core import exceptions
from pyx12lib.core.grammar import BaseSegment, Element, NotUsedElement, element, segment
from pyx12lib.core.renderer import SegmentRenderer


class _TestSegment(BaseSegment):
    segment_id = "TEST"
    usage = segment.USAGE_MANDATORY
    max_use = 1
    elements = (
        NotUsedElement(reference_designator="TEST01"),
        Element(
            reference_designator="TEST02",
            name="Test Element",
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=2,
            maximum=3,
        ),
        Element(
            reference_designator="TEST03",
            name="Test Element",
            usage=element.USAGE_OPTIONAL,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=1,
        ),
        Element(
            reference_designator="TEST04",
            name="Test Element",
            usage=element.USAGE_OPTIONAL,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=1,
        ),
    )


class TestSegmentRenderer(TestCase):
    def test_mandatory_segment_raises_error(self):
        # arrange
        data = {
            "test_data": "",
        }

        class _TestSegmentRenderer(SegmentRenderer):
            grammar = _TestSegment
            element_value_getters = {
                "TEST02": lambda ele, data, stat: data["test_data"],
            }

        # action & assert
        renderer = _TestSegmentRenderer(data)
        with self.assertRaises(exceptions.MandatorySegmentException):
            renderer.render()

    def test_mandatory_element_raises_error(self):
        # arrange
        data = {
            "test_data": "",
        }

        class _TestSegmentRenderer(SegmentRenderer):
            grammar = _TestSegment
            element_value_getters = {
                "TEST02": lambda ele, data, stat: data["test_data"],
                "TEST03": lambda ele, data, stat: "TEST 03",
            }

        # action & assert
        renderer = _TestSegmentRenderer(data)
        with self.assertRaises(exceptions.MandatoryElementException):
            renderer.render()

    def test_element_too_short_raises_error(self):
        # arrange
        data = {
            "test_data": "1",
        }

        class _TestSegmentRenderer(SegmentRenderer):
            grammar = _TestSegment
            element_value_getters = {
                "TEST02": lambda ele, data, stat: data["test_data"],
            }

        # action & assert
        renderer = _TestSegmentRenderer(data)
        with self.assertRaises(exceptions.LengthException):
            renderer.render()

    def test_element_too_long_raises_error(self):
        # arrange
        data = {
            "test_data": "1234",
        }

        class _TestSegmentRenderer(SegmentRenderer):
            grammar = _TestSegment
            element_value_getters = {
                "TEST02": lambda ele, data, stat: data["test_data"],
            }

        # action & assert
        renderer = _TestSegmentRenderer(data)
        with self.assertRaises(exceptions.LengthException):
            renderer.render()

    def test_renderer_with_complex_value_getter(self):
        # arrange
        expect_result = "TEST**000~"
        data = {
            "test_data": 0,
        }

        class _TestSegmentRenderer(SegmentRenderer):
            grammar = _TestSegment

            @property
            def element_value_getters(self):
                return {
                    "TEST02": self.test002,
                }

            @staticmethod
            def test002(ele, data, stat):
                return f"{data['test_data']:03d}"

        # action
        renderer = _TestSegmentRenderer(data)
        result = renderer.render()

        # assert
        self.assertEqual(expect_result, result)

    def test_omit_empty_trailing_elements(self):
        # arrange
        expect_result = "TEST**12~"
        data = {
            "test_data": "12",
        }

        class _TestSegmentRenderer(SegmentRenderer):
            grammar = _TestSegment
            element_value_getters = {
                "TEST02": lambda ele, data, stat: data["test_data"],
                "TEST03": lambda ele, data, stat: "",
                "TEST04": lambda ele, data, stat: "",
            }

        # action
        renderer = _TestSegmentRenderer(data)
        result = renderer.render()

        # assert
        self.assertEqual(expect_result, result)
