"""
changing functions as a design pattern (e.g., using function decorators)

changes should ensure backwards compatibility of the functions; that is, the
functions should still be able to be used in the way that they used to, in
addition to new ways that your changes/refactoring seeks to accomplish; the
general idea here is that refactoring/changes should be as local as possible
so that you're not making changes all over the program

consider using the composition of functions when refactoring; because functions
are compositional, changes can be done elegantly

function decorators are a syntactic sugar for achieving function composition

this section exemplifies, among other things, how the compositionality of
functions keep our code DRY
"""
from functools import update_wrapper

## all decorator functions are going to have some basic things in common, so
## in order to not repeat ourselves when creating various decorators, we
## collect all things common to all decorators into one decorator function and
## then decorate all decorators with decorator
def decorator(d):
    "make function d a decorator: d wraps a function fn"
    def _d(fn):
        return update_wrapper(d(fn), fn)  # returns d(fn), along with updated documentation
    update_wrapper(_d, d)
    return _d

# def decorator(d):
#     "@author Darius Bacon"
#     return lambda fn: update_wrapper(d(fn), fn)
#
# decorator = decorator(decorator)

@decorator
def n_ary(f):
    """given a binary function f, return an n-ary function g such that
    g(x, y, z) = f(x, f(y, z)); also allow for f(x) = x
    """
    def n_ary_f(x, *args):
        return f(x, n_ary_f(*args)) if args else x
    # def n_ary_f(x, *args): return reduce(f, args, x)
    return n_ary_f

## walkthrough:
## first:
##
## @decorator
## def n_ary(f):
##     ...
##
## update_wrapper(_d, d) will update decorator with documentation from n_ary
##
## then:
##
## @n_ary
## def seq(x, y):
##     ...
##
## update_wrapper(d(fn), fn) applies n_ary to seq (i.e., d(fn)) and then updates
## the documentation of d(fn) (i.e., n_ary(seq)) to be the documentation of fn (i.e., of seq)

@decorator
def memo(f):
    """decorator that caches the return value for each call to f(args)
    then when called again with same args, we can just look it up"""
    cache = {}  # only mutable variables are available in closures in Python
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            ## some element of args cannot be a dict key (i.e., cannot be hashed)
            return f(*args)
    return _f

@decorator
def countcalls(f):
    "decorator that makes the function count calls to itself in callcounts[f]"
    def _f(*args):
        callcounts[_f] += 1
        return f(*args)
    callcounts[_f] = 0  # initialize entry in callcounts to 0
    return _f

callcounts = {}

## compare fib(n) with and without memoization
@countcalls
@memo
def fib_good(n): return 1 if n<=1 else fib_good(n-1) + fib_good(n-2)

@countcalls
def fib_bad(n): return 1 if n<=1 else fib_bad(n-1) + fib_bad(n-2)

# cases = [(fib_bad, 'without memoization'), (fib_good, 'with memoization')]
# spacing = ' '*7
# header_line = 'n{space}fib(n){space}calls{space}call ratio'.format(space=spacing)
# result_line = '{n}{s1}{res}{s2}{ncalls}{s3}{call_ratio:.3f}'  # s1, s2, s3 correspond to white space

# # print
# for fn,message in cases:
#     print message, fn
#     print header_line
#     for n in xrange(31):
#         result = fn(n)
#         call_ratio = (float(callcounts[fn]) / ncalls) if n else 1
#         ncalls = callcounts[fn]
#         print result_line.format(n=n, res=result,
#                                  ncalls=ncalls, call_ratio=call_ratio,
#                                  s1=' '*(len('n'+spacing)-len(str(n))),
#                                  s2=' '*(len('fib(n)'+spacing)-len(str(result))),
#                                  s3=' '*(len('calls'+spacing)-len(str(ncalls))))
#     print
# print

@decorator
def trace(f):
    indent = ' '*4
    def _f(*args):
        ## --> is a call, <-- is a return
        signature = '{}({})'.format(f.__name__, ', '.join(map(repr, args)))
        print '{}--> {}'.format(trace.level*indent, signature)
        trace.level += 1
        try:
            result = f(*args)
            print '{}<-- {} === {}'.format((trace.level-1)*indent, signature, result)
        finally:
            trace.level -= 1
        return result
    trace.level = 0
    return _f

@trace
def fib(n): return 1 if n<=1 else fib(n-1) + fib(n-2)

# print
# fib(4)
# print

def disabled(f): return f
## now can write, e.g., 'trace = disabled' below the definition of trace in
## order to disable it, instead of going through the file, deleting all
## occurences of trace
