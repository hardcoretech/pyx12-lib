from pyx12lib.core.renderer import SegmentRenderer

from .grammar import SeSegment, StSegment


class StRenderer(SegmentRenderer):
    grammar = StSegment

    @property
    def element_value_getters(self):
        return {
            'ST01': lambda ele, data, stat: '304',  # Shipping Instruction
            'ST02': lambda ele, data, stat: '{:04d}'.format(data.transaction_set_no),
        }


class SeRenderer(SegmentRenderer):
    grammar = SeSegment

    @property
    def element_value_getters(self):
        return {
            'SE01': lambda ele, data, stat: str(data.segment_counts),
            'SE02': lambda ele, data, stat: '{:04d}'.format(data.transaction_set_no),
        }
