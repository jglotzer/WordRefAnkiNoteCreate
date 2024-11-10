#! /usr/bin/env python3

# Requires and inspired by wordreference python module https://github.com/n-wissam/wordreference
# This code requires wordreference module.
# This code requires Anki running with the AnkiConnct AddOn installed.
# Download page for AnkiConnect AddOn https://ankiweb.net/shared/info/2055492159
# Home page for AnkiConnect https://foosoft.net/projects/anki-connect/
import wordreference as wr
import argparse
import json
import urllib.request

# Desired JSON to be sent to AnkiConnect (see home page for AnkiConnect)
# {
#     "action": "addNote",
#     "version": 6,
#     "params": {
#         "note":
#             {
#                 "deckName": "French",
#                 "modelName": "Basic",
#                 "fields": {
#                     "Front": "front content",
#                     "Back": "back content"
#                    }
#                 }
#             }
#  }
# NB: more complex options are possible, see AnkiConnect Home page.
# NB: deckName is hardcoded here - change according to preference.

json_format_str = '{\
                    "action": "addNote",\
                    "version": 6,\
                    "params": {\
                        "note":\
                           {\
                               "deckName": "French",\
                               "modelName": "Basic",\
                               "fields": {\
                                   "Front": "front content",\
                                   "Back":  "back content"\
                                }\
                      }\
            }\
  }'

# These colors correspond to the Terminal Color commands after a cut and paste from Terminal using "Copy HTML" command.
yellow = '#FCE94F'
cyan =   '#34E2E2'
purple = '#AD7FA8'

# Use a passed in Json String to send an addNote command to the Anki Connect server.
# Code modified from that on AnkiConnect website.
def invoke_json(requestJsonString):
    encodedJsonString = requestJsonString.encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', encodedJsonString)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

# Print translations to the terminal in an Anki Card specific way.
def print_translations(translations):
    for value in translations.values():
        print ("\033[92m" + value['word'] + "\033[00m")
        for meaning in value["meanings"]:
            print("\033[96m" + meaning + "\033[00m", end=' ')
        print ("\033[95m",   value['definition'])

# Gen the HTML code for the translations that will go on back of created card.
def gen_translations_for_connect(translations):
    return_str = "<pre>"
    for value in translations.values():
        return_str += f"<font color={cyan}>"
        for meaning in value["meanings"]:
            return_str += f"{meaning} " # meaning is English Meaning.
        return_str += f"</font> &nbsp;&nbsp; <font color={purple}>{value['definition']}</font><br>" #definition is French definition.
    return return_str[:-4] + "</pre>" # get rid of last <br>, close tag.

# Print examples to the terminal in an Anki Card specific way.
def print_examples(translations, invert):
    print('\033[3m', end='')
    for value in translations.values():
        for examples_list in value["examples"]:
            for example in range(len(examples_list)):
                if (not example and not invert) or (example and invert): # Only want French examples, not their English translations.
                    print("\033[93m"  + examples_list[example])
    print('\033[0m', end='')

# Gen the HTML code for the examples that will go on front of created card.
def gen_examples_for_connect(translations, invert):
    return_str=f"<i><font color={yellow}>"
    num_examples = 0
    for value in translations.values():
        for examples_list in value["examples"]:
            for example in range(len(examples_list)):
                if (not example and not invert) or (example and invert): # Only want French examples, not their English translations.
                    return_str += f"{examples_list[example]}<br>"
                    num_examples += 1
    if num_examples > 0:
        return_str = return_str[:-4] # get rid of last <br> tag if at least 1 example.
    return return_str + "</font></i>" # close tags.

def parse_arguments():
    parser = argparse.ArgumentParser(description="get translation and/or make Anki Card using wordreference.com ")
    parser.add_argument("dictionary_code", help="dictionary code", choices=["enar","enzh","encz","ennl","enfr","ende","engr","enis","enit","enja","enko","enpl","enpt","enro","enru","enes","ensv","entr","aren","czen","deen","dees","esde","esen","esfr","esit","espt","fren","fres","gren","isen","iten","ites","jaen","koen","nlen","plen","pten","ptes","roen","ruen","sven","tren","zhen"], metavar ="DICTIONARY_CODE")
    parser.add_argument("-c", "--connect", help="create an Anki Card as well", action='store_true')
    parser.add_argument("-i", "--invert",  help="invert in other direction", action='store_true')
    parser.add_argument("word", nargs='+',  help = "word (with optional article) to translate or to make Anki Card")
    args = parser.parse_args()
    return args

# usage: WordReferenceAnkiNoteCreate.py [-h] [-c] DICTIONARY_CODE [article] word

# get translation and/or make Anki Card using wordreference.com

# positional arguments:
#   DICTIONARY_CODE  dictionary code
#   article          optional article (e.g. le, la, un, une) not used in lookup but used to create card
#   word             word to translate or to make Anki Card

# options:
#   -h, --help       show this help message and exit
#   -c, --connect    create an Anki Card as well
#   -i, --invert     invert direction
def main():
    args = parse_arguments()
    # If more than one token in words consider the first to be an article which is not part of lookup.
    # If only one token in words then article is the empty string.
    article=""
    # Case of optional argument e.g. la maison
    if len(args.word) > 1:
        article = args.word[0] + " "
        word = args.word[1]
    # case of no optional argument e.g. aller
    else:
        word = args.word[0]

    # Get translations data from wordreference module.
    translations, *_  = wr.define_word(word, args.dictionary_code)
    print('\n')
    # Always print retrieved data.
    print_examples(translations, args.invert)
    print('\n')
    print_translations(translations)
    print('\n')
    # If connect argument is given also generate a card using Anki Connect.
    if args.connect:
       tmp_front_str = gen_examples_for_connect(translations, args.invert)
       front_str = f"<pre><b>{article}{word}</b></font><br><br>" + tmp_front_str + "</pre>"
       # Encode double quotes to protect JSON
       front_str = front_str.replace('"', "&quot;")
       back_str = gen_translations_for_connect(translations)
       # Encode double quotes to protect JSON
       back_str = back_str.replace('"', "&quot;")
       data = json.loads(json_format_str)
       data['params']['note']['fields']['Front'] = front_str
       data['params']['note']['fields']['Back'] = back_str
       json_string = json.dumps(data, ensure_ascii=False) # Don't want to escape non-ASCII chars
       result = invoke_json(json_string)
       print('Created a new Anki card: {}\n'.format(result))

if __name__ == '__main__':
    main()
