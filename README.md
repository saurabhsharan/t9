# T9 Text Entry

## Usage

To run:

````
python t9.py
````

The script will repeatedly prompt you to enter a sequence of numbers, and output both exact and prefix matches. Press enter to exit the program.

## Design

The program loads the list of words (in words.txt) into a trie, for fast prefix matching. When the user enters a sequence of numbers, each number is converted to the associated letters (e.g. '2' => ['a', 'b', 'c']) and the trie is searched for both exact matches and prefix matches with the corresponding letters.

## Tests

To run unit tests on the trie, un-comment lines 104-106 in the `main()` function and run the program.
