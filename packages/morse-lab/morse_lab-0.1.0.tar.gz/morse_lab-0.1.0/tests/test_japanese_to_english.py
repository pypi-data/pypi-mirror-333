import pytest
from morse_lab import japanese_to_english, JAPANESE_TO_ENGLISH

def test_japanese_to_english():
    assert japanese_to_english("カタカナ") == "KA TA KA NA"
    assert japanese_to_english("コンニチハ") == "KO N NI CHI HA"
    assert japanese_to_english("ワタシ") == "WA TA SHI"
    assert japanese_to_english("ニホンゴ") == "NI HO N GO"
