"""
interpreter for a subset of the regular expressions
also see: http://tinyurl.com/pike-regexp

our subset of regular expressions:.
    ^ (beginning of string)
    $ (end of string)
    '' (empty string)
    * (Kleene star)
    ? (optional)
    . (any character)
    a (a specific character)
    ab (concatentation)

note that we are not considering grouping with parenthesis
hence, the surface form of our subset of regular expressions is a regular language
"""

## Professor Norvig's code, slightly revised by me ##

def search(pattern, text):
    "return True if pattern appears anywhere in text"
    if pattern.startswith('^'):
        return match(pattern[1:], text)
    else:
        return match('.*'+pattern, text)

def match(pattern, text):
    "return True if pattern appears at the start of text"
    if pattern=='':
        return True
    elif pattern=='$':
        return (text=='')
    elif len(pattern)>1 and pattern[1] in '*?':  # character or . followed by * or ?
        pat_1, op, pat_rest = pattern[0], pattern[1], pattern[2:]
        if op=='*':
            return match_star(pat_1, pat_rest, text)  # will be a recursive function
        elif op=='?':
            return ( (match1(pat_1, text) and match(pat_rest, text[1:])) or
                     match(pat_rest, text) )
    else:  # no special characters found near beginning of pattern, except for maybe .
        ## pattern[0] is either a literal character or .
        ## match first character of pattern against text with the special
        ## function, match1; then match the rest of pattern against the rest
        ## of the text
        return (match1(pattern[0], text) and match(pattern[1:], text[1:]))

def match1(p, text):
    "return True if first character of text matches pattern character p"
    if not text: return False  # will catch the case when p!='' and text==''
    return (p=='.' or p==text[0])

def match_star(p, pattern, text):
    "return True if any number of p, followed by pattern, matches text"
    return ( match(pattern, text) or  # match p zero times
             (match1(p, text) and match_star(p, pattern, text[1:])) )  # recursively match p against the beginning of the text

def tests():
    assert search('baa*!', 'sheep said baaaa!')
    assert search('baa*!', 'sheep said baaa humbug') == False
    assert match('baa*!', 'sheep said baaa!') == False
    assert match('baa*!', 'baaaaaa! said the sheep')
    assert search('def', 'abcdefg')
    assert search('def$', 'abcdef')
    assert search('def$', 'abcdefg') == False
    assert search('^start', 'not the start') == False
    assert match('start', 'not the start') == False
    assert match('a*b*c*', 'just anything')
    assert match('x?', 'text')
    assert match('text?', 'text')
    assert match('text?', 'tex')

    def words(text): return text.split()

    assert all(match('aa*bb*cc*', w) for w in words('abc aaabbccc aaaabcccc'))
    assert not any(match('aa*bb*cc*$', w) for w in words('ac aaabbcccd aaaa-b-cccc'))
    assert all(search('^ab.*aca.*a$', w) for w in words('abracadabra abacaa about-acacia'))
    assert all(search('t.p', w) for w in words('tip top tap atypical tepid stop'))
    assert not any(search('t.p', w) for w in words('TYPE teepee tp'))

    return 'tests pass!'

print tests()
