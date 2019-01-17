""" Iteration is fundamental to data processing.
    And when scanning datasets that don;t fit in memory, we need a way to fetch the items lazily
    , that is, one at a time and on demand. This is what the Iterator patten is about"""

""" This Chapter shows how the Iterator pattern is built into the Python Language """

""" Every collection in Python is iterable, and iterators are used internally to support:
    - for loops
    - collection types construction and extension
    - looping over text files line by line
    - list, dict and set comprehensions
    - tuple unpacking
    - unpacking actual parameters with * in function calls.
"""

""" This chapter covers the following topics:
    - How the iter(_) built-in function is used internally to handle iterable objects
    - How to implement the classic Iterator pattern in Python
    - How a generator function works in detail, with line by line descriptions
    - How the classic Iterator can be replaced by a generator function or generator expression
    - Leveraging the general purpose generator functions in the standard library
    - Using the new yield from statement to combine generators
    - A case study: using generator functions in a database conversion utility designed
      to work with large data sets.
    - WHy generators and coroutines look alike but are actually very different and should not be mixed
"""

# 1: a sequence of words
# Example 14-1 : shows a Sentence class that extracts words from a text by index

import re
import reprlib

RE_WORD = re.compile('\w+')

class Sentence:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text) # 're.findall' returns a list with all non-overlapping mathces

    def __getitem__(self, index):
        return self.words[index] # "self.words holds the result of .findall, so we can return the word at the given index

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        # reprlib.repr is a utility function to generate abbreviated string representations
        # of data structures that can be very large
        return 'Sentence(%s)' % reprlib.repr(self.text)

# # Test class'Sentence'
# s = Sentence('"The time has come," the Walrus said,')
# s
# for word in s:
#         print(word)

# Why sequences are iterable: the iter function
# Every Python programmer knows that sequences are iterable. Now we'll see precisely why.


