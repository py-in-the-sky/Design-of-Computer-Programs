"""
generator of a language for a given pattern, using the compiler approach

lesson3a-lesson3c were about recognizers
"""
from lesson3b import null

## compiler
# def lit(s): return (lambda Ns: set([s]) if len(s) in Ns else null)  # Ns = numbers
def lit(s):  # optimize lit(s) by doing the work of computing set([s]) only once and up front
    set_s = set([s])
    return (lambda Ns: set_s if len(s) in Ns else null)
def alt(x, y): return (lambda Ns: x(Ns) | y(Ns))
# def star(x): return (lambda Ns: opt(plus(x))(Ns))
def star(x):
    optplus_x = opt(plus(x))
    return (lambda Ns: optplus_x(Ns))
# def plus(x): return (lambda Ns: genseq(x, star(x), Ns, startx=1))  # tricky
def plus(x):
    star_x = star(x)
    return (lambda Ns: genseq(x, star_x, Ns, startx=1))
# def oneof(chars): return (lambda Ns: set(chars) if 1 in Ns else null)
def oneof(chars):
    set_chars = set(chars)
    return (lambda Ns: set_chars if 1 in Ns else null)
def seq(x, y): return (lambda Ns: genseq(x, y, Ns))
def opt(x): return alt(epsilon, x)
dot = oneof('?')  # you could expand the alphabet to more chars
## we return question mark to represent that dot matches any char
epsilon = lit('')  # the pattern that matches the empty string

def genseq(x, y, Ns, startx=0):  # can reduce most complexity to genseq
    "set of matches to xy whose total len is in Ns"
    ## tricky part: x+ is defined as: x+ = xx*
    ## to stop the recursion, the first x must generate at least 1 char,
    ## and then the recursive x* has that many fewer characters
    ## we use startx=1 to say that x must match at least 1 character
    if not Ns:
        return null
    xmatches = x(set(xrange(startx, max(Ns)+1)))
    Ns_x = set(len(m) for m in xmatches)
    Ns_y = set(n-m for n in Ns for m in Ns_x if n-m>=0)
    ymatches = y(Ns_y)
    return set(m1+m2 for m1 in xmatches for m2 in ymatches if len(m1+m2) in Ns)


### TESTING ###

def test():

    f = lit('hello')
    assert f(set([1, 2, 3, 4, 5])) == set(['hello'])
    assert f(set([1, 2, 3, 4]))    == null

    g = alt(lit('hi'), lit('bye'))
    assert g(set([1, 2, 3, 4, 5, 6])) == set(['bye', 'hi'])
    assert g(set([1, 3, 5])) == set(['bye'])

    h = oneof('theseletters')
    assert h(set([1, 2, 3])) == set(['t', 'h', 'e', 's', 'l', 'r'])
    assert h(set([2, 3, 4])) == null

    def N(hi): return set(xrange(hi+1))
    a,b,c = map(lit, 'abc')
    assert star(oneof('ab'))(N(2)) == set(['', 'a', 'aa', 'ab', 'ba', 'bb', 'b'])
    assert (seq(star(a), seq(star(b), star(c)))(set([4])) ==
            set(['aaaa', 'aaab', 'aaac', 'aabb', 'aabc', 'aacc', 'abbb', 'abbc',
                 'abcc', 'accc', 'bbbb', 'bbbc', 'bbcc', 'bccc', 'cccc']))
    assert (seq(plus(a), seq(plus(b), plus(c)))(set([5])) ==
            set(['aaabc', 'aabbc', 'aabcc', 'abbbc', 'abbcc', 'abccc']))
    assert (seq(oneof('bcfhrsm'), lit('at'))(N(3)) ==
            set(['bat', 'cat', 'fat', 'hat', 'mat', 'rat', 'sat']))
    assert (seq(star(alt(a, b)), opt(c))(set([3])) ==
            set(['aaa', 'aab', 'aac', 'aba', 'abb', 'abc', 'baa', 'bab', 'bac',
                'bba', 'bbb', 'bbc']))
    assert lit('hello')(set([5])) == set(['hello'])
    assert lit('hello')(set([4])) == set()
    assert lit('hello')(set([6])) == set()

    return 'tests pass'

print test()
