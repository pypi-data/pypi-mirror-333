import pytest
from morse_lab import morse_code_to_text, MORSE_CODE_DICT

def test_morse_to_text():
    assert morse_code_to_text(".... . .-.. .-.. --- ", MORSE_CODE_DICT) == "HELLO"
    assert morse_code_to_text("... --- ... ", MORSE_CODE_DICT) == "SOS"
    assert morse_code_to_text(".---- ..--- ...-- ", MORSE_CODE_DICT) == "123"
    assert morse_code_to_text(".... . .-.. .-.. ---  / .-- --- .-. .-.. -.. ", MORSE_CODE_DICT) == "HELLO WORLD"
