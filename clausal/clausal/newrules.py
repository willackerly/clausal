"""clausal newrules: NEW SENTENCES, compiled from the Clausebook alone.

    python3 -m clausal compile heldout/new_rules.feature [more.feature ...]

For feature files that are NOT part of the regression set (features/): every `Rule:` line and every scenario
is compiled through the composable Clausebook only. There is no old whole-phrase binding for such a sentence,
so there is no flat statement, no hand-written proof and no cucumber step; what a new sentence gets is

  compiled     the one composition of existing pieces, its Lean statement (type-checked by Lean), its echo
  searched     the reading evaluated on a grid of generated inputs through the frames' definitions and their
               executable readings (lean/Run/NewReadings.lean): a counterexample, or none on the grid
  or refused   UNBOUND / ILL-TYPED / AMBIGUOUS, with file:line and the nearest forms

Writes lean/Run/NewReadings.lean (the script), and after it has been run (`--collect`), out/new_sentences.json,
which `clausal report` prints as the section "New sentences". Informational: it never changes the exit
status of run.sh, except that a disagreement between a frame's definition and its executable reading is an error.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from . import rsearch, vocab
from .core import FeatureError, Problem, load_glossary, parse_feature
from .pipeline import LEAN, OUT, ROOT


def compile_files(paths) -> tuple:
    gl = load_glossary(ROOT / "glossary.yaml", "glossary.yaml")
    voc = vocab.load_project(ROOT, gl)
    comp = vocab.Compiler(voc)
    items = []          # [{kind, id, source, text, feature, expect, result: Reading | Problem}]
    for p in paths:
        rel = str(Path(p).resolve().relative_to(ROOT))
        f = parse_feature(ROOT / rel, rel)
        seen = set()
        for r in f.rules:
            sc_rds = {sc.id: comp.scenario(sc) for sc in r.scenarios}
            hint = next((x.info["ops"][0]["domain"] for x in sc_rds.values() if isinstance(x, vocab.Reading)), None)
            exp = "REFUTED" if "@expect-refuted" in r.tags else "UNBOUND" if "@expect-unbound" in r.tags else None
            items.append({"kind": "rule", "id": r.id, "source": f"{rel}:{r.line}", "text": f"Rule: {r.name}", "feature": f.name,
                          "expect": exp, "result": comp.rule(r, hint)})
            for sc in r.scenarios:
                seen.add(sc.id)
                items.append({"kind": "scenario", "id": sc.id, "source": f"{rel}:{sc.line}", "text": sc.text, "feature": f.name,
                              "expect": sc.expect, "result": sc_rds[sc.id]})
        for sc in f.scenarios:
            if sc.id not in seen:
                items.append({"kind": "scenario", "id": sc.id, "source": f"{rel}:{sc.line}", "text": sc.text, "feature": f.name,
                              "expect": sc.expect, "result": comp.scenario(sc)})
    return voc, items


def script(voc, items) -> tuple:
    rds = [(x["result"], None) for x in items if isinstance(x["result"], vocab.Reading)]
    text, side = rsearch.search_file(voc, rds)
    defs = "\n".join(f"/-- {rd.source}\n" + "\n".join("    " + l for l in rd.text.splitlines()) + " -/\n" + rd.lean_def() + "\n" for rd, _ in rds)
    text = text.replace("import Wallet.Readings\n", "".join(f"import {i}\n" for i in voc.raw["lean_imports"]))
    marker = "def rbits"
    text = text.replace(marker, defs + "\n" + marker, 1)
    text = text.replace("Run/ReadingSearch.lean", "Run/NewReadings.lean")
    return text, side


def cmd_compile(argv) -> int:
    collect = "--collect" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print(__doc__)
        return 2
    try:
        voc, items = compile_files(paths)
    except FeatureError as e:
        print(f"clausal compile: {e}", file=sys.stderr)
        return 1
    text, side = script(voc, items)
    (LEAN / "Run" / "NewReadings.lean").write_text(text)
    log = OUT / "new_sentences.log"
    rs = rsearch.parse(log.read_text(), side) if collect and log.exists() else {}
    out = []
    for x in items:
        r = x["result"]
        rec = {k: x[k] for k in ("kind", "id", "source", "text", "feature", "expect")}
        if isinstance(r, Problem):
            rec.update({"compiled": False, "status": r.status, "message": r.message, "hint": r.hint})
        else:
            s = rs.get(r.id)
            rec.update({"compiled": True, "lean": r.lean_def(), "echo": [list(e) for e in r.echo], "pieces": r.used,
                        "regular": r.regular, "frames": [c.frame["id"] for c in r.claims], "search": s,
                        "status": ("NOT-RUN" if not collect else "LEAN-REJECTED" if s is None else "NOT-SEARCHED" if "skipped" in s
                                   else "COUNTEREXAMPLE" if s.get("bad") else "NO-COUNTEREXAMPLE")})
        out.append(rec)
    if collect:
        OUT.mkdir(exist_ok=True)
        (OUT / "new_sentences.json").write_text(json.dumps({"files": paths, "items": out}, indent=1, ensure_ascii=False))
    for rec in out:
        print(f"{rec['status']:<18}{rec['kind']:<9}{rec['text'].splitlines()[0][:110]}   ({rec['source']})")
        if not rec["compiled"]:
            print(f"                  {rec['message']}")
    n = sum(r["compiled"] for r in out)
    print(f"{n} of {len(out)} sentences compiled from existing pieces" + ("" if collect else "; run lean/Run/NewReadings.lean, then --collect"))
    return 0
