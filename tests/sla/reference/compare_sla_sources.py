"""Compare repository scenarios to preserved ZIP source; never calculate SLA."""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("source", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    raw_repo, raw_source = args.repo.read_bytes(), args.source.read_bytes()
    repo = json.loads(raw_repo, object_pairs_hook=unique_object)
    source = json.loads(raw_source, object_pairs_hook=unique_object)
    rows = source["scenarios"]
    expected_ids = {f"SLA-{i:02}" for i in range(1, 70)}
    for values in (repo, rows):
        if len(values) != 69 or {r["scenario_id"] for r in values} != expected_ids:
            raise ValueError("Expected 69 unique scenario IDs")
    by_id = {r["scenario_id"]: r for r in rows}
    records = []
    business_count = 0
    for r in repo:
        s = by_id[r["scenario_id"]]
        fields = set(r) | set(s)
        business = {k for k in fields if k.startswith("expected_")} | {"created_at", "as_of", "policy_id", "events", "resolution_result_final"}
        business_count += len(business)
        differences = []
        for key in sorted(fields):
            if (key in r) != (key in s) or canonical(r.get(key)) != canonical(s.get(key)):
                differences.append({"field": key, "category": "business" if key in business else "metadata_or_description", "repo_present": key in r, "source_present": key in s, "repo": r.get(key), "source": s.get(key)})
        records.append({"scenario_id": r["scenario_id"], "business_fields_compared": sorted(business), "differences": differences})
    report = {
        "kind": "Structural source comparison, not SLA reference calculations",
        "executed_at": datetime.now(timezone(timedelta(hours=7))).isoformat(timespec="seconds"),
        "sha256": {args.repo.as_posix(): sha(raw_repo), args.source.as_posix(): sha(raw_source), "tests/sla/reference/compare_sla_sources.py": sha(Path(__file__).read_bytes())},
        "root_mapping": {"repo": "$ (array)", "source": "$.scenarios (array)", "source_only": "$.metadata", "per_scenario_field_mapping": "identity; no renamed fields"},
        "source_root_metadata": source["metadata"],
        "byte_equal": raw_repo == raw_source,
        "all_scenarios_structurally_equal_including_metadata_and_order": canonical(repo) == canonical(rows),
        "canonical_scenarios_sha256": {"repo": sha(canonical(repo)), "source": sha(canonical(rows))},
        "format": {"repo_bytes": len(raw_repo), "source_bytes": len(raw_source), "repo_lines": len(raw_repo.splitlines()), "source_lines": len(raw_source.splitlines()), "repo_bom": raw_repo.startswith(b"\xef\xbb\xbf"), "source_bom": raw_source.startswith(b"\xef\xbb\xbf")},
        "scenario_count": len(records),
        "business_field_equality_comparisons": business_count,
        "business_differences": sum(d["category"] == "business" for r in records for d in r["differences"]),
        "metadata_or_description_differences_within_scenarios": sum(d["category"] != "business" for r in records for d in r["differences"]),
        "adapter_required": False,
        "scenarios": records,
    }
    report["exit_code"] = int(any(r["differences"] for r in records))
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("scenario_count", "business_field_equality_comparisons", "business_differences", "metadata_or_description_differences_within_scenarios", "all_scenarios_structurally_equal_including_metadata_and_order", "exit_code")}))
    return report["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
