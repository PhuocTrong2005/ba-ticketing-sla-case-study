"""Read-only audit of the second independent clean checkout."""
import hashlib
import json
import re
import socket
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLONE = ROOT / ".clean-start-portfolio-20261013b"
EVIDENCE = ROOT / "tests/evidence"


def read(name):
    return json.loads((EVIDENCE / name).read_text(encoding="utf8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def junit(name):
    root = ET.parse(EVIDENCE / name).getroot()
    suites = [root] if root.tag == "testsuite" else root.findall("testsuite")
    return {key: sum(int(s.attrib.get(key, 0)) for s in suites)
            for key in ("tests", "failures", "errors", "skipped")}


def main():
    baseline = read("portfolio-clean-start-baseline-20261013.json")
    run = read("portfolio-clean-start-20261013b-run.json")
    proto = read("prototype-ux-20261013-022543.json")
    newman = read("newman-20261013-022639-428089-run.json")
    manifest = read("portfolio-clean-start-20261013b-artifacts.json")
    allowed = {"README.md", "TASKS.md", "api/README.md", "prototype/README.md",
               "docs/ac-traceability.md", "docs/backend-running.md", "docs/decision-log.md",
               "docs/release-checklist.md", "docs/traceability.md"}
    source_changed = [p for p, h in run["source_sha256"].items() if digest(CLONE / p) != h]
    artifact_changed = [p["file"] for p in manifest["files"] if digest(ROOT / p["file"]) != p["sha256"]]
    protected_changed = [p for p, h in baseline["files"].items()
                         if p not in allowed and (not (ROOT / p).exists() or digest(ROOT / p) != h)]
    database_changed = [p for p, h in baseline["databases"].items() if digest(ROOT / p) != h]
    links, missing = [], []
    for rel in ("AGENTS.md", "README.md", "api/README.md", "prototype/README.md",
                "docs/release-checklist.md", "docs/backend-running.md"):
        path = CLONE / rel
        for found in re.findall(r"\]\(([^)]+)\)|<img[^>]+src=\"([^\"]+)\"", path.read_text(encoding="utf8")):
            dest = next(x for x in found if x).split("#", 1)[0]
            if not dest or re.match(r"^(https?://|mailto:)", dest):
                continue
            links.append([rel, dest])
            if not (path.parent / dest).resolve().exists():
                missing.append([rel, dest])
    newman_xml = ET.parse(EVIDENCE / "newman-20261013-022639-428089.xml").getroot()
    newman_junit = sum(int(x.attrib["tests"]) for x in newman_xml.findall("testsuite"))
    ports = (8000, 8765, int(newman["base_url"].rsplit(":", 1)[1]),
             int(proto["base_url"].split(":")[2].split("/")[0]))
    closed = {}
    for port in ports:
        with socket.socket() as sock:
            closed[str(port)] = sock.connect_ex(("127.0.0.1", port)) != 0
    result = {
        "checked_commit": run["commit"], "os": run["os"],
        "stable_python": run["stable_python_version"], "fresh_python": run["new_python_version"],
        "node": newman["node_version"], "newman": newman["newman_version"],
        "initial_ignored_state": run["initial_ignored_state"],
        "clone_changed_tracked_source": source_changed,
        "artifact_mismatches": artifact_changed,
        "original_protected_changes": protected_changed,
        "original_database_changes": database_changed,
        "run_project_preserved": digest(ROOT / "Run Project.txt") == baseline["files"]["Run Project.txt"],
        "published_links_checked": len(links), "missing_published_links": missing,
        "pytest_first": junit("portfolio-clean-start-20261013b-junit.xml"),
        "pytest_retry": junit("portfolio-clean-start-20261013b-junit-retry.xml"),
        "prototype_cases_passed": sum(x["status"] == "PASS" for x in proto["harness"]["results"]),
        "prototype_cases_total": len(proto["harness"]["results"]),
        "local_static_smoke_checks": len(run["prototype_documented_static_smoke"]["checks"]),
        "prototype_historical_auditor_passed": read("prototype-ux-audit-20261013-022602.json")["passed"],
        "newman_requests": newman["stats"]["requests"],
        "newman_assertions": newman["stats"]["assertions"],
        "newman_junit_assertions": newman_junit,
        "newman_failure_count": len(newman["failures"]),
        "newman_fresh_database": not newman["database_existed_before_start"] and newman["database_retained"],
        "newman_owned_server_stopped": newman["owned_server_stopped"],
        "owned_ports_closed": closed,
        "backend_http": run["backend_http"],
        "owned_browser_stopped": run["owned_browser_stopped"],
        "published_instructions_fully_passed": False,
        "issues": {"pip_first": "environment: sandbox blocks PyPI network",
                   "pytest_first": "environment: sandbox denies pytest Temp directory",
                   "prototype_auditor": "documentation DOC-CS-01: historical task baseline expects files absent from fresh clone",
                   "implementation": "none observed"},
    }
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=CLONE, text=True).strip() == run["commit"]
    assert not (source_changed or artifact_changed or protected_changed or database_changed or missing)
    assert result["run_project_preserved"] and all(closed.values())
    assert result["pytest_retry"] == {"tests": 181, "failures": 0, "errors": 0, "skipped": 0}
    assert result["prototype_cases_passed"] == result["prototype_cases_total"] == 110
    assert result["newman_requests"]["total"] == 191 and result["newman_assertions"]["total"] == newman_junit == 514
    assert result["newman_failure_count"] == 0 and result["newman_fresh_database"]
    result["audit_passed"] = True
    out = EVIDENCE / "portfolio-clean-start-20261013b-audit.json"
    assert not out.exists()
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf8")
    print(out)


if __name__ == "__main__":
    main()
