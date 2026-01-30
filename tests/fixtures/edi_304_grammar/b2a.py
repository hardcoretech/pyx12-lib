from pyx12lib.core.grammar import Element
from pyx12lib.core.grammar.segment import USAGE_MANDATORY, BaseSegment


class B2aSegment(BaseSegment):
    segment_id = 'B2A'
    usage = 'M'
    max_use = 1
    elements = (
        Element(
            reference_designator='B2A01',
            name='Transaction Set Purpose Code',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=2,
            maximum=2,
        ),
    )
