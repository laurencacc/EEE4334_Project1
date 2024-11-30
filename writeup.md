
Challenges and Solutions

# Parsing Input Data:
Challenge: Parsing the PLA format accurately, especially differentiating between inputs, outputs, and terms with don't-cares.
Solution: Implemented robust parsing functions (readPla), ensuring correct handling of .ilb and .ob directives while validating line formats.

# Combining Implicants:
Challenge: Accurately combining implicants that differ by one bit while avoiding over-merging.
Solution: Implemented a helper function combineImplicants to handle Gray code checks and merging. It uses clear logic to ensure only valid combinations.

#  Prime Implicant Search:
Challenge: Avoiding excessive computation for large datasets while ensuring completeness.
Solution: Designed findPrimeImplicants to iteratively reduce implicants using recursion, minimizing computation by tracking used and unused implicants.

# Coverage Optimization:
Challenge: Ensuring all ON-set minterms are covered while selecting minimal implicants.
Solution: Implemented buildImplicantTable and selectEssentialPrimeImplicants to identify essential implicants and resolve ties through coverage-based selection.

# Validation:
Challenge: Verifying correctness across multiple test cases.
Solution: Created test cases with known inputs and outputs to validate the implementation. Compared results with expected outputs to ensure correctness.

# Verification of Functionality:

## Test Cases:
Provided two test cases (input0.pla and input1.pla) in the tests/ directory.
Each test case includes:
Input PLA file
Expected output PLA file

## Validation:
Verified the correctness of output files by comparing them against expected outputs using diff.

## Example Test Case:

Input:
.i 4
.o 1
.ilb a b c d
.ob f
.p 5
0000 1
0001 1
001- 1
0110 1
1111 1
.e

Expected Output:
.i 4
.o 1
.ilb a b c d
.ob f
.p 3
00-- 1
0-10 1
1111 1
.e
