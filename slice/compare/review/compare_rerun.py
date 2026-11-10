#!/usr/bin/env python3
"""Compare the review's rerun of a random sample of mutants (review/results/raw) with the builder's
raw results (results/raw), field by field, per mutant, arm and rule.

    python3 review/compare_rerun.py

Compared: the oracle's verdict; arm a, which Examples rows of each rule fail (and the literal
scenarios); arm b, each profile's status per rule and the shrunk row; arm c, each harness's status and
failed checks; arm d, the verdict of every scenario, which proof modules failed, and the search's
failing input. Confirmation by replay (harness/confirm.py) is not rerun: the builder's confirm records
are applied to both sides, so the comparison is of what the four arms themselves report.
Writes review/rerun_comparison.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMPARE = HERE.parent
sys.path.insert(0, str(HERE))
import recompute as R  # noqa: E402

MINE = HERE / "results" / "raw"
THEIRS = COMPARE / "results" / "raw"


def load(p):
    return json.loads(p.read_text()) if p.exists() else None


def main():
    sample = json.loads((HERE / "sample.json").read_text())
    conf = {p.stem: json.loads(p.read_text()) for p in (THEIRS / "confirm").glob("*.json")}
    base_t, base_m = load(THEIRS / "baseline.json"), load(MINE / "baseline.json")
    report = {"seed": sample["seed"], "sample": sample["sample"], "mutants": {}}
    if base_m:
        bdiff = []
        for r in R.RULES:
            rid = r["id"]
            for what, f in (("a rows", lambda b: {k: v["status"] for k, v in b["a"]["rows"].get(rid, {}).items()}),
                            ("b plain", lambda b: b["b"]["plain"]["rules"][rid]["status"]),
                            ("b edge", lambda b: b["b"]["edge"]["rules"][rid]["status"]),
                            ("c", lambda b: b["c"]["rules"][rid]["status"]),
                            ("d", lambda b: b["d"]["verdicts"].get(f"{r['crate']}.{rid}"))):
                if f(base_t) != f(base_m):
                    bdiff.append(f"{rid} {what}: builder {f(base_t)} / review {f(base_m)}")
        report["baseline"] = {"differences": bdiff, "secs_review": {"a": base_m["a"]["secs"], "b_plain": base_m["b"]["plain"]["secs"],
                                                                     "b_edge": base_m["b"]["edge"]["secs"], "c": base_m["c"]["secs"], "d": base_m["d"]["secs"]}}
        print("baseline:", "identical outcomes in every arm" if not bdiff else bdiff)
    else:
        print("baseline: not rerun yet")
    for mid in sample["sample"]:
        t, m = load(THEIRS / f"{mid}.json"), load(MINE / f"{mid}.json")
        if m is None:
            print(f"{mid}: not rerun yet")
            continue
        if "harness_error" in m:
            print(f"{mid}: HARNESS ERROR in rerun: {m['harness_error']}")
            report["mutants"][mid] = {"error": m["harness_error"]}
            continue
        diffs = []
        if t.get("viable") != m.get("viable"):
            diffs.append(f"viable {t.get('viable')} / {m.get('viable')}")
        if t["oracle"]["differs"] != m["oracle"]["differs"]:
            diffs.append(f"oracle differs {t['oracle']['differs']} / {m['oracle']['differs']}")
        ct = R.classify(t, base_t, conf)
        cm = R.classify(m, base_m or base_t, conf)
        for rid in ct:
            a, b = ct[rid], cm[rid]
            for k in ("a", "bp_status", "be_status", "c_status", "d_out"):
                if a[k] != b[k]:
                    diffs.append(f"{rid} {k}: builder {a[k]} / review {b[k]}")
            if sorted(x[0] for x in a["a_why"]) != sorted(x[0] for x in b["a_why"]):
                diffs.append(f"{rid} failing rows: builder {a['a_why']} / review {b['a_why']}")
            if sorted(a["c_checks"]) != sorted(b["c_checks"]):
                diffs.append(f"{rid} Kani failed checks: builder {a['c_checks']} / review {b['c_checks']}")
            for prof in ("plain", "edge"):
                rt = (t["b"][prof]["rules"].get(rid) or {}).get("row")
                rm = (m["b"][prof]["rules"].get(rid) or {}).get("row")
                if rt != rm:
                    diffs.append(f"{rid} b {prof} shrunk row: builder {rt} / review {rm}")
        # every scenario's verdict (literal and negative ones included) and the failed proof modules
        vt, vm = (t["d"].get("verdicts") or {}), (m["d"].get("verdicts") or {})
        for k in sorted(set(vt) | set(vm)):
            if vt.get(k) != vm.get(k):
                diffs.append(f"verdict {k}: builder {vt.get(k)} / review {vm.get(k)}")
        ft = sorted((t["d"].get("proofs") or {}).get("failed", []))
        fm = sorted((m["d"].get("proofs") or {}).get("failed", []))
        if ft != fm:
            diffs.append(f"failed proof modules differ: only builder {sorted(set(ft) - set(fm))}, only review {sorted(set(fm) - set(ft))}")
        st, sm = (t["d"].get("search") or {}), (m["d"].get("search") or {})
        for k in sorted(set(st) | set(sm)):
            bt, bm = (st.get(k) or {}).get("bad"), (sm.get(k) or {}).get("bad")
            if (bt or {}).get("values") != (bm or {}).get("values"):
                diffs.append(f"search counterexample {k}: builder {(bt or {}).get('values')} / review {(bm or {}).get('values')}")
        det_t = {a: sorted(r for r, o in ct.items() if o[a]) for a in ("a", "bp", "be", "c", "d")}
        det_m = {a: sorted(r for r, o in cm.items() if o[a]) for a in ("a", "bp", "be", "c", "d")}
        secs = {"builder": {"a": t["a"]["secs"], "bp": t["b"]["plain"]["secs"], "be": t["b"]["edge"]["secs"], "c": t["c"]["secs"], "d": t["d"].get("secs")},
                "review": {"a": m["a"]["secs"], "bp": m["b"]["plain"]["secs"], "be": m["b"]["edge"]["secs"], "c": m["c"]["secs"], "d": m["d"].get("secs")}}
        retried = [r for r, v in t["c"]["rules"].items() if v.get("retried")]
        report["mutants"][mid] = {"differences": diffs, "detected_by_builder": det_t, "detected_by_review": det_m,
                                  "same_detection": det_t == det_m, "secs": secs, "builder_kani_retried": retried}
        print(f"{mid}: {'IDENTICAL' if not diffs else str(len(diffs)) + ' differences'}; same detection per arm and rule: {det_t == det_m}"
              + (f"; builder's Kani retried: {retried}" if retried else ""))
        for d in diffs:
            print("    ", d)
    (HERE / "rerun_comparison.json").write_text(json.dumps(report, indent=1) + "\n")


if __name__ == "__main__":
    main()
