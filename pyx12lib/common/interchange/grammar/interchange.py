# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyx12lib.core.grammar import Element
from pyx12lib.core.grammar.segment import USAGE_MANDATORY, BaseSegment


class IsaSegment(BaseSegment):
    segment_id = 'ISA'
    usage = 'M'
    max_use = 1
    elements = (
        Element(
            reference_designator='ISA01',
            name='Authorization Information Qualifier',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=2,
            maximum=2,
        ),
        Element(
            reference_designator='ISA02',
            name='Authorization Information',
            usage=USAGE_MANDATORY,
            element_type='AN',
            minimum=10,
            maximum=10,
        ),
        Element(
            reference_designator='ISA03',
            name='Security Information Qualifier',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=2,
            maximum=2,
        ),
        Element(
            reference_designator='ISA04',
            name='Security Information',
            usage=USAGE_MANDATORY,
            element_type='AN',
            minimum=10,
            maximum=10,
        ),
        Element(
            reference_designator='ISA05',
            name='Interchange ID Qualifier',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=2,
            maximum=2,
        ),
        Element(
            reference_designator='ISA06',
            name='Interchange Sender ID',
            usage=USAGE_MANDATORY,
            element_type='AN',
            minimum=15,
            maximum=15,
        ),
        Element(
            reference_designator='ISA07',
            name='Interchange ID Qualifier',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=2,
            maximum=2,
        ),
        Element(
            reference_designator='ISA08',
            name='Interchange Receiver ID',
            usage=USAGE_MANDATORY,
            element_type='AN',
            minimum=15,
            maximum=15,
        ),
        Element(
            reference_designator='ISA09',
            name='Interchange Date',
            usage=USAGE_MANDATORY,
            element_type='DT',
            minimum=6,
            maximum=6,
        ),
        Element(
            reference_designator='ISA10',
            name='Interchange Time',
            usage=USAGE_MANDATORY,
            element_type='TM',
            minimum=4,
            maximum=4,
        ),
        Element(
            reference_designator='ISA11',
            name='Interchange Control Standards Identifier',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=1,
            maximum=1,
        ),
        Element(
            reference_designator='ISA12',
            name='Interchange Control Version Number',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=5,
            maximum=5,
        ),
        Element(
            reference_designator='ISA13',
            name='Interchange Control Number',
            usage=USAGE_MANDATORY,
            element_type='N0',
            minimum=9,
            maximum=9,
        ),
        Element(
            reference_designator='ISA14',
            name='Acknowledgment Requested',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=1,
            maximum=1,
        ),
        Element(
            reference_designator='ISA15',
            name='Usage Indicator',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=1,
            maximum=1,
        ),
        Element(
            reference_designator='ISA16',
            name='Component Element Separator',
            usage=USAGE_MANDATORY,
            element_type='AN',
            minimum=1,
            maximum=1,
        ),
    )


class IeaSegment(BaseSegment):
    segment_id = 'IEA'
    max_use = 1
    elements = (
        Element(
            reference_designator='IEA01',
            name='Number of Included Functional Groups',
            usage=USAGE_MANDATORY,
            element_type='N0',
            minimum=1,
            maximum=5,
        ),
        Element(
            reference_designator='IEA02',
            name='Interchange Control Number',
            usage=USAGE_MANDATORY,
            element_type='N0',
            minimum=9,
            maximum=9,
        ),
    )
