"""
Validation tests using EDI 315 grammar definitions.

These tests parse actual rendered X12 EDI 315 strings using grammar
definitions copied from a real EDI 315 implementation to verify the
parser works with production-grade segment definitions.

Grammar source: gf-notif-svc/edi_315 (B4, R4, DTM, N9, Q2 segments)
"""
import json
from unittest import TestCase

from pyx12lib.core.parser import SegmentParser, X12Parser
from pyx12lib.core.registry import GrammarRegistry, create_default_registry

from tests.fixtures.edi_315_grammar import (
    B4Segment, R4Segment, DTMSegment, N9Segment, Q2Segment,
)


def _make_edi315_registry():
    """Create a registry with all EDI 315 + envelope segments."""
    registry = create_default_registry()
    registry.register(B4Segment)
    registry.register(R4Segment)
    registry.register(DTMSegment)
    registry.register(N9Segment)
    registry.register(Q2Segment)
    return registry


class TestB4SegmentParsing(TestCase):
    """Parse B4 segments rendered by the edi_315 B4Renderer."""

    def test_parse_b4_vessel_depart_full_data(self):
        x12 = 'B4***VD*20221101*1400*USDAL*HASU*431617*L*40HC*USDAL*UN*0~'

        parser = SegmentParser(x12, grammar=B4Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'B4')
        # B401, B402 are NotUsed -> skipped
        self.assertEqual(result['elements'][0]['reference_designator'], 'B403')
        self.assertEqual(result['elements'][0]['value'], 'VD')
        self.assertEqual(result['elements'][1]['value'], '20221101')
        self.assertEqual(result['elements'][2]['value'], '1400')
        self.assertEqual(result['elements'][3]['value'], 'USDAL')
        self.assertEqual(result['elements'][4]['value'], 'HASU')
        self.assertEqual(result['elements'][5]['value'], '431617')
        self.assertEqual(result['elements'][6]['value'], 'L')
        self.assertEqual(result['elements'][7]['value'], '40HC')
        self.assertEqual(result['elements'][8]['value'], 'USDAL')
        self.assertEqual(result['elements'][9]['value'], 'UN')
        self.assertEqual(result['elements'][10]['value'], '0')

    def test_parse_b4_no_timestamp(self):
        x12 = 'B4***I***USDAL*HASU*431617*L*40HC*USDAL*UN*0~'

        parser = SegmentParser(x12, grammar=B4Segment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][0]['value'], 'I')
        self.assertEqual(result['elements'][1]['value'], '')
        self.assertEqual(result['elements'][2]['value'], '')
        self.assertEqual(result['elements'][3]['value'], 'USDAL')

    def test_parse_b4_empty_container_type(self):
        x12 = 'B4***I*20221101*1400*USDAL*HASU*431617*L*    *USDAL*UN*0~'

        parser = SegmentParser(x12, grammar=B4Segment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][7]['value'], '    ')

    def test_b4_validation(self):
        x12 = 'B4***VD*20221101*1400*USDAL*HASU*431617*L*40HC*USDAL*UN*0~'
        parser = SegmentParser(x12, grammar=B4Segment)
        self.assertTrue(parser.parse().is_valid())


class TestN9SegmentParsing(TestCase):
    """Parse N9 segments rendered by the edi_315 N9RendererLoop."""

    def test_parse_n9_bl_number(self):
        x12 = 'N9*BM*BL_NO~'

        parser = SegmentParser(x12, grammar=N9Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'N9')
        self.assertEqual(result['elements'][0]['value'], 'BM')
        self.assertEqual(result['elements'][0]['reference_designator'], 'N901')
        self.assertEqual(result['elements'][1]['value'], 'BL_NO')
        self.assertEqual(result['elements'][1]['reference_designator'], 'N902')

    def test_parse_n9_booking_number(self):
        x12 = 'N9*BN*BOOKING_NO~'

        parser = SegmentParser(x12, grammar=N9Segment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][0]['value'], 'BN')
        self.assertEqual(result['elements'][1]['value'], 'BOOKING_NO')

    def test_parse_n9_equipment(self):
        x12 = 'N9*EQ*HASU4316170~'

        parser = SegmentParser(x12, grammar=N9Segment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][0]['value'], 'EQ')
        self.assertEqual(result['elements'][1]['value'], 'HASU4316170')

    def test_parse_n9_scac(self):
        x12 = 'N9*SCA*SCAC_CODE~'

        parser = SegmentParser(x12, grammar=N9Segment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][0]['value'], 'SCA')
        self.assertEqual(result['elements'][1]['value'], 'SCAC_CODE')

    def test_parse_n9_po_number(self):
        x12 = 'N9*PO*PO123456789~'

        parser = SegmentParser(x12, grammar=N9Segment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][0]['value'], 'PO')
        self.assertEqual(result['elements'][1]['value'], 'PO123456789')

    def test_n9_validation(self):
        x12 = 'N9*BM*BL_NO~'
        parser = SegmentParser(x12, grammar=N9Segment)
        self.assertTrue(parser.parse().is_valid())


class TestR4SegmentParsing(TestCase):
    """Parse R4 segments rendered by the edi_315 R4RendererLoop."""

    def test_parse_r4_port_with_unlocode(self):
        x12 = 'R4*L*UN*VNHPH*HAIPHONG*VN~'

        parser = SegmentParser(x12, grammar=R4Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'R4')
        self.assertEqual(result['elements'][0]['value'], 'L')
        self.assertEqual(result['elements'][1]['value'], 'UN')
        self.assertEqual(result['elements'][2]['value'], 'VNHPH')
        self.assertEqual(result['elements'][3]['value'], 'HAIPHONG')
        self.assertEqual(result['elements'][4]['value'], 'VN')

    def test_parse_r4_port_with_city_name(self):
        x12 = 'R4*R*CI*HAIPHONG*HAIPHONG*VN~'

        parser = SegmentParser(x12, grammar=R4Segment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][0]['value'], 'R')
        self.assertEqual(result['elements'][1]['value'], 'CI')

    def test_parse_r4_discharge_port(self):
        x12 = 'R4*D*UN*SGSIN*SINGAPORE*SG~'

        parser = SegmentParser(x12, grammar=R4Segment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][0]['value'], 'D')
        self.assertEqual(result['elements'][2]['value'], 'SGSIN')
        self.assertEqual(result['elements'][3]['value'], 'SINGAPORE')

    def test_parse_r4_delivery_port(self):
        x12 = 'R4*E*UN*SGSIN*SINGAPORE*SG~'

        parser = SegmentParser(x12, grammar=R4Segment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][0]['value'], 'E')

    def test_parse_r4_minimal(self):
        x12 = 'R4*R*CI~'

        parser = SegmentParser(x12, grammar=R4Segment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][0]['value'], 'R')
        self.assertEqual(result['elements'][1]['value'], 'CI')
        for e in result['elements'][2:]:
            self.assertEqual(e['value'], '')

    def test_r4_validation(self):
        x12 = 'R4*L*UN*VNHPH*HAIPHONG*VN~'
        parser = SegmentParser(x12, grammar=R4Segment)
        self.assertTrue(parser.parse().is_valid())


class TestDTMSegmentParsing(TestCase):
    """Parse DTM segments rendered by the edi_315 DTMRenderer."""

    def test_parse_dtm_estimated(self):
        x12 = 'DTM*139*20221217*0000*LT~'

        parser = SegmentParser(x12, grammar=DTMSegment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'DTM')
        self.assertEqual(result['elements'][0]['value'], '139')
        self.assertEqual(result['elements'][1]['value'], '20221217')
        self.assertEqual(result['elements'][2]['value'], '0000')
        self.assertEqual(result['elements'][3]['value'], 'LT')

    def test_parse_dtm_actual(self):
        x12 = 'DTM*140*20220801*0000*LT~'

        parser = SegmentParser(x12, grammar=DTMSegment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][0]['value'], '140')

    def test_parse_dtm_empty_date(self):
        x12 = 'DTM*139***LT~'

        parser = SegmentParser(x12, grammar=DTMSegment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][0]['value'], '139')
        self.assertEqual(result['elements'][1]['value'], '')
        self.assertEqual(result['elements'][2]['value'], '')
        self.assertEqual(result['elements'][3]['value'], 'LT')

    def test_dtm_validation(self):
        x12 = 'DTM*139*20221217*0000*LT~'
        parser = SegmentParser(x12, grammar=DTMSegment)
        self.assertTrue(parser.parse().is_valid())


class TestQ2SegmentParsing(TestCase):
    """Parse Q2 segments rendered by the edi_315 Q2Renderer."""

    def test_parse_q2_full_data(self):
        x12 = 'Q2*******0*G*371S***L*CAP SAN MARCO***K~'

        parser = SegmentParser(x12, grammar=Q2Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'Q2')
        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}

        self.assertEqual(ref_map['Q201'], '')
        self.assertEqual(ref_map['Q202'], '')
        self.assertNotIn('Q203', ref_map)
        self.assertEqual(ref_map['Q204'], '')
        self.assertEqual(ref_map['Q205'], '')
        self.assertEqual(ref_map['Q206'], '')
        self.assertEqual(ref_map['Q207'], '0')
        self.assertEqual(ref_map['Q208'], 'G')
        self.assertEqual(ref_map['Q209'], '371S')
        self.assertEqual(ref_map['Q210'], '')
        self.assertEqual(ref_map['Q211'], '')
        self.assertEqual(ref_map['Q212'], 'L')
        self.assertEqual(ref_map['Q213'], 'CAP SAN MARCO')
        self.assertEqual(ref_map['Q214'], '')
        self.assertEqual(ref_map['Q215'], '')
        self.assertEqual(ref_map['Q216'], 'K')

    def test_parse_q2_only_vessel_name(self):
        x12 = 'Q2*******0*G****L*CAP SAN MARCO***K~'

        parser = SegmentParser(x12, grammar=Q2Segment)
        result = parser.to_dict()

        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['Q209'], '')
        self.assertEqual(ref_map['Q213'], 'CAP SAN MARCO')

    def test_parse_q2_empty(self):
        x12 = 'Q2*******0*G********K~'

        parser = SegmentParser(x12, grammar=Q2Segment)
        result = parser.to_dict()

        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['Q207'], '0')
        self.assertEqual(ref_map['Q208'], 'G')
        self.assertEqual(ref_map['Q216'], 'K')

    def test_q2_validation(self):
        x12 = 'Q2*******0*G*371S***L*CAP SAN MARCO***K~'
        parser = SegmentParser(x12, grammar=Q2Segment)
        self.assertTrue(parser.parse().is_valid())


class TestFullEdi315DocumentParsing(TestCase):
    """Parse complete EDI 315 documents using X12Parser with edi_315 grammars."""

    FULL_EDI_315 = (
        'ISA*00*          *00*          *ZZ*GOFREIGHT      *ZZ*PARTNERID      *230207*2022*U*00401*000000001*0*P*^~'
        'GS*QO*GOFREIGHT*PARTNERID*20230207*2022*1*X*004010~'
        'ST*315*0001~'
        'B4***VD*20221217*0000*VNHPH*HASU*431617*L*40HC*VNHPH*UN*0~'
        'N9*BM*BL_NO~'
        'N9*BN*BOOKING_NO~'
        'N9*EQ*HASU4316170~'
        'N9*SCA*SCAC_CODE~'
        'Q2*******0*G*371S***L*CAP SAN MARCO***K~'
        'R4*R*CI*HAIPHONG*HAIPHONG*VN~'
        'DTM*139*20221217*0000*LT~'
        'R4*L*UN*VNHPH*HAIPHONG*VN~'
        'DTM*139*20221217*0000*LT~'
        'R4*D*UN*SGSIN*SINGAPORE*SG~'
        'DTM*139*20221226*0000*LT~'
        'R4*E*UN*SGSIN*SINGAPORE*SG~'
        'DTM*139*20221226*0000*LT~'
        'SE*16*0001~'
        'GE*1*1~'
        'IEA*1*000000001~'
    )

    def test_parse_full_document(self):
        registry = _make_edi315_registry()
        parser = X12Parser(registry=registry)
        result = parser.parse(self.FULL_EDI_315).to_dict()

        segment_ids = [s['segment_id'] for s in result['segments']]
        self.assertEqual(segment_ids, [
            'ISA', 'GS', 'ST',
            'B4',
            'N9', 'N9', 'N9', 'N9',
            'Q2',
            'R4', 'DTM', 'R4', 'DTM', 'R4', 'DTM', 'R4', 'DTM',
            'SE', 'GE', 'IEA',
        ])

    def test_parse_full_document_segment_count(self):
        registry = _make_edi315_registry()
        parser = X12Parser(registry=registry)
        segments = parser.parse(self.FULL_EDI_315).segments

        self.assertEqual(len(segments), 20)

    def test_parse_full_document_to_json(self):
        registry = _make_edi315_registry()
        parser = X12Parser(registry=registry)
        json_output = parser.parse(self.FULL_EDI_315).to_json()

        data = json.loads(json_output)
        self.assertEqual(len(data['segments']), 20)

    def test_parse_b4_from_document(self):
        registry = _make_edi315_registry()
        parser = X12Parser(registry=registry)
        segments = parser.parse(self.FULL_EDI_315).segments

        b4 = segments[3]
        self.assertEqual(b4.segment_id, 'B4')
        b4_dict = b4.to_dict()
        ref_map = {e['reference_designator']: e['value'] for e in b4_dict['elements']}
        self.assertEqual(ref_map['B403'], 'VD')
        self.assertEqual(ref_map['B407'], 'HASU')
        self.assertEqual(ref_map['B408'], '431617')

    def test_parse_n9_segments_from_document(self):
        registry = _make_edi315_registry()
        parser = X12Parser(registry=registry)
        segments = parser.parse(self.FULL_EDI_315).segments

        n9_segments = [s for s in segments if s.segment_id == 'N9']
        self.assertEqual(len(n9_segments), 4)

        qualifiers = [
            s.to_dict()['elements'][0]['value'] for s in n9_segments
        ]
        self.assertEqual(qualifiers, ['BM', 'BN', 'EQ', 'SCA'])

    def test_parse_r4_dtm_pairs_from_document(self):
        registry = _make_edi315_registry()
        parser = X12Parser(registry=registry)
        segments = parser.parse(self.FULL_EDI_315).segments

        r4_segments = [s for s in segments if s.segment_id == 'R4']
        dtm_segments = [s for s in segments if s.segment_id == 'DTM']
        self.assertEqual(len(r4_segments), 4)
        self.assertEqual(len(dtm_segments), 4)

        port_functions = [
            s.to_dict()['elements'][0]['value'] for s in r4_segments
        ]
        self.assertEqual(port_functions, ['R', 'L', 'D', 'E'])

    def test_parse_two_transaction_document(self):
        """Parse the two-transaction document."""
        x12 = (
            'ISA*00*          *00*          *ZZ*GOFREIGHT      *ZZ*PARTNERID      *230207*2022*U*00401*000000001*0*P*^~'
            'GS*QO*GOFREIGHT*PARTNERID*20230207*2022*1*X*004010~'
            'ST*315*0001~'
            'B4***VD*20221217*0000*VNHPH*HASU*431617*L*40HC*VNHPH*UN*0~'
            'N9*BM*BL_NO~'
            'N9*BN*BOOKING_NO~'
            'N9*EQ*HASU4316170~'
            'N9*SCA*SCAC_CODE~'
            'Q2*******0*G*371S***L*CAP SAN MARCO***K~'
            'R4*R*CI*HAIPHONG*HAIPHONG*VN~'
            'DTM*139*20221217*0000*LT~'
            'R4*L*UN*VNHPH*HAIPHONG*VN~'
            'DTM*139*20221217*0000*LT~'
            'R4*D*UN*SGSIN*SINGAPORE*SG~'
            'DTM*139*20221226*0000*LT~'
            'R4*E*UN*SGSIN*SINGAPORE*SG~'
            'DTM*139*20221226*0000*LT~'
            'SE*16*0001~'
            'ST*315*0001~'
            'B4***AE*20221226*0000*SGSIN*TRHU*693609*L*40HC*SGSIN*UN*0~'
            'N9*BM*BL_NO~'
            'N9*EQ*TRHU6936090~'
            'Q2*******0*G********K~'
            'R4*R*UN*SGSIN*SINGAPORE*SG~'
            'DTM*139*20221226*0000*LT~'
            'R4*L*UN*SGSIN*SINGAPORE*SG~'
            'DTM*139*20221226*0000*LT~'
            'SE*10*0001~'
            'GE*2*1~'
            'IEA*1*000000001~'
        )

        registry = _make_edi315_registry()
        parser = X12Parser(registry=registry)
        segments = parser.parse(x12).segments

        counts = {}
        for s in segments:
            counts[s.segment_id] = counts.get(s.segment_id, 0) + 1

        self.assertEqual(counts['ISA'], 1)
        self.assertEqual(counts['GS'], 1)
        self.assertEqual(counts['ST'], 2)
        self.assertEqual(counts['B4'], 2)
        self.assertEqual(counts['N9'], 6)
        self.assertEqual(counts['Q2'], 2)
        self.assertEqual(counts['R4'], 6)
        self.assertEqual(counts['DTM'], 6)
        self.assertEqual(counts['SE'], 2)
        self.assertEqual(counts['GE'], 1)
        self.assertEqual(counts['IEA'], 1)

        self.assertEqual(len(segments), 30)

    def test_headers_only_document(self):
        """Parse envelope-only document (no transactions)."""
        x12 = (
            'ISA*00*          *00*          *ZZ*GOFREIGHT      *ZZ*PARTNERID      *230207*2022*U*00401*000000001*0*P*^~'
            'GS*QO*GOFREIGHT*PARTNERID*20230207*2022*1*X*004010~'
            'GE*0*1~'
            'IEA*1*000000001~'
        )

        registry = _make_edi315_registry()
        parser = X12Parser(registry=registry)
        result = parser.parse(x12).to_dict()

        segment_ids = [s['segment_id'] for s in result['segments']]
        self.assertEqual(segment_ids, ['ISA', 'GS', 'GE', 'IEA'])
