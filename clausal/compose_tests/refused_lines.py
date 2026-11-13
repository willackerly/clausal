#!/usr/bin/env python3
"""What composer version 2 gives for each REFUSED fixture Rule line of features/ and controls/ (INT3 fix round). Run from clausal/:

    python3 compose_tests/refused_lines.py          no Lean, no cargo: about four minutes; writes compose_tests/refused_lines.json

This is not a test and has no expectation. It records, per refused line: the compiler's refusal (status, code, message), the
composer's outcome, and for an ANSWER whether the sentence answered is itself a compiled fixture Rule line and whether its
term is the one clausebook/terms.lock.json records for that line. The self-check of compose_tests/v2.py "none of the REFUSED
fixture Rule lines is ANSWERED" fails on the tree after the merge of the trust stream, whose fixture
Rule.intake.counter_set_frozen_wording is refused for a retired form only; this script prints what that answer is.
The fixtures only: no trial sentence and no development sentence is read.
"""
import json
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from clausal import compose as v1, compose2 as c2, ctree       # noqa: E402
from clausal.core import Problem                                # noqa: E402
from clausal.pipeline import ROOT                               # noqa: E402


def main():
    voc, comp = v1.load()
    lock = json.loads((ROOT / "clausebook" / "terms.lock.json").read_text())["sentences"]
    lines = ctree.rule_lines(voc, comp)
    gold = {}
    for i, src, text, hint, rd in lines:
        if not isinstance(rd, Problem):
            gold.setdefault(text, []).append((i, rd))
    rows = []
    for i, src, text, hint, rd in lines:
        if not isinstance(rd, Problem):
            continue
        t = time.time()
        r = c2.compose(text, hint, l3=False)
        a = r.get("answer") or {}
        row = {"id": i, "refusal": {"status": rd.status, "code": rd.code, "message": rd.message},
               "outcome": r["outcome"] + (f" ({r['ask']})" if r.get("ask") else ""), "sentence": text, "answer": a.get("sentence"),
               "secs": round(time.time() - t, 1)}
        if a:
            same = [(j, g) for j, g in gold.get(a["sentence"], []) if a["term_sha256"] == ctree.body_sha(g)]
            row["answer_is_the_fixture_line"] = [j for j, _ in same]
            row["answer_term_is_the_locked_one"] = bool(same) and all(lock[j]["lean_sha256"] == ctree.term_sha(g) for j, g in same)
            row["coverage"] = {k: a["coverage"][k] for k in ("dropped", "added", "condition_dropped", "full")}
        rows.append(row)
        print(f"{row['refusal']['code']:<15} {row['outcome']:<14} {i}" + (f"\n    \"{text}\"\n -> \"{row['answer']}\"  fixture line: "
              f"{row['answer_is_the_fixture_line']}; the locked term: {row['answer_term_is_the_locked_one']}; coverage full: {row['coverage']['full']}" if a else ""), flush=True)
    by = Counter((r["refusal"]["code"], r["outcome"]) for r in rows)
    res = {"refused_fixture_rule_lines": len(rows), "answered": sum(r["outcome"] == "ANSWER" for r in rows),
           "by_refusal_code_and_outcome": [{"code": c, "outcome": o, "n": n} for (c, o), n in sorted(by.items())], "rows": rows}
    (HERE / "refused_lines.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(rows)} refused fixture Rule lines; ANSWERED: {res['answered']}; " + "; ".join(f"{c} -> {o}: {n}" for (c, o), n in sorted(by.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
