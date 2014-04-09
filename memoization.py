'''
Memoization: looking up a value is much faster than calculating
many complex functions, so checking if the return for a function call
is in the cache will speed up your functions by avoiding calculations.
'''

from functools import update_wrapper

def decorator(f):
    "make function f a decorator: f wraps function fn"
    def _f(fn):
        return update_wrapper(f(fn), fn)
    update_wrapper(_f, f)
    return _f

@decorator
def memo(f):
    '''Decorator that caches the return value for each call to
    f(args).  The when called again with same args, we can just
    look it up.'''
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # for elements of args that can't be dict key
            return f(args)
    return _f
