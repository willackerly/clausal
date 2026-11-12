#!/usr/bin/env python3
"""Cut the pipeline logs kept under results/raw down to what is worth keeping in the repository.

    python3 harness/trim.py

Per mutant, results/raw/<id>.json is the raw result and is kept whole. Of the pipeline's own output
(results/raw/lean/<id>/ and results/raw/confirm/lean/<id>/) this keeps proofs.json, search.json, the
feature files of a confirmation run, and the last 150 lines of run.log; it deletes the rest (the full
report, cucumber JSON, build and search logs: a non-terminating model alone writes a 900,000-line
stack trace).
"""
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "results" / "raw"
KEEP = {"proofs.json", "search.json", "run.log"}
for d in list((RAW / "lean").glob("*")) + list((RAW / "confirm" / "lean").glob("*")):
    for f in d.iterdir():
        if f.name == "run.log":
            lines = f.read_text(errors="replace").splitlines()
            if len(lines) > 150:
                f.write_text(f"[... {len(lines) - 150} lines cut by harness/trim.py ...]\n" + "\n".join(l[:600] for l in lines[-150:]) + "\n")
        elif f.name not in KEEP and f.suffix != ".feature":
            f.unlink()
print("trimmed", RAW)
