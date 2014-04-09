from functools import update_wrapper


def decorator(f):
    "make function f a decorator: f wraps function fn"
    # copy documentation from function to wrapper so that the documentation
    # can be carried along when function is wrapped, so that the documentation
    # help for f can be there for debugging
    def _f(fn):
        # update_wrapper returns the updated function
        # hence _f will also return the result of the call f(fn),
        # which is a function that will be updated with the input
        # function's (ie, fn's) documentation
        return update_wrapper(f(fn), fn)
    update_wrapper(_f, f)
    return _f

# for performance
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
            return f(*args)
    return _f

# for expressive power
@decorator
def n_ary(f):
    """Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x."""
    def n_ary_f(x, *args):
        return x if not args else f(x, n_ary_f(*args))
        #return x if len(args) == 0 else f(x, n_ary_f(args[0], *args[1:]))
        #if len(args) == 0:
            #return x
        #return f(x, n_ary_f(args[0], *args[1:]))
    return n_ary_f

# for debugging
@decorator
def countcalls(f):
    "Decorator that makes the function count call to it, in callcounts[f]."
    def _f(*args):
        callcounts[_f] += 1
        return f(*args)
    callcounts[_f] = 0
    return _f

callcounts = {}

# for debugging
@decorator
def trace(f):
    indent = '   '
    def _f(*args):
        signature = '%s(%s)' % (f.__name__, ', '.join(map(repr, args)))
        print '%s--> %s' % (trace.level*indent, signature)
        trace.level += 1
        try:
            result = f(*args)
            print '%s<-- %s == %s' % ((trace.level-1)*indent, 
                                      signature, result)
        finally:
            trace.level -= 1
        return result
    trace.level = 0
    return _f

# for debugging
@decorator
def disabled(f): return f
# e.g. after debugging is complete,
# we can reload our program with the following
# assignments added to get non-debugging behavior:
# trace = disabled
# countcalls = disabled
