import dateutil.parser

from pyx12lib.core.grammar.element import COMPONENT_DELIMITER
from pyx12lib.core.renderer import SegmentRenderer

from .grammar import IeaSegment, IsaSegment


class IsaRenderer(SegmentRenderer):
    grammar = IsaSegment

    @property
    def element_value_getters(self):
        return {
            'ISA01': lambda ele, data, stat: '00',  # No Authorization Info Present
            'ISA02': lambda ele, data, stat: '{: <10}'.format(' '),
            'ISA03': lambda ele, data, stat: '00',  # No Security Info Present
            'ISA04': lambda ele, data, stat: '{: <10}'.format(' '),
            'ISA05': lambda ele, data, stat: 'ZZ',  # Sender ID Mutually Defined
            'ISA06': lambda ele, data, stat: '{: <{width}}'.format(data.sender_id, width=ele.minimum),
            'ISA07': lambda ele, data, stat: 'ZZ',  # Receiver ID Mutually Defined
            'ISA08': lambda ele, data, stat: '{: <{width}}'.format(data.vendor_id, width=ele.minimum),
            'ISA09': self.isa09,
            'ISA10': self.isa10,
            'ISA11': lambda ele, data, stat: 'U',
            'ISA12': lambda ele, data, stat: '00401',
            'ISA13': self.isa13,
            'ISA14': lambda ele, data, stat: '1',  # to request an interchange ack
            'ISA15': lambda ele, data, stat: 'P',  # Production Data
            'ISA16': lambda ele, data, stat: COMPONENT_DELIMITER,
        }

    @staticmethod
    def isa09(ele, data, stat):
        if data.submit_datetime:
            datetime = dateutil.parser.parse(data.submit_datetime)
            return datetime.strftime("%y%m%d")

        return ''

    @staticmethod
    def isa10(ele, data, stat):
        if data.submit_datetime:
            datetime = dateutil.parser.parse(data.submit_datetime)
            return datetime.strftime("%H%M")

        return ''

    def isa13(self, ele, data, stat):
        div, mod = divmod(data.interchange_no, 999999999)  # ISA Control Number is a 9 digits integer
        control_no = mod if not div else mod + 1
        return '{:09d}'.format(control_no)


class IeaRenderer(SegmentRenderer):
    grammar = IeaSegment

    @property
    def element_value_getters(self):
        return {
            'IEA01': lambda ele, data, stat: str(data.functional_group_count),
            'IEA02': lambda ele, data, stat: '{:09d}'.format(data.interchange_no),
        }
