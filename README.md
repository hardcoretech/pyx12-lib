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

### Parsing X12 to JSON

* Quick parse using the top-level API.
```python
from pyx12lib import parse_x12, parse_x12_to_json

x12_data = "ST*997*0001~SE*1*0001~"

# Parse to Python dict
data = parse_x12(x12_data)
# {'segments': [{'segment_id': 'ST', 'elements': [...]}, ...]}

# Parse to JSON string
json_str = parse_x12_to_json(x12_data)
```

* Parse a single segment with explicit grammar.
```python
from pyx12lib.core.parser import SegmentParser
from pyx12lib.common.envelope.grammar import StSegment

parser = SegmentParser("ST*997*0001~", grammar=StSegment)
result = parser.to_dict()
# {'segment_id': 'ST', 'elements': [
#     {'reference_designator': 'ST01', 'name': 'Transaction Set Identifier Code', 'value': '997', ...},
#     {'reference_designator': 'ST02', 'name': 'Transaction Set Control Number', 'value': '0001', ...},
# ]}
```

* Register custom segment grammars for parsing.
```python
from pyx12lib import GrammarRegistry, X12Parser
from pyx12lib.core.grammar import BaseSegment, Element, element, segment

class MySegment(BaseSegment):
    segment_id = 'MY'
    usage = segment.USAGE_MANDATORY
    max_use = 1
    elements = (
        Element(
            reference_designator='MY01',
            name='My Field',
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=10,
        ),
    )

registry = GrammarRegistry()
registry.register(MySegment)

parser = X12Parser(registry=registry)
data = parser.parse("MY*hello~MY*world~").to_dict()
```

* Parse with loop definitions to group related segments.
```python
from pyx12lib import X12Parser, LoopDefinition, GrammarRegistry
from pyx12lib.core.grammar import BaseSegment, Element, element, segment

class N1Segment(BaseSegment):
    segment_id = 'N1'
    usage = segment.USAGE_OPTIONAL
    max_use = 99
    elements = (
        Element(reference_designator='N101', name='Entity Identifier Code',
                usage=element.USAGE_MANDATORY, element_type=element.ELEMENT_TYPE_ID,
                minimum=2, maximum=3),
    )

class N2Segment(BaseSegment):
    segment_id = 'N2'
    usage = segment.USAGE_OPTIONAL
    max_use = 2
    elements = (
        Element(reference_designator='N201', name='Name',
                usage=element.USAGE_MANDATORY, element_type=element.ELEMENT_TYPE_STRING,
                minimum=1, maximum=35),
    )

registry = GrammarRegistry()
registry.register_loop(LoopDefinition(N1Segment, [N2Segment]))

parser = X12Parser(registry=registry)
data = parser.parse("N1*CA~N1*SH~N2*ACME CORP~N1*CN~").to_dict()
# {'segments': [
#     {'loop_id': 'N1', 'segments': [{'segment_id': 'N1', 'elements': [...]}]},
#     {'loop_id': 'N1', 'segments': [
#         {'segment_id': 'N1', 'elements': [...]},
#         {'segment_id': 'N2', 'elements': [...]},
#     ]},
#     {'loop_id': 'N1', 'segments': [{'segment_id': 'N1', 'elements': [...]}]},
# ]}
```

* Auto-detect delimiters from ISA header.
```python
from pyx12lib import parse_x12

# Delimiters are automatically detected from the ISA segment
x12_data = (
    "ISA*00*          *00*          *ZZ*SENDER         "
    "*ZZ*RECEIVER       *210101*1200*^*00501*000000001*0*P*>~"
    "GS*FA*SENDER*RECEIVER*20210101*1200*1*X*005010~"
    "ST*997*0001~SE*1*0001~GE*1*1~IEA*1*000000001~"
)
data = parse_x12(x12_data)
```

---
## Test
```bash
python -m unittest discover
```
