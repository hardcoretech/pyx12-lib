from unittest import TestCase

from pyx12lib.core.delimiters import detect_delimiters, Delimiters, DEFAULT_DELIMITERS


class TestDetectDelimiters(TestCase):
    def test_standard_delimiters(self):
        # arrange: standard ISA with * ^ ~
        x12_string = (
            "ISA*00*          *00*          *ZZ*SENDER         "
            "*ZZ*RECEIVER       *210101*1200*^*00501*000000001*0*P*>~"
        )

        # action
        result = detect_delimiters(x12_string)

        # assert
        self.assertEqual(result.element_delimiter, '*')
        self.assertEqual(result.component_delimiter, '>')
        self.assertEqual(result.segment_terminator, '~')

    def test_non_standard_element_delimiter(self):
        # arrange: using | as element delimiter
        x12_string = (
            "ISA|00|          |00|          |ZZ|SENDER         "
            "|ZZ|RECEIVER       |210101|1200|^|00501|000000001|0|P|>~"
        )

        # action
        result = detect_delimiters(x12_string)

        # assert
        self.assertEqual(result.element_delimiter, '|')
        self.assertEqual(result.component_delimiter, '>')
        self.assertEqual(result.segment_terminator, '~')

    def test_non_standard_segment_terminator(self):
        # arrange: using \n as segment terminator
        x12_string = (
            "ISA*00*          *00*          *ZZ*SENDER         "
            "*ZZ*RECEIVER       *210101*1200*^*00501*000000001*0*P*>\n"
        )

        # action
        result = detect_delimiters(x12_string)

        # assert
        self.assertEqual(result.element_delimiter, '*')
        self.assertEqual(result.segment_terminator, '\n')

    def test_non_standard_component_delimiter(self):
        # arrange: using : as component separator (ISA16)
        x12_string = (
            "ISA*00*          *00*          *ZZ*SENDER         "
            "*ZZ*RECEIVER       *210101*1200*^*00501*000000001*0*P*:~"
        )

        # action
        result = detect_delimiters(x12_string)

        # assert
        self.assertEqual(result.component_delimiter, ':')

    def test_leading_whitespace_stripped(self):
        # arrange
        x12_string = (
            "  \n  ISA*00*          *00*          *ZZ*SENDER         "
            "*ZZ*RECEIVER       *210101*1200*^*00501*000000001*0*P*>~"
        )

        # action
        result = detect_delimiters(x12_string)

        # assert
        self.assertEqual(result.element_delimiter, '*')

    def test_no_isa_raises_error(self):
        # arrange
        x12_string = "GS*FA*SENDER*RECEIVER~"

        # action & assert
        with self.assertRaises(ValueError) as ctx:
            detect_delimiters(x12_string)
        self.assertIn("ISA", str(ctx.exception))

    def test_too_short_raises_error(self):
        # arrange
        x12_string = "ISA*00*short"

        # action & assert
        with self.assertRaises(ValueError) as ctx:
            detect_delimiters(x12_string)
        self.assertIn("106", str(ctx.exception))

    def test_default_delimiters_constant(self):
        self.assertEqual(DEFAULT_DELIMITERS.element_delimiter, '*')
        self.assertEqual(DEFAULT_DELIMITERS.component_delimiter, '^')
        self.assertEqual(DEFAULT_DELIMITERS.segment_terminator, '~')

    def test_delimiters_equality(self):
        d1 = Delimiters('*', '^', '~')
        d2 = Delimiters('*', '^', '~')
        d3 = Delimiters('|', '^', '~')

        self.assertEqual(d1, d2)
        self.assertNotEqual(d1, d3)

    def test_delimiters_repr(self):
        d = Delimiters('*', '^', '~')
        self.assertIn('*', repr(d))
        self.assertIn('^', repr(d))
        self.assertIn('~', repr(d))


class TestX12ParserWithAutoDetection(TestCase):
    """Test that X12Parser uses auto-detected delimiters."""

    def test_auto_detect_with_standard_isa(self):
        from pyx12lib.core.parser import X12Parser

        x12_string = (
            "ISA*00*          *00*          *ZZ*SENDER         "
            "*ZZ*RECEIVER       *210101*1200*^*00501*000000001*0*P*>~"
            "GS*FA*SENDER*RECEIVER*20210101*1200*1*X*005010~"
            "ST*997*0001~"
            "SE*1*0001~"
            "GE*1*1~"
            "IEA*1*000000001~"
        )

        parser = X12Parser()
        result = parser.parse(x12_string).to_dict()

        self.assertEqual(len(result['segments']), 6)

    def test_auto_detect_disabled_uses_defaults(self):
        from pyx12lib.core.parser import X12Parser

        x12_string = "ST*997*0001~SE*1*0001~"

        parser = X12Parser(auto_detect_delimiters=False)
        result = parser.parse(x12_string).to_dict()

        self.assertEqual(len(result['segments']), 2)

    def test_no_isa_falls_through_to_defaults(self):
        from pyx12lib.core.parser import X12Parser

        # No ISA present, auto_detect=True but should use defaults gracefully
        x12_string = "ST*997*0001~SE*1*0001~"

        parser = X12Parser(auto_detect_delimiters=True)
        result = parser.parse(x12_string).to_dict()

        self.assertEqual(len(result['segments']), 2)
