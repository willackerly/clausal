#!/usr/bin/env python3
"""ARM A1 ON THE 48 FROZEN SENTENCES: composer version 2 (no language model) with the dialogue and the oracle author.
CONTAMINATED: the design of version 2 was derived from the failures of version 1 on these sentences
(docs/studies/2026-11-12/composer-v2.md), and the wording changes of the last wave coincide with some of them. A
development measure; not used in a decision.

    P=<a private directory>
    cp -R trials/sentences $P/sentences                                       # the tracked files are only read
    bash clausal/mutation/workcopy.sh $P/sentences/work/clausal               # scratch copy of clausal/ AT THE FROZEN COMMIT
    python3 clausal/compose_tests/l4r.py $P/sentences --gold                  # 1. the gold readings (no composer is run); writes l4r_a1/gold.json
    tools/sem.sh 3 -- python3 clausal/compose_tests/l4r.py $P/sentences --smoke   # 2. plumbing, three sentences that are not of the 48
    tools/sem.sh 3 -- python3 clausal/compose_tests/l4r.py $P/sentences       # 3. THE ONE RUN; writes l4r_a1/{results.json,REPORT.md}
    python3 clausal/compose_tests/l4r.py $P/sentences --print                 # the report again

EVERYTHING BELOW IS FROZEN IN THIS FILE BEFORE THE RUN (and this file is committed with the composer before step 1).

THE GOLD READINGS (--gold). trials/sentences/rewordings.py holds, for 30 of the 48, the trial runner's expert rewording
into the book as it was at the trial. Since then the book retired forms (plan node Q4). Each rewording is compiled with
the CURRENT compiler; where it is refused as a retired form it is rewritten by following the refusal ("write the clause
as: ...", the method of clausebook/q4/sentences_migrate.py), at most 8 times. A rewording that then compiles is the GOLD
READING of its sentence. The other sentences have NO gold reading: the 18 the trial runner found no rewording for
(recorded with the missing piece the runner named), and any rewording that cannot be migrated. The study projects that
the pieces of the last wave make some of the 18 expressible; no gold is written for them here (that is the work of a
non-builder), so they are scored as sentences with no gold reading, and that is said in the report.
Nothing of the composer is run by --gold, and no gold sentence is written or edited by hand.

WHAT IS RUN (step 3), per sentence exactly as its author wrote it, with no system given and no human choice:
  A1   compose2.compose(sentence)                    ANSWER / ASK (system | operation | reading | dropped) / DECLINE
  A1d  where the sentence has a gold reading: dialogue.converse(sentence, Oracle([gold])), at most 3 questions.
       The oracle answers from the gold reading only (clausal/dialogue.py).
  The sentences that come out (an ANSWER of A1; the sentence a dialogue ends with; each gold reading) are replayed on the
  author's five recorded cases with the trial's own machinery, as compose_tests/l4b.py does for version 1 (arm A0).

HOW A SENTENCE IS JUDGED ON THE CASES: exactly as in l4b.py (its functions are used). Per case: agrees / silent / says
more / CONTRADICTS / NOT EVALUATED / NOT ENCODABLE. Per sentence: RIGHT (at least one encodable case, and every
encodable case agrees), CONTRADICTS, NOT-EVALUABLE, SCOPE-DIFFERS, NOT-SCORABLE (no encodable case).

THE TALLIES (each of the 48 in exactly one row; the same rows as the development set, compose_tests/dev.py):
  answered right          A1 answers with no question, and the answer is RIGHT on the author's cases
  right after questions   the sentence has a gold reading, A1 did not answer alone, and the dialogue ends ANSWER or CHOSEN
                          AT GOLD (the same Lean term as the gold reading, or proved equal to it) within 3 questions
  answered wrong          A1 answers with no question and the answer is not RIGHT on the cases (this includes every answer
                          to a sentence none of whose cases is encodable)
  wrong after questions   the dialogue ends ANSWER or CHOSEN with a sentence that is not the gold reading
  asked                   not answered: an ASK on a sentence with no gold reading, or a dialogue that ends UNRESOLVED
  declined                DECLINE
  declined but expressible   of the declined: the sentence has a gold reading
  A0 beside it, from the committed run compose_tests/l4b_a0/results.json (version 1 never asks and never declines):
  answered right = TOP-RIGHT; answered wrong = every other sentence (RIGHT-IN-TOP-3, WRONG-READING, NOT-SCORABLE: its top
  candidate was given as the answer).
  Also reported: for each A1 answer, the verdict against the gold reading where there is one; the questions asked.

NOTHING IS CHANGED AFTER THIS RUN. What it suggests is listed as proposals (clausal/COMPOSE2.md).
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "l4r_a1"
MAX_STEPS = 8


def migrate(comp, compile_sentence, Problem, text: str, systems: list) -> dict:
    """One rewording through the current compiler, following retired-form refusals. No hand edit."""
    line, steps, last = text, 0, None
    while True:
        rd = compile_sentence(comp, line, None)
        system = None
        if isinstance(rd, Problem):
            for d in systems:                        # a sentence two systems read, or one only a hint settles
                r2 = compile_sentence(comp, line, d)
                if not isinstance(r2, Problem):
                    rd, system = r2, d
                    break
        if not isinstance(rd, Problem):
            return {"sentence": line, "steps": steps, "status": "COMPILED", "system": rd.info["domain"], "needs_system": system is not None}
        last = rd
        m = re.search(r': "(.*?)" is written in a way', rd.message or "")
        h = re.search(r'write the clause as: "(.*?)"\n', (rd.hint or "") + "\n")
        if not (m and h) or steps >= MAX_STEPS:
            break
        old, new = m.group(1), h.group(1)
        i = line.lower().find(old.lower())
        if i < 0:
            break
        new = new[0].upper() + new[1:] if line[i].isupper() else new
        line, steps = line[:i] + new + line[i + len(old):], steps + 1
    return {"sentence": None, "steps": steps, "status": "REFUSED: " + (last.status if last is not None else "?"), "last_tried": line,
            "message": (last.message or "")[:300] if last is not None else None}


def gold_main(trial: Path) -> int:
    work = trial / "work" / "clausal"
    sys.path.insert(0, str(trial))
    sys.path.insert(0, str(work))
    import os
    os.chdir(work)
    import rewordings
    from clausal import compose
    from clausal.core import Problem
    voc, comp = compose.load()
    systems = sorted({o["domain"] for o in voc.ops.values()})
    authors = json.loads((trial / "authors.json").read_text())["authors"]
    keys = [f"{a['author']}/{r['id']}" for a in authors for r in a["rules"]]
    assert len(keys) == 48
    out = {}
    for k in keys:
        v = rewordings.R.get(k) or {}
        if not v.get("text"):
            out[k] = {"sentence": None, "status": "NO REWORDING IN THE TRIAL", "missing": v.get("missing"), "fit": v.get("fit")}
            continue
        g = migrate(comp, compose.compile_sentence, Problem, v["text"], systems)
        g["trial_rewording"] = v["text"]
        out[k] = g
    n = sum(1 for g in out.values() if g["sentence"])
    res = {"what": "GOLD READINGS for the 48 frozen sentences: the trial runner's expert rewordings (trials/sentences/rewordings.py), "
                   "each compiled with the current compiler and, where refused as a retired form, rewritten by following the refusal. "
                   "Generated by clausal/compose_tests/l4r.py --gold; no sentence written or edited by hand; the composer is not run.",
           "date": time.strftime("%Y-%m-%d"), "sentences": 48, "with_gold": n,
           "rewordings_in_the_trial": sum(1 for g in out.values() if g.get("trial_rewording")),
           "rewritten_by_following_refusals": sum(1 for g in out.values() if g.get("sentence") and g.get("steps")),
           "not_migrated": sorted(k for k, g in out.items() if g.get("trial_rewording") and not g["sentence"]), "gold": out}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "gold.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    print(f"gold readings: {n} of 48 ({res['rewordings_in_the_trial']} rewordings in the trial; {res['rewritten_by_following_refusals']} rewritten by "
          f"following refusals; not migrated: {res['not_migrated'] or 'none'})")
    return 0


def run_main(trial: Path, smoke: bool) -> int:
    import l4b                                       # the trial plumbing and the judging of arm A0 (reads sys.argv[1]; chdir to the scratch copy)
    from clausal import compose, compose2, dialogue  # the scratch copy
    from clausal.core import Problem
    cs, rv = l4b.cs, l4b.rv
    work = l4b.WORK
    t0 = time.time()
    if smoke:
        flat = [(k, {"rule": s, "meantToBeTrue": True}) for k, s, _ in l4b.SMOKE]
        cs.CASES = {k: [cs.C("SMOKE", v, e) for v, e in cases] for k, _, cases in l4b.SMOKE}
        gold = {"smoke/rejected": {"sentence": "A rejected transfer never changes the ledger", "system": "ledger"},
                "smoke/deposit": {"sentence": "A deposit increases the wallet's balance by exactly the amount", "system": "wallet"},
                "smoke/money": {"sentence": None}}
        out_dir = work / "build" / "l4r_smoke"
    else:
        authors = json.loads((trial / "authors.json").read_text())["authors"]
        flat = [(f"{a['author']}/{r['id']}", r) for a in authors for r in a["rules"]]
        assert len(flat) == 48, len(flat)
        gold = json.loads((OUT / "gold.json").read_text())["gold"]
        out_dir = OUT
    voc, comp = compose.load()
    rows, uniq, op_of = [], {}, {}

    def want(c):
        """A sentence to replay: {sentence, system, operations, key}."""
        if c is None:
            return
        uniq.setdefault(c["sentence"], f"c{len(uniq):03d}")
        op_of.setdefault(c["sentence"], c["operations"][0][0])

    def cand_of(sentence, system):
        rd = compose.compile_sentence(comp, sentence, None)
        if isinstance(rd, Problem):
            rd = compose.compile_sentence(comp, sentence, system)
        return {"sentence": sentence, "system": rd.info["domain"], "operations": [[o["id"] for o in c["ops"]] for c in rd.info["clauses"]],
                "key": compose.reading_key(rd), "outside_books": compose2.outside_books(voc, rd)}

    for k, r in flat:
        g = gold.get(k) or {}
        row = {"key": k, "rule": r["rule"], "meantToBeTrue": r["meantToBeTrue"], "gold": g.get("sentence"), "gold_status": g.get("status"),
               "gold_missing": g.get("missing"), "A1": None, "A1d": None, "sentences": {}}
        try:
            a1 = compose2.compose(r["rule"])
            row["A1"] = {"outcome": a1["outcome"], "ask": a1["ask"], "why": a1["why"], "system": a1.get("system"), "counts": a1.get("counts"),
                         "missing_kinds": a1.get("missing_kinds"),
                         "questions": [{x: q.get(x) for x in ("a", "b", "verdict")} for q in a1.get("questions") or []],
                         "shown": [{"sentence": c["sentence"], "dropped": c["coverage"]["dropped"], "added": c["coverage"]["added"],
                                    "condition_dropped": c["coverage"]["condition_dropped"], "full": c["coverage"]["full"],
                                    "order_refused": c["coverage"].get("order_refused"), "clause_by_clause": c.get("clause_by_clause", False),
                                    "words": c["coverage"]["words"]} for c in a1["candidates"]]}
            if a1["outcome"] == "ANSWER":
                row["sentences"]["A1"] = cand_of(a1["answer"]["sentence"], a1["answer"]["system"])
        except Exception as e:                       # a crash of the composer is a result, not a reason to stop
            row["A1"] = {"outcome": "CRASH", "ask": None, "why": repr(e), "shown": []}
        if g.get("sentence"):
            row["sentences"]["gold"] = cand_of(g["sentence"], g.get("system"))
            try:
                orc = dialogue.Oracle([g["sentence"]], row["sentences"]["gold"]["system"])
                d = dialogue.converse(r["rule"], orc)
                ag = dialogue.at_gold(d, orc)
                row["A1d"] = {"end": d["end"], "questions": d["questions"], "why": d["why"], "last_outcome": d.get("last_outcome"),
                              "turns": [{"kind": t["kind"], "answer": t["answer"], "values": t.get("values"),
                                         "shown": [x["sentence"] for x in t.get("shown") or t.get("candidates") or []]} for t in d["turns"]],
                              "acknowledgement": d["acknowledgement"], "against_gold": ag["verdict"], "at_gold": ag["at_gold"], "sentence": d["sentence"]}
                if d["sentence"]:
                    row["sentences"]["A1d"] = cand_of(d["sentence"], d["system"])
                if row["A1"]["outcome"] == "ANSWER":
                    row["A1"]["against_gold"] = orc.is_gold([{"sentence": a1["answer"]["sentence"], "system": a1["answer"]["system"]}])[0]["verdict"]
            except Exception as e:
                row["A1d"] = {"end": "CRASH", "questions": 0, "why": repr(e), "turns": [], "at_gold": False, "against_gold": None, "sentence": None}
        for c in row["sentences"].values():
            if not c["outside_books"]:
                want(c)
        rows.append(row)
        print(f"{k}: {row['A1']['outcome']} {row['A1']['ask'] or ''}" + (f" | dialogue {row['A1d']['end']} after {row['A1d']['questions']}, at gold {row['A1d']['at_gold']}" if row["A1d"] else ""),
              file=sys.stderr, flush=True)
    t_compose = round(time.time() - t0, 1)
    # ---- the replay on the authors' cases: the plumbing of l4b.py
    log = {}
    status = {}
    if uniq:
        files = l4b.list_candidates(voc, uniq, op_of)
        log["feature_files"] = {p: len(v) for p, v in files.items()}
        rc, out, secs = rv.sh("python3 -m clausal gen")
        log["gen"] = {"rc": rc, "secs": secs, "tail": out[-300:]}
        assert rc == 0, out[-3000:]
        gen = json.loads((work / "build" / "evidence_gen.json").read_text())
        rid = {s: f"Rule.{l4b.FEATURE}_{p}.{uniq[s]}" for p, v in files.items() for s in v}
        log["without_generated_predicate"] = [s for s, i in rid.items() if i not in gen["readings"]]
        ids = [i for i in rid.values() if i in gen["readings"]]
        rc, out, secs = rv.sh(f"python3 -m clausal evidence --quick --only '{','.join(ids)}'", timeout=3600)
        log["evidence"] = {"rc": rc, "secs": secs, "line": out.strip().splitlines()[-1] if out.strip() else ""}
        reqs = []
        for row in rows:
            for arm, c in row["sentences"].items():
                if c["sentence"] not in rid:
                    continue
                for n, case in enumerate(cs.CASES.get(row["key"], [])):
                    if case["values"]:
                        reqs.append({"rule": rid[c["sentence"]], "values": case["values"], "tag": f"{row['key']}|{arm}|{n}"})
        f = work / "evidence" / "target" / "l4r_replay.jsonl"
        f.write_text("\n".join(json.dumps(r) for r in reqs) + "\n")
        rc, out, secs = rv.sh(f"./target/debug/rule-evidence --replay '{f}' --timeout-secs 20 --trees '{work / 'build' / 'trees.json'}'", cwd=work / "evidence")
        status = {r["tag"]: r for r in (json.loads(l) for l in out.splitlines() if l.startswith("{")) if "tag" in r}
        log["replay"] = {"rc": rc, "requests": len(reqs), "answers": len(status), "secs": secs}
    for row in rows:
        cases = cs.CASES.get(row["key"], [])
        row["cases"] = [{k: c[k] for k in ("unit", "values", "expect", "note")} for c in cases]
        for arm, c in row["sentences"].items():
            if c["outside_books"]:
                c["cases"], c["kind"] = [], "NOT-OF-ITS-PROJECT"
                continue
            clauses = c["key"].split(" | ")
            mod = l4b.modifier(c) if len(clauses) == 1 else None
            ops = c["operations"][0]
            js = []
            for n, case in enumerate(cases):
                if not case["values"]:
                    js.append({"status": "not encodable", "judgement": "NOT ENCODABLE"})
                    continue
                st = status.get(f"{row['key']}|{arm}|{n}", {}).get("status", "no answer")
                rec = {"status": st}
                if st == "holds" and mod and len(ops) == 1:
                    try:
                        acc = l4b.accepted(ops[0], rv.outcome(case["values"]))
                    except Exception:
                        acc = None
                    if acc is not None and acc is not (mod == "successful"):
                        rec["status"], rec["replay_status"] = "out-of-scope", f"holds (vacuously: the call is outside '{mod}')"
                rec["judgement"] = rv.judge(case["expect"], rec["status"])
                js.append(rec)
            c["cases"] = js
            c["kind"] = l4b.kind_of([j["judgement"] for j in js])
        row["cell"] = cell(row)
    res = {"schema": "l4r-a1-v1", "date": time.strftime("%Y-%m-%d"),
           "what": "ARM A1 (CONTAMINATED): composer version 2, no language model, no system given, with the dialogue and the oracle author where a "
                   "gold reading exists, on the 48 frozen trial sentences; sentences replayed on the authors' cases through the trial machinery",
           "seconds_compose": t_compose, "log": log, "sentences": len(rows), "rows": rows, "tallies": tallies(rows)}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "results.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str) + "\n")
    text = report(res)
    (out_dir / "REPORT.md").write_text(text + "\n")
    print(text)
    return 0


ROWS = ("answered wrong", "wrong after questions", "answered right", "right after questions", "asked", "declined")


def cell(row: dict) -> str:
    a = row["A1"]
    if a["outcome"] == "ANSWER":
        return "answered right" if row["sentences"]["A1"]["kind"] == "RIGHT" else "answered wrong"
    d = row.get("A1d")
    if d and d["end"] in ("ANSWER", "CHOSEN"):
        return "right after questions" if d["at_gold"] else "wrong after questions"
    if d and d["end"] == "DECLINE" or (not d and a["outcome"] == "DECLINE"):
        return "declined"
    return "asked"                                   # ASK with no gold reading; UNRESOLVED; a crash is not an answer


def tallies(rows: list) -> dict:
    t = {k: sorted(r["key"] for r in rows if r["cell"] == k) for k in ROWS}
    t["declined but expressible"] = sorted(r["key"] for r in rows if r["cell"] == "declined" and r["gold"])
    t["with_gold"] = sum(1 for r in rows if r["gold"])
    d = [r["A1d"] for r in rows if r.get("A1d")]
    t["dialogue"] = {"ends": {e: sum(x["end"] == e for x in d) for e in ("ANSWER", "CHOSEN", "UNRESOLVED", "DECLINE", "CRASH")},
                     "at_gold": sum(x["at_gold"] for x in d), "questions_of_those_at_gold": [x["questions"] for x in d if x["at_gold"]],
                     "question_kinds": {k: sum(t_["kind"] == k for x in d for t_ in x["turns"]) for k in ("system", "operation", "input", "which", "accept")}}
    t["A1_outcomes"] = {}
    for r in rows:
        k = r["A1"]["outcome"] + (f" ({r['A1']['ask']})" if r["A1"]["ask"] else "")
        t["A1_outcomes"][k] = t["A1_outcomes"].get(k, 0) + 1
    t["gold_not_right_on_the_cases"] = sorted(f"{r['key']} ({r['sentences']['gold']['kind']})" for r in rows if r["gold"] and r["sentences"]["gold"]["kind"] != "RIGHT")
    a0 = HERE / "l4b_a0" / "results.json"
    if a0.exists() and len(rows) == 48:
        c = json.loads(a0.read_text())["counts"]
        t["A0"] = {"answered right": c["TOP-RIGHT"], "answered wrong": 48 - c["TOP-RIGHT"], "right after questions": 0, "wrong after questions": 0,
                   "asked": 0, "declined": 0, "declined but expressible": 0, "counts": c}
    return t


def say_cases(c: dict) -> str:
    return ", ".join(j["judgement"] + ("" if j["judgement"] in ("agrees", "NOT ENCODABLE") else f" [{j['status']}]") for j in c["cases"]) or "none"


def report(d: dict) -> str:
    t, n = d["tallies"], d["sentences"]
    a0 = t.get("A0")
    o = ["# Arm A1 on the 48 frozen sentences: composer version 2 (no language model) with the oracle author. CONTAMINATED", "",
         f"Run of {d['date']}. Generated by `clausal/compose_tests/l4r.py`; do not edit. {d['what']}.", "",
         "**Contaminated: a development measure.** Version 2 was designed from the failures of version 1 on these sentences, and the wording "
         "changes of the last wave coincide with some of them. Definitions: the text at the top of `l4r.py`, frozen before the run.", "",
         f"Gold readings: {t['with_gold']} of {n} (the trial's expert rewordings, migrated by following the compiler's refusals; `l4r_a1/gold.json`). "
         f"The other {n - t['with_gold']} have none and can only be answered wrong, asked or declined here.", "",
         "| | A1 (version 2 + oracle author) | A0 (version 1, top candidate) |", "|---|---|---|"]
    for k in ROWS:
        o.append(f"| {k} | {len(t[k])} | {a0[k] if a0 else 'n/a'} |")
    o.append(f"| declined but expressible (of the declined) | {len(t['declined but expressible'])} | {a0['declined but expressible'] if a0 else 'n/a'} |")
    g = t["dialogue"]
    qs = g["questions_of_those_at_gold"]
    o += ["", "A1 alone, before any question: " + ", ".join(f"{k} {v}" for k, v in sorted(t["A1_outcomes"].items())) + ".",
          f"The dialogue ({t['with_gold']} sentences with a gold reading): ends ANSWER {g['ends']['ANSWER']}, CHOSEN {g['ends']['CHOSEN']}, UNRESOLVED {g['ends']['UNRESOLVED']}, "
          f"DECLINE {g['ends']['DECLINE']}, crashed {g['ends']['CRASH']}; at the gold reading {g['at_gold']}; questions where it ends at gold: {sum(qs)} over {len(qs)}"
          + (f" ({sum(qs) / len(qs):.2f} each)" if qs else "") + "; kinds asked: " + ", ".join(f"{k} {v}" for k, v in g["question_kinds"].items()) + ".",
          "Gold readings that are not RIGHT on the author's cases: " + (", ".join(t["gold_not_right_on_the_cases"]) or "none") + ".", ""]
    if d.get("log", {}).get("replay"):
        o.append(f"Replay: {d['log']['replay']['requests']} requests, {d['log']['replay']['answers']} answers; sentences without a generated predicate: "
                 f"{len(d['log'].get('without_generated_predicate') or [])}.")
    titles = {"answered wrong": "## Wrong answers (first)", "wrong after questions": "## Wrong after questions (the dialogue ended at another reading)",
              "answered right": "## Answered right with no question", "right after questions": "## Right after questions (oracle author)",
              "asked": "## Asked, not resolved", "declined": "## Declined"}
    for k in ROWS:
        o += ["", titles[k], ""]
        if not t[k]:
            o.append("None.")
        for r in d["rows"]:
            if r["cell"] != k:
                continue
            a = r["A1"]
            o.append(f"- **{r['key']}** (meant {'true' if r['meantToBeTrue'] else 'false'}): \"{r['rule']}\"")
            o.append("  - gold: " + (f"\"{r['gold']}\" ({r['sentences']['gold']['kind']} on the cases)" if r["gold"] else f"none ({r['gold_status']}"
                                     + (f"; missing: {r['gold_missing']}" if r.get("gold_missing") else "") + ")"))
            head = a["outcome"] + (f" ({a['ask']})" if a["ask"] else "")
            if a["outcome"] == "ANSWER":
                c = r["sentences"]["A1"]
                o.append(f"  - A1: **ANSWER** \"{c['sentence']}\": {c['kind']}; cases: {say_cases(c)}" + (f"; against gold: {a['against_gold']}" if a.get("against_gold") else ""))
            elif a["shown"]:
                s = a["shown"][0]
                o.append(f"  - A1: {head}; first shown \"{s['sentence']}\"" + (f" (dropped: {', '.join(s['dropped'])})" if s["dropped"] else "")
                         + (f" (added: {', '.join(s['added'])})" if s["added"] else "") + (f" (CONDITION DROPPED: {'; '.join(s['condition_dropped'])})" if s["condition_dropped"] else ""))
            else:
                o.append(f"  - A1: {head}: {(a['why'] or '')[:220]}")
            x = r.get("A1d")
            if x:
                turns = "; ".join(f"{t_['kind']} -> {t_['answer'] if t_['answer'] is not None else 'none'}" for t_ in x["turns"]) or "no question"
                c = r["sentences"].get("A1d")
                o.append(f"  - A1d (oracle author): {x['end']} after {x['questions']} question(s) [{turns}]"
                         + (f": \"{c['sentence']}\"; against gold: {x['against_gold']}; on the cases: {c['kind']} ({say_cases(c)})" if c else f": {(x['why'] or '')[:200]}"))
    return "\n".join(o)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    if "--print" in sys.argv:
        print(report(json.loads((OUT / "results.json").read_text())))
        sys.exit(0)
    TRIAL = Path(sys.argv[1]).resolve()
    assert (TRIAL / "work" / "clausal" / "clausal" / "compose2.py").exists(), f"no scratch copy at {TRIAL}/work/clausal (see the usage)"
    if "--gold" in sys.argv:
        sys.exit(gold_main(TRIAL))
    sys.path.insert(0, str(HERE))
    sys.exit(run_main(TRIAL, "--smoke" in sys.argv))
