"""clausal sizes: flag a statement whose subject can be LARGER than every size any layer tried (plan node E2).

A sentence about "a batch" or "the ledger" speaks of a collection of any length. The layers below a proof try only some
lengths: the grid search uses the sample lists of glossary.yaml, the generated property test draws collections of at most
`size` items, and the generated bounded check (Kani) is run at a fixed ladder of sizes. A rule that is false only at a
larger input passes all of them (FINDINGS.md, "A false rule can pass every layer").

So, for every compiled reading that has a collection which no Given fixes, and whose verdict is neither a kernel-checked
proof for all inputs nor a falsifying input, the verdict carries the flag LARGER INPUTS NOT EXAMINED with the largest size
each layer tried in THIS run. Nothing here changes a verdict code.

Where each number comes from (none is written down here):
  which collections   build/evidence_gen.json `collections`, written by evgen.write_all from Plan.uses(): the variables of
                      the reading's composition tree that are a list of balances or a batch and that no Given fixes
  grid search         build/rsearch_grid.json: the longest literal of each such variable on the reading's grid
  property test       out/evidence.json `size` (passed to the runner as --size) and the reading's property-test row
  bounded check       out/evidence.json: the rungs of the ladder that were run for this reading and what Kani answered

A reading with no entry in build/evidence_gen.json (no typed reading could be generated for it) is flagged too, saying the
sizes its subject can take could not be determined: the flag fails towards saying less was checked, not more.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FLAG = "LARGER INPUTS NOT EXAMINED"
# On a Rule (or scenario): the run fails unless the verdict carries FLAG. (Not `@expect-...`: core.Scenario.expect reads
# every tag with that prefix as an expected verdict code.)
TAG = "@must-flag-larger-inputs"
# Verdicts that the sizes tried do not limit: a kernel-checked proof covers every size; a falsifying input settles it.
SETTLED = ("PROVED-FOR-ALL", "PROVED-INSTANCE", "REFUTED", "COUNTEREXAMPLE", "VACUOUS")
# collection type of the trees -> (what one item is, how the sentence's subject is described)
KINDS = {"balances": ("accounts", "a ledger with any number of accounts"), "batch": ("transfers", "a batch of any number of transfers")}


def load_gen(root: Path = ROOT) -> dict:
    p = root / "build" / "evidence_gen.json"
    return json.loads(p.read_text()).get("readings", {}) if p.exists() else {}


def load_grid(root: Path = ROOT) -> dict:
    p = root / "build" / "rsearch_grid.json"
    return json.loads(p.read_text()) if p.exists() else {}


def _items(text: str) -> int:
    inner = text.strip()[1:-1].strip()
    return len(inner.split(", ")) if inner else 0


def unbounded(gen_reading: dict | None) -> list | None:
    """The collection types of the reading that no Given fixes (in KINDS order); None when that is not known."""
    c = (gen_reading or {}).get("collections")
    if c is None:
        return None
    return [k for k in KINDS if c.get(k)]


def grid_tried(side: dict | None, kinds: list) -> dict | None:
    """{items word: longest literal of that type on the reading's grid}; None when the reading was not put on a grid."""
    if not side or "skipped" in side or "vars" not in side:
        return None
    types = (side.get("rust") or {}).get("types") or {}
    out = {}
    for name, vals in side["vars"]:
        t = types.get(name)
        if t in kinds:
            w = KINDS[t][0]
            out[w] = max([out.get(w, 0)] + [_items(v) for v in vals if v.strip().startswith("[")])
    return out or None


def _and(bits: list) -> str:
    return " and ".join(bits)


def assess(status: str, gen_reading: dict | None, side: dict | None, ev: dict | None, rid: str) -> dict:
    """What the layers tried for one reading, and whether its verdict must carry FLAG.
    {flag, unbounded: [type] | None, layers: [{layer, ran, ...}], text}"""
    kinds = unbounded(gen_reading)
    out = {"flag": False, "unbounded": kinds, "layers": [], "text": ""}
    if kinds == []:
        return out          # the sentence speaks of no collection of open length: nothing can be larger than what was tried
    open_ = status not in SETTLED
    known = kinds if kinds is not None else list(KINDS)
    layers = []
    # 1 grid search
    g = grid_tried(side, known)
    layers.append({"layer": "grid search", "ran": g is not None, "largest": g,
                   "text": "grid search (Lean model, and the compiled Rust when it ran): " +
                           ("not run" if g is None else "at most " + _and([f"{n} {w}" for w, n in g.items()]))})
    # 2 generated property test
    r = ((ev or {}).get("readings") or {}).get(rid)
    p = (r or {}).get("property") or {}
    if p.get("status") in ("pass", "fail", "hang", "abort", "mismatch"):
        size = ev.get("size")
        layers.append({"layer": "property test", "ran": True, "largest": {"items": size}, "cases": p.get("cases"),
                       "text": f"generated property test: collections of at most {size} items each, and only the "
                               f"{p.get('cases')} inputs it drew (a sample, not every input of those sizes)"})
    else:
        layers.append({"layer": "property test", "ran": False, "largest": None, "text": "generated property test: not run"})
    # 3 generated bounded check
    b = (r or {}).get("bounded") or {}
    if b.get("ran") and b.get("rungs"):
        rungs = b["rungs"]
        top = {w: max([x[w] or 0 for x in rungs]) for w in ("accounts", "transfers") if any(x[w] is not None for x in rungs)}
        ver = [x["label"] for x in rungs if x["status"] == "verified"]
        no = [x["label"] for x in rungs if x["status"] != "verified"]
        layers.append({"layer": "bounded check", "ran": True, "largest": top, "answered": ver, "no_answer": no,
                       "text": "generated bounded check (Kani): no rung of the ladder has more than " + _and([f"{n} {w}" for w, n in top.items()])
                               + "; it holds at " + ("; at ".join(ver) if ver else "NO rung")
                               + ("; NOT verified at " + "; at ".join(no) if no else "")})
    else:
        layers.append({"layer": "bounded check", "ran": False, "largest": None,
                       "text": "generated bounded check (Kani): not run" + (" (--quick skips it)" if (ev or {}).get("quick") else "")})
    out["layers"] = layers
    subject = (_and([KINDS[k][1] for k in kinds]) if kinds is not None else
               "collections whose possible sizes could not be determined (no typed reading was generated for it)")
    tried = "Largest size tried, per layer: " + ". ".join(l["text"][0].upper() + l["text"][1:] for l in layers) + ". "
    if open_:
        out["flag"] = True
        out["text"] = (f"{FLAG}: the statement speaks of {subject}. " + tried +
                       "No input larger than these was examined by any layer, and there is no kernel-checked proof for all "
                       "inputs: the verdict says NOTHING about larger inputs, and the statement may be false there.")
    else:
        out["text"] = (f"the statement speaks of {subject}. " + tried +
                       ("The proof covers every size." if status.startswith("PROVED") else "A falsifying input settles it at any size."))
    return out


def apply(v, status: str, rid: str, tags, gen: dict, grid: dict, ev: dict | None) -> None:
    """Put the assessment on a verdict object (report.Verdict or vreport.RuleVerdict): `sizes`, the flag, one report
    line; and fail the verdict when its sentence is tagged TAG and the flag is not there."""
    a = assess(status, gen.get(rid), grid.get(rid), ev, rid)
    v.sizes = a
    if a["flag"]:
        v.flags.append(FLAG)
        v.lines.append("sizes            " + a["text"])
    if TAG in tags and FLAG not in v.flags:
        v.fatal.append(f"EXPECTED FLAG MISSING: the sentence is tagged {TAG}, but its verdict does not carry the flag {FLAG}")
        v.as_expected = False


def summary(flagged: list, total: int, what: str) -> str:
    """One line for the end of the report. `flagged`: [(name, assessment)]."""
    if not flagged:
        return f"sizes: none of the {total} {what} is flagged {FLAG}"
    return (f"sizes: {len(flagged)} of {total} {what} flagged {FLAG}: the subject can be larger than every size the grid search, "
            f"the generated property test and the generated bounded check tried, and there is no proof for all inputs ("
            + "; ".join(n for n, _ in flagged) + ")")
