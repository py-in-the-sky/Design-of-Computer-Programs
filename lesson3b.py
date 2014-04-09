"""
interpreter for a larger set of the regular expressions

in this section, we take a compositional approach to constructing a grammar;
that is, given a regular expression as a grammar, we implement the recognizer
for the grammar's language by composing functions, each of which are recognizers
of smaller grammars

we will develop an API for this compositional approach, which will involve the
functions lit, seq, alt, star, oneof, eol, and dot, which respectively correspond
to a literal character, concatenation, or (e.g., |), Kleene star, one of a set
(e.g., [abc]), the end of a line, and any character (e.g., .)

concept inventory:
    - pattern
    - text & result
    - partial result, which could potentially be built upon or just returned
    - control over iteration, in order to return shortest or longest match, which
      allows us to properly handle partial results; we will address this by making
      the partial results be a set of remainders (what in the text hasn't been
      addressed yet)
"""
### API ###

## regex functions

def search(pattern, text):
    "return earliest/longest match of pattern in text; otherwise, None"
    for i in xrange(len(text)):
        m = match(pattern, text[i:])  # longest match or None
        if m is not None:
            return m

def match(pattern, text):
    "return longest match of pattern starting at the beginning of text, or None"
    remainders = matchset(pattern, text)
    ## if remainders = null, then this if block will be skipped and the function
    ## will return None (the Python default return value)
    if remainders:
        shortest = min(remainders, key=len)
        return text[: len(text)-len(shortest) ]

## pattern constructors
def lit(string):    return ('lit', string)
def seq(x, y):      return ('seq', x, y)
def alt(x, y):      return ('alt', x, y)
def star(x):        return ('star', x)
def plus(x):        return seq(x, star(x))
def opt(x):         return alt(lit(''), x)
def oneof(chars):   return ('oneof', tuple(chars))
dot =                      ('dot',)
eol =                      ('eol',)


### NON-API PRIVATE FUNCTIONS ###

null = frozenset()  # for failed matches between pattern and text

def matchset(pattern, text):
    """match pattern at start of text; return a set of remainders of text
    return a non-empty set of remainders if there is a successful match;
    otherwise return null
    constraint: match + remainder = text"""
    op, x, y = components(pattern)
    if 'lit'==op:
        return set([text[len(x):]]) if text.startswith(x) else null
    elif 'seq'==op:
        return set(t2 for t1 in matchset(x, text) for t2 in matchset(y, t1))
    elif 'alt'==op:
        return matchset(x, text) | matchset(y, text)
    elif 'dot'==op:  # matches any single character
        return set([text[1:]]) if text else null
    elif 'oneof'==op:  # oneof('abc') will match a or b or c; oneof('abc') = ('oneof', ('a', 'b', 'c'))
        ## text.startswith(x) accepts x as either a string or a tuple of strings to check
        return set([text[1:]]) if text.startswith(x) else null
        # return set([text[1:]]) if any(text.startswith(char) for char in x) else null
    elif 'eol'==op:
        return set(['']) if text=='' else null
    elif 'star'==op:
        return ( set([text]) |
                 set(t2 for t1 in matchset(x, text) if t1!=text
                     for t2 in matchset(pattern, t1)) )
    else:
        raise ValueError('unkown pattern: {}'.format(pattern))

## decompose a pattern into its component parts
def components(pattern):
    "return op, x, and y arguments; x and y are None if missing"
    x = pattern[1] if len(pattern)>1 else None
    y = pattern[2] if len(pattern)>2 else None
    return pattern[0], x, y


### TESTING ###

def tests():
    assert lit('abc')         == ('lit', 'abc')
    assert seq(('lit', 'a'),
               ('lit', 'b'))  == ('seq', ('lit', 'a'), ('lit', 'b'))
    assert alt(('lit', 'a'),
               ('lit', 'b'))  == ('alt', ('lit', 'a'), ('lit', 'b'))
    assert star(('lit', 'a')) == ('star', ('lit', 'a'))
    assert plus(('lit', 'c')) == ('seq', ('lit', 'c'),
                                  ('star', ('lit', 'c')))
    assert opt(('lit', 'x'))  == ('alt', ('lit', ''), ('lit', 'x'))
    assert oneof('abc')       == ('oneof', ('a', 'b', 'c'))

    a,b,c = lit('a'), lit('b'), lit('c')
    abcstars = seq(star(a), seq(star(b), star(c)))  # a*b*c*
    dotstar = star(dot)  # .*
    assert search(lit('def'), 'abcdefg') == 'def'
    assert search(seq(lit('def'), eol), 'abcdef') == 'def'
    assert search(seq(lit('def'), eol), 'abcdefg') == None
    assert search(a, 'not the start') == 'a'
    assert match(a, 'not the start') == None
    assert match(abcstars, 'aaabbbccccdef') == 'aaabbbcccc'
    assert match(abcstars, 'junk') == ''
    assert all(match(seq(abcstars, eol), s) == s for s in 'abc aaabbccc aaaabcccc'.split())
    assert all(match(seq(abcstars, eol), s) == None for s in 'cab aaabbcccd aaaa-b-cccc'.split())

    r = seq(lit('ab'), seq(dotstar, seq(lit('aca'), seq(dotstar, seq(a, eol)))))  # ab.*aca.*a$

    assert all(search(r, s) is not None for s in 'abracadabra abacaa about-acacia'.split())
    assert all(match(seq(c, seq(dotstar, b)), s) is not None for s in 'cab cob carob cb carbuncle'.split())  # c.*b
    assert not any(match(seq(c, seq(dot, b)), s) for s in 'crab cb across scab'.split())  # c.b

    assert matchset(('lit', 'abc'), 'abcdef')            == set(['def'])
    assert matchset(('seq', ('lit', 'hi '),
                     ('lit', 'there ')),
                   'hi there nice to meet you')          == set(['nice to meet you'])
    assert matchset(('alt', ('lit', 'dog'),
                    ('lit', 'cat')), 'dog and cat')      == set([' and cat'])
    assert matchset(('dot',), 'am i missing something?') == set(['m i missing something?'])
    assert matchset(('oneof', 'a'), 'aabc123')           == set(['abc123'])
    assert matchset(('eol',),'')                         == set([''])
    assert matchset(('eol',),'not end of line')          == frozenset([])
    assert matchset(('star', ('lit', 'hey')), 'heyhey!') == set(['!', 'heyhey!', 'hey!'])

    assert match(('star', ('lit', 'a')),'aaabcd') == 'aaa'  # a*
    assert match(('alt', ('lit', 'b'), ('lit', 'c')), 'ab') == None  # c|b
    assert match(('alt', ('lit', 'b'), ('lit', 'a')), 'ab') == 'a'  # b|a
    assert search(('alt', ('lit', 'b'), ('lit', 'c')), 'ab') == 'b'  # b|c
    assert search(('star', ('lit', 'a')), 'baab') == 'aa'  # a*
    assert search(('star', ('lit', 'a')), 'bbbb') == ''  # a*
    assert search(('lit', ''), 'abc') ==''  # ''
    return 'tests pass!'

print tests()
