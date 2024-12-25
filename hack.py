import os
import sys

def create_binary_string(a_number):
	no_pad_binary = bin(a_number)[2:]
	pad_binary = no_pad_binary.zfill(16)
	return pad_binary



def parse_c_instruction(instruction):
    # Initialize parts
    dest = None
    comp = None
    jump = None
    
    # Check for '=' first
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

def main():
    a_number_string = "7" # test code
    a_number = int(a_number_string)
    a_instruct = create_binary_string(a_number)
    # print(a_instruct) # test code
    # print(type(a_instruct)) # test code

    c_instruct_string = "AM=M+1"
    c_instruct_parts = parse_c_instruction(c_instruct_string)
    # print(f"\nInstruction: {c_instruct_string}") # test code
    # print(f"Destination: {c_instruct_parts['dest']}") # test code
    # print(f"Computation: {c_instruct_parts['comp']}") # test code
    # print(f"Jump: {c_instruct_parts['jump']}") # test code

if __name__ == "__main__":
    main()
