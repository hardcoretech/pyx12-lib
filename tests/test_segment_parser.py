from unittest import TestCase

from pyx12lib.core.grammar import BaseSegment, Element, NotUsedElement, element, segment
from pyx12lib.core.parser import SegmentParser


class _TestSegment(BaseSegment):
    segment_id = "TEST"
    usage = segment.USAGE_MANDATORY
    max_use = 1
    elements = (
        NotUsedElement(reference_designator="TEST01"),
        Element(
            reference_designator="TEST02",
            name="Test Element 1",
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=2,
            maximum=3,
        ),
        Element(
            reference_designator="TEST03",
            name="Test Element 2",
            usage=element.USAGE_OPTIONAL,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=5,
        ),
    )


class _SimpleSegment(BaseSegment):
    segment_id = "SIM"
    usage = segment.USAGE_MANDATORY
    max_use = 1
    elements = (
        Element(
            reference_designator="SIM01",
            name="Element 1",
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_ID,
            minimum=3,
            maximum=3,
        ),
        Element(
            reference_designator="SIM02",
            name="Element 2",
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=4,
            maximum=9,
        ),
    )


class TestSegmentParser(TestCase):
    def test_parse_simple_segment(self):
        # arrange
        x12_string = "SIM*997*0001~"

        # action
        parser = SegmentParser(x12_string, grammar=_SimpleSegment)
        result = parser.to_dict()

        # assert
        self.assertEqual(result['segment_id'], 'SIM')
        self.assertEqual(len(result['elements']), 2)
        self.assertEqual(result['elements'][0]['value'], '997')
        self.assertEqual(result['elements'][0]['reference_designator'], 'SIM01')
        self.assertEqual(result['elements'][1]['value'], '0001')

    def test_parse_segment_with_not_used_element(self):
        # arrange: TEST01 is NotUsedElement, should be skipped in output
        x12_string = "TEST**AB*hello~"

        # action
        parser = SegmentParser(x12_string, grammar=_TestSegment)
        result = parser.to_dict()

        # assert
        self.assertEqual(result['segment_id'], 'TEST')
        self.assertEqual(len(result['elements']), 2)  # NotUsedElement skipped
        self.assertEqual(result['elements'][0]['value'], 'AB')
        self.assertEqual(result['elements'][0]['reference_designator'], 'TEST02')
        self.assertEqual(result['elements'][1]['value'], 'hello')

    def test_parse_segment_with_empty_trailing_elements(self):
        # arrange
        x12_string = "TEST**AB~"

        # action
        parser = SegmentParser(x12_string, grammar=_TestSegment)
        result = parser.to_dict()

        # assert
        self.assertEqual(result['elements'][0]['value'], 'AB')
        self.assertEqual(result['elements'][1]['value'], '')

    def test_parse_segment_to_json(self):
        # arrange
        x12_string = "SIM*997*0001~"

        # action
        parser = SegmentParser(x12_string, grammar=_SimpleSegment)
        json_output = parser.to_json()

        # assert
        self.assertIn('"segment_id": "SIM"', json_output)
        self.assertIn('"value": "997"', json_output)

    def test_invalid_segment_id_raises_error(self):
        # arrange
        x12_string = "WRONG*AB*12345~"

        # action & assert
        parser = SegmentParser(x12_string, grammar=_SimpleSegment)
        with self.assertRaises(ValueError) as ctx:
            parser.parse()
        self.assertIn('SIM', str(ctx.exception))
        self.assertIn('WRONG', str(ctx.exception))

    def test_parse_caches_result(self):
        # arrange
        x12_string = "SIM*997*0001~"

        # action
        parser = SegmentParser(x12_string, grammar=_SimpleSegment)
        result1 = parser.parse()
        result2 = parser.parse()

        # assert - same object returned
        self.assertIs(result1, result2)

    def test_parse_segment_without_terminator(self):
        # arrange: no trailing ~
        x12_string = "SIM*997*0001"

        # action
        parser = SegmentParser(x12_string, grammar=_SimpleSegment)
        result = parser.to_dict()

        # assert
        self.assertEqual(result['segment_id'], 'SIM')
        self.assertEqual(result['elements'][0]['value'], '997')

    def test_parsed_element_metadata(self):
        # arrange
        x12_string = "SIM*997*0001~"

        # action
        parser = SegmentParser(x12_string, grammar=_SimpleSegment)
        result = parser.to_dict()

        # assert
        ele = result['elements'][0]
        self.assertEqual(ele['name'], 'Element 1')
        self.assertEqual(ele['type'], element.ELEMENT_TYPE_ID)
        self.assertEqual(ele['usage'], element.USAGE_MANDATORY)

    def test_is_valid_with_valid_segment(self):
        # arrange
        x12_string = "SIM*997*0001~"

        # action
        parser = SegmentParser(x12_string, grammar=_SimpleSegment)
        parsed = parser.parse()

        # assert
        self.assertTrue(parsed.is_valid())

    def test_is_valid_with_missing_mandatory_element(self):
        # arrange: SIM01 is mandatory but empty
        x12_string = "SIM**0001~"

        # action
        parser = SegmentParser(x12_string, grammar=_SimpleSegment)
        parsed = parser.parse()

        # assert
        self.assertFalse(parsed.is_valid())
