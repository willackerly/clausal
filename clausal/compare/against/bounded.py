"""Bounded-check (Kani) rung results of out/graph.json against the same file at a git revision.
Usage: python3 compare/against/bounded.py [rev]. A difference is not a regression (the rungs run under a time limit and
answer differently under machine load); each one is listed."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def ladders(g: dict) -> dict:
    out = {}
    for n in g["nodes"]:
        l = ((n.get("attrs") or {}).get("reading") or {}).get("ladder")
        if l and "bounded" in l:
            b = l["bounded"]
            out[n["id"]] = (b.get("status"), tuple(b.get("verified", [])), tuple(b.get("timeout", [])), tuple(b.get("failed", [])))
    return out


def main(argv) -> int:
    rev = argv[0] if argv else "5e6cfa7"
    old = subprocess.run(["git", "show", f"{rev}:clausal/out/graph.json"], cwd=ROOT, check=True, capture_output=True, text=True).stdout
    a, b = ladders(json.loads(old)), ladders(json.loads((ROOT / "out" / "graph.json").read_text()))
    print(f"readings with a bounded check: at {rev} {len(a)}, this tree {len(b)}, same ids: {set(a) == set(b)}")
    d = [k for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)]
    print(f"bounded-check results that differ: {len(d)}")
    for k in d:
        print(f"   {k}\n      at {rev}: (status, verified, timeout, failed) = {a.get(k)}\n      this tree: {b.get(k)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
