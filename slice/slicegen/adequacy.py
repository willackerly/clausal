"""slicegen adequacy: the suite adequacy note (docs/PLAN.md node F1). INFORMATIONAL: it never changes a
verdict and never fails a run.

A proved scenario says what the code does on the inputs its Givens admit. It does not say the code does
anything useful: "a transfer never changes the total" is also true of code that rejects every transfer.
That is expected of one scenario. The question asked here is about the SUITE: taken together, do the proved
universal scenarios of an operation still hold of an implementation that does nothing?

For each operation (a model function some When phrase is bound to) a handful of TRIVIAL MODELS are generated.
Each is a Lean definition whose type is, by `type_of%`, exactly the type of the Aeneas-generated model:

    reject-all   always answers with a rejecting value and leaves the state as it was
    no-op        always answers with a success value and leaves the state as it was (does nothing but report success)
    identity     answers as the code does, but never changes the state
    constant     always answers the same value; the state is left as it was or reset to a fixed one

Which values of a result type count as a rejection or a success is stated in the glossary (`trivial.outcomes`);
an operation whose "does nothing but report success" is not a constant gets it written out (`trivial.extra`).

For each (scenario, trivial model of an operation the scenario calls) the scenario's statement is generated
again with the trivial model in place of the call, and

  1. the boundary grid of the counterexample search is searched for an input on which that statement is false
     (Run/Adequacy.lean; evidence kind: tested);
  2. where an input is found, a kernel-checked refutation at that input is attempted; where none is found, a
     kernel-checked proof that the statement holds of the trivial model for ALL inputs is attempted
     (Run/AdequacyAudit.lean; evidence kind: kernel-checked when the generated script goes through).

A scenario RULES OUT a trivial model when (1) finds an input. A set of scenarios rules it out when one of them
does, and STILL ALLOWS it otherwise. "Still allows" therefore means "no scenario of the set was shown false of
it": proved for all inputs where (2) succeeded for every scenario of the set, otherwise only not refuted on the grid.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from . import emit
from .core import Bound, slug

KINDS = ["reject-all", "no-op", "identity", "constant"]
KIND_TEXT = {
    "reject-all": "rejects everything and changes nothing",
    "no-op": "does nothing but report success",
    "identity": "answers as the code does but never changes the state",
    "constant": "always returns the same thing",
}


@dataclass
class Triv:
    call: str             # the model function it stands in for
    key: str              # unique within the operation, e.g. "same:overflow", "reset:ok", "keep-state", "x:claims_all_applied"
    kind: str             # one of KINDS
    label: str            # one line of English
    lean_name: str
    body: str             # Lean lambda
    constant: bool        # the body is `fun .. => ok <value>`: the generated kernel scripts apply

    @property
    def lean_def(self) -> str:
        return f"/-- {self.kind}: {self.label} -/\ndef {self.lean_name} : type_of% @{self.call} :=\n  {self.body}\n"

    @property
    def id(self) -> str:
        return f"{self.call}/{self.key}"


def op_slug(call: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", call)


def trivial_models(gloss) -> dict:
    """model function -> [Triv], for every function a When phrase is bound to. Empty when the glossary has no
    `trivial` section."""
    cfg = gloss.raw.get("trivial")
    out = {}
    if not cfg:
        return out
    pts, actors = gloss.param_types, gloss.actors
    for e in gloss.entries:
        if e.kind != "when" or e.call in out:
            continue
        slots = {name: typ for typ, name in e.slots}
        names = []
        for a in e.args:
            m = re.fullmatch(r"pre\((\w+)\)", a)
            names.append(m.group(1) if m else a)
        posts = [re.fullmatch(r"post\((\w+)\)", r).group(1) for r in e.returns if r.startswith("post(")]
        ov = gloss.raw.get("outcome_values", {}).get(e.outcome_type, {})
        cls = cfg.get("outcomes", {}).get(e.outcome_type, {})
        rej, suc = cls.get("reject", []), cls.get("success", [])
        lam = "fun " + " ".join(names) + " => "

        def reset(x):
            b = actors[slots[x]]["build"]
            first = str(pts[b["param_type"]]["sample"][0])
            return "(" + b["with"].format("(" + emit.lit_term(pts, b["param_type"], first) + ")") + ")", first

        def ret(c, state):
            parts = [c] + [(x if state == "same" else reset(x)[0]) for x in posts]
            return "ok " + (parts[0] if len(parts) == 1 else "(" + ", ".join(parts) + ")")

        base = f"Trivial.{op_slug(e.call)}"
        ts = []
        for key, term in ov.items():
            kind = "reject-all" if key in rej else "no-op" if key in suc else "constant"
            label = f"always answers `{key}`" + (" and leaves the state as it was" if posts else "")
            ts.append(Triv(e.call, f"same:{key}", kind, label, f"{base}.same_{slug(key)}", lam + ret(term, "same"), True))
        if posts:
            for key, term in ov.items():
                to = ", ".join(f"{slots[x]} of {reset(x)[1]}" for x in posts)
                ts.append(Triv(e.call, f"reset:{key}", "constant", f"always answers `{key}` and resets the state ({to})",
                               f"{base}.reset_{slug(key)}", lam + ret(term, "reset"), True))
            pat = "(" + ", ".join(["o"] + ["_"] * len(posts)) + ")"
            ts.append(Triv(e.call, "keep-state", "identity", "answers as the code does, but never changes the state",
                           f"{base}.keep_state",
                           lam + f"do let {pat} ← {e.call} {' '.join(names)}; " + ret("o", "same"), False))
        for x in cfg.get("extra", {}).get(e.id, []):
            ts.append(Triv(e.call, f"x:{x['name']}", x["kind"], x["label"], f"{base}.x_{slug(x['name'])}", x["lean"],
                           bool(x.get("constant", False))))
        out[e.call] = ts
    return out


def in_suite(b: Bound) -> bool:
    """Scenarios the note looks at: meant to be proved, and not a control."""
    return b.sc.expect not in ("REFUTED", "VACUOUS", "COUNTEREXAMPLE") and not b.sc.control


def pairs(bounds, models) -> list:
    """[(name, Bound, Triv)]: every scenario of a suite against every trivial model of every operation it calls."""
    out = []
    for b in bounds:
        if not in_suite(b):
            continue
        for c in b.calls:
            for t in models.get(c, []):
                out.append((pair_name(b, t), b, t))
    return out


def pair_name(b: Bound, t: Triv) -> str:
    return f"{b.id}.adq.{op_slug(t.call)}.{t.lean_name.rsplit('.', 1)[1]}"


def env_of(b: Bound, t: Triv) -> emit.Env:
    return emit.Env(b, subst={t.call: t.lean_name})


def stmt_text(name: str, b: Bound, t: Triv) -> str:
    """The scenario's statement with the trivial model in place of the call."""
    return emit.statement(b, env_of(b, t), name=name + ".stmt")


PRELUDE = ("import Wallet.Checks\nimport Bdd.Audit\nopen Aeneas Aeneas.Std Result\n"
           "set_option linter.unusedVariables false\nset_option linter.unusedTactic false\n"
           "set_option linter.unreachableTactic false\nset_option linter.unusedSimpArgs false\n"
           "set_option linter.style.nameCheck false\n")


def models_text(models) -> str:
    out = ["-- The trivial models. `type_of% @f` makes each one's type exactly the type of the generated model `f`."]
    for ts in models.values():
        out += [t.lean_def for t in ts]
    return "\n".join(out)


def search_file(bounds, models) -> str:
    """Run/Adequacy.lean: for every pair, search the scenario's boundary grid for an input on which the
    statement with the trivial model in place of the call is false. One ADEQ line per pair."""
    out = [emit.HEADER + "-- SUITE ADEQUACY NOTE, step 1 (informational; see slicegen/adequacy.py).\n"
           "-- Run once per pipeline run with `lake env lean Run/Adequacy.lean` (interpreter). Nothing here is\n"
           "-- imported by anything else, so a failure costs the note and nothing more.\n" + PRELUDE, models_text(models)]
    main = []
    for k, (name, b, t) in enumerate(pairs(bounds, models)):
        env = env_of(b, t)
        bind = emit.group(emit.in_binders(b))
        args = " ".join(n for n, _ in emit.in_binders(b))
        ts = ", ".join(f"decide ({emit.prop(b, x, env)})" for x in b.thens)
        conj = " ∧ ".join(emit.prop(b, x, env) for x in b.thens)
        tup = emit.tuple_of(emit.all_outs(env))
        run = emit.chain(b, env)
        shows = [f"{{{b.when.entry.outcome_show} outcome}}"] + [
            f"{a}: {{{b.gloss.actors[dict(b.actors)[a]]['show']} {env.post[a]}}}" for a in b.returned]
        vars_ = emit.search_vars(b)
        fn = [f"def {name}.check {bind} : Bdd.Check :=\n"
              f"  if ({b.id}.givens {args}).all id then\n"
              f"    Bdd.run ({run}) (fun {tup} => decide ({conj}))\n"
              f"  else .givenFalse",
              f"def adqSearch{k} : IO Unit := do",
              "  let mut tried := 0", "  let mut inside := 0", "  let mut bad : Option String := none"]
        ind = "  "
        for i, (n, ty) in enumerate(vars_):
            vals = ", ".join(emit.lit(b, ty, v) for v in emit.grid_values(b, ty))
            fn.append(f"{ind}for ({n}, i{i}) in ([{vals}] : List ({b.gloss.param_types[ty]['lean']})).zipIdx do")
            ind += "  "
        fn.append(f"{ind}if bad.isNone then")
        ind += "  "
        pvars = {n: n for n, _ in vars_}
        for a, _ in b.actors:
            fn.append(f"{ind}let {b.var(a)} := {emit.build_term(b, a, pvars)}")
        idx = "[" + ", ".join(f"i{i}" for i in range(len(vars_))) + "]" if vars_ else "([] : List Nat)"
        fn += [f"{ind}tried := tried + 1",
               f"{ind}let c := {name}.check {args}",
               f"{ind}if c != .givenFalse then",
               f"{ind}  inside := inside + 1",
               f"{ind}  if c != .pass then",
               f"{ind}    bad := some (Bdd.badLine {idx} c (Bdd.runThens ({run}) (fun {tup} => [{ts}])) "
               f"(Bdd.showResult ({run}) (fun {tup} => s!\"{'; '.join(shows)}\")))",
               f'  IO.println s!"ADEQ\\t{name}\\t{{tried}}\\t{{inside}}\\t{{bad.getD "-\\t-\\t-\\t-"}}"']
        out.append("\n".join(fn) + "\n")
        main.append(f"  adqSearch{k}")
    out.append("#eval show IO Unit from do\n" + ("\n".join(main) if main else "  pure ()") + "\n")
    return "\n".join(out)


def parse_search(log: str, bounds, models) -> dict:
    """ADEQ lines -> {pair name: {tried, inside, bad: {values, check, thens, returned} | None}}.
    A pair with no line is absent (the script failed before reaching it)."""
    by_name = {name: (b, t) for name, b, t in pairs(bounds, models)}
    res = {}
    for line in log.splitlines():
        p = line.split("\t")
        if p[0] != "ADEQ" or len(p) != 8 or p[1] not in by_name:
            continue
        _, name, tried, inside, bidx, bcheck, bthens, bret = p
        b, _ = by_name[name]
        bad = None
        if bidx != "-":
            idx = [int(x) for x in re.findall(r"\d+", bidx)]
            vals = {n: emit.grid_values(b, ty)[i] for (n, ty), i in zip(emit.search_vars(b), idx)}
            bad = {"values": vals, "check": bcheck, "thens": bthens, "returned": bret}
        res[name] = {"tried": int(tried), "inside": int(inside), "bad": bad}
    return res


def simp_sets(b: Bound) -> tuple:
    hints = b.gloss.raw.get("proof_hints", {})
    base = ", ".join(emit.vocab_defs(b) + emit.builder_defs(b) + emit.hint_simp(b))
    extra = "".join(", " + x for x in hints.get("refute_simp", []))
    more = "".join(", " + x for x in hints.get("refute_simp_more", []))
    return base, extra, more


def holds_theorem(name: str, b: Bound, t: Triv) -> str:
    """Attempt: the statement with the trivial model in place of the call holds for ALL inputs."""
    base, extra, _ = simp_sets(b)
    n = len(emit.out_binders(b))
    return (f"theorem {name}.holds : {name}.stmt := by\n"
            f"  unfold {name}.stmt\n"
            f"  intros\n"
            f"  refine ⟨{', '.join(['_'] * n)}, rfl, ?_⟩\n"
            f"  first\n"
            f"    | trivial\n"
            f"    | (simp_all [{base}]; done)\n"
            f"    | (simp_all [{base}]; scalar_tac)\n"
            f"    | (simp_all [{base}{extra}]; done)\n"
            f"    | (simp_all [{base}{extra}]; scalar_tac)\n"
            f"    | scalar_tac\n")


def refuted_theorem(name: str, b: Bound, t: Triv, values: dict) -> str:
    """Attempt: the statement with the trivial model in place of the call is FALSE, at the input the search found."""
    base, extra, more = simp_sets(b)
    cenv = emit.concrete_env(b, values, subst={t.call: t.lean_name})
    outs = emit.out_binders(b)
    names = ", ".join(x for x, _ in outs)
    given_proofs = " ".join(f"(by {emit.close_tac(base)})" for _ in b.givens)
    split = (f"  simp only [Prod.mk.injEq] at e3\n  obtain ⟨{', '.join('rfl' for _ in outs)}⟩ := e3\n" if len(outs) > 1
             else "  subst e3\n")
    return (f"theorem {name}.refuted : ¬ {name}.stmt := by\n"
            f"  intro h\n"
            f"  obtain ⟨{names}, e, t⟩ := h {emit.concrete_args(b, values)} {given_proofs}\n"
            f"  have e3 := Bdd.ok_inj e\n"
            f"{split}"
            f"  first\n"
            f"    | (simp [{base}] at t; done)\n"
            f"    | (simp [{base}] at t; scalar_tac)\n"
            f"    | (simp [{base}{extra}] at t; done)\n"
            f"    | (simp [{base}{extra}] at t; scalar_tac)\n"
            f"    | (simp [{base}{extra}{more}] at t; done)\n"
            f"    | (simp [{base}{extra}{more}] at t; scalar_tac)\n"
            f"    | (simp_all [{base}{extra}{more}]; done)\n"
            f"    | (simp_all [{base}{extra}{more}]; scalar_tac)\n")


def audit_file(bounds, models, search: dict) -> tuple:
    """Run/AdequacyAudit.lean and the names of the theorems it attempts.
    Only pairs with a constant trivial model and a single When get a kernel attempt; the others stay `tested`."""
    out = [emit.HEADER + "-- SUITE ADEQUACY NOTE, step 2 (informational; see slicegen/adequacy.py).\n"
           "-- For each (scenario, trivial model) pair: where the search found an input on which the statement is\n"
           "-- false of the trivial model, a kernel-checked refutation at that input; where it found none, a\n"
           "-- kernel-checked proof that the statement holds of the trivial model for every input. Scripts that\n"
           "-- fail are logged as errors and show up with `sorryAx`, which counts as no theorem.\n" + PRELUDE,
           models_text(models)]
    names = []
    for name, b, t in pairs(bounds, models):
        s = search.get(name)
        if s is None:
            continue
        out.append(stmt_text(name, b, t) + "\n")
        if b.multi or not t.constant:
            continue
        if s["bad"] is None:
            out.append(holds_theorem(name, b, t))
            names.append(name + ".holds")
        else:
            out.append(refuted_theorem(name, b, t, s["bad"]["values"]))
            names.append(name + ".refuted")
    out.append(f"#eval Bdd.Audit.report\n  (proofs := #[])\n  (refutations := #[])\n"
               f"  (derived := {emit.lean_names(names)})\n  (stmts := #[])\n  (defs := #[])\n  (fns := #[])\n")
    return "\n".join(out), names


# --------------------------------------------------------------------------- the note

STD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def kernel_ok(audit, name) -> bool:
    t = (audit or {}).get("theorems", {}).get(name) or {}
    return bool(t and t["exists"] and t.get("is_theorem") and t.get("local") and set(t["axioms"]) <= STD_AXIOMS)


def decide(bounds, models, search, audit) -> dict:
    """pair name -> {scenario, call, trivial (Triv), result: 'ruled-out' | 'holds' | 'not-ruled-out', evidence:
    'kernel-checked' | 'tested', tried, inside, bad, axioms}. Pairs the search never reported are left out."""
    out = {}
    for name, b, t in pairs(bounds, models):
        s = search.get(name)
        if s is None:
            continue
        if s["bad"] is not None:
            k = kernel_ok(audit, name + ".refuted")
            thm = name + ".refuted"
            result = "ruled-out"
        else:
            k = kernel_ok(audit, name + ".holds")
            thm = name + ".holds"
            result = "holds" if k else "not-ruled-out"
        out[name] = {"name": name, "scenario": b.id, "call": t.call, "trivial": t, "result": result,
                     "evidence": "kernel-checked" if k else "tested", "theorem": thm if k else None,
                     "axioms": ((audit or {}).get("theorems", {}).get(thm) or {}).get("axioms", []) if k else [],
                     "tried": s["tried"], "inside": s["inside"], "bad": s["bad"]}
    return out


def _assess(univ, inst, ts, decided) -> list:
    """One row per trivial model: is it ruled out by the proved universal scenarios `univ` (and, separately, by the
    proved literal examples `inst`)?"""
    rows = []
    for t in ts:
        res = {b.id: decided.get(pair_name(b, t)) for b in univ + inst}
        by = [b.id for b in univ if res[b.id] and res[b.id]["result"] == "ruled-out"]
        by_ex = [b.id for b in inst if res[b.id] and res[b.id]["result"] == "ruled-out"]
        rows.append({"trivial": t, "state": "ruled-out" if by else "allowed", "by": by, "by_examples": by_ex,
                     "not_run": [b.id for b in univ + inst if res[b.id] is None],
                     # every universal scenario is PROVED to hold of it (not merely unrefuted on the grid)
                     "holds_proved": bool(univ) and all(res[b.id] and res[b.id]["result"] == "holds" for b in univ)})
    return rows


def _kinds(rows) -> tuple:
    """(kinds every instance of which is ruled out, [(kind, allowed rows, instances of the kind)])."""
    ruled, allowed = [], []
    for k in KINDS:
        rs = [r for r in rows if r["trivial"].kind == k]
        al = [r for r in rs if r["state"] == "allowed"]
        if rs and not al:
            ruled.append(k)
        elif al:
            allowed.append((k, al, len(rs)))
    return ruled, allowed


def _allowed_text(allowed) -> str:
    out = []
    for k, al, n in allowed:
        lab = "; ".join(r["trivial"].label for r in al[:2]) + (f"; and {len(al) - 2} more" if len(al) > 2 else "")
        how = ("proved to satisfy every scenario counted" if all(r["holds_proved"] for r in al)
               else "no scenario counted is false of it on the search grid")
        out.append(f"{k}" + (f" ({len(al)} of {n} variants)" if n > 1 else "") + f": {lab} [{how}]")
    return "; ".join(out)


def line(rows) -> str:
    ruled, allowed = _kinds(rows)
    return ("rules out: " + (", ".join(ruled) or "(nothing)") + "; still allows: "
            + (_allowed_text(allowed) or "(none found)"))


EXPECTED = "(A single scenario or rule that also holds of a trivial implementation is expected; adequacy is judged for the suite.)"


def note(st, verdicts, decided, ran: bool, why: str = "") -> dict:
    """The whole note. {ran, why, ops: {call: {...}}, groups: {graph node id of a Rule or Feature: {...}}}.
    Only scenarios with a PROVED verdict are counted: universal ones for "rules out", literal ones separately."""
    models = st.triv
    status = {v.sc.id: v.status for v in verdicts}
    cand = [b for b in st.bounds if in_suite(b)]
    name = {b.id: b.sc.name for b in st.bounds}
    out = {"ran": ran, "why": why, "ops": {}, "groups": {}}
    if not ran:
        return out
    for call, ts in models.items():
        mine = [b for b in cand if call in b.calls]
        univ = [b for b in mine if status[b.id] == "PROVED-FOR-ALL"]
        inst = [b for b in mine if status[b.id] == "PROVED-INSTANCE"]
        rows = _assess(univ, inst, ts, decided)
        ruled, allowed = _kinds(rows)
        lines = [line(rows) if univ else "no proved universal scenario exercises this operation, so nothing is ruled out for all inputs"]
        ex_only = [r for r in rows if r["state"] == "allowed" and r["by_examples"]]
        if ex_only and univ:
            exs = sorted({i for r in ex_only for i in r["by_examples"]})
            lines.append(f"of those still allowed, {len(ex_only)} are ruled out only by a literal example, for its one input: "
                         + "; ".join(f'"{name[i]}"' for i in exs))
        unproved = [b for b in mine if not status[b.id].startswith("PROVED")]
        if unproved:
            lines.append("not counted (not proved in this run): " + "; ".join(f'"{b.sc.name}"' for b in unproved))
        if any(r["not_run"] for r in rows):
            lines.append("INCOMPLETE: the check did not run for every scenario of this operation (see out/adequacy.log)")
        out["ops"][call] = {"call": call, "rows": rows, "universal": [b.id for b in univ], "instances": [b.id for b in inst],
                            "unproved": [b.id for b in unproved], "ruled_kinds": ruled,
                            "allowed_kinds": [k for k, _, _ in allowed], "lines": lines,
                            "complete": not any(r["not_run"] for r in rows)}
    for f in st.features:
        for rule, scs in f.suites():
            gid = f"group:rule:{rule.id}" if rule else f"group:feature:{f.slug}"
            ids = {sc.id for sc in scs}
            mine = [b for b in cand if b.id in ids]
            calls = [c for c in models if any(c in b.calls for b in mine)]
            lines, data, expected, heads = [], {}, False, []
            if not mine:
                bound = {b.id for b in st.bounds}
                lines.append("not assessed: " + ("its scenarios are tagged @control" if any(sc.control for sc in scs)
                                                 else "there is no scenario beneath this rule" if not scs
                                                 else "the adequacy note is generated from the flat statements of the old glossary, and the "
                                                      "scenarios of this group are NEW sentences that have none"
                                                 if not any(sc.id in bound for sc in scs)
                                                 else "no scenario of this group is meant to be proved"))
                heads.append(lines[-1])
            for call in calls:
                op = out["ops"][call]
                pre = f"[{call}] " if len(calls) > 1 else ""
                univ = [b for b in mine if call in b.calls and status[b.id] == "PROVED-FOR-ALL"]
                inst = [b for b in mine if call in b.calls and status[b.id] == "PROVED-INSTANCE"]
                rows = _assess(univ, inst, models[call], decided)
                ruled, allowed = _kinds(rows)
                data[call] = {"universal": [b.id for b in univ], "ruled_kinds": ruled, "allowed_kinds": [k for k, _, _ in allowed],
                              "allowed": [r["trivial"].id for r in rows if r["state"] == "allowed"]}
                if not univ:
                    lines.append(pre + "no proved universal scenario of this group exercises "
                                 + (f"`{call}`" if not pre else "it") + ", so the group rules nothing out for all inputs"
                                 + (f" ({len(inst)} literal example{'s' if len(inst) != 1 else ''} only)" if inst else ""))
                    heads.append(lines[-1])
                    continue
                lines.append(pre + "suite " + line(rows))
                heads.append(lines[-1])
                # (a) this group alone allows it; the operation's whole suite does not
                said = False
                elsewhere = [(r, o) for r, o in zip(rows, op["rows"]) if r["state"] == "allowed" and o["state"] == "ruled-out"]
                if elsewhere:
                    by_rules = []
                    for _, o in elsewhere:
                        for i in o["by"]:
                            b = next(x for x in cand if x.id == i)
                            nm = f'Rule "{b.sc.rule.name}"' if b.sc.rule else f'scenario "{b.sc.name}"'
                            if nm not in by_rules:
                                by_rules.append(nm)
                    ks = [k for k in KINDS if any(r["trivial"].kind == k for r, _ in elsewhere)]
                    lines.append(f"{pre}taken alone, this group would also hold of: {', '.join(ks)} "
                                 f"({len(elsewhere)} variant{'s' if len(elsewhere) != 1 else ''}); the whole suite for `{call}` "
                                 f"rules {'them' if len(elsewhere) != 1 else 'it'} out through {'; '.join(by_rules)}")
                    said = True
                # (b) one scenario alone allows a kind that the group rules out
                for b in univ:
                    alone = _assess([b], [], models[call], decided)
                    ks = [k for k in ruled if any(r["trivial"].kind == k and r["state"] == "allowed" for r in alone)]
                    if ks and len(univ) > 1:
                        others = []
                        for r, a in zip(rows, alone):
                            if a["state"] == "allowed" and r["trivial"].kind in ks:
                                others += [i for i in r["by"] if i not in others]
                        lines.append(f'{pre}alone, "{b.sc.name}" would also hold of: {", ".join(ks)}; ruled out here by '
                                     + "; ".join(chr(34) + name[i] + chr(34) for i in others))
                        said = True
                expected = expected or said
                # (c) nothing proved for all inputs rules it out, anywhere
                left = [(r, o) for r, o in zip(rows, op["rows"]) if r["state"] == "allowed" and o["state"] == "allowed"]
                if left:
                    exs = sorted({i for _, o in left for i in o["by_examples"]})
                    lines.append(f"{pre}no proved universal scenario of any rule rules out the {len(left)} still allowed"
                                 + (f"; the literal example{'s' if len(exs) != 1 else ''} "
                                    + "; ".join(f'"{name[i]}"' for i in exs) + f" rule{'s' if len(exs) == 1 else ''} out "
                                    + ("all" if all(o["by_examples"] for _, o in left) else "some") + " of them, for one input each"
                                    if exs else ""))
                unproved = [b for b in mine if call in b.calls and not status[b.id].startswith("PROVED")]
                if unproved:
                    lines.append(pre + "not counted (not proved in this run): " + "; ".join(f'"{b.sc.name}"' for b in unproved))
            if expected:
                lines.append(EXPECTED)
            out["groups"][gid] = {"lines": lines, "data": data, "heads": heads}
    return out
