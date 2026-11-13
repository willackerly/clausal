"""Tests of the computed display (plan node Q6) against display_tests/expected.json, which was frozen first.

    python3 display_tests/run.py            the gates T1 to T6 (one Lean run, about a minute); writes display_tests/results.json
    python3 display_tests/run.py --unit     no Lean: the cell labels, the Calls value read off probes, and that a flipped
                                            table cell is reported by the comparison with the reading search

Run from clausal/. Needs lean/ built (a finished ./run.sh is enough). T1b uses out/rsearch.log and build/rsearch_grid.json
of the last ./run.sh if they are there, and says so if they are not.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from clausal import display, displaytext, rsearch, vocab            # noqa: E402
from clausal.core import Feature, Problem, Rule        # noqa: E402
from clausal.pipeline import OUT, ROOT, State          # noqa: E402


def unit() -> list:
    bad = []

    def check(name, ok):
        if not ok:
            bad.append(name)
    L = display.label
    check("label allowed", L({"n": 4, "true": 4, "eq": 0}) == "allowed")
    check("label forbidden", L({"n": 4, "true": 0, "eq": 4}) == "forbidden")
    check("label same", L({"n": 4, "true": 1, "eq": 4}) == "same")
    check("label mixed", L({"n": 4, "true": 1, "eq": 3}) == "mixed")
    check("label empty", L({"n": 0, "true": 0, "eq": 0}) == "empty")
    seen = display.calls_seen({"probe": {"accepted": [5, 5], "rejected": [5, 5], "silent": [3, 3]}}, False)
    check("calls every", seen["consistent_with"] == ["every"])
    seen = display.calls_seen({"probe": {"accepted": [5, 5], "rejected": [0, 5], "silent": [0, 3]}}, False)
    check("calls accepted", seen["consistent_with"] == ["accepted"])
    seen = display.calls_seen({"probe": {"accepted": [5, 5], "rejected": [0, 5], "silent": [3, 3]}}, False)
    check("calls: accepted answers only, yet silence breaks it, fits no Calls value", seen["consistent_with"] == [])
    seen = display.calls_seen({"probe": {"accepted": [5, 5], "rejected": [0, 0], "silent": [3, 3]}}, False)
    check("calls: an operation with no rejected answer is not settled beyond what was probed", seen["consistent_with"] == ["every"])
    check("point", display.point([("a", ["x", "y"]), ("b", ["1", "2", "3"])], 4) == {"a": "y", "b": "2"})
    check("distance", display.distance("a b c d", "a x c d") == 1 and display.distance("a b", "a new b") == 1)
    check("swap", display.swap_form("A t never loses acceptance when V", "never loses acceptance when {v:variation}",
                                    "gives the same answer when {v:variation}") == "A t gives the same answer when V")
    # T1b control: three points (accepted, rejected, accepted), every pair in scope and related; the reading search says the
    # statement is false exactly at (accepted, rejected). A right table passes; one with the cell flipped is reported.
    kinds = "010"
    bits = "".join("11" + ("0" if (kinds[i], kinds[j]) == ("0", "1") else "1") for i in range(3) for j in range(3))
    r = {"bits": bits, "width": 3, "layout": [["scope", 0], ["rel", 0], ["at", 0]]}
    cells = {a + b: {"label": "forbidden" if a + b == "ar" else "allowed"} for a in "arn" for b in "arn"}
    d = {"claims": [{"runs": 2, "table": {"cells": cells}, "point_kinds": kinds, "checks": {}}]}
    check("T1b: a right table is consistent with the reading search", display.against_search(copy.deepcopy(d), r, {}) == [])
    d2 = copy.deepcopy(d)
    d2["claims"][0]["table"]["cells"]["ar"]["label"] = "allowed"
    check("T1b: a flipped cell (forbidden shown as allowed) is reported", len(display.against_search(d2, r, {})) == 2)      # pairs (0, 1) and (2, 1)
    d3 = copy.deepcopy(d)
    d3["claims"][0]["table"]["cells"]["aa"]["label"] = "forbidden"
    check("T1b: a flipped cell (allowed shown as forbidden) is reported", len(display.against_search(d3, r, {})) == 4)      # the four accepted/accepted pairs
    # T7e (no Lean): a sequence whose call-by-call run does not give the sequence's outcome as the last call's is reported,
    # so is a sequence with no call-by-call run, so is a sequence line on a claim about one call; a right one is not
    base = {"unit": "u", "runs": 1, "calls": "every", "covers": {"agrees_with_calls_value": True},
            "checks": {"table_or_reading_against_Claim_check_on_grid": {"n": 3, "agree": 3}, "definition_against_executable_reading": None}}
    q = {"calls": 2, "computed": True, "points": 3, "outcome_is_the_last_calls": 3, "first_difference": None, "in_scope": 3, "by_steps": {"00": 3}}
    P = lambda ops, seq: display.problems({"r": {"claims": [{**base, "operation": ops, "sequence": seq}]}})
    check("T7e: a right sequence line is no fault", P(["a", "b"], q) == [])
    check("T7e: an outcome that is not the last call's is reported", any("NOT the last call's" in x for x in P(["a", "b"], {**q, "outcome_is_the_last_calls": 2, "first_difference": 1})))
    check("T7e: a sequence with no call-by-call run is reported", len(P(["a", "b"], None)) == 1 and len(P(["a", "b"], {"calls": 2, "computed": False})) == 1)
    check("T7e: a sequence line on one call is reported", len(P(["a"], q)) == 1)
    check("T7e: such a line is printed NOT SETTLED", displaytext.say_sequence({**q, "outcome_is_the_last_calls": 2}, ["an a", "a b"]).startswith("NOT SETTLED"))
    check("say_steps", displaytext.say_steps(["an a", "a b"], [0, 1], "is ") == "an a is accepted, then a b is rejected"
          and displaytext.say_steps(["an a", "a b"], [2]) == "an a gives no answer; a b is not reached")
    # the module never reads the echo, the book's flat: text or its coverage: texts
    for mod in ("display.py", "displaytext.py"):
        src = (HERE.parent / "clausal" / mod).read_text().split('"""', 2)[2]
        for word in (".echo", "echo_rule", '["flat"]', "voc.covers", "accepted_echo", "coverage"):
            check(f"{mod} does not touch `{word}`", word not in src)
    # ... and the compiler does not read the display
    for mod in ("vocab.py", "core.py", "narrowing.py", "emit.py", "oblig.py", "links.py", "trees.py", "evgen.py"):
        check(f"{mod} does not import the display", "display" not in (HERE.parent / "clausal" / mod).read_text())
    return bad


def tampered(voc, strict) -> dict:
    """NEGATIVE CONTROL of T1 and T6: the display script of a rule the model breaks, with the run-substituted executable
    reading (`chk`) replaced by `true`. The table is then all `allowed`; it must be reported as differing from the compiler's
    executable reading on the grid (at the pairs where the model breaks the rule) and from the frame's definition."""
    import re
    f = Feature(path="<display_tests>", name="display_tests", slug="display_tests")
    rd = strict.rule(Rule(feature=f, name="A transfer never loses acceptance when the amount is the same or larger", line=1, tags=["@id:tampered"]), "ledger")
    text, side = display.script(voc, [{"reading": rd, "sentence": "tampered", "neighbours": []}])
    text, n = re.subn(r"^  chk := fun run st inp st2 inp2 => .*$", "  chk := fun run st inp st2 inp2 => true", text, flags=re.M)
    work = ROOT / "build" / "display" / "tests-tampered"
    work.mkdir(parents=True, exist_ok=True)
    (work / "Display.lean").write_text(text)
    log = display.run_lean(work / "Display.lean", work / "display.log")
    probs = display.problems(display.summarise(side, display.parse(log, side)))
    return {"lines_replaced": n, "problems": probs,
            "grid_difference_reported": any("differs from the compiler's executable reading" in p for p in probs),
            "definition_difference_reported": any("definition and its executable reading differ" in p for p in probs)}


def tampered_sequence(voc, off) -> dict:
    """NEGATIVE CONTROL of T7a (gate T7e): the display script of the control 'A rejected batch followed by a computation of
    the total is accepted exactly when ...' with the LAST call's notion of acceptance in the call-by-call run replaced by
    `true`. The steps then say the last call is always accepted; the run must report that the sequence's outcome is not
    the last call's."""
    import re
    f = Feature(path="<display_tests>", name="display_tests", slug="display_tests")
    rd = off.rule(Rule(feature=f, name="A rejected batch followed by a computation of the total is accepted exactly when the total of the ledger's balances "
                                       "is at most the maximum", line=1, tags=["@id:tampered_sequence"]), "ledger")
    text, side = display.script(voc, [{"reading": rd, "sentence": "tampered sequence", "neighbours": []}])
    text, n = re.subn(r"^(\s*\| some \(r1, st1\) => #\[if )decide \(.*\) (then 0 else 1\]\)?)$", r"\1true \2", text, flags=re.M)
    work = ROOT / "build" / "display" / "tests-tampered-sequence"
    work.mkdir(parents=True, exist_ok=True)
    (work / "Display.lean").write_text(text)
    log = display.run_lean(work / "Display.lean", work / "display.log")
    disp = display.summarise(side, display.parse(log, side))
    probs = display.problems(disp)
    q = [c.get("sequence") for d in disp.values() for c in d["claims"]]
    return {"lines_replaced": n, "problems": probs, "sequence": q, "reported": any("NOT the last call's" in p for p in probs),
            "printed_not_settled": any("sequence  NOT SETTLED" in l for d in disp.values() for l in displaytext.render(d))}


def main(argv) -> int:
    bad = unit()
    for b in bad:
        print(f"UNIT FAILED: {b}")
    if "--unit" in argv:
        print(f"unit: {'ok' if not bad else str(len(bad)) + ' failed'}")
        return 1 if bad else 0
    exp = json.loads((HERE / "expected.json").read_text())
    st = State()
    voc = st.voc
    strict, off = vocab.Compiler(voc), vocab.Compiler(voc, refuse_vacuous=False)
    items, group = display.fixture_items(st), {}
    for it in items:
        group[it["reading"].id] = "fixture"
    fixture_rules = [(r, rd) for r, rd in st.rules]
    controls = {"says-nothing": [], "covers": [], "refused-on": 0}
    for c in st.narrowing_controls():
        r = c["rule"]
        tag = next((t.split(":")[0][1:] for t in r.tags if t.startswith(("@says-nothing", "@covers"))), None)
        if tag == "says-nothing":
            controls["refused-on"] += isinstance(c["on"], Problem) and c["on"].status == "SAYS-NOTHING"
            rd = c["off"]
        elif tag == "covers":
            rd = c["on"]
        else:
            continue
        if isinstance(rd, Problem):
            controls[tag].append((r.id, None))
            continue
        controls[tag].append((r.id, rd.id))
        group[rd.id] = tag
        items.append({"reading": rd, "sentence": r.name.strip(), "neighbours": []})
    f = Feature(path="<display_tests>", name="display_tests", slug="display_tests")
    tables = []
    for k, t in enumerate(exp["tables"]):
        got = [x for x in (strict.rule(Rule(feature=f, name=t["sentence"], line=k + 1, tags=[f"@id:table{k}_{d}"]), d)
                           for d in sorted({o["domain"] for o in voc.ops.values()})) if isinstance(x, vocab.Reading)]
        tables.append((t, got[0].id if len(got) == 1 else None))
        if len(got) == 1:
            group[got[0].id] = "table"
            items.append({"reading": got[0], "sentence": t["sentence"], "neighbours": []})
    disp, side, log = display.compute(voc, items, ROOT / "build" / "display" / "tests")
    rs = None
    if (OUT / "rsearch.log").exists() and (ROOT / "build" / "rsearch_grid.json").exists():
        rs = rsearch.parse((OUT / "rsearch.log").read_text(), json.loads((ROOT / "build" / "rsearch_grid.json").read_text()))
    probs = display.problems(disp, rs, side)
    claims = [(group[rid], c) for rid, d in disp.items() for c in d["claims"]]
    okc = [(g, c) for g, c in claims if "error" not in c]
    G = lambda c: c["checks"]["table_or_reading_against_Claim_check_on_grid"] or {"n": 0, "agree": 0}
    E = lambda c: c["checks"]["definition_against_executable_reading"] or {"n": 0, "agree": 0}
    two = [(g, c) for g, c in okc if c["runs"] == 2]
    res = {"gates": {}, "reported": {}, "problems": probs, "log": str(log)}

    def gate(name, ok, **numbers):
        res["gates"][name] = {"pass": bool(ok), **numbers}
    # as frozen: every pair / point in scope agrees; at least one pair evaluated per TWO-call claim (a one-call claim with no
    # grid input in scope is reported under `one_call_claims_with_nothing_in_scope`, and its display says so)
    gate("T1", all(G(c)["agree"] == G(c)["n"] for _, c in okc) and all(c.get("table") and G(c)["n"] > 0 for _, c in two),
         one_call_claims_with_nothing_in_scope=[c["unit"] for _, c in okc if c["runs"] == 1 and G(c)["n"] == 0],
         two_call_claims=len(two), two_call_pairs=sum(G(c)["n"] for _, c in two), two_call_pairs_agree=sum(G(c)["agree"] for _, c in two),
         one_call_claims=len(okc) - len(two), one_call_points=sum(G(c)["n"] for _, c in okc if c["runs"] == 1),
         one_call_points_agree=sum(G(c)["agree"] for _, c in okc if c["runs"] == 1))
    srch = [c["checks"]["cells_against_the_reading_search"] for _, c in two if "cells_against_the_reading_search" in c["checks"]]
    gate("T1b", rs is not None and srch and all(x["inconsistent"] == 0 for x in srch) and not bad,
         reading_search_present=rs is not None, tables_compared=len(srch), pairs=sum(x["pairs"] for x in srch),
         inconsistent=sum(x["inconsistent"] for x in srch), unit_control_of_a_flipped_cell="reported" if not bad else "FAILED")
    sn = [(rid, disp.get(did)) for rid, did in controls["says-nothing"]]
    sn_bad = [rid for rid, d in sn if d is None or any("error" in c or display.has_forbidden(c) or c.get("forbidden") for c in d["claims"])]
    gate("T2", len(sn) == 12 and controls["refused-on"] == 12 and not sn_bad, lines=len(sn), refused_with_the_refusal_on=controls["refused-on"],
         showing_a_forbidden_row_or_case=sn_bad)
    cv = [(rid, disp.get(did)) for rid, did in controls["covers"]]
    cv_bad = [rid for rid, d in cv if d is None or any("error" in c or not display.has_forbidden(c) for c in d["claims"])]
    # The freeze says "(9 lines)". controls/narrowing.feature has 8 @covers lines: the 9 was a miscount, made before the code
    # existed. expected.json is not edited; the gate is "each @covers line", and the count is reported beside it.
    gate("T2b", len(cv) > 0 and not cv_bad, lines=len(cv), lines_according_to_the_freeze=9, count_as_frozen=len(cv) == 9,
         showing_no_forbidden_row_or_case=cv_bad)
    tb, t3 = [], []
    for t, did in tables:
        d = disp.get(did) if did else None
        c = d["claims"][0] if d and len(d["claims"]) == 1 and "error" not in d["claims"][0] else None
        got = {k: v["label"] for k, v in c["table"]["cells"].items()} if c and c.get("table") else None
        tb.append({"name": t["name"], "sentence": t["sentence"], "pass": got == t["cells"], "got": got,
                   "differs": sorted(k for k in t["cells"] if not got or got.get(k) != t["cells"][k])})
        if t.get("must_have_no_answer_row"):
            t3.append(bool(got) and all(got.get(k) == t["cells"][k] and got.get(k) != "empty" for k in ("na", "nr", "nn")))
    gate("T3", all(x["pass"] for x in tb) and all(t3), tables=len(tb), tables_as_frozen=sum(x["pass"] for x in tb),
         with_no_answer_row=sum(t3), no_answer_row_required=len(t3), detail=tb)
    want = [rd.id for _, rd in fixture_rules if isinstance(rd, vocab.Reading)]
    missing = [i for i in want if i not in disp] + [rid for rid, did in controls["says-nothing"] + controls["covers"] if did is None]
    errors = [c["unit"] for _, c in claims if "error" in c]
    gate("T4", not missing and not errors, fixture_rule_lines=len(fixture_rules), fixture_rule_lines_compiled=len(want),
         control_lines=len(sn) + len(cv), claims=len(claims), errors=errors, missing=missing)
    mism = [c["unit"] for _, c in okc if not c["covers"]["agrees_with_calls_value"]]
    unsettled = [c["unit"] for _, c in okc if len(c["covers"]["seen"]["consistent_with"]) != 1]
    gate("T5", not mism, claims=len(okc), mismatches=mism, by_calls_value={k: sum(c["calls"] == k for _, c in okc) for k in ("every", "accepted", "rejected")},
         consistent_with_more_than_one_value_because_a_kind_of_answer_was_not_sampled=unsettled)
    gate("T6", all(E(c)["agree"] == E(c)["n"] for _, c in okc), evaluations=sum(E(c)["n"] for _, c in okc), agree=sum(E(c)["agree"] for _, c in okc))
    # ---- the sequence line (expected_sequence.json, frozen in commit 239f53a before its code)
    seqc = [(g, c) for g, c in okc if len(c["operation"]) > 1]
    Q = lambda c: c.get("sequence") or {}
    gate("T7a", len(seqc) >= 8 and all(Q(c).get("computed") and Q(c)["points"] > 0 and Q(c)["outcome_is_the_last_calls"] == Q(c)["points"] for _, c in seqc),
         sequence_claims=len(seqc), by_group={k: sum(g == k for g, _ in seqc) for k in sorted({g for g, _ in seqc})},
         generated_calls=sum(Q(c).get("points", 0) for _, c in seqc), outcome_is_the_last_calls=sum(Q(c).get("outcome_is_the_last_calls", 0) for _, c in seqc))
    before = HERE / "before_sequence.json"
    old = json.loads(before.read_text()) if before.exists() else None
    changed, compared = [], 0
    if old is not None:
        for rid, d in disp.items():
            if rid in old and all(len(c["operation"]) == 1 for c in d["claims"]):
                compared += 1
                if old[rid] != displaytext.render(d):
                    changed.append(rid)
    lines = {rid: displaytext.render(d) for rid, d in disp.items()}
    has_line = lambda rid, k: sum(l.startswith("  sequence  ") for l in lines[rid])
    wrong = [c["unit"] for g, c in okc if (len(c["operation"]) > 1) != bool(c.get("sequence")) or (c.get("sequence") and Q(c)["calls"] != len(c["operation"]))]
    wrong += [rid for rid, d in disp.items() if has_line(rid, 0) != sum(len(c["operation"]) > 1 and "error" not in c for c in d["claims"])]
    gate("T7b", not wrong and old is not None and compared > 0 and not changed, exceptions=wrong, one_call_displays_compared_with_the_print_before_the_fix=compared,
         changed=changed, print_before_the_fix="display_tests/before_sequence.json" if old is not None else "ABSENT")
    t7c, t7d = {}, {}
    for name, steps_frozen in (("q2_sequence_narrowed_rejected", [0, 1]), ("q2_sequence_narrowed_accepted", [0, 0])):
        did = next((d for r, d in controls["covers"] if r.endswith(name) or r == name), None)
        d = disp.get(did) if did else None
        c = d["claims"][0] if d and len(d["claims"]) == 1 and "error" not in d["claims"][0] else None
        text = " ".join(" ".join(l.split()) for l in lines[did]) if c else ""
        al = c["allowed"] if c else None
        t7c[name] = {"says_LAST_call": "LAST call of the sequence, a computation of the total." in text, "names_the_earlier_call": "an earlier call (a batch)" in text,
                     "allowed_case_is_the_models": bool(al) and al["how"] == "model", "allowed_case_steps": al.get("steps") if al else None,
                     "allowed_case_steps_as_frozen": bool(al) and al.get("steps") == [steps_frozen],
                     "steps_printed": "(in the sequence: " + displaytext.say_steps(c["nouns"], steps_frozen, "is ") + ")" in text if c else False}
        t7d[name] = Q(c).get("by_steps") if c else None
    gate("T7c", all(all(v for k, v in x.items() if k != "allowed_case_steps") for x in t7c.values()), **t7c)
    rj = t7d["q2_sequence_narrowed_rejected"] or {}
    gate("T7d", rj.get("01", 0) > 0, rejected_control_calls_in_scope_by_steps=rj, accepted_control_calls_in_scope_by_steps=t7d["q2_sequence_narrowed_accepted"],
         with_the_batch_accepted_and_the_sequence_rejected=rj.get("01", 0))
    res["negative_control_sequence"] = tampered_sequence(voc, off)
    ns = res["negative_control_sequence"]
    gate("T7e", ns["lines_replaced"] == 1 and ns["reported"] and ns["printed_not_settled"] and not bad, lines_replaced=ns["lines_replaced"],
         reported=ns["reported"], printed_not_settled=ns["printed_not_settled"], unit_tests="ok" if not bad else "FAILED")
    res["reported"]["sequence_claims"] = {c["unit"]: {"group": g, "by_steps": Q(c).get("by_steps")} for g, c in seqc}
    res["displays_of_the_two_controls"] = {n: lines[d] for n, d in ((r, d) for r, d in controls["covers"] if "q2_sequence_narrowed" in r) if d}
    res["negative_control"] = tampered(voc, strict)
    nc_ok = res["negative_control"]["lines_replaced"] == 1 and res["negative_control"]["grid_difference_reported"] and res["negative_control"]["definition_difference_reported"]
    fx = [c for g, c in okc if g == "fixture"]
    res["reported"] = {**res["reported"], "fixture_claims": len(fx), "fixture_claims_without_a_forbidden_case": [c["unit"] for c in fx if not display.has_forbidden(c)],
                       "fixture_rule_lines_with_neighbours_tried": sum(any("neighbours_tried" in c for c in disp[i]["claims"]) for i in want),
                       "fixture_rule_lines_with_a_neighbour_allowing_the_forbidden_case": sum(any(c.get("neighbour") for c in disp[i]["claims"]) for i in want),
                       "forbidden_case_shown_is_the_models_own": sum(bool(c.get("forbidden")) and c["forbidden"]["how"] == "model" for c in fx),
                       "forbidden_case_shown_is_substituted": sum(bool(c.get("forbidden")) and c["forbidden"]["how"] == "substituted" for c in fx),
                       "forbidden_case_shown_is_silence": sum(bool(c.get("forbidden")) and c["forbidden"]["how"] == "silent" for c in fx)}
    res["pass"] = all(g["pass"] for g in res["gates"].values()) and not probs and not bad and nc_ok
    (HERE / "results.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    for name, g in res["gates"].items():
        print(f"{name}: {'pass' if g['pass'] else 'FAIL'}  " + json.dumps({k: v for k, v in g.items() if k not in ('pass', 'detail')}, ensure_ascii=False))
    print("reported: " + json.dumps(res["reported"], ensure_ascii=False))
    print(f"negative control (a tampered table): {'reported, as it must be' if nc_ok else 'NOT REPORTED'}  " + json.dumps(res["negative_control"], ensure_ascii=False)[:600])
    for p in probs:
        print(f"PROBLEM: {p}")
    print("ALL GATES PASS" if res["pass"] else "A GATE FAILED")
    return 0 if res["pass"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
