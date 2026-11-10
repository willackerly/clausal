"""slicegen vreport: what the report says about the COMPOSABLE VOCABULARY.

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
from .vocab import Reading, base_cat

STD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
INTERNAL = {"Frames.Op.HoldsAt", "Frames.Op.Holds", "Frames.Op.HoldsAt2"}     # not frames: a reading may not mention them
SLOTS = ("applies to", "assuming", "then", "defaults", "not default")


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
                                                         "proofs": [], "consts": [], "holds": []}


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
                out.setdefault(q[1], []).append({"what": q[2], "points": int(q[3]), "agree": int(q[4]), "false": int(q[5])})
    return out


def load_new_sentences() -> dict:
    p = OUT / "new_sentences.json"
    return json.loads(p.read_text()) if p.exists() else {}


def lthm(links, name) -> dict:
    return (links or {}).get("theorems", {}).get(name) or {}


def lclean(links, name) -> bool:
    t = lthm(links, name)
    return bool(t and t["exists"] and t.get("is_theorem") and t.get("type_ok") and set(t["axioms"]) <= STD_AXIOMS)


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
    return f"non-standard axioms {t['axioms']}"


def lean_defs(voc) -> dict:
    """Lean name -> {text, file, line, end} for every declaration of the vocabulary's Lean files."""
    out = {}
    for ns, files in voc.raw["lean_files"].items():
        for rel in ([files] if isinstance(files, str) else files):
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
    a = voc.line_of(id_)
    if not a:
        return id_
    b = a
    while b < len(voc.lines) and not re.match(r"\s*-\s*\{?\s*id:", voc.lines[b]) and not re.match(r"[a-z_]+:\s*$", voc.lines[b]) \
            and not voc.lines[b].lstrip().startswith("# ====="):
        b += 1
    return "\n".join(l for l in voc.lines[a - 1:b] if l.strip() and not l.strip().startswith("#"))


def all_ids(voc) -> list:
    return list(voc.ops) + list(voc.pieces) + list(voc.idioms)


def entry_of(voc, id_: str) -> dict:
    return voc.ops.get(id_) or voc.pieces.get(id_) or voc.idioms[id_]


def def_names(voc, id_: str) -> list:
    e = entry_of(voc, id_)
    if id_ in voc.ops:
        return [e["lean"]]
    return list(e.get("defs", []))


def piece_digest(voc, defs: dict, id_: str) -> str:
    """What a sign-off of a piece is a sign-off OF: its vocabulary entry and the text of every Lean definition it names."""
    parts = [entry_text(voc, id_)] + [defs.get(d, {}).get("text", f"MISSING {d}") for d in def_names(voc, id_)]
    return sha("\n".join(parts))


def load_piece_signoff() -> dict:
    p = ROOT / "vocabulary.signoff.json"
    return json.loads(p.read_text()) if p.exists() else {}


def reviewed_pieces(voc, defs: dict) -> set:
    so = load_piece_signoff()
    return {i for i in all_ids(voc) if so.get(i, {}).get("digest") == piece_digest(voc, defs, i)}


def review(voc, which: str, reviewer: str) -> int:
    defs = lean_defs(voc)
    so = load_piece_signoff()
    ids = all_ids(voc) if which == "all" else [which]
    for i in ids:
        so[i] = {"reviewer": reviewer, "date": datetime.date.today().isoformat(), "digest": piece_digest(voc, defs, i)}
        e = entry_of(voc, i)
        print(f"signed off piece {i} ({e.get('kind', 'domain')}): {e.get('form') or (e.get('when') or e.get('forms') or e.get('then_forms') or [''])[:1]}")
    (ROOT / "vocabulary.signoff.json").write_text(json.dumps(so, indent=2) + "\n")
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


def reading_attrs(st, rd, ctx) -> dict:
    """What the graph stores about a compiled reading (so the per-Rule blocks can be rendered from the graph alone)."""
    voc = st.voc
    if isinstance(rd, Problem):
        return {"compiled": False, "status": rd.status, "message": rd.message, "hint": rd.hint}
    return {"compiled": True, "name": rd.name, "lean": rd.lean_def(), "echo": [list(x) for x in rd.echo], "defaults": rd.defaults,
            "regular": rd.regular,
            "pieces": [{"id": i, "kind": kind_of(voc, i), "signed": i in ctx["piece_reviewed"],
                        "by": load_piece_signoff().get(i, {}).get("reviewer") if i in ctx["piece_reviewed"] else None} for i in rd.used]}


# --------------------------------------------------------------------------- Rule verdicts

class RuleVerdict:
    """The verdict of one `Rule:` statement.

    PROVED-FOR-ALL   the generated glue `<rule>.from_scenarios` is kernel-checked AND every scenario it rests on is
                     PROVED-FOR-ALL; or a hand-written proof of exactly the rule statement is kernel-checked
    REFUTED          the reading search found an input at which the statement is false, and `¬ <rule>.reading` is
                     kernel-checked at that input            (COUNTEREXAMPLE: found, not confirmed in the kernel)
    NOT-PROVED       compiled and searched on the grid, no counterexample, no proof
    UNBOUND / ILL-TYPED / AMBIGUOUS   the rule line is not a composition of vocabulary pieces: no statement"""

    def __init__(self, rule, rd, st, ctx, scen: dict):
        self.rule, self.rd = rule, rd
        self.lines, self.flags, self.fatal = [], [], []
        self.how, self.counterexample, self.parts, self.rests_on = "", None, [], []
        self.pieces = [] if isinstance(rd, Problem) else rd.used
        self.unreviewed = [i for i in self.pieces if i not in ctx["piece_reviewed"]]
        tags = rule.tags
        self.expected = ("REFUTED" if "@expect-refuted" in tags else "UNBOUND" if "@expect-unbound" in tags
                         else "NOT-PROVED" if "@expect-unproved" in tags else "PROVED-FOR-ALL")
        self.status = self.compute(st, ctx, scen)
        if ctx["strict"] and self.status.startswith("PROVED") and self.unreviewed:
            self.fatal.append(f"--strict: the rule statement rests on {len(self.unreviewed)} vocabulary pieces with no valid sign-off")
        self.as_expected = self.status == self.expected and not self.fatal

    def compute(self, st, ctx, scen) -> str:
        rd, L = self.rd, self.lines
        links, meta, rs_all = ctx["links"], ctx["links_meta"], ctx["rs"]
        if isinstance(rd, Problem):
            L.append(rd.message)
            L += ["  " + h for h in rd.hint.splitlines()]
            L.append("the rule line is not a composition of vocabulary pieces, so no statement was generated for it")
            return rd.status
        rs = rs_all.get(rd.id, {})
        cs = set((links or {}).get("consts", {}).get(rd.name, {}).get("consts", []))
        if cs & INTERNAL:
            self.flags.append("GENERATOR-CHECK-FAILED")
            self.fatal.append("GENERATOR-CHECK-FAILED: the reading mentions " + ", ".join(sorted(cs & INTERNAL)) + ", which is not a frame")
        if rs.get("diff"):
            self.flags.append("FRAME READINGS DISAGREE")
            self.fatal.append("FRAME READINGS DISAGREE: the definition and the executable reading of a frame differ at " + json.dumps(rs["diff"]["values"]))
        tested = ""
        if "skipped" in rs:
            tested = f"not searched: {rs['skipped']}"
        elif rs:
            tested = (f"tested           searched on {rs['tried']} generated inputs ({rs['in_scope']} in scope): "
                      + ("no counterexample" if not rs.get("bad") else "counterexample found")
                      + f"; the definition of each frame and its executable reading agree on {rs['agree']} of {rs['evals']} evaluations")
            if rs["in_scope"] == 0:
                self.flags.append("NO INPUT IN SCOPE ON THE GRID")
        trust = (f"tool-trusted     rule line compiled by {st.tool['generator']} from {len(self.pieces)} vocabulary pieces; echoed above for comparison"
                 if hasattr(st, "tool") else "")
        signed = len(self.pieces) - len(self.unreviewed)
        human = (f"human-asserted   {signed} of {len(self.pieces)} vocabulary pieces signed off" if signed else
                 f"NOT ASSERTED     0 of {len(self.pieces)} vocabulary pieces signed off by anyone")
        if rs.get("bad"):
            bad = rs["bad"]
            kernel = lclean(links, rd.id + ".refuted")
            j = bad["bits"].index("0")
            self.counterexample = {"values": bad["values"], "failed": rd.claims[j].echo, "kernel_checked": kernel}
            if kernel:
                L.append(f"kernel-checked   theorem {rd.id}.refuted : ¬ {rd.name}; axioms {', '.join(lthm(links, rd.id + '.refuted')['axioms'])}")
            else:
                L.append("tested           counterexample found by the reading search; kernel confirmation "
                         + ("not generated (the failing clause is about accepted or rejected calls only, or about a sequence)"
                            if not lthm(links, rd.id + ".refuted").get("exists") else "attempted and FAILED"))
            L.append("counterexample   " + ", ".join(f"{k.replace('the_', '').replace('_state', '')} = {v}" for k, v in bad["values"].items()))
            L.append("                 at this input the rule does not hold: NOT \"" + rd.claims[j].echo + "\"")
            L += [x for x in (tested, trust, human) if x]
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
        whole = rd.id + ".holds"
        if glue_ok and not unproved and not lclean(links, whole):
            L.append(f"not proved       the glue and every part are there, but the one theorem that puts them together ({whole} : {rd.name}) "
                     f"is not ({lwhy(links, whole)})")
            L += [x for x in (tested, trust, human) if x]
            self.rests_on = ["tested", "tool-trusted"] + (["human-asserted"] if signed else [])
            return "NOT-PROVED"
        if glue_ok and not unproved:
            self.how = "from its scenarios"
            L.append(f"kernel-checked   theorem {whole} : {rd.name}  (THE RULE STATEMENT ITSELF, as one theorem; type checked by the audit); "
                     f"axioms {', '.join(lthm(links, whole)['axioms'])}")
            L.append(f"kernel-checked   theorem {imp[0]} : " + " → ".join(h.rsplit('.', 2)[-2] + ".reading" for h in imp[1])
                     + f" → {rd.name}  (generated glue, type checked by the audit); axioms {', '.join(lthm(links, imp[0])['axioms'])}")
            L.append(f"                 and each of those {len(imp[1])} scenario readings is PROVED-FOR-ALL (its own proof, carried through its equivalence)")
            L.append("scope            every state and every input the rule line names (see `applies to`)")
            L += [x for x in (tested, trust, human) if x]
            self.rests_on = ["kernel-checked", "tool-trusted", "tested"] + (["human-asserted"] if signed else [])
            return "PROVED-FOR-ALL"
        if hand_ok:
            self.how = "by a hand-written proof"
            L.append(f"kernel-checked   theorem {hand[0]} : {rd.name}  (hand-written, {rule_proof_path(self.rule.id).relative_to(ROOT)}; "
                     f"type checked by the audit); axioms {', '.join(lthm(links, hand[0])['axioms'])}")
            L.append("glue             " + (f"the generated glue from the scenarios did not go through ({lwhy(links, imp[0])})" if imp else
                                           f"no glue from the scenarios was generated: {meta['noglue'].get(rd.id, 'not attempted')}"))
            L.append("scope            every state and every input the rule line names (see `applies to`)")
            L += [x for x in (tested, trust, human) if x]
            self.rests_on = ["kernel-checked", "tool-trusted", "tested"] + (["human-asserted"] if signed else [])
            return "PROVED-FOR-ALL"
        if imp and glue_ok:
            L.append(f"not proved       the glue {imp[0]} is kernel-checked, but it rests on scenarios that are not proved: "
                     + ", ".join(h.rsplit('.', 2)[-2] for h in unproved))
        elif imp:
            L.append(f"not proved       the generated glue from the scenarios did not go through ({lwhy(links, imp[0])}), and there is no hand-written proof "
                     f"({rule_proof_path(self.rule.id).relative_to(ROOT)})")
        else:
            L.append(f"not proved       no glue from the scenarios: {meta['noglue'].get(rd.id, 'not attempted')}; no hand-written proof "
                     f"({rule_proof_path(self.rule.id).relative_to(ROOT)})")
        L += [x for x in (tested, trust, human) if x]
        self.rests_on = ["tested", "tool-trusted"] + (["human-asserted"] if signed else [])
        return "NOT-PROVED"

    @property
    def headline(self) -> str:
        return {"PROVED-FOR-ALL": "PROVED FOR ALL INPUTS" + (f" ({self.how})" if self.how else ""),
                "REFUTED": "REFUTED (false at a concrete input, kernel-checked)",
                "COUNTEREXAMPLE": "COUNTEREXAMPLE FOUND (not confirmed in the kernel)",
                "NOT-PROVED": "COMPILED AND SEARCHED, NOT PROVED"}.get(self.status, self.status + " (no statement)")


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
        for c in rd.claims:
            p = per.setdefault(c.frame["id"], {"evals": 0, "readings": set(), "bad": False})
            p["evals"] += r["in_scope"]
            p["readings"].add(id_)
            p["bad"] = p["bad"] or bool(r.get("diff"))
    new = {}
    for it in load_new_sentences().get("items", []):
        sr = it.get("search") or {}
        if it.get("compiled") and sr.get("evals"):
            for f in it["frames"]:
                q = new.setdefault(f, {"evals": 0, "n": 0, "bad": False})
                q["evals"] += sr["in_scope"]
                q["n"] += 1
                q["bad"] = q["bad"] or bool(sr.get("diff"))
    ft = load_frame_tests()
    o = ["## The frame library", "",
         "Shared and project-independent: `lean/Frames/` imports nothing but Lean's core. A frame is a statement shape about ONE "
         "call of an abstract operation (a state, an input, and either an answer with the state afterwards, or no answer). Its holes are "
         "typed (a measure, a value known before the call, a condition, a class of answers, a named collection, a condition on an item, "
         "a relation between two inputs), so no frame takes an arbitrary relation between before and after. Each frame has three things:", "",
         "- **(a) a Lean definition** (`lean/Frames/Frames.lean`), with the fail-closed defaults written once, in `Frames.Op.HoldsAt`;",
         "- **(b) a fixed English paraphrase** with slots, used for the echo (`vocabulary.yaml`, `echo:`);",
         "- **(c) an independent executable reading** (`lean/Frames/Check.lean`): run the call, then case on what came back. "
         "The definition and the executable reading are evaluated side by side on generated inputs for the concrete operations "
         "(`lean/Run/ReadingSearch.lean`; NASA FRET's practice of two semantics per template). A disagreement fails the run.", "",
         "| # | Frame | Lean definition | English paraphrase (slots in braces) | Executable reading | Definition vs executable reading |",
         "|---|---|---|---|---|---|"]
    tot_e = tot_a = 0
    for p in voc.frames():
        d = defs.get(p["lean"].split()[0] + ".at", {}).get("text", "")
        q = per.get(p["id"])
        bits = []
        if q:
            bits.append(("**DISAGREE**" if q["bad"] else "agree") + f" on {q['evals']} evaluations in {len(q['readings'])} readings of the fixtures")
        if p["id"] in new:
            n = new[p["id"]]
            bits.append(("**DISAGREE**" if n["bad"] else "agree") + f" on {n['evals']} evaluations in {n['n']} new sentences (`heldout/`)")
        cmp_ = "; ".join(bits) or "not exercised by any sentence of this run"
        o.append(f"| {p['number']} | `{p['id']}` | `{md_escape(d)}` | {md_escape(p['echo'])} | `{p['check'].split()[0]}` | {cmp_} |")
    for f in voc.raw.get("frames_without_surface", []):
        d = defs.get(f["lean"] + ".at", {}).get("text", "")
        t = ft.get(f["id"])
        cmp_ = ("; ".join(f"{x['what']}: {'agree' if x['agree'] == x['points'] else '**DISAGREE**'} on {x['agree']} of {x['points']} "
                          f"evaluations ({x['false']} of them false)" for x in t) if t else "hand-written test not run")
        o.append(f"| {f['number']} | `{f['id']}` (no surface form yet) | `{md_escape(d)}` | {md_escape(f['echo'])} | `{f['check']}` | {cmp_} |")
    te = sum(r.get("evals", 0) for r in rs.values())
    ta = sum(r.get("agree", 0) for r in rs.values())
    ne = sum((it.get("search") or {}).get("evals", 0) for it in load_new_sentences().get("items", []))
    na = sum((it.get("search") or {}).get("agree", 0) for it in load_new_sentences().get("items", []))
    o += ["", f"Over all compiled readings of the fixtures: the definition and the executable reading of the frames agree on **{ta} of {te}** "
              f"(point, frame) evaluations" + (f"; over the new sentences of `heldout/`: **{na} of {ne}**" if ne else "")
              + ". The frames with no surface form are compared by `lean/Run/FrameTests.lean` on hand-written instances "
              "over the ledger and the wallet. Agreement on generated inputs is a test, not a proof that the two readings are the same.", "",
          "**The defaults** (fail-closed; each reading lists the ones applied to it):", ""]
    o += [f"- **{k}** {v}" for k, v in voc.raw["defaults"].items()]
    o += ["", "**Weakenings** (never applied silently; a modifier has to ask):", ""]
    o += [f"- **{k}**: {v}" for k, v in voc.raw["weakenings"].items()]
    o += ["", "**Quantifier scope, the one rule.** Every outline `<parameter>`, then the state, then the input are universally quantified "
              "at the front, in that order, and Givens restrict them. Collection words (`every`, `the first`, `no`) bind inside the one "
              "clause they are written in. Negation applies to the one atomic condition it is written on. Nothing is ever existentially "
              "quantified over inputs. The tool never chooses a scope.", ""]
    return o


def vocabulary_section(st, ctx, verdicts, rule_verdicts) -> list:
    voc, defs = st.voc, ctx["lean_defs"]
    used = {}
    for v in list(verdicts) + list(rule_verdicts):
        for i in (getattr(v, "pieces", None) or []):
            used[i] = used.get(i, 0) + 1
    so = load_piece_signoff()
    kinds = voc.kinds()
    o = ["## Vocabulary (the link from English to Lean)", "",
         f"`vocabulary.yaml`: **{kinds['domain']} domain words** ({len(voc.ops)} operations, {kinds['domain'] - len(voc.ops)} measures, conditions, "
         f"collections and answer words), **{kinds['modifier']} modifiers**, **{kinds['frame']} frames**, and {len(voc.idioms)} idioms "
         "(a surface form that is not the regular form of one piece, with the composition it means; an idiom adds English, no Lean). "
         "A sentence is the composition of pieces its words spell out; this table and the Lean files it names are what a reviewer has to read "
         "to trust the step from English to Lean. Sign-off is per piece and is void as soon as the piece's entry or a Lean definition it names changes.", "",
         "| Piece | Kind | Type | Surface forms | Lean | Definition | English paraphrase | Used by | Sign-off |", "|---|---|---|---|---|---|---|---|---|"]

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
                 f"| `{o_['lean']}` around the Aeneas model `{o_['model']}` | {dtext([o_['lean']])} | {md_escape(o_['echo'])} | {used.get(o_['id'], 0)} | {signoff(o_['id'])} |")
        n_un += o_["id"] not in ctx["piece_reviewed"]
    for p in voc.pieces.values():
        forms = "; ".join(p.get("forms", []) + p.get("then_forms", []) + [f"(Rule) {x}" for x in p.get("vp_forms", [])]
                          + [f"(negated) {x}" for x in p.get("not_forms", [])]
                          + [f"(plural) {x}" for x in p.get("per_actor", {}).get("forms", [])]) or "(no surface of its own)"
        o.append(f"| {p['id']} | {p['kind']} | {md_escape(p['cat'])} | {md_escape(forms)} | `{md_escape(p['lean'])}` | {dtext(p.get('defs', []))} "
                 f"| {md_escape(p['echo'])} | {used.get(p['id'], 0)} | {signoff(p['id'])} |")
        n_un += p["id"] not in ctx["piece_reviewed"]
    for i in voc.idioms.values():
        o.append(f"| {i['id']} | idiom | {md_escape(i['cat'])} | {md_escape(i['form'])} | means `{md_escape(i['means'])}` | - | (the reading of that composition) "
                 f"| {used.get(i['id'], 0)} | {signoff(i['id'])} |")
        n_un += i["id"] not in ctx["piece_reviewed"]
    total = len(all_ids(voc))
    o += ["", f"{n_un} of {total} entries are unreviewed. Record a review with `python3 -m slicegen review <id|all> --reviewer <name>` "
              "(piece ids and the ids of the old glossary are both accepted).", ""]
    return o


def regression_section(st, ctx, verdicts) -> list:
    links, meta = ctx["links"], ctx["links_meta"]
    o = ["## Regression: every old statement against its new reading (plan node V3)", "",
         "Each scenario has two Lean statements: the **reading** compiled from the composable vocabulary (`lean/Wallet/Readings.lean`) and the "
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


def new_sentences_section() -> list:
    data = load_new_sentences()
    if not data:
        return []
    items = data["items"]
    o = ["## New sentences (not in the fixtures)", "",
         "Informational; it changes no verdict and no exit status. The feature files of `heldout/` hold rules that are in no fixture, written "
         "with the existing vocabulary: **no piece was added or changed for them**. Each is compiled from the vocabulary alone "
         "(`python3 -m slicegen compile heldout/*.feature`). A new sentence has no old whole-phrase binding, so it has no flat statement, "
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
        o.append(f"| {md_escape(first)} (`{it['source']}`) | yes | {len(it['pieces'])} | {'none' if it['regular'] else 'yes'} | "
                 + (f"{sr.get('tried', 0)} inputs, {sr.get('in_scope', 0)} in scope; definition and executable reading agree on "
                    f"{sr.get('agree', 0)} of {sr.get('evals', 0)}" if sr and 'skipped' not in sr else "not searched")
                 + f" | **{md_escape(res)}**" + (f" (expected {it['expect']})" if it.get("expect") else "") + " |")
    n = sum(it["compiled"] for it in items)
    o += ["", f"{n} of {len(items)} sentences compiled with no new piece.", ""]
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
