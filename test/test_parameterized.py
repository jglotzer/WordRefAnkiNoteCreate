import json
import pytest
from unittest.mock import patch, MagicMock

from WordRefAnkiNoteCreate import (
    gen_clean_filename_base,
    send_json_request,
    gen_word_for_voice_lookup,
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
