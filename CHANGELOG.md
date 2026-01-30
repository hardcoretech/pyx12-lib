Changelog
=========

0.4
-----

Changes:

- Add X12 parsing support (X12 -> JSON/Python dict).
- Add `SegmentParser` for parsing individual segments against a grammar.
- Add `X12Parser` for parsing complete X12 documents with auto-detection.
- Add `GrammarRegistry` for mapping segment IDs to grammar definitions.
- Add `ParsedSegment`, `ParsedElement`, `ParsedCompositeElement`, `ParsedComponent`, `ParsedLoop` data structures.
- Add `detect_delimiters()` for automatic ISA delimiter detection.
- Add `parse_x12()` and `parse_x12_to_json()` convenience functions.

0.3
-----

Changes:

- Rename common module `interchange` to `envelop` for fitting X12's language.

0.2
-----

Changes:

- Drop support to Python 2.7.
- Add store rendered values on objects for renderer segments and rendered elements.

0.1
-----

Changes:

- Start this project by extracting the code from a private repository. 
