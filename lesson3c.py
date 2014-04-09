"""
complier for the larger set of regular expressions

will compile patterns into functions that operate on text directly, rather than
relying on matchset to do the work of figuring out the pattern and then applying
appropriate procedures on the text

what were previously our pattern constructors will act as components in our
compiler; these components will return functions that will map the text to the
result that matchset would have given us in our interpreter

a pattern is now a composition of functions, where each function does what it's
supposed to do; in our interpreter, a pattern was a composition of tuples, and
then matchset had to parse these tuples and apply the right procedures

these new pattern-functions are compositional, just like regex patterns themselves

hence, the target language of our compiler is Python functions (as opposed to
machine code or byte code)
"""
from lesson3b import null, search  # will search call match from lesson3b or from lesson3c?

### API ###

def match(pattern, text):
    "return longest match of pattern starting at the beginning of text, or None"
    remainders = pattern(text)
    if remainders:
        shortest = min(remainders, key=len)
        return text[: len(text)-len(shortest) ]

## compiler
## patterns return functions that take text as an input and perform the operations
## that matchset used to perform for the pattern; these functions return sets of remainders
def lit(s): return (lambda t: set(t[len(s):]) if t.startswith(s) else null)
def seq(x, y): return (lambda t: set().union( *map(y, x(t)) ))  # applies x to text t and then y to the remainders of x(t)
def alt(x, y): return (lambda t: x(t) | y(t))
def oneof(chars): return (lambda t: set([t[1:]]) if t and t[0] in chars else null)
dot = (lambda t: set([t[1:]]) if t else null)
eol = (lambda t: set(['']) if t=='' else null)
def star(x): return (lambda t: ( set([t]) |  # have already taken care of whole text t here
                                 set(t2 for t1 in x(t) if t1!=t  # no need to progress with t1 if its not a reduction of t
                                     for t2 in star(x)(t1)) ))



### TESTING ###

def test():
    g = alt(lit('a'), lit('b'))
    print g('abc')
    assert g('abc') == set(['bc'])

    assert match(star(lit('a')), 'aaaaabbbaa') == 'aaaaa'
    assert match(lit('hello'), 'hello how are you?') == 'hello'
    assert match(lit('x'), 'hello how are you?') == None
    assert match(oneof('xyz'), 'x**2 + y**2 = r**2') == 'x'
    assert match(oneof('xyz'), '   x is here!') == None

    return 'test passes'

print test()
