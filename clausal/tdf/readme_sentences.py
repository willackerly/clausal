"""Do the three sentences README.md plans for TDFLite compile against the access-control pack? (plan nodes T9.7a, Q10)

    python3 tdf/readme_sentences.py          (from clausal/; needs no overlay, no Lean, no crate)

Each sentence is compiled, as a Rule line, against core + clausebook/abac.yaml + clausebook/local/tdf.yaml with the
types of tdf/types.yaml. Then the nearest wording that today's pieces DO read is compiled the same way. Compiling says
nothing about truth: the verdict of a sentence that is in tdf/features/tdf.feature is in tdf/verdicts.md.
"""
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from clausal import overlay, vocab                      # noqa: E402
from clausal.core import parse_feature                  # noqa: E402

PROJECT = {"name": "tdf", "books": ["core.yaml", "abac.yaml", "local/tdf.yaml"], "types": "tdf/types.yaml", "features": []}
README = [
    ("A key release is accepted only if every attribute of the data is satisfied by the subject under its rule",
     "A key release is accepted only if every label of the request is satisfied by the subject of the request under the policy"),
    ("A key release never loses acceptance when the subject gains an entitlement",
     "A key release never loses acceptance when the subject holds more values"),
    ("A key release gives the same answer when only the order of the attributes differs", None),
]


def compile_line(comp, line):
    with tempfile.TemporaryDirectory() as t:
        p = Path(t) / "x.feature"
        p.write_text(f"Feature: x\n  @id:s\n  Rule: {line}\n")
        return comp.rule(parse_feature(p, "x.feature").rules[0], None, None)


def main() -> int:
    from clausal.core import load_glossary
    gl = load_glossary(ROOT / PROJECT["types"], PROJECT["types"])
    voc = vocab.Vocabulary([(ROOT / vocab.BOOK_DIR / b, f"{vocab.BOOK_DIR}/{b}") for b in PROJECT["books"]], gl)
    comp = vocab.Compiler(voc)
    n = 0
    for as_written, nearest in README:
        r = compile_line(comp, as_written)
        ok = isinstance(r, vocab.Reading)
        n += ok
        print(f"{'COMPILES' if ok else r.status:<10}README: {as_written}")
        if not ok:
            print(f"          {r.message.split(': ', 1)[-1][:200]}")
        if nearest:
            r2 = compile_line(comp, nearest)
            ok2 = isinstance(r2, vocab.Reading)
            print(f"{'COMPILES' if ok2 else r2.status:<10}nearest: {nearest}")
            if ok2:
                print(f"          {r2.claims[0].lean}")
    print(f"{n} of {len(README)} README sentences compile as written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
