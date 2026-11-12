# T9 planning study: `tdf-core` staged build plan

Read-only study; nothing was built or run. During the study `slice/` was renamed to `clausal/`, so Clausebook and compiler paths below use the new names (read under the old ones).

## 0. Findings that change the plan

1. **The integer core in Go is not what production calls.** `SnapshotDecider.Decide` (`private/tdflite-src/internal/lite/kas/decider.go:108-127`) calls `snapconform.ABAC.Evaluate` (`pkg/pdp/snapshot/snapconform/abac.go`). That evaluator groups by parsed strings and reads the hierarchy claim as a string. The pure-ID `DecideResource` (`pkg/pdp/snapshot/decide.go:70-184`) has no production caller (pilot finding N11, `private/tdflite-pilot/OWNER_SUMMARY.md`). So `tdf-core` is a new arrangement of the ruled specification, not a port.
2. **There is no ruled ID-level model.** The Lean model has today's ID core (`private/tdflite-pilot/lean/TdfModel/Snapshot.lean:538-585`). The ruled model stops at the string level (`t3r/lean/Ruled/Spec.lean`, `Model.lean`). The Rust core needs a small new ID-level specification and a bridge theorem to `Spec.release`.
3. **Compiling the vocabulary in Rust can remove the named facts.** Guarantee 8 for the Go rests on 8 unproved facts (C1–C7 about `snapshot.Compile`, plus `FoldsOnce`; `t3r/SPEC.md` §5). If `tdf-core` does its own string-to-ID compile and proves those facts of it, the Rust result is unconditional. This is the largest gain available over stage 1.
4. **The pipeline is hardwired to two crates.** `clausal/run.sh:90` loops `for crate in wallet ledger` and line 115 names `Wallet.*` and `Ledger.*` Lean modules. A third project needs this parametrised; that is part of C1/R1, and T9 is blocked on it for the Clausal steps only.
5. **Lean versions differ.** The pipeline pins Lean v4.35.0 (`clausal/lean/lean-toolchain`); the ruled spec is on v4.36.0-rc2 with no Mathlib (`t3r/lean/lean-toolchain`). Whether `Spec.lean` and `GoString.lean` build under v4.35.0 was not checked.
6. **The README's ABAC sentences do not match today's grammar.** "Adding an entitlement to a subject more-never-loses an accepted key-release decision" (`README.md:67`) matches no form. The only monotone forms are "never loses acceptance when {variation}" and "never loses that {class} when {variation}" (`clausal/clausebook.yaml:938`). Judged from the form list; not run through the compiler.
7. **Go decision code is unchanged at the owner's checkout.** `diff -rq` of `pkg/pdp` and `internal/lite/kas` between `/Users/will/dev/tdflite` (`e75f6340`) and `private/tdflite-src` (`4aca7ca0`) shows only test files. There is no `Cargo.toml` in the TDFLite checkout.
8. **`AGENTS.md` is stale on privacy.** It still calls `tdflite-ideas/` and `docs/TDFLITE.md` private; both are tracked (`git ls-files`; `DECISIONS.md`, "Owner's steer").

## (a) Open owner decisions

A default is given for each so work proceeds; each is a parameter or a vector set that can be re-run. Sources: `t2/RULINGS.md`, `t2/AFTER-REVIEW.md`, `t3r/README.md` ("Choices…"), `t3r/SPEC.md` §10, `t3r/CHANGES.md:63-77`, `t2/WORKSHEET.md:106-125`.

| # | Question | Default | Blocks |
|---|---|---|---|
| O1 | D4(a) third sub-choice: is `[SECRET, MARS]` "no level"? | Yes (already in `Spec.lean`; vector `0023`) | T9.4 only; one vector flips |
| O2 | Guarantee 4: restricted form only, or also "a subject with one higher level keeps access"? | State and prove both | Nothing; sets pack contents (c) |
| O3 | D1 namespace compared ignoring case; repeated identical level counts as two; "rejected" means no level, not a refused token | All stand | T9.4 only (vectors `0007`, `0022`) |
| O4 | **New.** Case folding in Rust: ASCII only, with any non-ASCII byte in a name, value, label or claim failing to resolve? Go folds Unicode; the profile has no modelled `str` methods (`census/PROFILE.md` rule 5) | ASCII only, fail closed. Consistent with ADR-0028 as summarised in `t3r/CHANGES.md:69-71` | T9.4 design and the bridge theorem; non-ASCII cases become a classified difference in T9.6 |
| O5 | D5 mechanism: fold at match (rulings) or normalise once at ingress (ADR-0028)? With `strict_case` on, refuse? | Normalise once at intake; permissive posture; `strict_case` a later parameter | T9.4 structure, not verdicts |
| O6 | Scope of core v0: `read` action only, one subject, claims mode? Go has action planes, per-action ranks and a subject list (`decide.go:70-114`, `subject.go`) | Yes; anything else is not offered | T9.1 types |
| O7 | R10: which client identity (caller's, or the enforcement point's as TDFLite's own `docs/DECISIONS.md:1149-1153` says)? | Core takes an abstract client reference: not established, known, or known but named by no trigger. The shell chooses what to pass | Not the core. Blocks interpreting shadow-mode numbers: item 2 denies wherever a scoped trigger exists and no identity is passed |
| O8 | First listed hierarchy value is highest; requirement is the highest bound level (worksheet open question 2) | Yes | Nothing; one comparison if reversed |
| O9 | Translator: plain patched Aeneas (the T9 node text) or hax contracts (the owner's plan, step 4)? | Plain Aeneas with the `census/fork` patches; contracts live as Clausal sentences. Rust written so hax attributes can be added | T9.2 onwards |
| O10 | Where the crate lives and whether it is tracked (see (b)) | Standalone local git repository at `private/tdf-core/`, unpublished; `clausebook/abac` tracked here | T9.1 location; reversible until pushed |
| O11 | Guarantee 6: what a caller observes (error code, obligation list, size; timing and audit?) and whether "this wrapped key is valid here" counts as learning about the key (`SPEC.md` §6; worksheet question 4) | Response value only, no timing; conditional on binding outcome | T9.5 theorem statement |
| O12 | Does key material enter the Rust core? If unwrap and re-encrypt stay in Go, a Rust `Permit` type constrains no Go code | Core is generic over an opaque key type; crypto stays in the shell; Go-side KeyGate remains the enforcement | T9.5 claim strength; T9.7 ABI |
| O13 | Packaging: WebAssembly under wazero, or cgo? | wazero (the owner's plan, step 7) | T9.7 only |
| O14 | Guarantee 5 "enforced" means "declared" (ruled, R10 item 4); deeper obligations work is T7 | Stands | Nothing |

- **Shell-only, do not block T9:** R9 refusal code and which repeats count; D6 default when a decider cannot report the setting; D5 in the authorization service and descope primitive.
- **Count mismatch:** `docs/HANDOFF.md` item 5 cites "the eight decisions listed in `t3r/README.md`". That section has eleven bullets; I could not tell which eight are meant.

## (b) The Rust decision core

**Location.** Build as a self-contained crate with no path dependencies.
- Agents may not create anything in `/Users/will/dev/tdflite` (`AGENTS.md`).
- The translator, its pinned nightly and the Clausebook are here; the TDFLite checkout has no Rust or Lean.
- `private/` has no version control (`private/.git` absent), so a crate placed there bare would be unversioned. Hence a nested local repository.
- The crate's final home is the TDFLite repository, as a vendored copy pinned by hash.
- The vectors and Go comparison harness stay in `private/tdflite-pilot/t9/`: they list 40 behaviours the production Go does not yet have.
- The alternative is a tracked `targets/tdf-core/` here. It is simpler for the pipeline but irreversible once pushed. That is O10.

**Layout** (no dependencies, `#![forbid(unsafe_code)]`):

| Module | Content |
|---|---|
| `snapshot.rs` | `Snapshot { value_attr: Vec<u32>, rank: Vec<u32>, attr_rule: Vec<Rule>, trig_unscoped: Vec<u64>, trig_scoped: Vec<ScopedPlane>, deny_unlabelled: bool }`; `enum Rule { Hierarchy, AllOf, AnyOf }`. Dense vectors replace Go's maps (rule 15: maps are axioms) |
| `subject.rs` | `Subject { held: Vec<u32>, level: Vec<Level> }`; `enum Level { None, At(u32) }`. D4(a) is settled at intake, so the core never sees a claim list |
| `request.rs` | `enum Bound { Unresolved, Labels(Vec<u32>) }`; `enum Client { NotEstablished, Known(u32), Unlisted }` (`Unlisted`: identity established but named by no trigger, so no scoped trigger applies). `Unresolved` puts the D1–D3 gate inside the proved core and closes N11 |
| `set.rs` | `contains(xs: &[u32], id: u32) -> bool`, linear |
| `rules.rs` | `attr_satisfied(...)`: one pass over the bound IDs of one attribute |
| `entitle.rs` | `entitled(...)` |
| `oblig.rs` | `plane_mask`, `required`, `subset(required, declared)` |
| `decide.rs` | `decide(...) -> Decision`; D6 rule for the empty list |
| `fmt.rs` | Any `Debug`/`Display`, kept apart (rule 14) |

**Profile constraints applied** (`census/PROFILE.md`):
- No iterator chains (rule 6), no `?` on `Option` (rule 15), no `str` methods (rule 5), no `HashMap`.
- Loops leave by `break` with a flag; inner loops are helper functions (rule 2).
- `v.get(i)` with a `match`, so an out-of-range ID is a Deny, not a `fail`.
- No type named `Slice`, `Array`, `Str` or `Result` (rule 13).

**Loops and invariants.**

| Loop | Kind (p2 terms) | Invariant |
|---|---|---|
| `contains` | search, early exit | no element before `i` equals `id` |
| `attr_satisfied` | read-only accumulation, two flags | `all_ok` iff every bound ID of this attribute in `[0,i)` passes its rule; `any_hit` iff some does |
| `entitled` | loop calling a looping function | `ok` iff every ID in `[0,i)` has a known attribute that is satisfied |
| `plane_mask` | accumulation | bit `k` set iff some `j < i` has bit `k` in `table[bound[j]]` |
| `required` (over scoped planes) | loop calling a looping function | mask is the union over planes in `[0,i)` that apply to the client |

**Two deliberate trades.**
- `entitled` re-scans per label (quadratic in labels per object). This is the shape of `Spec.entitled` (`SPEC.md` §2.6), so the bridge is near-syntactic. Go's aggregate table (`decide.go:118-158`) is an in-place update, the most expensive class in p2.
- `held` is unsorted with linear search, so no sortedness invariant exists.

Both cost speed; neither was measured. Faster versions can be added later and proved equal.

**Expected cost** (`p2/RESULTS.md`):
- p2 measured about 6.0 to 6.1 hand-written Lean lines per Rust line. Read-only loops cost 3.4 to 6.5; a loop calling loops 5.1 to 5.4 own lines (15 to 17 including callees); in-place update 7.5 to 9.0, which this design avoids.
- The core is an estimated 150 to 200 Rust code lines with five loops, so about 900 to 1,200 Lean lines for function specifications.
- The ID-level spec and bridge are not measured by p2. The analogous engine comparison in `t3r/lean/Ruled/Engines.lean` is 350 lines; estimate 400 to 800.
- Caveats: p2 was one crate of textbook loops, 7 of 7 proved, which cannot tell a 70% agent from a 100% one. It had no `u64` mask reasoning; t3r's mask lemmas are over `Nat` and would need bridging to `U64`.

## (c) Guarantees 1 to 8 as candidate Clausal sentences

Shapes are from `clausal/clausal/vocab.py:1002-1010`, `clausal/clausebook.yaml:695-1010` and `clausal/features/ledger_rules.feature`. None was compiled. Every sentence needs the operations and domain words below, which are the `clausebook/abac` pack.

| G | Candidate canonical sentence (today's frames) | Frame | Missing |
|---|---|---|---|
| 1 | `A key release for which some label of the object is not defined by the policy is always rejected` (likewise "is not a label", "is outside the policy's namespace") | `never` via `is always rejected`, `some_of` | Domain words. The two-grounds form needs "or" in a condition; I found `and` splitting (`vocab.py:1221`, not traced) and no `or` |
| 2 | `A key release is accepted only if every label of the object is defined by the policy` | `only_if`, `every` | Domain words only |
| 3 | `A check of a hierarchy attribute is accepted exactly when the subject's level is at or above every bound level`; `A check of an allOf attribute is accepted exactly when every bound value is held by the subject`; `A check of an anyOf attribute is accepted exactly when some bound value is held by the subject`; `A key release agrees with the reference release` | `exactly_when`, `agrees_with` | A second operation (attribute check); "is at or above" |
| 4 | `A key release never loses acceptance when the subject holds more values` | `monotone` | Variation word; its definition must say "same single level" (D4(a)) |
| 4b | `A key release never loses acceptance when the subject's level is higher` | `monotone` | Variation word; unproved today (O2) |
| 5 | `A key release is accepted only if every required obligation is declared by the client`; `For a key release, every listed obligation is a required obligation` | `only_if`, `within` | "required obligation" as a collection; "not entitled, so none listed" needs a count on the answer |
| 6 | `A key release gives the same answer when only the data key differs, if it is rejected` | `same_answer_if` | An operation over the response path with a key in its input. On bare `decide` it is true by typing and proves nothing (`docs/PLAN.md`, T5). Binding-outcome condition belongs in the variation |
| 7 | `A policy load is accepted only if the bundle verifies under the pinned anchor`; `A policy load is accepted only if the bundle is at least as new as the current policy`; `A rejected policy load never changes the current policy` | `only_if`, `never_changes`, `rejected` | A stateful load operation; an ordered pair (epoch, revision); "verifies" as an assumed predicate |
| 8 | `A key release agrees with the reference release` (reference is `Spec.release`) | `agrees_with` | For Rust: provable. For Go: tested only, the Route B evidence class |
| extra | `A key release gives the same answer when the subject's values are reordered` | `same_answer` | Variation word; true under D4(a), false today |

**Pack contents.**
- Operations: key release, attribute check, policy load.
- Collections: labels of the object, bound values, required obligations, listed obligations.
- Predicates: is defined by the policy, is held by the subject, is declared by the client, is at or above.
- Variations: holds more values, level is higher, values reordered, only the data key differs.
- Reference: the reference release.

**Sentences that read badly, with a plainer equivalent.**

| Today | Plainer, same meaning |
|---|---|
| `never loses acceptance when the subject holds more values` | `A key release that is accepted stays accepted when the subject holds more values` |
| `A lookup never loses that there is a result when the ledger is extended` (the worst existing form) | `A lookup that has a result still has one when the ledger is extended` |
| `gives the same answer when only the data key differs, if it is rejected` | `A rejected key release gives the same answer whatever the data key` |
| `is accepted only if every label of the object is defined by the policy` | Reads acceptably |
| `A key release agrees with the reference release` | Short, but hides the content; pair it with the three per-rule sentences |

For the readability track: "stays accepted when…" could replace the monotone form as the single canonical one, with no synonym added. The README sentence should be rewritten to whichever is chosen.

## (d) Intake and the permit token

**Intake (T9.4), bytes in, IDs out.**
- `lower_ascii`, `bytes_eq`.
- `parse_label`: prefix `https://`, exactly five parts, markers `attr` and `value`, nothing after the value.
- `compile`: vocabulary to `Snapshot`, refusing the R8 grammar and, under O4, non-ASCII.
- `intake_object -> Bound`: any failure gives `Unresolved`.
- `intake_subject -> Subject`: values of every claim whose name matches ignoring case; exactly one defined value gives `Level::At`.
- `intake_declared -> u64`.

JSON and token parsing stay outside; the owner's plan tests them differentially. Proof target: C1–C7 of `SPEC.md` §5 as theorems about `compile`, then `decide ∘ intake = Spec.release` on ASCII input. Cost is unmeasured: p2 has no byte-parsing loops. A guess is 250 to 350 Rust lines and 1,500 to 2,500 Lean lines.

**Permit token (T9.5).**
- `Permit` and `Dek` have private fields; only `decide` constructs a `Permit`.
- `release(permit, dek)` consumes both and checks that they carry the same binding hash.
- What Lean can prove is a two-run theorem over a `handle` function generic in the key type. Lean cannot see Rust privacy, so "no public constructor" is enforced by the Rust compiler and tested by a compile-fail test. That is tool-trusted evidence, not kernel-checked.
- Named blocker: O11 and O12. I did not read ADR-0016 or `rewrap.go` beyond the pilot's summaries.

## (e) Three-way oracle

**What exists.**
- Harness `t3rdiff today|ruled|facts|lower` (`t3r/lean/Harness.lean`, `HarnessMain.lean`).
- Generator and comparators in `t3r/scripts/` (`gen_cases.py`, `compare.py`, `compare_ruled.py`).
- `t3r/check.sh` (Go against the model of today).
- Scratch Go with all ten changes at `t3r/go/TDFLite-all`.
- `t3r/vectors/cases.jsonl`: the 75 vectors expand to 116 harness cases: 42 `engine`, 62 `kas`, 12 `wrap`.

**What to add.** A `tdfcore-diff` binary in a separate unverified harness crate (JSON dependency allowed there). It reads the same JSONL and writes the same record fields.

| Comparison | Expectation |
|---|---|
| Rust vs Lean `ruled` | 0 differences on the 104 `engine` and `kas` cases and on the 17,612-case generated set; non-ASCII reported separately (O4) |
| Rust vs scratch Go with changes | 0 differences |
| Rust vs Go today | Differs on exactly the cases where Lean `ruled` differs from Lean `today`, case by case; any other pattern is a finding |
| Rust binary vs its own Aeneas-generated Lean | 0 differences; tests the translator link, as `census/fork/FORK.md` "Soundness sample" did |

**Limits.**
- The 12 `wrap` cases and the descope guard exercise the shell and do not apply to `tdf-core`.
- The existing ID-level trace (`Harness.lean:52-74`) is today's semantics and is comparable only where no ruling bites, so compare at string level.

## (f) Hand-over for shadow mode (owner's repository, out of scope)

One versioned bundle:
- the crate source with its content hash;
- a thin unverified ABI crate and a `wasm32` build (pending O13), with the flat byte layout of inputs and verdicts documented;
- the Lean proofs with the axiom audit;
- the `.feature` file and pack with verdicts;
- the three-way report;
- the vectors in `abac_decide` corpus format;
- a "rests on" page: crypto, token parsing, the shell, the client-declaration assumption, rustc visibility;
- a short Go sketch of a second `Decider` that logs disagreements, as text, not applied.

Also flag that until the ten proposed Go changes land (`t3r/CHANGES.md`), shadow mode will log the 40-vector class as disagreements by design.

## Plan node T9

| Node | Input | Output | Test | Blocker |
|---|---|---|---|---|
| T9.0 Decisions | Table (a) | Defaults logged in `DECISIONS.md`; a rulings parameter file | Each default maps to named vectors | None |
| T9.1 ID-level spec | `Ruled/Spec.lean` | `IdSpec.lean`: `entitled`, `required`, `release` over naturals; statement of the bridge to `Spec.release` | Builds; evaluates equal to `t3rdiff ruled` on the 104 cases | Lean version (finding 5) |
| T9.2 Core crate | T9.1, profile | `tdf-core` core modules, unit tests | Translates with zero axioms under patched Aeneas; 104 cases through a test adapter | R1 for the pipeline; a direct Charon and Aeneas run does not need it |
| T9.3 Core proofs | T9.2 | Loop lemmas; `decide = IdSpec.release`; totality | Exact statement types, standard axioms, kernel replay (as p2's audit); mutation run with "lost proof is not detection" | None beyond T9.2 |
| T9.4 Intake | O1, O3, O4, O5 | Intake and `compile` in Rust; C1–C7 proved; `decide ∘ intake = Spec.release` | Same audit; differential run from day one | O4; cost unmeasured |
| T9.5 Permit and release | O11, O12 | Type-state, `handle`, two-run theorem | Compile-fail test; theorem audited; reading confirmed by the owner | O11, O12 |
| T9.6 Three-way oracle | t3r harness, T9.2 | `tdfcore-diff`, comparison script, report | Table in (e); negative control (a mutated core must be reported) | None |
| T9.7 Clausal layer | C1, parametrised `run.sh` | `clausebook/abac`, `tdf.feature`, verdict per sentence, list of every change to `clausebook/core` | Sentences compile as written; guarantees 1–5 and 8 proved on extracted Rust; target of zero core changes, reported whatever it is | C1; finding 4; "or" in conditions for guarantee 1 |
| T9.8 Guarantee 7 | A load-path model | Load operation, anti-rollback rule, proofs | As T9.3 | Not modelled at all today (`SPEC.md` §6); last |
| T9.9 Hand-over | All | Bundle in (f) | Clean-checkout rebuild from the bundle alone | O13 |

T9.1 to T9.3 and T9.6 need neither C1 nor the owner. That is earlier than `docs/PLAN.md` implies by making all of T9 depend on R1, C1 and the owner.

## Not checked

- No Lean, Rust or Go was built or run; every count is quoted from the cited files.
- Whether any candidate sentence compiles.
- Whether `Spec.lean` builds on Lean v4.35.0.
- Whether the patched Aeneas handles `u64` mask operations in loops without axioms; the profile says bit operations are modelled.
- ADR-0012, ADR-0016 and ADR-0028 themselves, `rewrap.go`, `compile.go`, `private/tdflite-pilot/MODEL.md`, `REPORT.md`, most of `t3r/CHANGES.md` and all but the head of `census/fork/FORK.md`.
- The status of plan node T6a (the Aeneas-versus-hax spike).
- The JS twin and go-tak-server engines.
- Performance of the linear and quadratic choices.

## First three pieces of work for tonight (no owner needed)

1. **T9.1, the ID-level spec and bridge statement** in a scratch copy of `t3r/lean`. About 3 agent-hours, plus 1 for an independent review. It also answers the Lean version question.
2. **T9.2, the core crate through Charon and patched Aeneas** in `private/tdf-core/` (per the O10 default), with the 104 cases as tests. About 4 agent-hours plus 1 review. Exit: zero axioms in the extracted Lean.
3. **T9.6, the `tdfcore-diff` harness and three-way comparison script,** built against a stub and then pointed at item 2. About 3 agent-hours plus 1 review. Exit: the negative control is caught.

T9.3 (core proofs) follows item 2. Going by p2 it is one to two sessions of 2 to 3 agent-hours each, with the mask reasoning as the unmeasured part.