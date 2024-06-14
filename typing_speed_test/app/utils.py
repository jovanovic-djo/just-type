import json
import os


def load_words(language, accent):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "words", f"{language}.json")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        words = data.get("words", [])
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
