from pyx12lib.core.grammar import Element, NotUsedElement
from pyx12lib.core.grammar.segment import USAGE_MANDATORY, USAGE_OPTIONAL, BaseSegment


class B2Segment(BaseSegment):
    segment_id = 'B2'
    usage = 'M'
    max_use = 1
    elements = (
        Element(
            reference_designator='B201',
            name='Tariff Service Code',
            usage=USAGE_OPTIONAL,
            element_type='ID',
            minimum=2,
            maximum=2,
        ),
        Element(
            reference_designator='B202',
            name='Standard Carrier Alpha Code',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=2,
            maximum=4,
        ),
        NotUsedElement(
            reference_designator='B203',
        ),
        Element(
            reference_designator='B204',
            name='Shipment Identification Number',
            usage=USAGE_MANDATORY,
            element_type='AN',
            minimum=1,
            maximum=30,
        ),
        NotUsedElement(
            reference_designator='B205',
        ),
        Element(
            reference_designator='B206',
            name='Shipment Method of Payment',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=2,
            maximum=2,
        ),
        NotUsedElement(
            reference_designator='B207',
        ),
        Element(
            reference_designator='B208',
            name='Total Equipment',
            usage=USAGE_OPTIONAL,
            element_type='N0',
            minimum=1,
            maximum=3,
        ),
    )
