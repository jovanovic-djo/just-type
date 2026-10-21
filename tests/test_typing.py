"""The test page: typing, word locking, pasting, the results and their buttons, hotkeys and the timer."""

import json
import time

from browser import Chrome

WORDS = '/type.html?language=english&accent=on&topic=none&complexity=low&mode=words&mode-value=5'
TIMED = '/type.html?language=german&accent=on&topic=none&complexity=low&mode=time&time-value=15'

# WORD LOCKING, CHECKED IN THE PAGE: RETURNS [name, got, expected] FOR EACH CHECK
LOCKING = """(() => {
    const input = document.getElementById('typing-input'), target = document.getElementById('word-display').textContent;
    const words = target.split(' '), checks = [];
    const set = v => { input.value = v; input.dispatchEvent(new Event('input', {bubbles: true})); return input.value; };
    const type = s => { for (const c of s) set(input.value + c); return input.value; };
    const erase = n => { for (let i = 0; i < n; i++) set(input.value.slice(0, -1)); return input.value; };
    const restart = () => document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Tab', bubbles: true, cancelable: true}));
    const typo = w => (w[0] === 'q' ? 'z' : 'q') + w.slice(1);
    const check = (name, got, want) => checks.push([name, got, want]);

    type(words[0] + ' ' + words[1].slice(0, 2));
    check('a correct word with its space locks', erase(30), words[0] + ' ');
    restart(); type(words[0]);
    check('a correct word without its space does not lock', erase(30), '');
    restart(); type(typo(words[0]) + ' ' + words[1].slice(0, 2));
    check('a wrong word can be deleted', erase(30), '');
    restart(); type(words[0] + ' ' + typo(words[1]) + ' ' + words[2].slice(0, 1));
    check('deleting stops at the last correct word', erase(30), words[0] + ' ');
    type(words[1] + ' ');
    check('a fixed word locks', erase(30), words[0] + ' ' + words[1] + ' ');
    restart(); type(words[0] + 'x');
    check('a wrong character instead of the space does not lock', erase(30), '');
    restart(); type(words[0] + ' ' + words[1].slice(0, 2));
    check('selecting everything and deleting keeps the locked word', set(''), words[0] + ' ');
    const before = input.value;
    check('typing in the middle is undone', set('Z' + before), before);
    for (const key of ['ArrowLeft', 'Home', 'End', 'PageUp']) {
        const event = new KeyboardEvent('keydown', {key, bubbles: true, cancelable: true});
        input.dispatchEvent(event);
        check(key + ' cannot move the caret', event.defaultPrevented, true);
    }
    return checks;
})()"""

modal = lambda c: c.js("document.getElementById('result-modal').style.display")
value = lambda c: c.js("document.getElementById('typing-input').value")
words = lambda c: c.js("document.getElementById('word-display').textContent")
focused = lambda c: c.js('document.activeElement.id')
result = lambda c, name: c.js(f"document.getElementById('{name}').innerText")
timer = lambda c: c.js("document.getElementById('timer').textContent")


def finish(chrome, typo=False):
    text = words(chrome)
    if typo:
        chrome.key('q' if text[0] != 'q' else 'z')
        chrome.key('Backspace')
    chrome.type(text)
    chrome.wait("document.getElementById('result-modal').style.display === 'block'")
    return text


def locking(report, chrome, base):
    for name, url in (('words mode', WORDS.replace('mode-value=5', 'mode-value=10')), ('time mode', TIMED)):
        report.section(f'word locking, {name}')
        chrome.goto(base + url)
        for check, got, want in chrome.js(LOCKING):
            report.check(check, got, want)


def pasting(report, chrome, base):
    report.section('pasting')
    chrome.cdp('Browser.grantPermissions', origin=base, permissions=['clipboardReadWrite', 'clipboardSanitizedWrite'])
    chrome.goto(base + WORDS)
    text = words(chrome)
    report.check('clipboard holds the whole test',
                 chrome.js(f"navigator.clipboard.writeText({json.dumps(text)}).then(() => navigator.clipboard.readText())"), text)
    chrome.js("document.getElementById('typing-input').focus()")
    paste = dict(key='v', code='KeyV', windowsVirtualKeyCode=86, modifiers=2)
    chrome.cdp('Input.dispatchKeyEvent', type='rawKeyDown', commands=['paste'], **paste)
    chrome.cdp('Input.dispatchKeyEvent', type='keyUp', **paste)
    time.sleep(0.3)
    report.check('ctrl+v pastes nothing', value(chrome), '')
    report.check('no results after pasting', modal(chrome), '')
    chrome.type(text[:3])
    report.check('typing still works', value(chrome), text[:3])

    # THE WHOLE TEXT IN ONE INPUT EVENT (E.G. A PHONE KEYBOARD INSERTING IT) HAS NO TYPING TIME.
    # THE CLOCK TICKS 5ms ON EVERY READ HERE, SO THE PAGE CAN'T RELY ON THE TWO READS BEING EQUAL
    chrome.goto(base + WORDS)
    chrome.js("""(() => { const RealDate = Date; let now = RealDate.now();
        window.Date = class extends RealDate { constructor(...a) { if (a.length) super(...a); else super(now += 5); } };
        const i = document.getElementById('typing-input');
        i.value = document.getElementById('word-display').textContent;
        i.dispatchEvent(new Event('input', {bubbles: true})); })()""")
    report.check('finishing in one go shows 0, not a huge speed',
                 [result(chrome, 'cpm'), result(chrome, 'wpm'), result(chrome, 'accuracy'), result(chrome, 'time')],
                 ['CPM: 0', 'WPM: 0', 'Accuracy: 100%', 'Time: 0.0s'])


def buttons(report, chrome, base, device):
    report.section(f'results buttons, {device}')
    press = chrome.tap if device == 'phone' else chrome.click
    chrome.goto(base + WORDS)
    if device == 'phone':
        chrome.type(words(chrome)[:2])
        chrome.mark()
        chrome.key('Enter')
        report.check("the keyboard's enter key mid-test does nothing", same_page(chrome), True)
        chrome.key('Tab')
    first = finish(chrome, typo=True)
    report.check('results shown at the end', modal(chrome), 'block')
    report.check('a typo fixed with backspace still counts', result(chrome, 'mistakes'), 'Mistakes: 1')
    report.check('WPM is a number', result(chrome, 'wpm').split(': ')[1].isdigit(), True)

    chrome.type('abc')
    report.check('typing after the end is ignored', value(chrome), first)
    press(at=chrome.center('#cpm'))
    time.sleep(0.2)
    report.check('pressing the results text does nothing', modal(chrome), 'block')

    if device == 'desktop':
        x, y = chrome.center('#restart-button')
        chrome.cdp('Input.dispatchMouseEvent', type='mousePressed', x=x, y=y, button='left', clickCount=1)
        chrome.cdp('Input.dispatchMouseEvent', type='mouseMoved', x=x, y=y + 200, button='left')
        chrome.cdp('Input.dispatchMouseEvent', type='mouseReleased', x=x, y=y + 200, button='left', clickCount=1)
        time.sleep(0.2)
        report.check('pressing restart and sliding off does nothing', modal(chrome), 'block')
        report.check('the input keeps the focus', focused(chrome), 'typing-input')

    press('#restart-button')
    chrome.wait("document.getElementById('result-modal').style.display === 'none'")
    report.check('restart: same words, empty input', [words(chrome), value(chrome)], [first, ''])
    report.check('restart: input focused, so the phone keyboard opens', focused(chrome), 'typing-input')
    report.check('restart: title no longer faded', chrome.js("document.getElementById('test-title').style.opacity"), '0.8')

    finish(chrome)
    report.check('restart: mistakes start from 0', [result(chrome, 'mistakes'), result(chrome, 'accuracy')],
                 ['Mistakes: 0', 'Accuracy: 100%'])

    press('#restart-button')
    press(at=chrome.center('#restart-button'))
    time.sleep(0.2)
    chrome.type(first[:2])
    report.check('pressing restart twice: typing works', [modal(chrome), value(chrome)], ['none', first[:2]])
    chrome.type(first[2:])

    url = chrome.js('location.href')
    chrome.mark()
    press('#new-test-button')
    chrome.loaded('type.html')
    report.check('new test: same options', chrome.js('location.href'), url)
    report.check('new test: fresh, with the input focused', [modal(chrome), value(chrome), focused(chrome)],
                 ['', '', 'typing-input'])

    finish(chrome)
    chrome.mark()
    press('#home-button')
    chrome.loaded('index.html')
    report.check('home: on the home page', chrome.js("location.pathname.endsWith('/index.html')"), True)


def fits(report, chrome, base):
    report.section('results buttons fit on small screens')
    for width, height in ((320, 568), (390, 844), (430, 932), (844, 390), (390, 450)):
        chrome.screen(width, height, phone=True)
        chrome.goto(base + WORDS)
        finish(chrome)
        report.check(f'{width}x{height}: all buttons on screen and tappable', chrome.js("""
            [...document.querySelectorAll('.result-actions button')].every(b => {
                const r = b.getBoundingClientRect();
                return r.top >= 0 && r.left >= 0 && r.bottom <= innerHeight && r.right <= innerWidth
                    && document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2) === b;
            })"""), True)


def hotkeys(report, chrome, base):
    report.section('hotkeys')
    chrome.goto(base + WORDS)
    first = finish(chrome)
    chrome.key('Tab')
    time.sleep(0.2)
    report.check('tab on the results restarts', [modal(chrome), value(chrome), words(chrome)], ['none', '', first])
    finish(chrome)
    url = chrome.js('location.href')
    chrome.mark()
    chrome.key('Enter')
    chrome.loaded('type.html')
    report.check('enter on the results starts a new test', [chrome.js('location.href'), modal(chrome)], [url, ''])
    finish(chrome)
    chrome.mark()
    chrome.key('Escape')
    chrome.loaded('index.html')
    report.check('esc on the results goes home', chrome.js("location.pathname.endsWith('/index.html')"), True)


def same_page(chrome):
    """After mark(): wait a moment and say whether the page is still the same document."""
    time.sleep(0.7)
    return chrome.js(f'window.__tag === {json.dumps(chrome.tag)}')


def enter(report, chrome, base):
    report.section('enter')
    chrome.goto(base + WORDS)
    chrome.mark()
    chrome.key('Enter')
    chrome.loaded('type.html')
    report.check('before typing: enter gives new words', True, True)

    text = words(chrome)
    chrome.type(text[:3])
    chrome.mark()
    chrome.key('Enter')
    report.check('while typing: enter does nothing', [same_page(chrome), value(chrome)], [True, text[:3]])
    chrome.type(text[3:])
    chrome.wait("document.getElementById('result-modal').style.display === 'block'")
    report.check('while typing: the test can still be finished', modal(chrome), 'block')

    chrome.key('Tab')
    chrome.mark()
    chrome.key('Enter')
    chrome.loaded('type.html')
    report.check('after tab restarts: enter gives new words again', True, True)

    chrome.goto(base + TIMED)
    chrome.type(words(chrome)[:3])
    chrome.mark()
    chrome.key('Enter')
    report.check('time mode while typing: enter does nothing', same_page(chrome), True)
    time.sleep(1.5)
    report.check('time mode while typing: the timer keeps running', timer(chrome) in ('14', '13'), True)


def timed(report, chrome, base):
    report.section('time mode')
    chrome.goto(base + TIMED)
    report.check('timer shows the seconds', timer(chrome), '15')
    time.sleep(1.5)
    report.check('timer waits for the first key', timer(chrome), '15')
    text = words(chrome)
    chrome.type(text[:6])
    chrome.key('q' if text[6] != 'q' else 'z')
    chrome.wait("document.getElementById('result-modal').style.display === 'block'", timeout=20)
    report.check('time up: results with the full time', result(chrome, 'time'), 'Time: 15.0s')
    report.check('time up: the typo counted', result(chrome, 'mistakes'), 'Mistakes: 1')
    chrome.type('xyz')
    report.check('typing after time up is ignored', len(value(chrome)), 7)
    chrome.click('#restart-button')
    time.sleep(0.3)
    report.check('restart: timer back to 15, results hidden', [timer(chrome), modal(chrome)], ['15', 'none'])
    time.sleep(1.5)
    report.check('restart: timer waits for a key again', timer(chrome), '15')
    chrome.type(text[:3])
    time.sleep(2.2)
    report.check('restart: the countdown runs again', timer(chrome), '13')
    report.check('restart: the words start at the top', chrome.js("document.getElementById('word-display').scrollTop"), 0)
    chrome.wait("document.getElementById('result-modal').style.display === 'block'", timeout=20)
    chrome.mark()
    chrome.key('Enter')
    chrome.loaded('type.html')
    report.check('time up: enter starts a new test', modal(chrome), '')


def run(report, base):
    with Chrome() as chrome:
        locking(report, chrome, base)
        pasting(report, chrome, base)
        buttons(report, chrome, base, 'desktop')
        hotkeys(report, chrome, base)
        enter(report, chrome, base)
        timed(report, chrome, base)
    with Chrome() as chrome:
        chrome.screen(390, 844, phone=True)
        buttons(report, chrome, base, 'phone')
        fits(report, chrome, base)
