
// WHEN EACH OPTION GROUP IS DISABLED, BASED ON THE CURRENT SELECTION
const disabledWhen = {
    'language-choice': ({ topic }) => topic === 'numbers',
    'topic-choice': ({ language }) => language === 'lorem',
    'accent-choice': ({ language, topic }) => language === 'english' || language === 'lorem' || topic === 'numbers',
    'complexity-choice': ({ language, topic }) => language === 'lorem' || topic !== 'none',
    'mode-value-choice': ({ language, topic }) => language !== 'lorem' && topic === 'quotes',
};


// HANDLE SWITCHING RADIO BUTTONS
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');

    function handleRadioChange() {
        const selection = {
            language: form.elements['language'].value,
            topic: form.elements['topic'].value,
        };

        for (const [groupId, isDisabled] of Object.entries(disabledWhen)) {
            const disabled = isDisabled(selection);
            document.querySelectorAll(`#${groupId} input[type="radio"]`).forEach(radio => {
                radio.disabled = disabled;
            });
        }
    }

    form.addEventListener('change', handleRadioChange);
    handleRadioChange();
});


// REMEMBER COMPLEXITY FOR TEXT SIZE ON THE TEST PAGE
document.addEventListener('DOMContentLoaded', () => {
    const radios = document.querySelectorAll('#complexity-choice input[type="radio"]');

    radios.forEach(radio => {
        radio.addEventListener('change', () => {
            if (radio.checked) {
                localStorage.setItem('complexity', radio.value);
            }
        });
    });
});
