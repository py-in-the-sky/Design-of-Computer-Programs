'''
general solution for least-cost searches

concept inventory: paths, path_cost, states, actions, action_cost, successors, start, goal

how to represent these concepts?

paths: [state, action, state...]

path_cost: number

states: atomic; anything that fits the particular problem (the problem-specific
        successors function will deal with this; see lesson 4 "Shortest Path Search")

actions: atomic as well

action_cost: number

successors: state -> {state: action}

start: atomic

goal: state -> bool

states, actions, and start will be atomic to our general solution and their innner structure
will be hidden from our solution, known only to the successors and goal functions

the inner workings of successors and goal will be problem-specific and hidden from our general solution,
and our solution's interface to them will be their signatures as well as the state-action dict and bool,
respectively, that they return

our solution: lowest_cost_search(start, successors, goal, cost) -> path
'''

def final_state(path): return path[-1]


def path_cost(path):
    if len(path) < 3:
        return 0
    else:
        action, total_cost = path[-2]
        return total_cost


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
        frontier.sort(key=path_cost)  # keep heap in sorted order (sorted by path_cost)


def lowest_cost_search(start, successors, is_goal, action_cost):
    """Return the lowest cost path, starting from start state,
    and considering successors(state) => {state:action,...},
    that ends in a state for which is_goal(state) is true,
    where the cost of a path is the sum of action costs,
    which are given by action_cost(action)."""
    # no longer reflects knowledge of internal structure of states (e.g., start); it is therefore more general
    explored = set()  # set of states we have visited
    frontier = [ [start] ]  # heap of paths we have blazed (ordered by cost)
    while frontier:
        path = frontier.pop(0)
        state1 = final_state(path)
        # test for solution after path's pulled off heap, rather than before it's put into heap
        if is_goal(state1):
            return path
        explored.add(state1)
        pcost = path_cost(path)
        for (state, action) in successors(state1).items():
            if state not in explored:
                total_cost = action_cost(action) + pcost
                path2 = path + [(action, total_cost), state]
                add_to_frontier(frontier, path2)  # insert or keep least costly path that gets to state path2[-1]
    return Fail


Fail = []
