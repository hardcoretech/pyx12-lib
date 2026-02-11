from unittest import TestCase

from pyx12lib.core.grammar import BaseSegment, element, segment
from pyx12lib.core.grammar.loop import LoopDefinition


class _SegA(BaseSegment):
    segment_id = "A"
    usage = segment.USAGE_MANDATORY
    max_use = 1
    elements = ()


class _SegB(BaseSegment):
    segment_id = "B"
    usage = segment.USAGE_OPTIONAL
    max_use = 99
    elements = ()


class _SegC(BaseSegment):
    segment_id = "C"
    usage = segment.USAGE_OPTIONAL
    max_use = 99
    elements = ()


class _SegD(BaseSegment):
    segment_id = "D"
    usage = segment.USAGE_OPTIONAL
    max_use = 99
    elements = ()


class TestLoopDefinition(TestCase):
    def test_basic_construction(self):
        loop = LoopDefinition(_SegA, [_SegB, _SegC])

        self.assertEqual(loop.loop_id, "A")
        self.assertEqual(loop.start_segment_id, "A")
        self.assertIs(loop.start_segment_grammar, _SegA)

    def test_children_segments_stored(self):
        loop = LoopDefinition(_SegA, [_SegB, _SegC])

        self.assertEqual(loop.child_segment_ids, frozenset(["B", "C"]))
        self.assertEqual(loop.child_segment_grammars, [_SegB, _SegC])

    def test_children_with_nested_loop(self):
        nested = LoopDefinition(_SegC, [_SegD])
        loop = LoopDefinition(_SegA, [_SegB, nested])

        # child_segment_ids excludes nested loop's segments
        self.assertEqual(loop.child_segment_ids, frozenset(["B"]))
        self.assertEqual(loop.child_segment_grammars, [_SegB])
        self.assertEqual(len(loop.child_loops), 1)
        self.assertIs(loop.child_loops[0], nested)

    def test_is_start(self):
        loop = LoopDefinition(_SegA, [_SegB])

        self.assertTrue(loop.is_start("A"))
        self.assertFalse(loop.is_start("B"))
        self.assertFalse(loop.is_start("X"))

    def test_is_child(self):
        loop = LoopDefinition(_SegA, [_SegB, _SegC])

        self.assertTrue(loop.is_child("B"))
        self.assertTrue(loop.is_child("C"))
        self.assertFalse(loop.is_child("A"))
        self.assertFalse(loop.is_child("X"))

    def test_all_segment_grammars(self):
        nested = LoopDefinition(_SegC, [_SegD])
        loop = LoopDefinition(_SegA, [_SegB, nested])

        grammars = list(loop.all_segment_grammars())

        self.assertEqual(grammars, [_SegA, _SegB, _SegC, _SegD])

    def test_no_children(self):
        loop = LoopDefinition(_SegA)

        self.assertEqual(loop.child_segment_ids, frozenset())
        self.assertEqual(loop.child_segment_grammars, [])
        self.assertEqual(loop.child_loops, [])
        self.assertEqual(list(loop.all_segment_grammars()), [_SegA])

    def test_invalid_start_segment_raises(self):
        with self.assertRaises(TypeError):
            LoopDefinition("not_a_segment", [_SegB])

        with self.assertRaises(TypeError):
            LoopDefinition(_SegA(), [_SegB])  # instance, not class

    def test_invalid_child_raises(self):
        with self.assertRaises(TypeError):
            LoopDefinition(_SegA, ["not_a_segment"])

        with self.assertRaises(TypeError):
            LoopDefinition(_SegA, [42])
