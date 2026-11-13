"""Plan node Q3b: the numbers of clausebook/q3b/README.md that `clausal book check` does not print by itself.
Run from clausal/:  python3 clausebook/q3b/check.py

  1. Cross-system: two Rule lines about "a transfer", compiled in each declared project, with no project named, and in
     a project (in memory) that lists the local books of the wallet and of the ledger; and what the lint counts as
     shared across systems under each of those project lists.
  2. Separations: for each one recorded in a book, the project it is read in, whether it separates, whether its
     recorded separating input is for today's two terms, whether it is signed; and the violations that would remain
     if every proposal were signed (computed in memory: nothing is signed, nothing is written).
Nothing here runs Lean. `python3 -m clausal book check --separate` runs `clausal separate` on each separation again."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
from clausal import attest, book, projects, vocab, vreport          # noqa: E402
from clausal.core import Feature, Rule, load_glossary       # noqa: E402
from clausal.pipeline import ROOT                           # noqa: E402

LINES = ["A transfer is always accepted", "For a transfer, it is accepted"]       # the witnesses of clausebook/q4/README.md


def main() -> int:
    gl = load_glossary(ROOT / "glossary.yaml", "glossary.yaml")
    voc = vocab.load_project(ROOT, gl)
    pr = projects.load(ROOT)
    comp = vocab.Compiler(voc)
    scopes = {p.name: projects.books_of(pr, p.features[0]) for p in pr}
    both = scopes["wallet"] | scopes["ledger"]
    scopes["(wallet and ledger books in one project, in memory)"] = both
    scopes["(no project named: every book)"] = None
    f = Feature(path="<q3b>", name="q3b", slug="q3b")
    print("1. Rule lines about \"a transfer\", with no scenario beneath them")
    for n, line in enumerate(LINES):
        print(f"  \"{line}\"")
        for name, books in scopes.items():
            r = comp.rule(Rule(feature=f, name=line, line=n + 1, tags=[f"@id:q3b_{n}"]), None, books)
            what = ("ONE statement, about " + ", ".join(dict.fromkeys(o["id"] for c in r.info["clauses"] for o in c["ops"]))
                    if isinstance(r, vocab.Reading) else f"refused {r.status}")
            print(f"    {name}: {what}")
    across = lambda p: sorted(x["skeleton"] for x in book.lint(voc, attest.Records(), p)[0] if x["check"] == "4 shared skeleton across systems")
    print(f"  lint, skeletons shared across systems: declared projects: {across(None)}; "
          f"one project with the books of both: {across([('both', sorted(b.split('/', 1)[1] for b in both))])}; no project declared: {across([])}")
    print("2. Separations recorded in the books")
    recs = vreport.load_attestations(voc, {})
    by = lambda i: attest.person_review(recs.of(i, {"separation"}))
    ok = True
    for s in voc.separations.values():
        st = book.separation_state(voc, s)
        w = book.witness_state(s, st) if st["ok"] else None
        good = st["ok"] and w is not None and w["ok"]
        ok = ok and good
        print(f"  {s['id']} ({voc.at(s['id'])}), read in project `{st['project']}`: "
              + ("separates" if st["ok"] else "DOES NOT SEPARATE: " + "; ".join(st["why"]))
              + ("" if not st["ok"] else "; no separating input recorded" if w is None else
                 f"; separating input {s['witness']['input']} (the sentence for `{s['witness']['holds']}` holds), recorded for today's two terms" if w["ok"]
                 else "; RECORDED INPUT VOID: " + "; ".join(w["why"]))
              + ("; " + attest.said(by(s["id"])) if by(s["id"]) else "; UNSIGNED (no person's review or approval on record)"))
    now, _ = book.lint(voc)
    # WHAT-IF, in memory only: each proposed pair as if a person had approved it. Nobody has; nothing is stored.
    as_if = attest.Records()
    as_if.valid = [attest.make("separation", vreport.book_name(voc.book_of(i)), i, vreport.subject_digest(voc, {}, i), "approved",
                               "human:nobody-shown-as-if-approved", "what-if of clausebook/q3b/check.py; stored nowhere") for i in voc.separations]
    V, _ = book.lint(voc, records=as_if)
    print(f"  lint violations today: {len(now)}; were these {len(voc.separations)} separations signed: {len(V)}")
    for x in V:
        print(f"    [{x['check']}] {x['key']}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
