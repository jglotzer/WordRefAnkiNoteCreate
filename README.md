# WordRefAnkiNoteCreate
A python command line utility for creating Anki Notes using wordreference.com, wordreference.py, Anki and the AnkiConnect AddOn.
This used to be a tedious, manual process - what once took many minutes is now done in seconds.
Note: Code does **not** add photos, that must be done manually by the user.

# Usage
```text
usage: WordReferenceAnkiNoteCreate.py [-h] [-c] DICTIONARY_CODE word

get translation and/or make Anki note using wordreference.com
Console output only without the -c switch.
Console output *and* Anki Note created with the -c switch.

Invert switch is intended to support use case where lookup word is in English but
examples are still given in the foreign language.

Numdefs switch is intended to help truncate the number of definitions returned
often because WordReference throws in "extra" definitions.

The word can have an optional article e.g. "un bateu" ou "bateau" will both look up
the same word but if an article is supplied it will be displayed on the card.

positional arguments:
  DICTIONARY_CODE        dictionary code
  word                   word (with optional article) to translate or to make Anki Card

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
* Change name of Anki Deck to suit (currently set to French).
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

