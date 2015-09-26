import random
import string
import sys

NUMBERS_TO_LETTERS = {
  '2': ['a', 'b', 'c'],
  '3': ['d', 'e', 'f'],
  '4': ['g', 'h', 'i'],
  '5': ['j', 'k', 'l'],
  '6': ['m', 'n', 'o'],
  '7': ['p', 'q', 'r', 's'],
  '8': ['t', 'u', 'v'],
  '9': ['w', 'x', 'y', 'z'],
}

EXACT_MATCH = 'exact'
PREFIX_MATCH = 'prefix'

class Trie:
  def __init__(self):
    self.children = {}
    self.isWord = False

  # Adds the specified word to the trie
  def addWord(self, word):
    if len(word) == 0:
      self.isWord = True
    else:
      if word[0] not in self.children:
        self.children[word[0]] = Trie()
      self.children[word[0]].addWord(word[1:])

  # Returns a list of (word, match) tuples, where match is EXACT_MATCH or PREFIX_MATCH
  def wordsWithNumericPrefix(self, numericPrefix, currentWord = "", isExactMatch = False):
    words = []
    if len(numericPrefix) == 0:
      for c in self.children:
        words = words + self.children[c].wordsWithNumericPrefix(numericPrefix, currentWord + c, False)
      if self.isWord and not isExactMatch:
        words.append((currentWord, PREFIX_MATCH))
    else:
      if numericPrefix[0] in NUMBERS_TO_LETTERS:
        letters = NUMBERS_TO_LETTERS[numericPrefix[0]]
        for letter in letters:
          if letter in self.children:
            isExactMatch = len(numericPrefix) == 1 and self.children[letter].isWord
            if isExactMatch:
              words.append((currentWord + letter, EXACT_MATCH))
            words = words + self.children[letter].wordsWithNumericPrefix(numericPrefix[1:], currentWord + letter, isExactMatch)
    return words

# Helper function that converts from letters to numeric sequence
# Example: numbersFromLetters('apple') => '27753'
def numbersFromLetters(letters):
  number = ""
  for letter in letters:
    for n in NUMBERS_TO_LETTERS:
      if letter in NUMBERS_TO_LETTERS[n]:
        number = number + n
  return number

def basicTest():
  t = Trie()

  t.addWord('hello')
  t.addWord('world')
  t.addWord('meteor')
  t.addWord('meeting')

  assert sorted([('meteor', PREFIX_MATCH),
                 ('meeting', PREFIX_MATCH)]) == sorted(t.wordsWithNumericPrefix(numbersFromLetters('me')))

def randomTest():
  def randomStringOfLength(l):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(l))

  t = Trie()

  random_prefix = randomStringOfLength(100)
  random_words = []
  for i in range(500):
    random_words.append((random_prefix + randomStringOfLength(i + 10), PREFIX_MATCH))
    t.addWord(random_words[i][0])

  assert sorted(random_words) == sorted(t.wordsWithNumericPrefix(numbersFromLetters(random_prefix)))

def mixedMatchTest():
  t = Trie()

  t.addWord('apple')
  t.addWord('app')
  t.addWord('bob')
  t.addWord('hello')

  assert sorted([('apple', PREFIX_MATCH),
                 ('app', PREFIX_MATCH),
                 ('bob', PREFIX_MATCH)]) == sorted(t.wordsWithNumericPrefix("2"))

  assert sorted([('app', EXACT_MATCH),
                 ('apple', PREFIX_MATCH)]) == sorted(t.wordsWithNumericPrefix("277"))

def main():
  # Uncomment these lines to run unit tests for Trie
  # basicTest()
  # randomTest()
  # mixedMatchTest()

  print "Reading list of words..."

  trie = Trie()
  with open('words.txt') as f:
    for word in f:
      trie.addWord(word.strip())

  while True:
    number = raw_input('Enter numeric input (enter to exit): ')

    if not number:
      break

    matches = trie.wordsWithNumericPrefix(number)

    print "EXACT MATCHES:"
    for match in matches:
      if match[1] == EXACT_MATCH:
        print match[0]

    print "PREFIX MATCHES:"
    for match in matches:
      if match[1] == PREFIX_MATCH:
        print match[0]

if __name__ == '__main__':
  main()
