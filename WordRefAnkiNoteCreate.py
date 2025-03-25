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
#                 "modelName": "Basic (and reversed card)",
#                 "fields": {
#                     "Front": "front content",
#                     "Back": "back content"
#                    }
#                 }
#             }
#  }
# NB: more complex options are possible, see AnkiConnect Home page.
# NB: deckName is hardcoded here - change according to preference.
# NB: modelName is hardcoded here - change according to preference.

json_format_str = '{\
                    "action": "addNote",\
                    "version": 6,\
                    "params": {\
                        "note":\
                           {\
                               "deckName": "French",\
                               "modelName": "Basic (and reversed card)",\
                               "fields": {\
                                   "Front": "front content",\
                                   "Back":  "back content"\
                                }\
                      }\
            }\
  }'

# HTML color codes that exactly match the Ascii Terminal codes.
yellow  = '#FCE94F'
cyan    = '#34E2E2'
magenta = '#AD7FA8'

# Python escape codes for controlling the terminal when printing.
# Colors are prefixed with 'b' to indicate "bright".
terminal_reset = '\033[00m'
italic         = '\033[03m'
bgreen         = '\033[92m'
byellow        = '\033[93m'
bmagenta       = '\033[95m'
bcyan          = '\033[96m'

# Use a passed in Json String to send an addNote command to the Anki Connect server.
# Code modified from that on AnkiConnect website.
def send_json_request(requestJsonString):
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
def print_translations(translations, num_requested):
    num_found = 0
    for value in translations.values():
        if num_found >= num_requested:
            break
        print (bgreen + value['word'] + terminal_reset)
        # A supplied word can have multiple meanings.
        for meaning in value["meanings"]:
            print(bcyan + meaning + terminal_reset, end=' ')
        # Each of those meanings will have a single definition.
        print (bmagenta,  value['definition'])
        num_found += 1
    print(terminal_reset)

# Gen the HTML code for the translations that will go on back of created card.
def gen_translations_for_connect(translations, num_requested):
    # Tried optimizing the HTML for maximum maintainability but can only do so much because
    # Anki/QtWebEngine changes the HTML to match the DOM.
    return_str = "<pre>"
    num_found = 0
    for value in translations.values():
        if num_found >= num_requested:
            break
        return_str += f"<font color={cyan}>"
        # A supplied word can have multiple meanings.
        for meaning in value["meanings"]:
            return_str += f"{meaning} " # meaning is English Meaning.
        return_str = return_str.rstrip()
        # Each of those meanings will have a single definition.
        return_str += f"</font>    <font color={magenta}>{value['definition']}</font>\n"
        num_found +=1
    # If none found leave template for user to add their own.
    if not num_found:
        return_str += f"<font color={cyan}>  </font>     <font color={magenta}>  </font>\n"
    return_str += "\n\n\n</pre>" # Add space for pics and close tag.
    return return_str.replace('"', "&quot;") # Protect JSON from double quotes by encoding them.

# Print examples to the terminal in an Anki Card specific way.
def print_examples(translations, invert):
    print(byellow)
    for value in translations.values():
        for examples_list in value["examples"]:
            for example_index in range(len(examples_list)):
                # Only want French examples, not English translations.
                # This means example_index of 0 in non invert case.
                # or example_index non-zero in invert case.
                if (not example_index and not invert) or (example_index and invert):
                    # Can have multiple phrases separated by a double space.
                    print(examples_list[example_index].replace("  ", "\n"))
    print(terminal_reset)

# Gen the HTML code for the examples that will go on front of created card.
def gen_examples_for_connect(translations, invert):
    return_str=f"<i><font color={yellow}><br>\n"
    for value in translations.values():
        for examples_list in value["examples"]:
            for example_index in range(len(examples_list)):
                # Only want French examples, not English translations.
                # This means example_index of 0 in non invert case.
                # or example_index non-zero in invert case.
                if (not example_index and not invert) or (example_index and invert):
                    # Can have multiple phrases separated by a double space.
                    return_str += examples_list[example_index].replace("  ", "\n") + "\n"
    return_str += "</font></i></pre>" # close tags.
    return return_str.replace('"', "&quot;") # Protect JSON from double quotes by encoding them.

def parse_arguments():
    parser = argparse.ArgumentParser(description="get translation and/or make Anki Note using wordreference.com ")
    parser.add_argument("dictionary_code", help="dictionary code", choices=["enar","enzh","encz","ennl","enfr","ende","engr","enis","enit","enja","enko","enpl","enpt","enro","enru","enes","ensv","entr","aren","czen","deen","dees","esde","esen","esfr","esit","espt","fren","fres","gren","isen","iten","ites","jaen","koen","nlen","plen","pten","ptes","roen","ruen","sven","tren","zhen"], metavar ="DICTIONARY_CODE")
    parser.add_argument("-c", "--connect", help="create an Anki Note as well", action='store_true')
    parser.add_argument("-i", "--invert",  help="invert in other direction", action='store_true')
    parser.add_argument("-n", "--numdefs", type=int, help="number of defns wanted")
    parser.add_argument("word", nargs='+',  help = "word (with optional article) to translate or to make Anki Note")
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
    invert = args.invert
    dictionary_code = args.dictionary_code
    connect = args.connect
    if args.numdefs:
        numdefs = args.numdefs
    else:
        numdefs = 9999

    # Get translations data from wordreference module.
    translations, *_  = wr.define_word(word, dictionary_code)

    # Always print retrieved data.
    print_examples(translations, invert)
    print_translations(translations, numdefs)

    # If connect argument is given also generate a card using Anki Connect.
    if connect:
       # Format the supplied word, add examples, leave space for pics, close <pre> tag.
       front_str = f"<pre><b>{article}{word}</b>" + gen_examples_for_connect(translations, invert)
       back_str = gen_translations_for_connect(translations, numdefs)
       data = json.loads(json_format_str)
       data['params']['note']['fields']['Front'] = front_str
       data['params']['note']['fields']['Back'] = back_str
       json_string = json.dumps(data, ensure_ascii=False) # Don't want to escape non-ASCII chars
       result = send_json_request(json_string)
       print('Created a new Anki Note with ID:{}\n'.format(result))

if __name__ == '__main__':
    main()
