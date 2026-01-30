from pyx12lib.core.grammar import Element, NotUsedElement, element, segment


class R4Segment(segment.BaseSegment):
    segment_id = 'R4'
    usage = segment.USAGE_OPTIONAL
    max_use = 12
    elements = (
        Element(
            reference_designator='R401',
            name='Port Function Code',
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_ID,
            minimum=1,
            maximum=1,
        ),
        Element(
            reference_designator='R402',
            name='Location Qualifier',
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_ID,
            minimum=1,
            maximum=2,
        ),
        Element(
            reference_designator='R403',
            name='Location Identifier',
            usage=element.USAGE_CONDITIONAL,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=30,
        ),
        Element(
            reference_designator='R404',
            name='Port name',
            usage=element.USAGE_OPTIONAL,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=2,
            maximum=24,
        ),
        Element(
            reference_designator='R405',
            name='Country Code',
            usage=element.USAGE_OPTIONAL,
            element_type=element.ELEMENT_TYPE_ID,
            minimum=2,
            maximum=3,
        ),
        Element(
            reference_designator='R406',
            name='Terminal name',
            usage=element.USAGE_OPTIONAL,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=2,
            maximum=30,
        ),
        NotUsedElement(reference_designator='R407'),
        Element(
            reference_designator='R408',
            name='State or Province Code',
            usage=element.USAGE_OPTIONAL,
            element_type=element.ELEMENT_TYPE_ID,
            minimum=2,
            maximum=2,
        ),
    )


class DTMSegment(segment.BaseSegment):
    segment_id = 'DTM'
    usage = segment.USAGE_OPTIONAL
    max_use = 15
    elements = (
        Element(
            reference_designator='DTM01',
            name='Date/Time Qualifier',
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_ID,
            minimum=3,
            maximum=3,
        ),
        Element(
            reference_designator='DTM02',
            name='Date',
            usage=element.USAGE_CONDITIONAL,
            element_type=element.ELEMENT_TYPE_DATE,
            minimum=8,
            maximum=8,
        ),
        Element(
            reference_designator='DTM03',
            name='Time',
            usage=element.USAGE_CONDITIONAL,
            element_type=element.ELEMENT_TYPE_TIME,
            minimum=4,
            maximum=8,
        ),
        Element(
            reference_designator='DTM04',
            name='Time Code',
            usage=element.USAGE_OPTIONAL,
            element_type=element.ELEMENT_TYPE_ID,
            minimum=2,
            maximum=2,
        ),
    )
