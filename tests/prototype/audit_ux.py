"""Audit UX changes against this task's baseline; keep all old evidence intact."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
from datetime import datetime, timezone
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
ALLOWED = {
    'prototype/app.js', 'prototype/index.html', 'prototype/styles.css',
    'prototype/README.md', 'docs/05-prototype/prototype-spec.md',
    'docs/decision-log.md', 'docs/traceability.md',
    'tests/prototype/test.js', 'tests/prototype/run_browser.py'
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    baseline = json.loads((ROOT / 'tests/evidence/ux-baseline-20261013.json').read_text(encoding='utf8'))
    unexpected, preserved, edited = [], [], []
    for name, sha in baseline.items():
        path = ROOT / name
        if path.exists() and digest(path) == sha:
            preserved.append(name)
        elif name in ALLOWED:
            edited.append(name)
        else:
            unexpected.append(name)
    runs = sorted(p for p in (ROOT / 'tests/evidence').glob('prototype-ux-*.json') if re.fullmatch(r'prototype-ux-\d{8}-\d{6}\.json',p.name))
    run_path = runs[-1]
    run = json.loads(run_path.read_text(encoding='utf8'))
    mismatches = [name for name, sha in run['source_sha256'].items() if not (ROOT / name).exists() or digest(ROOT / name) != sha]
    docs = [ROOT / name for name in ALLOWED if name.endswith('.md')] + [ROOT / 'tests/evidence/prototype-ux-report-20261013.md']
    broken, checked = [], 0
    for path in docs:
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text(encoding='utf8')):
            if re.match(r'(?:https?://|mailto:|#)', target):
                continue
            target = unquote(target.split('#')[0].strip('<>'))
            checked += 1
            if target and not (path.parent / target).exists():
                broken.append({'file':str(path.relative_to(ROOT)), 'target':target})
    diff = subprocess.run(['git','diff','--check'],cwd=ROOT,capture_output=True,text=True)
    output = {
        'baseline':'tests/evidence/ux-baseline-20261013.json',
        'run_record':str(run_path.relative_to(ROOT)),
        'protected_files_preserved':preserved,
        'old_evidence_preserved_count':sum(name.startswith('tests/evidence/') for name in preserved),
        'allowed_files_changed':edited,
        'unexpected_changed_or_deleted':unexpected,
        'fixture_sha256':digest(ROOT / 'tests/sla/sla-scenarios.json'),
        'source_hash_mismatches_since_browser_run':mismatches,
        'local_links_checked':checked,'broken_links':broken,
        'git_diff_check_exit_code':diff.returncode,
        'browser_suite_passed':run.get('harness',{}).get('failed')==0 and run.get('harness',{}).get('passed')==110 and run.get('ux_browser_passed') is True and not run.get('runtime_errors') and run.get('no_api_calls') is True,
        'backend_tests_rerun':False,
        'limitations':'Headless installed Edge at desktop and 390px; no physical device/cross-browser/owner UX acceptance. All checks use current task baseline, including pre-existing uncommitted files.'
    }
    output['passed'] = not (unexpected or mismatches or broken or diff.returncode) and output['browser_suite_passed']
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
    dest=ROOT / f'tests/evidence/prototype-ux-audit-{stamp}.json'
    dest.write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in output.items() if k!='protected_files_preserved'},ensure_ascii=False,indent=2))
    print(dest)
    return int(not output['passed'])


if __name__ == '__main__':
    raise SystemExit(main())
