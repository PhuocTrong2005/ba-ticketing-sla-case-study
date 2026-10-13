"""Record preservation, runtime/test source match, links and staged hygiene."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time
from urllib.parse import unquote
from public_smoke import RUNTIME

ROOT = Path(__file__).resolve().parents[2]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    baseline = json.loads((ROOT / 'tests/evidence/pages-baseline-20261013.json').read_text(encoding='utf8'))
    changed = [n for n, h in baseline.items() if not (ROOT / n).exists() or digest(ROOT / n) != h]
    runs = sorted((ROOT / 'tests/evidence').glob('prototype-ux-*.json'))
    runs = [p for p in runs if re.fullmatch(r'prototype-ux-\d{8}-\d{6}\.json', p.name)]
    latest = runs[-1]
    run = json.loads(latest.read_text(encoding='utf8'))
    required = ['prototype/' + n for n in RUNTIME] + ['tests/prototype/test.js', 'tests/prototype/index.html', 'tests/prototype/run_browser.py']
    mismatch = [n for n in required if digest(ROOT / n) != run['source_sha256'].get(n)]
    broken, count = [], 0
    docs = [ROOT / n for n in ['README.md', 'TASKS.md', 'docs/decision-log.md', 'docs/traceability.md', 'docs/05-prototype/prototype-spec.md', 'prototype/README.md', 'tests/evidence/pages-report-20261013.md']]
    for p in docs:
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', p.read_text(encoding='utf8')):
            if re.match(r'(?:https?://|mailto:|#)', target):
                continue
            target = unquote(target.split('#')[0].strip('<>'))
            count += 1
            if target and not (p.parent / target).exists():
                broken.append({'file': str(p.relative_to(ROOT)), 'target': target})
    diff = subprocess.run(['git', 'diff', '--check'], capture_output=True, text=True)
    staged_diff = subprocess.run(['git', 'diff', '--cached', '--check'], capture_output=True, text=True)
    staged = subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines()
    forbidden = [n for n in staged if re.search(r'(?:^|/)(?:\.venv[^/]*|__pycache__|\.pytest_cache|node_modules|data|_site)(?:/|$)|\.(?:sqlite3|db|pyc|log)$|(?:^|/)\.env(?:\.|$)', n)]
    secret_hits = []
    pattern = re.compile(rb'github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')
    for n in staged:
        p = ROOT / n
        if p.is_file() and p.suffix not in ['.png', '.jpg'] and pattern.search(p.read_bytes()):
            secret_hits.append(n)
    tracked = subprocess.check_output(['git', 'ls-files'], text=True).splitlines()
    byte_scope = [n for n in tracked if n.startswith(('prototype/', 'tests/prototype/', 'tests/evidence/prototype-', 'tests/evidence/pages-', 'tests/evidence/ux-baseline-'))]
    index_mismatch = [n for n in byte_scope if (ROOT / n).is_file() and subprocess.check_output(['git', 'show', ':' + n]) != (ROOT / n).read_bytes()]
    result = {'local_run': str(latest.relative_to(ROOT)).replace('\\', '/'),
              'protected_files': len(baseline), 'old_evidence_preserved': sum(n.startswith('tests/evidence/') for n in baseline) if not changed else None,
              'changed_or_deleted': changed, 'runtime_and_harness_source_mismatches': mismatch,
              'fixture_sha256': digest(ROOT / 'tests/sla/sla-scenarios.json'),
              'links_checked': count, 'broken_links': broken,
              'git_diff_check': diff.returncode, 'git_staged_diff_check': staged_diff.returncode,
              'staged_files': staged, 'forbidden_staged': forbidden, 'secret_pattern_hits': secret_hits,
              'index_bytes_checked': len(byte_scope), 'index_byte_mismatches': index_mismatch,
              'local_suite': {'passed': run['harness']['passed'], 'failed': run['harness']['failed'], 'ux_browser_passed': run['ux_browser_passed'], 'runtime_errors': run['runtime_errors'], 'no_api_calls': run['no_api_calls']},
              'backend_tests_rerun': False}
    result['passed'] = not any([changed, mismatch, index_mismatch, broken, diff.returncode, staged_diff.returncode, forbidden, secret_hits, run['harness']['failed'], run['runtime_errors']]) and run['harness']['passed'] == 110 and run['ux_browser_passed'] and run['no_api_calls']
    dest = ROOT / ('tests/evidence/pages-audit-' + time.strftime('%Y%m%d-%H%M%S', time.gmtime()) + '.json')
    dest.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf8')
    print(json.dumps({k: v for k, v in result.items() if k != 'staged_files'}, ensure_ascii=False, indent=2))
    print(dest)
    return int(not result['passed'])


if __name__ == '__main__':
    raise SystemExit(main())
