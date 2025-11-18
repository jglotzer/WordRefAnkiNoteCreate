import json
import pytest
from unittest.mock import patch, MagicMock
# https://pavolkutaj.medium.com/how-to-test-printed-output-in-python-with-pytest-and-its-capsys-fixture-161010cfc5ad

from WordRefAnkiNoteCreate import (
    terminal_reset, bgreen, byellow, bmagenta, bcyan, cyan, magenta, yellow,
    gen_clean_filename_base,
    send_json_request,
    gen_word_for_voice_lookup,
    print_translations,
    print_examples,
    gen_translations_for_connect,
    gen_examples_for_connect,
)

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
    "article, word, se, expected",
    [
        ("un ", "oiseau", False, "un oiseau "),
        ("la ", "maison", False, "la maison "),
        ("le ", "chat", False, "le chat "),
        ("", "débattre", True, "débattre   - se débattre "),
        ("", "enfuir", True, "enfuir   - s'enfuir "),
        ("", "éloigner", True, "éloigner   - s'éloigner "),
    ]
)
def test_gen_word_for_voice_lookup(article, word, se, expected):
    generated = gen_word_for_voice_lookup(article, word, se=se)
    assert expected == generated


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
    "translations, expected",
    [
        ({1:
         {'word': 'couillon',
          'definition': 'argot (personne bête, stupide) (pejorative)',
          'meanings': ['idiot'], 'examples': [["Ce boulot est à la portée de n'importe quel couillon."]]}},
         f'<pre><font color={cyan}>idiot</font>    <font color={magenta}>argot'
         f' (personne bête, stupide) (pejorative)</font>\n\n\n\n</pre>'),
    ]
)
def test_gen_translations(translations, expected):
    captured = gen_translations_for_connect(translations, 1)
    assert captured == expected

@pytest.mark.parametrize(
    "translations, expected",
    [
        ({1:
         {'word': 'couillon',
          'definition': 'argot (personne bête, stupide) (pejorative)',
          'meanings': ['idiot'], 'examples': [["Ce boulot est à la portée de n'importe quel couillon."]]}},
         f"<i><font color={yellow}><br>\nCe boulot est à la portée de n'importe quel couillon.\n</font></i>"
         ),
    ]
)
def test_gen_examples(translations, expected):
    captured = gen_examples_for_connect(translations, False)
    assert captured == expected

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
