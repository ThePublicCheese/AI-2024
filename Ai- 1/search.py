# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    ##interesting, looks like we're only returning instructions???
    #We should just explore one by one... sounds easy
    from game import Directions  
    from util import Stack

    #initializing our stack with our starting path
    stackOfStates = Stack()
    
    #we HAVE to push in a blank so it can pop a touple(?), otherwise it breaks
    stackOfStates.push((problem.getStartState(), []))
    
    #making visited a set (Still weird to me)
    visited = set()

    #while our stack is not empty(?)
    while stackOfStates:
        #pop our value and set our path to NESW and our state to a real value
        currentState, path = stackOfStates.pop()

        if problem.isGoalState(currentState):
            return path

        if currentState not in visited:
            
            #redundency check
            visited.add(currentState)
            
            #unpack our list of touples
            successors = problem.getSuccessors(currentState)
            
            # same as for (i=0;...), unpacks the two important values and throws away the other, we have to unpack every touple
            # creates new graph by unpacking successors and then we explore then unpack again 
            for successor, action, garbageWeDontNeed in successors:
                #print(action)
                #action has to be a list???
                newState = path + [action]
                stackOfStates.push((successor, newState))

    return None
        
        

def breadthFirstSearch(problem: SearchProblem):
    #We need to explode each node one by one? Should be the only difference
    #Which means that we need to explore every state within a stack...
    #two stacks??? mirrored as old/new? that alternate and populate eachother?
    #As a swap space of sorts?
    
    from game import Directions  
    from util import Stack

    #initializing our stack with our starting path
    oldStackOfStates = Stack()
    oldStackOfStates.push((problem.getStartState(), []))
    
    newStackOfStates = Stack()
    newStackOfStates.push((problem.getStartState(), []))
    #making visited an set (Still weird to me)
    visited = set()

    #while our stack is not empty
    while oldStackOfStates or newStackOfStates:
        
        while oldStackOfStates.isEmpty() == False:
            #pop our value and set our path to NESW and our state to a real value
            currentState, path = oldStackOfStates.pop()
            if problem.isGoalState(currentState):
                return path

            if currentState not in visited:
                
                #redundency check
                visited.add(currentState)
                
                #unpack our list of touples
                successors = problem.getSuccessors(currentState)
                
                # same as for (i=0;...), unpacks the two important values and throws away the other, we have to unpack every touple
                # creates new graph by unpacking successors and then we explore then unpack again 
                for successor, action, garbageWeDontNeed in successors:
                    #print(action)
                    newState = path + [action]
                    newStackOfStates.push((successor, newState))
                    
        while newStackOfStates.isEmpty() == False:
            #pop our value and set our path to NESW and our state to a real value
            currentState, path = newStackOfStates.pop()
            if problem.isGoalState(currentState):
                return path

            if currentState not in visited:
                
                #redundency check
                visited.add(currentState)
                
                #unpack our list of touples
                successors = problem.getSuccessors(currentState)
                
                # same as for (i=0;...), unpacks the two important values and throws away the other, we have to unpack every touple
                # creates new graph by unpacking successors and then we explore then unpack again 
                for successor, action, garbageWeDontNeed in successors:
                    #print(action)
                    newState = path + [action]
                    oldStackOfStates.push((successor, newState))
                    
    return None

def uniformCostSearch(problem: SearchProblem):
    from game import Directions  
    from util import PriorityQueue

    #literally the same thing as our first attempt but with a PQ
    
    priorityQueueOfStates = PriorityQueue()
    priorityQueueOfStates.push((problem.getStartState(), [], 0), 0)
    
    visited = set()
    
 
    while priorityQueueOfStates:
        
        currentState, path, cost = priorityQueueOfStates.pop()

        if problem.isGoalState(currentState):
            return path

        if currentState not in visited:
            visited.add(currentState)

            successors = problem.getSuccessors(currentState)

            for successor, action, sucCost in successors:
                newCost = cost + sucCost
                newState = path + [action]
                priorityQueueOfStates.push((successor, newState, newCost), newCost)

    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    from game import Directions
    from util import PriorityQueue
    
    ##relatively the same just using heuristicCost as a new value in totalCost? with a PQ
    priorityQueueOfStates = PriorityQueue()
    priorityQueueOfStates.push((problem.getStartState(), [], 0), 0 + heuristic(problem.getStartState(), problem))
    
    visited = set()

    while not priorityQueueOfStates.isEmpty():
        currentState, path, cost = priorityQueueOfStates.pop()

        if problem.isGoalState(currentState):
            return path

        if currentState not in visited:
            visited.add(currentState)

            successors = problem.getSuccessors(currentState)

            for successor, action, sucCost in successors:
                newCost = cost + sucCost
                heuristicCost = heuristic(successor, problem)
                totalCost = newCost + heuristicCost
                newState = path + [action]
                priorityQueueOfStates.push((successor, newState, newCost), totalCost)

    return None


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
