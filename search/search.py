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

def depthFirstSearch(problem):
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()                                                 #frontier will be a stack
    actions = []                                                            #a list where we will keep the actions for pacman
    predecessor = {}                                                        #a dictionary to keep the parents for every child 
    node = problem.getStartState()
    if problem.isGoalState(node):
        return []

    frontier.push(node)
    explored = set()                                                        #we use set to have O(1) for accessing a node
    predecessor[node] = ((-1,-1), 'Stop')                                   #add predecessor for starting node to be (-1,-1) and action Stop

    while True:
        if frontier.isEmpty():
            return []
        node = frontier.pop()
        
        if problem.isGoalState(node):
            start_state = problem.getStartState()
            while node != start_state:
                actions.insert(0, predecessor[node][1])                     #we insert the action at start because we go from bottom to top
                node = predecessor[node][0]
            return actions
        
        explored.add(node)
        for child in problem.getSuccessors(node):
            if child[0] not in explored:
                predecessor[child[0]] = (node,child[1])
            if child[0] not in explored and child[0] not in frontier.list:
                frontier.push(child[0])

def breadthFirstSearch(problem):
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()                                                 #now frontier will be a FIFO Queue
    actions = []
    predecessor = {}
    node = problem.getStartState()
    if problem.isGoalState(node):
        return []
    frontier.push(node)
    explored = set()
    predecessor[node] = ((-1,-1), 'Stop')                                   #add predecessor for starting node to be (-1,-1) and action Stop

    while True:
        if frontier.isEmpty():
            return []
        node = frontier.pop()
        
        if problem.isGoalState(node):
            start_state = problem.getStartState()
            while node != start_state:
                actions.insert(0, predecessor[node][1])
                node = predecessor[node][0]
            return actions
        
        explored.add(node)
        for child in problem.getSuccessors(node):
            if child[0] not in explored and child[0] not in frontier.list:
                predecessor[child[0]] = (node,child[1])
                frontier.push(child[0])

def uniformCostSearch(problem):
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()                                           #now frontier will be a priority queue
    actions = []
    predecessor = {}
    node = problem.getStartState()
    if problem.isGoalState(node):
        return []

    frontier.push(node, 0)
    explored = set()
    predecessor[node] = ((-1,-1), 'Stop', 0)                                   #add predecessor for starting node to be (-1,-1) and action Stop

    while True:
        if frontier.isEmpty():
            return []
        node = frontier.pop()
        
        if problem.isGoalState(node):
            start_state = problem.getStartState()
            while node != start_state:
                actions.insert(0, predecessor[node][1])
                node = predecessor[node][0]
            return actions
        
        explored.add(node)
        for child in problem.getSuccessors(node):
            if child[0] not in [item[2] for item in frontier.heap]:
                if child[0] not in explored:
                    cost_until_parent = predecessor[node][2]
                    predecessor[child[0]] = (node,child[1], child[2] + cost_until_parent) #for this child i save the cost of action from parent and also the
                    frontier.push(child[0], child[2] + cost_until_parent)                 #cost until the parent
            else:
                for item in frontier.heap:                              #we have to see if the node is also in frontier with a bigger cost and if it is then
                    if (item[2] == child[0]):                           #we have to swap it and keep the lower cost
                        cost = item[0]
                        if cost > (predecessor[node][2] + child[2]):
                            frontier.update(child[0],predecessor[node][2] + child[2])               #call update for priority queue to change the cost
                            predecessor[child[0]] = (node,child[1],predecessor[node][2] + child[2]) #change the predecessor we had for the node to the new parent

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# astarSearch is like uniformCostSearch but we also add to the cost the value from our heuristic 
def aStarSearch(problem, heuristic=nullHeuristic):
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    actions = []
    predecessor = {}
    node = problem.getStartState()
    if problem.isGoalState(node):
        return []
    frontier.push(node, 0)
    explored = set()
    predecessor[node] = ((-1,-1), 'Stop', 0)                                   #add predecessor for starting node to be (-1,-1) and action Stop
    while True:
        if frontier.isEmpty():
            return []
        node = frontier.pop()
        if problem.isGoalState(node):
            start_state = problem.getStartState()
            while node != start_state:
                actions.insert(0, predecessor[node][1])
                node = predecessor[node][0]
            return actions
        explored.add(node)
        for child in problem.getSuccessors(node):
            if child[0] not in [item[2] for item in frontier.heap]:
                if child[0] not in explored:
                    cost_until_parent = predecessor[node][2]
                    #attention: we don't put the heuristic's value below because we couldn't be able to find the cost until the parent
                    predecessor[child[0]] = (node,child[1], child[2] + cost_until_parent)
                    frontier.push(child[0], child[2] + cost_until_parent + heuristic(child[0],problem))     #in frontier we also add the heuristic's value for the node
            else:
                for item in frontier.heap:
                    if (item[2] == child[0]):
                        cost = item[0]
                        if cost > (predecessor[node][2] + child[2] + heuristic(child[0],problem)):          #we add the heuristic's value
                            frontier.update(child[0],predecessor[node][2] + child[2] + heuristic(child[0],problem)) #we add the heuristic's value
                            predecessor[child[0]] = (node,child[1],predecessor[node][2] + child[2]) 



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
