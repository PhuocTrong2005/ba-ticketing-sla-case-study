import json
from pathlib import Path
import pytest
from backend.sla import replay, deadline, work_seconds, iso

ROWS = json.loads((Path(__file__).parents[1] / 'sla/sla-scenarios.json').read_text())


def fixture_result(result):
    data = {}
    for clock, values in result['sla'].items():
        for field in ('due_at','consumed_seconds','remaining_seconds','status','warning_level'):
            data[f'expected_{clock}_{field}'] = values[field]
    for clock in ('first_response','resolution'):
        field = f'{clock}_sla_status_at_assignment'
        data['expected_' + field] = result['snapshot'][field] if result['snapshot'] else None
    data.update(expected_resolution_intervals=result['resolution_intervals'], expected_ticket_state=result['state'], expected_rejection_count=result['rejection_count'], expected_open_review=result['open_review'], resolution_result_final=result['resolution_result_final'])
    data['expected_reviews'] = [{k:v for k,v in review.items() if k in ('review_key','requested_at','completed_at','wait_calendar_seconds','wait_overlap_seconds','breach_context')} for review in result['reviews']]
    return data


@pytest.mark.parametrize('row', ROWS, ids=[r['scenario_id'] for r in ROWS])
def test_verified_fixture(row):
    assert row['review_status'] == 'verified'
    actual = fixture_result(replay(row['created_at'], row['policy_id'], row['events'], row['as_of']))
    for field, value in actual.items():
        assert value == row[field], f"{row['scenario_id']} {field}: {value!r} != {row[field]!r}"


def test_exact_close_and_weekend_calendar():
    assert iso(deadline('2026-10-05T16:00:00+07:00',3600)) == '2026-10-05T17:00:00+07:00'
    assert iso(deadline('2026-10-09T16:59:00+07:00',3600)) == '2026-10-12T08:59:00+07:00'
    assert work_seconds('2026-10-09T17:00:00+07:00','2026-10-12T08:00:01+07:00') == 1


def test_timezone_wheel_fallback_without_system_iana_database():
    import os, subprocess, sys
    environment = {**os.environ, 'PYTHONTZPATH': ''}
    command = "from backend.sla import deadline, iso; print(iso(deadline('2026-10-09T16:59:00+07:00',3600)))"
    result = subprocess.run([sys.executable,'-c',command],env=environment,capture_output=True,text=True)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == '2026-10-12T08:59:00+07:00'
