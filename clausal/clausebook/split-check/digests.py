"""The sign-off digest of every Clausebook entry (its text and the Lean definitions it names), against the digests
recorded from the flat clausebook.yaml at commit dc38b56, before the split (plan node C1).

    cd clausal && PYTHONPATH=. python3 clausebook/split-check/digests.py

Prints the entries whose digest differs and the entries that are new. Moving an entry between books keeps its digest;
at the commit of the split the only differences were `changes_only` (its holes generalised from `acct` to `<T>`) and
`l.apply` (its `internal:` field gained the echo line that was a Python string). Later commits change more (plan node
Q3 puts further forms and texts into the entries)."""
import json
import sys
from pathlib import Path

from clausal import pipeline, vreport

st = pipeline.State()
defs = vreport.lean_defs(st.voc)
now = {i: vreport.piece_digest(st.voc, defs, i) for i in vreport.all_ids(st.voc)}
was = json.loads((Path(__file__).parent / "digests-before-split.json").read_text())
print(f"entries before the split: {len(was)}; now: {len(now)}")
print("digest differs:", sorted(i for i in was if i in now and was[i] != now[i]))
print("gone:", sorted(set(was) - set(now)))
print("new:", sorted(set(now) - set(was)))
sys.exit(0)
