# clausal/ design: Gherkin scenarios bound to Lean theorems about real Rust

Date: 2026-11-09. Status: **implemented; see section 10 for what was built, what differs from this design, and the maths-side fit test.**

**Toolchain: Aeneas works.** Rust -> Charon -> Aeneas -> Lean runs end to end on this machine from prebuilt
binaries (see `TOOLCHAIN.md`). No fallback design is needed and there is no big decision pending for the owner.

**Decision: a hybrid built on the external-generator design (design B), with five grafts from the Lean-native
design (design A).** Standard `.feature` file + YAML glossary + a short hand-written Lean Clausebook file ->
generated Lean `Prop` statements -> proofs in a separate file -> a Lean audit executable -> `graph.json` and
`report.md`. The same feature file also runs under cucumber-rs against the compiled Rust.

Everything marked **[observed]** below was run today against the pinned Aeneas
(`nightly-2026.11.09-5a392f4`, Lean v4.35.0); the files are in `clausal/probe/`. Everything marked **[not checked]**
is an expectation.

---

## 1. Scores and why

Scale 1 (poor) to 5 (good).

| Criterion | A: Lean-native (attributes + elaborator) | B: external generator + YAML + cucumber-rs | Hybrid |
|---|---|---|---|
| 1. Auditability of English -> formal by a non-Lean reader | 3 - English sits beside the Lean def, but the reader must open a Lean file with attributes and a `World` type | 4 - a YAML table of phrases; each points at a one-line definition | 4-5 - B's table, plus A's rendered two-column glossary in the report |
| 2. Soundness (no false "proved") | 4 - checked term is the generated term; bans model functions in Given/Then; vacuity and trivial-Then checks; sign-off hashes | 3 - requires a satisfiability witness, flags frame-trivial Thens, but nothing stops a Then defined as "whatever the code returns" | 4-5 - B plus A's checks |
| 3. Same feature file runs as ordinary tests | 1 - not standard cucumber; only evaluation inside Lean | 5 - standard Gherkin, cucumber-rs | 5 |
| 4. Cost of a thin slice | 2 - parser, three attributes, environment extensions, term elaborator and exporter, all in Lean metaprogramming | 4 - about 400 lines of Python emitting plain Lean text | 4 |
| 5. Graph schema also fits maths lemma graphs | 4 - several evidence entries per edge; lemma = interface + implementation | 4 - staleness via input hashes, explicit verdict records | 5 - union of both |

Why B is the base:

- **Criterion 3 decides it.** A cannot run the feature file as ordinary tests without building a second system.
- **Cost.** A's value (errors at the point of definition, one environment) is real but is paid for in Lean
  metaprogramming, which is the most expensive code to write and debug here. B's generator never writes Lean
  expressions; it only applies named definitions to variables, and Lean still type-checks the result.
- **Named actors read better than a `World` record.** "Alice transfers 30 to Bob" needs no state type, and the
  frame condition (untouched actors keep their pre-state) falls out of the argument wiring.

What is taken from A:

1. **Given/Then definitions may not use any model function** (enforced by the audit, section 6.3). Without this a
   Then can restate the code and prove nothing.
2. **Trivial-Then check**: a postcondition that follows from the Givens alone is reported.
3. **Sign-off hashes** per glossary entry; a changed definition shows as UNREVIEWED.
4. **The report prints the glossary as a two-column table** (English | Lean body) and prints each statement next to
   its scenario, since the generator itself is untrusted code.
5. **Several evidence entries per edge**, and no single "weakest link" ordering: tested and tool-trusted are not
   comparable, so a verdict lists the evidence kinds it rests on.

What is dropped: A's `World` type, the in-Lean Gherkin parser and attributes, Plausible-based search (boundary grid
instead), and B's single total order over evidence kinds.

---

## 2. What Aeneas output really looks like [observed]

Rust (`probe/wallet_lib.rs`):

```rust
pub fn transfer(src: &mut Wallet, dst: &mut Wallet, amt: u64) -> Result<(), Error> {
    if src.balance < amt { return Err(Error::InsufficientFunds); }
    let nb = match dst.balance.checked_add(amt) { Some(b) => b, None => return Err(Error::Overflow) };
    src.balance -= amt;
    dst.balance = nb;
    Ok(())
}
```

Generated Lean (`probe/Wallet.generated.lean`, namespace = crate name in lower case, file `Generated/Wallet.lean`):

```lean
inductive Error where | InsufficientFunds : Error | Overflow : Error
structure Wallet where balance : Std.U64

def Wallet.deposit (self : Wallet) (amt : Std.U64) : Result ((core.result.Result Unit Error) × Wallet)
def Wallet.withdraw (self : Wallet) (amt : Std.U64) : Result ((core.result.Result Unit Error) × Wallet)

def transfer (src : Wallet) (dst : Wallet) (amt : Std.U64) :
  Result ((core.result.Result Unit Error) × Wallet × Wallet) := do
  if src.balance < amt
  then ok (core.result.Result.Err Error.InsufficientFunds, src, dst)
  else
    let o ← lift (U64.checked_add dst.balance amt)
    match o with
    | none => ok (core.result.Result.Err Error.Overflow, src, dst)
    | some b =>
      let i ← src.balance - amt
      ok (core.result.Result.Ok (), { balance := i }, { balance := b })
```

Facts the design depends on:

- **Two result layers.** Outer `Result` (Aeneas) = returned / panicked / diverged. Inner `core.result.Result`
  (`Ok` / `Err`) is the Rust value. A Rust `Err` is an ordinary returned value.
- **`&mut` arguments come back as extra tuple components, in parameter order**, after the return value:
  `(ret, src', dst')`. Early returns hand back the unchanged inputs.
- **Outer `Result` is not an inductive.** It is `@[irreducible] def Result α := ITree RustEffect α`. `ok`, `fail`,
  `div` are functions. Consequences:
  - `decide` on `f x = ok y` fails (no `Decidable` instance).
  - `match r with | .ok .. | .fail .. | .div` does not work; observe through `Result.match r`, which returns the
    inductive `MatchResult` (`.ok a`, `.div`, `.vis eff k`; a panic is `.vis (.fail e) _`).
  - **The model does evaluate**: `#eval` of a checker built on `Result.match` returned the right answers for
    success, overflow and insufficient-funds inputs.
- **Hoare triples**: `Aeneas.Std.WP.spec m Q`, notation `m ⦃ r => Q r ⦄`; the tactics are `step` and `step*`
  (not `progress`). `spec` is total correctness: `spec (fail e) Q` and `spec div Q` are `False`.
- **Bridge both ways between `spec` and the plain form** `∃ r, m = ok r ∧ Q r` is a five-line lemma
  (`probe/ProbeHolds.lean`), so statements can be written without Aeneas notation and still proved with `step*`.
- **Proof effort for the wallet scenarios is small**: `intro ..; apply Bdd.ok3_of_spec; unfold wallet.transfer; step*;
  simp [Vocab defs] at *; scalar_tac` closed the universal success statement; `step*` alone closed the rejection
  statement. Axioms: `[propext, Classical.choice, Quot.sound]`.
- **Kernel-checked refutation works**, but not by `decide`/`simp` on the model. Working recipe: prove, with `step*`,
  that at the witness the call returns a value satisfying the negated Then; combine with the assumed statement.
- **`decide` gets stuck on `U64.max`** inside a Given. Satisfiability witnesses close with
  `by simp [Vocab defs]; scalar_tac` instead.
- **`DecidableEq` is not derived for generated types.** `deriving instance DecidableEq for wallet.Wallet` (and for
  the error enum and `core.result.Result`) works from a hand-written file.
- **Name clash**: generated files `open ... Error`, and a Rust enum called `Error` becomes ambiguous with Aeneas's
  `Std.Error` in files that open both namespaces. The slice names its enum `WalletError`.
- Literals are `30#u64`; numeric value is `x.val`; bound is `U64.max : Nat`. `checked_add` is covered by Aeneas's
  hand-written library model `U64.checked_add`, not by translating std.
- [not checked] Loops, traits, generics, collections, `?`, closures.

---

## 3. Layout

All under `clausal/`. `translate.sh` is extended to take a list of crates; the existing `rust/` (`checked_add`) stays.

```
wallet/                      cargo crate `wallet` (code under test; no derives, no test code)
wallet-bdd/                  cargo crate: cucumber-rs runner + tests/steps.rs (Charon never sees it)
features/wallet.feature      standard Gherkin
glossary.yaml                phrase -> Lean definition + argument wiring       (human-asserted)
glossary.signoff.json        {entry id, def hash, reviewer, date}
clausal/                    Python generator (parser, matcher, emitter, report)
lean/Generated/Wallet.lean   Aeneas output, never edited                        (tool-trusted)
lean/Bdd/Basic.lean          fixed support: bridge lemmas, Check type, run      (kernel-checked / plain defs)
lean/Wallet/Vocab.lean       hand-written glossary definitions                  (human-asserted)
lean/Wallet/Statements.lean  GENERATED, overwritten each run
lean/Wallet/Checks.lean      GENERATED, overwritten each run
lean/Wallet/Proofs.lean      scaffolded once, then owned by people/agents; tool only appends
lean/Wallet/Audit.lean       GENERATED: `lake exe audit` prints JSON
out/graph.json, out/report.md
```

Pipeline (`./run.sh`, batch only):

1. `translate.sh` (Charon, Aeneas, provenance hashes).
2. `clausal gen`: parse, match, emit `Statements`, `Checks`, `Audit`, append missing proof stubs.
3. `lake build` in `clausal/lean`.
4. `lake exe audit` -> `out/audit.json` (axioms, row checks, search results, glossary lints).
5. `cargo test -p wallet-bdd` -> cucumber JSON.
6. `clausal report` -> `graph.json`, `report.md`.

---

## 4. Glossary format

Two files. Together they are the whole human-asserted surface.

### 4.1 `lean/Wallet/Vocab.lean`

```lean
import Generated.Wallet
import Bdd.Basic
open Aeneas Aeneas.Std

deriving instance DecidableEq for wallet.WalletError
deriving instance DecidableEq for wallet.Wallet
deriving instance DecidableEq for core.result.Result

namespace Vocab
open wallet
abbrev Outcome := core.result.Result Unit wallet.WalletError

@[reducible] def hasBalance (w : Wallet) (n : U64) : Prop := w.balance = n
@[reducible] def covers (w : Wallet) (n : U64) : Prop := n.val ≤ w.balance.val
@[reducible] def exceeds (n : U64) (w : Wallet) : Prop := w.balance.val < n.val
@[reducible] def roomFor (w : Wallet) (n : U64) : Prop := w.balance.val + n.val ≤ U64.max
@[reducible] def noRoomFor (w : Wallet) (n : U64) : Prop := U64.max < w.balance.val + n.val
@[reducible] def succeeds (o : Outcome) : Prop := o = .Ok ()
@[reducible] def rejectedWith (o : Outcome) (e : WalletError) : Prop := o = .Err e
@[reducible] def decreasedBy (pre post : Wallet) (n : U64) : Prop := post.balance.val + n.val = pre.balance.val
@[reducible] def increasedBy (pre post : Wallet) (n : U64) : Prop := post.balance.val = pre.balance.val + n.val
@[reducible] def unchanged (pre post : Wallet) : Prop := post = pre
@[reducible] def totalUnchanged (pre post : List Wallet) : Prop :=
  (post.map (·.balance.val)).sum = (pre.map (·.balance.val)).sum
def mkWallet (n : U64) : Wallet := { balance := n }
end Vocab
```

These exact definitions elaborate, are decidable by unfolding, and were used in the probe proofs [observed].

Rules (checked by the audit, section 6.3):

- A definition used by a Given or Then **must not depend, transitively, on any function listed in
  `translation.json`**. Types, constructors and projections are fine.
- Non-recursive, and small (warning above 40 expression nodes).
- `Decidable` must be synthesizable once arguments are supplied; otherwise the entry must say `checkable: false`
  and scenarios using it lose counterexample search (the report says so).
- No truncating `Nat` subtraction: state "decreased by" additively.

### 4.2 `glossary.yaml`

```yaml
version: 1
lean_import: [Generated.Wallet, Wallet.Vocab]
param_types:
  amount:
    lean: U64
    literal_regex: '\d+'
    lean_literal: '{0}#u64'          # 30 -> 30#u64
    max: 18446744073709551615        # generator rejects larger literals with file:line
    sample: [0, 1, 2, 9223372036854775808, 18446744073709551614, 18446744073709551615]
  error:
    lean: wallet.WalletError
    enum: { 'insufficient funds': wallet.WalletError.InsufficientFunds,
            'overflow': wallet.WalletError.Overflow }
actors:
  wallet: { lean: wallet.Wallet, name_regex: '[A-Z][a-z]+' }   # Alice -> alice (pre), alice' (post)
steps:
  - id: G-balance
    kind: given
    phrase: "{wallet:w} has a balance of {amount:n}"
    lean: Vocab.hasBalance
    args: [pre(w), n]
    builds: { actor: w, with: "Vocab.mkWallet {n}" }   # constructive Given: lets a row be evaluated/tested
  - { id: G-covers,  kind: given, phrase: "{amount:n} is not more than {wallet:w}'s balance", lean: Vocab.covers,  args: [pre(w), n] }
  - { id: G-exceeds, kind: given, phrase: "{amount:n} is more than {wallet:w}'s balance",     lean: Vocab.exceeds, args: [n, pre(w)] }
  - { id: G-room,    kind: given, phrase: "{wallet:w}'s balance plus {amount:n} does not exceed the maximum", lean: Vocab.roomFor,   args: [pre(w), n] }
  - { id: G-noroom,  kind: given, phrase: "{wallet:w}'s balance plus {amount:n} exceeds the maximum",         lean: Vocab.noRoomFor, args: [pre(w), n] }
  - id: W-transfer
    kind: when
    phrase: "{wallet:src} transfers {amount:n} to {wallet:dst}"
    call: wallet.transfer
    args: [pre(src), pre(dst), n]
    returns: [outcome, post(src), post(dst)]   # return value first, then &mut args in parameter order [observed]
    outcome_type: Vocab.Outcome
    distinct: [src, dst]                       # two &mut cannot alias
    rust_fn: "wallet::transfer"                # must match rust_name in translation.json
  - { id: W-deposit,  kind: when, phrase: "{wallet:w} deposits {amount:n}",  call: wallet.Wallet.deposit,  args: [pre(w), n], returns: [outcome, post(w)], outcome_type: Vocab.Outcome, rust_fn: "wallet::{wallet::Wallet}::deposit" }
  - { id: W-withdraw, kind: when, phrase: "{wallet:w} withdraws {amount:n}", call: wallet.Wallet.withdraw, args: [pre(w), n], returns: [outcome, post(w)], outcome_type: Vocab.Outcome, rust_fn: "wallet::{wallet::Wallet}::withdraw" }
  - { id: T-ok,    kind: then, phrase: "the operation succeeds", lean: Vocab.succeeds, args: [outcome] }
  - { id: T-err,   kind: then, phrase: "the operation is rejected with {error:e}", lean: Vocab.rejectedWith, args: [outcome, e] }
  - { id: T-dec,   kind: then, phrase: "{wallet:w}'s balance is decreased by {amount:n}", lean: Vocab.decreasedBy, args: [pre(w), post(w), n] }
  - { id: T-inc,   kind: then, phrase: "{wallet:w}'s balance is increased by {amount:n}", lean: Vocab.increasedBy, args: [pre(w), post(w), n] }
  - { id: T-same,  kind: then, phrase: "{wallet:w}'s balance is unchanged", lean: Vocab.unchanged, args: [pre(w), post(w)] }
  - { id: T-total, kind: then, phrase: "the total of all balances is unchanged", lean: Vocab.totalUnchanged, args: [all_pre(wallet), all_post(wallet)] }
```

Argument terms - the complete language:

- a slot name: the placeholder or literal that filled the slot;
- `pre(x)` / `post(x)`: the actor before / after the call. `post(x)` of an actor the call does not return is
  rendered as `pre(x)` and the conjunct is flagged `frame-trivial`;
- `outcome`: the Rust-level return value;
- `all_pre(T)` / `all_post(T)`: list literal of every actor of type T, in order of first mention.

Matching:

- Whitespace is trimmed and collapsed. Matching is case-sensitive and anchored to the whole step text.
- A slot matches its type's `literal_regex`, an enum key, an actor name, or `<ident>`.
- `And` / `But` / `*` inherit the previous keyword. Background steps are prepended to the Givens.
- Exactly one entry of the right kind must match; zero is UNBOUND, two or more is AMBIGUOUS.
- A `when` entry's `call` must equal a `lean_name` in `translation.json`, and `rust_fn` its `rust_name`. The
  generator checks this, so a When cannot silently point at a hand-written function.

Sign-off: `clausal review <id>` records the sha256 of the YAML entry plus the Lean definition text into
`glossary.signoff.json` with reviewer and date. Any later change makes the entry UNREVIEWED.

Cucumber side: `wallet-bdd/tests/steps.rs` has one step function per glossary id, tagged `// glossary: <id>`, with
a regex string identical to the one `clausal` prints for that entry (checked). The Rust step bodies are a
**second hand-written reading** of each phrase; the graph records that as its own human-asserted edge.

---

## 5. Translation rule

Input: one Scenario or Scenario Outline, with Background, every step matched.

1. **Id** = `slug(feature).slug(scenario name)`; a tag `@id:<name>` overrides the scenario part so a rename does
   not orphan the proof. Duplicate ids are an error.
2. **Parameters**: each `<x>` becomes a bound variable typed by its slot. Conflicting slot types: `E_TYPE`.
   Literals go through `lean_literal`; enum keys become constructors.
3. **Actors**: each distinct actor name, in order of first mention, is a variable of the actor's Lean type. Each
   actor the When returns also gets a primed post variable.
4. **Exactly one When** (`E_WHEN` otherwise). Givens must precede it and Thens follow it (`E_ORDER`). At least one
   Then (`E_NOTHEN`).
5. Emit into `Wallet/Statements.lean`:

   ```
   def <id>.stmt : Prop :=
     ∀ (params) (actors), G_1 → … → G_k →
       ∃ (outcome) (post actors), <call> = ok (outcome, post actors…) ∧ T_1 ∧ … ∧ T_m
   ```

   This is the Hoare triple `{G} call {T}` in total-correctness form: for every input satisfying the Givens the
   Rust function returns (no panic, no divergence) and the result satisfies every Then. The form uses no Aeneas
   notation, so a reader needs only `∀`, `→`, `∃`, `∧`.
6. **Scope**. Outline: `universal`; Examples columns are `∀`-bound and the rows leave the statement. Plain
   Scenario: `instance`; no parameters, literals inline, actors still `∀`-bound under their Givens.
7. **Output columns**. A placeholder that first appears in a Then has no defining relation: `E_OUTPUT_COLUMN`,
   with the hint to phrase the Then relationally or tag the outline `@examples-only`. With that tag the outline
   expands to one `instance` statement per row (`<id>.row<N>.stmt`).
8. Emit into `Wallet/Checks.lean`, per statement:
   - `<id>.check (params) (actors) : Bdd.Check` - `.givenFalse` if a Given is false, else
     `Bdd.run <call> (fun (outcome, posts…) => decide (T_1 ∧ … ∧ T_m))`, where `Bdd.run` observes through
     `Result.match` and returns `.pass | .thenFalse | .panicked | .diverged` [observed working];
   - one evaluation per Examples row, actors built with the `builds` entries;
   - `theorem <id>.sat : ∃ params actors, G_1 ∧ … ∧ G_k`, from the first row that is not `.givenFalse`, closed by
     `by simp [<vocab defs used>]; scalar_tac` (not `decide`, which sticks on `U64.max`) [observed].
9. `Wallet/Proofs.lean`: if `theorem <id>` is missing, append `theorem <id> : <id>.stmt := by sorry`. Existing text
   is never touched. A theorem whose id has gone is reported as an orphan.
10. Unsupported Gherkin (doc strings, data tables, several Whens) is a hard error naming the line.
    (`Rule:` was in this list until section 13; several Whens until section 12.)

`lean/Bdd/Basic.lean` (fixed, about 40 lines) holds `Bdd.Check`, `Bdd.run`, and the bridge lemmas
`Bdd.ok_of_spec`, `Bdd.ok2_of_spec`, `Bdd.ok3_of_spec` (one per return arity in use):

```lean
theorem ok3_of_spec {m : Result (α × β × γ)} {Q : α → β → γ → Prop}
    (h : Std.WP.spec m (fun r => Q r.1 r.2.1 r.2.2)) : ∃ a b c, m = ok (a, b, c) ∧ Q a b c
```

### Worked example A - Scenario Outline, universal [statement and proof observed to check]

```gherkin
Feature: Wallet transfers

  Scenario Outline: A covered transfer moves the money and conserves the total
    Given Alice has a balance of <a>
    And Bob has a balance of <b>
    And <amount> is not more than Alice's balance
    And Bob's balance plus <amount> does not exceed the maximum
    When Alice transfers <amount> to Bob
    Then the operation succeeds
    And Alice's balance is decreased by <amount>
    And Bob's balance is increased by <amount>
    And the total of all balances is unchanged
    Examples:
      | a   | b  | amount |
      | 100 | 20 | 30     |
      | 5   | 0  | 5      |
```

```lean
def wallet_transfers.a_covered_transfer_moves_the_money_and_conserves_the_total.stmt : Prop :=
  ∀ (a b amount : U64) (alice bob : wallet.Wallet),
    Vocab.hasBalance alice a →
    Vocab.hasBalance bob b →
    Vocab.covers alice amount →
    Vocab.roomFor bob amount →
    ∃ (outcome : Vocab.Outcome) (alice' bob' : wallet.Wallet),
      wallet.transfer alice bob amount = ok (outcome, alice', bob') ∧
      Vocab.succeeds outcome ∧
      Vocab.decreasedBy alice alice' amount ∧
      Vocab.increasedBy bob bob' amount ∧
      Vocab.totalUnchanged [alice, bob] [alice', bob']
```

Proof that checked in the probe (axioms `propext, Classical.choice, Quot.sound`):

```lean
  intro a b amount alice bob h1 h2 h3 h4
  apply Bdd.ok3_of_spec
  unfold wallet.transfer
  step*
  simp [Vocab.hasBalance, Vocab.decreasedBy, Vocab.increasedBy, Vocab.totalUnchanged] at *
  scalar_tac
```

The two rows give: two cucumber cases on the compiled Rust, two `check` evaluations on the Lean model (both
`.pass` in the probe; a row with `amount = 6`, `a = 5` gave `.givenFalse`), and the `.sat` witness.

### Worked example B - plain Scenario, instance

```gherkin
  Scenario: Transferring more than you have is rejected and changes nothing
    Given Alice has a balance of 10
    And Bob has a balance of 7
    When Alice transfers 11 to Bob
    Then the operation is rejected with insufficient funds
    And Alice's balance is unchanged
    And Bob's balance is unchanged
```

```lean
def wallet_transfers.transferring_more_than_you_have_is_rejected_and_changes_nothing.stmt : Prop :=
  ∀ (alice bob : wallet.Wallet),
    Vocab.hasBalance alice (10#u64) →
    Vocab.hasBalance bob (7#u64) →
    ∃ (outcome : Vocab.Outcome) (alice' bob' : wallet.Wallet),
      wallet.transfer alice bob (11#u64) = ok (outcome, alice', bob') ∧
      Vocab.rejectedWith outcome wallet.WalletError.InsufficientFunds ∧
      Vocab.unchanged alice alice' ∧
      Vocab.unchanged bob bob'
```

Reported as PROVED-INSTANCE: kernel-checked, one input. The all-inputs version is the same text as an Outline with
`<a> <b> <amount>` and the Given "`<amount>` is more than Alice's balance"; its proof in the probe was
`apply Bdd.ok3_of_spec; unfold wallet.transfer; step*`.

### Worked example C - a false scenario [refutation observed to check]

Delete the fourth Given from example A. The statement still generates and is false. Search finds
`a = 1, b = 18446744073709551615, amount = 1`; the model returns `Err Overflow`; "the operation succeeds" fails.
The generated refutation has this shape:

```lean
theorem <id>.refuted : ¬ <id>.stmt := by
  intro h
  obtain ⟨o, a', b', e, t⟩ := h 1#u64 18446744073709551615#u64 1#u64
      (Vocab.mkWallet 1#u64) (Vocab.mkWallet 18446744073709551615#u64) (by decide) (by decide) (by decide)
  have w : ∃ o a' b', wallet.transfer (Vocab.mkWallet 1#u64) (Vocab.mkWallet 18446744073709551615#u64) 1#u64
             = ok (o, a', b') ∧ ¬ Vocab.succeeds o := by
    apply Bdd.ok3_of_spec; unfold wallet.transfer; step*
    simp [Vocab.mkWallet] at *; scalar_tac
  obtain ⟨o2, a2, b2, e2, t2⟩ := w
  rw [e] at e2; simp at e2
  exact t2 (e2.1 ▸ t)
```

The middle step (`w`) says "at this input the call returns something that fails the Then", proved with the same
`step*` machinery as a positive proof. That is the general recipe, since the model cannot be reduced by `decide`.

### Worked example D - frame substitution

`When Alice deposits <n>` / `Then Bob's balance is unchanged`: `W-deposit` returns only Alice, so the Then renders
as `Vocab.unchanged bob bob`, flagged `frame-trivial` in the report.

---

## 6. Checks and verdicts

### 6.1 Verdict Clausebook

One verdict per scenario; first match in this order wins.

| Verdict | Meaning | Evidence it reports |
|---|---|---|
| `UNBOUND` | a step matches no glossary entry of its kind; no statement emitted | file:line, three nearest phrases, paste-ready YAML stub |
| `AMBIGUOUS` | a step matches two or more entries | the entries |
| `UNSUPPORTED` | `E_TYPE`, `E_WHEN`, `E_ORDER`, `E_NOTHEN`, `E_OUTPUT_COLUMN`, literal out of range, unsupported Gherkin | the rule and line |
| `STALE` | a hash on the scenario's chain differs from the one its evidence was computed from | what changed; previous verdict shown struck through |
| `VACUOUS` | `theorem <id>.unsat : ¬ ∃ …, G_1 ∧ … ∧ G_k` is kernel-checked | theorem name; smallest contradictory set of Givens |
| `VACUOUS-SUSPECTED` | no assignment satisfying the Givens found in rows or grid; `.unsat` not proved | assignments tried |
| `REFUTED` | `theorem <id>.refuted : ¬ <id>.stmt` kernel-checked with clean axioms | counterexample in Gherkin terms |
| `COUNTEREXAMPLE` | search found a failing input; kernel confirmation failed or not attempted | counterexample; "tested on the Lean model" |
| `PROVED-FOR-ALL` | `theorem <id>` has clean axioms, `<id>.sat` exists, scope `universal` | full chain, see 6.4 |
| `PROVED-INSTANCE` | the same, scope `instance` | "holds for THIS input" |
| `TESTED-ONLY` | no complete proof, Givens satisfiable, no counterexample | rows passed on Rust / on model, N grid points, seed |

Flags that attach to any verdict:

- `MODEL/GLUE MISMATCH` (top-level alarm): a row passes under cucumber-rs and fails under the Lean check, or the
  reverse. Cause is the translation or a divergence between a step body and its Vocab definition.
- `UNREVIEWED GLOSSARY (n of m)`: some phrase used is unsigned or changed since sign-off.
- `TRIVIAL-THEN`: `∀ …, G → T` is provable with the outcome and post-states arbitrary.
- `FRAME-TRIVIAL`: a Then conjunct mentions only pre-states because the call does not return that actor.
- `ROW OUTSIDE GIVENS`: an Examples row gives `.givenFalse`; it tests nothing.
- `NOT RUNNABLE AS TEST`: an actor has no constructive Given (`builds`), so rows cannot build it.
- `NO SEARCH`: a phrase used is `checkable: false`.
- `COMPILER-TRUSTED`: the proof's axioms include `Lean.ofReduceBool` (`native_decide`).

A proof with `sorryAx` counts as no proof. A proved statement with no `.sat` is never shown as proved.

Exit code is non-zero for UNBOUND, AMBIGUOUS, UNSUPPORTED, STALE, VACUOUS, REFUTED, COUNTEREXAMPLE and
MODEL/GLUE MISMATCH.

### 6.2 Counterexample search

Run for every scenario without a complete proof. `lake exe audit` evaluates `<id>.check` on:

1. every Examples row;
2. the boundary grid: product of each parameter type's `sample` list, plus every literal in the scenario and its
   neighbours, capped at 20,000 tuples; actors built through `builds`, and for actors with no constructive Given,
   through the actor type's sample values;
3. 2,000 seeded pseudo-random tuples.

The first `.thenFalse`, `.panicked` or `.diverged` is shrunk toward small sample values. Each Then conjunct is
then evaluated separately to list failed and held Thens. The report prints the witness as a pasteable Examples row.
`clausal` then appends the refutation theorem of example C; if it compiles the verdict is REFUTED, otherwise
COUNTEREXAMPLE with "kernel confirmation attempted and failed".

Report text:

```
REFUTED  Scenario Outline: A covered transfer moves the money ...     (wallet.feature:3)
  counterexample (kernel-checked: wallet_transfers.<id>.refuted)
    | a | b                    | amount |
    | 1 | 18446744073709551615 | 1      |
    When Alice transfers 1 to Bob   =>  returned Err Overflow; Alice and Bob unchanged
    failed Then: "the operation succeeds"; "Alice's balance is decreased by <amount>"; "Bob's balance is increased by <amount>"
    held   Then: "the total of all balances is unchanged"
```

### 6.3 Glossary audit (in `lake exe audit`, read from the Lean environment)

- For each Given/Then definition: collect transitive constants; fail if any is a `lean_name` of a function in
  `translation.json`.
- For each statement: the constants it uses are exactly the glossary definitions of its steps, the When's `call`,
  and `ok` / logical connectives. Anything else means the generator misbehaved.
- For each theorem: `Lean.collectAxioms`.
- Dead phrases (bound, unused) are warnings.

### 6.4 The line printed for a proved scenario

Never shortened to one tick:

```
PROVED-FOR-ALL  A covered transfer moves the money and conserves the total
  kernel-checked   theorem wallet_transfers.<id>; axioms propext, Classical.choice, Quot.sound; Givens satisfiable (<id>.sat)
  about            the Lean model wallet.transfer, not the Rust
  tool-trusted     model = Rust: rustc 1.100.0-nightly, charon 0.1.315, aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used: U64.checked_add, U64 subtraction
  tool-trusted     statement generated by clausal <sha>; printed below for comparison with the scenario
  human-asserted   9 glossary phrases, 9 reviewed (will, 2026-11-09)
  tested           2 rows pass on compiled Rust (cucumber-rs); 2 rows pass on the Lean model; they agree
```

---

## 7. Refinement-graph schema (`out/graph.json`)

> **Superseded.** This section describes version 1. The graph is now emitted in version 2, described in
> `../docs/SCHEMA.md` (section 7 there lists what changed and why). Kept for the record.

A **node** is anything with an interface (what others rely on) and, optionally, an implementation (what makes it
so). An **edge** is a claim relating two nodes. Every claim, including "this implementation realises this
interface", carries a list of evidence entries.

```json
{
  "schema": "rosette.refinement-graph/1",
  "generated_at": "ISO-8601",
  "toolchain": { "lean": "", "mathlib": "", "aeneas": "", "charon": "", "rustc": "", "generator": "" },
  "nodes": [ {
    "id": "stable string, e.g. scenario:wallet_transfers.<slug> | phrase:G-balance | def:Vocab.hasBalance | stmt:<id>.stmt | fn:lean:wallet.transfer | fn:rust:wallet::transfer | libmodel:U64.checked_add | row:<id>#2 | lemma:<Lean name>",
    "kind": "claim | phrase | definition | statement | function | library_model | example",
    "interface": {
      "language": "gherkin | english | lean | rust",
      "text": "scenario text, phrase pattern, Lean Prop or signature, Rust signature",
      "text_unfolded": "statements only: the Prop with glossary definitions unfolded",
      "source": { "file": "", "line_start": 0, "line_end": 0 },
      "sha256": "of text, whitespace-normalised"
    },
    "implementation": null,
    "attrs": { "scope": "universal | instance", "tags": [], "size": 0 }
  } ],
  "edges": [ {
    "id": "string",
    "from": "node id", "to": "node id",
    "relation": "formalises | composed_of | binds | uses | translates | models | instance_of | refutes | exercises | lifted_from | generalises",
    "evidence": [ { "$ref": "#/evidence" } ]
  } ],
  "verdicts": [ {
    "node": "scenario or claim node id",
    "status": "one of section 6.1",
    "flags": [],
    "chain": ["edge ids, from the claim down to the Rust function"],
    "rests_on": ["kernel-checked", "tool-trusted", "human-asserted", "tested"],
    "counterexample": null
  } ]
}
```

`implementation`, when present:

```json
{ "language": "lean-proof | lean-def | rust",
  "ref": "Lean constant name or Rust path",
  "source": { "file": "", "line_start": 0, "line_end": 0 },
  "sha256": "",
  "complete": true,
  "realises": [ { "$ref": "#/evidence" } ] }
```

`evidence` entry:

```json
{ "kind": "kernel-checked | tested | tool-trusted | human-asserted",
  "by": "lean-kernel | lean-eval | cucumber-rs | boundary-search | charon+aeneas | aeneas-library | clausal | extract_goal | reviewer:<name> | UNREVIEWED",
  "artifact": "theorem name, log path, sign-off record id",
  "axioms": ["kernel-checked only"],
  "scope": "all-inputs | n examples | n samples | n/a",
  "inputs_sha256": ["hash of every node text this evidence was computed from"],
  "stale": false,
  "witness": null,
  "detail": "" }
```

An edge or `realises` list with no entries means "claimed, no evidence"; there is no `none` kind.

### Relations and the evidence each may carry

| Relation | From -> to | Evidence allowed |
|---|---|---|
| `composed_of` | scenario claim -> phrase | tool-trusted (`clausal` match) |
| `binds` | phrase -> definition | human-asserted only (reviewer or UNREVIEWED); a second entry for the `steps.rs` reading |
| `formalises` | statement -> claim | tool-trusted (`clausal`, translation rule version) **and** human-asserted (derived from the `binds` edges it rests on) |
| `uses` | statement -> definition / function / lemma | kernel-checked (constants in the elaborated term) |
| `translates` | Lean function -> Rust function | tool-trusted (`charon+aeneas`); may add tested (row agreement between cucumber-rs and lean-eval); never kernel-checked |
| `models` | library model -> std Rust function | tool-trusted (`aeneas-library`, hand-written) |
| `instance_of` | example row -> statement | kernel-checked by instantiation once the statement is proved; tested entries from each runner |
| `refutes` | statement (`¬ stmt`, with proof) -> statement | kernel-checked, with witness; or tested, with witness |
| `exercises` | example row -> function | tested |
| `lifted_from` | lemma -> lemma | tool-trusted (`extract_goal`), becoming kernel-checked when the parent re-checks using the lemma |
| `generalises` | lemma -> lemma | kernel-checked by an instantiation proof |

Node-internal `realises`:

- statement / lemma: proof realises Prop - kernel-checked with axioms; `sorryAx` means the list is empty;
  `Lean.ofReduceBool` is recorded as tool-trusted (`lean-compiler`).
- satisfiability is a second statement node (`<id>.sat`) with its own proof, linked by `uses`.

### Fit to the maths side

| Software slice | Maths lemma graph |
|---|---|
| `claim` in Gherkin | `claim` in English (a paper's sentence, a blueprint entry) |
| `statement` with a proof | `statement` = lemma with a proof |
| `phrase` + `definition` + `binds` | informal term + Lean definition + `binds` (the same human-asserted gap) |
| `formalises` (human-asserted + tool-trusted) | `formalises` (human-asserted; tool-trusted if autoformalised) |
| `uses` | lemma depends on lemma |
| `translates`, `models`, `exercises` | not used |
| - | `lifted_from`, `generalises` |
| `attrs.size` unused | `attrs.size` = proof size, for the cognitive-bottleneck gate |

The verdict record applies unchanged to an informal claim: PROVED-FOR-ALL, STALE, VACUOUS (hypotheses of a lifted
lemma are contradictory) and TESTED-ONLY (checked on instances) all carry over. This fit is argued, not yet
demonstrated on a real lifted-lemma export.

---

## 8. Implementation plan (ordered)

Each step ends with something that runs. Use `lake build` inside `clausal/lean` only; never touch the repo root.

1. **Wallet crate and translation.** Add `clausal/wallet/` (enum named `WalletError`, no derives). Extend
   `translate.sh` to a crate list. Done when `Generated/Wallet.lean` matches `probe/Wallet.generated.lean` up to
   the enum rename and `provenance.json` covers both crates.
2. **Fixed Lean support.** `Bdd/Basic.lean` (bridge lemmas for arities 1-3, `Check`, `run`) and `Wallet/Vocab.lean`
   from section 4.1; add the `Bdd` and `Wallet` libraries to `lakefile.toml`. Lift the lemmas from `probe/`.
3. **Hand-write one statement and proof** (worked example A) in the final file layout, to fix the exact text the
   generator must emit. Done when `lake build` is green with clean axioms.
4. **`clausal gen`, statements only.** Gherkin subset parser, YAML loader, matcher, emitter for
   `Statements.lean`, proof stubs. Golden test: output for example A equals the hand-written statement of step 3.
   UNBOUND / AMBIGUOUS / UNSUPPORTED errors with file:line.
5. **Feature file with five scenarios**: example A; the universal insufficient-funds rejection; the universal
   overflow rejection; example B (instance); example C (deliberately false, tagged `@expect-refuted` so the run
   exits zero). Plus one scenario with contradictory Givens and one with an unbound step, kept in
   `features/negative.feature`, to exercise VACUOUS and UNBOUND.
6. **Proofs** for the true scenarios in `Wallet/Proofs.lean`. Record minutes of effort per scenario in the report;
   proof cost per scenario is one of the things this probe measures.
7. **`Checks.lean` and `lake exe audit`**: row evaluation, `.sat` theorems, boundary search, axiom collection,
   glossary audit (6.3), JSON out.
8. **Refutation and vacuity scaffolds**: generate `.refuted` from a found witness and `.unsat` stubs; trivial-Then
   check.
9. **`clausal report`**: `graph.json` (validate against the schema), `report.md` with the glossary table,
   statements beside scenarios, verdict blocks. Sign-off command and staleness.
10. **cucumber-rs runner** (`wallet-bdd/`): `steps.rs`, regex identity check, JSON output merged into the report,
    MODEL/GLUE MISMATCH. This adds crates.io dependencies (cucumber, tokio); log them in `DECISIONS.md`.
11. **Maths-side fit test**: export one small lifted-lemma graph from the root project's data into this schema by
    hand (read-only use of root files) and record what did not fit.

Steps 1-6 already give a kernel-checked verdict per scenario. Steps 7-9 make false, vacuous and unbound scenarios
report correctly. Step 10 delivers "same file as ordinary tests". Step 11 tests the schema claim.

---

## 9. Known limits and things not verified

- **The glossary can still be wrong.** A Given that is too strong or a Then that is too weak gives a green proof
  of the wrong claim. Small definitions, the model-function ban, sign-off hashes and the trivial-Then check
  reduce this; the edge stays human-asserted.
- **Two readings of each phrase** (Vocab.lean and steps.rs). Identical regexes keep matching in sync, not meaning.
  Row disagreement is the only automatic check. A later option is to generate the Rust test harness from the
  glossary and evaluate Thens in Lean on the observed outcomes, which removes the second reading; not designed here.
- **The generator is untrusted.** A bug could emit a statement that does not match the scenario. Defences: the
  audit's constant check (6.3) and the statement printed beside the scenario.
- **Universal reading changes how scenarios must be written**: relational Thens and explicit precondition Givens.
  Features written with expected-value columns fall back to `@examples-only`.
- **One When, named actors, no tables or sequencing.** Multi-step scenarios need chaining through intermediate
  states; that is a real extension.
- **Search is bounded.** A false scenario whose counterexamples are all away from boundaries is TESTED-ONLY.
- **Proof automation is shown on two statements only.** `step*` + `scalar_tac` worked for transfer success and
  rejection; nothing is known for loops or richer state.
- **The auto-generated refutation script is shown on one case.** The recipe is general in form; the closing
  tactics may need variants.
- **Not checked**: the trivial-Then check, the `.unsat` proof by `scalar_tac`, `Lean.collectAxioms` from a
  `lake exe` on this toolchain, cucumber-rs on the pinned nightly, Aeneas output for `deposit`/`withdraw` under
  `step*`, and Lake tracking of the `.feature` file (the hash check in the report covers staleness meanwhile).
- **AGENTS.md rule 1.** The probes used seven one-off `lake env lean` runs (about 3 s each), not a loop. The warm
  bridges the rule names no longer exist; if proof search over scenarios is ever automated in a loop it needs a
  warm server on the slice's Lean v4.35.0.

---

## 10. Implementation notes (added after the build)

`./run.sh` runs the whole chain; `README.md` has the layout. Verdicts on the eight scenarios: 4 PROVED-FOR-ALL,
1 PROVED-INSTANCE, 1 REFUTED (kernel-checked, counterexample `a = 1, b = 18446744073709551615, amount = 1`),
1 UNBOUND, 1 VACUOUS (kernel-checked `.unsat`).

### Differences from sections 3-8

- **The old `rust/` crate (`checked_add`) was replaced by `wallet/`**, not kept beside it. `translate.sh` still
  handles one crate.
- **No `lake exe audit`.** A native executable importing the model would need every transitive module (Mathlib
  included) compiled to object code. Instead two generated scripts are run once each with `lake env lean`
  (interpreter): `Run/Search.lean` (row evaluation, grid search) and `Run/Audit.lean` (derived theorems, then
  `Lean.collectAxioms` and constant collection via `#eval`). Two batch invocations per run, about 3 s each, no loop.
- **Derived theorems live in `Run/Audit.lean`, not in a library module**: `.sat`, `.unsat`, `.refuted` and one
  `.trivial_k` per Then. A script that fails is elaborated with `sorryAx`; the audit reads axioms, so a failed
  derived theorem counts as absent. The trivial-Then attempts are expected to fail and their errors are in
  `out/audit.log`.
- **Scenario ids are `Spec.<feature>.<scenario>`**, because a feature called "Wallet" would otherwise put statements
  in the generated model's `wallet` namespace.
- **No proof stub is appended for a scenario tagged `@expect-refuted` or `@expect-vacuous`.**
- **A broken `Proofs.lean` does not stop the run.** The model, statements and checks must build; if the proofs
  do not, the run continues without them, every scenario loses its proof, and the report says so and exits 1.
- **Search is the boundary grid only**: no random tuples, no shrinking (the grid is ordered small values first).
  Actors with no constructive Given get a hidden grid parameter.
- **STALE is not implemented.** Every run regenerates and rechecks everything. Evidence entries carry
  `inputs_sha256` so a later incremental mode could compute it.
- **`text_unfolded` is not produced.**
- **Graph additions**: node kind `feature` and relation `contains`; optional `attrs` on edges; `source.term_path`;
  verdict fields `expected` and `as_expected`. The `by` field is an open string. The schema is now a JSON Schema
  file, `schema/refinement-graph.schema.json`, and `clausal report` validates `graph.json` against it. The schema
  itself forbids kernel-checked evidence on `binds`, `formalises`, `translates` and `models` edges.
- **Sign-off exists but nobody has signed**: every glossary entry shows UNREVIEWED. That is the true state.
- **Proof effort**: all five proofs were accepted at the first attempt, 4 to 6 lines each, same recipe.

### Checks of the checks (run by hand, then reverted)

| Change | Result |
|---|---|
| Rust mutant: `deposit` also rejects a sum equal to `u64::MAX`. Unit tests and every Examples row still pass. | `Proofs.lean` stops compiling; search finds `a = 0, amount = 18446744073709551615`; "A deposit does not touch a bystander" becomes REFUTED once the refutation script was given two more closing tactics (first attempt: COUNTEREXAMPLE, kernel confirmation failed); the other proved scenarios drop to TESTED-ONLY; exit 1. |
| One proof replaced by `sorry` | that scenario TESTED-ONLY ("proof incomplete (sorry)"); exit 1 |
| A Rust step body changed to disagree with its Lean definition | MODEL/GLUE MISMATCH on every scenario using the phrase; exit 1 |
| A glossary definition that mentions a model function | not reached through `run.sh`: the definition was not decidable, so `Checks.lean` failed to build. The ban itself was confirmed with a one-off script: `model_deps` listed `wallet.Wallet.withdraw` through one level of indirection. |

### Maths-side fit test (plan step 11)

`schema/maths_fit.py` reads the root project's `out/rosette_tests_candidates.jsonl` (read-only) and writes the
candidate tree of `Polynomial.card_roots'` (16 nodes, 15 `lifted_from` edges) as
`schema/maths-example.graph.json`; it validates against the same JSON Schema. What fitted and what did not:

- Fitted unchanged: a lemma is a `statement` node (interface = the Prop, implementation = a proof);
  parent/child is `lifted_from`; evidence kinds and the "empty list = claimed, no evidence" rule.
- **A candidate is not yet a lemma.** Its implementation is a sub-term of the parent's proof, located by a term
  path, not a source range. Added `source.term_path`; marked with `attrs.candidate`. Its statement comes from type
  inference and this export records no standalone kernel check, so the evidence is tool-trusted, not kernel-checked.
- **Edges needed attributes** (the role of the sub-term: `arg`, `haveValue`, `lamBody`, ...). Added optional `attrs`.
- **`by` could not be a closed list**: the maths side does not use `extract_goal`; it works on proof terms.
- **Hashes differ**: the maths side has a 16-hex `stmtHash` of the expression; the schema wants sha256 of
  whitespace-normalised text. Both are kept (`interface.sha256`, `attrs.stmtHash`). One should be chosen.
- **Metrics have no home** except free-form `attrs` (`hidingRatio`, `proofSizeDag`, `proofSizeTree`,
  `statementSize`). `attrs.size` alone is ambiguous between DAG and tree size.
- The claim / phrase / `formalises` layer and the `verdicts` list are empty for this export. Nothing on the maths
  side currently produces an English claim per lemma, so that half of the schema is untested there.
- Not tried: the lifted-lemma output of `Rosette/Demo.lean` (kernel-checked lemmas, `generalises` edges).

---

## 11. After the reviews (added 2026-11-09)

Two reviews of the build (evidence in `review/`) led to these changes. Sections 3 to 10 above are not rewritten;
where they disagree with this section, this section is current.

- **Proof type check.** `Bdd.Audit.report` now reports, per theorem, whether its type is exactly the expected
  constant (`<id>.stmt`, or `¬ <id>.stmt` for a refutation), whether it is a theorem, and which module declares
  it. A scenario proof counts only if all three are right. Derived theorems must be declared in the audit script.
- **One proof module per scenario** (`lean/Wallet/Proofs/<feature>/<scenario>.lean`) replaces `Proofs.lean`.
  `lake build` builds every module it can; `clausal proofs` reads its log and `Run/Audit.lean` imports only the
  modules that compiled.
- **Four more universal scenarios**, so that each operation's proved scenarios cover every input, and a generated
  **coverage theorem** per group of scenarios: `∀ <the When's inputs>, ∃ <other parameters>, <constructive Givens>
  ∧ (<rest of scenario 1> ∨ <rest of scenario 2> ∨ ...)`. Nothing is assumed; the theorem exhibits the parameters.
- **The second reading of each Given/Then phrase is a pure Rust predicate** (`wallet-bdd/src/lib.rs`) that the
  cucumber step asserts. Each is evaluated on the same argument grid as the Lean definition and compared.
- **Counterexample replay**: each found counterexample is written as a literal scenario to
  `build/replay/replay.feature` and run by cucumber-rs.
- **`--strict`**, a headline that counts substantive Thens, and a sign-off record that stores the digests of the
  phrase (with its argument order) and of the definition.
- **Mutation harness** (`mutation/`), run on demand, with the negative controls that section 10 ran by hand.
- **Graph schema version 2** (`../docs/SCHEMA.md`); `clausal/graphlint.py` holds the lint and the staleness rule.

Still as in section 10: the audit is two `lake env lean` scripts, search is the boundary grid only, and
`translate.sh` handles one crate.

---

## 12. The ledger: loops, a collection, several Whens (added 2026-11-10)

A second crate, `ledger/` (85 lines), was added beside the wallet to test the slice on code that is not
straight-line: a `Vec<u64>` of balances, a `&[Transfer]` batch, two `while` loops, a call from inside a loop,
`Vec::clone`. `./run.sh` covers both crates. Sections 1 to 11 are not rewritten; where they say "one crate",
"one When" or "the wallet", this section is current.

### 12.1 What Aeneas generates for a loop [observed]

Not a recursive function. For

```rust
pub fn apply_batch(&mut self, batch: &[Transfer]) -> usize {
    let mut i = 0;
    while i < batch.len() {
        if !self.apply(&batch[i]) { break; }
        i += 1;
    }
    i
}
```

the output is three definitions (`lean/Generated/Ledger.lean`):

```lean
@[rust_loop_body]
def Ledger.apply_batch_loop.body (batch : Slice Transfer) (self : Ledger) (i : Std.Usize) :
    Result (ControlFlow (Ledger × Std.Usize) (Std.Usize × Ledger)) := do
  let i1 := Slice.len batch
  if i < i1
  then
    let t ← Slice.index_usize batch i
    let (b, self1) ← Ledger.apply self t
    if b
    then let i2 ← i + 1#usize
         ok (cont (self1, i2))
    else ok (done (i, self1))
  else ok (done (i, self))

@[rust_loop]
def Ledger.apply_batch_loop (self : Ledger) (batch : Slice Transfer) (i : Std.Usize) :
    Result (Std.Usize × Ledger) := do
  loop (fun (self1, i1) => Ledger.apply_batch_loop.body batch self1 i1) (self, i)

@[reducible]
def Ledger.apply_batch (self : Ledger) (batch : Slice Transfer) : Result (Std.Usize × Ledger) := do
  Ledger.apply_batch_loop self batch 0#usize
```

- The loop state is the tuple of what the loop changes; `cont` carries the next state, `done` the result of the
  whole function (a `break` and an early `return` both become `done`).
- `loop` is `Aeneas.Std.loop`, defined with `partial_fixpoint`. Consequences: `decide` and `rfl` cannot run it;
  `simp` with its unfolding equation does not terminate usefully; the Lean interpreter does run it, so row
  evaluation and the counterexample search work unchanged (4 s for all 29 statements).
- `Vec<T>` is a structure wrapping `Slice T`, itself a length-indexed list with a bound proof; `.val` gives the
  `List`. Indexing is `alloc.vec.Vec.index (SliceIndexUsizeSlice U64) v i` and fails (panics) out of bounds; a
  write is `index_mut`, which returns the old value and a "back" function that `step*` resolves to `Vec.set`.
- The proof rule is `Aeneas.Std.loop.spec_decr_nat measure invariant`: show that the body, from a state satisfying
  the invariant, either finishes with the postcondition or continues in a state satisfying the invariant with a
  smaller measure. Inside it, `unfold <fn>_loop.body; step*` behaves as on straight-line code.

### 12.2 What changed in the design

- **Two crates, one glossary, one statements file.** `translate.sh` takes a crate list; `lean/translation.json`
  is the merge, with a `crate` field. The glossary gained 28 ledger entries (ids `LG-`, `LW-`, `LT-`), whose
  definitions are in `lean/Ledger/Vocab.lean` (namespace `LVocab`). Statements of every feature are still
  generated into `lean/Wallet/Statements.lean` and proofs live under `lean/Wallet/Proofs/<feature>/`; the
  library name `Wallet` is now a misnomer, kept so the wallet's nine proof files did not have to change.
- **Literals for collections.** A parameter type is a scalar (`literal_regex`, `lean_literal: '{0}#u64'`), a
  record (`fields: true`: the regex groups fill `{0} {1} ...`, e.g. `0->1:30`), or a list (`list_of: <type>`,
  written `[a, b]`, `lean_literal: '[{items}]'`). Universal statements quantify over `List U64` and
  `Slice ledger.Transfer` directly, so "for all batches and all ledgers" is literally `∀ batch main`.
- **The result type of a Then is checked.** Operations now return different things (`Usize`, `Option U64`,
  `Bool`, the wallet's `Outcome`). A Then that speaks about the result declares `outcome_type`; binding it to a
  When that returns something else is `UNSUPPORTED E_TYPE`, not a Lean type error in the generated file.
- **Several Whens (translation rule version 2).** Steps must be `Given*, When+, Then+`. For Whens `W1 .. Wn`:

  ```
  ∀ params actors, G_1 → … → G_k →
    ∃ out_1, call_1 = ok out_1 ∧
    ∃ out_2, call_2 = ok out_2 ∧ …
    ∃ out_n, call_n = ok out_n ∧ T_1 ∧ … ∧ T_m
  ```

  `pre(x)` in a When is the actor's current state (what the latest earlier When handed back, else the initial
  one); in a Given or Then, `pre(x)` is the state before the first When and `post(x)` the state after the last
  When that returns x; `outcome` is the last When's result. Outputs of an earlier When are named `outcome_k`,
  `x_k`. With one When the emitted text is exactly what version 1 emitted (the wallet statements are unchanged).
  This is the smallest extension that is sound: it claims every call returns, and nothing about intermediate
  results. Not supported, and reported as such: a Then between two Whens (`E_ORDER`); a kernel refutation for a
  multi-When scenario (a counterexample is reported as COUNTEREXAMPLE); input coverage. The cucumber side needed
  one change: When steps read the current state, not the initial one.
- **Hand-written lemma library** `lean/Ledger/Lemmas/` (modules `Basic`, `Apply`, `Batch`, `Total`, `Balance`,
  `All`: one per Rust function, so that a change to one function costs only the scenarios about it their proofs),
  imported by the ledger proof modules and (glossary `audit_imports`) by the generated audit script. It is not
  trusted and appears in no statement. If a module does not compile, every proof module that depends on it,
  directly or not, is reported as lost with the module's name; the other proofs are unaffected. (It was first one
  file; a mutant in `total` then cost all sixteen ledger scenarios their proofs, which said nothing useful.)
- **Refutation through a loop.** The generated script now tries `unfold <call>; step*` and, failing that, `step*`
  on the call itself, which uses a registered `@[step]` lemma if one is imported. See 12.4.
- **The audit** lists, per model function, the constants it reaches through other model functions, so a function
  whose loop body uses `checked_add` shows that library model, and the report knows which calls contain a loop.

### 12.3 The scenarios and their verdicts

*(Counts corrected after the adversarial review, which found this paragraph miscounted; and four scenarios were
added in response to it, see 12.8.)* At the time of the review there were 19 ledger scenarios (13 PROVED-FOR-ALL,
4 PROVED-INSTANCE, 2 REFUTED), not 18 and 12 as first written here. There are now 23: 13 universal single-When,
3 universal with two Whens, 5 with literal values, 2 deliberately false. All get their expected verdict:
16 PROVED-FOR-ALL, 5 PROVED-INSTANCE, 2 REFUTED (kernel-checked, both found by the grid search, both pass all
their example rows, both replayed on the compiled Rust). With the wallet's 10 and the 2 negative controls that
is 35 scenarios.

The five asked for: (1) `batch_conserves` - any batch on any ledger conserves the total; (2) `batch_first_invalid`;
(3) `batch_count_bounded`; (4) `batch_all_valid_all_applied` (false: transfers each valid on the starting ledger
need not all be applied; counterexample balances `[1, 0]`, batch `[0->1:1, 0->1:1]`) and `total_always_available`
(false: counterexample `[18446744073709551615, 1]`); (5) `batch_then_total` (apply a batch, then compute the
total: the result is the sum before the batch - two Whens, both loops) and `two_batches_conserve`.

### 12.4 Proof effort (honest log)

Counted in `lake build` attempts of the file concerned (2 to 5 s each); "failed" means the build reported an
error. Elapsed time was not instrumented; the figures in the last column are estimates from the session.
**The line counts in this table were understated; the review recounted them, and 12.8 gives the mechanical
count (`python3 effort/count.py`): 227 code lines of lemmas, not "about 205", and about 6 lines of hand-written
Lean per code line of Rust once proofs and glossary definitions are included, not 2.4 or 4.** Attempt counts
below are the builder's own tally and cannot be checked against any file; from the review fixes on, attempts
are logged by `./lakebuild.sh` in `effort/attempts.tsv`.

| Piece (hand-written) | Lines | Builds until accepted (failed) | What went wrong on the way |
|---|---|---|---|
| `Ledger.apply.spec` (no loop; `Vec` reads and writes): valid -> moved, total kept; invalid -> unchanged | 32 with the exact part | 4 (2), then 5 (4) more for the exact part | `l[i]!` in the glossary versus `l[i]` produced by `step*`; `simp_all` behaving differently once a fact about an unfolded definition is in context |
| `sum_set`, `sum_move` (list arithmetic) | 15 | 1 (0) | - |
| `batchInv` + `Ledger.apply_batch_loop.spec` (THE loop invariant) | 5 + 39 | 5 (3), then 2 (1) more for the exact part | first invariant too weak (it lacked "once i > 0 the first transfer was valid"), found from the unprovable goal; two failures on the shape of the goal after `step*` |
| `totalInv` + `Ledger.total.spec` | 2 + 28 | 3 (2) | both failures were a wrong library lemma name in a three-line helper |
| `Ledger.balance.spec`, `clone_vec_u64.spec` | 14 | 1 (0) each | Aeneas ships no `step` lemma for `Vec<u64>::clone` |
| `Ledger.apply_all.spec` | 26 | 2 (0), then 4 (3) more for the exact part | `simp` hit the recursion limit on a goal mentioning the pure model |
| pure model `nums`, `stepN`, `runN` + 5 linking lemmas | 30 | 3 (2) | - |
| **Lemma library total** | **about 205** (262 with comments) | **about 30 builds, 17 failed** | est. 1.5 to 2 hours |
| 12 universal scenario proofs | 3 to 8 each, 54 in all | 1 (0): all accepted at the first attempt | 4 needed a one-token change later, when a lemma gained a conjunct |
| 4 literal-value scenario proofs | 5 to 6 each | 5 (4) for the first three, 1 (0) for the fourth | all four failures were one cause: the batch was still a metavariable when `simp` ran |

Per scenario, the hand-written invariants and lemmas each proof rests on:

| Scenario | Proof lines | Rests on | Failed attempts |
|---|---|---|---|
| batch_conserves, batch_first_invalid, batch_count_bounded | 3, 4, 3 | `apply_batch.spec` (invariant `batchInv`), `apply.spec`, `sum_move` | 0 |
| transfer_valid_moves, transfer_invalid_rejected | 5, 5 | `apply.spec`, `sum_move` | 0 (1 pattern fix later) |
| total_is_sum, total_overflow | 6, 3 | `total.spec` (invariant `totalInv`) | 0 |
| balance_of_account, balance_no_account | 4, 4 | `balance.spec` | 0 |
| whole_conserves, whole_first_invalid | 3, 5 | `apply_all.spec`, `apply_batch.spec`, `clone_vec_u64.spec` | 0 (1 pattern fix later) |
| batch_then_total (two Whens) | 8 | `apply_batch.spec`, `total.spec` | 0 |
| two_batches_conserve (two Whens) | 5 | `apply_batch.spec` twice | 0 |
| batch_example_all, batch_example_stop, whole_example_rollback, whole_example_accept (literal values) | 6, 6, 6, 5 | the exact part of `apply_batch.spec` / `apply_all.spec` and the pure model `runN` | 4 in total |

Wallet baseline, for comparison: 9 proofs of 4 to 6 lines, no helper lemma, no invariant, 2 failed attempts in
all. The ledger's scenario proofs are as short, but only because about 205 lines of lemmas stand behind them:
roughly 4 lines of hand-written Lean per line of Rust with a loop in it, against none for the wallet.

Which automation worked and which did not:

- **Worked**: `step*` through `Vec`/slice indexing, `index_mut` back-functions, `checked_add`, and calls to
  functions that have a registered `@[step]` lemma (including a disjunctive one); `scalar_tac` for every bounds
  and index side condition; `simp_all` with the glossary definitions for most closing goals;
  `loop.spec_decr_nat` as the loop rule; `step*` even closed the "rejected, so stop" branch of the batch loop
  on its own.
- **Did not work**: `unfold f; step*` on a function with a loop (nothing happens: there is no lemma about
  `loop`, and no invariant can be guessed); `decide` / `rfl` / `simp` on a loop with concrete inputs;
  `step*` after unrolling `loop` once by hand with the callee inlined (it stops at an `if` nested under a bind);
  `Vec::clone` (no lemma shipped). `simp` discharging `[a, b].length ≤ Usize.max` inside a conditional builder
  needed a helper lemma (`LVocab.mkBatch_val`).
- **Robustness**: replacing `l[i]!` by a helper `bal` throughout the glossary definitions needed three edits in
  the lemma file and none in the scenario proofs. Strengthening a lemma (adding a conjunct) broke four scenario
  proofs, each fixed by one more `-` in an `obtain` pattern.

### 12.5 Exact results: the finding about loops that matters most

An invariant says what every run preserves; it does not say what a given run returns. Two things need the
latter: a scenario with literal values (PROVED-INSTANCE), and the kernel check of a counterexample (REFUTED).
On the wallet both came for free from `step*`. On a loop they do not:

- First state of this work: with invariants only, the (then three) literal-value scenarios were TESTED-ONLY and the
  counterexample to `batch_all_valid_all_applied` was reported as COUNTEREXAMPLE ("kernel confirmation failed").
  `total_always_available` was REFUTED automatically even then, because the invariant lemma for `total` happens
  to determine the result when the sum overflows.
- What fixed it: writing the batch computation a second time as plain structural recursion over lists of
  numbers (`stepN`, `runN`, 13 lines), adding "the loop computes `runN`" to the invariant (one more conjunct of
  `batchInv`), and proving it (about 60 more lines, 11 builds, 8 failed). After that the generated refutation
  script closes with `simp_all [..., ledger.runN, ledger.stepN]` (glossary `proof_hints.refute_simp_more`), and
  the literal-value proofs are six lines each.
- So kernel-checked refutation and instance proofs through a loop are available, at the price of one exact
  functional lemma per loop, written by hand. Without it the slice still reports the counterexample, found by
  search and reproduced on the compiled Rust, but as tested evidence only.

### 12.6 Mutation run on the ledger (`mutation/results.md`)

22 hand-picked mutants of `ledger/src/lib.rs`, 10 of them loop bugs (off-by-one bound, wrong accumulator,
missing early exit, skipped element, wrong counter, wrong early exit, in both loops). Each is run through the
whole pipeline without the crate's unit tests.

| | Ledger (22) | Wallet (18), for comparison |
|---|---|---|
| noticed by the scenarios (run exits non-zero) | 22 | 18 |
| an example row or literal scenario differs on the compiled Rust | 21 | 17 |
| the grid search finds a new counterexample on the Lean model | 21 | 17 |
| at least one proof is lost | 22 | 18 |
| noticed ONLY by a lost proof (no row, no counterexample) | 1 (`la6`) | 1 (`d6`) |
| missed by the crate's own unit tests | 1 (`la6`) | 3 |

Reading it:

- Example rows alone catch 21 of 22; the proofs add one, `la6` (a transfer of exactly 1,000,003 credits one
  unit too few), which is the mutant built to sit away from every example and grid point. Same picture as the
  wallet.
- "A proof is lost" is weaker evidence than it sounds. A proof is lost when its lemma module no longer compiles,
  and a lemma module covers a whole Rust function (and what calls it). A mutant in `apply` costs 13 scenarios
  their proofs although the grid finds a counterexample for only 3 to 8 of them. Only a counterexample shows a
  statement to be false of the mutant.
- With the lemmas in one file (the first run), every ledger mutant cost all 16 ledger proofs, and one mutant
  (`lw3`: `apply_all` rejects every batch) was "noticed" although no scenario statement was false of it: the
  run failed only because a lemma stronger than any scenario stopped proving. The fix was a scenario, not a
  lemma: `whole_example_accept` now states that a good batch is accepted. The lemmas were then split per function.
- Four mutants (`lb2` last transfer never applied, `lb6` stop after the first applied transfer, `lw1` no
  rollback, `lw3`) falsify no universal scenario. Conservation, the count bound and "first invalid changes
  nothing" all still hold of them; they are safety properties and say nothing about progress. These four are
  caught only by the literal-value scenarios. A universal statement of what a batch does achieve would need the
  pure model (`runN`) in the glossary, which the rule against restating the code in a Then is there to prevent.
- 15 negative controls, all as expected, including four new ones: a broken shared lemma module (only the proofs
  depending on it are lost), a weakened loop invariant (the lemma stops proving), a narrowed ledger definition
  (the two readings disagree), a multi-When scenario whose Then is about the wrong kind of result (rejected).

### 12.7 Known limits specific to this section

- The glossary now contains two helper definitions (`LVocab.total`, `LVocab.valid`, plus `bal`) that restate
  part of what the code checks. They do not mention any model function (the audit confirms it), but "valid
  transfer" is the code's own acceptance condition written again, so a wrong reading shared by the Rust and the
  glossary would not be seen. The two readings (Lean, Rust) agree on all grid points; both were written by the
  same agent.
- The sample batches are every sequence of at most two transfers over four sample transfers, plus two more.
  The counterexample to the false batch claim needs two transfers; a false claim needing three would not be
  found.
- The grid for `two_batches_conserve` has 4,761 points; a third list-typed parameter would need the 20,000 cap.
- `usize` literals are limited to `u32::MAX` by the generator, because Aeneas's `Usize.max` is only known to be
  at least that.
- Coverage ("every input falls under a proved scenario") is shown for `balance`, `apply`, `apply_batch` and
  `apply_all`. It is NOT shown for `total`, although its two scenarios do cover every ledger: coverage groups
  scenarios by identical variable lists, and one scenario names the sum (`<sum>`) while the other does not, so
  they land in two groups, neither of which covers alone. Merging them would need the generator to exhibit a
  `U64` equal to the total, which it cannot do with `simp`. The loop and loop-body functions are listed
  separately by Aeneas and show as "not shown", which is correct but noise.

### 12.8 After the adversarial review of the ledger (added 2026-11-10)

The review (`review/loops/`) confirmed what could be checked and made six material findings. All six were
reproduced and fixed or answered; evidence of the reruns is in `review/loops-fix/`.

| Finding | Reproduced | What changed |
|---|---|---|
| Atomicity of `apply_all` was stated by no universal scenario; a mutant without rollback (`r3`) passed once its lemma was re-proved | yes: `r3` changes no row and gives the search nothing on the old tree | new universal scenario `whole_rejected_unchanged` ("if it is rejected, ledger Main is unchanged") and a literal one three transfers deep. With the reviewer's own re-proved lemma applied, the run now fails with a counterexample replayed on the compiled Rust (`review/loops-fix/r3_reproved_after_fix_run.log`) |
| "22 of 22 noticed" rested on a lemma stronger than the scenarios | yes: `r1`, `r2`, `r3`, `r5` were noticed only through a lost proof | the mutation summary and the report now give two figures, "a scenario is shown false" and "the run fails only because a proof stopped compiling"; only the first counts. New universal scenario `batch_stops_at_invalid` states progress without a second copy of the code |
| `batch_then_total` was narrower than its title | yes, by reading the statement | retitled "... when that total fits"; overflow twin `batch_then_total_overflow` added and proved |
| "Every input covered" was trivially true for the loops | yes | the section is renamed "which inputs the scenarios apply to", and lists per operation what the proved Thens say about the returned value and about the state |
| The grid could not see a third iteration or a fourth account; witnesses exercised no iteration | yes | two four-account ledgers and four batches of three and four transfers added to the grid; the non-vacuity witness is now chosen to be non-empty and to change state where one exists (for `batch_conserves`: `[1, 0]` with `[0->1:1]`) |
| Cost figures understated | yes | recounted mechanically, below; build attempts are now logged by `./lakebuild.sh` |

What was NOT done: no pure model of the batch was put in the glossary (the rule of section 1 against restating
the code in a Then). The universal scenarios therefore still do not determine the ledger a batch leaves, nor
that every counted transfer was applied; `apply_all` is never universally promised to ACCEPT anything. Two of
the 27 ledger mutants (`lw3` every batch rejected, `r4` a rejected last transfer counted) falsify no universal
scenario and are caught only by literal-value scenarios.

**Scenario proofs added, with logged effort** (`effort/attempts.tsv`): one pure lemma (`runN_stops`, 8 lines,
induction on the batch) and one bridge (`Ledger.apply_batch.stops`, 9 lines) accepted at the first build; four
scenario proofs of 3 to 7 lines, one of which failed once (a `rw` that should have been `congrArg`). Three
builds, one failed, 32 seconds between the first and the last. This supports the review's observation that,
once "the loop computes `runN`" is proved, a further universal property is a short list induction; it says
nothing about the cost of the first invariant.

**Cost, counted the same way for both crates** (`python3 effort/count.py`; code lines only):

| | Wallet (straight-line) | Ledger (2 loops, a Vec) |
|---|---|---|
| Rust code lines (raw lines) | 37 (45) | 65 (85) |
| Scenario proofs; tactic lines each; in all | 8; 4 to 6; 34 | 21; 3 to 10; 107 |
| Hand-written lemma library | none | 227 code lines: 18 theorems, 5 definitions, 2 loop invariants |
| Glossary definitions (Lean) | 24 | 55 |
| Hand-written Lean in all | 58 | 389 |
| Lean per Rust code line (without the glossary) | 1.6 (0.9) | 6.0 (5.1) |

**Mutation run after the fixes** (45 Rust mutants, 15 controls, 21 minutes with 8 jobs on a loaded machine):

| | Ledger (27: the builder's 22 + the reviewer's 5) | Wallet (18) |
|---|---|---|
| A scenario is shown false (a row differs on the compiled Rust, or the search finds a counterexample) | 26 | 17 |
| ... of which a UNIVERSAL scenario is shown false by the search | 24 | 17 |
| The run fails only because a proof stopped compiling | 1 (`la6`) | 1 (`d6`) |
| The run does not fail | 0 | 0 |
| Missed by the crate's own unit tests | 4 (`la6`, `r1`, `r2`, `r3`) | 3 |

`la6` and `d6` are the mutants built to be wrong only at an amount no example or grid point uses. For them the
lost proof is the only signal, and by the rule above it is reported as "not shown false". Before the fixes the
same harness gave, for the reviewer's five: one shown false (`r4`), four lost-proof-only. The rows, grid points
and scenarios were added knowing those five mutants, so 26 of 27 is a fix confirmed, not a detection rate.

## 13. Gherkin `Rule:`, the suite adequacy note, the per-Rule block (added 2026-11-10)

Plan nodes F1, the first check of V2, and X1a for the slice (`../docs/PLAN.md`). Judgement calls:
`../DECISIONS.md`, "slice: Rule and adequacy note".

### 13.1 `Rule:` under cucumber-rs [observed]

`docs/VOCABULARY.md` decision 5 keeps Gherkin as the surface and writes a one-line claim with Gherkin's own
`Rule:` keyword, the scenarios beneath it being its examples. Whether the pinned runner executes that was open.
It does: with cucumber 0.23.0 (gherkin 0.16.0, the versions in `wallet-bdd/Cargo.lock`) a feature with a
Scenario Outline and Examples under a `Rule:`, a second scenario under the same rule, a Background under a
Rule, a Background under the Feature, the `Example:` keyword and a tag on the Rule ran as 4 scenarios in 2
rules, the Feature's Background before the Rule's. Kept in `review/rule-probe/` (feature, runner log, JSON).
Since then the real feature files are the standing check: all 35 scenarios sit in files that use `Rule:` and
run through cucumber-rs on every `./run.sh`.

Two things the runner does that the generator had to allow for:

- the JSON writer reports a Background as a separate element with the same `line` as the scenario it ran
  before. `load_cucumber` (and the mutation harness) used to keep the last element per line; they now put the
  steps of both together, so a failing Background step is not lost;
- the JSON writer does not copy a Rule's tags onto its scenarios, and gives the rule line no meaning at all.
  Tag inheritance and everything else about a Rule is therefore done by clausal from the feature text.

### 13.2 What the generator does with a Rule

- **Parse** (`core.py`): `Rule:` starts a rule; every scenario up to the next `Rule:` belongs to it; scenarios
  before the first Rule belong to none. The free text under the rule line is its description. A Background
  may open a Rule. A Rule needs text; two Rules of one feature may not have the same id.
- **Carry, do not compile.** The rule line and its description go into the report and the graph verbatim.
  No Lean is generated from them and no `formalises` edge points at a Rule. What is proved is each scenario.
  Nothing checks that the rule line says what the scenarios say; a Rule with no scenario is reported as
  "nothing stated".
- **Ids.** A scenario's id is still `Spec.<feature>.<scenario>`: the Rule is not part of it, so moving a
  scenario under a Rule moves no proof file and changes no statement. A Rule's id is
  `Rule.<feature>.<slug of its text>`, or `@id:<name>` on the Rule.
- **Tags.** Tags on the Feature and on the Rule apply to the scenarios beneath (`Scenario.all_tags`).
  `@id:` is not inherited. `@expect-*`: the scenario's own, else its Rule's, else its Feature's.
  `@control` (new) marks a check of the pipeline itself; it changes no verdict and takes the scenario out of
  the adequacy note.
- **Suite.** The scenarios under a Rule are its suite (`Feature.suites()`); scenarios under no Rule form one
  group per feature.
- **Graph.** A Rule is a `group` node (`group:rule:<id>`, text = rule line + description,
  `attrs.level: rule`, `attrs.compiled: false`); Feature `contains` Rule `contains` scenario.

The wallet and ledger files were regrouped by a script that moved each scenario block unchanged: 5 Rules in
the wallet, 9 in the ledger; `negative.feature` has none and is tagged `@control`.

### 13.3 The suite adequacy note

Informational. It feeds no verdict and no exit status; its two Lean scripts are imported by nothing, run in
the background beside steps 5 to 7 of `run.sh`, and their exit status is ignored (`--no-adequacy` skips them).

**Trivial models** (`adequacy.trivial_models`). For every model function a When phrase is bound to:

| Kind | Generated as |
|---|---|
| reject-all | `fun args => ok (r, state unchanged)` for each result value `r` the glossary lists as a rejection |
| no-op | the same for each value listed as a success; plus hand-written ones from `trivial.extra` (for `apply_batch`: `fun l b => ok (Slice.len b, l)`, "reports the whole batch as applied") |
| identity | `fun args => do let (o, _) <- f args; ok (o, state unchanged)`: answers as the code does, never changes the state. Not generated for an operation that hands back no state |
| constant | each remaining listed result value with the state unchanged, and every listed value with the state reset to a fixed one (the actor's `build` applied to the first `sample`) |

Each is declared `def Trivial.<op>.<name> : type_of% @<model function> := ...`, so Lean checks that it has
exactly the type of the generated model. The result values come from the glossary's existing `outcome_values`;
which of them is a rejection or a success is the new `trivial.outcomes`. Wallet operations get 7 models each,
`apply_batch` 12, `apply` and `apply_all` 5, `total` and `balance` 5 (an operation with no state has only
constant answers, classed as reject-all or no-op).

**Pairs.** Every scenario that is meant to be proved and is not a control, against every trivial model of
every operation it calls: the scenario's statement is generated again by the ordinary generator with the
trivial model's name where the call was (`Env(subst=...)`; in a multi-When scenario, in every When that calls
that operation). 234 pairs on this tree.

**Step 1, search** (`Run/Adequacy.lean`, interpreter). For each pair the scenario's own boundary grid is
searched for an input that satisfies the Givens and fails a Then. Evidence kind: tested.

**Step 2, kernel attempts** (`Run/AdequacyAudit.lean`). Where step 1 found an input: a theorem
`not <restated statement>` at that input. Where it found none: a theorem that the restated statement holds
for all inputs. Only for a constant-bodied model and a single When; the others stay tested-only. A script
that fails shows up with `sorryAx` and counts as no theorem.

**Reading the result.** A scenario *rules out* a trivial model when step 1 finds an input. A set of scenarios
rules it out when one of them does, and *still allows* it otherwise. "Still allows" is proved only where the
report says "proved to satisfy every scenario counted" (step 2 succeeded for every scenario of the set);
otherwise it means no scenario was shown false of it on the grid. A kind is listed under "rules out" when
every variant of that kind is ruled out.

**What is counted.** Only scenarios whose verdict in this run is PROVED-FOR-ALL. Literal examples
(PROVED-INSTANCE) are evaluated too and reported separately ("ruled out only by a literal example, for its
one input"). Unproved scenarios are named as not counted.

**Three levels**, all from the same pair results:

- per operation: all its proved universal scenarios, across Rules (terminal: `  <op>: rules out: ...; still
  allows: ...`; one verdict per operation in the graph);
- per Rule: the Rule's own proved universal scenarios, per operation they call (`Suite` line of the block).
  If the Rule alone still allows something that the operation's whole suite rules out, the block says which
  Rule does so; if nothing proved for all inputs rules it out anywhere, it says that, and whether a literal
  example does;
- per scenario: where one scenario alone would hold of a kind its Rule rules out, the block names the
  scenario and the one that rules it out.

The last two are stated without judgement and followed by one fixed sentence: a single scenario or rule that
also holds of a trivial implementation is expected; adequacy is judged for the suite.

### 13.4 The note in the graph (schema v2 unchanged)

- trivial model: `function` node `fn:lean:Trivial.<op>.<name>` with `attrs.trivial` (`of`, `kind`, `label`);
- pair: `statement` node `stmt:<scenario id>.adq.<op>.<name>.stmt` (the restated statement) with
  `attrs.adequacy` (`scenario`, `trivial`, `result`, grid counts); it `uses` the trivial model;
- found input: `example` node that `refutes` the pair's statement, with tested evidence and, when the kernel
  script went through, kernel-checked evidence naming the theorem and its axioms;
- proved to hold: an implementation on the pair's statement with kernel-checked `realises` evidence;
- per operation: `attrs.adequacy` and a `note` label on the model function's node, and a verdict with code
  `SUITE-RULES-OUT-TRIVIAL` (outcome `pass`, or `review` while the glossary is unsigned) or
  `SUITE-ALLOWS-TRIVIAL` (outcome `open`); the allowed variants are its flags, the refuting edges its chain;
- per Rule: `attrs.suite_lines`, `attrs.suite_headlines`, `attrs.suite` and a `note` label on the Rule's group.

`../docs/SCHEMA.md` does not yet describe Rule groups or the two verdict codes.

### 13.5 The per-Rule block, generated from the graph

`clausal/rules.py` imports nothing from the rest of the generator. `blocks(graph)` walks the JSON:
group -> `contains` -> scenarios; scenario -> verdict record; scenario -> `composed_of` -> phrase ->
`binds` (sign-off); `formalises` -> statement -> kernel-checked `realises` evidence (theorem, axioms),
`refutes` (refutation or vacuity), `instance_of` (example rows, with the result on the model and on the
compiled Rust), `uses` -> model function -> `translates` (tool, versions from the run record); the
compiled-Rust run's `rustc`. `clausal report` writes `out/graph.json`, reads the file back, renders the
blocks from what it read, and fails the run if a block's scenarios, verdicts or row counts differ from the
verdicts computed in memory. `python3 -m clausal rules [graph.json]` prints the blocks of a stored graph.

Block layout (the README target, minus the compiled reading): rule text and description; `Verdict` (a
headline over the scenarios, then each scenario's verdict); `Examples`; `Suite`; `Rests on` with four lines:
`meaning` (Clausebook entries used, how many signed, by whom), `proof` (theorems for all inputs, for literal
values, refutations, vacuity proofs; axioms), `translation` (model functions, Charon and Aeneas versions,
example rows cross-checked on Rust and model), `compilation` (the `rustc` that built the tested binary).
A compiled reading of the rule line is not echoed back: there is nothing compiled to echo until the frame
library exists. The generated Lean statement of each scenario is printed beneath the block, as before.

### 13.6 What it reports on this tree

Measured by `./run.sh` on 2026-11-10 (35 scenarios, 14 Rules). Toy fixtures: these numbers show the
machinery working, not anything about suites in general.

- **Verdicts.** All 35 scenario verdicts, flags and counterexamples, and all 12 input-coverage verdicts, are
  identical to the run before the change (compared field by field against the graph of the previous tree; the
  only difference is a line number inside one message). cucumber-rs: 81 scenarios and 365 steps as before, now
  in 14 rules.
- **Trivial models.** 53 for 8 operations: 11 reject-all, 14 no-op, 6 identity, 22 constant. 234 pairs.
- **Pairs.** The scenario is false of the trivial model for 169 (133 with a kernel-checked refutation at the
  found input; 36 tested only, all multi-When or identity pairs). It is proved to hold of the trivial model,
  for all inputs, for 32. Neither for 33: 32 multi-When or identity pairs that get no kernel attempt, and the
  one pair described in 13.8 whose proof attempt fails. Every kernel attempt at a refutation succeeded
  (133 of 133); 32 of 33 attempts at "holds" succeeded.
- **Per operation, the whole suite:**

  | Operation | Proved universal scenarios | Trivial variants | Ruled out | Still allowed |
  |---|---|---|---|---|
  | `wallet.transfer` | 3 | 7 | 7 | none found |
  | `wallet.Wallet.deposit` | 2 | 7 | 7 | none found |
  | `wallet.Wallet.withdraw` | 2 | 7 | 7 | none found |
  | `ledger.Ledger.apply` | 2 | 5 | 5 | none found |
  | `ledger.Ledger.apply_batch` | 7 | 12 | 12 | none found |
  | `ledger.Ledger.apply_all` | 3 | 5 | 3 | **reject-all** (always `false`, state unchanged; proved to satisfy all three scenarios) and **identity** |
  | `ledger.Ledger.total` | 4 | 5 | 5 | none found |
  | `ledger.Ledger.balance` | 2 | 5 | 5 | none found |

  The `apply_all` line is a real gap in the scenario set, and one already found by hand: section 12.8 records
  that `apply_all` is never universally promised to accept anything, and that mutant `lw3` (every batch
  rejected) falsifies no universal scenario. Both allowed variants are ruled out by the literal example
  "a batch of valid transfers applied as a whole is accepted and applied", for its one input, and the note
  says so. No scenario was added to close it: stating "a batch whose transfers all apply in sequence is
  accepted" needs the intermediate ledgers, which is the open problem of section 12.5.
- **Per Rule.** Of the 10 Rules with a proved universal scenario, 6 rule out every variant on their own
  (the three wallet Rules; single transfer; total; lookup). The other four:
  "applying a batch never changes the total" still allows the hand-written no-op (reports the whole batch as
  applied), which the count Rule rules out; the count Rule still allows reject-all and identity, which the
  first Rule's progress scenario rules out; "applying a batch does not change the total computed afterwards"
  rules out nothing about `apply_batch` on its own; and the `apply_all` Rule is the gap above. In every
  block where one scenario alone would hold of a trivial implementation, the block names it and the scenario
  that rules it out (for example the conservation scenario alone holds of reject-all, identity and constant).
- **Cost.** Two more Lean processes per run: 21 s (search) and 12 s (kernel attempts) of wall time measured
  alone on a lightly loaded machine; they run beside steps 5 to 7. The whole of `./run.sh` took 33 s before
  the change on the same machine; a clean after figure could not be taken because other jobs held the
  machine at a load average of 60 to 100 (87 s and 95 s were measured under that load). `out/graph.json`
  grew from 358 nodes and 886 edges to 828 nodes and 1303 edges, almost all of it the 234 pair statements
  and the 169 found inputs.

### 13.7 Controls (mutation/run_mutants.py)

| Control | Change | Expected |
|---|---|---|
| c16 | the progress scenario of the batch suite (`batch_stops_at_invalid`) is removed | exit 0; `apply_batch` reported as still allowing reject-all |
| c17 | the progress scenario of the withdrawal rule (`withdraw_covered`) is removed | exit 0; `withdraw` reported as still allowing "always insufficient funds", proved to satisfy the remaining scenario |
| c18 | none | exit 0; `apply_batch` and `transfer` report "(none found)"; the known `apply_all` gap is reported |
| c19 | the hand-written trivial model in the glossary is made ill-typed | exit 0; "not computed"; the tally of verdicts is unchanged |
| c20 | `@expect-refuted` is removed from a Rule line | exit 1: the scenario beneath no longer inherits the tag |

The same ideas at the level of the Python, without Lean: `python3 -m clausal.selftest` (22 checks: Rule
parsing, tag inheritance, Backgrounds, removing a scenario by id, and the note's bookkeeping on made-up results,
including "the same suite with its progress scenario removed is reported as allowing reject-all").

**Mutation run after the change** (45 Rust mutants, 20 controls; 26 minutes with 6 jobs on a machine at a load
average of 60 to 100): every recorded field of every mutant (unit tests, rows changed, proofs lost, new
counterexamples, verdicts that changed, exit status) is identical to the run of section 12.8; controls c1 to
c15 behave as before; c16 to c20 behave as expected. Four changes were made to the harness itself and are
listed in `../DECISIONS.md`: scenarios are removed by id (`core.without_scenarios`) because the files were
regrouped; c3 matches each count of the verdict tally separately because the tally follows scenario order;
c14's patch text is re-indented; mutant runs pass `--no-adequacy` (the baseline and all controls run the whole
pipeline).

### 13.8 Limits

- The rule line is English that nothing reads. A rule whose text claims more than its scenarios say is not
  detected. Closing that gap is what the frame library and echo-back (V2, V3, V5) are for.
- Four kinds of trivial implementation, built from the result values the glossary happens to list. "Still
  allows: (none found)" means none of these, not that the suite pins the behaviour: the ledger's universal
  scenarios still do not determine which ledger a batch leaves (section 12.8).
- "Rejection" and "success" are a hand-made classification of result values in the glossary, unsigned.
- "Still allows" without "proved" rests on the grid. One pair shows the difference: "a batch stops only at an
  invalid transfer" against "always answers 4, state unchanged" has no failing input on a grid whose batches
  have at most four transfers, and the proof attempt rightly fails (a batch of five refutes it). It is
  reported as not shown false on the grid, not as holding.
- No kernel attempt for multi-When pairs or for the identity variant; those results are tested only.
- Only single operations: a suite that is adequate per operation can still leave their interplay open.
- Coverage theorems are still numbered by scenario order (`Coverage.g<k>`), so regrouping renumbers them.


## 14. The composable Clausebook: frames, pieces, compiled Rule lines, echo-back (added 2026-11-10)

Plan nodes V2 and V3. Sections 4 to 13 describe a slice that binds WHOLE phrases: one glossary entry, one
Lean definition and one sign-off per step sentence, and a `Rule:` line that nothing reads. This section
describes what replaced that as the link from English to Lean. The old binding is still in the tree, in a
new and smaller role (14.6).

### 14.1 The frame library (`lean/Frames/`, Lake library `Frames`)

Imports nothing but Lean's core (no Mathlib, no Aeneas), so it can be lifted into a package of its own.

- **The abstract operation** (`Frames/Core.lean`, `Frames.Op σ α ρ`): `run : σ → α → Option (ρ × σ)` (one call
  from a state with an input: an answer and the state afterwards, or `none` = no answer: panic, abort,
  divergence), `accepted : ρ → Prop` (which answers are acceptances; every other answer is a rejection),
  `scope` (the inputs a claim is about; everything by default) and `calls` (every call, by default; or only
  accepted, or only rejected ones).
- **Typed holes.** `Measure σ α μ` (a quantity of the state; it may name parts by the input, e.g. "the
  sender's account"), `Term σ α μ` (a value known before the call), `Cond σ α`, `AnswerClass ρ`, `Answer ρ μ`,
  `Coll σ α ρ ι` (a named collection, read after the call), `ItemCond σ α ι`, `Variation σ α` (a relation
  between two (state, input) pairs). No frame has a hole of type `σ → α → ρ → σ → Prop`. That type occurs in
  one definition, `Op.HoldsAt`, which is where the defaults are written down; it is not a frame and the
  Clausebook has no entry for it. The link audit checks every compiled reading against an ALLOWLIST: of the
  constants declared in this project, a reading may mention only the frames of the pieces it uses, the Lean
  definitions those pieces name (`defs:`), its operations, and the types and literal constructors of the
  Clausebook; anything else (`HoldsAt`, the old glossary, a model function) fails it (GENERATOR-CHECK-FAILED;
  control c31). The hole types are polymorphic, so the types alone do not stop a general relation: `EveryOf`
  with the answer as its "collection" can state any predicate of (input, answer, state after) (kernel-checked in
  `review/frames/rv_tools/ReviewProbeV2.lean`). What stops it is that no piece produces such a collection, that
  the allowlist admits only what the pieces name, and that pieces are signed; 0 of 87 are signed today.
- **The defaults, once.** `Op.HoldsAt op Q s a`: outside the scope, nothing; with `calls = every` (default)
  the call gives an answer AND `Q` holds of it; with `accepted` / `rejected`, IF the call gives an answer of
  that kind, `Q` holds of it. So "never" and "always" cover every input including rejected ones and include
  "always answers", and a weaker reading has to be asked for (`Op.successful`, `Op.rejected`).
- **The frames** (`Frames/Frames.lean`): 23 definitions for the 14 frames of the first catalogue
  (`out/prior_art_vocabulary.md`). For each `F`: `F.at op holes s a` (what it says of one call) and
  `F op holes := ∀ s a, F.at …`. Two-run frames (12, 14) go through `Op.HoldsAt2`.

  | Catalogue | Lean | Reachable from a sentence |
  |---|---|---|
  | 1 always answers | `AlwaysAnswers` | yes |
  | 2 never changes | `NeverChanges` | yes |
  | 3 changes only | `ChangesOnly` | yes (through an idiom and one Then form) |
  | 4 always / never | `Always`, `Never` | yes |
  | 5 if-then | `IfThen`: fail-closed, the call answers whether or not C holds (changed after the review; before, it was frame 4 on the operation narrowed to C, which claimed nothing outside C while its echo printed D1). The narrowed claim is still sayable: `Op.given` on any frame, "<operation> for which C is always accepted" | yes |
  | 6 only if | `OnlyIf` | yes |
  | 7 exactly when | `ExactlyWhen` | yes |
  | 8 rejected and unchanged | `RejectedUnchanged` | yes |
  | 9 changes by exactly / is now / the result is | `IncreasesBy`, `DecreasesBy`, `Becomes`, `ResultIs` | yes |
  | 10 at most / at least | `ResultAtMost`, `ResultAtLeast`, `AtMost`, `AtLeast` | yes |
  | 11 counting over a collection | `EveryOf`, `NoneOf`; `CountOf` (a number) | every / no: yes; with a number: NO SURFACE YET |
  | 12 monotone | `Monotone` | NO SURFACE YET |
  | 13 agrees with a reference | `AgreesWith` (`ResultIs` for the answer alone) | NO SURFACE YET |
  | 14 independent of (two runs) | `IndependentOf` | NO SURFACE YET |

  "No surface yet" means: defined, with an executable reading and a comparison of the two on hand-written
  instances (`lean/Run/FrameTests.lean`), but no form in `clausebook.yaml` and no domain word of the hole
  types they need (a relation between two inputs, a reference function). Nothing in the fixtures needs them.
- **The second reading** (`Frames/Check.lean`): `Frames.Check.<frame> op holes s a : Bool`, written as a
  program ("run the call; case on what was seen": `Op.observe` gives out of scope / no answer / not covered /
  answered). The definition is evaluated through a `Decidable` instance (`Op.decHoldsAt`), which is correct
  by construction, so a disagreement between `decide (F.at …)` and `Check.F …` always means the checker and
  the definition say different things. Compared on generated inputs by `lean/Run/ReadingSearch.lean` (every
  compiled reading of the run), `lean/Run/NewReadings.lean` (the held-out sentences) and
  `lean/Run/FrameTests.lean`. This is FRET's two-semantics practice; it is a test, not a proof of equality, and
  both readings have one author. The comparison can only catch a wrong reading at a point where the claim is false
  or the call gives no answer. The fixtures supply the first rarely (125 of 23,772 evaluations, in three frames)
  and the second never, so `lean/Run/FrameToyTests.lean` (core Lean only) states EVERY frame of a toy operation
  that gives no answer at input 0, rejects input 1 and accepts from 2 on, each with a claim that is false at some
  points; the reading search counts, per frame, the false and the silent evaluations, and the report marks a
  frame `comparison untested` when no comparison of the run saw both.
- **Lemmas about the frames** (`Frames/Lemmas.lean`, kernel-checked): `IfThen.alwaysAnswers`, `IfThen.given`,
  `IfThen_of_given` (what "if C then Q" says beside the narrowed claim) and `ExactlyWhen_iff` ("exactly when" is
  "if" and "only if" together).
- **Modifiers defined in Lean**: `Op.given`, `Op.successful`, `Op.rejected`, `Op.internal`, `Op.andThen`
  (a sequence of Whens), `Op.beside` (a bystander), `aggregate`, `every`, `noneOf`, `theFirst`.

### 14.2 The Clausebook (`clausebook.yaml`), three kinds of piece

| Kind | Count | Lean side | Scope |
|---|---|---|---|
| domain word | 31 (8 operations; 23 measures, conditions, collections, answer words, named values) | `lean/Wallet/Pieces.lean` (`W`), `lean/Ledger/Pieces.lean` (`L`) | one system |
| modifier | 27 | `lean/Frames/Core.lean`, or Lean notation written in the entry (`=`, `≤`, `<`, `+`, `¬`) | shared |
| frame | 19 with a surface form (+ 4 without) | `lean/Frames/Frames.lean` | shared |

Plus 10 **idioms**: a surface form that is not the regular form of one piece, with the composition it MEANS
written in piece ids (`"{w:wallet} has a balance of {t:term<num>}"` means `is(w.balance(w), t)`). An idiom
adds English and no Lean. It exists because the feature files were to keep their sentences (the same files
run under cucumber-rs through the old step definitions); 10 of the 36 old Given/Then phrases needed one.

- **Every piece has a category** and every hole of a form names one: value types (`amount`, `index`,
  `balances`, `transfer`, `batch`, `error`), actor types (`wallet`, `ledger`), `measure<T>`, `nums`,
  `term<T>`, `cond`, `item<T>`, `coll<T>`, `itempred<T>`, `ameasure<T>`, `class`, `acoll<T>`, `parts<T>`,
  `claim`. `T` in a form is one type throughout that form.
- **An operation names roles** (`state: [[sender, wallet], [receiver, wallet]]`, `input: [[amount, amount]]`).
  In a scenario an actor is a name ("Alice", "ledger Main") and a value a literal or an outline
  `<parameter>`; in a Rule the same holes are filled by the role ("the sender", "the amount"). So one form
  serves both: `"{w:wallet}'s balance"` reads "Alice's balance" and "the sender's balance".
- **Composition** (`clausal/vocab.py`). A Given is parsed as a `cond`, a When against the operations' `when`
  forms, a Then as a `claim` (optionally under `if it is rejected,` / `if it is accepted,`). The parser tries
  every form of the wanted category and every way of splitting the text among its holes, recursively.
  Exactly one tree: the reading. None: UNBOUND, with the nearest forms. None, but one if type parameters and
  value types are ignored: ILL-TYPED, saying which piece has which type where which is needed. Several:
  AMBIGUOUS, listing them. Each with file:line; none is ever resolved by a guess. Answer words must match the
  answer type of the (last) operation (ILL-TYPED otherwise). Lean then type-checks the generated statement.
- **What a scenario compiles to.** The state is the tuple of the first operation's roles, extended by any
  actor the scenario names and the When does not pass (`Op.beside`: a bystander, unchanged by construction;
  this keeps the old control "a deposit does not touch a bystander" meaningful). Several Whens are one
  `Op.andThen`. Outline parameters that are a When's input become the input; the others are quantified at
  the front. All Givens (and a literal input, as `inp = literal`) become ONE `Op.given`. Each Then becomes one
  frame applied to that operation (an idiom may give several). The statement is the conjunction.
  `lean/Wallet/Readings.lean` holds one `def <id>.reading : Prop` per scenario and per Rule.
- **Sign-off is per piece** (`python3 -m clausal review <piece-id|all> --reviewer NAME`,
  `clausebook.signoff.json`): the digest covers the piece's YAML entry and the text of every Lean definition
  it names (`defs:`), and the sign-off is void when either changes. `--strict` fails a proved scenario or
  rule that rests on an unsigned piece. Nothing is signed.

### 14.3 The Rule line is compiled; how a Rule relates to its scenarios

Grammar of a rule line (controlled; standard Gherkin, the runner ignores it):

    <clause> [, and <clause>]…
    <clause>  ::=  <subject> <what it does> [and <what it does>]…          "A transfer never changes the total of all balances"
               |   for <subject>, <what a Then would say> [and …]           "For a lookup, the result is the balance of the account in the ledger"
    <subject> ::=  a | an  [successful | rejected | internal]  <operation> [followed by <operation>] [for which <condition>]

A clause is one or more frames applied to the subject's operation; the rule is the conjunction: ONE Lean
statement, `Rule.<feature>.<id>.reading`. A subject with no adjective is read fail-closed; `successful` and
`rejected` narrow the clause to those calls and the echo says so.

**The relation, decided:** the universal scenarios beneath a Rule that are meant to hold are its PARTS, and the
rule statement is proved FROM them, in one direction:

    <rule>.from_scenarios : S₁.reading → … → Sₙ.reading → <rule>.reading        (generated, kernel-checked)

The script is fixed (`clausal/links.py`, `rule_glue`): take any state and input; pull in the facts of every
part that has no condition; case on the conditions of each conditional part in turn (a Given that only names a
value, `<measure> is <parameter>`, is discharged by `rfl`, which makes Lean find the parameter); in the
remaining case the conditions of the suite must be contradictory. Leaf facts are closed by one tactic,
`bridge`. The rule is PROVED-FOR-ALL when this theorem is kernel-checked, has exactly that type (the link
audit checks it), and every part it names is itself PROVED-FOR-ALL.

- Where the script does not go through, a hand-written proof of exactly the rule statement may stand in
  (`lean/Wallet/RuleProofs/<feature>/<id>.lean`, theorem `<rule id>` of type `<rule id>.reading`; audited).
  Two rules need one (14.7).
- A scenario may say more than its rule; nothing claims the converse direction. Literal scenarios are
  instances, not parts. The per-Rule block marks each scenario as a part, an instance, or neither.
- A rule statement that the reading search finds false is refuted in the kernel at that input
  (`<rule>.refuted : ¬ <rule>.reading`), by stepping through the model as section 6 does for scenarios
  (`Bdd.false_of_spec`). Only for a clause about every call of a single operation.
- Verdicts: PROVED-FOR-ALL, REFUTED / COUNTEREXAMPLE, NOT-PROVED (compiled and searched, no proof),
  UNBOUND / ILL-TYPED / AMBIGUOUS. Expected: PROVED-FOR-ALL unless the Rule is tagged `@expect-refuted`,
  `@expect-unbound` or `@expect-unproved`. `run.sh` now exits 0 iff every scenario AND every rule statement
  got its expected verdict.

### 14.4 Quantifier scope: one rule

Every outline `<parameter>`, then the state, then the input are universally quantified at the front, in that
order; Givens restrict them. Collection words (`every`, `the first`, `no`) bind inside the one Given, Then or
rule clause they are written in. Negation applies to the one atomic condition it is written on (`is not
valid`), so "every X is not P" reads "no X is P" and never "not every X is P" (printed as D9 with every reading
it was applied to; "not every" cannot be said at all). Conditions are judged on the state BEFORE the call (D8):
"accepted exactly when every transfer of the batch is valid on the ledger" speaks of the starting ledger, not
of the ledger each transfer meets in turn. Nothing is existentially quantified over inputs. The compiler never
chooses between scopes: a sentence that would need another scope does not parse. (The review showed that a
natural-sounding sentence can still compile to the unintended one of two scopes; D8 and D9 are now printed so
the echo shows which was taken. Whether readers notice is K1/V5.)

### 14.5 Echo-back

Every reading is printed in fixed English with four slots, FRET-style, beside the sentence and above the
Lean: **applies to** (the operation; every role; whether rejected calls are covered), **assuming** (the
Givens), **then** (one line per frame, from the frame's `echo` template filled with its pieces' templates;
"the call gives an answer [default D1]" is printed when it was applied), **accepted** (which answers of the
operation count as accepted, printed whenever a reading speaks of accepted, successful or rejected calls; for
applying a batch it says that every answer is an acceptance), **defaults** (D1 to D9, each printed with every
reading it was applied to) and **not default** (when `successful` / `rejected` removed one). Every outline
`<parameter>` and every input is printed with its type ("sum (a u64: 0 to 2^64 - 1)"), because the type
restricts what the reading is about. A clause about accepted or rejected calls only that covered no call on the
search grid is flagged COVERS NO CALL ON THE GRID. The
report (`out/report.md`) and the terminal print the echo first; the Lean statement, the flat statement and
the proof are folded underneath.

### 14.6 Regression: NEW ↔ OLD (V3)

The old pipeline (sections 4 to 13) is unchanged and still runs: `glossary.yaml`, `lean/Wallet/Vocab.lean`,
`lean/Ledger/Vocab.lean`, the flat statements `<id>.stmt`, the hand-written proofs, the search, the audit, the
adequacy note, the Rust steps. It is no longer the link from English to Lean. Its statement is now an
intermediate: for every scenario a generated theorem

    <id>.reading_iff : <id>.reading ↔ <id>.stmt

is kernel-checked and its type audited (`lean/Run/Links.lean`, `lean/Bdd/AuditLinks.lean`); the audit also
walks everything its proof reaches through constants of this project and does not count the equivalence if it
meets a proof of either side (an iff between two proved closed propositions follows from the two proofs alone,
which compares nothing; control c30). It comes together with
`<id>.reading_sat` (the scope of the reading is satisfiable, at the witness the search found) and, where the
flat statement has a proof,

    <id>.reading_holds : <id>.reading := <id>.reading_iff.mpr <id>

so that a PROVED scenario is ONE kernel-checked theorem whose type is exactly the compiled reading. Likewise
a rule proved from its scenarios is one theorem, `<rule>.holds : <rule>.reading :=
<rule>.from_scenarios S₁.reading_holds … Sₙ.reading_holds`. The verdict of the flat statement is reported as
the reading's verdict only if these are there; otherwise the verdict is UNLINKED. So the existing proofs carry over through the equivalence and were not touched (the only edit to a
legacy Lean file moves three `deriving instance` lines from `Wallet/Vocab.lean` to `Wallet/Instances.lean`).

The script is explicit about structure (how the flat statement's variables build the state and the input;
which frame gives which fact; `Frames.Op.answer_unique` to identify the answers of several frames;
`Bdd.opMut_some` and friends to move between `run … = some …` and `model … = ok …`) and leaves only leaf facts
to `bridge`. Result on this tree: 34 of 34 equivalent, standard axioms only. No scenario statement was
strengthened by the defaults: the old statements already said the call returns for every input satisfying the
Givens.

### 14.7 What it reports on this tree (2026-11-10)

- 34 of 35 scenarios and 13 of 14 rule lines compile (the two "earns interest" sentences are UNBOUND, as
  intended). All 35 scenario verdicts are what they were.
- 14 rule statements: 10 PROVED-FOR-ALL (8 from their scenarios by the generated glue, 2 by a hand-written
  proof from the loop lemmas: `total_fits`, `batch_then_total`, whose scenarios name a sum with a `u64`
  parameter the script cannot produce), 3 REFUTED in the kernel (the three deliberately false ones), 1 UNBOUND.
- The definition and the executable reading of the frames agree on 23,772 of 23,772 evaluations over the 47
  readings of the fixtures (23,700 before the withdrawal and deposit rules regained a clause). The definition is
  false at 125 of them, in three frames, and no call in scope gives no answer, so that comparison cannot see a
  checker that is wrong only on false claims or silent calls. On the hand-written instances (toy operation
  included): 3,141 of 3,141, 632 false, 192 with a silent call; every frame is compared at both.
- The 44 whole-phrase entries are read with 73 entries of the new Clausebook (31 domain words, 21 modifiers,
  11 frames, 10 idioms); the Clausebook has 77 pieces and 10 idioms in all. The glossary did not get smaller.
  What changed is where a new sentence lands: 46 of the 77 pieces are shared by kind; 12 of them are used by
  sentences of both fixtures (24 by one, 10 by none).
- Five new ledger rules (`heldout/new_rules.feature`), written by the Clausebook's builder: 5 of 5 compile
  (the Clausebook files were edited after them, so "no change to the Clausebook" cannot be confirmed); 4 have no counterexample on the grid, 1 (meant to be false) has one. None is
  proved: a new sentence gets a statement and a search for free, not a proof, and no Rust step.

### 14.8 Controls (mutation/run_mutants.py)

c21 a frame's definition weakened (readings no longer equivalent; the two readings of the frame differ);
c22 a domain word redefined in Lean (readings no longer equivalent, though the old glossary and the Rust
readings are untouched); c23 a frame's executable reading wrong (nothing kernel-checked changes; the
comparison fails the run); c24 an ill-typed rule line (ILL-TYPED with file:line and the two types);
c25 a rule line that says more than its scenarios and is false (refuted in the kernel while every scenario
stays proved); c26 a signed piece whose Lean text is edited (that sign-off void, `--strict` fails on it);
c27 a form removed from the Clausebook (UNBOUND; the old statement is not reported in the reading's place).
Two older controls changed their expected exit status from 0 to 1, deliberately: c8 and c17 remove progress
scenarios, and the rule statements that were proved from them are now reported as no longer proved.
Added with the fixes after the review: c28 a rule clause about rejected calls of an operation that never rejects
(flagged COVERS NO CALL ON THE GRID; the run passes); c29 a checker that is wrong only on a call that gives no
answer (invisible to the fixture comparison; the toy operation fails the run); c30 an equivalence whose proof
uses the proof of the old statement (not counted; the scenario is UNLINKED); c31 a model field written straight
into a domain word's Lean text (fails the allowlist, where the old blocklist of three names passed).

### 14.9 Limits

- **The Rust side is not compositional.** The cucumber steps and the Rust second readings are still one per
  old whole phrase. A new composition has no step, so a new sentence is not run on the compiled Rust. This is
  the largest gap between this and the README target.
- **Idioms.** Every scenario of the fixtures uses at least one (the naming Givens). An idiom is an English
  claim ("this sentence means that composition") that someone has to sign, like a piece.
- **The echo is unreviewed.** Its templates are the builder's; no reader has been asked whether they catch a
  wrong meaning (plan nodes K1, V5).
- **The glue script is one script.** It handles suites that split by cases on Givens; it cannot instantiate a
  parameter that names a computed number. Where it fails the rule needs a hand proof or stays NOT-PROVED.
- **Frames 12 to 14 and counting with a number have no surface form** and are tested on hand-written
  instances only (ten on the wallet and the ledger, ten on the toy operation).
- **The comparison of definition and checker has power only on the toy operation.** On the fixtures a claim is
  almost never false and no call is silent; both readings have one author.
- **Three reworded rule lines say less than the lines they replaced** (total_fits, batch_then_total,
  whole_batch); the pieces to say more do not exist.
- **Rule grammar.** One operation or a `followed by` sequence per clause; `for which` takes one condition;
  no rule about two different operations of one system at once.
- **A reading and its flat statement share the Aeneas model and the search grid.** The equivalence removes
  the generator and the old glossary from what a verdict rests on; it does not add evidence about the Rust.
- **Cost.** `./run.sh` took 3 min 56 s with the Lake cache cold for the new modules and 1 min 51 s warm
  (load average 58 to 120 from other agents); the three new Lean scripts (reading search, links, frame tests)
  cost about 17 s, 23 s and 4 s of CPU. Not measured on an idle machine.

## 15. End to end for a new sentence: Rust readings per piece, generated obligations, two-run frames (added 2026-11-10/11)

Section 14 left a NEW sentence (one with no entry in the old whole-phrase glossary) with a reading, an echo and a search on the
model. This section is what takes it the rest of the way. Nothing here changes what an older scenario's verdict rests on.

### 15.1 The Rust side is compositional

- **One Rust reading per piece** (`wallet-bdd/src/pieces.rs`): `eval` has one arm per domain word and modifier, `run_op` /
  `accepted` / `internal` bind the operations to the compiled crates, `frame_content` has one arm per one-call frame,
  `frame2_content` per two-call frame, `variation` and `reference` one arm per relation and reference function. The fail-closed
  defaults are written once, in `holds_at` / `holds_at2`, the counterparts of `Frames.Op.HoldsAt` / `HoldsAt2`. A call that
  panics is "no answer". The readings were written by the same agent as the Lean pieces, in the same pass. When a meaning
  changed (candidate 2's reference, 16.6), the Lean, tree-evaluator and typed readings were changed together. The two
  references that are code operations call the compiled crate itself. Agreement therefore shows consistency, not
  independent confirmation.
- **Composition trees** (`clausal/trees.py` writes `build/trees.json` at `gen`). Two kinds of entry:
  - `steps`: one per distinct step FORM. The step text with every actor name, literal and outline value replaced by a named
    capture, and the tree with those captures as leaves. Literals are captured too, so one form serves an outline row, a plain
    scenario and a replayed counterexample.
  - `readings`: every compiled reading (scenario or Rule) with its grid of generated inputs.
- **One generic cucumber step** (`wallet-bdd/tests/bdd.rs`). Every step form's regular expression is registered with the same
  function; an empty named group `T<n>` says which tree. Given: `<the measure that is the whole of an actor> is <value>` builds
  the actor (pieces marked `builds: true`: a wallet's balance, a ledger's balances); any other Given must hold on the state
  before the first When, else GIVEN-FALSE. When: runs the operation; no answer fails the step. Then: each frame of the step, on
  the state before the first When, the state now and the last answer. A step that does not compile has no entry, so cucumber
  skips its scenario as before.
- **The comparison** (`wallet-bdd/tests/grid.rs`, `clausal/ppath.py`). The Lean side prints, per reading and grid point, one
  character per unit scope, per relation between two calls and per claim (`RBITS`, `lean/Run/ReadingSearch.lean`); the Rust
  side writes the same string from the compiled crate (`out/rust_bits.tsv`). A difference is fatal (`PIECE READINGS DISAGREE`).
  This is one check of two things: that each Rust reading says what its Lean piece says, and that the model behaves as the
  compiled Rust at those inputs. It cannot tell which of the two is at fault.
- **What it replaces**: the 44 hand-written steps. The old whole-phrase predicates of `src/lib.rs` stay only for the grid
  comparison of the old glossary's definitions.

### 15.2 The flat proof obligation

- **Where**: `lean/Wallet/Obligations.lean`, generated at `gen` for every new scenario and every compiled Rule line
  (`clausal/oblig.py`). Proofs go in `lean/Wallet/Proofs/<feature>/<scenario>.lean` or
  `lean/Wallet/RuleProofs/<feature>/<rule>.lean` as a theorem named exactly `<id>` of type exactly `<id>.obligation`.
- **How it is generated**: each frame has a `flat:` template in `clausebook.yaml`, its content at one call with no frame
  library in it (`{m}` read before the call, `{m'}` after, `ans` the answer). Per unit (a scenario, or one clause of a Rule):

      claims about every call          ∀ params st inp, H → ∃ ans st', RUN ∧ Q₁ ∧ … ∧ (acc ans → Qₖ) ∧ (¬ acc ans → Qₗ)
      only accepted / rejected claims  ∀ st inp, H → ∀ ans st', RUN → (acc ans → Q₁) ∧ …
      a claim comparing two calls      ∀ st inp st2 inp2, H → H₂ → rel → ∃ ans st' ans2 st2', RUN ∧ RUN₂ ∧ Q

  RUN is the model call written out (`f st inp = ok (ans, st')`; for a `&self` function `f st inp = ok ans ∧ st' = st`; one ∃
  per earlier call of a sequence and per bystander).
- **What it rests on**: nothing by itself. `lean/Run/Links.lean` holds a generated script for
  `<id>.reading_iff_obligation : <id>.reading ↔ <id>.obligation`; the link audit checks its type, its axioms and that its
  proof uses no proof of either side. With it and a supplied proof, `<id>.reading_holds` (scenario) or `<id>.proved` (Rule) is
  the reading itself as one theorem.
- **Stub**: created once, `sorry`. A Rule gets one only when no universal scenario beneath it is a usable part.

### 15.3 Verdicts of a new sentence

| Verdict | Needs |
|---|---|
| PROVED-FOR-ALL / PROVED-INSTANCE | proof of the obligation (right name, right type, compiled) + the equivalence + the carried theorem + (scenario) `reading_sat` at the grid point the search found |
| REFUTED | the reading search finds a point where a claim is false and `<id>.refuted` (or, for a Rule, `.refuted2`) is kernel-checked there. The report also says whether the compiled Rust fails the claim at that point |
| COUNTEREXAMPLE | found, not confirmed in the kernel |
| TESTED-ONLY | neither. For a Rule this replaces NOT-PROVED |

Rows of a new scenario: the model side evaluates the reading itself at the row (`RROW`), the Rust side is the cucumber run.
A Rule may be proved three ways, tried in this order: generated glue from its scenarios, a supplied proof of its obligation, a
hand-written proof of the reading itself (the two older rule proofs).

### 15.4 Refutation at a counterexample, generalised

`oblig.refutation` writes one script for every shape it covers. It first proves a witness
`∃ out, <model call at the point> = ok out ∧ <the claim's content is false of out>` by stepping the model (or its step lemma),
then feeds what the reading says into it.

| Shape | How |
|---|---|
| every call of one operation | the reading gives an answer and the claim; the witness's output is that answer |
| accepted or rejected calls only | the reading is applied to the witness's output; the witness also says which kind of answer it is |
| two calls compared | one witness per call. Monotone: the class holds of the first and not of the second. Same answer (and its conditioned form): one answer is an acceptance and the other is not; both orders are tried |
| a sequence of two calls | the facts of each call from its hand-proved step lemma (`Bdd.post_of_spec`), then arithmetic |

Not generated: longer sequences, sequences without step lemmas, a two-run claim narrowed to accepted or rejected calls,
scenarios with a bystander, two answers that differ without one being a rejection.

### 15.5 Two-run and reference frames at the surface

- **Domain-word kinds**: `variation` (a relation between two calls; Lean type `Frames.Variation σ α`) and `reference` (a
  reference function; `Frames.Term σ α (ρ × σ)`). Each names its operation (`for_op`); used with another operation it is
  ILL-TYPED. They are constants: no lambda is put around them.
- **Rule forms**: "never loses acceptance when <relation>", "never loses that <class> when <relation>", "agrees with
  <reference>", "gives the same answer when <relation>", "gives the same answer when <relation>, if <class>".
- **New frames**: 15 `Within` / `Covers` (containment between a collection of the answer and a collection of the input before
  the call; "every <answer collection> is a <input collection>" and the reverse) and 16 `IndependentGiven` (frame 14 under the
  condition that the first answer is in a class; both calls must still answer). New modifier `some_of`.
- **Echo**: a two-run rule prints "(TWO calls are compared …)" and default D10.
- **Search**: the grid of a two-run rule has a second state and input over the same samples (4,356 points for a transfer).

### 15.6 Limits

- The comparison of 15.1 is a test on a small boundary grid and both sides have one author.
- A wrong `flat:` template cannot make a false sentence PROVED (the equivalence fails), but it can make a true one unprovable.
- The obligation of a clause repeats the hypotheses for each two-run claim; a rule mixing several two-run claims gets one
  conjunct each.
- The step forms are matched by regular expressions built from the literal syntax of each type. Two forms that match the same
  text would be reported by cucumber as ambiguous; `clausal steps` reports forms that compile to different trees.
- New sentences are outside the suite adequacy note and the input-coverage table (both are built from the old flat statements).

## 16. Layered evidence from one compiled rule: generated property tests and Kani harnesses, feed-back (plan node E1, added 2026-11-11)

K2 (`compare/TRADES.md`) measured that hand-written property tests and Kani harnesses find nearly every falsifiable rule and that
proofs give the only unbounded result. This section makes the tool produce the first two itself, from the composition tree it
already has, and feeds what they find back to the Lean side. No test code is written per rule.

### 16.1 One generated predicate

- `clausal gen` writes `build/trees.json` (15.1). `clausal/evgen.py` reads the same file and writes three Rust files:
  - `evidence/src/checks.rs`: per compiled reading (scenario or Rule line) one function `check_<n>`. It is the reading at one
    point as straight-line typed Rust: per unit its scope (the Givens / "for which" / "internal"), the call or calls on the
    COMPILED crate, and per claim the frame's content under the defaults. It returns the bits the grid comparison prints and
    whether every claim holds.
  - `evidence/src/table.rs`: per reading its variables and types, which variable a Given FIXES, which belongs to the second
    call of a two-run rule, the numbers written in the sentence, and a glue function from generated values to `check_<n>`.
  - `evidence/kani/src/harnesses.rs`: per reading and per rung of the size ladder one `#[kani::proof]`.
- **The typed piece readings** (`evidence/src/typed.rs`, hand-written once): one function per domain word, modifier, frame
  default, relation and reference, over plain types (a ledger is `&[u64]`, numbers are `u128`). The tree evaluator of
  `wallet-bdd/src/pieces.rs` works on JSON and dynamically typed values, which Kani cannot digest; hence a typed twin.
  It is a THIRD reading of each piece by the same author and is not trusted (16.2).
- Both harnesses assert the same `check_<n>`. A reading the generator cannot type is listed as skipped
  (`build/evidence_gen.json`); none is at present.

### 16.2 The property test

- **Runner** (`evidence/src/main.rs`, generic): proptest with shrinking, 10,000 cases IN SCOPE per reading, one seed per run
  (20261111) mixed with the reading id. An input outside the reading's scope is rejected and does not count.
- **Generators are derived, not written per rule.** From the types: amounts weighted to the ends of the u64 range, small
  numbers, and values at or next to a number already drawn for the same case (a balance, a sum, the room left below the
  maximum); account numbers mostly existing positions, otherwise the length give or take one, small numbers, anything; lists
  up to 6 items; a list of balances sometimes completed so that its sum is the maximum give or take one. From the Givens: a
  variable that a Given fixes (`ledger Main holds the balances <balances>`) is not generated, it IS that value; the numbers
  written in the sentence join the pool of edge values; every other Given is kept by rejection. For a two-run rule the second
  call is the first again, a small change of it (the same route with another amount, the ledger extended or changed at one
  account), or independent.
- **What proptest shrinks is the choice** (which edge, which neighbour), not the number, so a shrunk input stays on the edge
  that made it fail. Shrunk inputs are small but not always minimal.
- **The typed reading is checked at every case**: the runner also evaluates the same tree with `pieces.rs` (`eval_point`,
  moved there from `tests/grid.rs`) and compares the bits. A difference is READING MISMATCH, reported per reading and fatal
  for the run. A reading that does not finish is "no answer in time" with the input it was evaluating; the runner then stops
  and the caller starts the remaining readings in a fresh process, because the hung thread cannot be stopped.

### 16.3 The bounded check

- **One harness per reading and rung.** Every integer is symbolic. A list of balances has at most A items and a batch at most
  B. A reading with no collection has one harness and no size bound.
- **The ladder is fixed**, the same for every rule and every mutant: (A, B) = (2, 1), (2, 2), (4, 1), (2, 3), (6, 4). It
  comes from TRADES.md section 4 (a third and fourth account is what some bugs need under a total rule, a third transfer
  what others need, rules without a total verify at 6 and 4); the first rung was added when the two-step rules gave no answer
  at (2, 2). Rungs that do not differ for a reading (no batch: only A matters) are run once.
- **Result per rung**: verified, failed, or no answer in the time allowed (30 s per harness in `./run.sh`, 6 harnesses at a
  time; `./run.sh --kani-timeout=N --kani-jobs=N`). All three are printed. A failed harness is run again for Kani's concrete input, which is decoded from the
  harness's known layout and REPLAYED on the compiled Rust through the property-test runner (typed predicate and tree
  evaluator); "NOT reproduced" would be printed if the replay did not fail.
- Under Kani a panic of the code under test is a failed check of Kani's own, not "no answer". For a claim about every call
  that is the same thing; for a claim about accepted or rejected calls only it is stricter than the reading. The failed
  check is named in the result.
- Kani-specific choices in the generated code (taken from K2's harnesses): a ledger is built from a fixed array cut to a
  symbolic length, a batch is mapped from a fixed array, nothing of symbolic size is cloned.

### 16.4 Feed-back

- `./run.sh` step 5b runs both harness sets before `derive` and writes `out/evidence.json`.
- `clausal witness` writes `lean/Run/Witness.lean`: every falsifying input, evaluated on the Lean model through the reading
  (`decide` of its scope and of each claim); for a scenario with an old flat statement also as one more row of that statement.
- `clausal derive` (`evidence.feed_back`): an input that fails on the model too becomes the reading's counterexample where
  the grid search has none, carrying its source. From there nothing is new: the refutation scripts of 15.4 (Rule lines, new
  sentences) or of section 6 (flat statements) make the kernel-checked `¬ statement`, and the report prints REFUTED or
  COUNTEREXAMPLE with "source: the generated property test / bounded check".
- **MODEL MISMATCH**: the compiled Rust fails (or gives no answer) at the input and the model holds or is out of scope there.
  The verdict is flagged, the run fails, and the block prints it. It is a finding about the translation link.
- An input the grid search also covers changes nothing: the grid's counterexample is kept.
- The model leaves the width of `usize` open (at least 32 bits), so an account number above 4294967295 has no literal there.
  A falsifying input with such a number (Kani likes them) is reported as found on the compiled Rust and NOT EVALUATED on the
  model, with that reason. It is not fed back.
- A scenario with two Whens gets the input as one more row too; its verdict is then COUNTEREXAMPLE (no kernel refutation is
  generated for a multi-When statement, as before).

### 16.5 The evidence ladder in the per-Rule block

`clausal/rules.py` prints, from the graph alone (`attrs.reading.ladder` of the rule and scenario nodes), four rungs with a
"rests on" line each, every falsifying input with its source and what the model said, and STRONGEST HELD:

| Strongest held | When |
|---|---|
| a kernel-checked REFUTATION | a `¬ statement` theorem exists; the source of the input is named |
| a COUNTEREXAMPLE, not confirmed in the kernel | false on the model and the Rust, no script closed the refutation |
| none that can be relied on (MODEL MISMATCH) | the two sides disagree at an input |
| PROOF | a kernel-checked theorem of the rule statement for all inputs |
| BOUNDED CHECK only | no proof; Kani verifies at one rung at least and fails at none; the sizes are printed |
| PROPERTY TEST only | no proof, no bounded result; no generated input falsifies it |
| EXAMPLE ROWS only | nothing but rows |

Nothing is called proved without a kernel-checked theorem; a rule with rungs 2 and 3 only is TESTED-ONLY in the verdict line.

### 16.6 The two candidate rules of the trade map

TRADES.md section 5 proposed two rules for the four mutants no arm caught. Both are in `features/ledger_rules.feature`,
through the "agrees with a reference" frame, where the reference is another operation of the same code:

| Rule | Reference (new domain word) | Lean | Verdict on the unmutated code |
|---|---|---|---|
| A batch applied as a whole agrees with the same batch applied transfer by transfer and kept only if every transfer is applied | `l.ref_whole_by_batch` | `L.refWholeByBatch`: `apply_batch` of the model; accepted with its ledger if it applies every transfer, else rejected with the ledger as it was | PROVED-FOR-ALL (hand-written proof from the two step lemmas) |
| A batch agrees with its transfers applied one at a time until one is rejected | `l.ref_batch_by_transfers` | `L.refBatchByTransfers`: `apply` of the model once per transfer (`L.foldApply`) | TESTED-ONLY on purpose: property test and bounded check only |

Two things to decide in the Clausebook track: these references mention the generated model, which `lean/Ledger/Pieces.lean`
reserved for operations; and the second is the inductive pure model of a batch that 12.8 kept out of the glossary, here said
as "agrees with". TRADES.md proposed both as two-run rules; the two-run frames compare answers only, not ledgers.

### 16.7 Limits

- The generators are generic. An input that needs a structure they seldom draw, or a value that occurs only in the code,
  is not found by the property test; the bounded check finds such a value when the input lies within its sizes.
- A bounded result says nothing beyond its sizes, and where a rung gives no answer it says nothing at that size.
- The typed readings and the tree evaluator have one author; their agreement is tested at every generated case, not proved.
  Under Kani only the typed reading runs.
- The feed-back needs the model to be evaluable at the input. Where the pipeline cannot evaluate a model (a loop that does
  not terminate crashes step 5, a model that does not build stops step 4) `./run.sh` stops before step 5b, so the generated
  harnesses do not run in it at all; `python3 -m clausal evidence` still runs them on the compiled Rust.
- The mutation harness runs every pipeline with `--quick` and repeats a mutant run WITH the bounded check only when the
  quick run shows no scenario false (`mutation/run_mutants.py`).
- The bounded check costs minutes per run; `./run.sh --quick` skips it.

## 17. Narrowed claims: refused when they say nothing; printed coverage taken from the Calls value (plan nodes Q1, Q2, added 2026-11-12)

Source: `docs/studies/2026-11-12/readability-critique.md`, sections 2.1 and 2.2, and the adopted synthesis
`readability.md`. Both findings were reproduced on this tree before anything was changed: the four sentences of 2.1
compiled without any flag, and the two shapes of 2.2 printed coverage that contradicted their Lean.

### 17.1 What "narrowed" means

`successful` and `rejected` set `Frames.Op.calls` to `.accepted` / `.rejected`. `Op.HoldsAt` and `Op.HoldsAt2`
(`lean/Frames/Core.lean`) then ask for the frame's content only of calls that answer and whose answer is of that kind.
The narrowing can be written on the subject ("a successful transfer") or, in the Then voice, on the claim ("for a
transfer, if it is accepted, ..."); both give the same Lean.

### 17.2 Q1: a narrowed Rule clause that holds of every operation is refused

**The defect.** Under a narrowing the frame's content is proved under the hypothesis that the answers are of the
narrowed kind. If the content follows from that hypothesis, the statement holds whatever `run` is. Such a rule has
`True` as its scope, so `reading_sat` is satisfied, and accepted calls occur on the grid, so `COVERS NO CALL ON THE
GRID` is silent.

**The theorems** (`lean/Frames/Narrowing.lean`, core Lean only, built with the `Frames` library):

- `Op.covered op r`: the condition a narrowing puts on an answer; `Op.narrowed op`: `op.calls ≠ .every`.
- `Narrowed.holdsAt`, `Narrowed.holdsAt2`: if the content follows from `covered`, the frame's pointwise form holds at
  every call (pair of calls). No hypothesis mentions `run`. `#print axioms`: none.
- One named theorem per reason the compiler can give: `covers_no_call`, `covers_no_call2`, `alwaysAnswers`, `always`,
  `never`, `ifThen`, `onlyIf`, `monotone_holds`, `monotone_fails`, `independentOf`, `independentGiven_view`,
  `independentGiven_fails`. Each takes one side hypothesis about the operation's acceptance.
- `Narrowed.Critique.*`: the five facts of critique 2.1 as stated there (any `run`, any variation). The fifth
  (`neverChanges_of_silent`) is about one operation that never answers; it is not a reason for a refusal.

**The decision** (`clausal/clausal/narrowing.py`, called from `Compiler.rule` after the one composition is settled,
so it never changes which composition is found):

- `REASONS` maps a frame to the theorems that can apply and to what each needs: the class in hole `c` holds of every
  covered answer, or of none, or any two covered answers are the same, or nothing.
- What narrowing settles for an operation is declared in its entry of `clausebook.yaml`:
  `narrowing: { accepted: { holds: [...], fails: [...], one_answer: true }, rejected: { ..., no_call: true } }`.
  The shared class `accepted` is the operation's own notion and needs no line; `not` flips a class.
- A refusal is a `Problem` with status `SAYS-NOTHING`. Its message says: vacuous by narrowing; which calls the clause
  is about and which word asked for it; why the claim follows; the Lean statement; the theorem; and that no code can
  break the rule. The hint says how to rewrite.

**Why this is not a pattern list.** Nothing declared and nothing in `REASONS` is trusted. `clausal gen` writes
`lean/Run/Narrowing.lean` and `./run.sh` runs it and stops if `clausal narrowing` finds a wrong answer:

1. every declared fact is kernel-checked (fixed tactic `narrow_side`);
2. every fact that could be written for an operation and was not is attempted with the same tactic and must fail, so
   the lists in the book are exactly what that tactic proves;
3. every control sentence the compiler refuses (`controls/narrowing.feature`, tag `@says-nothing:<theorem>`) is
   compiled once more with the refusal off (`Compiler(voc, refuse_vacuous=False)`), and "for every `run`, the claim
   holds" is kernel-checked through the theorem the refusal named, and again by the generic tactic
   `vacuous_by_narrowing`. The statement is the claim's own Lean with the operation replaced by
   `{ op with run := run }` (`Claim.any_run`);
4. every narrowed claim that was not refused (all fixture Rules, and the controls that must compile) gets the same
   statement and `vacuous_by_narrowing`, which must fail. If it succeeds, the claim says nothing and the table
   missed it: the run fails with `SAYS NOTHING BUT WAS NOT REFUSED`.

**Limits.** The two tactics are proof search. A true fact they cannot prove is not declared, and a vacuous claim
that depends on it is not refused and not caught by step 4. Classes with holes ("is rejected with <error>") have no
facts. Only Rule lines are refused; a scenario's Then is not examined. A contradictory narrowed claim ("a successful
transfer is always rejected") is not vacuous (it holds only of an operation that never accepts) and is not refused.
Refusal is per claim: a line with one vacuous clause among others is refused whole, which is stricter than "the
reading holds of every operation".

### 17.3 Q2: the printed coverage is the Calls value

**The defect.** `echo_rule` chose the coverage lines from the subject's modifiers. A narrowing written on the claim
left the subject bare, so the echo printed "every such call, accepted or rejected [default D2]" and "the call gives
an answer [default D1]" over a statement that covers accepted calls only. Every narrowed two-run rule printed "both
must give an answer [default D10]", which `HoldsAt2` does not require under a narrowing.

**The fix.**

- `Claim.calls` is set in `Compiler.claim`, at the place the claim's operation text is written, from the `calls:`
  field of the modifiers applied (`successful: accepted`, `rejected: rejected`; otherwise `every`).
- The lines are in the book, not in Python: section `coverage:` of `clausebook.yaml`, one entry per constructor of
  `Frames.Calls` (`calls.every`, `calls.accepted`, `calls.rejected`) with `covers`, `answer`, `prefix`, `two_calls`,
  `weakening` and `removes` (the defaults a narrowing removes: D1, D2, D10). The top-level `weakenings:` key is gone;
  its two texts are the `weakening` fields.
- `echo_rule` and `echo_scenario` print a `covers` slot per clause from the Calls values of its claims, require an
  answer only where a claim covers every call, print the two-call note of the claim's own Calls value, and drop the
  defaults the narrowing removes.
- Sign-off: the coverage entries are in `all_ids`, so they are signed by id; `piece_digest` now also hashes the text
  of every default an entry names (`defaults:`, `removes:`), for every entry; and each reading lists the coverage
  entries it prints among its pieces, so `--strict` and the "n of m pieces signed" counts include them.

**The check.** `lean/Run/Narrowing.lean` asks Lean for `(op).calls` of every claim of every compiled reading
(`#calls`, `lean/Bdd/NarrowingAudit.lean`: elaborate, `whnf`, print the constructor). `clausal narrowing` compares
(a) that constructor with `Claim.calls`, and (b) the coverage lines found in the printed echo (looked up among the
book's texts, `narrowing.printed`) with the lines the book gives for the constructors Lean reported
(`narrowing.expected`). The two faulty shapes are control lines tagged `@covers:<calls>`.

### 17.4 Controls

- `python3 -m clausal.selftest` (no Lean): the four sentences are refused, with the reason; they compile with the
  refusal off; every `@says-nothing` control is refused for its tagged theorem and every theorem is exercised; no
  fixture Rule changes with the refusal on or off; the two shapes print the narrowed coverage; the coverage check
  reports the old printed lines, a wrong Calls value and a missing answer; a fixture claim proved for every `run`
  fails the run; the coverage text is under the digest.
- `./run.sh`: the kernel side of the same controls, on every run.

### 17.5 What changed for existing sentences

Measured against the tree before this change (85 compilations: 39 scenarios, 46 Rule lines): the Lean statement, the
status and the list of defaults of every one are identical. The echo text differs in 7: five Rule lines now print
"ONLY accepted calls [asked for]" where they printed "ONLY successful calls [asked for]" (the line is chosen by the
Calls constructor), and two scenarios with a narrowed Then list the narrowing in the `covers` slot as well as on the
claim's line. The coverage line moved from an unnamed continuation of `applies to` to a slot of its own, `covers`.

### 17.6 After review: four corrections (2026-11-12)

A review of 17.2 to 17.5 found four defects. Each is fixed; none is argued away.

**A must-fail attempt counts only if its statement was read.** Parts 2 and 4 of `lean/Run/Narrowing.lean` expect a
script to fail. Lean also recovers from a statement that does not elaborate, by putting `sorry` in the type, and both
cases leave `sorryAx` among the axioms. `#narrowing_report` reported both as `notproved`, so a statement the generator
wrote wrongly would have passed as "not provable". It now reports four states: `proved`, `notproved` (the type has
no `sorry`, the proof does), `badstatement` (the type has `sorry`), `missing` (not declared). `collect` takes only
`notproved` as "not shown"; any other state for a must-fail item, and anything but `proved` for a must-prove item,
fails the run. The script carries one statement broken on purpose (`NarrowingRun.control_bad_statement`, an operation
that does not exist) and one name that is never declared; `collect` fails unless they come back `badstatement` and
`missing`. One more expected error in `out/narrowing.log`.

**The sequence note is a coverage line.** A Rule clause about a sequence printed, from a string in `echo_rule`,
"every call in it must answer". True when the clause covers every call (`HoldsAt` then asks for an answer of the
whole sequence). False under a narrowing: no call has to answer, and a sequence in which a call gives no answer is
outside the clause. The note is now the `sequence` text of the `coverage:` entry of each Calls value in the clause
(`sequence_scenario` of `calls.every` for a scenario with several Whens, which always has a claim about every call),
so it is under the sign-off digest. The check covers it: `#calls` also prints whether the claim's operation is a
sequence (its elaborated term mentions `Frames.Op.andThen`), `narrowing.expected` asks for one sequence note per
Calls value of a clause Lean says is about a sequence, and `narrowing.printed` turns any line that starts
"(of a sequence" and is not a line of the book into a token that never matches. The texts of `calls.accepted` and
`calls.rejected` also say that acceptance is judged on the LAST call's answer and that earlier answers are not looked
at: `Op.andThen` takes `accepted` from the second operation and runs it whatever the first answered.

**One clause, one narrowing word.** The subject parser kept the last of several leading words ("a successful internal
transfer" was compiled as every internal transfer), the claim parser kept the last of several "if it is ...", and a
narrowed subject with a narrowed claim was emitted as `((op).successful).rejected`, where the last `calls := ...`
wins. Printed coverage and Lean agreed in all of these, so the coverage check could not see them: the meaning was
changed before Lean. Every leading word is now read (`strip_words`), and a clause with more than one is refused:
status `UNSUPPORTED`, code `NARROWED-TWICE`, naming the words and why (no call is both; the same narrowing twice;
`internal` with a narrowing word on the subject is not a composition of the book). The refusal ranks before "no
composition" so it is the message shown. `Compiler.calls_of` raises if two Calls-setting modifiers ever reach it.
What can still be said: scope on the subject, narrow on the claim ("for an internal transfer, if it is accepted, ...",
a control line). Combining the two words on the subject was not added: that would be new grammar, and a reader of
"a successful internal transfer" gets a refusal with that advice, not a guess.

**The comparisons are scripts in the repository.** `compare/against/` (`verdicts.py`, `readings.py`, `bounded.py`;
see its README): this tree against a git revision, read with `git show` / `git archive`.

Controls added: 9 lines in `controls/narrowing.feature` (2 narrowed sequences that must compile and print the
narrowed sequence note, 6 `@narrowed-twice`, 1 internal operation narrowed on the claim); self-test checks for each
correction, each seen to fail with the correction taken out (statement state, sequence note printed, sequence note
checked, second word overriding, subject and claim both narrowed).

## 18. The Clausebook as a list of books; every accepted form in the book; `clausal book check` (plan nodes C1, Q3, added 2026-11-12)

The flat `clausebook.yaml` that sections 14 to 17 name is now four books under `clausebook/`: `core.yaml`
(frames, modifiers, coverage, grammar, defaults), `ledger.yaml` (the ledger pack), `local/ledger.yaml` and
`local/wallet.yaml` (the fixtures' own words and operations), listed in `clausebook/project.yaml`. Where an earlier
section says "`clausebook.yaml`", read "the book that defines the entry".

The design notes are beside the books:

- `clausebook/ASSIGNMENT.md`: which entry went where and why, written before the split, with the changes made while
  building.
- `clausebook/README.md`: the loader (a list of books, what each book states, per-book sign-off files), the check
  that core stands alone, the dependence on the fixtures that remains, where each formerly hard-coded form now lives,
  the registration lint (`python3 -m clausal book check`) and the violations it reports on today's book.

Three things a reader of the earlier sections should know:

- **Core has 48 pieces, not 53.** The five modifiers that read a literal of a fixture type as a value moved to the
  pack (four) and to the ledger's local book (one). Their ids, text and Lean are unchanged.
- **The compiler holds no surface form.** The articles, the narrowing words and prefixes, the acceptance verb phrases
  and the words that join a Rule line are read from `core.yaml`. Section 14's description of `Compiler.rule_part`
  and `subjects` is still right about what is accepted, and out of date about where it is written.
- **A reading's list of pieces is longer.** It now ends with the grammar entries the line was read through and every
  default printed with it, so the sign-off of a reading covers them.
