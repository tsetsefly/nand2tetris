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

  def test_read_and_format_input_processes_labels(self):
    """Test that labels are properly processed and counted"""
    input_lines = [
      "@100",     # counter becomes 1
      "(LOOP)",   # LOOP gets value 1
      "D=M",      # counter becomes 2
      "(END)",    # END gets value 2
      "@LOOP"     # counter becomes 3
    ]
    formatted_input, label_table = self.formatter.read_and_format_input(input_lines)
    
    expected_formatted = ["@100", "(LOOP)", "D=M", "(END)", "@LOOP"]
    expected_labels = {"LOOP": "1", "END": "2"}  # Changed from "3" to "2"
    
    self.assertEqual(formatted_input, expected_formatted)
    self.assertEqual(label_table, expected_labels)