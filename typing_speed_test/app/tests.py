import os
import pytest
from app import utils


@pytest.mark.parametrize(
    "accent, words, expected",
    [
        (
            "on",
            ["sada", "izgleda", "ja", "godine", "ali"],
            ["sada", "izgleda", "ja", "godine", "ali"],
        ),
        (
            "on",
            ["Taća", "kažeš", "đubre", "Ćilim", "Koštana"],
            ["Taća", "kažeš", "đubre", "Ćilim", "Koštana"],
        ),
        (
            "off",
            ["Taća", "kažeš", "đubre", "Ćilim", "Koštana"],
            ["Taca", "kazes", "djubre", "Cilim", "Kostana"],
        ),
        (
            "off",
            ["sada", "izgleda", "ja", "godine", "ali"],
            ["sada", "izgleda", "ja", "godine", "ali"],
        ),
        (
            "off",
            ["čćšđž", "ČĆŠĐŽ"],
            ["ccsdjz", "CCSDjZ"],
        ),
        (
            "off",
            ["äöüß", "ÄÖÜẞ"],
            ["aouss", "AOUSS"],
        ),
    ],
)
def test_accent_trim(accent, words, expected):
    assert utils.accent_trim(accent, words) == expected


@pytest.mark.parametrize(
    "language, topic, complexity, expected",
    [
        (
            "serbian",
            "none",
            "insane",
            "serbianinsane.json",
        ),
        (
            None,
            "numbers",
            None,
            "numbers.json",
        ),
        (
            "german",
            "none",
            "low",
            "germanlow.json",
        ),
        (
            "english",
            "food",
            None,
            "englishfood.json",
        ),
    ],
)
def test_select_file_path(language, topic, complexity, expected):
    if language is None:
        language = ""
    if topic is None:
        topic = ""
    if complexity is None:
        complexity = ""

    expected_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "words", expected
    )
    assert utils.select_file_path(language, topic, complexity) == expected_path
