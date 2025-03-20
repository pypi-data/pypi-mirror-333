from morse_lab import text_to_morse_code, morse_code_to_text, WABUN_MORSE_CODE_DICT

def test_wabun_morse_conversion():
    original_text = "カタカナ"  
    morse = text_to_morse_code(original_text, WABUN_MORSE_CODE_DICT)  
    decoded_text = morse_code_to_text(morse, WABUN_MORSE_CODE_DICT) 
    assert decoded_text == original_text