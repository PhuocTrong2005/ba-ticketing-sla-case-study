"""Verify the 83-case run evidence and preservation of the 81-case milestone.

Run from repository root after the reference checker and structural audit.
This checks artefacts, not backend functionality or owner verification methods.
"""

from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote

sys.dont_write_bytecode = True
from audit_fixture_structure import unique_object


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_bytes(), object_pairs_hook=unique_object)


def main():
    root = Path.cwd()
    evidence = Path('tests/evidence')
    fixture = Path('tests/sla/sla-scenarios.json')
    rows = read(fixture)
    baseline = read(evidence / 'sla-verification-83-baseline.json')
    old_raw = subprocess.check_output(['git', 'show', baseline['git_commit'] + ':' + fixture.as_posix()])
    full = read(evidence / 'sla-reference-83-results.json')
    prior_81 = read(evidence / 'sla-reference-81-results.json')
    m69 = read(evidence / 'sla-reference-83-milestone-69.json')
    m81 = read(evidence / 'sla-reference-83-milestone-81.json')
    original = read(evidence / 'sla-reference-83-original-69.json')
    audit = read(evidence / 'sla-fixture-83-audit.json')
    checks = {
        '83_unique_ordered_verified_ids': [r['scenario_id'] for r in rows] ==
            [f'SLA-{i:02}' for i in range(1, 84)] and all(r['review_status'] == 'verified' for r in rows),
        'baseline_fixture_matches_git': hashlib.sha256(old_raw).hexdigest() == baseline['fixture_sha256'],
        'old_81_objects_unchanged': rows[:81] == json.loads(old_raw),
        'old_81_object_bytes_unchanged': hashlib.sha256(fixture.read_bytes()[
            :baseline['old_object_prefix_bytes']]).hexdigest() == baseline['old_object_prefix_sha256'],
        'new_rows_use_existing_schema': all(set(r) == set(rows[70]) for r in rows[81:]),
        'no_invented_confirmation_time': all(r['verified_at'] is None for r in rows[81:]),
        'reference_83_pass_1496': full['exit_code'] == 0 and full['total'] ==
            {'cases': 83, 'passed': 83, 'failed': 0, 'field_comparisons': 1496},
        'boundary_pass_5_separate': full['supplementary_summary'] ==
            {'cases': 1, 'passed': 1, 'failed': 0, 'field_comparisons': 5} and full['all_comparisons'] == 1501,
        'milestone_69_pass_1243': m69['exit_code'] == 0 and m69['total'] ==
            {'cases': 69, 'passed': 69, 'failed': 0, 'field_comparisons': 1243},
        'milestone_81_pass_1460': m81['exit_code'] == 0 and m81['total'] ==
            {'cases': 81, 'passed': 81, 'failed': 0, 'field_comparisons': 1460},
        'original_69_pass_1243': original['passed'] == 69 and original['failed'] == 0
            and original['field_comparisons'] == 1243,
        '83_first_81_results_match_historical_81': full['scenarios'][:81] == prior_81['scenarios'],
        'milestone_results_match_full_run': m69['scenarios'] == full['scenarios'][:69]
            and m81['scenarios'] == full['scenarios'][:81],
        'original_results_match_current_69': original['scenarios'] == m69['scenarios'],
        'audit_pass_4876': audit['exit_code'] == 0 and all(audit['global_checks'].values())
            and audit['total'] == {'cases': 83, 'passed': 83, 'failed': 0,
                                  'structural_assertions': 4876, 'sla_comparisons': 0},
    }
    for count, report in ((83, full), (69, m69), (81, m81)):
        checks[f'report_{count}_hashes_match'] = (
            report['source_sha256'] == sha(fixture)
            and report['checker_sha256'] == sha('tests/sla/reference/validate_sla_reference_current.py')
            and report['comparison_module_sha256'] == sha('tests/sla/reference/validate_sla_reference_81.py')
            and report['original_engine_sha256'] == sha('tests/sla/reference/validate_sla_reference.py'))
        checks[f'report_{count}_selected_ids_match'] = report['selected_ids'] == [r['scenario_id'] for r in rows[:count]]
    checks['original_69_hashes_match'] = (
        original['source_sha256'] == sha('tests/sla/reference/source/sla_draft_data.json')
        and original['checker_sha256'] == sha('tests/sla/reference/validate_sla_reference.py'))
    checks['audit_hashes_match'] = (
        audit['fixture_sha256'] == sha(fixture)
        and audit['audit_sha256'] == sha('tests/sla/audit_fixture_83.py')
        and audit['preserved_source_sha256'] == sha('tests/sla/reference/source/sla_draft_data.json')
        and all(sha(path) == digest for path, digest in audit['dependency_sha256'].items()))
    runtime_files = list(evidence.glob('sla-reference-83-*.json')) + [
        evidence / 'sla-fixture-83-audit.json', fixture,
        Path('tests/sla/reference/validate_sla_reference_current.py'),
        Path('tests/sla/audit_fixture_83.py'), Path(__file__)]
    checks['runtime_inputs_reports_use_checkout_stable_lf'] = all(
        b'\r\n' not in p.read_bytes() for p in runtime_files)
    preserved = {path: sha(path) == digest for path, digest in baseline['preserved_files'].items()
                 if path != 'tests/sla/reference/README.md'}
    checks['historical_artefacts_and_tools_unchanged'] = all(preserved.values())
    docs = [Path(p) for p in ('docs/spec/scenario-coverage.md', 'docs/decision-log.md',
                             'docs/traceability.md', 'docs/open-questions.md', 'TASKS.md',
                             'tests/sla/reference/README.md', 'tests/evidence/sla-verification-83.md')]
    # The final report is generated below; account for that link on the first run.
    report_path = evidence / 'sla-verification-83-checks.json'
    manifest_path = evidence / 'sla-verification-83.sha256'
    broken, links = [], 0
    for doc in docs:
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', doc.read_text(encoding='utf-8')):
            if target.startswith(('http:', 'https:', '#', 'mailto:')):
                continue
            links += 1
            resolved = (doc.parent / unquote(target.split('#', 1)[0])).resolve()
            if not resolved.exists() and resolved not in {root / report_path, root / manifest_path}:
                broken.append({'document': str(doc), 'target': target})
    checks['document_links_resolve'] = not broken
    diff = subprocess.run(['git', 'diff', '--check'], capture_output=True, text=True)
    checks['git_diff_check_exit_zero'] = diff.returncode == 0
    report = {
        'kind': '83-case artefact integrity and provenance checks; not backend/API tests',
        'executed_at': datetime.now(timezone(timedelta(hours=7))).isoformat(timespec='seconds'),
        'command_argv': sys.orig_argv, 'checks': checks,
        'preserved_files': preserved, 'links_checked': links, 'broken_links': broken,
        'git_diff_check': {'exit_code': diff.returncode, 'stdout': diff.stdout, 'stderr': diff.stderr},
        'fixture_sha256': sha(fixture), 'verification_script_sha256': sha(__file__),
        'exit_code': int(not all(checks.values())),
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    # Hash only LF-pinned runtime/evidence files; historical manifests stay intact.
    files = sorted(set([fixture, Path(__file__).relative_to(root),
                        Path('tests/sla/audit_fixture_83.py'),
                        Path('tests/sla/audit_fixture_structure.py'),
                        Path('tests/sla/audit_draft_import.py'),
                        Path('tests/sla/reference/validate_sla_reference_current.py'),
                        Path('tests/sla/reference/validate_sla_reference_81.py'),
                        Path('tests/sla/reference/validate_sla_reference.py'),
                        Path('tests/sla/reference/source/sla_draft_data.json'),
                        evidence / 'sla-fixture-83-audit.json']
                       + list(evidence.glob('sla-reference-83-*.json'))
                       + list(evidence.glob('sla-verification-83-*.json'))))
    manifest_path.write_text(''.join(f'{sha(p)}  {p.as_posix()}\n' for p in files), encoding='utf-8', newline='\n')
    manifest_valid = all(sha(path) == digest for digest, path in
                         (line.split('  ', 1) for line in manifest_path.read_text().splitlines()))
    print(json.dumps({'checks': len(checks), 'failed': [k for k, v in checks.items() if not v],
                      'preserved_files': len(preserved), 'manifest_entries': len(files),
                      'manifest_verified': manifest_valid, 'exit_code': report['exit_code']}))
    return report['exit_code'] or int(not manifest_valid)


if __name__ == '__main__':
    raise SystemExit(main())
