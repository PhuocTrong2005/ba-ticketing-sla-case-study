"""Read-only preservation and collection/run audit; emits new evidence only."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import socket
import sqlite3
import subprocess
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    baseline = json.loads((ROOT/'tests/evidence/postman-baseline-20261013.json').read_text(encoding='utf8'))
    changed = [n for n,h in baseline['files'].items() if not (ROOT/n).exists() or digest(ROOT/n)!=h]
    databases = [n for n,h in baseline['existing_databases'].items() if not (ROOT/n).exists() or digest(ROOT/n)!=h]
    run_path = sorted((ROOT/'tests/evidence').glob('newman-*-run.json'))[-1]
    run = json.loads(run_path.read_text(encoding='utf8'))
    mismatch = [n for n,h in run['source_sha256'].items() if digest(ROOT/n)!=h]
    collection = json.loads((ROOT/'api/ticketing-sla.postman_collection.json').read_text(encoding='utf8'))
    environment = json.loads((ROOT/'api/ticketing-sla.postman_environment.json').read_text(encoding='utf8'))
    requests = [r for group in collection['item'] for r in group['item']]
    names = [r['name'] for r in requests]
    reserved = {'timestamp','actor','actor_id','assignee','assignee_id','event_id','created_at','occurred_at','at','status'}
    payload_violations = []
    hardcoded_ids = []

    def inspect(value, name):
        if isinstance(value,dict):
            for key,item in value.items():
                if key in reserved:
                    payload_violations.append({'request':name,'field':key})
                inspect(item,name)
        elif isinstance(value,list):
            for item in value:
                inspect(item,name)

    for item in requests:
        request = item['request']
        if re.search(r'/tickets/\d+(?:/|\?|$)',request['url']):
            hardcoded_ids.append(item['name'])
        if 'body' in request:
            try:
                inspect(json.loads(request['body']['raw']),item['name'])
            except json.JSONDecodeError:
                if not item['name'].startswith('PM-224 '):
                    payload_violations.append({'request':item['name'],'field':'unexpected malformed JSON'})
    env = {v['key']:v['value'] for v in environment['values']}
    correct_identities = all(env[k]==str(v) for k,v in {'customer_1':1,'customer_2':2,'agent_3':3,'agent_4':4,'agent_5':5,'manager_6':6}.items())
    text = (ROOT/'api/ticketing-sla.postman_collection.json').read_text(encoding='utf8')+(ROOT/'api/ticketing-sla.postman_environment.json').read_text(encoding='utf8')
    # A drive prefix must start at a boundary; do not match the s:/ in https://.
    sensitive = bool(re.search(r'github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|-----BEGIN .*PRIVATE KEY-----|(?<![A-Za-z])[A-Za-z]:[\\/]|/Users/',text))
    report = json.loads((ROOT/run['reports'][0]).read_text(encoding='utf8'))
    executed = [e['item']['name'] for e in report['run']['executions']]
    executed_match = names==executed
    nonlocal_requests = [e['item']['name'] for e in report['run']['executions'] if e['request']['url'].get('protocol')!='http' or e['request']['url'].get('host')!=['127','0','0','1'] or str(e['request']['url'].get('port'))!=run['base_url'].rsplit(':',1)[1]]
    broken,links = [],0
    docs = ['api/README.md','TASKS.md','docs/decision-log.md','docs/traceability.md','tests/evidence/postman-report-20261013.md']
    for name in docs:
        path=ROOT/name
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',path.read_text(encoding='utf8')):
            if re.match(r'(?:https?://|mailto:|#)',target):
                continue
            target=unquote(target.split('#')[0].strip('<>'))
            links+=1
            if target and not (path.parent/target).exists():
                broken.append({'file':name,'target':target})
    diff=subprocess.run(['git','diff','--check'],cwd=ROOT,capture_output=True,text=True)
    current_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    staged=subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT,text=True).splitlines()
    source_files=[ROOT/n for n in docs]+list((ROOT/'tests/postman').glob('*.py'))+list((ROOT/'api').glob('*.postman_*.json'))
    whitespace=[str(p.relative_to(ROOT)).replace('\\','/') for p in source_files if any(line.rstrip()!=line for line in p.read_text(encoding='utf8').splitlines())]
    db=(ROOT/run['database']).resolve()
    assert db.is_relative_to((ROOT/'.postman-runs').resolve())
    with sqlite3.connect(db.as_uri()+'?mode=ro',uri=True) as connection:
        data={'tickets':connection.execute('SELECT count(*) FROM tickets').fetchone()[0],
              'states':dict(connection.execute('SELECT status,count(*) FROM tickets GROUP BY status').fetchall()),
              'reviews':connection.execute('SELECT count(*) FROM ticket_reviews').fetchone()[0],
              'events':connection.execute('SELECT count(*) FROM ticket_events').fetchone()[0]}
    port=int(run['base_url'].rsplit(':',1)[1])
    with socket.socket() as sock:
        sock.settimeout(.5)
        port_closed=sock.connect_ex(('127.0.0.1',port))!=0
    result={'run_record':str(run_path.relative_to(ROOT)).replace('\\','/'),
            'protected_files':len(baseline['files']),
            'old_evidence_preserved_count':sum(n.startswith('tests/evidence/') for n in baseline['files']) if not changed else None,
            'changed_or_deleted_protected':changed,'existing_database_changes':databases,
            'current_source_hash_mismatches':mismatch,
            'collection_requests':len(requests),'unique_request_names':len(set(names))==len(names),
            'newman_execution_order_matches_collection':executed_match,
            'nonlocal_newman_requests':nonlocal_requests,
            'payload_reserved_field_violations':payload_violations,'hardcoded_ticket_id_requests':hardcoded_ids,
            'identity_environment_correct':correct_identities,'secret_or_private_path_pattern_hits':sensitive,
            'live_openapi_matches_tracked':run['live_openapi_matches_tracked'],
            'requests':run['stats']['requests'],'assertions':run['stats']['assertions'],
            'runner_exit_code':run['exit_code'],'runner':'Newman CLI',
            'database_readonly_summary':data,'owned_server_stopped':run['owned_server_stopped'],
            'owned_port_closed_after_run':port_closed,'local_links_checked':links,'broken_links':broken,
            'git_diff_check_exit_code':diff.returncode,'trailing_whitespace_source_files':whitespace,
            'head_unchanged_no_commit':current_head==baseline['head'],'staged_files':staged,
            'fixture_sha256':digest(ROOT/'tests/sla/sla-scenarios.json'),
            'backend_pytest_rerun':False,'limitations':'Sequential Newman HTTP; no race/calendar/deadline/fixture calculation claims. No Postman UI runner.'}
    result['passed']=not any([changed,databases,mismatch,payload_violations,hardcoded_ids,sensitive,nonlocal_requests,broken,diff.returncode,whitespace,staged]) and correct_identities and executed_match and len(set(names))==len(names) and result['head_unchanged_no_commit'] and run['passed'] and port_closed and len(requests)==191 and run['stats']['assertions']['total']==514
    dest=ROOT/('tests/evidence/postman-audit-'+datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')+'.json')
    dest.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    print(dest)
    return int(not result['passed'])


if __name__ == '__main__':
    raise SystemExit(main())
