import json
from unittest import TestCase

from pyx12lib.core.grammar import BaseSegment, Element, element, segment
from pyx12lib.core.parsed import ParsedLoop
from pyx12lib.core.parser import SegmentParser


class _StubSegment(BaseSegment):
    segment_id = "STB"
    usage = segment.USAGE_MANDATORY
    max_use = 1
    elements = (
        Element(
            reference_designator="STB01",
            name="Stub Element",
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=10,
        ),
    )


class TestParsedLoop(TestCase):
    def _make_segment(self, value):
        parser = SegmentParser("STB*{}~".format(value), grammar=_StubSegment)
        return parser.parse()

    def test_loop_basic(self):
        # arrange
        seg1 = self._make_segment("A")
        seg2 = self._make_segment("B")

        # action
        loop = ParsedLoop(loop_id="TEST_LOOP", segments=[seg1, seg2])
        result = loop.to_dict()

        # assert
        self.assertEqual(result['loop_id'], 'TEST_LOOP')
        self.assertEqual(len(result['segments']), 2)
        self.assertNotIn('child_loops', result)

    def test_loop_with_children(self):
        # arrange
        parent_seg = self._make_segment("PARENT")
        child_seg = self._make_segment("CHILD")

        parent_loop = ParsedLoop(loop_id="PARENT", segments=[parent_seg])
        child_loop = ParsedLoop(loop_id="CHILD", segments=[child_seg])
        parent_loop.add_child_loop(child_loop)

        # action
        result = parent_loop.to_dict()

        # assert
        self.assertIn('child_loops', result)
        self.assertEqual(len(result['child_loops']), 1)
        self.assertEqual(result['child_loops'][0]['loop_id'], 'CHILD')

    def test_add_segment(self):
        # arrange
        loop = ParsedLoop(loop_id="TEST")
        seg = self._make_segment("ADDED")

        # action
        loop.add_segment(seg)
        result = loop.to_dict()

        # assert
        self.assertEqual(len(result['segments']), 1)

    def test_to_json(self):
        # arrange
        seg = self._make_segment("JSON")
        loop = ParsedLoop(loop_id="JSON_LOOP", segments=[seg])

        # action
        json_output = loop.to_json()
        data = json.loads(json_output)

        # assert
        self.assertEqual(data['loop_id'], 'JSON_LOOP')

    def test_nested_loops_to_dict(self):
        # arrange
        root = ParsedLoop(loop_id="ROOT")
        root.add_segment(self._make_segment("R1"))

        mid = ParsedLoop(loop_id="MID")
        mid.add_segment(self._make_segment("M1"))

        leaf = ParsedLoop(loop_id="LEAF")
        leaf.add_segment(self._make_segment("L1"))

        mid.add_child_loop(leaf)
        root.add_child_loop(mid)

        # action
        result = root.to_dict()

        # assert
        self.assertEqual(result['loop_id'], 'ROOT')
        self.assertEqual(result['child_loops'][0]['loop_id'], 'MID')
        self.assertEqual(result['child_loops'][0]['child_loops'][0]['loop_id'], 'LEAF')

    def test_empty_loop(self):
        loop = ParsedLoop(loop_id="EMPTY")
        result = loop.to_dict()

        self.assertEqual(result['loop_id'], 'EMPTY')
        self.assertEqual(len(result['segments']), 0)
        self.assertNotIn('child_loops', result)
