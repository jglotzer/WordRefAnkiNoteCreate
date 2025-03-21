# WordRefAnkiNoteCreate
A python command line utility for creating Anki Notes using wordreference.com, wordreference.py, Anki and the AnkiConnect AddOn.
This used to be a tedious, manual process - what once took many minutes now takes seconds.
Note: Code does **not** add photos, that is done manually by the user.

Attention has been paid to the look and feel of the created notes, with a color scheme,
use of bold and italics, and element placement on both sides of the note which aids in retention
in a way not unlike how color highlighting aids comprehension with code.

Another goal has been to make the generated HTML nicely formatted so that users can easily modify
the HTML, for example to add additional examples or definitions. By using the \<pre\> tag newlines
entered in the HTML will be rendered as such, obviating the need to add any extra \<br\> tags.

# Usage
```text
usage: WordReferenceAnkiNoteCreate.py [-h] [-c] [-i] [-n] DICTIONARY_CODE word

positional arguments:
  DICTIONARY_CODE        dictionary code (e.g. fren for french to english, enfr for english to french)
  word                   word (with optional article) to be translated (e.g. bateau or "un bateau")
                         word can be a quoted string - useful for articles or for multiword expressions.

options:
  -h, --help             show this help message and exit
  -c, --connect          create an Anki Card as well
  -i, --invert           invert in other direction
  -n, --numdefs NUMDEFS  number of defns wanted

Obtain console output *only* by omitting the -c switch. This can be thought of as a "dryrun" mode or as a quick check.
Obtain console output *and* Anki Note by supplying the -c switch. This is really the object of the exercise.

Invert switch is intended to support use case where lookup word is in English but
examples are desired in the foreign language (if omitted examples are also in English).

Numdefs switch is intended to truncate the number of definitions returned
because WordReference often throws in "extra" definitions that may be related by not essential.

The word parameter can have an optional article e.g. "un bateau" ou "bateau" will both look up
the same word but the supplied article will be displayed on the card, helpful for gendered
languages.
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

