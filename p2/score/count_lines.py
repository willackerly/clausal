#!/usr/bin/env python3
"""Recount the hand-written Lean of one P2 arm, by declaration, and attribute it to the seven functions.

    python3 p2/score/count_lines.py <arm-dir> <audit.json> <out.json>

Counting rule (the same for both arms, and stated so it can be argued with):
  * a CODE line is a non-blank line that is not a comment: `--` lines and everything inside `/- ... -/` and
    docstrings `/-- ... -/` are comments; `import`, `open`, `namespace`, `end`, `section`, `variable`,
    `set_option` lines are BOILERPLATE, counted apart;
  * a scenario proof file is counted from the line after `theorem Spec.inventory.<id> : ... := by` (that line is
    fixed by the task); its header comment is generated;
  * each declaration in lean/Lemmas/ is located by Lean's own declaration ranges (from the audit) and split into
    STATEMENT lines (up to and including the first line holding `:=`, or up to the first `|` match arm) and PROOF
    lines (the rest);
  * a declaration is a LOOP LEMMA if its type mentions a generated loop function (`..._loop`, `..._loop0`, ...),
    a FUNCTION SPEC if it mentions another generated function, a DEFINITION if it is a `def`, an AENEAS/SCALAR
    HELPER if its statement mentions the Aeneas library's monad, scalars or containers (token list below), and
    a PURE HELPER otherwise (facts about lists, naturals and the reference definitions);
  * attribution: a declaration belongs to every function whose scenario proofs reach it (audit closure through
    proofs); EXCLUSIVE lines are reached from one function only, SHARED from several, UNUSED from none.
Rust: code lines of each function's body (`fn` line to closing brace, comments and blanks out); `can_fill` is
counted with `fill_orders`, the struct definitions with nobody.
"""
import json
import re
import sys
from pathlib import Path

SCEN_FN = {"stock_is_sum": "stock_of", "stock_too_big": "stock_of", "find_first_bin": "find_bin",
           "find_no_bin": "find_bin", "restock_adds": "restock", "restock_counts": "restock",
           "take_amount": "take", "take_stock_down": "take", "take_earliest_first": "take",
           "fill_count": "fill_orders", "fill_state": "fill_orders", "fill_at_most": "fill_orders",
           "count_products": "product_count", "count_at_most_bins": "product_count",
           "dominant_found": "dominant_product", "dominant_none": "dominant_product"}
ORDER = ["stock_of", "find_bin", "restock", "take", "fill_orders", "product_count", "dominant_product"]
LIB_TOKENS = re.compile(r"\bok\b|\bloop\b|Result|UScalar|alloc\.vec|Slice\.|saturating_add|checked_add|#usize|#u64|"
                        r"#u32|BitVec|U64\.max|Usize\.max|\.val = \w+\.val ↔")
BOILER = re.compile(r"(import|open|namespace|end|section|variable|set_option|noncomputable section)\b")
MODEL_FN = re.compile(r"inventory\.Warehouse\.(stock_of|find_bin|restock|take|can_fill|fill_orders|product_count|"
                      r"dominant_product)(_loop\d*)*$")
TACTICS = {"step*": r"\bstep\*", "step (single)": r"\bstep\b(?!\*)", "scalar_tac": r"\bscalar_tac\b",
           "omega": r"\bomega\b", "simp/simp_all/simpa": r"\bsimp(_all|a)?\b", "rw": r"\brw\b",
           "by_cases": r"\bby_cases\b", "induction": r"\binduction\b", "rcases/obtain": r"\b(rcases|obtain)\b",
           "loop.spec_decr_nat": r"loop\.spec_decr_nat", "WP.spec_bind": r"WP\.spec_bind",
           "loop_cont/loop_done": r"\bloop_(cont|done)\b"}


def classify_lines(text):
    kinds, in_block = [], 0
    for raw in text.splitlines():
        s = raw.strip()
        if in_block:
            in_block += s.count("/-") - s.count("-/")
            kinds.append("comment")
            in_block = max(in_block, 0)
            continue
        if s.startswith("/-"):
            in_block = s.count("/-") - s.count("-/")
            kinds.append("comment")
            continue
        if not s:
            kinds.append("blank")
        elif s.startswith("--"):
            kinds.append("comment")
        elif BOILER.match(s):
            kinds.append("boiler")
        else:
            kinds.append("code")
    return kinds


def rust_fn_lines(lib: Path):
    lines = lib.read_text().splitlines()
    out, cur, depth = {}, None, 0
    for ln in lines:
        s = ln.strip()
        m = re.match(r"(pub )?fn (\w+)", s)
        if m and cur is None:
            cur, depth = m.group(2), 0
        if cur:
            if s and not s.startswith("//"):
                out[cur] = out.get(cur, 0) + 1
            depth += ln.count("{") - ln.count("}")
            if depth == 0 and "}" in ln:
                cur = None
    out["fill_orders"] = out.get("fill_orders", 0) + out.pop("can_fill", 0)
    total = sum(1 for l in lines if l.strip() and not l.strip().startswith("//"))
    return out, total


def main():
    arm = Path(sys.argv[1]).resolve()
    audit = json.loads(Path(sys.argv[2]).read_text())
    out = Path(sys.argv[3])
    lean = arm / "lean"
    files = {p.stem: p for p in (lean / "Lemmas").glob("*.lean")}
    kinds = {stem: classify_lines(p.read_text()) for stem, p in files.items()}
    texts = {stem: p.read_text().splitlines() for stem, p in files.items()}
    decls = {}
    for d in audit["decls"]:
        if d["start"] is None:
            continue
        stem = d["module"].split(".")[-1]
        k = kinds[stem]
        rng = range(d["start"] - 1, d["end"])
        code_idx = [i for i in rng if k[i] == "code"]
        stmt_end = None
        for i in code_idx:
            if texts[stem][i].lstrip().startswith("|") and stmt_end is None:
                stmt_end = i - 1
                break
            if ":=" in texts[stem][i]:
                stmt_end = i
                break
        if stmt_end is None:
            stmt_end = code_idx[-1] if code_idx else d["start"] - 1
        stmt = [i for i in code_idx if i <= stmt_end]
        prf = [i for i in code_idx if i > stmt_end]
        stmt_text = "\n".join(texts[stem][i] for i in stmt)
        mf = [x for x in d["model_fns_in_type"] if MODEL_FN.match(x)]
        if d["decl_kind"] == "def":
            cat = "definition"
        elif any(re.search(r"_loop\d*(_loop\d*)?$", x) for x in mf):
            cat = "loop lemma"
        elif mf:
            cat = "function spec"
        elif LIB_TOKENS.search(stmt_text):
            cat = "Aeneas/scalar helper"
        else:
            cat = "pure helper"
        decls[d["name"]] = {"name": d["name"], "file": stem, "start": d["start"], "end": d["end"], "category": cat,
                            "statement_lines": len(stmt), "proof_lines": len(prf), "code_lines": len(code_idx),
                            "model_fns": mf, "used_by": set()}
    covered = {(v["file"], i) for v in decls.values() for i in range(v["start"] - 1, v["end"])}
    other_code = sum(1 for stem, k in kinds.items() for i, x in enumerate(k) if x == "code" and (stem, i) not in covered)
    boiler = sum(1 for k in kinds.values() for x in k if x == "boiler")

    def owner(n):
        parts = n.split(".")
        while parts:
            cand = ".".join(parts)
            if cand in decls:
                return cand
            parts = parts[:-1]
        return None
    for sid, s in audit["scenarios"].items():
        for n in s.get("hand", []):
            o = owner(n)
            if o:
                decls[o]["used_by"].add(SCEN_FN[sid])
    # scenario proof files
    proofs = {}
    for sid in SCEN_FN:
        p = lean / "Spec/Proofs/inventory" / f"{sid}.lean"
        lines = p.read_text().splitlines()
        k = classify_lines(p.read_text())
        i0 = next(i for i, l in enumerate(lines) if l.startswith("theorem Spec."))
        proofs[sid] = sum(1 for i in range(i0 + 1, len(lines)) if k[i] == "code")
    rust, rust_total = rust_fn_lines(arm / "inventory/src/lib.rs")
    vocab_code = sum(1 for x in classify_lines((lean / "Vocab/Inventory.lean").read_text()) if x == "code")
    # aggregate
    cats = {}
    for v in decls.values():
        c = cats.setdefault(v["category"], {"decls": 0, "statement_lines": 0, "proof_lines": 0})
        c["decls"] += 1
        c["statement_lines"] += v["statement_lines"]
        c["proof_lines"] += v["proof_lines"]
    per_fn = {}
    for fn in ORDER:
        own_fns = {f"inventory.Warehouse.{fn}"} | ({"inventory.Warehouse.can_fill"} if fn == "fill_orders" else set())
        mine = [v for v in decls.values() if fn in v["used_by"]]
        loops = [v for v in decls.values() if v["category"] == "loop lemma"
                 and any(re.sub(r"(_loop\d*)+$", "", x) in own_fns for x in v["model_fns"])]
        specs = [v for v in decls.values() if v["category"] == "function spec"
                 and any(x in own_fns for x in v["model_fns"])]
        helpers = [v for v in mine if v["category"] not in ("loop lemma", "function spec")]
        f = per_fn[fn] = {
            "rust_code_lines": rust.get(fn, 0),
            "scenario_proof_lines": sum(proofs[s] for s in SCEN_FN if SCEN_FN[s] == fn),
            "loop_lemmas": len(loops),
            "loop_lemma_statement_lines": sum(v["statement_lines"] for v in loops),
            "loop_lemma_proof_lines": sum(v["proof_lines"] for v in loops),
            "spec_lines": sum(v["code_lines"] for v in specs),
            "helper_lines_exclusive": sum(v["code_lines"] for v in helpers if v["used_by"] == [fn] or v["used_by"] == {fn}),
            "helper_lines_shared": sum(v["code_lines"] for v in helpers if len(v["used_by"]) > 1),
            "lines_needed": sum(v["code_lines"] for v in mine),
            "decls_needed": len(mine),
        }
        f["own_lines"] = (f["loop_lemma_statement_lines"] + f["loop_lemma_proof_lines"] + f["spec_lines"]
                          + f["helper_lines_exclusive"] + f["scenario_proof_lines"])
        f["own_lean_per_rust"] = round(f["own_lines"] / f["rust_code_lines"], 1) if f["rust_code_lines"] else None
        f["needed_lean_per_rust"] = round((f["lines_needed"] + f["scenario_proof_lines"]) / f["rust_code_lines"], 1) \
            if f["rust_code_lines"] else None
    lemma_code = sum(v["code_lines"] for v in decls.values()) + other_code
    proof_total = sum(proofs.values())
    unused = [v["name"] for v in decls.values() if not v["used_by"]]
    shared = [v["name"] for v in decls.values() if len(v["used_by"]) > 1]
    tactic_counts = {}
    def code_only(path):
        t = path.read_text()
        return "\n".join(l for l, k in zip(t.splitlines(), classify_lines(t)) if k == "code")
    alltext = "\n".join(code_only(p) for p in files.values()) + "\n" + "\n".join(
        code_only(lean / "Spec/Proofs/inventory" / f"{s}.lean") for s in SCEN_FN)
    for k, pat in TACTICS.items():
        tactic_counts[k] = len(re.findall(pat, alltext))
    summary = {
        "arm": arm.name, "rust_code_lines": rust_total, "vocab_code_lines_not_written_by_arm": vocab_code,
        "lemma_files": len(files), "lemma_code_lines": lemma_code, "lemma_boilerplate_lines": boiler,
        "lemma_code_outside_declarations": other_code,
        "scenario_proof_lines": proof_total, "scenario_proof_min": min(proofs.values()),
        "scenario_proof_max": max(proofs.values()),
        "hand_written_lean": lemma_code + proof_total,
        "lean_per_rust_code_line": round((lemma_code + proof_total) / rust_total, 2),
        "lean_per_rust_code_line_with_glossary": round((lemma_code + proof_total + vocab_code) / rust_total, 2),
        "declarations": len(decls), "theorems": sum(1 for v in decls.values() if v["category"] != "definition"),
        "definitions": sum(1 for v in decls.values() if v["category"] == "definition"),
        "loop_lemmas": sum(1 for v in decls.values() if v["category"] == "loop lemma"),
        "by_category": cats, "unused_declarations": unused, "shared_declarations": shared,
        "tactic_occurrences": tactic_counts,
    }
    for v in decls.values():
        v["used_by"] = sorted(v["used_by"])
    out.write_text(json.dumps({"summary": summary, "per_function": per_fn, "proof_lines": proofs,
                               "declarations": sorted(decls.values(), key=lambda v: (v["file"], v["start"]))}, indent=1))
    print(json.dumps(summary, indent=1, ensure_ascii=False))
    for fn, f in per_fn.items():
        print(fn, f)


if __name__ == "__main__":
    main()
