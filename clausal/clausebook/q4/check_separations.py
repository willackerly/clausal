"""Plan node Q4: the PROPOSED separating pairs of clausebook/q4/separations.proposed.yaml, checked in memory.
Run from clausal/:  python3 clausebook/q4/check_separations.py
Nothing is written and nothing is signed. For each pair: would it be in force once signed? Then the lint is run with the
pairs treated as signed, to show which violations would remain."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
from clausal import book, vocab, vreport            # noqa: E402
from clausal.core import load_glossary              # noqa: E402
from clausal.pipeline import ROOT                   # noqa: E402


def main():
    gl = load_glossary(ROOT / "glossary.yaml", "glossary.yaml")
    rel = f"{vocab.BOOK_DIR}/core.yaml"
    text = (ROOT / rel).read_text()
    assert text.count("\ngrammar:\n") == 1
    prop = (HERE / "separations.proposed.yaml").read_text()
    prop = prop[prop.index("\nseparations:\n") + 1:]
    voc = vocab.load_project(ROOT, gl, overrides={rel: text.replace("\ngrammar:\n", "\n" + prop + "\ngrammar:\n")})
    ok = 0
    for s in voc.separations.values():
        st = book.separation_state(voc, s)
        ok += st["ok"]
        print(f"{s['id']}: {'separates (would be in force once signed)' if st['ok'] else 'DOES NOT SEPARATE: ' + '; '.join(st['why'])}")
    print(f"{ok} of {len(voc.separations)} proposed pairs separate")
    # WHAT-IF, in memory only: each proposed pair as if a person had approved it. Nobody has; nothing is stored.
    from clausal import attest
    as_if = attest.Records()
    as_if.valid = [attest.make("separation", vreport.book_name(voc.book_of(i)), i, vreport.subject_digest(voc, {}, i), "approved",
                               "human:nobody-shown-as-if-approved", "what-if of clausebook/q4/check_separations.py; stored nowhere") for i in voc.separations]
    V, _ = book.lint(voc, records=as_if)
    now, _ = book.lint(vocab.load_project(ROOT, gl))
    print(f"lint violations today: {len(now)}; with these {len(voc.separations)} pairs signed: {len(V)}")
    for x in V:
        print(f"  [{x['check']}] {x['key']}")


if __name__ == "__main__":
    main()
