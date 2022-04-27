# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyx12lib.core.grammar import Element
from pyx12lib.core.grammar.segment import USAGE_MANDATORY, BaseSegment


class GsSegment(BaseSegment):
    segment_id = 'GS'
    usage = 'M'
    max_use = 1
    elements = (
        Element(
            reference_designator='GS01',
            name='Functional Identifier Code',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=2,
            maximum=2,
        ),
        Element(
            reference_designator='GS02',
            name='Application Sender\'s Code',
            usage=USAGE_MANDATORY,
            element_type='AN',
            minimum=2,
            maximum=15,
        ),
        Element(
            reference_designator='GS03',
            name='Application Receiver\'s Code',
            usage=USAGE_MANDATORY,
            element_type='AN',
            minimum=2,
            maximum=15,
        ),
        Element(
            reference_designator='GS04',
            name='Date',
            usage=USAGE_MANDATORY,
            element_type='DT',
            minimum=8,
            maximum=8,
        ),
        Element(
            reference_designator='GS05',
            name='Time',
            usage=USAGE_MANDATORY,
            element_type='TM',
            minimum=4,
            maximum=8,
        ),
        Element(
            reference_designator='GS06',
            name='Group Control Number',
            usage=USAGE_MANDATORY,
            element_type='N0',
            minimum=1,
            maximum=9,
        ),
        Element(
            reference_designator='GS07',
            name='Responsible Agency Code',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=1,
            maximum=2,
        ),
        Element(
            reference_designator='GS08',
            name='Version / Release / Industry Identifier Code',
            usage=USAGE_MANDATORY,
            element_type='AN',
            minimum=1,
            maximum=12,
        ),
    )


class GeSegment(BaseSegment):
    segment_id = 'GE'
    max_use = 1
    elements = (
        Element(
            reference_designator='GE01',
            name='VNumber of Transaction Sets Included',
            usage=USAGE_MANDATORY,
            element_type='N0',
            minimum=1,
            maximum=6,
        ),
        Element(
            reference_designator='GE02',
            name='Group Control Number',
            usage=USAGE_MANDATORY,
            element_type='N0',
            minimum=1,
            maximum=9,
        ),
    )
