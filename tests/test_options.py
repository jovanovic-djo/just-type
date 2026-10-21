"""Home page options: which groups are disabled or hidden, what the form sends,
and that every possible test opens with the right words."""

from browser import Chrome

# THE RULES, WRITTEN OUT AGAIN HERE ON PURPOSE, SO A CHANGE TO js/home.js IS CHECKED AGAINST THEM
RULES = """
const GROUPS = {language: 'language-choice', accent: 'accent-choice', topic: 'topic-choice', complexity: 'complexity-choice',
                mode: 'mode-choice', 'mode-value': 'mode-value-choice', 'time-value': 'time-value-choice'};
const expectDisabled = s => {
    const quote = s.language !== 'lorem' && s.topic === 'quotes';
    return {
        language: s.topic === 'numbers',
        topic: s.language === 'lorem',
        accent: ['english', 'lorem'].includes(s.language) || s.topic === 'numbers',
        complexity: s.language === 'lorem' || s.topic !== 'none',
        mode: quote,
        'mode-value': quote || s.mode === 'time',
        'time-value': quote || s.mode !== 'time',
    };
};
const fileFor = p => p.get('language') === 'lorem' ? 'lorem'
    : p.get('topic') === 'none' ? p.get('language') + p.get('complexity')
    : p.get('topic') === 'numbers' ? 'numbers'
    : p.get('language') + p.get('topic');
"""

# CLICK RANDOM OPTION LABELS (DISABLED ONES TOO) AND CHECK THE PAGE AFTER EVERY CLICK
WALK = RULES + """
(async () => {
    const fails = [], fail = (...a) => { if (fails.length < 20) fails.push(a.join(' ')); };
    let seed = 12345;
    const random = n => {  // mulberry32, so every run clicks the same way
        seed = seed + 0x6D2B79F5 | 0;
        let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
        t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
        return Math.floor(((t ^ t >>> 14) >>> 0) / 4294967296 * n);
    };
    const form = document.querySelector('form');
    const state = () => Object.fromEntries(Object.keys(GROUPS).map(n => [n, form.elements[n].value]));
    const labels = [...form.querySelectorAll('label')];
    const files = {};
    const fileExists = async name => files[name] ??= (await fetch(`words/${name}.json`)).ok;
    const reached = new Set();
    let blocked = 0;

    for (let i = 0; i < CLICKS; i++) {
        const label = labels[random(labels.length)], radio = document.getElementById(label.htmlFor);
        const before = JSON.stringify(state()), wasDisabled = radio.disabled;
        label.click();
        const s = state();
        if (wasDisabled) {
            blocked++;
            if (JSON.stringify(s) !== before) fail('clicking disabled', label.htmlFor, 'changed the selection');
        } else if (!radio.checked) {
            fail('clicking', label.htmlFor, 'did not select it');
        }
        const disabled = expectDisabled(s);
        for (const [name, group] of Object.entries(GROUPS)) {
            const radios = [...document.querySelectorAll(`#${group} input`)];
            if (radios.filter(r => r.checked).length !== 1) fail(name, 'does not have exactly one choice');
            if (radios.some(r => r.disabled !== disabled[name])) fail(name, 'disabled should be', disabled[name], 'in', JSON.stringify(s));
        }
        if (document.getElementById('mode-value-choice').hidden !== (s.mode === 'time')) fail('word counts shown wrong in', JSON.stringify(s));
        if (document.getElementById('time-value-choice').hidden !== (s.mode !== 'time')) fail('seconds shown wrong in', JSON.stringify(s));
        const sent = new URLSearchParams(new FormData(form));
        for (const name of Object.keys(GROUPS)) {
            if (sent.has(name) === disabled[name]) fail(name, disabled[name] ? 'sent although disabled' : 'missing although enabled', sent);
        }
        if (!await fileExists(fileFor(sent))) fail('no word file', fileFor(sent), 'for', sent);
        reached.add(sent.toString());
    }

    // EVERY SELECTION THE RULES ALLOW, AS THE FORM WOULD SEND IT
    const values = Object.fromEntries(Object.keys(GROUPS).map(n => [n, [...form.querySelectorAll(`[name="${n}"]`)].map(r => r.value)]));
    const all = new Set();
    const combine = (names, s) => {
        if (!names.length) {
            if (s.language === 'lorem' && s.topic === 'numbers') return;  // each disables the other, can't be chosen
            const disabled = expectDisabled(s);
            all.add(new URLSearchParams(Object.entries(s).filter(([n]) => !disabled[n])).toString());
            return;
        }
        for (const v of values[names[0]]) combine(names.slice(1), {...s, [names[0]]: v});
    };
    combine(Object.keys(GROUPS), {});
    for (const q of reached) if (!all.has(q)) fail('reached a selection the rules do not allow:', q);
    return {fails, labels: labels.length, blocked, reached: reached.size, all: [...all]};
})()
"""

# CHECK A TEST PAGE AGAINST THE OPTIONS IN ITS ADDRESS
CHECK_TEST = RULES + """
(async () => {
    const p = new URLSearchParams(location.search), problems = [];
    const text = document.getElementById('word-display').textContent;
    const timed = p.get('mode') === 'time' && p.get('topic') !== 'quotes';
    const quote = p.get('topic') === 'quotes' && p.get('language') !== 'lorem';
    let list = (await (await fetch(`words/${fileFor(p)}.json`)).json()).words;
    const map = accentMaps[p.get('language')];
    if (p.get('accent') === 'off' && map) {
        list = list.map(w => [...w].map(c => map[c] || c).join(''));
        if ([...text].some(c => map[c])) problems.push('accents left in');
    }
    if (quote) {
        if (!list.includes(text)) problems.push('not a quote from the list');
    } else {
        const words = text.split(' '), want = timed ? 4 * p.get('time-value') : +p.get('mode-value');
        if (words.length !== want) problems.push(`${words.length} words instead of ${want}`);
        const strangers = words.filter(w => !list.includes(w));
        if (strangers.length) problems.push('words not in the list: ' + strangers.slice(0, 3));
    }
    const timer = document.getElementById('timer');
    if (timer.hidden === timed) problems.push('timer ' + (timed ? 'hidden' : 'shown'));
    if (timed && timer.textContent !== p.get('time-value')) problems.push('timer starts at ' + timer.textContent);
    const c = p.get('complexity'), classes = [...document.getElementById('word-display').classList].sort().join(' ');
    const want = [...(['high', 'insane'].includes(c) ? ['complexity-' + c] : []), ...(timed ? ['timed'] : [])].sort().join(' ');
    if (classes !== want) problems.push(`classes "${classes}" instead of "${want}"`);
    return problems.join(', ') || 'ok';
})()
"""


def run(report, base, clicks=4000):
    with Chrome() as chrome:
        report.section(f'home page options: {clicks} random clicks')
        chrome.goto(base + '/index.html')
        result = chrome.js(WALK.replace('CLICKS', str(clicks)))
        report.check('every click keeps the options consistent', result['fails'], [])
        report.check('the walk clicks disabled options too', result['blocked'] > 0, True)
        print(f'     {result["labels"]} options, {result["blocked"]} clicks on disabled ones, '
              f'{result["reached"]} of {len(result["all"])} possible selections reached')

        report.section(f'every possible test ({len(result["all"])})')
        wrong = []
        for query in result['all']:
            try:
                chrome.goto(f'{base}/type.html?{query}')
                problems = chrome.js(CHECK_TEST)
            except Exception as error:  # noqa: BLE001 - reported as a failure below
                problems = f'crashed: {error}'
            if problems != 'ok':
                wrong.append(f'{query}: {problems}')
        report.check(f'all {len(result["all"])} tests show the right words, timer and size', wrong[:10], [])
