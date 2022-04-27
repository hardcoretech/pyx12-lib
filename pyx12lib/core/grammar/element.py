# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from builtins import object

COMPONENT_DELIMITER = '^'

USAGE_MANDATORY = 'M'
USAGE_OPTIONAL = 'O'
USAGE_CONDITIONAL = 'C'

ELEMENT_TYPE_ID = 'ID'
ELEMENT_TYPE_STRING = 'AN'
ELEMENT_TYPE_DATE = 'DT'
ELEMENT_TYPE_TIME = 'TM'
ELEMENT_TYPE_NUMERIC = 'N'
ELEMENT_TYPE_DECIMAL = 'R'


def get_numeric_type(max_digits):
    return ELEMENT_TYPE_NUMERIC + str(max_digits)


class BaseElement(object):
    def __init__(self, reference_designator):
        self.reference_designator = reference_designator


class NotUsedElement(BaseElement):
    @staticmethod
    def value_getter(ele, data, stat):
        return ''


class Element(BaseElement):
    def __init__(self, reference_designator, name, usage, element_type, minimum, maximum):
        super(Element, self).__init__(reference_designator)

        self.name = name
        self.usage = usage
        self.type = element_type
        self.minimum = minimum
        self.maximum = maximum


class Component(Element):
    pass


class CompositeElement(Element):
    definition = None

    def __init__(self, reference_designator, name, usage, element_type, minimum, maximum, components):
        super(CompositeElement, self).__init__(reference_designator, name, usage, element_type, minimum, maximum)

        self.components = components
