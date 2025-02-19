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

