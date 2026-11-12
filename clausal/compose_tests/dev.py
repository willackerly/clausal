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
  A1   compose2.compose(sentence)                         -> ANSWER / ASK (system | reading | dropped) / DECLINE
  A1s  the same after ONE answer to the system question: an ASK (system) is run again with the set's `system`
       (the only question answered for the author; an oracle for reading questions is plan node L1d and is not built)
  A0   compose.compose(sentence, None, 1): version 1's top candidate, taken as its answer (version 1 never declines)

HOW AN ANSWER IS JUDGED (mechanical; frozen in this file before the reported run):
  NOT-OF-ITS-PROJECT  the sentence uses an entry of a book the project of its operation does not list (projects.yaml):
                   `clausal gen` stops on it, so it is not a sentence the author could put in that project's feature file
  WRONG-OPERATION  the sentence answered is about another operation than the one the set's cases call
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
    if want is None or ops != [[want]]:
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
    from clausal import compose, compose2          # the scratch copy
    import replay
    items = json.loads((OUT / "devset.json").read_text())
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
        try:
            a0 = compose.compose(it["sentence"], None, 1)
            top = a0["candidates"][0] if a0["candidates"] else None
        except Exception as e:                       # a crash of version 1 is a result (no candidate)
            top = None
        row = {"id": it["id"], "kind": it["kind"], "system": it["system"], "sentence": it["sentence"], "intent": it["intent"],
               "A1": brief(a1), "A1s": brief(a1s), "A0": {"first": None if top is None else {"sentence": top["sentence"], "operations": top["operations"], "system": top["system"]}}}
        for arm in ("A1", "A1s", "A0"):
            want(it, arm, row[arm]["first"])
        rows.append(row)
    t_compose = round(time.time() - t0, 1)
    status, vars_of, log = replay.run(work, voc, sentences, reqs)
    for it, row in zip(items, rows):
        for arm in ("A1", "A1s", "A0"):
            c = row[arm]["first"]
            row[arm]["judged"] = None if c is None else judge(it, c, status, f"{it['id']}|{arm}")
    res = {"schema": "compose-dev-v1", "date": time.strftime("%Y-%m-%d"), "sentences": len(rows), "seconds_compose": t_compose, "log": log,
           "what": "composer version 2 (A1; A1s after the system question is answered from the set) and version 1 (A0) on the development set; "
                   "DEVELOPMENT numbers, the composer was developed on these sentences", "rows": rows}
    res["table"] = table(rows)
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
    for arm in ("A1", "A1s", "A0", "always-decline"):
        ex = [cell(r, arm) for r in rows if r["kind"] in EXPRESSIBLE]
        nx = [cell(r, arm) for r in rows if r["kind"] not in EXPRESSIBLE]
        need = [cell(r, arm) for r in rows if r["kind"] == "inexpressible"]
        out[arm] = {"expressible": {"n": len(ex), "right": ex.count("right"), "wrong": ex.count("wrong"), "asked": ex.count("asked"),
                                    "declined": ex.count("declined"), "missed": len(ex) - ex.count("right")},
                    "not_expressible": {"n": len(nx), "answered": nx.count("answered"), "asked": nx.count("asked"), "declined": nx.count("declined")},
                    "needs_unbuilt_piece": {"n": len(need), "answered": need.count("answered"), "asked": need.count("asked"), "declined": need.count("declined")},
                    "wrong_answers": ex.count("wrong") + nx.count("answered")}
        if arm in ("A1", "A1s"):
            asks = [r[arm]["ask"] for r in rows if r[arm]["outcome"] == "ASK"]
            out[arm]["asks"] = {k: asks.count(k) for k in ("system", "reading", "dropped")}
            ans = [r for r in rows if r[arm]["outcome"] == "ANSWER"]
            out[arm]["answers_with_a_dropped_word"] = sum(bool(r[arm]["shown"][0]["dropped"] or r[arm]["shown"][0]["condition_dropped"]) for r in ans)
            d = [r for r in rows if r[arm]["outcome"] == "ASK" and r[arm]["ask"] == "dropped"]
            out[arm]["if_first_shown_were_acknowledged_unread"] = {
                "n": len(d), "not_contradicted": sum(r[arm]["judged"]["judgement"] == "NOT-CONTRADICTED" for r in d),
                "wrong": sum(r[arm]["judged"]["judgement"] != "NOT-CONTRADICTED" for r in d)}
    return out


def report(d: dict) -> str:
    t = d["table"]
    o = ["# The development set through composer version 2 (no language model), with version 1 beside it", "",
         f"Run of {d['date']}. Generated by `clausal/compose_tests/dev.py`; do not edit. {d['sentences']} sentences "
         "(`devset.json`), no system given, no human choice. **Development numbers: the composer was developed while looking at "
         "these sentences. Not a clean measurement.** Definitions: the text at the top of `dev.py`.", "",
         "Arms: **A1** version 2. **A1s** version 2 after the one system question is answered from the set's `system` field. "
         "**A0** version 1, top candidate taken as its answer (never declines). **always-decline** is the computed control.", "",
         "## Wrong answers first", "", "| arm | wrong answers (of 60) | on expressible | on not expressible |", "|---|---|---|---|"]
    for arm in ("A1", "A1s", "A0", "always-decline"):
        o.append(f"| {arm} | {t[arm]['wrong_answers']} | {t[arm]['expressible']['wrong']} | {t[arm]['not_expressible']['answered']} |")
    e = t["A1"]["expressible"]["n"]
    o += ["", f"## Expressible sentences ({e}: the set's author's label, kinds single and compound; not checked against the book)", "",
          "| arm | answered-right (not contradicted on the replayable cases) | answered-wrong | asked | declined | MISSED (no right answer) |", "|---|---|---|---|---|---|"]
    for arm in ("A1", "A1s", "A0", "always-decline"):
        x = t[arm]["expressible"]
        o.append(f"| {arm} | {x['right']} | {x['wrong']} | {x['asked']} | {x['declined']} | {x['missed']} of {x['n']} |")
    n = t["A1"]["not_expressible"]["n"]
    o += ["", f"## Not expressible ({n}: {t['A1']['needs_unbuilt_piece']['n']} need a piece the book does not have, the rest are vague)", "",
          "| arm | answered (each is a wrong answer) | asked | declined (correct) | of those that need an unbuilt piece: answered |", "|---|---|---|---|---|"]
    for arm in ("A1", "A1s", "A0", "always-decline"):
        x, y = t[arm]["not_expressible"], t[arm]["needs_unbuilt_piece"]
        o.append(f"| {arm} | {x['answered']} | {x['asked']} | {x['declined']} | {y['answered']} of {y['n']} |")
    o += ["", "## Version 2 in more detail", ""]
    for arm in ("A1", "A1s"):
        x = t[arm]
        o.append(f"- **{arm}**: asks by kind: system {x['asks']['system']}, reading {x['asks']['reading']}, dropped {x['asks']['dropped']}. "
                 f"Answers with a dropped word or condition: {x['answers_with_a_dropped_word']}. "
                 f"If the first candidate of each ASK (dropped) were acknowledged unread ({x['if_first_shown_were_acknowledged_unread']['n']}): "
                 f"{x['if_first_shown_were_acknowledged_unread']['not_contradicted']} not contradicted, {x['if_first_shown_were_acknowledged_unread']['wrong']} wrong.")
    o += ["", f"Replay: {d['log']['replay']['requests']} requests, {d['log']['replay']['answers']} answers; sentences without a generated predicate: "
              f"{len(d['log']['without_generated_predicate'])}.", "", "## Every sentence", ""]
    for r in d["rows"]:
        o.append(f"- **{r['id']}** ({r['kind']}, {r['system']}): \"{r['sentence']}\"")
        o.append(f"  - intent: {r['intent']}")
        for arm in ("A1", "A1s"):
            a = r[arm]
            if arm == "A1s" and not (r["A1"]["outcome"] == "ASK" and r["A1"]["ask"] == "system"):
                continue
            head = a["outcome"] + (f" ({a['ask']})" if a["ask"] else "")
            if a["outcome"] == "ANSWER":
                o.append(f"  - {arm}: **ANSWER** \"{a['shown'][0]['sentence']}\": {a['judged']['judgement']}")
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
        o.append("  - A0: " + ("no candidate" if a0["first"] is None else f"\"{a0['first']['sentence']}\": {a0['judged']['judgement']}"))
    return "\n".join(o)


if __name__ == "__main__":
    if "--print" in sys.argv:
        print(report(json.loads((OUT / "results.json").read_text())))
        sys.exit(0)
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main())
