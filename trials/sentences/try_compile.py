#!/usr/bin/env python3
"""Compile candidate rule lines in the scratch copy of clausal/ and print status, hint and echo. No Lean is run.
   usage: python3 try_compile.py "A transfer ..." "..."      (or lines on stdin)"""
import sys, os, json, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
WORK = HERE / "work" / "clausal"
sys.path.insert(0, str(WORK))
os.chdir(WORK)
from clausal import newrules, vocab          # noqa: E402
from clausal.core import Problem             # noqa: E402

def compile_lines(lines, ids=None, name="try"):
    d = WORK / "v4"; d.mkdir(exist_ok=True)
    p = d / f"{name}.feature"
    out = [f"Feature: {name}", ""]
    for k, l in enumerate(lines):
        out += [f"  @id:{ids[k] if ids else 't%d' % k}", f"  Rule: {l}", ""]
    p.write_text("\n".join(out))
    voc, items = newrules.compile_files([str(p)])
    res = []
    for x in items:
        r = x["result"]
        if isinstance(r, Problem):
            res.append({"id": x["id"], "text": x["text"], "compiled": False, "status": r.status, "message": r.message, "hint": r.hint})
        else:
            res.append({"id": x["id"], "text": x["text"], "compiled": True, "status": "COMPILED", "echo": [list(e) for e in r.echo],
                        "lean": r.lean_def(), "pieces": r.used, "frames": [c.frame["id"] for c in r.claims]})
    return voc, items, res

if __name__ == "__main__":
    lines = sys.argv[1:] or [l.strip() for l in sys.stdin if l.strip()]
    _, _, res = compile_lines(lines)
    for r in res:
        print("==", r["status"], "|", r["text"])
        if r["compiled"]:
            for a, b in r["echo"]:
                print(f"   {a:<11}{b}")
            if os.environ.get("LEAN"): print(r["lean"])
        else:
            print("   ", r["message"][:600]); print("    hint:", (r["hint"] or "")[:600])
