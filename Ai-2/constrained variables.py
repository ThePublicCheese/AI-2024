import sys

def main():
    
    #making sure our arguments can be taken from command line
    if len(sys.argv) != 4:
        print("Usage: main.py <variable_file> <constraint_file> <consistency_enforcing_procedure>")
        sys.exit(1)

    #assigning command line arguments
    var = sys.argv[1]
    con = sys.argv[2]
    operator = sys.argv[3]

    #parsing
    variables = parseVariable(var)
    constraints = parseConstraint(con)

    #setting bools based off of constraints
    if operator == "fc":
        forwardChecking = True
    elif operator == "none":
        forwardChecking = False
    else:
        print("Wrong format please try again")
        sys.exit(1)

    #getting the pathing, formatting and outputting
    solution, path, success = backtrackSearch(variables, constraints, forwardChecking)
    if success:
        print("Solution found:")
        print(formatAnswer(solution)) 
        print("Path:")
        formatPath(path, solution)
    else:
        print("No solution found.")
        


#parsing functions ########################################

#notes: We need to open each file, read it, strip,split at a delim and read it into variables/put it into a data structure.

#Correct
def parseVariable(file):
    variables = {}
    
    #opening our file in read mode
    with open(file, 'r') as f:
        for line in f:
            
            #splitting at the colon
            data = line.strip().split(':')
            
            #bugCheck
            if len(data) != 2:
                raise ValueError("Invalid variable file format")
            var, domain = data
            #creating domain
            domainVal = list(map(int, domain.split()))
            variables[var] = domainVal
            
    return variables

#See parseVariable

#Correct
def parseConstraint(file):
    constraints = []
    with open(file, 'r') as f:
        for line in f:
            data = line.strip().split()
            if len(data) != 3:
                raise ValueError("Invalid constraint file format")
            var1, operand, var2 = data
            constraints.append((var1, operand, var2))
    return constraints

###########################################################






#Backtracking #############################################

#Making sure our assignment satisfies whatever constraint it has
#Notes: tried using a switch statement just for fun, too much, just going to use an if/elif chain, it works easier

#Correct  
def isValid(assignment, constraints):
    for var1, operand, var2 in constraints:
        if operand == '=':
            if assignment[var1] != assignment[var2]:
                return False
        elif operand == '!':
            if assignment[var1] == assignment[var2]:
                return False
        elif operand == '>':
            if assignment[var1] <= assignment[var2]:
                return False
        elif operand == '<':
            if assignment[var1] >= assignment[var2]:
                return False
    return True



#backtracking search algorithm with forward checking call, using this as a hub for any data types needed in backtracking 
#(sets, queues, stacks, lists)) also it should help keep my data straight and make sure I'm not getting any weird type errors like I have been
#Should I combine this into one function later?

#Correct
def backtrackSearch(variables, constraints, forwardChecking):
    assignment = {}
    path = []
    return backtrack(assignment, path, variables, constraints, forwardChecking)


#Backtracking section to traverse and manipulate data.
#Notes: Use this recusively(?), set up a solution Check early, use forward checking to find inference, then backtrack using modified data???
#list, set, stack or queue to keep track of path? iterative backtracking??? 
#this whole thing is outlined in the book but this still sucks to try to write

#Correct, change the way you add paths and your output will be nicer
 
def backtrack(assignment, path, variables, constraints, forwardChecking):
    
    #checking to see if we have a proper solution
    if len(assignment) == len(variables):
        if isValid(assignment, constraints):
            return assignment, path, True
        else:
            return assignment, path, False
    
    #setting MCV
    var = mostConstrainedVariable(assignment, variables, constraints)
    
    #setting LCV and starting our backtracking/checking
    for value in leastConstrainingValue(var, assignment, variables, constraints):
        assignment[var] = value
        
        #for keeping path
        path.append((assignment.copy()))
        
        if forwardChecking == True:
            inferences = forwardCheck(assignment, var, value, variables, constraints)
           
           
            if inferences is not {}:
                result, path, success = backtrack(assignment, path, variables, constraints, forwardChecking)
                if success:
                    return result, path, True        
                else:
                    del assignment[var]
                    #remove some false paths
                    path.pop()
                    continue
         
        elif forwardChecking == False:
            result, path, success = backtrack(assignment, path, variables, constraints, forwardChecking)
            if success:
                return result, path, True
            
        del assignment[var]
        #remove some false paths
        path.pop
            
    return None, path, False

#MCV (this is correct -do not touch anymore please holy- )
#Notes: change from recusive method to a more reliable method (done)
def mostConstrainedVariable(assignment, variables, constraints):
    min = float('inf') #setting infinite min bound
    max = None #setting empty max bound
    
    #finding most constrained
    for var in variables:
        #skip when already assigned
        if var in assignment:
            continue
        
        #find remaining and update values
        values = len([value for value in variables[var] if value not in assignment.values()])
        if values < min:
            min = values
            max = var
    
    return max

#LCV (Correct as correct can be) 
#Notes: use I-J-K loop to keep track of the current varirable, its possible match and an unset variable
#keep track of what constraints have what weights, compare and find the least constrained value
def leastConstrainingValue(var, assignment, variables, constraints):
    domain = variables[var]
    val = []

    #finding which violate constraints and adjusting accordingly (Like the four queens problem ((in a way)) ?) reference if this is wrong to fix
    for value in domain:
        count = 0
        tempAssign = assignment.copy()
        tempAssign[var] = value

        #logic ijk for loop
        for tempVar in variables:
            if tempVar != var and tempVar not in tempAssign:
                for tempVal in variables[tempVar]:
                    tempAssign[tempVar] = tempVal
                    violations = 0
                    for constraint in constraints:
                        var1, operand, var2 = constraint
                        
                        #checking variables forward, with both operands that provide information
                        if var1 == var and var2 == tempVar:
                            if operand == '>':
                                if tempAssign[var] <= tempAssign[var2]:
                                    violations += 1
                            elif operand == '<':
                                if tempAssign[var] >= tempAssign[var2]:
                                    violations += 1
                        
                        #checking variables backwards, with both operands that provide information
                        elif var1 == tempVar and var2 == var:
                            if operand == '>':
                                if tempAssign[var1] <= tempAssign[var]:
                                    violations += 1
                            elif operand == '<':
                                if tempAssign[var1] >= tempAssign[var]:
                                    violations += 1
                    #boy oh boy we get to make decisions
                    count += violations
                    del tempAssign[tempVar]
    
        val.append((value, count))

    #sorting based on violations, fewer violations means sooner in list, means sooner solution (all this for loop junk is hurting me physically)
    for i in range(len(val)):
        for j in range(len(val) - 1 - i):
            if val[j][1] > val[j + 1][1]:
               val[j], val[j + 1] = val[j + 1], val[j]
    sorted = [value for value, _ in val]
    return sorted


#forward checking to reduce our domain values based on given data 
#(correct - do not change)
#Notes: If it is what we did for our written portion, If it passes comparisons, its the proper constraint and we make sure the other variable isn't assigned. 
#Then, based off of the given operand is reduces the domain values or increases the domain values for your "other variable" ?
def forwardCheck(assignment, var, value, variables, constraints):
    inferences = {}  #aka additional data (a suprise tool to help us later)

    #check constraints to find what is affected by contraints
    for var1, operand, var2 in constraints:
        
        #making sure our variable is the proper one and that var2 isn't already assigned a value
        if var1 == var and var2 not in assignment:
            
            #now we reduce domain values of var2 based on the current assignment
            if operand == '>':
                inferences[var2] = [v for v in variables[var2] if v > value]
            elif operand == '<':
                inferences[var2] = [v for v in variables[var2] if v < value]
                
        #covering all our bases, same code as above ^, same rough idea as our LCV which makes this easy
        elif var2 == var and var1 not in assignment:
            if operand == '>':
                inferences[var1] = [v for v in variables[var1] if v < value]
            elif operand == '<':
                inferences[var1] = [v for v in variables[var1] if v > value]

    #Bugcheck, if something goes wrong blow everything up and we all die a horrible death
    for var, domain in inferences.items():
        if not domain:
            return {}
        
    return inferences

###########################################################



#formatting ###############################################

#Work on this as much as you can to shrink formatting
def formatAnswer(solution):
    if solution is None:
        return "No solution found."
    else:
        return ', '.join(f"{var}={solution[var]}" for var in solution)

def formatPath(path, solution):
    if not path:
        print("No path found.")
        return
    count = 1
    for step in path:
        if step == solution:
            print(f"{count}. {formatAnswer(step)}  solution")
        else:
            assignment_str = ', '.join(f"{var}={val}" for var, val in step.items())
            print(f"{count}. {assignment_str}  failure")
        count += 1
        
###########################################################


if __name__ == "__main__":
    main()