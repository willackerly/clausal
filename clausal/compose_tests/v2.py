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

    # ---------------------------------------------------------------- the side of a condition; one negation word, one negation (fix round)
    inverted = "For a rejected transfer for which the amount of the transfer differs from zero, the amount of the transfer has moved between its accounts in the ledger and no other balance changed"
    right = "A rejected transfer for which the amount of the transfer equals zero never changes the ledger"
    for rough in ("A rejected transfer never changes the ledger when the amount is zero", "A rejected transfer never changes the ledger if the amount is zero"):
        cov = c2.coverage(voc, rough, v1.compile_sentence(comp, inverted, "ledger"))
        check(f"side: \"never\" written outside the condition is not mapped to the negated piece inside it ({rough[-22:]})",
              "never" in cov["dropped"] and not cov["full"] and {"word": "never", "piece": "equals (negated)"} in cov["refused_mappings"], str(cov["dropped"]))
        cov = c2.coverage(voc, rough, v1.compile_sentence(comp, right, "ledger"))
        check("side: the reading with the condition as written drops no word (its `equals` is ADDED: \"is\" is on the stop list)",
              not cov["dropped"] and not cov["condition_dropped"] and cov["added"] == ["equals"], str(cov["dropped"]) + str(cov["added"]))
    for rough in ("A rejected transfer never changes the ledger when the amount is zero", "A rejected transfer never changes the ledger if the amount is zero",
                  "An accepted transfer never changes the ledger when the amount is zero"):
        r = c2.compose(rough, None, l3=False)
        neg_in_cond = [c["sentence"] for c in r["candidates"] if "differs from" in c["sentence"] and c["coverage"]["full"]]
        check(f"side: \"{rough}\" is not answered and no full candidate inverts its condition (ASK (dropped), the condition as written first)",
              r["outcome"] == "ASK" and r["ask"] == "dropped" and not neg_in_cond and " equals zero never changes the ledger" in r["candidates"][0]["sentence"],
              f"{r['outcome']} {r['ask']} {[c['sentence'] for c in r['candidates']]}")
    cov = c2.coverage(voc, "A lookup does not give a result when the account is in the ledger",
                      v1.compile_sentence(comp, "For a lookup for which the account is not an account of the ledger, the result is the balance of the account in the ledger", "ledger"))
    check("side: a form word (\"not\") written outside the condition is not mapped to the negated piece inside it either", "not" in cov["dropped"], str(cov["dropped"]))
    cov = c2.coverage(voc, "A transfer that is rejected never changes the ledger when the amount is not zero",
                      v1.compile_sentence(comp, "A rejected transfer for which the amount of the transfer differs from zero never changes the ledger", "ledger"))
    check("side: a negation written in the condition is mapped to the negated piece of that condition (full coverage)", cov["full"], str(cov["dropped"]) + str(cov["added"]))
    cov = c2.coverage(voc, "A transfer that is rejected never changes the ledger when the amount is zero",
                      v1.compile_sentence(comp, "For a rejected transfer for which the amount of the transfer differs from zero, the amount of the transfer has moved between its accounts in the ledger and no other balance changed", "ledger"))
    check("side: a word of one condition span is not mapped into the other condition (\"never\" after \"that is rejected\")",
          "never" in cov["dropped"] and not cov["full"], str(cov["dropped"]))
    rough = "A lookup of an account that is not in the ledger gives no result"
    cov = c2.coverage(voc, rough, v1.compile_sentence(comp, "For a lookup for which the account is not an account of the ledger, the result is the balance of the account in the ledger", "ledger"))
    check("negation: \"no\" of \"gives no result\" is DROPPED by a candidate whose one negation already has the author's \"not\"",
          "no" in cov["dropped"] and not cov["full"], str(cov["dropped"]))      # (L1ab: dropped == ["gives", "no"]; with L1c "gives" is a cue of "the result is")
    cov = c2.coverage(voc, rough, v1.compile_sentence(comp, "For a lookup for which the account is not an account of the ledger, there is no result", "ledger"))
    check("negation: the candidate that says \"no result\" has both negation words mapped", "no" not in cov["dropped"] and "not" not in cov["dropped"], str(cov["dropped"]))

    # ---------------------------------------------------------------- the operation question (fix round)
    # (L1c: "take out" and "asking for" now anchor the withdrawal and the lookup as synonyms of their nouns, so the two sentences
    # of the fix round are no longer asked the operation question; these two say the operation with a verb that is no synonym.)
    for rough, op, noun in (("You can't remove more than the wallet holds", "w.withdraw", "withdrawal"),
                            ("Requesting the balance of an account that doesn't exist yields no number", "l.lookup", "lookup")):
        r = c2.compose(rough, None, l3=False)
        check(f"operation: no operation named, a word of a system written: ASK (operation) listing {op}, nothing generated ({rough[:30]})",
              r["outcome"] == "ASK" and r["ask"] == "operation" and op in [x["id"] for x in r["operation_question"]["operations"]] and not r["counts"] and not r["candidates"], r["why"])
        r2 = c2.compose(rough, None, l3=False, operation=op)
        check(f"operation: with --operation {op} that operation alone is tried, it is not an ADDED piece, and nothing is answered with a dropped word",
              r2["operations_anchored"] == [op] and r2["anchored_by"] == "--operation" and not (r2["outcome"] == "DECLINE" and r2["why"].startswith("no operation"))
              and all(op not in c["coverage"]["added"] and c["operations"] == [[op]] for c in r2["candidates"])
              and not (r2["outcome"] == "ANSWER" and not r2["answer"]["coverage"]["full"]), f"{r2['outcome']} {r2['ask']} {r2['why'][:80]}")
        check("operation: a noun names it too", c2.compose(rough, None, l3=False, operation=noun)["operations_anchored"] == [op])
    import contextlib as _c, io as _io
    with _c.redirect_stderr(_io.StringIO()) as err:
        rc = c2.main(["You can't remove more than the wallet holds", "--no-l3", "--operation", "transfer"])
    check("operation: a noun of two systems is refused with the ids to choose from", rc == 1 and "w.transfer" in err.getvalue() and "l.apply" in err.getvalue())

    # ---------------------------------------------------------------- acknowledgement and --write
    # (L1c changed this case: "a deposit adds exactly the amount to the wallet balance" dropped "to" and is now answered, so the
    # acknowledgement is tested on a sentence with a word of no book.)
    rough = "a deposit adds exactly the amount to the shiny wallet balance"
    r = c2.compose(rough, None, l3=False)
    check("ask: a sentence with a word nothing accounts for is ASK (dropped), with the word listed", r["outcome"] == "ASK" and r["ask"] == "dropped"
          and r["candidates"][0]["coverage"]["dropped"] == ["shiny"], str([c["coverage"]["dropped"] for c in r["candidates"]]))
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
              and (rec.get("acknowledgement") or {}).get("dropped_words") == ["shiny"] and rec.get("chosen_by") == "human:tester"
              and rec.get("proposed_by", {}).get("kind") == "rule-based", str(rec)[:300])
        with contextlib.redirect_stdout(io.StringIO()):
            rc = c2.main(["A rejected transfer never changes the ledger", "--no-l3", "--write", f, "--json"])
        side = json.loads(Path(f + ".compose.json").read_text())
        check("write: an ANSWER is written with a record and no acknowledgement", rc == 0 and len(side["rules"]) == 2
              and any(x["acknowledgement"] is None and x["checks"]["coverage"]["full"] for x in side["rules"].values()))
    if "--l3" in sys.argv:
        # (L1c: the L1ab case here was a comparison with its arguments swapped; that candidate is no longer full. The pair now
        # is 'whenever' against 'exactly when' for an author's "when".)
        s = "A transfer goes through when the amount is no more than the sender's balance"
        r = c2.compose(s, "wallet", l3=True)
        qs = r["questions"] or []
        check("l3: two full-coverage candidates that differ ('whenever' and 'exactly when' for the author's 'when') give ASK (reading) with a separating input",
              r["outcome"] == "ASK" and r["ask"] == "reading" and any(q["verdict"] == "SEPARATED" and q["question"] for q in qs),
              f"{r['outcome']} {r['ask']} {[q['verdict'] for q in qs]}")
        text = c2.render(r)
        check("l3: the question is printed with the input and what the compiled Rust did", "QUESTION:" in text and "HOLDS here" in text, text[-400:])
    # ---------------------------------------------------------------- L1c (plan node): REGRESSION SNAPSHOTS by the builder.
    # Three of the rough sentences are sentences of the development set (d05, d32, d10); the rest are the builder's own.
    def cov(rough, sent, dom=None):
        return c2.coverage(voc, rough, v1.compile_sentence(comp, sent, dom))

    def answer(r):
        return r["answer"]["sentence"] if r["outcome"] == "ANSWER" else None

    r = c2.compose("A withdrawal that fails leaves the balance untouched", None, l3=False)
    vias = {w["word"]: w["via"] for w in (r["answer"] or {"coverage": {"words": []}})["coverage"]["words"]}
    check("L1c phrase cue: 'leaves ... untouched' is accounted for by 'never changes', and the answer is the narrowed sentence",
          answer(r) == "A rejected withdrawal never changes the wallet's balance" and vias.get("leaves") == "phrase" and vias.get("untouched") == "phrase", str(r["outcome"]))
    r = c2.compose("A deposit adds exactly the amount to the wallet balance", None, l3=False)
    vias = {w["word"]: w["via"] for w in (r["answer"] or {"coverage": {"words": []}})["coverage"]["words"]}
    check("L1c function words: 'to' is accounted for with the phrase or its object (L1ab: ASK (dropped), 'to' dropped)",
          answer(r) == "A deposit increases the wallet's balance by exactly the amount" and vias.get("to") in ("phrase", "attached"), f"{r['outcome']} {vias}")
    c = cov("A deposit adds exactly the amount to the purse balance", "A deposit increases the wallet's balance by exactly the amount")
    check("L1c function words: a preposition whose object is dropped is not accounted for by attachment ('purse' is no word of the book)", "purse" in c["dropped"] and not c["full"], str(c["dropped"]))
    two = "When a deposit goes through the balance rises by the amount deposited, and when it fails the balance stays put"
    want = "An accepted deposit increases the wallet's balance by exactly the amount, and a rejected deposit never changes the wallet's balance"
    r = c2.compose(two, None, l3=False)
    check("L1c clause by clause: a sentence of two clauses is ANSWERED with a sentence of two clauses the one-clause generator cannot write",
          answer(r) == want and r["answer"].get("clause_by_clause") is True, f"{r['outcome']} {r['ask']} {answer(r)}")
    c = cov(two, "A rejected deposit increases the wallet's balance by exactly the amount, and an accepted deposit never changes the wallet's balance")
    check("L1c clause by clause: with the narrowings of the two clauses swapped the candidate is not full (a word of one clause is not mapped into the other)",
          not c["full"] and c["condition_dropped"], str(c["dropped"]))
    multi = [(text, hint, rd) for i, src, text, hint, rd in gold if len(rd.info["clauses"]) > 1]
    reach2 = Counter()
    for text, hint, rd in multi:
        r = c2.compose(text, hint, l3=False, identity=False)
        got = [x for x in r["candidates"] if x["term_sha256"] == ctree.body_sha(rd)]
        reach2["ANSWER, the same term" if r["outcome"] == "ANSWER" and got else "ANSWER, ANOTHER TERM" if r["outcome"] == "ANSWER"
               else "asked, the fixture's own sentence among those shown" if got else "asked or declined, not shown"] += 1
    numbers["multi_clause_reach_without_the_identity_step"] = {"fixture_lines_of_two_or_more_clauses": len(multi), **dict(reach2)}
    print(f"info  L1c: the {len(multi)} fixture Rule lines of two or more clauses, identity step off: {dict(reach2)}")
    check("L1c clause by clause: no fixture line of several clauses is ANSWERED with another term", reach2["ANSWER, ANOTHER TERM"] == 0)
    rough = "A transfer goes through only if the amount is no more than the sender's balance"
    ok_, sw, st = (cov(rough, "A transfer is accepted only if " + k, "wallet") for k in
                   ("the amount is at most the sender's balance", "the sender's balance is at most the amount", "the amount is more than the sender's balance"))
    check("L1c argument order: 'the amount is no more than the balance' is full for 'the amount is at most the balance'", ok_["full"])
    check("L1c argument order: the same comparison with its two sides swapped is refused and not full", not sw["full"] and sw["order_refused"], str(sw["order_refused"]))
    check("L1c argument order: the strict comparison is refused for a non-strict one and not full", not st["full"] and st["order_refused"], str(st["order_refused"]))
    r = c2.compose(rough, "wallet", l3=False)
    check("L1c argument order: the sentence is ANSWERED with the arguments in the author's order", answer(r) == "A transfer is accepted only if the amount is at most the sender's balance", f"{r['outcome']} {r['ask']}")
    r = c2.compose(rough.replace("only if", "when"), "wallet", l3=False)
    check("L1c connective: 'when' is ASKED (whenever / exactly when / for which), 'only if' is not offered", r["outcome"] == "ASK" and r["ask"] == "reading"
          and not any("only if" in x["sentence"] for x in r["candidates"]), str([x["sentence"] for x in r["candidates"]]))
    c = cov("The ledger's total equals the sum of all account balances", "A computation of the total never changes the ledger", "ledger")
    check("L1c comparison words: 'equals' is not accounted for by a piece that does not compare ('never changes')", "equals" in c["dropped"] and not c["full"], str(c["dropped"]))
    c = cov("A batch never changes the total of the ledger's balances", "A batch never leaves the total of the ledger's balances above the maximum")
    check("L1c comparison words: a piece that compares is ADDED unless a comparison word of the author's asks for it", "at_most" in c["added"], str(c["added"]))
    r = c2.compose("A transfer from an account to itself is refused", "ledger", l3=False)
    fullc = [x for x in r["candidates"] if x["coverage"]["full"]]
    check("L1c cues of the last wave: 'to itself' reaches 'equals' (every full candidate has the condition 'the sender ... equals the receiver ...')",
          fullc and all("equals" in x["key"] for x in fullc) and r["outcome"] in ("ANSWER", "ASK"), f"{r['outcome']} {r['ask']} {[x['sentence'] for x in r['candidates']][:2]}")
    r = c2.compose("Depositing an amount and then withdrawing the same amount puts the wallet back where it started", None, l3=False)
    check("L1c cues of the last wave: a tied sequence ('then ... the same amount') is ANSWERED 'followed by ... with the same input'",
          answer(r) == "A deposit followed by a withdrawal with the same input never changes the wallet's balance", f"{r['outcome']} {r['ask']} {answer(r)}")
    r = c2.compose("After a transfer, no account holds more than the maximum", "ledger", l3=False)
    check("L1c cues of the last wave: 'no account holds more than' reaches 'each of ... is afterwards at most' (shown; not answered: 'after' and the balances are not accounted for)",
          r["outcome"] == "ASK" and any(x["sentence"] == "For a transfer, each of the ledger's balances is afterwards at most the maximum" for x in r["candidates"]),
          str([x["sentence"] for x in r["candidates"]]))
    check("L1c filter: a condition between two constants is filtered ('the maximum equals zero')",
          c2.filtered(voc, v1.compile_sentence(comp, "A transfer for which the maximum equals zero is always rejected", "ledger")) == "constants")
    r = c2.compose("Bumping the counter by zero is always accepted", None, l3=False)
    check("L1c: 'bumping the counter by zero' is not ANSWERED with a condition on the counter's count (the counter's project cannot say the amount)", r["outcome"] != "ANSWER", str(answer(r)))
    check("no model: version 2 calls no language model", c2.compose("a deposit", None, l3=False)["language_model"] == "none")
    if "--json" in sys.argv:
        print(json.dumps(numbers, indent=1, ensure_ascii=False))
    print(f"{'FAILED: ' + str(len(fails)) if fails else 'all passed'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
