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
    readings = [x for x in a if isinstance(x, vocab.Reading)] + sh
    check(f"the coverage printed for each of the {len(readings)} compiled Rule lines (fixtures and the faulty shapes) is the coverage of its claims' Calls values",
          all(narrowing.coverage_mismatches(side_of(rd), lean_says(rd)) == [] for rd in readings))
    old = side_of(sh[0])
    old[sh[0].id]["printed"] = [["covers", ["every"]], ["answer"], ["weak", "accepted"]]       # what was printed before the fix
    check("THE CONTROL (Q2): the check reports the coverage that used to be printed for the first shape (this fails if the check is removed)",
          len(narrowing.coverage_mismatches(old, lean_says(sh[0]))) == 1)
    check("... and reports a claim whose emitted Lean carries another Calls value than the compiler took, and a claim Lean did not answer for",
          len(narrowing.coverage_mismatches(side_of(sh[0]), lean_says(sh[0], "every"))) == 2
          and len(narrowing.coverage_mismatches(side_of(sh[0]), {})) == 1)
    res = narrowing.collect({"facts": [], "certs": [], "open": [{"claim": "Rule.x#0", "tactic": "T.open_0", "lean": "P", "source": "x:1", "fixture": True}],
                             "calls": {}, "controls": []}, "NARROWING\tT.open_0\tproved\tpropext\n")
    check("a narrowed fixture claim the kernel proves for every `run` fails the run (the compiler should have refused it)",
          not res["ok"] and "SAYS NOTHING BUT WAS NOT REFUSED" in res["problems"][0])
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
