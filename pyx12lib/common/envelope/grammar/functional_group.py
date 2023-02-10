from pyx12lib.core.grammar import BaseSegment, Element, element, segment


class GsSegment(BaseSegment):
    segment_id = "GS"
    usage = segment.USAGE_MANDATORY
    max_use = 1
    elements = (
        Element(
            reference_designator="GS01",
            name="Functional Identifier Code",
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_ID,
            minimum=2,
            maximum=2,
        ),
        Element(
            reference_designator="GS02",
            name="Application Sender's Code",
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=2,
            maximum=15,
        ),
        Element(
            reference_designator="GS03",
            name="Application Receiver's Code",
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=2,
            maximum=15,
        ),
        Element(
            reference_designator="GS04",
            name="Date",
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_DATE,
            minimum=8,
            maximum=8,
        ),
        Element(
            reference_designator="GS05",
            name="Time",
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_TIME,
            minimum=4,
            maximum=8,
        ),
        Element(
            reference_designator="GS06",
            name="Group Control Number",
            usage=element.USAGE_MANDATORY,
            element_type=element.get_numeric_type(0),
            minimum=1,
            maximum=9,
        ),
        Element(
            reference_designator="GS07",
            name="Responsible Agency Code",
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_ID,
            minimum=1,
            maximum=2,
        ),
        Element(
            reference_designator="GS08",
            name="Version / Release / Industry Identifier Code",
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=12,
        ),
    )


class GeSegment(segment.BaseSegment):
    segment_id = "GE"
    max_use = 1
    elements = (
        Element(
            reference_designator="GE01",
            name="Number of Transaction Sets Included",
            usage=element.USAGE_MANDATORY,
            element_type=element.get_numeric_type(0),
            minimum=1,
            maximum=6,
        ),
        Element(
            reference_designator="GE02",
            name="Group Control Number",
            usage=element.USAGE_MANDATORY,
            element_type=element.get_numeric_type(0),
            minimum=1,
            maximum=9,
        ),
    )
