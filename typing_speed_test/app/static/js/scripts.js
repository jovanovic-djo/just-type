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

    function toggleRadios(radioGroup, shouldDisable) {
        radioGroup.forEach(radio => {
            radio.disabled = shouldDisable;
        });
    }
    
    function enableRadios(radioGroup, shouldEnable) {
        radioGroup.forEach(radio => {
            radio.disabled = !shouldEnable;
        });
    }

    function handleRadioChange() {
        const isLoremChecked = document.getElementById('language-lorem').checked;
        const isEnglishChecked = document.getElementById('language-english').checked;
        const isSerbianChecked = document.getElementById('language-serbian').checked;
        const isGermanChecked = document.getElementById('language-german').checked;  

        const isNumbersChecked = document.getElementById('topic-numbers').checked;
        const isAnimalsChecked = document.getElementById('topic-animals').checked;
        const isFoodChecked = document.getElementById('topic-food').checked;
        const isObjectsChecked = document.getElementById('topic-objects').checked;
        const isQuotesChecked = document.getElementById('topic-quotes').checked;

        toggleRadios(accentRadios, isEnglishChecked || isLoremChecked || isNumbersChecked);

        toggleRadios(complexityRadios, isLoremChecked || isNumbersChecked || isAnimalsChecked || isFoodChecked ||isObjectsChecked || isQuotesChecked);

        toggleRadios(topicRadios, isLoremChecked)

        toggleRadios(languageRadios, isNumbersChecked)

        toggleRadios(modeValueRadios, isQuotesChecked)

        enableRadios(modeValueRadios, isLoremChecked || isEnglishChecked || isSerbianChecked || isGermanChecked)

    }

    languageChoice.addEventListener('change', handleRadioChange);
    topicChoice.addEventListener('change', handleRadioChange);
    complexityChoice.addEventListener('change', handleRadioChange);
    modeValueChoice.addEventListener('change', handleRadioChange);
    accentChoice.addEventListener('change', handleRadioChange);
    
    handleRadioChange();
});

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
