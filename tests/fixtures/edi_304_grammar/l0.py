from pyx12lib.core.grammar import Element
from pyx12lib.core.grammar.segment import USAGE_CONDITIONAL, USAGE_OPTIONAL, BaseSegment


class L0Segment(BaseSegment):
    segment_id = 'L0'
    usage = 'M'
    max_use = 1
    elements = (
        Element(
            reference_designator='L001',
            name='Lading Line Item Number',
            usage=USAGE_OPTIONAL,
            element_type='N0',
            minimum=1,
            maximum=3,
        ),
        Element(
            reference_designator='L004',
            name='Weight',
            usage=USAGE_CONDITIONAL,
            element_type='R',
            minimum=1,
            maximum=10,
        ),
        Element(
            reference_designator='L005',
            name='Weight Qualifier',
            usage=USAGE_CONDITIONAL,
            element_type='ID',
            minimum=1,
            maximum=2,
        ),
        Element(
            reference_designator='L006',
            name='Volume',
            usage=USAGE_CONDITIONAL,
            element_type='R',
            minimum=1,
            maximum=8,
        ),
        Element(
            reference_designator='L007',
            name='Volume Unit Qualifier',
            usage=USAGE_CONDITIONAL,
            element_type='ID',
            minimum=1,
            maximum=1,
        ),
        Element(
            reference_designator='L008',
            name='Lading Quantity',
            usage=USAGE_CONDITIONAL,
            element_type='N0',
            minimum=1,
            maximum=7,
        ),
        Element(
            reference_designator='L009',
            name='Packaging Form Code',
            usage=USAGE_CONDITIONAL,
            element_type='ID',
            minimum=3,
            maximum=3,
        ),
        Element(
            reference_designator='L010',
            name='Dunnage Description',
            usage=USAGE_OPTIONAL,
            element_type='AN',
            minimum=2,
            maximum=25,
        ),
        Element(
            reference_designator='L011',
            name='Weight Unit Code',
            usage=USAGE_OPTIONAL,
            element_type='ID',
            minimum=1,
            maximum=1,
        ),
        Element(
            reference_designator='L014',
            name='Packaging Form Code',
            usage=USAGE_OPTIONAL,
            element_type='ID',
            minimum=3,
            maximum=3,
        ),
    )
