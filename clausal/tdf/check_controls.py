"""Negative controls of the overlay run (plan node T9.7a): does `clausal overlay run` withdraw a verdict when it should?

    python3 tdf/check_controls.py            (from clausal/; needs the overlay projects.local.yaml with the project `tdf`)

Each control copies the hand-written Lean of the project (tdf/lean) into a scratch directory, seeds ONE fault, runs
the project from an overlay file that points at the copy (as the project `tdfctl`, in its own workspace
build/overlay/tdfctl), and compares the verdict of the named sentence with what the fault must give. Nothing tracked
is written. Exit 1 if a control is not caught.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
P = "Rule.tdflite_decision_core."


def sub(path: Path, old: str, new: str, count: int = 1) -> None:
    s = path.read_text()
    assert old in s, f"{path.name}: the text to seed is not there: {old!r}"
    path.write_text(s.replace(old, new, count))


def c_sorry(d):          # a proof replaced by sorry
    p = d / "TdfProofs" / "g2_defined.lean"
    s = p.read_text()
    p.write_text(s[:s.index("\ntheorem") + 1] + f"theorem {P}g2_defined : {P}g2_defined.obligation := by\n  sorry\n")


def c_other_type(d):     # a theorem of that name, of another type
    p = d / "TdfProofs" / "g5_released_entitled.lean"
    s = p.read_text()
    p.write_text(s[:s.index("\ntheorem") + 1] + f"theorem {P}g5_released_entitled : True := trivial\n")


def c_axiom(d):          # a proof that rests on an added axiom
    p = d / "TdfProofs" / "g5_none_listed.lean"
    s = p.read_text()
    p.write_text(s[:s.index("\ntheorem") + 1] + f"axiom tdfctl_assumed : {P}g5_none_listed.obligation\n"
                 f"theorem {P}g5_none_listed : {P}g5_none_listed.obligation := tdfctl_assumed\n")


def c_meaning(d):        # the meaning of a pack word changed under a proof: "admits" now means "denies"
    sub(d / "Abac" / "Pieces.lean", "Prop := p.deny_unlabelled = false", "Prop := p.deny_unlabelled = true")


def c_no_sat(d):         # the proof kept, the non-vacuity theorem removed
    p = d / "TdfProofs" / "g1_labelled.lean"
    s = p.read_text()
    p.write_text(s[:s.index("/-- The scope is met")])


def c_refutation_gone(d):   # a refutation replaced by sorry
    p = d / "TdfProofs" / "w_entitled_not_released.lean"
    s = p.read_text()
    p.write_text(s[:s.index("\ntheorem") + 1] + f"theorem {P}w_entitled_not_released.refuted : ¬ {P}w_entitled_not_released.obligation := by\n  sorry\n")


CONTROLS = [
    ("a proof replaced by sorry", c_sorry, P + "g2_defined", "STATED-ONLY"),
    ("a theorem of the right name and another type", c_other_type, P + "g5_released_entitled", "STATED-ONLY"),
    ("a proof resting on an added axiom", c_axiom, P + "g5_none_listed", "STATED-ONLY"),
    ("the meaning of a pack word changed under its proof", c_meaning, P + "g1_unlabelled", "STATED-ONLY"),
    ("the non-vacuity theorem removed", c_no_sat, P + "g1_labelled", "STATED-ONLY"),
    ("a refutation replaced by sorry", c_refutation_gone, P + "w_entitled_not_released", "STATED-ONLY"),
]


def main() -> int:
    base = yaml.safe_load((ROOT / "projects.local.yaml").read_text())
    proj = next(p for p in base["projects"] if p["name"] == "tdf")
    caught, lines = 0, []
    for what, seed, item, want in CONTROLS:
        with tempfile.TemporaryDirectory() as t:
            copy = Path(t) / "lean"
            shutil.copytree(ROOT / "tdf" / "lean", copy)
            seed(copy)
            d = json.loads(json.dumps(proj))
            d["name"] = "tdfctl"
            for k, v in d["lean"]["sources"].items():
                if v.startswith("tdf/lean/"):
                    d["lean"]["sources"][k] = str(copy / v[len("tdf/lean/"):])
            ov = Path(t) / "overlay.yaml"
            ov.write_text(yaml.safe_dump({"version": 1, "projects": [d]}))
            subprocess.run([sys.executable, "-m", "clausal", "overlay", "run", "tdfctl"], cwd=ROOT, env=dict(os.environ, CLAUSAL_OVERLAY=str(ov)),
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            res = json.loads((ROOT / "build" / "overlay" / "tdfctl" / "out" / "verdicts.json").read_text())
            (ROOT / "build" / "overlay" / "tdfctl" / "out" / "verdicts.json").unlink()
            row = next(r for r in res["rows"] if r["id"] == item)
            others = [r["id"] for r in res["rows"] if r["id"] != item and r["expected"] != r["code"]]
            ok = row["code"] == want
            caught += ok
            lines.append(f"{'caught' if ok else 'NOT CAUGHT':<11}{what}: {item.split('.')[-1]} is {row['code']} (must be {want})"
                         + (f"; also changed: {', '.join(o.split('.')[-1] for o in others)}" if others else "")
                         + (f"\n           {row.get('why', '')[:200]}" if row.get("why") else ""))
    print("\n".join(lines))
    print(f"{caught} of {len(CONTROLS)} controls caught")
    return 0 if caught == len(CONTROLS) else 1


if __name__ == "__main__":
    sys.exit(main())
