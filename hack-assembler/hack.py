# Python 'Hack'-assembler program for Nand2Tetris Part 1: Project 6
# https://www.coursera.org/learn/build-a-computer/programming/cLdpd/project-6

import os
import sys
from constants import PREDEFINED_SYMBOLS, COMP_0_TABLE, COMP_1_TABLE, DEST_TABLE, JUMP_TABLE
from typing import List, Dict, Optional, Tuple


# Inputs a-instruction and outputs 16-bit binary instruction, a 15-bit binary number
def create_binary_number_string(a_number):
  no_pad_binary = bin(a_number)[2:]
  pad_binary = no_pad_binary.zfill(16)
  return pad_binary


# Parses different types of instructions for C-instruction parts
def parse_c_instruction(instruction):
  # Initialize parts of C-instruction segments
  dest = None
  comp = None
  jump = None

  # Check for presence of '=' first
  if "=" in instruction:
    dest, rest = instruction.split("=", 1)  # Split on first '=' only
  else:
    rest = instruction
    dest = None

  # Check for ';' in the remaining part
  if ";" in rest:
    comp, jump = rest.split(";", 1)  # Split on first ';' only
  else:
    comp = rest
    jump = None

  return {
    "dest": dest,
    "comp": comp,
    "jump": jump
  }


# Determines whether comparison value is referencing table 0 or table 1
def find_comp_type(comp):
  if comp in COMP_0_TABLE:
    return "0"

  if comp in COMP_1_TABLE:
    return "1"

  return None


# Converting hack C-instructions to binary instructions
def create_binary_c_instruct(parts):
  a_value = "0"
  comp = "0"

  # Finding destination binary value in table
  dest = DEST_TABLE.get(parts['dest'], "000")

  # Finding comparison binary value in table
  comp_type = find_comp_type(parts['comp'])
  if comp_type == "0":
    comp = COMP_0_TABLE.get(parts['comp'], None)
  elif comp_type == "1":
    comp = COMP_1_TABLE.get(parts['comp'], None)
    a_value = "1"
  
  # Finding jump binary value in table
  if parts['jump']:
    jump = JUMP_TABLE.get(parts['jump'], "000")
  else:
    jump = "000"

  c_instruct_binary = "111" + a_value + comp + dest + jump # Constructing binary C-instruction

  return c_instruct_binary


# formats line to remove whitespace, spaces, comments
def format_line(line: str) -> Optional[str]:
  line_parts = line.split("//", 1)
  formatted_line = line_parts[0].strip()
  return formatted_line or None


# initial pass through code to construct table for label symbols
def read_and_format_input(input_lines: List[str]) -> Tuple[List[Optional[str]], Dict[str, str]]:
  label_table: Dict[str,str] = {}
  label_counter = 0
  formatted_input: List[Optional[str]] = []

  for line in input_lines:
    formatted_line = format_line(line)
    formatted_input.append(formatted_line)

    # creates table of label symbols, requires full pass of input to populate
    if not formatted_line: # continue if whitespace, empty line and/or full line comment
      continue
    if formatted_line[0] == "(": # creates dictionary entry for label
      label_table[formatted_line[1:-1]] = str(label_counter)
    else:
      label_counter += 1

  return formatted_input, label_table


def process_instructions(lines, label_table):
  var_counter = 16
  var_table = {}
  processed_lines = []

  for line in lines:
    cleaned_line = format_line(line)
    
    if cleaned_line is not None:
      # Handling A-instructions
      if cleaned_line[0] == "@" and cleaned_line[1:].isdigit():
        a_number = int(cleaned_line.split("@")[1])
        cleaned_line = create_binary_number_string(a_number)
      
      # Checking for predefined symbols
      elif cleaned_line[0] == "@" and cleaned_line.split("@")[1] in PREDEFINED_SYMBOLS:
        cleaned_line = create_binary_number_string(int(PREDEFINED_SYMBOLS.get(cleaned_line.split("@")[1])))
      
      # Checking for label symbols
      elif cleaned_line[0] == "@" and cleaned_line.split("@")[1] in label_table:
        cleaned_line = create_binary_number_string(int(label_table.get(cleaned_line.split("@")[1])))
      
      # Checking for variable symbols
      elif cleaned_line[0] == "@" and cleaned_line.split("@")[1]:
        if cleaned_line.split("@")[1] in var_table:
          cleaned_line = create_binary_number_string(int(var_table.get(cleaned_line.split("@")[1])))
        else:
          var_table.update({
              cleaned_line.split("@")[1]:str(var_counter)
          })
          cleaned_line = create_binary_number_string(var_counter)
          var_counter += 1
      
      # Skipping binary instruction creation for lines with label symbol initiation
      elif cleaned_line[0] == "(":
        continue
      
      # Converting C-instructions to binary
      else:
        c_instruct_parts = parse_c_instruction(cleaned_line) # Creates dictionary with C-instruction parts
        cleaned_line = create_binary_c_instruct(c_instruct_parts) # Combines C-instruction parts together to store as binary instruction
      
      processed_lines.append(cleaned_line)

  return processed_lines


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
    label_table = {}
    processed_lines = []
    formatted_input: List[Optional[str]] = []
    
    with open(input_file, 'r') as infile:
      unformatted_input = infile.readlines()

    formatted_input, label_table = read_and_format_input(unformatted_input)
    processed_lines = process_instructions(unformatted_input, label_table)

    with open(output_file, 'w') as outfile:
      for line in processed_lines:
        outfile.write(line + '\n')

  except Exception as e:
    print(f"An error occured: {str(e)}")
    sys.exit(1)


if __name__ == "__main__":
  main()
