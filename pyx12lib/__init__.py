from pyx12lib.core.parser import SegmentParser, X12Parser
from pyx12lib.core.registry import GrammarRegistry, create_default_registry
from pyx12lib.core.delimiters import detect_delimiters, Delimiters


def parse_x12(x12_string, registry=None):
    """Parse an X12 string into a Python dict.

    Args:
        x12_string: Raw X12 EDI string.
        registry: Optional GrammarRegistry. Uses default envelope
                  segments (ISA/IEA/GS/GE/ST/SE) if not provided.

    Returns:
        Dict with 'segments' key containing list of parsed segment dicts.
    """
    parser = X12Parser(x12_string, registry=registry)
    return parser.to_dict()


def parse_x12_to_json(x12_string, indent=2, registry=None):
    """Parse an X12 string into a JSON string.

    Args:
        x12_string: Raw X12 EDI string.
        indent: JSON indentation level. None for compact output.
        registry: Optional GrammarRegistry. Uses default envelope
                  segments (ISA/IEA/GS/GE/ST/SE) if not provided.

    Returns:
        JSON string representation of the parsed X12 data.
    """
    parser = X12Parser(x12_string, registry=registry)
    return parser.to_json(indent=indent)
