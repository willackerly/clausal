"""Every compilation of the fixtures (scenarios and Rule lines), by this tree's compiler and by the compiler at a git
revision: Lean statement, status, defaults, echo. Usage: python3 compare/against/readings.py [rev]
No Lean and no run: the compiler is Python. The revision's compiler, book and fixtures are unpacked with `git archive`
into a temporary directory and run there."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
NEEDS = ["clausal", "clausebook", "clausebook.yaml", "vocabulary.yaml", "glossary.yaml", "features", "lean/translation.json"]

DUMP = r'''
import json, sys
sys.path.insert(0, ".")
from clausal import vocab
from clausal.pipeline import State
st = State()
out = {}
for rd, _ in st.compiled:
    out[rd.id] = {"status": "COMPILED", "lean": rd.lean_def(), "echo": [list(e) for e in rd.echo], "defaults": rd.defaults}
for r, rd in st.rules:
    if not isinstance(rd, vocab.Reading):
        out[r.id] = {"status": rd.status, "message": rd.message}
for sc, _ in st.results:
    rd = st.readings[sc.id]
    if not isinstance(rd, vocab.Reading):
        out[sc.id] = {"status": rd.status, "message": rd.message}
json.dump(out, sys.stdout, ensure_ascii=False)
'''


def dump(root: Path) -> dict:
    return json.loads(subprocess.run([sys.executable, "-c", DUMP], cwd=root, check=True, capture_output=True, text=True).stdout)


def main(argv) -> int:
    rev = argv[0] if argv else "5e6cfa7"
    have = subprocess.run(["git", "ls-tree", "--name-only", rev, "clausal/"], cwd=ROOT.parent, check=True, capture_output=True, text=True).stdout.split()
    paths = [f"clausal/{n}" for n in NEEDS if f"clausal/{n.split('/')[0]}" in have]
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "archive", rev] + paths, cwd=ROOT.parent, check=True, capture_output=True).stdout
        subprocess.run(["tar", "-x", "-C", d], input=tar, check=True)
        old = dump(Path(d) / "clausal")
    new = dump(ROOT)
    ids = sorted(set(old) | set(new))
    hard = [i for i in ids if i not in old or i not in new
            or any(old[i].get(k) != new[i].get(k) for k in ("status", "lean", "defaults", "message"))]
    echo = [i for i in ids if i in old and i in new and old[i].get("echo") != new[i].get("echo")]
    comp = sum(1 for i in ids if new.get(i, {}).get("status") == "COMPILED")
    print(f"compilations: at {rev} {len(old)}, this tree {len(new)} ({comp} compiled, {len(new) - comp} refused)")
    print(f"Lean statement, status, defaults or refusal message differ: {len(hard)}")
    for i in hard:
        print(f"   {i}")
        for k in ("status", "lean", "defaults", "message"):
            if old.get(i, {}).get(k) != new.get(i, {}).get(k):
                print(f"      {k} at {rev}: {old.get(i, {}).get(k)}\n      {k} now: {new.get(i, {}).get(k)}")
    texts = lambda e: [t for _, t in e]
    text = [i for i in echo if texts(old[i]["echo"]) != texts(new[i]["echo"])]
    print(f"echo differs: {len(echo)}; of these only in the NAME of a slot (same lines, same order): {len(echo) - len(text)}; "
          f"in the TEXT of a line: {len(text)}")
    for i in text:
        a, b = texts(old[i]["echo"]), texts(new[i]["echo"])
        print(f"   {i}")
        for t in a:
            if t not in b:
                print(f"      - {t}")
        for t in b:
            if t not in a:
                print(f"      + {t}")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
