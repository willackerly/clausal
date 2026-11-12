"""clausal vreport: what the report says about the COMPOSABLE CLAUSEBOOK.

  * the echo: every Rule's and every scenario's compiled reading in slot-structured English (applies to /
    assuming / then / defaults applied), printed beside the sentence as the primary thing a reader sees;
  * the verdict of each `Rule:` statement and how it relates to the scenarios beneath it;
  * sign-off per PIECE, void when the piece's entry or its Lean definition changes;
  * the frame library table, the two readings of each frame compared on generated inputs, the pieces by
    kind, and the regression table NEW ↔ OLD.
"""
from __future__ import annotations

import datetime
import json
import re

from .core import Problem, sha
from .pipeline import LEAN, OUT, ROOT, rule_proof_module, rule_proof_path
from .rsearch import covers_no_call
from .vocab import Reading, base_cat

STD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
INTERNAL = {"Frames.Op.HoldsAt", "Frames.Op.Holds", "Frames.Op.HoldsAt2"}     # not frames: a reading may not mention them


def allowed_consts(voc, rd) -> set:
    """The constants OF THIS PROJECT a compiled reading may mention: the frames of the pieces it uses, the Lean
    definitions those pieces name (`defs:` / `consts:`; for a frame only the frame itself, never `HoldsAt`), its
    operations, and the types and literal constructors of the Clausebook. Everything else of the project (the old
    glossary, a model function, the internals of the frame library) is outside the allowlist."""
    tok = lambda t: set(re.findall(r"[A-Za-z_][\w.']*", str(t)))
    out = set()
    for i in rd.used:
        if i in voc.ops:
            o = voc.ops[i]
            out |= {o["lean"]} | tok(o["answer"]) | {v for k, v in (o.get("internal") or {}).items() if k != "echo"}
        elif i in voc.pieces:
            p = voc.pieces[i]
            out |= {p["lean"].split()[0]} if p["kind"] == "frame" else set(p.get("defs", []))
            out |= set(p.get("consts", []))
    for pt in voc.pts.values():
        out |= tok(pt.get("lean", "")) | tok(pt.get("lean_literal", "")) | tok(" ".join(map(str, (pt.get("enum") or {}).values())))
    for a in voc.actors.values():
        out |= tok(a["lean"])
    return out


def outside_allowlist(links, voc, rd) -> list:
    """Project constants the reading mentions that its pieces do not account for (the generator is untrusted)."""
    c = (links or {}).get("consts", {}).get(rd.name, {})
    if "project" not in c:                      # an audit without the project list: the old blocklist
        return sorted(set(c.get("consts", [])) & INTERNAL)
    ok = allowed_consts(voc, rd)
    # `<some reading>.reading._proof_N`: auxiliary proofs Lean makes while elaborating a literal (a bound such as
    # 30 ≤ 2^64 - 1) and shares between readings that use the same literal. Proofs, not content.
    return sorted(x for x in c["project"] if x not in ok and not re.fullmatch(r"(Spec|Rule)\..*\.reading\._proof_\d+", x))
SLOTS = ("applies to", "covers", "assuming", "then", "accepted", "defaults", "not default")


# --------------------------------------------------------------------------- inputs

def load_links():
    p = OUT / "links.log"
    if not p.exists():
        return None
    for line in p.read_text().splitlines():
        if line.startswith("LINKS\t"):
            return json.loads(line.split("\t", 1)[1])
    return None


def load_links_meta() -> dict:
    p = ROOT / "build" / "links.json"
    return json.loads(p.read_text()) if p.exists() else {"iffs": [], "sats": [], "skipped": [], "imps": [], "noglue": {}, "nots": [],
                                                         "proofs": [], "consts": [], "holds": [], "oiffs": [], "oproofs": [], "ofail": {}}


def load_rsearch() -> dict:
    p = OUT / "rsearch.json"
    return json.loads(p.read_text()) if p.exists() else {}


def load_frame_tests() -> dict:
    """frame id -> {points, agree, what}: the frames with no surface form, from lean/Run/FrameTests.lean."""
    p = OUT / "frametests.log"
    out = {}
    if p.exists():
        for line in p.read_text().splitlines():
            q = line.split("\t")
            if q[0] == "FTEST" and len(q) >= 6:
                out.setdefault(q[1], []).append({"what": q[2], "points": int(q[3]), "agree": int(q[4]), "false": int(q[5]),
                                                 "silent": int(q[6]) if len(q) > 6 else None})
    return out


def load_new_sentences() -> dict:
    p = OUT / "new_sentences.json"
    return json.loads(p.read_text()) if p.exists() else {}


def lthm(links, name) -> dict:
    return (links or {}).get("theorems", {}).get(name) or {}


def lclean(links, name) -> bool:
    t = lthm(links, name)
    return bool(t and t["exists"] and t.get("is_theorem") and t.get("type_ok") and set(t["axioms"]) <= STD_AXIOMS
                and not t.get("uses_proof"))


def lwhy(links, name) -> str:
    t = lthm(links, name)
    if not links:
        return "the link audit did not run"
    if not t.get("exists"):
        return "no such theorem was generated"
    if "sorryAx" in t["axioms"]:
        return "the generated proof script failed (see out/links.log)"
    if not t.get("type_ok"):
        return "the theorem does not have exactly the expected type"
    if t.get("uses_proof"):
        return "the proof of the equivalence uses a proof of one of its two sides, so it does not compare what they say"
    return f"non-standard axioms {t['axioms']}"


def lean_defs(voc) -> dict:
    """Lean name -> {text, file, line, end} for every declaration of the Clausebook's Lean files."""
    out = {}
    for ns, files in voc.raw["lean_files"].items():
        for rel in files:
            lines = (ROOT / rel).read_text().splitlines()
            i = 0
            while i < len(lines):
                m = re.match(r"(?:@\[[^\]]*\]\s*)?(?:def|abbrev|inductive|structure|theorem)\s+([\w.']+)", lines[i])
                if m:
                    j = i + 1
                    while j < len(lines) and lines[j].strip() and not re.match(r"(/--|@\[|def |abbrev |theorem |instance |inductive |structure |end |namespace |-- )", lines[j]):
                        j += 1
                    out[f"{ns}.{m.group(1)}"] = {"text": " ".join(x.strip() for x in lines[i:j]), "file": rel, "line": i + 1, "end": j}
                    i = j
                else:
                    i += 1
    return out


# --------------------------------------------------------------------------- sign-off per piece

def entry_text(voc, id_: str) -> str:
    """The YAML text of one entry (piece, operation or idiom): from its `- id:` line to the next entry."""
    if id_ in voc.raw["defaults"]:                  # a default: its id and its one line of text
        return f"{id_}: {voc.raw['defaults'][id_]}"
    a = voc.line_of(id_)
    if not a:
        return id_
    lines = voc.book_of(id_).lines                  # the entry's own book: moving an entry between books keeps its text
    b = a
    while b < len(lines) and not re.match(r"\s*-\s*\{?\s*id:", lines[b]) and not re.match(r"[a-z_]+:\s*$", lines[b]) \
            and not lines[b].lstrip().startswith("# ====="):
        b += 1
    return "\n".join(l for l in lines[a - 1:b] if l.strip() and not l.strip().startswith("#"))


def all_ids(voc) -> list:
    """Every entry a person signs: operations, pieces, idioms, coverage lines, the grammar of a Rule line, the defaults."""
    return (list(voc.ops) + list(voc.pieces) + list(voc.idioms) + list(voc.coverage) + list(voc.grammar) + list(voc.raw["defaults"])
            + list(voc.separations))


def entry_of(voc, id_: str) -> dict:
    if id_ in voc.raw["defaults"]:
        return {"id": id_, "kind": "default", "echo": voc.raw["defaults"][id_], "forms": []}
    return (voc.ops.get(id_) or voc.pieces.get(id_) or voc.idioms.get(id_) or voc.coverage.get(id_) or voc.separations.get(id_)
            or voc.grammar[id_])


def def_names(voc, id_: str) -> list:
    e = entry_of(voc, id_)
    if id_ in voc.ops:
        return [e["lean"]]
    return list(e.get("defs", []))


def piece_digest(voc, defs: dict, id_: str) -> str:
    """What a sign-off of a piece is a sign-off OF: its Clausebook entry and the text of every Lean definition it names."""
    parts = [entry_text(voc, id_)] + [defs.get(d, {}).get("text", f"MISSING {d}") for d in def_names(voc, id_)]
    # ... and the text of every default the entry names (`defaults:` / `removes:`): the reading rules printed with it.
    # (Plan node Q2: the coverage lines and the defaults they cite are signed with the `coverage:` entry that prints them.)
    e = entry_of(voc, id_)
    parts += [f"{d} {voc.raw['defaults'].get(d, 'MISSING')}" for d in list(e.get("defaults", [])) + list(e.get("removes", []))]
    if id_ in voc.separations:
        # A separation is signed AS SEPARATING: the sign-off is of the two entries as they are written today and of what each
        # of its sentences compiles to today. Change a form of either piece, or a word that changes either reading, and it is void.
        from . import book
        parts += book.separation_parts(voc, e)
    return sha("\n".join(parts))


def book_signoff(book) -> dict:
    """The sign-offs stored beside one book (clausebook/<book>.signoff.json): only of entries that book defines."""
    p = book.signoff_path
    return json.loads(p.read_text()) if p.exists() else {}


def load_piece_signoff(voc) -> dict:
    """Entry id -> sign-off, read from the sign-off file of the book that DEFINES the entry. A record of an entry in
    another book's file is not a sign-off of it (an entry moved between books has to be signed again where it now is)."""
    out = {}
    for b in voc.books:
        out.update({i: r for i, r in book_signoff(b).items() if voc.home.get(i) is b})
    return out


def reviewed_pieces(voc, defs: dict) -> set:
    so = load_piece_signoff(voc)
    return {i for i in all_ids(voc) if so.get(i, {}).get("digest") == piece_digest(voc, defs, i)}


def review(voc, which: str, reviewer: str) -> int:
    defs = lean_defs(voc)
    ids = all_ids(voc) if which == "all" else [which]
    changed = {}
    for i in ids:
        b = voc.book_of(i)
        so = changed.setdefault(b.rel, (b, book_signoff(b)))[1]
        so[i] = {"reviewer": reviewer, "date": datetime.date.today().isoformat(), "digest": piece_digest(voc, defs, i)}
        e = entry_of(voc, i)
        print(f"signed off piece {i} ({e.get('kind', 'domain')}, {b.rel}): {e.get('form') or (e.get('when') or e.get('forms') or e.get('then_forms') or [''])[:1]}")
    for b, so in changed.values():
        b.signoff_path.write_text(json.dumps(so, indent=2) + "\n")
    return 0


def kind_of(voc, id_: str) -> str:
    return entry_of(voc, id_).get("kind", "domain")


# --------------------------------------------------------------------------- the echo

def echo_lines(rd: Reading, width: int = 108, defaults: bool = True) -> list:
    """The slot-structured English reading as text lines: a 12-wide slot column, the text wrapped beside it.
    `defaults=False` leaves the list of defaults out (the terminal; the report always prints them)."""
    import textwrap
    out = []
    in_defaults = False
    for slot, text in rd.echo:
        in_defaults = slot == "defaults" or (in_defaults and slot == "")
        if in_defaults and not defaults:
            continue
        w = textwrap.wrap(text, width, break_on_hyphens=False) or [""]
        out.append(f"{slot:<12}{w[0]}")
        out += [f"{'':<12}{x}" for x in w[1:]]
    return out


def summary_sentence(rd: Reading) -> str:
    """The reading as ONE sentence, put together from the slots of the echo (without the list of defaults): the form the
    per-Rule block leads with. The slot-by-slot echo, with every default spelled out, is printed beneath it."""
    parts, in_tail = [], False
    for slot, text in rd.echo:
        if slot in ("defaults", "not default", "accepted"):
            in_tail = True
        elif slot:
            in_tail = False
        if in_tail:
            continue
        if slot == "applies to":
            parts.append("for " + text)
        elif slot == "assuming":
            if not text.startswith("nothing"):
                parts.append("assuming " + text)
        elif slot == "then":
            parts.append("then " + text)
        else:
            parts.append(text)
    return "; ".join(parts)


def reading_attrs(st, rd, ctx) -> dict:
    """What the graph stores about a compiled reading (so the per-Rule blocks can be rendered from the graph alone)."""
    voc = st.voc
    if isinstance(rd, Problem):
        return {"compiled": False, "status": rd.status, "message": rd.message, "hint": rd.hint}
    return {"compiled": True, "name": rd.name, "lean": rd.lean_def(), "echo": [list(x) for x in rd.echo], "defaults": rd.defaults,
            "regular": rd.regular,
            "pieces": [{"id": i, "kind": kind_of(voc, i), "signed": i in ctx["piece_reviewed"],
                        "by": load_piece_signoff(voc).get(i, {}).get("reviewer") if i in ctx["piece_reviewed"] else None} for i in rd.used]}


# --------------------------------------------------------------------------- Rule verdicts

class RuleVerdict:
    """The verdict of one `Rule:` statement.

    PROVED-FOR-ALL   the generated glue `<rule>.from_scenarios` is kernel-checked AND every scenario it rests on is
                     PROVED-FOR-ALL; or a hand-written proof of exactly the rule statement is kernel-checked; or a
                     supplied proof of the rule's generated flat obligation is kernel-checked and carried to the
                     statement through the kernel-checked equivalence `<rule>.reading_iff_obligation`
    REFUTED          the reading search found an input at which the statement is false, and `¬ <rule>.reading` is
                     kernel-checked at that input            (COUNTEREXAMPLE: found, not confirmed in the kernel)
    TESTED-ONLY      compiled and evaluated on generated inputs (the Lean model; the compiled Rust when the Rust side
                     ran), no counterexample, no proof. (Called NOT-PROVED before the Rust side evaluated rule statements.)
    UNBOUND / ILL-TYPED / AMBIGUOUS   the rule line is not a composition of Clausebook pieces: no statement
    SAYS-NOTHING     the rule line is a composition, but a claim narrowed to accepted or to rejected calls holds of every
                     operation whatever (clausal/narrowing.py; lean/Frames/Narrowing.lean): refused, no statement"""

    def __init__(self, rule, rd, st, ctx, scen: dict):
        self.rule, self.rd = rule, rd
        self.lines, self.flags, self.fatal = [], [], []
        self.how, self.counterexample, self.parts, self.rests_on = "", None, [], []
        self.rust_grid, self.proof = {"ran": False}, None      # Lean vs compiled Rust on the grid; {kind, theorems, axioms} when proved or refuted
        self.pieces = [] if isinstance(rd, Problem) else rd.used
        self.unreviewed = [i for i in self.pieces if i not in ctx["piece_reviewed"]]
        tags = rule.tags
        self.expected = ("REFUTED" if "@expect-refuted" in tags else "UNBOUND" if "@expect-unbound" in tags
                         else "TESTED-ONLY" if "@expect-unproved" in tags else "PROVED-FOR-ALL")
        self.status = self.compute(st, ctx, scen)
        if ctx["strict"] and self.status.startswith("PROVED") and self.unreviewed:
            self.fatal.append(f"--strict: the rule statement rests on {len(self.unreviewed)} Clausebook pieces with no valid sign-off")
        self.as_expected = self.status == self.expected and not self.fatal

    def compute(self, st, ctx, scen) -> str:
        rd, L = self.rd, self.lines
        links, meta, rs_all = ctx["links"], ctx["links_meta"], ctx["rs"]
        if isinstance(rd, Problem):
            L.append(rd.message)
            L += ["  " + h for h in rd.hint.splitlines()]
            L.append("the rule line was read and refused: its statement would hold of every operation, so none was generated for it"
                     if rd.status == "SAYS-NOTHING" else
                     "the rule line was read and refused: one clause is narrowed or scoped by more than one word, and which calls it "
                     "covers is not guessed, so no statement was generated for it"
                     if rd.code == "NARROWED-TWICE" else
                     "the rule line was read and refused: a narrowing word stands on a sequence with a tie, and which call of the "
                     "sequence it is said of is not guessed, so no statement was generated for it"
                     if rd.code == "NARROWED-TIE" else
                     "the rule line is written with a form, or in a shape, that the Clausebook replaced (one live form per piece per "
                     "position): it is refused and the form to write is named, so no statement was generated for it"
                     if rd.code == "RETIRED-FORM" else
                     "the rule line is not a composition of Clausebook pieces, so no statement was generated for it")
            return rd.status
        rs = rs_all.get(rd.id, {})
        off = outside_allowlist(links, st.voc, rd)
        if off:
            self.flags.append("GENERATOR-CHECK-FAILED")
            self.fatal.append("GENERATOR-CHECK-FAILED: the reading mentions " + ", ".join(off) + ", which none of its Clausebook pieces accounts for")
        if rs.get("diff"):
            self.flags.append("FRAME READINGS DISAGREE")
            self.fatal.append("FRAME READINGS DISAGREE: the definition and the executable reading of a frame differ at " + json.dumps(rs["diff"]["values"]))
        from . import ppath
        cmp_ = ppath.apply_compare(self, rd.id, rs, ctx)
        tested = ""
        if "skipped" in rs:
            tested = f"not searched: {rs['skipped']}"
        elif rs:
            tested = (f"tested           searched on {rs['tried']} generated inputs ({rs['in_scope']} in scope): "
                      + ("no counterexample" if not rs.get("bad") else
                         f"no counterexample on the grid (the counterexample came from the generated {rs['bad']['source']})" if rs["bad"].get("source") else "counterexample found")
                      + f"; the definition of each frame and its executable reading agree on {rs['agree']} of {rs['evals']} evaluations")
            if rs["in_scope"] == 0:
                self.flags.append("NO INPUT IN SCOPE ON THE GRID")
            for echo, kind in covers_no_call(rs):
                self.flags.append("COVERS NO CALL ON THE GRID")
                tested += (f"\ncovers no call   the clause \"{echo}\" is about {kind} calls only, and none of the {rs['in_scope']} calls "
                           f"in scope on the grid was {kind}: there the clause holds because it says nothing")
            tested += "\n" + ppath.compare_line(cmp_)
        trust = (f"tool-trusted     rule line compiled by {st.tool['generator']} from {len(self.pieces)} Clausebook pieces; echoed above for comparison"
                 if hasattr(st, "tool") else "")
        signed = len(self.pieces) - len(self.unreviewed)
        human = (f"human-asserted   {signed} of {len(self.pieces)} Clausebook pieces signed off" if signed else
                 f"NOT ASSERTED     0 of {len(self.pieces)} Clausebook pieces signed off by anyone")
        if rs.get("bad"):
            bad = rs["bad"]
            # two generated scripts: the first for a claim about every call of one operation; the general one also for
            # claims about accepted or rejected calls, two calls compared, and sequences. Either one, kernel-checked, counts.
            thm_ = next((n for n in (rd.id + ".refuted", rd.id + ".refuted2") if lclean(links, n)), None)
            kernel = thm_ is not None
            j = bad["bits"].index("0")
            on_rust = ppath.rust_at(rd.id, rs, ctx.get("rust_bits"), bad["index"], j)
            replay = None if on_rust is None else ("reproduced" if on_rust is False else "NOT reproduced (the compiled Rust satisfies the claim there)")
            self.counterexample = {"values": bad["values"], "failed": rd.claims[j].echo, "kernel_checked": kernel, "replayed_on_rust": replay}
            if kernel:
                L.append(f"kernel-checked   theorem {thm_} : ¬ {rd.name}; axioms {', '.join(lthm(links, thm_)['axioms'])}")
                self.proof = {"kind": "refutation", "theorems": [thm_], "axioms": lthm(links, thm_)["axioms"]}
            else:
                tried = [n for n in (rd.id + ".refuted", rd.id + ".refuted2") if lthm(links, n).get("exists")]
                L.append(f"tested           counterexample found by {ppath.found_by(bad)}; kernel confirmation "
                         + ("not generated (no script for this shape: a sequence of more than two calls or without step lemmas, "
                            "a two-run claim narrowed to accepted or rejected calls, or a bystander)"
                            if not tried else "attempted and FAILED"))
            if bad.get("source"):
                L.append(f"source           the input was found on the compiled Rust by {ppath.found_by(bad)}, then evaluated on the Lean model, where the rule fails too")
                self.counterexample["source"] = bad["source"]
            L.append("counterexample   " + ", ".join(f"{k.replace('the_', '').replace('_state', '')} = {v}" for k, v in bad["values"].items())
                     + ("   (the names ending in _2 are the SECOND call's)" if rs.get("two_run") else ""))
            L.append("                 at this input the rule does not hold: NOT \"" + rd.claims[j].echo + "\"")
            if replay:
                L.append(f"tested           the same input on the compiled Rust (per-piece Rust readings): {replay}")
                if on_rust:
                    self.flags.append("MODEL/GLUE MISMATCH")
                    self.fatal.append("MODEL/GLUE MISMATCH: the counterexample found on the Lean model does not fail on the compiled Rust")
            L += [y for x in (tested, trust, human) if x for y in x.split("\n")]
            self.rests_on = (["kernel-checked"] if kernel else []) + ["tested", "tool-trusted"] + (["human-asserted"] if signed else [])
            return "REFUTED" if kernel else "COUNTEREXAMPLE"
        imp = next((x for x in meta["imps"] if x[0] == rd.id + ".from_scenarios"), None)
        by_name = {v.reading.name: v for v in scen.values() if isinstance(v.reading, Reading)}
        if imp:
            self.parts = [by_name[h].sc.id for h in imp[1] if h in by_name]
        glue_ok = bool(imp) and lclean(links, imp[0])
        unproved = [h for h in (imp[1] if imp else []) if h not in by_name or by_name[h].status != "PROVED-FOR-ALL"]
        hand = next((x for x in meta["proofs"] if x[0] == self.rule.id), None)
        hand_ok = bool(hand) and lclean(links, hand[0]) and lthm(links, hand[0]).get("module") == hand[2]
        # a supplied proof of the rule's FLAT OBLIGATION (generated from the pieces), carried through the equivalence
        ob = next((x for x in meta.get("oproofs", []) if x[0] == rd.id), None)
        iffo = rd.id + ".reading_iff_obligation"
        ob_ok = bool(ob) and lclean(links, ob[0]) and lthm(links, ob[0]).get("module") == ob[2] and lclean(links, iffo) and lclean(links, ob[3])
        whole = rd.id + ".holds"
        if glue_ok and not unproved and not lclean(links, whole):
            L.append(f"not proved       the glue and every part are there, but the one theorem that puts them together ({whole} : {rd.name}) "
                     f"is not ({lwhy(links, whole)})")
            L += [y for x in (tested, trust, human) if x for y in x.split("\n")]
            self.rests_on = ["tested", "tool-trusted"] + (["human-asserted"] if signed else [])
            return "TESTED-ONLY"
        if glue_ok and not unproved:
            self.how = "from its scenarios"
            L.append(f"kernel-checked   theorem {whole} : {rd.name}  (THE RULE STATEMENT ITSELF, as one theorem; type checked by the audit); "
                     f"axioms {', '.join(lthm(links, whole)['axioms'])}")
            L.append(f"kernel-checked   theorem {imp[0]} : " + " → ".join(h.rsplit('.', 2)[-2] + ".reading" for h in imp[1])
                     + f" → {rd.name}  (generated glue, type checked by the audit); axioms {', '.join(lthm(links, imp[0])['axioms'])}")
            L.append(f"                 and each of those {len(imp[1])} scenario readings is PROVED-FOR-ALL (its own proof, carried through its equivalence)")
            L.append("scope            every state and every input the rule line names (see `applies to`)")
            L += [y for x in (tested, trust, human) if x for y in x.split("\n")]
            self.rests_on = ["kernel-checked", "tool-trusted", "tested"] + (["human-asserted"] if signed else [])
            self.proof = {"kind": "from its scenarios", "theorems": [whole, imp[0]], "axioms": lthm(links, whole)["axioms"]}
            return "PROVED-FOR-ALL"
        if ob_ok:
            self.how = "by a supplied proof of its obligation"
            L.append(f"kernel-checked   theorem {ob[3]} : {rd.name}  (THE RULE STATEMENT ITSELF, as one theorem: the supplied proof of its flat "
                     f"obligation carried through the equivalence; type checked by the audit); axioms {', '.join(lthm(links, ob[3])['axioms'])}")
            L.append(f"kernel-checked   theorem {ob[0]} : {ob[1]}  (hand-written, {rule_proof_path(self.rule.id).relative_to(ROOT)}; type checked by the audit)")
            L.append(f"kernel-checked   theorem {iffo} : {rd.name} ↔ {ob[1]}  (generated script; the audit checked its type and that its proof "
                     f"uses no proof of either side); axioms {', '.join(lthm(links, iffo)['axioms'])}")
            L.append("scope            every state and every input the rule line names (see `applies to`)")
            L += [y for x in (tested, trust, human) if x for y in x.split("\n")]
            self.rests_on = ["kernel-checked", "tool-trusted", "tested"] + (["human-asserted"] if signed else [])
            self.proof = {"kind": "a supplied proof of its flat obligation", "theorems": [ob[3], ob[0], iffo], "axioms": lthm(links, ob[3])["axioms"]}
            return "PROVED-FOR-ALL"
        if hand_ok:
            self.how = "by a hand-written proof"
            L.append(f"kernel-checked   theorem {hand[0]} : {rd.name}  (hand-written, {rule_proof_path(self.rule.id).relative_to(ROOT)}; "
                     f"type checked by the audit); axioms {', '.join(lthm(links, hand[0])['axioms'])}")
            L.append("glue             " + (f"the generated glue from the scenarios did not go through ({lwhy(links, imp[0])})" if imp else
                                           f"no glue from the scenarios was generated: {meta['noglue'].get(rd.id, 'not attempted')}"))
            L.append("scope            every state and every input the rule line names (see `applies to`)")
            L += [y for x in (tested, trust, human) if x for y in x.split("\n")]
            self.rests_on = ["kernel-checked", "tool-trusted", "tested"] + (["human-asserted"] if signed else [])
            self.proof = {"kind": "a hand-written proof", "theorems": [hand[0]], "axioms": lthm(links, hand[0])["axioms"]}
            return "PROVED-FOR-ALL"
        if ob and not ob_ok:
            t = lthm(links, ob[0])
            L.append("not proved       " + (f"proof incomplete (sorry): {rule_proof_path(self.rule.id).relative_to(ROOT)} is still the generated stub, or part of it is"
                                           if "sorryAx" in t.get("axioms", []) else
                                           f"the supplied proof of the obligation does not count: {lwhy(links, ob[0]) if not lclean(links, ob[0]) else lwhy(links, iffo) if not lclean(links, iffo) else lwhy(links, ob[3])}"))
            L.append(f"obligation       {ob[1]} (lean/Wallet/Obligations.lean), generated from the pieces")
        elif not imp and rule_proof_path(self.rule.id).exists() and not hand:
            L.append(f"not proved       {rule_proof_path(self.rule.id).relative_to(ROOT)} does not compile, or holds no theorem named {self.rule.id} "
                     "(see out/proofs.log)")
        if imp and glue_ok:
            L.append(f"not proved       the glue {imp[0]} is kernel-checked, but it rests on scenarios that are not proved: "
                     + ", ".join(h.rsplit('.', 2)[-2] for h in unproved))
        elif imp:
            L.append(f"not proved       the generated glue from the scenarios did not go through ({lwhy(links, imp[0])}), and there is no hand-written proof "
                     f"({rule_proof_path(self.rule.id).relative_to(ROOT)})")
        else:
            L.append(f"not proved       no glue from the scenarios: {meta['noglue'].get(rd.id, 'not attempted')}; no hand-written proof "
                     f"({rule_proof_path(self.rule.id).relative_to(ROOT)})")
        L += [y for x in (tested, trust, human) if x for y in x.split("\n")]
        self.rests_on = ["tested", "tool-trusted"] + (["human-asserted"] if signed else [])
        return "TESTED-ONLY"

    @property
    def headline(self) -> str:
        from .sizes import FLAG
        if self.status == "TESTED-ONLY" and FLAG in self.flags:
            return f"TESTED ONLY (compiled, evaluated on generated inputs, no counterexample; NOT PROVED; {FLAG}: see `sizes`)"
        return {"PROVED-FOR-ALL": "PROVED FOR ALL INPUTS" + (f" ({self.how})" if self.how else ""),
                "REFUTED": "REFUTED (false at a concrete input, kernel-checked)",
                "COUNTEREXAMPLE": "COUNTEREXAMPLE FOUND (not confirmed in the kernel)",
                "TESTED-ONLY": "TESTED ONLY (compiled, evaluated on generated inputs, no counterexample; NOT PROVED)"}.get(self.status, self.status + " (no statement)")


# --------------------------------------------------------------------------- report sections

def md_escape(s: str) -> str:
    return s.replace("|", chr(92) + "|")


def frames_section(st, ctx) -> list:
    voc, defs, rs = st.voc, ctx["lean_defs"], ctx["rs"]
    per = {}
    for id_, r in rs.items():
        if "skipped" in r or not r.get("evals"):
            continue
        rd = next((x for x, _ in st.compiled if x.id == id_), None)
        if rd is None:
            continue
        # per-frame share of this reading's evaluations: each in-scope point evaluates every frame once
        for j, c in enumerate(rd.claims):
            p = per.setdefault(c.frame["id"], {"evals": 0, "readings": set(), "bad": False, "false": 0, "silent": 0})
            p["evals"] += r["in_scope"]
            p["readings"].add(id_)
            p["bad"] = p["bad"] or bool(r.get("diff"))
            p["false"] += (r.get("false") or [0] * len(rd.claims))[j]
            p["silent"] += (r.get("silent") or [0] * len(rd.claims))[j]
    new = {}
    for it in load_new_sentences().get("items", []):
        sr = it.get("search") or {}
        if it.get("compiled") and sr.get("evals"):
            for j, f in enumerate(it["frames"]):
                q = new.setdefault(f, {"evals": 0, "n": 0, "bad": False, "false": 0, "silent": 0})
                q["evals"] += sr["in_scope"]
                q["n"] += 1
                q["bad"] = q["bad"] or bool(sr.get("diff"))
                q["false"] += (sr.get("false") or [0] * len(it["frames"]))[j]
                q["silent"] += (sr.get("silent") or [0] * len(it["frames"]))[j]
    ft = load_frame_tests()
    o = ["## The frame library", "",
         "Shared and project-independent: `lean/Frames/` imports nothing but Lean's core. A frame is a statement shape about ONE "
         "call of an abstract operation (a state, an input, and either an answer with the state afterwards, or no answer). Its holes are "
         "typed (a measure, a value known before the call, a condition, a class of answers, a named collection, a condition on an item, "
         "a relation between two inputs), so no frame takes an arbitrary relation between before and after. Each frame has three things:", "",
         "- **(a) a Lean definition** (`lean/Frames/Frames.lean`), with the fail-closed defaults written once, in `Frames.Op.HoldsAt`;",
         "- **(b) a fixed English paraphrase** with slots, used for the echo (`clausebook/`, `echo:`);",
         "- **(c) an independent executable reading** (`lean/Frames/Check.lean`): run the call, then case on what came back. "
         "The definition and the executable reading are evaluated side by side on generated inputs for the concrete operations "
         "(`lean/Run/ReadingSearch.lean`; NASA FRET's practice of two semantics per template). A disagreement fails the run. "
         "The comparison can only catch a wrong reading where the claim is FALSE or the call gives NO ANSWER, and the fixtures hardly ever "
         "supply either, so every frame is also compared on a toy operation that gives no answer at one input and rejects another "
         "(`lean/Run/FrameToyTests.lean`). The last column counts, per source, the evaluations at which the definition is false and those "
         "at which the call is silent; a frame for which no comparison of this run saw both is marked **comparison untested**.", "",
         "| # | Frame | Lean definition | English paraphrase (slots in braces) | Executable reading | Definition vs executable reading |",
         "|---|---|---|---|---|---|"]
    tot_e = tot_a = 0
    power = frame_power(per, new, ft)
    ctx["frame_power"] = power

    def fs(q):
        return f" ({q['false']} false, {q['silent']} silent)"

    def hand(t):
        n = len(t)
        return ((("agree" if all(x["agree"] == x["points"] for x in t) else "**DISAGREE**")
                 + f" on {sum(x['agree'] for x in t)} of {sum(x['points'] for x in t)} evaluations in {n} hand-written "
                 + ("instance" if n == 1 else "instances") + " (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`)"
                 + fs({"false": sum(x["false"] for x in t), "silent": sum(x["silent"] or 0 for x in t)})) if t else "")

    def untested(id_):
        return "" if id_ not in power else f"; **comparison untested for `{id_}`**: no comparison of this run saw {power[id_]}"
    for p in voc.frames():
        d = defs.get(p["lean"].split()[0] + ".at", {}).get("text", "")
        q = per.get(p["id"])
        bits = []
        if q:
            bits.append(("**DISAGREE**" if q["bad"] else "agree") + f" on {q['evals']} evaluations in {len(q['readings'])} readings of the fixtures" + fs(q))
        if p["id"] in new:
            n = new[p["id"]]
            bits.append(("**DISAGREE**" if n["bad"] else "agree") + f" on {n['evals']} evaluations in {n['n']} new sentences (`heldout/`)" + fs(n))
        if ft.get(p["id"]):
            bits.append(hand(ft[p["id"]]))
        cmp_ = ("; ".join(bits) or "not exercised by any sentence of this run") + untested(p["id"])
        o.append(f"| {p['number']} | `{p['id']}` | `{md_escape(d)}` | {md_escape(p['echo'])} | `{p['check'].split()[0]}` | {cmp_} |")
    for f in voc.raw.get("frames_without_surface", []):
        d = defs.get(f["lean"] + ".at", {}).get("text", "")
        t = ft.get(f["id"])
        cmp_ = ("; ".join(f"{x['what']}: {'agree' if x['agree'] == x['points'] else '**DISAGREE**'} on {x['agree']} of {x['points']} "
                          f"evaluations ({x['false']} of them false" + (f", {x['silent']} with a silent call" if x["silent"] is not None else "") + ")"
                          for x in t) if t else "hand-written test not run") + untested(f["id"])
        o.append(f"| {f['number']} | `{f['id']}` (no surface form yet) | `{md_escape(d)}` | {md_escape(f['echo'])} | `{f['check']}` | {cmp_} |")
    te = sum(r.get("evals", 0) for r in rs.values())
    ta = sum(r.get("agree", 0) for r in rs.values())
    ne = sum((it.get("search") or {}).get("evals", 0) for it in load_new_sentences().get("items", []))
    na = sum((it.get("search") or {}).get("agree", 0) for it in load_new_sentences().get("items", []))
    tf = sum(sum(r.get("false") or []) for r in rs.values())
    tsil = sum(sum(r.get("silent") or []) for r in rs.values())
    nf = sum(sum((it.get("search") or {}).get("false") or []) for it in load_new_sentences().get("items", []))
    hp = sum(x["points"] for t in ft.values() for x in t)
    ha = sum(x["agree"] for t in ft.values() for x in t)
    hf = sum(x["false"] for t in ft.values() for x in t)
    hs = sum(x["silent"] or 0 for t in ft.values() for x in t)
    o += ["", f"Over all compiled readings of the fixtures: the definition and the executable reading of the frames agree on **{ta} of {te}** "
              f"(point, frame) evaluations; the definition is false at {tf} of them and the call is silent at {tsil}"
              + (f". Over the new sentences of `heldout/`: **{na} of {ne}** ({nf} false)" if ne else "")
              + f". On the hand-written instances (the wallet and the ledger for the frames with no surface form, and the toy operation for every "
              f"frame): **{ha} of {hp}** ({hf} false, {hs} with a silent call). "
              + ("Every frame was compared at a false claim and at a silent call at least once. " if not power else
                 f"**Comparison untested** for {len(power)} frames: " + "; ".join(f"`{k}` (no {v})" for k, v in power.items()) + ". ")
              + "Agreement on generated inputs is a test, not a proof that the two readings are the same; both readings were written by one author.", "",
          "**The defaults** (fail-closed; each reading lists the ones applied to it):", ""]
    o += [f"- **{k}** {v}" for k, v in voc.raw["defaults"].items()]
    o += ["", "**Weakenings** (never applied silently; a modifier has to ask):", ""]
    o += [f"- **{c['calls']}** (`{c['id']}`): {c['weakening']}" for c in voc.coverage.values() if "weakening" in c]
    o += ["", "**Quantifier scope, the one rule.** Every outline `<parameter>`, then the state, then the input are universally quantified "
              "at the front, in that order, and Givens restrict them. Collection words (`every`, `the first`, `no`) bind inside the one "
              "clause they are written in. Negation applies to the one atomic condition it is written on. Nothing is ever existentially "
              "quantified over inputs. The tool never chooses a scope.", ""]
    return o


def frame_power(per: dict, new: dict, ft: dict) -> dict:
    """frame id -> what no comparison of this run saw ("a false claim", "a call that gives no answer", or both).
    A comparison of a definition with its checker has no power where every claim is true and every call answers."""
    out = {}
    ids = list(dict.fromkeys(list(per) + list(new) + list(ft)))
    for i in ids:
        f = per.get(i, {}).get("false", 0) + new.get(i, {}).get("false", 0) + sum(x["false"] for x in ft.get(i, []))
        s_ = per.get(i, {}).get("silent", 0) + new.get(i, {}).get("silent", 0) + sum(x["silent"] or 0 for x in ft.get(i, []))
        miss = (["a false claim"] if not f else []) + (["a call that gives no answer"] if not s_ else [])
        if miss:
            out[i] = " or ".join(miss)
    return out


def vocabulary_section(st, ctx, verdicts, rule_verdicts) -> list:
    voc, defs = st.voc, ctx["lean_defs"]
    used = {}
    for v in list(verdicts) + list(rule_verdicts):
        for i in (getattr(v, "pieces", None) or []):
            used[i] = used.get(i, 0) + 1
    so = load_piece_signoff(voc)
    kinds = voc.kinds()
    o = ["## Clausebook (the link from English to Lean)", "",
         f"`clausebook/` ({len(voc.books)} books, in the order loaded: " + ", ".join(f"`{b.rel}` ({sum(1 for h in voc.home.values() if h is b)} entries)" for b in voc.books)
         + f"): **{kinds['domain']} domain words** ({len(voc.ops)} operations, {kinds['domain'] - len(voc.ops)} measures, conditions, "
         f"collections and answer words), **{kinds['modifier']} modifiers**, **{kinds['frame']} frames**, and {len(voc.idioms)} idioms "
         "(a surface form that is not the regular form of one piece, with the composition it means; an idiom adds English, no Lean). "
         "A sentence is the composition of pieces its words spell out; this table and the Lean files it names are what a reviewer has to read "
         "to trust the step from English to Lean. Sign-off is per piece and is void as soon as the piece's entry or a Lean definition it names changes.", "",
         "The column **Rust reading** says whether the piece's one Rust reading (`wallet-bdd/src/pieces.rs`) was set against the Lean "
         "definition in this run: every compiled reading that uses the piece is evaluated at every point of its grid of generated inputs on "
         "the Lean model (Lean pieces) and on the compiled Rust (Rust pieces), and the results are compared.", "",
         "| Piece | Kind | Type | Surface forms | Lean | Definition | English paraphrase | Used by | Rust reading | Sign-off |", "|---|---|---|---|---|---|---|---|---|---|"]
    pc = ctx.get("piece_cmp") or {}
    ran = ctx.get("rust_bits") is not None

    def rustcol(i):
        if not ran:
            return "not compared in this run"
        q = pc.get(i)
        if not q:
            return "**not compared**: no compiled reading of this run uses it"
        return ("**DISAGREES** " if q["bad"] else "agrees ") + f"in {q['readings']} readings, {q['points']} generated inputs"

    def signoff(i):
        if i in ctx["piece_reviewed"]:
            return f"signed off by {so[i]['reviewer']} {so[i]['date']}"
        return "UNREVIEWED (changed since sign-off)" if i in so else "UNREVIEWED"

    def dtext(names):
        return "<br>".join("`" + md_escape(defs[d]["text"]) + "`" for d in names if d in defs) or "-"
    n_un = 0
    for o_ in voc.ops.values():
        roles = ", ".join(f"{r}: {t}" for r, t in o_["state"]) + (" / " + ", ".join(f"{r}: {t}" for r, t in o_["input"]) if o_["input"] else "")
        o.append(f"| {o_['id']} | domain | operation ({roles}; answers `{o_['answer']}`) | {md_escape('; '.join(o_['when']))}; in a Rule: {', '.join(o_['nouns'])} "
                 f"| `{o_['lean']}` around the Aeneas model `{o_['model']}` | {dtext([o_['lean']])} | {md_escape(o_['echo'])} | {used.get(o_['id'], 0)} | {rustcol(o_['id'])} | {signoff(o_['id'])} |")
        n_un += o_["id"] not in ctx["piece_reviewed"]
    for p in voc.pieces.values():
        forms = "; ".join(p.get("forms", []) + p.get("then_forms", []) + [f"(Rule) {x}" for x in p.get("vp_forms", [])]
                          + [f"(negated) {x}" for x in p.get("not_forms", [])]
                          + [f"(plural) {x}" for x in p.get("per_actor", {}).get("forms", [])]) or "(no surface of its own)"
        o.append(f"| {p['id']} | {p['kind']} | {md_escape(p['cat'])} | {md_escape(forms)} | `{md_escape(p['lean'])}` | {dtext(p.get('defs', []))} "
                 f"| {md_escape(p['echo'])} | {used.get(p['id'], 0)} | {rustcol(p['id'])} | {signoff(p['id'])} |")
        n_un += p["id"] not in ctx["piece_reviewed"]
    for i in voc.idioms.values():
        o.append(f"| {i['id']} | idiom | {md_escape(i['cat'])} | {md_escape(i['form'])} | means `{md_escape(i['means'])}` | - | (the reading of that composition) "
                 f"| {used.get(i['id'], 0)} | n/a (an idiom adds no Lean and no Rust: it is its composition) | {signoff(i['id'])} |")
        n_un += i["id"] not in ctx["piece_reviewed"]
    for g_ in voc.grammar.values():       # the words that put a Rule line together and belong to no one piece
        o.append(f"| {g_['id']} | grammar | Rule line | {md_escape('; '.join(g_.get('forms', [])))} | - | - | {md_escape(g_['echo'])} | {used.get(g_['id'], 0)} "
                 f"| n/a (words of the Rule line; no Lean and no Rust of their own) | {signoff(g_['id'])} |")
        n_un += g_["id"] not in ctx["piece_reviewed"]
    for d_, text_ in voc.raw["defaults"].items():      # the reading rules, printed with every reading they were applied to
        o.append(f"| {d_} | default | reading rule | (printed with the reading) | - | - | {md_escape(text_)} | {used.get(d_, 0)} "
                 f"| n/a (a reading rule; what it says of the calls covered is compared with Lean through the coverage entries) | {signoff(d_)} |")
        n_un += d_ not in ctx["piece_reviewed"]
    for c in voc.coverage.values():       # what is printed about which calls a claim is about, one per constructor of Frames.Calls
        o.append(f"| {c['id']} | coverage | calls | (printed: {md_escape(c['covers'])}) | `{md_escape(c['lean'])}` | {dtext(c.get('defs', []))} "
                 f"| {md_escape(c['echo'])} | {used.get(c['id'], 0)} | n/a (printed text; compared with the Calls value Lean reports, `out/narrowing.json`) "
                 f"| {signoff(c['id'])} |")
        n_un += c["id"] not in ctx["piece_reviewed"]
    if voc.separations:                   # signed exemptions from lint check 4 of `clausal book check`
        from . import book
        for s_ in voc.separations.values():
            st_ = book.separation_state(voc, s_)
            o.append(f"| {s_['id']} | separation | {' / '.join(s_['between'])} | {md_escape('; '.join(s_['inputs'].values()))} | - | - "
                     f"| {md_escape('each sentence is read as its own entry and not the other' if st_['ok'] else 'DOES NOT SEPARATE: ' + '; '.join(st_['why']))} "
                     f"| 0 | n/a (an exemption of the registration lint; no Lean and no Rust of its own) | {signoff(s_['id'])} |")
            n_un += s_["id"] not in ctx["piece_reviewed"]
    total = len(all_ids(voc))
    npieces = len(voc.ops) + len(voc.pieces)
    ncmp = sum(1 for i in list(voc.ops) + list(voc.pieces) if i in pc)
    o += ["", f"{n_un} of {total} entries are unreviewed. Record a review with `python3 -m clausal review <id|all> --reviewer <name>` "
              "(piece ids and the ids of the old glossary are both accepted).", "",
          f"**What a person has to sign:** {total} entries ({npieces} pieces: {len(voc.ops)} operations, {kinds['domain'] - len(voc.ops)} other domain "
          f"words, {kinds['modifier']} modifiers, {kinds['frame']} frames; {len(voc.idioms)} idioms; {len(voc.coverage)} coverage entries, "
          f"the lines printed about which calls a claim covers; {len(voc.grammar)} grammar entries, the words that put a Rule line together; "
          f"and {len(voc.raw['defaults'])} defaults, the reading rules). A new sentence built from them adds none. "
          + (f"**Rust readings compared in this run:** {ncmp} of {npieces} pieces, through the compiled readings that use them; "
             f"not compared: {', '.join('`' + i + '`' for i in list(voc.ops) + list(voc.pieces) if i not in pc) or 'none'}."
             if ran else "The Rust readings were not compared in this run."), ""]
    return o


def regression_section(st, ctx, verdicts) -> list:
    links, meta = ctx["links"], ctx["links_meta"]
    o = ["## Regression: every old statement against its new reading (plan node V3)", "",
         "Each scenario has two Lean statements: the **reading** compiled from the composable Clausebook (`lean/Wallet/Readings.lean`) and the "
         "**flat statement** of the old whole-phrase glossary (`lean/Wallet/Statements.lean`, unchanged; every hand-written proof is about it). "
         "A generated theorem `<id>.reading_iff : <id>.reading ↔ <id>.stmt` is checked by Lean's kernel, and the audit checks that its type is "
         "exactly that (`lean/Run/Links.lean`, `lean/Bdd/AuditLinks.lean`). So a verdict is carried from the old statement to the new one by an "
         "equivalence, not by getting the same answer twice; a reading whose equivalence is missing gets the verdict UNLINKED.", "",
         "| Scenario | Old glossary entries | New pieces | Idioms needed | NEW ↔ OLD | Axioms | Reading non-vacuous |", "|---|---|---|---|---|---|---|"]
    n_ok = n = 0
    for v in verdicts:
        rd = v.reading
        if not isinstance(rd, Reading) or isinstance(v.r, Problem):
            continue
        n += 1
        iff = rd.id + ".reading_iff"
        ok = lclean(links, iff)
        n_ok += ok
        sat = rd.id + ".reading_sat"
        idi = [i for i in rd.used if i in st.voc.idioms]
        o.append(f"| `{rd.id.split('.', 1)[1]}` | {len(v.used)} | {len([i for i in rd.used if i not in st.voc.idioms])} | {', '.join(idi) or '-'} | "
                 + ("**equivalent** (kernel-checked)" if ok else f"**NOT SHOWN**: {lwhy(links, iff)}")
                 + f" | {', '.join(lthm(links, iff).get('axioms', [])) or '-'} | "
                 + ("kernel-checked" if lclean(links, sat) else "n/a (the Givens contradict each other)" if v.status == "VACUOUS" else "NOT SHOWN") + " |")
    o += ["", f"**{n_ok} of {n}** readings are proved equivalent to their old statement. "
              "**None is a deliberate strengthening**: the old statements were already fail-closed (each said the call returns, for every input "
              "satisfying the Givens), so the defaults change nothing at scenario level. The defaults do bite at the level of the `Rule:` lines, which "
              "had no statement before: each rule statement covers every input, and is proved FROM its scenarios (see each rule's block).", ""]
    for sid, why in meta.get("skipped", []):
        o.append(f"- no equivalence generated for `{sid}`: {why}")
    return o


def narrowing_section(voc) -> list:
    """Plan nodes Q1 and Q2, from out/narrowing.json (written by `clausal narrowing` after lean/Run/Narrowing.lean ran)."""
    p = ROOT / "out" / "narrowing.json"
    o = ["## Narrowed claims: vacuity and printed coverage (plan nodes Q1, Q2)", ""]
    if not p.exists():
        return o + ["`lean/Run/Narrowing.lean` was not run in this run, so nothing is reported here.", ""]
    r = json.loads(p.read_text())
    c = r["counts"]
    o += ["A claim narrowed to accepted calls (the modifier `successful`: \"an accepted <operation>\" in a Rule line, \"if it is accepted,\" before a Then) or to rejected calls covers only the calls that give "
          "an answer of that kind. **A narrowed Rule clause whose claim follows from the narrowing alone is refused** (`SAYS-NOTHING`): "
          "it would hold of every possible operation, so no code could break it. The compiler decides from what narrowing settles "
          "about each operation's answers (`narrowing:` in the operation's entry, `clausebook/local/`) and names a theorem of `lean/Frames/Narrowing.lean`; "
          "what follows is what Lean said about that in this run (`lean/Run/Narrowing.lean`).", "",
          f"- **Declared facts:** {c['facts_declared']} lines of `narrowing:` kernel-checked; the {c['facts_not_declared']} lines that could have "
          "been written and were not were each attempted with the same fixed tactic and are not provable by it.",
          f"- **Refused controls** (`controls/narrowing.feature`): {c['controls_refused']} sentences refused; compiled without the refusal, their "
          f"{c['refused_claims']} narrowed claims are kernel-checked to hold for every `run`, each through the theorem its refusal names.",
          f"- **Not refused:** {c['narrowed_not_refused']} narrowed claims ({c['narrowed_not_refused_fixture_rules']} in the fixture Rules, the rest in "
          f"the {c['controls_compiled']} controls that must compile). The fixed tactic `vacuous_by_narrowing` fails on each: none is shown to hold of "
          "every operation. This is proof search, not a proof that each says something.",
          f"- **Printed coverage:** Lean reported the `Frames.Calls` value of {c['calls_reported']} of {c['claims']} claims in {c['readings']} compiled "
          f"readings ({c['fixture_scenario_readings']} scenarios and {c['fixture_rule_readings']} Rule lines of the fixtures, {c['control_readings']} control "
          f"lines). The coverage lines printed for a reading differ from the lines the "
          f"book gives for those values in **{c['coverage_mismatches']}** readings. The lines compared are the `covers` slot, the answer "
          f"requirement, the note of a sequence ({c['sequence_claims']} claims are about a sequence according to Lean: their operation mentions "
          "`Frames.Op.andThen`), the note of two compared calls, and the stated weakenings.",
          f"- **Narrowed twice:** {c['controls_narrowed_twice']} control sentences narrow or scope one clause with more than one word (two of "
          "accepted / rejected on the subject or `internal` before one of them, a narrowed subject and `if it is ...` on its claim, or two `if it is ...`). Each "
          "is refused (`UNSUPPORTED`, code `NARROWED-TWICE`): a word is never dropped and never overrides another.",
          "- **Must-fail attempts count only if their statement was read.** A theorem whose script fails is reported `notproved`; one whose "
          "statement does not elaborate is reported `badstatement` and fails the run. One statement broken on purpose checks the report "
          f"itself on every run. Statements that did not elaborate, other than that one: **{len(c['bad_statements'])}**.", ""]
    if r["problems"]:
        o += ["**CHECK FAILED:**", ""] + [f"- {md_escape(x)}" for x in r["problems"]] + [""]
    o += ["Coverage lines, by `Frames.Calls` value (entries `coverage:` of the Clausebook, signed like any other entry):", ""]
    o += [f"- **{k}** (`{e['id']}`): {md_escape(e['covers'])}. Of a sequence: {md_escape(e['sequence'])}" for k, e in voc.covers.items()] + [""]
    return o


def new_sentences_section() -> list:
    data = load_new_sentences()
    if not data:
        return []
    items = data["items"]
    o = ["## New sentences (not in the fixtures)", "",
         "Informational; it changes no verdict and no exit status. The feature files of `heldout/` hold rules that are in no fixture, written "
         "with the words of the Clausebook. They were written by the Clausebook's builder, and the Clausebook files were last edited after "
         "them, so this run cannot confirm that no piece was added or changed for them. Each is compiled from the Clausebook alone "
         "(`python3 -m clausal compile heldout/*.feature`). A new sentence has no old whole-phrase binding, so it has no flat statement, "
         "no hand-written proof and no cucumber step: what it gets here is its compiled reading (type-checked by Lean), its echo, and a search "
         "on generated inputs through the frames' two readings. NO-COUNTEREXAMPLE is not a proof.", "",
         "| Sentence | Compiled from existing pieces | Pieces | Idioms | Searched on generated inputs | Result |", "|---|---|---|---|---|---|"]
    for it in items:
        first = it["text"].splitlines()[0]
        if not it["compiled"]:
            o.append(f"| {md_escape(first)} (`{it['source']}`) | **NO: {it['status']}** | - | - | - | {md_escape(it['message'])} |")
            continue
        sr = it.get("search") or {}
        res = it["status"] + (f": {json.dumps(sr['bad']['values'], ensure_ascii=False)}" if sr.get("bad") else "")
        for echo, kind in covers_no_call(sr):
            res += f"; COVERS NO CALL ON THE GRID: \"{echo}\" is about {kind} calls only and no call in scope was {kind}"
        o.append(f"| {md_escape(first)} (`{it['source']}`) | yes | {len(it['pieces'])} | {'none' if it['regular'] else 'yes'} | "
                 + (f"{sr.get('tried', 0)} inputs, {sr.get('in_scope', 0)} in scope; definition and executable reading agree on "
                    f"{sr.get('agree', 0)} of {sr.get('evals', 0)}" if sr and 'skipped' not in sr else "not searched")
                 + f" | **{md_escape(res)}**" + (f" (expected {it['expect']})" if it.get("expect") else "") + " |")
    n = sum(it["compiled"] for it in items)
    o += ["", f"{n} of {len(items)} sentences compiled from the pieces of the Clausebook as it now stands.", ""]
    for it in items:
        if not it["compiled"]:
            continue
        o += [f"#### {it['text'].splitlines()[0]}", "", f"`{it['source']}`  pieces `{', '.join(it['pieces'])}`", "", "```text"]
        import textwrap
        for slot, text in it["echo"]:
            w = textwrap.wrap(text, 108, break_on_hyphens=False) or [""]
            o.append(f"{slot:<12}{w[0]}")
            o += [f"{'':<12}{x}" for x in w[1:]]
        o += ["```", "", "<details><summary>Lean statement</summary>", "", "```lean", it["lean"], "```", "", "</details>", ""]
    return o
