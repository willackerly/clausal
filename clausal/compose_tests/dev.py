#!/usr/bin/env python3
"""THE DEVELOPMENT SET through composer version 2 (arm A1: no language model), with version 1 beside it (arm A0), scored so
that declining cannot hide errors.

    bash clausal/mutation/workcopy.sh <scratch>/clausal                       # a scratch copy of clausal/ (never the tracked tree)
    tools/sem.sh 3 -- python3 clausal/compose_tests/dev.py <scratch>/clausal  # writes clausal/compose_tests/dev/{results.json,REPORT.md}
    python3 clausal/compose_tests/dev.py --print                              # the report again, from results.json

THE SET. dev/devset.json: 60 sentences written by an author who had seen neither the tool nor the 48 trial sentences,
committed unchanged. Each has `kind` (single, compound, inexpressible, vague), `system`, five `cases` (a state, a call,
an outcome, `allowed`: does the author's sentence permit this behaviour, `shipped`: is it what the shipped code does) and
`intent`. THIS IS A DEVELOPMENT SET: version 2 was developed while looking at its output on it. No number here is a
clean measurement.

WHAT IS RUN, per sentence, with NO system given and no human choice:
  A1   compose2.compose(sentence)                         -> ANSWER / ASK (system | operation | reading | dropped) / DECLINE
  A1s  the same after ONE answer to the system question: an ASK (system) is run again with the set's `system`
       (an oracle for reading questions is plan node L1d and is not built)
  A1o  A1s, and an ASK (operation) is run again with --operation = the one operation the set's single-call cases call
       (fix round: ASK (operation) is what version 2 now gives, where it declined, when no operation is named and the
       sentence has a word of a system). Where the cases call no single operation the question stays unanswered (asked).
  A0   compose.compose(sentence, None, 1): version 1's top candidate, taken as its answer (version 1 never declines)
  A1d  (plan node L1d) the DIALOGUE with an ORACLE AUTHOR, for the sentences that have a GOLD READING (dev/gold.json: a sentence
       of the book that says the author's `intent`, written by the builder; null where the book cannot say it):
       dialogue.converse(sentence, Oracle(gold), at most 3 questions). The oracle answers the system and operation questions
       from the gold sentence, an input question with the gold reading's value at the input (Lean model), and accepts a
       candidate only if it IS a gold reading (same Lean term, or proved equal by Lean's kernel). The dialogue ends
       ANSWER / CHOSEN (the author accepted a candidate with dropped words, recorded) / UNRESOLVED / DECLINE.
       AT GOLD = the sentence it ends with is the same term as a gold sentence or proved equal to one.
  gold each gold sentence itself, replayed on the set's cases (a check of the gold: a gold a case CONTRADICTS is listed)

HOW AN ANSWER IS JUDGED (mechanical; frozen in this file before the reported run):
  NOT-OF-ITS-PROJECT  the sentence uses an entry of a book the project of its operation does not list (projects.yaml):
                   `clausal gen` stops on it, so it is not a sentence the author could put in that project's feature file
  WRONG-OPERATION  the sentence answered is about another operation than the one the set's cases call (a sentence of
                   several clauses: some clause is)
  CONTRADICTED     on a case with `shipped: true` and a single call, the reading's value on the compiled Rust (replay.py:
                   holds / fails / out-of-scope) disagrees with `allowed`: allowed and the reading FAILS there, or not
                   allowed and the reading does not fail there
  NOT-CONTRADICTED neither, and at least one case was evaluated
  UNSCORED         no case could be evaluated (every case is a sequence of calls or compares two runs, or is not what the code does)
  "NOT-CONTRADICTED" IS WEAK: at most five inputs, only behaviours the shipped code has (a case that is not what the code
  does cannot be replayed), and `allowed: true` does not say whether the rule holds there or is silent. Every answer is
  printed in the report beside the author's intent so that it can be read.

THE TABLE (per arm; nothing is pooled):
  expressible sentences (kind single or compound; THE SET'S AUTHOR'S LABEL, not checked against the book: some of these
  the book cannot say, so "missed" is an upper bound):
      answered-right (NOT-CONTRADICTED)   answered-wrong (NOT-OF-ITS-PROJECT, WRONG-OPERATION, CONTRADICTED, UNSCORED)   asked   declined
      MISSED = asked + declined + answered-wrong: an expressible sentence that did not get a right answer. The headline is
      answered-right over all expressible sentences.
  not expressible (kind inexpressible: needs a piece the book does not have; kind vague: not checkable as written):
      answered (EVERY answer here is wrong, whatever the cases say)   asked   declined (the correct outcome)
  WRONG ANSWERS, reported first: answered-wrong on expressible + every answer on not expressible.
  Controls: "always decline" (0 right, 0 wrong, every expressible sentence missed) and "never decline" (A0).
  For an ASK (dropped), also: what the FIRST candidate shown would be if the author acknowledged it without reading
  (judged as above). It is not an answer and is not counted as one.

THE TALLIES OF PLAN NODE L1c/L1d (`tallies`; frozen here before the run that reports them), over all 60 sentences, for
"A1 + oracle" and for A0. Every sentence is in exactly one row:
  answered right                 answered with no question, and NOT-CONTRADICTED on the replayable cases
  right after questions          has a gold reading; not answered with no question; the dialogue ends ANSWER or CHOSEN AT GOLD
                                 within 3 questions (A0 asks nothing: 0)
  answered wrong                 answered with no question and not right (expressible: contradicted, wrong operation, not of its
                                 project, unscored; not expressible: any answer)
  wrong after questions          has a gold reading; the dialogue ends ANSWER or CHOSEN with a sentence that is NOT a gold reading
                                 (the oracle accepts only gold, so this is an ANSWER that survived the questions)
  asked                          not answered: an ASK with no gold reading to answer it from, or a dialogue that ends UNRESOLVED
  declined                       DECLINE (alone, or at the end of a dialogue)
  declined but expressible       of the declined: the set's author labelled the sentence expressible (single, compound)
Also printed: of "answered right", how many have a gold reading and are / are not that reading (an answer the cases do not
contradict can still be another reading), and the questions asked per sentence that ends at gold.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "dev"
EXPRESSIBLE = ("single", "compound")
OPS = {("wallet", "withdraw"): "w.withdraw", ("wallet", "deposit"): "w.deposit", ("wallet", "transfer"): "w.transfer",
       ("ledger", "balance"): "l.lookup", ("ledger", "total"): "l.total", ("ledger", "apply"): "l.apply",
       ("ledger", "apply_batch"): "l.apply_batch", ("ledger", "apply_all"): "l.apply_all", ("counter", "bump"): "ctr.bump"}


def single(call) -> bool:
    """One call of one operation (not a sequence of calls, and not two runs compared)."""
    return isinstance(call, dict) and "op" in call


def tr(t: dict) -> str:
    return f"{t['from']}->{t['to']}:{t['amount']}"


def values(system: str, case: dict):
    """The replay's variables for a single-call case: {variable: literal}; None for a sequence of calls."""
    call, st = case["call"], case["state"]
    if not single(call):
        return None
    a = call["args"]
    if system == "wallet":
        if call["op"] == "transfer":
            return {"the_sender": str(st["src"]), "the_receiver": str(st["dst"]), "the_amount": str(a["amt"])}
        return {"the_wallet": str(st["balance"]), "the_amount": str(a["amt"])}
    if system == "counter":
        return {"the_counter": str(st["count"]), "the_amount": str(a["by"])}
    v = {"the_ledger": "[" + ", ".join(str(b) for b in st["balances"]) + "]"}
    if call["op"] == "apply":
        v["the_transfer"] = tr(a["t"])
    elif call["op"] in ("apply_batch", "apply_all"):
        v["the_batch"] = "[" + ", ".join(tr(t) for t in a["batch"]) + "]"
    elif call["op"] == "balance":
        v["the_account"] = str(a["i"])
    return v


def case_op(system: str, cases: list):
    ops = {c["call"]["op"] for c in cases if single(c["call"])}
    return OPS[(system, next(iter(ops)))] if len(ops) == 1 else None


def judge(item: dict, cand: dict, status: dict, tag: str) -> dict:
    """The judgement of one answered sentence (`cand`: {sentence, operations}) on the cases of `item`."""
    want = case_op(item["system"], item["cases"])
    ops = cand["operations"]
    per = []
    if cand.get("outside_books"):
        return {"judgement": "NOT-OF-ITS-PROJECT", "why": "uses " + ", ".join(cand["outside_books"]) + " of a book its project does not list", "cases": []}
    # (L1c: a sentence of several clauses about the one operation the cases call is about that operation. The L1ab scorer
    # compared with [[operation]] and so judged every sentence of two clauses WRONG-OPERATION; no answer of the 'before' run
    # had two clauses, only three gold sentences did.)
    if want is None or any(seq != [want] for seq in ops):
        seq = all(not single(c["call"]) for c in item["cases"])
        if not seq:
            return {"judgement": "WRONG-OPERATION", "why": f"the cases call {want}; the sentence is about {ops}", "cases": []}
    bad = False
    for n, c in enumerate(item["cases"]):
        if not single(c["call"]):
            per.append("sequence or two runs (not evaluated)")
            continue
        if not c["shipped"]:
            per.append("not what the code does (not evaluated)")
            continue
        st = status.get(f"{tag}|{n}", "no answer")
        if st not in ("holds", "fails", "out-of-scope"):
            per.append(f"allowed={c['allowed']}; reading: {st} (not evaluated)")
            continue
        ok = (st != "fails") if c["allowed"] else (st == "fails")
        bad = bad or not ok
        per.append(f"allowed={c['allowed']}; reading: {st}" + ("" if ok else "  <-- CONTRADICTS"))
    n_eval = sum("reading: " in p and "not evaluated" not in p for p in per)
    return {"judgement": "CONTRADICTED" if bad else "NOT-CONTRADICTED" if n_eval else "UNSCORED", "cases": per, "evaluated": n_eval}


def main() -> int:
    work = Path(sys.argv[1]).resolve()
    assert (work / "clausal" / "compose2.py").exists(), f"no scratch copy of clausal/ at {work} (see the usage)"
    sys.path.insert(0, str(work))
    sys.path.insert(0, str(HERE))
    import os
    os.chdir(work)
    from clausal import compose, compose2, dialogue          # the scratch copy
    import replay
    items = json.loads((OUT / "devset.json").read_text())
    gold = json.loads((OUT / "gold.json").read_text())["gold"]
    from clausal.core import Problem
    voc, comp = compose.load()
    t0 = time.time()
    rows, sentences, reqs = [], {}, []

    def brief(res):
        c = res["answer"] or (res["candidates"][0] if res["candidates"] else None)
        return {"outcome": res["outcome"], "ask": res["ask"], "why": res["why"], "system": res.get("system"), "system_by": res.get("system_by"),
                "counts": res.get("counts"), "missing_kinds": res.get("missing_kinds"), "decline": res.get("decline"),
                "questions": [{k: q.get(k) for k in ("a", "b", "verdict", "question")} for q in res.get("questions") or []],
                "shown": [{"sentence": x["sentence"], "operations": x["operations"], "dropped": x["coverage"]["dropped"], "added": x["coverage"]["added"],
                           "condition_dropped": x["coverage"]["condition_dropped"], "defaults_used": x["coverage"]["defaults_used"],
                           "full": x["coverage"]["full"], "words": x["coverage"]["words"]} for x in res["candidates"]],
                "first": None if c is None else {"sentence": c["sentence"], "operations": c["operations"], "system": c["system"]}}

    def want(item, arm, cand):
        if cand is None:
            return
        rd = compose.compile_sentence(comp, cand["sentence"], None)
        if isinstance(rd, Problem):                  # a sentence two systems read: in the system the composer read it in
            rd = compose.compile_sentence(comp, cand["sentence"], cand["system"])
        cand["outside_books"] = [] if isinstance(rd, Problem) else compose2.outside_books(voc, rd)
        if cand["outside_books"]:
            return                                   # not a sentence of its project: `clausal gen` would stop on it; judged wrong, not replayed
        sentences.setdefault(cand["sentence"], cand["operations"][0][0])
        for n, c in enumerate(item["cases"]):
            v = values(item["system"], c)
            if v is not None and c["shipped"]:
                reqs.append({"sentence": cand["sentence"], "values": v, "tag": f"{item['id']}|{arm}|{n}"})

    for it in items:
        a1 = compose2.compose(it["sentence"])
        a1s = compose2.compose(it["sentence"], it["system"]) if a1["outcome"] == "ASK" and a1["ask"] == "system" else a1
        opid = case_op(it["system"], it["cases"])
        a1o = compose2.compose(it["sentence"], None, operation=opid) if a1s["outcome"] == "ASK" and a1s["ask"] == "operation" and opid else a1s
        try:
            a0 = compose.compose(it["sentence"], None, 1)
            top = a0["candidates"][0] if a0["candidates"] else None
        except Exception as e:                       # a crash of version 1 is a result (no candidate)
            top = None
        row = {"id": it["id"], "kind": it["kind"], "system": it["system"], "sentence": it["sentence"], "intent": it["intent"],
               "A1": brief(a1), "A1s": brief(a1s), "A1o": brief(a1o), "A0": {"first": None if top is None else {"sentence": top["sentence"], "operations": top["operations"], "system": top["system"]}}}
        for arm in ("A1", "A1s", "A1o", "A0"):
            want(it, arm, row[arm]["first"])
        # the dialogue with the oracle author, where a gold reading is assigned
        g = (gold.get(it["id"]) or {}).get("sentences")
        row["gold"] = {"sentences": g, "why_none": (gold.get(it["id"]) or {}).get("why")}
        row["A1d"] = None
        if g:
            orc = dialogue.Oracle(g, it["system"])
            d = dialogue.converse(it["sentence"], orc)
            ag = dialogue.at_gold(d, orc)
            row["A1d"] = {"end": d["end"], "questions": d["questions"], "why": d["why"], "last_outcome": d.get("last_outcome"),
                          "turns": [{"kind": t["kind"], "answer": t["answer"], "values": t.get("values"),
                                     "shown": [x["sentence"] for x in t.get("shown") or t.get("candidates") or []]} for t in d["turns"]],
                          "acknowledgement": d["acknowledgement"], "against_gold": ag["verdict"], "at_gold": ag["at_gold"], "lean_runs": d["lean_runs"],
                          "first": None if d["sentence"] is None else {"sentence": d["sentence"], "operations": d["operations"], "system": d["system"]}}
            want(it, "A1d", row["A1d"]["first"])
            if a1["outcome"] == "ANSWER":            # an answer with no question: is it the gold reading?
                v = orc.is_gold([{"sentence": a1["answer"]["sentence"], "system": a1["answer"]["system"]}])[0]
                row["A1"]["against_gold"] = v["verdict"]
            if top is not None:
                row["A0"]["against_gold"] = orc.is_gold([{"sentence": top["sentence"], "system": top["system"]}])[0]["verdict"]
            row["gold"]["judged"] = []
            for k, gs in enumerate(g):
                rd = compose.compile_sentence(comp, gs, it["system"])
                c = {"sentence": gs, "operations": [[o["id"] for o in cl["ops"]] for cl in rd.info["clauses"]], "system": it["system"]}
                row["gold"]["judged"].append(c)
                want(it, f"gold{k}", c)
        print(f"{it['id']} {a1['outcome']} {a1['ask'] or ''}" + (f" | dialogue: {row['A1d']['end']} after {row['A1d']['questions']}, at gold: {row['A1d']['at_gold']}" if row["A1d"] else ""), file=sys.stderr, flush=True)
        rows.append(row)
    t_compose = round(time.time() - t0, 1)
    status, vars_of, log = replay.run(work, voc, sentences, reqs)
    for it, row in zip(items, rows):
        for arm in ("A1", "A1s", "A1o", "A0"):
            c = row[arm]["first"]
            row[arm]["judged"] = None if c is None else judge(it, c, status, f"{it['id']}|{arm}")
        if row["A1d"]:
            c = row["A1d"]["first"]
            row["A1d"]["judged"] = None if c is None else judge(it, c, status, f"{it['id']}|A1d")
            for k, c in enumerate(row["gold"]["judged"]):
                c["judged"] = judge(it, c, status, f"{it['id']}|gold{k}")
    res = {"schema": "compose-dev-v2", "date": time.strftime("%Y-%m-%d"), "sentences": len(rows), "seconds_compose": t_compose, "log": log,
           "what": "composer version 2 (A1; A1s after the system question is answered from the set; A1o after the operation question too) and version 1 (A0) on the development set; "
                   "DEVELOPMENT numbers, the composer was developed on these sentences", "rows": rows}
    res["table"] = table(rows)
    res["tallies"] = tallies(rows)
    (OUT / "results.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    text = report(res)
    (OUT / "REPORT.md").write_text(text + "\n")
    print(text)
    return 0


def cell(row: dict, arm: str) -> str:
    """One of: right, wrong, asked, declined (expressible) / answered, asked, declined (not expressible)."""
    if arm == "always-decline":
        return "declined"
    a = row[arm]
    answered = arm == "A0" and a["first"] is not None or arm != "A0" and a["outcome"] == "ANSWER"
    if arm == "A0" and a["first"] is None:
        return "declined"
    if not answered:
        return "asked" if a["outcome"] == "ASK" else "declined"
    if row["kind"] not in EXPRESSIBLE:
        return "answered"
    return "right" if a["judged"]["judgement"] == "NOT-CONTRADICTED" else "wrong"


def table(rows: list) -> dict:
    out = {}
    for arm in ("A1", "A1s", "A1o", "A0", "always-decline"):
        ex = [cell(r, arm) for r in rows if r["kind"] in EXPRESSIBLE]
        nx = [cell(r, arm) for r in rows if r["kind"] not in EXPRESSIBLE]
        need = [cell(r, arm) for r in rows if r["kind"] == "inexpressible"]
        out[arm] = {"expressible": {"n": len(ex), "right": ex.count("right"), "wrong": ex.count("wrong"), "asked": ex.count("asked"),
                                    "declined": ex.count("declined"), "missed": len(ex) - ex.count("right")},
                    "not_expressible": {"n": len(nx), "answered": nx.count("answered"), "asked": nx.count("asked"), "declined": nx.count("declined")},
                    "needs_unbuilt_piece": {"n": len(need), "answered": need.count("answered"), "asked": need.count("asked"), "declined": need.count("declined")},
                    "wrong_answers": ex.count("wrong") + nx.count("answered")}
        if arm in ("A1", "A1s", "A1o"):
            asks = [r[arm]["ask"] for r in rows if r[arm]["outcome"] == "ASK"]
            out[arm]["asks"] = {k: asks.count(k) for k in ("system", "operation", "reading", "dropped")}
            ans = [r for r in rows if r[arm]["outcome"] == "ANSWER"]
            dec = [r[arm]["why"] for r in rows if r[arm]["outcome"] == "DECLINE"]
            out[arm]["declines"] = {"no_operation_and_no_word_of_a_system": sum(w.startswith("no operation") for w in dec),
                                    "no_askable_candidate": sum(not w.startswith("no operation") for w in dec)}
            out[arm]["declined_but_expressible"] = [r["id"] for r in rows if r[arm]["outcome"] == "DECLINE" and r["kind"] in EXPRESSIBLE]
            out[arm]["answers_with_a_dropped_word"] = sum(bool(r[arm]["shown"][0]["dropped"] or r[arm]["shown"][0]["condition_dropped"]) for r in ans)
            d = [r for r in rows if r[arm]["outcome"] == "ASK" and r[arm]["ask"] == "dropped"]
            out[arm]["if_first_shown_were_acknowledged_unread"] = {
                "n": len(d), "not_contradicted": sum(r[arm]["judged"]["judgement"] == "NOT-CONTRADICTED" for r in d),
                "wrong": sum(r[arm]["judged"]["judgement"] != "NOT-CONTRADICTED" for r in d)}
    return out


def tally_cell(row: dict, arm: str) -> str:
    """The one row of THE TALLIES a sentence is in, for "A1+oracle" or "A0" (the definitions are in the module text)."""
    if arm == "A0":
        c = cell(row, "A0")
        return {"right": "answered right", "wrong": "answered wrong", "answered": "answered wrong", "declined": "declined"}[c]
    c = cell(row, "A1")
    if c in ("right", "wrong", "answered"):
        return "answered right" if c == "right" else "answered wrong"
    d = row.get("A1d")
    if d is None:
        return "asked" if c == "asked" else "declined"
    if d["end"] in ("ANSWER", "CHOSEN"):
        return "right after questions" if d["at_gold"] else "wrong after questions"
    return "asked" if d["end"] == "UNRESOLVED" else "declined"


TALLY_ROWS = ("answered right", "right after questions", "answered wrong", "wrong after questions", "asked", "declined")


def tallies(rows: list) -> dict:
    out = {}
    for arm in ("A1+oracle", "A0"):
        cells = {r["id"]: tally_cell(r, arm) for r in rows}
        t = {k: sorted(i for i, c in cells.items() if c == k) for k in TALLY_ROWS}
        t["declined but expressible"] = sorted(r["id"] for r in rows if cells[r["id"]] == "declined" and r["kind"] in EXPRESSIBLE)
        key = "A1" if arm != "A0" else "A0"
        right = [r for r in rows if cells[r["id"]] == "answered right"]
        t["answered right: is the gold reading"] = sorted(r["id"] for r in right if r[key].get("against_gold") in ("SAME-TERM", "PROVED-EQUAL"))
        t["answered right: has a gold reading and is not shown to be it"] = sorted(
            f"{r['id']} ({r[key]['against_gold']})" for r in right if r[key].get("against_gold") not in (None, "SAME-TERM", "PROVED-EQUAL"))
        out[arm] = t
    d = [r["A1d"] for r in rows if r.get("A1d")]
    out["dialogue"] = {"with_gold": len(d), "ends": {e: sum(x["end"] == e for x in d) for e in ("ANSWER", "CHOSEN", "UNRESOLVED", "DECLINE")},
                       "at_gold": sum(x["at_gold"] for x in d), "at_gold_with_no_question": sum(x["at_gold"] and x["questions"] == 0 for x in d),
                       "questions_of_those_at_gold": [x["questions"] for x in d if x["at_gold"]],
                       "question_kinds": {k: sum(t["kind"] == k for x in d for t in x["turns"]) for k in ("system", "operation", "input", "which", "accept")},
                       "ended_at_another_reading": sorted(r["id"] for r in rows if r.get("A1d") and r["A1d"]["end"] in ("ANSWER", "CHOSEN") and not r["A1d"]["at_gold"]),
                       "gold_contradicted_by_a_case": sorted(r["id"] for r in rows if any(c["judged"]["judgement"] not in ("NOT-CONTRADICTED", "UNSCORED")
                                                                                         for c in (r.get("gold") or {}).get("judged") or []))}
    return out


def say_tallies(d: dict) -> list:
    t = d["tallies"]
    n = d["sentences"]
    o = ["## The tallies of plan nodes L1c and L1d (all %d sentences; each sentence is in one row)" % n, "",
         "| | A1 + oracle author | A0 |", "|---|---|---|"]
    for k in TALLY_ROWS:
        o.append(f"| {k} | {len(t['A1+oracle'][k])} | {len(t['A0'][k])} |")
    o.append(f"| declined but expressible (of the declined) | {len(t['A1+oracle']['declined but expressible'])} | {len(t['A0']['declined but expressible'])} |")
    o.append("")
    for arm in ("A1+oracle", "A0"):
        x = t[arm]
        o.append(f"- **{arm}**: " + "; ".join(f"{k}: {', '.join(x[k]) or 'none'}" for k in TALLY_ROWS if k not in ("asked",)) + ".")
        o.append(f"  - of the answers counted right, the gold reading: {', '.join(x['answered right: is the gold reading']) or 'none'}; "
                 f"with a gold reading and not shown to be it: {', '.join(x['answered right: has a gold reading and is not shown to be it']) or 'none'}; "
                 f"declined but expressible: {', '.join(x['declined but expressible']) or 'none'}.")
    g = t["dialogue"]
    qs = g["questions_of_those_at_gold"]
    o.append(f"- **The dialogue with the oracle author** ({g['with_gold']} sentences have a gold reading): ends ANSWER {g['ends']['ANSWER']}, CHOSEN {g['ends']['CHOSEN']}, "
             f"UNRESOLVED {g['ends']['UNRESOLVED']}, DECLINE {g['ends']['DECLINE']}; at the gold reading {g['at_gold']} ({g['at_gold_with_no_question']} with no question); "
             f"questions asked where it ends at gold: {sum(qs)} over {len(qs)} sentences" + (f" ({sum(qs) / len(qs):.2f} each)" if qs else "")
             + "; question kinds over all dialogues: " + ", ".join(f"{k} {v}" for k, v in g["question_kinds"].items())
             + f"; ended at another reading: {', '.join(g['ended_at_another_reading']) or 'none'}; gold sentences a case contradicts: {', '.join(g['gold_contradicted_by_a_case']) or 'none'}.")
    o.append("- CHOSEN means the oracle accepted a candidate that does NOT account for every word of the rough sentence (its dropped words are in the "
             "acknowledgement). The oracle accepts only a gold reading; a person might accept another.")
    return o + [""]


def report(d: dict) -> str:
    t = d["table"]
    o = ["# The development set through composer version 2 (no language model), with version 1 beside it", "",
         f"Run of {d['date']}. Generated by `clausal/compose_tests/dev.py`; do not edit. {d['sentences']} sentences "
         "(`devset.json`), no system given, no human choice. **Development numbers: the composer was developed while looking at "
         "these sentences. Not a clean measurement.** Definitions: the text at the top of `dev.py`.", "",
         "Arms: **A1** version 2. **A1s** version 2 after the one system question is answered from the set's `system` field. "
         "**A1o** A1s, and the operation question answered with the operation the set's cases call. "
         "**A0** version 1, top candidate taken as its answer (never declines). **always-decline** is the computed control.", "",
         "## Wrong answers first", "", "| arm | wrong answers (of 60) | on expressible | on not expressible |", "|---|---|---|---|"]
    for arm in ("A1", "A1s", "A1o", "A0", "always-decline"):
        o.append(f"| {arm} | {t[arm]['wrong_answers']} | {t[arm]['expressible']['wrong']} | {t[arm]['not_expressible']['answered']} |")
    e = t["A1"]["expressible"]["n"]
    o += [""] + (say_tallies(d) if "tallies" in d else [])
    o += [f"## Expressible sentences ({e}: the set's author's label, kinds single and compound; not checked against the book)", "",
          "| arm | answered-right (not contradicted on the replayable cases) | answered-wrong | asked | declined | MISSED (no right answer) |", "|---|---|---|---|---|---|"]
    for arm in ("A1", "A1s", "A1o", "A0", "always-decline"):
        x = t[arm]["expressible"]
        o.append(f"| {arm} | {x['right']} | {x['wrong']} | {x['asked']} | {x['declined']} | {x['missed']} of {x['n']} |")
    n = t["A1"]["not_expressible"]["n"]
    o += ["", f"## Not expressible ({n}: {t['A1']['needs_unbuilt_piece']['n']} need a piece the book does not have, the rest are vague)", "",
          "| arm | answered (each is a wrong answer) | asked | declined (correct) | of those that need an unbuilt piece: answered |", "|---|---|---|---|---|"]
    for arm in ("A1", "A1s", "A1o", "A0", "always-decline"):
        x, y = t[arm]["not_expressible"], t[arm]["needs_unbuilt_piece"]
        o.append(f"| {arm} | {x['answered']} | {x['asked']} | {x['declined']} | {y['answered']} of {y['n']} |")
    o += ["", "## Version 2 in more detail", ""]
    for arm in ("A1", "A1s", "A1o"):
        x = t[arm]
        o.append(f"- **{arm}**: asks by kind: system {x['asks']['system']}, operation {x['asks']['operation']}, reading {x['asks']['reading']}, dropped {x['asks']['dropped']}. "
                 f"Declines: {x['declines']['no_operation_and_no_word_of_a_system']} with no operation named and no word of a system, "
                 f"{x['declines']['no_askable_candidate']} with no askable candidate; declined though labelled expressible: {', '.join(x['declined_but_expressible']) or 'none'}. "
                 f"Answers with a dropped word or condition: {x['answers_with_a_dropped_word']}. "
                 f"If the first candidate of each ASK (dropped) were acknowledged unread ({x['if_first_shown_were_acknowledged_unread']['n']}): "
                 f"{x['if_first_shown_were_acknowledged_unread']['not_contradicted']} not contradicted, {x['if_first_shown_were_acknowledged_unread']['wrong']} wrong.")
    o += ["", f"Replay: {d['log']['replay']['requests']} requests, {d['log']['replay']['answers']} answers; sentences without a generated predicate: "
              f"{len(d['log']['without_generated_predicate'])}.", "", "## Every sentence", ""]
    for r in d["rows"]:
        o.append(f"- **{r['id']}** ({r['kind']}, {r['system']}): \"{r['sentence']}\"")
        o.append(f"  - intent: {r['intent']}")
        for arm in ("A1", "A1s", "A1o"):
            a = r[arm]
            if arm == "A1s" and not (r["A1"]["outcome"] == "ASK" and r["A1"]["ask"] == "system"):
                continue
            if arm == "A1o" and not (r["A1s"]["outcome"] == "ASK" and r["A1s"]["ask"] == "operation"):
                continue
            head = a["outcome"] + (f" ({a['ask']})" if a["ask"] else "")
            if a["outcome"] == "ANSWER":
                o.append(f"  - {arm}: **ANSWER** \"{a['shown'][0]['sentence']}\": {a['judged']['judgement']}"
                         + (f"; against gold: {a['against_gold']}" if a.get("against_gold") else ""))
            elif a["outcome"] == "DECLINE":
                o.append(f"  - {arm}: DECLINE: {a['why'][:160]}")
            elif a["ask"] == "dropped":
                s = a["shown"][0]
                o.append(f"  - {arm}: {head}; first shown \"{s['sentence']}\" (dropped: {', '.join(s['dropped']) or 'none'}"
                         + (f"; added: {', '.join(s['added'])}" if s["added"] else "")
                         + (f"; CONDITION DROPPED: {'; '.join(s['condition_dropped'])}" if s["condition_dropped"] else "")
                         + f"); if acknowledged unread: {a['judged']['judgement']}")
            else:
                o.append(f"  - {arm}: {head}: {a['why'][:200]}")
        a0 = r["A0"]
        o.append("  - A0: " + ("no candidate" if a0["first"] is None else f"\"{a0['first']['sentence']}\": {a0['judged']['judgement']}")
                 + (f"; against gold: {a0['against_gold']}" if a0.get("against_gold") else ""))
        g = r.get("gold")
        if g and g["sentences"]:
            o.append("  - gold: " + " / ".join(f"\"{c['sentence']}\" ({c['judged']['judgement']} on the cases)" for c in g["judged"]))
            x = r["A1d"]
            turns = "; ".join(f"{t['kind']} -> {t['answer'] if t['answer'] is not None else 'none'}" for t in x["turns"]) or "no question"
            o.append(f"  - A1d (oracle author): {x['end']} after {x['questions']} question(s) [{turns}]"
                     + (f": \"{x['first']['sentence']}\"; against gold: {x['against_gold']}" + ("" if x["at_gold"] else " (NOT the gold reading)")
                        + f"; on the cases: {x['judged']['judgement']}" if x["first"] else f": {x['why'][:160]}"))
        elif g:
            o.append(f"  - gold: none ({g['why_none']})" if g["why_none"] else "  - gold: none (not labelled expressible)")
    return "\n".join(o)


if __name__ == "__main__":
    if "--print" in sys.argv:
        print(report(json.loads((OUT / "results.json").read_text())))
        sys.exit(0)
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main())
