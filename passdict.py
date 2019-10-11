# passdict.py

# Randomly select words from a dictionary file to use as a passphrase.

# Command line arguments: 
#    nw    = number of words to select
#    nmin  = minimum total number of characters in words (excluding separating spaces)

# Example:
# The following command would return 4 randomly selected words from the dictionary file totalling at least 25 characters.
#
#     python passdict.py 4 25
# 

# D. W. Hoard

# v1.0 - 20190918
# v1.1 - 20191003: added extra shuffle of words list


# import needed packages and routines
import sys
import random
from random import SystemRandom
from math import log2
from math import ceil

# DEFAULT VALUE: pick this many words in each set
nw=3
# DEFAULT VALUE: force word sets to have at least this many characters in total
nmin=11

# dictionary file name
dictfile = 'passdict.txt'

# check for command line arguments
if len(sys.argv) > 1:
    nw=int(sys.argv[1])
if len(sys.argv) > 2:
    nmin=int(sys.argv[2])
if len(sys.argv) > 3:
    print('*** WARNING: Ignoring extra command line arguments')

print('\nPicking '+str(nw)+' words with total length of at least '+str(nmin)+' characters.\n')

# read dictionary file 
# (ignore lines with leading # and remove whitespace and trailing newlines)
words=[]
with open(dictfile, 'r') as f:
    for line in f:
        if not line.lstrip().startswith('#'):
            words.append(line.lstrip().rstrip('\n'))
f.closed

# Scramble list (extra layer of randomization)
random.shuffle(words)

# how many words in the dictionary?
Nwords=len(words)

# select words - repeat as long as the total characters is < nmin
lswout1 = -1 # counter for total characters in selected words
counter = 0  # selection loop iteration counter
maxcounter = 1000  # bail out gracefully if we perform this many loops without success
while lswout1 < nmin:
    # check if maximum number of iterations has been exceeded
    if counter > maxcounter:
       break
    # increment counter 
    counter += 1

    # implement OS-level randomization (better than python internal)
    r = SystemRandom()

    # create list of randomly selected words from dictionary
    # (avoid duplicates by assigning to a set)
    wout = set()
    while len(wout) < nw:
        wout.add(words[r.randint(0,Nwords-1)])

    # count total number of characters in selected words
    lswout1 = sum(len(w) for w in wout)
    lswout2 = lswout1+nw-1  # counts the space between each word as an included character

if counter > maxcounter:
    print('*** ERROR: Cannot find requested words.')
    print('*** ERROR: Try again with fewer words and/or smaller total character count.\n')
else:
    # output word list in vertical and horizontal format
    swout = ''
    for word in wout:
       print(word.lower())
       swout += word.lower()+' '
    print('\n'+swout+'\n')

    # output statistical characteristics of selected words
    print('Number of words in dictionary =', Nwords)
    print('Total length of selected words = '+str(lswout1)+' characters ('+str(lswout2)+' with separating spaces)')

    # Entropy of passphrase out of the full dictionary set.
    # Repeating words is not allowed, so 
    #    S = alog2(N) + alog2(N-1) + alog2(N-2) + ... + alog2(N-(n-1))
    # where
    #    n = number of characters/words in password/passphrase
    #    N = total number of available characters/words
    S0 = 0.0
    for n in range(nw):
        S0 += log2(Nwords-n)
    print('Entropy (in '+str(Nwords)+'-word set)                = %.0f bits' % (S0))
    
    # Entropy of passphrase on the basis of just the a-z letters
    # Repeating characters is allowed, so S = alog2(N)*n
    S = log2(26)*lswout1
    print('Entropy (in '+str(26)+'-character set; w/o spaces) = %.0f bits' % (S))
    # Also calculate the entropy of space is counted as a character
    S = log2(27)*lswout2
    print('Entropy (in '+str(27)+'-character set; w/ spaces)  = %.0f bits' % (S))
   
    # Character length of a passphrase of equivalent entropy assuming 
    # all characters can be used.  This allows comparison of the word-based 
    # passphrase to a traditional character-based "nonsense" password.
    # Ideally, want the word-based passphrase to have an entropy equal or 
    # larger than a traditional password with a large (n > 12) number of characters.
    nset = [95]
    for n in nset:
     eqlen = ceil(S0/log2(n))
     print('Equivalent password length using '+str(n)+'-character set = '+str(eqlen)+' characters')

    print('  (95-character set includes a-z, A-Z, 0-9, all punctuation marks and space)\n')

