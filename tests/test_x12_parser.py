import json
from unittest import TestCase

from pyx12lib.core.grammar import BaseSegment, Element, element, segment
from pyx12lib.core.grammar.loop import LoopDefinition
from pyx12lib.core.parsed import ParsedLoop, ParsedSegment
from pyx12lib.core.parser import X12Parser, X12ParseResult
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


class _SegA(BaseSegment):
    segment_id = "A"
    usage = segment.USAGE_OPTIONAL
    max_use = 99
    elements = (
        Element(
            reference_designator="A01",
            name="A Element",
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=10,
        ),
    )


class _SegB(BaseSegment):
    segment_id = "B"
    usage = segment.USAGE_OPTIONAL
    max_use = 99
    elements = (
        Element(
            reference_designator="B01",
            name="B Element",
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=10,
        ),
    )


class _SegN1(BaseSegment):
    segment_id = "N1"
    usage = segment.USAGE_OPTIONAL
    max_use = 99
    elements = (
        Element(
            reference_designator="N101",
            name="Entity Identifier Code",
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=10,
        ),
    )


class _SegN2(BaseSegment):
    segment_id = "N2"
    usage = segment.USAGE_OPTIONAL
    max_use = 99
    elements = (
        Element(
            reference_designator="N201",
            name="Name",
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=60,
        ),
    )


class _SegN3(BaseSegment):
    segment_id = "N3"
    usage = segment.USAGE_OPTIONAL
    max_use = 99
    elements = (
        Element(
            reference_designator="N301",
            name="Address",
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=55,
        ),
    )


class _SegLX(BaseSegment):
    segment_id = "LX"
    usage = segment.USAGE_OPTIONAL
    max_use = 99
    elements = (
        Element(
            reference_designator="LX01",
            name="Assigned Number",
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_NUMERIC,
            minimum=1,
            maximum=6,
        ),
    )


class _SegN7(BaseSegment):
    segment_id = "N7"
    usage = segment.USAGE_OPTIONAL
    max_use = 99
    elements = (
        Element(
            reference_designator="N701",
            name="Equipment Initial",
            usage=element.USAGE_OPTIONAL,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=4,
        ),
    )


class TestX12Parser(TestCase):
    def test_parse_multiple_envelope_segments(self):
        # arrange
        x12_string = "ST*997*0001~SE*1*0001~"

        # action
        parser = X12Parser()
        result = parser.parse(x12_string).to_dict()

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
        parser = X12Parser()
        result = parser.parse(x12_string).to_dict()

        # assert
        self.assertEqual(len(result['segments']), 6)
        segment_ids = [s['segment_id'] for s in result['segments']]
        self.assertEqual(segment_ids, ['ISA', 'GS', 'ST', 'SE', 'GE', 'IEA'])

    def test_unknown_segments_are_skipped(self):
        # arrange: BOGUS is not in default registry
        x12_string = "ST*997*0001~BOGUS*DATA~SE*1*0001~"

        # action
        parser = X12Parser()
        result = parser.parse(x12_string).to_dict()

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
        parser = X12Parser(registry=registry)
        result = parser.parse(x12_string).to_dict()

        # assert
        self.assertEqual(len(result['segments']), 2)
        self.assertEqual(result['segments'][0]['elements'][0]['value'], 'hello')
        self.assertEqual(result['segments'][1]['elements'][0]['value'], 'world')

    def test_to_json_produces_valid_json(self):
        # arrange
        x12_string = "ST*997*0001~SE*1*0001~"

        # action
        parser = X12Parser()
        json_output = parser.parse(x12_string).to_json()

        # assert
        data = json.loads(json_output)
        self.assertIn('segments', data)
        self.assertEqual(len(data['segments']), 2)

    def test_empty_string_returns_no_segments(self):
        # arrange
        x12_string = ""

        # action
        parser = X12Parser()
        result = parser.parse(x12_string).to_dict()

        # assert
        self.assertEqual(len(result['segments']), 0)

    def test_whitespace_only_returns_no_segments(self):
        # arrange
        x12_string = "  \n  \n  "

        # action
        parser = X12Parser()
        result = parser.parse(x12_string).to_dict()

        # assert
        self.assertEqual(len(result['segments']), 0)

    def test_parse_returns_x12_parse_result(self):
        # arrange
        x12_string = "ST*997*0001~SE*1*0001~"

        # action
        parser = X12Parser()
        result = parser.parse(x12_string)

        # assert
        self.assertIsInstance(result, X12ParseResult)
        self.assertEqual(len(result.segments), 2)

    def test_parser_is_reusable(self):
        # arrange
        parser = X12Parser()

        # action
        result1 = parser.parse("ST*997*0001~SE*1*0001~")
        result2 = parser.parse("ST*997*0002~")

        # assert
        self.assertEqual(len(result1.segments), 2)
        self.assertEqual(len(result2.segments), 1)

    def test_newline_separated_segments(self):
        # arrange: segments separated by newlines
        x12_string = "ST*997*0001~\nSE*1*0001~\n"

        # action
        parser = X12Parser()
        result = parser.parse(x12_string).to_dict()

        # assert
        self.assertEqual(len(result['segments']), 2)

    def test_mixed_registry_with_defaults(self):
        # arrange: add custom to default registry
        registry = create_default_registry()
        registry.register(_CustomSegment)
        x12_string = "ST*997*0001~CUS*test~SE*1*0001~"

        # action
        parser = X12Parser(registry=registry)
        result = parser.parse(x12_string).to_dict()

        # assert
        self.assertEqual(len(result['segments']), 3)
        self.assertEqual(result['segments'][0]['segment_id'], 'ST')
        self.assertEqual(result['segments'][1]['segment_id'], 'CUS')
        self.assertEqual(result['segments'][2]['segment_id'], 'SE')


class TestX12ParserWithLoops(TestCase):
    """Test loop-aware parsing behavior."""

    def _make_registry(self, loop_defs=None, extra_grammars=None):
        registry = GrammarRegistry()
        if extra_grammars:
            registry.register_all(extra_grammars)
        if loop_defs:
            for ld in loop_defs:
                registry.register_loop(ld)
        return registry

    def test_no_loops_returns_flat_list(self):
        registry = GrammarRegistry()
        registry.register_all([_SegA, _SegB])
        x12_string = "A*x~B*y~"

        parser = X12Parser(registry=registry)
        result = parser.parse(x12_string)

        self.assertEqual(len(result.segments), 2)
        self.assertIsInstance(result.segments[0], ParsedSegment)
        self.assertIsInstance(result.segments[1], ParsedSegment)

    def test_single_loop_start_no_children(self):
        # [A, N1, B] → [A, Loop(N1), B]
        registry = self._make_registry(
            loop_defs=[LoopDefinition(_SegN1, [_SegN2, _SegN3])],
            extra_grammars=[_SegA, _SegB],
        )
        x12_string = "A*x~N1*CA~B*y~"

        parser = X12Parser(registry=registry)
        result = parser.parse(x12_string)

        self.assertEqual(len(result.segments), 3)
        self.assertIsInstance(result.segments[0], ParsedSegment)
        self.assertIsInstance(result.segments[1], ParsedLoop)
        self.assertEqual(result.segments[1].loop_id, "N1")
        self.assertEqual(len(result.segments[1].segments), 1)
        self.assertIsInstance(result.segments[2], ParsedSegment)

    def test_single_loop_with_children(self):
        # [N1, N2, N3] → [Loop(N1, N2, N3)]
        registry = self._make_registry(
            loop_defs=[LoopDefinition(_SegN1, [_SegN2, _SegN3])],
        )
        x12_string = "N1*CA~N2*Name~N3*Addr~"

        parser = X12Parser(registry=registry)
        result = parser.parse(x12_string)

        self.assertEqual(len(result.segments), 1)
        self.assertIsInstance(result.segments[0], ParsedLoop)
        self.assertEqual(result.segments[0].loop_id, "N1")
        self.assertEqual(len(result.segments[0].segments), 3)
        self.assertEqual(result.segments[0].segments[0].segment_id, "N1")
        self.assertEqual(result.segments[0].segments[1].segment_id, "N2")
        self.assertEqual(result.segments[0].segments[2].segment_id, "N3")

    def test_consecutive_loop_starts(self):
        # [N1, N1] → [Loop(N1), Loop(N1)]
        registry = self._make_registry(
            loop_defs=[LoopDefinition(_SegN1, [_SegN2])],
        )
        x12_string = "N1*CA~N1*SH~"

        parser = X12Parser(registry=registry)
        result = parser.parse(x12_string)

        self.assertEqual(len(result.segments), 2)
        self.assertIsInstance(result.segments[0], ParsedLoop)
        self.assertIsInstance(result.segments[1], ParsedLoop)
        self.assertEqual(len(result.segments[0].segments), 1)
        self.assertEqual(len(result.segments[1].segments), 1)

    def test_loop_terminated_by_non_child(self):
        # [N1, N2, B] → [Loop(N1, N2), B]
        registry = self._make_registry(
            loop_defs=[LoopDefinition(_SegN1, [_SegN2, _SegN3])],
            extra_grammars=[_SegB],
        )
        x12_string = "N1*CA~N2*Name~B*y~"

        parser = X12Parser(registry=registry)
        result = parser.parse(x12_string)

        self.assertEqual(len(result.segments), 2)
        self.assertIsInstance(result.segments[0], ParsedLoop)
        self.assertEqual(len(result.segments[0].segments), 2)
        self.assertIsInstance(result.segments[1], ParsedSegment)
        self.assertEqual(result.segments[1].segment_id, "B")

    def test_loop_terminated_by_different_loop(self):
        # [N1, N2, LX, N7] → [Loop(N1, N2), Loop(LX, N7)]
        registry = self._make_registry(
            loop_defs=[
                LoopDefinition(_SegN1, [_SegN2, _SegN3]),
                LoopDefinition(_SegLX, [_SegN7]),
            ],
        )
        x12_string = "N1*CA~N2*Name~LX*1~N7*HLCU~"

        parser = X12Parser(registry=registry)
        result = parser.parse(x12_string)

        self.assertEqual(len(result.segments), 2)
        self.assertIsInstance(result.segments[0], ParsedLoop)
        self.assertEqual(result.segments[0].loop_id, "N1")
        self.assertEqual(len(result.segments[0].segments), 2)
        self.assertIsInstance(result.segments[1], ParsedLoop)
        self.assertEqual(result.segments[1].loop_id, "LX")
        self.assertEqual(len(result.segments[1].segments), 2)

    def test_orphan_child_emitted_flat(self):
        # [N2, N1, N2] → [N2, Loop(N1, N2)]
        registry = self._make_registry(
            loop_defs=[LoopDefinition(_SegN1, [_SegN2])],
        )
        x12_string = "N2*orphan~N1*CA~N2*child~"

        parser = X12Parser(registry=registry)
        result = parser.parse(x12_string)

        self.assertEqual(len(result.segments), 2)
        self.assertIsInstance(result.segments[0], ParsedSegment)
        self.assertEqual(result.segments[0].segment_id, "N2")
        self.assertIsInstance(result.segments[1], ParsedLoop)
        self.assertEqual(len(result.segments[1].segments), 2)

    def test_to_dict_mixed_output(self):
        registry = self._make_registry(
            loop_defs=[LoopDefinition(_SegN1, [_SegN2])],
            extra_grammars=[_SegA],
        )
        x12_string = "A*x~N1*CA~N2*Name~"

        parser = X12Parser(registry=registry)
        result = parser.parse(x12_string).to_dict()

        self.assertIn('segment_id', result['segments'][0])
        self.assertEqual(result['segments'][0]['segment_id'], 'A')
        self.assertIn('loop_id', result['segments'][1])
        self.assertEqual(result['segments'][1]['loop_id'], 'N1')

    def test_to_json_with_loops(self):
        registry = self._make_registry(
            loop_defs=[LoopDefinition(_SegN1, [_SegN2])],
            extra_grammars=[_SegA],
        )
        x12_string = "A*x~N1*CA~N2*Name~"

        parser = X12Parser(registry=registry)
        json_output = parser.parse(x12_string).to_json()

        data = json.loads(json_output)
        self.assertIn('segments', data)
        self.assertEqual(len(data['segments']), 2)
        self.assertEqual(data['segments'][1]['loop_id'], 'N1')

    def test_parser_reusable_with_loops(self):
        registry = self._make_registry(
            loop_defs=[LoopDefinition(_SegN1, [_SegN2])],
        )

        parser = X12Parser(registry=registry)
        result1 = parser.parse("N1*CA~N2*Name~")
        result2 = parser.parse("N1*SH~")

        self.assertEqual(len(result1.segments), 1)
        self.assertEqual(len(result1.segments[0].segments), 2)
        self.assertEqual(len(result2.segments), 1)
        self.assertEqual(len(result2.segments[0].segments), 1)
