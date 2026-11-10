#!/usr/bin/env python3
"""Record (or check) the digests of everything PREREG.md says was fixed before the measured run.

    python3 harness/freeze.py            write results/frozen.json  (refuses if it exists; --force to replace)
    python3 harness/freeze.py --check    exit 1 and list what differs
"""
import datetime
import hashlib
import json
import sys
from pathlib import Path

COMPARE = Path(__file__).resolve().parent.parent
FILES = ["PREREG.md", "rules.json", "SLICE_COMMIT", "arms/proptests/src/main.rs", "arms/proptests/Cargo.toml", "arms/proptests/Cargo.lock",
         "arms/kani/src/lib.rs", "arms/kani/Cargo.toml", "arms/diff/src/main.rs", "arms/diff/Cargo.toml",
         "mutants/cargo-mutants.json", "mutants/hand-written.json"]


def digests():
    return {f: hashlib.sha256((COMPARE / f).read_bytes()).hexdigest() for f in FILES}


def main():
    out = COMPARE / "results" / "frozen.json"
    if "--check" in sys.argv:
        old = json.loads(out.read_text())["sha256"]
        diff = [f for f, h in digests().items() if old.get(f) != h]
        print("frozen files unchanged" if not diff else "CHANGED since freeze: " + ", ".join(diff))
        return 1 if diff else 0
    if out.exists() and "--force" not in sys.argv:
        sys.exit("results/frozen.json exists; use --force to replace it (and say so in TRADES.md)")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"frozen_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                               "sha256": digests()}, indent=1) + "\n")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
