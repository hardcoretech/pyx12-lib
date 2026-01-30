from pyx12lib.core.grammar import Element
from pyx12lib.core.grammar.segment import USAGE_MANDATORY, USAGE_OPTIONAL, BaseSegment


class K1Segment(BaseSegment):
    segment_id = 'K1'
    usage = 'O'
    max_use = 999
    elements = (
        Element(
            reference_designator='K101',
            name='Free-Form Message',
            usage=USAGE_MANDATORY,
            element_type='AN',
            minimum=1,
            maximum=30,
        ),
        Element(
            reference_designator='K102',
            name='Free-Form Message',
            usage=USAGE_OPTIONAL,
            element_type='AN',
            minimum=1,
            maximum=30,
        ),
    )
