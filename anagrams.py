#
# Your job is to write a function anagrams(), which takes as input 
# a phrase and an optional argument, shortest, which is an integer 
# that specifies the shortest acceptable word. Your function should
# return a set of all the possible combinations of anagrams. 
#
# Your function should not return every permutation of a multi word
# anagram: only the permutation where the words are in alphabetical
# order. For example, for the input string 'ANAGRAMS' the set that 
# your function returns should include 'AN ARM SAG', but should NOT 
# include 'ARM SAG AN', or 'SAG AN ARM', etc...

"""
letters -- str
    words -- str
    phrase -- str
dictionary -- set(words)
prefixes -- set(prefixes)
shortest -- int; min length of any word in answer
partition of letters in phrase into set of words
alphabetic ordering

there are many concepts to handle here, so we must pace ourselves
and develop intermediate goals and modular design
"""

from functools import update_wrapper
import string

def memo(f):
    cache = {}  # {args: result}
    def _f(*args):
        try:
            result = cache[args]
            return result
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:  # non-hashable args
            return f(*args)
    _f = update_wrapper(_f, f)
    return _f

def anagrams(phrase, shortest=2):
    """Return a set of phrases with words from WORDS that form anagram
    of phrase. Spaces can be anywhere in phrase or anagram. All words 
    have length >= shortest. Phrases in answer must have words in 
    lexicographic order (not all permutations)."""
    
    def _loop(tuples):  # tuples = tuple(tuple(word, remainder))
        # base cases: remainder is '' or next == set([])
        word, remainder = tuples[-1]
        if remainder is '':
            if all(len(w)>=shortest for w,r in tuples):
                results.add(tuples)  # all letters from phrase have been partitioned into valid words
            return
        next_words = find_words(remainder)  # set((word, remainder))
        for tup in next_words:
            _loop(tuples + (tup,))

    # use just letters from phrase, no white space or punctuation
    phrase = ''.join(c for c in phrase if c in string.letters)

    # changed find_words to return (word, remainder) and memoized it
    # initiate process by collecting all single words, and their remainders, that can be made from
    # the letters in phrase
    first_words = [tuple([(word,remainder)]) for word,remainder in find_words(phrase)]
    
    # collect sets of words that parition all letters of phrase
    results = set()
    for f in first_words:
        _loop(f)

    return set([' '.join(sorted(w for w,r in tups)) for tups in results])

       
    
# ------------
# Helpful functions
# 
# You may find the following functions useful. These functions
# are identical to those we defined in lecture. 

def removed(letters, remove):
    "Return a str of letters, but with each letter in remove removed once."
    for L in remove:
        letters = letters.replace(L, '', 1)
    return letters

@memo
def find_words(letters):
    return extend_prefix('', letters, set())

def extend_prefix(pre, letters, results):
    # base cases: pre in WORDS or pre not in PREFIXES
    if pre in WORDS: results.add((pre, letters))
    if pre in PREFIXES:
        for L in letters:
            extend_prefix(pre+L, letters.replace(L, '', 1), results)
    return results  # either empty or not

def prefixes(word):
    "A list of the initial sequences of a word, not including the complete word."
    return [word[:i] for i in range(len(word))]

def readwordlist(filename):
    "Return a pair of sets: all the words in a file, and all the prefixes. (Uppercased.)"
    wordset = set(open(filename).read().upper().split())
    prefixset = set(p for word in wordset for p in prefixes(word))
    return wordset, prefixset

WORDS, PREFIXES = readwordlist('words4k.txt')

# ------------
# Testing
# 
# Run the function test() to see if your function behaves as expected.

def test():
    assert 'DOCTOR WHO' in anagrams('TORCHWOOD')
    assert 'BOOK SEC TRY' in anagrams('OCTOBER SKY')
    assert 'SEE THEY' in anagrams('THE EYES')
    assert 'LIVES' in anagrams('ELVIS')
    assert anagrams('PYTHONIC') == set([
        'NTH PIC YO', 'NTH OY PIC', 'ON PIC THY', 'NO PIC THY', 'COY IN PHT',
        'ICY NO PHT', 'ICY ON PHT', 'ICY NTH OP', 'COP IN THY', 'HYP ON TIC',
        'CON PI THY', 'HYP NO TIC', 'COY NTH PI', 'CON HYP IT', 'COT HYP IN',
        'CON HYP TI'])
    return 'tests pass'

print test()
