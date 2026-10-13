"""Read-only final audit; saves a new report, never changes baseline artefacts."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]


def main():
    def git(*args):
        return subprocess.check_output(['git', *args], cwd=ROOT)

    editable = {'README.md', 'TASKS.md', 'docs/decision-log.md', 'docs/traceability.md'}
    tracked = git('ls-files', '-z').decode().split('\0')
    unchanged, changed, line_endings = [], [], []
    for name in filter(None, tracked):
        if name in editable:
            continue
        # The existing clean checkout mixes LF and CRLF. Never rewrite these
        # files just to force the current checkout attribute onto old evidence.
        actual = (ROOT / name).read_bytes()
        raw = git('show', 'HEAD:' + name)
        filtered = git('cat-file', '--filters', 'HEAD:' + name)
        if actual in (raw, filtered):
            unchanged.append(name)
        elif actual.replace(b'\r\n', b'\n') == raw.replace(b'\r\n', b'\n'):
            line_endings.append({'file':name,'current_sha256':hashlib.sha256(actual).hexdigest(),'comparison':'Only LF/CRLF differs from HEAD; initial working tree was clean. No claim of raw byte equality to Git blob.'})
        else:
            changed.append(name)
    spec_path = ROOT / 'docs/05-prototype/prototype-spec.md'
    spec_same = spec_path.read_bytes() == Path('D:/Download/prototype-spec.md').read_bytes()
    docs = [ROOT / p for p in editable] + [spec_path, ROOT / 'prototype/README.md', ROOT / 'tests/evidence/prototype-report-20261012.md']
    broken = []
    checked = 0
    for p in docs:
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', p.read_text(encoding='utf-8-sig')):
            if re.match(r'(?:https?://|mailto:|#)', target):
                continue
            target = unquote(target.split('#')[0].strip('<>'))
            if target and not (p.parent / target).exists():
                broken.append({'file':str(p.relative_to(ROOT)), 'target':target})
            checked += 1
    latest = sorted((ROOT / 'tests/evidence').glob('prototype-*-*.json'))
    runs = [p for p in latest if re.fullmatch(r'prototype-\d{8}-\d{6}\.json', p.name)]
    run = json.loads(runs[-1].read_text(encoding='utf8'))
    mismatch = [name for name, value in run['source_sha256'].items() if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != value]
    # Check runtime dependencies separately from test-only fetches.
    forbidden_runtime = []
    for p in (ROOT / 'prototype').glob('*.js'):
        if re.search(r'\b(?:fetch|XMLHttpRequest|WebSocket|expected_\w+)\b', p.read_text(encoding='utf8')):
            forbidden_runtime.append(str(p.relative_to(ROOT)))
    secret_hits = []
    for p in [*(ROOT / 'prototype').glob('*'), *(ROOT / 'tests/prototype').glob('*')]:
        if p.is_file() and re.search(r'AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}', p.read_text(encoding='utf8')):
            secret_hits.append(str(p.relative_to(ROOT)))
    output = {
        'base_commit':git('rev-parse','HEAD').decode().strip(),
        'main_commit':git('rev-parse','main').decode().strip(),
        'latest_browser_evidence':str(runs[-1].relative_to(ROOT)),
        'tracked_files_byte_unchanged_count':len(unchanged),
        'tracked_byte_comparison':'Exact match to HEAD blob or --filters checkout bytes; initial git status was clean. LF/CRLF-only cases recorded separately.',
        'line_ending_only_matches':line_endings,
        'tracked_files_byte_unchanged':unchanged,
        'unexpected_tracked_changes':changed,
        'fixture_sha256':hashlib.sha256((ROOT / 'tests/sla/sla-scenarios.json').read_bytes()).hexdigest(),
        'spec_exact_attachment_bytes':spec_same,
        'local_links_checked':checked,'broken_links':broken,
        'source_hash_mismatches_since_browser_run':mismatch,
        'forbidden_runtime_calls_or_expected_lookups':forbidden_runtime,
        'credential_pattern_hits':secret_hits,
        'git_diff_check':subprocess.run(['git','diff','--check'],cwd=ROOT,capture_output=True,text=True).returncode,
        'limitations':'Credential pattern scan is bounded; no production/customer data was used. Spec source path is local to this owner machine. Browser UX approval, physical devices and cross-browser remain separate.'
    }
    output['passed'] = not (changed or not spec_same or broken or mismatch or forbidden_runtime or secret_hits or output['git_diff_check'])
    dest = ROOT / 'tests/evidence/prototype-audit-20261012.json'
    dest.write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in output.items() if k!='tracked_files_byte_unchanged'},ensure_ascii=False,indent=2))
    return int(not output['passed'])


if __name__ == '__main__':
    raise SystemExit(main())
