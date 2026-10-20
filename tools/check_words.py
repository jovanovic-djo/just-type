"""Check the word lists in words/ for mistakes that break or spoil a test.

Run from the repository root:  python tools/check_words.py
Exits with status 1 if any problem is found.
"""

import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORDS_DIR = os.path.join(ROOT, 'words')
MIN_WORDS = 100
LEVELS = ['low', 'mid', 'high', 'insane']

problems = []


def problem(file, message):
    problems.append(f'{file}: {message}')
    # GitHub Actions shows this as an annotation on the file
    if os.environ.get('GITHUB_ACTIONS'):
        print(f'::error file=words/{file}::{message}')


def radio_values(html, name):
    return re.findall(rf'name="{name}" value="([^"]+)"', html)


def accent_maps(js):
    # accentMaps in js/test.js: the characters "remove accents" can replace, per language
    block = js[js.index('const accentMaps'):js.index('};', js.index('const accentMaps'))]
    maps = {}
    for language, body in re.findall(r'(\w+): \{(.*?)\}', block, re.S):
        maps[language] = set(re.findall(r'"(.)":', body))
    return maps


def load(file):
    with open(os.path.join(WORDS_DIR, file), encoding='utf-8') as f:
        data = json.load(f)
    words = data.get('words') if isinstance(data, dict) else None
    if not isinstance(words, list) or not all(isinstance(w, str) for w in words):
        raise ValueError('needs a "words" list of strings')
    return words


def main():
    html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    js = open(os.path.join(ROOT, 'js', 'test.js'), encoding='utf-8').read()
    maps = accent_maps(js)

    # every file the home page can lead to (see selectFilePath in js/test.js)
    languages = [l for l in radio_values(html, 'language') if l != 'lorem']
    topics = [t for t in radio_values(html, 'topic') if t not in ('none', 'numbers')]
    complexities = radio_values(html, 'complexity')
    expected = {'lorem.json', 'numbers.json'}
    expected |= {f'{l}{c}.json' for l in languages for c in complexities}
    expected |= {f'{l}{t}.json' for l in languages for t in topics}

    present = {f for f in os.listdir(WORDS_DIR) if f.endswith('.json')}
    for file in sorted(expected - present):
        problem(file, 'missing, but the home page can select it')

    lists = {}
    for file in sorted(present):
        try:
            words = load(file)
        except (ValueError, json.JSONDecodeError) as error:
            problem(file, f'invalid: {error}')
            continue
        lists[file[:-5]] = words

        name = file[:-5]
        is_quotes = name.endswith('quotes')
        language = next((l for l in maps if name.startswith(l)), None)

        seen = set()
        for word in words:
            if word in seen:
                problem(file, f'duplicate {word!r}')
            seen.add(word)
            if not word or word != word.strip():
                problem(file, f'empty or padded entry {word!r}')
            if unicodedata.normalize('NFC', word) != word:
                problem(file, f'{word!r} stores an accent as a separate mark, so it cannot be typed')

        if name == 'numbers':
            for word in words:
                if not word.isdigit():
                    problem(file, f'{word!r} is not a number')
            continue
        if is_quotes:
            continue

        if len(words) < MIN_WORDS:
            problem(file, f'only {len(words)} words, needs at least {MIN_WORDS}')
        for word in words:
            if word != word.lower():
                problem(file, f'{word!r} has capitals, word lists are lowercase')
            if ' ' in word:
                problem(file, f'{word!r} is two words')
            if language:
                nfc = unicodedata.normalize('NFC', word)  # a separated accent is reported above
                unmapped = {c for c in nfc if ord(c) > 127 and c not in maps[language]}
                if unmapped:
                    problem(file, f'{word!r} has {"".join(sorted(unmapped))}, which "remove accents" cannot replace')

    # a word belongs to one difficulty level per language
    for language in languages:
        for i, lower in enumerate(LEVELS):
            for higher in LEVELS[i + 1:]:
                a, b = lists.get(language + lower), lists.get(language + higher)
                if a and b:
                    for word in sorted(set(a) & set(b)):
                        problem(f'{language}{higher}.json', f'{word!r} is also in {language}{lower}.json')

    if problems:
        print(f'{len(problems)} problem(s) in word lists:')
        for p in problems:
            print('  ' + p)
        return 1
    print(f'{len(lists)} word lists OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
