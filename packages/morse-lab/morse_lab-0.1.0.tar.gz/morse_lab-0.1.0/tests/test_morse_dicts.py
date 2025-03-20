import pytest
from morse_lab import INTERNATIONAL_MORSE_CODE_DICT, AMERICAN_MORSE_CODE_DICT, WABUN_MORSE_CODE_DICT

def test_morse_dicts():
    # Checking some values in each dictionary
    assert INTERNATIONAL_MORSE_CODE_DICT["A"] == ".-"
    assert AMERICAN_MORSE_CODE_DICT["B"] == "-..."
    assert WABUN_MORSE_CODE_DICT["カ"] == "-.-.."
