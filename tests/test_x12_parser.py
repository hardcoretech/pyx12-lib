import json
from unittest import TestCase

from pyx12lib.core.grammar import BaseSegment, Element, element, segment
from pyx12lib.core.parser import X12Parser
from pyx12lib.core.registry import GrammarRegistry, create_default_registry


class _CustomSegment(BaseSegment):
    segment_id = "CUS"
    usage = segment.USAGE_OPTIONAL
    max_use = 99
    elements = (
        Element(
            reference_designator="CUS01",
            name="Custom Element",
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=10,
        ),
    )


class TestX12Parser(TestCase):
    def test_parse_multiple_envelope_segments(self):
        # arrange
        x12_string = "ST*997*0001~SE*1*0001~"

        # action
        parser = X12Parser(x12_string)
        result = parser.to_dict()

        # assert
        self.assertEqual(len(result['segments']), 2)
        self.assertEqual(result['segments'][0]['segment_id'], 'ST')
        self.assertEqual(result['segments'][1]['segment_id'], 'SE')

    def test_parse_full_envelope(self):
        # arrange
        x12_string = (
            "ISA*00*          *00*          *ZZ*SENDER         "
            "*ZZ*RECEIVER       *210101*1200*^*00501*000000001*0*P*>~"
            "GS*FA*SENDER*RECEIVER*20210101*1200*1*X*005010~"
            "ST*997*0001~"
            "SE*1*0001~"
            "GE*1*1~"
            "IEA*1*000000001~"
        )

        # action
        parser = X12Parser(x12_string)
        result = parser.to_dict()

        # assert
        self.assertEqual(len(result['segments']), 6)
        segment_ids = [s['segment_id'] for s in result['segments']]
        self.assertEqual(segment_ids, ['ISA', 'GS', 'ST', 'SE', 'GE', 'IEA'])

    def test_unknown_segments_are_skipped(self):
        # arrange: BOGUS is not in default registry
        x12_string = "ST*997*0001~BOGUS*DATA~SE*1*0001~"

        # action
        parser = X12Parser(x12_string)
        result = parser.to_dict()

        # assert
        self.assertEqual(len(result['segments']), 2)
        self.assertEqual(result['segments'][0]['segment_id'], 'ST')
        self.assertEqual(result['segments'][1]['segment_id'], 'SE')

    def test_custom_registry(self):
        # arrange
        registry = GrammarRegistry()
        registry.register(_CustomSegment)
        x12_string = "CUS*hello~CUS*world~"

        # action
        parser = X12Parser(x12_string, registry=registry)
        result = parser.to_dict()

        # assert
        self.assertEqual(len(result['segments']), 2)
        self.assertEqual(result['segments'][0]['elements'][0]['value'], 'hello')
        self.assertEqual(result['segments'][1]['elements'][0]['value'], 'world')

    def test_to_json_produces_valid_json(self):
        # arrange
        x12_string = "ST*997*0001~SE*1*0001~"

        # action
        parser = X12Parser(x12_string)
        json_output = parser.to_json()

        # assert
        data = json.loads(json_output)
        self.assertIn('segments', data)
        self.assertEqual(len(data['segments']), 2)

    def test_empty_string_returns_no_segments(self):
        # arrange
        x12_string = ""

        # action
        parser = X12Parser(x12_string)
        result = parser.to_dict()

        # assert
        self.assertEqual(len(result['segments']), 0)

    def test_whitespace_only_returns_no_segments(self):
        # arrange
        x12_string = "  \n  \n  "

        # action
        parser = X12Parser(x12_string)
        result = parser.to_dict()

        # assert
        self.assertEqual(len(result['segments']), 0)

    def test_parse_caches_result(self):
        # arrange
        x12_string = "ST*997*0001~SE*1*0001~"

        # action
        parser = X12Parser(x12_string)
        result1 = parser.parse()
        result2 = parser.parse()

        # assert
        self.assertIs(result1, result2)

    def test_newline_separated_segments(self):
        # arrange: segments separated by newlines
        x12_string = "ST*997*0001~\nSE*1*0001~\n"

        # action
        parser = X12Parser(x12_string)
        result = parser.to_dict()

        # assert
        self.assertEqual(len(result['segments']), 2)

    def test_mixed_registry_with_defaults(self):
        # arrange: add custom to default registry
        registry = create_default_registry()
        registry.register(_CustomSegment)
        x12_string = "ST*997*0001~CUS*test~SE*1*0001~"

        # action
        parser = X12Parser(x12_string, registry=registry)
        result = parser.to_dict()

        # assert
        self.assertEqual(len(result['segments']), 3)
        self.assertEqual(result['segments'][0]['segment_id'], 'ST')
        self.assertEqual(result['segments'][1]['segment_id'], 'CUS')
        self.assertEqual(result['segments'][2]['segment_id'], 'SE')
