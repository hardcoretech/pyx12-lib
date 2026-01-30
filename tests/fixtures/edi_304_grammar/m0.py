from pyx12lib.core.grammar import Element
from pyx12lib.core.grammar.segment import USAGE_MANDATORY, USAGE_OPTIONAL, BaseSegment


class M0Segment(BaseSegment):
    segment_id = 'M0'
    usage = 'O'
    max_use = 1
    elements = (
        Element(
            reference_designator='M001',
            name='Letter of Credit Number',
            usage=USAGE_MANDATORY,
            element_type='AN',
            minimum=2,
            maximum=40,
        ),
        Element(
            reference_designator='M002',
            name='Date',
            usage=USAGE_OPTIONAL,
            element_type='DT',
            minimum=8,
            maximum=8,
        ),
        Element(
            reference_designator='M003',
            name='Date',
            usage=USAGE_OPTIONAL,
            element_type='DT',
            minimum=8,
            maximum=8,
        ),
    )
