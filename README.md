Name: Lauren Caccamise
Project 1
UCF ID: 5142333

# Description:
This program implements the Quine-McCluskey algorithm for boolean function minimization. It processes input PLA files to identify prime implicants, selects essential prime implicants, and writes a minimized PLA file as output.

# Requirements:
Python 3.x (No additional libraries required)
Uses the following Python standard libraries:
itertools (for generating combinations in pattern expansion)
sys (for handling command-line arguments)

# How to Run the Program:
## Running the Algorithm:
### Clone the repository to your local machine:
git clone <repository_link>
cd qm-algorithm
### Run the following command to minimize a PLA file:
python qm.py tests/input0.pla output.pla
### Validate the output by comparing the generated file (output.pla) with the expected output:
diff output.pla tests/expected_outputs/output0.pla

# Testing in ABC:
## Strashing:
The input and calculated output circuits were strashed (structurally hashed) using ABC to optimize their representations.
## CEC Comparison:
A Combinational Equivalence Check (CEC) was performed between the input and output circuits to confirm their logical equivalence.
This ensures that the minimized PLA file maintains the same logical functionality as the original input.

# Files Included:
qm.py: The Python script implementing the Quine-McCluskey algorithm.
tests/input0.pla: A sample PLA input file for testing.
tests/expected_outputs/output0.pla: The expected output file for the given input.
tests/input1.pla: A sample PLA input file for testing.
tests/expected_outputs/output1.pla: The expected output file for the given input.
README.md: This file, providing instructions on how to run and test the program.
writeup.md: A file, detailing challenges, solutions, and verification of functionality.

# Notes:
The program accurately minimizes PLA files and supports don't-care conditions.
Outputs have been verified using the ABC tool to ensure logical equivalence between inputs and outputs.
Use the diff command for quick validation of outputs against expected files.