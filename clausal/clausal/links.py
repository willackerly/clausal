"""clausal links: generated, kernel-checked glue between the compiled readings and everything else.

For every scenario the pipeline now has TWO Lean statements:

  <id>.reading   compiled from the composable Clausebook (clausal/vocab.py): frames of lean/Frames applied
                 to an operation. This is the statement the report shows and the verdict is about.
  <id>.stmt      the FLAT statement of the old whole-phrase glossary (clausal/emit.py), unchanged. Every
                 hand-written proof, the counterexample search and the refutations are about this one.

This module writes lean/Run/Links.lean, a script run once per pipeline run, which holds

  <id>.reading_iff : <id>.reading ↔ <id>.stmt        (the V3 regression: NEW is equivalent to OLD)
  <id>.reading_sat : the scope of the reading is satisfiable, at the witness the search found
  Rule glue (see rules below)

and then asks the audit which of them the kernel accepted, with which axioms, and whether each has EXACTLY
the type it should (lean/Bdd/AuditLinks.lean). A theorem whose script fails shows up with `sorryAx` and
counts as absent: the scenario's verdict is then UNLINKED, never the old verdict.

The scripts are explicit about structure (which hypothesis gives which fact, how the two quantifier orders
correspond) and leave only LEAF facts (one old Given against one new condition; the new frame bodies against
one old Then) to a closing tactic, `bridge`.

RULES. A `Rule:` line is compiled to one statement `R` (a conjunction of frames). The universal scenarios
beneath it are its PARTS. Two generated theorems connect them:

  <rule>.from_scenarios : S₁.reading → … → Sₙ.reading → R     the suite beneath the rule entails the rule
  <rule>.gives_<k>      : R → Sₖ.reading                       the rule entails this scenario (used only to
                                                               carry a kernel-checked refutation of Sₖ up to R)
The first is attempted with a fixed script: take any state and input, case on the Givens of each scenario in
turn, use that scenario's Thens, and close the leaf with `bridge`. Where it fails, a hand-written proof of
exactly `R` may be supplied in lean/Wallet/RuleProofs/; otherwise the rule is reported as compiled, searched
on the grid through the executable frame checkers, and NOT PROVED.
"""
from __future__ import annotations

import re

from . import emit, projects
from .core import Bound
from .vocab import Reading, base_cat, group, input_paths, state_paths

HEADER = emit.HEADER


def legacy_name(b: Bound, actor_text: str) -> str:
    """The legacy variable of an actor as the Clausebook sees it written ("ledger Main" -> main)."""
    for a, _ in b.actors:
        if actor_text == a or actor_text.endswith(" " + a):
            return b.var(a)
    raise KeyError(actor_text)


def tuple_of(parts) -> str:
    return parts[0] if len(parts) == 1 else "(" + ", ".join(parts) + ")"


def nest(parts) -> str:
    """Left-nested pairs: [a, b, c] -> ((a, b), c)."""
    cur = parts[0]
    for p in parts[1:]:
        cur = f"({cur}, {p})"
    return cur


SHAPE_LEMMA = {"mut": "Bdd.opMut_some", "mut2": "Bdd.opMut2_some", "read": "Bdd.opRead_some", "read0": "Bdd.opRead0_some"}


def bridge_macro(voc, gloss) -> str:
    """The closing tactic for leaf facts. Old glossary definitions and new domain words are unfolded; the
    bridge lemmas say how the two ways of writing the same fact correspond."""
    old = [e.lean for e in gloss.entries if e.kind != "when"]
    old += gloss.raw.get("proof_hints", {}).get("simp", [])
    new = sorted({d for p in voc.pieces.values() for d in p.get("defs", []) if d.split(".")[0] in voc.domain_namespaces()
                  and not d.endswith(".at")}) + ["L.mkBatch", "LVocab.mkBatch", "Frames.aggregate", "Frames.every",
                                                 "Frames.noneOf", "Frames.theFirst"]
    # the facts each project declares for the glue (projects.yaml, `lean.bridge.lemmas`), between the fixed ones
    lem = ["Bdd.Bridge.u64_val_eq", "Bdd.Bridge.usize_val_eq"] + projects.load().bridge_lemmas() + ["Bdd.Bridge.range_eq",
           "Option.mem_toList", "Option.mem_def", "List.mem_range", "List.getElem?_eq_none_iff", "Nat.not_lt", "Nat.not_le"]
    s = ", ".join(dict.fromkeys(old + new))
    sl = ", ".join(lem)
    # for the non-vacuity witnesses: concrete ledgers and batches are built by constructors that must stay folded
    # (the glossary's `proof_hints.simp` lemmas say what they build)
    ss = ", ".join(dict.fromkeys([x for x in old + new if x not in ("L.mkBatch", "LVocab.mkBatch")] + ["Vocab.mkWallet", "L.mkBatch_val"]))
    return (f"macro \"bridge\" : tactic => `(tactic| first\n"
            f"  | assumption\n"
            f"  | trivial\n"
            f"  | (constructor <;> assumption)\n"
            f"  | (simp only [{s}, {sl}] at *; first | assumption | omega | (constructor <;> first | assumption | omega))\n"
            f"  | (simp_all [{s}, {sl}]; done)\n"
            f"  | (simp_all [{s}, {sl}]; omega)\n"
            f"  | (simp_all [{s}, {sl}]; grind)\n"
            f"  | grind)\n"
            f"macro \"bridge_sat\" : tactic => `(tactic| first\n"
            f"  | exact trivial\n"
            f"  | (refine ⟨trivial, ?_⟩; decide)\n"
            f"  | (refine ⟨trivial, ?_⟩; simp [{ss}]; done)\n"
            f"  | (refine ⟨trivial, ?_⟩; simp [{ss}]; scalar_tac)\n"
            f"  | (refine ⟨trivial, ?_⟩; simp [{ss}]; omega))\n")


class Link:
    """Everything about one scenario that both directions of the equivalence need."""

    def __init__(self, voc, rd: Reading, b: Bound):
        self.voc, self.rd, self.b = voc, rd, b
        info = rd.info
        self.ops = info["ops"]
        self.n = len(self.ops)
        self.ctx = info["ctx"]
        self.env = emit.Env(b)
        self.bys = info["bystanders"]
        self.nb = len(self.bys)
        self.roles = [legacy_name(b, a) for a in info["st_actors"]]
        self.rpaths, self.bpaths = state_paths(len(self.roles), self.nb)
        self.ipaths = info["ipaths"]
        # the input of each When: a legacy parameter name, a literal (pinned), or nothing
        self.inputs = []
        for o, bind in zip(self.ops, info["binds"]):
            if not o["input"]:
                self.inputs.append(("unit", "()"))
            else:
                leaf = bind[o["input"][0][0]]
                self.inputs.append(("param", leaf.param) if leaf.how == "param" else ("lit", self.ctx.value(leaf)))
        self.every = [k for k, c in enumerate(rd.claims) if not c.mods]
        self.filtered = [k for k, c in enumerate(rd.claims) if c.mods]
        self.given_conds = [c for c in rd.conds if c["pin"] is None]
        self.pins = [c for c in rd.conds if c["pin"] is not None]

    def ok(self) -> str | None:
        """None if the two statements have the shape the script assumes; otherwise why not."""
        b = self.b
        if len(self.given_conds) != len(b.givens):
            return "the reading has a different number of Givens from the flat statement"
        if len({c.step for c in self.rd.claims if c.step >= 0}) != len(b.thens):
            return "the reading has a different number of Thens from the flat statement"
        if [w.entry.call for w in b.whens] != [o["model"] for o in self.ops]:
            return "the reading and the flat statement are about different model functions"
        if not self.every:
            return "no claim of the reading covers every call"
        return None

    # ---- terms of the flat statement, written with the reading's variables, and the other way round
    def st_fwd(self) -> str:
        """The state, built from the flat statement's actor variables."""
        cur = tuple_of(self.roles)
        for a in self.bys:
            cur = f"({cur}, {legacy_name(self.b, a)})"
        return cur

    def inp_fwd(self) -> str:
        return nest([x for _, x in self.inputs])

    def inp_names(self) -> list:
        """Backward direction: the name each When's input goes by once `inp` is taken apart."""
        return ["inp"] if self.n == 1 else [f"i{k + 1}" for k in range(self.n)]

    def legacy_args(self) -> list:
        """The flat statement's ∀-binders (parameters, then actors), as terms over `st`, the input names and the outer parameters."""
        names = self.inp_names()
        by_param = {x: names[k] for k, (how, x) in enumerate(self.inputs) if how == "param"}
        out = []
        for n, _ in emit.in_binders(self.b):
            if n in by_param:
                out.append(by_param[n])
            elif n in [p for p, _ in self.b.params]:
                out.append(n)
            else:
                out.append("st" + self.path_of(n))
        return out

    def path_of(self, legacy_var: str) -> str:
        for a, p in zip(self.roles, self.rpaths):
            if a == legacy_var:
                return p
        for a, p in zip(self.bys, self.bpaths):
            if legacy_name(self.b, a) == legacy_var:
                return p
        raise KeyError(legacy_var)

    def stage_outs(self, k):
        """Legacy output names of stage k: (answer name, [post-state names])."""
        _, _, outs = self.env.stages[k]
        return outs[0][0], [n for n, _ in outs[1:]]

    def theorem(self) -> str:
        rd, b = self.rd, self.b
        outer = " ".join(n for n, _ in rd.outer)
        k = len(rd.claims)
        hs = [f"h{j + 1}" for j in range(k)]
        L = [f"/-- NEW ↔ OLD: the reading compiled from the Clausebook says exactly what the flat statement says. -/",
             f"theorem {rd.id}.reading_iff : {rd.name} ↔ {b.id}.stmt := by",
             "  constructor"]
        # ------------------------------------------------------------------ reading → flat
        bn = " ".join(n for n, _ in emit.in_binders(b))
        gs = [f"g{j + 1}" for j in range(len(b.givens))]
        L.append(f"  · intro h {bn} {' '.join(gs)}".rstrip())
        L.append(f"    obtain ⟨{', '.join(hs)}⟩ := h {outer}".rstrip() if k > 1 else f"    have h1 := h {outer}".rstrip())
        st, inp = self.st_fwd(), self.inp_fwd()
        if rd.conds:
            parts = ["trivial"] + ["by bridge"] * len(self.given_conds) + ["rfl"] * len(self.pins)
            L.append(f"    have sc : ({rd.op}).scope {st} {inp} := ⟨{', '.join(parts)}⟩")
        else:
            L.append(f"    have sc : ({rd.op}).scope {st} {inp} := trivial")
        first = True
        for j in self.every:
            if first:
                L.append(f"    obtain ⟨r, s', e, q{j + 1}⟩ := h{j + 1} {st} {inp} sc")
                first = False
            else:
                L.append(f"    obtain ⟨r2, s2, e2, q{j + 1}⟩ := h{j + 1} {st} {inp} sc")
                L.append("    obtain ⟨u1, u2⟩ := Frames.Op.answer_unique e e2; subst u1 u2; clear e2")
        for j in self.filtered:
            L.append(f"    have q{j + 1} := h{j + 1} {st} {inp} sc r s' e")
        L.append(f"    try clear h")
        L.append(f"    clear {' '.join(hs)} sc")
        L.append(f"    have x : ({rd.base}).run {st} {inp} = some (r, s') := e")
        L.append("    clear e")
        post, cur = "s'", "x"
        for i in reversed(range(self.nb)):
            L.append(f"    obtain ⟨t{i}, x{i}, u⟩ := Frames.Op.beside_some.mp {cur}; subst u; clear {cur}")
            post, cur = f"t{i}", f"x{i}"
        # stages: e{k} is the equation of stage k, with outputs (ans{k}, post{k})
        ans = {self.n - 1: "r"}
        posts = {self.n - 1: post}
        raw = {}
        for kk in range(self.n - 1, 0, -1):
            L.append(f"    obtain ⟨r{kk}, s{kk}, y{kk - 1}, z{kk}⟩ := Frames.Op.andThen_some.mp {cur}; clear {cur}")
            ans[kk - 1], posts[kk - 1] = f"r{kk}", f"s{kk}"
            raw[kk] = f"z{kk}"
            cur = f"y{kk - 1}"
        raw[0] = cur
        final = []
        for kk, o in enumerate(self.ops):
            lem = SHAPE_LEMMA[o["shape"]]
            if o["shape"] in ("mut", "mut2"):
                L.append(f"    have e{kk} := {lem}.mp {raw[kk]}")
                comps = [posts[kk]] if o["shape"] == "mut" else [posts[kk] + ".1", posts[kk] + ".2"]
            else:
                # the state after a read is the state before it: eliminate the read's own "after" variable
                L.append(f"    obtain ⟨e{kk}, u⟩ := {lem}.mp {raw[kk]}; have u := u.symm; subst u")
                comps = []
            final += [ans[kk]] + comps + [f"e{kk}"]
        final += ["by bridge"] * len(b.thens)
        L.append(f"    exact ⟨{', '.join(final)}⟩")
        # ------------------------------------------------------------------ flat → reading
        L.append(f"  · intro h {outer}".rstrip())
        if k > 1:
            L.append(f"    refine ⟨{', '.join(['?_'] * k)}⟩")
        L.append("    all_goals intro st inp sc")
        names = self.inp_names()
        if self.n > 1:
            pat = names[0]
            for nm in names[1:]:
                pat = f"⟨{pat}, {nm}⟩"
            L.append(f"    all_goals obtain {pat} := inp")
        if rd.conds:
            cs = [f"c{j + 1}" for j in range(len(self.given_conds))] + [f"p{j + 1}" for j in range(len(self.pins))]
            L.append(f"    all_goals obtain ⟨-, {', '.join(cs)}⟩ := sc")
            for j in range(len(self.pins)):
                L.append(f"    all_goals subst p{j + 1}")
        else:
            L.append("    all_goals clear sc")
        pat = []
        for kk in range(self.n):
            a, ps = self.stage_outs(kk)
            pat += [a] + ps + [f"eq{kk}"]
        pat += [f"t{j + 1}" for j in range(len(b.thens))]
        gargs = " ".join(["(by bridge)"] * len(b.givens))
        L.append(f"    all_goals obtain ⟨{', '.join(pat)}⟩ := h {' '.join(self.legacy_args())} {gargs}".rstrip())
        L.append("    all_goals clear h")
        # the state after each stage, in the flat statement's names
        cur_state = "st" + ".1" * self.nb
        E = None
        for kk, o in enumerate(self.ops):
            a, ps = self.stage_outs(kk)
            lem = SHAPE_LEMMA[o["shape"]]
            if o["shape"] in ("mut", "mut2"):
                term = f"{lem}.mpr eq{kk}"
                cur_state = tuple_of(ps)
            else:
                term = f"{lem}.mpr ⟨eq{kk}, rfl⟩"
            E = term if E is None else f"Frames.Op.andThen_some.mpr ⟨_, _, {E}, {term}⟩"
        post = cur_state
        for j in range(self.nb):
            E = f"Frames.Op.beside_some.mpr ⟨_, {E}, rfl⟩"
            post = f"({post}, st{self.bpaths[j]})"
        last_ans = self.stage_outs(self.n - 1)[0]
        inp_t = nest([nm if how != "lit" else x for nm, (how, x) in zip(names, self.inputs)])
        L.append(f"    all_goals have e : ({rd.base}).run st {inp_t} = some ({last_ans}, {post}) := {E}")
        for j, c in enumerate(rd.claims):
            if not c.mods:
                L.append("    · exact ⟨_, _, e, by bridge⟩")
            else:
                L.append("    · intro r2 s2 e2 hmod; obtain ⟨u1, u2⟩ := Frames.Op.answer_unique e e2; subst u1 u2; bridge")
        return "\n".join(L) + "\n"

    def sat_theorem(self, values: dict) -> str:
        """The scope of the reading can be met: at the input the search found for the flat statement's Givens."""
        rd, b = self.rd, self.b
        cenv = emit.concrete_env(b, values)
        outer = [cenv.params[n] for n, _ in rd.outer]
        actors = {b.var(a): cenv.pre[a] for a, _ in b.actors}
        st = tuple_of([actors[r] for r in self.roles])
        for a in self.bys:
            st = f"({st}, {actors[legacy_name(b, a)]})"
        ins = []
        for how, x in self.inputs:
            ins.append(cenv.params[x] if how == "param" else x)
        inp = nest(ins)
        binders = rd.outer + [("st", rd.state_type), ("inp", rd.input_type)]
        return (f"/-- The reading is not vacuous: some state and input are in its scope. -/\n"
                f"theorem {rd.id}.reading_sat : ∃ {group(binders)}, ({rd.op}).scope st inp :=\n"
                f"  ⟨{', '.join(outer + [st, inp])}, by bridge_sat⟩\n")


# --------------------------------------------------------------------------- Rules against their scenarios

def proj(j: int, k: int) -> str:
    """Projection of the j-th conjunct out of k (right-nested ∧)."""
    if k == 1:
        return ""
    return ".2" * j + (".1" if j < k - 1 else "")


def is_naming(cond: dict, outer: list) -> bool:
    """A Given that only names a value: `<measure> is <outline parameter>`. In a glue proof the parameter is
    whatever the measure is at the state at hand, so the condition holds by `rfl`."""
    n = cond["node"]
    if n is None or n.id != "is":
        return False
    t = n.args["t"]
    from .vocab import Leaf, Node
    if not isinstance(t, Node) or len(t.args) != 1:
        return False
    leaf = next(iter(t.args.values()))
    return isinstance(leaf, Leaf) and leaf.how == "param" and leaf.param in [x for x, _ in outer]


def mentions_outer(cond: dict, outer: list) -> bool:
    from .vocab import Leaf, walk
    names = [x for x, _ in outer]
    return any(isinstance(l, Leaf) and l.how == "param" and l.param in names for l in walk(cond["node"]))


def usable_part(sc_rd: Reading) -> bool:
    """A scenario that can serve as a part of its Rule: an outline about one operation, with no bystander and
    no pinned literal, whose non-naming Givens do not mention an outline parameter."""
    info = sc_rd.info
    if len(info["ops"]) != 1 or info["bystanders"] or info["pins"]:
        return False
    return all(is_naming(c, sc_rd.outer) or not mentions_outer(c, sc_rd.outer) for c in sc_rd.conds)


def use_scenario(sc: Reading, hname: str, kname: str, ind: str, have_answer: bool = False, tag: str = "") -> list:
    """Lines that pull every fact scenario `sc` gives at (st, inp) into the context: r, s', e, and one fact per
    claim (named q<tag><n>). `have_answer`: r, s', e are already there (from another scenario)."""
    under = " ".join(["_"] * len(sc.outer))
    base = f"({hname} {under})" if sc.outer else hname
    split = [c for c in sc.conds if not is_naming(c, sc.outer)]
    parts, j = ["trivial"], 0
    for c in sc.conds:
        if is_naming(c, sc.outer):
            parts.append("rfl")
        else:
            parts.append(kname + proj(j, len(split)))
            j += 1
    scope = "⟨" + ", ".join(parts) + "⟩" if sc.conds else "trivial"
    k = len(sc.claims)
    L, first = [], not have_answer
    for j, c in enumerate(sc.claims):
        if c.mods:
            continue
        h = f"{base}{proj(j, k)} st inp {scope}"
        if first:
            L.append(f"{ind}obtain ⟨r, s', e, q{tag}{j + 1}⟩ := {h}")
            first = False
        else:
            L.append(f"{ind}obtain ⟨r2, s2, e2, q{tag}{j + 1}⟩ := {h}")
            L.append(f"{ind}obtain ⟨u1, u2⟩ := Frames.Op.answer_unique e e2; subst u1 u2; clear e2")
    for j, c in enumerate(sc.claims):
        if c.mods:
            L.append(f"{ind}have q{tag}{j + 1} := {base}{proj(j, k)} st inp {scope} r s' e")
    return L


def rule_glue(rule: Reading, parts: list) -> tuple:
    """(text, hypothesis reading names) of `<rule>.from_scenarios`, or (reason, None) if it cannot be stated."""
    parts = [p for p in parts if usable_part(p)]
    if not parts:
        return "no universal scenario beneath the rule is about one operation with nothing pinned", None
    hs = [f"s{i + 1}" for i in range(len(parts))]
    L = [f"/-- The scenarios beneath the rule, together, entail the rule statement. -/",
         f"theorem {rule.id}.from_scenarios : " + " → ".join(p.name for p in parts) + f" → {rule.name} := by",
         f"  intro {' '.join(hs)}"]
    k = len(rule.claims)
    if k > 1:
        L.append(f"  refine ⟨{', '.join(['?_'] * k)}⟩")
    for c in rule.claims:
        clause = rule.info["clauses"][c.clause]
        cands = [(h, p) for h, p in zip(hs, parts) if p.base == clause["base"]]
        if not cands:
            return f"no universal scenario beneath the rule is about `{clause['base']}`", None
        L.append("  · intro st inp sc")
        if c.mods:
            L.append("    intro r0 s0 e0 hm")
        close = ("exact ⟨r, s', e, by bridge⟩" if not c.mods else
                 "obtain ⟨u1, u2⟩ := Frames.Op.answer_unique e0 e; subst u1 u2; bridge")
        def split_of(p):
            return [x for x in p.conds if not is_naming(x, p.outer)]
        always = [(h, p) for h, p in cands if not split_of(p)]      # scenarios that apply to every input
        some = [(h, p) for h, p in cands if split_of(p)]            # scenarios that apply to the inputs their Givens name
        got = False
        for n, (h, p) in enumerate(always):
            L += use_scenario(p, h, "", "    ", have_answer=got, tag=f"a{n}_")
            got = True

        def cases(cs, i, ind):
            if not cs:
                # no conditional scenario applies. With an unconditional one in hand the rule must follow from it;
                # otherwise the Givens of the suite must cover every input.
                return [ind + close] if got else [ind + "exfalso; bridge"]
            h, p = cs[0]
            kn = f"k{i}"
            body = use_scenario(p, h, kn, ind + "  ", have_answer=got, tag=f"c{i}_") + [ind + "  " + close]
            rest = cases(cs[1:], i + 1, ind + "  ")
            return ([f"{ind}by_cases {kn} : " + " ∧ ".join("(" + x["lean"] + ")" for x in split_of(p)),
                     ind + "· " + body[0].strip()] + body[1:] + [ind + "· " + rest[0].strip()] + rest[1:])
        L += cases(some, 1, "    ")
    return "\n".join(L) + "\n", [p.name for p in parts]


def rule_refutation(voc, gloss, rule: Reading, bad: dict, point: dict) -> str | None:
    """`¬ <rule>.reading`, at the grid point where the reading's own search found it false. Generated only when
    the failing frame covers every call and its clause is about a single operation."""
    j = bad["bits"].index("0")
    c = rule.claims[j]
    clause = rule.info["clauses"][c.clause]
    if c.mods or len(clause["ops"]) != 1 or c.runs != 1:
        return None
    o = clause["ops"][0]
    hints = gloss.raw.get("proof_hints", {})
    old = [e.lean for e in gloss.entries if e.kind != "when"] + hints.get("simp", [])
    new = sorted({d for p in voc.pieces.values() for d in p.get("defs", []) if d.split(".")[0] in voc.domain_namespaces() and not d.endswith(".at")})
    s1 = ", ".join(dict.fromkeys([x for x in old + new if x not in ("L.mkBatch",)] + ["Vocab.mkWallet", "L.mkBatch_val", "Frames.aggregate", "Frames.every",
                                                                                "Frames.theFirst", "Frames.noneOf"]))
    s2 = s1 + "".join(", " + x for x in hints.get("refute_simp", []))
    s3 = s2 + "".join(", " + x for x in hints.get("refute_simp_more", []))
    lem = SHAPE_LEMMA[o["shape"]]
    conv = (f"  have e0 := {lem}.mp x" if o["shape"] in ("mut", "mut2") else
            f"  obtain ⟨e0, u⟩ := {lem}.mp x; have u := u.symm; subst u")
    closers = ("       all_goals first\n"
               + "".join(f"         | (intro heq; cases heq; simp_all [{s}]; done)\n         | (intro heq; cases heq; simp_all [{s}]; scalar_tac)\n"
                         f"         | (simp_all [{s}]; done)\n         | (simp_all [{s}]; scalar_tac)\n" for s in (s1, s2, s3))
               + "         | scalar_tac)\n")
    return (f"/-- The rule statement is FALSE: at this input the model gives an answer the rule does not allow. -/\n"
            f"theorem {rule.id}.refuted : ¬ {rule.name} := by\n"
            f"  intro h\n"
            f"  obtain ⟨r, s', e, q⟩ := h{proj(j, len(rule.claims))} {point['st']} {point['inp']} (by bridge_sat)\n"
            f"  have x : ({clause['base']}).run {point['st']} {point['inp']} = some (r, s') := e\n"
            f"{conv}\n"
            f"  refine Bdd.false_of_spec e0 ?_\n"
            f"  first\n"
            f"    | (unfold {o['model']}\n       step*\n{closers}"
            f"    | (step*\n{closers}")


def lean_names(xs) -> str:
    return "#[" + ", ".join("`" + x for x in xs) + "]"


def build(st, search: dict, rs: dict, side: dict, ps: dict, extra=(), proof_mods: dict | None = None) -> tuple:
    """The whole of lean/Run/Links.lean and what it contains: (text, meta).
    meta: {iffs: [[theorem, reading, stmt]], sats: [...], skipped: [[id, why]], imps: [[theorem, [hyps], rule reading]],
           noglue: {rule: why}, nots: [[theorem, rule reading]], proofs: [[theorem, rule reading, module]], consts: [...]}"""
    from . import oblig
    from .pipeline import LEAN, proof_module, proof_path, rule_proof_module, rule_proof_path
    from .vocab import Reading
    voc, gloss = st.voc, st.gloss
    built = set(ps.get("built", []))
    new_mods = [proof_module(sc.id) for sc, _ in st.new_scenarios if proof_path(sc.id).exists() and proof_module(sc.id) in built]
    lemma_names = {f"ledger.{m}.spec" for f in sorted((LEAN / "Ledger" / "Lemmas").glob("*.lean"))
                   for m in re.findall(r"^theorem (Ledger\.\w+)\.spec\b", f.read_text(), re.M)}

    def about_obligation(path, id_) -> bool:
        return bool(re.search(rf"theorem\s+{re.escape(id_)}\s*:\s*{re.escape(id_)}\.obligation\b", path.read_text()))
    rule_mods = [rule_proof_module(r.id) for r, rd in st.rules
                 if isinstance(rd, Reading) and rule_proof_path(r.id).exists() and rule_proof_module(r.id) in built]
    out = [HEADER + "-- Run once per pipeline run with `lake env lean Run/Links.lean`.\n"
           "-- Part 1: NEW ↔ OLD. For every scenario, the reading compiled from the composable Clausebook is\n"
           "--         equivalent to the flat statement of the old whole-phrase glossary, which is the statement the\n"
           "--         hand-written proofs, the search and the refutations are about. And the reading is not vacuous.\n"
           "-- Part 2: every `Rule:` statement against the scenarios beneath it (glue), and a refutation of a Rule\n"
           "--         statement at the input where the reading search found it false.\n"
           "-- Part 3: the audit of all of the above, printed as one JSON line (`LINKS`).\n"
           "-- A theorem whose script fails is logged as an error and counts as absent.\n"
           + "".join(f"import {m}\n" for m in rule_mods)
           + "".join(f"import {m}\n" for m in new_mods)
           + "import Wallet.Obligations\n"
           + "".join(f"import {m}\n" for m in (proof_mods or {}).values())
           + "".join(f"import {m}\n" for m in extra)
           + "import Wallet.Readings\nimport Wallet.Statements\n"
           + "".join(f"import {m}\n" for m in projects.load().bridge_modules())
           + "import Bdd.AuditLinks\n"
           "open Aeneas Aeneas.Std Result\n"
           "set_option linter.unusedTactic false\nset_option linter.unreachableTactic false\n"
           "set_option linter.unusedSimpArgs false\nset_option linter.unusedVariables false\n"
           "set_option maxHeartbeats 200000\n\n" + bridge_macro(voc, gloss) + oblig.leaf_tactics(voc, gloss)]
    meta = {"iffs": [], "sats": [], "skipped": [], "imps": [], "noglue": {}, "nots": [], "proofs": [], "consts": [], "holds": [],
            "oiffs": [], "oproofs": [], "ofail": {}}
    held = set()        # readings for which `<id>.reading_holds` is generated
    for rd, b in st.link_pairs:
        lk = Link(voc, rd, b)
        out.append(f"-- ===== {rd.id}")
        why = lk.ok()
        if why:
            out.append(f"-- no equivalence generated: {why}\n")
            meta["skipped"].append([rd.id, why])
            continue
        out.append(lk.theorem())
        meta["iffs"].append([rd.id + ".reading_iff", rd.name, b.id + ".stmt"])
        if b.id in (proof_mods or {}):
            # the reading ITSELF as one theorem: the hand-written proof of the flat statement, carried through the equivalence
            out.append(f"/-- The compiled reading holds: the proof of the flat statement ({proof_mods[b.id]}), through the equivalence. -/\n"
                       f"theorem {rd.id}.reading_holds : {rd.name} := {rd.id}.reading_iff.mpr {b.id}\n")
            meta["holds"].append([rd.id + ".reading_holds", rd.name])
            held.add(rd.name)
        s = search.get(b.id, {})
        if s.get("sat") is not None:
            out.append(lk.sat_theorem(s["sat"]))
            meta["sats"].append(rd.id + ".reading_sat")
    # ---- NEW sentences: scenarios with no flat statement in the old glossary. Reading ↔ generated obligation; the reading
    # ---- itself from a supplied proof of the obligation; non-vacuity and refutation at the points the reading search found.
    out.append("-- ===== Part 1b: NEW sentences (no entry in the old glossary): reading ↔ flat proof obligation\n")
    for sc, rd in st.new_scenarios:
        out.append(f"-- ===== {rd.id}")
        try:
            out.append(oblig.iff_theorem(rd))
            meta["oiffs"].append([rd.id + ".reading_iff_obligation", rd.name, rd.id + ".obligation"])
        except KeyError as e:
            meta["ofail"][rd.id] = str(e)
            out.append(f"-- no obligation: {e}\n")
            continue
        if proof_module(sc.id) in new_mods:
            out.append(f"/-- The compiled reading holds: the supplied proof of its flat obligation ({proof_module(sc.id)}), through the equivalence. -/\n"
                       f"theorem {rd.id}.reading_holds : {rd.name} := {rd.id}.reading_iff_obligation.mpr {rd.id}\n")
            meta["holds"].append([rd.id + ".reading_holds", rd.name])
            meta["oproofs"].append([rd.id, rd.id + ".obligation", proof_module(sc.id), rd.id + ".reading_holds"])
            held.add(rd.name)
        r_ = rs.get(rd.id, {})
        if r_.get("sat"):
            out.append(oblig.sat_theorem(rd, rsearch_point(side, rd.id, r_["sat"])))
            meta["sats"].append(rd.id + ".reading_sat")
        if r_.get("bad"):
            t = oblig.refutation(voc, gloss, rd, r_["bad"], rsearch_point(side, rd.id, r_["bad"]), lemma_names)
            if t:
                out.append(t)
                meta["nots"].append([rd.id + ".refuted", rd.name])
    for r, rd in st.rules:
        if not isinstance(rd, Reading):
            continue
        out.append(f"-- ===== {rd.id}")
        try:
            out.append(oblig.iff_theorem(rd))
            meta["oiffs"].append([rd.id + ".reading_iff_obligation", rd.name, rd.id + ".obligation"])
            if rule_proof_module(r.id) in rule_mods and about_obligation(rule_proof_path(r.id), r.id):
                out.append(f"/-- The rule statement holds: the supplied proof of its flat obligation ({rule_proof_module(r.id)}), through the equivalence. -/\n"
                           f"theorem {rd.id}.proved : {rd.name} := {rd.id}.reading_iff_obligation.mpr {rd.id}\n")
                meta["holds"].append([rd.id + ".proved", rd.name])
                meta["oproofs"].append([rd.id, rd.id + ".obligation", rule_proof_module(r.id), rd.id + ".proved"])
        except KeyError as e:
            meta["ofail"][rd.id] = str(e)
        text, hyps = rule_glue(rd, st.rule_parts(r))
        if hyps is None:
            out.append(f"-- no glue generated: {text}\n")
            meta["noglue"][rd.id] = text
        else:
            out.append(text)
            meta["imps"].append([rd.id + ".from_scenarios", hyps, rd.name])
            if all(h in held for h in hyps):
                # the rule statement ITSELF as one theorem: the glue applied to the scenario readings, each already a theorem
                args = " ".join(h.rsplit(".", 1)[0] + ".reading_holds" for h in hyps)
                out.append(f"/-- The rule statement holds for every input: from its scenarios, each proved. -/\n"
                           f"theorem {rd.id}.holds : {rd.name} := {rd.id}.from_scenarios {args}\n")
                meta["holds"].append([rd.id + ".holds", rd.name])
        bad = rs.get(rd.id, {}).get("bad")
        if bad:
            t = rule_refutation(voc, gloss, rd, bad, rsearch_point(side, rd.id, bad))
            if t:
                out.append(t)
                meta["nots"].append([rd.id + ".refuted", rd.name])
            # the general script (also: clauses about accepted or rejected calls, two calls compared, sequences)
            t2 = oblig.refutation(voc, gloss, rd, bad, rsearch_point(side, rd.id, bad), lemma_names)
            if t2:
                out.append(t2.replace(f"theorem {rd.id}.refuted :", f"theorem {rd.id}.refuted2 :"))
                meta["nots"].append([rd.id + ".refuted2", rd.name])
        if rule_proof_module(r.id) in rule_mods and not about_obligation(rule_proof_path(r.id), r.id):
            meta["proofs"].append([r.id, rd.name, rule_proof_module(r.id)])
    meta["consts"] = [rd.name for rd, _ in st.compiled]
    out.append("#eval Bdd.Audit.reportLinks\n"
               "  (iffs := #[" + ", ".join(f"(`{a}, `{b}, `{c})" for a, b, c in meta["iffs"] + meta["oiffs"]) + "])\n"
               "  (imps := #[" + ", ".join(f"(`{t}, {lean_names(h)}, `{c})" for t, h, c in meta["imps"]) + "])\n"
               "  (nots := #[" + ", ".join(f"(`{a}, `{b})" for a, b in meta["nots"]) + "])\n"
               "  (proofs := #[" + ", ".join([f"(`{a}, `{b})" for a, b, _ in meta["proofs"]] + [f"(`{a}, `{b})" for a, b in meta["holds"]]
                                             + [f"(`{a}, `{b})" for a, b, _, _ in meta["oproofs"]]) + "])\n"
               f"  (locals := {lean_names(meta['sats'])})\n  (consts := {lean_names(meta['consts'])})\n"
               # the library roots of the declared projects: the audit refuses to report if it does not enter one of them
               f"  (roots := {lean_names(dict.fromkeys(r for p in projects.load() for r in p.roots))})\n")
    return "\n".join(out), meta


def rsearch_point(side: dict, id_: str, bad: dict) -> dict:
    from .rsearch import point_terms
    if bad.get("terms"):        # not a grid point: an input fed back from the generated harnesses (clausal/evidence.py)
        return bad["terms"]
    return point_terms(side[id_], bad["index"])
