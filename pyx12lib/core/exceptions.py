class BaseX12Exception(ValueError):
    pass


class MandatorySegmentException(BaseX12Exception):
    """
    Exception raised when a mandatory segment does not have any values
    """

    def __init__(self, segment):
        message = '{segment_id}: mandatory segment has no values'.format(
            segment_id=segment.segment_id,
        )
        super(MandatorySegmentException, self).__init__(message)


class MandatoryCompositeElementException(BaseX12Exception):
    """
    Exception raised when a mandatory composite element does not have any values
    """

    def __init__(self, element):
        message = '{segment_id}: mandatory composite element has no values'.format(
            segment_id=element.reference_designator,
        )
        super(MandatoryCompositeElementException, self).__init__(message)


class MandatoryElementException(BaseX12Exception):
    """
    Exception raised when a mandatory element is not filled with value
    """

    def __init__(self, element, value):
        message = '{ref_des} {name}'.format(
            ref_des=element.reference_designator,
            name=element.name,
        )
        super(MandatoryElementException, self).__init__(message)


class MandatoryComponentException(MandatoryElementException):
    """
    Exception raised when a mandatory component is not filled with value
    """


class LengthException(BaseX12Exception):
    """
    Exception raised when a element is not match its width limit
    """

    def __init__(self, element, value):
        message = '{ref_des} {name}: {value} not match {min}/{max}'.format(
            ref_des=element.reference_designator,
            name=element.name,
            value='~empty str~' if value == '' else value,
            min=element.minimum,
            max=element.maximum,
        )
        super(LengthException, self).__init__(message)


class NotStringException(BaseX12Exception):
    """
    Exception raised when a element is not in string type
    """

    def __init__(self, element, value):
        message = '{ref_des} {name}: {value} => {type}'.format(
            ref_des=element.reference_designator,
            name=element.name,
            value=value,
            type=type(value),
        )
        super(NotStringException, self).__init__(message)


class NotDecimalError(BaseX12Exception):
    """
    Exception raised when a element is not in string type
    """

    def __init__(self, element, value):
        message = '{ref_des} {name}: expect: {ele_type}, get: {value} => {type}'.format(
            ref_des=element.reference_designator,
            name=element.name,
            ele_type=element.type,
            value=value,
            type=type(value),
        )
        super(NotDecimalError, self).__init__(message)


class DecimalPlaceNotMatchError(BaseX12Exception):
    """
    Exception raised when a element is not in string type
    """

    def __init__(self, element, value):
        message = '{ref_des} {name}: expect: {ele_type}, get: {value} => {type}'.format(
            ref_des=element.reference_designator,
            name=element.name,
            ele_type=element.type,
            value=value,
            type=type(value),
        )
        super(DecimalPlaceNotMatchError, self).__init__(message)


class NotUsedElementException(BaseX12Exception):
    """
    Exception raised when NotUsedElement has value
    """

    def __init__(self, element, value):
        message = '{ref_des}: {value} NotUsedElement should not have values'.format(
            ref_des=element.reference_designator,
            value=value,
        )
        super(NotUsedElementException, self).__init__(message)
