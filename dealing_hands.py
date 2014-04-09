import random


mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC'] 


def deal(numhands, n=5, deck=mydeck):
    def shuffle_return(deck):
        random.shuffle(deck)
        return deck
    return [shuffle_return(deck)[0:n] for _ in xrange(numhands)]


def hand_percentages(n=700*1000):
    counts = [0]*9
    for i in xrange(n/10):
        for hand in deal(10):
            ranking = hand_rank(hand)[0]
            counts[ranking] += 1
    for i in reversed(xrange(9)):
        print '{}: {}'.format(hand_names[i], 100.*counts[i]/n)
