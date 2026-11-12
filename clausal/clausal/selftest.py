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
    # ---- plan node E2: a statement about a collection of open length, not proved and not shown false, is flagged with
    #      the largest size each layer tried (clausal/sizes.py); made-up results, no run needed
    from . import sizes
    rid = "Rule.x.probe"
    genr = {"collections": {"balances": True, "batch": True}}
    side = {"vars": [["the_ledger", ["[]", "[1, 0, 0, 1]"]], ["the_batch", ["[]", "[0->1:1, 1->0:1, 0->1:1]"]], ["the_account", ["0", "7"]]],
            "rust": {"types": {"the_ledger": "balances", "the_batch": "batch", "the_account": "index"}}}

    def rung(a, t, status):
        return {"label": f"up to {a} accounts and up to {t} transfers", "accounts": a, "transfers": t, "status": status}
    evd = {"size": 6, "quick": False, "readings": {rid: {"property": {"status": "pass", "cases": 10000, "limit": {"accounts": 8, "transfers": 6},
                                                                      "longest": {"accounts": 8, "transfers": 5}},
                                                         "bounded": {"ran": True, "rungs": [rung(2, 1, "verified"), rung(6, 4, "timeout")]}}}}
    a = sizes.assess("TESTED-ONLY", genr, side, evd, rid)
    check("E2: a tested-only statement about a ledger and a batch is flagged, with the largest size each layer tried",
          a["flag"] and a["text"].startswith(sizes.FLAG) and "at most 4 accounts and 3 transfers" in a["text"]
          and "property test: at most 8 accounts and 6 transfers (the longest its generators can produce for this statement; the longest "
                                                                  "among the inputs in scope that passed: 8 accounts and 5 transfers)" in a["text"] and "more than 6 accounts and 4 transfers" in a["text"]
          and "it holds at up to 2 accounts and up to 1 transfers; NOT verified at up to 6 accounts and up to 4 transfers" in a["text"]
          and "says NOTHING about larger inputs" in a["text"])
    check("E2: the same statement with a proof for all inputs is not flagged; nor is one shown false",
          not sizes.assess("PROVED-FOR-ALL", genr, side, evd, rid)["flag"] and not sizes.assess("REFUTED", genr, side, evd, rid)["flag"]
          and not sizes.assess("COUNTEREXAMPLE", genr, side, evd, rid)["flag"])
    check("E2: a statement that speaks of no collection of open length is not flagged, whatever its verdict",
          not sizes.assess("TESTED-ONLY", {"collections": {"balances": False, "batch": False}}, side, evd, rid)["flag"])
    check("E2: a reading with no generated harness (sizes unknown) IS flagged: the flag fails towards saying less was checked",
          sizes.assess("TESTED-ONLY", None, side, evd, rid)["flag"] and "could not be determined" in sizes.assess("TESTED-ONLY", None, side, evd, rid)["text"])
    q = sizes.assess("TESTED-ONLY", genr, None, {"size": 6, "quick": True, "readings": {rid: {"property": {"status": "pass", "cases": 5}, "bounded": {"ran": False, "rungs": []}}}}, rid)
    n = sizes.assess("UNLINKED", genr, side, None, rid)
    check("E2: a layer that did not run is reported as not run, never as a size tried",
          q["flag"] and "bounded check (Kani): not run (--quick skips it)" in q["text"] and "Grid search (Lean model, and the compiled Rust when it ran): not run" in q["text"]
          and n["flag"] and "property test: not run" in n["text"] and "bounded check (Kani): not run." in n["text"])

    class FakeVerdict:
        def __init__(self):
            self.flags, self.lines, self.fatal, self.as_expected = [], [], [], True
    ok_, lost = FakeVerdict(), FakeVerdict()
    sizes.apply(ok_, "TESTED-ONLY", rid, [sizes.TAG], {rid: genr}, {rid: side}, evd)
    sizes.apply(lost, "TESTED-ONLY", rid, [sizes.TAG], {rid: {"collections": {"balances": False, "batch": False}}}, {rid: side}, evd)
    check("E2, THE CONTROL: a sentence tagged " + sizes.TAG + " passes with the flag and FAILS when the flag is not there",
          ok_.as_expected and ok_.flags == [sizes.FLAG] and not ok_.fatal and len(ok_.lines) == 1
          and not lost.as_expected and lost.flags == [] and any("EXPECTED FLAG MISSING" in x for x in lost.fatal))
    # fix round: the property-test size is what the runner recorded for the reading, never the bare --size
    old = sizes.assess("TESTED-ONLY", genr, side, {"size": 6, "readings": {rid: {"property": {"status": "pass", "cases": 7}}}}, rid)
    one = sizes.assess("TESTED-ONLY", {"collections": {"balances": True, "batch": False}}, side, evd, rid)
    check("E2: the property-test size is the limit the runner recorded for the reading (8 accounts in a second call), only for "
          "the collections no Given fixes; a row with no recorded limit says so and gives no number",
          "limit not recorded" in old["text"] and "at most 6" not in old["text"].split("Generated property test")[1].split("Generated bounded")[0]
          and "property test: at most 8 accounts (the longest" in one["text"] and "6 transfers (the longest" not in one["text"])
    over = {"readings": {"R.a": {"property": {"limit": {"accounts": 6, "transfers": None}, "longest": {"accounts": 8, "transfers": None}}},
                         "R.b": {"property": {"limit": {"accounts": 8, "transfers": 6}, "longest": {"accounts": 8, "transfers": 0}}}}}
    check("E2: a property test that drew a collection longer than the limit it states is an error (the reported size would be too small)",
          len(sizes.overdrawn(over)) == 1 and "R.a drew 8 accounts, more than the limit it states (6)" in sizes.overdrawn(over)[0]
          and sizes.overdrawn(evd) == [] and sizes.overdrawn(None) == [])
    # fix round: the check that a tagged sentence is REPORTED with the flag, on the graph and the rendered block alone
    from . import mustflag, rules as rules_
    import textwrap as tw_

    def graph_(flags, sz, tags=(mustflag.TAG,)):
        return {"nodes": [{"id": "group:rule:R.p", "attrs": {"level": "rule", "tags": list(tags), "reading": {"sizes": sz}}}],
                "verdicts": [{"node": "group:rule:R.p", "code": "TESTED-ONLY", "flags": flags}]}

    def block_(head, text):
        w = tw_.wrap(text, 96, break_on_hyphens=False) if text else []
        return (["Rule: p", f"  {'Verdict':<10}{head}", f"  {'Examples':<10}none"]
                + ([f"    {'sizes tried':<17}{w[0]}"] + [f"    {'':<17}{x}" for x in w[1:]] if w else []) + [f"    {'STRONGEST HELD':<17}x"])
    head_ = f"TESTED ONLY (...; NOT PROVED; {sizes.FLAG}: see `sizes`)"
    good = graph_([sizes.FLAG], a)
    check("E2, THE CONTROL OUTSIDE sizes.py: mustflag uses the tag and the flag of sizes.py; a tagged rule reported with the flag passes",
          mustflag.TAG == sizes.TAG and mustflag.FLAG == sizes.FLAG
          and mustflag.check(good, {"group:rule:R.p": block_(head_, a["text"])}) == [])
    plain = "TESTED ONLY (compiled, evaluated on generated inputs, no counterexample; NOT PROVED)"
    e_none = mustflag.check(graph_([], None), {"group:rule:R.p": block_(plain, "")})       # what removing the call site leaves
    e_flag = mustflag.check(graph_([], a), {"group:rule:R.p": block_(head_, a["text"])})
    e_row = mustflag.check(good, {"group:rule:R.p": block_(head_, "")})
    e_head = mustflag.check(good, {"group:rule:R.p": block_(plain, a["text"])})
    e_layer = mustflag.check(graph_([sizes.FLAG], {**a, "layers": a["layers"][:2]}), {"group:rule:R.p": block_(head_, a["text"])})
    check("E2, THE CONTROL OUTSIDE sizes.py: it FAILS when the flag was never applied (no flag, no sizes record, plain verdict line), "
          "and for each part alone: the verdict's flag, the Verdict line, the `sizes tried` row, a layer's size",
          len(e_none) == 4 and all("EXPECTED FLAG MISSING" in x for x in e_none)
          and len(e_flag) == 1 and "does not carry the flag" in e_flag[0]
          and len(e_row) == 1 and "sizes tried" in e_row[0] and len(e_head) == 1 and "Verdict line" in e_head[0]
          and len(e_layer) == 1 and "bounded check" in e_layer[0]
          and mustflag.check(graph_([sizes.FLAG], a), {}) != []
          and mustflag.check(graph_([], None, tags=("@expect-unproved",)), {}) == [])
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
          set(voc.coverage) <= set(vreport.all_ids(voc)) and "calls.accepted" in sh[0].used
          # (the first Rule line of features/ledger.feature, a claim about every call. It was `a[0]`, the first fixture by
          #  file name, until the counter's feature file, plan node X7, came before it in that order.)
          and "calls.every" in next(x for r, x in zip(fixtures, a) if r.feature.path == "features/ledger.feature").used)
    check("changing a printed coverage line voids the sign-off of its entry and of no other; so does changing a default it names",
          [i for i in d0 if d0[i] != d1[i]] == ["calls.accepted"] and [i for i in d0 if d0[i] != d2[i]] == ["calls.every", "calls.accepted", "calls.rejected"])
    # ---- plan node Q3: every accepted surface form is in the book. CONTROL: take one form (or entry) out of the book and
    #      the sentence written with it no longer compiles; with the book intact it does. The book is edited in memory.
    from . import attest, book as bookmod
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
        # plan node L2: the one form of each new piece
        ("'equals' (equals)", '    forms: ["{a:term<T>} equals {b:term<T>}"]\n', '    forms: []\n',
         "A transfer for which the sender of the transfer equals the receiver of the transfer is rejected and changes nothing"),
        ("'differs from' (equals, negated)", '    not_forms: ["{a:term<T>} differs from {b:term<T>}"]\n', "",
         "A transfer for which the sender of the transfer differs from the receiver of the transfer is always accepted"),
        ("'each of ... is afterwards at most' (each_at_most)", '    then_forms: ["each of {ns:nums} is afterwards at most {t:term<num>}"]\n', "    then_forms: []\n",
         "For a transfer, each of the ledger's balances is afterwards at most the maximum"),
        ("'with <tie>' (tied)", '    subject_forms: ["{op} with {t:tie}"]\n', "", "A deposit followed by a withdrawal with the same input always answers"),
        ("'the same input' (same_input)", '    forms: ["the same input"]\n', "    forms: []\n", "A deposit followed by a withdrawal with the same input always answers"),
    ]
    intact = vocab.load_project(ROOT, gl)
    res = [(what, compiles(intact, line), compiles(without(old, new), line)) for what, old, new, line in removals]
    check(f"Q3 control: each of {len(removals)} surface forms and texts taken out of the book makes its sentence fail to compile "
          "(and every one of the sentences compiles with the book intact)",
          all(a and not b for _, a, b in res))
    for what, a, b in res:
        if not a or b:
            print(f"       {what}: intact compiles={a}, removed compiles={b}")
    # ---- plan node L2: what a tie is said of, and what it changes
    def refused(line):
        f, _ = parse(f"Feature: Tie\n\n  Rule: {line}\n")
        r = vocab.Compiler(intact).rule(f.rules[0], None)
        return (r.status, r.message) if isinstance(r, vocab.Problem) else ("COMPILED", r.lean_def())
    untied = refused("A deposit followed by a withdrawal always answers")
    tied = refused("A deposit followed by a withdrawal with the same input always answers")
    no_input = refused("A batch followed by a computation of the total with the same input is always accepted")
    other_type = refused("A fund transfer followed by a lookup with the same input always answers")
    three = refused("A deposit followed by a withdrawal followed by a deposit with the same input always answers")
    check("L2: a sequence of two operations that give the same role name is refused without a tie and is ONE statement with it, "
          "about ONE input (`(W.deposit).andThen W.withdraw` tied by `Frames.sameInput`); a tie said of an operation that takes no input, "
          "of two operations with different input types, or of three operations is refused with the reason",
          untied[0] == "UNBOUND" and tied[0] == "COMPILED" and "(((W.deposit).andThen W.withdraw).tied Frames.sameInput)" in tied[1]
          and no_input[0] == "ILL-TYPED" and "takes no input" in no_input[1]
          and other_type[0] == "ILL-TYPED" and "takes a index" in other_type[1]
          and three[0] == "ILL-TYPED" and "exactly two operations" in three[1])
    # ---- L2 fix round: a narrowing word on a tied sequence. It reads as said of the FIRST call; `Op.andThen` would narrow on the LAST
    #      call's answer (clausebook/l2/NarrowedTie.lean shows an input where the two differ). Refused, never moved to the other call.
    nt_lines = ["An accepted deposit followed by a withdrawal with the same input never changes the wallet's balance",
                "A rejected transfer followed by a transfer with the same input never changes the ledger",
                "For an accepted transfer followed by a transfer with the same input, each of the ledger's balances is afterwards at most the maximum",
                "A rejected deposit followed by a withdrawal with the same input for which the amount equals zero always answers"]
    nt = [vocab.Compiler(intact).rule(parse(f"Feature: Tie\n\n  Rule: {l}\n")[0].rules[0], None) for l in nt_lines]
    nt_loose = [vocab.Compiler(intact, refuse_vacuous=False).rule(parse(f"Feature: Tie\n\n  Rule: {l}\n")[0].rules[0], None) for l in nt_lines]
    check(f"L2: a narrowing word on the subject of a TIED sequence is refused ({len(nt_lines)} lines, with the Q1 refusal on and off), code "
          "NARROWED-TIE: the message quotes the word, says it reads as said of the first call while the sequence's answer is the last call's, "
          "and no statement with `.successful` or `.rejected` on a tied sequence is emitted; the same sequences without the word still compile",
          all(isinstance(g, vocab.Problem) and g.status == "UNSUPPORTED" and g.code == vocab.NARROWED_TIE
              and "FIRST call" in g.message and "LAST call" in g.message and "for which <condition>" in g.hint for g in nt + nt_loose)
          and "'accepted'" in nt[0].message and "'rejected'" in nt[1].message
          and tied[0] == "COMPILED" and ".successful" not in tied[1] and ".rejected" not in tied[1]
          and refused("A transfer followed by a transfer with the same input never changes the ledger")[0] == "COMPILED")
    for l, g in zip(nt_lines, nt):
        if not (isinstance(g, vocab.Problem) and g.code == vocab.NARROWED_TIE):
            print(f"       not refused as NARROWED-TIE: {l}")
    eq_two = refused("A deposit for which the amount equals the amount always answers")
    check("L2: `equals` between two values that can each be read on two sorts (an amount is a number, and a value that may be absent) "
          "is refused, nothing is chosen (the refusal shown is the general UNBOUND of a subject whose condition has no one reading)",
          eq_two[0] == "UNBOUND")
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
    # not the other, and a PERSON's approval of the entry (`clausal attest <id> --act approved --as human:…`, an attestation record
    # stored beside its book) is on record for exactly that. Done in a copy of clausebook/, because attesting writes a file.
    # The signer `human:selftest-fixture` is a fixture identity in a directory that is deleted: nobody, and nothing of it is stored.
    FIX, FIX_SCOPE = "human:selftest-fixture", "self-test fixture in a temporary copy of clausebook/; no person signed anything"
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
                vreport.attest_entries(v, SEP, "approved", FIX, FIX_SCOPE)
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
    # ---- Q4 fix round: THE SAME WORDS IN TWO SYSTEMS. "transfer" names an operation of the wallet and one of the ledger, and
    #      since row 3 both say "it is accepted". A Rule line with no scenario beneath it is read in every system.
    def one(line, hint=None, c=None):
        return (c or comp).rule(rules_of([line])[0], hint)
    two = one("For a transfer, it is accepted")
    check("Q4 fix: \"For a transfer, it is accepted\" with no scenario beneath it is refused AMBIGUOUS; the refusal names both systems "
          "and how to say which; each way it names gives ONE statement (the system of a scenario; a noun only one system has)",
          isinstance(two, vocab.Problem) and two.status == "AMBIGUOUS" and "2 systems (ledger, wallet)" in two.hint and 'ledger: "fund transfer"' in two.hint
          and "wallet: the book has none" in two.hint
          and all(isinstance(one("For a transfer, it is accepted", d), vocab.Reading) for d in ("ledger", "wallet"))
          and one("For a transfer, it is accepted", "ledger").claims[0].lean != one("For a transfer, it is accepted", "wallet").claims[0].lean
          and isinstance(one("For a fund transfer, it is accepted"), vocab.Reading))
    # the clause a refusal says to write is ONE statement where the refused line stands, or the refusal does not say "write ... as"
    alone, under = one("For a transfer, the operation succeeds"), one("For a transfer, the operation succeeds", "wallet")
    dep = one("For a deposit, the operation succeeds")
    offered = lambda r: re.findall(r'write the clause as: "([^"]+)"', r.hint)
    check("Q4 fix: a retired form's refusal offers \"write the clause as\" only for a clause that is one statement where the line stands: "
          "\"For a transfer, the operation succeeds\" under a wallet scenario gets it; with no scenario it is told the rewritten clause reads "
          "in 2 systems; \"For a deposit, the operation succeeds\" gets it with no scenario",
          all(isinstance(r, vocab.Problem) and r.code == vocab.RETIRED for r in (alone, under, dep))
          and offered(alone) == [] and "reads in 2 systems (ledger, wallet)" in alone.hint and '"for a transfer, it is accepted"' in alone.hint
          and offered(under) == ["for a transfer, it is accepted"] and isinstance(one("For a transfer, it is accepted", "wallet"), vocab.Reading)
          and offered(dep) == ["for a deposit, it is accepted"] and isinstance(one("For a deposit, it is accepted"), vocab.Reading))
    lines_q4 = [was for _, was, _ in retired_cases] + ["For a transfer, the operation succeeds", "For a rejected transfer, the operation succeeds",
                                                      "For a deposit, the operation succeeds", "For a withdrawal, the operation succeeds"]
    off = [(was, d, w) for was in lines_q4 for d in (None, "ledger", "wallet") for w in offered(one(was, d)) if isinstance(one(was, d), vocab.Problem)]
    bad_off = [(was, d, w) for was, d, w in off if not isinstance(one(w[0].upper() + w[1:], d, loose_comp), vocab.Reading)]
    check(f"Q4 fix: every clause offered by \"write the clause as\" ({len(off)} offers: {len(lines_q4)} old Rule lines, each with no scenario, under "
          "a ledger scenario and under a wallet scenario) compiles to one statement in the place it was offered for", len(off) >= len(lines_q4) and not bad_off)
    for x in bad_off:
        print(f"       offered and not one statement: {x}")
    # the book check counts a skeleton shared by two systems when the systems share a subject noun, and only then
    wal_local = f"{vocab.BOOK_DIR}/local/wallet.yaml"
    tw_ = (ROOT / wal_local).read_text()
    assert tw_.count("    nouns: [transfer]\n") == 1
    apart_voc = vocab.load_project(ROOT, gl, overrides={wal_local: tw_.replace("    nouns: [transfer]\n", "    nouns: [payment]\n")})
    across = lambda v: sorted(x["skeleton"] for x in bookmod.lint(v, attest.Records())[0] if x["check"] == "4 shared skeleton across systems")
    check("Q4 fix (book check): a skeleton shared by pieces of two systems is a violation while the systems share a Rule subject noun "
          "(\"transfer\": \"it is accepted\" of the wallet and of the ledger are then live in one sentence); with the wallet's operation "
          "named by a noun of its own (in memory) none is reported and the line compiles",
          "it is accepted" in across(intact) and "transfer" in across(intact) and across(apart_voc) == []
          and isinstance(one("For a transfer, it is accepted", None, vocab.Compiler(apart_voc)), vocab.Reading))
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
    # ---- plan node C1: a list of books; attestation records stored per book, beside it (plan node W1: the records replace the
    #      sign-off files; the expectations of this check are the ones it had with sign-off records)
    import contextlib, io, shutil
    with tempfile.TemporaryDirectory() as d:
        shutil.copytree(ROOT / vocab.BOOK_DIR, Path(d) / vocab.BOOK_DIR)
        v = vocab.Vocabulary([(Path(d) / rel, rel) for _, rel in vocab.project_books(ROOT)], gl)
        with contextlib.redirect_stdout(io.StringIO()):
            vreport.attest_entries(v, "all", "approved", FIX, FIX_SCOPE)
        vd = vreport.lean_defs(v)
        per_book = {b.name: {r["subject"]["id"] for r in json.loads(b.attest_path.read_text())} for b in v.books}
        all_signed = vreport.reviewed_pieces(v, vd) == set(vreport.all_ids(v))
        core_b, led_b = v.books[0], v.book_of("l.bal_of")
        a_, b_ = json.loads(core_b.attest_path.read_text()), json.loads(led_b.attest_path.read_text())
        a_.append(next(r for r in b_ if r["subject"]["id"] == "l.bal_of"))
        b_ = [r for r in b_ if r["subject"]["id"] != "l.bal_of"]
        core_b.attest_path.write_text(json.dumps(a_))
        led_b.attest_path.write_text(json.dumps(b_))
        moved_recs = vreport.load_attestations(v, vd)
        moved = "l.bal_of" in vreport.reviewed_pieces(v, vd, moved_recs)
        moved_refused = [why for _, why, r in moved_recs.refused if r["subject"]["id"] == "l.bal_of"]          # frozen R11
        # ... and a sign-off file of the OLD format is neither read nor passed over: it stops the load
        (Path(d) / vocab.BOOK_DIR / "core.signoff.json").write_text('{"always": {"reviewer": "x", "date": "2026-11-12", "digest": "0"}}')
        try:
            vreport.load_attestations(v, vd)
            old_refused = False
        except FeatureError as e:
            old_refused = "old format" in str(e)
    check("attestation records are stored per book, beside it: each store holds exactly the entries its book defines; a record of an entry "
          "in another book's store is not an attestation of it (it is refused, with the reason); a sign-off file of the old format stops the load",
          all_signed and all(per_book[b.name] == {i for i, h in v.home.items() if h is b} for b in v.books) and not moved
          and len(moved_refused) == 1 and "is not an entry of core.yaml" in moved_refused[0][0] and old_refused)
    # ---- plan node W1: the records that must be refused (frozen as R1 to R14 in trust/FREEZE.md, before this code was written)
    dg_now = vreport.subject_digest(intact, defs, "always")
    good = attest.make("piece", "core.yaml", "always", dg_now, "reviewed", "model:selftest-fixture", "fixture", at="2026-11-12T02:10:00-05:00")
    def variant(**kw):
        r = json.loads(json.dumps(good))
        for k, val in kw.items():
            if val is KeyError:
                del r[k]
            else:
                r[k] = val
        return r
    r_dir = tempfile.TemporaryDirectory()
    shutil.copytree(ROOT / vocab.BOOK_DIR, Path(r_dir.name) / vocab.BOOK_DIR)
    r_voc = vocab.Vocabulary([(Path(r_dir.name) / rel, rel) for _, rel in vocab.project_books(ROOT)], gl)
    def store_of(*recs):
        """Sort records as if they were the store of core.yaml, against a copy of the real Clausebook."""
        r_voc.books[0].attest_path.write_text(json.dumps(list(recs)))
        return vreport.load_attestations(r_voc, defs)
    R = {
        "R1": (variant(signer={"kind": "person", "id": "model:claude-fable-5-2"}), "the kind is read from the id"),
        "R2": (variant(signer={"kind": "model", "id": "human:someone"}), "the kind is read from the id"),
        "R3": (variant(signer={"kind": "person", "id": "Will"}), "carries no kind"),
        "R4": (variant(act="refereed"), "unknown act"),
        "R6": (variant(signer={"kind": "tool", "id": "tool:clausal"}, act="approved"), "a tool may only"),
        "R7a": (variant(on_behalf=None), "unknown field"),
        "R7b": (variant(scope=KeyError), "missing field"),
        "R8a": (variant(at="yesterday"), "ISO 8601"),
        "R8b": (variant(at="2026-11-12T02:10:00"), "ISO 8601"),
        "R9a": (variant(on_behalf_of="Will Ackerly"), "`on_behalf_of` is null or an agent id"),
        "R9b": (variant(on_behalf_of="model:selftest-fixture"), "names the signer itself"),
        "R10": (variant(signature="AAAAB3NzaC1yc2E"), "signatures are not checked"),
        "R12": (variant(subject={"kind": "assumption", "book": "core.yaml", "id": "A.sig.unforgeable", "digest": dg_now}), "reserved and not built"),
        "R13": (variant(scope="  "), "may not be empty"),
        "R14": (variant(subject={"kind": "piece", "book": "core.yaml", "id": "always", "digest": {"alg": "md5", "value": dg_now["value"]}}), "unknown digest algorithm"),
    }
    got = {}
    for k, (rec, frag) in R.items():
        rs_ = store_of(rec)
        got[k] = (not rs_.valid and not rs_.void and len(rs_.refused) == 1 and any(frag in w for w in rs_.refused[0][1]))
    # R5: well-formed, of a digest the entry no longer has: VOID (counts for nothing), not refused
    r5 = store_of(variant(subject={"kind": "piece", "book": "core.yaml", "id": "always", "digest": {"alg": "sha256-text", "value": "0" * 64}}))
    got["R5"] = not r5.valid and len(r5.void) == 1 and not r5.refused and "has changed since" in r5.void[0][1]
    # R11: the wrong store, both ways
    r11a = store_of(variant(subject={"kind": "piece", "book": "ledger.yaml", "id": "l.bal_of", "digest": vreport.subject_digest(intact, defs, "l.bal_of")}))
    r11b = store_of(variant(subject={"kind": "piece", "book": "ledger.yaml", "id": "always", "digest": dg_now}))
    got["R11a"] = not r11a.valid and len(r11a.refused) == 1 and "is not an entry of core.yaml" in r11a.refused[0][1][0]
    got["R11b"] = not r11b.valid and len(r11b.refused) == 1 and "in the store of core.yaml" in r11b.refused[0][1][0]
    ok_good = store_of(good)
    r_dir.cleanup()
    check("W1, the records that must be refused (frozen R1 to R14, 18 records): kind person with a model's id and kind model with a person's id; "
          "a bare name; an unknown act; a tool that approves; a misspelt and a missing field; a time that is no ISO 8601 time with an offset; a "
          "delegation with no kind prefix and one that names the signer; a signature (not checked in this build); a record in another book's "
          "store, both ways; a reserved subject kind; an empty scope; an unknown digest algorithm: each is refused FOR THAT REASON and counts "
          "for nothing. A well-formed record of a digest the entry no longer has is VOID. The same record, well-formed and current, is valid",
          all(got.values()) and len(got) == 18 and len(ok_good.valid) == 1 and not ok_good.refused and not ok_good.void)
    if not all(got.values()):
        print(f"       not refused as expected: {sorted(k for k, x in got.items() if not x)}")
    # ---- W1, kind mismatch at the level of what a record COUNTS for (frozen K1 to K3)
    with tempfile.TemporaryDirectory() as d:
        shutil.copytree(ROOT / vocab.BOOK_DIR, Path(d) / vocab.BOOK_DIR)
        v = vocab.Vocabulary([(Path(d) / rel, rel) for _, rel in vocab.project_books(ROOT)], gl)
        vd = vreport.lean_defs(v)
        with contextlib.redirect_stdout(io.StringIO()):
            vreport.attest_entries(v, "all", "approved", "model:selftest-fixture", FIX_SCOPE)
        k1 = vreport.load_attestations(v, vd)
        k1_ok = len(k1.valid) == len(vreport.all_ids(v)) and vreport.reviewed_pieces(v, vd, k1) == set() \
            and all(attest.brief(r)["evidence_kind"] == "model-asserted" for r in k1.valid)
        with contextlib.redirect_stdout(io.StringIO()):
            vreport.attest_entries(v, "all", "approved", "model:selftest-fixture", FIX_SCOPE, on_behalf_of=FIX)
        k2 = vreport.load_attestations(v, vd)
        k2_ok = len(k2.valid) == len(vreport.all_ids(v)) and all(r["on_behalf_of"] == FIX and r["signer"]["kind"] == "model" for r in k2.valid) \
            and vreport.reviewed_pieces(v, vd, k2) == set()
        before = {b.name: b.attest_path.read_text() for b in v.books}
        try:
            vreport.attest_entries(v, "all", "approved", "Some Name", FIX_SCOPE)
            k3_ok = False
        except FeatureError as e:
            k3_ok = "is not a signer" in str(e) and before == {b.name: b.attest_path.read_text() for b in v.books}
        # a person's record is what makes an entry reviewed; an edit of the entry voids it (the digest is the one a sign-off covered)
        with contextlib.redirect_stdout(io.StringIO()):
            vreport.attest_entries(v, "always", "reviewed", FIX, FIX_SCOPE)
        person_ok = vreport.reviewed_pieces(v, vd) == {"always"}
        cb = v.books[0]
        keep_ = list(cb.lines)
        cb.lines = [l.replace('was: "always succeeds"', 'was: "always wins"') for l in cb.lines]
        after_edit = vreport.load_attestations(v, vd)
        cb.lines = keep_
        void_ok = "always" not in vreport.reviewed_pieces(v, vd, after_edit) and {r["subject"]["id"] for r, _ in after_edit.void} == {"always"}
    check("W1, a model's record is its own kind (frozen K1 to K3): with every entry attested `approved` by a model, every record is valid and "
          "model-asserted and NO entry is reviewed; the same on behalf of a person: delegation does not upgrade; `attest … --as \"Some Name\"` is "
          "refused and writes nothing. A person's record makes exactly its entry reviewed, and an edit of the entry voids the records of that "
          "entry and of no other (the model's too)", k1_ok and k2_ok and k3_ok and person_ok and void_ok)
    # ---- plan node W3: a trust policy; strict mode is a function of (graph, policy)
    from . import projects, trust
    pr = projects.load(ROOT)
    def pol(text):
        import yaml as _y
        return trust.Policy(_y.safe_load(text), "selftest policy")
    def refused(text, frag):
        try:
            pol(text)
            return False
        except FeatureError as e:
            return frag in str(e)
    P_HEAD = "version: 1\nproject: p\nroots:\n  - {id: owner, signer: 'human:selftest-fixture'}\n  - {id: m, signer: 'model:selftest-fixture'}\n  - {id: later, signer: null}\n"
    p_person = pol(P_HEAD + "requirements:\n  meaning: {subject: piece, act: [reviewed, approved], kinds: [person], roots: [owner]}\nstrict:\n  demands: [meaning]\n")
    p_model = pol(P_HEAD + "requirements:\n  meaning: {subject: piece, act: [reviewed, approved], kinds: [person, model]}\nstrict:\n  demands: [meaning]\n")
    p_obo = pol("version: 1\nproject: p\nroots:\n  - {id: m, signer: 'model:selftest-fixture', on_behalf_of: ['human:selftest-fixture']}\n"
                "requirements:\n  meaning: {subject: piece, act: reviewed, kinds: [model]}\nstrict:\n  demands: [meaning]\n")
    p_refuse = pol(P_HEAD + "requirements:\n  meaning: {subject: piece, act: approved, kinds: [person]}\nstrict:\n  demands: [meaning]\n  unsigned_person_record: refuse\n")
    q_ = lambda p: p.requirements["meaning"]
    rec_m = {"act": "reviewed", "kind": "model", "by": "model:selftest-fixture", "on_behalf_of": None}
    rec_mo = dict(rec_m, on_behalf_of="human:selftest-fixture")
    rec_h = {"act": "approved", "kind": "person", "by": "human:selftest-fixture", "on_behalf_of": None}
    rec_other = {"act": "approved", "kind": "person", "by": "human:someone-else", "on_behalf_of": None}
    check("W3, a policy admits a record by act, by the signer's kind and by root: a requirement for a person is not met by a model's record, "
          "with or without a delegation to that person; a policy that lists `model` is; a person who is no root is not admitted; a root that "
          "lists delegations admits its signer only with one of them; `unsigned_person_record: refuse` admits no person; an awaited root admits nothing",
          not p_person.admitted(q_(p_person), rec_m) and not p_person.admitted(q_(p_person), rec_mo) and p_person.admitted(q_(p_person), rec_h)
          and p_model.admitted(q_(p_model), rec_m) and not p_person.admitted(q_(p_person), rec_other)
          and not p_obo.admitted(q_(p_obo), rec_m) and p_obo.admitted(q_(p_obo), rec_mo)
          and not p_refuse.admitted(q_(p_refuse), rec_h) and p_person.awaited() == ["later"])
    check("W3, a malformed policy is refused at load: an unknown key (`min:`), a root with a bare name, a requirement for a person that names a "
          "model root, a demand that is no requirement, an `ssh_key` (not checked in this build), a requirement a tool could never meet, records "
          "said both to count and not to count",
          refused(P_HEAD + "requirements:\n  meaning: {subject: piece, act: approved, kinds: [person], min: 2}\n", "unknown key(s) ['min']")
          and refused("version: 1\nproject: p\nroots:\n  - {id: owner, signer: Will}\n", "is not a signer id")
          and refused(P_HEAD + "requirements:\n  meaning: {subject: piece, act: approved, kinds: [person], roots: [m]}\n", "that root could never meet it")
          and refused(P_HEAD + "strict:\n  demands: [meaning]\n", "is not a requirement of the policy")
          and refused("version: 1\nproject: p\nroots:\n  - {id: owner, signer: 'human:x', ssh_key: 'ssh-ed25519 AAAA'}\n", "`ssh_key` must be null")
          and refused(P_HEAD + "requirements:\n  meaning: {subject: piece, act: approved, kinds: [tool]}\n", "a tool can only")
          and refused(P_HEAD + "requirements:\n  meaning: {subject: piece, act: reviewed, kinds: [model]}\nrecorded_not_counted:\n  - {act: [reviewed], kinds: [model]}\n",
                      "it cannot be both"))
    # two policies over ONE graph: different strict outcomes, and the graph is not touched
    idn = {"alg": "sha256-text", "value": "1" * 64}
    def gnode(i, kind, attrs, file=None):
        return {"id": i, "kind": kind, "status": "proposed", "origin": {"by": "tool:selftest"}, "reviews": [], "implementations": [],
                "interface": {"language": "english", "text": i, "text_complete": True, "identity": idn, **({"source": {"file": file}} if file else {})}, "attrs": attrs}
    wf = pr.items[0].features[0]
    def tiny(atts):
        return {"schema": "rosette.refinement-graph/2.1", "generated_at": "x", "runs": [], "edges": [],
                "nodes": [gnode("piece:always", "phrase", {"clausebook_entry": "always", "subject_kind": "piece", "book": "core.yaml", "attestations": atts}),
                          gnode("group:rule:r", "group", {"reading": {"pieces": [{"id": "always"}]}}, wf)],
                "verdicts": [{"node": "group:rule:r", "outcome": "review", "code": "PROVED-FOR-ALL", "flags": [], "chain": [], "rests_on": [],
                              "unreviewed": ["piece:always"]}]}
    g_m = tiny([dict(rec_m, digest=idn)])
    g_text = json.dumps(g_m, sort_keys=True)
    ev_ = lambda g_, p: trust.evaluate(g_, pr, {x.name: p for x in pr})
    e_person, e_model, e_none = ev_(g_m, p_person), ev_(g_m, p_model), ev_(tiny([]), p_model)
    p_later = pol(P_HEAD + "requirements:\n  vouch: {subject: assumption, act: vouched, kinds: [person]}\nstrict:\n  demands: [vouch]\n")
    check("W3, two policies over one graph: with a model's record on the one piece a proved rule rests on, the policy that asks for a person "
          "fails the rule in strict mode and names the piece; the policy that lists `model` passes it and flags it MEANING-MODEL-ONLY; with no "
          "record both fail; the graph is byte-identical after both evaluations and its digest is the same in both results; a demand this build "
          "cannot evaluate (an assumption's vouch) fails closed; and the model's record is listed as recorded, not counted, under the first policy",
          e_person["strict_fail"] == 1 and e_person["verdicts"][0]["unmet"] == [{"requirement": "meaning", "subjects": ["piece:always"]}]
          and e_model["strict_fail"] == 0 and e_model["verdicts"][0]["flags"] == ["MEANING-MODEL-ONLY"] and e_none["strict_fail"] == 1
          and json.dumps(g_m, sort_keys=True) == g_text and e_person["graph_sha256"] == e_model["graph_sha256"]
          and ev_(g_m, p_later)["strict_fail"] == 1 and "cannot be evaluated" in ev_(g_m, p_later)["verdicts"][0]["unmet"][0]["why"]
          and e_person["projects"][pr.items[0].name]["recorded_not_counted"] == {"model reviewed": 1}
          and e_model["projects"][pr.items[0].name]["recorded_not_counted"] == {})
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
          core_only.kinds() == {"domain": 0, "modifier": 26, "frame": 26} and not core_only.ops and twice_ and typed_)
    # ---- plan node X7: the declared list of projects (projects.yaml) against the files; made-up lists, nothing is run
    import copy
    from . import projects
    pr = projects.load(ROOT)
    clean = projects.check(pr)

    def changed(fn):
        q = copy.deepcopy(pr)
        fn(q)
        return projects.check(q)
    first = pr.items[0]
    unlisted = changed(lambda q: q.items[0].features.pop())
    twice = changed(lambda q: q.items[1].features.append(q.items[0].features[0]))
    nocrate = changed(lambda q: q.items.append(projects.Project("ghost", "ghost", ["core.yaml"], ["features/ghost.feature"], "Generated.Ghost",
                                                               modules=["Ghost.Pieces"])))
    nobook = changed(lambda q: q.items[0].books.remove("ledger.yaml") if "ledger.yaml" in q.items[0].books else q.items[0].books.pop(0))
    check("projects.yaml agrees with the files; a feature file no project lists, a file listed twice, a project whose crate, feature "
          "file and Lean module do not exist, and a book whose `needs:` the project does not list are each reported",
          clean == [] and any("is listed by no project" in x and first.features[-1] in x for x in unlisted)
          and any("is listed by two projects" in x for x in twice)
          and any("ghost/Cargo.toml" in x for x in nocrate) and any("features/ghost.feature does not exist" in x for x in nocrate)
          and any("Lean module Ghost.Pieces has no file" in x for x in nocrate) and any("no [[lean_lib]] named Ghost" in x for x in nocrate)
          and any("needs the book" in x for x in nobook))
    # a sentence may use only the books ITS project lists: the wallet's sentences read an amount through the ledger pack
    st_voc = vocab.load_project(ROOT, gl)
    w_comp = vocab.Compiler(st_voc)
    wf, _ = parse("Feature: Wallet\n\n  Rule: A rejected withdrawal never changes the wallet's balance\n")
    w_rd = w_comp.rule(wf.rules[0], None)
    wal = next(x for x in pr if x.crate == "wallet")
    q = copy.deepcopy(pr)
    next(x for x in q if x.crate == "wallet").books = ["core.yaml"]
    own = projects.book_use(pr, st_voc, [(wal.features[0], w_rd)])
    stray = projects.book_use(q, st_voc, [(wal.features[0], w_rd)])
    check("a sentence that uses an entry of a book its project does not list is reported with the entry and the book; with the project's "
          "own list nothing is reported; the order the feature files are read in is the first file of each project, then the rest by name",
          isinstance(w_rd, vocab.Reading) and own == [] and any(i == "w.withdraw" and b == "clausebook/local/wallet.yaml" for _, _, i, b in stray)
          and pr.feature_paths()[:len(pr.items)] == [x.features[0] for x in pr]
          and sorted(pr.feature_paths()) == sorted(f for x in pr for f in x.features))
    # X7 fix round: an UNBOUND rule line lists the operations of ITS project's books, whatever other projects are declared
    uf, _ = parse("Feature: Unbound\n\n  Rule: A deposit earns interest\n")
    listed = lambda r: set(r.hint.split(": ", 1)[1].split(", ")) if isinstance(r, vocab.Problem) and r.status == "UNBOUND" else None
    nouns_of = lambda x: {n for o in st_voc.ops.values() if st_voc.home[o["id"]].rel in projects.books_of(pr, x.features[0]) for n in o["nouns"]}
    per = {x.name: listed(w_comp.rule(uf.rules[0], None, projects.books_of(pr, x.features[0]))) for x in pr}
    every = {n for o in st_voc.ops.values() for n in o["nouns"]}
    check("an UNBOUND rule line lists the operations of the books its own project lists (for each declared project: exactly those, "
          "so none that only another project has); read with no project named, it lists the operations of every system it was tried in",
          all(per[x.name] == nouns_of(x) for x in pr) and len({frozenset(v) for v in per.values()}) == len(pr.items)
          and listed(w_comp.rule(uf.rules[0], None)) == every)
    print(f"{'all checks passed' if not bad else str(len(bad)) + ' CHECKS FAILED'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
