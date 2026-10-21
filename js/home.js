
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

    // COMING BACK TO THIS PAGE, PUT BACK THE OPTIONS THAT WERE CHOSEN. THE BROWSER'S OWN
    // RESTORE (TURNED OFF WITH autocomplete="off") RAN AFTER THIS SCRIPT AND SKIPPED
    // DISABLED OPTIONS, SO IT LEFT THE PAGE HALF RESTORED
    const saved = history.state && history.state.selection;
    if (saved) {
        for (const [name, value] of Object.entries(saved)) {
            if (form.elements[name]) {
                form.elements[name].value = value;
            }
        }
    }

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

        // REMEMBER EVERY CHOICE, ALSO THE DISABLED ONES, IN THIS PAGE'S HISTORY ENTRY
        // (BROWSERS LIMIT HOW OFTEN THIS CAN BE CALLED, SAFARI THROWS AN ERROR PAST THE LIMIT)
        const chosen = [...form.querySelectorAll('input[type="radio"]:checked')];
        try {
            history.replaceState({ selection: Object.fromEntries(chosen.map(radio => [radio.name, radio.value])) }, '');
        } catch (error) {
            console.warn("Couldn't remember the options:", error);
        }
    }

    form.addEventListener('change', handleRadioChange);
    handleRadioChange();
});

