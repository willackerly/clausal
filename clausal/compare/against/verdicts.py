"""Verdict codes of out/graph.json against the same file at a git revision. Usage: python3 compare/against/verdicts.py [rev]
The codes are the ones observe() and observe_rules() of mutation/run_mutants.py read (scenario and rule-group verdicts),
and every other verdict of the graph (functions)."""
import collections
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def at(rev: str, path: str) -> str:
    return subprocess.run(["git", "show", f"{rev}:clausal/{path}"], cwd=ROOT, check=True, capture_output=True, text=True).stdout


def codes(g: dict) -> dict:
    return {v["node"]: v["code"] for v in g["verdicts"]}


def kind(node: str) -> str:
    p = node.split(":")
    return ":".join(p[:2]) if p[0] == "group" else p[0]


def main(argv) -> int:
    rev = argv[0] if argv else "5e6cfa7"
    # `rev` may also be the path of a stored graph.json (a baseline kept outside the repository)
    old = Path(rev).read_text() if Path(rev).is_file() else at(rev, "out/graph.json")
    a, b = codes(json.loads(old)), codes(json.loads((ROOT / "out" / "graph.json").read_text()))
    print(f"verdicts at {rev}: {len(a)} {dict(collections.Counter(kind(k) for k in a))} | this tree: {len(b)}")
    diff = [(k, a.get(k), b.get(k)) for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)]
    print(f"verdict codes that differ: {len(diff)} of {len(set(a) | set(b))}")
    for k, x, y in diff:
        print(f"   {k}: {x} -> {y}")
    return 1 if diff else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
