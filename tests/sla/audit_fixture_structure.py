"""Read-only fixture/schema audit. No SLA calculator or reference-checker replacement.

Run from the repository root. Exit 0 means structural checks passed only.
Expected values are inspected for shape/types, never recomputed or changed.
"""

import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import platform
import re
import sys


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError(f"Duplicate JSON key: {key}")
        obj[key] = value
    return obj


def timestamp(value, raw=False):
    pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}" + (r"(?:\.\d+)?" if raw else "") + r"\+07:00"
    if not isinstance(value, str) or not re.fullmatch(pattern, value):
        raise ValueError(f"Invalid +07:00 timestamp: {value!r}")
    return datetime.fromisoformat(value)


def walk(value, path=""):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key, item, f"{path}/{key}"
            yield from walk(item, f"{path}/{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk(item, f"{path}/{index}")


def coverage_table(path):
    section = path.read_text(encoding="utf-8").split("## Mười hai nhóm kịch bản tối thiểu", 1)[1].split("## Điều kiện hoàn tất", 1)[0]
    groups = {}
    for line in section.splitlines():
        if not re.match(r"\| \d+ \|", line):
            continue
        cells = line.split("|")
        ids = []
        for first, last in re.findall(r"SLA-(\d+)(?:…SLA-(\d+))?", cells[3]):
            ids.extend(f"SLA-{n:02}" for n in range(int(first), int(last or first) + 1))
        groups[int(cells[1])] = ids
    return groups


def audit_case(case):
    errors = []
    checks = 0

    def check(condition, message):
        nonlocal checks
        checks += 1
        if not condition:
            errors.append(message)

    try:
        check(case["policy_id"] in {"HIGH", "NORMAL"}, "policy_id")
        created = timestamp(case["created_at"])
        as_of = timestamp(case["as_of"])
        check(as_of >= created, "as_of before created_at")
        check(case["review_status"] == "verified", "review_status")
        groups = case["coverage_groups"]
        check(bool(groups) and all(type(g) is int and 1 <= g <= 12 for g in groups)
              and len(groups) == len(set(groups)), "coverage_groups")
        check(case["drafted_by"] == "AI advisor", "drafted_by")
        check(case["verified_by"] == "project owner", "verified_by")
        timestamp(case["verified_at"])
        for key in ("verification_method", "verification_basis", "verification_evidence_status", "owner_confirmation", "calculation_note"):
            check(isinstance(case.get(key), str) and bool(case[key]), f"missing {key}")
        check(case.get("blocked_by") == [], "blocked_by is not empty")
        check(all(v is None for v in case.get("owner_results", {}).values()), "owner_results contains claimed personal calculations")
        check(type(case["resolution_result_final"]) is bool, "resolution_result_final type")
        for clock in ("first_response", "resolution"):
            for suffix in ("due_at", "consumed_seconds", "remaining_seconds", "status", "warning_level", "sla_status_at_assignment"):
                check(f"expected_{clock}_{suffix}" in case, f"missing expected_{clock}_{suffix}")
            check(case[f"expected_{clock}_status"] in {"pending", "met", "breached"}, f"{clock} status enum")
            check(case[f"expected_{clock}_warning_level"] in {"none", "soft", "emphasized", "due", "breached"}, f"{clock} warning enum")
        for key in ("expected_resolution_intervals", "expected_reviews", "expected_rejected_actions"):
            check(isinstance(case.get(key), list), f"{key} type")
        previous = (created, 0)
        future_events = []
        steps = []
        allowed = {"agent_assigned", "agent_public_reply", "resolved", "status_waiting", "customer_public_message", "customer_confirm", "customer_reject", "internal_note", "resolved_attempt", "review_completed"}
        for event in case["events"]:
            at = timestamp(event["at"])
            seq = event["seq"]
            check(type(seq) is int and seq > 0, "event seq must be positive integer")
            check((at, seq) > previous and seq > previous[1], "event timestamp/seq order")
            check(event["type"] in allowed, "event type")
            check("event_id" not in event, "fixture input must use seq, not client event_id")
            if "at_raw" in event:
                check(timestamp(event["at_raw"], raw=True).replace(microsecond=0) == at, "raw timestamp truncation")
            previous = (at, seq)
            steps.append((seq, at))
            if at > as_of:
                future_events.append(seq)
        for action in case["expected_rejected_actions"]:
            at = timestamp(action["at"])
            seq = action["step_seq"]
            check(type(seq) is int and seq > 0 and at >= created, "rejected step seq/time")
            check(action["error_code"] in {"REVIEW_REQUIRED", "INVALID_TICKET_STATE", "TICKET_CLOSED", "TICKET_ALREADY_ASSIGNED", "AGENT_CAPACITY_REACHED"}, "rejected error code")
            steps.append((seq, at))
        check(len({s for s, _ in steps}) == len(steps), "duplicate accepted/rejected step seq")
        ordered = sorted(steps)
        check(all(a[1] <= b[1] for a, b in zip(ordered, ordered[1:])), "combined accepted/rejected step order")
        for key, value, path in walk(case):
            if value is None:
                continue
            if key.endswith("_seconds") or key == "business_seconds_as_of":
                check(type(value) is int and value >= 0, f"integer seconds: {path}")
            if key.endswith("_at") or key in {"at", "as_of"}:
                timestamp(value)
    except (KeyError, ValueError, TypeError) as exc:
        errors.append(f"Schema error: {exc}")
        future_events = []
    return {"scenario_id": case.get("scenario_id"), "structural_status": "FAIL" if errors else "PASS", "structural_assertions": checks, "errors": errors, "events_after_as_of_allowed": future_events, "expected_values_recomputed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    coverage = Path("docs/spec/scenario-coverage.md")
    report = {"kind": "fixture_structure_only", "executed_at": datetime.now(timezone(timedelta(hours=7))).isoformat(timespec="seconds"), "executor": "Codex AI assistant running local Python on behalf of project owner", "python_version": platform.python_version(), "python_executable": sys.executable, "command": "python " + " ".join(sys.argv), "cwd": str(Path.cwd()), "sha256": {args.fixture.as_posix(): sha256(args.fixture), Path(__file__).relative_to(Path.cwd()).as_posix(): sha256(__file__), coverage.as_posix(): sha256(coverage)}, "errors": [], "reference_check": {"status": "NOT_RUN_MISSING_SOURCE", "pass": None, "fail": None, "comparisons": None, "exit_code": None, "missing": ["SLA_Verification_Package.zip", "validate_sla_reference.py"]}, "limitations": ["No SLA calculation or expected_* correctness check", "No comparison with package fixture; package unavailable", "No backend/API/SQL/prototype/concurrency execution", "Coverage group presence does not prove all branches covered", "Provenance strings checked for presence; original verification artefacts unavailable"]}
    try:
        data = json.loads(args.fixture.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object)
        scenarios = data if isinstance(data, list) else data["scenarios"]
        ids = [s["scenario_id"] for s in scenarios]
        if Counter(ids) != Counter(f"SLA-{i:02}" for i in range(1, 70)):
            report["errors"].append("Expected exactly 69 unique IDs SLA-01 through SLA-69")
        report["cases"] = [audit_case(s) for s in scenarios]
        groups = coverage_table(coverage)
        declared = {g: [s["scenario_id"] for s in scenarios if g in s.get("coverage_groups", [])] for g in range(1, 13)}
        report["coverage_table"] = groups
        report["fixture_coverage_groups"] = declared
        report["documented_additional_links"] = {g: sorted(set(groups.get(g, [])) - set(declared[g])) for g in declared}
        if set(groups) != set(declared) or any(not groups.get(g) or not declared[g] for g in declared):
            report["errors"].append("Missing coverage group")
        verified = {s["scenario_id"] for s in scenarios if s.get("review_status") == "verified"}
        if any(set(ids) - verified for ids in groups.values()):
            report["errors"].append("Coverage links a missing/unverified scenario")
        for group, ids in declared.items():
            if set(ids) - set(groups.get(group, [])):
                report["errors"].append(f"Coverage table omits declared group {group} IDs")
        report["provenance_values"] = {k: dict(Counter(json.dumps(s.get(k), ensure_ascii=False, sort_keys=True) for s in scenarios)) for k in ("drafted_by", "reviewed_by", "verified_by", "verified_at", "verification_method", "verification_basis", "verification_evidence_status", "owner_confirmation")}
        report["branch_inventory"] = {"maximum_customer_rejections_in_events": max(sum(e["type"] == "customer_reject" for e in s["events"]) for s in scenarios), "rejected_action_codes": sorted({a["error_code"] for s in scenarios for a in s["expected_rejected_actions"]}), "created_on_sunday": [s["scenario_id"] for s in scenarios if timestamp(s["created_at"]).weekday() == 6], "running_resolution_remaining_3600_or_900": [s["scenario_id"] for s in scenarios if s["expected_ticket_state"] in {"New", "In Progress"} and s["expected_resolution_remaining_seconds"] in {3600, 900}]}
    except (ValueError, KeyError, TypeError) as exc:
        report["errors"].append(str(exc))
    cases = report.get("cases", [])
    report["summary"] = {"cases": len(cases), "structural_pass": sum(c["structural_status"] == "PASS" for c in cases), "structural_fail": sum(c["structural_status"] == "FAIL" for c in cases), "structural_assertions": sum(c["structural_assertions"] for c in cases), "global_errors": len(report["errors"])}
    report["exit_code"] = int(bool(report["errors"]) or any(c["errors"] for c in cases))
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"summary": report["summary"], "exit_code": report["exit_code"], "reference_check": report["reference_check"]["status"]}))
    return report["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
