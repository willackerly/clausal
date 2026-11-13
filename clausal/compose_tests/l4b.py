#!/usr/bin/env python3
"""L4(b), FIRST MEASUREMENT: `clausal compose` on the 48 frozen trial sentences, scored on the authors' own cases.

    cp -R trials/sentences <private>/sentences                                 # a private copy; the tracked files are only read
    bash clausal/mutation/workcopy.sh <private>/sentences/work/clausal         # scratch copy of clausal/ (as run_v4.py wants it)
    tools/sem.sh 3 -- python3 clausal/compose_tests/l4b.py <private>/sentences [--out DIR]
    ... l4b.py <private>/sentences --smoke     the same plumbing on three sentences and cases written by the implementer (SMOKE
                                               below), NOT on the 48; writes <scratch copy>/build/l4b_smoke/. Used to check the
                                               plumbing before the one measured run.

For each of the 48 sentences of authors.json: the sentence, exactly as its author wrote it, is the rough input of
`compose.compose(sentence, None, 3)` (no system given, no language model, no human choice). The candidates are put in
a feature file of the scratch copy and go through the EXISTING trial machinery (trials/sentences/run_v4.py): `clausal
gen`, `clausal evidence --quick` (which builds the generated predicate of every reading), and `rule-evidence --replay`
of the author's five recorded cases (trials/sentences/cases.py: CASES) on the compiled Rust. `run_v4.judge` compares
what the author said of the rule at a case with the candidate reading's value there.

FROZEN BEFORE THE FIRST RUN (this file is committed with the composer's ranking rule, cue table and limits before
compose is run on any of the 48 sentences):

  per case       the replay's status of the candidate reading at the case's input: holds / fails / out-of-scope / other.
                 As in run_v4.py, a reading whose subject is "successful" or "rejected" reports "holds" on a call outside
                 that modifier (the claim is vacuous there); such a case is turned into out-of-scope, using the runner's
                 reference model (`run_v4.outcome`) for whether the call is accepted. Not applied to a sequence of two
                 operations.
                 judgement = run_v4.judge(author's word, status): agrees / silent / says more / CONTRADICTS /
                 NOT EVALUATED (no status: the candidate is about another operation, so the case's input is not an
                 input of it) / READING MISMATCH. A case the trial runner could not encode (values None) is left out.
  per candidate  RIGHT          at least one case is encodable and every encodable case `agrees`
                 CONTRADICTS    some case CONTRADICTS
                 NOT-EVALUABLE  no contradiction, some case NOT EVALUATED or READING MISMATCH
                 SCOPE-DIFFERS  none of the above: only `silent` / `says more` beside `agrees`
  per sentence   TOP-RIGHT        the top candidate is RIGHT
                 RIGHT-IN-TOP-3   the top candidate is not RIGHT; the second or the third is
                 WRONG-READING    there are candidates and none of the top three is RIGHT (the kind is the top candidate's)
                 NO-CANDIDATE     compose returned no candidate
                 NOT-SCORABLE     no case of the sentence is encodable (reported apart; the candidate is still listed)

"RIGHT" is agreement on at most five inputs. It is not a proof that the candidate is what the author meant.
Nothing is tuned after this run: what the result suggests is listed as proposals in COMPOSE.md.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(2)
TRIAL = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[sys.argv.index("--out") + 1]).resolve() if "--out" in sys.argv else Path(__file__).resolve().parent / "l4b"
WORK = TRIAL / "work" / "clausal"
assert (WORK / "clausal" / "compose.py").exists(), f"no scratch copy at {WORK} (see the usage)"
sys.path.insert(0, str(TRIAL))
sys.path.insert(0, str(WORK))
os.chdir(WORK)
import cases as cs                                   # noqa: E402  (the private copy of trials/sentences)
import run_v4 as rv                                  # noqa: E402
from clausal import compose                          # noqa: E402  (the scratch copy of clausal/)
from clausal.core import Problem                     # noqa: E402

TOP = 3
FEATURE = "l4b_compose"


def accepted(op: str, o: dict):
    """Does the runner's reference model say the call of `op` at this input is accepted?"""
    if op == "l.apply_batch":
        return True                                  # it reports a count and never rejects
    if op == "l.apply_all":
        return o.get("whole")
    if op in ("l.total", "l.lookup"):
        return o["ans"] != "none"
    return o["ans"] is True


def modifier(cand: dict):
    """The scoping modifier of a candidate's subject (the generator writes one clause): 'successful', 'rejected' or None."""
    subj = cand["key"].split(" :: ")[0].split("/given ")[0]
    return next((m for m in ("successful", "rejected") if m in subj.split("/")[1:]), None)


def kind_of(judgements: list) -> str:
    js = [j for j in judgements if j != "NOT ENCODABLE"]
    if not js:
        return "NOT-SCORABLE"
    if all(j == "agrees" for j in js):
        return "RIGHT"
    if "CONTRADICTS" in js:
        return "CONTRADICTS"
    if "NOT EVALUATED" in js or "READING MISMATCH" in js:
        return "NOT-EVALUABLE"
    return "SCOPE-DIFFERS"


def list_candidates(voc, uniq: dict, op_of: dict) -> dict:
    """Write the candidates to features/l4b_compose_<project>.feature of the scratch copy, one file per project, and list
    each file under its project in the scratch copy's projects.yaml. {project: [sentences]}."""
    import yaml
    from clausal import projects as pj, vocab
    assert WORK.resolve() != Path(__file__).resolve().parent.parent, "the scratch copy only: the tracked projects.yaml is never edited"
    files = {}
    for s in uniq:
        book = voc.home[op_of[s]].rel
        proj = next(p for p in pj.load(WORK) if any(book == f"{vocab.BOOK_DIR}/{b}" for b in p.books))
        files.setdefault(proj.name, []).append(s)
    path = WORK / pj.FILE
    raw = yaml.safe_load(path.read_text())
    for d in raw["projects"]:
        rel = f"features/{FEATURE}_{d['name']}.feature"
        d["features"] = [f for f in d["features"] if not Path(f).name.startswith(FEATURE)]
        (WORK / rel).unlink(missing_ok=True)
        if d["name"] in files:
            lines = [f"Feature: l4b compose {d['name']}", "  Candidates of `clausal compose` for the 48 trial sentences. Scratch copy only.", ""]
            for s in files[d["name"]]:
                lines += [f"  @id:{uniq[s]}", f"  Rule: {s}", ""]
            (WORK / rel).write_text("\n".join(lines))
            d["features"].append(rel)
    (WORK / "features" / f"{FEATURE}.feature").unlink(missing_ok=True)        # the one file of the first run
    path.write_text(yaml.safe_dump(raw, sort_keys=False))
    return files


# three sentences of the implementer's own with cases of the implementer's own: a plumbing check, not a measurement
SMOKE = [
    ("smoke/rejected", "if a transfer is rejected the ledger stays the same",
     [({"the_ledger": "[1, 0]", "the_transfer": "0->1:1"}, "silent"), ({"the_ledger": "[0, 0]", "the_transfer": "0->1:1"}, "holds")]),
    ("smoke/deposit", "a deposit adds exactly the amount to the wallet balance", [({"the_wallet": "5", "the_amount": "3"}, "holds")]),
    ("smoke/money", "money is never created or destroyed by a batch",
     [({"the_ledger": "[1, 0]", "the_batch": "[0->1:1]"}, "holds"), (None, "holds")]),
]


def main() -> int:
    global OUT
    t0 = time.time()
    if "--smoke" in sys.argv:
        flat = [(k, {"rule": s, "meantToBeTrue": True}) for k, s, _ in SMOKE]
        cs.CASES = {k: [cs.C("SMOKE", v, e) for v, e in cases] for k, _, cases in SMOKE}
        OUT = WORK / "build" / "l4b_smoke"
    else:
        authors = json.loads((TRIAL / "authors.json").read_text())["authors"]
        flat = [(f"{a['author']}/{r['id']}", r) for a in authors for r in a["rules"]]
        assert len(flat) == 48, len(flat)
    voc, comp = compose.load()
    rows, uniq, sys_of = [], {}, {}       # sys_of: candidate sentence -> its first operation (which project's file it goes in)
    for k, r in flat:
        aw = compose.compile_sentence(comp, r["rule"], None)
        try:
            res = compose.compose(r["rule"], None, TOP)
            err = None
        except Exception as e:                       # a crash of the composer is a result (no candidate), not a reason to stop
            res, err = {"candidates": [], "tokens": [], "generated": 0, "compiled": 0, "refused": {}, "anchored": None}, repr(e)
        for c in res["candidates"]:
            uniq.setdefault(c["sentence"], f"c{len(uniq):03d}")
            sys_of.setdefault(c["sentence"], c["operations"][0][0])
        rows.append({"key": k, "rule": r["rule"], "meantToBeTrue": r["meantToBeTrue"],
                     "as_written": "COMPILED" if not isinstance(aw, Problem) else aw.status, "compose_error": err,
                     "tokens": res["tokens"], "anchored": res["anchored"], "generated": res["generated"], "compiled": res["compiled"],
                     "refused": res["refused"],
                     "candidates": [{k2: c[k2] for k2 in ("rank", "sentence", "system", "score", "key", "operations", "unexplained",
                                                          "unsupported_pieces", "words_not_yours", "echo")} for c in res["candidates"]]})
    t_compose = round(time.time() - t0, 1)
    # the candidates as a feature of the scratch copy; the existing machinery from here on
    # REPAIR (2026-11-12, plan node L1ab; nothing that is scored changed). Since the project list (projects.yaml, plan node X7)
    # `clausal gen` reads only feature files a project lists, and a sentence may use only its project's books. One candidate
    # file spans systems, so the candidates are written to ONE FILE PER PROJECT of the scratch copy (the project whose books
    # define the candidate's operations) and each file is listed under its project in the SCRATCH COPY's projects.yaml. The
    # tracked projects.yaml is not touched. Sentences, ids (c000, ...), the order, the evidence step and the replay are as before;
    # only the feature slug in a reading's id differs (`Rule.l4b_compose_<project>.<id>`).
    files = list_candidates(voc, uniq, sys_of)
    log = {"feature_files": {p: len(v) for p, v in files.items()}}
    rc, out, secs = rv.sh("python3 -m clausal gen")
    log["gen"] = {"rc": rc, "secs": secs, "tail": out[-300:]}
    assert rc == 0, out[-3000:]
    gen = json.loads((WORK / "build" / "evidence_gen.json").read_text())
    rid = {s: f"Rule.{FEATURE}_{p}.{uniq[s]}" for p, v in files.items() for s in v}
    missing = [s for s, i in rid.items() if i not in gen["readings"]]
    log["candidates"] = {"unique": len(uniq), "without_generated_predicate": missing}
    ids = [i for i in rid.values() if i in gen["readings"]]
    rc, out, secs = rv.sh(f"python3 -m clausal evidence --quick --only '{','.join(ids)}'", timeout=3600)
    log["evidence"] = {"rc": rc, "secs": secs, "line": out.strip().splitlines()[-1] if out.strip() else ""}
    reqs = []
    for row in rows:
        for c in row["candidates"]:
            for n, case in enumerate(cs.CASES.get(row["key"], [])):
                if case["values"]:
                    reqs.append({"rule": rid[c["sentence"]], "values": case["values"], "tag": f"{row['key']}|{c['rank']}|{n}"})
    f = WORK / "evidence" / "target" / "l4b_replay.jsonl"
    f.write_text("\n".join(json.dumps(r) for r in reqs) + "\n")
    rc, out, secs = rv.sh(f"./target/debug/rule-evidence --replay '{f}' --timeout-secs 20 --trees '{WORK / 'build' / 'trees.json'}'", cwd=WORK / "evidence")
    back = {r["tag"]: r for r in (json.loads(l) for l in out.splitlines() if l.startswith("{")) if "tag" in r}
    log["replay"] = {"rc": rc, "requests": len(reqs), "answers": len(back), "secs": secs}
    for row in rows:
        cases = cs.CASES.get(row["key"], [])
        row["cases"] = [{k: c[k] for k in ("unit", "values", "expect", "note")} for c in cases]
        for c in row["candidates"]:
            mod, ops = modifier(c), c["operations"][0]
            js = []
            for n, case in enumerate(cases):
                if not case["values"]:
                    js.append({"status": "not encodable", "judgement": "NOT ENCODABLE"})
                    continue
                st = back.get(f"{row['key']}|{c['rank']}|{n}", {}).get("status", "no answer")
                rec = {"status": st}
                if st == "holds" and mod and len(ops) == 1:
                    try:
                        acc = accepted(ops[0], rv.outcome(case["values"]))
                    except Exception:
                        acc = None
                    if acc is not None and acc is not (mod == "successful"):
                        rec["status"], rec["replay_status"] = "out-of-scope", f"holds (vacuously: the call is outside '{mod}')"
                rec["judgement"] = rv.judge(case["expect"], rec["status"])
                js.append(rec)
            c["cases"] = js
            c["kind"] = kind_of([j["judgement"] for j in js])
        ks = [c["kind"] for c in row["candidates"]]
        if not ks:
            row["outcome"] = "NO-CANDIDATE"
        elif ks[0] == "NOT-SCORABLE":
            row["outcome"] = "NOT-SCORABLE"
        elif ks[0] == "RIGHT":
            row["outcome"] = "TOP-RIGHT"
        elif "RIGHT" in ks[1:]:
            row["outcome"] = "RIGHT-IN-TOP-3"
        else:
            row["outcome"] = "WRONG-READING"
    counts = {o: sum(r["outcome"] == o for r in rows) for o in ("TOP-RIGHT", "RIGHT-IN-TOP-3", "WRONG-READING", "NO-CANDIDATE", "NOT-SCORABLE")}
    res = {"schema": "l4b-compose-first-measurement-v1", "date": time.strftime("%Y-%m-%d"),
           "what": "clausal compose (no language model, no human choice, no system given) on the 48 frozen trial sentences; "
                   "top 3 candidates replayed on the authors' five cases through the existing trial machinery",
           "authors_are": "language models (proxy authors), not people",
           "compose_limits": compose.compose("a transfer", None, 1)["limits"], "top": TOP, "seconds_compose": t_compose,
           "log": log, "counts": counts, "sentences": len(rows), "rows": rows}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "results.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    text = report(res)
    (OUT / "REPORT.md").write_text(text + "\n")
    print(text)
    return 0


def say_cases(c: dict) -> str:
    return ", ".join(j["judgement"] + ("" if j["judgement"] in ("agrees", "NOT ENCODABLE") else f" [{j['status']}]") for j in c["cases"])


def report(d: dict) -> str:
    n = d["sentences"]
    c = d["counts"]
    o = ["# L4(b), first measurement: `clausal compose` on the 48 frozen sentences", "",
         f"Run of {d['date']}. Generated by `clausal/compose_tests/l4b.py`; do not edit. " + d["what"] + ". The authors are " + d["authors_are"] + ".",
         "", "| outcome | sentences |", "|---|---|"]
    for k in ("TOP-RIGHT", "RIGHT-IN-TOP-3", "WRONG-READING", "NO-CANDIDATE", "NOT-SCORABLE"):
        o.append(f"| {k} | {c[k]} of {n} |")
    wrong = [r for r in d["rows"] if r["outcome"] == "WRONG-READING"]
    kinds = {}
    for r in wrong:
        kinds[r["candidates"][0]["kind"]] = kinds.get(r["candidates"][0]["kind"], 0) + 1
    o += ["", "Wrong readings by the kind of the top candidate: " + (", ".join(f"{k} {v}" for k, v in sorted(kinds.items())) or "none") + ".",
          f"As written (before compose), {sum(r['as_written'] == 'COMPILED' for r in d['rows'])} of {n} sentences compile.",
          f"Unique candidate sentences: {d['log']['candidates']['unique']}; replay requests {d['log']['replay']['requests']}, answers {d['log']['replay']['answers']}.",
          "", "## Wrong readings (first)", ""]
    for title, pick in (("", "WRONG-READING"), ("## No candidate", "NO-CANDIDATE"), ("## Not scorable", "NOT-SCORABLE"),
                        ("## A right candidate in the top three, not first", "RIGHT-IN-TOP-3"), ("## Top candidate right on every encodable case", "TOP-RIGHT")):
        if title:
            o += ["", title, ""]
        for r in d["rows"]:
            if r["outcome"] != pick:
                continue
            o.append(f"- **{r['key']}** (meant {'true' if r['meantToBeTrue'] else 'false'}; as written: {r['as_written']}): \"{r['rule']}\"")
            if r["compose_error"]:
                o.append(f"  - compose failed: {r['compose_error']}")
            if not r["candidates"]:
                two = r["refused"].get("reads_in_two_systems") or []
                o.append(f"  - no candidate: {r['compiled']} of {r['generated']} generated sentences were compiled, none passed"
                         + (f"; AMBIGUOUS across systems as written: {'; '.join(two)}" if two else ""))
            for cand in r["candidates"]:
                o.append(f"  - [{cand['rank']}] {cand['kind']}: \"{cand['sentence']}\" (score {cand['score']}; words not accounted for: "
                         f"{', '.join(cand['unexplained']) or 'none'})")
                o.append(f"    - cases: {say_cases(cand)}")
    return "\n".join(o)


if __name__ == "__main__":
    if "--print" in sys.argv:
        print(report(json.loads((OUT / "results.json").read_text())))
        sys.exit(0)
    sys.exit(main())
