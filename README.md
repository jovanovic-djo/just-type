#### Typing speed test, great for touch typing exercises, most important functionalities/features are included.

Try it at **https://jovanovic-djo.github.io/just-type/**

## Features: 
- Multiple languages (English, French, German, Serbian, Spanish, also lorem ipsum included)
- Accent trim (for smoother test)
- Different topics (numbers - if you are into accounting, animals, objects and food for language learners, and also quotes)
- Complexity levels for general, none topic words (easy, mid, hard and insane)
- Two modes: type a set number of words (5, 10, 15 or 30), or type as much as you can in a set time (15, 30, 60 or 120 seconds)
- Hotkeys for faster interaction with test (tab for test restart, enter for new test and esc for back to main menu)
- Restart, new test and home buttons on the results, for phones without those keys
- WPM, CPM and accuracy results, plus time taken and number of mistakes
- Mistakes count even when fixed with backspace, and a correctly typed word can't be deleted
- Correct and incorrect input indicators while typing
- Works on phones and with the keyboard alone
- Themes (of course, dark one and light one)

## Design
##### Minimalist design
![image](https://github.com/user-attachments/assets/7210c4fe-daf3-4d58-b749-e59eab242418)
##### Intuitive test
![image](https://github.com/user-attachments/assets/f19d82f7-c2e7-499e-80c8-bfd3ebdc3f7d)
##### Result display
![image](https://github.com/user-attachments/assets/a7e1f52d-ad42-455d-839b-0255b439fd44)

## Word lists
The words live in `words/`, one JSON file per language and difficulty or topic, e.g. `words/germanlow.json`:

```json
{"words": ["haus", "straße", "..."]}
```

Word lists are lowercase single words, at least 100 per list, and a word belongs to only one difficulty level. After editing, check them with:

```
python tools/check_words.py
```

The same check runs on GitHub for every push and pull request that changes the word lists.

## Tests
The site is tested in headless Chrome: every option combination on the home page, the keyboard, the back button, typing, word locking, pasting, the results and their buttons, and the timer. Run them with:

```
pip install websocket-client
python tests/run.py
```

They also run on GitHub for every push and pull request.
