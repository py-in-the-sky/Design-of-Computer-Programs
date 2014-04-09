"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming. 
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)

concepts: names, occupations, gadgets, days (Mon through Fri)
choose the permutations of each group that satifsy conditions 1 through 12    
"""

from itertools import permutations

def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."
    ## your code here; you are free to define additional functions if needed
    names = permutations(range(1,6))
    occupations = permutations(range(1,6))
    gadgets = permutations(range(1,6))
    days = next([Hamming, Knuth, Minsky, Simon, Wilkes]
                for laptop, tablet, iphone, droid, _ in gadgets
                if (laptop is 3
                    and 2 in (iphone, tablet)
                    and tablet is not 5)
                for Hamming, Knuth, Minsky, Simon, Wilkes in names
                if Knuth is Simon+1 and Wilkes is 1
                for programmer, writer, manager, designer, _ in occupations
                if (designer is not 4
                    and laptop is writer
                    and Knuth is manager+1
                    and programmer is not Wilkes
                    and writer is not Minsky
                    and designer is not droid
                    and (Wilkes, Hamming) in ((programmer, droid), (droid, programmer))
                    and manager not in (Knuth, tablet))
                )
    return map(lambda tup: tup[1],
               sorted(zip(days, ['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes'])))
