#------------------
# User Instructions
#
# Hopper, Kay, Liskov, Perlis, and Ritchie live on 
# different floors of a five-floor apartment building. 
#
# Hopper does not live on the top floor. 
# Kay does not live on the bottom floor. 
# Liskov does not live on either the top or the bottom floor. 
# Perlis lives on a higher floor than does Kay. 
# Ritchie does not live on a floor adjacent to Liskov's. 
# Liskov does not live on a floor adjacent to Kay's. 
# 
# Where does everyone live?  
# 
# Write a function floor_puzzle() that returns a list of
# five floor numbers denoting the floor of Hopper, Kay, 
# Liskov, Perlis, and Ritchie.

import itertools

def is_adjacent(floor1, floor2):
    '''(int, int) -> bool
    returns True if floor1 is right above or right below floor2
    '''
    return abs(floor1 - floor2) == 1

def is_higher(floor1, floor2):
    '''(int, int) -> bool
    returns True if floor1 is higher than floor2
    '''
    return floor1 > floor2

def floor_puzzle():
    floors = bottom, _, _, _, top = [1,2,3,4,5]
    orderings = itertools.permutations(floors)

    return next([Hopper, Kay, Liskov, Perlis, Ritchie]
                for Hopper, Kay, Liskov, Perlis, Ritchie in orderings
                if is_higher(Perlis, Kay)  # prob of failing roughly 1/2
                if not is_adjacent(Ritchie, Liskov)  # roughly 1/2
                if not is_adjacent(Liskov, Kay)  # roughly 1/2
                if Liskov not in (top, bottom)  # roughly 2/5
                if Hopper is not top  # roughly 1/5
                if Kay is not bottom  # roughly 1/5
                ) 

print floor_puzzle()
