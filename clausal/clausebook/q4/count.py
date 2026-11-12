"""Plan node Q4, the freeze: how many Rule and step lines of features/*.feature each row of the first batch rewrites.
Run from clausal/ BEFORE the batch is applied:  python3 clausebook/q4/count.py   (it reads the files of a git revision
when given one:  python3 clausebook/q4/count.py 891bf01).
A line is a `Rule:` line or a Given / When / Then / And / But step. A line that two rows rewrite is counted under both."""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FILES = ["features/ledger.feature", "features/ledger_rules.feature", "features/negative.feature", "features/wallet.feature"]
LINE = re.compile(r"^\s*(Rule:|Given|When|Then|And|But)\s+(.*)$")
RULE = lambda kind: kind == "Rule:"
STEP = lambda kind: kind != "Rule:"
ANY = lambda kind: True
#        row  what the line is written with (old form)                                      which lines   pattern
ROWS = [("1", "the adjective 'successful' on a Rule subject",                               RULE, r"\b[Ss]uccessful \w"),
        ("2", "'always succeeds' / 'is never accepted'",                                    RULE, r"always succeeds|is never accepted"),
        ("3", "'the operation succeeds'",                                                   ANY,  r"the operation succeeds"),
        ("4", "'if it is accepted / rejected,' before the claim of a Rule line",            RULE, r"^[Ff]or .*?, if it is (accepted|rejected), "),
        ("5", "the articles 'every' / 'any' on a Rule subject",                             RULE, r"^(Every|Any|every|any) |, and (every|any) "),
        ("6", "'the aggregate {ns}'",                                                       ANY,  r"the aggregate "),
        ("7a", "l.balances_of: 'the balances of', 'all balances of', 'account value of'",   ANY,  r"(the balances of|all balances of|account value of) (the ledger|ledger \w+)"),
        ("7b", "l.balance_at: 'the balance of account {i} of {l}' (as the result)",         ANY,  r"the result is the balance of account "),
        ("7c", "l.the_transfer: 'the transfer {t}' (in a Given or a Then, not a When)",     STEP, r"^the transfer <\w+> is (not )?valid"),
        ("8", "'{t} is not more than {m}'",                                                 ANY,  r" is not more than "),
        ("9", "'{m} plus {t} does not exceed {z}'",                                         ANY,  r" does not exceed "),
        ("10", "'the amount is smaller' / 'the amount is larger'",                          RULE, r"the amount is (smaller|larger)"),
        ("11", "'every X is not P afterwards'",                                             ANY,  r"^([Ff]or [^,]*, )?every .* is not .* afterwards"),
        ("12", "'for <subject>, <Then form>' of a frame that has a verb phrase",            RULE, r"^[Ff]or .*(is unchanged|is increased by|is decreased by|it answers|nothing is changed|is afterwards at (most|least))"),
        ("13", "'is increased by' / 'is decreased by' / 'it is rejected and nothing is changed'", ANY, r"is (increased|decreased) by (?!exactly)|it is rejected and nothing is changed"),
        ("14", "'never loses that it is accepted'",                                         RULE, r"never loses that it is accepted"),
        ("15", "'gives the same answer when {v}, if it is accepted / rejected'",            RULE, r"gives the same answer when .*, if it is (accepted|rejected)"),
        ("19", "(no sentence: forms and texts moved into the book)",                        ANY,  r"$^")]


def text(rel, rev):
    if rev:
        return subprocess.run(["git", "show", f"{rev}:clausal/{rel}"], cwd=ROOT, check=True, capture_output=True, text=True).stdout
    return (ROOT / rel).read_text()


def main(argv):
    rev = argv[0] if argv else None
    lines = []
    for rel in FILES:
        for n, l in enumerate(text(rel, rev).splitlines(), 1):
            m = LINE.match(l)
            if m:
                lines.append((rel, n, m.group(1), m.group(2)))
    print(f"{len(lines)} Rule and step lines in {len(FILES)} files" + (f" at {rev}" if rev else ""))
    touched = set()
    for row, what, which, pat in ROWS:
        hits = [(rel, n) for rel, n, kind, body in lines if which(kind) and re.search(pat, body)]
        touched |= set(hits)
        rules = sum(1 for rel, n in hits if next(k for r, m, k, _ in lines if (r, m) == (rel, n)) == "Rule:")
        print(f"row {row:>3}: {len(hits):2d} lines ({rules} Rule, {len(hits) - rules} step)  {what}")
        for rel, n in hits:
            print(f"           {rel}:{n}")
    print(f"lines rewritten by at least one row: {len(touched)}")


if __name__ == "__main__":
    main(sys.argv[1:])
