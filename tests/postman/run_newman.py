"""Launch an owned backend on a new DB, then invoke the real Newman CLI.

Python orchestrates processes/records only; HTTP assertions are Postman scripts.
"""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[2]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')
    prefix = ROOT / 'tests/evidence' / ('newman-' + stamp)
    work = ROOT / '.postman-runs' / stamp
    work.mkdir(parents=True, exist_ok=False)
    db = work / 'ticketing.sqlite3'
    assert not db.exists()
    tools = json.loads((ROOT / '.postman-tools/tool-paths.json').read_text(encoding='utf8'))
    node, cli = tools['node'], tools['newman']
    collection = 'api/ticketing-sla.postman_collection.json'
    environment = 'api/ticketing-sla.postman_environment.json'
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    base_url = f'http://127.0.0.1:{port}'
    env = os.environ.copy()
    env['TICKETING_DB'] = str(db)
    paths = [p for d in ['backend','sql'] for p in (ROOT / d).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    paths += [ROOT / n for n in ['requirements.txt','api/openapi.json','docs/04-data-api/api-contract.md','docs/spec/business-rules.md','docs/spec/codes.md','tests/sla/sla-scenarios.json',collection,environment,'tests/postman/build_collection.py','tests/postman/run_newman.py']]
    record = {'started_utc': datetime.now(timezone.utc).isoformat(),
              'base_commit': subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
              'source_sha256': {str(p.relative_to(ROOT)).replace('\\','/'):digest(p) for p in paths},
              'database':str(db.relative_to(ROOT)).replace('\\','/'),
              'database_existed_before_start':False, 'base_url':base_url,
              'python_version':sys.version.split()[0],
              'node_version':subprocess.check_output([node,'--version'],text=True).strip(),
              'newman_version':subprocess.check_output([node,cli,'--version'],text=True).strip(),
              'server_command':[str(Path(sys.executable).relative_to(ROOT)) if Path(sys.executable).is_relative_to(ROOT) else 'python','-m','uvicorn','backend.app:app','--host','127.0.0.1','--port',str(port)],
              'server_environment':{'TICKETING_DB':str(db.relative_to(ROOT)).replace('\\','/')},
              'limitations':['Sequential HTTP run does not prove races.', 'Real server clock; no injected clock, DB timestamp changes or long waits.', 'Calendar/deadline/83-fixture/race evidence remains separate pytest evidence.', 'Do not add Newman assertions to pytest test count.']}
    json_path = prefix.with_suffix('.json')
    junit_path = prefix.with_suffix('.xml')
    stdout_path = prefix.with_name(prefix.name + '-stdout.txt')
    command = [node,cli,'run',collection,'-e',environment,'--env-var','base_url='+base_url,
               '--bail','failure','--timeout-request','10000','--reporters','cli,json,junit',
               '--reporter-json-export',str(json_path), '--reporter-junit-export',str(junit_path), '--color','off']
    record['newman_command'] = [str(Path(value).relative_to(ROOT)).replace('\\','/') if value.startswith(str(ROOT)) else value for value in command]
    record['runner'] = 'Newman CLI, not Python HTTP assertions'
    record['reports'] = [str(p.relative_to(ROOT)).replace('\\','/') for p in [json_path,junit_path,stdout_path]]
    proc = None
    try:
        with (work / 'server.log').open('w',encoding='utf8') as log:
            proc = subprocess.Popen([sys.executable,'-m','uvicorn','backend.app:app','--host','127.0.0.1','--port',str(port)],cwd=ROOT,env=env,stdout=log,stderr=log,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            record['owned_server_pid'] = proc.pid
            for _ in range(100):
                if proc.poll() is not None:
                    raise RuntimeError('Owned backend exited before readiness; retained server.log')
                try:
                    with urllib.request.urlopen(base_url+'/openapi.json',timeout=1) as response:
                        live = json.load(response)
                    break
                except OSError:
                    time.sleep(.1)
            else:
                raise RuntimeError('Backend readiness timed out')
            record['live_openapi_matches_tracked'] = live == json.loads((ROOT/'api/openapi.json').read_text(encoding='utf8'))
            if not record['live_openapi_matches_tracked']:
                raise RuntimeError('Live OpenAPI differs from tracked contract')
            if proc.poll() is not None or not db.exists():
                raise RuntimeError('Owned server/database readiness failed')
            with stdout_path.open('w',encoding='utf8') as output:
                result = subprocess.run(command,cwd=ROOT,stdout=output,stderr=subprocess.STDOUT,timeout=300)
            record['exit_code'] = result.returncode
            if json_path.exists():
                report = json.loads(json_path.read_text(encoding='utf8'))
                record['stats'] = report['run']['stats']
                record['timings'] = report['run']['timings']
                record['failures'] = [{k:v for k,v in failure.items() if k in ['error','at','source','parent']} for failure in report['run']['failures']]
            else:
                raise RuntimeError('Newman did not produce JSON report')
    except Exception as error:
        record['orchestration_error'] = str(error)
    finally:
        if proc:
            if proc.poll() is None:
                proc.terminate()
                proc.wait(timeout=15)
            record['owned_server_stopped'] = proc.poll() is not None
            record['server_exit_code'] = proc.returncode
        record['finished_utc'] = datetime.now(timezone.utc).isoformat()
        record['database_retained'] = db.exists()
        if db.exists():
            record['database_sha256_after_stop'] = digest(db)
        record['passed'] = record.get('exit_code') == 0 and not record.get('orchestration_error') and not record.get('failures') and record.get('owned_server_stopped') is True
        prefix.with_name(prefix.name+'-run.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({k:record.get(k) for k in ['passed','exit_code','orchestration_error','stats','owned_server_stopped','database']},indent=2))
    print('Evidence prefix:',prefix.name)
    return int(not record['passed'])


if __name__ == '__main__':
    raise SystemExit(main())
