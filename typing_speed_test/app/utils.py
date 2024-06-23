import json
import os
import random

def load_words(language, accent, mode, topic, complexity, word_count):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if language == "lorem":
        file_path = os.path.join(current_dir, "words", f"{language}.json")
    elif topic == "none":
        file_path = os.path.join(current_dir, "words", f"{language}{complexity}.json")
    elif topic == "numbers":
        file_path = os.path.join(current_dir, "words", f"{topic}.json")
    else:
        file_path = os.path.join(current_dir, "words", f"{language}{topic}.json")
   
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        words = data.get("words", [])
        random.shuffle(words)
        if topic == "quotes":
            words = words[:1]
        elif mode == "time":
            words = words[:word_count * 2]
        else:
            words = words[:word_count]

    if accent == "off":
        accent_map = {
            "ć": "c", "Ć": "C", "č": "c", "Č": "C",
            "š": "s", "Š": "S", "ž": "z", "Ž": "Z",
            "đ": "dj", "Đ": "Dj", "ä": "a", "Ä": "A",
            "ö": "o", "Ö": "O", "ü": "u", "Ü": "U",
            "ß": "ss", "ẞ": "SS"
        }
        words = [''.join(accent_map.get(char, char) for char in word) for word in words]
    
    return words
