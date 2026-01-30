from pyx12lib.common.envelope.grammar import (
    IsaSegment, IeaSegment,
    GsSegment, GeSegment,
    StSegment, SeSegment,
)


class GrammarRegistry(object):
    """Registry mapping segment IDs to their grammar definitions."""

    def __init__(self):
        self._registry = {}

    def register(self, segment_grammar):
        segment_id = segment_grammar.segment_id
        if segment_id in self._registry:
            raise ValueError(
                "Segment '{}' already registered".format(segment_id)
            )
        self._registry[segment_id] = segment_grammar

    def get(self, segment_id):
        return self._registry.get(segment_id)

    def has(self, segment_id):
        return segment_id in self._registry


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
