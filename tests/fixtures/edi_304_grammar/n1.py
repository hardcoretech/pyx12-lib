from pyx12lib.core.grammar import Element
from pyx12lib.core.grammar.segment import USAGE_CONDITIONAL, USAGE_MANDATORY, USAGE_OPTIONAL, BaseSegment


class N1Segment(BaseSegment):
    segment_id = 'N1'
    usage = 'O'
    max_use = 1
    elements = (
        Element(
            reference_designator='N101',
            name='Entity Identifier Code',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=2,
            maximum=3,
        ),
        Element(
            reference_designator='N102',
            name='Name',
            usage=USAGE_CONDITIONAL,
            element_type='AN',
            minimum=1,
            maximum=35,
        ),
        Element(
            reference_designator='N103',
            name='Identification Code Qualifier',
            usage=USAGE_CONDITIONAL,
            element_type='ID',
            minimum=1,
            maximum=2,
        ),
        Element(
            reference_designator='N104',
            name='Identification Code',
            usage=USAGE_CONDITIONAL,
            element_type='AN',
            minimum=2,
            maximum=35,
        ),
    )


class N2Segment(BaseSegment):
    segment_id = 'N2'
    usage = 'O'
    max_use = 2
    elements = (
        Element(
            reference_designator='N201',
            name='Name',
            usage=USAGE_MANDATORY,
            element_type='AN',
            minimum=1,
            maximum=35,
        ),
        Element(
            reference_designator='N202',
            name='Name',
            usage=USAGE_OPTIONAL,
            element_type='AN',
            minimum=1,
            maximum=35,
        ),
    )


class N3Segment(BaseSegment):
    segment_id = 'N3'
    usage = 'O'
    max_use = 2
    elements = (
        Element(
            reference_designator='N301',
            name='Address Information',
            usage=USAGE_MANDATORY,
            element_type='AN',
            minimum=1,
            maximum=35,
        ),
        Element(
            reference_designator='N302',
            name='Address Information',
            usage=USAGE_OPTIONAL,
            element_type='AN',
            minimum=1,
            maximum=35,
        ),
    )


class N4Segment(BaseSegment):
    segment_id = 'N4'
    usage = 'O'
    max_use = 1
    elements = (
        Element(
            reference_designator='N401',
            name='City Name',
            usage=USAGE_OPTIONAL,
            element_type='AN',
            minimum=2,
            maximum=30,
        ),
        Element(
            reference_designator='N402',
            name='State or Province Code',
            usage=USAGE_OPTIONAL,
            element_type='ID',
            minimum=2,
            maximum=2,
        ),
        Element(
            reference_designator='N403',
            name='Postal Code',
            usage=USAGE_OPTIONAL,
            element_type='ID',
            minimum=3,
            maximum=15,
        ),
        Element(
            reference_designator='N404',
            name='Country Code',
            usage=USAGE_OPTIONAL,
            element_type='ID',
            minimum=2,
            maximum=3,
        ),
        Element(
            reference_designator='N405',
            name='Location Qualifier',
            usage=USAGE_CONDITIONAL,
            element_type='ID',
            minimum=1,
            maximum=2,
        ),
        Element(
            reference_designator='N406',
            name='Location Identifier',
            usage=USAGE_OPTIONAL,
            element_type='AN',
            minimum=1,
            maximum=30,
        ),
    )


class G61Segment(BaseSegment):
    segment_id = 'G61'
    usage = 'O'
    max_use = 3
    elements = (
        Element(
            reference_designator='G6101',
            name='Contact Function Code',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=2,
            maximum=2,
        ),
        Element(
            reference_designator='G6102',
            name='Name',
            usage=USAGE_MANDATORY,
            element_type='AN',
            minimum=1,
            maximum=35,
        ),
        Element(
            reference_designator='G6103',
            name='Communication Number Qualifier',
            usage=USAGE_CONDITIONAL,
            element_type='ID',
            minimum=2,
            maximum=2,
        ),
        Element(
            reference_designator='G6104',
            name='Communication Number',
            usage=USAGE_CONDITIONAL,
            element_type='AN',
            minimum=1,
            maximum=80,
        ),
    )
