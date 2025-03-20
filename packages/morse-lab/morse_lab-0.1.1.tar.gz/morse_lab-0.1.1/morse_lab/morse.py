import winsound # OPTIONAL
import time # OPTIONAL

# Morse Code dictionary "a b c d e f g h i j k l m n o p q r s t u v w x y z 1 2 3 4 5 6 7 8 9 0 , . ? / - ( ) ' " & ; _ + = @"
MORSE_CODE_DICT = {
    # Alphabets
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
    'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.',
    'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-',
    'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
    # Numbers
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', 
    '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    # Symbols
    ',': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-', 
    '(': '-.--.', ')': '-.--.-', "'": '.----.', '"': '.-..-.', '&': '.-...', ';': '-.-.-.', 
    '_': '..--.-', '+': '.-.-.', '=': '-...-', '@': '.--.-.'
}

# Japanese to English
JAPANESE_TO_ENGLISH = {
    # Katakana
    'ア': 'A', 'イ': 'I', 'ウ': 'U', 'エ': 'E', 'オ': 'O',
    'カ': 'KA', 'キ': 'KI', 'ク': 'KU', 'ケ': 'KE', 'コ': 'KO',
    'サ': 'SA', 'シ': 'SHI', 'ス': 'SU', 'セ': 'SE', 'ソ': 'SO',
    'タ': 'TA', 'チ': 'CHI', 'ツ': 'TSU', 'テ': 'TE', 'ト': 'TO',
    'ナ': 'NA', 'ニ': 'NI', 'ヌ': 'NU', 'ネ': 'NE', 'ノ': 'NO',
    'ハ': 'HA', 'ヒ': 'HI', 'フ': 'FU', 'ヘ': 'HE', 'ホ': 'HO',
    'マ': 'MA', 'ミ': 'MI', 'ム': 'MU', 'メ': 'ME', 'モ': 'MO',
    'ヤ': 'YA', 'ユ': 'YU', 'ヨ': 'YO',
    'ラ': 'RA', 'リ': 'RI', 'ル': 'RU', 'レ': 'RE', 'ロ': 'RO',
    'ワ': 'WA', 'ヲ': 'WO', 'ン': 'N',
    
    # Voiced Sounds
    'ガ': 'GA', 'ギ': 'GI', 'グ': 'GU', 'ゲ': 'GE', 'ゴ': 'GO',
    'ザ': 'ZA', 'ジ': 'JI', 'ズ': 'ZU', 'ゼ': 'ZE', 'ゾ': 'ZO',
    'ダ': 'DA', 'ヂ': 'JI', 'ヅ': 'ZU', 'デ': 'DE', 'ド': 'DO',
    'バ': 'BA', 'ビ': 'BI', 'ブ': 'BU', 'ベ': 'BE', 'ボ': 'BO',
    'パ': 'PA', 'ピ': 'PI', 'プ': 'PU', 'ペ': 'PE', 'ポ': 'PO',

    # Numbers
    '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
    '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',

    # Symbols
    ',': ',', '.': '.', '?': '?', '/': '/', '-': '-',
    '(': '(', ')': ')', "'": "'", '"': '"', '&': '&',
    ';': ';', '_': '_', '+': '+', '=': '=', '@': '@'
}


# Function to convert Japanese text to English letters
def japanese_to_english(text):
    english_text = []
    code_type=JAPANESE_TO_ENGLISH
    
    for letter in text:
        if letter in code_type:
            english_text.append(code_type[letter])
        else:
            english_text.append(letter)  # Keep unknown characters as they are
    
    return ' '.join(english_text)  # Separate English letters with space



# Function to convert text to morse code
def text_to_morse_code(text, code_type=MORSE_CODE_DICT):
    morse_code = ''
    for letter in text.upper():
        if letter in code_type:
            morse_code += code_type[letter] + ' '  # Separate letters with a space
        else:
            morse_code += ' / '  # Separate words with '/'
    return morse_code


# Function to convert morse code to text
def morse_code_to_text(morse_code, code_type=MORSE_CODE_DICT):
    # Reverse the 'code_type' to map Morse code to characters
    REVERSE_MORSE_CODE_DICT = {value: key for key, value in code_type.items()}
    text = ''
    morse_words = morse_code.strip().split(' / ')  # Split by ' / ' for words
    for morse_word in morse_words:
        morse_letters = morse_word.split(' ')  # Split by ' ' for letters
        for code in morse_letters:
            if code in REVERSE_MORSE_CODE_DICT:
                text += REVERSE_MORSE_CODE_DICT[code]
        text += ' '  # Add space between words
    return text.strip()