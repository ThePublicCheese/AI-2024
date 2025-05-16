from collections import defaultdict

#Function of program is to solve various statements using propositional logic

def main():
    # opening file with a try/catch
    try:
        with open("input.kb", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Input file not found")
        return
    except Exception as e:
        print("Error reading input file:", e)
        return

    # setting up variables
    kb = []  # knowledge base
    refMap = {}  # reference map for connecting values

    # parsing for proper clauses
    kbClauses = [line.strip().split() for line in lines[:-1]]
    queryClauses = lines[-1].strip().split()

    # splitting/adding clasues
    for clause in kbClauses:
        if "^" in clause[-1]:
            subClauses = clause[-1].split("^")
            for subClause in subClauses:
                addClause(kb, [subClause], refMap)
        else:
            addClause(kb, clause, refMap)

    # Final statment testing the returned values
    result = generateClauses(kb, queryClauses, refMap)
    if result == "Success":
        printKb(kb, refMap)
    else:
        print("This clause is invalid")


# Function to negate, helps consistency if we have a specific function for it
def negateLiteral(literal):
    if literal.startswith("~"):
        return literal[1:]
    else:
        return "~" + literal


# Dictonary for standardizing & splitting statements, although our examples don't have any of these, I wanted to throw in extras just incase
# test cases need to be handled likewise.
def standardizeClause(clause):
    standardizedClause = []

    for literal in clause:

        if "=>" in literal:
            p, q = literal.split("=>")
            standardizedClause.append(f"~{p}")
            standardizedClause.append(q)

        elif "^" in literal:
            literals = literal.split("^")
            for lit in literals:
                standardizedClause.append(lit)

        elif "V" in literal:
            literals = literal.split("∨")
            for lit in literals:
                standardizedClause.append(lit)

        elif "~(" in literal:
            if "V" in literal:
                literals = literal.strip("~()").split("∨")
                for lit in literals:
                    standardizedClause.append(f"~{lit}")
            elif "^" in literal:
                literals = literal.strip("~()").split("^")
                for lit in literals:
                    standardizedClause.append(f"~{lit}")

        else:
            standardizedClause.append(literal)

    return list(set(standardizedClause))


# finds new clauses based off of compliments
def resolve(clause1, clause2):
    resolveClause = []
    for literal1 in clause1:
        for literal2 in clause2:
            # if they're compliments
            if negateLiteral(literal1) == literal2:
                # resolve
                resolveClause = [lit for lit in clause1 if lit != literal1] + [
                    lit for lit in clause2 if lit != literal2
                ]
                return standardizeClause(resolveClause)
    return None


# truth test
def isTrue(clause):
    return "True" in clause


# used for adding clauses into our reference map
def addClause(kb, clause, refMap, resolvedFrom=None):
    if not isTrue(clause) and tuple(clause) not in refMap.values():
        parentClauses = [resolvedFrom] if resolvedFrom is not None else []
        refMap[tuple(clause)] = {"index": len(kb) + 1, "parents": parentClauses}
        kb.append(clause)


# Negates, adds negations, then looks for new clauses or a final solution.
# If it runs out of possibilities it returns invalid.
def generateClauses(kb, query, refMap):
    negatedQuery = [negateLiteral(literal) for literal in query]
    for literal in negatedQuery:
        addClause(kb, [literal], refMap)

    while True:
        newKb = []
        for i, clause1 in enumerate(kb):
            for j, clause2 in enumerate(kb[:i]):
                newClause = resolve(clause1, clause2)
                if newClause is not None:
                    if not newClause:
                        return "Success"
                    if newClause not in kb and newClause not in newKb:
                        addClause(
                            newKb,
                            standardizeClause(newClause),
                            refMap,
                            resolvedFrom=(i + 1, j + 1),
                        )
        if not newKb:
            return "Failure"
        kb += newKb


# prints and makes sure a contradiction has been found.
def printKb(kb, refMap):
    for i, clause in enumerate(kb, 1):
        refClause = refMap[tuple(clause)]
        refParents = refClause["parents"]

        # formatting
        refParents = "{" + ", ".join(map(str, refParents)) + "}"
        print(f"{i}. {' '.join(clause)}  {refParents}")

    contradiction = False
    for i, clause1 in enumerate(kb, 1):
        for j, clause2 in enumerate(kb[: i - 1], 1):
            resolvedClause = resolve(clause1, clause2)
            if resolvedClause == []:
                print(f"Contradiction {{{i},{j}}}")
                contradiction = True
                break
        if contradiction:
            break

    if not contradiction:
        print("Valid")


if __name__ == "__main__":
    main()