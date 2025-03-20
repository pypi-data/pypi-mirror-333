import pytest
from morse_lab import text_to_morse_code, MORSE_CODE_DICT

def test_text_to_morse():
    assert text_to_morse_code("HELLO", MORSE_CODE_DICT) == ".... . .-.. .-.. --- "
    assert text_to_morse_code("SOS", MORSE_CODE_DICT) == "... --- ... "
    assert text_to_morse_code("123", MORSE_CODE_DICT) == ".---- ..--- ...-- "
    assert text_to_morse_code("HELLO WORLD", MORSE_CODE_DICT) == ".... . .-.. .-.. ---  / .-- --- .-. .-.. -.. "
