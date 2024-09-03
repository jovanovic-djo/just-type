// TRIM THE ACCENT OFF THE CHARACTERS
function accentTrim(accent, words, language) {
    if (accent === "off") {
        let accentMap = {};

        switch (language) {
            case "serbian":
                accentMap = {
                    "ć": "c",
                    "Ć": "C",
                    "č": "c",
                    "Č": "C",
                    "š": "s",
                    "Š": "S",
                    "ž": "z",
                    "Ž": "Z",
                    "đ": "dj",
                    "Đ": "Dj"
                };
                break;
            case "german":
                accentMap = {
                    "ä": "a",
                    "Ä": "A",
                    "ö": "o",
                    "Ö": "O",
                    "ü": "u",
                    "Ü": "U",
                    "ß": "ss",
                    "ẞ": "SS"
                };
                break;
            case "french":
                accentMap = {
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
                    "Ÿ": "Y"
                };
                break;
            case "spanish":
                accentMap = {
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
                    "Ü": "U"
                };
                break;
            default:
                break;
        }

        words = words.map(word => 
            word.split('').map(char => accentMap[char] || char).join('')
        );
    }

    return words;
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


// DISPLAY WORDS IN ONE STRING
function displayWords(words) {
    const wordDisplay = document.getElementById('word-display');
    wordDisplay.textContent = words.join(' ');
}


// ***************************************************************************** TEST TEST **********************************************

document.addEventListener('DOMContentLoaded', function() {
    const language = getQueryParam('language');
    const accent = getQueryParam('accent');
    const topic = getQueryParam('topic');
    const complexity = getQueryParam('complexity');
    const modeValue = parseInt(getQueryParam('mode-value'), 10);

    const filePath = selectFilePath(language, topic, complexity);

    fetch(filePath)
        .then(response => response.json())
        .then(data => {
            let words = data.words || [];
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
});


// **************************************************************************************************************************


// HANDLE SWITCHING RADIO BUTTONS
document.addEventListener("DOMContentLoaded", () => {

    const languageChoice = document.getElementById('language-choice');
    const topicChoice = document.getElementById('topic-choice');
    const complexityChoice = document.getElementById('complexity-choice');
    const modeValueChoice = document.getElementById('mode-value-choice');
    const accentChoice = document.getElementById('accent-choice');

    const accentRadios = accentChoice.querySelectorAll('input[type="radio"]');
    const topicRadios = topicChoice.querySelectorAll('input[type="radio"]');
    const complexityRadios = complexityChoice.querySelectorAll('input[type="radio"]');
    const modeValueRadios = modeValueChoice.querySelectorAll('input[type="radio"]');
    const languageRadios = languageChoice.querySelectorAll('input[type="radio"]');

    // DISABLE RADIO BUTTON FUNCTION
    function toggleRadios(radioGroup, shouldDisable) {
        radioGroup.forEach(radio => {
            radio.disabled = shouldDisable;
        });
    }
    
    // ENABLE RADIO BUTTON FUNCTION
    function enableRadios(radioGroup, shouldEnable) {
        radioGroup.forEach(radio => {
            radio.disabled = !shouldEnable;
        });
    }

    // HANDLE RADIO BUTTON CASES
    function handleRadioChange() {
        const isLoremChecked = document.getElementById('language-lorem').checked;
        const isEnglishChecked = document.getElementById('language-english').checked;
        const isSerbianChecked = document.getElementById('language-serbian').checked;
        const isGermanChecked = document.getElementById('language-german').checked;
        const isSpanishChecked = document.getElementById('language-spanish').checked;
        const isFrenchChecked = document.getElementById('language-french').checked;

        const isNumbersChecked = document.getElementById('topic-numbers').checked;
        const isAnimalsChecked = document.getElementById('topic-animals').checked;
        const isFoodChecked = document.getElementById('topic-food').checked;
        const isObjectsChecked = document.getElementById('topic-objects').checked;
        const isQuotesChecked = document.getElementById('topic-quotes').checked;

        toggleRadios(accentRadios, isEnglishChecked || isLoremChecked || isNumbersChecked);

        toggleRadios(complexityRadios, isLoremChecked || isNumbersChecked || isAnimalsChecked || isFoodChecked ||isObjectsChecked || isQuotesChecked);

        toggleRadios(topicRadios, isLoremChecked);

        toggleRadios(languageRadios, isNumbersChecked);

        enableRadios(modeValueRadios, isEnglishChecked || isSerbianChecked || isGermanChecked || isSpanishChecked || isFrenchChecked);

        if (isLoremChecked) {
            enableRadios(modeValueRadios, true);
        } else {
            toggleRadios(modeValueRadios, isQuotesChecked);
        }
    }

    languageChoice.addEventListener('change', handleRadioChange);
    topicChoice.addEventListener('change', handleRadioChange);
    complexityChoice.addEventListener('change', handleRadioChange);
    modeValueChoice.addEventListener('change', handleRadioChange);
    accentChoice.addEventListener('change', handleRadioChange);
    
    handleRadioChange();
});



// TEST HANDLER

document.addEventListener('DOMContentLoaded', () => {
    const words = document.getElementById('word-display').innerText.trim();
    const typingInput = document.getElementById('typing-input');
    const typedWordsDiv = document.getElementById('word-display');
    const resultModal = document.getElementById('result-modal');
    const closeModal = document.querySelector('.close');
    

    let startTime = null;
    let timerInterval = null;

    const redirectHome = () => {
        window.location.href = '/';
    };

    const newTest = () => {
        window.location.reload();
    };

    const restartTest = () => {
        typingInput.value = "";
        typedWordsDiv.innerHTML = words;
        startTime = null;
        clearInterval(timerInterval);
        resultModal.style.display = 'none';
        typingInput.focus();
    };

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            e.preventDefault();
            redirectHome();
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === '`' || e.key === '~') {
            e.preventDefault();
            newTest();
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            e.preventDefault();
            restartTest();
        }
    });

    typingInput.addEventListener('input', function() {
        if (startTime === null) {
            startTime = new Date();
            timerInterval = setInterval(() => {
                const elapsed = Math.floor((new Date() - startTime) / 1000);
            }, 1000);
        }

        document.getElementById("test-title").style.transition = "opacity 0.7s ease-in-out";
        document.getElementById("instruction-container").style.transition = "opacity 0.7s ease-in-out";
        document.getElementById("test-title").style.opacity = 0.1;
        document.getElementById("instruction-container").style.opacity = 0.1;

        const typed = typingInput.value;
        let correctChars = 0;
        let html = '';

        for (let i = 0; i < words.length; i++) {
            if (i < typed.length) {
                if (words[i] === typed[i]) {
                    html += `<span class="correct">${words[i]}</span>`;
                    correctChars++;
                } else {
                    html += `<span class="incorrect">${words[i]}</span>`;
                }
            } else if (i === typed.length) {
                html += `<span class="next-char">${words[i]}</span>`;
            } else {
                html += words[i];
            }
        }

        typedWordsDiv.innerHTML = html;

        if (typed.length == words.length) {
            clearInterval(timerInterval);

            const totalTime = (new Date() - startTime) / 1000;
            const cpm = Math.round((typed.length / totalTime) * 60);
            const wpm = Math.round((typed.split(' ').length / totalTime) * 60);
            const accuracy = Math.round((correctChars / typed.length) * 100);

            document.getElementById('cpm').innerText = `CPM: ${cpm}`;
            document.getElementById('wpm').innerText = `WPM: ${wpm}`;
            document.getElementById('accuracy').innerText = `Accuracy: ${accuracy}%`;
            
            resultModal.style.display = "block";
        }
    });


    closeModal.onclick = function() {
        resultModal.style.display = "none";
    };

    window.onclick = function(event) {
        if (event.target === resultModal) {
            resultModal.style.display = "none";
        }
    };

    const focusInput = () => {
        typingInput.focus();
    };

    document.addEventListener('click', (e) => {
        if (!resultModal.contains(e.target) && e.target !== typingInput) {
            focusInput();
        }
    });

    document.addEventListener('keydown', () => {
        focusInput();
    });

    focusInput();

});



// THEME SWIRCH

document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');

    if (localStorage.getItem('theme') === 'dark') {
        document.documentElement.classList.add('theme-dark');
        themeToggle.checked = true;
    }

    themeToggle.addEventListener('change', () => {
        if (themeToggle.checked) {
            document.documentElement.classList.add('theme-dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.classList.remove('theme-dark');
            localStorage.setItem('theme', 'light');
        }
    });
});



// HANDLE TEXT SIZE BASED ON COMPLEXITY

document.addEventListener('DOMContentLoaded', function() {
    const complexityChoice = document.getElementById('complexity-choice');

    if (complexityChoice) {
        const radios = complexityChoice.querySelectorAll('input[type="radio"]');
        
        radios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (radio.checked) {
                    localStorage.setItem('complexity', radio.value);
                }
            });
        });
    }

    const wordDisplay = document.getElementById('word-display');
    
    if (wordDisplay) {
        const complexity = localStorage.getItem('complexity');
        
        if (complexity === 'insane') {
            wordDisplay.style.fontSize = '32px';
        } else if (complexity === 'high'){
            wordDisplay.style.fontSize = '38px';
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                localStorage.clear();
            }
        });

    } 
});
