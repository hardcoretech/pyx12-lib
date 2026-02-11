"""
Validation tests using EDI 304 grammar definitions.

These tests parse actual rendered X12 EDI 304 strings using grammar
definitions copied from a real EDI 304 (Shipping Instruction) implementation
to verify the parser works with production-grade segment definitions.

Grammar source: fms/app/edi/x12/implementations/cargo_smart
Segment types: B2, B2A, K1, L0, L3, PWK, SAC, LX, L4, L5, M0,
               N1, N2, N3, N4, G61, N7, QTY, M7, W09, N9, R2, R4, V1
"""
import json
from unittest import TestCase

from pyx12lib.core.grammar.loop import LoopDefinition
from pyx12lib.core.parsed import ParsedLoop, ParsedSegment
from pyx12lib.core.parser import SegmentParser, X12Parser
from pyx12lib.core.registry import GrammarRegistry, create_default_registry

from tests.fixtures.edi_304_grammar import (
    B2Segment, B2aSegment, K1Segment, L3Segment, PWKSegment, SACSegment,
    LxSegment, L0Segment, L4Segment, L5Segment,
    l0_L0Segment,
    M0Segment,
    N1Segment, N2Segment, N3Segment, N4Segment, G61Segment,
    N7Segment, QtySegment, M7Segment, W09Segment,
    N9Segment, R2Segment, R4Segment, V1Segment,
)


def _make_edi304_registry():
    """Create a registry with all EDI 304 + envelope segments."""
    registry = create_default_registry()
    registry.register(B2Segment)
    registry.register(B2aSegment)
    registry.register(K1Segment)
    registry.register(L3Segment)
    registry.register(PWKSegment)
    registry.register(SACSegment)
    registry.register(LxSegment)
    registry.register(L0Segment)
    registry.register(L4Segment)
    registry.register(L5Segment)
    registry.register(M0Segment)
    registry.register(N1Segment)
    registry.register(N2Segment)
    registry.register(N3Segment)
    registry.register(N4Segment)
    registry.register(G61Segment)
    registry.register(N7Segment)
    registry.register(QtySegment)
    registry.register(M7Segment)
    registry.register(W09Segment)
    registry.register(N9Segment)
    registry.register(R2Segment)
    registry.register(R4Segment)
    registry.register(V1Segment)
    return registry


class TestB2SegmentParsing(TestCase):
    """Parse B2 segments (Beginning of Shipment)."""

    def test_parse_b2_full_data(self):
        x12 = 'B2*YY*HLCU**FILE123456**PP**3~'

        parser = SegmentParser(x12, grammar=B2Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'B2')
        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['B201'], 'YY')
        self.assertEqual(ref_map['B202'], 'HLCU')
        # B203 is NotUsed -> skipped
        self.assertNotIn('B203', ref_map)
        self.assertEqual(ref_map['B204'], 'FILE123456')
        # B205 is NotUsed -> skipped
        self.assertNotIn('B205', ref_map)
        self.assertEqual(ref_map['B206'], 'PP')
        # B207 is NotUsed -> skipped
        self.assertNotIn('B207', ref_map)
        self.assertEqual(ref_map['B208'], '3')

    def test_parse_b2_no_tariff(self):
        x12 = 'B2**HDMU**SI-2024-001**CC**1~'

        parser = SegmentParser(x12, grammar=B2Segment)
        result = parser.to_dict()

        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['B201'], '')
        self.assertEqual(ref_map['B202'], 'HDMU')
        self.assertEqual(ref_map['B204'], 'SI-2024-001')
        self.assertEqual(ref_map['B206'], 'CC')
        self.assertEqual(ref_map['B208'], '1')

    def test_parse_b2_no_equipment_count(self):
        x12 = 'B2**MAEU**MAEU12345**PP~'

        parser = SegmentParser(x12, grammar=B2Segment)
        result = parser.to_dict()

        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['B202'], 'MAEU')
        self.assertEqual(ref_map['B208'], '')

    def test_b2_validation(self):
        x12 = 'B2*YY*HLCU**FILE123456**PP**3~'
        parser = SegmentParser(x12, grammar=B2Segment)
        self.assertTrue(parser.parse().is_valid())


class TestB2aSegmentParsing(TestCase):
    """Parse B2A segments (Transaction Set Purpose Code)."""

    def test_parse_b2a_original(self):
        x12 = 'B2A*00~'

        parser = SegmentParser(x12, grammar=B2aSegment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'B2A')
        self.assertEqual(result['elements'][0]['value'], '00')
        self.assertEqual(result['elements'][0]['reference_designator'], 'B2A01')

    def test_parse_b2a_replacement(self):
        x12 = 'B2A*05~'

        parser = SegmentParser(x12, grammar=B2aSegment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][0]['value'], '05')

    def test_b2a_validation(self):
        x12 = 'B2A*00~'
        parser = SegmentParser(x12, grammar=B2aSegment)
        self.assertTrue(parser.parse().is_valid())


class TestN9SegmentParsing304(TestCase):
    """Parse N9 segments (Reference Identification) for 304."""

    def test_parse_n9_bl_number(self):
        x12 = 'N9*BM*HLCUSHA2209QSEA1~'

        parser = SegmentParser(x12, grammar=N9Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'N9')
        self.assertEqual(result['elements'][0]['value'], 'BM')
        self.assertEqual(result['elements'][1]['value'], 'HLCUSHA2209QSEA1')

    def test_parse_n9_booking(self):
        x12 = 'N9*BN*BKG2024001~'

        parser = SegmentParser(x12, grammar=N9Segment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][0]['value'], 'BN')
        self.assertEqual(result['elements'][1]['value'], 'BKG2024001')

    def test_parse_n9_contract(self):
        x12 = 'N9*CT*CONTRACT-001~'

        parser = SegmentParser(x12, grammar=N9Segment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][0]['value'], 'CT')
        self.assertEqual(result['elements'][1]['value'], 'CONTRACT-001')

    def test_parse_n9_forwarder_ref(self):
        x12 = 'N9*FN*FWD-REF-123~'

        parser = SegmentParser(x12, grammar=N9Segment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][0]['value'], 'FN')

    def test_parse_n9_si_file_number(self):
        x12 = 'N9*SI*FILENO-456~'

        parser = SegmentParser(x12, grammar=N9Segment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][0]['value'], 'SI')
        self.assertEqual(result['elements'][1]['value'], 'FILENO-456')

    def test_parse_n9_itn_number(self):
        x12 = 'N9*TN*X20240101234567~'

        parser = SegmentParser(x12, grammar=N9Segment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][0]['value'], 'TN')

    def test_n9_validation(self):
        x12 = 'N9*BM*HLCUSHA2209QSEA1~'
        parser = SegmentParser(x12, grammar=N9Segment)
        self.assertTrue(parser.parse().is_valid())


class TestV1SegmentParsing(TestCase):
    """Parse V1 segments (Vessel Information)."""

    def test_parse_v1_full_data(self):
        x12 = 'V1*9834276*HYUNDAI FORWARD**0024W*HDMU***L~'

        parser = SegmentParser(x12, grammar=V1Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'V1')
        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['V101'], '9834276')
        self.assertEqual(ref_map['V102'], 'HYUNDAI FORWARD')
        self.assertNotIn('V103', ref_map)
        self.assertEqual(ref_map['V104'], '0024W')
        self.assertEqual(ref_map['V105'], 'HDMU')
        self.assertNotIn('V106', ref_map)
        self.assertNotIn('V107', ref_map)
        self.assertEqual(ref_map['V108'], 'L')

    def test_parse_v1_no_voyage(self):
        x12 = 'V1*9834276*EVER GLORY***EGLV***L~'

        parser = SegmentParser(x12, grammar=V1Segment)
        result = parser.to_dict()

        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['V102'], 'EVER GLORY')
        self.assertEqual(ref_map['V104'], '')
        self.assertEqual(ref_map['V105'], 'EGLV')

    def test_parse_v1_minimal(self):
        x12 = 'V1**MSC AURORA~'

        parser = SegmentParser(x12, grammar=V1Segment)
        result = parser.to_dict()

        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['V101'], '')
        self.assertEqual(ref_map['V102'], 'MSC AURORA')

    def test_v1_validation(self):
        x12 = 'V1*9834276*HYUNDAI FORWARD**0024W*HDMU***L~'
        parser = SegmentParser(x12, grammar=V1Segment)
        self.assertTrue(parser.parse().is_valid())


class TestM0SegmentParsing(TestCase):
    """Parse M0 segments (Letter of Credit)."""

    def test_parse_m0_full(self):
        x12 = 'M0*LC123456789*20231215*20240115~'

        parser = SegmentParser(x12, grammar=M0Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'M0')
        self.assertEqual(result['elements'][0]['value'], 'LC123456789')
        self.assertEqual(result['elements'][1]['value'], '20231215')
        self.assertEqual(result['elements'][2]['value'], '20240115')

    def test_parse_m0_no_dates(self):
        x12 = 'M0*LC999~'

        parser = SegmentParser(x12, grammar=M0Segment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][0]['value'], 'LC999')
        self.assertEqual(result['elements'][1]['value'], '')
        self.assertEqual(result['elements'][2]['value'], '')

    def test_m0_validation(self):
        x12 = 'M0*LC123456789*20231215*20240115~'
        parser = SegmentParser(x12, grammar=M0Segment)
        self.assertTrue(parser.parse().is_valid())


class TestN1LoopSegmentsParsing(TestCase):
    """Parse N1, N2, N3, N4, G61 segments (Trade Partner Loop)."""

    def test_parse_n1_shipper(self):
        x12 = 'N1*SH*ACME TRADING CO*25*123456789~'

        parser = SegmentParser(x12, grammar=N1Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'N1')
        self.assertEqual(result['elements'][0]['value'], 'SH')
        self.assertEqual(result['elements'][1]['value'], 'ACME TRADING CO')
        self.assertEqual(result['elements'][2]['value'], '25')
        self.assertEqual(result['elements'][3]['value'], '123456789')

    def test_parse_n1_consignee(self):
        x12 = 'N1*CN*BUYER CORP~'

        parser = SegmentParser(x12, grammar=N1Segment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][0]['value'], 'CN')
        self.assertEqual(result['elements'][1]['value'], 'BUYER CORP')
        self.assertEqual(result['elements'][2]['value'], '')
        self.assertEqual(result['elements'][3]['value'], '')

    def test_parse_n1_carrier(self):
        x12 = 'N1*CA*HAPAG LLOYD~'

        parser = SegmentParser(x12, grammar=N1Segment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][0]['value'], 'CA')

    def test_parse_n2_additional_name(self):
        x12 = 'N2*ADDITIONAL NAME LINE 1*LINE 2~'

        parser = SegmentParser(x12, grammar=N2Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'N2')
        self.assertEqual(result['elements'][0]['value'], 'ADDITIONAL NAME LINE 1')
        self.assertEqual(result['elements'][1]['value'], 'LINE 2')

    def test_parse_n3_address(self):
        x12 = 'N3*123 MAIN STREET*SUITE 100~'

        parser = SegmentParser(x12, grammar=N3Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'N3')
        self.assertEqual(result['elements'][0]['value'], '123 MAIN STREET')
        self.assertEqual(result['elements'][1]['value'], 'SUITE 100')

    def test_parse_n4_full_location(self):
        x12 = 'N4*SHANGHAI*SH*200000*CN~'

        parser = SegmentParser(x12, grammar=N4Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'N4')
        self.assertEqual(result['elements'][0]['value'], 'SHANGHAI')
        self.assertEqual(result['elements'][1]['value'], 'SH')
        self.assertEqual(result['elements'][2]['value'], '200000')
        self.assertEqual(result['elements'][3]['value'], 'CN')

    def test_parse_n4_with_location_qualifier(self):
        x12 = 'N4*LOS ANGELES*CA*90001*US*UN*USLAX~'

        parser = SegmentParser(x12, grammar=N4Segment)
        result = parser.to_dict()

        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['N405'], 'UN')
        self.assertEqual(ref_map['N406'], 'USLAX')

    def test_parse_g61_contact(self):
        x12 = 'G61*IC*JOHN DOE*TE*+86-21-12345678~'

        parser = SegmentParser(x12, grammar=G61Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'G61')
        self.assertEqual(result['elements'][0]['value'], 'IC')
        self.assertEqual(result['elements'][1]['value'], 'JOHN DOE')
        self.assertEqual(result['elements'][2]['value'], 'TE')
        self.assertEqual(result['elements'][3]['value'], '+86-21-12345678')

    def test_n1_validation(self):
        x12 = 'N1*SH*ACME TRADING CO*25*123456789~'
        parser = SegmentParser(x12, grammar=N1Segment)
        self.assertTrue(parser.parse().is_valid())

    def test_g61_validation(self):
        x12 = 'G61*IC*JOHN DOE*TE*+86-21-12345678~'
        parser = SegmentParser(x12, grammar=G61Segment)
        self.assertTrue(parser.parse().is_valid())


class TestR4SegmentParsing304(TestCase):
    """Parse R4 segments (Port or Terminal) for 304."""

    def test_parse_r4_port_of_receipt(self):
        x12 = 'R4*R*UN*CNSHA*SHANGHAI*CN~'

        parser = SegmentParser(x12, grammar=R4Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'R4')
        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['R401'], 'R')
        self.assertEqual(ref_map['R402'], 'UN')
        self.assertEqual(ref_map['R403'], 'CNSHA')
        self.assertEqual(ref_map['R404'], 'SHANGHAI')
        self.assertEqual(ref_map['R405'], 'CN')
        self.assertNotIn('R406', ref_map)
        self.assertNotIn('R407', ref_map)

    def test_parse_r4_port_of_loading(self):
        x12 = 'R4*L*UN*CNSHA*SHANGHAI*CN~'

        parser = SegmentParser(x12, grammar=R4Segment)
        result = parser.to_dict()

        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['R401'], 'L')

    def test_parse_r4_port_of_discharge(self):
        x12 = 'R4*D*UN*USLAX*LOS ANGELES*US***CA~'

        parser = SegmentParser(x12, grammar=R4Segment)
        result = parser.to_dict()

        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['R401'], 'D')
        self.assertEqual(ref_map['R403'], 'USLAX')
        self.assertEqual(ref_map['R404'], 'LOS ANGELES')
        self.assertEqual(ref_map['R408'], 'CA')

    def test_parse_r4_delivery(self):
        x12 = 'R4*E*UN*USLAX*LOS ANGELES*US~'

        parser = SegmentParser(x12, grammar=R4Segment)
        result = parser.to_dict()

        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['R401'], 'E')

    def test_parse_r4_bl_release_office(self):
        x12 = 'R4*K*UN*CNSHA*SHANGHAI*CN~'

        parser = SegmentParser(x12, grammar=R4Segment)
        result = parser.to_dict()

        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['R401'], 'K')

    def test_r4_validation(self):
        x12 = 'R4*R*UN*CNSHA*SHANGHAI*CN~'
        parser = SegmentParser(x12, grammar=R4Segment)
        self.assertTrue(parser.parse().is_valid())


class TestR2SegmentParsing(TestCase):
    """Parse R2 segments (Route Information) with many NotUsed."""

    def test_parse_r2_full(self):
        x12 = 'R2*HDMU*B**********CY~'

        parser = SegmentParser(x12, grammar=R2Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'R2')
        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['R201'], 'HDMU')
        self.assertEqual(ref_map['R202'], 'B')
        # R203-R211 are NotUsed -> skipped
        for i in range(3, 12):
            self.assertNotIn('R2%02d' % i, ref_map)
        self.assertEqual(ref_map['R212'], 'CY')

    def test_parse_r2_no_service_type(self):
        x12 = 'R2*MAEU*B~'

        parser = SegmentParser(x12, grammar=R2Segment)
        result = parser.to_dict()

        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['R201'], 'MAEU')
        self.assertEqual(ref_map['R202'], 'B')
        self.assertEqual(ref_map['R212'], '')

    def test_r2_validation(self):
        x12 = 'R2*HDMU*B**********CY~'
        parser = SegmentParser(x12, grammar=R2Segment)
        self.assertTrue(parser.parse().is_valid())


class TestN7SegmentParsing(TestCase):
    """Parse N7 segments (Equipment Details) with many NotUsed."""

    def test_parse_n7_full_container(self):
        x12 = 'N7*HLCU*3456789*15000*G*4200***28*E*S*******K*7****22GP~'

        parser = SegmentParser(x12, grammar=N7Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'N7')
        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['N701'], 'HLCU')
        self.assertEqual(ref_map['N702'], '3456789')
        self.assertEqual(ref_map['N703'], '15000')
        self.assertEqual(ref_map['N704'], 'G')
        self.assertEqual(ref_map['N705'], '4200')
        self.assertNotIn('N706', ref_map)
        self.assertNotIn('N707', ref_map)
        self.assertEqual(ref_map['N708'], '28')
        self.assertEqual(ref_map['N709'], 'E')
        self.assertEqual(ref_map['N710'], 'S')
        for i in range(11, 17):
            self.assertNotIn('N7%d' % i, ref_map)
        self.assertEqual(ref_map['N717'], 'K')
        self.assertEqual(ref_map['N718'], '7')
        self.assertNotIn('N719', ref_map)
        self.assertNotIn('N720', ref_map)
        self.assertNotIn('N721', ref_map)
        self.assertEqual(ref_map['N722'], '22GP')

    def test_parse_n7_minimal(self):
        x12 = 'N7**1234567~'

        parser = SegmentParser(x12, grammar=N7Segment)
        result = parser.to_dict()

        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['N701'], '')
        self.assertEqual(ref_map['N702'], '1234567')

    def test_n7_validation(self):
        x12 = 'N7*HLCU*3456789*15000*G*4200***28*E*S*******K*7****22GP~'
        parser = SegmentParser(x12, grammar=N7Segment)
        self.assertTrue(parser.parse().is_valid())


class TestQtySegmentParsing(TestCase):
    """Parse QTY segments (Quantity)."""

    def test_parse_qty(self):
        x12 = 'QTY*38*100~'

        parser = SegmentParser(x12, grammar=QtySegment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'QTY')
        self.assertEqual(result['elements'][0]['value'], '38')
        self.assertEqual(result['elements'][1]['value'], '100')

    def test_qty_validation(self):
        x12 = 'QTY*38*100~'
        parser = SegmentParser(x12, grammar=QtySegment)
        self.assertTrue(parser.parse().is_valid())


class TestM7SegmentParsing(TestCase):
    """Parse M7 segments (Seal Information)."""

    def test_parse_m7_full(self):
        x12 = 'M7*SEAL001*SEAL002*SEAL003**CA~'

        parser = SegmentParser(x12, grammar=M7Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'M7')
        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['M701'], 'SEAL001')
        self.assertEqual(ref_map['M702'], 'SEAL002')
        self.assertEqual(ref_map['M703'], 'SEAL003')
        self.assertNotIn('M704', ref_map)
        self.assertEqual(ref_map['M705'], 'CA')

    def test_parse_m7_single_seal(self):
        x12 = 'M7*SL12345~'

        parser = SegmentParser(x12, grammar=M7Segment)
        result = parser.to_dict()

        self.assertEqual(result['elements'][0]['value'], 'SL12345')

    def test_m7_validation(self):
        x12 = 'M7*SEAL001*SEAL002*SEAL003**CA~'
        parser = SegmentParser(x12, grammar=M7Segment)
        self.assertTrue(parser.parse().is_valid())


class TestW09SegmentParsing(TestCase):
    """Parse W09 segments (Equipment Characteristics)."""

    def test_parse_w09_reefer(self):
        x12 = 'W09*RC*-18*FA**CE*FROZEN GOODS***500~'

        parser = SegmentParser(x12, grammar=W09Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'W09')
        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['W0901'], 'RC')
        self.assertEqual(ref_map['W0902'], '-18')
        self.assertEqual(ref_map['W0903'], 'FA')
        self.assertNotIn('W0904', ref_map)
        self.assertEqual(ref_map['W0905'], 'CE')
        self.assertEqual(ref_map['W0906'], 'FROZEN GOODS')
        self.assertNotIn('W0907', ref_map)
        self.assertNotIn('W0908', ref_map)
        self.assertEqual(ref_map['W0909'], '500')

    def test_parse_w09_dry(self):
        x12 = 'W09*CN~'

        parser = SegmentParser(x12, grammar=W09Segment)
        result = parser.to_dict()

        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['W0901'], 'CN')

    def test_w09_validation(self):
        x12 = 'W09*RC*-18*FA**CE*FROZEN GOODS***500~'
        parser = SegmentParser(x12, grammar=W09Segment)
        self.assertTrue(parser.parse().is_valid())


class TestLxLoopSegmentsParsing(TestCase):
    """Parse LX, L0 (lx variant), L4, L5 segments."""

    def test_parse_lx(self):
        x12 = 'LX*1~'

        parser = SegmentParser(x12, grammar=LxSegment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'LX')
        self.assertEqual(result['elements'][0]['value'], '1')

    def test_parse_l0_lx_variant(self):
        """L0 from lx.py context (with NotUsed positions)."""
        x12 = 'L0*1***5000*G*28*E*100*CTN**K***PLT~'

        parser = SegmentParser(x12, grammar=L0Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'L0')
        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['L001'], '1')
        self.assertNotIn('L002', ref_map)
        self.assertNotIn('L003', ref_map)
        self.assertEqual(ref_map['L004'], '5000')
        self.assertEqual(ref_map['L005'], 'G')
        self.assertEqual(ref_map['L006'], '28')
        self.assertEqual(ref_map['L007'], 'E')
        self.assertEqual(ref_map['L008'], '100')
        self.assertEqual(ref_map['L009'], 'CTN')
        self.assertNotIn('L010', ref_map)
        self.assertEqual(ref_map['L011'], 'K')
        self.assertNotIn('L012', ref_map)
        self.assertNotIn('L013', ref_map)
        self.assertEqual(ref_map['L014'], 'PLT')

    def test_parse_l0_standalone_variant(self):
        """L0 from l0.py (no NotUsed, sequential elements)."""
        x12 = 'L0*1*5000*G*28*E*100*CTN**K*PLT~'

        parser = SegmentParser(x12, grammar=l0_L0Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'L0')
        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['L001'], '1')
        self.assertEqual(ref_map['L004'], '5000')
        self.assertEqual(ref_map['L005'], 'G')
        self.assertEqual(ref_map['L006'], '28')
        self.assertEqual(ref_map['L007'], 'E')
        self.assertEqual(ref_map['L008'], '100')
        self.assertEqual(ref_map['L009'], 'CTN')
        self.assertEqual(ref_map['L010'], '')
        self.assertEqual(ref_map['L011'], 'K')
        self.assertEqual(ref_map['L014'], 'PLT')

    def test_parse_l4_measurement(self):
        x12 = 'L4*120*240*260*E~'

        parser = SegmentParser(x12, grammar=L4Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'L4')
        self.assertEqual(result['elements'][0]['value'], '120')
        self.assertEqual(result['elements'][1]['value'], '240')
        self.assertEqual(result['elements'][2]['value'], '260')
        self.assertEqual(result['elements'][3]['value'], 'E')

    def test_parse_l5_full(self):
        x12 = 'L5*1*ELECTRONIC GOODS*8471300000*T**MARK123~'

        parser = SegmentParser(x12, grammar=L5Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'L5')
        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['L501'], '1')
        self.assertEqual(ref_map['L502'], 'ELECTRONIC GOODS')
        self.assertEqual(ref_map['L503'], '8471300000')
        self.assertEqual(ref_map['L504'], 'T')
        self.assertNotIn('L505', ref_map)
        self.assertEqual(ref_map['L506'], 'MARK123')

    def test_parse_l5_no_hts(self):
        x12 = 'L5*1*GARMENTS~'

        parser = SegmentParser(x12, grammar=L5Segment)
        result = parser.to_dict()

        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['L502'], 'GARMENTS')
        self.assertEqual(ref_map['L503'], '')

    def test_l0_validation(self):
        x12 = 'L0*1***5000*G*28*E*100*CTN**K***PLT~'
        parser = SegmentParser(x12, grammar=L0Segment)
        self.assertTrue(parser.parse().is_valid())

    def test_l5_validation(self):
        x12 = 'L5*1*ELECTRONIC GOODS*8471300000*T**MARK123~'
        parser = SegmentParser(x12, grammar=L5Segment)
        self.assertTrue(parser.parse().is_valid())


class TestL3LoopSegmentsParsing(TestCase):
    """Parse L3, PWK, SAC segments (Total / Paperwork / Charges)."""

    def test_parse_l3_totals(self):
        x12 = 'L3*25000*G*******150*E*100*K~'

        parser = SegmentParser(x12, grammar=L3Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'L3')
        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['L301'], '25000')
        self.assertEqual(ref_map['L302'], 'G')
        # L303-L308 are NotUsed -> skipped
        for i in range(3, 9):
            self.assertNotIn('L3%02d' % i, ref_map)
        self.assertEqual(ref_map['L309'], '150')
        self.assertEqual(ref_map['L310'], 'E')
        self.assertEqual(ref_map['L311'], '100')
        self.assertEqual(ref_map['L312'], 'K')

    def test_parse_pwk_paperwork(self):
        x12 = 'PWK*BL*FX*3****ORIGINAL BILL OF LADING~'

        parser = SegmentParser(x12, grammar=PWKSegment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'PWK')
        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['PWK01'], 'BL')
        self.assertEqual(ref_map['PWK02'], 'FX')
        self.assertEqual(ref_map['PWK03'], '3')
        self.assertNotIn('PWK04', ref_map)
        self.assertNotIn('PWK05', ref_map)
        self.assertNotIn('PWK06', ref_map)
        self.assertEqual(ref_map['PWK07'], 'ORIGINAL BILL OF LADING')

    def test_parse_sac_charges(self):
        x12 = 'SAC*C*D240**********06~'

        parser = SegmentParser(x12, grammar=SACSegment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'SAC')
        ref_map = {e['reference_designator']: e['value'] for e in result['elements']}
        self.assertEqual(ref_map['SAC01'], 'C')
        self.assertEqual(ref_map['SAC02'], 'D240')
        # SAC03-SAC11 are NotUsed -> skipped
        for i in range(3, 12):
            self.assertNotIn('SAC%02d' % i, ref_map)
        self.assertEqual(ref_map['SAC12'], '06')

    def test_parse_k1_remarks(self):
        x12 = 'K1*HANDLE WITH CARE*FRAGILE~'

        parser = SegmentParser(x12, grammar=K1Segment)
        result = parser.to_dict()

        self.assertEqual(result['segment_id'], 'K1')
        self.assertEqual(result['elements'][0]['value'], 'HANDLE WITH CARE')
        self.assertEqual(result['elements'][1]['value'], 'FRAGILE')

    def test_l3_validation(self):
        x12 = 'L3*25000*G*******150*E*100*K~'
        parser = SegmentParser(x12, grammar=L3Segment)
        self.assertTrue(parser.parse().is_valid())

    def test_sac_validation(self):
        x12 = 'SAC*C*D240**********06~'
        parser = SegmentParser(x12, grammar=SACSegment)
        self.assertTrue(parser.parse().is_valid())


class TestFullEdi304DocumentParsing(TestCase):
    """Parse a complete EDI 304 document using X12Parser with all grammars."""

    FULL_EDI_304 = (
        'ISA*00*          *00*          *ZZ*GOFREIGHT      *ZZ*CARGOSMART     *240115*1030*U*00401*000000001*0*P*^~'
        'GS*SO*GOFREIGHT*CARGOSMART*20240115*1030*1*X*004010~'
        'ST*304*0001~'
        'B2**HDMU**SI-2024-001**PP**2~'
        'B2A*00~'
        'N9*BM*HDMUSHA2401QSEA1~'
        'N9*BN*BKG2024001~'
        'N9*CT*CONTRACT-001~'
        'N9*SI*FILENO-456~'
        'V1*9834276*HYUNDAI FORWARD**0024W*HDMU***L~'
        'N1*SH*ACME TRADING CO*25*123456789~'
        'N3*123 MAIN STREET*SUITE 100~'
        'N4*SHANGHAI*SH*200000*CN~'
        'G61*IC*JOHN DOE*TE*+86-21-12345678~'
        'N1*CN*BUYER CORP~'
        'N3*456 HARBOR DRIVE~'
        'N4*LOS ANGELES*CA*90001*US~'
        'N1*CA*HAPAG LLOYD~'
        'N1*FW*GOFREIGHT INC~'
        'R4*R*UN*CNSHA*SHANGHAI*CN~'
        'R4*L*UN*CNSHA*SHANGHAI*CN~'
        'R4*D*UN*USLAX*LOS ANGELES*US~'
        'R4*E*UN*USLAX*LOS ANGELES*US~'
        'R2*HDMU*B**********CY~'
        'LX*1~'
        'N7*HLCU*3456789*15000*G*4200***28*E*S*******K*7****22GP~'
        'QTY*38*100~'
        'M7*SEAL001**~'
        'L5*1*ELECTRONIC GOODS*8471300000*T**MARK123~'
        'LX*2~'
        'N7*HDMU*7654321*18000*G*4500***33*E*S*******K*1****40HC~'
        'QTY*38*200~'
        'M7*SEAL002~'
        'L5*2*GARMENTS~'
        'L3*33000*G*******61*E*300*K~'
        'K1*HANDLE WITH CARE~'
        'SE*36*0001~'
        'GE*1*1~'
        'IEA*1*000000001~'
    )

    def test_parse_full_document(self):
        registry = _make_edi304_registry()
        parser = X12Parser(self.FULL_EDI_304, registry=registry)
        result = parser.to_dict()

        segment_ids = [s['segment_id'] for s in result['segments']]
        self.assertEqual(segment_ids, [
            'ISA', 'GS', 'ST',
            'B2', 'B2A',
            'N9', 'N9', 'N9', 'N9',
            'V1',
            'N1', 'N3', 'N4', 'G61',
            'N1', 'N3', 'N4',
            'N1', 'N1',
            'R4', 'R4', 'R4', 'R4',
            'R2',
            'LX', 'N7', 'QTY', 'M7', 'L5',
            'LX', 'N7', 'QTY', 'M7', 'L5',
            'L3', 'K1',
            'SE', 'GE', 'IEA',
        ])

    def test_parse_full_document_segment_count(self):
        registry = _make_edi304_registry()
        parser = X12Parser(self.FULL_EDI_304, registry=registry)
        segments = parser.parse()

        self.assertEqual(len(segments), 39)

    def test_parse_full_document_to_json(self):
        registry = _make_edi304_registry()
        parser = X12Parser(self.FULL_EDI_304, registry=registry)
        json_output = parser.to_json()

        data = json.loads(json_output)
        self.assertEqual(len(data['segments']), 39)

    def test_parse_b2_from_document(self):
        registry = _make_edi304_registry()
        parser = X12Parser(self.FULL_EDI_304, registry=registry)
        segments = parser.parse()

        b2 = segments[3]
        self.assertEqual(b2.segment_id, 'B2')
        ref_map = {e['reference_designator']: e['value'] for e in b2.to_dict()['elements']}
        self.assertEqual(ref_map['B202'], 'HDMU')
        self.assertEqual(ref_map['B204'], 'SI-2024-001')
        self.assertEqual(ref_map['B206'], 'PP')
        self.assertEqual(ref_map['B208'], '2')

    def test_parse_v1_from_document(self):
        registry = _make_edi304_registry()
        parser = X12Parser(self.FULL_EDI_304, registry=registry)
        segments = parser.parse()

        v1 = [s for s in segments if s.segment_id == 'V1'][0]
        ref_map = {e['reference_designator']: e['value'] for e in v1.to_dict()['elements']}
        self.assertEqual(ref_map['V101'], '9834276')
        self.assertEqual(ref_map['V102'], 'HYUNDAI FORWARD')
        self.assertEqual(ref_map['V104'], '0024W')
        self.assertEqual(ref_map['V105'], 'HDMU')
        self.assertEqual(ref_map['V108'], 'L')

    def test_parse_n9_segments_from_document(self):
        registry = _make_edi304_registry()
        parser = X12Parser(self.FULL_EDI_304, registry=registry)
        segments = parser.parse()

        n9_segments = [s for s in segments if s.segment_id == 'N9']
        self.assertEqual(len(n9_segments), 4)

        qualifiers = [
            s.to_dict()['elements'][0]['value'] for s in n9_segments
        ]
        self.assertEqual(qualifiers, ['BM', 'BN', 'CT', 'SI'])

    def test_parse_n1_segments_from_document(self):
        registry = _make_edi304_registry()
        parser = X12Parser(self.FULL_EDI_304, registry=registry)
        segments = parser.parse()

        n1_segments = [s for s in segments if s.segment_id == 'N1']
        self.assertEqual(len(n1_segments), 4)

        entity_codes = [
            s.to_dict()['elements'][0]['value'] for s in n1_segments
        ]
        self.assertEqual(entity_codes, ['SH', 'CN', 'CA', 'FW'])

    def test_parse_r4_ports_from_document(self):
        registry = _make_edi304_registry()
        parser = X12Parser(self.FULL_EDI_304, registry=registry)
        segments = parser.parse()

        r4_segments = [s for s in segments if s.segment_id == 'R4']
        self.assertEqual(len(r4_segments), 4)

        port_functions = [
            s.to_dict()['elements'][0]['value'] for s in r4_segments
        ]
        self.assertEqual(port_functions, ['R', 'L', 'D', 'E'])

    def test_parse_lx_containers_from_document(self):
        registry = _make_edi304_registry()
        parser = X12Parser(self.FULL_EDI_304, registry=registry)
        segments = parser.parse()

        lx_segments = [s for s in segments if s.segment_id == 'LX']
        self.assertEqual(len(lx_segments), 2)
        self.assertEqual(lx_segments[0].to_dict()['elements'][0]['value'], '1')
        self.assertEqual(lx_segments[1].to_dict()['elements'][0]['value'], '2')

    def test_parse_n7_equipment_from_document(self):
        registry = _make_edi304_registry()
        parser = X12Parser(self.FULL_EDI_304, registry=registry)
        segments = parser.parse()

        n7_segments = [s for s in segments if s.segment_id == 'N7']
        self.assertEqual(len(n7_segments), 2)

        first_n7 = n7_segments[0].to_dict()
        ref_map = {e['reference_designator']: e['value'] for e in first_n7['elements']}
        self.assertEqual(ref_map['N701'], 'HLCU')
        self.assertEqual(ref_map['N702'], '3456789')
        self.assertEqual(ref_map['N722'], '22GP')

        second_n7 = n7_segments[1].to_dict()
        ref_map2 = {e['reference_designator']: e['value'] for e in second_n7['elements']}
        self.assertEqual(ref_map2['N701'], 'HDMU')
        self.assertEqual(ref_map2['N722'], '40HC')

    def test_parse_l3_totals_from_document(self):
        registry = _make_edi304_registry()
        parser = X12Parser(self.FULL_EDI_304, registry=registry)
        segments = parser.parse()

        l3 = [s for s in segments if s.segment_id == 'L3'][0]
        ref_map = {e['reference_designator']: e['value'] for e in l3.to_dict()['elements']}
        self.assertEqual(ref_map['L301'], '33000')
        self.assertEqual(ref_map['L302'], 'G')
        self.assertEqual(ref_map['L309'], '61')
        self.assertEqual(ref_map['L310'], 'E')
        self.assertEqual(ref_map['L311'], '300')
        self.assertEqual(ref_map['L312'], 'K')

    def test_document_all_segments_valid(self):
        registry = _make_edi304_registry()
        parser = X12Parser(self.FULL_EDI_304, registry=registry)
        segments = parser.parse()

        for seg in segments:
            self.assertTrue(
                seg.is_valid(),
                msg='Segment {} is not valid'.format(seg.segment_id),
            )


def _make_edi304_loop_registry():
    """Create a registry with EDI 304 segments and loop definitions."""
    registry = create_default_registry()
    registry.register_all([
        B2Segment, B2aSegment, N9Segment, V1Segment,
        R4Segment, R2Segment, L3Segment, PWKSegment,
    ])
    registry.register_loop(
        LoopDefinition(N1Segment, [N2Segment, N3Segment, N4Segment, G61Segment])
    )
    registry.register_loop(
        LoopDefinition(LxSegment, [N7Segment, QtySegment, M7Segment, L0Segment, L5Segment])
    )
    return registry


class TestFullEdi304LoopParsing(TestCase):
    """Parse an EDI 304 document with loop definitions applied.

    Uses a different X12 string from TestFullEdi304DocumentParsing to
    provide complementary coverage — N1 with N2 children, single LX
    with multiple containers, PWK segments instead of K1.
    """

    FULL_EDI_304_WITH_LOOPS = (
        'ISA*00*          *00*          *ZZ*GOFREIGHT      *ZZ*CARGOSMART     *240115*1030*^*00401*000000001*0*P*^~'
        'GS*SO*CARGOSMART*GOFREIGHT*20240115*1030*1*X*004010~'
        'ST*304*123456789~'
        'B2*PP*EGLV**OE-25120002**MX**2~'
        'B2A*00~'
        'N9*BM*123324~'
        'N9*BN*12334~'
        'N9*CT*QWER~'
        'N9*SI*OE-25120002~'
        'N9*TN*12345~'
        'V1**PACIFIC VOYAGER**1234*EGLV~'
        'N1*CA*EGLV~'
        'N1*SH*ACME EXPORTS INC~'
        'N1*CN*TERMINAL WEST PORT~'
        'N2*100 DOCK STREET~'
        'N2*PORTSIDE 100 BC CA~'
        'N1*FW*TERMINAL WEST PORT~'
        'N2*100 DOCK STREET~'
        'N2*PORTSIDE 100 BC CA~'
        'N1*SI*ACME EXPORTS INC*25*12345~'
        'G61*IC*JANE SMITH*EM*contact@acme-exports.test~'
        'R4*R*UN*US2AA~'
        'R4*D*UN*US267~'
        'R4*L*UN*US267~'
        'R4*E*UN*US2AA~'
        'R4*W*UN*US267~'
        'R2*EGLV*O**********02~'
        'LX*000001~'
        'N7**12*1*G*4200***22*E*S*******K*7****22G0~'
        'QTY*39*100~'
        'M7*12321*1231***SH~'
        'N7**2234*100*G*4200***22*E*S*******K*7****22G0~'
        'QTY*39*100~'
        'M7*32123*12345***SH~'
        'L0*001***101*G*100*X*200*CTN**K~'
        'L5*001*TEST DESC****TEST MARK~'
        'L3*101*G*******100*X*200*K~'
        'PWK*BC*EI*5~'
        'PWK*BL*EI*3~'
        'SE*38*123456789~'
        'GE*1*123456789~'
        'IEA*1*000000001~'
    )

    def setUp(self):
        self.registry = _make_edi304_loop_registry()
        self.parser = X12Parser(self.FULL_EDI_304_WITH_LOOPS, registry=self.registry)
        self.result = self.parser.parse()

    def test_loop_parse_top_level_item_count(self):
        # ISA, GS, ST, B2, B2A, 5x N9, V1 = 11 flat
        # 5x N1 loops = 5 loops
        # 5x R4, R2 = 6 flat
        # 1x LX loop = 1 loop
        # L3, 2x PWK, SE, GE, IEA = 6 flat
        # Total = 11 + 5 + 6 + 1 + 6 = 29
        self.assertEqual(len(self.result), 29)

    def test_loop_parse_n1_loop_count(self):
        n1_loops = [item for item in self.result if isinstance(item, ParsedLoop) and item.loop_id == 'N1']
        self.assertEqual(len(n1_loops), 5)

    def test_loop_n1_ca_has_no_children(self):
        n1_loops = [item for item in self.result if isinstance(item, ParsedLoop) and item.loop_id == 'N1']
        ca_loop = n1_loops[0]
        self.assertEqual(len(ca_loop.segments), 1)
        self.assertEqual(ca_loop.segments[0].segment_id, 'N1')

    def test_loop_n1_cn_has_two_n2(self):
        n1_loops = [item for item in self.result if isinstance(item, ParsedLoop) and item.loop_id == 'N1']
        cn_loop = n1_loops[2]  # CA, SH, CN
        self.assertEqual(len(cn_loop.segments), 3)
        self.assertEqual(cn_loop.segments[0].segment_id, 'N1')
        self.assertEqual(cn_loop.segments[1].segment_id, 'N2')
        self.assertEqual(cn_loop.segments[2].segment_id, 'N2')

    def test_loop_n1_si_has_g61(self):
        n1_loops = [item for item in self.result if isinstance(item, ParsedLoop) and item.loop_id == 'N1']
        si_loop = n1_loops[4]  # CA, SH, CN, FW, SI
        self.assertEqual(len(si_loop.segments), 2)
        self.assertEqual(si_loop.segments[0].segment_id, 'N1')
        self.assertEqual(si_loop.segments[1].segment_id, 'G61')

    def test_loop_n1_entity_codes(self):
        n1_loops = [item for item in self.result if isinstance(item, ParsedLoop) and item.loop_id == 'N1']
        entity_codes = []
        for loop in n1_loops:
            n1_seg = loop.segments[0]
            code = n1_seg.to_dict()['elements'][0]['value']
            entity_codes.append(code)
        self.assertEqual(entity_codes, ['CA', 'SH', 'CN', 'FW', 'SI'])

    def test_loop_lx_count(self):
        lx_loops = [item for item in self.result if isinstance(item, ParsedLoop) and item.loop_id == 'LX']
        self.assertEqual(len(lx_loops), 1)

    def test_loop_lx_contains_all_children(self):
        lx_loops = [item for item in self.result if isinstance(item, ParsedLoop) and item.loop_id == 'LX']
        lx_loop = lx_loops[0]
        self.assertEqual(len(lx_loop.segments), 9)
        seg_ids = [s.segment_id for s in lx_loop.segments]
        self.assertEqual(seg_ids, ['LX', 'N7', 'QTY', 'M7', 'N7', 'QTY', 'M7', 'L0', 'L5'])

    def test_loop_lx_two_containers(self):
        lx_loops = [item for item in self.result if isinstance(item, ParsedLoop) and item.loop_id == 'LX']
        lx_loop = lx_loops[0]
        n7_segments = [s for s in lx_loop.segments if s.segment_id == 'N7']
        self.assertEqual(len(n7_segments), 2)

    def test_r4_segments_are_flat(self):
        r4_items = [item for item in self.result if isinstance(item, ParsedSegment) and item.segment_id == 'R4']
        self.assertEqual(len(r4_items), 5)

    def test_l3_after_lx_loop_is_flat(self):
        l3_items = [item for item in self.result if isinstance(item, ParsedSegment) and item.segment_id == 'L3']
        self.assertEqual(len(l3_items), 1)

    def test_pwk_after_l3_are_flat(self):
        pwk_items = [item for item in self.result if isinstance(item, ParsedSegment) and item.segment_id == 'PWK']
        self.assertEqual(len(pwk_items), 2)

    def test_n9_segments_before_loops_are_flat(self):
        n9_items = [item for item in self.result if isinstance(item, ParsedSegment) and item.segment_id == 'N9']
        self.assertEqual(len(n9_items), 5)

    def test_envelope_segments_unaffected(self):
        envelope_ids = ['ISA', 'GS', 'ST', 'SE', 'GE', 'IEA']
        for env_id in envelope_ids:
            matches = [item for item in self.result if isinstance(item, ParsedSegment) and item.segment_id == env_id]
            self.assertEqual(len(matches), 1, msg='Expected 1 {} segment, got {}'.format(env_id, len(matches)))

    def test_to_dict_loop_items_have_loop_id(self):
        result_dict = self.parser.to_dict()
        loop_items = [item for item in result_dict['segments'] if 'loop_id' in item]
        self.assertEqual(len(loop_items), 6)  # 5 N1 + 1 LX

    def test_to_dict_flat_items_have_segment_id(self):
        result_dict = self.parser.to_dict()
        flat_items = [item for item in result_dict['segments'] if 'segment_id' in item]
        self.assertEqual(len(flat_items), 23)  # 29 total - 6 loops

    def test_to_json_round_trip(self):
        json_output = self.parser.to_json()
        data = json.loads(json_output)
        self.assertIn('segments', data)
        self.assertEqual(len(data['segments']), 29)
