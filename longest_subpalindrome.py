# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes 
# a string as input and returns the i and j indices that 
# correspond to the beginning and end indices of the longest 
# palindrome in the string. 
#
# Grading Notes:
# 
# You will only be marked correct if your function runs 
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!

def longest_subpalindrome_slice(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    text_len = len(text)
    if text_len == 0: return (0, 0)
    text = text.lower()

    def longest_pal(a, b):
        return (longest_pal(a-1, b+1) if a-1 >= 0 and b+1 < text_len and text[a-1] == text[b+1]
                else (a, b))
        # could use a while loop in place of tail recursion for handling very long text
        # tail recursion would be preferable if supported; it's not supported in Python

    def pal_len(tup): return tup[1] - tup[0]

    def try_index(ind):
        "see whether character at index ind can be the center of an even-length palindrome"
        odd, even = (ind, ind), (ind, ind+1) if (ind+1 < text_len and text[ind] == text[ind+1]) else (0, 0)
        return max((longest_pal(*odd), longest_pal(*even)), key=pal_len)

    pal_indeces = i, j = max((try_index(i) for i in xrange(text_len)), key=pal_len)
    return (0, 0) if pal_len(pal_indeces) == 0 else (i, j+1)


# Peter Norvig's solution:
def solution(text):
    if text == '': return (0, 0)
    def length(slice): a,b = slice; return b-a
    candidates = [grow(text, start, end) for start in xrange(len(text)) for end in (start, start+1)]
    return max(candidates, key=length)

def grow(text, start, end):
    while start > 0 and end < len(text) and text[start-1].upper() == text[end].upper():
        start -= 1; end += 1
    return (start, end)


def OLD_longest_subpalindrome_slice(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    N = len(text)
    if N == 0:
        return (0,0)
    elif N % 2 == 0:
        indeces = [N/2 + a * b for a in range(N/2) for b in [1,-1]]
        indeces.pop(0) # remove duplicate N/2
    else:
        indeces = [N/2 + a * b for a in range(N/2 + 1) for b in [1,-1]]
        indeces.pop(0)
        indeces.pop() # remove 0
    # start in middle and cycle outward
    pal_indeces = (0,0,1)
    for i in indeces:
        if pal_indeces[0] / 2.0 >= min(i + 1, N - i, N / 2.0):
            break
        offset, check_even, check_odd = 1, True, True
        even_pal, odd_pal = (0,0,1), (0,0,1)
        while i - offset >= 0 and i + offset <= N:
            # check for odd palindrome
            if check_odd and i + offset <= N -1 and text[i-offset].lower() == text[i+offset].lower():
                odd_pal = (2*offset, i-offset, i+offset+1)
            else:
                check_odd = False
            if odd_pal[0] > pal_indeces[0]:
                pal_indeces = odd_pal
            # check for even palindrom
            if check_even and text[i-offset].lower() == text[i+offset-1].lower():
                even_pal = (2*offset-1, i-offset, i+offset)
            else:
                check_even = False
            if even_pal[0] > pal_indeces[0]:
                pal_indeces = even_pal
            # break from while loop if no longer checking for either even or odd palindromes around index i
            if not check_even and not check_odd:
                break
            offset += 1
    return pal_indeces[1], pal_indeces[2]
    
    
def test():
    L = longest_subpalindrome_slice
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    return 'tests pass'


if __name__ == '__main__':
    print test()
