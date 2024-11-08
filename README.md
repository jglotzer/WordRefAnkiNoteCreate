# WordRefAnkiNoteCreate
A python command line utility for creating Anki Notes using wordreference.com, wordreference.py, Anki and the AnkiConnect AddOn.

This used to be a tedious, manual process - what once took many minutes to create a note now done in seconds.

Note: Code does **not** add photos, that is required to be done manually by the user.

# Usage
```text
usage: WordReferenceAnkiNoteCreate.py [-h] [-c] DICTIONARY_CODE word

get translation and/or make Anki note using wordreference.com
Console output only without the -c switch.
Console output and Anki Note created with the -c switch.

positional arguments:
  DICTIONARY_CODE  dictionary code
  word             word or words (if > 1, 1st considered as an article which is not part of lookup) to translate or to make Anki Card

options:
  -h, --help       show this help message and exit
  -c, --connect    create an Anki Note as well
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

