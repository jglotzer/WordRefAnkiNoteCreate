import json
from unittest.mock import patch, MagicMock

from WordRefAnkiNoteCreate import (
    gen_clean_filename_base,
    send_json_request,
    gen_word_for_voice_lookup,
)

# -------------------------
#  Pure function tests
# -------------------------

def test_gen_clean_filename_base_simple():
    assert gen_clean_filename_base("maison") == "maison"


def test_gen_clean_filename_base_punctuation():
    # space → "_", apostrophe → "_"; remove '?', '!'
    assert gen_clean_filename_base("l' ami!") == "l__ami"


# --- gen_word_for_voice_lookup ---

def test_gen_word_for_voice_lookup_article_noun():
    # Valid use case: noun with article, no "se"
    out = gen_word_for_voice_lookup("un ", "oiseau", se=False)
    assert out == "un oiseau "


def test_gen_word_for_voice_lookup_se_consonant():
    # Valid SE verb example: consonant start
    out = gen_word_for_voice_lookup("", "débattre", se=True)
    assert "se débattre" in out


def test_gen_word_for_voice_lookup_se_vowel():
    # Valid SE verb example: vowel start, no article
    out = gen_word_for_voice_lookup("", "enfuir", se=True)
    # Should produce "...  - s'enfuir "
    assert "s'enfuir" in out


# -------------------------
#  Mocking urlopen
# -------------------------

@patch("urllib.request.urlopen")
def test_send_json_request_success(mock_urlopen):
    fake_response = {"error": None, "result": 12345}

    mock_file = MagicMock()
    mock_file.read.return_value = json.dumps(fake_response).encode("utf-8")
    mock_urlopen.return_value = mock_file

    result = send_json_request('{"foo": "bar"}')

    assert result == 12345
    mock_urlopen.assert_called_once()
