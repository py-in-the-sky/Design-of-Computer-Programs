from functools import update_wrapper

def n_ary(f):
    """Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x."""
    def n_ary_f(x, *args):
        if len(args) == 0:
            return x
        return f(x, n_ary_f(args[0], *args[1:]))
    # copy documentation from f to n_ary_f so that the documentation
    # can be carried along when f is wrapped, so that the documentation
    # help for f can be there for debugging:
    update_wrapper(n_ary_f, f) 
    return n_ary_f


# One way to use n_ary:

def summation(x,y): return x + y

su = n_ary(summation)


# New way to use n_ary, with wrapper/decorator notation:

@n_ary
def summa(x,y): return x + y

'''
if your module will contain many decorator functions, then
use the following method to define functions as decorators
and keep DRY by not repeating "update_wrapper(g, f)" for
each decorator function definition

def decorator(f):
    "make function f a decorator: f wraps function fn"
    def _f(fn):
        return update_wrapper(f(fn), fn)
    update_wrapper(_f, f)
    return _f

then define n_ary and other wrappers/decorators thus:

@decorator
def n_ary(f):
    """Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x."""
    def n_ary_f(x, *args):
        if len(args) == 0:
            return x
        return f(x, n_ary_f(args[0], *args[1:]))
    return n_ary_f
'''
