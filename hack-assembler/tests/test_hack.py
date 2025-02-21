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
        result = AssemblyFormatter.format_line(input_line)
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
    expected_labels = {"LOOP": "1", "END": "2"}
    
    self.assertEqual(formatted_input, expected_formatted)
    self.assertEqual(label_table, expected_labels)


class TestBinaryConverter(unittest.TestCase):
  def test_create_binary_number(self):
    """Test binary number conversion"""
    test_cases = [
      (0, "0000000000000000"),
      (1, "0000000000000001"),
      (16384, "0100000000000000"),  # SCREEN address
      (24576, "0110000000000000"),  # KBD address
    ]
    for input_num, expected in test_cases:
      with self.subTest(input_num=input_num):
        result = BinaryConverter.create_binary_number(input_num)
        self.assertEqual(result, expected)