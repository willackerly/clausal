#!/usr/bin/env python3
"""THE ORACLE AUTHOR ON THE CASES OF clausal/separate_tests (plan node L1d).

    ../tools/sem.sh 3 -- python3 compose_tests/oracle.py            # from clausal/; needs lean/ built; writes compose_tests/oracle_results.json

THE TEST (frozen in this file before its first run). For every case of separate_tests/cases.json and cases_review.json,
the CANDIDATES are the case's sentences, each as compiled in every system that reads it (the two readings of one
sentence that two systems read are two candidates). For EVERY candidate in turn, that candidate is the intended reading:
an oracle author (clausal/dialogue.py `Oracle`) is given it and answers the tool's questions (`dialogue.resolve`).

  PASS  the dialogue ends with ANSWER, the sentence it ends with is a gold reading (the same Lean term as the intended
        one, or proved equal to it by Lean's kernel), and at most 3 questions were asked.
  The number of questions PREDICTED for each dialogue (from the verdicts frozen in separate_tests: SEPARATED -> one input
  question; NONE-FOUND -> one "which do you mean"; two systems -> one system question; operations with no common input in
  one system -> one operation question; SAME-TERM / PROVED-EQUAL -> none) is in PREDICTED below. A dialogue that passes
  with another number of questions is reported as a MISPREDICTION, not as a failure.

CONTROL (the test must be able to fail): for the case `scope`, an oracle whose intended reading is NOT among the
candidates ("A rejected withdrawal never changes the wallet's balance"). Its answers leave one candidate; the dialogue
must be reported as NOT ending at the gold reading.
"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from clausal import dialogue, separate          # noqa: E402

# case id -> {candidate "<A|B>/<system>": questions predicted}
PREDICTED = {
    "scope": {"A/wallet": 1, "B/wallet": 1},
    "strict": {"A/wallet": 1, "B/wallet": 1},
    "cross_two_sentences": {"A/wallet": 1, "B/ledger": 1},
    "cross_one_sentence_silent": {"A/wallet": 0},
    "cross_one_sentence_both": {"A/ledger": 1, "A/wallet": 1},
    "same_term": {"A/ledger": 0, "B/ledger": 0},
    "same_meaning_proved": {"A/ledger": 0, "B/ledger": 0},
    "same_on_fixture_not_proved": {"A/ledger": 1, "B/ledger": 1},
    "beyond_bounds": {"A/ledger": 1, "B/ledger": 1},
    "different_operations_one_system": {"A/ledger": 2, "B/ledger": 2, "B/wallet": 1},
    "one_call_against_two": {"A/ledger": 1, "B/ledger": 1},
    "same_input_different_operations": {"A/ledger": 1, "B/ledger": 1},
}
CONTROL = ("scope", "A rejected withdrawal never changes the wallet's balance", "wallet")


def main() -> int:
    cases = [c for f in ("cases.json", "cases_review.json") for c in json.loads((HERE.parent / "separate_tests" / f).read_text())["cases"]]
    voc, comp = separate.load()
    rows, bad, t0 = [], [], time.time()
    for case in cases:
        golds = []
        for label, s in zip("AB", case["sentences"]):
            for c in separate.candidates(voc, comp, s, label):
                if c["compiled"]:
                    golds.append((c["label"], s, c["domain"]))
        assert sorted(l for l, _, _ in golds) == sorted(PREDICTED[case["id"]]), (case["id"], golds)
        for label, s, d in golds:
            o = dialogue.Oracle([s], d)
            out = dialogue.resolve(case["sentences"], o)
            g = dialogue.at_gold(out, o)
            ok = out["end"] == "ANSWER" and g["at_gold"] and out["questions"] <= 3
            row = {"case": case["id"], "gold": label, "gold_sentence": s, "end": out["end"], "ended_with": out["sentence"], "ended_in": out["system"],
                   "against_gold": g["verdict"], "questions": out["questions"], "kinds": [t["kind"] for t in out["turns"]],
                   "answers": [t["answer"] for t in out["turns"]], "predicted": PREDICTED[case["id"]][label], "pass": ok, "why": out["why"]}
            rows.append(row)
            print(("PASS " if ok else "FAIL ") + f"{case['id']:<34}{label:<10} {out['end']:<10} questions {out['questions']} "
                  f"({', '.join(row['kinds']) or 'none'}; predicted {row['predicted']}) against gold: {g['verdict']}", flush=True)
            if not ok:
                bad.append(f"{case['id']} {label}")
    cid, gs, gd = CONTROL
    case = next(c for c in cases if c["id"] == cid)
    o = dialogue.Oracle([gs], gd)
    out = dialogue.resolve(case["sentences"], o)
    g = dialogue.at_gold(out, o)
    control = {"case": cid, "gold_sentence": gs, "end": out["end"], "ended_with": out["sentence"], "against_gold": g["verdict"], "at_gold": g["at_gold"],
               "questions": out["questions"], "pass": not g["at_gold"]}
    print(("PASS " if control["pass"] else "FAIL ") + f"control: an intended reading that is not a candidate ends {out['end']} with \"{out['sentence']}\", "
          f"against gold: {g['verdict']} (must not be reported as the gold reading)")
    if not control["pass"]:
        bad.append("control")
    mis = [f"{r['case']} {r['gold']}: {r['questions']} (predicted {r['predicted']})" for r in rows if r["pass"] and r["questions"] != r["predicted"]]
    res = {"what": "the oracle author on the cases of separate_tests (plan node L1d)", "date": time.strftime("%Y-%m-%d"), "seconds": round(time.time() - t0, 1),
           "dialogues": len(rows), "passed": sum(r["pass"] for r in rows), "at_most_three_questions": sum(r["questions"] <= 3 for r in rows),
           "questions_histogram": {str(n): sum(r["questions"] == n for r in rows) for n in range(4)},
           "mispredicted_question_counts": mis, "control": control, "rows": rows}
    (HERE / "oracle_results.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    print(f"\n{res['passed']} of {res['dialogues']} dialogues end at the gold reading within three questions; questions asked: {res['questions_histogram']}; "
          f"mispredicted counts: {len(mis)}; control {'passed' if control['pass'] else 'FAILED'}")
    for m in mis:
        print("  MISPREDICTION " + m)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
