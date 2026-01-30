from unittest import TestCase

from pyx12lib.core.grammar import (
    BaseSegment, Element, CompositeElement, Component, NotUsedElement,
    element, segment,
)
from pyx12lib.core.parser import SegmentParser


class _TestCompositeSegment(BaseSegment):
    segment_id = "COMP"
    usage = segment.USAGE_MANDATORY
    max_use = 1
    elements = (
        Element(
            reference_designator="COMP01",
            name="Simple Element",
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=2,
            maximum=3,
        ),
        CompositeElement(
            reference_designator='COMP02',
            name='Composite Element',
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_COMPOSITE,
            minimum=1,
            maximum=35,
            components=(
                Component(
                    reference_designator='C001',
                    name='Component 1',
                    usage=element.USAGE_MANDATORY,
                    element_type=element.ELEMENT_TYPE_ID,
                    minimum=1,
                    maximum=2,
                ),
                Component(
                    reference_designator='C002',
                    name='Component 2',
                    usage=element.USAGE_OPTIONAL,
                    element_type=element.ELEMENT_TYPE_STRING,
                    minimum=1,
                    maximum=5,
                ),
            ),
        ),
        Element(
            reference_designator="COMP03",
            name="Trailing Element",
            usage=element.USAGE_OPTIONAL,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=30,
        ),
    )


class _SegmentWithNotUsedAndComposite(BaseSegment):
    segment_id = "MIX"
    usage = segment.USAGE_MANDATORY
    max_use = 1
    elements = (
        NotUsedElement(reference_designator="MIX01"),
        Element(
            reference_designator="MIX02",
            name="Simple",
            usage=element.USAGE_OPTIONAL,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=2,
            maximum=3,
        ),
        CompositeElement(
            reference_designator='MIX03',
            name='Composite',
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_COMPOSITE,
            minimum=1,
            maximum=35,
            components=(
                Component(
                    reference_designator='M001',
                    name='Comp 1',
                    usage=element.USAGE_MANDATORY,
                    element_type=element.ELEMENT_TYPE_ID,
                    minimum=1,
                    maximum=1,
                ),
                Component(
                    reference_designator='M002',
                    name='Comp 2',
                    usage=element.USAGE_OPTIONAL,
                    element_type=element.ELEMENT_TYPE_STRING,
                    minimum=1,
                    maximum=5,
                ),
            ),
        ),
        Element(
            reference_designator="MIX04",
            name="After Composite",
            usage=element.USAGE_OPTIONAL,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=30,
        ),
    )


class TestCompositeParser(TestCase):
    def test_parse_composite_element(self):
        # arrange
        x12_string = "COMP*AB*X^TEST~"

        # action
        parser = SegmentParser(x12_string, grammar=_TestCompositeSegment)
        result = parser.to_dict()

        # assert
        self.assertEqual(result['segment_id'], 'COMP')
        self.assertEqual(len(result['elements']), 3)

        # First element is simple
        self.assertEqual(result['elements'][0]['value'], 'AB')

        # Second element is composite
        composite = result['elements'][1]
        self.assertIn('components', composite)
        self.assertEqual(len(composite['components']), 2)
        self.assertEqual(composite['components'][0]['value'], 'X')
        self.assertEqual(composite['components'][0]['reference_designator'], 'C001')
        self.assertEqual(composite['components'][1]['value'], 'TEST')
        self.assertEqual(composite['components'][1]['reference_designator'], 'C002')

    def test_parse_composite_with_trailing_element(self):
        # arrange
        x12_string = "COMP*AB*A^BCD*TRAILING ELE~"

        # action
        parser = SegmentParser(x12_string, grammar=_TestCompositeSegment)
        result = parser.to_dict()

        # assert
        self.assertEqual(result['elements'][2]['value'], 'TRAILING ELE')

    def test_parse_composite_with_empty_components(self):
        # arrange: composite has only first component
        x12_string = "COMP*AB*X~"

        # action
        parser = SegmentParser(x12_string, grammar=_TestCompositeSegment)
        result = parser.to_dict()

        # assert
        composite = result['elements'][1]
        self.assertEqual(composite['components'][0]['value'], 'X')
        self.assertEqual(composite['components'][1]['value'], '')

    def test_parse_empty_composite(self):
        # arrange: composite is empty
        x12_string = "COMP*AB*~"

        # action
        parser = SegmentParser(x12_string, grammar=_TestCompositeSegment)
        result = parser.to_dict()

        # assert
        composite = result['elements'][1]
        self.assertEqual(len(composite['components']), 2)
        # Empty string split gives [''], first component gets ''
        self.assertEqual(composite['components'][0]['value'], '')
        self.assertEqual(composite['components'][1]['value'], '')

    def test_composite_validation_valid(self):
        # arrange
        x12_string = "COMP*AB*X^TEST~"

        # action
        parser = SegmentParser(x12_string, grammar=_TestCompositeSegment)
        parsed = parser.parse()

        # assert
        self.assertTrue(parsed.is_valid())

    def test_composite_validation_missing_mandatory_component(self):
        # arrange: C001 is mandatory but empty
        x12_string = "COMP*AB*^TEST~"

        # action
        parser = SegmentParser(x12_string, grammar=_TestCompositeSegment)
        parsed = parser.parse()

        # assert - composite has empty mandatory component
        composite = parsed.elements[1]
        self.assertFalse(composite.is_valid())

    def test_segment_with_not_used_and_composite(self):
        # arrange: MIX01 is NotUsed, MIX02 is simple, MIX03 is composite
        x12_string = "MIX**AB*A^BCD*TRAILING~"

        # action
        parser = SegmentParser(x12_string, grammar=_SegmentWithNotUsedAndComposite)
        result = parser.to_dict()

        # assert: NotUsed skipped, 3 elements in output
        self.assertEqual(len(result['elements']), 3)
        self.assertEqual(result['elements'][0]['reference_designator'], 'MIX02')
        self.assertEqual(result['elements'][0]['value'], 'AB')
        self.assertIn('components', result['elements'][1])
        self.assertEqual(result['elements'][1]['components'][0]['value'], 'A')
        self.assertEqual(result['elements'][2]['value'], 'TRAILING')

    def test_parse_composite_json_output(self):
        # arrange
        x12_string = "COMP*AB*X^TEST~"

        # action
        parser = SegmentParser(x12_string, grammar=_TestCompositeSegment)
        json_output = parser.to_json()

        # assert
        self.assertIn('"components"', json_output)
        self.assertIn('"C001"', json_output)


class TestEnvelopeSegmentParsing(TestCase):
    """Test parsing with real envelope grammar definitions."""

    def test_parse_st_segment(self):
        from pyx12lib.common.envelope.grammar import StSegment

        # arrange
        x12_string = "ST*997*0001~"

        # action
        parser = SegmentParser(x12_string, grammar=StSegment)
        result = parser.to_dict()

        # assert
        self.assertEqual(result['segment_id'], 'ST')
        self.assertEqual(result['elements'][0]['value'], '997')
        self.assertEqual(result['elements'][0]['reference_designator'], 'ST01')
        self.assertEqual(result['elements'][1]['value'], '0001')

    def test_parse_se_segment(self):
        from pyx12lib.common.envelope.grammar import SeSegment

        # arrange
        x12_string = "SE*5*0001~"

        # action
        parser = SegmentParser(x12_string, grammar=SeSegment)
        result = parser.to_dict()

        # assert
        self.assertEqual(result['segment_id'], 'SE')
        self.assertEqual(result['elements'][0]['value'], '5')
        self.assertEqual(result['elements'][1]['value'], '0001')

    def test_parse_gs_segment(self):
        from pyx12lib.common.envelope.grammar import GsSegment

        # arrange
        x12_string = "GS*FA*SENDER*RECEIVER*20210101*1200*1*X*005010~"

        # action
        parser = SegmentParser(x12_string, grammar=GsSegment)
        result = parser.to_dict()

        # assert
        self.assertEqual(result['segment_id'], 'GS')
        self.assertEqual(len(result['elements']), 8)
        self.assertEqual(result['elements'][0]['value'], 'FA')
        self.assertEqual(result['elements'][1]['value'], 'SENDER')
        self.assertEqual(result['elements'][7]['value'], '005010')

    def test_parse_ge_segment(self):
        from pyx12lib.common.envelope.grammar import GeSegment

        # arrange
        x12_string = "GE*1*1~"

        # action
        parser = SegmentParser(x12_string, grammar=GeSegment)
        result = parser.to_dict()

        # assert
        self.assertEqual(result['segment_id'], 'GE')
        self.assertEqual(result['elements'][0]['value'], '1')
        self.assertEqual(result['elements'][1]['value'], '1')

    def test_parse_isa_segment(self):
        from pyx12lib.common.envelope.grammar import IsaSegment

        # arrange
        x12_string = (
            "ISA*00*          *00*          *ZZ*SENDER         "
            "*ZZ*RECEIVER       *210101*1200*^*00501*000000001*0*P*>~"
        )

        # action
        parser = SegmentParser(x12_string, grammar=IsaSegment)
        result = parser.to_dict()

        # assert
        self.assertEqual(result['segment_id'], 'ISA')
        self.assertEqual(len(result['elements']), 16)
        self.assertEqual(result['elements'][0]['value'], '00')
        self.assertEqual(result['elements'][0]['reference_designator'], 'ISA01')
        # ISA06 = Sender ID (padded)
        self.assertEqual(result['elements'][5]['value'], 'SENDER         ')
        # ISA16 = component separator
        self.assertEqual(result['elements'][15]['value'], '>')

    def test_parse_iea_segment(self):
        from pyx12lib.common.envelope.grammar import IeaSegment

        # arrange
        x12_string = "IEA*1*000000001~"

        # action
        parser = SegmentParser(x12_string, grammar=IeaSegment)
        result = parser.to_dict()

        # assert
        self.assertEqual(result['segment_id'], 'IEA')
        self.assertEqual(result['elements'][0]['value'], '1')
        self.assertEqual(result['elements'][1]['value'], '000000001')
