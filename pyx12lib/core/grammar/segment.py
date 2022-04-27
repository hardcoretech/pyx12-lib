# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from builtins import object

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
