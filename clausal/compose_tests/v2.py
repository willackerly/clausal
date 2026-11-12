#!/usr/bin/env python3
"""Tests of composer version 2 (clausal/compose2.py: plan nodes L1a, L1b) and of the tree interface (clausal/ctree.py: L1e).
Run from clausal/:

    python3 compose_tests/v2.py             no Lean, no cargo: about a minute
    python3 compose_tests/v2.py --json      the counts as JSON (what COMPOSE2.md quotes)
    python3 compose_tests/v2.py --l3        also one ASK (reading) through `clausal separate` (needs lean/ built and cargo)

THE GOLD of every test here is the book's own fixtures: the Rule lines of features/ and controls/ that
clausebook/terms.lock.json records as compiled. None of the 48 trial sentences and none of the development set is used.

  identity     every compiled fixture Rule line, given as the rough sentence (in the system the lock compiles it in), comes back
               as ITSELF: outcome ANSWER, the same sentence, the Lean term whose digest the lock records, coverage full.
               Also reported: the same with no system given (ANSWER or ASK (system), never another sentence); what the refused
               fixture Rule lines get; and, informational, how many come back when the first step (a sentence of the book is its
               own answer) is switched off, i.e. what version 1's generator and ranking reach.
  round trip   tree -> sentence -> compile -> the same Lean term and the same tree, on every compiled fixture Rule line; each tree
               validates against the schema generated from the book; trees that name a piece the book does not have, a role
               of another operation, or leave a hole out are rejected by the schema; a tree whose sentence the compiler refuses
               is refused with the compiler's message.
  seeded drop  from the tree of every compiled fixture Rule line, ONE condition or narrowing is deleted at a time (the
               narrowing word, `internal`, the "for which" condition, the tie, the condition of "is accepted whenever / only if /
               exactly when", the class of "..., if <first call ...>"); the mutated tree is written as a sentence and compiled.
               The ORIGINAL sentence is the rough sentence and the mutated reading the candidate: `coverage` must report the
               drop (the candidate is not full, and a word the deletion removed is DROPPED or the span is CONDITION DROPPED).
               100% is required. This is also the planted composer that drops every condition.
  no silent    every ANSWER of a set of rough sentences (compose_tests/cases.json, the thirteen of version 1's implementer)
               has no DROPPED word, no ADDED piece and no CONDITION DROPPED; every word has exactly one status.
  filters, system question, decline, acknowledgement, --write   as named below.
"""
import json
import sys
import tempfile
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from clausal import compose as v1, compose2 as c2, ctree       # noqa: E402
from clausal.core import Problem                                # noqa: E402
from clausal.pipeline import ROOT                               # noqa: E402

fails, numbers = [], {}


def check(name, ok, why=""):
    print(("ok    " if ok else "FAIL  ") + name + ("" if ok else f": {why}"))
    if not ok:
        fails.append(name)


def drops(tree: dict) -> list:
    """[(what, mutated tree)]: the tree with one condition or narrowing deleted."""
    out = []
    for k, c in enumerate(tree["clauses"]):
        def mut(f):
            t = json.loads(json.dumps(tree))
            f(t["clauses"][k])
            return t
        s = c["subject"]
        if s["narrowing"]:
            out.append((f"narrowing `{s['narrowing']}`", mut(lambda x: x["subject"].update(narrowing=None))))
        if s["internal"]:
            out.append(("`internal`", mut(lambda x: x["subject"].update(internal=False))))
        if s["condition"] is not None:
            out.append(("the 'for which' condition", mut(lambda x: x["subject"].update(condition=None))))
        if s["tie"] is not None:
            out.append(("the tie", mut(lambda x: x["subject"].update(tie=None))))
        for j, cl in enumerate(c["claims"]):
            if cl.get("piece") in ("if_then", "only_if", "exactly_when"):
                out.append((f"the condition of `{cl['piece']}`",
                            mut(lambda x, j=j: x["claims"].__setitem__(j, {"piece": "always", "args": {"c": {"piece": "accepted", "args": {}}}}))))
            if cl.get("piece") == "same_answer_if":
                out.append(("the first-call class of `same_answer_if`",
                            mut(lambda x, j=j, cl=cl: x["claims"].__setitem__(j, {"piece": "same_answer", "args": {"v": cl["args"]["v"]}}))))
    return out


def main():
    voc, comp = v1.load()
    lock = json.loads((ROOT / "clausebook" / "terms.lock.json").read_text())["sentences"]
    lines = ctree.rule_lines(voc, comp)
    gold = [(i, src, text, hint, rd) for i, src, text, hint, rd in lines if not isinstance(rd, Problem)]
    refused = [(i, src, text, hint, rd) for i, src, text, hint, rd in lines if isinstance(rd, Problem)]
    check(f"gold: the compiled fixture Rule lines are the {sum(v['compiled'] for k, v in lock.items() if k.startswith('Rule.'))} the lock records",
          {i for i, *_ in gold} == {k for k, v in lock.items() if k.startswith("Rule.") and v["compiled"]})

    # ---------------------------------------------------------------- identity
    same = full = bare = 0
    bad = []
    for i, src, text, hint, rd in gold:
        r = c2.compose(text, hint, l3=False)
        a = r["answer"]
        ok = (r["outcome"] == "ANSWER" and a["sentence"] == text and a["term_sha256"] == ctree.body_sha(rd)
              and lock[i]["lean_sha256"] == ctree.term_sha(rd))
        same += ok
        full += bool(ok and a["coverage"]["full"])
        if not ok or not a["coverage"]["full"]:
            bad.append((i, r["outcome"], a and (a["coverage"]["dropped"], a["coverage"]["added"], a["coverage"]["condition_dropped"])))
        r0 = c2.compose(text, None, l3=False)
        bare += (r0["outcome"] == "ANSWER" and r0["answer"]["sentence"] == text) or (r0["outcome"] == "ASK" and r0["ask"] == "system")
    numbers["identity"] = {"gold": len(gold), "came_back_as_itself": same, "with_full_coverage": full, "no_system_given_itself_or_system_question": bare}
    check(f"identity: {same} of {len(gold)} compiled fixture Rule lines come back as themselves (ANSWER, same sentence, the locked term)", same == len(gold), str(bad[:3]))
    check(f"identity: {full} of {len(gold)} with full coverage under their own tree (no DROPPED, no ADDED, no CONDITION DROPPED)", full == len(gold), str(bad[:3]))
    check(f"identity: with no system given, {bare} of {len(gold)} are ANSWERED as themselves or get the system question", bare == len(gold))
    out = Counter()
    answered = []
    for i, src, text, hint, rd in refused:
        r = c2.compose(text, hint, l3=False)
        out[r["outcome"] + (f" ({r['ask']})" if r["ask"] else "")] += 1
        if r["outcome"] == "ANSWER":
            answered.append((text, r["answer"]["sentence"]))
    numbers["refused_fixture_lines"] = {"n": len(refused), "outcomes": dict(out), "answered": answered}
    check(f"identity: none of the {len(refused)} REFUSED fixture Rule lines is ANSWERED, as itself or as another sentence ({dict(out)})",
          not answered, str(answered[:2]))
    reach = Counter()
    for i, src, text, hint, rd in gold:
        r = c2.compose(text, hint, l3=False, identity=False)
        if r["outcome"] == "ANSWER" and r["answer"]["term_sha256"] == ctree.body_sha(rd):
            reach["ANSWER, the same term"] += 1
        elif r["outcome"] == "ANSWER":
            reach["ANSWER, ANOTHER TERM"] += 1
        else:
            reach[r["outcome"] + (f" ({r['ask']})" if r["ask"] else "")] += 1
    numbers["generator_reach_without_the_identity_step"] = dict(reach)
    print(f"info  generator reach (identity step off): {dict(reach)} of {len(gold)}")
    check("identity step off: no fixture sentence is ANSWERED with another term", reach["ANSWER, ANOTHER TERM"] == 0)

    # ---------------------------------------------------------------- round trip and schema
    rt = ctree.check(voc, comp)
    numbers["round_trip"] = {k: rt[k] for k in ("rule_lines", "compiled", "round_trip_same_term", "same_sentence", "term_is_the_locked_one", "schema_valid")}
    check(f"round trip: tree -> sentence -> compile -> the same term: {rt['round_trip_same_term']} of {rt['compiled']}", rt["round_trip_same_term"] == rt["compiled"] == len(gold),
          str([r for r in rt["rows"] if r["compiled"] and not r["ok"]][:2]))
    check(f"round trip: the term is the one the lock records: {rt['term_is_the_locked_one']} of {rt['compiled']}", rt["term_is_the_locked_one"] == rt["compiled"])
    check(f"schema: every fixture tree validates: {rt['schema_valid']} of {rt['compiled']}", rt["schema_valid"] == rt["compiled"])
    sch = ctree.schema(voc)
    try:
        import jsonschema
        jsonschema.Draft202012Validator.check_schema(sch)
        V = jsonschema.Draft202012Validator(sch)
        agree = sum(V.is_valid(ctree.of_reading(rd)) for *_, rd in gold)
        check(f"schema: a draft 2020-12 schema; the `jsonschema` package accepts {agree} of {len(gold)} fixture trees", agree == len(gold))
    except ImportError:
        print("info  the `jsonschema` package is not installed: the schema was checked with ctree.validate only")
    t = ctree.of_reading(v1.compile_sentence(comp, "A rejected transfer never changes the balance of account the sender of the transfer of the ledger"))
    neg = {}
    m = json.loads(json.dumps(t)); m["clauses"][0]["claims"][0]["piece"] = "conserves_everything"; neg["a piece the book does not have"] = m
    m = json.loads(json.dumps(t)); m["clauses"][0]["claims"][0]["args"]["m"]["args"]["k"]["args"]["t"] = {"role": "the wallet"}; neg["a role of another operation"] = m
    m = json.loads(json.dumps(t)); del m["clauses"][0]["claims"][0]["args"]["m"]["args"]["l"]; neg["a hole left out"] = m
    m = json.loads(json.dumps(t)); m["clauses"][0]["subject"]["narrowing"] = "sometimes"; neg["a narrowing the book does not have"] = m
    m = json.loads(json.dumps(t)); m["clauses"][0]["claims"][0]["text"] = "and also something else"; neg["prose in a field"] = m
    m = json.loads(json.dumps(t)); m["clauses"][0]["subject"]["operations"] = ["w.deposit"]; neg["a domain word of another system's operation"] = m
    for what, m in neg.items():
        e = ctree.validate(m, sch)
        refused_too = False
        try:
            ctree.sentence(m, voc, comp)
        except (ctree.TreeError, KeyError, TypeError):
            refused_too = True
        check(f"schema: {what} is rejected by the schema, and `ctree.sentence` does not write it", bool(e) and refused_too, str(e)[:200])
    m = json.loads(json.dumps(t)); m["clauses"][0]["claims"] = [{"piece": "always_answers", "args": {}}]
    try:
        ctree.sentence(m, voc, comp)
        check("tree: a tree whose sentence the compiler refuses (a narrowed claim that says nothing) is refused", False, "it was written")
    except ctree.TreeError as e:
        check("tree: a tree whose sentence the compiler refuses (a narrowed claim that says nothing) is refused, with the compiler's message",
              "SAYS NOTHING" in str(e) and not ctree.validate(m, sch), str(e)[:200])

    # ---------------------------------------------------------------- seeded drop
    seeded = reported = by_span = skipped = 0
    hidden, kinds = [], Counter()
    for i, src, text, hint, rd in gold:
        for what, m in drops(ctree.of_reading(rd)):
            try:
                got = ctree.sentence(m, voc, comp)
            except ctree.TreeError:
                skipped += 1
                continue
            seeded += 1
            kinds[what.split("`")[0].strip() or what] += 1
            cov = c2.coverage(voc, text, got["reading"])
            gone = Counter(c2.stems(text)) - Counter(c2.stems(got["sentence"]))
            named = any(c2.v1.stem(w) in gone for w in cov["dropped"]) or bool(cov["condition_dropped"])
            ok = not cov["full"] and named
            reported += ok
            by_span += bool(cov["condition_dropped"])
            if not ok:
                hidden.append((text, what, got["sentence"], cov["dropped"], cov["condition_dropped"]))
    numbers["seeded_drop"] = {"seeded": seeded, "reported": reported, "of_which_flagged_CONDITION_DROPPED": by_span,
                              "not_constructible": skipped, "hidden": hidden}
    check(f"seeded drop: {reported} of {seeded} deleted conditions and narrowings are reported ({by_span} also as CONDITION DROPPED; "
          f"{skipped} deletions give a sentence the compiler refuses and are not counted)", seeded > 20 and reported == seeded, str(hidden[:2]))

    # ---------------------------------------------------------------- no silent drop; partition
    cases = json.loads((HERE / "cases.json").read_text())
    outcomes, silent, part = Counter(), [], True
    for c in cases:
        r = c2.compose(c["rough"], c.get("domain"), l3=False)
        outcomes[r["outcome"] + (f" ({r['ask']})" if r["ask"] else "")] += 1
        for x in r["candidates"]:
            part = part and all(w["status"] in ("STOP", "MAPPED", "DEFAULT", "DROPPED") for w in x["coverage"]["words"]) \
                and [w["word"] for w in x["coverage"]["words"]] == [w for w, _ in c2.lex(c["rough"])]
        if r["outcome"] == "ANSWER" and not r["answer"]["coverage"]["full"]:
            silent.append(c["rough"])
        check(f"repeat: {c['rough'][:50]}", json.dumps(r, sort_keys=True, default=str) == json.dumps(c2.compose(c["rough"], c.get("domain"), l3=False), sort_keys=True, default=str))
    numbers["version_1_cases"] = dict(outcomes)
    check(f"no silent drop: no ANSWER on the thirteen sentences of cases.json has a dropped word, an added piece or a dropped condition ({dict(outcomes)})", not silent, str(silent))
    check("partition: every word of every rough sentence has exactly one status against every candidate shown", part)

    # ---------------------------------------------------------------- filters
    for s, d, want in [("A rejected transfer is always accepted", "ledger", "opposite-narrowing"),
                       ("An accepted transfer is always rejected", "ledger", "opposite-narrowing"),
                       ("An accepted transfer is rejected and changes nothing", "ledger", "opposite-narrowing"),
                       ("For a rejected transfer, it is accepted", "ledger", "opposite-narrowing"),
                       ("A deposit increases the wallet's balance by exactly zero", None, "by-zero"),
                       ("A transfer for which the sender of the transfer equals the sender of the transfer is always rejected", "ledger", "same-sides"),
                       ("A rejected transfer never changes the ledger", None, None),
                       ("An accepted transfer is accepted only if the amount of the transfer is at most the balance of account the sender of the transfer of the ledger", "ledger", None)]:
        rd = v1.compile_sentence(comp, s, d)
        got = "DOES NOT COMPILE" if isinstance(rd, Problem) else c2.filtered(voc, rd)
        check(f"filter: \"{s[:70]}\" -> {want}", got == want or (want is None and got in (None, "DOES NOT COMPILE")), str(got))
    r = c2.compose("a transfer that is refused is accepted", "ledger", l3=False)
    check("filter: no candidate shown is a narrowed subject with the opposite claim", r["counts"]["filtered"]["opposite-narrowing"] > 0
          and not any(c2.filtered(voc, v1.compile_sentence(comp, c["sentence"], "ledger")) for c in r["candidates"]), str(r["counts"]))

    # ---------------------------------------------------------------- the system question, decline
    r = c2.compose("a transfer always goes through", None, l3=False)
    check("system: a bare \"transfer\" with no word of one system gets ASK (system) before anything is generated",
          r["outcome"] == "ASK" and r["ask"] == "system" and r["systems"] == ["ledger", "wallet"] and not r["counts"], r["why"])
    r = c2.compose("a transfer always goes through", "ledger", l3=False)
    check("system: with --domain the question is not asked", not (r["outcome"] == "ASK" and r["ask"] == "system") and r["system"] == "ledger")
    r = c2.compose("a transfer never changes the ledger's balances", None, l3=False)
    check("system: a word only one system has (\"ledger\") settles it", r["system"] == "ledger" and "ledger" in r["system_by"], str(r["system_by"]))
    r = c2.compose("A transfer is always accepted", None, l3=False)
    check("system: a sentence of the book that two systems read gets ASK (system), not an answer", r["outcome"] == "ASK" and r["ask"] == "system")
    r = c2.compose("the answer never depends on anything", None, l3=False)
    check("decline: a sentence that names no operation is DECLINED (version 1 answered \"A bump always answers\")",
          r["outcome"] == "DECLINE" and not r["candidates"] and bool(r["decline"]["unmapped"]), r["why"])
    r = c2.compose("a batch is handled gracefully", None, l3=False)
    check("decline: when every candidate claims something no word asks for, DECLINE with the words nothing accounts for",
          r["outcome"] == "DECLINE" and "gracefully" in r["decline"]["unmapped"], f"{r['outcome']} {r['ask']} {[c['sentence'] for c in r['candidates']]}")

    # ---------------------------------------------------------------- condition spans
    rd = v1.compile_sentence(comp, "A transfer never changes the ledger", None)
    cov = c2.coverage(voc, "a transfer never changes the ledger when it is rejected", rd)
    check("span: a condition the candidate has no piece for is printed as CONDITION DROPPED", cov["condition_dropped"] == ["when it rejected"] and not cov["full"], str(cov["condition_dropped"]))
    rd = v1.compile_sentence(comp, "A rejected transfer never changes the ledger", None)
    cov = c2.coverage(voc, "a transfer never changes the ledger when it is rejected", rd)
    check("span: the same span against a candidate with the narrowing is matched", not cov["condition_dropped"], str(cov))

    rd = v1.compile_sentence(comp, "A lookup is always accepted and always answers", None)
    cov = c2.coverage(voc, "An accepted lookup always answers", rd)
    check("span: a narrowing word before the noun that the candidate turns into a claim is CONDITION DROPPED", cov["condition_dropped"] == ["accepted"], str(cov["condition_dropped"]))

    # ---------------------------------------------------------------- acknowledgement and --write
    rough = "a deposit adds exactly the amount to the wallet balance"
    r = c2.compose(rough, None, l3=False)
    check("ask: a sentence with a word nothing accounts for is ASK (dropped), with the word listed", r["outcome"] == "ASK" and r["ask"] == "dropped"
          and r["candidates"][0]["coverage"]["dropped"] == ["to"], str([c["coverage"]["dropped"] for c in r["candidates"]]))
    with tempfile.TemporaryDirectory() as tmp:
        f = str(Path(tmp) / "new.feature")
        rc = c2.main([rough, "--no-l3", "--write", f, "--json"])
        check("write: an ASK (dropped) writes nothing without an acknowledgement", rc == 1 and not Path(f).exists())
        rc = c2.main([rough, "--no-l3", "--acknowledge", "1", "--write", f, "--json"])
        check("write: an acknowledgement needs a name", rc == 1 and not Path(f).exists())
        import contextlib, io
        with contextlib.redirect_stdout(io.StringIO()):
            rc = c2.main([rough, "--no-l3", "--acknowledge", "1", "--by", "tester", "--write", f, "--json"])
        side = json.loads(Path(f + ".compose.json").read_text()) if Path(f + ".compose.json").exists() else {"rules": {}}
        rec = next(iter(side["rules"].values()), {})
        check("write: with --acknowledge K --by NAME the sentence is written and the record lists the dropped word and who accepted it",
              rc == 4 and "Rule: A deposit increases the wallet's balance by exactly the amount" in Path(f).read_text()
              and (rec.get("acknowledgement") or {}).get("dropped_words") == ["to"] and rec.get("chosen_by") == "human:tester"
              and rec.get("proposed_by", {}).get("kind") == "rule-based", str(rec)[:300])
        with contextlib.redirect_stdout(io.StringIO()):
            rc = c2.main(["A rejected transfer never changes the ledger", "--no-l3", "--write", f, "--json"])
        side = json.loads(Path(f + ".compose.json").read_text())
        check("write: an ANSWER is written with a record and no acknowledgement", rc == 0 and len(side["rules"]) == 2
              and any(x["acknowledgement"] is None and x["checks"]["coverage"]["full"] for x in side["rules"].values()))
    if "--l3" in sys.argv:
        s = "A computation of the total is accepted exactly when the total of the ledger's balances is at most the maximum"
        r = c2.compose(s, None, l3=True, identity=False)
        qs = r["questions"] or []
        check("l3: two full-coverage candidates that differ (the arguments of a comparison swapped) give ASK (reading) with a separating input",
              r["outcome"] == "ASK" and r["ask"] == "reading" and any(q["verdict"] == "SEPARATED" and q["question"] for q in qs),
              f"{r['outcome']} {r['ask']} {[q['verdict'] for q in qs]}")
        text = c2.render(r)
        check("l3: the question is printed with the input and what the compiled Rust did", "QUESTION:" in text and "HOLDS here" in text, text[-400:])
    check("no model: version 2 calls no language model", c2.compose("a deposit", None, l3=False)["language_model"] == "none")
    if "--json" in sys.argv:
        print(json.dumps(numbers, indent=1, ensure_ascii=False))
    print(f"{'FAILED: ' + str(len(fails)) if fails else 'all passed'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
