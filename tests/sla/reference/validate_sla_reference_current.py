#!/usr/bin/env python3
"""Cross-check 69/81/83-case milestones with the unchanged reference engine.

--case-count selects an ordered prefix of a supported fixture. The full source
hash and the selected IDs are recorded. No backend or HTTP code is executed.
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
import validate_sla_reference_81 as prior


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def summary(records):
    return {'cases': len(records),
            'passed': sum(r['result'] == 'PASS' for r in records),
            'failed': sum(r['result'] == 'FAIL' for r in records),
            'field_comparisons': sum(r['checks'] for r in records)}


def due_boundary(row, calendar):
    """Supplementary snapshot explicitly confirmed by the owner on 2026-10-10.

    This uses SLA-83's events; it is not an additional fixture or owner review.
    The main case remains evaluated at 08:00:01.
    """
    asof = '2026-10-06T08:00:00+07:00'
    expected = {'expected_resolution_status': 'pending',
                'expected_resolution_warning_level': 'due',
                'expected_resolution_due_at': asof,
                'expected_resolution_consumed_seconds': 28800,
                'expected_resolution_remaining_seconds': 0}
    actual = prior.original.calculate(row, calendar, asof)
    mismatches = [{'field': key, 'owner_expected': value, 'reference_result': actual[key]}
                  for key, value in expected.items() if actual[key] != value]
    return {'scenario_id': 'SLA-83', 'as_of_override': asof,
            'basis': 'Owner-supplied boundary statement, conversation 2026-10-10; BR-23/39/48/60',
            'checks': len(expected), 'result': 'FAIL' if mismatches else 'PASS',
            'expected': expected, 'reference': {key: actual[key] for key in expected},
            'mismatches': mismatches}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--case-count', type=int, choices=(69, 81, 83))
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    raw = args.source.read_bytes()
    pack = json.loads(raw)
    rows = pack['scenarios'] if isinstance(pack, dict) else pack
    if len(rows) not in (69, 81, 83) or [r['scenario_id'] for r in rows] != [
            f'SLA-{i:02}' for i in range(1, len(rows) + 1)]:
        raise ValueError('69, 81 or 83 unique ordered IDs starting at SLA-01 required')
    count = args.case_count or len(rows)
    if count > len(rows):
        raise ValueError('Requested milestone exceeds source fixture size')
    selected = rows[:count]
    calendar = prior.original.Calendar(selected)
    records = [prior.check_case(row, calendar) for row in selected]
    boundary = [due_boundary(selected[82], calendar)] if count == 83 else []
    report = {
        'kind': 'AI-assisted standalone reference fixture cross-check; not backend/API',
        'source_file': str(args.source), 'source_sha256': sha(raw),
        'source_cases': len(rows), 'selected_ids': [r['scenario_id'] for r in selected],
        'checker_sha256': sha(Path(__file__).read_bytes()),
        'comparison_module_sha256': sha(Path(prior.__file__).read_bytes()),
        'original_engine_sha256': sha(Path(prior.original.__file__).read_bytes()),
        'executed_at': datetime.now(prior.original.TZ).isoformat(timespec='seconds'),
        'execution_by': 'Codex AI assistant running local Python',
        'command': subprocess.list2cmdline(sys.orig_argv), 'command_argv': sys.orig_argv,
        'python_version': platform.python_version(),
        'method': 'Unchanged 69-case Calendar/ts/calculate and 81-case check_case; 18 deep field comparisons per case plus one per refusal context. Boundary comparisons are counted separately.',
        'old_69': summary(records[:69]), 'milestone_81': summary(records[:81]),
        'new_2': summary(records[81:]), 'total': summary(records),
        'supplementary_boundary': boundary,
        'supplementary_summary': summary(boundary),
        'all_comparisons': sum(r['checks'] for r in records + boundary),
        'limitations': [
            'Owner confirmation is supplied in conversation; owner verification method and precise confirmation time were not provided.',
            'Both fixture and checker have AI assistance; this is not proof of independent human calculation.',
            'No backend, API, HTTP, SQL, prototype, permissions, payload or concurrency testing.',
        ],
        'scenarios': records,
    }
    report['exit_code'] = int(any(r['result'] == 'FAIL' for r in records + boundary))
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({k: report[k] for k in ('total', 'supplementary_summary', 'all_comparisons', 'exit_code')}))
    return report['exit_code']


if __name__ == '__main__':
    raise SystemExit(main())
