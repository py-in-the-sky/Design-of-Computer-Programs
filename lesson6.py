"""
board -- 2D array?
letters -- str
    words -- str
    hand -- str or list
legal play -- fn to generate legal play; tuple to represent play (pos, dir, word)
score -- fn
    letters -- {'z': 10}
    play -- fn
    bonus -- fn to map pos -> val
dictionary -- set(words)
blank tile -- str ' ' or '_'; scoring needs to know about blanks

there are many concepts to handle here, so we must pace ourselves
and develop intermediate goals and modular design
"""

from string import uppercase

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

# first goal: hand and dictionary
# from a given hand, what are all the possible words
# from the dictionary that I can make?

#WORDS = set(file('words4k.txt').read().upper().split())
WORDS, PREFIXES = readwordlist('words4k.txt')

def find_words(hand):  # hand is 7 letters
    "find all words that can be made from letters in hand"
    # the following code is slow because we go through every loop
    # we need to introduce the notion of prefix so that we can stop
    # at, say, 'zq', knowing that no words begin with the prefix 'zq'
    # allowing us to preempt bypass any further loops with 'zq'
    # added "if w not in PREFIXES: continue" to address this inefficiency
    # however, there is a lot of repetition and rigidity here (it only works
    # with 7 letters)
    # this problem can be addressed with a recursive routine
    results = set()
    # for a in hand:
    #     if a in WORDS: results.add(a)
    #     if a not in PREFIXES: continue
    #     for b in removed(hand, a):
    #         w = a+b
    #         if w in WORDS: results.add(w)
    #         if w not in PREFIXES: continue
    #         for c in removed(hand, w):
    #             w = a+b+c
    #             if w in WORDS: results.add(w)
    #             if w not in PREFIXES: continue
    #             for d in removed(hand, w):
    #                 w = a+b+c+d
    #                 if w in WORDS: results.add(w)
    #                 if w not in PREFIXES: continue
    #                 for e in removed(hand, w):
    #                     w = a+b+c+d+e
    #                     if w in WORDS: results.add(w)
    #                     if w not in PREFIXES: continue
    #                     for f in removed(hand, w):
    #                         w = a+b+c+d+e+f
    #                         if w in WORDS: results.add(w)
    #                         if w not in PREFIXES: continue
    #                         for g in removed(hand, w):
    #                             w = a+b+c+d+e+f+g
    #                             if w in WORDS: results.add(w)
    def extend_prefix(w, letters):
        # base cases: w not in PREFIXES; letters==''
        if w in WORDS: results.add(w)
        if w not in PREFIXES: return
        for L in letters:
            extend_prefix(w+L, removed(letters, L))

    extend_prefix('', letters)
    return results

def removed(letters, remove):
    "return letters with each letter from remove removed once"
    for L in remove: letters = letters.replace(L, '', 1)
    return letters

def prefixes(word):
    "a list of all prefixes of word, not including the complete word"
    return [word[:i] for i in xrange(len(word))]

def readwordlist(filename):
    "return a set of words and a set of prefixes from a file of words"
    wordfile = open(filename)
    text = wordfile.read().upper().split()  # .read() puts file into string
    wordset, prefixset = set(text), set(sum((prefixes(w) for w in text), []))
    return wordset, prefixset


### TESTING
hands = {}  # {hand: set(words from WORDS)} for regression testing
# see: http://en.wikipedia.org/wiki/Regression_testing
# unit tests verify that your function is doing the right thing
# regression tests allow you to see whether you've broken things: whether
# results have changed after making a change to the program
def test_words():
    assert prefixes('WORD') == ['', 'W', 'WO', 'WOR']
    assert removed('LETTERS', 'L')   == 'ETTERS'
    t, results = timedcall(map, find_words, hands)
    for ((hand, expected), got) in zip(hands.iteritems(), results):
        assert got = expected, 'For {}: got {}, expected {} (diff {})'.format(
            hand, got, expected, expected ^ got)
    return t


# second goal: legal play
# given a letter already on the board, can my letters form a prefix
# or suffix that, when combined with letter on board, form a word

def word_plays(hand, board_letters):
    """find all word plays from hand that can be made to abut with a letter on the board

    don't worry about collisions with other words/letters on the board or running off the board
    """
    # find prefix + L + suffix; L from board_letters, rest from hand
    results = set()
    for pre in find_prefixes(hand):  #find_prefixes(hand, '', set()):
        for L in board_letters:
            add_suffixes(removed(hand, pre), pre+L, results)
    return results

prev_hand, prev_results = '', set()  # cache for find_prefixes

def find_prefixes(hand):
    "find all prefixes (of words) that can be made from letters in hand"
    global prev_hand, prev_results
    if hand is prev_hand: return prev_results
    results = set()
    def _loop(hand, pre=''):
        # base cases: pre not in PREFIXES; hand==''
        if pre in WORDS or pre in PREFIXES: results.add(pre)
        if pre in PREFIXES:
            for L in hand:
                _loop(hand.replace(L, '', 1), pre+L)
    _loop(hand)
    prev_hand = hand
    prev_results = results
    return results

# def find_prefixes(hand, pre='', results=None):
#     "find all prefixes (of words) that can be made from letters in hand"
#     global prev_hand, prev_results
#     if hand is prev_hand: return prev_results
#     if results is None: results = set()
#     if pre is '': prev_hand, prev_results = hand, results
#     # pre is '' only at top-level call
    
#     if pre in WORDS or pre in PREFIXES: results.add(pre)
#     if pre in PREFIXES:
#         for L in hand:
#             find_prefixes(hand.replace(L, '', 1), pre+L, results)
#     return results

#def add_suffixes(hand, pre, results):
    "return the set of words that can be formed by extending pre with letters in hand"
    # base cases: pre not in PREFIXES or hand==''
    #if pre in WORDS: results.add(pre)
    #if pre in PREFIXES:  # can't form any more words
        #for L in hand:  # see what other words can be formed from valid prefixes
            #add_suffixes(hand.replace(L, '', 1), pre+L, results)
    #return results

def add_suffixes(hand, pre, start, row, results, anchored=True):
    "add all possible suffixes, and accumulate (start, word) pairs in results"
    # base cases: pre in WORDS; pre not in WORDS and not in PREFIXES
    i = start + len(pre)
    if pre in WORDS and anchored and not is_letter(row[i]):
        results.add((start, pre))
    if pre in PREFIXES:
        sq = row[i]
        if is_letter(sq):
            add_suffixes(hand, pre+sq, start, row, results)
        elif is_empty(sq):
            possibilities = sq if isinstance(sq, anchor) else ANY
            for L in hand:
                if L in possibilities:
                    add_suffixes(hand.replace(L, '', 1), pre+L, start, row, results)
    return results

def longest_words(hand, board_letters):
    "return all word plays, longest first"
    return sorted(word_plays(hand, board_letters), key=len, reverse=True)


# third goal: scoring
# score a word and find the top-scoring words

POINTS = dict(A=1, B=3, C=3, D=2, E=1, F=4, G=2, H=4, I=1, J=8, K=5, L=1, M=3, N=1,
                O=1, P=3, Q=10, R=1, S=1, T=1, U=1, V=4, W=4, X=8, Y=4, Z=10, _=0)

def word_score(word):
    "the sum of the individual letter point scores for word"
    return sum(POINTS.get(L, 0) for L in word)

def topn(hand, board_letters, n=10):
    "return a list of the top n words that hand can play, sorted by word score"
    return sorted(word_plays(hand, board_letters), reverse=True, key=word_score)[:n]


# fourth goal: board
# place words on a row while worrying about cross words
# rule: one letter that you play must be adjacent to a letter already on board
# anchor square: square adjacent to a letter on the board

# row = ['|', '.', 'A', ..., '|'] where '.' is an empty spot and '|' is
# a virtual element representing the border of the board

class anchor(set):
    "anchor is where a new word can be placed; has a set of allowable letters"

LETTERS = list(uppercase)
ANY = anchor(LETTERS)  # the anchor that can be any letter

# |A.....BE.C...D.|
mnx, moab = anchor('MNX'), anchor('MOAB')
a_row = row = ['|', 'A', mnx, moab, '.', '.', ANY, 'B', 'E', ANY, 'C', ANY, '.', ANY, 'D', ANY, '|']
a_hand = 'ABCEHKN'

def row_plays(hand, row):
    "return a set of legal plays in a row; a row play is an (start, 'WORD') pair"
    results = set()
    # to each allowable prefix, add all suffixes, keeping words
    for i,sq in enumerate(row[1:-1], 1):  # don't enumerate the virtual border elements
        if isinstance(sq, anchor):
            pre,maxsize = legal_prefix(i, row)
            if pre:  # add to the letters already on the board
                start = i - len(pre)
                add_suffixes(hand, pre, start, row, results, anchored=False)
            else:  # empty to left: go through the set of all possible prefixes
                for pre in find_prefixes(hand):
                    if len(pre) <= maxsize:
                        start = i - len(pre)
                        add_suffixes(removed(hand, pre), pre, start, row, results, anchored=False)
    return results

def legal_prefix(i, row):
    """a legal prefix of an anchor at row[i] is either a string of letters
    already on the board or new letters that fit into an empty space
    return the tuple (prefix_on_board, maxsize) to indicate this
    e.g., legal_prefix(a_row, 9) == ('BE', 2) and for 6, ('', 2)
    """
    s = i
    while is_letter(row[s-1]): s -= 1
    if s < i:  # there is a prefix on the board
        return ''.join(row[s:i]), i-s
    while is_empty(row[s-1]) and not isinstance(row[s-1], anchor): s -= 1
    return ('', i-s)

def is_empty(sq): return sq == '.' or sq == '*' or isinstance(sq, anchor)

def is_letter(sq): return isinstance(sq, str) and sq in LETTERS

def test_row():
    assert legal_prefix(2, a_row) == ('A', 1)
    assert legal_prefix(3, a_row) == ('', 0)
    assert legal_prefix(6, a_row) == ('', 2)
    assert legal_prefix(9, a_row) == ('BE', 2)
    assert legal_prefix(11, a_row) == ('C', 1)
    assert legal_prefix(13, a_row) == ('', 1)
    return 'test_row passes'


# fifth goal: handling complete boards and setting anchors in a row

def a_board():
    "return a sample board"
    return map(list, ['|||||||||||||||||',
                      '|J............I.|',
                      '|A.....BE.C...D.|',
                      '|GUY....F.H...L.|',
                      '|||||||||||||||||'])

def show_board(board):
    "pretty-print a board; will show multiplier if the square not occupied by a letter"
    #for row in board: print ' '.join(row)
    for i,row in enumerate(board):
        for j,square in enumerate(row):
            # print letter if square occupied, else multplier
            print (square if (is_letter(square) or square=='|') else BONUS[i][j]),  # will print one white space between squares
        print  # will print new line between rows

def horizontal_plays(hand, board):
    "find all horizontal plays, (score, (i,j), word) pairs, across all rows"
    results = set()
    for j,row in enumerate(board[1:-1], 1):
        set_anchors(row, j, board)
        #results.update([((i,j),word) for i,word in row_plays(hand,row)])
        for i,word in row_plays(hand, row):
            score = calculate_score(board, (i,j), ACROSS, hand, word)
            results.add((score, (i,j), word))
    return results

def all_plays(hand, board):
    """all plays in both directions
    a play is a (score, pos, dir, word) tuple, where pos is an (i,j) pair
    and dir is ACROSS or DOWN
    """
    hplays = horizontal_plays(hand, board)  # set of ((i,j), word)
    vplays = horizontal(hand, transpose(board))  # set of ((j,i), word)
    return (set([(score, pos, ACROSS, word) for score,pos,word in hplays]) |
            set([(score, (i,j), DOWN, word) for score,(j,i),word in vplays]))

ACROSS, DOWN = (1,0), (0,1)  # directions that words can go

def set_anchors():
    """anchors are empty squares with a neighboring letter
    some are restricted by cross-words to be only a subset of letters
    """
    for i,sq in enumerate(row[1:-1], 1):
        neighborlist = N,S,E,W = neighbors(board, i, j)
        # anchors are squares adjacent to a letter, plus the '*' square
        if sq=='*' or (is_empty(sq) and any(map(is_letter, neighborlist))):
            if is_letter(N) or is_letter(S):  # we have cross-word
                # find letter that fit with the cross (vertical) word
                j2, w = find_cross_word(board, i, j)
                row[i] = anchor(L for L in LETTERS if w.replace('.', L) in WORDS)
            else:  # unrestricted empty square (i.e., any letter will fit)
                row[i] = ANY

def find_cross_word(board, i, j):
    """find the vertical word that crosses board[j][i]
    return (j2, w), where j2 is the starting row and w is the word
    """
    sq = board[j][i]
    w = sq if is_letter(sq) else '.'
    for j2 in range(j, 0, -1):  # prepend w with letters directly above it
        sq2 = board[j2-1][i]
        if is_letter(sq2): w = sq2 + w
        else: break
    of j3 in range(j+1, len(board)):  # append w with letters directly below it
        sq3 = board[j3][i]
        if is_letter(sq3): w = w + sq3
        else: break
    return j2, w

def neighbors(board, i, j):
    "return a list of the contents of four neighboring squares in order of N,S,E,W"
    return [board[j-1][i], board[j+1][i], board[j][i+1], board[j][i-1]]

def transpose(matrix):
    # or: [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    return map(list, zip(*matrix))

def test_board():
    assert find_cross_word(a_board(), 2, 2) == (2, '.U')
    assert find_cross_word(a_board(), 1, 2) == (1, 'JAG')
    assert anchor(L for L in LETTERS if '.U'.replace('.', L) in WORDS) == anchor(['X', 'M', 'N'])
    assert neighbors(a_board(), 2, 2) == ['.', 'U', '.', 'A']
    assert transpose([[1,2,3], [4,5,,6]]) == [[1,4], [2,5], [3,6]]
    assert transpose(transpose(a_board)) == a_board
    b = a_board()
    set_anchors(b[2], 2, b)
    assert b[2] == a_row
    print 'board tests complete'

# sixth goal: scoring
# modified horizontal_plays and all_plays to incorporate scores from calculate_score
# need another representation of the board that holds information about special scoring
# features of the board (e.g., letter multipliers like double- or triple-letter-score squares)

BONUS = [[]]  # gives us the letter and word multipliers for a position on BOARD

def calculate_score(board, pos, dir, hand, word):
    "return the total score for the play"
    total, crosstotal, word_mult = 0, 0, 1
    starti, startj = pos
    di, dj = direction
    other_direction = DOWN if direction==ACROSS else ACROSS
    for n,L in enumerate(word):
        i, j = starti + n*di, startj + n*dj
        sq = board[j][i]
        b = BONUS[j][i]
        word_mult *= 1 if is_letter(sq) else 3 if b==TW else 2 if b in (DW,'*') else 1
        letter_mult = 1 if is_letter(sq) else 3 if b==TL else 2 if b==DL else 1
        total += POINTS[L] * letter_mult
        if isinstance(sq, anchor) and sq is not ANY and direction is not DOWN:
            crosstotal += cross_word_score(board, L, (i,j), other_direction)
    return crosstotal + word_mult * total

def cross_word_score(board, L, pos, direction):
    "return score of a word made in the other direction from the main word"
    i, j = pos
    j2, word = find_cross_word(board, i, j)
    return calculate_score(board, (i, j2), DOWN, L, word.replace('.', L))

def bonus_template(quadrant):
    "make a board from the upper-left quadrant"
    return mirror(map(mirror, quadrant.split()))

def mirror(sequence): return sequence + sequence[-2::-1]

SCRABBLE = bonus_template("""
    |||||||||
    |3..:...3
    |.2...;..
    |..2...:.
    |:..2...:
    |....2...
    |.;...;..
    |..:...:.
    |3..:...*
    """)

DW, TW, DL, TL = '23:;'

def test_score():
    assert mirror('|.....*') == '|.....*.....|'
    assert mirror('^._') == '^._.^'
    assert mirror("""
        ...
        3.*
        """) == ['.....',
                 '3.*.3',
                 '.....']
    assert sorted(all_plays(a_hand, a_board()), reverse=True)
    print 'score tests pass!'

# seventh goal: make play and modify board

def make_play(play, board):
    "put word on board"
    score, (i,j), (di,dj), word = play  # score, start_position, direction, word
    # a board is a list of rows, and each row is a list of characters
    for L in word:
        board[j][i] = L
        i, j = i+di, j+dj
    return board

NOPLAY = None

def best_play(hand, board):
    "return highest-scoring play or NOPLAY"
    # tuples are compared lexicographically
    # so since score is the first element of the tuple hand, no special key is needed for max()
    try: return max(all_plays(hand, board))
    except ValueError: return NOPLAY

def show_best(hand, board):
    print 'Current board:'
    show(board)
    play = best_play(hand, board)
    if play:
        print '\nNew word: {} scores {}'.format(play[-1], play[0])
        show(make_play(play, board))
    else:
        print '\nSorry, no legal plays'
