"""Structural import audit only. Does not calculate SLA or change review status.

Run at repository root. The original 69-case audit/checker stay unchanged.
"""
import argparse
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from audit_fixture_structure import audit_case, coverage_table, timestamp, unique_object, walk


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def business(row):
    return {k: v for k, v in row.items() if k.startswith('expected_') or k in
            ('policy_id', 'created_at', 'as_of', 'events', 'resolution_result_final')}


def audit_draft(row, source):
    errors, count = [], 0

    def check(condition, message):
        nonlocal count
        count += 1
        if not condition:
            errors.append(message)

    try:
        forbidden = {'verified_by', 'verified_at', 'owner_check_result', 'owner_results',
                     'owner_calculation_note', 'owner_confirmation'}
        required = (set(source[0]) - forbidden)
        check(required <= set(row), 'Missing fixture fields')
        check(not (set(row) & forbidden), 'Owner verification fields in draft')
        check(set(row) <= set(source[0]), 'Invented fixture fields')
        check(row['review_status'] == 'draft', 'Draft review_status')
        check(row['reviewed_by'] is None, 'No claimed reviewer')
        check(row['drafted_by'] == 'AI advisor', 'Provenance author')
        for key in ('description', 'calculation_note', 'verification_method',
                    'verification_basis', 'verification_evidence_status'):
            check(isinstance(row[key], str) and bool(row[key].strip()), key)
        check(row['blocked_by'] == [], 'Unexpected blocker')
        check(isinstance(row['draft_assumptions'], list), 'Assumptions list')
        groups = row['coverage_groups']
        check(bool(groups) and len(groups) == len(set(groups)) and
              all(type(g) is int and 1 <= g <= 12 for g in groups), 'Coverage groups')
        check(row['policy_id'] in {'HIGH', 'NORMAL'}, 'Policy')
        created, asof = timestamp(row['created_at']), timestamp(row['as_of'])
        check(asof >= created, 'as_of before creation')
        check(type(row['resolution_result_final']) is bool, 'Final flag type')
        check(row['expected_ticket_state'] in {'New', 'In Progress', 'Waiting for Customer',
                                             'Resolved', 'Closed'}, 'Ticket state enum')
        for clock in ('first_response', 'resolution'):
            check(row[f'expected_{clock}_status'] in {'pending', 'met', 'breached'}, 'SLA enum')
            check(row[f'expected_{clock}_warning_level'] in
                  {'none', 'soft', 'emphasized', 'due', 'breached'}, 'Warning enum')
            check(row[f'expected_{clock}_sla_status_at_assignment'] in
                  {None, 'pending', 'breached'}, 'Snapshot enum')
        check(type(row['expected_rejection_count']) is int and
              row['expected_rejection_count'] >= 0, 'Rejection count type')
        steps = []
        allowed = {e['type'] for s in source for e in s['events']}
        check(isinstance(row['events'], list), 'Events list')
        previous = (created, 0)
        for event in row['events']:
            check(set(event) == {'seq', 'type', 'at'}, 'Successful event schema')
            at, seq = timestamp(event['at']), event['seq']
            check(type(seq) is int and seq > previous[1] and at >= previous[0], 'Event order')
            check(created <= at <= asof, 'Event evaluation window')
            check(event['type'] in allowed and event['type'] != 'resolved_attempt', 'Successful event type')
            previous = (at, seq)
            steps.append((seq, at))
        for key in ('expected_resolution_intervals', 'expected_reviews', 'expected_rejected_actions'):
            check(isinstance(row[key], list), key)
        action_shape = set(source[60]['expected_rejected_actions'][0])
        for action in row['expected_rejected_actions']:
            check(set(action) == action_shape, 'Rejected action schema matches SLA-61')
            check(type(action['step_seq']) is int and action['step_seq'] > 0, 'Rejected seq')
            check(action['type'] == 'resolved_attempt' and action['error_code'] == 'REVIEW_REQUIRED'
                  and action['http_status'] == 409, 'Declared refusal enum; not HTTP execution')
            check(action['expected_state_change'] is False and
                  action['expected_sla_interval_change'] is False, 'Declared no-change flags')
            at = timestamp(action['at'])
            check(created <= at <= asof, 'Rejected action window')
            steps.append((action['step_seq'], at))
        check(len({seq for seq, _ in steps}) == len(steps), 'Unique combined step seq')
        steps.sort()
        check(all(a[1] <= b[1] for a, b in zip(steps, steps[1:])), 'Combined step order')
        previous_end = created
        for i, interval in enumerate(row['expected_resolution_intervals']):
            start = timestamp(interval['started_at'])
            end = timestamp(interval['ended_at']) if interval['ended_at'] else None
            seconds_key = 'business_seconds' if end else 'business_seconds_as_of'
            check(set(interval) == {'started_at', 'ended_at', seconds_key}, 'Interval schema')
            check(previous_end <= start <= asof and (end is None or start <= end <= asof), 'Interval order')
            check(end is not None or i == len(row['expected_resolution_intervals']) - 1, 'Open interval last')
            previous_end = end or asof
        review_keys = []
        for review in row['expected_reviews']:
            check(set(review) == {'review_key', 'requested_at', 'completed_at',
                                 'wait_calendar_seconds', 'wait_overlap_seconds', 'breach_context'}, 'Review schema')
            review_keys.append(review['review_key'])
            check(review['breach_context'] in {'none', 'before_request', 'during_wait'}, 'Review enum')
            start = timestamp(review['requested_at'])
            end = timestamp(review['completed_at']) if review['completed_at'] else asof
            check(created <= start <= end <= asof, 'Review window')
        check(len(review_keys) == len(set(review_keys)), 'Unique review keys')
        open_keys = [r['review_key'] for r in row['expected_reviews'] if r['completed_at'] is None]
        check(open_keys == ([] if row['expected_open_review'] is None else [row['expected_open_review']]), 'Open review link')
        for key, value, path in walk(row):
            if value is None:
                continue
            if key.endswith('_seconds') or key == 'business_seconds_as_of':
                check(type(value) is int and value >= 0, f'Integer seconds {path}')
            if key.endswith('_at') or key in {'at', 'as_of'}:
                timestamp(value)
    except (KeyError, ValueError, TypeError) as exc:
        errors.append(str(exc))
    return dict(scenario_id=row.get('scenario_id'), structural_status='FAIL' if errors else 'PASS',
                structural_assertions=count, errors=errors, expected_values_recomputed=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, default=Path('tests/evidence/sla-draft-import-structure.json'))
    args = parser.parse_args()
    fixture = Path('tests/sla/sla-scenarios.json')
    raw = fixture.read_bytes()
    rows = json.loads(raw, object_pairs_hook=unique_object)
    source_path = Path('tests/sla/reference/source/sla_draft_data.json')
    source = json.loads(source_path.read_bytes(), object_pairs_hook=unique_object)['scenarios']
    baseline = json.loads(Path('tests/evidence/sla-draft-import-baseline.json').read_bytes())
    old, new = rows[:69], rows[69:]
    global_checks = {
        'exact_unique_ids': [r['scenario_id'] for r in rows] == [f'SLA-{n:02}' for n in range(1, 82)],
        'old_69_objects_equal_source': old == source,
        'old_69_object_bytes_preserved': sha(raw[:baseline['old_object_prefix_bytes']]) == baseline['old_object_prefix_sha256'],
        'original_checker_unchanged': sha(Path('tests/sla/reference/validate_sla_reference.py').read_bytes()) == baseline['checker_sha256'],
        'historical_audit_unchanged': sha(Path('tests/sla/audit_fixture_structure.py').read_bytes()) == baseline['historical_audit_sha256'],
    }
    duplicates = {r['scenario_id']: [s['scenario_id'] for s in old if business(r) == business(s)] for r in new}
    global_checks['no_new_old_duplicate'] = not any(duplicates.values())
    global_checks['no_new_new_duplicate'] = not any(business(a) == business(b) for i, a in enumerate(new) for b in new[i+1:])
    coverage_path = Path('docs/spec/scenario-coverage.md')
    verified_groups = coverage_table(coverage_path)
    verified_ids = {r['scenario_id'] for r in old if r['review_status'] == 'verified'}
    global_checks['verified_table_only_verified'] = all(set(ids) <= verified_ids for ids in verified_groups.values())
    global_checks['verified_groups_retained'] = set(verified_groups) == set(range(1, 13)) and all(verified_groups.values())
    coverage = coverage_path.read_text(encoding='utf-8')
    for i, row in enumerate(new, 1):
        expected_line = f"| S{i} | {row['scenario_id']} | " + ', '.join(map(str, row['coverage_groups'])) + ' |'
        global_checks[f'S{i}_draft_coverage_mapping'] = expected_line in coverage
    records = [audit_case(r) for r in old] + [audit_draft(r, source) for r in new]
    def summary(cases):
        return dict(cases=len(cases), passed=sum(c['structural_status'] == 'PASS' for c in cases),
                    failed=sum(c['structural_status'] == 'FAIL' for c in cases),
                    structural_assertions=sum(c['structural_assertions'] for c in cases), sla_comparisons=0)
    report = dict(kind='Fixture structure/source preservation only; no SLA calculation',
                  executed_at=datetime.now(timezone(timedelta(hours=7))).isoformat(timespec='seconds'),
                  executed_by='Codex AI assistant', command='python ' + ' '.join(sys.argv),
                  fixture_sha256=sha(raw), audit_sha256=sha(Path(__file__).read_bytes()),
                  source_sha256=sha(source_path.read_bytes()), global_checks=global_checks,
                  old=summary(records[:69]), new=summary(records[69:]),
                  new_old_business_object_comparisons=len(old)*len(new), duplicates=duplicates,
                  new_new_business_object_comparisons=len(new)*(len(new)-1)//2,
                  cases=records)
    report['exit_code'] = int(not all(global_checks.values()) or any(c['errors'] for c in records))
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('old', 'new', 'exit_code')}))
    return report['exit_code']


if __name__ == '__main__':
    raise SystemExit(main())
