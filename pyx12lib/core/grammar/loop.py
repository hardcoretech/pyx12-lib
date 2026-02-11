from pyx12lib.core.grammar.segment import BaseSegment


class LoopDefinition(object):
    """Defines a loop structure for X12 parsing.

    A loop starts with a specific segment type and contains child segments
    and/or nested loop definitions.

    Args:
        start_segment: BaseSegment subclass that triggers a new loop instance.
        children: List of BaseSegment subclasses or nested LoopDefinition objects.

    Raises:
        TypeError: If start_segment is not a BaseSegment subclass.
        TypeError: If any child is neither a BaseSegment subclass nor LoopDefinition.
    """

    def __init__(self, start_segment, children=None):
        if not _is_segment_class(start_segment):
            raise TypeError(
                "start_segment must be a BaseSegment subclass, got {}".format(
                    type(start_segment)
                )
            )

        self._start_segment = start_segment
        self._children = children or []

        self._child_segment_grammars = []
        self._child_loops = []

        for child in self._children:
            if isinstance(child, LoopDefinition):
                self._child_loops.append(child)
            elif _is_segment_class(child):
                self._child_segment_grammars.append(child)
            else:
                raise TypeError(
                    "Each child must be a BaseSegment subclass or "
                    "LoopDefinition, got {}".format(type(child))
                )

        self._child_segment_ids = frozenset(
            g.segment_id for g in self._child_segment_grammars
        )

    @property
    def loop_id(self):
        return self._start_segment.segment_id

    @property
    def start_segment_id(self):
        return self._start_segment.segment_id

    @property
    def start_segment_grammar(self):
        return self._start_segment

    @property
    def child_segment_ids(self):
        return self._child_segment_ids

    @property
    def child_segment_grammars(self):
        return list(self._child_segment_grammars)

    @property
    def child_loops(self):
        return list(self._child_loops)

    def is_start(self, segment_id):
        return segment_id == self._start_segment.segment_id

    def is_child(self, segment_id):
        return segment_id in self._child_segment_ids

    def all_segment_grammars(self):
        """Yield all grammar classes recursively (start + children + nested)."""
        yield self._start_segment
        for grammar in self._child_segment_grammars:
            yield grammar
        for child_loop in self._child_loops:
            for grammar in child_loop.all_segment_grammars():
                yield grammar


def _is_segment_class(obj):
    """Check if obj is a class that is a subclass of BaseSegment."""
    return isinstance(obj, type) and issubclass(obj, BaseSegment)
