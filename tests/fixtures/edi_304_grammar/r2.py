from pyx12lib.core.grammar import Element, NotUsedElement
from pyx12lib.core.grammar.segment import USAGE_MANDATORY, USAGE_OPTIONAL, BaseSegment


class R2Segment(BaseSegment):
    segment_id = 'R2'
    usage = 'O'
    max_use = 1
    elements = (
        Element(
            reference_designator='R201',
            name='Standard Carrier Alpha Code',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=2,
            maximum=4,
        ),
        Element(
            reference_designator='R202',
            name='Routing Sequence Code',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=1,
            maximum=2,
        ),
        NotUsedElement(reference_designator='R203'),
        NotUsedElement(reference_designator='R204'),
        NotUsedElement(reference_designator='R205'),
        NotUsedElement(reference_designator='R206'),
        NotUsedElement(reference_designator='R207'),
        NotUsedElement(reference_designator='R208'),
        NotUsedElement(reference_designator='R209'),
        NotUsedElement(reference_designator='R210'),
        NotUsedElement(reference_designator='R211'),
        Element(
            reference_designator='R212',
            name='Type of Service Code',
            usage=USAGE_OPTIONAL,
            element_type='ID',
            minimum=2,
            maximum=2,
        ),
    )
