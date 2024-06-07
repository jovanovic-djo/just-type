import json
import os

def load_words(language):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'words', f'{language}.json')
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        words = data.get('words', [])
    
    return words