"""Smoke the actual Pages origin with installed Edge and rendered UI controls.

This does not upload a test harness/fixtures or claim full six-group coverage.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import socket
import subprocess
import tempfile
import time
import urllib.request
from urllib.parse import urljoin
from run_browser import ROOT, EDGE, WebSocket

RUNTIME = ['index.html', 'styles.css', 'app.js', 'domain.js', 'guidance.js',
           'reports.js', 'seeds.js', 'sla.js', 'storage.js']


def main(url):
    stamp = time.strftime('%Y%m%d-%H%M%S', time.gmtime())
    prefix = ROOT / 'tests/evidence' / ('pages-public-smoke-' + stamp)
    result = {'url': url, 'started_utc': stamp,
              'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
              'scope': 'Six groups: initial-state smoke only. DEMO-01: complete ticket workflow. Not the local 110-case suite.',
              'checks': [], 'assets': [], 'screenshots': []}

    def check(name, value):
        result['checks'].append({'name': name, 'passed': bool(value)})
        if not value:
            raise AssertionError(name)

    try:
        for name in RUNTIME:
            with urllib.request.urlopen(urljoin(url, name), timeout=30) as response:
                content = response.read()
                digest = hashlib.sha256(content).hexdigest()
                result['assets'].append({'file': name, 'status': response.status, 'sha256': digest})
                check('public asset matches source: ' + name,
                      digest == hashlib.sha256((ROOT / 'prototype' / name).read_bytes()).hexdigest())
        with socket.socket() as s:
            s.bind(('127.0.0.1', 0))
            port = s.getsockname()[1]
        with tempfile.TemporaryDirectory(prefix='pages-smoke-') as profile:
            with prefix.with_name(prefix.name + '-edge.log').open('w', encoding='utf8') as log:
                proc = subprocess.Popen([str(EDGE), '--headless=new', '--disable-gpu', '--no-sandbox',
                    '--no-first-run', '--no-default-browser-check', '--remote-allow-origins=*',
                    f'--remote-debugging-port={port}', f'--user-data-dir={profile}', 'about:blank'],
                    stdout=log, stderr=log, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
                ws = None
                try:
                    for _ in range(100):
                        try:
                            targets = json.load(urllib.request.urlopen(f'http://127.0.0.1:{port}/json', timeout=2))
                            if targets:
                                break
                        except OSError:
                            time.sleep(.1)
                    ws = WebSocket(next(t['webSocketDebuggerUrl'] for t in targets if t['type'] == 'page'))
                    for domain in ['Network', 'Runtime', 'Page']:
                        ws.call(domain + '.enable')
                    ws.call('Emulation.setDeviceMetricsOverride', {'width': 1440, 'height': 1080, 'deviceScaleFactor': 1, 'mobile': False})
                    ws.call('Page.navigate', {'url': url})
                    for _ in range(100):
                        if ws.evaluate("!!document.querySelector('#main')?.children.length"):
                            break
                        time.sleep(.1)

                    def ev(js):
                        return ws.evaluate(js)

                    def change(selector, value):
                        ev(f"(()=>{{const e=document.querySelector({json.dumps(selector)});e.value={json.dumps(str(value))};e.dispatchEvent(new Event('change',{{bubbles:true}}));}})()")
                        time.sleep(.1)

                    def click(selector):
                        check('control available: ' + selector, ev(f"!!document.querySelector({json.dumps(selector)}) && !document.querySelector({json.dumps(selector)}).disabled"))
                        ev(f"document.querySelector({json.dumps(selector)}).click()")
                        time.sleep(.1)

                    def form(selector, values):
                        ev(f"(()=>{{const f=document.querySelector({json.dumps(selector)});for(const [k,v] of Object.entries({json.dumps(values)}))f.elements[k].value=v;f.requestSubmit();}})()")
                        time.sleep(.1)
                        check('form accepted: ' + selector, ev("!document.querySelector('#feedback').classList.contains('error')"))

                    def go(ticket=1):
                        ev(f"location.hash='ticket/{ticket}'")
                        time.sleep(.1)

                    def clock(hour):
                        form('#clock-form', {'clock-target': '2026-10-05T' + hour})

                    def screenshot(name):
                        shot = ws.call('Page.captureScreenshot', {'format': 'png', 'captureBeyondViewport': True})
                        dest = prefix.with_name(prefix.name + '-' + name + '.png')
                        dest.write_bytes(base64.b64decode(shot['data']))
                        result['screenshots'].append(str(dest.relative_to(ROOT)).replace('\\', '/'))

                    check('actual Pages origin', ev('location.href') == url)
                    check('simulation banner', ev("document.querySelector('.demo-banner').textContent.includes('không gọi API')"))
                    # Six initial-state smokes, not full local scenario assertions.
                    for i in range(1, 7):
                        scenario = f'DEMO-{i:02}'
                        change('#scenario', scenario)
                        check(scenario + ' selected', ev("document.querySelector('#guide-title').textContent").startswith(scenario))
                        change('#identity', 3)
                        check(scenario + ' Agent view', ev('location.hash') == '#agent')
                        screenshot(scenario + '-initial')
                        change('#identity', 6)
                        check(scenario + ' Manager view', ev("!!document.querySelector('#manager-reports')"))
                        change('#identity', 1)
                        check(scenario + ' Customer privacy', ev("document.querySelectorAll('[data-internal],.metric,.sla,[data-action=note],[data-action=review]').length") == 0)
                    change('#scenario', 'DEMO-06')
                    variants = ev("[...document.querySelector('#variant').options].map(o=>o.value)")
                    for variant in variants:
                        change('#variant', variant)
                        check('variant selected: ' + variant, ev("JSON.parse(localStorage.getItem('ba-ticketing.prototype.v1')).variant") == variant)
                    before = ev("JSON.parse(localStorage.getItem('ba-ticketing.prototype.v1')).clock")
                    click('[data-advance="1"]')
                    check('clock advances', ev("JSON.parse(localStorage.getItem('ba-ticketing.prototype.v1')).clock") != before)
                    click('#reset')
                    check('reset restores clock', ev("JSON.parse(localStorage.getItem('ba-ticketing.prototype.v1')).clock") == before)
                    change('#scenario', 'DEMO-01')
                    change('#identity', 1)
                    form('[data-action=create]', {'title': 'Pages smoke DEMO-01', 'description': 'Browser-only deployment validation', 'priority': 'HIGH'})
                    clock('09:05:00')
                    change('#identity', 3)
                    click('[data-claim="1"]')
                    clock('09:10:00')
                    form('[data-action=message]', {'content': 'Pages smoke public reply'})
                    clock('09:30:00')
                    form('[data-action=resolve]', {'resolution_summary': 'Pages smoke resolution'})
                    clock('09:35:00')
                    change('#identity', 1)
                    go()
                    click('[data-confirm="1"]')
                    check('DEMO-01 Closed visible', ev("document.querySelector('#main').textContent.includes('Closed')"))
                    check('Customer detail privacy', ev("document.querySelectorAll('[data-internal],.sla,[data-action=note],[data-action=review]').length") == 0)
                    screenshot('customer-closed')
                    stored = ev("localStorage.getItem('ba-ticketing.prototype.v1')")
                    ws.call('Page.reload', {'ignoreCache': True})
                    time.sleep(1)
                    check('Pages localStorage persists across reload', stored == ev("localStorage.getItem('ba-ticketing.prototype.v1')"))
                    check('reload renders Closed', ev("document.querySelector('#main').textContent.includes('Closed')"))
                    change('#identity', 2)
                    go()
                    check('other Customer cannot view ticket', ev("document.querySelector('#main').textContent.includes('404')"))
                    change('#scenario', 'DEMO-04')
                    change('#identity', 6)
                    for heading in ['manager-reviews', 'manager-reports', 'manager-load', 'manager-tickets']:
                        click('[data-jump="' + heading + '"]')
                        check('Manager navigation ' + heading, ev('document.activeElement.id') == heading)
                    screenshot('manager-dashboard')
                    go()
                    check('Manager review form present', ev("!!document.querySelector('[data-action=review]')"))
                    check('Manager restricted actions absent', ev("document.querySelectorAll('[data-claim],[data-confirm],[data-action=message],[data-action=resolve]').length") == 0)
                    screenshot('manager-review-detail')
                    change('#identity', 3)
                    go()
                    check('Agent review blocks Resolved', ev("document.querySelector('[data-action=resolve] button').disabled"))
                    click('.controls summary')
                    check('collapsed controls', ev("!document.querySelector('.controls').open"))
                    screenshot('agent-controls-collapsed')
                    result['runtime_errors'] = [e for e in ws.events if e.get('method') == 'Runtime.exceptionThrown']
                    result['requests'] = [{'url': e['params']['request']['url'], 'type': e['params'].get('type'), 'method': e['params']['request']['method']} for e in ws.events if e.get('method') == 'Network.requestWillBeSent']
                    result['responses'] = [{'url': e['params']['response']['url'], 'status': e['params']['response']['status'], 'type': e['params'].get('type')} for e in ws.events if e.get('method') == 'Network.responseReceived']
                    result['network_failures'] = [e['params'] for e in ws.events if e.get('method') == 'Network.loadingFailed']
                    check('no blocking JavaScript errors', not result['runtime_errors'])
                    check('no Fetch/XHR/API requests', not any(r['type'] in ['Fetch', 'XHR'] or '/api/' in r['url'] or ':8000' in r['url'] for r in result['requests']))
                    check('browser runtime assets loaded', all(any(r['status'] == 200 and r['url'] == urljoin(url, name) for r in result['responses']) for name in RUNTIME if name != 'index.html'))
                finally:
                    if ws:
                        ws.sock.close()
                    proc.terminate()
                    proc.wait(timeout=15)
    except Exception as error:
        result['error'] = str(error)
    result['passed'] = not result.get('error') and all(c['passed'] for c in result['checks'])
    prefix.with_suffix('.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf8')
    print(json.dumps({'passed': result['passed'], 'error': result.get('error'), 'checks': len(result['checks']), 'evidence': str(prefix.with_suffix('.json'))}))
    return int(not result['passed'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='Literal html_url returned by GitHub Pages')
    raise SystemExit(main(parser.parse_args().url))
