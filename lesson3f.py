"""
transitioning to context-free languages

grammar: finite description of a language
language: possibly infinite set of strings

grammar for algebraic expressions (see Udacity course "Programming Languages"):

Exp     =>  Term [+-] Exp | Term
Term    =>  Factor [*/] Term | Factor
Factor  =>  Funcall | Var | Num | [(] Exp [)]
Funcall =>  Var [(] Exps [)]
Exps    =>  Exp [,] Exps | Exp
Var     =>  [a-zA-Z_]\w*
Num     =>  [-+]?[0-9]+([.][0-9])?

now we need a program that understands the format this grammar is in

define a function 'grammar' that can understand this format and return data that's
useful for further down-stream processes
"""

from lesson3e import memo

def grammar(description, whitespace=r'\s*'):
    """
    Convert a description to a grammar. Each line is a rule for a
    non-terminal symbol; it looks like this:

        Symbol => A1 A2 ... | B1 B2 ... | C1 C2 ...

    where the right-hand side is one or more alternatives, separated by
    the '|' sign. Each alternative is a sequence of atoms, separated by
    spaces.  An atom is either a symbol on syme left-hand side, or it is a
    regular expression that will be passed to re.match to match a token.

    Notation for *, +, or ? not allowed in a rule alternative (but ok within a
    token). Use '\' to continue long lines. You must include spaces or tabs
    around '=>' and '|'. That's within the grammar description itself(...?). The
    grammar that gets defined allows whitespace between tokens by default or
    specify '' as the second argument to grammar() to disallow this (or supply
    any regular expression to describe allowable whitespace between
    tokens)."""
    G = {' ': whitespace}
    description = description.replace('\t', ' ')  # no tabs!
    for line in split(description, '\n'):
        lhs, rhs = split(line, ' => ', 1)
        alternatives = split(rhs, ' | ')
        G[lhs] = tuple(map(split, alternatives))
    return G

def split(text, sep=None, maxsplit=-1):
    "like str.split applied to text, but strips whitespace from each piece"
    return [t.strip() for t in text.strip().split(sep, maxsplit) if t]

G = grammar(r'''
Exp     =>  Term [+-] Exp | Term
Term    =>  Factor [*/] Term | Factor
Factor  =>  Funcall | Var | Num | [(] Exp [)]
Funcall =>  Var [(] Exps [)]
Exps    =>  Exp [,] Exps | Exp
Var     =>  [a-zA-Z_]\w*
Num     =>  [-+]?[0-9]+([.][0-9])?
''')

## G = {'Exp': (['Term', '[+-]', 'Exp'], ['Term']),
##      'Term': (['Factor', '[*/]', 'Term'], ['Factor']),
##      ...}

# print G

Fail = (None, None)

def parse(symbol, text, grammar):
    """Example call: parse('Exp', '3*x + b', G).
    Returns a (tree, remainder) pair. If remainder is '', it parsed the whole
    string. Failure iff remainder is None. This is a deterministic PEG parser,
    so rule order (left-to-right) matters. Do 'E => T op E | T', putting the
    longest parse first; don't do 'E => T | T op E'
    Also, no left recursion allowed: don't do 'E => E op T'

    See: http://en.wikipedia.org/wiki/Parsing_expression_grammar

    >>> parse('Exp', 'a * x', G)
    (['Exp', ['Term', ['Factor', ['Var', 'a']], '*', ['Term', ['Factor', ['Var', 'x']]]]], '')
    """
    tokenizer = grammar[' '] + '(%s)'

    def parse_sequence(sequence, text):
        """
        Try to match the sequence of atoms against text.

        Parameters:
        sequence : an iterable of atoms
        text : a string

        Returns:
        Fail : if any atom in sequence does not match
        (tree, remainder) : the tree and remainder if the entire sequence matches text
        """
        result = []
        for atom in sequence:
            tree, text = parse_atom(atom, text)
            if text is None: return Fail
            result.append(tree)
        return result, text

    @memo
    def parse_atom(atom, text):
        """
        Parameters:
        atom : either a key in grammar or a regular expression
        text : a string

        Returns:
        Fail : if no match can be found
        (tree, remainder) : if a match is found
            tree is the parse tree of the first match found
            remainder is the text that was not matched
        """
        if atom in grammar:  # Non-Terminal: tuple of alternatives
            for alternative in grammar[atom]:
                tree, rem = parse_sequence(alternative, text)
                if rem is not None: return [atom]+tree, rem
            return Fail
        else:  # Terminal: match characters against start of text
            m = re.match(tokenizer % atom, text)
            return Fail if (not m) else (m.group(1), text[m.end():])  # the only place where the text advances

    return parse_atom(start_symbol, text)

## for helping you verify that you've written your grammar correctly (e.g., according to the specs)
def verify(G):
    lhstokens = set(G) - set([' '])
    print(G.values())
    rhstokens = set(t for alts in G.values() for alt in alts for t in alt)
    def show(title, tokens): print title, '=', ' '.join(map(repr, sorted(tokens)))
    show('Non-Terms', G)
    show('Terminals', rhstokens - lhstokens)
    show('Suspects', [t for t in (rhstokens-lhstokens) if t.isalnum()])
    show('Orphans ', lhstokens-rhstokens)
