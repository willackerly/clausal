#!/usr/bin/env python3
"""Reviewer (V2/V3 review, second pass): instrument a generated reading-search file (Run/ReadingSearch.lean or
Run/NewReadings.lean) so that, beside the builder's counts, every RSEARCH line also reports

  DEFFALSE  in-scope (point, frame) evaluations where the DEFINITION says false
  FPOS      the same per frame position
  SILENT    in-scope points where the (first) operation gives NO answer (run = none)
  REJ       in-scope points where it answers with a rejection

These say how much power the definition-vs-checker comparison has: a checker that is wrong only where the claim
is false, or only on a silent call, can only be caught on such points. Writes a copy; the input is untouched.
usage: instr.py IN.lean OUT.lean
"""
import re
import sys


def balanced_from(s, i):
    """s[i] == '(' ; return index just past the matching ')'."""
    d = 0
    for j in range(i, len(s)):
        if s[j] == "(":
            d += 1
        elif s[j] == ")":
            d -= 1
            if d == 0:
                return j + 1
    raise ValueError("unbalanced")


def main(src, dst):
    out = []
    op = None
    for ln in open(src).read().split("\n"):
        st = ln.strip()
        if st == "let mut agree := 0":
            ind = ln[: len(ln) - len(ln.lstrip())]
            out += [ln, ind + "let mut defFalse := 0", ind + "let mut silent := 0", ind + "let mut rej := 0",
                    ind + "let mut fpos : Array Nat := #[]"]
            continue
        if st.startswith("if decide (") and ".scope st inp)" in st:
            k = ln.index("decide (") + len("decide ")
            inner = ln[k:balanced_from(ln, k)]          # "((OP).scope st inp)"
            assert inner.endswith(".scope st inp)"), inner
            op = inner[1:-len(".scope st inp)")]        # "(OP)"
            out.append(ln)
            continue
        if st == "evals := evals + ats.length":
            ind = ln[: len(ln) - len(ln.lstrip())]
            out += [ln,
                    ind + "if fpos.isEmpty then fpos := Array.replicate ats.length 0",
                    ind + "for (v, j) in ats.zipIdx do",
                    ind + "  if !v then",
                    ind + "    defFalse := defFalse + 1",
                    ind + "    fpos := fpos.modify j (· + 1)",
                    ind + f"match {op}.run st inp with",
                    ind + "| none => silent := silent + 1",
                    ind + f"| some (r, _) => if !(decide ({op}.accepted r)) then rej := rej + 1"]
            continue
        if st.startswith('IO.println s!"RSEARCH'):
            ln = ln[:-1] + '\\tDEFFALSE={defFalse}\\tSILENT={silent}\\tREJ={rej}\\tFPOS={fpos.toList}"'
        out.append(ln)
    open(dst, "w").write("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
