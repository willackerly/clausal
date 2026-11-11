#!/usr/bin/env python3
"""Reviewer (V2/V3 review, second pass): break ONE frame at a time in the scratch copy rv/ (its executable reading
in Frames/Check.lean, its definition in Frames/Frames.lean, or the defaults in Frames/Core.lean), run the pipeline
there (`./run.sh --no-rust --no-adequacy`: the cucumber runs and the adequacy note do not read the frame library),
record what catches it, restore the pristine file. Sequential: one pipeline at a time.
usage: fmut.py [ids...]"""
import json
import os
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RV = os.path.join(os.path.dirname(HERE), "rv")
OUT = os.path.join(HERE, "fmut")
ENV = dict(os.environ, PATH=os.path.expanduser("~/.elan/bin") + ":" + os.path.expanduser("~/.cargo/bin") + ":" + os.environ["PATH"])

M = [
    # executable second reading (Check.lean)
    ("X1", "Check", "checker drops D1: a call that gives no answer passes a claim about every call",
     "  | .every => false\n  | _ => true", "  | .every => true\n  | _ => true"),
    ("X2", "Check", "never_changes checker always true",
     "  on op s a fun _ s' => m s' a == m s a\n", "  on op s a fun _ s' => true\n"),
    ("X3", "Check", "exactly_when checker reads only 'if C then Q'",
     "  on op s a fun r _ => decide (cls r) == decide (C s a)", "  on op s a fun r _ => if C s a then decide (cls r) else true"),
    ("X4", "Check", "every_of checker reads 'some' for 'every'",
     ".all fun x => decide (P s' a x)", ".any fun x => decide (P s' a x)"),
    ("X5", "Check", "'rejected calls only' checker covers the ACCEPTED calls instead",
     "| .rejected => if op.accepted r then .notCovered else .answered r s'",
     "| .rejected => if op.accepted r then .answered r s' else .notCovered"),
    ("X6", "Check", "decreases_by checker drops its 'was at least f' guard (truncated subtraction)",
     "on op s a fun _ s' => f s a ≤ m s a && m s' a == m s a - f s a", "on op s a fun _ s' => m s' a == m s a - f s a"),
    ("X7", "Check", "at_most checker strict",
     "on op s a fun _ s' => !(f s a < m s' a)", "on op s a fun _ s' => m s' a < f s a"),
    # definitions (Frames.lean, Core.lean)
    ("Y1", "Core", "default no longer requires an answer (D1 dropped from the definition)",
     "| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s'", "| .every    => ∀ r s', op.run s a = some (r, s') → Q s a r s'"),
    ("Y2", "Frames", "never_changes definition vacuous",
     "op.HoldsAt (fun s a _ s' => m s' a = m s a) s a", "op.HoldsAt (fun s a _ s' => m s' a = m s' a) s a"),
    ("Y3", "Frames", "at_most definition strict",
     "op.HoldsAt (fun s a _ s' => m s' a ≤ f s a) s a", "op.HoldsAt (fun s a _ s' => m s' a < f s a) s a"),
    ("Y4", "Frames", "only_if definition reversed into 'if'",
     "op.HoldsAt (fun s a r _ => cls r → C s a) s a", "op.HoldsAt (fun s a r _ => C s a → cls r) s a"),
    ("Y5", "Frames", "exactly_when definition weakened to 'only if'",
     "op.HoldsAt (fun s a r _ => cls r ↔ C s a) s a", "op.HoldsAt (fun s a r _ => cls r → C s a) s a"),
]


def main(ids):
    os.makedirs(OUT, exist_ok=True)
    resf = os.path.join(OUT, "results.json")
    results = json.load(open(resf)) if os.path.exists(resf) else {}
    for mid, fname, what, old, new in M:
        if ids and mid not in ids:
            continue
        path = os.path.join(RV, "lean", "Frames", fname + ".lean")
        pristine = os.path.join(OUT, fname + ".lean.pristine")
        if not os.path.exists(pristine):
            shutil.copy2(path, pristine)
        src = open(pristine).read()
        n = src.count(old)
        if n != 1:
            results[mid] = {"what": what, "status": f"PATCH-NOT-APPLIED ({n} matches)"}
            json.dump(results, open(resf, "w"), indent=1, ensure_ascii=False)
            continue
        open(path, "w").write(src.replace(old, new))
        t = time.time()
        try:
            with open(os.path.join(OUT, mid + ".out"), "w") as f:
                p = subprocess.run(["./run.sh", "--no-rust", "--no-adequacy"], cwd=RV, env=ENV, stdout=f,
                                   stderr=subprocess.STDOUT, timeout=3600)
            rc = p.returncode
        finally:
            shutil.copy2(pristine, path)
        txt = open(os.path.join(OUT, mid + ".out")).read()
        o = os.path.join(RV, "out")
        def rd(n):
            q = os.path.join(o, n)
            return open(q).read() if os.path.exists(q) else ""
        rs, nr, ft, ln = rd("rsearch.log"), rd("new_sentences.log"), rd("frametests.log"), rd("links.log")
        diffs = [l.split("\t")[1] for l in rs.splitlines() if l.startswith("RSEARCH") and l.split("\t")[6] != "-"]
        ndiffs = [l.split("\t")[1] for l in nr.splitlines() if l.startswith("RSEARCH") and l.split("\t")[6] != "-"]
        fdis = [l.split("\t")[2] for l in ft.splitlines() if l.startswith("FTEST") and l.split("\t")[3] != l.split("\t")[4]]
        m = re.search(r"readings: (\d+) of (\d+) scenario readings proved equivalent.*?agree on (\d+) of (\d+)", txt)
        results[mid] = {
            "what": what, "file": fname, "exit": rc, "secs": round(time.time() - t),
            "build_failed": "lake build" in txt and rc != 0 and "RESULT" not in txt,
            "equivalent": (m.group(1) + " of " + m.group(2)) if m else None,
            "agree": (m.group(3) + " of " + m.group(4)) if m else None,
            "fixture_readings_with_diff": diffs, "heldout_readings_with_diff": ndiffs, "frametests_disagree": fdis,
            "links_errors": len(re.findall(r": error", ln)),
            "result_line": next((l for l in txt.splitlines() if l.startswith("RESULT")), None),
            "fatal_lines": [l.strip() for l in txt.splitlines() if "DISAGREE" in l or "disagree" in l][:6],
        }
        print(mid, rc, results[mid]["equivalent"], results[mid]["agree"], diffs[:3], ndiffs[:3], fdis[:3], flush=True)
        json.dump(results, open(resf, "w"), indent=1, ensure_ascii=False)
    # pristine tree, rebuilt
    with open(os.path.join(OUT, "restore.out"), "w") as f:
        p = subprocess.run(["./run.sh", "--no-rust", "--no-adequacy"], cwd=RV, env=ENV, stdout=f, stderr=subprocess.STDOUT, timeout=3600)
    print("restored; pristine run exit", p.returncode, flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
