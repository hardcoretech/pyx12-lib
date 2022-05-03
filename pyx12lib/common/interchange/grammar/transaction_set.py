from pyx12lib.core.grammar import Element, BaseSegment, segment, element


class StSegment(BaseSegment):
    segment_id = 'ST'
    usage = segment.USAGE_MANDATORY
    max_use = 1
    elements = (
        Element(
            reference_designator='ST01',
            name='Transaction Set Identifier Code',
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_ID,
            minimum=3,
            maximum=3,
        ),
        Element(
            reference_designator='ST02',
            name='Transaction Set Control Number',
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_STRING,
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
            usage=element.USAGE_MANDATORY,
            element_type=element.get_numeric_type(0),
            minimum=1,
            maximum=10,
        ),
        Element(
            reference_designator='SE02',
            name='Transaction Set Control Number',
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=4,
            maximum=9,
        ),
    )
