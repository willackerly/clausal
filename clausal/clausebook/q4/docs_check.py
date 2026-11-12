#!/usr/bin/env python3
"""Sentences QUOTED IN DOCUMENTS that the book refuses since the first batch (plan node Q4, fix round).

A document that shows a Rule line shows it in backticks, in double quotes or after "Rule:". Every such text that begins like
a Rule line (a / an / for / every / any ...) is compiled as a Rule line with no scenario beneath it. Reported:
  RETIRED    refused as written with a retired form or shape; the clause the refusal says to write is printed
  AMBIGUOUS  one sentence, several statements
Texts that are no composition of the book at all (prose in quotes, sentences of another domain) are counted, not listed.

    python3 clausebook/q4/docs_check.py                    the root README.md and clausal/README.md
    python3 clausebook/q4/docs_check.py FILE ...           other files (paths from the repo root)
    python3 clausebook/q4/docs_check.py --json ...         {sentence: {where, status, code, hint | lean}}
Exit 1 if any quoted sentence is RETIRED.
"""
import json
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[2]))
from clausal import vocab                                   # noqa: E402
from clausal.core import FeatureError, load_glossary, parse_feature   # noqa: E402
from clausal.pipeline import ROOT                           # noqa: E402

REPO = ROOT.parent
DEFAULT = ["README.md", "clausal/README.md"]
START = re.compile(r"(A|An|For|Every|Any|a|an|for|every|any) \S+ \S+")


def quoted(path: Path) -> dict:
    out = {}
    for n, line in enumerate(path.read_text().split("\n"), 1):
        for c in re.findall(r"`([^`]+)`", line) + re.findall(r'"([^"]+)"', line) + re.findall(r"Rule:\s*(.+)$", line):
            c = c.strip()
            if START.match(c) and len(c.split()) >= 4:
                out.setdefault(c, []).append(n)
    return out


def main(argv) -> int:
    files = [a for a in argv if not a.startswith("--")] or DEFAULT
    comp = vocab.Compiler(vocab.load_project(ROOT, load_glossary(ROOT / "glossary.yaml", "glossary.yaml")))
    res, n_ret = {}, 0
    for f in files:
        for s, lines in quoted(REPO / f).items():
            where = [f"{f}:{n}" for n in lines]
            if s in res:
                res[s]["where"] += where
                continue
            try:
                with tempfile.TemporaryDirectory() as d:
                    p = Path(d) / "doc.feature"
                    p.write_text(f"Feature: D\n\n  Rule: {s}\n")
                    r = comp.rule(parse_feature(p, "doc.feature").rules[0], None)
            except FeatureError as e:
                res[s] = {"where": where, "status": "NOT A RULE LINE", "code": "", "hint": str(e)}
                continue
            if isinstance(r, vocab.Reading):
                res[s] = {"where": where, "status": "COMPILED", "code": "", "lean": r.lean_def().split(":=", 1)[1].strip()}
            else:
                res[s] = {"where": where, "status": r.status, "code": r.code or "", "hint": (r.hint or "").split("\n")[0], "message": r.message}
    if "--json" in argv:
        print(json.dumps(res, indent=1, ensure_ascii=False))
    count = {}
    for s, x in res.items():
        k = "RETIRED" if x["code"] == vocab.RETIRED else x["status"]
        count[k] = count.get(k, 0) + 1
        n_ret += k == "RETIRED"
        if "--json" not in argv and k in ("RETIRED", "AMBIGUOUS"):
            print(f"{k}  {', '.join(x['where'])}\n    {s}\n    {x['hint']}")
    if "--json" not in argv:
        print(f"docs check: {len(res)} quoted texts that begin like a Rule line in {', '.join(files)}: "
              + ", ".join(f"{v} {k}" for k, v in sorted(count.items())))
    return 1 if n_ret else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
