import itertools


# --------------------------------------------
# Helper Functions
# --------------------------------------------

def readPla(filename):
    """Reads a PLA file and extracts inputs, outputs, minterms, and don't-cares."""
    with open(filename, 'r') as file:
        lines = file.readlines()

    numInputs = 0
    numOutputs = 0
    inputLabels = []
    outputLabels = []
    terms = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):  # Skip empty lines and comments
            continue
        if line.startswith('.i '):
            numInputs = int(line.split()[1])
        elif line.startswith('.o '):
            numOutputs = int(line.split()[1])
        elif line.startswith('.ilb '):
            inputLabels = line.split()[1:]
        elif line.startswith('.ob '):
            outputLabels = line.split()[1:]
        elif line.startswith('.p '):
            numTerms = int(line.split()[1])
        elif line.startswith('.e'):
            break
        elif not line.startswith('.'):
            parts = line.split()
            if len(parts) == 2:
                inputPattern, outputPattern = parts
                terms.append((inputPattern, outputPattern))
            else:
                raise ValueError(f"Invalid term format: {line}")

    return numInputs, numOutputs, inputLabels, outputLabels, terms


def patternToMinterms(pattern):
    """Expands a binary pattern with dashes into all possible minterms."""
    positions = []
    for c in pattern:
        if c == '0':
            positions.append(['0'])
        elif c == '1':
            positions.append(['1'])
        elif c == '-':
            positions.append(['0', '1'])
    return [int(''.join(bits), 2) for bits in itertools.product(*positions)]


def decToBin(value, numBits):
    """Converts a decimal number to a binary string of fixed length."""
    return bin(value)[2:].zfill(numBits)


def combineImplicants(a, b):
    """Combines two binary strings if they differ by exactly one bit."""
    combined = ''
    differences = 0

    for x, y in zip(a, b):
        if x == y:
            combined += x
        else:
            combined += '-'
            differences += 1
        if differences > 1:
            return None  # More than one difference; cannot combine.

    return combined


# --------------------------------------------
# Prime Implicant Finder
# --------------------------------------------

def findPrimeImplicants(minterms):
    """Recursively finds all prime implicants."""
    nextMinterms = set()
    used = set()
    unused = set()

    for i, m1 in enumerate(minterms):
        for j, m2 in enumerate(minterms):
            if i < j:  # Avoid duplicate combinations
                combined = combineImplicants(m1, m2)
                if combined:
                    nextMinterms.add(combined)
                    used.add(m1)
                    used.add(m2)

    # Collect all implicants that couldn't be combined
    unused = minterms - used

    if not nextMinterms:  # No further combinations are possible
        return unused
    else:
        # Recur to process the next level of implicants
        return unused | findPrimeImplicants(nextMinterms)


# --------------------------------------------
# Coverage Optimization
# --------------------------------------------

def buildImplicantTable(primeImplicants, onSet):
    """Builds a table mapping prime implicants to the minterms they cover."""
    table = {}
    for minterm in onSet:
        table[minterm] = []
        for implicant in primeImplicants:
            if minterm in patternToMinterms(implicant):
                table[minterm].append(implicant)
    return table


def selectEssentialPrimeImplicants(implicantTable):
    """Finds essential prime implicants and reduces the implicant table."""
    essentialPrimeImplicants = []
    remainingMinterms = set(implicantTable.keys())

    while remainingMinterms:
        # Find essential prime implicants
        for minterm, implicants in list(implicantTable.items()):
            if len(implicants) == 1:
                essential = implicants[0]
                if essential not in essentialPrimeImplicants:
                    essentialPrimeImplicants.append(essential)
                # Remove all minterms covered by this implicant
                coveredMinterms = patternToMinterms(essential)
                for covered in coveredMinterms:
                    implicantTable.pop(covered, None)
                remainingMinterms -= set(coveredMinterms)
                break
        else:
            # Handle ties: pick the implicant covering the most minterms
            coverage = {imp: 0 for impList in implicantTable.values() for imp in impList}
            for minterm, implicants in implicantTable.items():
                for implicant in implicants:
                    coverage[implicant] += 1
            bestImplicant = max(coverage, key=coverage.get)
            essentialPrimeImplicants.append(bestImplicant)
            coveredMinterms = patternToMinterms(bestImplicant)
            for covered in coveredMinterms:
                implicantTable.pop(covered, None)
            remainingMinterms -= set(coveredMinterms)

    return essentialPrimeImplicants


# --------------------------------------------
# Write Output
# --------------------------------------------

def writePla(outputFilename, numInputs, numOutputs, inputLabels, outputLabels, minimizedFunctions):
    """Writes the minimized PLA to a file."""
    with open(outputFilename, 'w') as file:
        file.write(f'.i {numInputs}\n')
        file.write(f'.o {numOutputs}\n')
        if inputLabels:
            file.write('.ilb ' + ' '.join(inputLabels) + '\n')
        if outputLabels:
            file.write('.ob ' + ' '.join(outputLabels) + '\n')
        implicantCount = sum(len(func) for func in minimizedFunctions.values())
        file.write(f'.p {implicantCount}\n')
        for outputIdx, primeImplicants in minimizedFunctions.items():
            for implicant in primeImplicants:
                output = '-' * outputIdx + '1' + '-' * (numOutputs - outputIdx - 1)
                file.write(f"{implicant} {output}\n")
        file.write('.e\n')


# --------------------------------------------
# Main Program
# --------------------------------------------

def main(inputFilename, outputFilename):
    numInputs, numOutputs, inputLabels, outputLabels, terms = readPla(inputFilename)
    minimizedFunctions = {}

    for outputIdx in range(numOutputs):
        onSet = set()
        dcSet = set()

        for inputPattern, outputPattern in terms:
            if outputPattern[outputIdx] == '1':
                onSet.update(patternToMinterms(inputPattern))
            elif outputPattern[outputIdx] == '-':
                dcSet.update(patternToMinterms(inputPattern))

        # Convert to binary strings
        binaryMinterms = {decToBin(m, numInputs) for m in onSet | dcSet}

        # Find prime implicants
        primeImplicants = findPrimeImplicants(binaryMinterms)

        # Build implicant table and optimize coverage
        implicantTable = buildImplicantTable(primeImplicants, onSet)
        minimizedFunctions[outputIdx] = selectEssentialPrimeImplicants(implicantTable)

    writePla(outputFilename, numInputs, numOutputs, inputLabels, outputLabels, minimizedFunctions)


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python qm.py input.pla output.pla")
    else:
        main(sys.argv[1], sys.argv[2])
