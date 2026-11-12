"""Fast checks of the Rule parser, tag inheritance and the suite-adequacy bookkeeping. No Lean, no Rust, no out/.

    python3 -m clausal.selftest

The end-to-end controls (a real suite with its progress scenario removed, an ill-typed trivial model, a tag
taken off a Rule) are c16 to c20 in mutation/run_mutants.py; these are the same ideas at the level of the Python.
"""
from __future__ import annotations

import json
import re

import sys
import tempfile
from pathlib import Path

from . import adequacy, rules
from .core import FeatureError, parse_feature, without_scenarios

FEATURE = """\
@ftag
Feature: Probe
  Feature description.

  Background:
    Given Carol has a balance of 1

  Scenario: before any rule
    Given Alice has a balance of 1
    When Alice deposits 1
    Then the operation succeeds

  # a comment that belongs to the rule below
  @rtag @expect-refuted @id:first
  Rule: First claim
    Description line one.
    Description line two.

    Background:
      Given Bob has a balance of 2

    # comment above the scenario
    @id:outline
    Scenario Outline: an outline
      Given Alice has a balance of <a>
      When Alice deposits <a>
      Then the operation succeeds

      Examples:
        | a |
        | 1 |
        | 2 |

    @expect-vacuous
    Scenario: own tag wins
      Given Alice has a balance of 1
      When Alice deposits 1
      Then the operation succeeds

  Rule: Second claim
    Example: uses the Example keyword
      Given Alice has a balance of 1
      When Alice deposits 1
      Then the operation succeeds

  Rule: A rule with nothing under it
"""

FAILS = [
    ("a Rule with no text", "Feature: X\n  Rule:\n"),
    ("two Rules with the same id", "Feature: X\n  Rule: Same\n  Rule: Same\n"),
    ("a Background after a scenario of its Rule",
     "Feature: X\n  Rule: R\n    Scenario: s\n      Given a\n      When b\n      Then c\n    Background:\n      Given d\n"),
    ("a Rule before the Feature", "Rule: R\nFeature: X\n"),
]


def parse(text: str):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "probe.feature"
        p.write_text(text)
        return parse_feature(p, "probe.feature"), p


class FakeTriv:
    def __init__(self, kind, key):
        self.kind, self.key, self.label, self.call, self.lean_name = kind, key, f"{kind} {key}", "op", f"Trivial.op.{key}"


class FakeBound:
    def __init__(self, id_):
        self.id = id_


def main() -> int:
    bad = []

    def check(what, ok):
        print(f"  {'ok  ' if ok else 'FAIL'} {what}")
        if not ok:
            bad.append(what)

    f, _ = parse(FEATURE)
    r1, r2, r3 = f.rules
    loose, o, own, ex = f.scenarios
    check("three Rules, four scenarios, one of them before any Rule",
          len(f.rules) == 3 and len(f.scenarios) == 4 and loose.rule is None and [len(r.scenarios) for r in f.rules] == [2, 1, 0])
    check("the rule line and its description are carried verbatim",
          r1.name == "First claim" and r1.description == ["Description line one.", "Description line two."]
          and r1.text == "Rule: First claim\nDescription line one.\nDescription line two.")
    check("@id: on a Rule names the Rule and is not inherited by its scenarios",
          r1.id == "Rule.probe.first" and o.id == "Spec.probe.outline" and r2.id == "Rule.probe.second_claim")
    check("Feature and Rule tags apply to the scenarios beneath, own tags last",
          o.all_tags == ["@ftag", "@rtag", "@expect-refuted", "@id:outline"] and loose.all_tags == ["@ftag"] and ex.all_tags == ["@ftag"])
    check("@expect-* is inherited from the Rule; the scenario's own tag wins",
          o.expect == "REFUTED" and own.expect == "VACUOUS" and loose.expect is None and ex.expect is None)
    check("Backgrounds: the Feature's, then the Rule's",
          [s.text for s in o.background] == ["Carol has a balance of 1", "Bob has a balance of 2"]
          and [s.text for s in ex.background] == ["Carol has a balance of 1"])
    check("a scenario's text stops before the next Rule and its tags and comments",
          o.text.splitlines()[0] == "Scenario Outline: an outline" and o.text.splitlines()[-1].strip() == "| 2 |"
          and loose.text.splitlines()[-1].strip() == "Then the operation succeeds")
    check("the Example keyword is a scenario; Examples rows are read under a Rule", ex.name == "uses the Example keyword" and len(o.rows) == 2)
    check("suites(): the loose scenarios first, then each Rule",
          [(r.name if r else None, len(s)) for r, s in f.suites()] == [(None, 1), ("First claim", 2), ("Second claim", 1), ("A rule with nothing under it", 0)])
    for what, text in FAILS:
        try:
            parse(text)
            check(f"rejected: {what}", False)
        except FeatureError:
            check(f"rejected: {what}", True)
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "probe.feature"
        p.write_text(FEATURE)
        t = without_scenarios(p, "probe.feature", ("outline",))
        p.write_text(t)
        g = parse_feature(p, "probe.feature")
    check("removing a scenario by id takes its tags and comments with it and keeps the Rule",
          "@id:outline" not in t and "comment above the scenario" not in t and "Rule: First claim" in t
          and [len(r.scenarios) for r in g.rules] == [1, 1, 0] and len(g.scenarios) == 3)

    # ---- the note's bookkeeping, on made-up results: scenarios `safety` and `progress` of one operation
    ts = [FakeTriv("reject-all", "rej"), FakeTriv("no-op", "noop"), FakeTriv("constant", "c1"), FakeTriv("constant", "c2")]
    real_pair_name = adequacy.pair_name
    adequacy.pair_name = lambda b, t: f"{b.id}/{t.key}"
    try:
        def res(r):
            return {"result": r}
        decided = {"safety/rej": res("holds"), "safety/noop": res("holds"), "safety/c1": res("ruled-out"), "safety/c2": res("not-ruled-out"),
                   "progress/rej": res("ruled-out"), "progress/noop": res("not-ruled-out"), "progress/c1": res("ruled-out"),
                   "progress/c2": res("ruled-out"), "example/noop": res("ruled-out")}
        safety, progress, example = FakeBound("safety"), FakeBound("progress"), FakeBound("example")
        full = adequacy._assess([safety, progress], [], ts, decided)
        check("a suite with its progress scenario rules out reject-all",
              adequacy._kinds(full)[0] == ["reject-all", "constant"] and "reject-all" not in adequacy.line(full).split("still allows")[1])
        alone = adequacy._assess([safety], [], ts, decided)
        check("THE CONTROL: the same suite with its progress scenario removed is reported as allowing reject-all",
              "reject-all" in adequacy.line(alone).split("still allows")[1] and "reject-all" not in adequacy._kinds(alone)[0])
        check("'proved to satisfy' is said only when every scenario counted is proved to hold of it",
              [r["holds_proved"] for r in alone] == [True, True, False, False]
              and "proved to satisfy every scenario counted" in adequacy.line(alone)
              and [r["holds_proved"] for r in full] == [False, False, False, False])
        check("a kind is ruled out only when every variant of it is (constant: one of two left)",
              "constant (1 of 2 variants)" in adequacy.line(alone))
        ex_only = adequacy._assess([safety, progress], [example], ts, decided)
        check("a literal example that rules a model out is recorded separately and does not count as ruling it out",
              ex_only[1]["state"] == "allowed" and ex_only[1]["by_examples"] == ["example"])
        check("a pair the search never reported is listed as not run, not as allowed-and-proved",
              adequacy._assess([FakeBound("missing")], [], ts[:1], decided)[0]["not_run"] == ["missing"]
              and not adequacy._assess([FakeBound("missing")], [], ts[:1], decided)[0]["holds_proved"])
        check("no scenario counted: nothing is ruled out, and nothing is 'proved'",
              all(r["state"] == "allowed" and not r["holds_proved"] for r in adequacy._assess([], [], ts, decided)))
    finally:
        adequacy.pair_name = real_pair_name

    # ---- a Rule with no scenario is shown, and says that nothing was stated
    dg = {"alg": "sha256-text", "value": "x"}
    g = {"runs": [], "verdicts": [], "edges": [],
         "nodes": [{"id": "group:rule:Rule.x.empty", "kind": "group", "attrs": {"level": "rule", "tags": []},
                    "interface": {"text": "Rule: Empty\nwords", "identity": dg, "source": {"file": "x.feature", "line_start": 2}},
                    "implementations": []}]}
    bl = rules.blocks(g)
    check("a Rule with no scenario gets a block that says nothing was stated",
          len(bl) == 1 and bl[0]["verdict"]["head"].startswith("NOTHING STATED") and any("NOTHING STATED" in l for l in rules.render(bl[0])))
    # ---- the composable Clausebook refuses, it never guesses (added after the review of the frame library: no control
    #      or check exercised AMBIGUOUS before)
    from . import vocab
    from .core import load_glossary
    from .pipeline import ROOT
    gl = load_glossary(ROOT / "glossary.yaml", "glossary.yaml")
    comp = vocab.Compiler(vocab.load_project(ROOT, gl))
    vf, _ = parse("Feature: Refusals\n\n  Rule: A batch never leaves the ledger below zero\n\n  Rule: A withdrawal never alters the wallet's balance\n\n"
                  "  Rule: A transfer always answers\n\n  Rule: A withdrawal is accepted whenever the amount is at most the wallet's balance\n")
    got = [comp.rule(r, None) for r in vf.rules]
    check("a rule line is refused, never guessed: ILL-TYPED, UNBOUND, AMBIGUOUS (two domains, no scenario beneath)",
          [getattr(g, "status", "COMPILED") for g in got[:3]] == ["ILL-TYPED", "UNBOUND", "AMBIGUOUS"])
    check("the echo of 'is accepted whenever' says the call answers whether or not the condition holds, and names D8",
          isinstance(got[3], vocab.Reading) and "whether or not" in " ".join(t for _, t in got[3].echo) and "D8" in got[3].defaults
          and any(slot == "accepted" for slot, _ in got[3].echo))
    # ---- plan node Q1: a narrowed Rule clause that holds of EVERY operation is refused, with the reason
    #      (readability critique 2.1; the kernel side of the same controls is lean/Run/Narrowing.lean, read by `clausal narrowing`)
    from . import narrowing, vreport
    voc = comp.voc
    loose_comp = vocab.Compiler(voc, refuse_vacuous=False)

    def rules_of(lines):
        f, _ = parse("Feature: Narrowing\n\n" + "".join(f"  Rule: {x}\n\n" for x in lines))
        return f.rules
    four = ["An accepted transfer never loses acceptance when the amount is the same or larger",
            "An accepted transfer gives the same answer when the amount is the same or larger",
            "A rejected transfer gives the same answer when only the amount differs",
            "An accepted transfer never loses that it is rejected when the amount is the same or smaller"]
    got = [comp.rule(r, None) for r in rules_of(four)]
    check("THE CONTROL (Q1): the four sentences of the critique are refused as SAYS-NOTHING (this fails if the refusal is removed)",
          [getattr(g, "status", "COMPILED") for g in got] == ["SAYS-NOTHING"] * 4)
    check("the refusal names the reason: vacuous by narrowing, which calls, and the theorem that proves it",
          all(isinstance(g, vocab.Problem) and "vacuous by narrowing" in g.message and f"Frames.Narrowed.{t}, lean/Frames/Narrowing.lean" in g.message
              and f"about {k} calls only" in g.message
              for g, t, k in zip(got, ["monotone_holds", "independentOf", "independentOf", "monotone_fails"],
                                 ["accepted", "accepted", "rejected", "accepted"])))
    off = [loose_comp.rule(r, None) for r in rules_of(four)]
    check("the same four compile when the refusal is switched off (so it is the refusal that stops them), each with a claim stated for any `run`",
          all(isinstance(g, vocab.Reading) and all("with run := run" in c.any_run for c in g.claims) for g in off))
    ctl = parse_feature(ROOT / "controls" / "narrowing.feature", "controls/narrowing.feature").rules
    twice = [r for r in ctl if "@narrowed-twice" in r.tags]
    ctl = [r for r in ctl if r not in twice]
    want = {r.id: next((t.split(":", 1)[1] for t in r.tags if t.startswith("@says-nothing:")), None) for r in ctl}
    on = {r.id: comp.rule(r, None) for r in ctl}
    check(f"controls/narrowing.feature: the {sum(v is not None for v in want.values())} lines tagged @says-nothing are refused for the tagged reason, "
          f"the other {sum(v is None for v in want.values())} compile",
          all((isinstance(on[i], vocab.Problem) and on[i].status == "SAYS-NOTHING" and f"Frames.Narrowed.{w}," in on[i].message) if w
              else isinstance(on[i], vocab.Reading) for i, w in want.items())
          and sum(v is not None for v in want.values()) >= 12 and sum(v is None for v in want.values()) >= 5)
    check("every theorem the compiler can name is exercised by a control line",
          {t for rs in narrowing.REASONS.values() for _, t, _ in rs} | {"covers_no_call"} <= {w for w in want.values() if w})
    fixtures = [r for p in sorted((ROOT / "features").glob("*.feature")) for r in parse_feature(p, f"features/{p.name}").rules]
    a, b = [comp.rule(r, None) for r in fixtures], [loose_comp.rule(r, None) for r in fixtures]
    same = lambda x, y: (x.lean_def() == y.lean_def() and x.echo == y.echo) if isinstance(x, vocab.Reading) and isinstance(y, vocab.Reading) \
        else (getattr(x, "status", 0), getattr(x, "message", 0)) == (getattr(y, "status", 1), getattr(y, "message", 1))
    check(f"no fixture Rule line is refused: all {len(fixtures)} compile to the same statement and echo with the refusal on and off",
          all(same(x, y) for x, y in zip(a, b)) and not any(getattr(x, "status", "") == "SAYS-NOTHING" for x in a))

    # ---- plan node Q2: the printed coverage is the Calls value of each claim, not the words of the subject (critique 2.2)
    # (Since plan node Q4 a Rule line narrows on its subject only: the first shape, "for a lookup, if it is accepted, ...",
    #  is refused in a Rule line and these are the same two statements written the one way the book has. The shape is still
    #  read before a Then step; `f3` below is one.)
    shapes = ["For an accepted lookup, the result is the balance of the account in the ledger",
              "A rejected transfer never changes the ledger",
              "An accepted lookup gives the same answer when the ledger is extended"]
    sh = [comp.rule(r, None) for r in rules_of(shapes)]
    texts = lambda rd: [t for _, t in getattr(rd, "echo", [("", "(refused)")])]
    cov = voc.covers
    check("first faulty shape (a narrowed claim about one call; before Q4 written 'for X, if it is accepted / rejected, ...'): covers the narrowed calls only, no answer required, D1 and D2 not applied",
          all(isinstance(rd, vocab.Reading) for rd in sh)
          and [("covers", cov[k]["covers"]) in rd.echo for rd, k in zip(sh[:2], ("accepted", "rejected"))] == [True, True]
          and not any(cov["every"]["covers"] in " ".join(texts(rd)) or cov["every"]["answer"] in texts(rd) for rd in sh[:2])
          and not any(d in rd.defaults for rd in sh[:2] for d in ("D1", "D2"))
          and [rd.coverage for rd in sh[:2]] == [["accepted"], ["rejected"]])
    check("second faulty shape (a narrowed rule about two calls): it does not print that both calls must give an answer, and D10 is not applied",
          not any("both must give an answer" in t for t in texts(sh[2])) and "D10" not in sh[2].defaults
          and cov["accepted"]["two_calls"] in texts(sh[2]) and "BOTH are accepted" in cov["accepted"]["two_calls"])

    def side_of(rd):
        return {rd.id: {"kind": rd.kind, "printed": narrowing.printed(voc, rd.echo), "control": False,
                        "claims": [{"calls": c.calls, "clause": c.clause, "runs": c.runs} for c in rd.claims]}}

    def lean_says(rd, calls=None):          # what `#calls` would print, if Lean agreed with the compiler (or said `calls`)
        return {f"{rd.id}#{j}": calls or c.calls for j, c in enumerate(rd.claims)}

    def seq_says(rd):                       # what `#calls` would print about sequences, if Lean agreed with the compiler
        return {f"{rd.id}#{j}": len(rd.info["clauses"][c.clause]["ops"]) > 1 for j, c in enumerate(rd.claims)}
    readings = [x for x in a if isinstance(x, vocab.Reading)] + sh
    check(f"the coverage printed for each of the {len(readings)} compiled Rule lines (fixtures and the faulty shapes) is the coverage of its claims' Calls values",
          all(narrowing.coverage_mismatches(side_of(rd), lean_says(rd), seq_says(rd)) == [] for rd in readings))
    old = side_of(sh[0])
    old[sh[0].id]["printed"] = [["covers", ["every"]], ["answer"], ["weak", "accepted"]]       # what was printed before the fix
    check("THE CONTROL (Q2): the check reports the coverage that used to be printed for the first shape (this fails if the check is removed)",
          len(narrowing.coverage_mismatches(old, lean_says(sh[0]))) == 1)
    check("... and reports a claim whose emitted Lean carries another Calls value than the compiler took, and a claim Lean did not answer for",
          len(narrowing.coverage_mismatches(side_of(sh[0]), lean_says(sh[0], "every"))) == 2
          and len(narrowing.coverage_mismatches(side_of(sh[0]), {})) == 1)
    one_open = {"facts": [], "certs": [], "open": [{"claim": "Rule.x#0", "tactic": "T.open_0", "lean": "P", "source": "x:1", "fixture": True}],
                "calls": {}, "controls": []}
    report_ok = f"NARROWING\t{narrowing.BAD_STATEMENT}\tbadstatement\tsorryAx\nNARROWING\t{narrowing.ABSENT}\tmissing\t\n"
    res = narrowing.collect(one_open, report_ok + "NARROWING\tT.open_0\tproved\tpropext\n")
    check("a narrowed fixture claim the kernel proves for every `run` fails the run (the compiler should have refused it)",
          not res["ok"] and len(res["problems"]) == 1 and "SAYS NOTHING BUT WAS NOT REFUSED" in res["problems"][0])
    # ---- review of Q1/Q2, defect 1: a must-fail attempt counts only if its STATEMENT elaborated
    res_np = narrowing.collect(one_open, report_ok + "NARROWING\tT.open_0\tnotproved\tsorryAx\n")
    res_bs = narrowing.collect(one_open, report_ok + "NARROWING\tT.open_0\tbadstatement\tsorryAx\n")
    und = {"facts": [{"name": "T.fact_0", "op": "o", "kind": "accepted", "key": "holds", "cls": "c", "declared": False, "lean": "P"}],
           "certs": [], "open": [], "calls": {}, "controls": []}
    res_fs = narrowing.collect(und, report_ok + "NARROWING\tT.fact_0\tbadstatement\tsorryAx\n")
    check("THE CONTROL (statement state): a must-fail attempt passes when its script failed (`notproved`) and FAILS THE RUN when its statement "
          "did not elaborate (`badstatement`), for a narrowed claim and for an undeclared fact (this fails if the two states are merged again)",
          res_np["ok"] and not res_bs["ok"] and "NO ANSWER (badstatement)" in res_bs["problems"][0]
          and not res_fs["ok"] and "NO ANSWER (badstatement)" in res_fs["problems"][0])
    merged = report_ok.replace("badstatement", "notproved")       # what `#narrowing_report` printed before: no such state
    check("... and the run fails if Lean's report does not tell the two apart: the statement broken on purpose must come back `badstatement`, "
          "the name never declared `missing`",
          not narrowing.collect(one_open, merged + "NARROWING\tT.open_0\tnotproved\tsorryAx\n")["ok"]
          and not narrowing.collect(one_open, "NARROWING\tT.open_0\tnotproved\tsorryAx\n")["ok"]
          and narrowing.BAD_STATEMENT in narrowing.script(voc, [], [])[0])
    # ---- review of Q1/Q2, defect 2: a narrowed clause about a SEQUENCE (third faulty shape)
    seqs = ["An accepted batch followed by a computation of the total is accepted exactly when the total of the ledger's balances is at most the maximum",
            "A rejected batch followed by a computation of the total is accepted exactly when the total of the ledger's balances is at most the maximum",
            "A batch followed by a computation of the total is accepted exactly when the total of the ledger's balances is at most the maximum"]
    sq = [comp.rule(r, None) for r in rules_of(seqs)]
    is_seq = lambda rd: {f"{rd.id}#{j}": True for j in range(len(rd.claims))}
    check("third faulty shape (a narrowed rule about a sequence): it does not print that every call in the sequence must answer; it prints "
          "the sequence line of its Calls value, and the unnarrowed sequence still prints the line of `every`",
          all(isinstance(rd, vocab.Reading) for rd in sq) and [rd.coverage for rd in sq] == [["accepted"], ["rejected"], ["every"]]
          and all(cov[k]["sequence"] in texts(rd) for rd, k in zip(sq, ("accepted", "rejected", "every")))
          and not any("every call in it must answer" in t for rd in sq[:2] for t in texts(rd))
          and "every call in it must answer" in cov["every"]["sequence"] and "must answer" not in cov["accepted"]["sequence"] + cov["rejected"]["sequence"])
    check("the coverage check covers the sequence note: the three sequence rules pass when Lean says the operation is a sequence",
          all(narrowing.coverage_mismatches(side_of(rd), lean_says(rd), is_seq(rd)) == [] for rd in sq))
    old = side_of(sq[0])
    old[sq[0].id]["printed"] = [["seq", "every"] if t == ["seq", "accepted"] else t for t in old[sq[0].id]["printed"]]   # what was printed before
    hard = side_of(sq[0])
    hard[sq[0].id]["printed"] = narrowing.printed(voc, [(sl, "(of a sequence: something the book does not say)") if t == cov["accepted"]["sequence"] else (sl, t)
                                                        for sl, t in sq[0].echo])
    check("THE CONTROL (sequence note): the check reports the note that used to be printed for a narrowed sequence, a sequence note that is not "
          "a line of the book, a missing note, and a note on a claim Lean says is no sequence (this fails if the note leaves the check)",
          len(narrowing.coverage_mismatches(old, lean_says(sq[0]), is_seq(sq[0]))) == 1
          and len(narrowing.coverage_mismatches(hard, lean_says(sq[0]), is_seq(sq[0]))) == 1
          and len(narrowing.coverage_mismatches(side_of(sq[0]), lean_says(sq[0]), {})) == 1
          and len(narrowing.coverage_mismatches(side_of(sh[0]), lean_says(sh[0]), is_seq(sh[0]))) == 1)
    scen = [g for g in (comp.scenario(sc) for p in sorted((ROOT / "features").glob("*.feature"))
                        for sc in parse_feature(p, f"features/{p.name}").scenarios) if isinstance(g, vocab.Reading)]
    seq_scen = [rd for rd in scen if cov["every"]["sequence_scenario"] in texts(rd)]
    check(f"the sequence note of a scenario is a line of the book too ({len(seq_scen)} fixture scenarios print it), and no reading prints a "
          "sequence note that is not one",
          len(seq_scen) >= 1 and not any(["seq", "?"] in narrowing.printed(voc, rd.echo) for rd in scen + readings + sq)
          and all(["seq", "every"] in narrowing.printed(voc, rd.echo) for rd in seq_scen))
    # ---- review of Q1/Q2, defect 3: one clause, one narrowing word; a second is refused, never dropped, never the winner
    tw = {r.id: (comp.rule(r, None), loose_comp.rule(r, None)) for r in twice}
    check(f"THE CONTROL (narrowed twice): the {len(twice)} control lines tagged @narrowed-twice are refused, with the Q1 refusal on and off, "
          "and the message names the words (this fails if a second word is dropped or overrides the first again)",
          len(twice) >= 6 and all(isinstance(g, vocab.Problem) and g.code == "NARROWED-TWICE" and "more than one word" in g.message
                                  for pair in tw.values() for g in pair))
    msgs = {r.name: getattr(tw[r.id][0], "message", "") for r in twice}
    check("the refusal says what was written: both words, and why (no call is both; 'internal' is written after the one narrowing word, never before it)",
          "'internal' and 'accepted'" in msgs["An internal accepted transfer never changes the total of the ledger's balances"]
          and "after the one narrowing word" in msgs["An internal accepted transfer never changes the total of the ledger's balances"]
          and "'accepted' and 'if it is rejected'" in msgs["For an accepted transfer, if it is rejected, the ledger is unchanged"]
          and "no call is both accepted and rejected" in msgs["For an accepted transfer, if it is rejected, the ledger is unchanged"]
          and "asked for twice" in msgs["For a rejected transfer, if it is rejected, the ledger is unchanged"]
          and "'if it is rejected' and 'if it is accepted'" in msgs["For a transfer, if it is rejected, if it is accepted, the ledger is unchanged"])
    f2, _ = parse("Feature: Twice\n\n  Scenario: twice\n    Given Alice's balance is 10\n    When Alice withdraws 4\n"
                  "    Then if it is rejected, if it is accepted, Alice's balance is unchanged\n")
    g2 = comp.scenario(f2.scenarios[0])
    f3, _ = parse("Feature: Once\n\n  Scenario: once\n    Given Alice's balance is 10\n    When Alice withdraws 4\n"
                  "    Then if it is rejected, Alice's balance is unchanged\n")
    check("a scenario Then narrowed twice is refused the same way (and the same Then narrowed once compiles)",
          isinstance(g2, vocab.Problem) and g2.code == "NARROWED-TWICE" and isinstance(comp.scenario(f3.scenarios[0]), vocab.Reading))
    try:
        comp.calls_of(["successful", "rejected"])
        both = False
    except Exception as e:
        both = "more than one modifier" in str(e)
    check("the emitter never resolves two narrowings as 'the last one wins': it stops", both and comp.calls_of(["internal", "successful"]) == "accepted")
    # ---- ... and the coverage text is under the sign-off digest
    defs = vreport.lean_defs(voc)
    d0 = {i: vreport.piece_digest(voc, defs, i) for i in voc.coverage}
    book = voc.book_of("calls.accepted")          # the book that holds the coverage entries (core)
    keep_lines, keep_d10 = list(book.lines), voc.raw["defaults"]["D10"]
    book.lines = [l.replace("ONLY accepted calls [asked for]", "ONLY accepted calls") for l in book.lines]
    d1 = {i: vreport.piece_digest(voc, defs, i) for i in voc.coverage}
    book.lines = keep_lines
    voc.raw["defaults"]["D10"] = keep_d10 + " (changed)"
    d2 = {i: vreport.piece_digest(voc, defs, i) for i in voc.coverage}
    voc.raw["defaults"]["D10"] = keep_d10
    check("the coverage lines are entries of the book: signed by id, and a reading that prints one rests on it",
          set(voc.coverage) <= set(vreport.all_ids(voc)) and "calls.accepted" in sh[0].used and "calls.every" in a[0].used)
    check("changing a printed coverage line voids the sign-off of its entry and of no other; so does changing a default it names",
          [i for i in d0 if d0[i] != d1[i]] == ["calls.accepted"] and [i for i in d0 if d0[i] != d2[i]] == ["calls.every", "calls.accepted", "calls.rejected"])
    # ---- plan node Q3: every accepted surface form is in the book. CONTROL: take one form (or entry) out of the book and
    #      the sentence written with it no longer compiles; with the book intact it does. The book is edited in memory.
    from . import book as bookmod
    core_rel = f"{vocab.BOOK_DIR}/core.yaml"
    core_text = (ROOT / core_rel).read_text()

    def without(old, new=""):
        assert core_text.count(old) == 1, f"selftest: {old!r} occurs {core_text.count(old)} times in {core_rel}"
        return vocab.load_project(ROOT, gl, overrides={core_rel: core_text.replace(old, new)})

    def compiles(v, line):
        """A Rule line, or (a line that begins "Then ") the one Then of a small scenario."""
        try:
            if line.startswith("Then "):
                f, _ = parse(f"Feature: Removal\n\n  Scenario: one Then\n    Given Alice's balance is 10\n    When Alice deposits 4\n    {line}\n")
                return isinstance(vocab.Compiler(v).scenario(f.scenarios[0]), vocab.Reading)
            f, _ = parse(f"Feature: Removal\n\n  Rule: {line}\n")
            return isinstance(vocab.Compiler(v).rule(f.rules[0], None), vocab.Reading)
        except FeatureError:
            return False

    removals = [     # (what is taken out, the text removed from core.yaml, what replaces it, a Rule line that needs it)
        ("the verb phrase 'is always accepted'", '    vp_forms: ["is always accepted"]\n', '    vp_forms: []\n', "A deposit is always accepted"),
        ("the verb phrase 'is always rejected'", '    vp_forms: ["is always rejected"]\n', '    vp_forms: []\n', "A deposit is always rejected"),
        ("the article 'a'", '"a {op}", ', "", "A deposit always answers"),
        ("the article 'an'", ', "an {op}"]', "]", "An internal fund transfer always answers"),
        ("the subject word 'accepted'", '    subject_forms: ["accepted {op}"]\n', "", "An accepted deposit increases the wallet's balance by exactly the amount"),
        ("the subject word 'rejected'", '    subject_forms: ["rejected {op}"]\n', "", "A rejected deposit never changes the wallet's balance"),
        ("the subject word 'internal'", '    subject_forms: ["internal {op}"]\n', "", "An internal fund transfer always answers"),
        ("the claim prefix 'if it is accepted,' (before a Then)", '    claim_forms: ["if it is accepted, {claim}"]\n', "", "Then if it is accepted, Alice's balance is increased by exactly 4"),
        ("the claim prefix 'if it is rejected,' (before a Then)", '    claim_forms: ["if it is rejected, {claim}"]\n', "", "Then if it is rejected, Alice's balance is unchanged"),
        ("'for which' (given)", '    subject_forms: ["{op} for which {c:cond}"]\n', "",
         "A batch for which some transfer of the batch is valid on the ledger never changes the total of the ledger's balances"),
        ("'followed by' (and_then)", '    subject_forms: ["{op} followed by {op2}"]\n', "", "A batch followed by a computation of the total is always accepted"),
        ("the voice 'for <subject>, <claim>' (g.rule_for)", '    forms: ["for {subject}, {claim}"]\n', "    forms: []\n",
         "For a batch, the number of transfers applied is at most the length of the batch"),
        ("the voice '<subject> <verb phrase>' (g.rule_vp)", '    forms: ["{subject} {vp}"]\n', "    forms: []\n", "A deposit always answers"),
        ("' and ' between claims (g.claims)", '    forms: ["{claim} and {claim}"]\n', "    forms: []\n", "A deposit always answers and never changes the wallet's balance"),
        ("', and ' between clauses (g.clauses)", '    forms: ["{clause}, and {clause}"]\n', "    forms: []\n", "A deposit always answers, and a withdrawal always answers"),
        ("'the <role>' (g.role)", '    forms: ["the {role}"]\n', "    forms: []\n", "A withdrawal is accepted only if the amount is at most the wallet's balance"),
        ("the capital first letter (g.line)", "    first_letter_either_case: true", "    first_letter_either_case: false", "A deposit always answers"),
        ("the final full stop (g.line)", "    final_full_stop_optional: true", "    final_full_stop_optional: false", "a deposit always answers."),
        ("what 'is accepted only if' stands for (implied, only_if)",
         '    vp_forms: ["is accepted only if {k:cond}"]\n    implied: { c: accepted }\n', '    vp_forms: ["is accepted only if {k:cond}"]\n',
         "A withdrawal is accepted only if the amount is at most the wallet's balance"),
        ("the default D4 (its text)", '  D4: "for all values:', '  D40: "for all values:', "A deposit always answers"),
    ]
    intact = vocab.load_project(ROOT, gl)
    res = [(what, compiles(intact, line), compiles(without(old, new), line)) for what, old, new, line in removals]
    check(f"Q3 control: each of {len(removals)} surface forms and texts taken out of the book makes its sentence fail to compile "
          "(and every one of the sentences compiles with the book intact)",
          all(a and not b for _, a, b in res))
    for what, a, b in res:
        if not a or b:
            print(f"       {what}: intact compiles={a}, removed compiles={b}")
    # ---- ... and the SCOPING modifiers a scenario or a subject is put together with (`given`, `and_then`, `beside`, `internal`):
    #      their Lean text is the `lean:` of the book entry, not a constant of the compiler. CONTROL: with the entry out of the book
    #      no sentence that uses it compiles to its term; with its `lean:` text changed, exactly the sentences that use it change.
    terms0 = bookmod.compiled_terms(intact)
    def users(id_):
        return {i for i, t in terms0.items() if t["compiled"] and id_ in t["pieces"]}
    def differs(v, i):
        t = bookmod.compiled_terms(v)[i]
        return any(t.get(k) != terms0[i].get(k) for k in ("compiled", "status", "code", "lean_sha256")), t["compiled"]
    def cut(id_):
        m = re.search(rf"^  - id: {id_}\n(?:(?!  - id: |  # ====).*\n)*", core_text, re.M)
        return vocab.load_project(ROOT, gl, overrides={core_rel: core_text[:m.start()] + core_text[m.end():]})
    scoping = [("given", '=> {c})"', '=> ¬ ({c}))"'), ("and_then", '"({op}).andThen {op2}"', '"({op2}).andThen ({op})"'),
               ("internal", "{member} {parties}", "{parties} {member}"), ("beside", '"({op}).beside {type}"', '"({op}).beside ({type} × Unit)"')]
    sc_rows = []
    for id_, old, new in scoping:
        u = users(id_)
        gone_ = cut(id_)
        still = sorted(i for i in u if differs(gone_, i)[1])                       # sentences that use it and still compile without it
        v_ = without(old, new)
        changed = {i for i in terms0 if differs(v_, i)[0]}
        sc_rows.append((id_, len(u), still, changed == u))
    check("Q3 control: each of the scoping modifiers given, and_then, internal, beside taken out of the book makes EVERY fixture sentence "
          f"that uses it fail to compile ({', '.join(f'{i}: {n}' for i, n, _, _ in sc_rows)} sentences), and changing its `lean:` text "
          "changes the term of exactly those sentences (the text signed is the text emitted)",
          all(n and not still and same for _, n, still, same in sc_rows))
    for id_, n, still, same in sc_rows:
        if not n or still or not same:
            print(f"       {id_}: {n} users; still compiling without it: {still[:4]}; a changed `lean:` changes exactly its users: {same}")
    # ---- plan node C1, CONTROL of the two checks that core stands alone which read the files (not the loader): a fixture noun
    #      written into a comment of the frame library or of core.yaml, and an import from outside the frame library, are reported
    #      with file and line; the unchanged copy passes. (The build of lean/Frames alone needs Lean: mutation control c42.)
    import shutil as _sh
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        _sh.copytree(ROOT / vocab.BOOK_DIR, d / vocab.BOOK_DIR)
        _sh.copy(ROOT / "glossary.yaml", d / "glossary.yaml")
        _sh.copytree(ROOT / "lean" / "Frames", d / "lean" / "Frames")
        clean = bookmod.core_alone(root=d)
        fc, fl, cy = d / "lean/Frames/Core.lean", d / "lean/Frames/Lemmas.lean", d / core_rel
        keep = {p: p.read_text() for p in (fc, fl, cy)}
        def seeded_core(p, text, top=False):
            p.write_text(text + keep[p] if top else keep[p] + text)
            r = bookmod.core_alone(root=d)
            p.write_text(keep[p])
            return r
        n_core = len(keep[fc].splitlines())
        r_noun = seeded_core(fc, "\n-- every account of the ledger\n")
        r_yaml = seeded_core(cy, "\n# said of a wallet\n")
        r_imp = seeded_core(fl, "import Wallet.Pieces\n", top=True)
        r_word = seeded_core(fc, "\n-- accounting for the ledgerless, and rewalleting\n")          # whole words only
        nouns_ = bookmod.fixture_nouns(intact, gl)
    check("core stands alone, THE CONTROL of the noun scan and of the import check: the unchanged copy passes; a comment naming "
          "`account` and `ledger` in lean/Frames/Core.lean, a comment naming `wallet` in core.yaml, and `import Wallet.Pieces` in "
          "lean/Frames/Lemmas.lean are each reported with the file (and the line of the noun); a longer word that contains a noun is not",
          clean["ok"] and not r_noun["ok"] and any(p.startswith(f"lean/Frames/Core.lean:{n_core + 2}: names `account`") for p in r_noun["problems"])
          and any("names `ledger`" in p for p in r_noun["problems"])
          and not r_yaml["ok"] and any(p.startswith(core_rel) and "names `wallet`" in p for p in r_yaml["problems"])
          and not r_imp["ok"] and any("lean/Frames/Lemmas.lean: imports Wallet.Pieces, which is outside the frame library" in p for p in r_imp["problems"])
          and r_word["ok"] and bookmod.find_nouns("the Wallet. of an Account", nouns_) and not bookmod.find_nouns("frames and claims", nouns_))
    # ---- ... and the registration lint can see each kind of violation (seeded into the book in memory)
    def keys(v):
        return {(x["check"].split(" (")[0], x["key"]) for x in bookmod.lint(v)[0]}
    base = keys(intact)
    def seeded(old, new, rel=core_rel):
        t = (ROOT / rel).read_text()
        assert t.count(old) == 1, f"selftest: {old!r} occurs {t.count(old)} times in {rel}"
        return keys(vocab.load_project(ROOT, gl, overrides={rel: t.replace(old, new)})) - base
    s1 = seeded('forms: ["{m:measure<T>} is {t:term<T>}"]', 'forms: ["{m:measure<T>} is {t:term<T>}", "{m:measure<T>} is zero"]')
    s1c = seeded('forms: ["{m:measure<num>} plus {t:term<num>} exceeds {z:term<num>}"]',
                 'forms: ["{m:measure<num>} plus {t:term<num>} exceeds {z:term<num>}", "{m:measure<num>} and {t:measure<num>} exceed {z:term<num>}"]')
    s2 = seeded('forms: ["{m:measure<num>} plus {t:term<num>} exceeds {z:term<num>}"]',
                'forms: ["{m:measure<num>} plus {t:term<num>} exceeds {z:term<num>}", "{t:term<num>} on top of {m:measure<num>} exceeds {z:term<num>}", '
                '"{m:measure<num>} added to {z:term<num>} goes beyond {t:term<num>}"]')
    led = f"{vocab.BOOK_DIR}/ledger.yaml"
    s4 = seeded('forms: ["the balance of account {k:term<acct>} of {l:ledger}"]',
                'forms: ["the balance of account {k:term<acct>} of {l:ledger}", "the balance of {k:term<acct>} in {l:ledger}"]', led)
    # A SEPARATION lifts a pair only while it is IN FORCE: its two sentences are compiled and each is read as its own piece and
    # not the other, and a sign-off of the entry (`clausal review <id>`, stored beside its book) is on record for exactly that.
    # Done in a copy of clausebook/, because signing writes a file.
    import contextlib, io, shutil
    S_MORE = "A withdrawal for which the amount is more than the wallet's balance is always rejected"          # read with more_than
    S_EXC = "A withdrawal for which the wallet's balance is more than the amount always answers"               # read with exceeds
    SEP, PAIR, NIF = "sep.more_than.exceeds", "{} is more than {}|exceeds,more_than", "4 separation not in force"
    def sep_yaml(a=S_MORE, b=S_EXC):
        return f"separations:\n  - id: {SEP}\n    between: [more_than, exceeds]\n    inputs:\n      more_than: \"{a}\"\n      exceeds: \"{b}\"\ngrammar:\n"
    with tempfile.TemporaryDirectory() as d:
        shutil.copytree(ROOT / vocab.BOOK_DIR, Path(d) / vocab.BOOK_DIR)
        books_d = [(Path(d) / rel, rel) for _, rel in vocab.project_books(ROOT)]
        def with_sep(text=None):
            t = core_text.replace("grammar:\n", sep_yaml() if text is None else text)
            return vocab.Vocabulary(books_d, gl, overrides={core_rel: t})
        def sign(v):
            with contextlib.redirect_stdout(io.StringIO()):
                vreport.review(v, SEP, "test-reviewer")
        v_sep = with_sep()
        k_unsigned = keys(v_sep)                                   # recorded, compiles, separates; nobody signed
        sign(v_sep)
        k_signed = keys(v_sep)                                     # ... and signed: in force
        k_reworded = keys(with_sep(sep_yaml(b="A deposit for which the wallet's balance is more than the amount always answers")))   # a sentence changed after signing
        t_piece = core_text.replace("grammar:\n", sep_yaml())
        assert t_piece.count('echo: "{m} is strictly more than {t}"') == 1
        k_piece = keys(vocab.Vocabulary(books_d, gl, overrides={core_rel: t_piece.replace('echo: "{m} is strictly more than {t}"', 'echo: "{m} is above {t}"')}))   # a piece changed after signing
        v_same = with_sep(sep_yaml(b=S_MORE))                      # both sentences are read with more_than: nothing is told apart
        sign(v_same)
        k_same = keys(v_same)
        v_text = with_sep(sep_yaml(a="(recorded for the self-test only)", b="(recorded for the self-test only)"))                    # two strings that are no sentences
        sign(v_text)
        k_text = keys(v_text)
        v_off = with_sep(sep_yaml(a="A withdrawal always answers", b="A deposit always answers"))    # sentences that compile and have nothing to do with the pair
        sign(v_off)
        k_off = keys(v_off)
        try:                                                       # the form of the first build: two strings and a name
            with_sep("separations:\n  - between: [more_than, exceeds]\n    input: \"(recorded for the self-test only)\"\n    signed_by: selftest\ngrammar:\n")
            old_form = False
        except FeatureError:
            old_form = True
    sep_ok = (base - k_signed == {("4 shared skeleton", PAIR)} and not (k_signed - base)                 # in force: lifts exactly that pair
              and all(base <= k and k - base == {(NIF, SEP)} for k in (k_unsigned, k_reworded, k_piece, k_same, k_text, k_off)) and old_form)
    check("book check 1: a form with a hole filled by a literal, and a hole given another category, are reported",
          any(k[0] == "1 holes" and k[1].startswith("is|forms|{m:measure<T>} is zero") for k in s1)
          and any(k[0] == "1 holes" and "and {t:measure<num>} exceed" in k[1] for k in s1c))
    check("book check 2: holes of one category in another order are reported; holes of different categories in another order are not",
          any(k[0] == "2 order" and "added to" in k[1] for k in s2) and not any(k[0] == "2 order" and "on top of" in k[1] for k in s2))
    check("book check 3: a second form in one position is reported", any(k[0] == "3a one form per position" and k[1] == "is|forms" for k in s1))
    check("book check 4: a form that takes another piece's skeleton is reported (\"the balance of {k} in {l}\" as a form of l.bal_of "
          "against l.balance_at)", any(k[0] == "4 shared skeleton" and k[1].startswith("the balance of {} in {}|") for k in s4))
    check("book check 4, THE CONTROL: a separation lifts its pair, and only that pair, when its two sentences compile, each is read as its "
          "own piece and not the other, and the entry has a valid sign-off record. It lifts nothing, and is itself reported, when it is "
          "unsigned; when a sentence or a piece changed after the sign-off; when both sentences are read as the same piece; when the "
          "inputs are not sentences; when they compile and are not written with the shared skeleton (the last three although signed). "
          "Two strings and a name (`input:`, `signed_by:`) are refused by the loader",
          sep_ok)
    if not sep_ok:
        for n_, k_ in (("unsigned", k_unsigned), ("signed", k_signed), ("reworded", k_reworded), ("piece", k_piece), ("same", k_same), ("text", k_text), ("off", k_off)):
            print(f"       {n_}: lifted {sorted(base - k_)}, added {sorted(k_ - base)}")
        print(f"       old form refused: {old_form}")
    v5 = bookmod.same_terms(without('vp_forms: ["never changes {m:measure<T>}"]', 'vp_forms: ["never alters {m:measure<T>}"]'))[0]
    v5b = bookmod.same_terms(without('    lean: "{m} = {t}"', '    lean: "{t} = {m}"'))[0]
    check("book check 5: a sentence of the fixtures that stops compiling, or compiles to another term, is reported; none is on the book as it stands",
          len(v5) > 0 and all("is now refused" in x["what"] for x in v5) and len(v5b) > 0 and all("another Lean term" in x["what"] for x in v5b)
          and not bookmod.same_terms(intact)[0])
    # ---- plan node Q4: REPLACEMENT. The old form of each row of the first batch is refused (UNBOUND, code RETIRED-FORM), the
    #      refusal names the clause to write, and that clause compiles. (clausebook/q4/FREEZE.md lists the rows.)
    retired_cases = [     # (row, the Rule line as it was written before, the clause the refusal must name)
        ("1", "A successful deposit increases the wallet's balance by exactly the amount", "an accepted deposit increases the wallet's balance by exactly the amount"),
        ("2", "A deposit always succeeds", "a deposit is always accepted"),
        ("2", "A deposit is never accepted", "a deposit is always rejected"),
        ("4", "For a lookup, if it is accepted, the result is the balance of the account in the ledger",
         "for an accepted lookup, the result is the balance of the account in the ledger"),
        ("4", "For an internal transfer, if it is accepted, the total of the ledger's balances is unchanged",
         "an accepted internal transfer never changes the total of the ledger's balances"),
        ("5", "Every deposit always answers", "a deposit always answers"),
        ("5", "Any internal transfer always answers", "an internal transfer always answers"),
        ("6, 7a", "An internal fund transfer never changes the aggregate account value of the ledger", "an internal fund transfer never changes the total of the ledger's balances"),
        ("7a", "A batch never changes the total of all balances of the ledger", "a batch never changes the total of the ledger's balances"),
        ("7a", "A batch never changes the total of the balances of the ledger", "a batch never changes the total of the ledger's balances"),
        ("7b", "For a lookup, the result is the balance of account the account of the ledger", "for a lookup, the result is the balance of the account in the ledger"),
        ("8", "A withdrawal is accepted only if the amount is not more than the wallet's balance", "a withdrawal is accepted only if the amount is at most the wallet's balance"),
        ("9", "A deposit is accepted whenever the wallet's balance plus the amount does not exceed the maximum",
         "a deposit is accepted whenever the wallet's balance plus the amount is at most the maximum"),
        ("10", "A transfer never loses acceptance when the amount is smaller", "a transfer never loses acceptance when the amount is the same or smaller"),
        ("11", "For a batch, every transfer at which the batch stopped is not valid on the ledger afterwards",
         "for a batch, no transfer at which the batch stopped is valid on the ledger afterwards"),
        ("12", "For a deposit, the wallet's balance is unchanged", "a deposit never changes the wallet's balance"),
        ("12", "For a deposit, it answers", "a deposit always answers"),
        ("12, 13", "For a deposit, the wallet's balance is increased by the amount", "a deposit increases the wallet's balance by exactly the amount"),
        ("12", "For a batch, the number of transfers applied is zero and the ledger is unchanged",
         "for a batch, the number of transfers applied is zero, and a batch never changes the ledger"),
        ("14", "A transfer never loses that it is accepted when the amount is the same or smaller", "a transfer never loses acceptance when the amount is the same or smaller"),
        ("15", "A transfer gives the same answer when the amount is the same or larger, if it is rejected",
         "a transfer gives the same answer when the amount is the same or larger, if the first call is rejected"),
    ]
    q4 = []
    for row, was, now in retired_cases:
        r = comp.rule(rules_of([was])[0], None)
        named = isinstance(r, vocab.Problem) and r.status == "UNBOUND" and r.code == vocab.RETIRED and f'write the clause as: "{now}"' in r.hint
        again = [loose_comp.rule(x, None) for x in rules_of([now[0].upper() + now[1:]])][0]
        q4.append((row, was, named, isinstance(again, vocab.Reading)))
    check(f"Q4 control: each of {len(retired_cases)} Rule lines written with an old form of the first batch (rows 1, 2, 4 to 15) is refused "
          "as RETIRED-FORM, the refusal names the clause to write, and that clause compiles",
          all(named and ok for _, _, named, ok in q4))
    for row, was, named, ok in q4:
        if not (named and ok):
            print(f"       row {row}: \"{was}\": refused with the clause to write: {named}; that clause compiles: {ok}")
    fq, _ = parse("Feature: Retired\n\n  Scenario: old steps\n    Given Alice's balance is 10\n    And 4 is not more than Alice's balance\n"
                  "    When Alice withdraws 4\n    Then the operation succeeds\n    And Alice's balance is decreased by 4\n")
    rq = comp.scenario(fq.scenarios[0])
    fq2, _ = parse("Feature: Live\n\n  Scenario: new steps\n    Given Alice's balance is 10\n    And 4 is at most Alice's balance\n"
                   "    When Alice withdraws 4\n    Then it is accepted\n    And Alice's balance is decreased by exactly 4\n")
    check("Q4 control (rows 3, 8, 13 in a scenario): steps written with old forms are refused as RETIRED-FORM, each with the step to write; "
          "the scenario written with those steps compiles",
          isinstance(rq, vocab.Problem) and rq.code == vocab.RETIRED
          and all(x in rq.hint for x in ('"4 is at most Alice\'s balance"', '"it is accepted"', '"Alice\'s balance is decreased by exactly 4"'))
          and isinstance(comp.scenario(fq2.scenarios[0]), vocab.Reading))
    # ... and each refusal of a SHAPE is what the book says, not a constant of the compiler: with the line taken out of the book
    # the sentence compiles again.
    shape_lines = [
        ("`reads: no_verb_phrase` (g.rule_for)", "    reads: no_verb_phrase ", "    was_reads: no_verb_phrase ", "For a deposit, the wallet's balance is unchanged"),
        ("`narrowing: on_subject` (g.rule_for)", "    narrowing: on_subject ", "    was_narrowing: on_subject ",
         "For a lookup, if it is accepted, the result is the balance of the account in the ledger"),
        ("`negated:` (every_of)", "    negated: { p: none_of } ", "    was_negated: { p: none_of } ",
         "For a batch, every transfer at which the batch stopped is not valid on the ledger afterwards"),
        ("`implied_only:` (monotone)", "    implied_only: true ", "    was_implied_only: true ",
         "A transfer never loses that it is accepted when the amount is the same or smaller"),
    ]
    sh4 = [(what, compiles(intact, line), compiles(without(old, new), line)) for what, old, new, line in shape_lines]
    check("Q4 control: each refused shape (a Then form of a frame that has a verb phrase, a narrowing before the claim of a Rule line, "
          "`every ... is not ...`, `never loses that it is accepted`) is refused because of a line of the book: with the line out, the sentence compiles",
          all(not a and b for _, a, b in sh4))
    for what, a, b in sh4:
        if a or not b:
            print(f"       {what}: compiles with the book intact: {a}; with the line out: {b}")
    both = comp.rule(rules_of(["An accepted internal transfer never changes the total of the ledger's balances"])[0], None)
    check("Q4: a subject takes one narrowing word and then `internal`; the reading carries BOTH (neither word is dropped)",
          isinstance(both, vocab.Reading) and both.coverage == ["accepted"] and ".internal " in both.claims[0].lean and ".successful" in both.claims[0].lean)
    led_local = f"{vocab.BOOK_DIR}/local/ledger.yaml"
    try:
        tl = (ROOT / led_local).read_text()
        assert tl.count("accepted: { holds: [l.accepted], one_answer: true }") == 2
        vocab.load_project(ROOT, gl, overrides={led_local: tl.replace("accepted: { holds: [l.accepted], one_answer: true }", "accepted: { one_answer: true }")})
        same_as_ = False
    except FeatureError as e:
        same_as_ = "same_as" in str(e)
    check("Q4: `same_as: accepted` on a class is not taken on trust: it is refused unless the `narrowing:` facts of every operation it can be "
          "said of (kernel-checked on every run) list it under both `accepted: holds` and `rejected: fails`", same_as_)
    dgq = lambda v: {i: vreport.piece_digest(v, vreport.lean_defs(v), i) for i in vreport.all_ids(v)}
    d_now, d_ret = dgq(intact), dgq(without('was: "always succeeds"', 'was: "always wins"'))
    check("Q4 (row 19): a retired form is in its entry and under that entry's digest: changing it voids the sign-off of that entry and of no other",
          [i for i in d_now if d_now[i] != d_ret[i]] == ["always"])
    # ---- plan node Q8: the four mechanical negative controls of the readability synthesis (section 3). Each is refused, for the
    #      stated reason.
    q8_1 = seeded('    vp_forms: ["gives the same answer when {v:variation}"]\n', '    vp_forms: ["never changes the answer when {v:variation}"]\n')
    q8_23 = [comp.rule(r, None) for r in rules_of(["A rejected transfer gives the same answer when the amount is the same or larger",
                                                   "An accepted transfer never loses acceptance when the amount is the same or larger"])]
    q8 = [any(k[0] == "4 head collision" and k[1] == "never changes the answer when {}|never_changes,same_answer" for k in q8_1),
          isinstance(q8_23[0], vocab.Problem) and q8_23[0].status == "SAYS-NOTHING" and "Frames.Narrowed.independentOf," in q8_23[0].message,
          isinstance(q8_23[1], vocab.Problem) and q8_23[1].status == "SAYS-NOTHING" and "Frames.Narrowed.monotone_holds," in q8_23[1].message,
          any(k[0] == "4 shared skeleton" and k[1].startswith("the balance of {} in {}|") and "l.bal_of" in k[1] and "l.balance_at" in k[1] for k in s4)]
    check("Q8, the four mechanical negative controls: (1) \"never changes the answer when {v}\" as the verb phrase of frame 14 is reported by the "
          "lint as taking the head of `never_changes`, no separating pair signed; (2) \"A rejected transfer gives the same answer when the amount "
          "is the same or larger\" and (3) \"An accepted transfer never loses acceptance when the amount is the same or larger\" are refused as "
          "SAYS-NOTHING with the theorem; (4) \"the balance of {k} in {l}\" as a form of `l.bal_of` is reported as sharing a skeleton with `l.balance_at`",
          all(q8))
    if not all(q8):
        print(f"       controls 1 to 4 refused: {q8}; lint keys added by control 1: {sorted(q8_1)}")
    # ---- plan node Q5: the duplicate-meaning report
    from . import duplicates
    dup_fix = duplicates.groups(intact, duplicates.compiled(intact, sorted((ROOT / "features").glob("*.feature"))))
    with tempfile.TemporaryDirectory() as d:
        pq = Path(d) / "pair.feature"
        pq.write_text("Feature: Pair\n\n  Rule: A batch applied as a whole is always accepted\n\n  Rule: For a batch applied as a whole, it is accepted\n\n"
                      "  Rule: A batch applied as a whole always answers\n")
        dup_pair = duplicates.groups(intact, duplicates.compiled(intact, [pq]))
    ids_of = lambda gs: [sorted(m["id"] for m in g["members"]) for g in gs]
    check("Q5: the duplicate report finds the two Rule lines of the fixtures that differ only in the noun of one operation, and (on a file of its "
          "own) \"is always accepted\" against \"for ..., it is accepted\", whose Lean texts differ and are the same once the operation's acceptance "
          "is unfolded; a third line that says something else is in no group",
          ["Rule.ledger_rules.n1_internal_transfer", "Rule.ledger_rules.readme_internal_transfers"] in ids_of(dup_fix)
          and len(dup_pair) == 1 and len(dup_pair[0]["members"]) == 2 and not dup_pair[0]["same_lean"])
    # ---- ... and the new entries are under the sign-off digest
    defs = vreport.lean_defs(intact)
    dg = lambda v: {i: vreport.piece_digest(v, vreport.lean_defs(v), i) for i in vreport.all_ids(v)}
    d0, d1 = dg(intact), dg(without('"any {op}"', '"each {op}"'))
    d2 = dg(without('  D4: "for all values:', '  D4: "for all the values:'))
    f, _ = parse("Feature: Digest\n\n  Rule: A deposit always answers\n")
    used = vocab.Compiler(intact).rule(f.rules[0], None).used
    check("the grammar entries and the defaults are entries of the book: signed by id; changing a form or a default's text voids that "
          "entry's sign-off and no other; a Rule reading rests on the grammar it was read through and on every default printed with it",
          [i for i in d0 if d0[i] != d1[i]] == ["g.subject"] and [i for i in d0 if d0[i] != d2[i]] == ["D4"]
          and {"g.subject", "g.rule_vp", "g.line", "D1", "D2", "D4"} <= set(used))
    # ---- plan node C1: a list of books; sign-offs stored per book, beside it
    import contextlib, io, shutil
    with tempfile.TemporaryDirectory() as d:
        shutil.copytree(ROOT / vocab.BOOK_DIR, Path(d) / vocab.BOOK_DIR)
        v = vocab.Vocabulary([(Path(d) / rel, rel) for _, rel in vocab.project_books(ROOT)], gl)
        with contextlib.redirect_stdout(io.StringIO()):
            vreport.review(v, "all", "test-reviewer")
        vd = vreport.lean_defs(v)
        per_book = {b.name: set(json.loads(b.signoff_path.read_text())) for b in v.books}
        all_signed = vreport.reviewed_pieces(v, vd) == set(vreport.all_ids(v))
        core_b, led_b = v.books[0], v.book_of("l.bal_of")
        a_, b_ = json.loads(core_b.signoff_path.read_text()), json.loads(led_b.signoff_path.read_text())
        a_["l.bal_of"] = b_.pop("l.bal_of")
        core_b.signoff_path.write_text(json.dumps(a_))
        led_b.signoff_path.write_text(json.dumps(b_))
        moved = "l.bal_of" in vreport.reviewed_pieces(v, vd)
    check("sign-offs are stored per book, beside it: each file holds exactly the entries its book defines; a record of an entry "
          "in another book's file is not a sign-off of it",
          all_signed and all(per_book[b.name] == {i for i, h in v.home.items() if h is b} for b in v.books) and not moved)
    core_only = vocab.Vocabulary([(ROOT / core_rel, core_rel)])
    try:
        vocab.Vocabulary([(ROOT / core_rel, core_rel), (ROOT / core_rel, core_rel)])
        twice_ = False
    except FeatureError:
        twice_ = True
    try:
        without('forms: ["zero"]', 'forms: ["{x:amount}"]')
        typed_ = False
    except FeatureError as e:
        typed_ = "uses_types" in str(e)
    check("core loads alone, with no glossary and no other book; a book cannot be loaded twice; core cannot name a literal type of the project",
          core_only.kinds() == {"domain": 0, "modifier": 23, "frame": 25} and not core_only.ops and twice_ and typed_)
    print(f"{'all checks passed' if not bad else str(len(bad)) + ' CHECKS FAILED'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
