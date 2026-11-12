#!/usr/bin/env python3
"""Strict mode over a graph edited by hand (trust/FREEZE-fix1.md, section B: T1 to T7, frozen before this was written).

    python3 trust/tests/tampered_graph.py          (after ./run.sh; no pipeline run, a few seconds)

The tampered graph is out/graph.json in which every node with `attrs.subject_kind` stores the attestation
{act: approved, kind: person, by: model:selftest-fixture}: a model's record with `person` written on it. Before the fix
round graphlint called it valid and `clausal trust --strict` under the built-in policy passed every proved verdict.
Everything runs in a scratch copy (the built-in policy is what a project with no `trust:` key gets, so the copy's
projects.yaml loses those keys); the tree is not touched. Writes trust/tests/tampered_graph.result.json.
"""
import copy
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SKIP = shutil.ignore_patterns("target", ".lake", ".tools", "mutation", "work", "__pycache__", "census", "review", "probe", "effort", "build")


def tamper(g: dict) -> dict:
    g = copy.deepcopy(g)
    for n in g["nodes"]:
        if "subject_kind" in n.get("attrs", {}):
            n["attrs"]["attestations"] = [{"act": "approved", "kind": "person", "by": "model:selftest-fixture", "on_behalf_of": None,
                                           "at": "2026-11-12T00:00:00+00:00", "scope": "x", "digest": n["interface"]["identity"],
                                           "evidence_kind": "model-asserted"}]
    return g


def main() -> int:
    G = json.loads((ROOT / "out" / "graph.json").read_text())
    n_proved = sum(v["code"].startswith("PROVED") for v in G["verdicts"])
    with tempfile.TemporaryDirectory() as d:
        c = Path(d) / "clausal"
        shutil.copytree(ROOT, c, ignore=SKIP, symlinks=True)
        run = lambda *a: subprocess.run([sys.executable, "-m", *a], cwd=c, capture_output=True, text=True)
        last = lambda r: (r.stdout.strip().splitlines() or [""])[-1]
        t1 = Path(d) / "tampered.graph.json"
        t1.write_text(json.dumps(tamper(G)))
        g2 = copy.deepcopy(G)
        rule = next(v for v in g2["verdicts"] if v["node"].startswith("group:rule:") and v["code"] == "PROVED-FOR-ALL")
        rule.update({"outcome": "pass", "unreviewed": []})
        t2 = Path(d) / "pass-empty.graph.json"
        t2.write_text(json.dumps(g2))
        # beyond the freeze: a proved scenario that keeps its pieces listed and drops only the old-glossary entries
        g3 = copy.deepcopy(G)
        froms = {e["from"] for e in g3["edges"] if e["relation"] == "composed_of"}
        sc = next(v for v in g3["verdicts"] if v["node"] in froms and v["code"].startswith("PROVED"))
        sc["unreviewed"] = [u for u in sc["unreviewed"] if u.startswith("piece:")]
        t3 = Path(d) / "glossary-dropped.graph.json"
        t3.write_text(json.dumps(g3))

        # beyond the freeze, and the other way round: a graph that says a PERSON approved every entry (well-formed: human: id,
        # kind person; on an old-glossary node the digest is the bound definition's, not the node's identity) and whose
        # proved verdicts list nothing unreviewed is a VALID graph. The lint must not refuse it (it did, for one run of this
        # fix round: control c10 caught it). That such a hand-written graph then passes strict mode is the unchecked claim
        # of a person's record (W9), stated in trust/README.md; it is not closed here.
        g4 = copy.deepcopy(G)
        for n in g4["nodes"]:
            if "subject_kind" in n.get("attrs", {}):
                own = "clausebook_entry" in n["attrs"]
                n["attrs"]["attestations"] = [{"act": "approved", "kind": "person", "by": "human:selftest-fixture", "on_behalf_of": None,
                                               "at": "2026-11-12T00:00:00+00:00", "scope": "x", "evidence_kind": "human-asserted",
                                               "digest": n["interface"]["identity"] if own else {"alg": "sha256-text", "value": "1" * 64}}]
        for v in g4["verdicts"]:
            if v["code"].startswith("PROVED"):
                v["unreviewed"] = []
        t4 = Path(d) / "person-claimed.graph.json"
        t4.write_text(json.dumps(g4))

        # T6 first: the policies projects.yaml names, the graph as it is
        r6 = run("clausal", "trust", "--strict")
        # the built-in policy from here on
        p = c / "projects.yaml"
        p.write_text("\n".join(l for l in p.read_text().splitlines() if not l.strip().startswith("trust:")) + "\n")
        r1 = run("clausal.graphlint", str(t1))
        r2 = run("clausal", "trust", "--graph", str(t1), "--strict")
        r5 = run("clausal", "trust", "--strict")
        r7 = run("clausal", "trust", "--graph", str(t2), "--strict")
        r8 = run("clausal", "trust", "--graph", str(t3), "--strict")
        r9 = run("clausal.graphlint", str(t4))
        # T3, T4: evaluate() itself, with no validation in front of it
        code = ("import json,sys\nfrom pathlib import Path\nfrom clausal import trust, projects\npr = projects.load()\n"
                "g = json.loads(Path(sys.argv[1]).read_text())\nout = {}\n"
                "for name, ov in (('built-in', None), ('person.yaml', Path('trust/tests/person.yaml')), ('model.yaml', Path('trust/tests/model.yaml'))):\n"
                "    r = trust.evaluate(g, pr, trust.policies(pr, ov))\n"
                "    out[name] = {'proved': len(r['verdicts']), 'pass': sum(x['strict'] == 'pass' for x in r['verdicts']), 'fail': r['strict_fail']}\n"
                "print(json.dumps(out))\n")
        r3 = subprocess.run([sys.executable, "-c", code, str(t1)], cwd=c, capture_output=True, text=True)
        ev = json.loads(r3.stdout) if r3.returncode == 0 else {}
    kind_errs = sum("is not the kind of its signer" in l for l in r1.stdout.splitlines())
    fails = lambda r: f"strict mode would fail {n_proved} proved verdicts" in last(r)
    checks = [
        ("T1 graphlint refuses the tampered graph and names the kind mismatch", r1.returncode == 1 and kind_errs > 0,
         f"exit {r1.returncode}; {kind_errs} errors name the mismatch"),
        ("T2 `clausal trust --graph <tampered> --strict`, built-in policy: exit 2, refused, no line says a verdict passes",
         r2.returncode == 2 and "REFUSED" in last(r2) and "proved verdicts pass" not in r2.stdout, f"exit {r2.returncode} | {last(r2)[:150]}"),
        ("T3 evaluate() on the tampered graph, built-in policy: 0 pass, all fail",
         ev.get("built-in") == {"proved": n_proved, "pass": 0, "fail": n_proved}, json.dumps(ev.get("built-in"))),
        ("T4 the same under person.yaml and under model.yaml: 0 pass under either",
         all(ev.get(k) == {"proved": n_proved, "pass": 0, "fail": n_proved} for k in ("person.yaml", "model.yaml")),
         json.dumps({k: ev.get(k) for k in ("person.yaml", "model.yaml")})),
        ("T5 `clausal trust --strict`, untampered graph, built-in policy: exit 1, every proved verdict fails", r5.returncode == 1 and fails(r5),
         f"exit {r5.returncode} | {last(r5)}"),
        ("T6 `clausal trust --strict`, untampered graph, the policies of projects.yaml: exit 1, every proved verdict fails", r6.returncode == 1 and fails(r6),
         f"exit {r6.returncode} | {last(r6)}"),
        ("T7 a proved Rule verdict rewritten `pass` with an empty `unreviewed`: exit 2, refused", r7.returncode == 2 and "REFUSED" in last(r7),
         f"exit {r7.returncode} | {last(r7)[:150]}"),
        ("(not in the freeze) a proved scenario whose `unreviewed` drops only its old-glossary entries: exit 2, the error names a phrase node",
         r8.returncode == 2 and any("rests on phrase:" in l for l in r8.stdout.splitlines()), f"exit {r8.returncode} | {r8.stdout.splitlines()[0][:150] if r8.stdout else ''}"),
        ("(not in the freeze) a well-formed graph in which a person is written as having approved every entry is still a valid graph",
         r9.returncode == 0, f"exit {r9.returncode} | {(r9.stdout.splitlines() or [''])[0][:150]}"),
    ]
    for what, ok, got in checks:
        print(f"  {'ok  ' if ok else 'FAIL'}  {what}   [{got}]")
    good = sum(ok for _, ok, _ in checks)
    print(f"{good} of {len(checks)} as expected ({n_proved} proved verdicts in out/graph.json)")
    (HERE / "tampered_graph.result.json").write_text(json.dumps(
        {"proved": n_proved, "checks": [{"what": w, "as_expected": bool(ok), "got": got} for w, ok, got in checks]}, indent=1, ensure_ascii=False) + "\n")
    return 0 if good == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
