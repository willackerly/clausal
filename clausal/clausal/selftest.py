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
    print(f"{'all checks passed' if not bad else str(len(bad)) + ' CHECKS FAILED'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
