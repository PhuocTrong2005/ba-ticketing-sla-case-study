"""Standard-library CDP runner for installed Edge; no project dependency changes.

Serves the repo under /case-study/ to exercise project-subpath asset resolution.
Uses a private temporary browser profile; never touches the user's browser profile.
"""
import base64
import hashlib
import http.server
import json
import os
from pathlib import Path
import socket
import struct
import subprocess
import tempfile
import threading
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
EDGE = Path(os.environ.get('PROGRAMFILES(X86)', 'C:/Program Files (x86)')) / 'Microsoft/Edge/Application/msedge.exe'


class WebSocket:
    def __init__(self, url):
        from urllib.parse import urlsplit
        parsed = urlsplit(url)
        self.sock = socket.create_connection((parsed.hostname, parsed.port), timeout=30)
        key = base64.b64encode(os.urandom(16)).decode()
        self.sock.sendall((f'GET {parsed.path} HTTP/1.1\r\nHost: {parsed.netloc}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n').encode())
        header = b''
        while not header.endswith(b'\r\n\r\n'):
            header += self.sock.recv(1)
        if b' 101 ' not in header:
            raise RuntimeError(header.decode())
        self.seq = 0
        self.events = []

    def read(self, n):
        out = b''
        while len(out) < n:
            chunk = self.sock.recv(n - len(out))
            if not chunk:
                raise RuntimeError('CDP socket closed')
            out += chunk
        return out

    def receive(self):
        result = b''
        while True:
            a, b = self.read(2)
            size = b & 127
            if size == 126:
                size = struct.unpack('!H', self.read(2))[0]
            elif size == 127:
                size = struct.unpack('!Q', self.read(8))[0]
            mask = self.read(4) if b & 128 else None
            payload = self.read(size)
            if mask:
                payload = bytes(v ^ mask[i % 4] for i, v in enumerate(payload))
            if a & 15 == 8:
                raise RuntimeError('CDP closed')
            result += payload
            if a & 128:
                return json.loads(result)

    def call(self, method, params=None):
        self.seq += 1
        data = json.dumps({'id': self.seq, 'method': method, 'params': params or {}}).encode()
        mask = os.urandom(4)
        header = b'\x81' + (bytes([128 | len(data)]) if len(data) < 126 else b'\xfe' + struct.pack('!H', len(data)))
        self.sock.sendall(header + mask + bytes(v ^ mask[i % 4] for i, v in enumerate(data)))
        while True:
            msg = self.receive()
            if msg.get('id') == self.seq:
                if 'error' in msg:
                    raise RuntimeError(msg['error'])
                return msg.get('result', {})
            self.events.append(msg)

    def evaluate(self, expression):
        r = self.call('Runtime.evaluate', {'expression': expression, 'awaitPromise': True, 'returnByValue': True})
        if 'exceptionDetails' in r:
            raise RuntimeError(r['exceptionDetails'])
        return r.get('result', {}).get('value')


def main():
    stamp = time.strftime('%Y%m%d-%H%M%S', time.gmtime())
    prefix = ROOT / 'tests/evidence' / f'prototype-ux-{stamp}'
    requests = []

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(ROOT), **kwargs)

        def translate_path(self, path):
            if path.startswith('/case-study/'):
                path = path[len('/case-study'):]
            return super().translate_path(path)

        def log_message(self, format, *args):
            requests.append(format % args)

    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        debug_port = s.getsockname()[1]
    url = f'http://127.0.0.1:{server.server_port}/case-study/'
    source_hashes = {str(p.relative_to(ROOT)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest() for directory in ['prototype', 'tests/prototype'] for p in (ROOT / directory).glob('*') if p.is_file()}
    result = {'command': './.venv/Scripts/python.exe tests/prototype/run_browser.py', 'base_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(), 'fixture_sha256': hashlib.sha256((ROOT / 'tests/sla/sla-scenarios.json').read_bytes()).hexdigest(), 'source_sha256': source_hashes, 'base_url': url, 'started_utc': stamp}
    with tempfile.TemporaryDirectory(prefix='ticketing-prototype-') as profile:
        command = [str(EDGE), '--headless=new', '--disable-gpu', '--no-sandbox', '--no-first-run', '--no-default-browser-check', '--remote-allow-origins=*', f'--remote-debugging-port={debug_port}', f'--user-data-dir={profile}', 'about:blank']
        log_path = prefix.with_name(prefix.name + '-edge.log')
        with log_path.open('w', encoding='utf-8') as log:
            proc = subprocess.Popen(command, stdout=log, stderr=log, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            try:
                targets = None
                for _ in range(100):
                    try:
                        targets = json.load(urllib.request.urlopen(f'http://127.0.0.1:{debug_port}/json', timeout=2))
                        if targets:
                            break
                    except OSError:
                        time.sleep(.1)
                if not targets:
                    raise RuntimeError('Edge CDP unavailable')
                ws = WebSocket(next(t['webSocketDebuggerUrl'] for t in targets if t['type'] == 'page'))
                print('CDP connected', flush=True)
                ws.call('Network.enable')
                ws.call('Runtime.enable')
                ws.call('Page.enable')
                ws.call('Emulation.setDeviceMetricsOverride', {'width': 1440, 'height': 1080, 'deviceScaleFactor': 1, 'mobile': False})
                print('CDP domains enabled', flush=True)
                ws.call('Page.navigate', {'url': url + 'tests/prototype/index.html'})
                print('Harness navigated', flush=True)
                for _ in range(300):
                    capture = ws.evaluate('window.__capture || null')
                    if capture:
                        bounds = ws.evaluate("(()=>{const f=document.querySelector('#ui');const height=f.contentDocument.documentElement.scrollHeight;f.style.height=height+'px';const r=f.getBoundingClientRect();return {x:r.x+scrollX+2,y:r.y+scrollY+2,width:1280,height,scale:1}})()")
                        shot = ws.call('Page.captureScreenshot', {'format':'png','clip':bounds,'captureBeyondViewport':True})
                        prefix.with_name(prefix.name + '-' + capture['name'] + '.png').write_bytes(base64.b64decode(shot['data']))
                        ws.evaluate("document.querySelector('#ui').style.height='900px'")
                        ws.evaluate('window.__capture=null')
                    report = ws.evaluate('window.__prototypeResults || null')
                    if report:
                        break
                    time.sleep(.25)
                if not report:
                    raise RuntimeError('JS harness did not finish; see CDP events')
                result['harness'] = report
                print(json.dumps({'passed': report['passed'], 'failed': report['failed'], 'failures': [x for x in report['results'] if x['status'] == 'FAIL']}, ensure_ascii=False, indent=2))
                # Preview screenshots show actual prototype, not synthesized graphics.
                ws.call('Page.navigate', {'url': url + 'prototype/index.html'})
                time.sleep(.5)
                ws.evaluate("document.querySelector('#scenario').value='DEMO-04';document.querySelector('#scenario').dispatchEvent(new Event('change'));document.querySelector('#identity').value='6';document.querySelector('#identity').dispatchEvent(new Event('change'))")
                ws.call('Emulation.setDeviceMetricsOverride', {'width': 1440, 'height': 1080, 'deviceScaleFactor': 1, 'mobile': False})
                shot = ws.call('Page.captureScreenshot', {'format': 'png', 'captureBeyondViewport': True})
                prefix.with_name(prefix.name + '-manager-desktop.png').write_bytes(base64.b64decode(shot['data']))
                ws.evaluate("location.hash='ticket/1'")
                time.sleep(.2)
                shot = ws.call('Page.captureScreenshot', {'format': 'png', 'captureBeyondViewport': True})
                prefix.with_name(prefix.name + '-review-detail.png').write_bytes(base64.b64decode(shot['data']))
                ws.evaluate("document.querySelector('#scenario').value='DEMO-05';document.querySelector('#scenario').dispatchEvent(new Event('change'));document.querySelector('#identity').value='1';document.querySelector('#identity').dispatchEvent(new Event('change'));location.hash='ticket/1'")
                ws.call('Emulation.setDeviceMetricsOverride', {'width': 390, 'height': 844, 'deviceScaleFactor': 1, 'mobile': True})
                time.sleep(.2)
                result['mobile'] = ws.evaluate("({width:innerWidth,document_width:document.documentElement.scrollWidth,internal_blocks:document.querySelectorAll('[data-internal]').length,unlabelled_fields:[...document.querySelectorAll('input,select,textarea')].filter(e=>!e.labels?.length).length})")
                shot = ws.call('Page.captureScreenshot', {'format': 'png', 'captureBeyondViewport': True})
                prefix.with_name(prefix.name + '-customer-mobile.png').write_bytes(base64.b64decode(shot['data']))
                ws.evaluate("document.querySelector('#identity').focus()")
                ws.call('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': 'Tab', 'code': 'Tab', 'windowsVirtualKeyCode': 9})
                ws.call('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': 'Tab', 'code': 'Tab', 'windowsVirtualKeyCode': 9})
                result['keyboard'] = ws.evaluate("({active_id:document.activeElement.id,focus_visible:document.activeElement.matches(':focus-visible')})")
                # Native summary keyboard activation, using real CDP key input.
                ws.evaluate("document.querySelector('.controls summary').focus()")
                before = ws.evaluate("localStorage.getItem('ba-ticketing.prototype.v1')")
                for key, code, vk in [('Enter', 'Enter', 13), (' ', 'Space', 32)]:
                    for kind in ['keyDown', 'keyUp']:
                        params = {'type':kind,'key':key,'code':code,'windowsVirtualKeyCode':vk}
                        if kind == 'keyDown':
                            params['text'] = '\r' if vk == 13 else ' '
                        ws.call('Input.dispatchKeyEvent', params)
                    time.sleep(.1)
                    if vk == 13:
                        collapsed = ws.evaluate("!document.querySelector('.controls').open")
                result['collapse_keyboard'] = {'enter_collapsed':collapsed,'space_expanded':ws.evaluate("document.querySelector('.controls').open"),'source_unchanged':before == ws.evaluate("localStorage.getItem('ba-ticketing.prototype.v1')")}
                ws.evaluate("document.querySelector('#identity').value='6';document.querySelector('#identity').dispatchEvent(new Event('change'))")
                time.sleep(.2)
                ws.evaluate("document.querySelector('[data-jump=manager-load]').focus()")
                for kind in ['keyDown','keyUp']:
                    params = {'type':kind,'key':'Enter','code':'Enter','windowsVirtualKeyCode':13}
                    if kind == 'keyDown':
                        params['text'] = '\r'
                    ws.call('Input.dispatchKeyEvent', params)
                result['jump_keyboard'] = ws.evaluate("({heading:document.activeElement.id,focus_visible:document.activeElement.matches(':focus-visible')})")
                result['manager_mobile'] = ws.evaluate("({width:innerWidth,document_width:document.documentElement.scrollWidth,table_regions:[...document.querySelectorAll('.table-wrap')].map(e=>({width:e.clientWidth,scroll_width:e.scrollWidth})),unlabelled_fields:[...document.querySelectorAll('input,select,textarea')].filter(e=>!e.labels?.length).length})")
                result['ux_browser_passed'] = (all(result['collapse_keyboard'].values()) and result['jump_keyboard']['heading']=='manager-load' and result['jump_keyboard']['focus_visible'] and result['mobile']['document_width']==390 and result['manager_mobile']['document_width']==390 and not result['mobile']['internal_blocks'] and not result['mobile']['unlabelled_fields'] and not result['manager_mobile']['unlabelled_fields'] and result['keyboard']['focus_visible'])
                result['network_requests'] = [e['params']['request']['url'] for e in ws.events if e.get('method') == 'Network.requestWillBeSent']
                result['runtime_errors'] = [e['params'] for e in ws.events if e.get('method') == 'Runtime.exceptionThrown']
                result['server_requests'] = requests
                result['no_api_calls'] = not any('/tickets' in u or '/reports/' in u or ':8000' in u for u in result['network_requests'])
                ws.sock.close()
            except Exception as e:
                result['runner_error'] = str(e)
                if 'ws' in locals():
                    result['cdp_events_on_error'] = ws.events
                result['server_requests'] = requests
                print(str(e))
            finally:
                proc.terminate()
                proc.wait(timeout=15)
                server.shutdown()
    prefix.with_suffix('.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Evidence:', prefix.with_suffix('.json'))
    return int(bool(result.get('runner_error') or result.get('harness', {}).get('failed') or result.get('runtime_errors') or not result.get('ux_browser_passed')))


if __name__ == '__main__':
    raise SystemExit(main())
