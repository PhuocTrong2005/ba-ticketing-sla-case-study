"""Acceptance orchestration against an independently cloned origin/main.

Uses only the clean checkout's venv, source and documented runners. No copying
old environments, databases, caches or repository configuration. Evidence is
written in the original workspace under new names; clean run artifacts retained.
"""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import socket
import subprocess
import tempfile
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
CHECKOUT = ROOT / '.clean-start-portfolio-20261013'
STATE = ROOT / 'tests/evidence/portfolio-clean-start-20261013-run.json'
STABLE = Path(os.environ['LOCALAPPDATA']) / 'Programs/Python/Python312/python.exe'
PYTHON = CHECKOUT / '.venv/Scripts/python.exe'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(record):
    STATE.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')


def command(record, name, args, timeout=600):
    path = ROOT / f'tests/evidence/portfolio-clean-start-20261013-{name}.txt'
    assert not path.exists(), 'Evidence name already exists'
    env=os.environ.copy()
    env.pop('TICKETING_DB',None)
    env.pop('PYTHONPATH',None)
    # Independent empty cache for this checkout, not the original repo cache.
    env['PIP_CACHE_DIR']=str(CHECKOUT/'.acceptance-pip-cache')
    started=datetime.now(timezone.utc).isoformat()
    with path.open('w',encoding='utf8') as output:
        result=subprocess.run([str(a) for a in args],cwd=CHECKOUT,env=env,stdout=output,stderr=subprocess.STDOUT,timeout=timeout)
    display=[str(a).replace(str(CHECKOUT),'<fresh-checkout>').replace(str(STABLE),'<stable-python-3.12>') for a in args]
    record['commands'].append({'name':name,'command':display,'cwd':'fresh checkout root','started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'exit_code':result.returncode,'output':str(path.relative_to(ROOT)).replace('\\','/')})
    save(record)
    print(name,'exit',result.returncode,flush=True)
    return result.returncode


def prepare():
    assert CHECKOUT.resolve().is_relative_to(ROOT.resolve())
    tracked=subprocess.check_output(['git','ls-files'],cwd=CHECKOUT,text=True).splitlines()
    initial={n:(CHECKOUT/n).exists() for n in ['.venv','.postman-tools','.postman-runs','data/ticketing.sqlite3','Run Project.txt','.pytest_cache']}
    assert not any(initial.values()), initial
    record={'started_utc':datetime.now(timezone.utc).isoformat(),'os':platform.platform(),'checkout':str(CHECKOUT.relative_to(ROOT)),
            'clone_command':['git','clone','--branch','main','--single-branch','https://github.com/PhuocTrong2005/ba-ticketing-sla-case-study.git',str(CHECKOUT.relative_to(ROOT))],
            'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=CHECKOUT,text=True).strip(),'remote':subprocess.check_output(['git','remote','get-url','origin'],cwd=CHECKOUT,text=True).strip(),
            'initial_git_status':subprocess.check_output(['git','status','--short'],cwd=CHECKOUT,text=True),
            'initial_ignored_state':initial,'source_sha256':{n:digest(CHECKOUT/n) for n in tracked},'commands':[],
            'isolation':'Fresh remote clone and fresh venv/cache/tooling/database/browser profiles; no files copied from original repo into checkout.',
            'documentation_observations':[], 'servers':[]}
    assert not STATE.exists()
    record['stable_python_version']=subprocess.check_output([str(STABLE),'--version'],text=True).strip()
    save(record)
    if command(record,'create-venv',[STABLE,'-m','venv','.venv']):return 1
    record['venv_config']=(CHECKOUT/'.venv/pyvenv.cfg').read_text().replace(str(STABLE.parent),'<stable-python-directory>').replace(str(CHECKOUT),'<fresh-checkout>')
    record['new_python_version']=subprocess.check_output([str(PYTHON),'--version'],text=True).strip()
    save(record)
    if command(record,'pip-install',[PYTHON,'-m','pip','install','-r','requirements.txt']):return 1
    if command(record,'pip-check',[PYTHON,'-m','pip','check']):return 1
    command(record,'pip-freeze',[PYTHON,'-m','pip','freeze'])
    return command(record,'pytest',[PYTHON,'-m','pytest','--junitxml=tests/evidence/portfolio-clean-start-20261013-junit.xml'])


def server(record, name, args, url, inspect):
    env=os.environ.copy();env.pop('TICKETING_DB',None);env.pop('PYTHONPATH',None)
    log=ROOT/f'tests/evidence/portfolio-clean-start-20261013-{name}-server.txt'
    assert not log.exists()
    with log.open('w',encoding='utf8') as output:
        proc=subprocess.Popen([str(a) for a in args],cwd=CHECKOUT,env=env,stdout=output,stderr=output,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        entry={'name':name,'pid':proc.pid,'command':[str(a).replace(str(CHECKOUT),'<fresh-checkout>') for a in args],'url':url,'log':str(log.relative_to(ROOT)).replace('\\','/')}
        record['servers'].append(entry);save(record)
        try:
            for _ in range(100):
                if proc.poll() is not None:raise RuntimeError(name+' exited before readiness')
                try:
                    with urllib.request.urlopen(url,timeout=1) as response:
                        content=response.read();entry['http_status']=response.status
                    break
                except OSError:time.sleep(.1)
            else:raise RuntimeError(name+' readiness timed out')
            inspect(content)
            entry['checks_completed']=True
        except Exception as error:
            entry['error']=str(error)
            raise
        finally:
            if proc.poll() is None:proc.terminate();proc.wait(timeout=15)
            entry['stopped']=proc.poll() is not None;entry['process_exit_code']=proc.returncode;save(record)


def backend(record):
    def inspect(content):
        with urllib.request.urlopen('http://127.0.0.1:8000/openapi.json',timeout=10) as response:
            live=json.load(response)
        record['backend_http']={'docs_http':200,'docs_has_swagger_ui':b'swagger-ui' in content,'openapi_http':200,'openapi_matches_tracked':live==json.loads((CHECKOUT/'api/openapi.json').read_text(encoding='utf8')),'routes':list(live['paths'])}
        save(record)
        assert record['backend_http']['docs_has_swagger_ui'] and record['backend_http']['openapi_matches_tracked']
    server(record,'backend',[PYTHON,'-m','uvicorn','backend.app:app','--host','127.0.0.1','--port','8000'],'http://127.0.0.1:8000/docs',inspect)


def prototype_smoke(record):
    # CDP transport is imported from the clean clone's documented runner.
    spec=importlib.util.spec_from_file_location('clean_cdp',CHECKOUT/'tests/prototype/run_browser.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    checks=[];shots=[]
    with tempfile.TemporaryDirectory(prefix='clean-portfolio-browser-') as profile:
        with (ROOT/'tests/evidence/portfolio-clean-start-20261013-browser.txt').open('w',encoding='utf8') as output:
            proc=subprocess.Popen([str(module.EDGE),'--headless=new','--disable-gpu','--no-sandbox','--no-first-run','--no-default-browser-check','--remote-allow-origins=*',f'--remote-debugging-port={port}',f'--user-data-dir={profile}','about:blank'],stdout=output,stderr=output,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            ws=None
            try:
                for _ in range(100):
                    try:
                        targets=json.load(urllib.request.urlopen(f'http://127.0.0.1:{port}/json',timeout=1))
                        if targets:break
                    except OSError:time.sleep(.1)
                ws=module.WebSocket(next(t['webSocketDebuggerUrl'] for t in targets if t['type']=='page'))
                for domain in ['Network','Runtime','Page']:ws.call(domain+'.enable')
                ws.call('Page.navigate',{'url':'http://127.0.0.1:8765/prototype/'})
                for _ in range(100):
                    if ws.evaluate("!!document.querySelector('#main')?.children.length"):break
                    time.sleep(.1)
                def ev(js):return ws.evaluate(js)
                def check(name, value):
                    checks.append({'name':name,'passed':bool(value)});assert value,name
                def change(sel,value):
                    ev(f"(()=>{{let e=document.querySelector({json.dumps(sel)});e.value={json.dumps(str(value))};e.dispatchEvent(new Event('change'));}})()");time.sleep(.1)
                def click(sel):ev(f"document.querySelector({json.dumps(sel)}).click()");time.sleep(.1)
                def form(sel,values):
                    ev(f"(()=>{{let f=document.querySelector({json.dumps(sel)});for(let [k,v] of Object.entries({json.dumps(values)}))f.elements[k].value=v;f.requestSubmit();}})()");time.sleep(.1)
                    check('UI form accepted '+sel,ev("!document.querySelector('#feedback').classList.contains('error')"))
                def clock(h):form('#clock-form',{'clock-target':'2026-10-05T'+h})
                def go():ev("location.hash='ticket/1'");time.sleep(.1)
                def shot(name):
                    p=ROOT/f'tests/evidence/portfolio-clean-start-20261013-{name}.png';assert not p.exists()
                    p.write_bytes(base64.b64decode(ws.call('Page.captureScreenshot',{'format':'png','captureBeyondViewport':True})['data']));shots.append(str(p.relative_to(ROOT)).replace('\\','/'))
                check('documented prototype URL',ev('location.href')=='http://127.0.0.1:8765/prototype/')
                check('browser storage initially fresh',ev("document.querySelector('#scenario').value")=='DEMO-01')
                form('[data-action=create]',{'title':'CLEAN-START DEMO-01','description':'Documented fresh checkout workflow','priority':'HIGH'})
                clock('09:05:00');change('#identity',3);click('[data-claim="1"]')
                clock('09:10:00');form('[data-action=message]',{'content':'Clean-start public reply'})
                clock('09:30:00');form('[data-action=resolve]',{'resolution_summary':'Clean-start public result'})
                clock('09:35:00');change('#identity',1);go();click('[data-confirm="1"]')
                check('DEMO01 Closed',ev("document.querySelector('#main').textContent.includes('Closed')"))
                check('Customer privacy',ev("document.querySelectorAll('[data-internal]').length")==0);shot('customer-closed')
                saved=ev("localStorage.getItem('ba-ticketing.prototype.v1')");ws.call('Page.reload');time.sleep(.6)
                check('localStorage survives reload',saved==ev("localStorage.getItem('ba-ticketing.prototype.v1')"))
                click('#reset');check('reset restores sample',ev("document.querySelector('#main').textContent.includes('Tạo ticket')"))
                change('#scenario','DEMO-04');change('#identity',3);go()
                check('review blocks Resolved',ev("document.querySelector('[data-action=resolve] button').disabled"))
                clock('11:30:00');click('[data-waiting="1"]');clock('12:00:00');change('#identity',6);go()
                form('[data-action=review]',{'unresolved_reason':'Clean-start cause','next_action':'Clean-start recorded plan','expert_note':'Record only'})
                check('Manager plan keeps Waiting',ev("document.querySelector('#main').textContent.includes('Waiting for Customer')"));shot('manager-plan')
                change('#identity',1);go();clock('12:30:00');form('[data-action=message]',{'content':'Clean-start resume'})
                change('#identity',3);go();check('Customer resumes IP',ev("document.querySelector('[data-action=resolve] button')?.disabled===false"))
                click('.controls summary');check('controls collapse',ev("!document.querySelector('.controls').open"))
                runtime=[e for e in ws.events if e.get('method')=='Runtime.exceptionThrown']
                requests=[e['params']['request']['url'] for e in ws.events if e.get('method')=='Network.requestWillBeSent']
                check('no JavaScript errors',not runtime);check('no API requests',not any('/tickets' in u or '/reports/' in u or ':8000' in u for u in requests))
                record['prototype_documented_static_smoke']={'checks':checks,'runtime_errors':runtime,'network_requests':requests,'screenshots':shots,'scope':'Local documented URL smoke; not Pages retest or full six-group workflow.'}
            finally:
                if ws:ws.sock.close()
                proc.terminate();proc.wait(timeout=15)
                record['owned_browser_stopped']=proc.poll() is not None;save(record)


def exercise():
    record=json.loads(STATE.read_text(encoding='utf8'))
    try:
        backend(record)
        server(record,'prototype-static',[PYTHON,'-m','http.server','8765','--bind','127.0.0.1'],'http://127.0.0.1:8765/prototype/',lambda content:prototype_smoke(record))
        if command(record,'prototype-suite',[PYTHON,'tests/prototype/run_browser.py']):return 1
        # This auditor is explicitly mentioned by the published prototype README.
        command(record,'prototype-audit-as-published',[PYTHON,'tests/prototype/audit_ux.py'])
        if command(record,'newman-tools-setup',[PYTHON,'tests/postman/setup_tools.py']):return 1
        if command(record,'newman-run',[PYTHON,'tests/postman/run_newman.py']):return 1
        return 0
    except Exception as error:
        record['exercise_error']=str(error);save(record);print(str(error),flush=True);return 1
    finally:
        record['finished_utc']=datetime.now(timezone.utc).isoformat()
        record['checkout_git_status']=subprocess.check_output(['git','status','--short'],cwd=CHECKOUT,text=True)
        record['changed_tracked_source']=[n for n,h in record['source_sha256'].items() if digest(CHECKOUT/n)!=h]
        save(record)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['prepare','exercise']);args=parser.parse_args()
    raise SystemExit(prepare() if args.phase=='prepare' else exercise())
