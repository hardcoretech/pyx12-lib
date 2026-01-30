from pyx12lib.core.grammar import Element, NotUsedElement
from pyx12lib.core.grammar.segment import USAGE_CONDITIONAL, USAGE_MANDATORY, USAGE_OPTIONAL, BaseSegment


class R4Segment(BaseSegment):
    segment_id = 'R4'
    usage = 'O'
    max_use = 1
    elements = (
        Element(
            reference_designator='R401',
            name='Port or Terminal Function Code',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=1,
            maximum=1,
        ),
        Element(
            reference_designator='R402',
            name='Location Qualifier',
            usage=USAGE_CONDITIONAL,
            element_type='ID',
            minimum=1,
            maximum=2,
        ),
        Element(
            reference_designator='R403',
            name='Location Identifier',
            usage=USAGE_CONDITIONAL,
            element_type='AN',
            minimum=1,
            maximum=30,
        ),
        Element(
            reference_designator='R404',
            name='Port Name',
            usage=USAGE_OPTIONAL,
            element_type='AN',
            minimum=2,
            maximum=60,
        ),
        Element(
            reference_designator='R405',
            name='Country Code',
            usage=USAGE_OPTIONAL,
            element_type='ID',
            minimum=2,
            maximum=3,
        ),
        NotUsedElement(reference_designator='R406'),
        NotUsedElement(reference_designator='R407'),
        Element(
            reference_designator='R408',
            name='State or Province Code',
            usage=USAGE_OPTIONAL,
            element_type='ID',
            minimum=2,
            maximum=2,
        ),
    )
