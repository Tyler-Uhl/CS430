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
#from argparse import Action
#from search.game import Directions
from pip._vendor.cachecontrol import heuristics


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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    """
    "*** YOUR CODE HERE ***"
    
    print('Start', problem.getStartState())
    print('Is the start a goal?', problem.isGoalState(problem.getStartState()))
    print('Starts successors:', problem.getSuccessors(problem.getStartState()))
    
    #variable for get the start state
    state = problem.getStartState()
    
    #area to push nodes onto
    theFringe = util.Stack()
    
    #pushing the start state to the stack
    theFringe.push((state, [], []))
    
    #initializing the explored set
    exploredSet = set()
    
    while not theFringe.isEmpty():
        curNode = theFringe.pop()
        
        #variables for each current node member
        curState = curNode[0]
        curPath = curNode[1]
        curCost = curNode[2]
        
        if problem.isGoalState(curState):
            return curPath
        
        if curState not in exploredSet:
            exploredSet.add(curState)

            
            for childSuccessor in problem.getSuccessors(curState):
                cLoc = childSuccessor[0]
                actionToChild = childSuccessor[1]
                actionCost = childSuccessor[2]
                theFringe.push((cLoc, curPath + [actionToChild], curCost + [actionCost]))
     
    util.raiseNotDefined()
    


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    state = problem.getStartState()
    theFringe = util.Queue()
    exploredSet = set()
    
    theFringe.push((state, [], []))
    
    while not theFringe.isEmpty():
        curNode = theFringe.pop()
    
        curState = curNode[0]
        curPath = curNode[1]
        curCost = curNode[2]
        
        if problem.isGoalState(curState):
            return curPath
        
        if curState not in exploredSet:
            exploredSet.add(curState)
            
            for childSuccessor in problem.getSuccessors(curState):
                cLoc = childSuccessor[0]
                actionToChild = childSuccessor[1]
                actionCost = childSuccessor[2]
                theFringe.push((cLoc, curPath + [actionToChild], curCost + [actionCost])) 
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    state = problem.getStartState()
    theFringe = util.PriorityQueue()
    exploredSet = set()
    
    #now pushing 1 node with 4 members, and a priority
    theFringe.push((state, [],[], []), 0)
    
    while not theFringe.isEmpty():
        curNode = theFringe.pop()
    
        curState = curNode[0]
        curPath = curNode[1]
        curCost = curNode[2]
        curPriority = curNode[3]
        
        if problem.isGoalState(curState):
            return curPath
        
        if curState not in exploredSet:
            exploredSet.add(curState)
            
            for childSuccessor in problem.getSuccessors(curState):
                #conducting a check on if the future has already been visited
                if childSuccessor[0] not in exploredSet:
                    cLoc = childSuccessor[0]
                    actionToChild = childSuccessor[1]
                    actionCost = childSuccessor[2]
                    
                    #creating a variable that type casts our expanded node to list
                    newPriority = list(curPriority)
                    
                    #now adding that particular action cost to our newPriority list
                    newPriority.append(actionToChild)
                    
                    #pushing everything before with our node, along with the node's priority and 
                    theFringe.push((cLoc, curPath+[actionToChild], curCost+[actionCost], newPriority), problem.getCostOfActions(newPriority))
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    state = problem.getStartState()
    theFringe = util.PriorityQueue()
    exploredSet = set()
    
    #now pushing 1 node with 4 members, and a priority
    theFringe.push((state,[],0), heuristic(state, problem))
    
    while not theFringe.isEmpty():
        curNode = theFringe.pop()
    
        curState = curNode[0]
        curPath = curNode[1]
        curCost = curNode[2]
        
        if problem.isGoalState(curState):
            return curPath
        
        if curState not in exploredSet:
            exploredSet.add(curState)
            
            for childSuccessor in problem.getSuccessors(curState):
                #conducting a check on if the future has already been visited
                if childSuccessor[0] not in exploredSet:
                    cLoc = childSuccessor[0]
                    actionToChild = childSuccessor[1]
                    actionCost = childSuccessor[2]
                    cPrice = curCost + actionCost
                    
                    theFringe.push((cLoc, curPath+[actionToChild], curCost+actionCost), cPrice + heuristic(cLoc, problem))
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
