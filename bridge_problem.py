
import doctest

# explored is our hash table of visited states
# frontier is our min-heap of paths in process
def bridge_problem(here):
    here = frozenset(here) | frozenset(['light'])
    explored = set()  # set of states we have visited
    # state will be a (people-here, people-there, time-elapsed) tuple
    frontier = [ [(here, frozenset(), 0)] ]  # ordered list of paths we have blazed
    if not here:
        return frontier[0]
    while frontier:
        path = frontier.pop(0)
        state1 = here1, there1, t1 = path[-1]
        # test for solution after path's pulled off heap, rather than before it's put into heap
        if not here1 or here1 == frozenset(['light']):  # nobody left 'here'
            return path
        for (state, action) in bsuccessors(path[-1]).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                frontier.append(path2)
                frontier.sort(key=elapsed_time)
                # this sorting of frontier upon every insert effectively makes frontier a heap
                # sorting is a bit wasteful, though; using a binary search and bisecting the list
                # for an insert would be better
    return []

def elapsed_time(path): return path[-1][2]

def bsuccessors(state):
    """returns a dict of {state: action} pairs.  a state is a (here, there, t) tuple,
    where here and there are frozensets of people (indicated by their times) and/or
    the 'light', and t is a number indicating the elasped time.  action is represented
    by '->' for here to there and '<-' for there to here."""
    here, there, t = state
    if 'light' in here:
        return dict(((here - frozenset([a,b,'light']), there | frozenset([a,b,'light']), t+max(a,b)), (a,b,'->'))
                    for a in here if a is not 'light' for b in here if b is not 'light')
    else:
        return dict(((here | frozenset([a,b,'light']), there - frozenset([a,b,'light']), t+max(a,b)), (a,b,'<-'))
                    for a in there if a is not 'light' for b in there if b is not 'light')

def path_states(path):
    "Return a list of states in this path."
    return path[0::2]
    
def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

class TestBridge: """
>>> elapsed_time(bridge_problem([1,2,5,10]))
17

## There are two equally good solutions
>>> S1 = [(2, 1, '->'), (1, 1, '<-'), (5, 10, '->'), (2, 2, '<-'), (2, 1, '->')]
>>> S2 = [(2, 1, '->'), (2, 2, '<-'), (5, 10, '->'), (1, 1, '<-'), (2, 1, '->')]
>>> path_actions(bridge_problem([1,2,5,10])) in (S1, S2)
True

## Try some other problems
>>> path_actions(bridge_problem([1,2,5,10,15,20]))
[(2, 1, '->'), (1, 1, '<-'), (10, 5, '->'), (2, 2, '<-'), (2, 1, '->'), (1, 1, '<-'), (15, 20, '->'), (2, 2, '<-'), (2, 1, '->')]

>>> path_actions(bridge_problem([1,2,4,8,16,32]))
[(2, 1, '->'), (1, 1, '<-'), (8, 4, '->'), (2, 2, '<-'), (1, 2, '->'), (1, 1, '<-'), (16, 32, '->'), (2, 2, '<-'), (2, 1, '->')]

>>> [elapsed_time(bridge_problem([1,2,4,8,16][:N])) for N in range(6)]
[0, 1, 2, 7, 15, 28]

>>> [elapsed_time(bridge_problem([1,1,2,3,5,8,13,21][:N])) for N in range(8)]
[0, 1, 1, 2, 6, 12, 19, 30]

>>> path_actions(bridge_problem(['light']))
[]

>>> PA1 = [(2, 1, '->'), (1, 1, '<-'), (3, 1, '->')]
>>> PA2 = [(3, 1, '->'), (1, 1, '<-'), (2, 1, '->')]
>>> path_actions(bridge_problem([1,2,3])) in (PA1, PA2)
True

>>> path_actions(bridge_problem([4,4,4,4,4,4,4]))
[(4, '->')]
"""
# Testing is important! Try to get in the habit of doing it regularly.
print doctest.testmod()

def bsuccessors2(state):
    "returns a dict of {state: action} pairs.  a state is a (here, there) tuple."
    here, there = state
    if 'light' in here:
        return dict(((here - frozenset([a,b,'light']), there | frozenset([a,b,'light'])), (a,b,'->'))
                    for a in here if a is not 'light' for b in here if b is not 'light')
    else:
        return dict(((here | frozenset([a,b,'light']), there - frozenset([a,b,'light'])), (a,b,'<-'))
                    for a in there if a is not 'light' for b in there if b is not 'light')

def bcost(action):
    """Returns the cost (a number) of an action in the
    bridge problem."""
    # An action is an (a, b, arrow) tuple; a and b are 
    # times; arrow is a string. 
    a, b, arrow = action
    return max(a, b)

def path_cost(path):
    """The total cost of a path (which is stored in a tuple
    with the final action)."""
    # path = [state, (action, total_cost), state, ... ]
    if len(path) < 3:
        return 0
    else:
        last_action, total_cost = path[-2]
        return total_cost

def final_state(path): return path[-1]

def add_to_frontier(frontier, path):
    "add path to frontier, replacing costlier path to same state if there is one."
    # (this could be done more efficiently)
    # determine whether there is an old path to the final state of this path
    old = None
    for i,p in enumerate(frontier):
        if final_state(p) == final_state(path):
            old = i
            break
    if old is not None and path_cost(frontier[old]) < path_cost(path):
        return  # old path was better; do nothing
    elif old is not None:
        del frontier[old]  # old path was worse; delete it
        frontier.append(path)  # append new, better path
        frontier.sort(key=path_cost)

def bridge_problem2(here):
    here = frozenset(here) | frozenset(['light'])
    explored = set()  # set of states we have visited
    # state will be a (people-here, people-there, time-elapsed) tuple
    frontier = [ [(here, frozenset())] ]  # ordered list of paths we have blazed
    if not here:
        return frontier[0]
    while frontier:
        path = frontier.pop(0)
        state1 = here1, there1 = final_state(path)
        # test for solution after path's pulled off heap, rather than before it's put into heap
        if not here1 or here1 == frozenset(['light']):  # nobody left 'here'
            return path
        explored.add(state1)  # moved this out of the for-loop to here
        # the reason this was moved here and out of the for-loop is the same reason we moved
        # the 'if not here' out of the for-loop to the above position: if a path that ends at
        # state1 gets popped off the heap then we know it's the cheapest of all paths that go
        # through state1, just as a path that ends in a solution that's popped off the heap is
        # the cheapest path to the solution (all other paths that were cheaper when this path
        # landed on state1 or the solution had a chance, thanks to moving this part of the program
        # out of the for-loop, to get to state1 or the solution at a lower cost but, as we see now,
        # manifestly didn't do that)
        # moved it here because you don't want to say you've explored the state when you first
        # encounter it in the for loop
        pcost = path_cost(path)
        for (state, action) in bsuccessors2(state1).items():
            if state not in explored:
                total_cost = bcost(action) + pcost
                path2 = path + [(action, total_cost), state]
                add_to_frontier(frontier, path2)  # keep least costly path that gets to state path2[-1]
                # this sorting of frontier upon every insert effectively makes frontier a heap
                # sorting is a bit wasteful, though; using a binary search and bisecting the list
                # for an insert would be better
    return []
