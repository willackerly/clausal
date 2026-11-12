"""Fast checks of the Rule parser, tag inheritance and the suite-adequacy bookkeeping. No Lean, no Rust, no out/.

    python3 -m clausal.selftest

The end-to-end controls (a real suite with its progress scenario removed, an ill-typed trivial model, a tag
taken off a Rule) are c16 to c20 in mutation/run_mutants.py; these are the same ideas at the level of the Python.
"""
from __future__ import annotations

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
    comp = vocab.Compiler(vocab.Vocabulary(ROOT / "clausebook.yaml", "clausebook.yaml", gl))
    vf, _ = parse("Feature: Refusals\n\n  Rule: A batch never leaves the ledger below zero\n\n  Rule: A withdrawal never alters the wallet's balance\n\n"
                  "  Rule: A transfer always answers\n\n  Rule: A withdrawal is accepted whenever the amount is not more than the wallet's balance\n")
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
    four = ["A successful transfer never loses acceptance when the amount is larger",
            "A successful transfer gives the same answer when the amount is larger",
            "A rejected transfer gives the same answer when only the amount differs",
            "A successful transfer never loses that it is rejected when the amount is smaller"]
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
    shapes = ["For a lookup, if it is accepted, the result is the balance of the account in the ledger",
              "For a transfer, if it is rejected, the ledger is unchanged",
              "A successful lookup gives the same answer when the ledger is extended"]
    sh = [comp.rule(r, None) for r in rules_of(shapes)]
    texts = lambda rd: [t for _, t in getattr(rd, "echo", [("", "(refused)")])]
    cov = voc.covers
    check("first faulty shape ('for X, if it is accepted / rejected, ...'): covers the narrowed calls only, no answer required, D1 and D2 not applied",
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
    seqs = ["A successful batch followed by a computation of the total is accepted exactly when the total of the balances of the ledger is at most the maximum",
            "A rejected batch followed by a computation of the total is accepted exactly when the total of the balances of the ledger is at most the maximum",
            "A batch followed by a computation of the total is accepted exactly when the total of the balances of the ledger is at most the maximum"]
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
    check("the refusal says what was written: both words, and why (no call is both; 'internal' with a narrowing word is not a composition)",
          "'successful' and 'internal'" in msgs["A successful internal transfer never changes the total of all balances of the ledger"]
          and "'successful' and 'if it is rejected'" in msgs["For a successful transfer, if it is rejected, the ledger is unchanged"]
          and "no call is both accepted and rejected" in msgs["For a successful transfer, if it is rejected, the ledger is unchanged"]
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
    keep_lines, keep_d10 = list(voc.lines), voc.raw["defaults"]["D10"]
    voc.lines = [l.replace("ONLY accepted calls [asked for]", "ONLY accepted calls") for l in voc.lines]
    d1 = {i: vreport.piece_digest(voc, defs, i) for i in voc.coverage}
    voc.lines = keep_lines
    voc.raw["defaults"]["D10"] = keep_d10 + " (changed)"
    d2 = {i: vreport.piece_digest(voc, defs, i) for i in voc.coverage}
    voc.raw["defaults"]["D10"] = keep_d10
    check("the coverage lines are entries of the book: signed by id, and a reading that prints one rests on it",
          set(voc.coverage) <= set(vreport.all_ids(voc)) and "calls.accepted" in sh[0].used and "calls.every" in a[0].used)
    check("changing a printed coverage line voids the sign-off of its entry and of no other; so does changing a default it names",
          [i for i in d0 if d0[i] != d1[i]] == ["calls.accepted"] and [i for i in d0 if d0[i] != d2[i]] == ["calls.every", "calls.accepted", "calls.rejected"])
    print(f"{'all checks passed' if not bad else str(len(bad)) + ' CHECKS FAILED'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
