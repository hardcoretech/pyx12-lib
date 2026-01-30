from unittest import TestCase

from pyx12lib.core.grammar import BaseSegment, Element, element, segment
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
