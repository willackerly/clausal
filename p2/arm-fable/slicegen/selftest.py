"""Fast checks of the Rule parser, tag inheritance and the suite-adequacy bookkeeping. No Lean, no Rust, no out/.

    python3 -m slicegen.selftest

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
    print(f"{'all checks passed' if not bad else str(len(bad)) + ' CHECKS FAILED'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
