"""clausal duplicates: sentences that MEAN the same thing (plan node Q5; readability synthesis, section 3).

    python3 -m clausal duplicates [file.feature ...] [--json]

With no file: every Rule line and scenario of features/. Two sentences are reported together when their compiled Lean
statements are the same text AFTER THE OPERATION'S ACCEPTANCE IS UNFOLDED: `(<operation>).accepted ans`, which is what
"is always accepted" and "never loses acceptance" emit, is replaced by `<its accepted function> ans`, which is what the
class word of the same operation emits ("it is accepted": `L.said ans`). The function is the `accepted:` of the
operation's entry in the book. So "A batch applied as a whole is always accepted" and "For a batch applied as a whole,
it is accepted" fall together, although their Lean differs (readability critique 2.3), and two Rule lines that differ
only in the noun of one operation ("fund transfer", "transfer") fall together as well.

WHAT THIS IS NOT. The key is text. It finds sentences whose statements are equal up to that one unfolding; it does not
find two statements that are equivalent for a deeper reason (`every X is not P` and `no X is P` were such a pair; the
first is now refused). And the unfolding is read off the book, not asked of Lean: that `(L.apply).accepted` IS `L.said`
is true by definition in lean/Ledger/Pieces.lean, and nothing here checks it. Informational: it never changes a verdict.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from . import vocab
from .core import load_glossary, parse_feature
from .pipeline import ROOT


def normal_form(voc, rd) -> str:
    """The statement of a reading with its name dropped and the acceptance of each of its operations unfolded."""
    body = rd.lean_def().split(":=", 1)[1]
    for o in sorted(voc.ops.values(), key=lambda o: -len(o["lean"])):
        for base in (f"({o['lean']})", o["lean"]):
            body = body.replace(f"({base}).accepted ans", f"{o['accepted']} ans").replace(f"{base}.accepted ans", f"{o['accepted']} ans")
    return re.sub(r"\s+", " ", body).strip()


def compiled(voc, paths) -> list:
    """[(id, source, text, Reading)] for every scenario and Rule line of the files that compiles."""
    comp = vocab.Compiler(voc)
    out = []
    for p in paths:
        p = Path(p).resolve()
        rel = str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else p.name
        f = parse_feature(p, rel)
        rds = {sc.id: comp.scenario(sc) for sc in f.scenarios}
        for sc in f.scenarios:
            if isinstance(rds[sc.id], vocab.Reading):
                out.append((sc.id, f"{rel}:{sc.line}", f"Scenario: {sc.name}", rds[sc.id]))
        for r in f.rules:
            hint = next((rds[sc.id].info["ops"][0]["domain"] for sc in r.scenarios if isinstance(rds.get(sc.id), vocab.Reading)), None)
            rd = comp.rule(r, hint)
            if isinstance(rd, vocab.Reading):
                out.append((r.id, f"{rel}:{r.line}", f"Rule: {r.name}", rd))
    return out


def groups(voc, items) -> list:
    """[{normal_form, same_lean, members: [{id, source, text, lean}]}]: every set of two or more sentences with one normal form."""
    by = {}
    for id_, source, text, rd in items:
        by.setdefault(normal_form(voc, rd), []).append({"id": id_, "source": source, "text": text, "lean": rd.lean_def().split(":=", 1)[1].strip()})
    return [{"normal_form": k, "same_lean": len({m["lean"] for m in ms}) == 1, "members": ms} for k, ms in by.items() if len(ms) > 1]


def main(argv) -> int:
    gl = load_glossary(ROOT / "glossary.yaml", "glossary.yaml")
    voc = vocab.load_project(ROOT, gl)
    paths = [a for a in argv if not a.startswith("--")] or sorted((ROOT / "features").glob("*.feature"))
    items = compiled(voc, paths)
    gs = groups(voc, items)
    if "--json" in argv:
        print(json.dumps(gs, indent=1, ensure_ascii=False))
        return 0
    print(f"duplicates: {len(items)} compiled sentences; {len(gs)} groups of sentences with the same statement once the operation's acceptance is unfolded")
    for g in gs:
        print(f"  the same statement ({'the same Lean text' if g['same_lean'] else 'DIFFERENT Lean text, equal after unfolding'}):")
        for m in g["members"]:
            print(f"    {m['source']}  {m['text']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
