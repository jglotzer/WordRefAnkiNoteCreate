# WordRefAnkiNoteCreate
A python command line utility for creating Anki Notes using wordreference.com, wordreference.py, Anki and the AnkiConnect AddOn.
This used to be a tedious, manual process - what once took many minutes now takes seconds.
Note: Code does **not** add photos, that is done manually by the user.

# Usage
```text
usage: WordReferenceAnkiNoteCreate.py [-h] [-c] [-i] [-n] DICTIONARY_CODE word

get translation and/or make Anki note using wordreference.com
Obtain console output *only* by omitting the -c switch.
Obtain console output *and* Anki Note by supplying the -c switch.

Invert switch is intended to support use case where lookup word is in English but
examples are desired in the foreign language (if omitted examples are also in English).

Numdefs switch is intended to truncate the number of definitions returned
because WordReference often throws in "extra" definitions that may be related by not essential.

The word parameter can have an optional article e.g. "un bateu" ou "bateau" will both look up
the same word but the supplied article will be displayed on the card, helpful for gendered
languages.

positional arguments:
  DICTIONARY_CODE        dictionary code (e.g. fren for french to english, enfr for english to french)
  word                   word (with optional article) to be translated (e.g. bateau or "un bateau")
                         word can be a quoted string - useful for articles or for multiword expressions.

options:
  -h, --help             show this help message and exit
  -c, --connect          create an Anki Card as well
  -i, --invert           invert in other direction
  -n, --numdefs NUMDEFS  number of defns wanted
```

# Dependencies
* wordreference.py [wordreference.py](https://github.com/n-wissam/wordreference)
* Anki running with AnkiConnect AddOn installed [AnkiConnect AddOn](https://foosoft.net/projects/anki-connect/)

# User Changes Needed
* Change deck name of Anki Deck to suit (currently set to French).
* Change model name of Note type to suit (current set to Basic and Reversed Card).
* Supply desired 4 character dictionary code on command line.
 * to get list of codes run wordreference.py -l

# Screenshots
Console output:
![bâtonnet_console_screenshot](https://github.com/user-attachments/assets/e60d847b-5c6b-4cb1-8c80-19cb4fd6b882)

Resulting Anki Note created (Photos to be added by user, not added by code):
![bâtonnet_screenshot](https://github.com/user-attachments/assets/b43ea9be-c5ef-4c69-9834-898569f9082b)

# Acknowledgements
* wordreference.com [wordreference.com](https://www.wordreference.com)
* wordreference.py [wordreference.py](https://github.com/n-wissam/wordreference)
* Anki [https://apps.ankiweb.net/](https://apps.ankiweb.net/)
* AnkiConnect [AnkiConnect AddOn](https://foosoft.net/projects/anki-connect/)

