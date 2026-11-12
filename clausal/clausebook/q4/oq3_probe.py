"""Open question 3 of the readability synthesis: can a variation be WORDED so that it states "on the same ledger", and
still parse once? Tried against the parser only (no Lean, no reader). Run from clausal/:  python3 clausebook/q4/oq3_probe.py
Each candidate wording replaces the forms of `l.smaller_amount` and `l.larger_amount` in the book IN MEMORY; nothing is
written. A candidate passes if every probe sentence compiles to exactly the Lean statement it has with today's wording.
The candidates were listed in clausebook/q4/FREEZE.md before this was run. None is adopted: wording is the owner's."""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from clausal import vocab                                    # noqa: E402
from clausal.core import load_glossary, parse_feature        # noqa: E402
from clausal.pipeline import ROOT                            # noqa: E402

TODAY = ("the amount is the same or smaller", "the amount is the same or larger")
CANDIDATES = [("the amount is the same or smaller on the same ledger", "the amount is the same or larger on the same ledger"),
              ("only the amount differs and it is the same or smaller", "only the amount differs and it is the same or larger"),
              ("only the amount differs, and it is the same or smaller", "only the amount differs, and it is the same or larger")]
PROBES = ["A transfer never loses acceptance when {S}",
          "A transfer never loses acceptance when {L}",
          "A transfer gives the same answer when {L}, if the first call is rejected",
          "A transfer gives the same answer when {L}, if the first call is accepted",
          "A transfer gives the same answer when {L}",
          "A transfer never loses acceptance when {S} and always answers",
          "A transfer always answers and never loses acceptance when {S}",
          "A transfer never loses acceptance when {S}, and a transfer gives the same answer when {L}, if the first call is rejected",
          "A transfer gives the same answer when {L}, if the first call is rejected, and a rejected transfer never changes the ledger",
          "A transfer gives the same answer when only the amount differs",
          "A transfer never loses acceptance when {S}, and a transfer gives the same answer when only the amount differs"]


def compile_all(voc, s, l):
    comp = vocab.Compiler(voc, refuse_vacuous=False)
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "p.feature"
        p.write_text("Feature: P\n\n" + "".join(f"  Rule: {x.replace('{S}', s).replace('{L}', l)}\n\n" for x in PROBES))
        f = parse_feature(p, "p.feature")
    out = []
    for r in f.rules:
        x = comp.rule(r, None)
        out.append(x.lean_def().split(":=", 1)[1] if isinstance(x, vocab.Reading) else f"{x.status} ({x.code})")
    return out


def main():
    gl = load_glossary(ROOT / "glossary.yaml", "glossary.yaml")
    rel = f"{vocab.BOOK_DIR}/local/ledger.yaml"
    text = (ROOT / rel).read_text()
    base = compile_all(vocab.load_project(ROOT, gl), *TODAY)
    print(f"today's wording: {sum(not b.split()[0].isupper() for b in base)} of {len(PROBES)} probe sentences compile")
    for s, l in CANDIDATES:
        t = text
        for old, new in zip(TODAY, (s, l)):
            a = f'    forms: ["{old}"]\n'
            assert t.count(a) == 1
            t = t.replace(a, f'    forms: ["{new}"]\n')
        got = compile_all(vocab.load_project(ROOT, gl, overrides={rel: t}), s, l)
        same = [g == b for g, b in zip(got, base)]
        print(f"candidate \"{s}\" / \"... larger\": {sum(same)} of {len(PROBES)} probe sentences compile to the same statement as today")
        for p, g, ok in zip(PROBES, got, same):
            if not ok:
                print(f"    NOT THE SAME: \"{p}\": {g if len(g) < 60 else 'another statement'}")


if __name__ == "__main__":
    main()
