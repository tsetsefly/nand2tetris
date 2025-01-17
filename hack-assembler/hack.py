# Python 'Hack'-assembler program for Nand2Tetris Part 1: Project 6
# https://www.coursera.org/learn/build-a-computer/programming/cLdpd/project-6

import os
import sys
from constants import PREDEFINED_SYMBOLS, COMP_0_TABLE, COMP_1_TABLE, DEST_TABLE, JUMP_TABLE
from typing import List, Dict, Optional, Tuple, Literal
from dataclasses import dataclass


@dataclass
class CInstruction:
    dest: Optional[str] = None
    comp: Optional[str] = None
    jump: Optional[str] = None


# Initial pass through input to construct table for label symbols AND create formatted input list
def read_and_format_input(input_lines: List[str]) -> Tuple[List[Optional[str]], Dict[str, str]]:
  label_table: Dict[str,str] = {}
  label_counter = 0
  formatted_input: List[Optional[str]] = []

  for line in input_lines:
    formatted_line = format_line(line)
    if formatted_line:
      formatted_input.append(formatted_line)

    # creates table of label symbols, requires full pass of input to populate
    if not formatted_line: # continue if whitespace, empty line and/or full line comment
      continue
    if formatted_line[0] == "(": # creates label definition
      label_table[formatted_line[1:-1]] = str(label_counter)
    else:
      label_counter += 1

  return formatted_input, label_table


# Formats line to remove whitespace, spaces, comments
def format_line(line: str) -> Optional[str]:
  line_parts = line.split("//", 1)
  formatted_line = line_parts[0].strip()
  return formatted_line or None


def convert_instructions_to_binary(formatted_input: list[str], label_table: dict) -> list[str]:
  var_counter = 16
  var_table = {}
  converted_instructions = []

  for line in formatted_input:
    
    # Skip label declaration lines
    if line.startswith("("):
      continue

    # Convert variables / label symbol references to binary
    if line.startswith("@"):
      binary_line, var_table, var_counter = convert_at_sign_instruction(line, var_table, label_table, var_counter)
      converted_instructions.append(binary_line)
      continue

    # Convert C-instructions to binary
    binary_line = convert_c_instruction(line)
    converted_instructions.append(binary_line)

  return converted_instructions


  def convert_at_sign_instruction(instruction: str, var_table: dict, label_table: dict, var_counter: int) -> tuple[str, dict, int]:
    value = instruction[1:]  # Removes @ symbol
    
    # If instruction is an existing case (no changes required to var_table or counter variables)
    if value.isdigit():
        return create_binary_number_string(int(value)), var_table, var_counter
        
    if value in PREDEFINED_SYMBOLS:
        return create_binary_number_string(int(PREDEFINED_SYMBOLS[value])), var_table, var_counter
        
    if value in label_table:
        return create_binary_number_string(int(label_table[value])), var_table, var_counter
        
    if value in var_table:
        return create_binary_number_string(int(var_table[value])), var_table, var_counter
        
    # If new variable detected
    var_table[value] = str(var_counter)
    result = create_binary_number_string(var_counter)

    return result, var_table, var_counter + 1


# Inputs a number and outputs a binary number as a string formatted for Hack binary
def create_binary_number_string(binary_number: int) -> str:
    return format(binary_number, '016b')


def convert_c_instruction(instruction: str) -> str:
    parsed = parse_c_instruction(instruction)
    
    # Get binary values for each part
    a_bit, comp_bits = get_comp_binary(parsed.comp)
    dest_bits = DEST_TABLE.get(parsed.dest, "000")
    jump_bits = JUMP_TABLE.get(parsed.jump, "000")
    
    # Construct final binary instruction
    return f"111{a_bit}{comp_bits}{dest_bits}{jump_bits}"


def parse_c_instruction(instruction: str) -> CInstruction:
    """Parse a C-instruction into its components.
    
    Possible formats:
    - dest=comp;jump
    - dest=comp
    - comp;jump
    - comp
    """
    c_instruction = CInstruction()
    
    # Split on '=' first if it exists
    if "=" in instruction:
        dest, rest = instruction.split("=", 1)
        c_instruction.dest = dest
    else:
        rest = instruction
    
    # Split remaining part on ';' if it exists
    if ";" in rest:
        comp, jump = rest.split(";", 1)
        c_instruction.comp = comp
        c_instruction.jump = jump
    else:
        c_instruction.comp = rest
    
    return c_instruction


def get_comp_binary(comp: str) -> tuple[str, str]:
    # Returns (a_bit, comp_bits)
    if comp in COMP_0_TABLE:
        return "0", COMP_0_TABLE[comp]
    elif comp in COMP_1_TABLE:
        return "1", COMP_1_TABLE[comp]
    else:
        raise ValueError(f"Invalid comp instruction: {comp}")





def main():
  if len(sys.argv) != 3:
    print("Usage: python3 script.py input_file output_file")
    sys.exit(1)

  input_file = sys.argv[1]
  output_file = sys.argv[2]

  if not os.path.exists(input_file):
    print(f"Error: Input file '{input_file}' not found")
    sys.exit(1)

  try:
    unformatted_input = []
    label_table = {}
    converted_instructions = []
    formatted_input: List[Optional[str]] = []

    with open(input_file, 'r') as infile:
      unformatted_input = infile.readlines()

    formatted_input, label_table = read_and_format_input(unformatted_input)
    converted_instructions = convert_instructions_to_binary(formatted_input, label_table)

    with open(output_file, 'w') as outfile:
      for line in converted_instructions:
        outfile.write(line + '\n')

  except Exception as e:
    print(f"An error occured: {str(e)}")
    sys.exit(1)


if __name__ == "__main__":
  main()
