"""Home page with the keyboard, and coming back to it with Back, reload and Esc."""

from browser import Chrome

# EMPTY IF THE DISABLED AND HIDDEN GROUPS MATCH THE SELECTION, OTHERWISE THE GROUPS THAT DON'T
CONSISTENT = """(() => {
    const form = document.querySelector('form'), s = n => form.elements[n].value;
    const language = s('language'), topic = s('topic'), mode = s('mode'), quote = language !== 'lorem' && topic === 'quotes';
    const expected = {
        'language-choice': topic === 'numbers',
        'topic-choice': language === 'lorem',
        'accent-choice': ['english', 'lorem'].includes(language) || topic === 'numbers',
        'complexity-choice': language === 'lorem' || topic !== 'none',
        'mode-choice': quote,
        'mode-value-choice': quote || mode === 'time',
        'time-value-choice': quote || mode !== 'time',
    };
    const wrong = Object.entries(expected)
        .filter(([group, disabled]) => [...document.querySelectorAll(`#${group} input`)].some(r => r.disabled !== disabled))
        .map(([group]) => group + ' disabled');
    if (document.getElementById('mode-value-choice').hidden !== (mode === 'time')) wrong.push('word counts shown');
    if (document.getElementById('time-value-choice').hidden !== (mode !== 'time')) wrong.push('seconds shown');
    return wrong.join(', ');
})()"""

# THE CHOSEN OPTIONS THAT ARE ON SCREEN
CHOSEN = """[...document.querySelectorAll('form input:checked')].filter(r => !r.closest('[hidden]')).map(r => r.id).join(' ')"""
FOCUSED = """(e => e.id || (e.tagName === 'A' ? e.querySelector('img').alt : e.tagName))(document.activeElement)"""
DEFAULTS = 'language-english accent-on topic-none complexity-low mode-words mode-value-5'


def chosen(chrome, name):
    return chrome.js(f"document.querySelector('[name=\"{name}\"]:checked').value")


def keyboard(report, base):
    report.section('home page with the keyboard')
    with Chrome() as chrome:
        chrome.goto(base + '/index.html')
        order = []
        for _ in range(10):
            chrome.key('Tab')
            order.append(chrome.js(FOCUSED))
        report.check('tab goes through every enabled group once', order,
                     ['GitHub', 'YouTube', 'theme-toggle', 'language-english', 'topic-none',
                      'complexity-low', 'mode-words', 'mode-value-5', 'start-test', 'BODY'])
        chrome.key('Tab', shift=True)
        report.check('shift+tab goes back', chrome.js(FOCUSED), 'start-test')

        chrome.js("document.getElementById('language-english').focus()")
        seen = []
        for _ in range(6):
            chrome.key('ArrowRight')
            seen.append(chosen(chrome, 'language'))
        report.check('arrow keys pick the next language and wrap around', seen,
                     ['german', 'serbian', 'french', 'spanish', 'lorem', 'english'])
        chrome.key('ArrowLeft')
        report.check('arrow left wraps to the last language', chosen(chrome, 'language'), 'lorem')
        report.check('lorem: groups disabled to match', chrome.js(CONSISTENT), '')
        order = []
        for _ in range(3):
            chrome.key('Tab')
            order.append(chrome.js(FOCUSED))
        report.check('lorem: tab skips the disabled accents, topic and difficulty', order,
                     ['mode-words', 'mode-value-5', 'start-test'])

        chrome.js("document.getElementById('language-lorem').focus()")
        chrome.key('ArrowRight')
        chrome.js("document.getElementById('topic-none').focus()")
        chrome.key('ArrowRight')
        report.check('arrow to numbers', chosen(chrome, 'topic'), 'numbers')
        chrome.key('Tab', shift=True)
        report.check('numbers: shift+tab skips the disabled languages', chrome.js(FOCUSED), 'theme-toggle')
        chrome.js("document.getElementById('topic-numbers').focus()")
        chrome.key('ArrowLeft')
        report.check('arrow back to no topic', chosen(chrome, 'topic'), 'none')

        chrome.js("document.getElementById('mode-words').focus()")
        chrome.key('ArrowRight')
        report.check('arrow to time mode', chosen(chrome, 'mode'), 'time')
        chrome.key('Tab')
        report.check('tab goes to the chosen seconds', chrome.js(FOCUSED), 'time-value-30')
        for _ in range(3):
            chrome.key('ArrowRight')
        report.check('seconds wrap around', chosen(chrome, 'time-value'), '15')
        report.check('groups disabled to match', chrome.js(CONSISTENT), '')
        chrome.mark()
        chrome.key('Enter')
        chrome.loaded('type.html')
        report.check('enter starts the test', chrome.js('location.search'),
                     '?language=english&topic=none&complexity=low&mode=time&time-value=15')


def start(chrome):
    chrome.mark()
    chrome.click('#start-test')
    chrome.loaded('type.html')
    return chrome.js('location.search')


def coming_back(report, base, cache):
    report.section(f'coming back to the home page ({"with" if cache else "without"} the back/forward cache)')
    with Chrome(*([] if cache else ['--disable-features=BackForwardCache'])) as chrome:
        chrome.goto(base + '/index.html')
        for option in ('language-german', 'complexity-high', 'mode-time', 'time-value-60'):
            chrome.click(f'label[for={option}]')
        report.check('start sends the options', start(chrome),
                     '?language=german&accent=on&topic=none&complexity=high&mode=time&time-value=60')
        chrome.back('index.html')
        report.check('back: options kept', chrome.js(CHOSEN),
                     'language-german accent-on topic-none complexity-high mode-time time-value-60')
        report.check('back: groups disabled to match', chrome.js(CONSISTENT), '')

        chrome.click('label[for=topic-quotes]')
        report.check('quotes after coming back', start(chrome), '?language=german&accent=on&topic=quotes')
        chrome.back('index.html')
        report.check('back from quotes: groups disabled to match', chrome.js(CONSISTENT), '')
        chrome.mark()
        chrome.js('history.forward()')
        chrome.loaded('type.html')
        report.check('forward: the quote test again', chrome.js('location.search'), '?language=german&accent=on&topic=quotes')

        chrome.mark()
        chrome.key('Escape')
        chrome.loaded('index.html')
        report.check('esc: fresh home page with the defaults', chrome.js(CHOSEN), DEFAULTS)
        report.check('esc: groups disabled to match', chrome.js(CONSISTENT), '')

        # TWO HOME PAGES IN HISTORY, EACH COMES BACK WITH ITS OWN OPTIONS
        for option in ('language-lorem', 'mode-time', 'time-value-120'):
            chrome.click(f'label[for={option}]')
        start(chrome)
        chrome.mark()
        chrome.key('Escape')
        chrome.loaded('index.html')
        chrome.click('label[for=topic-numbers]')
        report.check('numbers sends no language', start(chrome), '?topic=numbers&mode=words&mode-value=5')
        chrome.back('index.html')
        report.check('back to the numbers page', chrome.js(CHOSEN),
                     'language-english accent-on topic-numbers complexity-low mode-words mode-value-5')
        report.check('numbers page: groups disabled to match', chrome.js(CONSISTENT), '')
        chrome.back('type.html')
        chrome.back('index.html')
        report.check('back to the lorem page', chrome.js(CHOSEN),
                     'language-lorem accent-on topic-none complexity-low mode-time time-value-120')
        report.check('lorem page: groups disabled to match', chrome.js(CONSISTENT), '')
        report.check('lorem page starts the same test', start(chrome), '?language=lorem&mode=time&time-value=120')

        # RELOAD KEEPS THE OPTIONS
        chrome.back('index.html')
        chrome.click('label[for=language-spanish]')
        chrome.click('label[for=accent-off]')
        chrome.mark()
        chrome.cdp('Page.reload')
        chrome.loaded('index.html')
        report.check('reload keeps the options', chrome.js(CHOSEN),
                     'language-spanish accent-off topic-none complexity-low mode-time time-value-120')
        report.check('reload: groups disabled to match', chrome.js(CONSISTENT), '')
        report.check('reload then start', start(chrome),
                     '?language=spanish&accent=off&topic=none&complexity=low&mode=time&time-value=120')


def run(report, base):
    keyboard(report, base)
    coming_back(report, base, cache=True)
    coming_back(report, base, cache=False)
