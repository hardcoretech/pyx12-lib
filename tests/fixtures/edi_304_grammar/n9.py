from pyx12lib.core.grammar import Element
from pyx12lib.core.grammar.segment import USAGE_CONDITIONAL, USAGE_MANDATORY, BaseSegment


class N9Segment(BaseSegment):
    segment_id = 'N9'
    usage = 'M'
    max_use = 100
    elements = (
        Element(
            reference_designator='N901',
            name='Reference Identification Qualifier',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=2,
            maximum=3,
        ),
        Element(
            reference_designator='N902',
            name='Reference Identification',
            usage=USAGE_CONDITIONAL,
            element_type='AN',
            minimum=1,
            maximum=35,
        ),
    )
