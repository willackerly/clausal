#!/usr/bin/env python3
"""Tests of `clausal compose` (plan node L1, first version). Run from clausal/:

    python3 compose_tests/run.py            no Lean, no cargo: about 5 s
    python3 compose_tests/run.py --l3       also one question through `clausal separate` (needs lean/ built and cargo)
    python3 compose_tests/run.py --record   rewrite the `top` of every case in cases.json from the current output

What is checked:
  tokens      the tokeniser and the stemmer on fixed words
  guarantee   every candidate of every case (--top 10) is written to a feature file under build/ and compiled by
              `clausal compile`'s own entry point (newrules.compile_files): each must compile, to the Lean text shown
  top         the top candidate of each case is the one recorded in cases.json (a REGRESSION snapshot, see README.md:
              these sentences were written by the implementer and the ranking was adjusted while looking at them)
  repeat      composing twice gives the same JSON
  scoping     no candidate carries successful / rejected / internal / "for which" unless the rough sentence has a cue
  write       --write appends a Rule line that compiles, and puts the file back when the sentence does not compile
  hook        the model hook returns nothing
None of the 48 trial sentences is used here.
"""
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from clausal import compose, newrules          # noqa: E402
from clausal.core import FeatureError, Problem  # noqa: E402
from clausal.pipeline import ROOT              # noqa: E402

fails = []


def check(name, ok, why=""):
    print(("ok    " if ok else "FAIL  ") + name + ("" if ok else f": {why}"))
    if not ok:
        fails.append(name)


def main():
    cases = json.loads((HERE / "cases.json").read_text())
    # tokens
    check("tokens: stems", [compose.stem(w) for w in ("balances", "changed", "changes", "succeeds", "successful", "withdrawals",
                                                     "applied", "exceeds", "transferred", "computation")]
          == ["balanc", "chang", "chang", "succeed", "succeed", "withdraw", "apply", "exceed", "transfer", "comput"])
    check("tokens: stop words and order", compose.tokens("The total of the balances is never changed") == ["total", "balanc", "never", "chang"])
    # guarantee, top, repeat, scoping
    all_c, got = [], {}
    for c in cases:
        r = compose.compose(c["rough"], c.get("domain"), 10)
        got[c["rough"]] = r
        check(f"repeat: {c['rough'][:50]}", json.dumps(r, sort_keys=True) == json.dumps(compose.compose(c["rough"], c.get("domain"), 10), sort_keys=True))
        top = r["candidates"][0]["sentence"] if r["candidates"] else None
        if "--record" in sys.argv:
            c["top"] = top
        check(f"top: {c['rough'][:50]}", top == c["top"], f"got {top!r}")
        R = set(r["tokens"])
        for x in r["candidates"]:
            if c.get("domain") is None:
                all_c.append(x)
            for m in ("successful", "rejected", "internal", "given", "and_then"):
                if m in x["pieces"] and not compose.CUE_BAGS[m] & R:
                    check(f"scoping: {x['sentence'][:60]}", False, f"`{m}` without a cue")
    check("scoping: no narrowing piece without a cue word", not [f for f in fails if f.startswith("scoping")])
    if "--record" in sys.argv:
        (HERE / "cases.json").write_text(json.dumps(cases, indent=1, ensure_ascii=False) + "\n")
    d = ROOT / "build" / "compose_tests"
    d.mkdir(parents=True, exist_ok=True)
    f = d / "candidates.feature"
    uniq = list({x["sentence"]: x for x in all_c}.values())
    f.write_text("Feature: compose candidates\n\n" + "".join(f"  @id:c{n}\n  Rule: {x['sentence']}\n\n" for n, x in enumerate(uniq)))
    _, items = newrules.compile_files([str(f)])
    bad = [(x["sentence"], getattr(i["result"], "message", "another reading")) for x, i in zip(uniq, items)
           if isinstance(i["result"], Problem) or i["result"].lean_def().split(":=", 1)[1] != x["lean"].split(":=", 1)[1]]
    check(f"guarantee: {len(uniq)} candidates compile as written through `clausal compile`", len(uniq) > 30 and not bad, str(bad[:3]))
    # the assertion itself: a tampered result must be refused
    r = compose.compose(cases[0]["rough"], None, 2)
    r["candidates"][0]["sentence"] = "A transfer conserves everything"
    try:
        compose.checked(r)
        check("guarantee: `checked` refuses a sentence that does not compile", False, "it was let through")
    except AssertionError:
        check("guarantee: `checked` refuses a sentence that does not compile", True)
    # write
    with tempfile.TemporaryDirectory() as t:
        p = Path(t) / "new.feature"
        compose.write_feature(p, "A rejected transfer never changes the ledger", None)
        compose.write_feature(p, "A deposit increases the wallet's balance by exactly the amount", None)
        text = p.read_text()
        check("write: two Rule lines in a new file", text.count("  Rule: ") == 2 and text.startswith("Feature: new"))
        try:
            compose.write_feature(p, "A transfer conserves everything", None)
            check("write: a sentence that does not compile is not written", False, "it was written")
        except FeatureError:
            check("write: a sentence that does not compile is not written", p.read_text() == text)
        rc = compose.main([cases[0]["rough"], "--write", str(Path(t) / "x.feature"), "--no-ask"])
        check("write: nothing is written without a choice", rc == 2 and not (Path(t) / "x.feature").exists())
    check("hook: no model is called", compose.model_hook("x", None, []) == ([], None))
    # a sentence refused only because it reads in two systems is shown, with the question, also when candidates exist
    r = compose.compose("a transfer always goes through", None, 3)
    amb = r["refused"]["ambiguous_as_written"]
    text = compose.render(r, None)
    check("two systems: the refused sentence is recorded with its systems and where it ranked",
          bool(r["candidates"]) and any(x["sentence"] == "A transfer is always accepted" and x["systems"] == ["ledger", "wallet"]
                                        and x["ahead_of_rank"] == 1 for x in amb), str(amb)[:300])
    check("two systems: printed with candidates present, with the --domain question",
          "NOT OFFERED" in text and "  - A transfer is always accepted " in text and "QUESTION: which system is your rule about (ledger or wallet)?" in text
          and "--domain" in text, text[-600:])
    check("two systems: the list of sentences in the JSON is unchanged", r["refused"]["reads_in_two_systems"] == [x["sentence"] for x in amb])
    rd = compose.compose("a transfer always goes through", "ledger", 3)
    check("two systems: with --domain the sentence is offered and nothing is listed as not offered",
          rd["candidates"][0]["sentence"] == "A transfer is always accepted" and not rd["refused"]["ambiguous_as_written"]
          and "NOT OFFERED" not in compose.render(rd, None))
    check("two systems: nothing printed when no sentence was refused for it",
          "NOT OFFERED" not in compose.render(compose.compose("a deposit increases the wallet's balance by exactly the amount", None, 3), None))
    if "--l3" in sys.argv:
        r = compose.compose("if a transfer is rejected the ledger stays the same", None, 3)
        qs = compose.questions(r, 2)
        check("l3: the top two candidates of the rejected-transfer case are SEPARATED, with a question",
              len(qs) == 1 and qs[0]["verdict"] == "SEPARATED" and bool(qs[0]["question"]), str(qs)[:300])
        # two separating inputs that point opposite ways: each must be asked about by number, with its own direction
        r = compose.compose("a withdrawal that is refused leaves the wallet as it was", None, 3)
        qs = compose.questions(r, 3)
        opp = [q for q in qs if q["verdict"] == "SEPARATED" and len({(i["holds"], i["fails"]) for i in q["inputs"]}) > 1]
        check("l3: a pair with two separating inputs pointing opposite ways exists in the refused-withdrawal case", bool(opp), str(qs)[:300])
        for q in opp:
            want = [f"On input {i['n']} ({i['values']}): should your rule hold there (then you do not mean candidate {i['fails']}) "
                    f"or fail there (then you do not mean candidate {i['holds']})?" for i in q["inputs"]]
            check(f"l3: candidates {q['a']} and {q['b']}: one question per input, each naming its input and its own direction",
                  all(w in q["question"] for w in want) and "the input above" not in q["question"]
                  and all(f"input {i['n']}: {i['values']}" in q["detail"] for i in q["inputs"]), q["question"])
        for q in qs:
            if q["verdict"] == "SEPARATED":
                check(f"l3: candidates {q['a']} and {q['b']}: every HOLDS/FAILS line agrees with the question's direction for that input",
                      all(f"  candidate {i['holds']} HOLDS here; candidate {i['fails']} FAILS here" in q["detail"] for i in q["inputs"])
                      and (len(q["inputs"]) > 1 or f"do not mean candidate {q['inputs'][0]['fails']}) or fail" in q["question"]), q["question"])
    print(f"{'FAILED: ' + str(len(fails)) if fails else 'all passed'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
