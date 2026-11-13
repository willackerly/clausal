"""Plan node Q3b, fix round: a recorded separating input that does NOT separate. THE CONTROL of the two-part check.
Run from clausal/, under tools/sem.sh (it runs Lean and cargo):  python3 clausebook/q3b/bogus.py

In a copy of the Clausebook (a temporary directory; the book is not touched), the `witness:` of `sep.more_than.exceeds` is
replaced by the reviewer's input (the empty ledger and the empty batch, grid 1), which is not a separating input
`clausal separate` finds for the two sentences; the two term hashes are left as they are. Expected:

  1  the plain lint still counts the separation as a proposal (the hashes are current; it does not run the input), and what
     it prints says the input is NOT run by it, and does not say "machine-checked";
  2  `book.rerun_separation` (what `book check --separate` and ./run.sh ask) answers NOT CONFIRMED;
  3  `clausal review sep.more_than.exceeds` signs nothing and exits 1; the violation of the pair stays.
  4  THE OTHER SIDE: on the book as it stands the same three are: a proposal and CONFIRMED (nothing is signed).
Exit 0 iff all four are as expected. Nothing of the repository is written."""
import contextlib
import io
import re
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
from clausal import attest, book, vocab, vreport            # noqa: E402
from clausal.core import load_glossary              # noqa: E402
from clausal.pipeline import ROOT                   # noqa: E402

SEP = "sep.more_than.exceeds"
PAT = re.compile(r'(      holds: more_than\n      input: )\{ the_ledger: "\[2, 1\]", the_batch: "\[0->1:1\]" \}\n      grid: 297\n')
BOGUS = r'\1{ the_ledger: "[]", the_batch: "[]" }\n      grid: 1\n'


def main() -> int:
    gl = load_glossary(ROOT / "glossary.yaml", "glossary.yaml")
    real = vocab.load_project(ROOT, gl)
    ok = True
    with tempfile.TemporaryDirectory() as d:
        shutil.copytree(ROOT / vocab.BOOK_DIR, Path(d) / vocab.BOOK_DIR)
        f = Path(d) / vocab.BOOK_DIR / "local" / "ledger.yaml"
        text, n = PAT.subn(BOGUS, f.read_text())
        assert n == 1, "the recorded input of sep.more_than.exceeds is not the one this control replaces"
        f.write_text(text)
        v = vocab.Vocabulary([(Path(d) / rel, rel) for _, rel in vocab.project_books(ROOT)], gl)
        s = v.separations[SEP]
        V, notes = book.lint(v, attest.Records())
        mine = [x["what"] for x in V if SEP in (x.get("proposed") or [])]
        nif = [x["key"] for x in V if x["check"] == "4 separation not in force"]
        one = len(mine) == 1 and not nif and "NOT run by this check" in mine[0] and "machine-checked" not in mine[0]
        print(f"bogus input {s['witness']['input']} (grid {s['witness']['grid']}), term hashes unchanged")
        print(f"1 plain lint: {len(V)} violations, {len(nif)} 'separation not in force'; the pair's violation says: ...{mine[0][mine[0].index('no separating pair'):mine[0].index(': `sep')] if mine else '(none)'}")
        r = book.rerun_separation(v, s)
        print(f"2 rerun (book check --separate): {'CONFIRMED' if r['ok'] else 'NOT CONFIRMED: ' + '; '.join(r['why'])}")
        sf = v.book_of(SEP).attest_path
        before = sf.read_text() if sf.exists() else None
        with contextlib.redirect_stdout(io.StringIO()) as o:
            rc = vreport.attest_entries(v, SEP, "approved", "human:control-of-q3b-bogus", "control of clausebook/q3b/bogus.py in a temporary copy; no person signed anything")
        same = (sf.read_text() if sf.exists() else None) == before
        V2, _ = book.lint(v)
        print(f"3 clausal attest {SEP} --act approved: exit {rc}; attestation store {'unchanged' if same else 'CHANGED'}; violations after: {len(V2)}; it printed: {o.getvalue().splitlines()[0]}")
        ok = one and not r["ok"] and rc == 1 and same and len(V2) == len(V)
    V0, _ = book.lint(real, attest.Records())
    r0 = book.rerun_separation(real, real.separations[SEP])
    print(f"4 the book as it stands: {len(V0)} violations; rerun of {SEP}: {'CONFIRMED at ' + str(real.separations[SEP]['witness']['input']) if r0['ok'] else 'NOT CONFIRMED'}")
    ok = ok and r0["ok"]
    print("control: " + ("as expected" if ok else "FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
