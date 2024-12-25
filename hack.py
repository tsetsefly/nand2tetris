import os
import sys

def create_binary_number_string(a_number):
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


def find_comp_type(comp, comp_0_table, comp_1_table):
	if comp in comp_0_table:
		return "0"

	if comp in comp_1_table:
		return "1"

	return None


def create_binary_c_instruct(parts):
	a_value = "0"

	comp_0_table = {
		"0":	"101010",
		"1":	"111111",
		"-1":	"111010",
		"D":	"001100",
		"A":	"110000",
		"!D":	"001101",
		"!A":	"110001",
		"-D":	"001111",
		"-A":	"110011",
		"D+1":	"011111",
		"A+1":	"110111",
		"D-1":	"001110",
		"A-1":	"110010",
		"D+A":	"000010",
		"D-A":	"010011",
		"A-D":	"000111",
		"D&A":	"000000",
		"D|A":	"010101"
	}
	comp_1_table = {
		"M":	"110000",
		"!M":	"110001",
		"-M":	"110011",
		"M+1":	"110111",
		"M-1":	"110010",
		"D+M":	"000010",
		"D-M":	"010011",
		"M-D":	"000111",
		"D&M":	"000000",
		"D|M":	"010101"
	}
	dest_table = {
		"null":	"000",
		"M":	"001",
		"D":	"010",
		"DM":	"011",
		"A":	"100",
		"AM":	"101",
		"AD":	"110",
		"ADM":	"111"
	}
	jump_table = {
		"null":	"000",
		"JGT":	"001",
		"JEQ":	"010",
		"JGE":	"011",
		"JLT":	"100",
		"JNE":	"101",
		"JLE":	"110",
		"JMP":	"111"
	}

	# finding destination binary value in table
	dest = dest_table.get(parts['dest'], "000")

	# finding comparison binary value in table
	comp_type = find_comp_type(parts['comp'], comp_0_table, comp_1_table)
	if comp_type == "0":
		comp = comp_0_table.get(parts['comp'], None)
	elif comp_type == "1":
		comp = comp_1_table.get(parts['comp'], None)
		a_value = "1"
	
	# finding jump binary value in table
	if parts['jump']:
		jump = jump_table.get(parts['jump'], "000")
	else:
		jump = "000"

	c_instruct_binary = "111" + a_value + comp + dest + jump

	return c_instruct_binary


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
		with open(input_file, 'r') as infile:
			lines = infile.readlines()

			processed_lines = []
			for line in lines:
				line = line.strip()
				# add stuff here
				processed_lines.append(line)

		with open(output_file, 'w') as outfile:
			for line in processed_lines:
				outfile.write(line + '\n')

	except Exception as e:
		print(f"An error occured: {str(e)}")
		sys.exit(1)


	a_number_string = "7" # test code
	a_number = int(a_number_string)
	a_instruct = create_binary_number_string(a_number)
	# print(a_instruct) # test code
	# print(type(a_instruct)) # test code

	c_instruct_string = "A=-1"
	c_instruct_parts = parse_c_instruction(c_instruct_string)
	c_instruct = create_binary_c_instruct(c_instruct_parts)
	print(c_instruct)
	# print(f"\nInstruction: {c_instruct_string}") # test code
	# print(f"Destination: {c_instruct_parts['dest']}") # test code
	# print(f"Computation: {c_instruct_parts['comp']}") # test code
	# print(f"Jump: {c_instruct_parts['jump']}") # test code

if __name__ == "__main__":
    main()
