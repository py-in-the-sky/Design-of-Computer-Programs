
def inverse(f, delta=1.0/128):
    "returns the inverse of f"
    def f_inv(y):
        # since f is monotonic, f(x) - y has one root
        # use Newton's method to find the root of g(x) = f(x) - y

        # TODO: how can the accuracy be improved for very large and very small
        # numbers without running into ZeroDivision and InfiniteRecursion
        # problems?
        def zero(x): return f(x) - y
        def deriv(x): return (zero(x + delta) - zero(x)) / delta
        def close_enough(x): return abs(zero(x)) < delta
        def improve_guess(x): return x - zero(x) / deriv(x)
        def fixed_point(x): return x if close_enough(x) else fixed_point(improve_guess(x))
        return fixed_point(1.0)

    return f_inv

# Peter Norvig's solution
# notice how similar it is to my solution for finding some random large integer
def PN_inverse(f, delta=1.0/128):
    def f_inv(y):
        low, high = find_bounds(f, y)  # takes first upper bound found and uses previous try as lower bound
        return binary_search(f, y, lo, hi, delta)  # binary search between upper and lower bounds
    return f_inv

def find_bounds(f, y):
    "returns lo, hi such that f(lo) <= y <= f(hi)."
    hi = 1
    while f(hi) < y:
        hi *= 2.0
    lo = 0 if hi==1 else hi/2
    return lo, hi

def binary_search(f, y, lo, hi, delta):
    "given f(lo) <= y <= f(hi), returns x such that abs(f(x) - y) < delta"
    while lo <= hi:
        x = (lo + hi) / 2.0
        fx = f(x)
        if fx < y: lo = x + delta
        elif fx > y: hi = x - delta
        else: return x
    return hi if f(hi) - y < y - f(lo) else lo
