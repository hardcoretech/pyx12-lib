ELEMENT_DELIMITER = '*'
SEGMENT_TERMINATOR = '~'

USAGE_MANDATORY = 'M'
USAGE_OPTIONAL = 'O'
USAGE_CONDITIONAL = 'X'


class BaseSegment(object):
    segment_id = None
    usage = None
    max_use = None
    elements = None
