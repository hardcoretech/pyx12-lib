from pyx12lib.core.grammar import Element, NotUsedElement
from pyx12lib.core.grammar.segment import USAGE_CONDITIONAL, USAGE_OPTIONAL, BaseSegment


class V1Segment(BaseSegment):
    segment_id = 'V1'
    usage = 'M'
    max_use = 1
    elements = (
        Element(
            reference_designator='V101',
            name='Vessel Code',
            usage=USAGE_CONDITIONAL,
            element_type='ID',
            minimum=1,
            maximum=20,
        ),
        Element(
            reference_designator='V102',
            name='Vessel Name',
            usage=USAGE_CONDITIONAL,
            element_type='AN',
            minimum=2,
            maximum=28,
        ),
        NotUsedElement(reference_designator='V103'),
        Element(
            reference_designator='V104',
            name='Flight/Voyage Number',
            usage=USAGE_OPTIONAL,
            element_type='AN',
            minimum=2,
            maximum=10,
        ),
        Element(
            reference_designator='V105',
            name='Standard Carrier Alpha Code',
            usage=USAGE_OPTIONAL,
            element_type='ID',
            minimum=2,
            maximum=4,
        ),
        NotUsedElement(reference_designator='V106'),
        NotUsedElement(reference_designator='V107'),
        Element(
            reference_designator='V108',
            name='Vessel Code Qualifier',
            usage=USAGE_OPTIONAL,
            element_type='ID',
            minimum=1,
            maximum=1,
        ),
    )
