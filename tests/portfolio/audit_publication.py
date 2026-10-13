"""Review evidence counts, source match, AC links and staged publication hygiene.

Read-only with respect to application/tests; writes a new audit record.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
import urllib.request
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(name):
    return json.loads((ROOT/name).read_text(encoding='utf8'))


def junit(name):
    root=ET.parse(ROOT/name)
    return {'cases':len(root.findall('.//testcase')), 'failures':len(root.findall('.//failure')), 'errors':len(root.findall('.//error')), 'skipped':len(root.findall('.//skipped')), 'names':[c.get('name') for c in root.findall('.//testcase')]}


def main():
    baseline=read('tests/evidence/portfolio-baseline-20261013.json')
    changed=[n for n,h in baseline['files'].items() if not (ROOT/n).exists() or digest(ROOT/n)!=h]
    unexpected=[n for n in changed if n!='api/README.md']
    windows=read('tests/evidence/step1-windows-20261012-162259-run.json')
    backend_files=[x for x in windows['source_manifest'] if x['path'].startswith(('backend/','tests/backend/','sql/queries/')) or x['path'] in ['requirements.txt','pytest.ini','api/openapi.json']]
    backend_mismatch=[x['path'] for x in backend_files if digest(ROOT/x['path'])!=x['sha256']]
    prototype=read('tests/evidence/prototype-ux-20261013-002503.json')
    core=[n for n in prototype['source_sha256'] if n.startswith('prototype/') or n in ['tests/prototype/test.js','tests/prototype/index.html','tests/prototype/run_browser.py']]
    proto_mismatch=[n for n in core if digest(ROOT/n)!=prototype['source_sha256'][n]]
    pages=read('tests/evidence/pages-public-smoke-20261013-002741.json')
    page_mismatch=[x['file'] for x in pages['assets'] if digest(ROOT/'prototype'/x['file'])!=x['sha256']]
    newman=read('tests/evidence/newman-20261013-004259-750031-run.json')
    newman_mismatch=[n for n,h in newman['source_sha256'].items() if digest(ROOT/n)!=h]
    raw=read('tests/evidence/newman-20261013-004259-750031.json')
    bj=junit('tests/evidence/step1-windows-20261012-162259-repo-junit.xml')
    clean=junit('tests/evidence/step1-windows-20261012-162259-clean-junit.xml')
    nj=junit('tests/evidence/newman-20261013-004259-750031.xml')
    collection=read('api/ticketing-sla.postman_collection.json')
    env=read('api/ticketing-sla.postman_environment.json')
    items=[x for group in collection['item'] for x in group['item']]
    executed=[e['item']['name'] for e in raw['run']['executions']]
    order_ok=[x['name'] for x in items]==executed
    tools=read('.postman-tools/tool-paths.json')
    schema_path=ROOT/'.postman-tools/collection-v2.1-schema.json'
    if not schema_path.exists():
        schema_path.write_bytes(urllib.request.urlopen('https://schema.getpostman.com/json/collection/v2.1.0/collection.json',timeout=30).read())
    schema_result=subprocess.run([tools['node'],'tests/portfolio/validate_collection.cjs'],cwd=ROOT,capture_output=True,text=True)
    schema=json.loads(schema_result.stdout) if schema_result.stdout else {'valid':False,'error':schema_result.stderr}
    docs=['README.md','TASKS.md','api/README.md','docs/decision-log.md','docs/traceability.md','docs/ac-traceability.md','docs/release-checklist.md','docs/backend-running.md','tests/evidence/README.md','tests/evidence/portfolio-publication-report-20261013.md']
    broken=[];link_count=0
    for name in docs:
        path=ROOT/name;text=path.read_text(encoding='utf8')
        targets=re.findall(r'\[[^\]]*\]\(([^)]+)\)',text)+re.findall(r'^\[[^\]]+\]:\s*(\S+)',text,re.M)+re.findall(r'<img[^>]+src="([^"]+)"',text)
        for target in targets:
            if re.match(r'(?:https?://|mailto:|#)',target):continue
            target=unquote(target.split('#')[0].strip('<>'));link_count+=1
            if target and not (path.parent/target).exists():broken.append({'file':name,'target':target})
    matrix=(ROOT/'docs/ac-traceability.md').read_text(encoding='utf8')
    ac_rows=re.findall(r'^\| (AC-\d+) \|',matrix,re.M)
    ac_expected=re.findall(r'^- (AC-\d+):',(ROOT/'docs/03-requirements/user-stories-draft.md').read_text(encoding='utf8'),re.M)
    tests=set(re.findall(r'`(test_[a-z_]+)(?:\[|`)',matrix))
    missing_tests=[n for n in tests if not any(name==n or name.startswith(n+'[') for name in bj['names'])]
    quoted=re.findall(r'\x60([^\x60]+)\x60',matrix)
    p_names={r['name'] for r in prototype['harness']['results']}
    missing_proto=[n for n in quoted if n.startswith(('UI-','UX-','DEMO-','Warnings ','SLA-83 ')) and n not in p_names]
    request_ids=set(re.findall(r'PM-\d+[a-z]?',matrix))
    present_ids={re.match(r'PM-\d+[a-z]?',name).group() for name in executed}
    missing_requests=sorted(request_ids-present_ids)
    staged=subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT,text=True).splitlines()
    forbidden=[n for n in staged if n=='Run Project.txt' or re.search(r'(?:^|/)(?:\.venv[^/]*|\.postman-tools|\.postman-runs|node_modules|__pycache__|data)(?:/|$)|\.(?:db|sqlite3|pyc|log)$',n)]
    pattern=re.compile(rb'github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')
    secret_hits=[n for n in staged if (ROOT/n).is_file() and pattern.search((ROOT/n).read_bytes())]
    private_pattern=re.compile(rb'(?<![A-Za-z])[A-Za-z]:[\\/]Users[\\/][A-Za-z0-9_.-]+|/(?:home|Users)/[A-Za-z0-9_.-]+|Bearer [A-Za-z0-9._-]{15,}')
    private_hits=[n for n in staged if (ROOT/n).is_file() and private_pattern.search((ROOT/n).read_bytes())]
    byte_scope=[n for n in staged if n.startswith(('api/ticketing-sla.postman_','tests/postman/','tests/evidence/newman-','tests/evidence/postman-','tests/evidence/portfolio-','tests/portfolio/'))]
    byte_mismatch=[n for n in byte_scope if subprocess.check_output(['git','show',':'+n],cwd=ROOT)!=(ROOT/n).read_bytes()]
    diffs=[subprocess.run(['git','diff']+mode+['--check'],cwd=ROOT,capture_output=True,text=True).returncode for mode in [[],['--cached']]]
    identities={v['key']:v['value'] for v in env['values']}
    env_ok=all(identities[k]==str(v) for k,v in {'customer_1':1,'customer_2':2,'agent_3':3,'agent_4':4,'agent_5':5,'manager_6':6}.items())
    count_ok=all(j['cases']==181 and not(j['failures'] or j['errors'] or j['skipped']) for j in [bj,clean]) and nj['cases']==514 and not(nj['failures'] or nj['errors'] or nj['skipped']) and prototype['harness']['passed']==110 and prototype['harness']['failed']==0 and len(pages['checks'])==74 and all(x['passed'] for x in pages['checks']) and len(items)==191 and raw['run']['stats']['assertions']['total']==514 and raw['run']['stats']['assertions']['failed']==0 and len(raw['run']['executions'])==191 and not raw['run']['failures'] and newman['exit_code']==0
    result={'baseline':'tests/evidence/portfolio-baseline-20261013.json','protected_files':len(baseline['files']),'old_evidence_preserved':sum(n.startswith('tests/evidence/') for n in baseline['files']) if not unexpected else None,'allowed_changed':changed,'unexpected_changed_or_deleted':unexpected,
            'backend_windows_manifest_files':len(backend_files),'backend_source_mismatches':backend_mismatch,'prototype_core_mismatches':proto_mismatch,'pages_runtime_mismatches':page_mismatch,'newman_source_collection_helper_mismatches':newman_mismatch,
            'evidence_counts':{'backend_repo':{k:v for k,v in bj.items() if k!='names'},'backend_clean':{k:v for k,v in clean.items() if k!='names'},'prototype_cases':110,'pages_smoke_checks':74,'newman_requests':len(executed),'newman_assertions_junit':nj['cases']},'counts_matched':count_ok,'newman_order_matches_collection':order_ok,'collection_schema_validation':schema,'official_schema_sha256':digest(ROOT/'.postman-tools/collection-v2.1-schema.json'),'environment_identities_correct':env_ok,
            'ac_rows':ac_rows,'all_34_ac_exactly_once':set(ac_rows)==set(ac_expected) and len(ac_rows)==len(ac_expected)==34,'missing_backend_test_names':missing_tests,'missing_prototype_test_names':missing_proto,'missing_request_ids':missing_requests,'local_links_images_checked':link_count,'broken_links_images':broken,
            'staged_files':staged,'forbidden_staged':forbidden,'secret_pattern_hits':secret_hits,'private_path_or_bearer_pattern_hits':private_hits,'staged_byte_mismatches':byte_mismatch,'git_diff_check_exit_codes':diffs,
            'newman_rerun':False,'backend_rerun':False,'prototype_rerun':False,'limitations':'Evidence review/schema/source/link checks, not new runtime tests; AC rows retain partial coverage limits, video absent.'}
    result['passed']=not any([unexpected,backend_mismatch,proto_mismatch,page_mismatch,newman_mismatch,missing_tests,missing_proto,missing_requests,broken,forbidden,secret_hits,private_hits,byte_mismatch,*diffs]) and count_ok and order_ok and schema.get('valid') is True and env_ok and result['all_34_ac_exactly_once']
    dest=ROOT/('tests/evidence/portfolio-publication-audit-'+datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')+'.json')
    dest.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['staged_files','ac_rows']},ensure_ascii=False,indent=2));print(dest)
    return int(not result['passed'])


if __name__=='__main__':
    raise SystemExit(main())
