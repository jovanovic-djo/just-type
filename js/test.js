
// ACCENTED CHARACTERS AND THEIR PLAIN REPLACEMENTS, PER LANGUAGE
const accentMaps = {
    serbian: {
        "ć": "c", "Ć": "C",
        "č": "c", "Č": "C",
        "š": "s", "Š": "S",
        "ž": "z", "Ž": "Z",
        "đ": "dj", "Đ": "Dj"
    },
    german: {
        "ä": "a", "Ä": "A",
        "ö": "o", "Ö": "O",
        "ü": "u", "Ü": "U",
        "ß": "ss", "ẞ": "SS"
    },
    french: {
        "à": "a", "À": "A",
        "â": "a", "Â": "A",
        "æ": "ae", "Æ": "AE",
        "ç": "c", "Ç": "C",
        "é": "e", "É": "E",
        "è": "e", "È": "E",
        "ê": "e", "Ê": "E",
        "ë": "e", "Ë": "E",
        "î": "i", "Î": "I",
        "ï": "i", "Ï": "I",
        "ô": "o", "Ô": "O",
        "œ": "oe", "Œ": "OE",
        "ù": "u", "Ù": "U",
        "û": "u", "Û": "U",
        "ü": "u", "Ü": "U",
        "ÿ": "y", "Ÿ": "Y"
    },
    spanish: {
        "á": "a", "Á": "A",
        "é": "e", "É": "E",
        "í": "i", "Í": "I",
        "ñ": "n", "Ñ": "N",
        "ó": "o", "Ó": "O",
        "ú": "u", "Ú": "U",
        "ü": "u", "Ü": "U"
    }
};


// TRIM THE ACCENT OFF THE CHARACTERS
function accentTrim(accent, words, language) {
    const accentMap = accentMaps[language];
    if (accent !== "off" || !accentMap) {
        return words;
    }

    return words.map(word =>
        word.split('').map(char => accentMap[char] || char).join('')
    );
}


// GET PARAMETER
function getQueryParam(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}


// GET CORRECT PATH BASED ON VARIABLES
function selectFilePath(language, topic, complexity) {
    if (language === "lorem") {
        return `words/${language}.json`;
    } else if (topic === "none") {
        return `words/${language}${complexity}.json`;
    } else if (topic === "numbers") {
        return `words/${topic}.json`;
    } else {
        return `words/${language}${topic}.json`;
    }
}


// SHUFFLE WORDS
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}


let words = [];


// DISPLAY WORDS IN ONE STRING
function displayWords(words) {
    const display = document.getElementById('word-display');
    display.textContent = words.join(' ');
    display.scrollTop = 0;
}


// PICK count WORDS, RESHUFFLING THE LIST WHENEVER IT RUNS OUT
function pickWords(list, count) {
    const picked = [];
    while (picked.length < count) {
        picked.push(...shuffleArray([...list]));
    }
    return picked.slice(0, count);
}


// FETCH WORDS FUNCTION
function fetchWords(language, accent, topic, complexity, wordCount) {
    const filePath = selectFilePath(language, topic, complexity);

    fetch(filePath)
        .then(response => {
            if (!response.ok) {
                throw new Error(`${response.status} ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            words = data.words || [];
            if (words.length === 0) {
                throw new Error('word list is empty');
            }
            words = pickWords(words, topic === "quotes" ? 1 : wordCount);
            words = accentTrim(accent, words, language);
            displayWords(words);
        })
        .catch(error => {
            words = [];
            console.error(`Error loading ${filePath}:`, error);
            document.getElementById('word-display').textContent =
                "Couldn't load the words. Check your connection and reload the page.";
        });
}


// MARK EACH CHARACTER AS CORRECT, INCORRECT OR NEXT, RETURN CORRECT COUNT
function renderProgress(display, target, typed) {
    const fragment = document.createDocumentFragment();
    let correctChars = 0;

    const addSpan = (className, char) => {
        const span = document.createElement('span');
        span.className = className;
        span.textContent = char;
        fragment.appendChild(span);
    };

    for (let i = 0; i < typed.length && i < target.length; i++) {
        if (typed[i] === target[i]) {
            addSpan('correct', target[i]);
            correctChars++;
        } else {
            addSpan('incorrect', target[i]);
        }
    }

    if (typed.length < target.length) {
        addSpan('next-char', target[typed.length]);
        fragment.appendChild(document.createTextNode(target.slice(typed.length + 1)));
    }

    display.replaceChildren(fragment);
    return correctChars;
}


// LENGTH OF TYPED TEXT THAT CAN'T BE DELETED: EVERYTHING UP TO AND INCLUDING
// THE LAST WORD THAT WAS TYPED CORRECTLY TOGETHER WITH ITS SPACE
function lockedLength(typed, target) {
    let locked = 0;
    let wordStart = 0;

    for (let i = 0; i < typed.length && i < target.length; i++) {
        if (target[i] === ' ') {
            if (typed.slice(wordStart, i + 1) === target.slice(wordStart, i + 1)) {
                locked = i + 1;
            }
            wordStart = i + 1;
        }
    }
    return locked;
}


// IN TIMED MODE ONLY A FEW LINES ARE SHOWN: SCROLL SO THE CURRENT LINE IS THE SECOND ONE
function scrollToCurrentLine(display) {
    const next = display.querySelector('.next-char');
    if (!next) {
        return;
    }
    const lineHeight = parseFloat(getComputedStyle(display).lineHeight);
    const line = Math.floor(next.offsetTop / lineHeight);
    display.scrollTop = Math.max(0, line - 1) * lineHeight;
}


// KEYS THAT WOULD MOVE THE CARET INSIDE THE TYPED TEXT
const caretKeys = ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End', 'PageUp', 'PageDown'];


// TEST HANDLER
document.addEventListener('DOMContentLoaded', () => {
    const language = getQueryParam('language');
    const accent = getQueryParam('accent');
    const topic = getQueryParam('topic');
    const complexity = getQueryParam('complexity');
    const timed = getQueryParam('mode') === 'time' && topic !== 'quotes';
    const seconds = parseInt(getQueryParam('time-value'), 10) || 30;
    const modeValue = parseInt(getQueryParam('mode-value'), 10);

    // IN TIMED MODE LOAD MORE WORDS THAN ANYONE CAN TYPE (4 WORDS PER SECOND = 240 WPM)
    fetchWords(language, accent, topic, complexity, timed ? seconds * 4 : modeValue);

    const typingInput = document.getElementById('typing-input');
    const typedWordsDiv = document.getElementById('word-display');
    const resultModal = document.getElementById('result-modal');
    const testTitle = document.getElementById('test-title');
    const instructions = document.getElementById('instruction-container');
    const timer = document.getElementById('timer');

    let startTime = null;
    let finished = false;
    let timerInterval = null;
    let correctChars = 0;
    let keystrokes = 0;
    let mistakes = 0;
    let previousValue = "";

    const setChromeOpacity = (opacity) => {
        testTitle.style.opacity = opacity;
        instructions.style.opacity = opacity;
    };

    const hideModal = () => {
        resultModal.style.display = 'none';
    };

    const showResults = (elapsed) => {
        finished = true;
        clearInterval(timerInterval);

        const minutes = elapsed / 60000;
        const cpm = Math.round(correctChars / minutes);
        const wpm = Math.round(correctChars / 5 / minutes);
        const accuracy = Math.round(((keystrokes - mistakes) / keystrokes) * 100);

        document.getElementById('cpm').innerText = `CPM: ${cpm}`;
        document.getElementById('wpm').innerText = `WPM: ${wpm}`;
        document.getElementById('accuracy').innerText = `Accuracy: ${accuracy}%`;

        resultModal.style.display = "block";
    };

    // COUNT DOWN FROM THE FIRST KEYSTROKE AND END THE TEST AT ZERO
    const startTimer = () => {
        timerInterval = setInterval(() => {
            const remaining = seconds - (new Date() - startTime) / 1000;
            timer.textContent = Math.max(0, Math.ceil(remaining));
            if (remaining <= 0) {
                showResults(seconds * 1000);
            }
        }, 100);
    };

    if (timed) {
        typedWordsDiv.classList.add('timed');
        timer.hidden = false;
        timer.textContent = seconds;
    }

    const restartTest = () => {
        if (words.length === 0) {
            return;
        }
        typingInput.value = "";
        displayWords(words);
        startTime = null;
        finished = false;
        clearInterval(timerInterval);
        timer.textContent = seconds;
        correctChars = 0;
        keystrokes = 0;
        mistakes = 0;
        previousValue = "";
        hideModal();
        setChromeOpacity(0.8);
        typingInput.focus();
    };

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            e.preventDefault();
            window.location.href = './index.html';
        } else if (e.key === 'Enter') {
            e.preventDefault();
            window.location.reload();
        } else if (e.key === 'Tab') {
            e.preventDefault();
            restartTest();
        } else if (caretKeys.includes(e.key)) {
            // KEEP THE CARET AT THE END, SO TEXT IS ONLY ADDED OR DELETED THERE
            e.preventDefault();
        }
        typingInput.focus();
    });

    typingInput.addEventListener('input', () => {
        if (finished || words.length === 0) {
            typingInput.value = previousValue;
            return;
        }

        if (startTime === null) {
            startTime = new Date();
            if (timed) {
                startTimer();
            }
        }

        testTitle.style.transition = "opacity 0.7s ease-in-out";
        instructions.style.transition = "opacity 0.7s ease-in-out";
        setChromeOpacity(0.1);

        let typed = typingInput.value;
        const target = words.join(' ');

        // DON'T LET DELETING GO BACK INTO A CORRECTLY TYPED WORD
        const lockedText = previousValue.slice(0, lockedLength(previousValue, target));
        if (!typed.startsWith(lockedText)) {
            typed = previousValue.startsWith(typed) ? lockedText : previousValue;
            typingInput.value = typed;
        }

        correctChars = renderProgress(typedWordsDiv, target, typed);
        if (timed) {
            scrollToCurrentLine(typedWordsDiv);
        }

        // COUNT EVERY NEW CHARACTER, SO MISTAKES FIXED WITH BACKSPACE STILL COUNT
        for (let i = previousValue.length; i < typed.length; i++) {
            keystrokes++;
            if (typed[i] !== target[i]) {
                mistakes++;
            }
        }
        previousValue = typed;

        if (typed.length === target.length) {
            showResults(new Date() - startTime);
        }
    });

    resultModal.addEventListener('click', (e) => {
        if (e.target === resultModal) {
            hideModal();
        }
    });

    document.addEventListener('click', (e) => {
        if (!resultModal.contains(e.target) && e.target !== typingInput) {
            typingInput.focus();
        }
    });

    typingInput.focus();
});


// HANDLE TEXT SIZE BASED ON COMPLEXITY
document.addEventListener('DOMContentLoaded', () => {
    const wordDisplay = document.getElementById('word-display');
    const complexity = getQueryParam('complexity');

    if (complexity === 'insane') {
        wordDisplay.style.fontSize = '32px';
    } else if (complexity === 'high') {
        wordDisplay.style.fontSize = '38px';
    }
});
