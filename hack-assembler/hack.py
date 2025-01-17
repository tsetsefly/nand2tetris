# Python 'Hack'-assembler program for Nand2Tetris Part 1: Project 6
# https://www.coursera.org/learn/build-a-computer/programming/cLdpd/project-6

import os
import sys
from constants import PREDEFINED_SYMBOLS, COMP_0_TABLE, COMP_1_TABLE, DEST_TABLE, JUMP_TABLE
from typing import List, Dict, Optional, Tuple, Literal
from dataclasses import dataclass


@dataclass
class CInstructionParts:
  dest: Optional[str] = None
  comp: Optional[str] = None
  jump: Optional[str] = None


def parse_system_arguments() -> Tuple[str, str]:
  if len(sys.argv) != 3:
    print("Usage: python3 script.py input_file output_file")
    sys.exit(1)
  return sys.argv[1], sys.argv[2]


def validate_input_file(input_file) -> None:
  if not os.path.exists(input_file):
    print(f"Error: Input file '{input_file}' not found")
    sys.exit(1)


def read_input_file(input_file) -> List[str]:
  try:
    with open(input_file, 'r') as infile:
      return infile.readlines()
  except Exception as e:
    print(f"Error reading input file: {str(e)}")
    sys.exit(1)


class AssemblyFormatter:

  @staticmethod
  def format_line(line: str) -> Optional[str]:
    """Formats line to remove whitespace, spaces, comments"""
    line_parts = line.split("//", 1)
    formatted_line = line_parts[0].strip()
    return formatted_line or None


  @classmethod
  def read_and_format_input(cls, input_lines: List[str]) -> Tuple[List[str], Dict[str, str]]:
    """Initial pass through input to construct table for label symbols AND create formatted input list"""
    label_table: Dict[str,str] = {}
    label_counter = 0
    formatted_input: List[Optional[str]] = []

    for line in input_lines:
      formatted_line = cls.format_line(line)
      if formatted_line:
        formatted_input.append(formatted_line)

      # Continues if whitespace, empty line and/or full line comment
      if not formatted_line: 
        continue

      # Creates table of label symbols, requires full pass of input to populate
      if formatted_line[0] == "(":
        label_table[formatted_line[1:-1]] = str(label_counter)
      else:
        label_counter += 1

    return formatted_input, label_table


class BinaryConverter:

  @staticmethod
  def create_binary_number(binary_number: int) -> str:
    """Inputs a number and outputs a binary number as a string formatted for Hack binary"""
    return format(binary_number, '016b')


  @staticmethod
  def convert_abit_and_comp_binary(comp: str) -> tuple[str, str]:
    """Inputs 'comp' part of C-instruction and converts both 'a-bit' and 'comp' into binary"""
    if comp in COMP_0_TABLE:
      return "0", COMP_0_TABLE[comp]
    elif comp in COMP_1_TABLE:
      return "1", COMP_1_TABLE[comp]
    else:
      raise ValueError(f"Invalid comp instruction: {comp}")


  @classmethod
  def get_c_instruction_parts(cls, instruction: str) -> CInstructionParts:
    """
    Parses C-instructions into (up to) 3 distinct instruction parts

    Possible formats:
    - dest=comp;jump
    - dest=comp
    - comp;jump
    - comp
    """
    c_instruction_parts = CInstructionParts()

    # Split on '=' first if it exists in instructions
    if "=" in instruction:
      dest, rest = instruction.split("=", 1)
      c_instruction_parts.dest = dest
    else:
      rest = instruction

    # Split remaining part on ';' if it exists in instructions
    if ";" in rest:
      comp, jump = rest.split(";", 1)
      c_instruction_parts.comp = comp
      c_instruction_parts.jump = jump
    else:
      c_instruction_parts.comp = rest

    return c_instruction_parts


  @classmethod
  def convert_c_instruction(cls, instruction: str) -> str:
    """Takes C-instruction parts, then converts to binary"""
    c_instruction_parts = cls.get_c_instruction_parts(instruction)
    
    # Get binary values for each C-instruction part
    a_bit, comp_bits = cls.convert_abit_and_comp_binary(c_instruction_parts.comp)
    dest_bits = DEST_TABLE.get(c_instruction_parts.dest, "000")
    jump_bits = JUMP_TABLE.get(c_instruction_parts.jump, "000")
    
    # Construct final binary instruction
    return f"111{a_bit}{comp_bits}{dest_bits}{jump_bits}"


class HackAssembler:

  def __init__(self):
    self.var_counter = 16
    self.var_table: Dict[str, str] = {}


  def convert_at_sign_instruction(self, instruction: str, label_table: Dict[str, str]) -> str:
    """Determines appropriate binary conversions for different instructions with @ symbols"""
    value = instruction[1:]  # Removes @ symbol
    
    if value.isdigit():
        return BinaryConverter.create_binary_number(int(value))
        
    if value in PREDEFINED_SYMBOLS:
        return BinaryConverter.create_binary_number(int(PREDEFINED_SYMBOLS[value]))
        
    if value in label_table:
        return BinaryConverter.create_binary_number(int(label_table[value]))
        
    if value in self.var_table:
        return BinaryConverter.create_binary_number(int(self.var_table[value]))
        
    # If new variable detected
    self.var_table[value] = str(self.var_counter)
    result = BinaryConverter.create_binary_number(self.var_counter)
    self.var_counter += 1

    return result


  def assemble(self, formatted_input: List[str], label_table: Dict[str, str]) -> List[str]:
    """Take formatted instruction list, determines instruction type for each line and converts to binary"""
    binary_instructions = []

    for line in formatted_input:
      
      # Skip label declaration lines
      if line.startswith("("):
        continue

      # Convert variables / label symbol references to binary
      if line.startswith("@"): 
        binary = self.convert_at_sign_instruction(line, label_table)
      # Convert variables / label symbol references to binary
      else:
        binary = BinaryConverter.convert_c_instruction(line)

      binary_instructions.append(binary)

    return binary_instructions


def write_output_file(output_file, instructions) -> None:
  try:
    with open(output_file, 'w') as outfile:
      for line in instructions:
          outfile.write(line + '\n')
  except Exception as e:
    print(f"Error writing output file: {str(e)}")
    sys.exit(1)


def main():
  input_file, output_file = parse_system_arguments()
  validate_input_file(input_file)
  
  try:
    unformatted_input = read_input_file(input_file)
    
    formatted_input, label_table = AssemblyFormatter.read_and_format_input(unformatted_input)

    assembler = HackAssembler()
    binary_instructions = assembler.assemble(formatted_input, label_table)

    write_output_file(output_file, binary_instructions)

  except Exception as e:
    print(f"An error occured: {str(e)}")
    sys.exit(1)


if __name__ == "__main__":
  main()
