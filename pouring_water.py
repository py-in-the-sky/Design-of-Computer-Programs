# this is a search problem (also known as a combinatorial complexity problem)

# analytical solution: fill the 9oz with the 4oz twice, emptying
# the 9oz each time
# the third time you fill it, you will have 2oz left in the 4oz,
# which will be tranferred to the 9oz
# then you will fill the 4oz one last time and
# tranfer that to the 9oz for a total of 6oz
# in the 9oz container

# the structure of pour_problem is pretty general with regards to breadth-first searches
# successors, however, is unique to this problem

# note that for a breadth-first search such as this, a min-heap is used to choose the shortest
# path to extend on each iteration and a set (read: hash table) is used to keep track of all
# visited nodes, which are quickly checked against at each node so to avoid duplicating effort

def pour_problem(X, Y, goal, start=(0, 0)):
    """X and Y are the capacity of the glasses; (x,y) is the current fill levels
    and represents a state.  the goal is a level that can be in either glass.
    begin at start state and follow successors until we reach goal.
    keep track of frontier and previously explored; fail when no frontier."""
    if goal in start:
        return [start]
    explored = set()  # set of states we have visited
    frontier = [ [start] ]  # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        (x, y) = path[-1]  # last state in the first path of the frontier
        for (state, action) in successors(x, y, X, Y).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if goal in state:
                    return path2
                else:
                    frontier.append(path2)
    return Fail

Fail = []

def successors(x, y, X, Y):
    """returns a dict of {state: action} pairs describing what can be reached from
    the (x, y) state, and how"""
    assert x <= X and y <= Y  # (x, y) is glass levels; X and Y are glass sizes
    return {((0,y+x) if y+x<=Y else (x-(Y-y), y+(Y-y))): 'X->Y',
            ((x+y,0) if x+y<=X else (x+(X-x), y-(X-x))): 'X<-Y',
            (X,y): 'fill X', (x,Y): 'fill Y', (0,y): 'empty X', (x, 0): 'empty Y'}



# -----------------
# The More Pour Problem
# User Instructions
# 
# In this problem, you will solve the pouring problem for an arbitrary
# number of glasses. Write a function, more_pour_problem, that takes 
# as input capacities, goal, and (optionally) start. This function should 
# return a path of states and actions.
#
# Capacities is a tuple of numbers, where each number represents the 
# volume of a glass. 
#
# Goal is the desired volume and start is a tuple of the starting levels
# in each glass. Start defaults to None (all glasses empty).
#
# The returned path should look like [state, action, state, action, ... ]
# where state is a tuple of volumes and action is one of ('fill', i), 
# ('empty', i), ('pour', i, j) where i and j are indices indicating the 
# glass number. 

def more_pour_problem(capacities, goal, start=None):
    """The first argument is a tuple of capacities (numbers) of glasses; the
    goal is a number which we must achieve in some glass.  start is a tuple
    of starting levels for each glass; if None, that means 0 for all.
    Start at start state and follow successors until we reach the goal.
    Keep track of frontier and previously explored; fail when no frontier.
    On success return a path: a [state, action, state2, ...] list, where an
    action is one of ('fill', i), ('empty', i), ('pour', i, j), where
    i and j are indices indicating the glass number."""
    # your code here
    
    
def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set()
    frontier = [ [start] ] 
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return Fail

Fail = []
    
def test_more_pour():
    assert more_pour_problem((1, 2, 4, 8), 4) == [
        (0, 0, 0, 0), ('fill', 2), (0, 0, 4, 0)]
    assert more_pour_problem((1, 2, 4), 3) == [
        (0, 0, 0), ('fill', 2), (0, 0, 4), ('pour', 2, 0), (1, 0, 3)] 
    starbucks = (8, 12, 16, 20, 24)
    assert not any(more_pour_problem(starbucks, odd) for odd in (3, 5, 7, 9))
    assert all(more_pour_problem((1, 3, 9, 27), n) for n in range(28))
    assert more_pour_problem((1, 3, 9, 27), 28) == []
    return 'test_more_pour passes'

print test_more_pour()
