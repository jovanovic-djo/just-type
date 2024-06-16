
document.addEventListener('DOMContentLoaded', (event) => {
    const words = document.getElementById('words').innerText.trim();
    const typingInput = document.getElementById('typingInput');
    const typedWordsDiv = document.getElementById('typedWords');
    const resultModal = document.getElementById('resultModal');
    const resultText = document.getElementById('resultText');
    const restartTestButton = document.getElementById('restartTestButton');
    const newTestButton = document.getElementById('newTestButton');
    const homeButton = document.getElementById('homeButton');
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
        typingInput.value = '';
        typedWordsDiv.innerHTML = '';
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

        if (typed.length >= words.length) {
            clearInterval(timerInterval);
            const totalTime = (new Date() - startTime) / 1000;
            const cpm = Math.round((typed.length / totalTime) * 60);
            const wpm = Math.round((typed.split(' ').length / totalTime) * 60);
            const accuracy = Math.round((correctChars / typed.length) * 100);
            resultText.innerHTML = `
                CPM: ${cpm}<br>
                WPM: ${wpm}<br>
                Accuracy: ${accuracy}%
            `;
            resultModal.style.display = "block";
        }
    });

    restartTestButton.onclick = restartTest;
    newTestButton.onclick = newTest;
    

    homeButton.onclick = function() {
        window.location.href = '/';
    };

    closeModal.onclick = function() {
        resultModal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == resultModal) {
            resultModal.style.display = "none";
        }
    }

    typingInput.focus();
});


document.addEventListener('DOMContentLoaded', function () {
    const languageChoice = document.getElementById('language-choice');
    const topicChoice = document.getElementById('topic-choice');
    const complexityChoice = document.getElementById('complexity-choice');
    const wordChoice = document.getElementById('word-choice');
    const accentRadios = document.querySelectorAll('input[name="accent"]');
    const topicRadios = topicChoice.querySelectorAll('input[type="radio"]');
    const complexityRadios = complexityChoice.querySelectorAll('input[type="radio"]');
    const languageRadios = languageChoice.querySelectorAll('input[type="radio"]');

    function toggleRadios(radios, disabled) {
        radios.forEach(radio => {
            radio.disabled = disabled;
            const label = document.querySelector(`label[for="${radio.id}"]`);
            if (label) {
                if (disabled) {
                    label.classList.add('disabled-section');
                } else {
                    label.classList.remove('disabled-section');
                }
            }
        });
    }

    function handleRadioChange() {
        const isLoremChecked = document.getElementById('lorem').checked;
        const isNumbersChecked = document.getElementById('numbers').checked;
        const isNoneChecked = document.getElementById('none').checked;

        toggleRadios(accentRadios, isLoremChecked);
        toggleRadios(topicRadios, isLoremChecked);
        toggleRadios(complexityRadios, isLoremChecked);

        toggleRadios(complexityRadios, isNumbersChecked);
        toggleRadios(accentRadios, isNumbersChecked);
        toggleRadios(languageRadios, isNumbersChecked);

        toggleRadios(complexityRadios, !isNoneChecked);
    }

    languageChoice.addEventListener('change', handleRadioChange);
    topicChoice.addEventListener('change', handleRadioChange);

    // Initialize the state on page load
    handleRadioChange();
});
