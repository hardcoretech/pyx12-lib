from pyx12lib.core.grammar import Element, NotUsedElement
from pyx12lib.core.grammar.segment import USAGE_CONDITIONAL, USAGE_MANDATORY, USAGE_OPTIONAL, BaseSegment


class L3Segment(BaseSegment):
    segment_id = 'L3'
    usage = 'O'
    max_use = 1
    elements = (
        Element(
            reference_designator='L301',
            name='Weight',
            usage=USAGE_CONDITIONAL,
            element_type='R',
            minimum=1,
            maximum=10,
        ),
        Element(
            reference_designator='L302',
            name='Weight Qualifier',
            usage=USAGE_CONDITIONAL,
            element_type='ID',
            minimum=1,
            maximum=2,
        ),
        NotUsedElement(reference_designator='L303'),
        NotUsedElement(reference_designator='L304'),
        NotUsedElement(reference_designator='L305'),
        NotUsedElement(reference_designator='L306'),
        NotUsedElement(reference_designator='L307'),
        NotUsedElement(reference_designator='L308'),
        Element(
            reference_designator='L309',
            name='Volume',
            usage=USAGE_CONDITIONAL,
            element_type='R',
            minimum=1,
            maximum=8,
        ),
        Element(
            reference_designator='L310',
            name='Volume Unit Qualifier',
            usage=USAGE_CONDITIONAL,
            element_type='ID',
            minimum=1,
            maximum=1,
        ),
        Element(
            reference_designator='L311',
            name='Lading Quantity',
            usage=USAGE_OPTIONAL,
            element_type='N0',
            minimum=1,
            maximum=7,
        ),
        Element(
            reference_designator='L312',
            name='Weight Unit Code',
            usage=USAGE_OPTIONAL,
            element_type='ID',
            minimum=1,
            maximum=1,
        ),
    )


class PWKSegment(BaseSegment):
    segment_id = 'PWK'
    usage = 'O'
    max_use = 50
    elements = (
        Element(
            reference_designator='PWK01',
            name='Report Type Code',
            usage=USAGE_CONDITIONAL,
            element_type='ID',
            minimum=2,
            maximum=2,
        ),
        Element(
            reference_designator='PWK02',
            name='Report Transmission Code',
            usage=USAGE_OPTIONAL,
            element_type='ID',
            minimum=1,
            maximum=2,
        ),
        Element(
            reference_designator='PWK03',
            name='Report Copies Needed',
            usage=USAGE_OPTIONAL,
            element_type='N0',
            minimum=1,
            maximum=2,
        ),
        NotUsedElement(reference_designator='PWK04'),
        NotUsedElement(reference_designator='PWK05'),
        NotUsedElement(reference_designator='PWK06'),
        Element(
            reference_designator='PWK07',
            name='Description',
            usage=USAGE_OPTIONAL,
            element_type='AN',
            minimum=1,
            maximum=80,
        ),
    )


class SACSegment(BaseSegment):
    segment_id = 'SAC'
    usage = 'M'
    max_use = 1
    elements = (
        Element(
            reference_designator='SAC01',
            name='Allowance or Charge Indicator',
            usage=USAGE_MANDATORY,
            element_type='ID',
            minimum=1,
            maximum=1,
        ),
        Element(
            reference_designator='SAC02',
            name='Service, Promotion, Allowance, or Charge Code',
            usage=USAGE_CONDITIONAL,
            element_type='ID',
            minimum=4,
            maximum=4,
        ),
        NotUsedElement(reference_designator='SAC03'),
        NotUsedElement(reference_designator='SAC04'),
        NotUsedElement(reference_designator='SAC05'),
        NotUsedElement(reference_designator='SAC06'),
        NotUsedElement(reference_designator='SAC07'),
        NotUsedElement(reference_designator='SAC08'),
        NotUsedElement(reference_designator='SAC09'),
        NotUsedElement(reference_designator='SAC10'),
        NotUsedElement(reference_designator='SAC11'),
        Element(
            reference_designator='SAC12',
            name='Allowance or Charge Method of Handling Code',
            usage=USAGE_OPTIONAL,
            element_type='ID',
            minimum=2,
            maximum=2,
        ),
    )
