"""Audit clean clone results and protect original repo; no application mutations."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import platform
import re
import socket
import subprocess
from urllib.parse import unquote,urlsplit
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
CLONE=ROOT/'.clean-start-portfolio-20261013'
ALLOWED={'README.md','TASKS.md','api/README.md','prototype/README.md','docs/decision-log.md','docs/release-checklist.md','docs/backend-running.md','docs/ac-traceability.md','docs/traceability.md'}


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf8'))
def closed(port):
    with socket.socket() as s:
        s.settimeout(.5);return s.connect_ex(('127.0.0.1',port))!=0


def main():
    baseline=read(ROOT/'tests/evidence/portfolio-clean-start-baseline-20261013.json')
    run=read(ROOT/'tests/evidence/portfolio-clean-start-20261013-run.json')
    recheck=read(ROOT/'tests/evidence/portfolio-clean-start-20261013-doc-recheck.json')
    changes=[n for n,h in baseline['files'].items() if sha(ROOT/n)!=h]
    unexpected=[n for n in changes if n not in ALLOWED]
    databases=[n for n,h in baseline['databases'].items() if sha(ROOT/n)!=h]
    older=read(ROOT/'tests/evidence/portfolio-baseline-20261013.json')
    old_logs={n:h for n,h in older['files'].items() if n.startswith('tests/evidence/') and n.endswith('.log')}
    log_changes=[n for n,h in old_logs.items() if not (ROOT/n).exists() or sha(ROOT/n)!=h]
    clone_changes=[n for n,h in run['source_sha256'].items() if sha(CLONE/n)!=h]
    tree=ET.parse(ROOT/'tests/evidence/portfolio-clean-start-20261013-junit.xml')
    pytest={'cases':len(tree.findall('.//testcase')),'failures':len(tree.findall('.//failure')),'errors':len(tree.findall('.//error')),'skipped':len(tree.findall('.//skipped'))}
    newman_path=ROOT/'tests/evidence/newman-20261013-012500-070211-run.json';newman=read(newman_path)
    newman_json=read(ROOT/'tests/evidence/newman-20261013-012500-070211.json')
    nj=ET.parse(ROOT/'tests/evidence/newman-20261013-012500-070211.xml')
    proto_before=read(ROOT/'tests/evidence/prototype-ux-20261013-012403.json')
    proto_after=read(ROOT/recheck['run_record'])
    issue=read(ROOT/'tests/evidence/portfolio-clean-start-20261013-documentation-issue-before-fix.json')
    runtime_mismatch=[n for n,h in newman['source_sha256'].items() if sha(CLONE/n)!=h]
    proto_mismatch=[n for n,h in proto_after['source_sha256'].items() if sha(CLONE/n)!=h]
    artifacts=read(ROOT/'tests/evidence/portfolio-clean-start-20261013-artifacts.json')+recheck['artifacts']
    artifact_mismatch=[x['file'] for x in artifacts if sha(ROOT/x['file'])!=x['sha256']]
    docs=['README.md','api/README.md','prototype/README.md','docs/backend-running.md','docs/release-checklist.md','docs/decision-log.md','docs/ac-traceability.md','docs/traceability.md','TASKS.md','tests/evidence/portfolio-clean-start-report-20261013.md']
    broken=[];count=0
    def links(name,text,base):
        nonlocal count
        targets=re.findall(r'\[[^\]]*\]\(([^)]+)\)',text)+re.findall(r'^\[[^\]]+\]:\s*(\S+)',text,re.M)+re.findall(r'<img[^>]+src="([^"]+)"',text)
        for target in targets:
            if re.match(r'(?:https?://|mailto:|#)',target):continue
            count+=1;target=unquote(target.split('#')[0].strip('<>'))
            if target and not(base/target).exists():broken.append({'file':name,'target':target})
    # Original published docs resolved against untouched tracked clone contents.
    for name in ['README.md','api/README.md','prototype/README.md','docs/backend-running.md','docs/release-checklist.md']:
        original=subprocess.check_output(['git','show','HEAD:'+name],cwd=CLONE).decode('utf8')
        links('as-published/'+name,original,(CLONE/name).parent)
    for name in docs:links('proposed/'+name,(ROOT/name).read_text(encoding='utf8'),(ROOT/name).parent)
    excluded=read(ROOT/recheck['excluded_original_repo_run'])
    ports={str(p):closed(p) for p in [8000,8765,urlsplit(newman['base_url']).port,urlsplit(proto_before['base_url']).port,urlsplit(proto_after['base_url']).port,urlsplit(excluded['base_url']).port]}
    versions={'python':subprocess.check_output([str(CLONE/'.venv/Scripts/python.exe'),'--version'],text=True).strip(),'pip':subprocess.check_output([str(CLONE/'.venv/Scripts/python.exe'),'-m','pip','--version'],text=True).strip().replace(str(CLONE),'<fresh-checkout>'),'node':newman['node_version'],'newman':newman['newman_version'],'os':platform.platform()}
    diff=subprocess.run(['git','diff','--check'],cwd=ROOT,capture_output=True,text=True)
    staged=subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT,text=True).splitlines()
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    runtime_ok=pytest['cases']==181 and not any(pytest[k] for k in ['failures','errors','skipped']) and all(proto['harness']['passed']==110 and proto['harness']['failed']==0 and proto['ux_browser_passed'] and not proto['runtime_errors'] and proto['no_api_calls'] for proto in [proto_before,proto_after]) and len(run['prototype_documented_static_smoke']['checks'])==24 and all(x['passed'] for x in run['prototype_documented_static_smoke']['checks']) and newman['passed'] and newman['exit_code']==0 and newman['stats']['requests']['total']==191 and newman['stats']['assertions']['total']==514 and len(nj.findall('.//testcase'))==514 and not(nj.findall('.//failure') or nj.findall('.//error')) and len(newman_json['run']['executions'])==191 and not newman_json['run']['failures'] and run['backend_http']['openapi_matches_tracked']
    result={'checked_commit':run['commit'],'clone':run['checkout'],'tool_versions':versions,'original_protected_files':len(baseline['files']),'original_changes_allowed':changes,'original_unexpected_changes':unexpected,'original_database_changes':databases,'run_project_preserved':sha(ROOT/'Run Project.txt')==baseline['files']['Run Project.txt'],'old_evidence_preserved':sum(n.startswith('tests/evidence/') for n in baseline['files']) if not unexpected else None,'clone_tracked_changes_after_docs_patch':clone_changes,'fresh_ignored_inventory_before_setup':run['initial_ignored_state'],'pytest':pytest,'prototype_before_and_after':{'cases_each':110,'local_static_smoke_checks':24,'accepted_recheck':recheck['run_record'],'excluded_original_repo_run':recheck['excluded_original_repo_run']},'newman':{'requests':191,'assertions':514,'exit_code':0,'fresh_database_retained':newman['database_retained'],'owned_server_stopped':newman['owned_server_stopped']},'fresh_newman_source_mismatches':runtime_mismatch,'fresh_prototype_source_mismatches':proto_mismatch,'copied_artifact_byte_mismatches':artifact_mismatch,'links_images_checked':count,'broken_links_images':broken,'owned_ports_closed':ports,'owned_recorded_servers_stopped':all(s['stopped'] for s in run['servers']) and run['owned_browser_stopped'],'git_diff_check_exit_code':diff.returncode,'staged_files':staged,'head_unchanged':head==baseline['head'],'runtime_acceptance_passed':runtime_ok,'as_published_all_documented_steps_passed':False,'documentation_defect':issue['id'],'doc_correction_verified_on_clone':recheck['passed'],'correction_published':False,'video_available':False,'limitations':'Windows/Edge headless local only; no Pages redeploy, Postman UI or production acceptance. False as-published flag remains because historical auditor failed; evidence not rewritten.'}
    result['older_ignored_evidence_logs_checked']=len(old_logs)
    result['older_ignored_evidence_log_changes']=log_changes
    result['audit_passed']=not any([unexpected,databases,log_changes,runtime_mismatch,proto_mismatch,artifact_mismatch,broken,diff.returncode,staged]) and clone_changes==['prototype/README.md'] and all(ports.values()) and result['owned_recorded_servers_stopped'] and result['head_unchanged'] and runtime_ok and result['doc_correction_verified_on_clone']
    p=ROOT/('tests/evidence/portfolio-clean-start-audit-'+datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')+'.json');assert not p.exists();p.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(result,ensure_ascii=False,indent=2));print(p)
    return int(not result['audit_passed'])


if __name__=='__main__':raise SystemExit(main())
