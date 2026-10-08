#!/usr/bin/env python3
"""Replay the current 81-case fixture with the preserved reference engine.

Only the CLI's fixed-ID limit and report metadata differ from the 69-case
checker. The working-second calendar and SLA calculation are imported intact.
This is a fixture cross-check, not a backend or HTTP test.
"""

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

sys.dont_write_bytecode = True
import validate_sla_reference as original


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def check_case(row, calendar):
    """Apply the original CLI's comparisons to one unchanged fixture row."""
    mismatches = []
    checks = 0
    calculated = None
    try:
        seq = [event['seq'] for event in row['events']]
        if len(set(seq)) != len(seq):
            raise ValueError('Duplicate event seq')
        for event in row['events']:
            if original.ts(event['at']) < original.ts(row['created_at']):
                raise ValueError('Event before creation')
            if datetime.fromisoformat(event['at']).microsecond:
                raise ValueError('Stored event not whole-second')
            if 'at_raw' in event and original.ts(event['at_raw']) != original.ts(event['at']):
                raise ValueError('Raw timestamp truncation mismatch')
        calculated = original.calculate(row, calendar)
        for key, value in calculated.items():
            checks += 1
            if row.get(key) != value:
                mismatches.append({'field': key, 'expected_fixture': row.get(key), 'reference_result': value})
        for action in row.get('expected_rejected_actions', []):
            checks += 1
            at_result = original.calculate(row, calendar, action['at'])
            if (action['type'] != 'resolved_attempt'
                    or at_result['expected_ticket_state'] != 'In Progress'
                    or at_result['expected_open_review'] is None
                    or action['error_code'] != 'REVIEW_REQUIRED'
                    or action['http_status'] != 409
                    or action['expected_state_change'] is not False
                    or action['expected_sla_interval_change'] is not False):
                mismatches.append({'field': 'expected_rejected_actions',
                                   'reason': 'Refusal context inconsistent'})
    except (ValueError, KeyError) as exc:
        mismatches.append({'field': 'fixture_structure_or_event_semantics', 'reason': str(exc)})
    return {'scenario_id': row['scenario_id'], 'checks': checks,
            'result': 'PASS' if not mismatches else 'FAIL',
            'mismatches': mismatches, 'reference': calculated}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    raw = args.source.read_bytes()
    pack = json.loads(raw)
    rows = pack['scenarios'] if isinstance(pack, dict) else pack
    expected_ids = {f'SLA-{i:02}' for i in range(1, 82)}
    if len(rows) != 81 or {row['scenario_id'] for row in rows} != expected_ids:
        raise ValueError('81 unique IDs SLA-01 through SLA-81 required')

    calendar = original.Calendar(rows)
    records = [check_case(row, calendar) for row in rows]
    def summary(part):
        return {'cases': len(part),
                'passed': sum(row['result'] == 'PASS' for row in part),
                'failed': sum(row['result'] == 'FAIL' for row in part),
                'field_comparisons': sum(row['checks'] for row in part)}

    report = {
        'kind': 'AI-assisted standalone reference fixture cross-check; not backend/API',
        'source_file': str(args.source),
        'source_sha256': sha(raw),
        'checker_sha256': sha(Path(__file__).read_bytes()),
        'original_engine_sha256': sha(Path(original.__file__).read_bytes()),
        'executed_at': datetime.now(original.TZ).isoformat(timespec='seconds'),
        'execution_by': 'Codex AI assistant running local Python',
        'command': subprocess.list2cmdline(sys.orig_argv),
        'command_argv': sys.orig_argv,
        'python_version': platform.python_version(),
        'method': ('Reuse the unmodified original Calendar, ts and calculate functions. '
                   'Enumerate working seconds, replay source events, compare the same 18 '
                   'calculated fields per case plus one refusal context check for each '
                   'expected_rejected_actions entry. Only the CLI ID limit is extended to 81.'),
        'old_69': summary(records[:69]),
        'new_12': summary(records[69:]),
        'total': summary(records),
        'limitations': [
            'Reference checker and fixture were authored with AI; this does not establish the project owner method of verification.',
            'Refusal checks establish event/review context only; no HTTP request, actor, payload, permission or atomicity is exercised.',
            'No backend, API, SQL, prototype or concurrency execution; coverage mapping and release gates require separate review.',
        ],
        'scenarios': records,
    }
    report['exit_code'] = 1 if report['total']['failed'] else 0
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('old_69', 'new_12', 'total', 'exit_code',
                                           'source_sha256', 'checker_sha256', 'original_engine_sha256')}))
    return report['exit_code']


if __name__ == '__main__':
    raise SystemExit(main())
