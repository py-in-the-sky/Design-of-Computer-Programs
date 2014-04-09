import re
from decorators import memo
import string

def grammar(description, whitespace=r'\s*'):
    "Convert a human-friendly description into a computer-friendly description"
    G = {' ': whitespace}
    description = description.replace('\t', ' ')  # replace tabs w/ single space
    for line in split(description, '\n'):
        lhs, rhs = split(line, ' => ', 1)
        alternatives = split(rhs, ' | ')
        G[lhs] = tuple(map(split, alternatives))
    return G

def split(text, sep=None, maxsplit=-1):
    "Like str.split applied to text but strips whitespace from each piece."
    return [t.strip() for t in text.strip().split(sep, maxsplit) if t]

def parse(start_symbol, text, grammar):
    """returns (tree, remainder) of text after symbol has been parsed
    a failed parse returns (None, None)

    >>> parse('Exp', 'a * x', G)
    (['Exp', ['Term', ['Factor', ['Var', 'a']], '*', ['Term', ['Factor', ['Var', 'x']]]]], '')
    """
    tokenizer = grammar[' '] + '(%s)'

    def parse_sequence(sequence, text):
        result = []
        for atom in sequence:
            tree, text = parse_atom(atom, text)
            if text is None: return Fail
            result.append(tree)
        return result, text

    # see 'Speedy Parsing' in lesson 3 for why memo is useful here
    # also, parse_atom is made to be an internal function so that it
    # doesn't have to take grammar, a dictionary (read: mutable object),
    # and hence just has to take two strings, which are mutable types
    # hence, parse_atom can be memoized
    @memo
    def parse_atom(atom, text):
        if atom in grammar:  # Non-Terminal: tuple of alternatives
            for alternative in grammar[atom]:
                tree, rem = parse_sequence(alternative, text)
                if rem is not None: return [atom]+tree, rem
            return Fail
        else:  # Terminal: match characters against start of text
            m = re.match(tokenizer % atom, text)
            return Fail if not m else (m.group(1), text[m.end():])  # where the text advances in the code

    return parse_atom(start_symbol, text)

Fail = (None, None)

G = grammar(r'''
    Exp     =>  Term [+-] Exp | Term
    Term    =>  Factor [*/] Term | Factor
    Factor  =>  Funcall | Var | Num | [(] Exp [)]
    Funcall =>  Var [(] Exps [)]
    Exps    =>  Exp [,] Exps | Exp
    Var     =>  [a-zA-Z_]\w*
    Num     =>  [-+]?[0-9]+([.][0-9]*)?
    ''')

# G will look like this:
# G = {'Exp': (['Term', '[+-'], 'Exp'], ['Term']),
#      'Term': (['Factor', '[*/]', 'Term'], ['Factor']),
#       ...}

JSON = grammar(r'''
    value       =>  string | number | object | array | true | false | null
    object      =>  [{] members [}] | [{] [}]
    members     =>  pair [,] members | pair
    pair        =>  string [:] value
    array       =>  [\[] elements [\]] | [\[] [\]]
    elements    =>  value [,] elements | value
    string      =>  ["][^\"\\]*["]
    number      =>  int frac exp | int frac | int exp | int
    int         =>  [-]?[1-9][0-9]*
    frac        =>  [\.][0-9]+
    exp         =>  [eE][-+]?[1-9][0-9]*
    ''')

# array and string: spacing?
# char: robust enough?
# chars       =>  char chars | char
# char        =>  [^\"\\]
# digit       =>  [0-9]
# digit1-9    =>  [1-9]
# digits      =>  digit digits | digit
# e           =>  [eE][-+]?

def json_parse(text):
    return parse('value', text, JSON)

def json_test():
    for e in examples:
        print e, ' == ', json_parse(e), '\n\n'

examples = ['["testing", 1, 2, 3]', '-123.456e+789', '{"age": 21, "state":"CO", "occupation":"rides the rodeo"}']

### HW 3 CHALLENGE PROBLEM: convert re str expression to Unit 3's API
# see API here: https://www.udacity.com/wiki/cs212/unit_3_code
#lit = ' | '.join(string.letters + string.digits)
lit = ' | '.joing(string.printable)
# instead of explicitly constructing all lit values, I could use a negative definition
# just defining lit to contain all single characters that aren't special re characters
REGRAMMAR = grammar('''
    RE      =>  exp RE | exp
    exp     =>  alt | star | plus | seq | dot | oneof | eol | lit
    alt     =>  (exp|exp)
    star    =>  
    plus    =>  
    seq     =>  
    dot     =>  
    oneof   =>  
    eol     =>  
    lit     =>  ''' + lit)

def parse_re(pattern):
    return convert(parse('RE', pattern, REGRAMMAR))

def convert(tree):
    "converts a tree returned from parse to Unit 3's API form"
    pass

def test_re():
    examples = ['a|b', '(a|b)', '[0-9]', '.*']
    for ex in examples:
        print ex, ' == ', parse_re(ex), '\n\n'
### END CHALLENGE PROBLEM

# debugging tool for catching typos in a grammar G (e.g., lines 4 through 11)
def verify(G):
    lhstokens = set(G) - set([' '])
    rhstokens = set(t for alts in G.values() for alt in alts for t in alt)

    def show(title, tokens): print title, '=', ' '.join(sorted(tokens))

    show('Non-Terminals', G)
    show('Terminals', rhstokens - lhstokens)
    show('Suspects', [t for t in (rhstokens - lhstokens) if t.isalnum()])  # suspected typos
    show('Orphans', lhstokens - rhstokens)  # LHS items that never appear on RHS
