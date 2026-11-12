#!/usr/bin/env python3
"""Tests of `clausal separate` (plan node L3).

    python3 separate_tests/run.py --unit         the comparison logic on hand-made bit strings (no Lean, no Rust)
    python3 separate_tests/run.py [case ...]     the cases of cases.json, each checked against its frozen expectation;
                                                 writes separate_tests/results.json

Run from clausal/. The cases need a built lean/ (./run.sh, or lake build) and cargo; run them under tools/sem.sh.
Exit status 0 iff every check passed.
"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from clausal import separate          # noqa: E402


def unit() -> list:
    """compare() on synthetic search results. Layout: one unit, one claim -> bits per point = scope, claim."""
    bad = []

    def check(name, cond):
        if not cond:
            bad.append(name)
    lay = [["scope", 0], ["at", 0]]
    side = {"vars": [("x", ["0", "1", "2"]), ("y", ["a", "b"])]}

    def r(points):          # points: list of (scope, holds) in grid order, y fastest
        return {"bits": "".join(("1" if s else "0") + ("1" if h else "0") for s, h in points), "width": 2, "layout": lay}
    all_true = r([(True, True)] * 6)
    one_false = r([(True, True)] * 3 + [(True, False)] + [(True, True)] * 2)          # false at x=1, y=b
    got = separate.compare(all_true, one_false, side, side)
    check("counts", got["counts"] == {"points": 6, "both_hold": 5, "both_fail": 0, "a_only": 1, "b_only": 0})
    check("first a_only", got["first"]["a_only"]["values"] == {"x": "1", "y": "b"} and got["first"]["b_only"] is None)
    check("bounds", got["bounds"]["points"] == 6 and [v["name"] for v in got["bounds"]["variables"]] == ["x", "y"])
    got = separate.compare(one_false, all_true, side, side)
    check("direction", got["counts"]["b_only"] == 1 and got["first"]["b_only"]["values"] == {"x": "1", "y": "b"})
    got = separate.compare(all_true, all_true, side, side)
    check("no difference", got["counts"]["a_only"] == 0 and got["counts"]["b_only"] == 0 and got["first"] == {"a_only": None, "b_only": None})
    # out of scope counts as holding (the bit of the claim is 1 there); the scope is reported
    out_scope = r([(False, True)] + [(True, True)] * 5)
    first_false = r([(True, False)] + [(True, True)] * 5)
    got = separate.compare(out_scope, first_false, side, side)
    check("scope", got["first"]["a_only"]["a"]["in_scope"] == [False] and got["first"]["a_only"]["a"]["holds"] is True)
    # a reading over a smaller grid (x only) against one over (x, y): compared on the larger grid by projection
    small_side = {"vars": [("x", ["0", "1", "2"])]}
    small = {"bits": "11" + "10" + "11", "width": 2, "layout": lay}                   # false at x=1
    got = separate.compare(small, all_true, small_side, side)
    check("projection", got["counts"] == {"points": 6, "both_hold": 4, "both_fail": 0, "a_only": 0, "b_only": 2}
          and got["first"]["b_only"]["values"] == {"x": "1", "y": "a"} and got["first"]["b_only"]["a"]["values"] == {"x": "1"})
    # different variables or different sample values: no common grid
    check("no common grid (names)", separate.compare(all_true, all_true, side, {"vars": [("x", ["0", "1", "2"]), ("z", ["a", "b"])]}) is None)
    check("no common grid (values)", separate.compare(all_true, all_true, side, {"vars": [("x", ["0", "1", "3"]), ("y", ["a", "b"])]}) is None)
    # a truncated search is an error, never "none found"
    try:
        separate.compare({"bits": "1111", "width": 2, "layout": lay}, all_true, side, side)
        check("truncated search raises", False)
    except ValueError:
        pass
    # the kernel answer: a theorem resting on sorryAx is not a proof; an absent line is not a proof
    log = ("'Separate.eq0_rfl' depends on axioms: [propext, sorryAx]\n'Separate.eq0_pointwise' depends on axioms: [propext,\n Quot.sound]\n"
           "'Separate.eq1_rfl' does not depend on any axioms\n'Separate.eq2_pointwise' depends on axioms: [sorryAx]\n")
    check("proved", [separate.proved(log, k) for k in range(4)] == ["pointwise", "rfl", None, None])
    return bad


def longest(values) -> int:
    return max((0 if v.strip() == "[]" else v.count(",") + 1) for v in values)


def check_case(case: dict, res: dict) -> list:
    e, bad = case["expect"], []

    def need(name, cond, got=None):
        if not cond:
            bad.append(f"{name}: got {got!r}" if got is not None else name)
    for label, doms in e.get("compiles_in", {}).items():
        got = sorted(c["domain"] for c in res["candidates"] if c["label"].startswith(label + "/") and c["compiled"])
        need(f"compiles_in {label}", got == sorted(doms), got)
    if "comparisons" in e:
        need("comparisons", len(res["comparisons"]) == e["comparisons"], len(res["comparisons"]))
    cmp_ = res["comparisons"][0] if res["comparisons"] else None
    if "verdict" in e:
        need("one comparison", len(res["comparisons"]) == 1, len(res["comparisons"]))
        need("verdict", cmp_ is not None and cmp_["verdict"] == e["verdict"], cmp_ and cmp_["verdict"])
    if cmp_ is None:
        cmp_ = {"separating": [], "counts": None, "bounds": None, "own_inputs": None}
    seps = cmp_["separating"]
    if e.get("no_separating"):
        need("no separating input", not seps, seps)
    if "holds_only" in e:
        need("holds_only", bool(seps) and all(p["holds"].startswith(e["holds_only"] + "/") for p in seps), [p["holds"] for p in seps])
    if "first_point" in e:
        need("first_point", bool(seps) and seps[0]["values"] == e["first_point"], seps[0]["values"] if seps else None)
    if "same_value" in e:
        a, b = e["same_value"]
        need("same_value", bool(seps) and seps[0]["values"][a] == seps[0]["values"][b], seps[0]["values"] if seps else None)
    if "rust_call" in e:
        want = e["rust_call"]
        for side in ("a", "b"):
            rv = seps[0][side].get("rust") if seps else None
            ok = bool(rv and rv.get("replayed") and rv["calls"])
            need(f"rust replayed ({side})", ok, rv)
            if ok:
                c = rv["calls"][0]
                need(f"rust accepted ({side})", c["accepted"] == want["accepted"], c["accepted"])
                need(f"rust answer ({side})", c["answer"] == want["answer"], c["answer"])
                need(f"rust state unchanged ({side})", (c["after"] == c["before"]) == want["state_unchanged"], [c["before"], c["after"]])
    views = [p[s].get("rust") for p in seps for s in ("a", "b")]
    for own in (cmp_["own_inputs"] or {}).values():
        views += [v for v in (own.get("rust") or {}).values()]
    if e.get("rust_agrees"):
        need("rust replayed something", bool(views))
        need("rust agrees with lean", all(v and v.get("replayed") and v["agrees_with_lean"] for v in views), views)
    if e.get("bounds_stated"):
        b = cmp_["bounds"]
        need("bounds stated", bool(b and b["points"] > 0 and b["variables"] and all(v["values"] for v in b["variables"])), b)
    for var, n in e.get("longest_list_on_grid", {}).items():
        vals = next((v["values"] for v in (cmp_["bounds"] or {"variables": []})["variables"] if v["name"] == var), None)
        need(f"longest {var} on the grid", vals is not None and longest(vals) == n, vals and longest(vals))
    if "cross_system_noun" in e:
        xs = res.get("cross_system", [])
        need("cross-system noun", bool(xs) and all(e["cross_system_noun"] in x["nouns"] for x in xs), xs)
    if "cross_system_refused_in" in e:
        xs = res.get("cross_system", [])
        got = sorted(r["domain"] for x in xs for r in x["refused_in"])
        need("cross-system refused in", got == sorted(e["cross_system_refused_in"]), got)
    for label, pts in e.get("own_inputs", {}).items():
        own = (cmp_["own_inputs"] or {}).get(label)
        for what, vals in pts.items():
            need(f"{label} {what}", own is not None and own[what] == vals, own and own[what])
    if e.get("own_inputs_replayed"):
        own = cmp_["own_inputs"] or {}
        need("an input for each reading", len(own) == 2 and all(o["holds_at"] or o["fails_at"] for o in own.values()), own)
        need("each replayed on Rust", all(v.get("replayed") for o in own.values() for v in (o.get("rust") or {}).values())
             and all(o.get("rust") for o in own.values()), own)
    return bad


def main(argv) -> int:
    if "--unit" in argv:
        bad = unit()
        print("separate unit tests: " + ("all passed" if not bad else "FAILED: " + "; ".join(bad)))
        return 1 if bad else 0
    cases = json.loads((HERE / "cases.json").read_text())["cases"]
    only = [a for a in argv if not a.startswith("--")]
    out, failed = [], 0
    for case in cases:
        if only and case["id"] not in only:
            continue
        t = time.time()
        res = separate.separate(case["sentences"])
        bad = check_case(case, res)
        failed += bool(bad)
        verdicts = [c["verdict"] for c in res["comparisons"]]
        print(f"{'ok  ' if not bad else 'FAIL'} {case['id']:<28} {', '.join(verdicts) or '(no comparison)':<22} {time.time() - t:5.1f} s"
              + ("" if not bad else "\n       " + "\n       ".join(bad)))
        out.append({"id": case["id"], "passed": not bad, "failed_checks": bad, "verdicts": verdicts, "seconds": round(time.time() - t, 1),
                    "result": res})
    if not only:
        text = json.dumps(out, indent=1, ensure_ascii=False).replace(str(HERE.parent), "clausal")      # no machine paths in the record
        (HERE / "results.json").write_text(text + "\n")
    print(f"{len(out) - failed} of {len(out)} cases as expected")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
