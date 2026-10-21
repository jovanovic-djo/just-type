"""Run the browser tests: python tests/run.py [options|home|typing ...]

Needs Google Chrome and the websocket-client package (pip install websocket-client).
Set CHROME to Chrome's path if it isn't found. Exits with status 1 if any check fails.
"""

import sys
import time
import traceback

import test_home
import test_options
import test_typing
from browser import Report, serve

SUITES = {'options': test_options, 'home': test_home, 'typing': test_typing}


def main():
    chosen = sys.argv[1:] or list(SUITES)
    unknown = [name for name in chosen if name not in SUITES]
    if unknown:
        raise SystemExit(f'unknown suite {", ".join(unknown)}, choose from {", ".join(SUITES)}')

    base = serve()
    report = Report()
    started = time.time()
    for name in chosen:
        try:
            SUITES[name].run(report, base)
        except Exception as error:  # noqa: BLE001 - a crash fails the run but the other suites still run
            traceback.print_exc()
            report.error(f'{name} suite', error)

    print(f'\n{report.passed} passed, {len(report.failed)} failed in {time.time() - started:.0f}s')
    for name in report.failed:
        print(f'  FAILED {name}')
    return 1 if report.failed else 0


if __name__ == '__main__':
    sys.exit(main())
