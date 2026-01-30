from pyx12lib.core.grammar import Element, NotUsedElement
from pyx12lib.core.grammar.segment import USAGE_CONDITIONAL, USAGE_MANDATORY, USAGE_OPTIONAL, BaseSegment


class N7Segment(BaseSegment):
    segment_id = 'N7'
    usage = 'O'
    max_use = 1
    elements = (
        Element(
            reference_designator='N701',
            name='Equipment Initial',
            usage=USAGE_OPTIONAL,
            element_type='AN',
            minimum=1,
            maximum=4,
        ),
        Element(
            reference_designator='N702',
            name='Equipment Number',
            usage=USAGE_MANDATORY,
            element_type='AN',
            minimum=1,
            maximum=10,
        ),
        Element(
            reference_designator='N703',
            name='Weight',
            usage=USAGE_CONDITIONAL,
            element_type='R',
            minimum=1,
            maximum=10,
        ),
        Element(
            reference_designator='N704',
            name='Weight Qualifier',
            usage=USAGE_CONDITIONAL,
            element_type='ID',
            minimum=1,
            maximum=2,
        ),
        Element(
            reference_designator='N705',
            name='Tare Weight',
            usage=USAGE_OPTIONAL,
            element_type='N0',
            minimum=3,
            maximum=8,
        ),
        NotUsedElement(reference_designator='N706'),
        NotUsedElement(reference_designator='N707'),
        Element(
            reference_designator='N708',
            name='Volume',
            usage=USAGE_CONDITIONAL,
            element_type='R',
            minimum=1,
            maximum=8,
        ),
        Element(
            reference_designator='N709',
            name='Volume Unit Qualifier',
            usage=USAGE_CONDITIONAL,
            element_type='ID',
            minimum=1,
            maximum=1,
        ),
        Element(
            reference_designator='N710',
            name='Ownership Code',
            usage=USAGE_OPTIONAL,
            element_type='ID',
            minimum=1,
            maximum=1,
        ),
        NotUsedElement(reference_designator='N711'),
        NotUsedElement(reference_designator='N712'),
        NotUsedElement(reference_designator='N713'),
        NotUsedElement(reference_designator='N714'),
        NotUsedElement(reference_designator='N715'),
        NotUsedElement(reference_designator='N716'),
        Element(
            reference_designator='N717',
            name='Weight Unit Code',
            usage=USAGE_OPTIONAL,
            element_type='ID',
            minimum=1,
            maximum=1,
        ),
        Element(
            reference_designator='N718',
            name='Equipment Number Check Digit',
            usage=USAGE_OPTIONAL,
            element_type='N0',
            minimum=1,
            maximum=1,
        ),
        NotUsedElement(reference_designator='N719'),
        NotUsedElement(reference_designator='N720'),
        NotUsedElement(reference_designator='N721'),
        Element(
            reference_designator='N722',
            name='Equipment Type',
            usage=USAGE_OPTIONAL,
            element_type='ID',
            minimum=4,
            maximum=4,
        ),
    )


class QtySegment(BaseSegment):
    segment_id = 'QTY'
    usage = 'O'
    max_use = 1
    elements = (
        Element(
            reference_designator='QTY01',
            name='Quantity Qualifier',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=2,
            maximum=2,
        ),
        Element(
            reference_designator='QTY02',
            name='Quantity',
            usage=USAGE_MANDATORY,
            element_type='R',
            minimum=1,
            maximum=15,
        ),
    )


class M7Segment(BaseSegment):
    segment_id = 'M7'
    usage = 'O'
    max_use = 5
    elements = (
        Element(
            reference_designator='M701',
            name='Seal Number',
            usage=USAGE_MANDATORY,
            element_type='AN',
            minimum=2,
            maximum=15,
        ),
        Element(
            reference_designator='M702',
            name='Seal Number',
            usage=USAGE_OPTIONAL,
            element_type='AN',
            minimum=2,
            maximum=15,
        ),
        Element(
            reference_designator='M703',
            name='Seal Number',
            usage=USAGE_OPTIONAL,
            element_type='AN',
            minimum=2,
            maximum=15,
        ),
        NotUsedElement(reference_designator='M704'),
        Element(
            reference_designator='M705',
            name='Entity Identifier Code',
            usage=USAGE_OPTIONAL,
            element_type='ID',
            minimum=2,
            maximum=3,
        ),
    )


class W09Segment(BaseSegment):
    segment_id = 'W09'
    usage = 'O'
    max_use = 1
    elements = (
        Element(
            reference_designator='W0901',
            name='Equipment Description Code',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=2,
            maximum=2,
        ),
        Element(
            reference_designator='W0902',
            name='Temperature',
            usage=USAGE_CONDITIONAL,
            element_type='R',
            minimum=1,
            maximum=4,
        ),
        Element(
            reference_designator='W0903',
            name='Unit or Basis for Measurement Code',
            usage=USAGE_CONDITIONAL,
            element_type='ID',
            minimum=2,
            maximum=2,
        ),
        NotUsedElement(reference_designator='W0904'),
        Element(
            reference_designator='W0905',
            name='Unit or Basis for Measurement Code',
            usage=USAGE_CONDITIONAL,
            element_type='ID',
            minimum=2,
            maximum=2,
        ),
        Element(
            reference_designator='W0906',
            name='Free Form Message',
            usage=USAGE_OPTIONAL,
            element_type='AN',
            minimum=1,
            maximum=60,
        ),
        NotUsedElement(reference_designator='W0907'),
        NotUsedElement(reference_designator='W0908'),
        Element(
            reference_designator='W0909',
            name='Quantity',
            usage=USAGE_OPTIONAL,
            element_type='R',
            minimum=1,
            maximum=15,
        ),
    )
