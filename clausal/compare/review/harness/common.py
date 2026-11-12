"""Shared pieces of the K2 comparison harness."""
from __future__ import annotations

import json
import os
import re
import signal
import subprocess
import time
from pathlib import Path

COMPARE = Path(__file__).resolve().parent.parent.parent   # slice/compare  (REVIEW COPY: harness lives in review/harness)
SLICE = COMPARE.parent
REVIEW = COMPARE / "review"
WORK = REVIEW / "work"                                     # review scratch copies, not compare/work
SNAPSHOT = WORK / "snapshot"                               # independent git-archive snapshot of SLICE_COMMIT
RESULTS = REVIEW / "results"                               # review results, never compare/results
MUTANTS = COMPARE / "mutants"                              # read only
ENV_PATH = f"{os.environ['HOME']}/.elan/bin:{os.environ['HOME']}/.cargo/bin:" + os.environ.get("PATH", "")

RULES = json.loads((COMPARE / "rules.json").read_text())["rules"]
RULE_IDS = [r["id"] for r in RULES]
RULE = {r["id"]: r for r in RULES}


def sh(cmd: str, cwd, timeout: float = 900):
    """Run a shell command in its own process group; on timeout kill the whole group.
    Returns (exit status or None on timeout, output, seconds)."""
    env = dict(os.environ, PATH=ENV_PATH)
    t0 = time.time()
    p = subprocess.Popen(cmd, cwd=str(cwd), shell=True, executable="/bin/bash", stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True, start_new_session=True, env=env)
    try:
        out, _ = p.communicate(timeout=timeout)
        return p.returncode, out, round(time.time() - t0, 2)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        try:
            out, _ = p.communicate(timeout=20)
        except Exception:
            out = ""
        return None, out or "", round(time.time() - t0, 2)


def scenario_spans(feature_text: str):
    """[(first line, last line, id, tags, 'Scenario Outline' | 'Scenario', title)], 1-based lines, from the @id: tags."""
    lines = feature_text.splitlines()
    starts = []
    for k, l in enumerate(lines, 1):
        m = re.match(r"\s*(@.*)$", l)
        if m and "@id:" in l:
            tags = l.split()
            sid = next(t for t in tags if t.startswith("@id:"))[4:]
            head = next(x for x in lines[k:] if x.strip().startswith("Scenario"))
            kind = "Scenario Outline" if head.strip().startswith("Scenario Outline") else "Scenario"
            starts.append((k, sid, tags, kind, head.split(":", 1)[1].strip()))
    out = []
    for n, (k, sid, tags, kind, title) in enumerate(starts):
        end = starts[n + 1][0] - 1 if n + 1 < len(starts) else len(lines)
        out.append((k, end, sid, tags, kind, title))
    return out


def feature_index(root: Path):
    """{feature file name: spans} for the three feature files of a slice tree."""
    return {p.name: scenario_spans(p.read_text()) for p in sorted((root / "features").glob("*.feature"))}


def rows_by_scenario(cucumber_json: Path, index):
    """{scenario id: {line: 'pass' | 'fail' | 'skipped'}} from a Cucumber JSON file."""
    out: dict = {}
    if not cucumber_json.exists() or not cucumber_json.read_text().strip():
        return out
    try:
        data = json.loads(cucumber_json.read_text())
    except json.JSONDecodeError:
        return out
    for f in data:
        name = f["uri"].rsplit("/", 1)[-1]
        for e in f.get("elements", []):
            st = [s["result"]["status"] for s in e["steps"]]
            status = "fail" if "failed" in st else "pass" if all(x == "passed" for x in st) else "skipped"
            sid = next((s[2] for s in index.get(name, []) if s[0] <= e["line"] <= s[1]), None)
            # a failed Given means the row is outside the Givens; cucumber reports it as failed too
            msg = " ".join(s["result"].get("error_message", "") for s in e["steps"] if s["result"]["status"] == "failed")
            out.setdefault(sid or f"?{name}:{e['line']}", {})[str(e["line"])] = {"status": status, "message": msg[:300]}
    return out
