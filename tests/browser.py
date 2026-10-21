"""Shared pieces for the browser tests: a local web server for the site,
a headless Chrome driven over the DevTools protocol, and pass/fail reporting.
"""

import functools
import http.server
import itertools
import json
import os
import shutil
import subprocess
import tempfile
import threading
import time
import urllib.request

import websocket  # pip install websocket-client

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# REPORTING

class Report:
    def __init__(self):
        self.passed = 0
        self.failed = []

    def section(self, title):
        print(f'\n=== {title}', flush=True)

    def check(self, name, got, want):
        if got == want:
            self.passed += 1
            print(f'PASS {name}', flush=True)
        else:
            self.failed.append(name)
            print(f'FAIL {name}: got {got!r}, expected {want!r}', flush=True)
            if os.environ.get('GITHUB_ACTIONS'):
                print(f'::error title=Browser test failed::{name}: got {got!r}, expected {want!r}')

    def error(self, name, error):
        self.check(f'{name} (crashed: {error})', False, True)


# WEB SERVER

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class QuietServer(http.server.ThreadingHTTPServer):
    def handle_error(self, request, client_address):
        pass  # CHROME CLOSING WITH A CONNECTION STILL OPEN IS NOT A PROBLEM


def serve():
    """Serve the repository root on a free port, return its base URL."""
    handler = functools.partial(QuietHandler, directory=ROOT)
    server = QuietServer(('127.0.0.1', 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return f'http://127.0.0.1:{server.server_port}'


# CHROME

def find_chrome():
    if os.environ.get('CHROME'):
        return os.environ['CHROME']
    for name in ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'chrome'):
        if shutil.which(name):
            return shutil.which(name)
    for path in (r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                 r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                 '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'):
        if os.path.exists(path):
            return path
    raise SystemExit('Chrome not found, set the CHROME environment variable to its path')


class Chrome:
    KEY_CODES = {'Tab': 9, 'Enter': 13, 'Escape': 27, 'Backspace': 8, ' ': 32,
                 'ArrowLeft': 37, 'ArrowUp': 38, 'ArrowRight': 39, 'ArrowDown': 40}

    def __init__(self, *flags):
        self.profile = tempfile.mkdtemp(prefix='just-type-test-')
        args = [find_chrome(), '--headless=new', '--remote-debugging-port=0', f'--user-data-dir={self.profile}',
                '--no-first-run', '--no-default-browser-check', *flags, 'about:blank']
        if os.environ.get('CI'):
            args.insert(1, '--no-sandbox')
        self.process = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # CHROME WRITES THE PORT IT PICKED INTO THE PROFILE FOLDER
        port_file = os.path.join(self.profile, 'DevToolsActivePort')
        deadline = time.time() + 30
        while not (os.path.exists(port_file) and open(port_file).read().strip()):
            if time.time() > deadline:
                raise RuntimeError('Chrome did not start')
            time.sleep(0.1)
        port = open(port_file).read().split()[0]
        while True:
            try:
                targets = json.load(urllib.request.urlopen(f'http://127.0.0.1:{port}/json/list'))
                page = next(t for t in targets if t['type'] == 'page')
                break
            except (OSError, StopIteration):
                if time.time() > deadline:
                    raise RuntimeError('Chrome has no page to drive')
                time.sleep(0.1)

        self.ws = websocket.create_connection(page['webSocketDebuggerUrl'], suppress_origin=True, timeout=60)
        self.ids = itertools.count(1)
        self.cdp('Page.enable')
        # HEADLESS PAGES ARE NEVER FOCUSED OTHERWISE, AND THE CLIPBOARD NEEDS FOCUS
        self.cdp('Emulation.setFocusEmulationEnabled', enabled=True)
        self.screen(1280, 900)

    def close(self):
        try:
            self.ws.close()
        finally:
            self.process.kill()
            self.process.wait()
            shutil.rmtree(self.profile, ignore_errors=True)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def cdp(self, method, **params):
        message_id = next(self.ids)
        self.ws.send(json.dumps({'id': message_id, 'method': method, 'params': params}))
        while True:
            message = json.loads(self.ws.recv())
            if message.get('id') == message_id:
                if 'error' in message:
                    raise RuntimeError(f'{method}: {message["error"]["message"]}')
                return message.get('result')

    def js(self, expression):
        result = self.cdp('Runtime.evaluate', expression=expression, awaitPromise=True, returnByValue=True)
        if 'exceptionDetails' in result:
            details = result['exceptionDetails']
            raise RuntimeError(details.get('exception', {}).get('description') or details.get('text'))
        return result['result'].get('value')

    def wait(self, expression, timeout=10):
        """Wait until the expression is truthy in the page, return its value."""
        deadline = time.time() + timeout
        while True:
            try:
                value = self.js(expression)
                if value:
                    return value
            except RuntimeError:
                pass  # THE PAGE IS BETWEEN DOCUMENTS
            if time.time() > deadline:
                raise TimeoutError(f'waited {timeout}s for {expression}')
            time.sleep(0.02)

    def screen(self, width, height, phone=False):
        self.cdp('Emulation.setDeviceMetricsOverride', width=width, height=height,
                 deviceScaleFactor=3 if phone else 1, mobile=phone)
        self.cdp('Emulation.setTouchEmulationEnabled', enabled=phone, maxTouchPoints=5)

    def mark(self):
        """Tag the current document, so loaded() can tell when another one replaced it.
        A page coming back from the back/forward cache keeps an older tag, so each tag is new."""
        self.tag = f'{time.time()}'
        self.js(f'window.__tag = {json.dumps(self.tag)}')

    def loaded(self, path=''):
        """Wait for another document (after mark()) that has finished loading."""
        self.wait(f"window.__tag !== {json.dumps(self.tag)} && document.readyState === 'complete'"
                  f" && location.pathname.endsWith({json.dumps(path)})")
        if path.endswith('type.html'):
            self.wait("document.getElementById('word-display').textContent")

    def goto(self, url):
        self.mark()
        self.cdp('Page.navigate', url=url)
        self.loaded(url.split('?')[0].rsplit('/', 1)[-1])

    def back(self, path):
        self.mark()
        self.js('history.back()')
        self.loaded(path)

    def key(self, key, shift=False):
        if key in self.KEY_CODES:
            code = self.KEY_CODES[key]
        elif key.isascii() and key.isalnum():
            code = ord(key.upper())
        else:
            code = 0
        text = '\r' if key == 'Enter' else key if len(key) == 1 else ''
        event = dict(key=key, code='Space' if key == ' ' else key, windowsVirtualKeyCode=code, modifiers=8 if shift else 0)
        self.cdp('Input.dispatchKeyEvent', type='keyDown' if text else 'rawKeyDown', text=text, **event)
        self.cdp('Input.dispatchKeyEvent', type='keyUp', **event)

    def type(self, text, delay=0.01):
        for char in text:
            self.key(char)
            time.sleep(delay)

    def center(self, selector):
        return self.js(f"""(() => {{
            const r = document.querySelector({json.dumps(selector)}).getBoundingClientRect();
            return [r.x + r.width / 2, r.y + r.height / 2];
        }})()""")

    def click(self, selector=None, at=None):
        x, y = at or self.center(selector)
        for kind in ('mouseMoved', 'mousePressed', 'mouseReleased'):
            self.cdp('Input.dispatchMouseEvent', type=kind, x=x, y=y, button='left', clickCount=1)

    def tap(self, selector=None, at=None):
        x, y = at or self.center(selector)
        self.cdp('Input.dispatchTouchEvent', type='touchStart', touchPoints=[{'x': x, 'y': y}])
        self.cdp('Input.dispatchTouchEvent', type='touchEnd', touchPoints=[])
