# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from builtins import str

import dateutil.parser

from pyx12lib.core.renderer import SegmentRenderer

from .grammar import GeSegment, GsSegment


class GsRenderer(SegmentRenderer):
    grammar = GsSegment

    @property
    def element_value_getters(self):
        return {
            'GS01': lambda ele, data, stat: 'SO',  # Shipping Instruction
            'GS02': lambda ele, data, stat: data.sender_id,
            'GS03': lambda ele, data, stat: data.vendor_id,
            'GS04': self.gs04,
            'GS05': self.gs05,
            'GS06': lambda ele, data, stat: '{:d}'.format(data.functional_group_no),
            'GS07': lambda ele, data, stat: 'X',  # ANSI X12
            'GS08': lambda ele, data, stat: '004010',  # Version 4010
        }

    @staticmethod
    def gs04(ele, data, stat):
        if data.submit_datetime:
            datetime = dateutil.parser.parse(data.submit_datetime)
            return datetime.strftime("%Y%m%d")

        return ''

    @staticmethod
    def gs05(ele, data, stat):
        if data.submit_datetime:
            datetime = dateutil.parser.parse(data.submit_datetime)
            return datetime.strftime('%H%M')

        return ''


class GeRenderer(SegmentRenderer):
    grammar = GeSegment

    @property
    def element_value_getters(self):
        return {
            'GE01': lambda ele, data, stat: str(data.transaction_count),
            'GE02': lambda ele, data, stat: '{:d}'.format(data.functional_group_no),
        }
