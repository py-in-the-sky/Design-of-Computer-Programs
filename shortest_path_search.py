'''
general solution for shortest-path searches (not for least-cost searches)

concept inventory: paths, states, actions, successors, start, goal

how to represent these concepts?

paths: [state, action, state...]

states: atomic; anything that fits the particular problem (the problem-specific
        successors function will deal with this; see lesson 4 "Shortest Path Search")

actions: atomic as well

successors: state -> {state: action}

start: atomic

goal: state -> bool

states, actions, and start will be atomic to our general solution and their innner structure
will be hidden from our solution, known only to the successors and goal functions

the inner workings of successors and goal will be problem-specific and hidden from our general solution,
and our solution's interface to them will be their signatures as well as the state-action dict and bool,
respectively, that they return

our solution: shortest_path_search(start, successors, goal) -> path
'''

def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set()  # sets of states we have visited
    frontier = [ [start] ]  # heap of paths we have blazed (ordered by length)
    while frontier:
        path = frontier.pop(0)
        for (state, action) in successors(path[-1]).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)  # added to end of frontier heap
    return Fail

Fail = []
