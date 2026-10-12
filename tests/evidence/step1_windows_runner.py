"""Reproduce Step 1 on Windows; retains backup and isolated workspace.

Run with a host Python: python tests/evidence/step1_windows_runner.py STAMP
Requires the separately installed official per-user Python 3.12.
"""
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
STAMP = sys.argv[1]
EVIDENCE = ROOT / 'tests/evidence'
PREFIX = f'step1-windows-{STAMP}'
BASE = Path(os.environ['LOCALAPPDATA']) / 'Programs/Python/Python312/python.exe'
CLEAN = ROOT / f'.clean-start-{STAMP}'
BACKUP = ROOT / f'.venv-backup-{STAMP}'
RESULT = {'stamp': STAMP, 'os': platform.platform(), 'source': str(ROOT),
          'clean_directory': str(CLEAN), 'backup': str(BACKUP), 'commands': [], 'http': []}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save():
    (EVIDENCE / f'{PREFIX}-run.json').write_text(json.dumps(RESULT, indent=2, ensure_ascii=False), encoding='utf-8')

def run(args, cwd, label, env=None):
    log = EVIDENCE / f'{PREFIX}-{label}.log'
    with log.open('w', encoding='utf-8') as output:
        proc = subprocess.run([str(a) for a in args], cwd=cwd, env=env, stdout=output,
                              stderr=subprocess.STDOUT, text=True)
    RESULT['commands'].append({'argv': [str(a) for a in args], 'cwd': str(cwd),
                               'exit_code': proc.returncode, 'log': log.name})
    save()
    print(label, 'exit', proc.returncode, flush=True)
    if proc.returncode:
        raise RuntimeError(f'{label} failed: see {log}')

def metadata(python, cwd):
    code = 'import sys,json;print(json.dumps(dict(executable=sys.executable,version=sys.version,base_prefix=sys.base_prefix,base_executable=sys._base_executable)))'
    return json.loads(subprocess.check_output([str(python), '-c', code], cwd=cwd, text=True))

def request(path, user=None, payload=None, expected=200):
    headers = {'Content-Type': 'application/json'}
    if user is not None:
        headers['X-Demo-User-Id'] = str(user)
    req = urllib.request.Request(URL + path, headers=headers,
          data=json.dumps(payload).encode() if payload is not None else None)
    try:
        response = urllib.request.urlopen(req, timeout=5)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        body = response.read().decode()
        status = response.status
    try:
        parsed = json.loads(body)
    except ValueError:
        parsed = body
    RESULT['http'].append({'method': req.get_method(), 'path': path, 'user': user,
                           'payload': payload, 'status': status, 'response': parsed})
    save()
    assert status == expected, (path, status, body)
    return parsed

def privacy(value):
    forbidden = {'sla', 'warning_level', 'reviews', 'needs_manager_review',
                 'assignment_snapshot', 'rejection_count', 'handling_plan'}
    def walk(item):
        if isinstance(item, dict):
            assert not forbidden.intersection(item), item
            for child in item.values():
                walk(child)
        elif isinstance(item, list):
            for child in item:
                walk(child)
    walk(value)
    assert 'STEP1-PRIVATE-NOTE' not in json.dumps(value)
    assert 'STEP1-PRIVATE-PLAN' not in json.dumps(value)

server = None
try:
    baseline = json.loads((EVIDENCE / f'{PREFIX}-baseline.json').read_text(encoding='utf-8-sig'))
    RESULT['initial_changed_files'] = [s for s in baseline['status'] if '.step1-stamp' not in s]
    fixture = ROOT / 'tests/sla/sla-scenarios.json'
    RESULT['fixture_before'] = digest(fixture)
    rows = json.loads(fixture.read_text(encoding='utf-8-sig'))
    assert len(rows) == 83 and all(r['review_status'] == 'verified' for r in rows)
    RESULT['fixture_count'] = len(rows)
    RESULT['old_environment'] = metadata(ROOT / '.venv/Scripts/python.exe', ROOT)
    RESULT['stable_python'] = metadata(BASE, ROOT)
    assert RESULT['stable_python']['version'].startswith('3.12.')
    assert 'temp' not in str(BASE).lower()
    assert not BACKUP.exists() and not CLEAN.exists()
    # The destination is a checked sibling within the authorized workspace.
    assert BACKUP.resolve().parent == ROOT.resolve()
    (ROOT / '.venv').rename(BACKUP)
    run([BASE, '-m', 'venv', ROOT / '.venv'], ROOT, 'repo-venv')
    python = ROOT / '.venv/Scripts/python.exe'
    RESULT['repo_environment'] = metadata(python, ROOT)
    env = os.environ.copy()
    env.pop('PYTHONPATH', None)
    env.pop('PYTHONHOME', None)
    env['PYTHONNOUSERSITE'] = '1'
    env['TICKETING_DB'] = str(ROOT / '.venv/step1-import.sqlite3')
    run([python, '-m', 'pip', 'install', '-r', 'requirements.txt'], ROOT, 'repo-install', env)
    run([python, '-m', 'pip', 'check'], ROOT, 'repo-pip-check', env)
    run([python, '-m', 'pip', 'freeze'], ROOT, 'repo-freeze', env)
    junit = EVIDENCE / f'{PREFIX}-repo-junit.xml'
    run([python, '-m', 'pytest', f'--junitxml={junit}'], ROOT, 'repo-pytest', env)
    CLEAN.mkdir()
    files = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard'], cwd=ROOT, text=True).splitlines()
    manifest = []
    roots = {'backend', 'api', 'sql', 'docs', 'tests'}
    root_files = {'AGENTS.md', 'README.md', 'TASKS.md', 'requirements.txt', 'pytest.ini', '.gitignore'}
    extensions = {'.py', '.json', '.sql', '.md', '.txt', '.ini', '.svg', '.png', '.drawio'}
    for name in files:
        rel = Path(name)
        if name not in root_files and (rel.parts[0] not in roots or rel.suffix not in extensions):
            continue
        if name.startswith('tests/evidence/') or any(p.startswith('.') for p in rel.parts[1:]):
            continue
        src = ROOT / rel
        if not src.is_file() or src.is_symlink():
            continue
        dest = CLEAN / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        assert digest(src) == digest(dest)
        manifest.append({'path': name, 'sha256': digest(dest)})
    RESULT['source_manifest'] = manifest
    RESULT['copy_policy'] = 'Allowlisted source/docs/test extensions from current tracked and untracked files; excludes evidence, .git, virtualenvs, caches, databases, env files, credentials and other local data.'
    run([BASE, '-m', 'venv', CLEAN / '.venv'], CLEAN, 'clean-venv')
    clean_python = CLEAN / '.venv/Scripts/python.exe'
    RESULT['clean_environment'] = metadata(clean_python, CLEAN)
    clean_env = env.copy()
    clean_env['TICKETING_DB'] = str(CLEAN / 'data/step1-http.sqlite3')
    run([clean_python, '-m', 'pip', 'install', '-r', 'requirements.txt'], CLEAN, 'clean-install', clean_env)
    run([clean_python, '-m', 'pip', 'check'], CLEAN, 'clean-pip-check', clean_env)
    run([clean_python, '-m', 'pip', 'freeze'], CLEAN, 'clean-freeze', clean_env)
    clean_junit = EVIDENCE / f'{PREFIX}-clean-junit.xml'
    run([clean_python, '-m', 'pytest', f'--junitxml={clean_junit}'], CLEAN, 'clean-pytest', clean_env)
    # Tests import the app and may create an empty default DB; HTTP gets a separate fresh DB.
    clean_env['TICKETING_DB'] = str(CLEAN / 'data/step1-workflow.sqlite3')
    assert not Path(clean_env['TICKETING_DB']).exists()
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    URL = f'http://127.0.0.1:{port}'
    RESULT['server'] = {'url': URL, 'database': clean_env['TICKETING_DB']}
    with (EVIDENCE / f'{PREFIX}-server.log').open('w', encoding='utf-8') as log:
        argv = [str(clean_python), '-m', 'uvicorn', 'backend.app:app', '--host', '127.0.0.1', '--port', str(port)]
        server = subprocess.Popen(argv, cwd=CLEAN, env=clean_env, stdout=log, stderr=subprocess.STDOUT)
        RESULT['server'].update(pid=server.pid, argv=argv, cwd=str(CLEAN))
        for _ in range(100):
            assert server.poll() is None, 'Uvicorn exited before ready'
            try:
                urllib.request.urlopen(URL + '/openapi.json', timeout=1).close()
                break
            except (OSError, urllib.error.URLError):
                time.sleep(0.2)
        else:
            raise RuntimeError('Uvicorn readiness timeout')
        assert 'swagger-ui' in request('/docs')
        assert '/tickets' in request('/openapi.json')['paths']
        ticket = request('/tickets', 1, {'title': 'ENV-STEP1-01 clean-start', 'description': 'Deterministic environment verification workflow', 'priority': 'NORMAL'}, 201)
        privacy(ticket)
        tid = ticket['id']
        assert ticket['status'] == 'NEW'
        assert request(f'/tickets/{tid}/claim', 3, {})['status'] == 'IN_PROGRESS'
        request(f'/tickets/{tid}/notes', 3, {'content': 'STEP1-PRIVATE-NOTE'})
        detail = request(f'/tickets/{tid}', 1)
        privacy(detail)
        internal = request(f'/tickets/{tid}', 3)
        assert 'sla' in internal and 'STEP1-PRIVATE-NOTE' in json.dumps(internal)
        assert request(f'/tickets/{tid}/resolve', 3, {'resolution_summary': 'ENV-STEP1-01 environment and workflow verified'})['status'] == 'RESOLVED'
        closed = request(f'/tickets/{tid}/confirm', 1, {})
        assert closed['status'] == 'CLOSED'
        privacy(closed)
        privacy(request('/tickets', 1))
        privacy(request(f'/tickets/{tid}', 1))
        request(f'/tickets/{tid}/reviews', 1, expected=404)
        # Separate deterministic workflow exercises actual nonempty internal review content.
        review_ticket = request('/tickets', 1, {'title': 'ENV-STEP1-02 review privacy', 'description': 'Three rejected resolutions create an internal review', 'priority': 'NORMAL'}, 201)['id']
        request(f'/tickets/{review_ticket}/claim', 3, {})
        for n in range(3):
            request(f'/tickets/{review_ticket}/resolve', 3, {'resolution_summary': f'ENV-STEP1-02 attempt {n+1}'})
            request(f'/tickets/{review_ticket}/reject', 1, {'reason': f'ENV-STEP1-02 unresolved {n+1}'})
        manager = request(f'/tickets/{review_ticket}/reviews', 6)
        assert len(manager) == 1
        request(f'/tickets/{review_ticket}/reviews/complete', 6, {'handling_plan': {'unresolved_reason': 'ENV-STEP1-02 repeated rejection', 'next_action': 'STEP1-PRIVATE-PLAN', 'needs_expert_input': False}})
        assert 'STEP1-PRIVATE-PLAN' in json.dumps(request(f'/tickets/{review_ticket}', 3))
        privacy(request(f'/tickets/{review_ticket}', 1))
        privacy(request('/tickets', 1))
        request(f'/tickets/{review_ticket}/reviews', 1, expected=404)
        RESULT['http_workflow'] = 'PASS'
        server.terminate()
        server.wait(timeout=15)
        RESULT['server']['stopped_owned_process'] = server.poll() is not None
    RESULT['fixture_after'] = digest(fixture)
    assert RESULT['fixture_after'] == RESULT['fixture_before'] == digest(CLEAN / 'tests/sla/sla-scenarios.json')
    changed = [entry['path'] for entry in baseline['files'] if (ROOT / entry['path']).is_file() and digest(ROOT / entry['path']) != entry['sha256']]
    assert not changed, changed
    RESULT['original_files_byte_preserved_before_doc_updates'] = True
    RESULT['python313_byte_preserved'] = hashlib.sha256(Path('C:/Program Files/Python313/python.exe').read_bytes()).hexdigest().upper() == baseline['python313_hash']
    assert RESULT['python313_byte_preserved']
    for label, path in [('repo', junit), ('clean', clean_junit)]:
        suite = ET.parse(path).getroot().find('testsuite')
        RESULT[f'{label}_pytest'] = dict(suite.attrib)
    RESULT['status'] = 'PASS'
except BaseException as error:
    RESULT['status'] = 'FAIL'
    RESULT['error'] = repr(error)
    raise
finally:
    if server is not None and server.poll() is None:
        server.terminate()
        server.wait(timeout=15)
        RESULT['server']['stopped_owned_process'] = True
    save()
