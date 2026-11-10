"""slicegen report: verdicts, out/graph.json (refinement graph, schema v2), out/report.md, terminal report.

Also: `steps` (cucumber regex identity check) and `review` (glossary sign-off).
"""
from __future__ import annotations

import datetime
import hashlib
import json
import re

from . import emit, graphlint
from .core import RULE_VERSION, Bound, Problem, sha
from .pipeline import LEAN, OUT, ROOT, State, parse_search, proof_module, proof_path, proofs_state, spec_digest, wants_proof

STD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
# constants a generated statement may mention besides glossary definitions and the When's call
STRUCTURAL = {"Exists", "And", "Eq", "Prod", "Prod.mk", "Unit", "List.cons", "List.nil", "Nat", "OfNat.ofNat",
              "instOfNatNat", "Aeneas.Std.Result", "Aeneas.Std.Result.ok", "Aeneas.Std.core.result.Result"}
DEF_SIZE_MAX = 40          # warning threshold for a glossary definition, in expression nodes (DESIGN.md 4.1)


# --------------------------------------------------------------------------- inputs

def vocab_defs(gloss=None) -> dict:
    """<Namespace>.<name> -> {text, line, end, file} read from the glossary's `vocab_files`
    (display and digests only)."""
    files = (gloss.raw.get("vocab_files") if gloss else None) or {"Vocab": "lean/Wallet/Vocab.lean"}
    out = {}
    for ns, rel in files.items():
        lines = (ROOT / rel).read_text().splitlines()
        i = 0
        while i < len(lines):
            m = re.match(r"(?:@\[\w+\]\s*)?(?:def|abbrev)\s+(\w+)\s*(.*)$", lines[i])
            if m:
                j, body = i + 1, [m.group(2)]
                while j < len(lines) and lines[j].startswith(" "):
                    body.append(lines[j].strip())
                    j += 1
                out[f"{ns}.{m.group(1)}"] = {"text": " ".join(body), "line": i + 1, "end": j, "file": rel}
                i = j
            else:
                i += 1
    return out


def steps_rs() -> dict:
    """glossary id -> (kind, regex, line) from the cucumber step file."""
    p = ROOT / "wallet-bdd" / "tests" / "bdd.rs"
    if not p.exists():
        return {}
    out = {}
    text = p.read_text()
    for m in re.finditer(r'// glossary: (\S+)\s*\n\s*#\[(given|when|then)\(regex = r"(.*)"\)\]', text):
        out[m.group(1)] = (m.group(2), m.group(3), text[:m.start()].count("\n") + 1)
    return out


def rust_readings() -> dict:
    """glossary id -> {name, text, line, end}: the Rust predicate for each Given/Then phrase (wallet-bdd/src/lib.rs)."""
    p = ROOT / "wallet-bdd" / "src" / "lib.rs"
    if not p.exists():
        return {}
    text = p.read_text()
    out = {}
    for m in re.finditer(r"// glossary: (\S+)[^\n]*\n(pub fn (\w+)\(.*?\n\})", text, re.S):
        a = text[:m.start(2)].count("\n") + 1
        out[m.group(1)] = {"name": m.group(3), "text": m.group(2), "line": a, "end": a + m.group(2).count("\n")}
    return out


def load_signoff() -> dict:
    p = ROOT / "glossary.signoff.json"
    return json.loads(p.read_text()) if p.exists() else {}


def _status(element) -> str:
    sts = [s["result"] for s in element["steps"]]
    failed = [r for r in sts if r["status"] == "failed"]
    if failed:
        return "givenFalse" if "GIVEN-FALSE" in failed[0].get("error_message", "") else "fail"
    return "pass" if all(r["status"] == "passed" for r in sts) else "skipped"


def load_cucumber():
    """(basename, line) -> status in {pass, fail, givenFalse, skipped}; None if the runner did not run."""
    p = OUT / "cucumber.json"
    if not p.exists():
        return None
    out = {}
    for f in json.loads(p.read_text()):
        base = f["uri"].rsplit("/", 1)[-1]
        for e in f.get("elements", []):
            out[(base, e["line"])] = _status(e)
    return out


def load_replay() -> dict:
    """scenario id -> status of its counterexample replayed on the compiled Rust."""
    p = OUT / "cucumber-replay.json"
    if not p.exists():
        return {}
    return {e["name"]: _status(e) for f in json.loads(p.read_text()) for e in f.get("elements", [])}


def load_readings(st, search):
    """glossary id -> {n, agree, first}: Lean definition vs Rust predicate on the argument grid.
    None if the Rust side did not run."""
    p = OUT / "readings.tsv"
    lean = search.get("__phrases__", {})
    if not p.exists():
        return None
    rust = dict(l.split("\t") for l in p.read_text().splitlines() if l)
    rows = emit.phrase_grid_rows(st.gloss)
    out = {}
    for id_, args in rows.items():
        a, b = lean.get(id_, ""), rust.get(id_, "")
        if len(a) != len(args) or len(b) != len(args):
            out[id_] = {"n": len(args), "agree": 0, "first": f"not evaluated on both sides (Lean {len(a)}, Rust {len(b)} of {len(args)} points)"}
            continue
        diff = [k for k in range(len(args)) if a[k] != b[k]]
        first = None
        if diff:
            k = diff[0]
            first = f"args ({'; '.join(args[k])}): Lean says {'true' if a[k] == '1' else 'false'}, Rust says {'true' if b[k] == '1' else 'false' if b[k] == '0' else 'not understood'}"
        out[id_] = {"n": len(args), "agree": len(args) - len(diff), "first": first}
    return out


def load_audit():
    p = OUT / "audit.log"
    if not p.exists():
        return None
    for line in p.read_text().splitlines():
        if line.startswith("AUDIT\t"):
            return json.loads(line.split("\t", 1)[1])
    return None


def load_mutation():
    p = ROOT / "mutation" / "results.json"
    return json.loads(p.read_text()) if p.exists() else None


def proof_block(id_: str):
    """(text, first line, last line, path relative to slice/) of `theorem <id>` in its proof module."""
    p = proof_path(id_)
    if not p.exists():
        return None
    lines = p.read_text().splitlines()
    for i, l in enumerate(lines):
        if re.match(rf"theorem {re.escape(id_)}\s*:", l):
            j = len(lines)
            while j > i + 1 and not lines[j - 1].strip():
                j -= 1
            return "\n".join(lines[i:j]), i + 1, j, str(p.relative_to(ROOT))
    return None


def decl_block(path, head: str):
    """(text, first line, last line) of the declaration starting with `head` up to the next blank line."""
    lines = path.read_text().splitlines()
    for i, l in enumerate(lines):
        if l.startswith(head):
            j = i
            while j < len(lines) and lines[j].strip():
                j += 1
            return "\n".join(lines[i:j]), i + 1, j
    return None


def lean_fn_block(lean_name: str, lean_file: str = "Generated/Wallet.lean"):
    lines = (LEAN / lean_file).read_text().splitlines()
    short = lean_name.split(".", 1)[1]
    for i, l in enumerate(lines):
        if l.strip() == f"def {short}" or l.startswith(f"def {short} "):
            j = i
            while j < len(lines) and lines[j].strip():
                j += 1
            return "\n".join(lines[i:j]), i + 1, j
    return lean_name, 1, 1


def derived_theorem(name: str):
    """(statement text, whole text, first line, last line) of a theorem generated into Run/Audit.lean."""
    blk = decl_block(LEAN / "Run" / "Audit.lean", f"theorem {name} :")
    if not blk:
        return None
    m = re.match(r"theorem \S+ : (.*?)\s*:=", blk[0], re.S)
    return (" ".join(m.group(1).split()) if m else name), blk[0], blk[1], blk[2]


def generator_sha() -> str:
    h = hashlib.sha256()
    for p in sorted((ROOT / "slicegen").glob("*.py")):
        h.update(p.read_bytes())
    return h.hexdigest()[:12]


def toolchain() -> dict:
    prov = json.loads((LEAN / "provenance.json").read_text())
    man = json.loads((LEAN / "lake-manifest.json").read_text())
    mathlib = next((p.get("rev", "") for p in man.get("packages", []) if p.get("name") == "mathlib"), "")
    return {"lean": (LEAN / "lean-toolchain").read_text().strip(), "mathlib": mathlib,
            "aeneas": prov["aeneas"], "charon": prov["charon"], "rustc": prov["rustc"],
            "generator": f"slicegen {generator_sha()} ({RULE_VERSION})"}


# --------------------------------------------------------------------------- verdicts

def thm(audit, name) -> dict:
    return (audit or {}).get("theorems", {}).get(name) or {}


def clean(audit, name) -> bool:
    """A theorem counts only if it exists, IS A THEOREM OF THE EXPECTED TYPE (for a scenario proof: exactly
    `<id>.stmt`, declared in that scenario's proof module), and uses no axiom beyond the standard three."""
    t = thm(audit, name)
    if not (t and t["exists"] and t.get("is_theorem") and t.get("type_ok") and set(t["axioms"]) <= STD_AXIOMS):
        return False
    if name.startswith("Spec.") and name.count(".") == 2:          # a hand-written scenario proof
        return t.get("module") == proof_module(name)
    return True


def axioms(audit, name) -> list:
    return thm(audit, name).get("axioms", [])


def why_not(audit, name, proofs) -> str:
    t = thm(audit, name)
    mod = proof_module(name)
    if not audit:
        return "no audit ran"
    if mod in proofs.get("failed", []):
        return f"the proof does not compile ({proofs['errors'].get(mod, 'see out/proofs.log')})"
    if not t.get("exists"):
        return "no theorem"
    if "sorryAx" in t["axioms"]:
        return "proof incomplete (sorry)"
    if not t.get("type_ok") or not t.get("is_theorem"):
        return f"a constant named {name} exists but its type is NOT `{name}.stmt`, so it proves something else"
    if t.get("module") != mod:
        return f"theorem {name} is declared in {t.get('module')}, not in its proof module {mod}"
    if not set(t["axioms"]) <= STD_AXIOMS:
        return f"non-standard axioms {t['axioms']}"
    return "no satisfiability witness for the Givens"


def row_text(header, cells: dict) -> str:
    return "| " + " | ".join(header) + " |\n| " + " | ".join(str(cells[h]) for h in header) + " |"


class Verdict:
    def __init__(self, sc, r, st, ctx):
        self.sc, self.r = sc, r
        self.flags, self.lines, self.counterexample = [], [], None
        self.rests_on, self.fatal = [], []
        self.rows = []               # [{n, line, cells, model, rust, agree}]
        self.unreviewed, self.used = [], []
        self.trivial, self.frame, self.replay = [], [], None
        self.stmt_missing, self.stmt_extra = [], []
        self.status = self.compute(st, ctx)
        if sc.outline:
            self.expected = sc.expect or "PROVED-FOR-ALL"
        else:
            self.expected = sc.expect or "PROVED-INSTANCE"
        if ctx["strict"] and self.status.startswith("PROVED") and self.unreviewed:
            self.fatal.append(f"--strict: rests on {len(self.unreviewed)} glossary entries with no valid sign-off")
        self.as_expected = self.status == self.expected and not self.fatal

    @property
    def substantive(self):
        """(Thens that say something about the code, all Thens); None if not a proved scenario."""
        if not isinstance(self.r, Bound) or not self.status.startswith("PROVED"):
            return None
        weak = set(self.trivial) | set(self.frame)
        return len([t for t in self.r.thens if t.step.text not in weak]), len(self.r.thens)

    @property
    def headline(self):
        s = self.substantive
        return self.status + (f" ({s[0]} of {s[1]} Thens substantive)" if s and s[0] < s[1] else "")

    def compute(self, st, ctx):
        search, audit, cuc, proofs = ctx["search"], ctx["audit"], ctx["cuc"], ctx["proofs"]
        sc, r, L = self.sc, self.r, self.lines
        base = sc.feature.path.rsplit("/", 1)[-1]
        if isinstance(r, Problem):
            L.append(f"{'' if r.code == r.status else r.code + '  '}{sc.feature.path}:{r.line}: {r.message}")
            L += ["  " + h for h in r.hint.splitlines()]
            L.append("no Lean statement was generated, so nothing was proved or refuted")
            if cuc is not None:
                lines = [ln for ln, _ in sc.rows] if sc.outline else [sc.line]
                res = sorted({cuc.get((base, ln), "not run") for ln in lines})
                L.append(f"tested           cucumber-rs on compiled Rust: {', '.join(res)}"
                         + (" (the undefined step and everything after it are skipped)" if "skipped" in res else ""))
            return r.status
        b: Bound = r
        s = search[b.id]
        tool = st.tool
        # rows: Lean model vs compiled Rust
        for row in s["rows"]:
            rust = cuc.get((base, row["line"])) if cuc is not None else None
            model = {"pass": "pass", "givenFalse": "givenFalse"}.get(row["check"], "fail")
            self.rows.append({**row, "model": model, "rust": rust, "agree": rust is None or rust == model})
        if any(not x["agree"] for x in self.rows):
            self.flags.append("MODEL/GLUE MISMATCH")
            self.fatal.append("MODEL/GLUE MISMATCH")
        if any(x["model"] == "givenFalse" for x in self.rows):
            self.flags.append("ROW OUTSIDE GIVENS")
        if b.hidden:
            self.flags.append("NOT RUNNABLE AS TEST")
        # glossary review state
        for bs in b.all_steps:
            if bs.entry.id not in self.used:
                self.used.append(bs.entry.id)
        used = self.used
        self.unreviewed = [i for i in used if i not in ctx["reviewed"]]
        reviewed = [i for i in used if i in ctx["reviewed"]]
        if self.unreviewed:
            self.flags.append(f"UNREVIEWED GLOSSARY ({len(self.unreviewed)} of {len(used)})")
        # the two readings of each phrase
        rd = ctx["readings"]
        if rd is not None:
            bad_rd = [i for i in used if i in rd and rd[i]["agree"] < rd[i]["n"]]
            if bad_rd:
                self.flags.append("READINGS DISAGREE")
                self.fatal.append("READINGS DISAGREE: " + ", ".join(bad_rd))
        # generator / glossary audit
        vac = s["sat"] is None
        if audit:
            cs = set(audit["stmts"][b.id + ".stmt"]["consts"])
            expected = set(emit.vocab_defs(b)) | set(b.calls)
            allowed = (STRUCTURAL | expected | {w.entry.outcome_type for w in b.whens}
                       | set(b.gloss.raw.get("literal_constants", []))
                       | {x for x in cs if re.fullmatch(r"Spec\..*\.stmt\._proof_\d+", x)}   # side proofs of literals (shared between statements)
                       | {x for x in cs if x.startswith("Aeneas.Std.") and (x.endswith(".ofNat") or re.fullmatch(r"Aeneas\.Std\.[UI]\w+", x))}
                       | {x for x in cs if x.rsplit(".", 1)[0] in {v["lean"] for v in b.gloss.param_types.values()}}
                       | {v["lean"] for v in b.gloss.param_types.values()} | {v["lean"] for v in b.gloss.actors.values()})
            self.stmt_missing = sorted(expected - cs)
            self.stmt_extra = sorted(cs - allowed)
            if self.stmt_missing or self.stmt_extra:
                self.flags.append("GENERATOR-CHECK-FAILED")
                self.fatal.append("GENERATOR-CHECK-FAILED")
            bad_defs = [d for d in emit.vocab_defs(b) if audit["defs"][d]["model_deps"]]
            if bad_defs:
                self.flags.append("GLOSSARY-USES-MODEL")
                self.fatal.append("GLOSSARY-USES-MODEL: " + ", ".join(bad_defs))
            if not vac:
                self.trivial = [t.step.text for k, t in enumerate(b.thens, 1) if clean(audit, f"{b.id}.trivial_{k}")]
                if self.trivial:
                    self.flags.append("TRIVIAL-THEN")
        ft = emit.frame_trivial(b)
        if ft:
            self.flags.append("FRAME-TRIVIAL")
        self.frame = [t.step.text for t, _ in ft]

        about = f"about            the Lean model {', then '.join(w.entry.call for w in b.whens)}, not the Rust source"
        if b.multi:
            about += (f"\n  sequence         {len(b.whens)} Whens run in order, each on the state the one before left; every call must return; "
                      "`the result` in a Then is the LAST When's, and earlier results are otherwise unconstrained")
        if rd is None:
            readings = "not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run"
        else:
            pts = sum(rd[i]["n"] for i in used if i in rd)
            ag = sum(rd[i]["agree"] for i in used if i in rd)
            readings = (f"tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on "
                        f"{ag} of {pts} grid points" + ("" if ag == pts else "  <-- THEY DISAGREE: "
                                                         + "; ".join(f"{i}: {rd[i]['first']}" for i in used if i in rd and rd[i]["agree"] < rd[i]["n"])))
        trust = [f"tool-trusted     model = Rust: {tool['rustc']}, charon {tool['charon']}, aeneas {tool['aeneas']}",
                 f"tool-trusted     Aeneas library models used by {', '.join(b.calls)}: "
                 + (", ".join(dict.fromkeys(m for c in b.calls for m in st.libmodels(c))) or "none"),
                 f"tool-trusted     statement generated by {tool['generator']}; printed for comparison with the scenario"
                 + ("" if not audit else "; constants it uses match the glossary: "
                    + ("yes" if not (self.stmt_missing or self.stmt_extra) else f"NO (missing {self.stmt_missing}, extra {self.stmt_extra})")),
                 (f"human-asserted   {len(reviewed)} of {len(used)} glossary phrases signed off" if reviewed else
                  f"NOT ASSERTED     0 of {len(used)} glossary phrases signed off by anyone")
                 + ("" if not self.unreviewed else f" - UNREVIEWED: {', '.join(self.unreviewed)}"),
                 readings]
        nr = len(self.rows)
        if nr:
            mp = sum(x["model"] == "pass" for x in self.rows)
            if cuc is None:
                tested = f"tested           {mp} of {nr} rows pass on the Lean model; cucumber-rs did not run"
            else:
                rp = sum(x["rust"] == "pass" for x in self.rows)
                agree = "they agree" if all(x["agree"] for x in self.rows) else "THEY DISAGREE"
                tested = (f"tested           {rp} of {nr} rows pass on compiled Rust (cucumber-rs); "
                          f"{mp} of {nr} pass on the Lean model; {agree}")
        else:
            tested = "tested           no rows could be evaluated (an actor has no constructive Given)"
        searched = f"tested           boundary grid on the Lean model: {s['tried']} inputs, " + (
            "no counterexample" if not s["bad"] else "counterexample found")
        human = ["human-asserted"] if reviewed else []

        if vac:
            if clean(audit, b.id + ".unsat"):
                L.append(f"kernel-checked   theorem {b.id}.unsat: no input satisfies all the Givens; axioms {', '.join(axioms(audit, b.id + '.unsat'))}")
                L.append("meaning          the scenario is true of nothing; any proof of it would be worthless")
                L += [about] + trust[2:] + [tested]
                self.rests_on = ["kernel-checked", "tool-trusted"] + human
                return "VACUOUS"
            L.append(f"tested           no input satisfying the Givens among the rows and {s['tried']} grid inputs; "
                     f"kernel proof of unsatisfiability failed")
            self.rests_on = ["tested"]
            return "VACUOUS-SUSPECTED"
        if s["bad"]:
            bad = s["bad"]
            hdr = [n for n, _ in emit.search_vars(b)]
            kernel = clean(audit, b.id + ".refuted")

            def fill(t):
                for n, v in bad["values"].items():
                    t = t.replace(f"<{n}>", v)
                return t
            when = fill("; then ".join(w.step.text for w in b.whens))
            failed = [fill(t.step.text) for t, bit in zip(b.thens, bad["thens"]) if bit == "0"]
            held = [fill(t.step.text) for t, bit in zip(b.thens, bad["thens"]) if bit == "1"]
            # the same input on the compiled Rust
            if cuc is None or b.hidden:
                self.replay = None
            else:
                got = ctx["replay"].get(b.id)
                self.replay = "reproduced" if got == "fail" else f"NOT reproduced (Rust: {got or 'not run'})"
                if got != "fail":
                    self.flags.append("MODEL/GLUE MISMATCH")
                    self.fatal.append("MODEL/GLUE MISMATCH: the counterexample found on the Lean model does not fail on the compiled Rust")
            self.counterexample = {"values": bad["values"], "returned": bad["returned"], "check": bad["check"],
                                   "failed_thens": failed, "held_thens": held, "kernel_checked": kernel,
                                   "replayed_on_rust": self.replay}
            if kernel:
                L.append(f"kernel-checked   theorem {b.id}.refuted : ¬ {b.id}.stmt; axioms {', '.join(axioms(audit, b.id + '.refuted'))}")
            elif b.multi:
                L.append("tested           counterexample found on the Lean model; no kernel confirmation is generated for a multi-When scenario")
            else:
                L.append("tested           counterexample found on the Lean model; kernel confirmation attempted and FAILED"
                         + (" (the call contains a loop: the generated script can only use a hand-proved loop lemma, "
                            "and none says enough at this input)" if any(st.has_loop(c) for c in b.calls) else ""))
            w = [max(len(h), len(bad["values"][h])) for h in hdr]
            L.append("counterexample   | " + " | ".join(h.ljust(n) for h, n in zip(hdr, w)) + " |")
            L.append("                 | " + " | ".join(bad["values"][h].ljust(n) for h, n in zip(hdr, w)) + " |")
            L.append(f"                 When {when}  =>  returned {bad['returned']}")
            L.append("                 failed Then: " + "; ".join(f'"{t}"' for t in failed))
            if held:
                L.append("                 held   Then: " + "; ".join(f'"{t}"' for t in held))
            if self.replay:
                L.append(f"tested           the same input on the compiled Rust (cucumber-rs): {self.replay}")
            L += [about] + trust + [tested, searched]
            if self.rows and all(x["model"] == "pass" for x in self.rows):
                L.append("note             every Examples row passes; the examples alone would not have caught this")
            self.rests_on = (["kernel-checked"] if kernel else []) + ["tool-trusted", "tested"] + human
            return "REFUTED" if kernel else "COUNTEREXAMPLE"
        proved = clean(audit, b.id) and clean(audit, b.id + ".sat")
        if proved:
            pb = proof_block(b.id)
            n = len(pb[0].splitlines()) - 1 if pb else 0
            L.append(f"kernel-checked   theorem {b.id} : {b.id}.stmt (type checked by the audit; {n}-line proof, {pb[3]}:{pb[1]}); "
                     f"axioms {', '.join(axioms(audit, b.id))}; Givens satisfiable ({b.id}.sat)")
            L.append("scope            " + ("every input satisfying the Givens" if b.scope == "universal"
                                              else "THIS input only (plain Scenario: the values are literals)"))
            L += [about] + trust + [tested]
            if self.trivial:
                L.append("flag             TRIVIAL-THEN: follows from the Givens alone, whatever the code does: "
                         + "; ".join(f'"{t}"' for t in self.trivial))
            if self.frame:
                L.append("flag             FRAME-TRIVIAL: the call does not return this actor, so the Then compares it with itself: "
                         + "; ".join(f'"{t}"' for t in self.frame))
            self.rests_on = ["kernel-checked", "tool-trusted"] + human + (["tested"] if nr else [])
            return "PROVED-FOR-ALL" if b.scope == "universal" else "PROVED-INSTANCE"
        L.append(f"not proved       {why_not(audit, b.id, proofs)}")
        L += [about] + trust + [tested, searched]
        self.rests_on = ["tested", "tool-trusted"] + human
        return "TESTED-ONLY"


def coverage(st, verdicts, audit) -> list:
    """Per model function: do the PROVED universal scenarios cover every input?
    [{call, covered, groups: [{name, ids, theorem_ok, all_proved, unproved}], scenarios: [(id, name, status)]}]"""
    status = {v.sc.id: v for v in verdicts}
    out = []
    groups = emit.coverage_groups(st.bounds)
    for call in st.model_fns:
        gs = []
        for g in groups:
            if g["call"] != call:
                continue
            unproved = [i for i in g["ids"] if status[i].status != "PROVED-FOR-ALL"]
            gs.append({"name": g["name"], "ids": g["ids"], "theorem_ok": clean(audit, g["name"]),
                       "axioms": axioms(audit, g["name"]), "unproved": unproved})
        scs = [(v.sc.id, v.sc.name, v.headline) for v in verdicts if isinstance(v.r, Bound) and call in v.r.calls]
        out.append({"call": call, "covered": any(g["theorem_ok"] and not g["unproved"] for g in gs), "groups": gs, "scenarios": scs})
    return out


def mutation_summary(mut) -> dict | None:
    """{current, by_fn: {rust fn: (survived, total)}, survivors: [...], total, killed_by_scenarios, at}"""
    if not mut:
        return None
    by_fn = {}
    for m in mut["mutants"]:
        s, t = by_fn.get(m["fn"], (0, 0))
        by_fn[m["fn"]] = (s + (not m["killed_by_scenarios"]), t + 1)
    return {"current": mut.get("spec_digest") == spec_digest(), "by_fn": by_fn, "at": mut.get("generated_at"),
            "total": len(mut["mutants"]), "killed": sum(m["killed_by_scenarios"] for m in mut["mutants"]),
            "survivors": [m for m in mut["mutants"] if not m["killed_by_scenarios"]]}


# --------------------------------------------------------------------------- graph (schema v2)

ALL, NA = {"quantifier": "all"}, {"quantifier": "n/a"}
SARIF = {"PROVED-FOR-ALL": "pass", "PROVED-INSTANCE": "pass", "REFUTED": "fail", "COUNTEREXAMPLE": "fail", "VACUOUS": "fail",
         "UNBOUND": "notApplicable", "AMBIGUOUS": "notApplicable", "UNSUPPORTED": "notApplicable", "TESTED-ONLY": "open",
         "VACUOUS-SUSPECTED": "review"}


def dg(text: str) -> dict:
    return {"alg": "sha256-text", "value": sha(text)}


def inst(n: int, method: str) -> dict:
    return {"quantifier": "instances", "n": n, "method": method}


def ev(kind, by, run=None, artifact=None, scope=None, axioms=None, witness=None, detail=None, method=None):
    e = {"kind": kind, "by": by}
    for k, v in (("run", run), ("artifact", artifact), ("scope", scope), ("axioms", axioms), ("witness", witness),
                 ("detail", detail), ("method", method)):
        if v is not None:
            e[k] = v
    return e


def src(file, a=None, b=None):
    s = {"file": file}
    if a:
        s["line_start"], s["line_end"] = a, b or a
    return s


class Graph:
    def __init__(self):
        self.nodes, self.edges = {}, {}

    def node(self, id_, kind, language, text, origin, source=None, impls=None, attrs=None, metrics=None, budgets=None):
        if id_ in self.nodes:
            return id_
        iface = {"language": language, "text": text, "text_complete": True, "identity": dg(text)}
        for k, v in (("source", source), ("metrics", metrics), ("budgets", budgets)):
            if v:
                iface[k] = v
        n = {"id": id_, "kind": kind, "status": "proposed", "origin": origin, "reviews": [], "interface": iface,
             "implementations": impls or []}
        if attrs:
            n["attrs"] = attrs
        self.nodes[id_] = n
        return id_

    def stamp(self, id_, end="interface", impl=None):
        n = self.nodes[id_]
        if end == "implementation":
            im = next(i for i in n["implementations"] if i["id"] == impl)
            return {"node": id_, "end": "implementation", "implementation": impl, "digest": im["digest"]}
        return {"node": id_, "end": "interface", "digest": n["interface"]["identity"]}

    def realise(self, id_, impl, evidence):
        """Attach `realises` evidence to an implementation, stamped with the interface it realises and itself."""
        im = next(i for i in self.nodes[id_]["implementations"] if i["id"] == impl)
        for x in evidence:
            x["inputs"] = [self.stamp(id_), self.stamp(id_, "implementation", impl)]
        im["realises"] += evidence

    def edge(self, frm, to, relation, evidence, from_impl=None, to_impl=None, occurrences=None, attrs=None, from_end=None):
        """Every evidence entry is stamped with the digests of the two node ends it is about."""
        id_ = f"{relation}:{frm}{'[' + from_impl + ']' if from_impl else ''}->{to}"
        ins = [self.stamp(frm, "implementation", from_impl) if from_impl else self.stamp(frm),
               self.stamp(to, "implementation", to_impl) if to_impl else self.stamp(to)]
        for x in evidence:
            x.setdefault("inputs", ins)
        e = self.edges.get(id_)
        if e is None:
            e = {"id": id_, "from": frm, "to": to, "relation": relation, "evidence": []}
            if from_impl:
                e["from_end"], e["from_implementation"] = "implementation", from_impl
            elif from_end or relation == "uses":
                e["from_end"] = "interface"
            if to_impl:
                e["to_end"] = "implementation"
            if attrs:
                e["attrs"] = attrs
            self.edges[id_] = e
        for x in evidence:
            if x not in e["evidence"]:
                e["evidence"].append(x)
        if occurrences:
            e.setdefault("occurrences", [])
            e["occurrences"] += [o for o in occurrences if o not in e["occurrences"]]
        return id_


def signoff_ok(so: dict, g: Graph, phrase_id: str, target_id: str) -> bool:
    return bool(so) and so.get("phrase") == g.nodes[phrase_id]["interface"]["identity"]["value"] \
        and so.get("target") == g.nodes[target_id]["interface"]["identity"]["value"]


def glossary_nodes(st, g: Graph, audit, vdefs, author) -> dict:
    """Phrase nodes and what they bind to. Returns glossary id -> (phrase node, target node)."""
    gl = st.gloss
    out = {}
    for e in gl.entries:
        text = f"{e.kind.capitalize()} {e.phrase}    [applies to: {', '.join(e.args)}]"
        pid = g.node(f"phrase:{e.id}", "phrase", "english", text, author,
                     src(gl.path, gl.text[:gl.text.index("id: " + e.id)].count("\n") + 1),
                     attrs={"step_kind": e.kind, "phrase": e.phrase, "cucumber_regex": e.cucumber_re})
        if e.kind == "when":
            out[e.id] = (pid, f"fn:lean:{e.call}")
        else:
            d = vdefs.get(e.lean, {"text": e.lean, "line": None, "end": None})
            a = (audit or {}).get("defs", {}).get(e.lean, {})
            size = a.get("size")
            g.node(f"def:{e.lean}", "definition", "lean", f"{e.lean} {d['text']}", author,
                   src(d.get("file", "lean/Wallet/Vocab.lean"), d["line"], d["end"]),
                   metrics={"size_tree": size} if size else None,
                   budgets=[{"measure": "expression nodes of a glossary definition (warning threshold, DESIGN.md 4.1)",
                             "value": size, "max": DEF_SIZE_MAX, "within": size <= DEF_SIZE_MAX}] if size else None,
                   attrs={"model_deps": a.get("model_deps", [])})
            out[e.id] = (pid, f"def:{e.lean}")
    return out


def build_graph(st, verdicts, cov, ctx, vdefs, rs, mut) -> dict:
    search, audit, cuc, proofs, readings = ctx["search"], ctx["audit"], ctx["cuc"], ctx["proofs"], ctx["readings"]
    g: Graph = ctx["graph"]
    bind_target, signoff = ctx["bind_target"], ctx["signoff"]
    tool, gl = st.tool, st.gloss
    author = {"by": gl.raw.get("authorship", {}).get("hand_written", "model:unrecorded")}
    gen = {"by": "tool:slicegen", "run": "run:slicegen"}
    rust_src = {}

    def rust_lines_of(fn):
        key = (fn.get("crate", "wallet"), fn["source"]["file"])
        if key not in rust_src:
            rust_src[key] = (ROOT / key[0] / key[1]).read_text().splitlines()
        return rust_src[key]
    grid = sum(search[b.id]["tried"] for b in st.bounds)
    runs = [
        {"id": "run:slicegen", "tool": "slicegen", "version": tool["generator"]},
        {"id": "run:translate", "tool": "charon+aeneas", "version": tool["aeneas"],
         "toolchain": {"charon": tool["charon"], "aeneas": tool["aeneas"], "rustc": tool["rustc"]}},
        {"id": "run:lean", "tool": "lake build + Run/Audit.lean (Lean kernel, Bdd.Audit)", "version": tool["lean"],
         "toolchain": {"lean": tool["lean"], "mathlib": tool["mathlib"]},
         "config": {"proof_modules_compiled": len(proofs["built"]), "proof_modules_failed": proofs["failed"]},
         "complete": not proofs["failed"]},
        {"id": "run:search", "tool": "Run/Search.lean (Lean interpreter on the model)", "version": tool["lean"],
         "config": {"method": "boundary grid, no random sampling", "grid_inputs_tried": grid}, "complete": True},
    ]
    if cuc is not None:
        runs.append({"id": "run:cucumber", "tool": "cucumber-rs on the compiled Rust", "toolchain": {"rustc": "default stable toolchain"}})

    # ---- functions: Rust -> Lean model
    for name, fn in st.model_fns.items():
        text, a, b = lean_fn_block(name, fn["lean_file"])
        sig = " ".join(text.split(":= do")[0].split())
        lsrc = src("lean/" + fn["lean_file"], a, b)
        rust_lines = rust_lines_of(fn)
        g.node(f"fn:lean:{name}", "function", "lean", sig, {"by": "tool:charon+aeneas", "run": "run:translate"}, lsrc,
               impls=[{"id": "body", "language": "lean-def", "ref": name, "source": lsrc, "digest": dg(text),
                       "complete": True, "realises": []}],
               attrs={"can_fail": fn["can_fail"], "can_diverge": fn["can_diverge"], "generated": True})
        s0 = fn["source"]
        body = "\n".join(rust_lines[s0["begin_line"] - 1:s0["end_line"]])
        rsrc = src(fn.get("crate", "wallet") + "/" + s0["file"], s0["begin_line"], s0["end_line"])
        g.node(f"fn:rust:{fn['rust_name']}", "function", "rust", rust_lines[s0["begin_line"] - 1].strip().rstrip("{").strip(),
               author, rsrc, impls=[{"id": "body", "language": "rust", "ref": fn["rust_name"], "source": rsrc,
                                     "digest": dg(body), "complete": True, "realises": []}])
        agree = [x for v in verdicts if isinstance(v.r, Bound) and name in v.r.calls for x in v.rows if x["rust"] is not None]
        evs = [ev("tool-trusted", "tool:charon+aeneas", "run:translate", "lean/provenance.json", ALL,
                  detail=f"{tool['rustc']}; charon {tool['charon']}; aeneas {tool['aeneas']}; the translation is not proved correct")]
        if agree:
            evs.append(ev("tested", "tool:cucumber-rs+lean-eval", "run:cucumber", "out/cucumber.json, out/search.log",
                          inst(len(agree), "examples"),
                          detail=f"{sum(x['agree'] for x in agree)} of {len(agree)} example rows give the same result on compiled Rust and on the Lean model"))
        g.edge(f"fn:lean:{name}", f"fn:rust:{fn['rust_name']}", "translates", evs, from_impl="body", to_impl="body")
        for c in st.libmodels(name):
            rust = gl.raw.get("library_models", {}).get(c)
            g.node(f"fn:lean:{c}", "function", "lean", c, {"by": "human:aeneas-authors"},
                   attrs={"library_model": True, "hand_written_in": "Aeneas Lean library", "aeneas": tool["aeneas"]})
            g.node(f"fn:rust:std:{rust}", "function", "rust", rust, {"by": "human:rust-std-authors"}, attrs={"std": True})
            g.edge(f"fn:lean:{c}", f"fn:rust:std:{rust}", "models",
                   [ev("tool-trusted", "tool:aeneas-library", "run:translate", f"aeneas {tool['aeneas']}", ALL,
                       detail="hand-written Lean model shipped with Aeneas; std's Rust body is not translated")])
            g.edge(f"fn:lean:{name}", f"fn:lean:{c}", "uses",
                   [ev("tool-trusted", "tool:lean-audit", "run:lean", name, NA,
                       detail="the constant occurs in the elaborated definition, or in a model function it calls (read from the environment by Bdd.Audit)")],
                   from_impl="body")

    # ---- glossary: phrase -> Lean definition / model function (first reading), -> Rust predicate (second reading)
    rr = rust_readings()
    regex_ok = {e.id: (rs.get(e.id, (None, None, 0))[1] == e.cucumber_re) for e in gl.entries}
    binds = {}
    for e in gl.entries:
        pid, target = bind_target[e.id]
        so = signoff.get(e.id, {})
        ok = e.id in ctx["reviewed"]
        binds[e.id] = g.edge(pid, target, "binds",
                             [ev("human-asserted", f"human:{so['reviewer']}", artifact=f"glossary.signoff.json#{e.id}", scope=NA,
                                 detail=f"signed off {so.get('date')}")] if ok else [],
                             attrs={"args": e.args, "reading": "Lean (the one statements are generated from)",
                                    "signoff": "valid" if ok else "changed since sign-off" if so else "none"})
        if e.id in rr:
            r = rr[e.id]
            rid = g.node(f"def:rust:wallet_bdd::{r['name']}", "definition", "rust", r["text"], author,
                         src("wallet-bdd/src/lib.rs", r["line"], r["end"]))
            g.edge(pid, rid, "binds", [], attrs={"reading": "Rust (asserted by the cucumber step)", "signoff": "none",
                                                 "step_regex_identical_to_glossary": regex_ok[e.id]},
                   occurrences=[{"role": "cucumber step", "at": src("wallet-bdd/tests/bdd.rs", rs[e.id][2])}] if e.id in rs else None)
            if readings is not None and e.id in readings:
                q = readings[e.id]
                g.edge(target, rid, "equivalent",
                       [ev("tested", "tool:lean-eval+rust-eval", "run:cucumber", "out/search.log, out/readings.tsv",
                           inst(q["n"], "argument-grid"),
                           detail=f"{q['agree']} of {q['n']} grid points give the same truth value"
                                  + (f"; first disagreement: {q['first']}" if q["first"] else ""))])

    # ---- features, scenarios, statements
    out_verdicts = []
    stmt_file = LEAN / "Wallet" / "Statements.lean"
    for f in st.features:
        g.node(f"group:feature:{f.slug}", "group", "gherkin", f"Feature: {f.name}", author, src(f.path, f.line, len(f.lines)))
    stmt_node = {}
    for v in verdicts:
        sc = v.sc
        sid = g.node(f"scenario:{sc.id}", "claim", "gherkin", sc.text, author, src(sc.feature.path, sc.line, sc.end_line),
                     attrs={"scope": "universal" if sc.outline else "instance", "tags": sc.tags})
        g.edge(f"group:feature:{sc.feature.slug}", sid, "contains",
               [ev("tool-trusted", "tool:slicegen", "run:slicegen", RULE_VERSION, NA, detail="Gherkin-subset parser")])
        rec = {"node": sid, "outcome": SARIF[v.status], "code": v.status, "expected": v.expected, "as_expected": v.as_expected,
               "flags": [f for f in v.flags if not f.startswith("UNREVIEWED")] + [f"FATAL: {x}" for x in v.fatal if x not in v.flags],
               "chain": [], "rests_on": v.rests_on, "unreviewed": [], "stale": []}
        if v.counterexample:
            rec["counterexample"] = v.counterexample
        out_verdicts.append(rec)
        if isinstance(v.r, Problem):
            rec["detail"] = f"{v.r.code}: {sc.feature.path}:{v.r.line}: {v.r.message}"
            continue
        b: Bound = v.r
        for bs in b.all_steps:
            g.edge(sid, f"phrase:{bs.entry.id}", "composed_of",
                   [ev("tool-trusted", "tool:slicegen", "run:slicegen", RULE_VERSION, NA,
                       detail="the step text matched this phrase's pattern and no other glossary entry")],
                   occurrences=[{"role": bs.entry.kind, "at": src(sc.feature.path, bs.step.line), "attrs": {"text": bs.step.text}}])
        stmt_text = emit.statement(b)
        blk = decl_block(stmt_file, f"def {b.id}.stmt ")
        impls = []
        pb = proof_block(b.id) if wants_proof(b) else None
        if pb:
            impls = [{"id": "p1", "language": "lean-proof", "ref": b.id, "source": src(pb[3], pb[1], pb[2]), "digest": dg(pb[0]),
                      "complete": clean(audit, b.id), "hidden": True, "metrics": {"size_lines": len(pb[0].splitlines()) - 1},
                      "realises": []}]
        tid = g.node(f"stmt:{b.id}.stmt", "statement", "lean", stmt_text, gen,
                     src("lean/Wallet/Statements.lean", blk[1], blk[2]) if blk else src("lean/Wallet/Statements.lean"),
                     impls=impls, attrs={"scope": b.scope})
        stmt_node[b.id] = tid
        if pb and clean(audit, b.id):
            g.realise(tid, "p1", [ev("kernel-checked", "tool:lean-kernel", "run:lean", b.id,
                                     ALL if b.scope == "universal" else inst(1, "the scenario's literals"), axioms=axioms(audit, b.id),
                                     method="library-module",
                                     detail=f"module {proof_module(b.id)}; the audit checked that the theorem's type is exactly {b.id}.stmt")])
        e_form = g.edge(tid, sid, "formalises", [
            ev("tool-trusted", "tool:slicegen", "run:slicegen", tool["generator"], NA,
               detail="translation rule of DESIGN.md section 5; audit of the constants in the elaborated statement: "
                      + ("passed" if audit and not (v.stmt_missing or v.stmt_extra) else "FAILED or not run"))])
        consts = set((audit or {}).get("stmts", {}).get(b.id + ".stmt", {}).get("consts", []))

        def use_ev(c, what):
            return [ev("tool-trusted", "tool:lean-audit", "run:lean", b.id + ".stmt", NA,
                       detail=f"{what}: the constant occurs in the elaborated statement (read from the environment by Bdd.Audit)")
                    if c in consts else
                    ev("tool-trusted", "tool:slicegen", "run:slicegen", b.id + ".stmt", NA,
                       detail=f"{what}: expected by the generator; NOT confirmed by the audit")]
        for d in emit.vocab_defs(b):
            g.edge(tid, f"def:{d}", "uses", use_ev(d, "a Given/Then"))
        call = b.when.entry.call
        e_uses = [g.edge(tid, f"fn:lean:{c}", "uses", use_ev(c, "a When"), to_impl="body") for c in b.calls]
        e_trs = [f"translates:fn:lean:{c}[body]->fn:rust:{st.model_fns[c]['rust_name']}" for c in b.calls]
        rec["chain"] = [e_form] + [binds[i] for i in v.used] + e_uses + e_trs
        rec["unreviewed"] = [binds[i] for i in v.unreviewed]
        if v.status.startswith("PROVED") and v.unreviewed:
            rec["outcome"] = "review"        # proved, but of a statement whose link to the English nobody has signed off
        s = search[b.id]
        # satisfiability / vacuity / refutation as their own statement nodes
        for suffix, what in ((".sat", "the Givens are jointly satisfiable"), (".unsat", "the Givens are contradictory"),
                             (".refuted", "the negation of the statement")):
            name = b.id + suffix
            dt = derived_theorem(name)
            if not thm(audit, name).get("exists") or not dt:
                continue
            ok = clean(audit, name)
            nid = g.node(f"stmt:{name}", "statement", "lean", dt[0], gen, src("lean/Run/Audit.lean", dt[2], dt[3]),
                         impls=[{"id": "p1", "language": "lean-proof", "ref": name, "source": src("lean/Run/Audit.lean", dt[2], dt[3]),
                                 "digest": dg(dt[1]), "complete": ok, "hidden": True, "realises": []}],
                         attrs={"derived_from_search": True, "meaning": what})
            if ok:
                g.realise(nid, "p1", [ev("kernel-checked", "tool:lean-kernel", "run:lean", name, ALL, axioms=axioms(audit, name),
                                         witness=s["sat"] if suffix == ".sat" else (s["bad"] or {}).get("values"),
                                         method="script-session",
                                         detail="generated proof script, elaborated and kernel-checked inside the audit run; not stored in an .olean")])
            if suffix == ".sat":
                g.edge(tid, nid, "requires", [ev("tool-trusted", "tool:slicegen", "run:slicegen", name, NA,
                                                 detail="non-vacuity side condition of a PROVED verdict: generated from the same Givens")])
            elif suffix == ".unsat":
                g.edge(nid, tid, "refutes", [ev("tool-trusted", "tool:slicegen", "run:slicegen", name, NA,
                                                detail="vacuity, not falsity: generated from the same Givens; the statement holds of no input")],
                       attrs={"how": "vacuity"})
            else:
                g.edge(nid, tid, "refutes", [ev("tool-trusted", "tool:lean-audit", "run:lean", name, NA,
                                                detail=f"the audit checked that the theorem's type is exactly ¬ {b.id}.stmt"
                                                       if thm(audit, name).get("type_ok") else "type NOT confirmed by the audit")],
                       attrs={"how": "falsity"})
        if s["bad"]:
            text = "\n".join(l.strip() for l in emit.replay_feature([b], search).splitlines()[4:]).strip() or json.dumps(s["bad"]["values"])
            cid = g.node(f"example:counterexample:{b.id}", "example", "gherkin", text, {"by": "tool:lean-eval", "run": "run:search"},
                         src("build/replay/replay.feature"), attrs={"values": s["bad"]["values"], "returned": s["bad"]["returned"]})
            evs = [ev("tested", "tool:lean-eval", "run:search", "out/search.log", inst(1, "boundary-grid"),
                      detail=f"on the Lean model the Givens hold and a Then fails; found among {s['tried']} grid inputs")]
            if v.replay:
                evs.append(ev("tested", "tool:cucumber-rs", "run:cucumber", "out/cucumber-replay.json", inst(1, "replay"),
                              detail=f"the same input on the compiled Rust: {v.replay}"))
                g.edge(cid, f"fn:rust:{st.model_fns[call]['rust_name']}", "exercises", [dict(evs[1])], to_impl="body")
            g.edge(cid, tid, "refutes", evs, attrs={"how": "falsity"})
        # example rows
        for x in v.rows:
            rid = g.node(f"example:{b.id}#{x['n']}", "example", "gherkin",
                         row_text(sc.header, x["cells"]) if sc.header else "(the scenario's own literals)",
                         author, src(sc.feature.path, x["line"]))
            e1 = ev("tested", "tool:lean-eval", "run:search", "out/search.log", inst(1, "examples"),
                    detail=f"{x['model']}; returned {x['returned']}")
            g.edge(rid, tid, "instance_of", [dict(e1)])
            g.edge(rid, f"fn:lean:{call}", "exercises", [dict(e1)], to_impl="body")
            if x["rust"] is not None:
                e2 = ev("tested", "tool:cucumber-rs", "run:cucumber", "out/cucumber.json", inst(1, "examples"), detail=x["rust"])
                g.edge(rid, tid, "instance_of", [dict(e2)])
                g.edge(rid, f"fn:rust:{st.model_fns[call]['rust_name']}", "exercises", [dict(e2)], to_impl="body")

    # ---- input coverage per model function
    ms = mutation_summary(mut)
    for c in cov:
        fid = f"fn:lean:{c['call']}"
        chain, unrev = [], []
        for grp in c["groups"]:
            dt = derived_theorem(grp["name"])
            if not dt:
                continue
            nid = g.node(f"stmt:{grp['name']}", "statement", "lean", dt[0], gen, src("lean/Run/Audit.lean", dt[2], dt[3]),
                         impls=[{"id": "p1", "language": "lean-proof", "ref": grp["name"], "source": src("lean/Run/Audit.lean", dt[2], dt[3]),
                                 "digest": dg(dt[1]), "complete": grp["theorem_ok"], "hidden": True, "realises": []}],
                         attrs={"meaning": "the Givens of the listed scenarios, taken together, hold of every input", "scenarios": grp["ids"]})
            if grp["theorem_ok"]:
                g.realise(nid, "p1", [ev("kernel-checked", "tool:lean-kernel", "run:lean", grp["name"], ALL, axioms=grp["axioms"],
                                         method="script-session",
                                         detail="generated proof script, elaborated and kernel-checked inside the audit run; not stored in an .olean")])
            chain.append(g.edge(nid, fid, "covers", [ev("tool-trusted", "tool:slicegen", "run:slicegen", grp["name"], NA,
                                                         detail="the scenarios were grouped by their When phrase and identical variables")]))
            for i in grp["ids"]:
                chain.append(g.edge(nid, stmt_node[i], "requires",
                                    [ev("tool-trusted", "tool:slicegen", "run:slicegen", grp["name"], NA,
                                        detail="one disjunct of the coverage statement is this scenario's Givens; coverage counts only if the scenario is proved")]))
                unrev += [u for v in out_verdicts if v["node"] == f"scenario:{i}" for u in v["unreviewed"]]
        unrev = sorted(set(unrev))
        rust_fn = st.model_fns[c["call"]]["rust_name"]
        flags = []
        if ms and ms["current"] and rust_fn in ms["by_fn"]:
            sv, tot = ms["by_fn"][rust_fn]
            flags.append(f"MUTANTS-SURVIVING-THE-SCENARIOS: {sv} of {tot}")
        out_verdicts.append({
            "node": fid, "outcome": ("review" if unrev else "pass") if c["covered"] else "open",
            "code": "INPUTS-COVERED" if c["covered"] else "INPUTS-NOT-COVERED", "flags": flags, "chain": chain,
            "rests_on": (["kernel-checked", "tool-trusted"] if c["covered"] else []), "unreviewed": unrev, "stale": [],
            "detail": ("every input is covered by the Givens of a proved universal scenario" if c["covered"] else
                       "not shown that every input is covered by a proved universal scenario: "
                       + ("no universal scenario exercises this function" if not c["groups"] else
                          "; ".join(f"{x['name']}: " + ("coverage theorem failed" if not x["theorem_ok"] else "unproved: " + ", ".join(x["unproved"]))
                                    for x in c["groups"])))})
    gr = {"schema": "rosette.refinement-graph/2",
          "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
          "runs": runs, "nodes": list(g.nodes.values()), "edges": list(g.edges.values()), "verdicts": out_verdicts}
    st_ = graphlint.staleness(gr)
    for v in gr["verdicts"]:
        v["stale"] = [e for e in v["chain"] if e in st_["edges"]]
    return gr


# --------------------------------------------------------------------------- report

def md_report(st, verdicts, cov, gr, ctx, vdefs, rs, errs, mut) -> str:
    audit, cuc, readings = ctx["audit"], ctx["cuc"], ctx["readings"]
    tool = st.tool
    gl = st.gloss
    o = ["# Slice: scenario report (wallet and ledger)", "",
         f"Generated {gr['generated_at']} by `slice/run.sh`. Lean `{tool['lean']}`, Aeneas `{tool['aeneas']}`, "
         f"Charon `{tool['charon']}`, `{tool['rustc']}`, {tool['generator']}.", "",
         "Each scenario below is an English claim about one of the Rust crates `slice/wallet` (three straight-line "
         "functions) and `slice/ledger` (loops over a `Vec` and a slice). The claim is turned into a Lean "
         "statement about the Aeneas-generated Lean model of that crate, and the statement is then proved, refuted or "
         "left open. Every link in that chain is labelled with the kind of evidence behind it:", "",
         "| Evidence kind | Meaning here |", "|---|---|",
         "| kernel-checked | Lean's kernel accepted a proof of exactly the stated theorem. Holds for every input the statement quantifies over. |",
         "| tested | Evaluated on particular inputs: Examples rows on the compiled Rust (cucumber-rs) and on the Lean model, a boundary grid on the model, counterexamples replayed on the Rust, and the two readings of each phrase compared on a grid. |",
         "| tool-trusted | Produced by a program whose output is not proved correct: Charon + Aeneas (Rust to Lean), Aeneas's hand-written models of std operations, slicegen (scenario to statement), and the audit that reads facts out of the Lean environment. |",
         "| human-asserted | A person's say-so: that each glossary phrase means its Lean definition. Nothing checks this. It exists only where someone has signed off. |", "",
         "## Summary", "", "| Scenario | Verdict | Expected | Rows on Rust / on model | Flags |", "|---|---|---|---|---|"]
    for v in verdicts:
        rows = (f"{sum(x['rust'] == 'pass' for x in v.rows) if cuc is not None else '-'} / {sum(x['model'] == 'pass' for x in v.rows)} of {len(v.rows)}"
                if v.rows else "-")
        o.append(f"| {v.sc.name} (`{v.sc.feature.path}:{v.sc.line}`) | **{v.headline}** | {v.expected}{'' if v.as_expected else ' - MISMATCH'} "
                 f"| {rows} | {'; '.join(v.flags) or '-'} |")
    ok = all(v.as_expected for v in verdicts) and not errs
    o += ["", ("Every scenario got the verdict it was expected to get." if ok else "**At least one scenario did not get its expected verdict.**"),
          "A scenario tagged `@expect-refuted`, `@expect-unbound` or `@expect-vacuous` is a deliberate negative control.", ""]
    n_unrev_proved = sum(1 for v in verdicts if v.status.startswith("PROVED") and v.unreviewed)
    if n_unrev_proved:
        o += [f"**{n_unrev_proved} proved scenarios rest on glossary entries with no valid sign-off.** A proof shows the Lean "
              "statement holds; that the statement says what the English says is exactly what the sign-off is for. "
              "`./run.sh --strict` makes this a failure.", ""]

    o += ["## How much of each operation the scenarios pin down", "",
          "A green scenario says nothing about inputs outside its Givens. Two measurements of what is left unsaid:", "",
          "1. **Inputs.** For each operation, a generated theorem states that the Givens of its proved universal scenarios, "
          "taken together, hold of every input. If the kernel accepts it, no input falls outside every scenario.",
          "2. **Outputs.** A mutation run (`python3 mutation/run_mutants.py`, not part of `run.sh`) changes the Rust in small "
          "wrong ways and reports which changes no scenario notices.", "",
          "| Operation (Lean model) | Every input covered by a proved scenario? | Scenarios |", "|---|---|---|"]
    for c in cov:
        if c["covered"]:
            gq = next(x for x in c["groups"] if x["theorem_ok"] and not x["unproved"])
            how = f"**yes**: kernel-checked `{gq['name']}` over {len(gq['ids'])} proved scenarios"
        elif not c["groups"]:
            how = "**NOT SHOWN**: no universal scenario exercises it"
        else:
            how = "**NOT SHOWN**: " + "; ".join(
                f"`{x['name']}` ({len(x['ids'])} scenarios): " + ("their Givens do not cover every input" if not x["theorem_ok"] else
                                                                  "not all proved (" + ", ".join(i.rsplit('.', 1)[1] for i in x["unproved"]) + ")")
                for x in c["groups"])
        o.append(f"| `{c['call']}` | {how} | " + "; ".join(f"{i.rsplit('.', 1)[1]}: {s}" for i, _, s in c["scenarios"]) + " |")
    o.append("")
    ms = mutation_summary(mut)
    if not ms:
        o += ["No mutation results found (`mutation/results.json`). Run `python3 mutation/run_mutants.py`.", ""]
    else:
        o += [f"Mutation run of {ms['at']}: {ms['total']} mutants of `wallet/src/lib.rs` and `ledger/src/lib.rs`; **{ms['killed']} noticed by the scenarios, "
              f"{ms['total'] - ms['killed']} not**. " + ("These results are for the current Rust, features, glossary and proofs."
                                                         if ms["current"] else
                                                         "**These results are for an OLDER version of the Rust, features, glossary or proofs; rerun.**"), "",
              "A lost proof means the proof (or a lemma it depends on) no longer compiles; it does not by itself mean the "
              "scenario's statement is false of the mutant. A new counterexample does.", "",
              "| Mutant | Operation | What was changed | Crate unit tests | Examples rows on Rust | Proofs lost | New counterexamples | Verdicts that changed | Noticed by the scenarios |",
              "|---|---|---|---|---|---|---|---|---|"]
        for m in mut["mutants"]:
            o.append(f"| {m['id']} | `{m['fn']}` | {m['description']} | {m['unit_tests']} | {m['rows_on_rust']} | "
                     f"{len(m.get('proof_broke', [])) or 'none'} | {len(m.get('search_found', [])) or 'none'} | {m['proof_layer']} | "
                     f"{'yes' if m['killed_by_scenarios'] else '**NO**'} |")
        o.append("")

    o += ["## Scenarios", ""]
    for v in verdicts:
        sc = v.sc
        o += [f"### {v.headline}: {sc.name}", "", f"`{sc.feature.path}:{sc.line}`  id `{sc.id}`" + (f"  tags `{' '.join(sc.tags)}`" if sc.tags else ""), "",
              "```gherkin", sc.text, "```", ""]
        if isinstance(v.r, Bound):
            o += ["Generated Lean statement (`lean/Wallet/Statements.lean`):", "", "```lean", emit.statement(v.r), "```", ""]
        o += ["```text", f"{v.headline}  {sc.name}"] + ["  " + l for l in v.lines] + ["```", ""]
        if isinstance(v.r, Bound):
            pb = proof_block(v.r.id)
            if pb and v.status.startswith("PROVED"):
                o += [f"Proof (`{pb[3]}`):", "", "```lean", pb[0], "```", ""]
    o += ["## Glossary (the link from English to Lean)", "",
          "Each English phrase and the one Lean definition (or model function) it is bound to. This table, "
          "`lean/Wallet/Vocab.lean` and `lean/Ledger/Vocab.lean` are what a reviewer has to read to trust the step from English to Lean. "
          "The last column compares that Lean definition with a second, independently written reading of the same phrase "
          "(the Rust predicate in `wallet-bdd/src/lib.rs` that the cucumber step asserts) on a grid of arguments. "
          "Agreement does not show that either reading matches the English; disagreement shows that one of them is wrong.", "",
          "| Id | Kind | English phrase | Lean | Definition | Sign-off | Rust step regex identical | Lean vs Rust reading |", "|---|---|---|---|---|---|---|---|"]
    n_unrev = 0
    for e in gl.entries:
        so = ctx["signoff"].get(e.id, {})
        okk = e.id in ctx["reviewed"]
        n_unrev += not okk
        lean = e.lean or e.call
        body = ("`" + vdefs[lean]["text"].replace("|", chr(92) + "|") + "`" if lean in vdefs
                else f"Aeneas-generated model of Rust `{e.rust_fn}`; returns `{', '.join(e.returns)}`")
        if e.kind == "when":
            rd = "n/a (the step calls the real function)"
        elif readings is None:
            rd = "not compared"
        else:
            q = readings.get(e.id)
            rd = "no Rust predicate" if not q else (f"agree on {q['agree']} of {q['n']}" if q["agree"] == q["n"]
                                                    else f"**DISAGREE** on {q['n'] - q['agree']} of {q['n']}: {q['first']}")
        o.append(f"| {e.id} | {e.kind} | {e.phrase} | `{lean}` applied to `{', '.join(e.args)}` | {body} | "
                 f"{'signed off by ' + so['reviewer'] + ' ' + so['date'] if okk else 'UNREVIEWED (changed since sign-off)' if so else 'UNREVIEWED'} | "
                 f"{'yes' if rs.get(e.id, (0, 0, 0))[1] == e.cucumber_re else 'NO' if rs else 'not checked'} | {rd} |")
    o += ["", f"{n_unrev} of {len(gl.entries)} entries are unreviewed. Record a review with "
              "`python3 -m slicegen review <id> --reviewer <name>`; any later change to the phrase, its argument order or its "
              "definition voids it.", ""]
    o += ["## Trusted base", "",
          "- **Rust to Lean**: `lean/Generated/Wallet.lean` and `lean/Generated/Ledger.lean` are produced by Charon + Aeneas "
          "from `wallet/src/lib.rs` and `ledger/src/lib.rs`. "
          "Hashes of inputs and outputs are in `lean/provenance.json`. The theorems are about the Lean models. "
          "A Rust `while` loop becomes a call of Aeneas's `loop` combinator on a separately generated loop-body function.",
          "- **Hand-written loop lemmas** (`lean/Ledger/Lemmas/`, one module per Rust function): not trusted. They are kernel-checked like any proof, "
          "and they appear in no statement; a scenario proof that uses one is still checked against exactly its statement.",
          "- **Aeneas library models** (hand-written Lean standing in for std operations): "
          + "; ".join(f"`{c}` for `{r}`" for c, r in gl.raw.get("library_models", {}).items()) + ".",
          "- **slicegen**: untrusted generator. Defences: Lean type-checks its output; the audit compares the constants in "
          "each elaborated statement with the glossary entries of the scenario's steps; the statement is printed above.",
          "- **The audit** (`lean/Bdd/Audit.lean`, about 120 lines): reads from the Lean environment which axioms each theorem uses, "
          "that each proof's type is exactly its scenario's statement, and which constants statements and definitions mention.",
          "- **Glossary**: `glossary.yaml` + `lean/Wallet/Vocab.lean` + `lean/Ledger/Vocab.lean`. The audit checks that no Given/Then definition "
          "depends on a model function"
          + ("" if not audit else ": " + ("passed for all " + str(len(audit["defs"])) + " definitions."
                                           if not any(d["model_deps"] for d in audit["defs"].values()) else "**FAILED**.")),
          "- **Second reading of each phrase**: the Rust predicates in `wallet-bdd/src/lib.rs`, asserted by the cucumber steps in "
          "`wallet-bdd/tests/bdd.rs`. The step regexes are checked against the glossary; the predicates are compared with the Lean "
          "definitions on a grid of arguments (table above) and by Examples rows giving the same result on both sides.",
          "- **Lean kernel** and the axioms `propext`, `Classical.choice`, `Quot.sound`; **rustc** for everything said about the compiled Rust.", ""]
    o += ["## What this run did not check", "",
          "- That any glossary definition means what its English phrase says. Only a person can.",
          "- A scenario with several Whens says that each call returns and constrains the state after the LAST one "
          "(and the last call's result). Results of earlier Whens are not constrained, no kernel refutation is generated "
          "for such a scenario, and it does not count towards input coverage.",
          "- A counterexample to a scenario about a loop is confirmed in the kernel only if a hand-proved lemma about that loop "
          "says enough at that input (here: the exact-result lemmas in `lean/Ledger/Lemmas/`). Without one the verdict is COUNTEREXAMPLE, not REFUTED.",
          "- The boundary grid is small (the product of each parameter's sample values plus literals and their neighbours); "
          "there is no random sampling and no shrinking. A false scenario whose counterexamples all lie away from the boundaries would be TESTED-ONLY, not REFUTED. "
          "The same holds for the grid on which the two readings of a phrase are compared.",
          "- The trivial-Then check is a `simp`/`scalar_tac` attempt. A Then that follows from the Givens by harder reasoning is not flagged, "
          "and a Then that is true but weaker than the English is invisible to it.",
          "- Input coverage says every input falls under some scenario's Givens. It does not say the Thens of that scenario pin the result down; "
          "that is what the mutation run measures, for the mutants it happens to contain.",
          "- The derived theorems (`.sat`, `.unsat`, `.refuted`, coverage, trivial-Then attempts) are checked by one `lean` run over "
          "`lean/Run/Audit.lean`, not stored as library modules. Trivial-Then attempts are expected to fail; their errors are in `out/audit.log`.",
          "- Staleness is computed from the digests in `out/graph.json`, but every run regenerates everything, so nothing is ever stale here. "
          "`python3 -m slicegen.graphlint out/graph.json --what-if <node-id>` shows what would be.", ""]
    if errs:
        o += ["## Errors", ""] + [f"- {e}" for e in errs] + [""]
    kinds = {}
    for e in gr["edges"]:
        for x in e["evidence"]:
            kinds[x["kind"]] = kinds.get(x["kind"], 0) + 1
    for n in gr["nodes"]:
        for im in n["implementations"]:
            for x in im["realises"]:
                kinds[x["kind"]] = kinds.get(x["kind"], 0) + 1
    o += ["## Refinement graph", "",
          f"`out/graph.json`: {len(gr['nodes'])} nodes, {len(gr['edges'])} edges, {len(gr['verdicts'])} verdicts. Evidence entries by kind: "
          + ", ".join(f"{k} {n}" for k, n in sorted(kinds.items()))
          + f". Edges claimed with no evidence at all: {sum(1 for e in gr['edges'] if not e['evidence'])} "
            "(the unsigned glossary bindings). Schema: `schema/refinement-graph.v2.schema.json`, described in `../docs/SCHEMA.md`.", ""]
    return "\n".join(o)


def cmd_report(st: State, argv) -> int:
    st.tool = toolchain()
    audit, cuc, signoff, vdefs, rs = load_audit(), load_cucumber(), load_signoff(), vocab_defs(st.gloss), steps_rs()
    search = parse_search(st)
    mut = load_mutation()

    def libmodels(fn):
        # everything the function reaches through other model functions (its loop, its loop body, callees)
        info = (audit or {}).get("fns", {}).get(fn, {})
        cs = info.get("closure") or info.get("consts", [])
        return [c for c in st.gloss.raw.get("library_models", {}) if c in cs]
    st.libmodels = libmodels
    # glossary nodes first: a sign-off is valid only for the current digests of the phrase and of what it binds to
    g = Graph()
    author = {"by": st.gloss.raw.get("authorship", {}).get("hand_written", "model:unrecorded")}
    st.has_loop = lambda fn: "Aeneas.Std.loop" in (audit or {}).get("fns", {}).get(fn, {}).get("closure", [])
    for name in st.model_fns:              # When phrases bind to these; build_graph fills in the rest
        lf = "lean/" + st.model_fns[name]["lean_file"]
        text, a, b = lean_fn_block(name, st.model_fns[name]["lean_file"])
        g.node(f"fn:lean:{name}", "function", "lean", " ".join(text.split(":= do")[0].split()),
               {"by": "tool:charon+aeneas", "run": "run:translate"}, src(lf, a, b),
               impls=[{"id": "body", "language": "lean-def", "ref": name, "source": src(lf, a, b),
                       "digest": dg(text), "complete": True, "realises": []}],
               attrs={"can_fail": st.model_fns[name]["can_fail"], "can_diverge": st.model_fns[name]["can_diverge"], "generated": True})
    bind_target = glossary_nodes(st, g, audit, vdefs, author)
    reviewed = {i for i, (p, t) in bind_target.items() if signoff_ok(signoff.get(i, {}), g, p, t)}
    ctx = {"search": search, "audit": audit, "cuc": cuc, "proofs": proofs_state(st), "replay": load_replay(),
           "readings": load_readings(st, search) if cuc is not None else None, "signoff": signoff, "reviewed": reviewed,
           "strict": "--strict" in argv, "graph": g, "bind_target": bind_target}
    verdicts = [Verdict(sc, r, st, ctx) for sc, r in st.results]
    cov = coverage(st, verdicts, audit)
    gr = build_graph(st, verdicts, cov, ctx, vdefs, rs, mut)
    errs = graphlint.schema_errors(gr) + graphlint.lint(gr)
    if audit is None:
        errs.append("out/audit.log has no AUDIT line: the audit did not run")
    bad_regex = [e.id for e in st.gloss.entries if rs and rs.get(e.id, (0, 0, 0))[1] != e.cucumber_re]
    if bad_regex:
        errs.append(f"cucumber step regex differs from the glossary for: {', '.join(bad_regex)}")
    rd = ctx["readings"]
    if rd is not None:
        for e in st.gloss.entries:
            if e.kind != "when" and (e.id not in rd or rd[e.id]["agree"] < rd[e.id]["n"]):
                errs.append(f"the two readings of glossary entry {e.id} disagree or were not both evaluated: "
                            f"{rd.get(e.id, {}).get('first', 'no result')}")
    OUT.mkdir(exist_ok=True)
    (OUT / "graph.json").write_text(json.dumps(gr, indent=1, ensure_ascii=False))
    (OUT / "report.md").write_text(md_report(st, verdicts, cov, gr, ctx, vdefs, rs, errs, mut))
    print()
    for v in verdicts:
        mark = "" if v.as_expected else f"   <-- EXPECTED {v.expected}" + (f"; {'; '.join(v.fatal)}" if v.fatal else "")
        print(f"{v.headline}  {v.sc.name}   ({v.sc.feature.path}:{v.sc.line}){mark}")
        for l in v.lines:
            print("  " + l)
        extra = [f for f in v.flags if f not in ("TRIVIAL-THEN", "FRAME-TRIVIAL")]
        if extra:
            print("  flags            " + "; ".join(extra))
        print()
    print("How much of each operation the scenarios pin down")
    for c in cov:
        if c["covered"]:
            gq = next(x for x in c["groups"] if x["theorem_ok"] and not x["unproved"])
            print(f"  {c['call']}: every input is covered by a proved scenario (kernel-checked {gq['name']} over {len(gq['ids'])} scenarios)")
        else:
            print(f"  {c['call']}: NOT SHOWN that every input is covered by a proved scenario")
    ms = mutation_summary(mut)
    if ms:
        print(f"  mutation run of {ms['at']}: {ms['killed']} of {ms['total']} Rust mutants noticed by the scenarios"
              + ("" if ms["current"] else "  (OUT OF DATE: rerun python3 mutation/run_mutants.py)"))
        for m in ms["survivors"]:
            print(f"    not noticed: {m['id']} ({m['fn']}): {m['description']}")
    else:
        print("  no mutation results (python3 mutation/run_mutants.py)")
    if rd is not None:
        print(f"Two readings of each Given/Then phrase (Lean definition, Rust predicate): "
              f"{sum(q['agree'] for q in rd.values())} of {sum(q['n'] for q in rd.values())} grid points agree, over {len(rd)} phrases")
    print()
    for e in errs:
        print(f"ERROR: {e}")
    ok = all(v.as_expected for v in verdicts) and not errs
    counts = {}
    for v in verdicts:
        counts[v.status] = counts.get(v.status, 0) + 1
    print(f"{len(verdicts)} scenarios: " + ", ".join(f"{n} {k}" for k, n in counts.items()))
    weak = [v for v in verdicts if v.substantive and v.substantive[0] < v.substantive[1]]
    if weak:
        print(f"  of the proved ones, {len(weak)} have a Then that says nothing about the code: " + ", ".join(v.sc.id.rsplit('.', 1)[1] for v in weak))
    unrev = sum(1 for v in verdicts if v.status.startswith("PROVED") and v.unreviewed)
    if unrev:
        print(f"  {unrev} proved scenarios rest on glossary entries with no valid sign-off"
              + (" (--strict: counted as failures)" if ctx["strict"] else " (./run.sh --strict makes this a failure)"))
    print(f"graph: {len(gr['nodes'])} nodes, {len(gr['edges'])} edges -> out/graph.json;  report -> out/report.md")
    print("RESULT: " + ("every scenario got its expected verdict" if ok else "MISMATCH between expected and actual verdicts, or errors (see above)"))
    return 0 if ok else 1


def cmd_steps(st: State) -> int:
    rs = steps_rs()
    bad = 0
    for e in st.gloss.entries:
        got = rs.get(e.id)
        state = "ok" if got and got[1] == e.cucumber_re and got[0] == e.kind else "MISSING" if not got else "DIFFERS"
        bad += state != "ok"
        print(f"{state:8} {e.id:11} #[{e.kind}(regex = r\"{e.cucumber_re}\")]")
    for i in rs:
        if i not in [e.id for e in st.gloss.entries]:
            print(f"EXTRA    {i}: step function with no glossary entry")
            bad += 1
    return 1 if bad else 0


def cmd_review(st: State, argv) -> int:
    """Record that a person has read a glossary entry and its Lean definition and agrees they say the same thing.
    The record holds the digests of the phrase (with its argument order) and of the definition it binds to;
    it is void as soon as either changes."""
    if len(argv) != 3 or argv[1] != "--reviewer":
        print("usage: python3 -m slicegen review <entry-id|all> --reviewer NAME")
        return 2
    g = Graph()
    for name in st.model_fns:
        text, a, b = lean_fn_block(name, st.model_fns[name]["lean_file"])
        g.node(f"fn:lean:{name}", "function", "lean", " ".join(text.split(":= do")[0].split()), {"by": "tool:charon+aeneas"})
    targets = glossary_nodes(st, g, load_audit(), vocab_defs(st.gloss), {"by": "model:unrecorded"})
    so = load_signoff()
    ids = [e.id for e in st.gloss.entries] if argv[0] == "all" else [argv[0]]
    for i in ids:
        e = st.gloss.entry(i)
        p, t = targets[i]
        so[i] = {"reviewer": argv[2], "date": datetime.date.today().isoformat(),
                 "phrase": g.nodes[p]["interface"]["identity"]["value"], "target": g.nodes[t]["interface"]["identity"]["value"]}
        print(f"signed off {i}: \"{e.phrase}\"  :=  {e.lean or e.call} {' '.join(e.args)}")
    (ROOT / "glossary.signoff.json").write_text(json.dumps(so, indent=2) + "\n")
    return 0
