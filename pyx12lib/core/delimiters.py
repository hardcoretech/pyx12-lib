"""Delimiter detection from ISA segment header.

In X12, the ISA segment defines the delimiters used throughout the interchange:
- Character at position 3 is the element delimiter (typically '*')
- ISA16 value is the component separator (typically '^')
- Character immediately after the ISA segment is the segment terminator (typically '~')
"""

from pyx12lib.core.grammar.segment import ELEMENT_DELIMITER, SEGMENT_TERMINATOR
from pyx12lib.core.grammar.element import COMPONENT_DELIMITER

# ISA segment is always exactly 106 characters (including the segment terminator)
ISA_SEGMENT_LENGTH = 106


class Delimiters(object):
    """Container for X12 delimiter characters."""

    def __init__(self, element_delimiter, component_delimiter, segment_terminator):
        self.element_delimiter = element_delimiter
        self.component_delimiter = component_delimiter
        self.segment_terminator = segment_terminator

    def __eq__(self, other):
        if not isinstance(other, Delimiters):
            return NotImplemented
        return (
            self.element_delimiter == other.element_delimiter
            and self.component_delimiter == other.component_delimiter
            and self.segment_terminator == other.segment_terminator
        )

    def __repr__(self):
        return "Delimiters(element='{}', component='{}', terminator='{}')".format(
            self.element_delimiter, self.component_delimiter, self.segment_terminator
        )


DEFAULT_DELIMITERS = Delimiters(
    element_delimiter=ELEMENT_DELIMITER,
    component_delimiter=COMPONENT_DELIMITER,
    segment_terminator=SEGMENT_TERMINATOR,
)


def detect_delimiters(raw_x12):
    """Detect delimiters from the ISA segment header.

    Args:
        raw_x12: Raw X12 string starting with ISA.

    Returns:
        Delimiters object with the detected characters.

    Raises:
        ValueError: If the string doesn't start with ISA or is too short.
    """
    stripped = raw_x12.lstrip()
    if not stripped.startswith('ISA'):
        raise ValueError("X12 data must start with ISA segment for delimiter detection")

    if len(stripped) < ISA_SEGMENT_LENGTH:
        raise ValueError(
            "ISA segment requires at least {} characters, got {}".format(
                ISA_SEGMENT_LENGTH, len(stripped)
            )
        )

    element_delimiter = stripped[3]
    segment_terminator = stripped[ISA_SEGMENT_LENGTH - 1]

    # ISA16 is the component separator. Count 16 element delimiters to find it.
    # ISA has exactly 16 elements, so there are 16 element delimiters.
    # The component separator is the value of the 16th element (ISA16),
    # which is between the 16th delimiter and the segment terminator.
    delimiter_count = 0
    for i, ch in enumerate(stripped):
        if ch == element_delimiter:
            delimiter_count += 1
            if delimiter_count == 16:
                if i + 1 >= len(stripped):
                    raise ValueError(
                        "ISA segment truncated after 16th element delimiter"
                    )
                component_delimiter = stripped[i + 1]
                break
    else:
        raise ValueError("Could not find 16 element delimiters in ISA segment")

    return Delimiters(
        element_delimiter=element_delimiter,
        component_delimiter=component_delimiter,
        segment_terminator=segment_terminator,
    )
