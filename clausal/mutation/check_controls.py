#!/usr/bin/env python3
"""Which negative controls does the book check of run.sh step 3 stop?

    python3 mutation/check_controls.py [--only ID,ID]

`./run.sh` runs `python3 -m clausal book check` in step 3, before the build, the proofs, the search and the report. A
control that changes what a fixture sentence compiles to (it edits a sentence, or a form or a `lean:` text of the book)
and does not RECORD the change (`recorded()` in run_mutants.py) is stopped there, and the defence it was written to test
is never reached. This script applies every control's patch to a light copy of clausal/ (no build output) and runs
`python3 -m clausal book check --quiet` on it: a few seconds per control, no Lean, no Rust.

Exit 0 iff the controls stopped are exactly STOPPED_AT_THE_BOOK (run_mutants.py): the ones written to be stopped there.
(c42 is stopped here by the import check alone; the build of lean/Frames in a directory of its own needs `--lean`, which
the full control run passes.)
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_mutants as rm  # noqa: E402

SKIP = shutil.ignore_patterns("target", ".lake", ".tools", "out", "build", "compare", "review", "probe", "__pycache__", "results*", "logs")


def main() -> int:
    only = set(filter(None, (sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else "").split(",")))
    stopped, bad = [], []
    for id_, what, patch, args, want_rc, pats in rm.CONTROLS:
        if only and id_ not in only:
            continue
        with tempfile.TemporaryDirectory(prefix="clausal-ctl-") as d:
            root = Path(d) / "clausal"
            shutil.copytree(rm.SLICE, root, ignore=SKIP, symlinks=True)
            try:
                patch(root)
            except Exception as e:      # noqa: BLE001  (a patch that no longer applies is what this script is for)
                print(f"  {id_}: THE PATCH DOES NOT APPLY: {type(e).__name__}: {str(e)[:300]}")
                bad.append(id_)
                continue
            r = subprocess.run([sys.executable, "-m", "clausal", "book", "check", "--quiet"], cwd=root, capture_output=True, text=True)
            out = r.stdout + r.stderr
        meant = id_ in rm.STOPPED_AT_THE_BOOK
        if r.returncode:
            stopped.append(id_)
        ok = bool(r.returncode) == meant
        if not ok:
            bad.append(id_)
        why = [l.strip()[:220] for l in out.splitlines() if "NOT EXPECTED" in l or "CORE IS NOT ALONE" in l or "Error" in l][:2]
        print(f"  {id_}: the book check {'STOPS the run' if r.returncode else 'passes'}"
              + (" (as meant)" if ok else "  <-- NOT AS MEANT: " + ("the control never reaches the defence it is about" if r.returncode else "it was written to be stopped here"))
              + ("".join("\n        " + w for w in why) if r.returncode else ""))
    print(f"{len(stopped)} controls are stopped by the book check: {', '.join(stopped) or 'none'}; meant: {', '.join(sorted(rm.STOPPED_AT_THE_BOOK, key=lambda x: int(x[1:])))}")
    print("all as meant" if not bad else f"NOT AS MEANT: {', '.join(bad)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
