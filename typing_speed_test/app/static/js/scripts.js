
document.addEventListener('DOMContentLoaded', (event) => {
    const words = document.getElementById('words').innerText.trim();
    const typingInput = document.getElementById('typingInput');
    const typedWordsDiv = document.getElementById('typedWords');
    const timerDiv = document.getElementById('timer');
    const resultModal = document.getElementById('resultModal');
    const resultText = document.getElementById('resultText');
    const closeModal = document.querySelector('.close');
    let startTime = null;
    let timerInterval = null;

    document.addEventListener('keydown', () => {
        typingInput.focus();
    });

    typingInput.addEventListener('input', function() {
        if (startTime === null) {
            startTime = new Date();
            timerInterval = setInterval(() => {
                const elapsed = Math.floor((new Date() - startTime) / 1000);
                timerDiv.textContent = `Time: ${elapsed} seconds`;
            }, 1000);
        }

        const typed = typingInput.value;
        let html = '';
        for (let i = 0; i < words.length; i++) {
            if (i < typed.length) {
                if (words[i] === typed[i]) {
                    html += `<span class="correct">${words[i]}</span>`;
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

        if (typed === words) {
            clearInterval(timerInterval);
            const totalTime = (new Date() - startTime) / 1000; // in seconds
            const cpm = Math.round((typed.length / totalTime) * 60);
            const wpm = Math.round((typed.split(' ').length / totalTime) * 60);
            resultText.innerHTML = `Test completed in ${totalTime.toFixed(2)} seconds<br>CPM: ${cpm}<br>WPM: ${wpm}`;
            resultModal.style.display = "block";
        }
    });

    closeModal.onclick = function() {
        resultModal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == resultModal) {
            resultModal.style.display = "none";
        }
    }
}); 