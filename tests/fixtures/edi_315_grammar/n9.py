from pyx12lib.core.grammar import Element, element, segment


class N9Segment(segment.BaseSegment):
    segment_id = 'N9'
    usage = segment.USAGE_OPTIONAL
    max_use = 30
    elements = (
        Element(
            reference_designator='N901',
            name='Reference Identification Qualifier',
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_ID,
            minimum=2,
            maximum=3,
        ),
        Element(
            reference_designator='N902',
            name='Reference Identification',
            usage=element.USAGE_CONDITIONAL,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=30,
        ),
    )
