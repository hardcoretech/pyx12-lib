from pyx12lib.core.grammar import Element, NotUsedElement
from pyx12lib.core.grammar.segment import USAGE_CONDITIONAL, USAGE_MANDATORY, USAGE_OPTIONAL, BaseSegment


class LxSegment(BaseSegment):
    segment_id = 'LX'
    usage = 'O'
    max_use = 1
    elements = (
        Element(
            reference_designator='LX01',
            name='Assigned Number',
            usage=USAGE_MANDATORY,
            element_type='N0',
            minimum=1,
            maximum=6,
        ),
    )


class L0Segment(BaseSegment):
    segment_id = 'L0'
    usage = 'O'
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
        NotUsedElement(reference_designator='L002'),
        NotUsedElement(reference_designator='L003'),
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
        NotUsedElement(reference_designator='L010'),
        Element(
            reference_designator='L011',
            name='Weight Unit Code',
            usage=USAGE_OPTIONAL,
            element_type='ID',
            minimum=1,
            maximum=1,
        ),
        NotUsedElement(reference_designator='L012'),
        NotUsedElement(reference_designator='L013'),
        Element(
            reference_designator='L014',
            name='Packaging Form Code',
            usage=USAGE_OPTIONAL,
            element_type='ID',
            minimum=3,
            maximum=3,
        ),
    )


class L4Segment(BaseSegment):
    segment_id = 'L4'
    usage = 'O'
    max_use = 1
    elements = (
        Element(
            reference_designator='L401',
            name='Length',
            usage=USAGE_MANDATORY,
            element_type='R',
            minimum=1,
            maximum=8,
        ),
        Element(
            reference_designator='L402',
            name='Width',
            usage=USAGE_MANDATORY,
            element_type='R',
            minimum=1,
            maximum=8,
        ),
        Element(
            reference_designator='L403',
            name='Height',
            usage=USAGE_MANDATORY,
            element_type='R',
            minimum=1,
            maximum=8,
        ),
        Element(
            reference_designator='L404',
            name='Measurement Unit Qualifier',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=1,
            maximum=1,
        ),
    )


class L5Segment(BaseSegment):
    segment_id = 'L5'
    usage = 'M'
    max_use = 990
    elements = (
        Element(
            reference_designator='L501',
            name='Lading Line Item Number',
            usage=USAGE_OPTIONAL,
            element_type='N0',
            minimum=1,
            maximum=3,
        ),
        Element(
            reference_designator='L502',
            name='Lading Description',
            usage=USAGE_OPTIONAL,
            element_type='AN',
            minimum=1,
            maximum=50,
        ),
        Element(
            reference_designator='L503',
            name='Commodity Code',
            usage=USAGE_CONDITIONAL,
            element_type='AN',
            minimum=1,
            maximum=30,
        ),
        Element(
            reference_designator='L504',
            name='Commodity Code Qualifier',
            usage=USAGE_CONDITIONAL,
            element_type='ID',
            minimum=1,
            maximum=1,
        ),
        NotUsedElement(reference_designator='L505'),
        Element(
            reference_designator='L506',
            name='Marks and Numbers',
            usage=USAGE_CONDITIONAL,
            element_type='AN',
            minimum=1,
            maximum=48,
        ),
    )
