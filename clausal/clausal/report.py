"""clausal report: verdicts, out/graph.json (refinement graph, schema v2), out/report.md, terminal report.

Also: `steps` (cucumber regex identity check) and `review` (glossary sign-off).
"""
from __future__ import annotations

import datetime
import hashlib
import json
import re

from . import adequacy, emit, graphlint, ppath, rules, vocab, vreport
from . import evidence
from .core import RULE_VERSION, Bound, Problem, sha
from .vocab import Reading
from .pipeline import (LEAN, OUT, ROOT, State, adequacy_search, parse_search, proof_module, proof_path, proofs_state,
                       spec_digest, wants_proof)

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
    # A Background (of the Feature or of a Rule) is reported as an element of its own, on the same line as the
    # scenario it ran before: the two are one run, so their steps are put together.
    steps = {}
    for f in json.loads(p.read_text()):
        base = f["uri"].rsplit("/", 1)[-1]
        for e in f.get("elements", []):
            steps.setdefault((base, e["line"]), []).extend(e["steps"])
    return {k: _status({"steps": v}) for k, v in steps.items()}


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


def load_adequacy_audit():
    p = OUT / "adequacy-audit.log"
    if not p.exists():
        return None
    for line in p.read_text().splitlines():
        if line.startswith("AUDIT\t"):
            return json.loads(line.split("\t", 1)[1])
    return None


def cucumber_rustc() -> str:
    """The compiler that built the binary cucumber-rs ran (written by run.sh), for the compilation link."""
    p = OUT / "rustc.txt"
    return p.read_text().strip() if p.exists() and p.read_text().strip() else "rustc (version not recorded)"


def load_mutation():
    p = ROOT / "mutation" / "results.json"
    return json.loads(p.read_text()) if p.exists() else None


def proof_block(id_: str):
    """(text, first line, last line, path relative to clausal/) of `theorem <id>` in its proof module."""
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
    for p in sorted((ROOT / "clausal").glob("*.py")):
        h.update(p.read_bytes())
    return h.hexdigest()[:12]


def toolchain() -> dict:
    prov = json.loads((LEAN / "provenance.json").read_text())
    man = json.loads((LEAN / "lake-manifest.json").read_text())
    mathlib = next((p.get("rev", "") for p in man.get("packages", []) if p.get("name") == "mathlib"), "")
    return {"lean": (LEAN / "lean-toolchain").read_text().strip(), "mathlib": mathlib,
            "aeneas": prov["aeneas"], "charon": prov["charon"], "rustc": prov["rustc"],
            "generator": f"clausal {generator_sha()} ({RULE_VERSION})"}


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
        self.reading = st.readings.get(sc.id)          # the reading compiled from the composable Clausebook, or a Problem
        self.pieces, self.pieces_unreviewed, self.link_ok = [], [], False
        self.new, self.rust_grid = False, {"ran": False}      # a NEW sentence (no flat statement in the old glossary); Lean vs compiled Rust on the grid
        self.status = self.compute(st, ctx)
        if sc.outline:
            self.expected = sc.expect or "PROVED-FOR-ALL"
        else:
            self.expected = sc.expect or "PROVED-INSTANCE"
        if ctx["strict"] and self.status.startswith("PROVED") and self.unreviewed:
            self.fatal.append(f"--strict: rests on {len(self.unreviewed)} glossary entries with no valid sign-off")
        if ctx["strict"] and self.status.startswith("PROVED") and self.pieces_unreviewed:
            self.fatal.append(f"--strict: rests on {len(self.pieces_unreviewed)} Clausebook pieces with no valid sign-off")
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
        """The verdict of the READING compiled from the Clausebook. The flat statement of the old glossary gets its
        verdict as before (`compute_flat`); that verdict is the reading's only if the kernel-checked equivalence
        `<id>.reading_iff` is there. Otherwise: UNLINKED."""
        rd, L = self.reading, self.lines
        links = ctx["links"]
        if isinstance(self.r, Problem) and isinstance(rd, vocab.Reading):
            # a NEW sentence: the Clausebook reads it, the old glossary has no flat statement for it. Its verdict comes from
            # the reading and its generated proof obligation alone (clausal/ppath.py).
            self.link_ok = True
            return ppath.new_scenario_verdict(self, st, ctx)
        status = self.compute_flat(st, ctx)
        if isinstance(self.r, Problem):
            if isinstance(rd, Problem):
                L.insert(0, f"Clausebook       {rd.status}: {rd.message}")
                for k, h in enumerate(rd.hint.splitlines(), 1):
                    L.insert(k, "                 " + h)
            elif rd is not None:
                L.insert(0, "Clausebook       the composable Clausebook reads this sentence, but the old glossary gives no flat statement for it "
                            "(a NEW sentence; see `python3 -m clausal compile`), so nothing here was proved or refuted")
            return status
        if isinstance(rd, Problem):
            self.lines = ([f"{rd.message}"] + ["  " + h for h in rd.hint.splitlines()]
                          + ["no reading was compiled from the Clausebook, so there is no statement to give a verdict on",
                             f"(the flat statement of the old glossary would have been: {status}; it is not reported in the reading's place)"])
            self.rests_on = []
            return rd.status
        self.pieces = rd.used
        self.pieces_unreviewed = [i for i in rd.used if i not in ctx["piece_reviewed"]]
        if self.pieces_unreviewed:
            self.flags.append(f"UNREVIEWED CLAUSEBOOK ({len(self.pieces_unreviewed)} of {len(rd.used)})")
        off = vreport.outside_allowlist(links, st.voc, rd)
        if off:
            self.flags.append("GENERATOR-CHECK-FAILED")
            self.fatal.append("GENERATOR-CHECK-FAILED: the reading mentions " + ", ".join(off) + ", which none of its Clausebook pieces accounts for")
        rs = ctx["rs"].get(rd.id, {})
        if rs.get("diff"):
            self.flags.append("FRAME READINGS DISAGREE")
            self.fatal.append("FRAME READINGS DISAGREE: the definition and the executable reading of a frame differ at "
                              + json.dumps(rs["diff"]["values"]) + f" (definition {rs['diff']['definition']}, executable {rs['diff']['checker']})")
        cmp_ = ppath.apply_compare(self, rd.id, rs, ctx)
        if status.startswith("PROVED") and rs.get("bad"):
            self.flags.append("READING/FLAT MISMATCH")
            self.fatal.append("READING/FLAT MISMATCH: the reading search finds the reading false at " + json.dumps(rs["bad"]["values"])
                              + " although the flat statement is proved")
        iff, sat = rd.id + ".reading_iff", rd.id + ".reading_sat"
        signed = len(rd.used) - len(self.pieces_unreviewed)
        meaning = ((f"human-asserted   {signed} of {len(rd.used)} Clausebook pieces signed off" if signed else
                    f"NOT ASSERTED     0 of {len(rd.used)} Clausebook pieces signed off by anyone")
                   + ("" if not self.pieces_unreviewed else f" - UNREVIEWED: {', '.join(self.pieces_unreviewed)}"))
        two = ("" if not rs or "skipped" in rs else
               f"tested           the reading on {rs['tried']} generated inputs ({rs['in_scope']} in scope): the definition of each frame and its "
               f"executable reading agree on {rs['agree']} of {rs['evals']} evaluations"
               + ("; the reading is false at one of them" if rs.get("bad") and not rs["bad"].get("source") else
                  f"; the reading is false at none of them (the counterexample came from the generated {rs['bad']['source']})" if rs.get("bad") else ""))
        for echo, kind in vreport.covers_no_call(rs):
            self.flags.append("COVERS NO CALL ON THE GRID")
            two += (f"\ncovers no call   \"{echo}\" is about {kind} calls only, and none of the {rs['in_scope']} calls in scope on the grid "
                    f"was {kind}: there the line holds because it says nothing")
        if not vreport.lclean(links, iff):
            L.insert(0, f"NOT LINKED       the reading compiled from the Clausebook is NOT proved equivalent to the flat statement "
                        f"({vreport.lwhy(links, iff)}); what follows is about the flat statement {self.r.id}.stmt only (it would be: {status})")
            self.rests_on = [x for x in self.rests_on if x != "kernel-checked"]
            return "UNLINKED"
        if status.startswith("PROVED") and not vreport.lclean(links, sat):
            L.insert(0, f"NOT LINKED       the reading is equivalent to the flat statement, but its own non-vacuity ({sat}) is not shown "
                        f"({vreport.lwhy(links, sat)})")
            return "UNLINKED"
        holds = rd.id + ".reading_holds"
        if status.startswith("PROVED") and not vreport.lclean(links, holds):
            L.insert(0, f"NOT LINKED       the reading is equivalent to the flat statement and the flat statement is proved, but the one theorem "
                        f"that puts the two together ({holds} : {rd.name}) is not there ({vreport.lwhy(links, holds)})")
            return "UNLINKED"
        self.link_ok = True
        head = []
        if status.startswith("PROVED"):
            head.append(f"kernel-checked   theorem {holds} : {rd.name}  (THE READING ITSELF, as one theorem: the proof of the flat statement "
                        f"carried through the equivalence; type checked by the audit); axioms {', '.join(vreport.lthm(links, holds)['axioms'])}")
        head += [f"kernel-checked   theorem {iff} : {rd.name} ↔ {self.r.id}.stmt  (NEW ↔ OLD: the reading compiled from "
                 f"{len(rd.used)} Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); "
                 f"axioms {', '.join(vreport.lthm(links, iff)['axioms'])}"
                 + (f"; reading non-vacuous ({sat})" if vreport.lclean(links, sat) else "")]
        self.lines = head + L + [meaning] + (two.split("\n") if two else []) + [ppath.compare_line(cmp_)]
        return status

    def compute_flat(self, st, ctx):
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
            "no counterexample" if not s["bad"] else
            f"no counterexample on the grid (the counterexample above came from the generated {s['bad']['source']})" if s["bad"].get("source") else "counterexample found")
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
            if bad.get("source"):
                L.append(f"source           the input was found on the compiled Rust by {ppath.found_by(bad)}, not by the grid search; it was then "
                         "evaluated on the Lean model as an extra row of the flat statement, where it fails too")
                self.counterexample["source"] = bad["source"]
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
        out.append({"call": call, "covered": any(g["theorem_ok"] and not g["unproved"] for g in gs), "groups": gs, "scenarios": scs,
                    "says": said_about(call, verdicts)})
    return out


def said_about(call, verdicts) -> dict:
    """What the PROVED universal scenarios whose (last) When is `call` say about each of its outputs.
    {"result": [(Then phrase, condition, scenario)], "state": [...]}; condition is "" when the scenario has no Given
    beyond the ones that only name a value. This LISTS what is said; nothing checks that it determines the output."""
    out = {"result": [], "state": []}
    for v in verdicts:
        b = v.r
        if not isinstance(b, Bound) or v.status != "PROVED-FOR-ALL" or b.when.entry.call != call:
            continue
        cond = "; ".join(g.step.text for g in b.givens if not g.entry.builds)
        if b.multi:
            cond = "; ".join(filter(None, [cond, "after: " + "; then ".join(w.step.text for w in b.whens[:-1])]))
        weak = set(v.trivial) | set(v.frame)
        for t in b.thens:
            if t.step.text in weak:
                continue
            item = (t.entry.phrase, cond, b.id.rsplit(".", 1)[1])
            seen = lambda xs: any(x[:2] == item[:2] for x in xs)
            if "outcome" in t.entry.args and not seen(out["result"]):
                out["result"].append(item)
            if any(a.startswith("post(") or a.startswith("all_post(") for a in t.entry.args) and not seen(out["state"]):
                out["state"].append(item)
    return out


def said_text(items, md=True) -> str:
    if not items:
        return "**nothing**" if md else "nothing"
    return "; ".join(f"\"{p}\" ({'always' if not c else 'only when: ' + c})" for p, c, _ in items)


def mutation_summary(mut) -> dict | None:
    """{current, by_fn: {rust fn: (survived, total)}, survivors: [...], total, killed_by_scenarios, at}"""
    if not mut:
        return None
    by_fn = {}
    for m in mut["mutants"]:
        s, t = by_fn.get(m["fn"], (0, 0))
        by_fn[m["fn"]] = (s + (not m["killed_by_scenarios"]), t + 1)
    false_of = lambda m: bool(m.get("rows_changed") or m.get("search_found"))      # a scenario is SHOWN false of the mutant
    not_false = {}
    for m in mut["mutants"]:
        s, t = not_false.get(m["fn"], (0, 0))
        not_false[m["fn"]] = (s + (not false_of(m)), t + 1)
    return {"current": mut.get("spec_digest") == spec_digest(), "by_fn": by_fn, "not_false_by_fn": not_false, "at": mut.get("generated_at"),
            "total": len(mut["mutants"]), "killed": sum(m["killed_by_scenarios"] for m in mut["mutants"]),
            "shown_false": sum(false_of(m) for m in mut["mutants"]), "false_of": false_of,
            "lemma_only": [m for m in mut["mutants"] if m["killed_by_scenarios"] and not false_of(m)],
            "survivors": [m for m in mut["mutants"] if not m["killed_by_scenarios"]]}


# --------------------------------------------------------------------------- graph (schema v2)

ALL, NA = {"quantifier": "all"}, {"quantifier": "n/a"}
SARIF = {"PROVED-FOR-ALL": "pass", "PROVED-INSTANCE": "pass", "REFUTED": "fail", "COUNTEREXAMPLE": "fail", "VACUOUS": "fail",
         "UNBOUND": "notApplicable", "AMBIGUOUS": "notApplicable", "UNSUPPORTED": "notApplicable", "TESTED-ONLY": "open",
         "VACUOUS-SUSPECTED": "review", "ILL-TYPED": "notApplicable", "UNLINKED": "open", "NOT-PROVED": "open"}     # NOT-PROVED: no longer given (a Rule without a proof is TESTED-ONLY)


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
    gen = {"by": "tool:clausal", "run": "run:clausal"}
    rust_src = {}

    def rust_lines_of(fn):
        key = (fn.get("crate", "wallet"), fn["source"]["file"])
        if key not in rust_src:
            rust_src[key] = (ROOT / key[0] / key[1]).read_text().splitlines()
        return rust_src[key]
    grid = sum(search[b.id]["tried"] for b in st.bounds)
    runs = [
        {"id": "run:clausal", "tool": "clausal", "version": tool["generator"]},
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
        runs.append({"id": "run:cucumber", "tool": "cucumber-rs on the compiled Rust", "toolchain": {"rustc": cucumber_rustc()}})
    note = ctx["note"]
    if note["ran"]:
        runs += [{"id": "run:adequacy", "tool": "Run/Adequacy.lean (Lean interpreter: scenario statements with a trivial model in place of the call)",
                  "version": tool["lean"], "config": {"method": "the boundary grid of the counterexample search", "pairs": len(ctx["decided"])},
                  "complete": not note["why"], **({"note": note["why"]} if note["why"] else {})},
                 {"id": "run:adequacy-audit", "tool": "Run/AdequacyAudit.lean (Lean kernel: generated scripts, best effort)", "version": tool["lean"],
                  "complete": ctx["adequacy_audit"] is not None}]

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
    out_verdicts, rule_recs = [], []
    stmt_file = LEAN / "Wallet" / "Statements.lean"
    parser_ev = lambda: [ev("tool-trusted", "tool:clausal", "run:clausal", RULE_VERSION, NA, detail="Gherkin-subset parser")]
    for f in st.features:
        fid = g.node(f"group:feature:{f.slug}", "group", "gherkin", f"Feature: {f.name}", author, src(f.path, f.line, len(f.lines)),
                     attrs={"level": "feature", "tags": f.tags, "description": f.description})
        for r in f.rules:
            # the rule line and its description, as written, and the READING compiled from the rule line (attrs.reading)
            rv = ctx["rule_verdicts"][r.id]
            ra = vreport.reading_attrs(st, rv.rd, ctx)
            ra.update({"status": rv.status, "expected": rv.expected, "as_expected": rv.as_expected, "headline": rv.headline,
                       "lines": rv.lines, "flags": rv.flags + [f"FATAL: {x}" for x in rv.fatal if x not in rv.flags],
                       "parts": rv.parts, "counterexample": rv.counterexample,
                       # what the per-Rule block needs about the rule STATEMENT itself (clausal/rules.py reads the graph only)
                       "rust_grid": {k: rv.rust_grid.get(k) for k in ("ran", "points", "evals", "agree", "error")},
                       "proof": rv.proof, "searched": ({"tried": ctx["rs"].get(r.id, {}).get("tried"), "in_scope": ctx["rs"].get(r.id, {}).get("in_scope")}
                                                       if isinstance(rv.rd, Reading) else None),
                       "model_fns": (list(dict.fromkeys(o["model"] for cl in rv.rd.info["clauses"] for o in cl["ops"]))
                                     if isinstance(rv.rd, Reading) else []),
                       "summary": vreport.summary_sentence(rv.rd) if isinstance(rv.rd, Reading) else None,
                       "obligation": ppath.obligation_text(r.id) if isinstance(rv.rd, Reading) else None,
                       # plan node E1: what the generated property test and bounded check say about the rule statement
                       "ladder": evidence.ladder(ctx.get("evidence"), rv.rd.id) if isinstance(rv.rd, Reading) else None})
            rid = g.node(f"group:rule:{r.id}", "group", "gherkin", r.text, author, src(f.path, r.line, r.end_line),
                         attrs={"level": "rule", "tags": r.tags, "feature": fid, "compiled": isinstance(rv.rd, Reading), "reading": ra})
            g.edge(fid, rid, "contains", parser_ev())
            rule_recs.append({"node": rid, "outcome": SARIF[rv.status], "code": rv.status, "expected": rv.expected,
                              "as_expected": rv.as_expected, "flags": ra["flags"], "chain": [], "rests_on": rv.rests_on,
                              "unreviewed": [], "stale": [], "detail": "the statement compiled from the Rule line"})
    stmt_node = {}
    for v in verdicts:
        sc = v.sc
        sid = g.node(f"scenario:{sc.id}", "claim", "gherkin", sc.text, author, src(sc.feature.path, sc.line, sc.end_line),
                     attrs={"scope": "universal" if sc.outline else "instance", "tags": sc.all_tags, "own_tags": sc.tags,
                            "name": sc.name, **({"rule": f"group:rule:{sc.rule.id}"} if sc.rule else {}),
                            "reading": {**vreport.reading_attrs(st, v.reading, ctx), "linked": v.link_ok,
                                        "ladder": evidence.ladder(ctx.get("evidence"), v.reading.id) if isinstance(v.reading, Reading) else None}})
        g.edge(f"group:rule:{sc.rule.id}" if sc.rule else f"group:feature:{sc.feature.slug}", sid, "contains", parser_ev())
        rec = {"node": sid, "outcome": SARIF[v.status], "code": v.status, "expected": v.expected, "as_expected": v.as_expected,
               "flags": [f for f in v.flags if not f.startswith("UNREVIEWED")] + [f"FATAL: {x}" for x in v.fatal if x not in v.flags],
               "chain": [], "rests_on": v.rests_on, "unreviewed": [], "stale": []}
        if v.counterexample:
            rec["counterexample"] = v.counterexample
        out_verdicts.append(rec)
        if v.new:
            # a NEW sentence: its statement is the compiled reading; its proof is the supplied proof of the generated flat
            # obligation, carried through the kernel-checked equivalence. No node of the old glossary is involved.
            rd, links = v.reading, ctx["links"]
            proved = v.status.startswith("PROVED")
            rblk = decl_block(LEAN / "Wallet" / "Readings.lean", f"def {rd.name} ")
            pp = proof_path(sc.id)
            impls = []
            if pp.exists():
                impls = [{"id": "p1", "language": "lean-proof", "ref": rd.id, "source": src(str(pp.relative_to(ROOT))), "digest": dg(pp.read_text()),
                          "complete": proved, "hidden": True, "metrics": {"size_lines": len(pp.read_text().split("theorem ", 1)[-1].splitlines()) - 1},
                          "realises": []}]
            scope = "universal" if sc.outline else "instance"
            tid = g.node(f"stmt:{rd.name}", "statement", "lean", rd.lean_def(), gen,
                         src("lean/Wallet/Readings.lean", rblk[1], rblk[2]) if rblk else src("lean/Wallet/Readings.lean"),
                         impls=impls, attrs={"scope": scope, "compiled_from": "clausebook.yaml", "pieces": rd.used, "new_sentence": True,
                                             "obligation": ppath.obligation_text(rd.id)})
            e_form = g.edge(tid, sid, "formalises", [
                ev("tool-trusted", "tool:clausal", "run:clausal", tool["generator"], NA,
                   detail="composition of Clausebook pieces (clausal/vocab.py); echoed in English in the report")])
            holds, iff = rd.id + ".reading_holds", rd.id + ".reading_iff_obligation"
            if proved and impls:
                g.realise(tid, "p1", [ev("kernel-checked", "tool:lean-kernel", "run:lean", holds,
                                         ALL if sc.outline else inst(1, "the scenario's literals"),
                                         axioms=vreport.lthm(links, holds).get("axioms", []), method="script-session",
                                         detail=f"the supplied proof of the generated flat obligation ({rd.id} : {rd.id}.obligation, module "
                                                f"{proof_module(sc.id)}) carried through the kernel-checked equivalence {iff}; the link audit "
                                                "checked the type of all three")])
            e_uses = [g.edge(tid, f"fn:lean:{o['model']}", "uses",
                             [ev("tool-trusted", "tool:clausal", "run:clausal", rd.name, NA,
                                 detail="the operation of the When is bound to this model function (clausebook.yaml, lean/*/Pieces.lean)")],
                             to_impl="body") for o in rd.info["ops"]]
            name = rd.id + ".refuted"
            if vreport.lclean(links, name):
                nid = g.node(f"stmt:{name}", "statement", "lean", f"theorem {name} : ¬ {rd.name}", gen, src("lean/Run/Links.lean"),
                             impls=[{"id": "p1", "language": "lean-proof", "ref": name, "source": src("lean/Run/Links.lean"), "digest": dg(name),
                                     "complete": True, "hidden": True, "realises": []}],
                             attrs={"derived_from_search": True, "meaning": "the negation of the reading"})
                g.realise(nid, "p1", [ev("kernel-checked", "tool:lean-kernel", "run:lean", name, ALL, axioms=vreport.lthm(links, name).get("axioms", []),
                                         witness=(v.counterexample or {}).get("values"), method="script-session",
                                         detail="generated proof script, elaborated and kernel-checked inside the link run; not stored in an .olean")])
                g.edge(nid, tid, "refutes", [ev("tool-trusted", "tool:lean-audit", "run:lean", name, NA,
                                                detail=f"the link audit checked that the theorem's type is exactly ¬ {rd.name}")],
                       attrs={"how": "falsity"})
            for x in v.rows:
                rid_ = g.node(f"example:{sc.id}#{x['n']}", "example", "gherkin",
                              row_text(sc.header, x["cells"]) if sc.header else "(the scenario's own literals)",
                              author, src(sc.feature.path, x["line"]), attrs={"model": x["model"], "rust": x["rust"]})
                e1 = ev("tested", "tool:lean-eval", "run:search", "out/rsearch.log", inst(1, "examples"),
                        detail=f"{x['model']}: the reading itself evaluated at the row on the Lean model")
                g.edge(rid_, tid, "instance_of", [dict(e1)])
                for o in rd.info["ops"]:
                    g.edge(rid_, f"fn:lean:{o['model']}", "exercises", [dict(e1)], to_impl="body")
                if x["rust"] is not None:
                    e2 = ev("tested", "tool:cucumber-rs", "run:cucumber", "out/cucumber.json", inst(1, "examples"),
                            detail=f"{x['rust']}: the generic step evaluated the step's composition tree with the per-piece Rust readings")
                    g.edge(rid_, tid, "instance_of", [dict(e2)])
                    for o in rd.info["ops"]:
                        g.edge(rid_, f"fn:rust:{st.model_fns[o['model']]['rust_name']}", "exercises", [dict(e2)], to_impl="body")
            rec["chain"] = [e_form] + e_uses + [f"translates:fn:lean:{o['model']}[body]->fn:rust:{st.model_fns[o['model']]['rust_name']}" for o in rd.info["ops"]]
            rec["detail"] = "a NEW sentence: read by the composable Clausebook alone; no entry of the old whole-phrase glossary is involved"
            if proved and v.pieces_unreviewed:
                rec["outcome"] = "review"
            continue
        if isinstance(v.r, Problem):
            rec["detail"] = f"{v.r.code}: {sc.feature.path}:{v.r.line}: {v.r.message}"
            continue
        b: Bound = v.r
        for bs in b.all_steps:
            g.edge(sid, f"phrase:{bs.entry.id}", "composed_of",
                   [ev("tool-trusted", "tool:clausal", "run:clausal", RULE_VERSION, NA,
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
        if isinstance(v.reading, Reading):
            # the compiled reading as its own statement node, tied to the flat statement by a kernel-checked equivalence
            rd, links = v.reading, ctx["links"]
            rblk = decl_block(LEAN / "Wallet" / "Readings.lean", f"def {rd.name} ")
            rnode = g.node(f"stmt:{rd.name}", "statement", "lean", rd.lean_def(), gen,
                           src("lean/Wallet/Readings.lean", rblk[1], rblk[2]) if rblk else src("lean/Wallet/Readings.lean"),
                           attrs={"scope": b.scope, "compiled_from": "clausebook.yaml", "pieces": rd.used})
            g.edge(rnode, sid, "formalises", [
                ev("tool-trusted", "tool:clausal", "run:clausal", tool["generator"], NA,
                   detail="composition of Clausebook pieces (clausal/vocab.py); echoed in English in the report")])
            iff = rd.id + ".reading_iff"
            g.edge(rnode, tid, "equivalent",
                   [ev("kernel-checked", "tool:lean-kernel", "run:lean", iff, ALL, axioms=vreport.lthm(links, iff).get("axioms", []),
                       method="script-session",
                       detail="generated proof script (lean/Run/Links.lean); the link audit checked that the theorem's type is "
                              f"exactly {rd.name} ↔ {b.id}.stmt")] if vreport.lclean(links, iff) else [])
        if pb and clean(audit, b.id):
            g.realise(tid, "p1", [ev("kernel-checked", "tool:lean-kernel", "run:lean", b.id,
                                     ALL if b.scope == "universal" else inst(1, "the scenario's literals"), axioms=axioms(audit, b.id),
                                     method="library-module",
                                     detail=f"module {proof_module(b.id)}; the audit checked that the theorem's type is exactly {b.id}.stmt")])
        e_form = g.edge(tid, sid, "formalises", [
            ev("tool-trusted", "tool:clausal", "run:clausal", tool["generator"], NA,
               detail="translation rule of DESIGN.md section 5; audit of the constants in the elaborated statement: "
                      + ("passed" if audit and not (v.stmt_missing or v.stmt_extra) else "FAILED or not run"))])
        consts = set((audit or {}).get("stmts", {}).get(b.id + ".stmt", {}).get("consts", []))

        def use_ev(c, what):
            return [ev("tool-trusted", "tool:lean-audit", "run:lean", b.id + ".stmt", NA,
                       detail=f"{what}: the constant occurs in the elaborated statement (read from the environment by Bdd.Audit)")
                    if c in consts else
                    ev("tool-trusted", "tool:clausal", "run:clausal", b.id + ".stmt", NA,
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
                g.edge(tid, nid, "requires", [ev("tool-trusted", "tool:clausal", "run:clausal", name, NA,
                                                 detail="non-vacuity side condition of a PROVED verdict: generated from the same Givens")])
            elif suffix == ".unsat":
                g.edge(nid, tid, "refutes", [ev("tool-trusted", "tool:clausal", "run:clausal", name, NA,
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
                         author, src(sc.feature.path, x["line"]), attrs={"model": x["model"], "rust": x["rust"]})
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
            chain.append(g.edge(nid, fid, "covers", [ev("tool-trusted", "tool:clausal", "run:clausal", grp["name"], NA,
                                                         detail="the scenarios were grouped by their When phrase and identical variables")]))
            for i in grp["ids"]:
                chain.append(g.edge(nid, stmt_node[i], "requires",
                                    [ev("tool-trusted", "tool:clausal", "run:clausal", grp["name"], NA,
                                        detail="one disjunct of the coverage statement is this scenario's Givens; coverage counts only if the scenario is proved")]))
                unrev += [u for v in out_verdicts if v["node"] == f"scenario:{i}" for u in v["unreviewed"]]
        unrev = sorted(set(unrev))
        rust_fn = st.model_fns[c["call"]]["rust_name"]
        flags = []
        if ms and ms["current"] and rust_fn in ms["by_fn"]:
            sv, tot = ms["by_fn"][rust_fn]
            flags.append(f"MUTANTS-SURVIVING-THE-SCENARIOS: {sv} of {tot}")
            nf, _ = ms["not_false_by_fn"][rust_fn]
            flags.append(f"MUTANTS-OF-WHICH-NO-SCENARIO-IS-SHOWN-FALSE: {nf} of {tot}")
        out_verdicts.append({
            "node": fid, "outcome": ("review" if unrev else "pass") if c["covered"] else "open",
            "code": "INPUTS-COVERED" if c["covered"] else "INPUTS-NOT-COVERED", "flags": flags, "chain": chain,
            "rests_on": (["kernel-checked", "tool-trusted"] if c["covered"] else []), "unreviewed": unrev, "stale": [],
            "detail": ("every input is covered by the Givens of a proved universal scenario" if c["covered"] else
                       "not shown that every input is covered by a proved universal scenario: "
                       + ("no universal scenario exercises this function" if not c["groups"] else
                          "; ".join(f"{x['name']}: " + ("coverage theorem failed" if not x["theorem_ok"] else "unproved: " + ", ".join(x["unproved"]))
                                    for x in c["groups"])))})
    adequacy_graph(st, g, ctx, out_verdicts, gen)
    out_verdicts += rule_recs
    gr = {"schema": "rosette.refinement-graph/2",
          "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
          "runs": runs, "nodes": list(g.nodes.values()), "edges": list(g.edges.values()), "verdicts": out_verdicts}
    st_ = graphlint.staleness(gr)
    for v in gr["verdicts"]:
        v["stale"] = [e for e in v["chain"] if e in st_["edges"]]
    return gr


def adequacy_graph(st, g: Graph, ctx, out_verdicts, gen):
    """The suite adequacy note in the graph (no schema change):
      - each trivial model is a `function` node (attrs.trivial: which operation it stands in for, its kind);
      - each (scenario, trivial model) pair is a `statement` node: the scenario's statement with the trivial model
        in place of the call. It `uses` the trivial model. Where the search found an input on which it is false, an
        `example` node `refutes` it (tested; kernel-checked too when the generated refutation went through). Where it
        was proved for all inputs, the proof is an implementation with kernel-checked `realises` evidence;
      - one verdict per operation (SUITE-RULES-OUT-TRIVIAL / SUITE-ALLOWS-TRIVIAL), informational;
      - the lines printed per Rule are a `note` label and `attrs.suite_lines` on the Rule's group node."""
    note, decided = ctx["note"], ctx["decided"]
    if not note["ran"]:
        for n in g.nodes.values():
            if n["kind"] == "group":
                n.setdefault("attrs", {})["suite_lines"] = [f"not computed: {note['why']}"]
        return
    byid = {b.id: b for b in st.bounds}
    for call, ts in st.triv.items():
        for t in ts:
            s0 = src("lean/Run/Adequacy.lean")
            g.node(f"fn:lean:{t.lean_name}", "function", "lean", f"{t.lean_name} : type_of% @{t.call}", gen, s0,
                   impls=[{"id": "body", "language": "lean-def", "ref": t.lean_name, "source": s0, "digest": dg(t.lean_def),
                           "complete": True, "realises": []}],
                   attrs={"generated": True, "trivial": {"of": f"fn:lean:{call}", "kind": t.kind, "key": t.key, "label": t.label}})
    ruled_edge = {}
    for name, d in decided.items():
        b, t = byid[d["scenario"]], d["trivial"]
        impls = []
        if d["result"] == "holds":
            impls = [{"id": "p1", "language": "lean-proof", "ref": name + ".holds", "source": src("lean/Run/AdequacyAudit.lean"),
                      "digest": dg(adequacy.holds_theorem(name, b, t)), "complete": True, "hidden": True, "realises": []}]
        nid = g.node(f"stmt:{name}.stmt", "statement", "lean", adequacy.stmt_text(name, b, t), gen, src("lean/Run/AdequacyAudit.lean"),
                     impls=impls, attrs={"adequacy": {"scenario": f"scenario:{b.id}", "of_statement": f"stmt:{b.id}.stmt",
                                                      "trivial": f"fn:lean:{t.lean_name}", "result": d["result"],
                                                      "grid_tried": d["tried"], "grid_inside_givens": d["inside"]}})
        if d["result"] == "holds":
            g.realise(nid, "p1", [ev("kernel-checked", "tool:lean-kernel", "run:adequacy-audit", name + ".holds", ALL, axioms=d["axioms"],
                                     method="script-session",
                                     detail="the scenario's statement holds of the trivial model for every input (generated proof script)")])
        g.edge(nid, f"fn:lean:{t.lean_name}", "uses",
               [ev("tool-trusted", "tool:clausal", "run:clausal", name + ".stmt", NA,
                   detail="the generator wrote the trivial model where the scenario's statement calls the model function")], to_impl="body")
        if d["result"] == "ruled-out":
            vals = d["bad"]["values"]
            text = row_text(list(vals), vals) if vals else "(the scenario's own literals)"
            cid = g.node(f"example:adequacy:{name}", "example", "gherkin", text, {"by": "tool:lean-eval", "run": "run:adequacy"},
                         src("out/adequacy.log"), attrs={"values": vals, "returned": d["bad"]["returned"], "check": d["bad"]["check"]})
            evs = [ev("tested", "tool:lean-eval", "run:adequacy", "out/adequacy.log", inst(1, "boundary-grid"),
                      detail=f"with the trivial model in place of the call, the Givens hold and a Then fails; the {d['tried']}th grid input tried")]
            if d["evidence"] == "kernel-checked":
                evs.append(ev("kernel-checked", "tool:lean-kernel", "run:adequacy-audit", name + ".refuted", inst(1, "the input the search found"),
                              axioms=d["axioms"], witness=vals, method="script-session",
                              detail=f"theorem of type ¬ {name}.stmt (generated refutation script)"))
            ruled_edge[name] = g.edge(cid, nid, "refutes", evs, attrs={"how": "falsity"})
    unsigned = {v["node"]: v["unreviewed"] for v in out_verdicts if v["node"].startswith("scenario:")}
    for call, op in note["ops"].items():
        fid = f"fn:lean:{call}"
        chain, kinds, cands = [], set(), []
        for r in op["rows"]:
            t = r["trivial"]
            cands.append({"trivial": f"fn:lean:{t.lean_name}", "kind": t.kind, "label": t.label, "state": r["state"],
                          "ruled_out_by": [f"scenario:{i}" for i in r["by"]],
                          "ruled_out_by_examples": [f"scenario:{i}" for i in r["by_examples"]], "holds_proved": r["holds_proved"]})
            if r["by"]:
                # one ruling pair on the chain per trivial model: a kernel-checked one if there is one
                names = [adequacy.pair_name(byid[i], t) for i in r["by"]]
                name = next((x for x in names if decided[x]["evidence"] == "kernel-checked"), names[0])
                chain.append(ruled_edge[name])
                kinds.add(decided[name]["evidence"])
        allowed = [r for r in op["rows"] if r["state"] == "allowed"]
        unrev = sorted({u for i in op["universal"] for u in unsigned.get(f"scenario:{i}", [])})
        out_verdicts.append({
            "node": fid, "outcome": "open" if (allowed or not op["universal"]) else "review" if unrev else "pass",
            "code": "SUITE-ALLOWS-TRIVIAL" if (allowed or not op["universal"]) else "SUITE-RULES-OUT-TRIVIAL",
            "flags": [f"STILL-ALLOWS {r['trivial'].kind}: {r['trivial'].label}" for r in allowed],
            "chain": chain, "rests_on": sorted(kinds) + (["tool-trusted"] if chain else []), "unreviewed": unrev, "stale": [],
            "detail": "INFORMATIONAL (suite adequacy note; never a failure). The proved universal scenarios of this operation, as a suite: "
                      + " | ".join(op["lines"])})
        n = g.nodes[fid]
        n.setdefault("attrs", {})["adequacy"] = {"universal": [f"scenario:{i}" for i in op["universal"]],
                                                 "instances": [f"scenario:{i}" for i in op["instances"]],
                                                 "candidates": cands, "lines": op["lines"]}
        n.setdefault("labels", []).append({"kind": "note", "text": "Suite adequacy note: " + " | ".join(op["lines"]),
                                           "by": "tool:clausal", "run": "run:clausal", "about": n["interface"]["identity"]})
    for gid, grp in note["groups"].items():
        n = g.nodes[gid]
        n.setdefault("attrs", {}).update({"suite_lines": grp["lines"], "suite_headlines": grp["heads"], "suite": grp["data"]})
        if grp["lines"]:
            n.setdefault("labels", []).append({"kind": "note", "text": "Suite adequacy note: " + " | ".join(grp["lines"]),
                                               "by": "tool:clausal", "run": "run:clausal", "about": n["interface"]["identity"]})


# --------------------------------------------------------------------------- report

def suite_table(gr: dict) -> list:
    """Per operation, from the graph: [(operation, n universal, n literal, lines, [candidate dicts])]."""
    out = []
    for n in gr["nodes"]:
        a = n.get("attrs", {}).get("adequacy") if n["kind"] == "function" else None
        if a and "candidates" in a:
            out.append((n["id"].split(":", 2)[2], len(a["universal"]), len(a["instances"]), a["lines"], a["candidates"]))
    return out


def rules_match(blocks, verdicts) -> list:
    """The per-Rule blocks were computed from the graph file alone. Check them against the verdicts computed in
    memory: every scenario in exactly one block, with the same verdict and the same number of example rows."""
    errs, seen = [], {}
    for b in blocks:
        for s in b["scenarios"]:
            seen.setdefault(s["id"], []).append(s)
    for v in verdicts:
        got = seen.get(v.sc.id, [])
        if len(got) != 1:
            errs.append(f"rule blocks: scenario {v.sc.id} appears in {len(got)} blocks of out/graph.json (expected 1)")
        elif got[0]["code"] != v.status or len(got[0]["rows"]) != len(v.rows):
            errs.append(f"rule blocks: {v.sc.id} is {got[0]['code']} with {len(got[0]['rows'])} rows in the graph, "
                        f"{v.status} with {len(v.rows)} rows in this run")
    return errs


def md_report(st, verdicts, cov, gr, ctx, vdefs, rs, errs, mut, blocks) -> str:
    audit, cuc, readings = ctx["audit"], ctx["cuc"], ctx["readings"]
    tool = st.tool
    gl = st.gloss
    kinds = st.voc.kinds()
    rvs = ctx["rule_verdicts"]
    o = ["# Slice: rule and scenario report (wallet and ledger)", "",
         f"Generated {gr['generated_at']} by `clausal/run.sh`. Lean `{tool['lean']}`, Aeneas `{tool['aeneas']}`, "
         f"Charon `{tool['charon']}`, `{tool['rustc']}`, {tool['generator']}.", "",
         "Each `Rule:` line and each scenario below is an English claim about one of the Rust crates `clausal/wallet` (three straight-line "
         "functions) and `clausal/ledger` (loops over a `Vec` and a slice). The sentence is not bound as a whole: it is **assembled from typed "
         f"pieces** of a Clausebook ({kinds['domain']} domain words, {kinds['modifier']} modifiers, {kinds['frame']} frames). The composition "
         "is compiled to one Lean statement about the Aeneas-generated Lean model of the crate, and **echoed back in fixed, slot-structured "
         "English** (applies to / assuming / then / defaults applied) so the author can check that the tool read the sentence as it was meant. "
         "The echo is the first thing printed for every rule and scenario; the Lean is underneath. The statement is then proved, refuted or "
         "left open, and every link in that chain is labelled with the kind of evidence behind it:", "",
         "| Evidence kind | Meaning here |", "|---|---|",
         "| kernel-checked | Lean's kernel accepted a proof of exactly the stated theorem. Holds for every input the statement quantifies over. |",
         "| tested | Evaluated on particular inputs: Examples rows on the compiled Rust (cucumber-rs, one generic step) and on the Lean model, a boundary grid on the model, counterexamples replayed on the Rust, every compiled reading on generated inputs three ways (the definition of each frame, its executable reading, and the Rust reading of every piece on the compiled crate), and the two readings of each old glossary phrase compared on a grid. |",
         "| tool-trusted | Produced by a program whose output is not proved correct: Charon + Aeneas (Rust to Lean), Aeneas's hand-written models of std operations, clausal (sentence to composition to statement), and the audits that read facts out of the Lean environment. |",
         "| human-asserted | A person's say-so: that each Clausebook piece means its Lean definition. Nothing checks this. It exists only where someone has signed off. |", "",
         "**How a Rule relates to its scenarios.** The rule line compiles to ONE Lean statement that covers every input (fail-closed: "
         "rejected calls included, and the call must answer). The scenarios beneath it are its tested instances (their Examples rows run on the "
         "compiled Rust) and, where they are outlines, its **parts**: a generated, kernel-checked theorem `<rule>.from_scenarios` derives the "
         "rule statement from the scenario statements, by cases on their Givens. Where that script does not go through, a hand-written proof of "
         "exactly the rule statement may stand in (`lean/Wallet/RuleProofs/`). A rule statement found false by the reading search is refuted in "
         "the kernel at that input. A scenario may say more than its rule (a progress scenario under a safety rule); the block says which "
         "scenarios are parts.", "",
         "**Two statements per scenario.** The reading compiled from the Clausebook is what is shown and what the verdict is about. For the "
         "OLDER scenarios the hand-written proofs, the counterexample search and the refutations are about the *flat statement* of the old "
         "whole-phrase glossary, unchanged; a generated kernel-checked equivalence carries the verdict across "
         "([Regression](#regression-every-old-statement-against-its-new-reading-plan-node-v3)). A **NEW sentence** (marked so) has no entry "
         "in the old glossary: its flat proof obligation is generated from the pieces, a supplied proof of it is carried to the reading by a "
         "kernel-checked equivalence, and it runs on the compiled Rust through the generic step "
         "([New sentences, end to end](#new-sentences-end-to-end)).", "",
         "## Rules", "",
         "Generated from `out/graph.json` (`python3 -m clausal rules` prints the same from the stored graph). "
         "The full block of each rule, with its reading and what it rests on, is under [Rules and their scenarios](#rules-and-their-scenarios).", "",
         "| Rule | The rule statement | Its scenarios | Examples on Rust / on model | Suite adequacy (informational) |", "|---|---|---|---|---|"]
    for b in blocks:
        ex = b["examples"]
        rd = b["reading"]
        rcell = "-" if b["kind"] != "rule" else (f"**{rd.get('headline', rd.get('status', '?'))}**" + ("" if rd.get("as_expected", True) else " - NOT AS EXPECTED"))
        o.append(f"| {b['title'].replace('|', chr(92) + '|')} (`{b['source']}`) | {rcell} | **{b['verdict']['head']}**"
                 + ("" if b["verdict"]["as_expected"] else " - NOT AS EXPECTED") + f"<br>{b['verdict']['tally']} "
                 f"| {ex['rust_pass'] if ex['both'] else '-'} / {ex['model_pass']} of {ex['rows']} "
                 f"| {'<br>'.join(l.replace('|', chr(92) + '|') for l in b['suite_head']) or '-'} |")
    rc = {}
    for rv in rvs.values():
        rc[rv.status] = rc.get(rv.status, 0) + 1
    o += ["", f"{len(rvs)} rule statements: " + ", ".join(f"{n} {k}" for k, n in rc.items()) + ". "
          + ("Every rule statement got the verdict it was expected to get." if all(rv.as_expected for rv in rvs.values())
             else "**At least one rule statement did not get its expected verdict.**"), ""]
    o += ["", "## Summary", "", "| Scenario | Verdict | Expected | Rows on Rust / on model | Flags |", "|---|---|---|---|---|"]
    for v in verdicts:
        rows = (f"{sum(x['rust'] == 'pass' for x in v.rows) if cuc is not None else '-'} / {sum(x['model'] == 'pass' for x in v.rows)} of {len(v.rows)}"
                if v.rows else "-")
        o.append(f"| {v.sc.name} (`{v.sc.feature.path}:{v.sc.line}`) | **{v.headline}** | {v.expected}{'' if v.as_expected else ' - MISMATCH'} "
                 f"| {rows} | {'; '.join(v.flags) or '-'} |")
    ok = all(v.as_expected for v in verdicts) and all(rv.as_expected for rv in rvs.values()) and not errs
    o += ["", ("Every scenario got the verdict it was expected to get." if ok else "**At least one scenario did not get its expected verdict.**"),
          "A scenario tagged `@expect-refuted`, `@expect-unbound` or `@expect-vacuous` is a deliberate negative control.", ""]
    n_unrev_proved = sum(1 for v in verdicts if v.status.startswith("PROVED") and v.unreviewed)
    if n_unrev_proved:
        o += [f"**{n_unrev_proved} proved scenarios rest on glossary entries with no valid sign-off.** A proof shows the Lean "
              "statement holds; that the statement says what the English says is exactly what the sign-off is for. "
              "`./run.sh --strict` makes this a failure.", ""]

    o += ["## Which inputs the scenarios apply to, and what they say about the outputs", "",
          "A green scenario says nothing about inputs outside its Givens, and nothing about an output its Thens do not mention. "
          "Three views of what is left unsaid:", "",
          "1. **Inputs for which some scenario applies.** For each operation, a generated theorem states that the Givens of its proved "
          "universal scenarios, taken together, hold of every input. If the kernel accepts it, no input falls outside every scenario. "
          "**This says nothing about what those scenarios promise.** A scenario with no Given beyond naming its values applies to "
          "every input whatever its Then says, so for such an operation the answer is trivially yes.",
          "2. **What is said about each output.** The Thens of the proved universal scenarios, listed per output (the value the call "
          "returns; the state it hands back), each with the condition under which it is promised. This is a list for a person to read: "
          "nothing checks that the Thens determine the output, and for the loops here they do not "
          "(the ledger an `apply_batch` leaves is constrained only by its total and by where the batch stopped).",
          "3. **Mutants.** A mutation run (`python3 mutation/run_mutants.py`, not part of `run.sh`) changes the Rust in small "
          "wrong ways and reports for which changes some scenario is shown false.", "",
          "| Operation (Lean model) | Does some proved universal scenario apply to every input? | Said about the returned value | Said about the state afterwards | Scenarios |",
          "|---|---|---|---|---|"]
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
        o.append(f"| `{c['call']}` | {how} | {said_text(c['says']['result'])} | {said_text(c['says']['state'])} | "
                 + "; ".join(f"{i.rsplit('.', 1)[1]}: {s}" for i, _, s in c["scenarios"]) + " |")
    o.append("")
    ms = mutation_summary(mut)
    if not ms:
        o += ["No mutation results found (`mutation/results.json`). Run `python3 mutation/run_mutants.py`.", ""]
    else:
        o += [f"Mutation run of {ms['at']}: {ms['total']} mutants of `wallet/src/lib.rs` and `ledger/src/lib.rs`. "
              f"**A scenario is shown false of {ms['shown_false']} of them** (an example row differs on the compiled Rust, or the search "
              f"finds a counterexample). For {len(ms['lemma_only'])} more ({', '.join(m['id'] for m in ms['lemma_only']) or '-'}) "
              f"the run fails only because a hand-written proof or lemma stopped compiling, which is not detection by the scenarios. "
              f"{ms['total'] - ms['killed']} make no difference to the run at all. " + ("These results are for the current Rust, features, glossary and proofs."
                                                         if ms["current"] else
                                                         "**These results are for an OLDER version of the Rust, features, glossary or proofs; rerun.**"), "",
              "A lost proof means the proof (or a lemma it depends on) no longer compiles; it does not by itself mean the "
              "scenario's statement is false of the mutant. A new counterexample does.", "",
              "| Mutant | Operation | What was changed | Crate unit tests | Examples rows on Rust | Proofs lost | New counterexamples | Verdicts that changed | A scenario shown false | Run fails |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for m in mut["mutants"]:
            o.append(f"| {m['id']} | `{m['fn']}` | {m['description']} | {m['unit_tests']} | {m['rows_on_rust']} | "
                     f"{len(m.get('proof_broke', [])) or 'none'} | {len(m.get('search_found', [])) or 'none'} | {m['proof_layer']} | "
                     f"{'yes' if ms['false_of'](m) else '**NO** (lost proof only)' if m['killed_by_scenarios'] else '**NO**'} | "
                     f"{'yes' if m['killed_by_scenarios'] else '**NO**'} |")
        o.append("")

    o += ["## Suite adequacy note", "",
          "**Informational. It changes no verdict and never fails a run.** A single proved scenario is not expected to pin behaviour: "
          "\"a transfer never changes the total\" is also true of code that rejects every transfer. The question here is about "
          "the suite. For each operation, trivial implementations are generated as Lean models of exactly the type of the "
          "Aeneas-generated model (`type_of%`), and each proved universal scenario is stated again with the trivial model in place "
          "of the call:", "",
          "| Trivial implementation | What it does |", "|---|---|",
          "| reject-all | always answers with a rejecting value and leaves the state as it was |",
          "| no-op | always answers with a success value and leaves the state as it was (does nothing but report success) |",
          "| identity | answers as the code does, but never changes the state |",
          "| constant | always answers the same value; the state is left as it was, or reset to a fixed one |", "",
          "A scenario **rules out** a trivial implementation when the search finds an input on which the scenario is false of it "
          "(the same boundary grid as the counterexample search; a kernel-checked refutation at that input is attempted). A suite "
          "rules it out when one of its scenarios does, and **still allows** it otherwise. \"Still allows\" is proved for all inputs "
          "only where it says so; otherwise it means no scenario was shown false of it on the grid. Scenarios tagged `@control` and "
          "scenarios that are not proved are not counted. Which result values count as a rejection or a success is stated in "
          "`glossary.yaml` (`trivial`).", ""]
    note = ctx["note"]
    if not note["ran"]:
        o += [f"**Not computed in this run:** {note['why']}.", ""]
    else:
        if note["why"]:
            o += [f"**Incomplete:** {note['why']}.", ""]
        dec = ctx["decided"]
        nk = sum(d["evidence"] == "kernel-checked" for d in dec.values())
        o += [f"{len(dec)} (scenario, trivial implementation) pairs were checked: the scenario is false of the trivial implementation for "
              f"{sum(d['result'] == 'ruled-out' for d in dec.values())} (an input is given for each), proved to hold of it for all inputs for "
              f"{sum(d['result'] == 'holds' for d in dec.values())}, and neither for "
              f"{sum(d['result'] == 'not-ruled-out' for d in dec.values())} (no input found on the grid, no proof). "
              f"{nk} of the {len(dec)} results are kernel-checked; the rest rest on evaluation by the Lean interpreter (tested).", "",
              "| Operation (Lean model) | Proved universal scenarios counted | The suite as a whole | Trivial implementations still allowed |",
              "|---|---|---|---|"]
        for call, nu, ni, lines, cands in suite_table(gr):
            al = [c for c in cands if c["state"] == "allowed"]
            o.append(f"| `{call}` | {nu}" + (f" (and {ni} literal example{'s' if ni != 1 else ''}, counted separately)" if ni else "")
                     + f" | {'<br>'.join(l.replace('|', chr(92) + '|') for l in lines)} | "
                     + ("<br>".join(f"{c['kind']}: {c['label']}" + (" (proved to satisfy every scenario counted)" if c["holds_proved"] else "")
                                    + (" (ruled out by a literal example only)" if c["ruled_out_by_examples"] else "") for c in al) or "none found")
                     + " |")
        o += ["", "The per-rule line (\"suite rules out ...; still allows ...\") is in each rule's block below. Where a rule or a single "
                  "scenario would on its own also be true of a trivial implementation that the wider suite rules out, the block says so; "
                  "that is the normal case and not a defect of the rule.", ""]

    o += ["## Layered evidence from one compiled rule", "",
          "From the composition tree that gives a sentence its Lean statement and its echo, `clausal gen` also writes a property test and a "
          "bounded-model-checking harness (`evidence/`, generated; `clausal/evgen.py`). No test code is written per rule: both assert one "
          "generated predicate, straight-line Rust over one typed reading per Clausebook piece (`evidence/src/typed.rs`). The property test's "
          "generators are derived from the types of the rule's variables and from its Givens. The bounded check runs each rule at every rung of "
          "one fixed ladder of sizes. Every input either of them finds false is evaluated on the Lean model through the reading: if it fails "
          "there too it becomes the reading's counterexample and gets a kernel-checked refutation; if the model does not fail where the compiled "
          "Rust did, the verdict is flagged MODEL MISMATCH. Each rule's block below has the ladder: example rows, property test, bounded check, "
          "proof, what each rests on, and which is the strongest evidence held. Nothing is called proved without a kernel-checked theorem.", ""]
    o += evidence.overview(ctx.get("evidence"))
    fed = [(rid, r) for rid, r in ((ctx.get("evidence") or {}).get("readings") or {}).items() if r["witnesses"]]
    if fed:
        o += ["| Reading | Source | Falsifying input | Compiled Rust | Lean model |", "|---|---|---|---|---|"]
        for rid, r in fed:
            for w in r["witnesses"]:
                o.append(f"| `{rid}` | {w['source']} | `{json.dumps(w['values'], ensure_ascii=False)}` | {w['rust']} | "
                         + ("**MODEL MISMATCH**: " if w.get("mismatch") else "") + f"{w.get('model')} |")
        o.append("")
    vmap = {v.sc.id: v for v in verdicts}
    o += ["## Rules and their scenarios", "",
          "One block per `Rule:` (and one per feature for scenarios that sit under no rule), generated from `out/graph.json`: the rule "
          "line, **its compiled reading echoed in English**, the verdict of the rule statement, the scenarios beneath it and whether each is "
          "a part the rule is proved from, the example rows, the suite note, and what the result rests on. Beneath each block: the rule's "
          "Lean statement, then every scenario with its own reading, verdict and (folded) Lean.", ""]
    for blk in blocks:
        o += [f"### {blk['title']}", "", "```text"] + rules.render(blk) + ["```", ""]
        if blk["kind"] == "rule" and blk["reading"].get("compiled"):
            o += ["<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>", "", "```lean",
                  blk["reading"]["lean"], "```", "", "</details>", ""]
        for s_ in blk["scenarios"]:
            v = vmap.get(s_["id"])
            if v is None:
                continue
            sc = v.sc
            o += [f"#### {v.headline}: {sc.name}", "",
                  f"`{sc.feature.path}:{sc.line}`  id `{sc.id}`" + (f"  tags `{' '.join(sc.all_tags)}`" if sc.all_tags else ""), "",
                  "```gherkin", sc.text, "```", ""]
            if isinstance(v.reading, Reading):
                o += ["Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):", "", "```text"]
                o += vreport.echo_lines(v.reading) + ["```", ""]
            o += ["```text", f"{v.headline}  {sc.name}"] + ["  " + l for l in v.lines] + ["```", ""]
            if isinstance(v.reading, Reading) or isinstance(v.r, Bound):
                o += ["<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>", ""]
                if isinstance(v.reading, Reading):
                    o += [f"Compiled reading (`lean/Wallet/Readings.lean`), from pieces `{', '.join(v.reading.used)}`:", "", "```lean",
                          v.reading.lean_def(), "```", ""]
                if v.new:
                    o += ["Flat proof obligation, generated from the pieces (`lean/Wallet/Obligations.lean`); a NEW sentence has no flat "
                          "statement in the old glossary:", "", "```lean", ppath.obligation_text(v.reading.id), "```", ""]
                    pp = proof_path(sc.id)
                    if pp.exists() and v.status.startswith("PROVED"):
                        o += [f"Supplied proof of the obligation (`{pp.relative_to(ROOT)}`):", "", "```lean",
                              "theorem " + pp.read_text().split("\ntheorem ", 1)[-1].rstrip(), "```", ""]
                if isinstance(v.r, Bound):
                    o += ["Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):", "", "```lean", emit.statement(v.r), "```", ""]
                    pb = proof_block(v.r.id)
                    if pb and v.status.startswith("PROVED"):
                        o += [f"Proof of the flat statement (`{pb[3]}`):", "", "```lean", pb[0], "```", ""]
                o += ["</details>", ""]
    o += vreport.frames_section(st, ctx)
    o += vreport.vocabulary_section(st, ctx, verdicts, list(rvs.values()))
    o += vreport.regression_section(st, ctx, verdicts)
    o += ppath.end_to_end_section(st, ctx, verdicts, list(rvs.values()))
    o += vreport.new_sentences_section()
    o += ["## The old whole-phrase glossary (the flat statements and the Rust steps)", "",
          "NO LONGER the link from English to Lean: that is the Clausebook above. These entries are what the flat statements of the OLDER "
          "scenarios are written with (each proved equivalent to its reading). The cucumber steps are no longer keyed by them (a step is the "
          "composition tree of its pieces), and a NEW sentence needs no entry here. "
          "Each English phrase and the one Lean definition (or model function) it is bound to: `glossary.yaml`, "
          "`lean/Wallet/Vocab.lean` and `lean/Ledger/Vocab.lean`. "
          "The last column compares that Lean definition with a second, independently written reading of the same phrase "
          "(the whole-phrase Rust predicate in `wallet-bdd/src/lib.rs`) on a grid of arguments. "
          "Agreement does not show that either reading matches the English; disagreement shows that one of them is wrong.", "",
          "| Id | Kind | English phrase | Lean | Definition | Sign-off | Lean vs Rust reading |", "|---|---|---|---|---|---|---|"]
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
                 f"{rd} |")
    o += ["", f"{n_unrev} of {len(gl.entries)} entries are unreviewed. Record a review with "
              "`python3 -m clausal review <id> --reviewer <name>`; any later change to the phrase, its argument order or its "
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
          "- **clausal**: untrusted generator. Defences: Lean type-checks its output; the audit compares the constants in "
          "each elaborated statement with the glossary entries of the scenario's steps; the statement is printed above.",
          "- **The audit** (`lean/Bdd/Audit.lean`, about 120 lines): reads from the Lean environment which axioms each theorem uses, "
          "that each proof's type is exactly its scenario's statement, and which constants statements and definitions mention.",
          "- **Glossary**: `glossary.yaml` + `lean/Wallet/Vocab.lean` + `lean/Ledger/Vocab.lean`. The audit checks that no Given/Then definition "
          "depends on a model function"
          + ("" if not audit else ": " + ("passed for all " + str(len(audit["defs"])) + " definitions."
                                           if not any(d["model_deps"] for d in audit["defs"].values()) else "**FAILED**.")),
          "- **The Rust side** (`wallet-bdd/`): one Rust reading per Clausebook piece and an evaluator of composition trees "
          "(`src/pieces.rs`), ONE generic cucumber step (`tests/bdd.rs`) and the grid evaluation (`tests/grid.rs`). No step and no predicate "
          "is written per sentence. The trees come from clausal (`build/trees.json`, untrusted); a wrong tree or a wrong Rust reading shows "
          "up as a disagreement with the Lean side on generated inputs, or as an Examples row that differs between the compiled Rust and the model.",
          "- **Second reading of each OLD phrase**: the whole-phrase Rust predicates in `wallet-bdd/src/lib.rs` are no longer asserted by any "
          "cucumber step; they are still compared with the old glossary's Lean definitions on a grid of arguments (table above).",
          "- **The generated harnesses** (`evidence/`): `clausal/evgen.py` (untrusted generator), one typed Rust reading per Clausebook piece "
          "(`evidence/src/typed.rs`, hand-written once; a third reading by the same author) and a generic runner (`evidence/src/main.rs`). "
          "Defence: at every generated case the generated predicate is compared with the tree evaluator of `wallet-bdd/src/pieces.rs`, which is "
          "itself compared with the Lean pieces on the grid. Under Kani only the typed reading runs; a failing Kani input is replayed on the "
          "compiled Rust through the property-test runner, tree evaluator included. **proptest** for sampling and shrinking; **Kani and CBMC** "
          "for every bounded result.",
          "- **Lean kernel** and the axioms `propext`, `Classical.choice`, `Quot.sound`; **rustc** for everything said about the compiled Rust.", ""]
    o += ["## What this run did not check", "",
          "- A property test that finds nothing has sampled; a bounded check that verifies has covered every input up to the sizes it "
          "names and nothing larger, and where it gives no answer in the time allowed it has shown nothing. Neither is a proof, and the "
          "block of each rule says which of them it holds.",
          "- The generators of the property tests are generic (types and Givens). A falsifying input that needs a structure they are "
          "unlikely to draw, or a value that appears only in the code, is not found by them; the bounded check finds such a value "
          "when it lies within its sizes.",
          "- That any glossary definition means what its English phrase says. Only a person can.",
          "- That the echo of a reading says what the author meant. It is printed so that a person can check; nobody has (no trial with "
          "readers has been run on these generated echoes).",
          "- That any Clausebook piece means what its English says. Only a person can; no piece is signed.",
          "- A `Rule:` statement is tied to its scenarios in one direction only: the scenarios entail the rule. That the rule says everything "
          "its scenarios say is not claimed, and usually false (a rule is one sentence; its suite says more).",
          "- A rule statement with a hand-written proof rests on the loop lemmas, not on the scenarios beneath it.",
          "- That the Rust reading of a Clausebook piece (`wallet-bdd/src/pieces.rs`) and its Lean definition say the same is TESTED, not "
          "proved: every compiled reading is evaluated on its grid of generated inputs on both sides and the results are compared. A piece "
          "is compared only through the readings that use it, so a piece no sentence uses is not compared at all (the Clausebook table "
          "says which), and the two sides were written by one author.",
          "- A `Rule:` line with no scenario beneath it has no Examples rows: on the compiled Rust it is evaluated on generated inputs only. "
          "A rule that compares two calls cannot have a Gherkin scenario at all (a scenario is one run).",
          "- A flat proof obligation is generated text. What ties it to the reading is one kernel-checked equivalence per sentence; if that "
          "script fails the sentence cannot be PROVED, whatever is proved of the obligation.",
          "- The suite adequacy note and the input-coverage table are generated from the flat statements of the old glossary, so the NEW "
          "sentences are in neither.",
          "- The definition of each frame and its executable reading are compared on generated inputs, not proved equal. The frame with "
          "no surface form (counting with a number) is compared on a few hand-written instances only.",
          "- The suite adequacy note covers four kinds of trivial implementation, generated from the result values listed in the "
          "glossary. An implementation that is wrong in some other way is not looked for (the mutation run samples that). "
          "\"Still allows\" without \"proved\" means only that the search grid holds no input on which a scenario fails; "
          "pairs with several Whens, and the `identity` variant (which calls the real model), get no kernel attempt.",
          "- A scenario with several Whens says that each call returns and constrains the state after the LAST one "
          "(and the last call's result). Results of earlier Whens are not constrained, no kernel refutation is generated "
          "for such a scenario, and it does not count towards input coverage.",
          "- A counterexample to a scenario about a loop is confirmed in the kernel only if a hand-proved lemma about that loop "
          "says enough at that input (here: the exact-result lemmas in `lean/Ledger/Lemmas/`). Without one the verdict is COUNTEREXAMPLE, not REFUTED.",
          "- The search grid for the ledger has ledgers of up to four accounts and batches of up to four transfers "
          "(two of each length three and four). A fault that needs a fifth loop iteration, or particular amounts, is outside it.",
          "- The boundary grid is small (the product of each parameter's sample values plus literals and their neighbours); "
          "there is no random sampling and no shrinking. A false scenario whose counterexamples all lie away from the boundaries would be TESTED-ONLY, not REFUTED. "
          "The same holds for the grid on which the two readings of a phrase are compared.",
          "- The trivial-Then check is a `simp`/`scalar_tac` attempt. A Then that follows from the Givens by harder reasoning is not flagged, "
          "and a Then that is true but weaker than the English is invisible to it.",
          "- \"Some scenario applies to every input\" is about Givens only. Whether the Thens pin the result down is not checked by anything: "
          "the report lists the Thens per output for a person to judge, and the mutation run samples it with the mutants it happens to contain.",
          "- For the ledger's loops the universal scenarios do NOT determine the result. They state: the total is conserved, the count is at most "
          "the batch length, a batch stops only at a transfer that is invalid on the ledger it left, a rejected whole batch changes nothing, and what "
          "happens when the first transfer is invalid. They do not state which ledger a partly or fully applied batch leaves, nor that every counted "
          "transfer was really applied. That would need the batch computation written again as a specification in the glossary, which this design "
          "does not allow. The hand-written lemma library does prove the exact result (against its own pure model `runN`), but a lemma is not a scenario.",
          "- A mutant for which the run fails only because a proof or lemma stopped compiling is not counted as detected: the proof could be "
          "rewritten to fit the changed code.",
          "- The derived theorems (`.sat`, `.unsat`, `.refuted`, coverage, trivial-Then attempts) are checked by one `lean` run over "
          "`lean/Run/Audit.lean`, not stored as library modules. Trivial-Then attempts are expected to fail; their errors are in `out/audit.log`.",
          "- Staleness is computed from the digests in `out/graph.json`, but every run regenerates everything, so nothing is ever stale here. "
          "`python3 -m clausal.graphlint out/graph.json --what-if <node-id>` shows what would be.", ""]
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
    # the composable Clausebook: glue theorems, the reading search, sign-off per piece
    ctx["links"], ctx["links_meta"], ctx["rs"] = vreport.load_links(), vreport.load_links_meta(), vreport.load_rsearch()
    ctx["lean_defs"] = vreport.lean_defs(st.voc)
    ctx["piece_reviewed"] = vreport.reviewed_pieces(st.voc, ctx["lean_defs"])
    ctx["rust_bits"] = ppath.load_rust_bits() if cuc is not None else None      # every reading on the compiled Rust (tests/grid.rs)
    ctx["piece_cmp"] = ppath.piece_comparison(st, ctx)
    ctx["evidence"] = evidence.load() if cuc is not None else None      # generated property tests and bounded checks (plan node E1)
    verdicts = [Verdict(sc, r, st, ctx) for sc, r in st.results]
    scen = {v.sc.id: v for v in verdicts}
    ctx["rule_verdicts"] = {r.id: vreport.RuleVerdict(r, rd, st, ctx, scen) for r, rd in st.rules}
    rule_verdicts = list(ctx["rule_verdicts"].values())
    # MODEL MISMATCH: an input at which the compiled Rust fails a reading (found by a generated harness) and the Lean model
    # does not. A finding about the translation link; never hidden, and it fails the run.
    for v_, rd_ in [(v, v.reading) for v in verdicts] + [(rv, rv.rd) for rv in rule_verdicts]:
        if not isinstance(rd_, Reading):
            continue
        for w in ((ctx["evidence"] or {}).get("readings", {}).get(rd_.id) or {}).get("witnesses", []):
            if w.get("mismatch"):
                v_.flags.append("MODEL MISMATCH")
                v_.fatal.append(f"MODEL MISMATCH: at {json.dumps(w['values'], ensure_ascii=False)} (found by the generated {w['source']}) the compiled Rust "
                                f"{w['rust']} and the Lean model {w['model']}: the translation link is in question")
                v_.as_expected = False
        p_ = ((ctx["evidence"] or {}).get("readings", {}).get(rd_.id) or {}).get("property", {})
        if p_.get("status") == "mismatch":
            v_.flags.append("READING MISMATCH (generated)")
            v_.fatal.append(f"READING MISMATCH: the generated typed predicate and the tree evaluator disagree: {p_.get('message')}")
            v_.as_expected = False
    cov = coverage(st, verdicts, audit)
    # suite adequacy note (informational): what the search and the kernel attempts said about each (scenario, trivial model) pair
    adq, why = adequacy_search(st)
    ctx["adequacy_audit"] = load_adequacy_audit()
    ctx["decided"] = adequacy.decide(st.bounds, st.triv, adq, ctx["adequacy_audit"])
    ctx["note"] = adequacy.note(st, verdicts, ctx["decided"], ran=bool(adq), why=why)
    gr = build_graph(st, verdicts, cov, ctx, vdefs, rs, mut)
    errs = graphlint.schema_errors(gr) + graphlint.lint(gr)
    if audit is None:
        errs.append("out/audit.log has no AUDIT line: the audit did not run")
    if ctx["links"] is None:
        errs.append("out/links.log has no LINKS line: the link audit did not run, so no reading is tied to a checked statement")
    for it in vreport.load_new_sentences().get("items", []):
        if (it.get("search") or {}).get("diff"):
            errs.append(f"new sentence {it['source']}: the definition and the executable reading of a frame disagree at "
                        + json.dumps(it["search"]["diff"]["values"]))
    for fid, tests in vreport.load_frame_tests().items():
        for t in tests:
            if t["agree"] != t["points"]:
                errs.append(f"frame `{fid}` ({t['what']}): its definition and its executable reading disagree on "
                            f"{t['points'] - t['agree']} of {t['points']} evaluations")
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
    # The per-Rule blocks are computed from the FILE just written and from nothing else, then checked against this run.
    gr_disk = json.loads((OUT / "graph.json").read_text())
    blocks = rules.blocks(gr_disk)
    errs += rules_match(blocks, verdicts)
    (OUT / "report.md").write_text(md_report(st, verdicts, cov, gr_disk, ctx, vdefs, rs, errs, mut, blocks))
    print()
    for v in verdicts:
        mark = "" if v.as_expected else f"   <-- EXPECTED {v.expected}" + (f"; {'; '.join(v.fatal)}" if v.fatal else "")
        print(f"{v.headline}  {v.sc.name}   ({v.sc.feature.path}:{v.sc.line}){mark}")
        if isinstance(v.reading, Reading):      # the echo: how the sentence was read (defaults are in out/report.md)
            for k, l in enumerate(vreport.echo_lines(v.reading, 120, defaults=False)):
                print(("  reading          " if k == 0 else "                   ") + l)
        for l in v.lines:
            print("  " + l)
        extra = [f for f in v.flags if f not in ("TRIVIAL-THEN", "FRAME-TRIVIAL")]
        if extra:
            print("  flags            " + "; ".join(extra))
        print()
    print("Rules (each block is generated from out/graph.json: the rule line, its compiled reading echoed in English, the verdict of the rule "
          "statement, the scenarios beneath it)")
    print()
    for blk in blocks:
        for l in rules.render(blk):
            print(l)
        print()
    print("Which inputs the scenarios apply to, and what they say about the outputs")
    print("  (\"applies to every input\" is about the Givens only; it does not mean the result is pinned down. The Thens are listed so that can be read off.)")
    for c in cov:
        if c["covered"]:
            gq = next(x for x in c["groups"] if x["theorem_ok"] and not x["unproved"])
            print(f"  {c['call']}: some proved universal scenario applies to every input (kernel-checked {gq['name']} over {len(gq['ids'])} scenarios)")
        else:
            print(f"  {c['call']}: NOT SHOWN that some proved universal scenario applies to every input")
        if c["scenarios"]:
            print(f"      said about the returned value:   {said_text(c['says']['result'], md=False)}")
            print(f"      said about the state afterwards: {said_text(c['says']['state'], md=False)}")
    ms = mutation_summary(mut)
    if ms:
        print(f"  mutation run of {ms['at']}: a scenario is shown false of {ms['shown_false']} of {ms['total']} Rust mutants; "
              f"{len(ms['lemma_only'])} more make the run fail only through a lost proof; {ms['total'] - ms['killed']} make no difference"
              + ("" if ms["current"] else "  (OUT OF DATE: rerun python3 mutation/run_mutants.py)"))
        for m in ms["lemma_only"]:
            print(f"    lost proof only (no scenario shown false): {m['id']} ({m['fn']}): {m['description']}")
        for m in ms["survivors"]:
            print(f"    not noticed: {m['id']} ({m['fn']}): {m['description']}")
    else:
        print("  no mutation results (python3 mutation/run_mutants.py)")
    print("Suite adequacy note (informational; changes no verdict): the proved universal scenarios of each operation, as a suite, "
          "against trivial implementations")
    note = ctx["note"]
    if not note["ran"]:
        print(f"  not computed: {note['why']}")
    else:
        dec = ctx["decided"]
        for call, nu, ni, lines, cands in suite_table(gr_disk):
            print(f"  {call}: {lines[0]}")
            for l in lines[1:]:
                print(f"      {l}")
        print(f"  {len(dec)} (scenario, trivial implementation) pairs: false of it for {sum(d['result'] == 'ruled-out' for d in dec.values())}, "
              f"proved to hold of it for {sum(d['result'] == 'holds' for d in dec.values())}, neither for "
              f"{sum(d['result'] == 'not-ruled-out' for d in dec.values())}; {sum(d['evidence'] == 'kernel-checked' for d in dec.values())} kernel-checked"
              + (f"  [INCOMPLETE: {note['why']}]" if note["why"] else ""))
    if rd is not None:
        print(f"Two readings of each Given/Then phrase (Lean definition, Rust predicate): "
              f"{sum(q['agree'] for q in rd.values())} of {sum(q['n'] for q in rd.values())} grid points agree, over {len(rd)} phrases")
    print()
    for e in errs:
        print(f"ERROR: {e}")
    ok = all(v.as_expected for v in verdicts) and all(rv.as_expected for rv in rule_verdicts) and not errs
    counts = {}
    for v in verdicts:
        counts[v.status] = counts.get(v.status, 0) + 1
    print(f"{len(verdicts)} scenarios: " + ", ".join(f"{n} {k}" for k, n in counts.items()))
    rcounts = {}
    for rv in rule_verdicts:
        rcounts[rv.status] = rcounts.get(rv.status, 0) + 1
    print(f"{len(rule_verdicts)} Rule statements: " + ", ".join(f"{n} {k}" for k, n in rcounts.items()))
    for rv in rule_verdicts:
        if not rv.as_expected:
            print(f"  Rule \"{rv.rule.name}\" ({rv.rule.feature.path}:{rv.rule.line}): {rv.status}   <-- EXPECTED {rv.expected}"
                  + (f"; {'; '.join(rv.fatal)}" if rv.fatal else ""))
    nlinked = sum(1 for v in verdicts if v.link_ok and not v.new)
    nboth = sum(1 for v in verdicts if isinstance(v.reading, Reading) and isinstance(v.r, Bound))
    tot_e, tot_a = sum(x.get("evals", 0) for x in ctx["rs"].values()), sum(x.get("agree", 0) for x in ctx["rs"].values())
    print(f"readings: {nlinked} of {nboth} scenario readings proved equivalent to their flat statement (kernel-checked NEW <-> OLD); "
          f"definition and executable reading of the frames agree on {tot_a} of {tot_e} evaluations")
    nnew = [v for v in verdicts if v.new]
    nob = sum(1 for x in ctx["links_meta"].get("oiffs", []) if vreport.lclean(ctx["links"], x[0]))
    print(f"new sentences: {len(nnew)} scenarios read by the Clausebook alone (no entry in the old glossary); flat proof obligations "
          f"generated from the pieces and proved equivalent to their reading for {nob} of {len(ctx['links_meta'].get('oiffs', []))} readings "
          "(those scenarios and every Rule line)")
    rb = ctx.get("rust_bits")
    if rb is None:
        print("compiled Rust: the readings were not evaluated on it in this run")
    else:
        cs = [ppath.compare(rd.id, ctx["rs"].get(rd.id, {}), rb) for rd, _ in st.compiled]
        cs = [c for c in cs if c.get("ran")]
        print(f"compiled Rust: {sum(1 for c in cs if not c['error'])} of {len(st.compiled)} compiled readings evaluated on it through the per-piece Rust readings; "
              f"they agree with the Lean pieces on the Lean model on {sum(c['agree'] for c in cs)} of {sum(c['evals'] for c in cs)} evaluations")
    fp = ctx.get("frame_power")
    if fp is not None:
        ev_ = ctx.get("evidence")
        if ev_ and ev_.get("readings"):
            print("generated evidence: " + evidence.summary_line(ev_).replace("\n  ", "\n                    "))
            ws_ = [w for _, _, w in evidence.witness_list(ev_)]
            print(f"                    falsifying inputs fed back: {len(ws_)}; {sum(w.get('model') == 'fails' for w in ws_)} fail on the Lean model too, "
                  f"{sum(bool(w.get('mismatch')) for w in ws_)} MODEL MISMATCH")
        print("frame comparison: " + ("every frame was compared at a false claim and at a silent call at least once (toy operation included)" if not fp
                                      else "UNTESTED for " + "; ".join(f"{k} (no {v})" for k, v in fp.items())))
    nocall = [x for x in list(verdicts) + rule_verdicts if "COVERS NO CALL ON THE GRID" in x.flags]
    if nocall:
        print(f"  {len(nocall)} readings have a clause about accepted or rejected calls only that covered no call on the grid (flag COVERS NO CALL ON THE GRID)")
    weak = [v for v in verdicts if v.substantive and v.substantive[0] < v.substantive[1]]
    if weak:
        print(f"  of the proved ones, {len(weak)} have a Then that says nothing about the code: " + ", ".join(v.sc.id.rsplit('.', 1)[1] for v in weak))
    unrev = sum(1 for v in verdicts if v.status.startswith("PROVED") and v.unreviewed)
    if unrev:
        print(f"  {unrev} proved scenarios rest on glossary entries with no valid sign-off"
              + (" (--strict: counted as failures)" if ctx["strict"] else " (./run.sh --strict makes this a failure)"))
    punrev = sum(1 for v in verdicts if v.status.startswith("PROVED") and v.pieces_unreviewed)
    if punrev:
        print(f"  {punrev} proved scenarios rest on Clausebook pieces with no valid sign-off"
              + (" (--strict: counted as failures)" if ctx["strict"] else " (./run.sh --strict makes this a failure)"))
    print(f"graph: {len(gr['nodes'])} nodes, {len(gr['edges'])} edges -> out/graph.json;  report -> out/report.md")
    print("RESULT: " + ("every scenario got its expected verdict" + ("" if not rule_verdicts else " and every Rule statement its expected one")
                        if ok else "MISMATCH between expected and actual verdicts, or errors (see above)"))
    return 0 if ok else 1


def cmd_steps(st: State) -> int:
    """List the step forms the generic cucumber step is registered for (build/trees.json, written by `gen`).
    There are no hand-written steps to compare with the glossary any more: a step is the composition tree of its pieces."""
    p = ROOT / "build" / "trees.json"
    if not p.exists():
        print("build/trees.json is missing (run `python3 -m clausal gen`)")
        return 1
    tr = json.loads(p.read_text())
    for e in tr["steps"]:
        print(f"{e['kind']:6} {e['regex']}   [{e['example']}]")
    for x in tr["problems"]:
        print(f"CLASH  {x}")
    print(f"step forms compiled to composition trees: {len(tr['steps'])} "
          f"({sum(e['kind'] == 'given' for e in tr['steps'])} Given, {sum(e['kind'] == 'when' for e in tr['steps'])} When, "
          f"{sum(e['kind'] == 'then' for e in tr['steps'])} Then); hand-written steps: 0; clashes: {len(tr['problems'])}")
    return 1 if tr["problems"] else 0


def cmd_review(st: State, argv) -> int:
    """Record that a person has read a glossary entry and its Lean definition and agrees they say the same thing.
    The record holds the digests of the phrase (with its argument order) and of the definition it binds to;
    it is void as soon as either changes."""
    if len(argv) != 3 or argv[1] != "--reviewer":
        print("usage: python3 -m clausal review <entry-id|all> --reviewer NAME")
        return 2
    # a piece of the composable Clausebook (clausebook.yaml)? `all` signs the pieces AND the old glossary entries.
    if argv[0] in vreport.all_ids(st.voc):
        return vreport.review(st.voc, argv[0], argv[2])
    if argv[0] == "all":
        vreport.review(st.voc, "all", argv[2])
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
