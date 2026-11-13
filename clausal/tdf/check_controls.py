"""Negative controls of the overlay run (plan node T9.7a): does `clausal overlay run` withdraw a verdict when it should?
A control is caught when the named sentence gets the verdict the fault must give AND the run reports a difference from the
expected verdicts (it would exit 1).

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


def cut(p: Path, text: str) -> None:
    """Keep the header of a proof module (up to its first theorem) and put `text` after it."""
    s = p.read_text()
    p.write_text(s[:s.index("\ntheorem") + 1] + text)


def c_sorry(d):          # a proof replaced by sorry
    cut(d / "TdfProofs" / "g2_defined_release.lean", f"theorem {P}g2_defined_release : {P}g2_defined_release.obligation := by\n  sorry\n")


def c_other_type(d):     # a theorem of that name, of another type
    cut(d / "TdfProofs" / "g5_release_required_declared.lean", f"theorem {P}g5_release_required_declared : True := trivial\n")


def c_axiom(d):          # a proof that rests on an added axiom
    cut(d / "TdfProofs" / "g2_defined_release.lean", f"axiom tdfctl_assumed : {P}g2_defined_release.obligation\n"
        f"theorem {P}g2_defined_release : {P}g2_defined_release.obligation := tdfctl_assumed\n")


def c_meaning(d):        # the meaning of a pack word changed under the link that uses it: "admits" now means "denies"
    sub(d / "Abac" / "Pieces.lean", "Prop := p.deny_unlabelled = false", "Prop := p.deny_unlabelled = true")


def c_no_sat(d):         # the non-vacuity theorem removed
    p = d / "TdfProofs" / "g1_labelled.lean"
    s = p.read_text()
    p.write_text(s[:s.index("/-- The scope is met")])


def c_refutation_gone(d):   # a refutation replaced by sorry
    cut(d / "TdfProofs" / "w_entitled_not_released.lean",
        f"theorem {P}w_entitled_not_released.refuted : ¬ {P}w_entitled_not_released.obligation := by\n  sorry\n")


# ---- the links (fix round)

def c_link_missing(d):   # the proof of a link removed
    (d / "TdfLinks" / "g4.lean").unlink()


def c_link_other_type(d):   # a theorem of the link's name, of another type
    cut(d / "TdfLinks" / "g2.lean", "theorem Link.g2 : True := trivial\n")


def c_link_sorry(d):     # a link proved with sorry
    cut(d / "TdfLinks" / "g5.lean", "theorem Link.g5 : Link.g5.claim := by\n  sorry\n")


def c_link_uses_statement(d):   # the direction "the sentences give the statements" taken from the statements' own theorems
    p = d / "TdfLinks" / "g1.lean"
    s = p.read_text().replace("theorem Link.g1 : Link.g1.claim", "theorem Link.g1.honest : Link.g1.claim")
    p.write_text(s + "\ntheorem Link.g1 : Link.g1.claim := by\n  have h : Link.g1.claim := Link.g1.honest\n  unfold Link.g1.claim at h ⊢\n"
                     "  exact ⟨fun _ => ⟨T93.core_g1, T93.decide_total⟩, h.mpr⟩\n")


def c_link_weakened_repaired(d):
    # THE REVIEWER'S CONTROL. A pack word is weakened ("the policy admits unlabelled objects" now means True), so the
    # sentence g1_unlabelled says less than T9.3; the link is repaired so that everything compiles: the direction that is
    # now false is taken from the statements' own theorems, the other direction needs nothing for the weakened word.
    sub(d / "Abac" / "Pieces.lean", "Prop := p.deny_unlabelled = false", "Prop := True")
    p = d / "TdfLinks" / "g1.lean"
    s = p.read_text()
    old = ("      rcases h with ⟨_, hdeny⟩ | ⟨hne, _⟩\n      · exact hdeny\n      · exact absurd h0 hne\n")
    assert old in s
    s = s.replace(old, "      trivial\n")
    a, b = s.index("  · rintro ⟨O1, O2, O3⟩\n"), s.index("  · rintro ⟨S1, S2⟩\n")
    p.write_text(s[:a] + "  · exact fun _ => ⟨T93.core_g1, T93.decide_total⟩\n" + s[b:])


def c_link_outside_given(d):   # a link whose proof rests on a theorem of T9.3 that is not among its `given`
    sub(d / "TdfLinks" / "g2.lean", "  unfold Link.g2.claim\n", "  unfold Link.g2.claim\n  have extra := T93.decide_refines\n")


def c_through(d):        # nothing seeded in the Lean: the expected file lists one more theorem the proof must go through
    def change(proj, tmp):
        e = json.loads((ROOT / proj["expected"]).read_text())
        e["items"][P + "g2_defined_release"]["through"].append("T93.core_g4")
        (tmp / "expected.json").write_text(json.dumps(e))
        proj["expected"] = str(tmp / "expected.json")
    return change


CONTROLS = [
    ("a proof replaced by sorry", c_sorry, P + "g2_defined_release", "STATED-ONLY"),
    ("a theorem of the right name and another type", c_other_type, P + "g5_release_required_declared", "STATED-ONLY"),
    ("a proof resting on an added axiom", c_axiom, P + "g2_defined_release", "STATED-ONLY"),
    ("the meaning of a pack word changed under the link that uses it", c_meaning, P + "g1_unlabelled", "UNLINKED"),
    ("the non-vacuity theorem removed", c_no_sat, P + "g1_labelled", "STATED-ONLY"),
    ("a refutation replaced by sorry", c_refutation_gone, P + "w_entitled_not_released", "STATED-ONLY"),
    ("the proof of a link removed", c_link_missing, P + "g4_more_values", "UNLINKED"),
    ("a theorem of a link's name and another type", c_link_other_type, P + "g2_defined", "UNLINKED"),
    ("a link proved with sorry", c_link_sorry, P + "g5_none_listed", "UNLINKED"),
    ("a link one direction of which is the statements' own theorems", c_link_uses_statement, P + "g1_labelled", "UNLINKED"),
    ("a pack word weakened and the link repaired with the statements' theorems (the reviewer's control)", c_link_weakened_repaired, P + "g1_unlabelled", "UNLINKED"),
    ("a link resting on a theorem of T9.3 outside its `given`", c_link_outside_given, P + "g2_defined", "UNLINKED"),
    ("a proof that does not reach a theorem the expected file says it goes through", c_through, P + "g2_defined_release", "STATED-ONLY"),
]


def main() -> int:
    base = yaml.safe_load((ROOT / "projects.local.yaml").read_text())
    proj = next(p for p in base["projects"] if p["name"] == "tdf")
    caught, lines = 0, []
    for what, seed, item, want in CONTROLS:
        with tempfile.TemporaryDirectory() as t:
            copy = Path(t) / "lean"
            shutil.copytree(ROOT / "tdf" / "lean", copy)
            change = seed(copy)
            d = json.loads(json.dumps(proj))
            d["name"] = "tdfctl"
            if change:
                change(d, Path(t))
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
            run_differs = bool(res["differ"])
            ok = row["code"] == want and run_differs
            caught += ok
            lines.append(f"{'caught' if ok else 'NOT CAUGHT':<11}{what}: {item.split('.')[-1]} is {row['code']} (must be {want})"
                         + (f"; also changed: {', '.join(o.split('.')[-1] for o in others)}" if others else "")
                         + (f"\n           {row.get('why', '')[:300]}" if row.get("why") else ""))
    print("\n".join(lines))
    print(f"{caught} of {len(CONTROLS)} controls caught")
    return 0 if caught == len(CONTROLS) else 1


if __name__ == "__main__":
    sys.exit(main())
