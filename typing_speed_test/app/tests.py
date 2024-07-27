import pytest
from app import utils

@pytest.mark.parametrize("accent, words, expected", 
    [("on", ['sada', 'izgleda', 'ja', 'godine', 'ali'], ['sada', 'izgleda', 'ja', 'godine', 'ali']), 
    ("on", ['Taća', 'kažeš', 'đubre', 'Ćilim', 'Koštana'], ['Taća', 'kažeš', 'đubre', 'Ćilim', 'Koštana']),
    ("off", ['Taća', 'kažeš', 'đubre', 'Ćilim', 'Koštana'], ['Taca', 'kazes', 'djubre', 'Cilim', 'Kostana']),
    ("off", ['sada', 'izgleda', 'ja', 'godine', 'ali'], ['sada', 'izgleda', 'ja', 'godine', 'ali']),
    ("off", ['čćšđž', 'ČĆŠĐŽ'], ['ccsdjz', 'CCSDjZ']),
    ("off", ['äöüß', 'ÄÖÜẞ'], ['aouss', 'AOUSS']),
    ])
def test_add(accent, words, expected):
    assert utils.accent_trim(accent, words) == expected


