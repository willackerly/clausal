"""clausal mustflag: the standing check that a sentence tagged @must-flag-larger-inputs is REPORTED with the flag
LARGER INPUTS NOT EXAMINED (plan node E2, fix round).

This check is on purpose not part of clausal/sizes.py and imports nothing from it. sizes.py raises the flag; if that code
is switched off, or the loop in report.cmd_report that calls it is removed, a guard that lives in the same function goes
with it (that was the defect: the probe then read as a clean TESTED ONLY and the run was green). So this module looks
only at what the run WROTE, after every flag has been applied:

  out/graph.json (as read back from disk)   the node's tags, its verdict record, and attrs.reading.sizes
  the rule blocks rendered from that file   the text a reader sees (rules.render), for a tagged Rule line

and the tag and the flag are spelled out here as literals (the self-test checks that they are the strings sizes.py uses).
A tagged sentence passes only if all of this holds:

  1. its verdict record in the graph carries the flag;
  2. attrs.reading.sizes exists, says flag = true, its text starts with the flag, and it names the grid search, the
     generated property test and the generated bounded check, each with a text (a size, or "not run");
  3. (a Rule line) the rendered block shows the flag on its Verdict line and has a `sizes tried` row with that text.

What it cannot do: notice that the tag itself was taken off the fixture, or that the call to this check was removed.
Controls c39, c40 and c41 (mutation/run_mutants.py) remove the flag in three different places and expect this check, or
the guard in sizes.apply, to fail the run.
"""
from __future__ import annotations

TAG = "@must-flag-larger-inputs"
FLAG = "LARGER INPUTS NOT EXAMINED"
LAYERS = ("grid search", "property test", "bounded check")


def _norm(text: str) -> str:
    return " ".join(text.split())


def _rows(lines: list, label: str, indent: int) -> list:
    """The rows of a rendered block that start with `label`, each with its continuation lines (indented by `indent`)."""
    out = []
    for k, l in enumerate(lines):
        if l.startswith(label):
            j = k + 1
            while j < len(lines) and lines[j].startswith(" " * indent) and lines[j].strip():
                j += 1
            out.append(_norm(" ".join(x.strip() for x in lines[k:j])))
    return out


def tagged(graph: dict) -> list:
    """The nodes of the graph (Rule lines and scenarios) whose sentence carries TAG."""
    return [n for n in graph.get("nodes", []) if TAG in ((n.get("attrs") or {}).get("tags") or [])]


def check(graph: dict, rendered: dict) -> list:
    """Errors, one per thing missing. `graph`: out/graph.json as read from disk. `rendered`: {node id: the lines of the
    rule block rendered from that graph} for the Rule lines."""
    errs = []
    records = {}
    for r in graph.get("verdicts", []):
        records.setdefault(r.get("node"), []).append(r)
    for n in tagged(graph):
        nid = n["id"]
        what = f"EXPECTED FLAG MISSING ({nid}, tagged {TAG})"
        recs = records.get(nid, [])
        if not recs:
            errs.append(f"{what}: the graph has no verdict for it")
        elif not all(FLAG in (r.get("flags") or []) for r in recs):
            errs.append(f"{what}: its verdict {recs[0].get('code')} does not carry the flag {FLAG}; it would read as checked "
                        "at every size, and no layer examined an input larger than the sizes it tried")
        sz = ((n.get("attrs") or {}).get("reading") or {}).get("sizes")
        text = (sz or {}).get("text") or ""
        if not sz or sz.get("flag") is not True or not text.startswith(FLAG):
            errs.append(f"{what}: the graph does not record the sizes tried for it with the flag raised (attrs.reading.sizes)")
        else:
            got = {l.get("layer"): l for l in sz.get("layers") or []}
            for layer in LAYERS:
                if not (got.get(layer) or {}).get("text"):
                    errs.append(f"{what}: the sizes recorded for it do not say what the {layer} tried")
        if (n.get("attrs") or {}).get("level") == "rule":
            lines = rendered.get(nid)
            verdict_rows, size_rows = _rows(lines or [], "  Verdict", 12), _rows(lines or [], "    sizes tried", 21)
            if not lines:
                errs.append(f"{what}: no rule block was rendered for it")
            else:
                if not any(FLAG in v for v in verdict_rows):
                    errs.append(f"{what}: the Verdict line of its rule block does not say {FLAG}")
                if not text or not any(_norm(text) in r for r in size_rows):
                    errs.append(f"{what}: its rule block has no `sizes tried` row with the largest size each layer tried")
    return errs
