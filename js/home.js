
// A QUOTE IS ALWAYS ONE WHOLE QUOTE, SO WORD COUNT AND TIME DON'T APPLY
const quoteTest = ({ language, topic }) => language !== 'lorem' && topic === 'quotes';


// WHEN EACH OPTION GROUP IS DISABLED, BASED ON THE CURRENT SELECTION
const disabledWhen = {
    'language-choice': ({ topic }) => topic === 'numbers',
    'topic-choice': ({ language }) => language === 'lorem',
    'accent-choice': ({ language, topic }) => language === 'english' || language === 'lorem' || topic === 'numbers',
    'complexity-choice': ({ language, topic }) => language === 'lorem' || topic !== 'none',
    'mode-choice': quoteTest,
    'mode-value-choice': (selection) => quoteTest(selection) || selection.mode === 'time',
    'time-value-choice': (selection) => quoteTest(selection) || selection.mode !== 'time',
};


// ONLY THE VALUES FOR THE CHOSEN MODE (WORDS OR TIME) ARE SHOWN
const hiddenWhen = {
    'mode-value-choice': ({ mode }) => mode === 'time',
    'time-value-choice': ({ mode }) => mode !== 'time',
};


// HANDLE SWITCHING RADIO BUTTONS
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');

    function handleRadioChange() {
        const selection = {
            language: form.elements['language'].value,
            topic: form.elements['topic'].value,
            mode: form.elements['mode'].value,
        };

        for (const [groupId, isDisabled] of Object.entries(disabledWhen)) {
            const disabled = isDisabled(selection);
            document.querySelectorAll(`#${groupId} input[type="radio"]`).forEach(radio => {
                radio.disabled = disabled;
            });
        }

        for (const [groupId, isHidden] of Object.entries(hiddenWhen)) {
            document.getElementById(groupId).hidden = isHidden(selection);
        }
    }

    form.addEventListener('change', handleRadioChange);
    handleRadioChange();
});

