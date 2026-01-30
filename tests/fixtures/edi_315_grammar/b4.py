from pyx12lib.core.grammar import Element, NotUsedElement, element, segment


class B4Segment(segment.BaseSegment):
    segment_id = 'B4'
    usage = segment.USAGE_MANDATORY
    max_use = 1
    elements = (
        NotUsedElement(
            reference_designator='B401',
        ),
        NotUsedElement(
            reference_designator='B402',
        ),
        Element(
            reference_designator='B403',
            name='Status Code',
            usage=element.USAGE_OPTIONAL,
            element_type=element.ELEMENT_TYPE_ID,
            minimum=1,
            maximum=2,
        ),
        Element(
            reference_designator='B404',
            name='Status Date',
            usage=element.USAGE_OPTIONAL,
            element_type=element.ELEMENT_TYPE_DATE,
            minimum=8,
            maximum=8,
        ),
        Element(
            reference_designator='B405',
            name='Status Time',
            usage=element.USAGE_OPTIONAL,
            element_type=element.ELEMENT_TYPE_TIME,
            minimum=4,
            maximum=4,
        ),
        Element(
            reference_designator='B406',
            name='Status Location',
            usage=element.USAGE_OPTIONAL,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=3,
            maximum=5,
        ),
        Element(
            reference_designator='B407',
            name='Transaction Equipment Initial',
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=2,
            maximum=4,
        ),
        Element(
            reference_designator='B408',
            name='Equipment Number',
            usage=element.USAGE_CONDITIONAL,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=10,
        ),
        Element(
            reference_designator='B409',
            name='Equipment Status Code',
            usage=element.USAGE_OPTIONAL,
            element_type=element.ELEMENT_TYPE_ID,
            minimum=1,
            maximum=2,
        ),
        Element(
            reference_designator='B410',
            name='Equipment Type',
            usage=element.USAGE_OPTIONAL,
            element_type=element.ELEMENT_TYPE_ID,
            minimum=4,
            maximum=4,
        ),
        Element(
            reference_designator='B411',
            name='Location Identifier',
            usage=element.USAGE_CONDITIONAL,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=30,
        ),
        Element(
            reference_designator='B412',
            name='Location Qualifier',
            usage=element.USAGE_CONDITIONAL,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=2,
        ),
        Element(
            reference_designator='B413',
            name='Equipment Number Check Digit',
            usage=element.USAGE_OPTIONAL,
            element_type=element.get_numeric_type(max_digits=0),
            minimum=1,
            maximum=1,
        ),
    )
