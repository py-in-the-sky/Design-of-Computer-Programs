
# Peter Norvig's awesome solution, refactored at the return line of csuccessors to not
# allow negative numbers in successor states

def csuccessors(state):
    """find successors (including ones that result in dining) to the state
    a given state where cannibals can dine has no successors"""
    M1, C1, B1, M2, C2, B2 = state
    if C1 > M1 > 0 or C2 > M2 > 0:
        return {}

    items = []  # is this general enough to be correct for the case when (B1 + B2 > 1)?
    if B1: items += [(sub(state,delta), a+'->') for delta,a in deltas.items()]
    if B2: itmes += [(add(state,delta), '<-'+a) for delta,a in deltas.items()]

    return dict([(state, action) for state,action items if all(n >= 0 for n in state)])  # no negative numbers in states

deltas = {(2, 0, 1,     -2,  0, -1): 'MM',
          (0, 2, 1,      0, -2, -1): 'CC',
          (1, 1, 1,     -1, -1, -1): 'MC',
          (1, 0, 1,     -1,  0, -1): 'M',
          (0, 1, 1,      0, -1, -1): 'C'}

def sub(state, delta):
    "add vectors state and delta"
    return tuple([current - delta for current,delta in zip(state, delta)])

def add(state, delta):
    "subtract vector delta from vector state"
    return tuple([current + delta for current,delta in zip(state, delta)])

Fail = []

def mc_problem(start=(3,3,1,0,0,0), goal=None):
    """solves the missionaries and cannibals problem
    state is 6 ints: (M1, C1, B1, M2, C2, B2) on the start (1) and other (2) sides
    find a path that goes from the initial state to the goal state (which, if not
    specified, is the state with no people or boats on the start side)
    note that this is a minimum-step solution, not a minimum-cost solution, so
    it is more like the pouring-water problems than the bridge problem"""
    if goal is None:
        goal = (0,0,0) + start[:3]
    if start == goal:
        return [start]
    explored = set()  # set of states we have visited
    frontier = [ [start] ]  # heap of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in csuccessors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if state == goal:
                    return path2
                else:
                    frontier.append(path2)  # to the end of the frontier heap
    return Fail
