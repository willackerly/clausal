#!/usr/bin/env python3
"""The four negative controls of mutation/run_mutants.py that are about attestation and strict mode (c9, c10, c11, c26), run
alone: each is one `./run.sh --no-unit --quick` in a scratch copy (build/mutation/w0), after the copy is made afresh.

    python3 trust/tests/strict_controls.py          (about 2 minutes per control; run through tools/sem.sh)

  c9   --strict on the unchanged tree fails, and names a requirement of the project's trust policy
  c10  every entry attested `approved` by the fixture person, strict under trust/tests/person.yaml: passes
  c11  the same, then the text of one old-glossary definition is edited: exactly that entry's record is void, strict fails
  c26  the same, then the Lean text of one Clausebook word is edited: exactly that piece's record is void, strict fails

The complete control run is `python3 mutation/run_mutants.py`; this script does not write mutation/results.json.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "mutation"))
import run_mutants as rm  # noqa: E402

IDS = ("c9", "c10", "c11", "c26")


def main() -> int:
    work = rm.SLICE / "build" / "mutation" / "w0"
    out = []
    for c in rm.CONTROLS:
        if c[0] in IDS:
            r = rm.run_one(("control", c, work, None))
            out.append(r)
            print(f"{r['id']}: exit {r['exit']} (expected {r['expected_exit']}); expected output missing: {r['missing_output'] or 'none'}; "
                  f"{'as expected' if r['as_expected'] else 'NOT AS EXPECTED'}", flush=True)
    (HERE / "strict_controls.result.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(f"{sum(r['as_expected'] for r in out)} of {len(out)} controls as expected")
    return 0 if len(out) == len(IDS) and all(r["as_expected"] for r in out) else 1


if __name__ == "__main__":
    sys.exit(main())
