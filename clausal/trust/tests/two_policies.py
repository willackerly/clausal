#!/usr/bin/env python3
"""The W3 test (trust/FREEZE.md section 5): two policies over one tree give different strict outcomes and byte-identical evidence.

    python3 trust/tests/two_policies.py            (after ./run.sh or ./run.sh --quick: it needs out/ and build/)

Everything runs in a scratch copy of clausal/ (sources, out/, build/; no target/, no .lake/), so nothing here writes to the tree
and no attestation is left in it. In the copy `python3 -m clausal report --strict --trust-policy F` is run once per policy: the
real report step, which rebuilds out/graph.json from the run's logs each time.

  Pair 1, the tree as committed (whatever records it holds):
      trust/tests/person.yaml   every entry under a proved verdict approved or reviewed by a person root
      trust/tests/open.yaml     nothing about meaning
  Pair 2, the copy after `clausal attest all --act reviewed --as model:selftest-fixture` (a FIXTURE model, in the copy only):
      trust/tests/person.yaml
      trust/tests/model.yaml    the same requirements, admitting a person or a model

"Evidence" is out/graph.json, all of it except `generated_at` (the clock). Writes trust/tests/two_policies.result.json.
Exit 0 iff every frozen expectation holds.
"""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SKIP = shutil.ignore_patterns("target", ".lake", ".tools", "mutation", "work", "__pycache__", "census", "review", "probe", "effort")


def report(root: Path, policy: str) -> dict:
    r = subprocess.run([sys.executable, "-m", "clausal", "report", "--strict", "--trust-policy", policy], cwd=root, capture_output=True, text=True)
    raw = (root / "out" / "graph.json").read_text()
    g = json.loads(raw)
    tr = json.loads((root / "out" / "trust.json").read_text())
    clock = g.pop("generated_at")
    body = raw.replace(json.dumps(clock), '""', 1)            # the file's bytes with the clock blanked
    proved = [v for v in g["verdicts"] if v["code"].startswith("PROVED")]
    kinds = {}
    for e in g["edges"]:
        for x in e["evidence"]:
            kinds[x["kind"]] = kinds.get(x["kind"], 0) + 1
    return {"policy": policy, "exit": r.returncode,
            "result_line": next((l for l in reversed(r.stdout.splitlines()) if l.startswith("RESULT")), ""),
            "errors": [l for l in r.stdout.splitlines() if l.startswith("ERROR")],
            "graph_bytes_sha256": hashlib.sha256(body.encode()).hexdigest(), "graph_sha256": tr["graph_sha256"],
            "codes": {v["node"] + "#" + str(k): v["code"] for k, v in enumerate(g["verdicts"])},
            "proved": len(proved), "proved_unreviewed": sum(bool(v.get("unreviewed")) for v in proved),
            "proved_outcomes": sorted({v["outcome"] for v in proved}),
            "evidence_on_edges": kinds,
            "strict_pass": sum(x["strict"] == "pass" for x in tr["verdicts"]), "strict_fail": tr["strict_fail"],
            "model_only": sum("MEANING-MODEL-ONLY" in x["flags"] for x in tr["verdicts"]),
            "strict_lines": sum(l.startswith("STRICT: ") for l in r.stdout.splitlines())}


def main() -> int:
    if not (ROOT / "out" / "audit.log").exists():
        print("out/audit.log is missing: run ./run.sh --quick first")
        return 2
    with tempfile.TemporaryDirectory() as d:
        copy = Path(d) / "clausal"
        shutil.copytree(ROOT, copy, ignore=SKIP, symlinks=True)
        shutil.copytree(ROOT / "mutation", copy / "mutation", ignore=shutil.ignore_patterns("logs", "__pycache__"))     # the report reads results.json
        a1, a2 = report(copy, "trust/tests/person.yaml"), report(copy, "trust/tests/open.yaml")
        r = subprocess.run([sys.executable, "-m", "clausal", "attest", "all", "--act", "reviewed", "--as", "model:selftest-fixture",
                            "--scope", "W3 test fixture: written by trust/tests/two_policies.py in a scratch copy; no model reviewed anything"],
                           cwd=copy, capture_output=True, text=True)
        attested = sum(l.startswith("attested ") for l in r.stdout.splitlines())
        if r.returncode != 0:
            print(r.stdout[-2000:] + r.stderr[-2000:])
            return 1
        b1, b2 = report(copy, "trust/tests/person.yaml"), report(copy, "trust/tests/model.yaml")
    in_tree = sorted(str(p.relative_to(ROOT)) for p in list(ROOT.glob("clausebook/**/*.attest.json")) + list(ROOT.glob("glossary.attest.json")))
    n = a1["proved"]
    checks = [
        ("pair 1: under person.yaml strict fails every proved verdict and the run exits 1", a1["strict_fail"] == n and a1["strict_pass"] == 0 and a1["exit"] == 1 and n > 0),
        ("pair 1: under open.yaml strict passes every proved verdict and the run exits 0", a2["strict_fail"] == 0 and a2["strict_pass"] == n and a2["exit"] == 0),
        ("pair 1: out/graph.json is byte-identical under the two policies (clock excepted)", a1["graph_bytes_sha256"] == a2["graph_bytes_sha256"]),
        ("pair 1: every verdict code is identical", a1["codes"] == a2["codes"]),
        ("pair 2: the fixture model attested every entry in the copy", attested > 0),
        ("pair 2: under person.yaml strict still fails every proved verdict (a model's record never meets a requirement for a person)",
         b1["strict_fail"] == n and b1["strict_pass"] == 0 and b1["exit"] == 1),
        ("pair 2: under model.yaml strict passes every proved verdict, each flagged MEANING-MODEL-ONLY, and the run exits 0",
         b2["strict_fail"] == 0 and b2["strict_pass"] == n and b2["model_only"] == n and b2["exit"] == 0),
        ("pair 2: out/graph.json is byte-identical under the two policies (clock excepted)", b1["graph_bytes_sha256"] == b2["graph_bytes_sha256"]),
        ("pair 2: every verdict code is identical, and identical to pair 1", b1["codes"] == b2["codes"] == a1["codes"]),
        ("pair 2: the graph carries the model's records as model-asserted evidence and no human-asserted evidence",
         b1["evidence_on_edges"].get("model-asserted", 0) > 0 and b1["evidence_on_edges"].get("human-asserted", 0) == a1["evidence_on_edges"].get("human-asserted", 0)),
        ("pair 2: in that graph every proved verdict still lists unreviewed entries and none is `pass`",
         b1["proved_unreviewed"] == n and "pass" not in b1["proved_outcomes"]),
        ("no report had an ERROR line", not (a1["errors"] or a2["errors"] or b1["errors"] or b2["errors"])),
    ]
    for what, ok in checks:
        print(f"  {'ok  ' if ok else 'FAIL'} {what}")
    strip = lambda x: {k: v for k, v in x.items() if k != "codes"}
    res = {"pair_1_tree_as_committed": [strip(a1), strip(a2)], "pair_2_fixture_model_attested_everything": [strip(b1), strip(b2)],
           "entries_attested_in_the_copy": attested, "attestation_stores_in_the_tree_for_entries": in_tree,
           "verdicts": len(a1["codes"]), "checks": [{"what": w, "ok": bool(ok)} for w, ok in checks]}
    (HERE / "two_policies.result.json").write_text(json.dumps(res, indent=1) + "\n")
    print(f"pair 1: person.yaml strict fails {a1['strict_fail']} of {n} proved verdicts (exit {a1['exit']}); open.yaml fails {a2['strict_fail']} (exit {a2['exit']}); "
          f"graph {a1['graph_bytes_sha256'][:16]} / {a2['graph_bytes_sha256'][:16]}")
    print(f"pair 2 ({attested} entries attested by the fixture model, in the copy): person.yaml strict fails {b1['strict_fail']} of {n} (exit {b1['exit']}); "
          f"model.yaml fails {b2['strict_fail']}, MEANING-MODEL-ONLY on {b2['model_only']} (exit {b2['exit']}); graph {b1['graph_bytes_sha256'][:16]} / {b2['graph_bytes_sha256'][:16]}")
    print(f"{sum(bool(ok) for _, ok in checks)} of {len(checks)} expectations hold")
    return 0 if all(ok for _, ok in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
