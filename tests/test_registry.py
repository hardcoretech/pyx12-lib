from unittest import TestCase

from pyx12lib.core.grammar import BaseSegment, Element, element, segment
from pyx12lib.core.grammar.loop import LoopDefinition
from pyx12lib.core.registry import GrammarRegistry, create_default_registry


class _CustomSegment(BaseSegment):
    segment_id = "CUS"
    usage = segment.USAGE_MANDATORY
    max_use = 1
    elements = (
        Element(
            reference_designator="CUS01",
            name="Custom Element",
            usage=element.USAGE_MANDATORY,
            element_type=element.ELEMENT_TYPE_STRING,
            minimum=1,
            maximum=10,
        ),
    )


class _LoopStart(BaseSegment):
    segment_id = "LS"
    usage = segment.USAGE_MANDATORY
    max_use = 1
    elements = ()


class _LoopChild1(BaseSegment):
    segment_id = "LC1"
    usage = segment.USAGE_OPTIONAL
    max_use = 99
    elements = ()


class _LoopChild2(BaseSegment):
    segment_id = "LC2"
    usage = segment.USAGE_OPTIONAL
    max_use = 99
    elements = ()


class TestGrammarRegistry(TestCase):
    def test_register_and_get(self):
        registry = GrammarRegistry()
        registry.register(_CustomSegment)

        result = registry.get("CUS")
        self.assertIs(result, _CustomSegment)

    def test_get_unknown_returns_none(self):
        registry = GrammarRegistry()

        result = registry.get("UNKNOWN")
        self.assertIsNone(result)

    def test_has(self):
        registry = GrammarRegistry()
        registry.register(_CustomSegment)

        self.assertTrue(registry.has("CUS"))
        self.assertFalse(registry.has("NOPE"))

    def test_duplicate_register_raises_error(self):
        registry = GrammarRegistry()
        registry.register(_CustomSegment)

        with self.assertRaises(ValueError) as ctx:
            registry.register(_CustomSegment)
        self.assertIn("CUS", str(ctx.exception))

    def test_default_registry_has_envelope_segments(self):
        registry = create_default_registry()

        self.assertTrue(registry.has("ISA"))
        self.assertTrue(registry.has("IEA"))
        self.assertTrue(registry.has("GS"))
        self.assertTrue(registry.has("GE"))
        self.assertTrue(registry.has("ST"))
        self.assertTrue(registry.has("SE"))

    def test_default_registry_returns_correct_grammar(self):
        from pyx12lib.common.envelope.grammar import IsaSegment, StSegment
        registry = create_default_registry()

        self.assertIs(registry.get("ISA"), IsaSegment)
        self.assertIs(registry.get("ST"), StSegment)

    def test_register_all(self):
        registry = GrammarRegistry()
        registry.register_all([_LoopStart, _LoopChild1, _LoopChild2])

        self.assertTrue(registry.has("LS"))
        self.assertTrue(registry.has("LC1"))
        self.assertTrue(registry.has("LC2"))

    def test_register_loop(self):
        registry = GrammarRegistry()
        loop_def = LoopDefinition(_LoopStart, [_LoopChild1, _LoopChild2])
        registry.register_loop(loop_def)

        result = registry.get_loop("LS")
        self.assertIs(result, loop_def)

    def test_register_loop_auto_registers_grammars(self):
        registry = GrammarRegistry()
        loop_def = LoopDefinition(_LoopStart, [_LoopChild1, _LoopChild2])
        registry.register_loop(loop_def)

        self.assertTrue(registry.has("LS"))
        self.assertTrue(registry.has("LC1"))
        self.assertTrue(registry.has("LC2"))

    def test_has_loops(self):
        registry = GrammarRegistry()
        self.assertFalse(registry.has_loops)

        loop_def = LoopDefinition(_LoopStart, [_LoopChild1])
        registry.register_loop(loop_def)
        self.assertTrue(registry.has_loops)

    def test_duplicate_loop_start_raises(self):
        registry = GrammarRegistry()
        loop_def = LoopDefinition(_LoopStart, [_LoopChild1])
        registry.register_loop(loop_def)

        loop_def2 = LoopDefinition(_LoopStart, [_LoopChild2])
        with self.assertRaises(ValueError) as ctx:
            registry.register_loop(loop_def2)
        self.assertIn("LS", str(ctx.exception))

    def test_register_loop_type_error(self):
        registry = GrammarRegistry()
        with self.assertRaises(TypeError):
            registry.register_loop("not_a_loop_definition")

    def test_get_loop_unknown_returns_none(self):
        registry = GrammarRegistry()
        self.assertIsNone(registry.get_loop("UNKNOWN"))

    def test_register_loop_skips_already_registered_grammars(self):
        registry = GrammarRegistry()
        registry.register(_LoopStart)
        loop_def = LoopDefinition(_LoopStart, [_LoopChild1])
        # Should not raise even though _LoopStart is already registered
        registry.register_loop(loop_def)

        self.assertIs(registry.get("LS"), _LoopStart)
        self.assertTrue(registry.has("LC1"))
