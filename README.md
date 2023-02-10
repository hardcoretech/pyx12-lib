# pyx12-lib

---

## Quick Example

### Rendering
* Define the grammar for the segment.
```python
from pyx12lib.core.grammar import Element, BaseSegment, segment, element


class StSegment(BaseSegment):
    segment_id = 'ST'
    usage = segment.USAGE_MANDATORY
    max_use = 1
    elements = (
        Element(
            reference_designator='ST01',
            name='Transaction Set Identifier Code',
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_ID,
            minimum=3,
            maximum=3,
        ),
        Element(
            reference_designator='ST02',
            name='Transaction Set Control Number',
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=4,
            maximum=9,
        ),
    )
```
* Render the segment from its grammar.
```python
from pyx12lib.common.envelope.grammar import StSegment
from pyx12lib.core.renderer import SegmentRenderer


class StRenderer(SegmentRenderer):
    grammar = StSegment

    element_value_getters =  {
        'ST01': lambda ele, data, stat: '997',
        'ST02': lambda ele, data, stat: '{:04d}'.format(data.transaction_set_no),
    }
```
* Advanced definition for element value getters
```python
from pyx12lib.common.envelope.grammar import StSegment
from pyx12lib.core.renderer import SegmentRenderer


class StRenderer(SegmentRenderer):
    grammar = StSegment

    @property
    def element_value_getters(self):
        return {
            'ST01': lambda ele, data, stat: '997',
            'ST02': self.st02,
        }

    @staticmethod
    def st02(ele, data, stat):
        assert ele is StSegment.elements[1]  # the grammar for the element.
        assert stat['ST01'] is '997'  # stat consists of rendered data so far.
        return '{:04d}'.format(data.transaction_set_no)  # return value should always be strings
```

---
## Test
```bash
python -m unittest discover
```
