"""Plan node L2: which literal words of the new forms occur in the 48 frozen trial sentences (trials/sentences/authors.json).

The forms were written from the kind of claim, not from the sentences. This script reports, after the forms were frozen
(clausebook/l2/FREEZE.md), where their literal words coincide with a trial sentence anyway. It prints rule keys and
counts only, never a sentence. Nothing under trials/ is written.

  usage (from clausal/):  python3 clausebook/l2/coincide.py
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]

# the literal words of each new form (holes left out), as the book has them
FORMS = {
    "equals: \"{a} equals {b}\"": [r"\bequals\b"],
    "equals, negated: \"{a} differs from {b}\"": [r"\bdiffers from\b"],
    "each_at_most: \"each of {ns} is afterwards at most {t}\"": [r"\beach of\b.*\bis afterwards at most\b"],
    "each_at_most, its first words only: \"each of\"": [r"\beach of\b"],
    "each_at_most, its last words only: \"is afterwards at most\"": [r"\bis afterwards at most\b"],
    "tied + same_input: \"{op} followed by {op2} with the same input\"": [r"\bfollowed by\b.*\bwith the same input\b"],
    "tied: \" with \" after a sequence (\"followed by ... with\")": [r"\bfollowed by\b.*\bwith\b"],
    "same_input: \"the same input\"": [r"\bthe same input\b"],
}


def main():
    authors = json.loads((REPO / "trials/sentences/authors.json").read_text())["authors"]
    rules = [(f"{a.get('id') or a.get('author') or a.get('name')}/{r['id']}", r["rule"]) for a in authors for r in a["rules"]]
    print(f"{len(rules)} frozen sentences")
    for name, pats in FORMS.items():
        hits = [k for k, text in rules if all(re.search(p, text, re.I) for p in pats)]
        print(f"  {len(hits):2d}  {name}" + (":  " + ", ".join(hits) if hits else ""))


if __name__ == "__main__":
    main()
