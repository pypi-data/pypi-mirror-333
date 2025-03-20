# Morse Lab

A package for Morse code conversions.

## Features

- Convert text to Morse code.
- Convert Morse code to text.
- Supports Japanese Wabun Morse Code.

## Installation

You can install the package using pip:

```bash
pip install git+https://github.com/rushiharkal1/morse_lab.git
```

or

```bash
pip install morse-lab
```

## Usage

```python
from morse_lab import text_to_morse_code, morse_code_to_text, japanese_to_english

# Convert text to Morse
print(text_to_morse_code("HELLO WORLD"))  # Output: ".... . .-.. .-.. ---  / .-- --- .-. .-.. -.. "

# Convert Morse to text
print(morse_code_to_text(".... . .-.. .-.. ---"))  # Output: "HELLO"

# Convert Japanese Katakana to English
print(japanese_to_english("コンニチハ"))  # Output: "KO N NI CHI HA"
```

## Running Tests

You can run the tests using `pytest`:

First, clone the repository:
```bash
git clone https://github.com/rushiharkal1/morse_lab.git
```

Then, install pytest if you haven't already:
```bash
pip install pytest
```

Now, you can run the tests:
```bash
pytest tests/
```

## License

This project is licensed under the MIT License.
