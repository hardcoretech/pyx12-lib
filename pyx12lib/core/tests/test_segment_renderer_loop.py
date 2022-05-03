from unittest import TestCase

from pyx12lib.core.grammar import BaseSegment, Element, NotUsedElement, element, segment
from pyx12lib.core.renderer import SegmentRenderer, SegmentRendererLoop


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


class _Test2Segment(BaseSegment):
    segment_id = "TEST2"
    usage = segment.USAGE_MANDATORY
    max_use = 1
    elements = (
        Element(
            reference_designator="TEST201",
            name="Test Element",
            usage=element.USAGE_OPTIONAL,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=1,
        ),
    )


class TestSegmentRendererLoop(TestCase):
    def test_default_data_list_for_renderer_loop(self):
        # arrange
        expect_result = "TEST**11~" "TEST2*2~"
        data = {
            "test_data_1": "11",
            "test_data_2": "2",
        }

        class _TestSegmentRenderer(SegmentRenderer):
            grammar = _TestSegment
            element_value_getters = {
                "TEST02": lambda ele, data, stat: data["test_data_1"],
            }

        class _Test2SegmentRenderer(SegmentRenderer):
            grammar = _Test2Segment
            element_value_getters = {
                "TEST201": lambda ele, data, stat: data["test_data_2"],
            }

        class _TestSegmentRendererLoop(SegmentRendererLoop):
            loop_id = "TEST"
            renderer_class_list = [
                _TestSegmentRenderer,
                _Test2SegmentRenderer,
            ]

        # action
        renderer = _TestSegmentRendererLoop(data)
        result = renderer.render()

        # assert
        self.assertEqual(expect_result, result)

    def test_customized_data_list_for_renderer_loop(self):
        # arrange
        expect_result = "TEST**AA~" "TEST2*1~" "TEST**BB~" "TEST2*2~"
        data = {
            "test_data_1": ["AA", "1"],
            "test_data_2": ["BB", "2"],
        }

        class _TestSegmentRenderer(SegmentRenderer):
            grammar = _TestSegment
            element_value_getters = {
                "TEST02": lambda ele, data, stat: data.test_data_1,
            }

        class _Test2SegmentRenderer(SegmentRenderer):
            grammar = _Test2Segment
            element_value_getters = {
                "TEST201": lambda ele, data, stat: data.test_data_2,
            }

        class _TestSegmentRendererLoop(SegmentRendererLoop):
            loop_id = "TEST"
            renderer_class_list = [
                _TestSegmentRenderer,
                _Test2SegmentRenderer,
            ]

            def preprocess_data(self, data):
                data_list = []
                data_list.append(
                    self.build_data(
                        test_data_1=data["test_data_1"][0],
                        test_data_2=data["test_data_1"][1],
                    )
                )
                data_list.append(
                    self.build_data(
                        test_data_1=data["test_data_2"][0],
                        test_data_2=data["test_data_2"][1],
                    )
                )
                return data_list

        # action
        renderer = _TestSegmentRendererLoop(data)
        result = renderer.render()

        # assert
        self.assertEqual(expect_result, result)
