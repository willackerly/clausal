#!/usr/bin/env python3
"""Count the hand-written Lean behind each crate, the same way for both, against CODE lines of Rust.

    python3 effort/count.py

"Code line" = non-blank and not a comment. For Lean a line inside /- ... -/ or starting with -- is a comment;
import / open / namespace / end lines are counted separately as boilerplate. A proof file is counted from its
`theorem` line on (the header above it is a generated comment).
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEAN = ROOT / "lean"


def lean_lines(text: str):
    code = boiler = 0
    in_block = False
    for raw in text.splitlines():
        s = raw.strip()
        if in_block:
            if "-/" in s:
                in_block = False
            continue
        if s.startswith("/-"):
            in_block = "-/" not in s
            continue
        if not s or s.startswith("--"):
            continue
        if re.match(r"(import|open|namespace|end)\b", s) or s.startswith("set_option"):
            boiler += 1
        else:
            code += 1
    return code, boiler


def rust_lines(text: str) -> int:
    return sum(1 for l in text.splitlines() if l.strip() and not l.strip().startswith("//"))


def proof_lines(path: Path) -> int:
    lines = path.read_text().splitlines()
    i = next(k for k, l in enumerate(lines) if l.startswith("theorem Spec."))
    return sum(1 for l in lines[i + 1:] if l.strip())       # tactic lines, comments included, statement line excluded


def main():
    rows = []
    for crate, lemma_dir, vocab, proofs in (("wallet", None, LEAN / "Wallet/Vocab.lean", LEAN / "Wallet/Proofs/wallet"),
                                            ("ledger", LEAN / "Ledger/Lemmas", LEAN / "Ledger/Vocab.lean", LEAN / "Wallet/Proofs/ledger")):
        rust_raw = (ROOT / crate / "src/lib.rs").read_text()
        lem = [lean_lines(p.read_text()) for p in sorted(lemma_dir.glob("*.lean"))] if lemma_dir else []
        lem_code, lem_boiler = sum(c for c, _ in lem), sum(b for _, b in lem)
        lem_text = "".join(p.read_text() for p in sorted(lemma_dir.glob("*.lean"))) if lemma_dir else ""
        pf = sorted(proofs.glob("*.lean"))
        pl = [proof_lines(p) for p in pf]
        voc_code, _ = lean_lines(vocab.read_text())
        total = lem_code + sum(pl) + voc_code
        rc = rust_lines(rust_raw)
        rows.append((crate, len(rust_raw.splitlines()), rc, len(pf), min(pl), max(pl), sum(pl), lem_code, lem_boiler,
                     len(re.findall(r"(?m)^theorem ", lem_text)), len(re.findall(r"(?m)^def ", lem_text)),
                     len(re.findall(r"loop\.spec_decr_nat", lem_text)), voc_code, total, total / rc, (lem_code + sum(pl)) / rc))
    hdr = ["crate", "Rust lines (raw)", "Rust code lines", "scenario proofs", "shortest", "longest", "proof lines in all",
           "lemma code lines", "lemma boilerplate lines", "lemma theorems", "lemma definitions", "loop invariants used",
           "glossary (Vocab) code lines", "hand-written Lean in all", "Lean per Rust code line", "same without the glossary"]
    for k, h in enumerate(hdr):
        print(f"{h:32s} " + "  ".join(f"{(r[k] if not isinstance(r[k], float) else round(r[k], 1))!s:>8}" for r in rows))


if __name__ == "__main__":
    main()
