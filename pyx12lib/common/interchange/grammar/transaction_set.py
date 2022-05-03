from pyx12lib.core.grammar import Element
from pyx12lib.core.grammar.segment import USAGE_MANDATORY, BaseSegment


class StSegment(BaseSegment):
    segment_id = 'ST'
    usage = 'M'
    max_use = 1
    elements = (
        Element(
            reference_designator='ST01',
            name='Transaction Set Identifier Code',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=3,
            maximum=3,
        ),
        Element(
            reference_designator='ST02',
            name='Transaction Set Control Number',
            usage=USAGE_MANDATORY,
            element_type='AN',
            minimum=4,
            maximum=9,
        ),
    )


class SeSegment(BaseSegment):
    segment_id = 'SE'
    max_use = 1
    elements = (
        Element(
            reference_designator='SE01',
            name='Number of Included Segments',
            usage=USAGE_MANDATORY,
            element_type='N0',
            minimum=1,
            maximum=10,
        ),
        Element(
            reference_designator='SE02',
            name='Transaction Set Control Number',
            usage=USAGE_MANDATORY,
            element_type='AN',
            minimum=4,
            maximum=9,
        ),
    )
