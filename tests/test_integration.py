import json
import time
from unittest import TestCase

from pyx12lib import parse_x12, parse_x12_to_json
from pyx12lib.core.parser import SegmentParser


class TestIntegrationFullEnvelope(TestCase):
    """Integration tests with complete X12 envelope structures."""

    FULL_X12 = (
        "ISA*00*          *00*          *ZZ*SENDER         "
        "*ZZ*RECEIVER       *210101*1200*^*00501*000000001*0*P*>~"
        "GS*FA*SENDER*RECEIVER*20210101*1200*1*X*005010~"
        "ST*997*0001~"
        "SE*1*0001~"
        "GE*1*1~"
        "IEA*1*000000001~"
    )

    def test_parse_complete_transaction(self):
        result = parse_x12(self.FULL_X12)

        self.assertEqual(len(result['segments']), 6)
        segment_ids = [s['segment_id'] for s in result['segments']]
        self.assertEqual(segment_ids, ['ISA', 'GS', 'ST', 'SE', 'GE', 'IEA'])

    def test_parse_to_json_is_valid_json(self):
        json_output = parse_x12_to_json(self.FULL_X12)

        data = json.loads(json_output)
        self.assertIn('segments', data)
        self.assertEqual(len(data['segments']), 6)

    def test_isa_element_values(self):
        result = parse_x12(self.FULL_X12)

        isa = result['segments'][0]
        self.assertEqual(isa['segment_id'], 'ISA')
        # ISA01 = Authorization Info Qualifier
        self.assertEqual(isa['elements'][0]['value'], '00')
        # ISA05 = Interchange ID Qualifier
        self.assertEqual(isa['elements'][4]['value'], 'ZZ')
        # ISA13 = Interchange Control Number
        self.assertEqual(isa['elements'][12]['value'], '000000001')
        # ISA15 = Usage Indicator
        self.assertEqual(isa['elements'][14]['value'], 'P')
        # ISA16 = Component Separator
        self.assertEqual(isa['elements'][15]['value'], '>')

    def test_gs_element_values(self):
        result = parse_x12(self.FULL_X12)

        gs = result['segments'][1]
        self.assertEqual(gs['segment_id'], 'GS')
        self.assertEqual(gs['elements'][0]['value'], 'FA')
        self.assertEqual(gs['elements'][1]['value'], 'SENDER')
        self.assertEqual(gs['elements'][7]['value'], '005010')

    def test_st_se_element_values(self):
        result = parse_x12(self.FULL_X12)

        st = result['segments'][2]
        se = result['segments'][3]
        self.assertEqual(st['elements'][0]['value'], '997')
        self.assertEqual(st['elements'][1]['value'], '0001')
        self.assertEqual(se['elements'][0]['value'], '1')
        self.assertEqual(se['elements'][1]['value'], '0001')

    def test_compact_json_no_indent(self):
        json_output = parse_x12_to_json(self.FULL_X12, indent=None)

        self.assertNotIn('\n', json_output)
        data = json.loads(json_output)
        self.assertEqual(len(data['segments']), 6)


class TestEdgeCases(TestCase):
    """Edge case tests for parser robustness."""

    def test_empty_string(self):
        result = parse_x12("")
        self.assertEqual(result['segments'], [])

    def test_only_terminators(self):
        result = parse_x12("~~~")
        self.assertEqual(result['segments'], [])

    def test_only_whitespace(self):
        result = parse_x12("   \n\t  ")
        self.assertEqual(result['segments'], [])

    def test_single_segment(self):
        result = parse_x12("ST*997*0001~")
        self.assertEqual(len(result['segments']), 1)

    def test_trailing_newlines(self):
        result = parse_x12("ST*997*0001~\n\n\n")
        self.assertEqual(len(result['segments']), 1)

    def test_segments_separated_by_crlf(self):
        result = parse_x12("ST*997*0001~\r\nSE*1*0001~\r\n")
        self.assertEqual(len(result['segments']), 2)

    def test_segment_with_many_trailing_empty_elements(self):
        from pyx12lib.core.grammar import BaseSegment, Element, element, segment
        from pyx12lib.core.registry import GrammarRegistry

        class _BigSegment(BaseSegment):
            segment_id = "BIG"
            usage = segment.USAGE_OPTIONAL
            max_use = 1
            elements = tuple(
                Element(
                    reference_designator="BIG{:02d}".format(i),
                    name="Elem {}".format(i),
                    usage=element.USAGE_OPTIONAL,
                    element_type=element.ELEMENT_TYPE_STRING,
                    minimum=1,
                    maximum=10,
                )
                for i in range(1, 11)
            )

        registry = GrammarRegistry()
        registry.register(_BigSegment)

        # Only first element has a value
        result = parse_x12("BIG*hello~", registry=registry)
        self.assertEqual(len(result['segments']), 1)
        elements = result['segments'][0]['elements']
        self.assertEqual(elements[0]['value'], 'hello')
        # Remaining elements should be empty strings
        for e in elements[1:]:
            self.assertEqual(e['value'], '')

    def test_unknown_segments_between_known(self):
        x12 = "ST*997*0001~FOO*BAR~BAZ*QUX*123~SE*1*0001~"
        result = parse_x12(x12)

        # Only ST and SE should be parsed (FOO and BAZ unknown)
        self.assertEqual(len(result['segments']), 2)
        self.assertEqual(result['segments'][0]['segment_id'], 'ST')
        self.assertEqual(result['segments'][1]['segment_id'], 'SE')

    def test_segment_parser_with_extra_elements(self):
        """Parser should not crash if X12 has more elements than grammar defines."""
        from pyx12lib.common.envelope.grammar import StSegment

        # ST grammar has 2 elements, but string has 3
        parser = SegmentParser("ST*997*0001*EXTRA~", grammar=StSegment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'ST')
        self.assertEqual(len(result['elements']), 2)
        self.assertEqual(result['elements'][0]['value'], '997')
        self.assertEqual(result['elements'][1]['value'], '0001')

    def test_segment_parser_with_fewer_elements(self):
        """Parser should handle fewer elements than grammar defines."""
        from pyx12lib.common.envelope.grammar import GsSegment

        # GS grammar has 8 elements, but string has only 3
        parser = SegmentParser("GS*FA*SENDER~", grammar=GsSegment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'GS')
        self.assertEqual(result['elements'][0]['value'], 'FA')
        self.assertEqual(result['elements'][1]['value'], 'SENDER')
        # Missing elements should be empty
        for e in result['elements'][2:]:
            self.assertEqual(e['value'], '')


class TestValidation(TestCase):
    """Tests for parsed segment validation."""

    def test_valid_st_segment(self):
        from pyx12lib.common.envelope.grammar import StSegment

        parser = SegmentParser("ST*997*0001~", grammar=StSegment)
        self.assertTrue(parser.parse().is_valid())

    def test_invalid_st_missing_mandatory(self):
        from pyx12lib.common.envelope.grammar import StSegment

        parser = SegmentParser("ST**0001~", grammar=StSegment)
        self.assertFalse(parser.parse().is_valid())

    def test_invalid_element_too_long(self):
        from pyx12lib.common.envelope.grammar import StSegment

        # ST01 max=3, giving 4 chars
        parser = SegmentParser("ST*9977*0001~", grammar=StSegment)
        self.assertFalse(parser.parse().is_valid())

    def test_invalid_element_too_short(self):
        from pyx12lib.common.envelope.grammar import StSegment

        # ST01 min=3, giving 2 chars
        parser = SegmentParser("ST*99*0001~", grammar=StSegment)
        self.assertFalse(parser.parse().is_valid())

    def test_invalid_numeric_element(self):
        from pyx12lib.common.envelope.grammar import SeSegment

        # SE01 expects numeric, giving non-numeric
        parser = SegmentParser("SE*abc*0001~", grammar=SeSegment)
        self.assertFalse(parser.parse().is_valid())

    def test_valid_numeric_element(self):
        from pyx12lib.common.envelope.grammar import SeSegment

        parser = SegmentParser("SE*5*0001~", grammar=SeSegment)
        self.assertTrue(parser.parse().is_valid())

    def test_empty_optional_segment_is_valid(self):
        from pyx12lib.core.grammar import BaseSegment, Element, element, segment

        class _OptSegment(BaseSegment):
            segment_id = "OPT"
            usage = segment.USAGE_OPTIONAL
            max_use = 1
            elements = (
                Element(
                    reference_designator="OPT01",
                    name="Optional El",
                    usage=element.USAGE_OPTIONAL,
                    element_type=element.ELEMENT_TYPE_STRING,
                    minimum=1,
                    maximum=5,
                ),
            )

        parser = SegmentParser("OPT*~", grammar=_OptSegment)
        self.assertTrue(parser.parse().is_valid())


class TestPerformance(TestCase):
    """Basic performance sanity check."""

    def test_parse_many_segments(self):
        # Build a string with 2000 segments (1000 ST + 1000 SE)
        parts = []
        for i in range(1000):
            parts.append("ST*997*{:04d}~SE*1*{:04d}~".format(i, i))
        x12_string = "".join(parts)

        start = time.time()
        result = parse_x12(x12_string)
        elapsed = time.time() - start

        self.assertEqual(len(result['segments']), 2000)
        # Should parse 2000 segments in well under 1 second
        self.assertLess(elapsed, 1.0)
