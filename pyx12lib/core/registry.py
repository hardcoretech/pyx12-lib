from pyx12lib.common.envelope.grammar import (
    IsaSegment, IeaSegment,
    GsSegment, GeSegment,
    StSegment, SeSegment,
)
from pyx12lib.core.grammar.loop import LoopDefinition


class GrammarRegistry(object):
    """Registry mapping segment IDs to their grammar definitions."""

    def __init__(self):
        self._registry = {}
        self._loop_definitions = {}

    def register(self, segment_grammar):
        segment_id = segment_grammar.segment_id
        if segment_id in self._registry:
            raise ValueError(
                "Segment '{}' already registered".format(segment_id)
            )
        self._registry[segment_id] = segment_grammar

    def register_all(self, segment_grammars):
        """Register a list of segment grammar classes."""
        for grammar in segment_grammars:
            self.register(grammar)

    def register_loop(self, loop_definition):
        """Register a loop definition and auto-register all its segment grammars.

        Args:
            loop_definition: A LoopDefinition instance.

        Raises:
            TypeError: If loop_definition is not a LoopDefinition.
            ValueError: If a loop with the same start_segment_id is already registered.
        """
        if not isinstance(loop_definition, LoopDefinition):
            raise TypeError(
                "Expected LoopDefinition, got {}".format(type(loop_definition))
            )

        start_id = loop_definition.start_segment_id
        if start_id in self._loop_definitions:
            raise ValueError(
                "Loop with start segment '{}' already registered".format(start_id)
            )

        self._loop_definitions[start_id] = loop_definition

        for grammar in loop_definition.all_segment_grammars():
            if not self.has(grammar.segment_id):
                self.register(grammar)

    def get(self, segment_id):
        return self._registry.get(segment_id)

    def get_loop(self, start_segment_id):
        return self._loop_definitions.get(start_segment_id)

    def has(self, segment_id):
        return segment_id in self._registry

    @property
    def has_loops(self):
        return bool(self._loop_definitions)


def create_default_registry():
    """Create a registry with standard envelope segments pre-registered."""
    registry = GrammarRegistry()
    registry.register(IsaSegment)
    registry.register(IeaSegment)
    registry.register(GsSegment)
    registry.register(GeSegment)
    registry.register(StSegment)
    registry.register(SeSegment)
    return registry
