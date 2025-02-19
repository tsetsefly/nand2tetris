# nand2tetris: Hack Assembler

## [Project 6](https://www.coursera.org/learn/build-a-computer/programming/cLdpd/project-6)
[Project description](https://drive.google.com/file/d/1CITliwTJzq19ibBF5EeuNBZ3MJ01dKoI/view)
[Module 8 lecture notes](https://drive.google.com/file/d/1uKGRMnL-gqk9DsgeN50z0EpHoSMWe6F5/view)

An assembler that translates programs written in the Hack assembly language into binary code for the Hack computer platform (Nand2Tetris Project 6).

## Overview

This assembler translates symbolic Hack assembly language (.asm) files into Hack machine code (.hack) files. The Hack assembly language is a low-level programming language designed for the Hack computer platform.

## Features

- Translates Hack assembly programs into 16-bit binary machine code
- Supports both symbolic and non-symbolic references
- Handles variables and labels
- Processes standard Hack assembly instructions (A-instructions and C-instructions)
- Handles common assembly programming patterns
- Manages label definitions (LOOP, END, etc.)
- Supports variable allocation

## Implementation Details

The assembler follows a two-pass approach:

1. **First Pass**: 
   - Builds the symbol table
   - Handles label declarations (xxx)
   - No code generation in this phase

2. **Second Pass**:
   - Handles A-instructions (@xxx)
   - Handles C-instructions (dest=comp;jump)
   - Manages variable declarations
   - Generates final binary code

## Test Programs

The assembler has been tested with the following programs:

- **Add.asm**: Adds constants 2 and 3, storing result in R0
- **Max.asm**: Computes max(R0, R1) and stores result in R2
- **Rect.asm**: Draws a 16-pixel wide rectangle with height R0
- **Pong.asm**: Basic implementation of a single-player Pong game

Test programs are available in two versions:
- With symbolic references (e.g., Max.asm)
- Without symbolic references (e.g., MaxL.asm)

## Usage

```bash
python3 hack.py <input.asm> <output.hack>
```

This will generate an output file named `<output.hack>` in the same directory as the input file.

```
python3 -m unittest discover tests
```

This will run whatever tests are set up in ```tests/test_hack.py```

## Known Issues

- According to the Hack language specification, both forms of multiple destination instructions are accepted:
  - DM=... and MD=... (both valid for d-bits 011)
  - ADM=... and AMD=... (both valid for d-bits 111)

## Development Notes

The assembler was developed in two stages:

1. Basic assembler handling non-symbolic reference programs
2. Extended assembler with full symbol handling capabilities

## Testing

To test the assembler:

1. Run the assembler on a test program
2. Compare output with the official assembler using the Nand2Tetris tools
3. Test the generated .hack file in the CPU emulator

## References

- Based on the Nand2Tetris Project 6 specifications
- Part of the "From Nand to Tetris" course
- [Official Nand2Tetris Website](http://www.nand2tetris.org)

## Other

### [venv tutorial](https://www.youtube.com/watch?v=N5vscPTWKOk)
Create a new virtual environment:
```
python -m venv myproject_env
```

Activate virtual environment
```
source myproject_env/bin/activate
```

Deactivate virtual environment
```
deactivate
```

*NOTE:* make sure you've added your venv directory to your ```.gitignore```, example:
```
# Add to .gitignore
venv/
env/
.env/
```