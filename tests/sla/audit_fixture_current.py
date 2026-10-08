"""Audit the current 81-case fixture without recalculating SLA expectations.

The earlier 12-draft import audit and its evidence remain unchanged. For the
newly verified cases this script reuses its structural checks on an in-memory
copy, then checks the actual owner-confirmation metadata separately.
"""

import argparse
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
from audit_fixture_structure import audit_case, coverage_table, unique_object
from audit_draft_import import audit_draft, business


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def audit_new_case(row, source):
    shadow = dict(row)
    for key in ('verified_by', 'verified_at', 'owner_confirmation'):
        shadow.pop(key, None)
    shadow['review_status'] = 'draft'
    result = audit_draft(shadow, source)
    errors = result['errors']
    count = result['structural_assertions']

    def check(condition, message):
        nonlocal count
        count += 1
        if not condition:
            errors.append(message)

    check(row.get('review_status') == 'verified', 'Owner-confirmed status')
    check(row.get('verified_by') == 'project owner', 'Verified by project owner')
    check('verified_at' in row and row['verified_at'] is None,
          'No invented second-precision confirmation time')
    check(row.get('reviewed_by') is None, 'No invented reviewer')
    check(row.get('owner_confirmation') ==
          'tôi đã verify bộ SLA đó; 08/10/2026; scope SLA-70..SLA-81',
          'Confirmation text/date/scope')
    check('owner_confirmation' in row.get('verification_basis', ''),
          'Confirmation provenance')
    check('owner verification method was not provided' in
          row.get('verification_method', ''), 'No invented owner method')
    check('owner_calculation_note' not in row and 'owner_check_result' not in row
          and 'owner_results' not in row, 'No invented owner calculations/results')
    result['structural_assertions'] = count
    result['structural_status'] = 'FAIL' if errors else 'PASS'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('fixture', type=Path)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    raw = args.fixture.read_bytes()
    rows = json.loads(raw, object_pairs_hook=unique_object)
    source_path = Path('tests/sla/reference/source/sla_draft_data.json')
    old_source = json.loads(source_path.read_bytes(), object_pairs_hook=unique_object)['scenarios']
    baseline = json.loads(Path('tests/evidence/sla-draft-import-baseline.json').read_bytes())
    old, new = rows[:69], rows[69:]
    groups = coverage_table(Path('docs/spec/scenario-coverage.md'))
    all_ids = {row['scenario_id'] for row in rows}
    global_checks = {
        'exact_81_unique_ordered_ids': [row['scenario_id'] for row in rows] ==
                                  [f'SLA-{i:02}' for i in range(1, 82)],
        'old_69_objects_equal_preserved_source': old == old_source,
        'old_69_object_bytes_preserved': sha(raw[:baseline['old_object_prefix_bytes']]) ==
                                         baseline['old_object_prefix_sha256'],
        'original_69_checker_unchanged': sha(Path('tests/sla/reference/validate_sla_reference.py').read_bytes()) ==
                                         baseline['checker_sha256'],
        'all_12_groups_present_in_table': set(groups) == set(range(1, 13)) and all(groups.values()),
        'coverage_table_links_existing_verified_ids': all(set(ids) <= all_ids for ids in groups.values()),
        'new_case_groups_linked_in_table': all(row['scenario_id'] in groups[group]
                                             for row in new for group in row['coverage_groups']),
        'SLA_81_due_and_refusal': new[-1]['expected_resolution_due_at'] ==
                                  '2026-10-06T08:30:00+07:00'
                                  and len(new[-1]['expected_rejected_actions']) == 1
                                  and not any(e['type'] == 'resolved_attempt' for e in new[-1]['events']),
        'no_new_old_duplicate_business_case': not any(business(a) == business(b)
                                                       for a in new for b in old),
    }
    records = [audit_case(row) for row in old] + [audit_new_case(row, old_source) for row in new]

    def summary(part):
        return {'cases': len(part), 'passed': sum(r['structural_status'] == 'PASS' for r in part),
                'failed': sum(r['structural_status'] == 'FAIL' for r in part),
                'structural_assertions': sum(r['structural_assertions'] for r in part),
                'sla_comparisons': 0}

    report = {
        'kind': 'Fixture structure/provenance/coverage audit only; no SLA calculation',
        'executed_at': datetime.now(timezone(timedelta(hours=7))).isoformat(timespec='seconds'),
        'execution_by': 'Codex AI assistant running local Python',
        'command': subprocess.list2cmdline(sys.orig_argv),
        'command_argv': sys.orig_argv,
        'fixture_sha256': sha(raw),
        'audit_sha256': sha(Path(__file__).read_bytes()),
        'preserved_source_sha256': sha(source_path.read_bytes()),
        'global_checks': global_checks,
        'old_69': summary(records[:69]),
        'new_12': summary(records[69:]),
        'cases': records,
    }
    report['exit_code'] = int(not all(global_checks.values()) or
                              any(record['errors'] for record in records))
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('old_69', 'new_12', 'exit_code')}))
    return report['exit_code']


if __name__ == '__main__':
    raise SystemExit(main())
