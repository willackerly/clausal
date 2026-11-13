#!/usr/bin/env python3
"""Trust test 1 (plan node W6): the seven controls, as frozen in trust/test1/controls.yaml and trust/FREEZE-w46.md section 5.

    python3 trust/tests/test1_controls.py [--only T1.1,T1.3] [--work DIR] [--keep]     (after ./run.sh or ./run.sh --quick)
    python3 trust/tests/test1_controls.py --collect      write trust/tests/test1_controls.result.json from what the controls left

Nothing here writes to the tree except the result file: every change is made in a scratch copy (mutation/workcopy.sh for the
controls that run the pipeline; a copy without build output for the ones that only read records). A control leaves its
result in <work>/<id>.json; `--collect` puts them together, so controls can be run at the same time in separate processes.
Heavy steps go through tools/sem.sh 3.

  T1.1  intake with the verify step deleted            ./run.sh --quick --no-unit: U1 REFUTED, every rule on `in.verifies` flagged
  T1.2  intake verifies under a key from the message   ./run.sh --quick --no-unit: accept_only_if_verified REFUTED
  T1.3  the Lean definition of `in.verifies` edited    clausal attest check: the model record is VOID
  T1.4  a record kind person with a model: id          clausal attest check: REFUSED, exit 1
  T1.5  --strict on the unmutated run                  fails, naming the owner and the specialist as awaited
  T1.6  the ledger entry deleted                       clausal gen stops; ./run.sh --quick stops before step 4
  T1.7  verify in a crate that is not translated       reduced scope (see the freeze): passed iff a theorem of U1 AS GENERATED (the
                                                       obligation of SM-2 with the word rebound to the axiom's answer) is reported with
                                                       the axiom, does not count with `lean_axioms: []`, and counts and is flagged once
                                                       the axiom is listed. NOT PASSED: U1 as generated has no proof of the variant (it
                                                       says every call answers; `T17.needs` shows that needs the external verifier to
                                                       return). Reported beside it, and not a pass: the same three questions asked of a
                                                       hand-written statement WEAKER than U1 (`shown_on_a_weaker_statement_only`)

(--no-unit: the crate's own unit tests fail on T1.1 and T1.2, which would stop run.sh at step 1 before any sentence is looked
at; the mutation harness passes the same flag for the same reason. Whether the unit tests fail is recorded too.)
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))
SEM = ROOT.parent / "tools" / "sem.sh"
if not SEM.exists():                       # a git worktree: tools/ is beside clausal/ in every checkout
    SEM = Path(subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()) / "tools" / "sem.sh"
ENV = dict(os.environ, PATH=f"{Path.home()}/.elan/bin:{Path.home()}/.cargo/bin:" + os.environ.get("PATH", ""))
A = "A.sig.unforgeable"
U1 = "group:rule:Rule.intake.accept_only_if_verified"
LIGHT = shutil.ignore_patterns("target", ".lake", ".tools", "mutation", "work", "__pycache__", "census", "review", "probe", "effort", "compare")

# the mutants, as text replacements in sigintake/src/lib.rs (each `old` occurs exactly once)
VERIFY_STEP = """    if !verify(expected_key, msg.payload, msg.counter, msg.tag) {
        return false;
    }
"""
MUTANTS = {
    "T1.1": (VERIFY_STEP, ""),                                                    # accepts on the counter alone: verify is never called
    "T1.2": (VERIFY_STEP, """    let from_message = Key { id: msg.hint };
    if !verify(&from_message, msg.payload, msg.counter, msg.tag) {
        return false;
    }
"""),                                                                             # the key is taken from the message (its hint)
}
# T1.7: the verifier as a second crate, which Charon does not translate
SIGVERIFY_TOML = '[package]\nname = "sigverify"\nversion = "0.1.0"\nedition = "2021"\n\n[lib]\npath = "src/lib.rs"\n'
SIGVERIFY_RS = ("//! The verifier as ANOTHER crate: not translated, so the model has an axiom for it.\n"
                "pub fn verify(key: u64, payload: u64, counter: u64, tag: u64) -> bool {\n"
                "    tag == (key % 16) * 256 + (payload % 16) * 16 + counter % 16\n}\n")
OBLIGATION = "Rule.intake.accept_only_if_verified.obligation"
T17_LEAN = r"""import Generated.Sigintake
import Bdd.Basic
import Bdd.AuditLinks
open Aeneas Aeneas.Std Result Lean

namespace T17

/-- The word, bound to the answer of the verifier that is NOT translated (a Lean axiom). -/
def verifies (k : sigintake.Key) (m : sigintake.Message) : Prop :=
  sigintake.sigverify.verify k.id m.payload m.counter m.tag = ok true

/-- "is accepted", as lean/Intake/Pieces.lean has it (`In.said`). -/
@[reducible] def said (r : Bool) : Prop := r = true

/-- U1 (SM-2) AS GENERATED: the text of the obligation clausal generated for the sentence (lean/Wallet/Obligations.lean,
    put here by trust/tests/test1_controls.py), with the two words rebound: `In.verifies` -> `T17.verifies`, `In.said` -> `T17.said`.
    It says that EVERY call answers, and that an accepted one verifies. NOTHING BELOW PROVES IT: a theorem `T17.U1` of this
    type is what the control asks for, and there is none. -/
def U1.generated : Prop :=
  @@OBLIGATION@@

/-- WEAKER than U1, hand-written for this control, not generated: only about the calls that DO answer. It drops the first
    half of U1 (every call answers). -/
def U1.weaker : Prop :=
  ∀ (st : sigintake.Key × sigintake.Counter) (inp : sigintake.Message) (ans : Bool) (st' : sigintake.Key × sigintake.Counter),
    sigintake.intake st.1 st.2 inp = ok (ans, st') → ans = true → verifies st.1 inp

theorem U1_weaker : U1.weaker := by
  intro st inp ans st' e ha
  unfold verifies
  unfold sigintake.intake at e
  cases h : sigintake.sigverify.verify st.1.id inp.payload inp.counter inp.tag using Result.cases with
  | ret b =>
    rw [h] at e
    cases b with
    | true => rfl
    | false => subst ha; simp at e
  | vis i k => rw [h] at e; simp at e
  | div => rw [h] at e; simp at e

/-- What U1 as generated needs and the model does not give: the external verifier returns an answer at every input. -/
def VerifierReturns : Prop :=
  ∀ (k p c t : Std.U64), ∃ b : Bool, sigintake.sigverify.verify k p c t = ok b

/-- WHY there is no `T17.U1`: U1 as generated IMPLIES that the external verifier always returns, which the axiom does not say. -/
def Needs : Prop := U1.generated → VerifierReturns

theorem needs : Needs := by
  intro h k p c t
  obtain ⟨ans, st', e, -⟩ := h (⟨k⟩, ⟨0#u64⟩) ⟨p, c, t, 0#u64⟩
  unfold sigintake.intake at e
  simp only at e
  cases hv : sigintake.sigverify.verify k p c t using Result.cases with
  | ret b => exact ⟨b, rfl⟩
  | vis i k' => rw [hv] at e; simp at e
  | div => rw [hv] at e; simp at e

end T17

open Bdd.Audit in
#eval show CoreM Unit from do
  let u1 ← theoremEntry `T17.U1 fun _ ci => ci.type == mkConst `T17.U1.generated
  let w ← theoremEntry `T17.U1_weaker fun _ ci => ci.type == mkConst `T17.U1.weaker
  let n ← theoremEntry `T17.needs fun _ ci => ci.type == mkConst `T17.Needs
  IO.println s!"T17\t{(Json.mkObj [u1, w, n]).compress}"
"""


def run(cmd, cwd, heavy=False, timeout=3600):
    if heavy:
        cmd = [str(SEM), "3", "--"] + cmd
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=ENV, timeout=timeout)
    return r.returncode, r.stdout + r.stderr


def workcopy(dest: Path):
    rc, out = run([str(ROOT / "mutation" / "workcopy.sh"), str(dest)], ROOT)
    assert rc == 0, out[-2000:]
    return dest


def lightcopy(dest: Path):
    shutil.copytree(ROOT, dest, ignore=LIGHT, symlinks=True)
    return dest


def graph(root: Path) -> dict:
    return json.loads((root / "out" / "graph.json").read_text())


def intake(g: dict) -> dict:
    """Rule node -> {code, flags, uses_verifies, assumptions} for the Rules of features/intake.feature."""
    nodes = {n["id"]: n for n in g["nodes"]}
    out = {}
    for v in g["verdicts"]:
        if v["node"].startswith("group:rule:Rule.intake."):
            rd = nodes[v["node"]]["attrs"].get("reading") or {}
            out[v["node"]] = {"code": v["code"], "outcome": v["outcome"], "flags": [f for f in v["flags"] if "ASSUM" in f],
                              "uses_verifies": any(p["id"] == "in.verifies" for p in rd.get("pieces", [])), "assumptions": rd.get("assumptions", []),
                              "rests_on": v["rests_on"]}
    return out


def assumption_item(g: dict, node: str) -> list:
    """The lines of the assumption item in the rendered block of one Rule."""
    from clausal import rules
    b = next(b for b in rules.blocks(g) if b["node"] == node)
    lines = rules.render(b)
    k = next((i for i, l in enumerate(lines) if "ASSUMED" in l), None)
    if k is None:
        return []
    out = [lines[k]]
    for l in lines[k + 1:]:
        if re.match(r"\s+\d+ \w|    -- |  Detail|\s*$", l):
            break
        out.append(l)
    return out


def mutant(cid: str, work: Path) -> dict:
    copy = workcopy(work / cid)
    lib = copy / "sigintake" / "src" / "lib.rs"
    old, new = MUTANTS[cid]
    src = lib.read_text()
    assert src.count(old) == 1
    lib.write_text(src.replace(old, new))
    unit_rc, _ = run(["cargo", "test", "--quiet"], copy / "sigintake", heavy=True)
    rc, out = run(["./run.sh", "--quick", "--no-unit"], copy, heavy=True, timeout=5400)
    (work / f"{cid}.log").write_text(out)
    res = {"change": "sigintake/src/lib.rs: " + ("the verify step deleted" if cid == "T1.1" else "verify is called with a key made from msg.hint"),
           "run": "./run.sh --quick --no-unit", "exit": rc, "unit_tests_of_the_crate_fail": unit_rc != 0,
           "result_line": next((l for l in reversed(out.splitlines()) if l.startswith("RESULT")), None)}
    if not (copy / "out" / "graph.json").exists():
        return {**res, "passed": False, "why": "the run wrote no graph", "tail": out[-1500:]}
    g, g0 = graph(copy), graph(ROOT)
    now, before = intake(g), intake(g0)
    res["codes"] = {k.split(".")[-1]: v["code"] for k, v in now.items()}
    res["codes_before"] = {k.split(".")[-1]: v["code"] for k, v in before.items()}
    flag = f"ASSUMPTION-CONDITION-NOT-MET:{A}"
    on_word = {k: v for k, v in now.items() if v["uses_verifies"]}
    res["rules_using_in.verifies"] = {k.split(".")[-1]: {"code": v["code"], "flagged": flag in v["flags"], "flags": v["flags"]} for k, v in on_word.items()}
    res["flagged_before"] = sorted(k.split(".")[-1] for k, v in before.items() if flag in v["flags"])
    item, item0 = assumption_item(g, U1), assumption_item(g0, U1)
    res["assumption_item_of_U1"] = item
    res["assumption_item_of_U1_unmutated"] = item0
    nodes = {n["id"]: n for n in g["nodes"]}
    res["counterexample_of_U1"] = (nodes[U1]["attrs"]["reading"].get("counterexample") or {})
    if cid == "T1.1":
        res["passed"] = (now[U1]["code"] == "REFUTED" and bool(on_word) and all(flag in v["flags"] for v in on_word.values())
                         and not res["flagged_before"] and item != item0 and any("REFUTED" in l for l in item))
    else:
        res["passed"] = now[U1]["code"] == "REFUTED"
    return res


def t13(work: Path) -> dict:
    copy = lightcopy(work / "T1.3")
    p = copy / "lean" / "Intake" / "Pieces.lean"
    old = "(m.payload.val % 16) * 16"
    s = p.read_text()
    assert s.count(old) == 1
    rc0, out0 = run([sys.executable, "-m", "clausal", "attest", "check"], copy)
    p.write_text(s.replace(old, "(m.payload.val % 8) * 16"))
    rc, out = run([sys.executable, "-m", "clausal", "attest", "check"], copy)
    void = [l for l in out.splitlines() if l.startswith("VOID") and "`in.verifies`" in l]
    valid_before = [l for l in out0.splitlines() if l.startswith("valid") and "piece records: reviewed by a model" in l]
    valid_after = [l for l in out.splitlines() if l.startswith("valid") and "piece records: reviewed by a model" in l]
    return {"change": "lean/Intake/Pieces.lean: `(m.payload.val % 16) * 16` -> `(m.payload.val % 8) * 16` in the definition of In.verifies",
            "command": "python3 -m clausal attest check", "exit": rc, "before": valid_before, "after": valid_after, "void": void,
            "passed": rc0 == 0 and len(valid_before) == 1 and not valid_after and len(void) == 1 and "model:claude-fable-5-2 reviewed it" in void[0]}


def t14(work: Path) -> dict:
    copy = lightcopy(work / "T1.4")
    store = copy / "clausebook" / "local" / "intake.attest.json"
    recs = json.loads(store.read_text())
    bad = json.loads(json.dumps(recs[0]))
    bad["signer"] = {"kind": "person", "id": "model:claude-fable-5-2"}
    bad["act"] = "approved"
    store.write_text(json.dumps(recs + [bad], indent=2))
    rc, out = run([sys.executable, "-m", "clausal", "attest", "check"], copy)
    refused = [l for l in out.splitlines() if l.startswith("REFUSED")]
    summary = next((l for l in out.splitlines() if l.startswith("attestation records:")), "")
    return {"change": "clausebook/local/intake.attest.json: a second record on in.verifies, act approved, signer {kind: person, id: model:claude-fable-5-2}",
            "command": "python3 -m clausal attest check", "exit": rc, "refused": refused, "summary": summary,
            "passed": rc == 1 and len(refused) == 1 and "signer kind `person` with the id `model:claude-fable-5-2`" in refused[0]
            and "entries reviewed or approved by a person: 0 of" in summary}


def t15(work: Path) -> dict:
    rc, out = run([sys.executable, "-m", "clausal", "trust", "--strict"], ROOT)
    rcj, outj = run([sys.executable, "-m", "clausal", "trust", "--json"], ROOT)
    tr = json.loads(outj)
    vs = [x for x in tr["verdicts"] if x["project"] == "sigintake"]
    owner = [u for x in vs for u in x["unmet"] if u["requirement"] in ("meaning.core", "meaning.domain") and "root `owner`" in u.get("awaited", "")]
    crypto = [u for x in vs for u in x["unmet"] if u["requirement"] == "assumption.vouch" and "root `crypto` (nobody named" in u.get("awaited", "")]
    usage = [u for x in vs for u in x["unmet"] if u["requirement"] == "assumption.usage"]
    lines = [l for l in out.splitlines() if "sigintake" in l or l.startswith("    ") and "AWAITED" in l]
    block = out[out.index("trust, project sigintake"):].splitlines()[:14] if "trust, project sigintake" in out else []
    same_policy = [l for l in (ROOT / "trust" / "sigintake.yaml").read_text().splitlines() if not l.startswith("#")] == \
                  [("project: sigintake" if l == "project: intake" else l) for l in (HERE.parent / "test1" / "intake.policy.yaml").read_text().splitlines() if not l.startswith("#")]
    return {"command": "python3 -m clausal trust --strict", "exit": rc, "proved_sigintake_verdicts": len(vs), "strict_fail": sum(x["strict"] == "fail" for x in vs),
            "awaited_owner": sorted({u["awaited"] for u in owner}), "awaited_specialist": sorted({u["awaited"] for u in crypto}),
            "assumption.usage_unmet": sorted({c for u in usage for c in u["conditions"]}), "output": block,
            "policy_is_the_frozen_one_but_for_the_project_line": same_policy,
            "passed": rc == 1 and bool(vs) and all(x["strict"] == "fail" for x in vs) and bool(owner) and bool(crypto) and same_policy}


def t16(work: Path) -> dict:
    copy = workcopy(work / "T1.6")
    led = copy / "trust" / "assumptions.yaml"
    text = led.read_text()
    k = text.index("  - id: A.sig.unforgeable")
    led.write_text(text[:k].rstrip("\n").replace("assumptions:", "assumptions: []") + "\n")
    rc, out = run([sys.executable, "-m", "clausal", "gen"], copy)
    rcb, outb = run([sys.executable, "-m", "clausal", "book", "check", "--quiet"], copy)
    rcr, outr = run(["./run.sh", "--quick"], copy, heavy=True, timeout=1800)
    steps = re.findall(r"^== (\d)[b]?/8", outr, flags=re.M)
    return {"change": "trust/assumptions.yaml: the entry A.sig.unforgeable deleted (`assumptions: []`)",
            "gen_exit": rc, "gen_says": [l for l in out.splitlines() if "in.verifies" in l or "ledger" in l][:3],
            "book_check_exit": rcb, "book_check_says": [l for l in outb.splitlines() if "in.verifies" in l][:2],
            "run_exit": rcr, "run_steps_started": steps, "run_tail": outr.splitlines()[-3:],
            "passed": rc != 0 and "in.verifies" in out and A in out and rcb != 0 and rcr != 0 and "4" not in steps}


def t17(work: Path) -> dict:
    from clausal import ledger, vreport
    copy = workcopy(work / "T1.7")
    crate = copy / "sigintake"
    (crate / "sigverify" / "src").mkdir(parents=True)
    (crate / "sigverify" / "Cargo.toml").write_text(SIGVERIFY_TOML)
    (crate / "sigverify" / "src" / "lib.rs").write_text(SIGVERIFY_RS)
    (crate / "Cargo.toml").write_text((crate / "Cargo.toml").read_text() + 'sigverify = { path = "sigverify" }\n')
    lib = crate / "src" / "lib.rs"
    s = lib.read_text()
    a, b = s.index("/// TOY: the tag"), s.index("/// Accepts a message")
    s = s[:a] + s[b:]
    assert s.count("if !verify(expected_key, msg.payload") == 1
    lib.write_text(s.replace("if !verify(expected_key, msg.payload", "if !sigverify::verify(expected_key.id, msg.payload"))
    res = {"change": "sigintake: `verify` moved to the path dependency sigintake/sigverify (not translated); intake calls sigverify::verify(expected_key.id, ...)",
           "scope": "REDUCED (trust/FREEZE-w46.md section 5): translation, one theorem, the audit, lclean and the flags; not a pipeline run"}
    rc, out = run(["./translate.sh"], copy, heavy=True)
    model = (copy / "lean" / "Generated" / "Sigintake.lean").read_text() if rc == 0 else ""
    res["translate_exit"] = rc
    res["axiom_in_model"] = [l.strip() for l in model.splitlines() if l.startswith("axiom ")]
    res["model_is_noncomputable"] = "noncomputable section" in model
    if rc != 0 or not res["axiom_in_model"]:
        return {**res, "passed": False, "why": "the variant did not translate to a model with an axiom", "tail": out[-1200:]}
    rcb, outb = run(["lake", "build", "Generated.Sigintake"], copy / "lean", heavy=True)
    # U1 AS GENERATED: the obligation clausal wrote for the sentence, with the two words of the variant in place of the tree's
    obl = (copy / "lean" / "Wallet" / "Obligations.lean").read_text().splitlines()
    k = next(i for i, l in enumerate(obl) if l.startswith(f"def {OBLIGATION} : Prop :="))
    generated = obl[k + 1].strip()
    assert "In.verifies" in generated and "In.said" in generated and "In." not in generated.replace("In.verifies", "").replace("In.said", "")
    rebound = generated.replace("In.verifies", "T17.verifies").replace("In.said", "T17.said")
    (copy / "lean" / "Run" / "T17.lean").write_text(T17_LEAN.replace("@@OBLIGATION@@", rebound))
    rcl, outl = run(["lake", "env", "lean", "Run/T17.lean"], copy / "lean", heavy=True)
    line = next((l for l in outl.splitlines() if l.startswith("T17\t")), None)
    res.update({"model_builds": rcb == 0, "lean_exit": rcl, "lean_errors": [l for l in outl.splitlines() if "error" in l][:5]})
    if line is None:
        return {**res, "passed": False, "why": "the audit printed nothing", "tail": outl[-1200:]}
    links = {"theorems": json.loads(line.split("\t", 1)[1])}
    th = links["theorems"]
    keys = ("exists", "is_theorem", "type_ok", "axioms")
    ax = "sigintake.sigverify.verify"
    led = ledger.load(ROOT)
    e = led.entries[A]
    listed = ledger.Ledger({A: {**e, "class": "opaque-function", "lean_axioms": [ax]}})
    other = ledger.Ledger({A: {**e, "class": "opaque-function", "lean_axioms": ["sigintake.some_other_axiom"]}})
    allow0, allow1, allow2 = (ledger.allowed_axioms(x, [A]) for x in (led, listed, other))

    def asked(name):
        """lclean and the flags, asked about one theorem under the three ledgers. The usage conditions have NO verdict here (no run
        on the variant: `ledger.state(e, {})`), so every flag the computation returns is listed, the condition flags included."""
        t = th[name]
        used = sorted(set(t["axioms"]) & set(allow1))
        return {"audit": {k_: t[k_] for k_ in keys},
                "with_the_ledger_as_frozen": {"lean_axioms": e["lean_axioms"], "counts": vreport.lclean(links, name, allow0),
                                              "why_not": vreport.lwhy(links, name, allow0)},
                "with_the_axiom_listed": {"lean_axioms": [ax], "counts": vreport.lclean(links, name, allow1),
                                          "why_not": None if vreport.lclean(links, name, allow1) else vreport.lwhy(links, name, allow1),
                                          "flags": ledger.flags(listed.entries[A], ledger.state(e, {}), False, used),
                                          "flags_note": "computed with no verdict for any usage condition (nothing was run on the variant): "
                                                        "ASSUMPTION-CONDITION-NOT-MET is therefore among them and says nothing about the variant"},
                "with_another_axiom_listed": {"counts": vreport.lclean(links, name, allow2)}}
    # 1. what the freeze asks for: a theorem of U1, the generated obligation
    u1 = asked("T17.U1")
    res["U1_as_generated"] = {"statement": rebound, "is": f"the body of `{OBLIGATION}` (lean/Wallet/Obligations.lean, generated) with `In.verifies` -> "
                              "`T17.verifies` (the axiom's answer) and `In.said` -> `T17.said` (the same definition)",
                              "theorem": "T17.U1", **u1,
                              "proved": bool(th["T17.U1"]["exists"] and th["T17.U1"]["is_theorem"] and th["T17.U1"]["type_ok"] and "sorryAx" not in th["T17.U1"]["axioms"])}
    # 2. why there is none: a kernel-checked theorem that U1 as generated implies the external verifier always returns
    n = th["T17.needs"]
    res["why_U1_is_not_proved"] = {"theorem": "T17.needs : U1.generated → ∀ k p c t, ∃ b, sigintake.sigverify.verify k p c t = ok b",
                                   "audit": {k_: n[k_] for k_ in keys},
                                   "kernel_checked": bool(n["exists"] and n["is_theorem"] and n["type_ok"] and "sorryAx" not in n["axioms"]),
                                   "says": "U1 as generated says every call answers. Of the variant that needs the external verifier to return at every input; "
                                           "the model's axiom gives it a type and nothing else. No proof of U1 was found. That none exists without a second "
                                           "assumed fact (the verifier returns) is an argument from this theorem, not itself a theorem"}
    # 3. what WAS shown, on a statement that is not U1
    w = asked("T17.U1_weaker")
    tw = th["T17.U1_weaker"]
    shown = bool(tw["exists"] and tw["is_theorem"] and tw["type_ok"] and ax in tw["axioms"] and "sorryAx" not in tw["axioms"]
                 and not w["with_the_ledger_as_frozen"]["counts"] and "non-standard axioms" in w["with_the_ledger_as_frozen"]["why_not"]
                 and w["with_the_axiom_listed"]["counts"] and f"ASSUMPTION-AXIOM-USED:{A}" in w["with_the_axiom_listed"]["flags"]
                 and not w["with_another_axiom_listed"]["counts"])
    res["weaker_statement"] = {"statement": "T17.U1.weaker: ∀ st inp ans st', sigintake.intake st.1 st.2 inp = ok (ans, st') → ans = true → T17.verifies st.1 inp",
                               "is": "HAND-WRITTEN in this script, NOT generated, and WEAKER than U1: only the calls that answer. `type_ok` compares the theorem "
                                     "with this same hand-written statement, so it says only that the theorem is of the type the script wrote",
                               "theorem": "T17.U1_weaker", **w, "shown": shown,
                               "shows_only": "the audit reports the model's axiom, and `lclean` rejects a theorem that uses it while the ledger lists no axiom, "
                                             "admits it once the entry lists that axiom (flag ASSUMPTION-AXIOM-USED), and rejects it when the entry lists another"}
    # what the whole pipeline does with the variant: it is expected to stop (the search cannot evaluate an axiom)
    rcr, outr = run(["./run.sh", "--quick", "--no-unit"], copy, heavy=True, timeout=2400)
    steps = re.findall(r"^== (\d)[b]?/8", outr, flags=re.M)
    res["pipeline_on_the_variant"] = {"exit": rcr, "steps_started": steps, "stopped_with": [l for l in outr.splitlines() if "error" in l.lower() or "FAILED" in l][:4]}
    # Passed as frozen (FREEZE-w46.md section 5; W0: "PROVED with the flag once the axiom is listed") iff U1 ITSELF has a theorem that does not
    # count with `lean_axioms: []` and counts, flagged, with the axiom listed. A theorem of a weaker statement does not make it pass.
    res["passed"] = bool(res["U1_as_generated"]["proved"] and ax in th["T17.U1"]["axioms"] and not u1["with_the_ledger_as_frozen"]["counts"]
                         and u1["with_the_axiom_listed"]["counts"] and f"ASSUMPTION-AXIOM-USED:{A}" in u1["with_the_axiom_listed"]["flags"]
                         and not u1["with_another_axiom_listed"]["counts"])
    res["shown_on_a_weaker_statement_only"] = bool(shown and not res["passed"])
    if not res["passed"]:
        res["why"] = ("U1 as generated is not proved of the variant, with or without the axiom listed" + (
            "; what the control shows is only that the allow-list admits a listed axiom, on a hand-written statement weaker than U1" if shown else ""))
    return res


def sign_off_counts() -> dict:
    """Counts against (W0): the model record appears in any count labelled sign-off. Read from the graph and the blocks of the tree's run."""
    from clausal import rules
    g = graph(ROOT)
    nodes = {n["id"]: n for n in g["nodes"]}
    piece = nodes["piece:in.verifies"]["attrs"]
    rd = [n["attrs"]["reading"] for n in g["nodes"] if n["id"].startswith("group:rule:Rule.intake.") and (n["attrs"].get("reading") or {}).get("compiled")]
    signed = sum(bool(p.get("signed")) for r in rd for p in r["pieces"])
    blocks = {b["node"]: "\n".join(rules.render(b)) for b in rules.blocks(g) if b["node"].startswith("group:rule:Rule.intake.")}
    lines = [l.strip() for l in blocks[U1].splitlines() if "Clausebook pieces" in l or "carry a record by a model" in l]
    unrev = [v for v in g["verdicts"] if v["node"] in blocks and v["code"].startswith("PROVED") and "piece:in.verifies" not in v["unreviewed"]
             and any(p["id"] == "in.verifies" for p in nodes[v["node"]]["attrs"]["reading"]["pieces"])]
    report = (ROOT / "out" / "report.md").read_text()
    return {"records_on_in.verifies": [{k: a[k] for k in ("act", "kind", "by", "evidence_kind")} for a in piece["attestations"]],
            "pieces_marked_signed_in_intake_readings": signed, "meaning_lines_of_U1": lines,
            "proved_rules_on_in.verifies_that_do_not_list_it_unreviewed": len(unrev),
            "in_no_sign_off_count": signed == 0 and not unrev and any("0 signed" in l for l in lines)
            and [a["kind"] for a in piece["attestations"]] == ["model"] and "| in.verifies |" in report}


CONTROLS = {"T1.1": lambda w: mutant("T1.1", w), "T1.2": lambda w: mutant("T1.2", w), "T1.3": t13, "T1.4": t14, "T1.5": t15, "T1.6": t16, "T1.7": t17}


def main(argv) -> int:
    # the scratch copies are made OUTSIDE the tree (a copy of the tree inside the tree would copy itself)
    import hashlib
    work = (Path(argv[argv.index("--work") + 1]) if "--work" in argv
            else Path(tempfile.gettempdir()) / f"clausal-test1-{hashlib.sha1(str(ROOT).encode()).hexdigest()[:8]}")
    work.mkdir(parents=True, exist_ok=True)
    if "--collect" in argv:
        res = {c: json.loads((work / f"{c}.json").read_text()) for c in CONTROLS if (work / f"{c}.json").exists()}
        # an earlier round on an earlier tree, kept as <work>/first/<id>.json: reported beside the result, never in place of it
        first = {c: json.loads((work / "first" / f"{c}.json").read_text()) for c in CONTROLS if (work / "first" / f"{c}.json").exists()}
        prev_path = HERE / "test1_controls.result.json"
        prev = json.loads(prev_path.read_text()) if prev_path.exists() else {}
        commit = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        out = {"what": "trust test 1 (plan node W6): the seven controls of trust/test1/controls.yaml, run by trust/tests/test1_controls.py",
               "tree": commit, "controls": res, "passed": sorted(c for c, r in res.items() if r["passed"]),
               "not_passed": sorted(c for c, r in res.items() if not r["passed"]), "not_run": sorted(set(CONTROLS) - set(res)),
               "model_record_and_sign_off_counts": sign_off_counts(),
               "first_round": {"what": "the same controls as first run, on the tree of commit ac2dfbe (before the step lemma of `verify` was "
                                       "registered, lean/Intake/Lemmas/Verify.lean): kept whatever they said",
                               "passed": sorted(c for c, r in first.items() if r["passed"]), "not_passed": sorted(c for c, r in first.items() if not r["passed"]),
                               "controls": {c: r for c, r in first.items() if not r["passed"]}} if first else prev.get("first_round")}
        weaker = sorted(c for c, r in res.items() if r.get("shown_on_a_weaker_statement_only"))
        out["shown_on_a_weaker_statement_only"] = weaker
        # what an earlier collect said of T1.7 under a criterion that compared a hand-written weaker statement with itself
        old17 = prev.get("T1.7_as_first_reported") or ({"tree": prev.get("tree"), "reported": "passed", "result": prev["controls"]["T1.7"],
                                                         "withdrawn": "the theorem that counted was of a hand-written statement weaker than U1 (only the calls "
                                                                      "that answer) and its `type_ok` compared it with that same statement; it was not a theorem of U1"}
                                                        if prev.get("controls", {}).get("T1.7", {}).get("passed") and "audit" in prev["controls"]["T1.7"] else None)
        if old17:
            out["T1.7_as_first_reported"] = old17
        (HERE / "test1_controls.result.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
        for c in CONTROLS:
            print(f"  {c}  " + ("not run" if c not in res else "passed" if res[c]["passed"] else "NOT PASSED" + (f": {res[c]['why']}" if res[c].get("why") else "")))
        print(f"{len(out['passed'])} of {len(CONTROLS)} controls passed; the model record is in no sign-off count: {out['model_record_and_sign_off_counts']['in_no_sign_off_count']}")
        return 0 if len(out["passed"]) == len(CONTROLS) and out["model_record_and_sign_off_counts"]["in_no_sign_off_count"] else 1
    if not (ROOT / "out" / "graph.json").exists():
        print("out/graph.json is missing: run ./run.sh --quick first")
        return 2
    only = argv[argv.index("--only") + 1].split(",") if "--only" in argv else list(CONTROLS)
    bad = 0
    for c in only:
        for stale in (work / c, work / f"{c}.json"):
            if stale.is_dir():
                shutil.rmtree(stale)
            elif stale.exists():
                stale.unlink()
        r = CONTROLS[c](work)
        (work / f"{c}.json").write_text(json.dumps(r, indent=1, ensure_ascii=False) + "\n")
        print(f"  {c}  {'passed' if r['passed'] else 'NOT PASSED' + (': ' + r['why'] if r.get('why') else '')}")
        bad += not r["passed"]
        if "--keep" not in argv and (work / c).is_dir():
            shutil.rmtree(work / c)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
