import unittest
from unittest.mock import patch, mock_open
from hack import (
    AssemblyFormatter, 
    BinaryConverter,
    HackAssembler,
    CInstructionParts,
    parse_system_arguments,
    validate_input_file,
    read_input_file
)

class TestAssemblyFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = AssemblyFormatter()

    def test_format_line_removes_comments(self):
        """Test that comments are properly removed from lines"""
        test_cases = [
            ("@100 // initialize i=100", "@100"),
            ("// full line comment", None),
            ("D=M//get value", "D=M"),
            ("   @R0   // comment", "@R0"),
        ]
        for input_line, expected in test_cases:
            with self.subTest(input_line=input_line):
                result = self.formatter.format_line(input_line)
                self.assertEqual(result, expected)
