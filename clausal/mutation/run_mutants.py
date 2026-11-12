#!/usr/bin/env python3
"""Mutation test of the scenario layer, and negative controls for the pipeline's own checks.

    python3 mutation/run_mutants.py [--jobs N] [--only ID,ID] [--keep] [--resummarise]
    python3 mutation/run_mutants.py --before-review      the same mutants against the scenario set as it was before
                                                         the four scenarios added after the review (no controls);
                                                         writes mutation/results-before-review.{json,md} instead

Each MUTANT is one small wrong change to wallet/src/lib.rs or ledger/src/lib.rs (ids starting with
`l`; they include loop bugs: off-by-one bound, wrong accumulator, missing early exit, skipped
element). It is applied in a scratch copy of clausal/
(mutation/workcopy.sh; the real tree is never touched), the crate's own unit tests are run, and then
the whole pipeline is run WITHOUT those unit tests (`./run.sh --no-unit`), so the question answered is:
do the scenarios, on their own, notice? TWO answers are recorded, and they are not the same thing:

  shown false   a scenario is SHOWN FALSE of the mutant: an Examples row (or a literal scenario) gives a different
                result on the compiled Rust, or the grid search finds a counterexample to a scenario statement.
                This is what the scenarios detect.
  run fails     `./run.sh` exits non-zero. This also happens when nothing is shown false and only a hand-written
                proof or lemma stops compiling. A lemma can be stronger than every scenario, and a lost proof can
                be won back by re-proving against the changed code (the review did exactly that for mutant r3), so
                "the run fails" on its own is NOT counted as detection by the scenarios.

Each CONTROL is a deliberately wrong change to something other than the Rust (a proof, the glossary,
the Rust reading of a phrase, the scenario set) and states what the pipeline is expected to say.

Writes mutation/results.json (read by `clausal report`) and mutation/results.md.
Took about 16 minutes with 8 jobs on a warm, otherwise idle machine when there were 61 pipeline runs; there are 73 now
(45 mutants without the suite adequacy note and the held-out sentences, the baseline and 27 controls with them), and
each run also compiles the readings, searches them and checks the glue (lean/Run/ReadingSearch.lean, Links.lean).

Since the composable Clausebook (plan nodes V2, V3) each mutant also records `rules_changed` / `rule_shown_false`: the
statements compiled from the `Rule:` lines whose verdict changed, and those found false (by the reading search; REFUTED
if confirmed in the kernel). They are reported BESIDE the scenario columns and are not part of "a scenario is shown
false", which means what it meant before.

For each mutant the result records three separate layers:
  rows_on_rust   an Examples row (or a literal scenario) gives a different result on the compiled Rust
  proof_broke    a scenario that was PROVED is no longer proved (its proof, or a lemma it uses, fails)
  search_found   the boundary-grid search on the Lean model finds a counterexample that was not there
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLICE = HERE.parent
sys.path.insert(0, str(SLICE))
from clausal.core import without_scenarios  # noqa: E402
from clausal.pipeline import spec_digest  # noqa: E402

DEPOSIT, WITHDRAW, TRANSFER = "wallet::{wallet::Wallet}::deposit", "wallet::{wallet::Wallet}::withdraw", "wallet::transfer"

# (id, function, what was changed, old text, new text) on wallet/src/lib.rs; old must occur exactly once
MUTANTS = [
    ("d1", DEPOSIT, "no overflow check: the balance wraps around",
     """        match self.balance.checked_add(amt) {
            Some(b) => {
                self.balance = b;
                Ok(())
            }
            None => Err(WalletError::Overflow),
        }""",
     """        self.balance = self.balance.wrapping_add(amt);
        Ok(())"""),
    ("d2", DEPOSIT, "a successful deposit sets the balance to the amount instead of adding it",
     "                self.balance = b;", "                let _ = b; self.balance = amt;"),
    ("d3", DEPOSIT, "overflow is reported as insufficient funds",
     "            None => Err(WalletError::Overflow),", "            None => Err(WalletError::InsufficientFunds),"),
    ("d4", DEPOSIT, "a deposit that reaches exactly the maximum is rejected",
     """            Some(b) => {
                self.balance = b;
                Ok(())
            }
            None => Err(WalletError::Overflow),""",
     """            Some(b) => {
                if b == u64::MAX {
                    return Err(WalletError::Overflow);
                }
                self.balance = b;
                Ok(())
            }
            None => Err(WalletError::Overflow),"""),
    ("d5", DEPOSIT, "a rejected deposit empties the wallet",
     "            None => Err(WalletError::Overflow),",
     """            None => {
                self.balance = 0;
                Err(WalletError::Overflow)
            }"""),
    ("d6", DEPOSIT, "a deposit of exactly 1000003 credits one unit too few (wrong only at an input no example or grid point uses)",
     "                self.balance = b;",
     "                self.balance = if amt == 1_000_003 { b - 1 } else { b };"),
    ("w1", WITHDRAW, "withdrawing the whole balance is rejected (> became >=)",
     "        if amt > self.balance {", "        if amt >= self.balance {"),
    ("w2", WITHDRAW, "a successful withdrawal does not take the money",
     "        self.balance -= amt;\n        Ok(())", "        Ok(())"),
    ("w3", WITHDRAW, "insufficient funds is reported as overflow",
     "        if amt > self.balance {\n            return Err(WalletError::InsufficientFunds);",
     "        if amt > self.balance {\n            return Err(WalletError::Overflow);"),
    ("w4", WITHDRAW, "a rejected withdrawal empties the wallet",
     "        if amt > self.balance {\n            return Err(WalletError::InsufficientFunds);",
     "        if amt > self.balance {\n            self.balance = 0;\n            return Err(WalletError::InsufficientFunds);"),
    ("w5", WITHDRAW, "a successful withdrawal takes one unit too many when it can",
     "        self.balance -= amt;\n        Ok(())",
     "        self.balance -= amt;\n        if self.balance > 0 {\n            self.balance -= 1;\n        }\n        Ok(())"),
    ("t1", TRANSFER, "transferring the whole balance is rejected (< became <=)",
     "    if src.balance < amt {", "    if src.balance <= amt {"),
    ("t2", TRANSFER, "the sender is debited before the receiver's overflow check, so a rejected transfer loses money",
     """    let nb = match dst.balance.checked_add(amt) {
        Some(b) => b,
        None => return Err(WalletError::Overflow),
    };
    src.balance -= amt;""",
     """    src.balance -= amt;
    let nb = match dst.balance.checked_add(amt) {
        Some(b) => b,
        None => return Err(WalletError::Overflow),
    };"""),
    ("t3", TRANSFER, "the receiver is never credited (money vanishes)",
     "    src.balance -= amt;\n    dst.balance = nb;", "    src.balance -= amt;\n    let _ = nb;"),
    ("t4", TRANSFER, "the sender is never debited (money is created)",
     "    src.balance -= amt;\n    dst.balance = nb;", "    dst.balance = nb;"),
    ("t5", TRANSFER, "receiver overflow is reported as insufficient funds",
     "        None => return Err(WalletError::Overflow),", "        None => return Err(WalletError::InsufficientFunds),"),
    ("t6", TRANSFER, "insufficient funds is reported as overflow",
     "    if src.balance < amt {\n        return Err(WalletError::InsufficientFunds);",
     "    if src.balance < amt {\n        return Err(WalletError::Overflow);"),
    ("t7", TRANSFER, "no funds check at all (the subtraction panics instead)",
     "    if src.balance < amt {\n        return Err(WalletError::InsufficientFunds);\n    }\n", ""),
]

L = "ledger::{ledger::Ledger}::"
L_TOTAL, L_APPLY, L_BATCH, L_ALL, L_BALANCE = L + "total", L + "apply", L + "apply_batch", L + "apply_all", L + "balance"

# the same, on ledger/src/lib.rs
LEDGER_MUTANTS = [
    ("lt1", L_TOTAL, "LOOP off-by-one bound: the last balance is not added",
     "        while i < self.balances.len() {", "        while i + 1 < self.balances.len() {"),
    ("lt2", L_TOTAL, "LOOP wrong accumulator: the sum is overwritten by each balance instead of accumulated",
     "                Some(s) => s,", "                Some(_) => self.balances[i],"),
    ("lt3", L_TOTAL, "LOOP skipped element: summing starts at account 1",
     "        let mut sum: u64 = 0;\n        let mut i = 0;", "        let mut sum: u64 = 0;\n        let mut i = 1;"),
    ("lt4", L_TOTAL, "an overflowing total is reported as u64::MAX instead of absent",
     "                None => return None,", "                None => return Some(u64::MAX),"),
    ("lt5", L_TOTAL, "LOOP wrong accumulator: wrapping addition, so an overflowing total wraps around",
     """            sum = match sum.checked_add(self.balances[i]) {
                Some(s) => s,
                None => return None,
            };""", "            sum = sum.wrapping_add(self.balances[i]);"),
    ("la1", L_APPLY, "no check that sender and receiver differ: a self-transfer creates money",
     "        if t.from >= n || t.to >= n || t.from == t.to {", "        if t.from >= n || t.to >= n {"),
    ("la2", L_APPLY, "transferring the sender's whole balance is rejected (< became <=)",
     "        if f < t.amount {", "        if f <= t.amount {"),
    ("la3", L_APPLY, "the receiver is never credited (money vanishes)",
     "        self.balances[t.to] = nb;", "        let _ = nb;"),
    ("la4", L_APPLY, "the sender is never debited (money is created)",
     "        self.balances[t.from] = f - t.amount;", "        let _ = f - t.amount;"),
    ("la5", L_APPLY, "receiver bounds check off by one (>= became >): indexing one past the end panics",
     "t.to >= n ||", "t.to > n ||"),
    ("la6", L_APPLY, "a transfer of exactly 1000003 credits one unit too few (wrong only at an input no example or grid point uses)",
     "        self.balances[t.to] = nb;", "        self.balances[t.to] = if t.amount == 1_000_003 { nb - 1 } else { nb };"),
    ("lb1", L_BATCH, "LOOP missing early exit: the batch carries on after a rejected transfer and counts it",
     """            if !self.apply(&batch[i]) {
                break;
            }""", "            self.apply(&batch[i]);"),
    ("lb2", L_BATCH, "LOOP off-by-one bound: the last transfer of the batch is never applied",
     "        while i < batch.len() {", "        while i + 1 < batch.len() {"),
    ("lb3", L_BATCH, "LOOP skipped element: every second transfer is skipped (i += 2)",
     "            i += 1;\n        }\n        i\n", "            i += 2;\n        }\n        i\n"),
    ("lb4", L_BATCH, "LOOP wrong result: the batch length is returned instead of the number applied",
     "            i += 1;\n        }\n        i\n", "            i += 1;\n        }\n        batch.len()\n"),
    ("lb5", L_BATCH, "LOOP wrong counter: a rejected transfer is counted as applied",
     """            if !self.apply(&batch[i]) {
                break;
            }""", """            if !self.apply(&batch[i]) {
                i += 1;
                break;
            }"""),
    ("lb6", L_BATCH, "LOOP wrong early exit: the batch stops after the first APPLIED transfer",
     """            if !self.apply(&batch[i]) {
                break;
            }
            i += 1;""", """            if !self.apply(&batch[i]) {
                break;
            }
            i += 1;
            break;"""),
    ("lw1", L_ALL, "no rollback: a rejected batch keeps the transfers applied before the failure",
     "            self.balances = saved;", "            let _ = saved;"),
    ("lw2", L_ALL, "a rolled-back batch is reported as applied",
     "            self.balances = saved;\n            return false;", "            self.balances = saved;\n            return true;"),
    ("lw3", L_ALL, "every batch is rolled back and rejected (< became <=)",
     "        if applied < batch.len() {", "        if applied <= batch.len() {"),
    ("lg1", L_BALANCE, "lookup bounds check off by one (< became <=): looking up account `len` panics",
     "        if i < self.balances.len() {", "        if i <= self.balances.len() {"),
    ("lg2", L_BALANCE, "lookup returns the balance of account 0 whatever the account",
     "            Some(self.balances[i])", "            Some(self.balances[0])"),
    # The five mutants of the adversarial review (review/loops/): aimed at what the scenario set of that time left
    # open. Three need a third loop iteration or a fourth account, one breaks atomicity, one miscounts.
    ("r1", L_BATCH, "REVIEW LOOP cap: the batch silently stops after three transfers",
     "        while i < batch.len() {", "        while i < batch.len() && i < 3 {"),
    ("r2", L_TOTAL, "REVIEW LOOP cap: only the first three accounts are summed",
     "        while i < self.balances.len() {", "        while i < self.balances.len() && i < 3 {"),
    ("r3", L_ALL, "REVIEW atomicity: no rollback once two or more transfers have been applied",
     "            self.balances = saved;", "            if applied < 2 {\n                self.balances = saved;\n            }"),
    ("r4", L_BATCH, "REVIEW LOOP wrong counter: a rejected LAST transfer (not the first) is counted as applied",
     """            if !self.apply(&batch[i]) {
                break;
            }""", """            if !self.apply(&batch[i]) {
                if i > 0 && i + 1 == batch.len() {
                    i += 1;
                }
                break;
            }"""),
    ("r5", L_BATCH, "REVIEW LOOP state corruption: one unit is minted to account 0 at the start of the third iteration "
                    "(conservation is false, but only for batches whose first two transfers apply and that have a third)",
     "        while i < batch.len() {\n            if !self.apply(&batch[i]) {",
     "        while i < batch.len() {\n            if i == 2 && self.balances[0] < u64::MAX {\n                self.balances[0] += 1;\n            }\n            if !self.apply(&batch[i]) {"),
]

PROOF = "lean/Wallet/Proofs/wallet/transfer_conserves.lean"


def sub(path, old, new, count=1):
    def f(root: Path):
        p = root / path
        s = p.read_text()
        assert s.count(old) == count, f"{path}: expected {count} occurrence(s) of {old!r}, found {s.count(old)}"
        p.write_text(s.replace(old, new))
    return f


def shipped_wallet(old, new):
    """The Rust-side crates (wallet-bdd, evidence) are built against a changed COPY of the wallet; the translation is not."""
    def f(root: Path):
        import shutil
        dst = root / "wallet-shipped"
        shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(root / "wallet", dst, ignore=shutil.ignore_patterns("target"))
        lib = dst / "src" / "lib.rs"
        s = lib.read_text()
        assert s.count(old) == 1
        lib.write_text(s.replace(old, new))
        for cargo, frm, to in (("wallet-bdd/Cargo.toml", 'path = "../wallet"', 'path = "../wallet-shipped"'),
                               ("evidence/Cargo.toml", 'path = "../wallet"', 'path = "../wallet-shipped"'),
                               ("evidence/kani/Cargo.toml", 'path = "../../wallet"', 'path = "../../wallet-shipped"')):
            p = root / cargo
            t = p.read_text()
            assert t.count(frm) == 1, cargo
            p.write_text(t.replace(frm, to))
    return f


def retheorem(path, name, new_decl):
    def f(root: Path):
        p = root / path
        s = p.read_text()
        i = s.index(f"theorem {name} :")
        p.write_text(s[:i] + new_decl + "\n")
    return f


def drop_scenarios(feature, names):
    """Remove the named scenarios (and their proof files) from features/<feature>.feature, wherever they sit
    (under a Rule or not). The Rules themselves stay."""
    def f(root: Path):
        p = root / f"features/{feature}.feature"
        p.write_text(without_scenarios(p, f"features/{feature}.feature", names))
        for n in names:
            (root / f"lean/Wallet/Proofs/{feature}/{n}.lean").unlink()
    return f


drop_new_scenarios = drop_scenarios("wallet", ("withdraw_covered", "deposit_with_room", "transfer_short", "transfer_no_room"))


def signed(then=None):
    """Sign off the whole glossary as a test reviewer (in the scratch copy only), then optionally patch."""
    def f(root: Path):
        r = subprocess.run([sys.executable, "-m", "clausal", "review", "all", "--reviewer", "test-reviewer"],
                           cwd=root, capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr
        if then:
            then(root)
    return f


# (id, what is wrong, patch, extra run.sh args, expected exit status, regexes that must all appear in the output)
CONTROLS = [
    ("c1", "a 'proof' whose type is True instead of the scenario's statement",
     retheorem(PROOF, "Spec.wallet.transfer_conserves", "theorem Spec.wallet.transfer_conserves : True := by\n  trivial"),
     [], 1, [r"TESTED-ONLY  A covered transfer", r"its type is NOT `Spec\.wallet\.transfer_conserves\.stmt`"]),
    ("c2", "a proof replaced by sorry",
     retheorem(PROOF, "Spec.wallet.transfer_conserves",
               "theorem Spec.wallet.transfer_conserves : Spec.wallet.transfer_conserves.stmt := by\n  sorry"),
     [], 1, [r"TESTED-ONLY  A covered transfer", r"proof incomplete \(sorry\)"]),
    ("c3", "one proof that does not compile: only its own scenario should lose its proof",
     retheorem("lean/Wallet/Proofs/wallet/withdraw_too_much.lean", "Spec.wallet.withdraw_too_much",
               "theorem Spec.wallet.withdraw_too_much : Spec.wallet.withdraw_too_much.stmt := by\n  exact this_does_not_exist"),
     [], 1, [r"TESTED-ONLY  Withdrawing more than the balance", r"the proof does not compile",
             # the order of the tally follows the order of the scenarios in the feature files, so each count is matched on its own
             r"39 scenarios: [^\n]*\b26 PROVED-FOR-ALL\b", r"39 scenarios: [^\n]*\b1 TESTED-ONLY\b", r"39 scenarios: [^\n]*\b6 PROVED-INSTANCE\b"]),
    ("c4", "glossary: 'decreased by <amount>' weakened so it no longer mentions the amount (proofs still compile)",
     sub("lean/Wallet/Vocab.lean", "post.balance.val + n.val = pre.balance.val", "post.balance.val ≤ pre.balance.val"),
     [], 1, [r"READINGS DISAGREE: .*T-dec", r"the two readings of glossary entry T-dec disagree"]),
    ("c5", "glossary: 'does not exceed the maximum' silently narrowed to amounts up to a million (proofs still compile)",
     sub("lean/Wallet/Vocab.lean", "w.balance.val + n.val ≤ U64.max", "w.balance.val + n.val ≤ U64.max ∧ n.val ≤ 1000000"),
     [], 1, [r"READINGS DISAGREE: .*G-room", r"the two readings of glossary entry G-room disagree"]),
    ("c6", "glossary: 'is not more than' reversed in the Lean definition",
     sub("lean/Wallet/Vocab.lean", "n.val ≤ w.balance.val", "w.balance.val ≤ n.val"),
     [], 1, [r"the two readings of glossary entry G-covers disagree"]),
    ("c7", "the Rust reading of 'is not more than' made strict (the Lean definition is untouched)",
     sub("wallet-bdd/src/lib.rs", "    n <= pre\n", "    n < pre\n"),
     [], 1, [r"READINGS DISAGREE: .*G-covers"]),
    # CHANGED with the composable Clausebook (expected exit 0 before): the Rule lines are now compiled to statements that cover
    # every input and are proved FROM the scenarios. With four scenarios gone, three rule statements lose their proof, and
    # the run fails. The original expectations (inputs no longer covered; the run says so) are kept.
    ("c8", "the four scenarios added after the review are removed: inputs are no longer covered, and the run says so; "
           "the rule statements that were proved from those scenarios are no longer proved, and the run fails",
     drop_new_scenarios, [], 1,
     [r"wallet\.Wallet\.deposit: NOT SHOWN", r"wallet\.Wallet\.withdraw: NOT SHOWN", r"wallet\.transfer: NOT SHOWN",
      r"Rule \"A transfer never changes the total of all balances\" [^\n]*TESTED-ONLY   <-- EXPECTED PROVED-FOR-ALL",
      r"35 scenarios: [^\n]*\b23 PROVED-FOR-ALL\b"]),
    ("c9", "--strict on the unchanged tree: proved scenarios rest on a glossary nobody has signed off",
     lambda root: None, ["--strict"], 1, [r"--strict: rests on \d+ glossary entries with no valid sign-off"]),
    ("c10", "not a fault: every glossary entry signed off by a test reviewer, then --strict; the run should pass",
     signed(), ["--strict"], 0, [r"human-asserted   6 of 6 glossary phrases signed off", r"RESULT: every scenario got its expected verdict"]),
    ("c11", "signed off, then the text of one definition is edited (same meaning): that sign-off is void",
     signed(sub("lean/Wallet/Vocab.lean", "o = .Ok ()", "o = core.result.Result.Ok ()")), ["--strict"], 1,
     [r"UNREVIEWED: .*T-ok", r"--strict: rests on 1 glossary entries with no valid sign-off"]),
    ("c12", "the shared hand-written lemma module does not compile: every ledger proof that depends on it is lost; the wallet's proofs and the lookup proofs are not",
     sub("lean/Ledger/Lemmas/Basic.lean", "theorem sum_take_le (L : List Nat) (i : Nat) : (L.take i).sum ≤ L.sum := by",
         "theorem sum_take_le (L : List Nat) (i : Nat) : (L.take i).sum ≤ L.sum := by\n  exact this_does_not_exist"),
     [], 1, [r"DOES NOT COMPILE: Ledger\.Lemmas\.Basic", r"PROVED-FOR-ALL  A covered transfer moves the money",
             r"TESTED-ONLY  Applying any batch of transfers conserves", r"it depends on Ledger\.Lemmas\.Basic, which does not compile",
             r"PROVED-FOR-ALL  Looking up an existing account gives its balance"]),
    ("c13", "ledger glossary: `valid` in Lean no longer requires sender and receiver to differ (the Rust reading still does)",
     sub("lean/Ledger/Vocab.lean", "t.to.val < l.balances.val.length ∧ t.from.val ≠ t.to.val ∧", "t.to.val < l.balances.val.length ∧"),
     [], 1, [r"READINGS DISAGREE: .*LG-valid", r"the two readings of glossary entry LG-first-invalid disagree"]),
    ("c14", "multi-step scenario whose Then is about the wrong When's kind of result: rejected, not mis-translated",
     sub("features/ledger.feature", "      And the total of ledger Main is computed\n      Then the result is <sum>",
         "      And the total of ledger Main is computed\n      Then the number of transfers applied is zero"),
     [], 1, [r"UNSUPPORTED  The total computed after any batch", r"E_TYPE .*speaks about a result of type `Usize`, but the last When returns `Option U64`"]),
    ("c15", "the batch loop's invariant weakened in its lemma module: the lemma no longer proves, the batch scenarios lose their proofs, the total's do not",
     sub("lean/Ledger/Lemmas/Batch.lean", "  LVocab.total p.1 = LVocab.total l0 ∧ p.2.val ≤ batch.val.length ∧\n  (p.2.val = 0 → p.1 = l0)",
         "  True ∧ p.2.val ≤ batch.val.length ∧\n  (p.2.val = 0 → p.1 = l0)"),
     [], 1, [r"DOES NOT COMPILE: Ledger\.Lemmas\.Batch", r"TESTED-ONLY  Applying any batch of transfers conserves",
             r"PROVED-FOR-ALL  The total is the sum of the balances when that fits"]),
    # ---- Gherkin `Rule:` and the suite adequacy note (added with plan node F1). The note is informational: none of
    # ---- these may change the exit status through the note itself.
    ("c16", "suite adequacy: the progress scenario of the batch suite is removed; the suite must be reported as still allowing "
            "a batch function that applies nothing (reject-all), and the run must still pass",
     drop_scenarios("ledger", ("batch_stops_at_invalid",)), [], 0,
     [r"ledger\.Ledger\.apply_batch: rules out: [^\n]*still allows: reject-all: always answers `0` and leaves the state as it was",
      r"RESULT: every scenario got its expected verdict"]),
    ("c17", "suite adequacy: the progress scenario of the withdrawal rule is removed; the suite must be reported as still allowing "
            "a withdraw that always answers insufficient funds, and (kernel-checked) as satisfied by it",
     # CHANGED with the composable Clausebook (expected exit 0 before): the withdrawal Rule line is now a statement proved
     # from its scenarios; without the progress scenario it is no longer proved, and the run fails. The note is unchanged.
     drop_scenarios("wallet", ("withdraw_covered",)), [], 1,
     [r"wallet\.Wallet\.withdraw: rules out: [^\n]*still allows: reject-all \(1 of 2 variants\): always answers `insufficient funds` "
      r"and leaves the state as it was \[proved to satisfy every scenario counted\]",
      r"wallet\.Wallet\.withdraw: NOT SHOWN",
      r"Rule \"A withdrawal always answers, and a successful withdrawal decreases[^\n]*TESTED-ONLY   <-- EXPECTED PROVED-FOR-ALL"]),
    ("c18", "not a fault: the unchanged tree. A suite that has its progress scenario must NOT be reported as allowing a trivial "
            "implementation; the one known gap (apply_all has no universal progress scenario) must be reported; exit 0",
     lambda root: None, [], 0,
     [r"ledger\.Ledger\.apply_batch: rules out: reject-all, no-op, identity, constant; still allows: \(none found\)",
      r"wallet\.transfer: rules out: reject-all, no-op, identity, constant; still allows: \(none found\)",
      r"ledger\.Ledger\.apply_all: rules out: no-op, constant; still allows: reject-all: always answers `false`",
      r"Suite     suite rules out: reject-all, no-op, identity, constant; still allows: \(none found\)"]),
    ("c19", "suite adequacy: a trivial model in the glossary is ill-typed, so the adequacy script fails; the note must say it "
            "was not computed and every verdict and the exit status must be as on the unchanged tree",
     sub("glossary.yaml", "lean: 'fun l b => ok (Slice.len b, l)'", "lean: 'fun l b => ok (l, Slice.len b)'"), [], 0,
     [r"not computed: the adequacy search produced no result", r"39 scenarios: 27 PROVED-FOR-ALL, 6 PROVED-INSTANCE, 4 REFUTED, 1 UNBOUND, 1 VACUOUS",
      r"RESULT: every scenario got its expected verdict"]),
    ("c20", "Rule tags: @expect-refuted is removed from the Rule line above the deliberately false transfer scenario; the scenario "
            "no longer inherits it, so its REFUTED verdict is no longer the expected one",
     sub("features/wallet.feature",
         "  @expect-refuted @id:transfer_affordable\n  Rule: A transfer for which the amount is not more than the sender's balance is always accepted",
         "  @id:transfer_affordable\n  Rule: A transfer for which the amount is not more than the sender's balance is always accepted"),
     [], 1, [r"REFUTED  A transfer the sender can afford always succeeds [^\n]*<-- EXPECTED PROVED-FOR-ALL",
             r"Rule \"A transfer for which the amount is not more than the sender's balance is always accepted\" [^\n]*REFUTED   <-- EXPECTED PROVED-FOR-ALL"]),
    # ---- the composable Clausebook (plan nodes V2, V3): frames, pieces, readings, Rule statements
    ("c21", "frame library: the DEFINITION of a frame is weakened (`decreases by` no longer mentions the amount; the executable reading is "
            "untouched). The readings that use it are no longer equivalent to their old statements, and the two readings of the frame differ",
     sub("lean/Frames/Frames.lean", "op.HoldsAt (fun s a _ s' => m s' a + f s a = m s a) s a", "op.HoldsAt (fun s a _ s' => m s' a ≤ m s a) s a"),
     # (The covered-TRANSFER scenario keeps its equivalence: its other Thens, "Bob's balance is increased by" and "the total is
     # unchanged", imply the exact decrease. Seen in the first run of this control; the withdrawal has no such redundancy.)
     [], 1, [r"UNLINKED  A covered withdrawal succeeds and takes exactly the amount",
             r"NOT LINKED       the reading compiled from the Clausebook is NOT proved equivalent",
             r"FRAME READINGS DISAGREE", r"PROVED-FOR-ALL  Transferring more than the sender has is rejected"]),
    ("c22", "Clausebook: a DOMAIN WORD is redefined in Lean (`valid on` no longer requires sender and receiver to differ). The old glossary and "
            "the Rust readings are untouched; the readings that use the word are no longer equivalent to their old statements",
     sub("lean/Ledger/Pieces.lean", "t.from.val < l.balances.val.length ∧ t.to.val < l.balances.val.length ∧ t.from.val ≠ t.to.val ∧",
         "t.from.val < l.balances.val.length ∧ t.to.val < l.balances.val.length ∧"),
     [], 1, [r"UNLINKED  A valid transfer is accepted and moves exactly its amount", r"UNLINKED  An invalid transfer is rejected and changes nothing",
             r"PROVED-FOR-ALL  Applying any batch of transfers conserves"]),
    ("c23", "frame library: the EXECUTABLE reading of a frame is wrong (`always` negated; the definition is untouched). Nothing kernel-checked "
            "changes; the comparison of the two readings on generated inputs must say so, and the run must fail",
     sub("lean/Frames/Check.lean", "  on op s a fun r _ => decide (cls r)\n\ndef never", "  on op s a fun r _ => !decide (cls r)\n\ndef never"),
     [], 1, [r"FRAME READINGS DISAGREE: the definition and the executable reading of a frame differ at",
             r"39 scenarios: 27 PROVED-FOR-ALL, 6 PROVED-INSTANCE, 4 REFUTED, 1 UNBOUND, 1 VACUOUS"]),
    ("c24", "an ILL-TYPED composition in a Rule line (a whole ledger where a number is needed): reported with file:line and the types, "
            "no statement is guessed, and the run fails",
     sub("features/ledger.feature", "  Rule: A batch never changes the total of all balances of the ledger",
         "  Rule: A batch never leaves the ledger above the maximum"),
     [], 1, [r"ILL-TYPED", r"features/ledger\.feature:13: \"a batch never leaves the ledger above the maximum\"|features/ledger\.feature:13: \"never leaves the ledger above the maximum\"",
             r"`l\.ledger` is a measure<balances>, where `at_most` takes a measure<num>",
             r"Rule \"A batch never leaves the ledger above the maximum\" [^\n]*ILL-TYPED   <-- EXPECTED PROVED-FOR-ALL"]),
    ("c25", "a Rule line that says more than its scenarios and is FALSE (every scenario beneath it stays true and proved): the rule "
            "statement is refuted at a concrete input, in the kernel, and the run fails",
     sub("features/wallet.feature", "  Rule: A transfer never changes the total of all balances", "  Rule: A transfer never changes the sender's balance"),
     [], 1, [r"Rule \"A transfer never changes the sender's balance\" [^\n]*REFUTED   <-- EXPECTED PROVED-FOR-ALL",
             r"kernel-checked   theorem Rule\.wallet\.transfer_total\.refuted", r"PROVED-FOR-ALL  A covered transfer moves the money"]),
    ("c26", "sign-off per PIECE: everything signed, then the Lean text of one domain word is edited (same meaning): that piece's sign-off "
            "is void, and --strict fails on exactly that piece",
     signed(sub("lean/Wallet/Pieces.lean", "@[reducible] def balance (w : Wallet) : Nat := w.balance.val",
                "@[reducible] def balance (w : Wallet) : Nat := (w.balance).val")), ["--strict"], 1,
     [r"UNREVIEWED: w\.balance", r"--strict: rests on 1 Clausebook pieces with no valid sign-off"]),
    ("c27", "an UNBOUND word in a scenario whose old whole-phrase binding still exists cannot fall back on it: one form of the Clausebook "
            "is removed, the scenarios that need it get no reading and no verdict from the old statement",
     sub("clausebook.yaml", '    then_forms: ["{m:measure<num>} is increased by {t:term<num>}"]', '    then_forms: []'),
     [], 1, [r"UNBOUND  A deposit with room succeeds and adds exactly the amount", r"no composition of Clausebook pieces reads \"Alice's balance is increased by <amount>\" as a claim",
             r"it is not reported in the reading's place"]),
    # ---- added with the fixes after the review of the frame library (2026-11-10)
    ("c28", "a Rule clause about REJECTED calls of an operation that never rejects (applying a batch reports a count): it compiles and no "
            "counterexample can exist, because it covers no call. The run must say so (it is expected to be unproved, so the run passes)",
     sub("features/ledger.feature", "  @id:batch_count\n",
         "  @expect-unproved @id:rejected_batch_total\n  Rule: A rejected batch never changes the total of all balances of the ledger\n\n  @id:batch_count\n"),
     [], 0, [r"COVERS NO CALL ON THE GRID", r"covers no call   the clause", r"every answer is an acceptance",
             r"RESULT: every scenario got its expected verdict"]),
    ("c29", "frame library: the EXECUTABLE reading is wrong only on a call that gives NO ANSWER (it lets a silent call pass a claim about "
            "every call). No call of the fixtures is silent, so the fixture comparison cannot see it (in the review this change passed the "
            "run); the toy operation of lean/Run/FrameToyTests.lean must, and the run must fail",
     sub("lean/Frames/Check.lean", "  | .every => false\n  | _ => true", "  | .every => true\n  | _ => true"),
     [], 1, [r"frame `always_answers` \(toy operation[^\n]*its definition and its executable reading disagree",
             r"definition and executable reading of the frames agree on (\d+) of \1 evaluations"]),
    ("c30", "an equivalence NEW <-> OLD whose proof uses the PROOF of the old statement for one direction (the type is exactly right, the "
            "axioms are standard): the audit must not count it, and the scenario must be UNLINKED",
     sub("clausal/links.py", "        out.append(lk.theorem())\n        meta[\"iffs\"]",
         "        t_ = lk.theorem()\n        if rd.id == \"Spec.wallet.withdraw_covered\":\n"
         "            t_ = (t_.replace(f\"theorem {rd.id}.reading_iff :\", f\"theorem {rd.id}.reading_iff_real :\")\n"
         "                  + f\"\\ntheorem {rd.id}.reading_iff : {rd.name} ↔ {b.id}.stmt := ⟨fun _ => {b.id}, {rd.id}.reading_iff_real.mpr⟩\\n\")\n"
         "        out.append(t_)\n        meta[\"iffs\"]"),
     [], 1, [r"UNLINKED  A covered withdrawal succeeds and takes exactly the amount",
             r"the proof of the equivalence uses a proof of one of its two sides"]),
    ("c31", "the generator smuggles a constant of the project into a reading that none of its pieces accounts for (a field of the Aeneas "
            "model written straight into the `lean:` of a domain word; the meaning is the same and every equivalence still proves). The "
            "old blocklist of three names passes this; the allowlist must fail it",
     sub("clausebook.yaml", '    lean: "W.balance {w}"', '    lean: "({w}).balance.val"'),
     [], 1, [r"GENERATOR-CHECK-FAILED: the reading mentions wallet\.Wallet\.balance"]),
    # ---- added with "end to end for new sentences" (2026-11-10/11): the Rust reading per piece, the generic step, the flat
    # ---- proof obligation of a new sentence, the general refutation script. Builder's controls.
    ("c32", "the RUST reading of ONE PIECE is wrong (`is not more than` made strict in wallet-bdd/src/pieces.rs; the Lean piece is "
            "untouched). The comparison of every compiled reading on generated inputs, Lean pieces on the model against Rust pieces on "
            "the compiled crate, must say so, and the run must fail",
     sub("wallet-bdd/src/pieces.rs", '"not_more_than" => Val::Bool(n("t") <= n("m")),', '"not_more_than" => Val::Bool(n("t") < n("m")),'),
     [], 1, [r"PIECE READINGS DISAGREE", r"<-- THEY DISAGREE"]),
    ("c33", "the generated FLAT OBLIGATION of a new sentence says less than its reading (the `flat:` template of `never changes` "
            "replaced by True). The obligation is easy to prove; the equivalence with the reading must fail, and the new scenario must "
            "not be PROVED",
     sub("clausebook.yaml", "    flat: \"{m'} = {m}\"\n", '    flat: "True"\n'),
     [], 1, [r"NOT LINKED       the flat proof obligation is NOT proved equivalent to the reading",
             r"TESTED-ONLY  a transfer between two accounts of the ledger [^\n]*<-- EXPECTED PROVED-FOR-ALL"]),
    ("c34", "the supplied proof of a NEW sentence's obligation is replaced by sorry: the sentence is TESTED-ONLY, and so is the Rule "
            "that was proved from it; nothing else changes",
     retheorem("lean/Wallet/Proofs/ledger_rules/readme_transfer_keeps_aggregate.lean", "Spec.ledger_rules.readme_transfer_keeps_aggregate",
               "theorem Spec.ledger_rules.readme_transfer_keeps_aggregate : Spec.ledger_rules.readme_transfer_keeps_aggregate.obligation := by\n  sorry"),
     [], 1, [r"TESTED-ONLY  a transfer between two accounts of the ledger", r"proof incomplete \(sorry\)",
             r"Rule \"An internal fund transfer never changes the aggregate account value of the ledger\" [^\n]*TESTED-ONLY   <-- EXPECTED PROVED-FOR-ALL",
             r"39 scenarios: [^\n]*\b26 PROVED-FOR-ALL\b"]),
    ("c35", "a NEW Rule line about SUCCESSFUL calls that is false (every scenario beneath it stays true and proved): the rule statement is "
            "refuted in the kernel by the general script, at an input the compiled Rust confirms, and the run fails",
     sub("features/ledger_rules.feature", "  Rule: An internal fund transfer never changes the aggregate account value of the ledger",
         "  Rule: A successful fund transfer never changes the ledger"),
     [], 1, [r"Rule \"A successful fund transfer never changes the ledger\" [^\n]*REFUTED   <-- EXPECTED PROVED-FOR-ALL",
             r"kernel-checked   theorem Rule\.ledger_rules\.readme_internal_transfers\.refuted2",
             r"the same input on the compiled Rust \(per-piece Rust readings\): reproduced",
             r"PROVED-FOR-ALL  a transfer between two accounts of the ledger"]),
    # ---- added with plan node E1 "layered evidence" (2026-11-11): the generated property tests and Kani harnesses, the feed-back
    # ---- of their falsifying inputs to the Lean model, MODEL MISMATCH and READING MISMATCH. Builder's controls.
    ("c36", "the magic-value mutant d6 (a deposit of exactly 1000003 credits one unit too few): no example row, no grid point and no "
            "generated sample uses that amount, so until now the only signal was a lost proof. The GENERATED Kani harness must find the "
            "input, it must be replayed on the compiled Rust and on the Lean model, and the scenario must be shown FALSE with its source",
     sub("wallet/src/lib.rs", "                self.balance = b;", "                self.balance = if amt == 1_000_003 { b - 1 } else { b };"),
     ["--full"], 1, [r"fed back: Spec\.wallet\.deposit_with_room is false at an input found by the generated bounded check",
                     r"(REFUTED|COUNTEREXAMPLE)  A deposit with room succeeds and adds exactly the amount[^\n]*<-- EXPECTED PROVED-FOR-ALL",
                     r"source           the input was found on the compiled Rust by the generated bounded check \(Kani\)",
                     r"\"amount\": \"1000003\""]),
    ("c37", "ONE TYPED piece reading of the generated harnesses is wrong (`the balance of account k` gives 1, not 0, for an account "
            "that does not exist; evidence/src/typed.rs). The property test compares the generated predicate with the tree evaluator at "
            "every case: it must report READING MISMATCH and the run must fail",
     sub("evidence/src/typed.rs", "        l[k as usize] as u128\n    } else {\n        0\n    }", "        l[k as usize] as u128\n    } else {\n        1\n    }"),
     [], 1, [r"READING MISMATCH", r"[1-9][0-9]* READING MISMATCH"]),
    ("c38", "the COMPILED Rust is not the Rust that was translated: the Rust-side crates are pointed at a copy of the wallet in which a "
            "successful withdrawal does not take the money, while Charon and Aeneas still translate the original. The generated "
            "property test fails on the compiled Rust at inputs where the Lean model does not: MODEL MISMATCH, and the run fails",
     shipped_wallet("        self.balance -= amt;\n        Ok(())", "        Ok(())"),
     [], 1, [r"MODEL MISMATCH: [^\n]*the compiled Rust fails and the Lean model holds",
             r"[1-9][0-9]* MODEL MISMATCH"]),
]


BEFORE_REVIEW = False


def sh(cmd, cwd, timeout=3600):      # 900 s until the composable Clausebook: one control (c22) ran out on a machine at load 150
    r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, timeout=timeout,
                       executable="/bin/bash")
    return r.returncode, r.stdout + r.stderr


def fresh(work: Path):
    rc, out = sh(f"'{HERE}/workcopy.sh' '{work}'", SLICE)
    if rc:
        raise RuntimeError(out)


def observe(work: Path):
    """What the run in `work` concluded: scenario id -> verdict code; (feature, line) -> cucumber status."""
    g = json.loads((work / "out/graph.json").read_text()) if (work / "out/graph.json").exists() else {"verdicts": []}
    codes = {v["node"].split("Spec.", 1)[1]: v["code"] for v in g["verdicts"] if v["node"].startswith("scenario:")}
    rows = {}
    cj = work / "out/cucumber.json"
    if cj.exists():
        steps = {}          # a Background is reported as its own element on the scenario's line: one run, steps put together
        for f in json.loads(cj.read_text()):
            for e in f.get("elements", []):
                steps.setdefault(f"{f['uri'].rsplit('/', 1)[-1]}:{e['line']}", []).extend(s["result"]["status"] for s in e["steps"])
        for k, st in steps.items():
            rows[k] = "fail" if "failed" in st else "pass" if all(x == "passed" for x in st) else "skipped"
    return codes, rows


FALSE = ("REFUTED", "COUNTEREXAMPLE")


def observe_rules(work: Path) -> dict:
    """Rule id -> verdict code of the statement compiled from the Rule line (added with the composable Clausebook)."""
    g = json.loads((work / "out/graph.json").read_text()) if (work / "out/graph.json").exists() else {"verdicts": []}
    return {v["node"].split("Rule.", 1)[1]: v["code"] for v in g["verdicts"] if v["node"].startswith("group:rule:")}


def shown_false(m: dict) -> bool:
    """A scenario is shown false of the mutant: a row differs on the compiled Rust, or the search found a counterexample."""
    return bool(m["rows_changed"] or m["search_found"])


def new_fed(m: dict) -> list:
    """The readings of a mutant run whose counterexample came from a generated harness, without the fixture rule that is
    fed back on the unmutated code as well (features/ledger_rules.feature, e1_fifth_account_empty)."""
    return [x for x in m.get("fed_back", []) if x[0] != "Rule.ledger_rules.e1_fifth_account_empty"]


def layers(changed: dict, base: dict) -> dict:
    """What the proof layer and the search layer each noticed, from the verdicts that changed.
    proof_broke:        scenarios that were PROVED and no longer are (the proof, or a lemma module it depends on,
                        no longer compiles). NOT the same as "the statement is false": a proof is also lost when a
                        lemma about the same Rust function fails, although this scenario's statement still holds.
    search_found:       scenarios for which the grid search now finds a counterexample and did not before
                        (the statement IS false of the mutant, on the Lean model).
    refutation_changed: deliberately false scenarios whose verdict changed (their counterexample is gone, or it
                        can no longer be confirmed in the kernel)."""
    return {"proof_broke": sorted(k for k, v in changed.items() if base.get(k, "").startswith("PROVED") and not v.startswith("PROVED")),
            "search_found": sorted(k for k, v in changed.items() if v in FALSE and base.get(k) not in FALSE),
            "refutation_changed": sorted(k for k, v in changed.items() if base.get(k) in FALSE)}


def write_md(res: dict, stem: str, before_review: bool = False):
    mutants, controls = res["mutants"], res["controls"]
    md = ["# Mutation run" + (" against the scenario set BEFORE the review (8 scenarios)" if before_review else ""), "",
          f"Generated {res['generated_at']} by `python3 mutation/run_mutants.py`. Logs: `mutation/logs/`.", "",
          "Columns. *Examples rows on Rust*: an Examples row or a literal scenario gives a different result on the compiled "
          "Rust. *Proofs lost*: scenarios that were PROVED and no longer are, because their proof or a lemma module it "
          "depends on no longer compiles; this does not by itself mean their statement is false of the mutant. "
          "*New counterexamples*: scenarios for which the grid search on the Lean model now finds a failing input, so "
          "their statement is false of the mutant.", "",
          "Two rates are reported. **Shown false**: a row differs or a counterexample is found, so some scenario is "
          "demonstrably false of the mutant. **Run fails only because a proof is lost**: nothing is shown false; the run "
          "fails because a hand-written proof or lemma no longer compiles. The second is not detection by the scenarios: "
          "the lemma may say more than any scenario does, and an agent that re-proves against the changed code can make the "
          "run pass again unless some scenario statement really is false of it.", ""]
    for crate in ("wallet", "ledger"):
        ms = [m for m in mutants if m.get("crate", "wallet") == crate]
        if not ms:
            continue
        rows = [m for m in ms if m["rows_changed"]]
        proof = [m for m in ms if m["proof_broke"]]
        search = [m for m in ms if m["search_found"]]
        md += [f"## `{crate}/src/lib.rs`: {len(ms)} mutants", "",
               f"- **a scenario is shown false of the mutant** (a row differs on the compiled Rust, or the search finds a "
               f"counterexample): **{len([m for m in ms if shown_false(m)])} of {len(ms)}**",
               f"- the run fails ONLY because a proof or lemma stopped compiling (nothing shown false): "
               f"{len([m for m in ms if m['killed_by_scenarios'] and not shown_false(m)])} "
               f"({', '.join(m['id'] for m in ms if m['killed_by_scenarios'] and not shown_false(m)) or '-'})",
               f"- the run does not fail at all: {len([m for m in ms if not m['killed_by_scenarios']])} "
               f"({', '.join(m['id'] for m in ms if not m['killed_by_scenarios']) or '-'})",
               f"- the run fails (pipeline without the crate's unit tests, exit status non-zero), for either reason: "
               f"{sum(m['killed_by_scenarios'] for m in ms)} of {len(ms)}",
               f"- noticed by an example row on the compiled Rust: {len(rows)}",
               f"- at least one proof lost: {len(proof)}",
               f"- a new counterexample found by the search on the Lean model: {len(search)}",
               f"- a scenario or rule shown false at an input a GENERATED harness found and the grid search did not (fed back to the "
               f"Lean model; the fixture rule that is fed back on the unmutated code too is not counted): "
               f"{len([m for m in ms if new_fed(m)])} of {len(ms)} mutants, {sum(len(new_fed(m)) for m in ms)} readings "
               f"({sum(1 for m in ms for x in new_fed(m) if x[1] == 'property test')} from the property test, "
               f"{sum(1 for m in ms for x in new_fed(m) if x[1] == 'bounded check')} from the bounded check); with the bounded check "
               f"(run only when the quick run shows no scenario false): {', '.join(m['id'] for m in ms if m.get('bounded_check_run')) or 'none'}; "
               f"MODEL MISMATCH reported for: {', '.join(m['id'] for m in ms if m.get('model_mismatch')) or 'none'}",
               f"- a proof lost but NO example row differs: {len([m for m in proof if not m['rows_changed']])} "
               f"({', '.join(m['id'] for m in proof if not m['rows_changed']) or '-'})",
               f"- an example row differs but NO proof is lost: {len([m for m in rows if not m['proof_broke']])} "
               f"({', '.join(m['id'] for m in rows if not m['proof_broke']) or '-'})",
               f"- missed by the crate's own unit tests: {len([m for m in ms if m['unit_tests'] == 'MISSED'])} "
               f"({', '.join(m['id'] for m in ms if m['unit_tests'] == 'MISSED') or '-'})",
               f"- a RULE statement (compiled from a `Rule:` line) that holds of the unmutated code is found false: "
               f"{len([m for m in ms if m.get('rule_shown_false')])} of {len(ms)} "
               f"(confirmed in the kernel for {len([m for m in ms if any(m['rules_changed'][k] == 'REFUTED' for k in m.get('rule_shown_false', []))])}); "
               f"of mutants of which NO scenario is shown false: "
               f"{', '.join(m['id'] + ' (' + ', '.join(m['rule_shown_false']) + ')' for m in ms if m.get('rule_shown_false') and not shown_false(m)) or 'none'}; "
               f"a scenario is shown false but no rule statement is: "
               f"{', '.join(m['id'] for m in ms if shown_false(m) and not m.get('rule_shown_false')) or 'none'}", "",
               "| Mutant | Operation | What was changed | Crate unit tests | Examples rows on Rust | Proofs lost | New counterexamples | Verdicts that changed | A scenario shown false | Run fails |",
               "|---|---|---|---|---|---|---|---|---|---|"]
        for m in ms:
            md.append(f"| {m['id']} | `{m['fn']}` | {m['description']} | {m['unit_tests']} | {m['rows_on_rust']} | "
                      f"{len(m['proof_broke']) or 'none'} | {len(m['search_found']) or 'none'} | {m['proof_layer']} | "
                      f"{'yes' if shown_false(m) else '**NO** (lost proof only)' if m['killed_by_scenarios'] else '**NO**'} | "
                      f"{'yes' if m['killed_by_scenarios'] else '**NO**'} |")
        md.append("")
    md += ["", "## Negative controls (checks of the checks)", "", "| Control | What is wrong | Expected exit | Got | As expected |", "|---|---|---|---|---|"]
    for c in controls:
        md.append(f"| {c['id']} | {c['what']} | {c['expected_exit']} | {c['exit']} | {'yes' if c['as_expected'] else '**NO**: missing ' + '; '.join(c['missing_output'])} |")
    (HERE / f"{stem}.md").write_text("\n".join(md) + "\n")


def run_one(job):
    kind, item, work, base = job
    fresh(work)
    if BEFORE_REVIEW:
        drop_new_scenarios(work)
    PATH = 'export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"; '
    if kind == "baseline":
        # --quick (since plan node E1): the generated Kani harnesses take about ten minutes per run and feed no verdict of
        # the unmutated tree; the generated property tests still run. A control that needs the bounded check asks with --full.
        rc, out = sh(PATH + "./run.sh --no-unit --quick", work)
        return {"exit": rc, "codes": observe(work)[0], "rows": observe(work)[1], "rules": observe_rules(work), "tail": out[-600:]}
    if kind == "control":
        id_, what, patch, args, want_rc, pats = item
        patch(work)
        rc, out = sh(PATH + "./run.sh --no-unit " + ("" if "--full" in args else "--quick ") + " ".join(x for x in args if x != "--full"), work)
        missing = [p for p in pats if not re.search(p, out)]
        (HERE / "logs").mkdir(exist_ok=True)
        (HERE / "logs" / f"{id_}.log").write_text(out)
        return {"id": id_, "what": what, "expected_exit": want_rc, "exit": rc, "expected_output": pats, "missing_output": missing,
                "as_expected": rc == want_rc and not missing}
    id_, fn, what, old, new = item
    crate = "ledger" if fn.startswith("ledger::") else "wallet"
    lib = work / crate / "src/lib.rs"
    s = lib.read_text()
    assert s.count(old) == 1, f"{id_}: pattern occurs {s.count(old)} times"
    lib.write_text(s.replace(old, new))
    urc, uout = sh(PATH + f"cd {crate} && cargo test --quiet", work)
    compiles = "error[" not in uout and "could not compile" not in uout
    # --no-adequacy: the suite adequacy note feeds no verdict and no exit status, and a mutant run is read only for
    # those. The baseline and the controls run the whole pipeline, note included.
    # --no-heldout: the new sentences of heldout/ are informational too.
    def attempt(extra):
        rc, out = sh(PATH + "./run.sh --no-unit --no-adequacy --no-heldout" + extra, work)
        (HERE / "logs").mkdir(exist_ok=True)
        (HERE / "logs" / f"{id_}{'-before-review' if BEFORE_REVIEW else ''}.log").write_text(out)
        codes, rows = observe(work)
        translated = "wrote lean/Generated/Wallet.lean" in out
        changed = {k: v for k, v in codes.items() if base["codes"].get(k) != v}
        rows_changed = sorted(k for k, v in rows.items() if base["rows"].get(k) != v)
        rules = observe_rules(work)
        rules_changed = {k: v for k, v in rules.items() if base.get("rules", {}).get(k) != v}
        # which counterexamples came from a generated harness (plan node E1) and not from the grid search
        fed = sorted(set(re.findall(r"^  fed back: (\S+) is false at an input found by the generated (property test|bounded check)", out, re.M)))
        return {"id": id_, "fn": fn, "crate": crate, "description": what, **layers(changed, base["codes"]),
                # the statements compiled from the Rule lines (not part of `shown false`, which is about scenarios as before)
                "rules_changed": rules_changed,
                # NEWLY found false: a rule that is deliberately false at baseline and merely loses its kernel confirmation
                # (REFUTED -> COUNTEREXAMPLE) does not count
                "rule_shown_false": sorted(k for k, v in rules_changed.items() if v in FALSE and base.get("rules", {}).get(k) not in FALSE),
                "valid": compiles and translated,
                "unit_tests": "caught" if urc else "MISSED",
                "rows_on_rust": f"caught ({len(rows_changed)} rows)" if rows_changed else "MISSED",
                "proof_layer": ("; ".join(f"{k.split('.', 1)[1]}: {v}" for k, v in changed.items()) or "MISSED") if translated else "not translated",
                "verdicts_changed": changed, "rows_changed": rows_changed, "fed_back": [list(x) for x in fed],
                "model_mismatch": bool(re.search(r"^  MODEL MISMATCH: ", out, re.M)),
                "exit": rc, "killed_by_scenarios": rc != 0}
    # --quick: the generated property tests run, the bounded checks (Kani, about ten minutes) do not. If no scenario is
    # shown false that way, the run is repeated WITH the bounded checks, and the result says so.
    r = attempt(" --quick")
    r["bounded_check_run"] = False
    if r["valid"] and not shown_false(r):
        r = attempt("")
        r["bounded_check_run"] = True
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--only", default="")
    ap.add_argument("--keep", action="store_true", help="keep the scratch copies under build/mutation/")
    ap.add_argument("--before-review", action="store_true")
    ap.add_argument("--resummarise", action="store_true",
                    help="no runs: recompute the per-layer summary of mutation/results.json from the verdicts it recorded, and rewrite results.md")
    a = ap.parse_args()
    if a.resummarise:
        res = json.loads((HERE / "results.json").read_text())
        for m in res["mutants"]:
            m.setdefault("crate", "ledger" if m["fn"].startswith("ledger::") else "wallet")
            m.update(layers(m["verdicts_changed"], res["baseline"]["verdicts"]))
            if "rules_changed" in m:
                m["rule_shown_false"] = sorted(k for k, v in m["rules_changed"].items()
                                               if v in FALSE and res["baseline"].get("rules", {}).get(k) not in FALSE)
        (HERE / "results.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
        write_md(res, "results")
        print("rewrote mutation/results.json and mutation/results.md from the recorded verdicts")
        return 0
    global BEFORE_REVIEW
    BEFORE_REVIEW = a.before_review
    stem = "results-before-review" if BEFORE_REVIEW else "results"
    only = set(filter(None, a.only.split(",")))
    root = SLICE / "build" / "mutation"
    works = [root / f"w{i}" for i in range(a.jobs)]
    base = run_one(("baseline", None, works[0], None))
    if base["exit"] != 0:
        sys.exit("the unmutated tree does not pass ./run.sh --no-unit:\n" + base["tail"])
    print(f"baseline ok: {len(base['codes'])} scenarios")
    # controls FIRST (since 2026-11-11): they test the pipeline's own checks, so a run that has to be cut short still has them
    items = [("control", c) for c in CONTROLS if (not only or c[0] in only) and not BEFORE_REVIEW] + [("mutant", m) for m in MUTANTS + LEDGER_MUTANTS if not only or m[0] in only]
    results = []
    partial = HERE / f"{stem}.partial.jsonl"       # one line per finished item, so an interrupted run leaves what it measured
    if not only:
        partial.write_text(json.dumps({"kind": "baseline", "spec_digest": spec_digest(), "exit": base["exit"], "verdicts": base["codes"],
                                       "rules": base.get("rules", {})}, ensure_ascii=False) + "\n")

    def worker(i):
        out = []
        for kind, item in items[i::a.jobs]:
            r = run_one((kind, item, works[i], base))
            out.append((kind, r))
            if not only:
                with partial.open("a") as fh:
                    fh.write(json.dumps({"kind": kind, **r}, ensure_ascii=False) + "\n")
            if kind == "mutant":
                print(f"  {r['id']}: unit tests {r['unit_tests']}; rows {r['rows_on_rust']}; proofs/search {r['proof_layer']}; "
                      f"a scenario shown false: {'yes' if shown_false(r) else 'NO'}; run fails: {'yes' if r['killed_by_scenarios'] else 'NO'}" + ("" if r["valid"] else "  [INVALID MUTANT]"), flush=True)
            else:
                print(f"  {r['id']}: {'as expected' if r['as_expected'] else 'NOT AS EXPECTED'} (exit {r['exit']}, missing {r['missing_output']})", flush=True)
        return out
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex:
        for chunk in ex.map(worker, range(a.jobs)):
            results += chunk
    order = {m[0]: k for k, m in enumerate(MUTANTS + LEDGER_MUTANTS)} | {c[0]: 100 + k for k, c in enumerate(CONTROLS)}
    mutants = sorted([r for k, r in results if k == "mutant"], key=lambda r: order[r["id"]])
    controls = sorted([r for k, r in results if k == "control"], key=lambda r: order[r["id"]])
    res = {"generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
           "spec_digest": spec_digest(), "complete": not only,
           "command": "python3 mutation/run_mutants.py",
           "baseline": {"exit": base["exit"], "verdicts": base["codes"], "rules": base.get("rules", {})},
           "mutants": mutants, "controls": controls}
    if only:
        print(json.dumps(res, indent=1)[:4000])
        return 0
    (HERE / f"{stem}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    write_md(res, stem, BEFORE_REVIEW)
    if not a.keep:
        sh(f"rm -rf '{root}'", SLICE)
    print(f"wrote mutation/{stem}.json and mutation/{stem}.md")
    return 0 if all(c["as_expected"] for c in controls) and all(m["valid"] for m in mutants) else 1


if __name__ == "__main__":
    sys.exit(main())
