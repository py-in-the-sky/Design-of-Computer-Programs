"""
Google Prep:

see "Compile Word" near end of lesson 2
see "Avoiding Repetition" in the middle of lesson 3 (compile vs run time; 'lifting')
"""
####
"""
Python notes:
numbers beginning with a 0 are octal numbers
012 is 10; 09 results in an error

cProfile: 
from command line: python -m cProfile mymod.py
in Python interpreter: import cProfile; cProfile.run('myfunc()')

a lambda expression evaluates to a function; therefore, you'll get
the following in an interpreter:
>>> f = eval('lambda x: x**2')
>>> f(2)
4

to see how a function breaks down, or compiles, into Python byte code,
you could follow the example below:
>>> import dis
>>> dis.dis(lambda x: x**2)

generator expressions help us avoid materializing lists that we're never going
to use; if we only need to iterate on a sequence of elements/calculations but
do not need random access, then let's use generators instead of lists;
this will help us avoid using an unecessary amount of memory

the global environment is where all primitive operators are bound
"""
####
"""
going from vague to more concrete understanding of the problem:
includes working on a more concrete understanding of the goal;
includes a concept inventory;
includes understanding the type of data that will be worked on
and the types of operations that will be performed on that
data

moving from problem understanding to definition/specification:
includes a greater degree of formalization of the data types and
operations to be involved;
includes an investingation and inventory of existing resources
for data and functionality

design towards and iterating with specification:
a functional style can help in making the implementation match
the specification;
clarity and correctness are important in writing functions;
every part of the specification should have code that implements it
as well as code that tests the implementation;
tests should reflect all the behavior to be expected from the program;
when writing tests, take the time to review the specification and
brainstorm again all expected behavior, including edge cases/extreme values
writing tests will allow you to progess and rewrite code while being
sure that you haven't broken any of the expected behavior;
tests make it clear what return values you expect from functions, helping
you with function specification prior to implementation

timing and taking measurments brings computer science into the realm of
experimental science.  taking repeated measurments helps to reduce the
effect of external events, randomness, and errors. however, repetition alone
won't solve all problems; if you have a systematic error in your process, then
repetition will only repeat that error again and again.

aspects of a program: correctness, efficiency, debugging infrastructure, elegance,
generality.  always think about separating out these aspects/concerns as much as
possible to achieve a good dose of aspect-oriented design.  let them live, as much
as possible, in different parts of the code, having minimal interfaces among these
aspects

design process review: concept inventory; refine ideas; simple implementation;
back of envelope analysis; refine code; build specific tools to help implement
and debug/evaluate (e.g., timing and count tools); procede in an aspect-oriented
way

in lesson 2, "Future Imports," Peter says he likes using generator functions as he
has in the solution because it MAKES THE LOGIC OF THE MAIN FUNCTION SIMPLE WHILE ALSO
NOT OVERLOADING THE MEMORY BY MATERIALIZING A FULL LIST BEFORE CHECKING ITS ELEMENTS

make the logic of your main functions as clear and as declarative as possible, working
top-down in the spirit of wishful thinking
"""

import time

# my convention: docstrings use " while other strings use either " or '

assert max([3, 4, -5, 0], key=abs) == -5

def tests():
    "all tests for module here"
    # write tests here, using assert
    return 'tests passed!'

def average(numbers):
    return sum(numbers) / float(len(numbers))

def timedcall(fn, *args):
    "call fn w/ args; return time in seconds and result"
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1-t0, result

def timedcalls(n, fn, *args):
    """call fn n times with args in n is an int; if n is float, repeat up to n seconds;
    return min, avg, and max times"""
    if isinstance(n, int):
        times = [timedcall(fn, *args)[0] for _ in xrange(n)]

    elif isinstance(n, float):
        timer, times = 0.0, []
        while timer < n:
            times.append(timedcall(fn, *args)[0])
            timer += times[-1]

    return min(times), average(times), max(times)
