
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
    document.getElementById('word-display').textContent = words.join(' ');
}


// FETCH WORDS FUNCTION
function fetchWords(language, accent, topic, complexity, modeValue) {
    const filePath = selectFilePath(language, topic, complexity);

    fetch(filePath)
        .then(response => response.json())
        .then(data => {
            words = data.words || [];
            words = shuffleArray(words);
            if (topic === "quotes") {
                words = words.slice(0, 1);
            } else {
                words = words.slice(0, modeValue);
            }
            words = accentTrim(accent, words, language);
            displayWords(words);
        })
        .catch(error => console.error('Error fetching JSON:', error));
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


// TEST HANDLER
document.addEventListener('DOMContentLoaded', () => {
    const language = getQueryParam('language');
    const accent = getQueryParam('accent');
    const topic = getQueryParam('topic');
    const complexity = getQueryParam('complexity');
    const modeValue = parseInt(getQueryParam('mode-value'), 10);

    fetchWords(language, accent, topic, complexity, modeValue);

    const typingInput = document.getElementById('typing-input');
    const typedWordsDiv = document.getElementById('word-display');
    const resultModal = document.getElementById('result-modal');
    const testTitle = document.getElementById('test-title');
    const instructions = document.getElementById('instruction-container');

    let startTime = null;
    let isModalVisible = false;

    const setChromeOpacity = (opacity) => {
        testTitle.style.opacity = opacity;
        instructions.style.opacity = opacity;
    };

    const hideModal = () => {
        resultModal.style.display = 'none';
        isModalVisible = false;
    };

    const restartTest = () => {
        typingInput.value = "";
        displayWords(words);
        startTime = null;
        hideModal();
        setChromeOpacity(0.8);
        typingInput.focus();
    };

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            e.preventDefault();
            localStorage.removeItem('complexity');
            window.location.href = './index.html';
        } else if (e.key === '`' || e.key === '~') {
            e.preventDefault();
            window.location.reload();
        } else if (e.key === 'Tab') {
            e.preventDefault();
            restartTest();
        }
        typingInput.focus();
    });

    typingInput.addEventListener('input', () => {
        if (isModalVisible) {
            return;
        }

        if (startTime === null) {
            startTime = new Date();
        }

        testTitle.style.transition = "opacity 0.7s ease-in-out";
        instructions.style.transition = "opacity 0.7s ease-in-out";
        setChromeOpacity(0.1);

        const typed = typingInput.value;
        const target = words.join(' ');
        const correctChars = renderProgress(typedWordsDiv, target, typed);

        if (typed.length === target.length) {
            const totalTime = (new Date() - startTime) / 1000;
            const cpm = Math.round((typed.length / totalTime) * 60);
            const wpm = Math.round((typed.split(' ').length / totalTime) * 60);
            const accuracy = Math.round((correctChars / typed.length) * 100);

            document.getElementById('cpm').innerText = `CPM: ${cpm}`;
            document.getElementById('wpm').innerText = `WPM: ${wpm}`;
            document.getElementById('accuracy').innerText = `Accuracy: ${accuracy}%`;

            resultModal.style.display = "block";
            isModalVisible = true;
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
    const complexity = localStorage.getItem('complexity');

    if (complexity === 'insane') {
        wordDisplay.style.fontSize = '32px';
    } else if (complexity === 'high') {
        wordDisplay.style.fontSize = '38px';
    }
});
