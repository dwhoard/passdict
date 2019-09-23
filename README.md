# passdict
Python script to generate passphrases of randomly selected words.


## Dictionary File
The words are drawn from a curated dictionary file (passdict.txt) that is stored in the same directory as the python script.
The original dictionary is Webster's Second International Dictionary (1934), which is available at
```
/usr/share/dict/web2
```
in the macOS operating system.
All words shorter than 3 characters or longer than 8 characters were excluded.
The remaining words were hand-selected to exclude archaic words, words with difficult spelling, and homonyms ("sound-alike" words).
American English spellings are used (e.g., "color" instead of "colour").
Some additional words not present in the original dictionary were added.

### WARNING
Curation of the supplied dictionary is not yet finished, so the number of available words is relatively small. I do not recommend using this script to generate passphrases until the entire dictionary has been finished.

### Non-Secret Dictionary
Although it seems like giving away the dictionary would lessen the security of passphrases drawn from it, it does not. Consider: when constructing a normal character-based password, you are using the same alphabet that everyone else knows.
That is, the source for the building blocks of your password is known to everyone.
The enhancements to security provided by a passphrase constructed from a dictionary of words stems from the following:
1. The number of available building blocks (words) in the dictionary is very large (many thousands), whereas the number of characters in the alphabet is limited (less than 100, even when including lower case and upper case letters, numbers 0-9, and all punctuation marks).
1. A passphrase constructed of words is easier to remember than a long, character-based "nonsense" password, which discourages practices such as choosing an easy to remember (short and/or non-random) password, or writing down the password in a convenient location.

### User-Supplied Dictionary
You can supply your own dictionary file by naming it "passdict.txt" or changing the dictionary name in the script (variable "dictfile").
The format of the dictionary file is a single column, one word per line.
Lines preceded by a "#" will be ignored.
Upper case letters are changed to lower case in the output.

## Command line arguments: 
nw    = number of words to select (defaults to 3 if not provided)

nmin  = minimum total number of characters in words (excluding separating spaces; defaults to 18 if not provided)


## Example:
The following command would return 4 randomly selected words from the dictionary file totalling at least 25 characters.
```
python passdict.py 4 25
```

## Passphrase Entropy
In additon to the randomly selected passphrase itself, the script outputs some information about passphrase/password entropy, which is related to the unpredictability (hence, security) of the passphrase.
The passphrase entropy depends on both the length of the passphrase and the size of the character set from which it is constructed (i.e., the number of possible building blocks, such as words or letters).
In general, the higher the entropy value, the more secure is the password/passphrase.

The passphrase entropy (S) is calculated as follows:

S = log2(N)\*n

if words/characters are allowed to repeat, or

S = log2(N) + log2(N-1) + log2(N-2) + ... + log2(N-(n-1))

if words/characters can only be used once, where

n = number of characters/words in password/passphrase

N = total number of available characters/words

log2 = the logarithm function with base 2; i.e., log2(2) = 1, log2(4) = 2, etc.

A passphrase with S bits of entropy has a total of 2\*\*S possible combinations (e.g., S = 40 bits is equivalent to 2\*\*40 = 1,099,511,627,776 possible combinations).
Each additional bit of entropy doubles the number of possible combinations.
On average, a brute force attacker would have to try half of the possible combinations before succeeding (which isn't to say that an attacker couldn't accidentally pick the right combination on the 2nd attempt, but it is equally likely that they pick the right combination on the 2nd to last attempt).

## Script Output
Sample output from the script is shown below.
```
$ python passdict.py 3 20

Picking 3 words with total length of at least 20 characters.

denizen
agnostic
hornet

denizen agnostic hornet 

Number of words in dictionary = 5560
Total length of selected words = 21 characters (23 with separating spaces)
Entropy (in 5560-word set)                = 37 bits
Entropy (in 26-character set; w/o spaces) = 99 bits
Entropy (in 27-character set; w/ spaces)  = 109 bits
Equivalent password length using 95-character set = 6 characters
  (95-character set includes a-z, A-Z, 0-9, all punctuation marks and space)
```
The three entropy values are:
1. The entropy of the passphrase based on it being drawn from the number of words available in the dictionary file.
2. For comparison, the entropy of the passphrase if it was considered as a password of characters drawn from the lower case alphabet.
3. Same as the previous entropy, but including the spaces between words in the passphrase as an additional alphabet character.

The equivalent password length is the number of characters that would have to be included in a normal password (drawn from the indicated 95 character set) to obtain the same entropy as the passphrase generated here.
