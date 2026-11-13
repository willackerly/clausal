#!/usr/bin/env python3
"""SENSITIVITY OF ARM A1 TO THE FROZEN-ONLY CUES (fix round of plan node L1c). NOT AN ARM, NOT A SECOND A1.

Arm A1 (compose_tests/l4r_a1/) was run once on the 48 frozen sentences with the composer frozen at 3147bb4, and stays the
measurement. A reviewer then found that 21 entries of the cue tables match a frozen sentence and no development sentence
(compose_tests/cue_audit.json), and that at least one "right after questions" depends on one of them ("larger"). This
script answers one question: WHAT ARE A1'S TALLIES WITHOUT THOSE ENTRIES?

    P=<a private directory>
    cp -R trials/sentences $P/sentences
    bash clausal/mutation/workcopy.sh $P/sentences/work/clausal
    tools/sem.sh 3 -- python3 clausal/compose_tests/l4r_sens.py $P/sentences --smoke   # plumbing, three sentences that are not of the 48
    tools/sem.sh 3 -- python3 clausal/compose_tests/l4r_sens.py $P/sentences           # the run; writes l4r_a1_sens/{results.json,REPORT.md}
    python3 clausal/compose_tests/l4r_sens.py --print                                  # the report again

FROZEN BEFORE THE RUN (this file, ablate.py and cue_audit.json are committed before it):
  - what is removed: exactly the list `frozen_only` of compose_tests/cue_audit.json, by the rules of compose_tests/ablate.py,
    in the running process. No file of the composer is changed.
  - everything else is arm A1's: l4r.run_main is called as it is (the same sentences, gold readings, dialogue, oracle
    author, replay, judging and tallies; l4r.py is not changed). The gold file is copied from l4r_a1/ and its hash checked.
  - the control: compose_tests/dev_sens.py runs the development set with the same entries removed and compares with the
    committed development results. No removed entry matches a development sentence, so every row should be the same; a
    row that differs would mean the removal does more than it says.
  - what is reported: the same table beside A1's, and every sentence whose row or whose first answer differs from A1's.

WHAT THIS IS NOT. The removed composer is not a better composer and is not adopted: "frozen-only" is a mechanical test
(see cue_audit.py), it removes plain English ("at most", "any", "exceeds") together with words that were quoted in the
study. The run brackets A1 from below: A1 as measured has the entries, this has none of them. It is a second pass of
a composer over the 48, which the freeze rule allows once; it is reported as a sensitivity analysis only and nothing is
changed after it.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "l4r_a1_sens"
A1 = HERE / "l4r_a1"
BANNER = ("**SENSITIVITY RUN, NOT AN ARM.** Arm A1 with the {n} cue entries removed that match a frozen sentence and no development sentence "
          "(`compose_tests/cue_audit.json`, removed in the running process by `compose_tests/ablate.py`). Arm A1 itself is "
          "`compose_tests/l4r_a1/`; this run does not replace it. Everything below the comparison is the report of `l4r.py` on this run.")


def first(a: dict):
    return a["shown"][0]["sentence"] if a.get("shown") else None


def compare(d: dict, a1: dict) -> list:
    """Per sentence whose row, outcome, first shown sentence or dialogue end differs from arm A1's."""
    old = {r["key"]: r for r in a1["rows"]}
    out = []
    for r in d["rows"]:
        o = old[r["key"]]
        x, y = o.get("A1d") or {}, r.get("A1d") or {}
        diff = {k: [a, b] for k, a, b in (
            ("row", o["cell"], r["cell"]),
            ("A1 outcome", o["A1"]["outcome"] + (f" ({o['A1']['ask']})" if o["A1"]["ask"] else ""), r["A1"]["outcome"] + (f" ({r['A1']['ask']})" if r["A1"]["ask"] else "")),
            ("first shown", first(o["A1"]), first(r["A1"])),
            ("dialogue end", (x.get("end"), x.get("questions"), x.get("at_gold")), (y.get("end"), y.get("questions"), y.get("at_gold"))),
            ("dialogue sentence", x.get("sentence"), y.get("sentence"))) if a != b}
        if diff:
            out.append({"key": r["key"], "rule": r["rule"], "diff": diff})
    return out


def report(d: dict) -> str:
    import l4r
    a1 = json.loads((A1 / "results.json").read_text())
    t, t1 = d["tallies"], a1["tallies"]
    cmp_ = d["against_A1"]
    o = ["# Sensitivity of arm A1 on the 48 frozen sentences to the frozen-only cue entries. CONTAMINATED; NOT AN ARM", "",
         BANNER.format(n=len(d["ablation"]["removed"])), "",
         "Removed: " + "; ".join(d["ablation"]["removed"]) + ".", "",
         "Matches skipped during the run (pattern entries only; a word taken out of a bag is not counted): "
         + ("; ".join(f"'{k}' {v}" for k, v in sorted(d["ablation"]["skipped"].items())) or "none") + ".", "",
         "| | A1 as measured (`l4r_a1/`) | without the frozen-only entries (this run) | A0 |", "|---|---|---|---|"]
    a0 = t1.get("A0") or {}
    for k in l4r.ROWS:
        o.append(f"| {k} | {len(t1[k])} | {len(t[k])} | {a0.get(k, 'n/a')} |")
    o.append(f"| declined but expressible (of the declined) | {len(t1['declined but expressible'])} | {len(t['declined but expressible'])} | {a0.get('declined but expressible', 'n/a')} |")
    o.append(f"| at the gold reading (of {t['with_gold']}) | {t1['dialogue']['at_gold']} | {t['dialogue']['at_gold']} | not measured here |")
    moved = [c for c in cmp_ if "row" in c["diff"]]
    o += ["", f"Sentences whose row differs from A1's: {len(moved)}. Sentences that differ in anything compared (row, A1's outcome, the first "
              f"sentence shown, how the dialogue ends, the sentence it ends with): {len(cmp_)} of {d['sentences']}.", ""]
    for c in cmp_:
        o.append(f"- **{c['key']}**: \"{c['rule']}\"")
        for k, (a, b) in c["diff"].items():
            o.append(f"  - {k}: A1 {a!r}; here {b!r}")
    o += ["", "---", "", l4r.report(d).split("\n", 1)[1]]
    return "\n".join(o)


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    if "--print" in sys.argv:
        print(report(json.loads((OUT / "results.json").read_text())))
        sys.exit(0)
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    TRIAL = Path(sys.argv[1]).resolve()
    assert (TRIAL / "work" / "clausal" / "clausal" / "compose2.py").exists(), f"no scratch copy at {TRIAL}/work/clausal (see the usage)"
    smoke = "--smoke" in sys.argv
    import l4r
    import l4b                                       # chdir to the scratch copy; puts it first on sys.path
    from clausal import compose2, cues2              # the scratch copy
    import ablate
    audit = json.loads((HERE / "cue_audit.json").read_text())
    rec = ablate.install(compose2, cues2, audit["frozen_only"])
    OUT.mkdir(exist_ok=True)
    gold = (A1 / "gold.json").read_bytes()
    (OUT / "gold.json").write_bytes(gold)
    l4r.OUT = OUT                                    # where run_main reads gold.json and writes its results
    rc = l4r.run_main(TRIAL, smoke)
    if smoke:
        print("smoke: skipped matches", {k[1]: v for k, v in ablate.hits.items()}, file=sys.stderr)
        sys.exit(rc)
    d = json.loads((OUT / "results.json").read_text())
    d["schema"] = "l4r-a1-sens-v1"
    d["what"] = "SENSITIVITY RUN, NOT AN ARM: " + d["what"] + ", with the frozen-only cue entries of compose_tests/cue_audit.json removed in the running process"
    d["ablation"] = {"removed": rec["removed"], "skipped": {k[1]: v for k, v in sorted(ablate.hits.items())},
                     "cue_audit_sha256": hashlib.sha256((HERE / "cue_audit.json").read_bytes()).hexdigest(),
                     "gold_sha256": hashlib.sha256(gold).hexdigest()}
    d["against_A1"] = compare(d, json.loads((A1 / "results.json").read_text()))
    (OUT / "results.json").write_text(json.dumps(d, indent=1, ensure_ascii=False, default=str) + "\n")
    text = report(d)
    (OUT / "REPORT.md").write_text(text + "\n")
    print(text)
    sys.exit(rc)
