import json
import os
import random


def select_file_path(language, topic, complexity):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    if language == "lorem":
        file_path = os.path.join(current_dir, "words", f"{language}.json")
    elif topic == "none":
        file_path = os.path.join(current_dir, "words", f"{language}{complexity}.json")
    elif topic == "numbers":
        file_path = os.path.join(current_dir, "words", f"{topic}.json")
    else:
        file_path = os.path.join(current_dir, "words", f"{language}{topic}.json")

    return file_path


def load_words(language, accent, topic, complexity, mode_value):
    file_path = select_file_path(language, topic, complexity)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        words = data.get("words", [])
        random.shuffle(words)
        if topic == "quotes":
            words = words[:1]
        else:
            words = words[: int(mode_value)]

    words = accent_trim(accent, words, language)

    return words


def accent_trim(accent, words, language):
    if accent == "off":
        if language == "serbian":
            accent_map = {
                "ć": "c",
                "Ć": "C",
                "č": "c",
                "Č": "C",
                "š": "s",
                "Š": "S",
                "ž": "z",
                "Ž": "Z",
                "đ": "dj",
                "Đ": "Dj",
            }
        elif language == "german":
            accent_map = {
                "ä": "a",
                "Ä": "A",
                "ö": "o",
                "Ö": "O",
                "ü": "u",
                "Ü": "U",
                "ß": "ss",
                "ẞ": "SS",
            }
        elif language == "french":
            accent_map = {
                "à": "a",
                "À": "A",
                "â": "a",
                "Â": "A",
                "æ": "ae",
                "Æ": "AE",
                "ç": "c",
                "Ç": "C",
                "é": "e",
                "É": "E",
                "è": "e",
                "È": "E",
                "ê": "e",
                "Ê": "E",
                "ë": "e",
                "Ë": "E",
                "î": "i",
                "Î": "I",
                "ï": "i",
                "Ï": "I",
                "ô": "o",
                "Ô": "O",
                "œ": "oe",
                "Œ": "OE",
                "ù": "u",
                "Ù": "U",
                "û": "u",
                "Û": "U",
                "ü": "u",
                "Ü": "U",
                "ÿ": "y",
                "Ÿ": "Y",
            }
        elif language == "spanish":
            accent_map = {
                "á": "a",
                "Á": "A",
                "é": "e",
                "É": "E",
                "í": "i",
                "Í": "I",
                "ñ": "n",
                "Ñ": "N",
                "ó": "o",
                "Ó": "O",
                "ú": "u",
                "Ú": "U",
                "ü": "u",
                "Ü": "U",
            }
        words = ["".join(accent_map.get(char, char) for char in word) for word in words]

    return words
