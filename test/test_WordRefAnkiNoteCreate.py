import json
import pytest
from unittest.mock import patch, MagicMock
# https://pavolkutaj.medium.com/how-to-test-printed-output-in-python-with-pytest-and-its-capsys-fixture-161010cfc5ad

from WordRefAnkiNoteCreate import (
    gen_clean_filename_base,
    send_json_request,
    gen_word_for_voice_lookup,
    print_translations,
    print_examples,
)

# -------------------------
# Terminal Control Characters
# -------------------------
terminal_reset = "\033[00m"
italic = "\033[03m"
bgreen = "\033[92m"
byellow = "\033[93m"
bmagenta = "\033[95m"
bcyan = "\033[96m"

# -------------------------
# gen_clean_filename_base
# -------------------------

@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("maison", "maison"),
        ("l' ami!", "l__ami"),
        ("qu'est-ce?", "qu_est-ce"),
        ("a b c", "a_b_c"),
        ("c'est un ami ?", "c_est_un_ami_"),
        ("c'est un ami ?!?!", "c_est_un_ami_")
    ]
)
def test_gen_clean_filename_base(input_str, expected):
    assert gen_clean_filename_base(input_str) == expected


# -------------------------
# gen_word_for_voice_lookup
# -------------------------

@pytest.mark.parametrize(
    "article, word, se, expected_substring",
    [
        ("un ", "oiseau", False, "un oiseau "),
        ("la ", "maison", False, "la maison "),
        ("le ", "chat", False, "le chat "),
        ("", "débattre", True, "se débattre"),
        ("", "enfuir", True, "s'enfuir"),
    ]
)
def test_gen_word_for_voice_lookup(article, word, se, expected_substring):
    out = gen_word_for_voice_lookup(article, word, se=se)
    assert expected_substring in out


# -------------------------
# send_json_request
# -------------------------

@patch("urllib.request.urlopen")
def test_send_json_request_success(mock_urlopen):
    fake_response = {"error": None, "result": 12345}

    mock_file = MagicMock()
    mock_file.read.return_value = json.dumps(fake_response).encode("utf-8")
    mock_urlopen.return_value = mock_file

    assert send_json_request('{"foo": "bar"}') == 12345
    mock_urlopen.assert_called_once()


@pytest.mark.parametrize(
    "translations, expected_out",
    [
        ({1:
         {'word': 'couillon',
          'definition': 'argot (personne bête, stupide) (pejorative)',
          'meanings': ['idiot'], 'examples': [["Ce boulot est à la portée de n'importe quel couillon."]]}},
         f'{bgreen}couillon{terminal_reset}\n{bcyan}idiot{terminal_reset} {bmagenta} argot (personne bête, stupide) '
         f'(pejorative)\n{terminal_reset}\n'),
    ]
)
def test_print_translations(capsys, translations, expected_out):
    print_translations(translations, 1)
    captured = capsys.readouterr()
    assert captured.out == expected_out


@pytest.mark.parametrize(
    "translations, expected_out",
    [
        ({1:
         {'word': 'couillon',
          'definition': 'argot (personne bête, stupide) (pejorative)',
          'meanings': ['idiot'], 'examples': [["Ce boulot est à la portée de n'importe quel couillon."]]}},
         f"{byellow}\nCe boulot est à la portée de n'importe quel couillon.\n{terminal_reset}\n"),
    ]
)
def test_print_examples(capsys, translations, expected_out):
    print_examples(translations, False)
    captured = capsys.readouterr()
    assert captured.out == expected_out
