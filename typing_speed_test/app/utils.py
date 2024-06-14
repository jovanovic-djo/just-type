import json
import os
import random


def load_words(language, accent, topic, complexity, word_count):
    current_dir = os.path.dirname(os.path.abspath(__file__))

        
    if topic == "none":
        file_path = os.path.join(current_dir, "words", f"{language}{complexity}.json")
    elif topic == "numbers" or topic == "quotes":
        file_path = os.path.join(current_dir, "words", f"{topic}.json")
    else:
        file_path = os.path.join(current_dir, "words", f"{language}{topic}.json")
 

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        words = data.get("words", [])
        if topic == "quotes":
            random.shuffle(words)
            words = words[:1]
        else:
            random.shuffle(words)
            words = words[:word_count]
        if accent == "off":
            for word in words:
                word.replace(
                    "ć", "c"
                ).replace(
                    "Ć", "C"
                ).replace(
                    "č", "c"
                ).replace(
                    "Č", "C"
                ).replace(
                    "š", "s"
                ).replace(
                    "Š", "S"
                ).replace(
                    "ž", "z"
                ).replace(
                    "Ž", "Z"
                ).replace(
                    "đ", "dj"
                ).replace(
                    "Đ", "Dj"
                ).replace(
                    "ä", "a"
                ).replace(
                    "Ä", "A"
                ).replace(
                    "ö", "o"
                ).replace(
                    "Ö", "O"
                ).replace(
                    "ü", "u"
                ).replace(
                    "Ü", "U"
                ).replace(
                    "ß", "ss"
                ).replace(
                    "ẞ", "SS"
                )

    return words
