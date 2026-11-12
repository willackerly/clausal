# Plan: hypotheses, tests and order of work

Status after the first wave added 2026-11-12 (see "Status after the wave").

Draft 7, 2026-11-12 (owner's steer and seven studies: tracks Q and T9, nodes K1, S1, X6; see "Refresh of 2026-11-12").

Draft 6, 2026-11-11 (Phase 2 adjusted after the identity decision: Clausal, the Clausebook, a composer in place of a wider grammar; see "What changed from the first Phase 2 draft").

Draft 5, 2026-11-11 (Phase 2 added; phase 1 closed).

Draft 4, 2026-11-10 (status and changes after the first night added below the Stance).

Draft 3, 2026-11-10 (owner's steer applied; see the end).

Draft 2, 2026-11-10. Draft 1 was reviewed by two critics on a different model (method and strategy) and checked against a prior-art survey (`out/prior_art_vocabulary.md`). Their main findings are folded in; "What changed from draft 1" at the end lists them.

Each node is a hypothesis with a test and a target, so a result can be read without arguing afterwards.

## Stance (owner, 2026-11-10)

- **The destination is fixed.** English descriptions and working code will have proofs between them. The question is never "is it worth it"; it is "how good can we make it, and what are the trades".
- **Report, don't gate.** The "Pass / fail" columns below are targets and signals. A miss changes what is built next and is reported plainly; it does not stop a track.
- **Do not overfit to the wallet.** The wallet and ledger are fixtures for building infrastructure, not sources of conclusions about real systems.
- **Rules come in suites.** A single rule is not expected to pin behaviour by itself; adequacy is judged for the suite.
- **A restricted Rust profile is acceptable**, and forking a tool to improve it is an option when a limitation is in the way.
- **People tests are deferred.** For now they run on naive subagent proxies, on infrastructure built so real people can take the same trial later without change.

## Phase 2 (agreed 2026-11-11; strategy adjusted the same day)

Phase 1 is closed; its nodes and results are in the sections below and in `docs/EXPERIMENTS.md`. Start from `docs/HANDOFF.md`.

The project is now named: **Clausal** is the language (strict Gherkin in `.feature` files), **the Clausebook** is the library of typed pieces, and the **Clausal compiler** (`clausal`, `cargo clausal`) is the toolchain. The code was renamed to match on 2026-11-11 (node X5): `clausal/clausebook.yaml` and `clausal/lean/Frames/` are the Clausebook, `clausal/clausal` is the compiler.

### What phase 1 changed about the problem

- **The pipeline works for an author who knows the vocabulary.** One rule yields a reading, tests, a bounded check, a proof slot and a trust statement.
- **The binding constraint is now phrasing.** None of 48 rules written without knowing the vocabulary compiled as written.
- **Nothing has yet been touched by a person:** no vocabulary entry is signed and no person has taken a trial.
- **Everything is on two toy crates,** and the patched translator is not in the pipeline.

### What changed from the first Phase 2 draft

The first draft of this section (earlier on 2026-11-11) closed the phrasing gap by widening what the static grammar accepts. The identity work done in parallel (`docs/HANDOFF_CLAUSAL.md`) changed that, and the owner adopted six adjustments:

1. **Track L is built around a composer, not a wider grammar.** Accepting many phrasings of one meaning in `.feature` files makes specifications differ between projects, adds ambiguity between pieces, and would still miss authors who have not seen the vocabulary. Instead each meaning has one canonical sentence, with its fail-closed defaults written out in the sentence, and `clausal compose` turns rough English into it. The old L1 (synonyms and sentence shapes in the parser) is withdrawn; L1 is now the composer. This also retires the separate echo: the canonical sentence is the one in the file.
2. **The Clausebook is split before it is signed** (new node C1): shared frames and modifiers, a ledger pack, and the fixtures' local nouns.
3. **H2 tests canonical sentences and separating inputs** in place of comparing a sentence with its echo.
4. **R2 is paired with TDFLite's `tdf-core`** (new node T9), both against the same unmodified core.
5. **Route B becomes a named evidence class** in `docs/SCHEMA.md` (part of X4).
6. **The rename is one later commit** (new node X5; made on 2026-11-11), and the mathematics corpus is recommended to move to its own repository (the owner's decision; X4).

### Refresh of 2026-11-12 (draft 7): owner's steer and seven studies

The owner asked for: the names adopted in the code (done, X5); TDFLite's decision core fully built as the top operational priority and the internal north-star example (the README keeps it de-emphasised); more readable Clausal, by aliases or any other means that does not weaken the formalism; and two roadmap candidates (DeepMind's Signal verification, and "Clausal packs"). The mathematics strand was left to us. Seven read-only studies were run, the readability one as three proposals, an adversarial critique and a synthesis. They are kept in `docs/studies/2026-11-12/`; nothing in them was built. What they change:

**Corrections to what this plan and the README said.**

- "One canonical sentence per meaning" is not true of the present book: five entries have several surface forms, four verb phrases for two meanings are hard-coded in `clausal/clausal/vocab.py`, and seven frames have two Rule voices. The hard-coded forms are under no signature.
- "Fail-closed defaults are written out in the sentence" is not true: no form accepts "accepted or rejected". Until Q-track settles it, the defaults are shown beside the sentence, computed from it.
- A narrowed rule that holds of every possible operation compiles unflagged, and the printed coverage text is wrong for two sentence shapes (both found by the readability critique, the first checked in the Lean kernel on a copy).
- The README's three TDFLite sentences are not Clausal: "more-never-loses" is a frame's name used as a verb, and the order-independence row names the wrong frame. They are to be rewritten in real forms and marked planned until `clausebook/abac` exists.
- The mathematics strand is about 70 GB on disk, not 150; `census/` (Clausal side) is 93 GB. The dead-code tool is not used by the Clausal audit.
- R1 is smaller than planned: the patched translator already produces byte-identical models for both fixtures.

**Track Q: readable Clausal** (`docs/studies/2026-11-12/readability.md`). The rule "the static grammar does not grow synonyms" is replaced by: **one live form per piece per position, every form in the signed book; wording is improved by replacement, never by addition.** Every alias proposed in the ordinary sense (fronted "If …,", parenthetical narrowing, a project's second noun, an "accepted or rejected" marker) was shown by the critique to invite a second reading, so none is admitted now; Q9 is the gate by which one can be admitted later on a measured result with people. The owner asked for aliases; this is the finding, reported, and the trial in Q7 is how it gets revisited.

| Node | What | Target | Needs |
|---|---|---|---|
| Q1 | Refuse a narrowed rule whose reading holds for every operation; the kernel theorems in the build | The four sentences in the critique refused; no fixture regression | — |
| Q2 | Printed coverage derived from each claim's `Calls` value, and under the digest | 0 mismatches between printed coverage and emitted Lean | — |
| Q3 | Every accepted form moved into the book; `clausal book check` (holes preserved, one form per position, no shared skeleton between pieces without a signed separating input, every feature recompiles to the same term) | Violations of today's book listed; zero after Q4 or each signed | with C1, before H1 |
| Q4 | First batch of rewordings (19 rows in the study: "accepted" for "successful", "is at most" for "is not more than", "no X is P" for "every X is not P", one Rule voice per frame, single forms for the multi-form entries, the more-never-loses family) | Generated Lean byte-identical except the one named rule; verdicts unchanged | Q1–Q3; review on a second model |
| Q5 | Duplicate-meaning report | Finds every pair the critique named | — |
| Q6 | Computed display: a "covers" line, a two-run outcome table, one allowed and one forbidden case. Derived from the statement, never compiler input, never pinned in the file | Agrees with the executable reading on the search grid | L3 |
| Q7 | Comprehension trial, three arms (today's forms, the new forms, new forms plus display), keys computed by the executable readings, decision rules by interval and frozen first, with a negative control the trial must detect | Helped / hurt / no measured difference / uninformative, per trap kind | Q4, Q6, people (H2) |
| Q8 | Four tempting forms that must be refused | 4 of 4 | Q1, Q3 |
| Q9 | Gate for any later second form | Admitted only on "helped" with people, logged | Q7 |
| Q10 | The README's TDFLite rows compile against a draft `clausebook/abac`, or are marked planned | 3 of 4 compile; the fourth has an L2 entry ("or" between conditions) | T9.7 |
| Q11 | Documents stop claiming forms the compiler does not accept | 0 such claims | — |

The first batch coincides with up to 13 of the 48 frozen sentences by the critique's count, so any rise in L4(a) after it is reported as contaminated; L5 is the clean test.

**Track T9: `tdf-core`, the north star** (`docs/studies/2026-11-12/tdf-core.md`). Findings: the integer core in the Go has no production caller, so the Rust core is a new arrangement of the ruled specification, not a port; there is no ruled ID-level model yet; and if the Rust does its own string-to-ID compile and proves the facts about it, guarantee 8 becomes unconditional, which the Go result is not. Fourteen open questions (O1–O14) each have a default, logged in `DECISIONS.md`, so nothing waits on the owner; each default is a parameter or a vector set and is re-run if ruled otherwise. The crate lives in a local, unpublished git repository at `private/tdf-core/`; `clausebook/abac` is tracked here.

| Node | Output | Test | Needs |
|---|---|---|---|
| T9.1 | ID-level specification and the statement of its bridge to the ruled `Spec.release` | Builds; agrees with the ruled model on the 104 cases | — |
| T9.2 | Core crate in the Rust profile | Translates with zero axioms under the patched translator; 104 cases pass | T9.1 |
| T9.3 | Loop lemmas, `decide = IdSpec.release`, totality | Exact statement types, standard axioms; mutation run | T9.2 |
| T9.4 | Intake and compile in Rust, facts C1–C7 proved, `decide ∘ intake = Spec.release` | Same audit; differential run | O4 default (ASCII-only folding, fail closed) |
| T9.5 | Permit type-state and the two-run statement for guarantee 6 | Compile-fail test; audited theorem; reading confirmed by the owner | O11, O12 defaults |
| T9.6 | Three-way comparison: Go, Lean model, Rust | A mutated core is reported | T9.2 for real runs |
| T9.7 | `clausebook/abac`, `tdf.feature`, a verdict per sentence, every change to `clausebook/core` listed | Guarantees 1–5 and 8 proved on extracted Rust | C1, the pipeline taking a third crate |
| T9.8 | Guarantee 7 (bundle loading, anti-rollback) | As T9.3 | a load-path model; last |
| T9.9 | Hand-over bundle for shadow mode in the owner's repository | Rebuilds from a clean checkout | O13 |

T9.1–T9.3 and T9.6 need neither C1 nor the owner and start now. T9 no longer waits on R1 or R2.

**K1: rule packs** (`docs/studies/2026-11-12/packs.md`). A Clausal pack is a parameterised suite of ordinary sentences with holes for a project's operation and nouns; instantiation writes plain canonical sentences into the `.feature` file, so a pack carries no meaning of its own (test: delete the pack, every verdict identical). It is distinct from a Clausebook domain pack, which supplies words. First pack: "validated input", frozen (template, slots, a seeded bug list) before any target is read, exercised on a toy parser, then on TDFLite label intake and the R2 crate. "Signed message intake" waits for K1's result; unforgeability is an assumption, not a frame. Counts against the idea: a seeded bug survives while the pack reads complete; fewer than half the sentences survive unedited on a second target. Needs C1, and L2 for two members.

**S1: Signal-shaped probe** (`docs/studies/2026-11-12/signal.md`). The answer to "build the Clausebook out to cover it" is no as a coverage target: the report's security theorems are adversarial, multi-party and probabilistic, about whole runs of a compiled binary, and outside a model of one pure call. One layer fits: the per-run agreement between binary and model (accepted, rejected and changes nothing, panics), which existing frames state. S1a: run `libsignal-protocol` through the census as an eleventh row. S1b: fourteen statement shapes frozen from the report, written against a toy ratchet. Counts as "not worth it": the entry points do not translate and under 10% of functions come through; or fewer than 8 of the 10 non-query shapes compile with at most two new pieces; or a new piece is used by nothing else. Three things are taken regardless: tied call sequences (already L2), a "sometimes" frame for witnesses, and a held-out copy of the specification compared after the run.

**X6: the mathematics strand moves to its own repository, later** (`docs/studies/2026-11-12/maths-split.md`). Decision: split, at the first quiet window with no agent working and before any public release, with history preserved. The couplings are few (one script pair, one example file, two schema strings, some document sections). So they do not forget each other: each README and `AGENTS.md` names the other; the evidence-graph schema stays here and the other repository pins a version of it; `docs/RESULTS.md` keeps the strand's rows with links; M10 and M11 move with it. The split frees no disk by itself.

**Order now.**

1. In parallel, each in its own git worktree (`tools/wt.sh`), heavy builds through `tools/sem.sh`: the book stream (Q1 and Q2, then C1 with Q3, then Q4, then L2), the composer stream (L3, then a first L1), the toolchain stream (R1, then E2, then the pipeline taking a third crate), the T9 stream (T9.1, T9.2, T9.3; T9.6 beside them), and S1a.
2. One integrator merges, then one quiet full run and the mutation harness.
3. Then: L1 complete with Q6, L4; T9.4–T9.7; K1; Q7 with H2's item bank; S1b; R2 and R3; L5.
4. H1 once Q4 has landed (so the owner signs the reworded forms once). X6 in a quiet window.

**Status after the wave of 2026-11-12** (reports in `docs/waves/2026-11-12/`, results in `docs/RESULTS.md`).

| Node | State |
|---|---|
| Q1, Q2, Q3, Q4, Q5, Q8 | Built and merged. Open from Q3/Q4: 21 book-check violations to settle (signed separating pairs, or an owner decision on words shared by two systems and on bare-hole forms) |
| C1, L2, L3, R1, E2, X5 | Done |
| X7 (new): the pipeline takes a declared list of projects | Done, with a third toy project |
| L1 | First version built; **negative result** on the 48 (5 right, 20 wrong, never declines). Version 2 is being designed: declining, accounting for every content word, a model as a constrained proposer, a clean re-measurement |
| L4 | (b) measured once, pre-merge; the command needs repair for the project list. (a) contaminated by Q4, to be reported as such |
| T9.1, T9.2, T9.3 | Done at the ID level |
| T9.6 | Harness built; real three-way run in progress |
| T9.4 | In progress: bridge proof (Lean) and Rust intake |
| S1a | Done: not a practical extraction target. S1b (statement shapes on a toy ratchet) remains optional |
| Q6, Q7, Q9, Q10, Q11, K1, H1–H3, R2, R3, L5, T9.5, T9.7–T9.9, X4, X6 | Not started |

Added to the roadmap from the owner's steer of 2026-11-12 (`DECISIONS.md`), design study in progress: **W-track, who is trusted for what.** Attestations with signer kinds (person, model, tool, organisation; a model's never counts as a person's); a per-project trust policy naming its roots; an assumption ledger in which each assumed fact carries usage conditions proved as ordinary rules; specialist terms admitted by reference to an external hashed definition; external proofs linked as evidence. Sequence-of-calls properties are a goal; adversarial and probabilistic security is not stated as Clausal sentences. First test: the signed-message pack with one real assumption.

### Dependency graph

```mermaid
graph TD
  L2[L2 add the missing Clausebook pieces] --> L4[L4 the 48 frozen sentences, measured two ways]
  L3[L3 separating inputs for ambiguous readings] --> L1[L1 clausal compose]
  L1 --> L4
  L4 --> L5[L5 fresh sentences from new authors]
  C1[C1 split the Clausebook: core, ledger pack, local bindings] --> H1[H1 owner signs clausebook/core]
  H1 --> H3[H3 strict mode on]
  L1 --> H2[H2 meaning trial taken by people]
  H2 --> L5
  R1[R1 wire the patched translator into the pipeline] --> R2[R2 a real crate end to end]
  L4 --> R2
  C1 --> R2
  R2 --> R3[R3 replay real commit history]
  R1 --> T9[T9 TDFLite tdf-core on the same core]
  C1 --> T9
  E2[E2 flag rules larger than every size tried]
  T8[T8 TDFLite follow-ups]
  M10[M10 detector for the repeated-structure pattern]
  M11[M11 deduplication linter]
  X4[X4 housekeeping: disk, schema, figures]
  X5[X5 the rename, one commit: done]
```

### Track L: close the phrasing gap

The frozen test set is the 48 sentences in `trials/sentences/`, with their authors' intended cases. It must not be edited.

Rule for this track, as revised on 2026-11-12 (track Q above): **one live form per piece per position, every form in the signed book; wording changes by replacement, not addition.** A new form enters only as the canonical sentence of a new piece (L2) or as a replacement checked by `clausal book check` (Q3). Meeting authors where they are remains the composer's job.

| Node | What | Target or output | Needs |
|---|---|---|---|
| L2 | Add the pieces five rules each needed: a comparison of two values known before the call; "every balance" inside a claim about a quantity; a sequence of calls with tied inputs. Then the eleven needed by one or two rules, judged case by case. Each is a Clausebook piece with one canonical sentence form | Each new piece has a Lean definition, a canonical English form, a second reading, and a toy case where it is false | — |
| L3 | Separating inputs. Given two candidate readings of one rough sentence (two pieces, two scopes, or one word naming operations in two systems), find a concrete input on which they differ, or report that none was found within stated bounds. The compiler itself keeps refusing ambiguous sentences | The silent wallet-versus-ledger choice from the trial is reported as ambiguous with an input; "accepted only" against "accepted or rejected", and `>` against `>=`, each get a separating input on the fixtures | — |
| L1 | `clausal compose`, suggest mode first (this is V7 from the earlier plan, brought forward). Input: rough English. Output: ranked canonical Clausal sentences, each a composition the Clausebook permits; where the top candidates differ in meaning, the separating input from L3 and a question; the chosen sentence written into the `.feature` file. A language model may rank or propose, constrained to valid compositions and trusted for nothing: the output is compiled by the ordinary compiler like any hand-written sentence | Every sentence it writes compiles as written. It never writes a sentence whose reading the author was not shown. A non-interactive mode exists so that L4 can score it | L3; first version can start on today's pieces |
| L4 | The same 48 sentences, measured two ways after each change. (a) Strict: do they compile as written against the canonical grammar with the L2 pieces. (b) Guided: feed each as rough input to `compose`, take its top candidate with no human choice, and evaluate that reading on the author's five recorded cases | Report both. For (a): compile as written, need a new piece, refused. For (b): top candidate right on all five cases, right in the top three, wrong reading, no candidate. Signal: half resolve correctly under (b). (a) is expected to stay low and is reported anyway. Any wrong reading is reported first | L1, L2 |
| L5 | Fresh sentences from authors who have seen neither the vocabulary nor the first 48: people if H2 has recruited any, otherwise a different model family and labelled proxy | Same two reports on unseen sentences, so L1–L3 are not fitted to the 48 | L4, H2 |

Freeze before measuring applies to L4(b): the composer's ranking rule, candidate limit and any model prompt are committed before the 48 are run, and the 48 are not used to tune it between runs without saying so.

### Track C and H: a Clausebook a person has signed

| Node | What | Target or output | Needs |
|---|---|---|---|
| C1 | Partition today's flat list of 96 entries into `clausebook/core` (the 25 frames and 28 modifiers), `clausebook/ledger` (accounting and conservation notions general enough to reuse), and local bindings for the wallet and ledger fixtures (from the 32 domain words, 8 operations and 3 idioms). The assignment of each domain entry to pack or local is written down with its reason before the split | Every existing verdict identical after the split; core contains no reference to a fixture noun, checked by building it alone | — |
| H1 | The owner reads and signs `clausebook/core` (53 entries), then the ledger pack; fixture nouns last or never | A record of time per entry, entries questioned, and entries changed as a result | C1, owner |
| H2 | The meaning trial, rebuilt. Part one: a person reads a canonical Clausal sentence and says, for concrete cases, whether the rule allows each. Part two: a person is shown a rough sentence, two candidate canonical sentences and a separating input, and picks; the traps are scope ones (accepted only against accepted or rejected, `>` against `>=`). A new item bank first, mutations drawn by a seeded rule, at least eight items per kind. Taken by the owner and at least two others who did not build it | Catch rate and false alarms for people, beside proxy figures on the same items, and beside the 92% proxy figure from the old two-sentence echo trial | L1 for part two, owner, recruits |
| H3 | Strict mode becomes the default once signatures exist; change one signed definition and confirm every dependent verdict goes stale | Staleness works with real signatures | H1 |

### Track R: leave the toys

| Node | What | Target or output | Needs |
|---|---|---|---|
| R1 | Build the patched translator from `census/fork/` and point the pipeline at it; drop the warnings-as-errors flag; confirm the fixtures are unchanged. Sending the patches upstream stays in the background and blocks nothing | Every existing verdict identical | — |
| R2 | One real crate that translates today (candidates from the census: a decimal-arithmetic or version-parsing crate), chosen by a stated rule before looking at its code. Domain vocabulary by one agent, rules by a different author, proofs by a third. It uses `clausebook/core` as split in C1 | Per rule: canonical sentence, evidence ladder, verdict. Report what share of the crate's public functions got at least one rule with each kind of evidence, Lean lines per Rust line, every place the Clausebook, the translator or the proof fell short, and **every change made to `clausebook/core`** | R1, L4, C1 |
| T9 | TDFLite stage 2: `tdf-core`, the decision logic in profiled Rust through the patched translator, with its domain words as `clausebook/abac`, against the same `clausebook/core` | The guarantees already proved on the Lean model of the Go, restated in Clausal and proved on the extracted Rust; every change made to core listed | R1, C1, owner |
| R3 | Replay the crate's later commits with the rules fixed; one agent repair attempt per broken proof | Share of commits that end green with no human proof work; breaks classified as real change or brittleness | R2 |

The reuse claim is tested by R2 and T9 together: the number of changes to `clausebook/core` needed to serve a ledger, an outside crate and access control. Zero is the target; whatever the number is, it is the result.

### Smaller nodes

| Node | What | Needs |
|---|---|---|
| E2 | Flag any rule whose subject can be larger than every size tried, and add the reviewer's probe rule as a standing fixture that must come out "tested only" | — |
| T8 | TDFLite follow-ups: correct the D4 wording in the ruled specification; state and prove "a subject with one higher level keeps access"; act on the owner's answers to the eight open decisions | Owner |
| M10 | A detector for the one pattern that paid in the families experiment: a structure, definition or module repeated with one inserted argument or guard, each copy with its own laws. Test first on the three cases the reviewer found | — |
| M11 | Deduplication as a linter: type aliases, verbatim copies, library notions under a local name; try removing the 389 type aliases in a scratch copy and rebuild | — |
| X4 | Prune disk; update `docs/SCHEMA.md` (rule groups, suite verdicts, the evidence ladder, and Route B as a named evidence class beside Route A); redraw the one remaining old figure (`docs/diagrams/pipeline.vector180.svg`); measure Cedar with all five patches; clean build timings. If the owner agrees, move the mathematics corpus experiments (`corpora/`, `out/corpus/`, M10, M11) to a companion repository, keeping the dead-code tool that the proof audit can use | — |
| X5 | The rename: `lean-rosette` to `clausal`, `slicegen` to `clausal`, in one commit, when no agent has a dirty working copy. **Done 2026-11-11 for the code** (`slice/` to `clausal/`, `slicegen` to the `clausal` package, `vocabulary.yaml` to `clausebook.yaml`); the repository and checkout names are left to the owner, and frozen records keep the old names | Owner's go-ahead; nothing else running |

### Order

1. L2, L3, C1 and R1 in parallel (different directories: pieces, search, catalogue layout, translator). C1 and L2 both touch the vocabulary file, so C1 goes first or they share one owner. A first `compose` (L1) on today's pieces alongside. E2 and X4 alongside.
2. L1 complete, then L4. H1 as soon as C1 lands and the owner is available. H2 once L1 can show separating inputs.
3. R2 and T9, then R3. L5.
4. M10, M11 and T8 as capacity allows. X5 (the code rename) is done.

### Models

- **Fable:** design, proofs, fixes.
- **Opus 5.5:** every review, and any role that must not share the builder's context (rule authors in R2, sentence authors in L5 unless a different model family is available).
- **A smaller model:** bulk runs.
- Two models from one vendor are not independent raters. Anything that needs a judgement about meaning needs a person.

## Status and changes after the first night (2026-11-10)

This section is the current state. The tables further down are the original node definitions.

### Where each node stands

| Node | State | Result in one line |
|---|---|---|
| K1 meaning trial | Done, proxy readers | 93% of wrong readings caught; harness ready for people |
| K2 trade map | Done, reviewed | Sampling and bounded checking find nearly every injected bug; proofs add the all-inputs result |
| K3 translation census | Done | 1% of real functions translate as shipped, 34% with aborts worked around; three small tool defects dominate |
| F1 suite note, `Rule:` | Done | In the slice report; 7 of 8 fixture operations fully constrained |
| T0, T1a, T1b TDFLite pilot | Done | Model matches the Go on 400k cases; all six known cases surfaced (search was guided); 15 more reproduced |
| T2 rulings | Done; owner has ruled | Rulings recorded privately |
| T3r ruled specification, T4 repeatable check | Done, reviewed | Guarantees 1–5 proved, 8 given named facts; 75 vectors; ten proposed changes, none applied |
| V1 prior art | Done | 14-frame catalogue |
| V2, V3 frame library | Done, reviewed, fixed | 25 frames; all old statements proved equivalent; rule lines compile and run on Rust |
| E1 layered evidence | Done, reviewed | Generated tests and bounded checks match hand-written ones |
| V4 naive sentences, V5 echo trial | Done, proxy | 0 of 48 compile as written; 92% of wrong echoes caught |
| P2 agent-written loop proofs | Done, independently scored | Both models 7 of 7 functions; cost unchanged at about 6 Lean lines per Rust line |
| Aeneas fork spike (new, A1) | Done | 1% to 35% of census functions (82% of nine crates); five upstream reports prepared, not sent |
| M2 definition-centred outline | Done, proxy readers | More followable, no more milestones; model readers split |
| M4 dead code | Done | A quarter of the machine corpus deleted, headline theorems still check |
| Paper ground truth (new) | Done | 117 paper items mapped to Lean |
| M8 dead-code tool | Done, reviewed | Three projects; safest class never wrong; shares depend on roots |
| M7 re-invention detector | Done, exploratory | Known case found unaided; recall unknown |
| M9 definition families | Done, exploratory | One family of seven paid; the valuable pattern is narrow |
| Constant threading (new) | Done | Small prize; the corpus re-invented big-O three times |

### What the results change

1. **Evidence comes in layers, and the tool should produce all of them from one compiled rule.** K2 showed property tests and bounded model checking are the best finders of counterexamples and proofs are the only unbounded evidence. Each frame already has an executable reading, so a rule can generate its own property test and bounded-checking harness as well as its Lean statement. New node **E1**.
2. **Tool robustness is on the critical path.** K3 showed the translator, not Rust idiom, limits coverage. New track **A**: carry patches in a fork, offer them upstream, add missing standard-library models.
3. **The TDFLite track moves from finding to specifying.** With rulings in hand: fix them in the model, prove the guarantees, and hand the owner test vectors and a proposed change list. New nodes **T3r** and **T7**.
4. **The stress target changes.** Cedar does not get through the translator today. Use one of the crates that mostly does (76% across the other nine) as S1 now, and return to Cedar after track A.
5. **Maths: build on what worked.** The dead-code report is cheap and real, so make it a tool for any Lean project (**M8**). The most interesting observation was a machine re-inventing a library abstraction; look for that directly (**M7**). Outline work continues only with a person to rate it.
6. **Model readers are instruments, not judges.** They are kept for mechanical checks and proxy trials, and not used as evidence of mathematical or semantic quality.

### New and changed nodes

| Node | What | Target or output | Needs |
|---|---|---|---|
| E1 | From one compiled rule, generate a property test and a bounded-checking harness alongside the Lean statement; feed any falsifying input back as an example row and a kernel-checked refutation | On the fixtures: every bug the K2 arms found is found by the generated harnesses, with no hand-written test code | V3 |
| A1 | Fork spike: patch the three translator defects, re-measure the census | Functions unlocked per patch; test suite unchanged | Running |
| A2 | Decide fork versus upstream; prepared reports are sent only by the owner | Decision | A1, owner |
| A3 | Models for the most-used unmodelled library items; drop the slice's warnings-as-errors flag | Share of functions that translate with no unmodelled dependency | A1 |
| T3r | The ruled specification: rulings fixed in the model, guarantees proved under them, test vectors for each ruling, and a proposed change list for the Go, all private and none applied | Guarantees 1–5 proved; 8 proved or its missing facts named; vectors run against today's Go and fail exactly where a ruling changes behaviour | T2 |
| T4 | Now: make the model-versus-Go differential check a repeatable command the owner can run at any commit | One command, minutes | T3r |
| T7 | Obligations in depth: proof of capability versus declaration, trigger scoping, parity | Roadmapped, not started | Owner |
| S1 | Stress target: start with a crate that translates today; Cedar after track A | As before | V3, A1 |
| V4–V6 | Unchanged, run with proxy authors and readers for now | As before | V3 |
| M7 | Find project definitions that are equivalent to an existing library notion (re-invented abstractions) | Candidates with a kernel-checked equivalence each | — |
| M8 | Dead-code report as a tool for any Lean project, with the elaboration-time dependencies it must not delete | Runs on a second and third project; deletions confirmed by build | — |
| M9 | Families: cluster subtly different definitions and their lemma families with a wide aperture; replace the best families with one parameterised primitive each (the owner's idea) | Concept count before and after, with proof size and elaboration cost beside it; each generalisation kernel-checked | M7 |
| X1 | Update `docs/SCHEMA.md` for rule groups, suite verdicts and layered evidence | Schema validates the slice graph | V3 |

### How the work is run

- **One owner per directory.** Agents write only in their own tree; anything that runs a pipeline does it in a scratch copy.
- **Build, review, fix.** Every substantial node is built by one agent, checked by a second on a different model, and the corrections are applied and rerun before results are written up. The fix step is now part of the node, not an afterthought.
- **Two heavy workflows at most at once**, about eight build-running agents. The first night ran more, pushed the machine to several times its capacity, and made every timing unreliable.
- **Timings are measured in a quiet window**, alone, after the heavy work finishes.
- **No broad process kills, no public posts, no changes to the owner's other repositories.**
- **Top-level findings are assembled by the orchestrator**; agents return them as text.

## Rules for every node

Each rule answers a mistake already made in this project (`docs/EXPERIMENTS.md`, `clausal/FINDINGS.md`).

1. **Frozen before data.** Thresholds, the item set (scenarios, sentences, mutants, samples) and the budget are committed before the measured run starts, and the report names that commit. Anything changed afterwards makes the node exploratory.
2. **Items are not chosen by the builder.** They come from a tool, a fixed rule, random sampling with a recorded seed, or a different author. The builder's ledger mutants were 21 of 22 caught; the reviewer's five were 1 of 5.
3. **Pass and fail are separated by a gap, and the interval is reported.** A cutoff placed at the target rate on 20 items passes a system that is exactly on target only about 60% of the time. Sample sizes below are sized so the pass and fail bands do not overlap; results in between are "unclear" and say so.
4. **People decide judgement calls.** A model reader is a proxy and is labelled as one. Two models are independent of each other's context, not of each other's blind spots.
5. **A lost proof is not a detection.** Only "a rule is shown false by a concrete input" counts. A proof that stops compiling means "not shown".
6. **Every rule suite gets an adequacy note** (node F1): what trivial implementations the suite as a whole would still allow, and what it leaves unconstrained. This is information for the author, not a mark against any one rule.
7. **Agents may not edit rules, vocabulary or axioms to make a proof go through** without the change being reported as such.

## Strategy in brief

- **Centre of gravity: the software chain.** English rule → Lean statement → proof about a model of the Rust → stated trust at each link.
- **Map the trades early.** Three questions shape how good the chain can be made, and none needs new tooling to start on: do readers catch wrong meanings, where does proof add over testing and at what cost, and which Rust translates today.
- **Forcing function: the TDFLite pilot, run blind.** It is the right first customer but an easy case (a small pure function, and AWS has done the same for Cedar). So it is paired with a harder second target.
- **Maths stays as a long-term bet with checkpoints**, in this repo.
- **Not yet:** compiler and hardware links, temporal frames, further graph-scoring ideas, free-form English with no signed vocabulary.

## Dependency graph

```mermaid
graph TD
  K1[K1 do people catch wrong meanings]
  K2[K2 does proof earn its cost]
  K3[K3 how much Rust translates]
  F1[F1 hollowness gate]
  P1[P1 loops cost, measured] --> P2[P2 agent-written proofs, two models]
  V1[V1 prior art, done] --> V2[V2 frame library]
  T0[T0 defect-layer census] --> T1a[T1a blind model of the decision]
  P1 --> T1a
  T1a --> T1b[T1b does it find the known defects]
  T1a --> V2
  P1 --> V2
  V2 --> V3[V3 recompile regression]
  V3 --> V4[V4 held-out sentences]
  V4 --> V6[V6 ambiguity questions]
  K1 --> V5[V5 echo-back trial with real echoes]
  V3 --> V5
  V5 --> V7[V7 suggest mode]
  V6 --> V7
  V7 --> V8[V8 interpret mode]
  V3 --> V9[V9 frame upgrade drill]
  T1a --> G1[G1 owner signs the glossary]
  T1a --> T2[T2 rulings table]
  T1a --> T4[T4 differential test against Go]
  T4 --> T3[T3 audit and mutation]
  F1 --> T3
  T1a --> T5[T5 two-run frame on the response path]
  V1 --> T6a[T6a toolchain spike]
  T1a --> T6a
  T6a --> T6[T6 Rust decision core]
  P2 --> T6
  K3 --> S1[S1 stress target: idiomatic Rust]
  V3 --> S1
  S1 --> S2[S2 replay real commit history]
  M1[M1 corpus and friction results] --> M2[M2 definition-centred outline]
  M2 --> M3[M3 does the outline help people do tasks]
  M1 --> M4[M4 what-not-to-read report]
  M4 --> M6[M6 does it serve software proofs]
  X2[X2 CI with negative controls]
  X1a[X1a rests-on block from the graph]
  X3[X3 clean-room re-check]
```

## Track K: map the trades (first)

These use only what exists today.

| Node | Hypothesis | Test | Pass / fail | Model |
|---|---|---|---|---|
| K1 | Readers catch a wrong meaning | Paper prototype, no frame code. (a) Seed 8 wrong definitions into the existing glossary (strict versus non-strict bound, dropped condition, rejected inputs excluded, wrong scope). (b) 30 rules with hand-written echoes; 10 wrong, 5 of those wrong only through composition. Seeds written by a different author from the reviewer. Run now with naive subagent readers of several models as a proxy; the trial harness records answers per reader so people can take the identical trial later | Target: ≥ 90% of wrong items caught, ≤ 10% false alarms. Reports state the measured catch rate beside the meaning link, labelled proxy until people have taken it | Subagent proxies now; people later |
| K2 | Where proof adds over testing, and at what cost | Discharge the same rules four ways on wallet and ledger: example rows; property-based tests (10,000 cases with shrinking); bounded model checking on the Rust (Kani); Lean proofs. Mutants from a tool (cargo-mutants) plus bugs transplanted from real fix commits; nobody who wrote a rule picks a mutant. Record cost per rule | Output: a trade map per kind of rule (what each method catches, what it costs), used to decide which evidence each rule gets by default. Not a go/no-go | Fable build; smaller model for runs |
| K3 | Which Rust translates, and what would widen it | Run current Charon/Aeneas and hax over 10 crates (5 business-logic, 5 sampled from popular crates). Per function: extracts or not, the generated Lean builds or not, which standard-library models it relies on | Output: a coverage figure, a written "supported Rust profile" that authors can code to, and a ranked list of tool improvements (candidates for a fork or upstream patch) by how much code each would unlock | Smaller model for runs; Fable to classify |

Current evidence bearing on K2: example rows alone catch 17 of 18 wallet mutants and nearly all ledger mutants; the proofs add one each.

## Cross-cutting

| Node | What | Pass | Model |
|---|---|---|---|
| F1 | **Suite adequacy note.** The rule suite for an operation is checked as a whole against trivial implementations (rejects everything, does nothing, always denies, identity) and tool-generated mutants; what the suite still allows is listed. Authors may record a few expected examples per rule before seeing the formal reading | Each report carries one adequacy note per operation. Informational | Fable |
| X1a | The "rests on" block of the target report is generated from the refinement graph | Report matches the graph on every run | Fable |
| X1b | The maths tooling writes the same graph format | Deferred until M2 needs it | — |
| X2 | CI runs `./run.sh` and the negative controls on every push | Controls fail when they should | Smaller model |
| X3 | **Clean-room re-check.** A fresh machine, given only a released evidence bundle, re-derives every verdict | Everything matches, one command, within 60 minutes | Smaller model |

F1 exists because a safety rule such as "internal transfers never change aggregate account value" is also true of a ledger that rejects every transfer. That is expected of a single rule; the note tells the author whether the suite includes the progress rule that rules it out.

## Track P: does proof cost stay manageable?

The cost track. Its results set how proofs get written (how much agent effort, which Rust profile, which tool improvements), not whether.

| Node | Hypothesis | Test | Pass / fail | Needs | Model |
|---|---|---|---|---|---|
| P1 | — | Measured, not a test. Ledger: 6.0 hand-written Lean lines per Rust line (wallet 1.6); two invariants; a 227-line lemma library; about 21 failed builds. Nothing about a loop was automatic | Recorded | — | — |
| P2 | An agent can write loop proofs unaided, at bounded cost | A new crate with at least 6 functions containing loops and no lemma library. Rules written by a different author. The agent must find the invariants and helper lemmas itself, within a fixed budget per rule (tokens and wall-clock). Two arms, Fable and Opus 5.5, same tasks | Per arm, counted per function, not per rule. Pass: ≥ 5 of 6 functions fully proved within budget. Fail: ≤ 2. Report Lean lines per Rust line and failed builds. The comparison between arms is descriptive | P1 | Both |

## Track V: does the vocabulary compose?

| Node | Hypothesis | Test | Pass / fail | Needs | Model |
|---|---|---|---|---|---|
| V1 | — | Done. Report in `out/prior_art_vocabulary.md`; summary below | — | — | — |
| V2 | A small typed frame library covers real rules | Build the shared library from the 14-frame catalogue below. Holes are typed, so one catch-all frame cannot pass. First check: a Scenario Outline under `Rule:` actually runs through cucumber-rs | Pass: every wallet, ledger **and TDFLite** guarantee is expressible with no one-off frame, and each frame has an independent executable reading that agrees with its Lean definition on generated inputs | V1, T1a, P1 | Fable; a person signs the frames |
| V3 | Composition loses nothing | Recompile every existing scenario through frames | Pass: each recompiled statement is proved equivalent to the old one by the kernel, not merely given the same verdict. Deliberate changes from fail-closed defaults are listed one by one | V2 | Fable |
| V4 | New sentences compile from existing pieces | 40 new rules, at least 20 written by people who know the domain but not the vocabulary. Each author records what they meant (five examples) before seeing the compiled reading | Pass: ≥ 75% compile with no new piece. Fail: < 50%. Any reading that contradicts its author's examples without being flagged is a fail regardless | V3 | People and a separate model author |
| V5 | Echo-back works with real, generated echoes | K1 repeated on the tool's own output | Same thresholds as K1 | K1, V3 | People |
| V6 | The tool notices ambiguity and asks the right question | Run on V4's naturally written rules, not seeded ones. Count ambiguities found, missed (judged by people) and false alarms | Pass: for each ambiguity found, an input that separates the readings, shown on compiled code | V4 | Fable |
| V7 | Suggest mode strengthens weak sentences | 30 loosely worded claims with the author's intent recorded first | Pass: a candidate matching the recorded intent in the top three for ≥ 80% | V5, V6 | Fable; people as authors |
| V8 | Interpret mode on a fixed document | A case study, labelled as one: one real document; every clause given a traced reading or listed as uninterpreted; a second person checks the uninterpreted list is complete | Descriptive | V7 | Fable; two people |
| V9 | A shared frame can change safely | In two projects on different Lean versions, change one frame without changing its meaning and one with | Pass: the first voids no signature (equivalence checked by the kernel); the second lists every affected rule with a separating input | V3 | Fable |

### What the prior-art check found (V1)

- **Frames with a fixed formal reading echoed back in English already exist**: NASA's FRET does this for timed requirements on signals. It has no typed domain vocabulary and no quantifiers, and it targets model checkers, not source code. Copy its echo format and its practice of giving each frame a second, executable reading.
- **First catalogue, 14 frames**: always answers; never changes; changes only; always / never; if-then; only if; exactly when; rejected and unchanged when; changes by exactly; at most / at least; counting over a named collection; monotone (more never loses); agrees with a reference; independent of (two runs). Five of these were missing from draft 1 and are needed by targets already in the plan.
- **Gherkin `Rule:`** may contain Scenario Outlines with Examples and tags, and all four main runners parse it. No runner gives the rule line any meaning, and no convention for a universally quantified rule was found, so that reading is this project's addition. Not yet executed here.
- **The whole chain was not found anywhere.** Pieces overlap with existing work: agent prove-and-audit loops for Aeneas-translated Rust (including a 16.7k-line cryptographic library), requirement-to-property tools that stop at property-based tests, and ambiguity scenarios over SMT in a cloud product.
- **hax's Lean backend is now built on Charon and Aeneas** (since late September 2026), adding contracts and its own library. Use plain Aeneas unless T6a shows otherwise.
- **The Cedar claim in the TDFLite plan is correct**: a Lean model, proofs about it, and differential random testing against the production Rust.

## Track T: TDFLite

Material about TDFLite's unresolved edge cases stays out of the public repository.

| Node | Hypothesis | Test | Pass / fail | Needs | Model |
|---|---|---|---|---|---|
| T0 | The proof must cover where the defects are | Classify every guarantee and D1–D6 by layer: integer core, string intake, rewrap shell, bundle acceptance. Four of the six sit in intake and one in the shell; only D4 is in the integer core that stage 2 would prove | Output: one "rests on" line per layer that is not proved | — | Fable |
| T1a | — | An agent that has not seen `tdflite-ideas/` or `docs/TDFLITE.md` writes the Lean model from the public Go source, including intake over strings. Guarantees given in plain English only. Adds a "model target" mode to the generator | Model builds; search settings frozen | T0, P1, owner's OK | Fable, blind |
| T1b | The chain finds defects it was not told about | Score T1a's output against D1–D6 | Pass: ≥ 4 of 6 surface as refutations or ambiguity questions, D4 among them. Fail: ≤ 2 | T1a | Opus 5.5 scores |
| G1 | — | The owner reads and signs the TDFLite glossary | Until signed, every verdict is recorded as "review", not "pass" | T1a | Owner |
| T2 | Rulings can be explored | The six rulings as parameters; each option one at a time from the suggested baseline (12 variants), plus the interactions among D1–D3 | Output: the decision table | T1a | Fable |
| T4 | The model matches production | Differential test against the Go engines, following Cedar's recipe: structure-aware generators, a second generator aimed at error paths, coverage-guided fuzzing. Each difference classified with the owner as Go defect, model defect or a seventh ruling | Pass: no unclassified difference; report the share of generated inputs that reach a Permit | T1a, owner's go-ahead | Fable |
| T3 | The guarantee set is not hollow | Tool-generated mutants of the model; F1 applied. "Noticed" means shown false. Survivors are accepted or rejected by the owner, not the builder | Pass: no survivor the owner rejects. Note: guarantees 1, 2, 4, 5, 6 and 7 all hold of a decision that always denies, so guarantee 3 must be stated as an equivalence | T4, F1 | Fable build; owner judges |
| T5 | Secrecy can be stated | A two-run frame over a model of the response path (unwrap, binding check, decide, respond). On the bare decision function the claim is true by typing and proves nothing | Pass: guarantee 6 stated on the response path, reading confirmed by the owner, proved | T1a, V2 | Fable |
| T6a | — | Toolchain spike: plain Aeneas against hax on two TDFLite-shaped functions, each proved against T1a's model | Output: the choice, with reasons | V1, T1a | Fable |
| T6 | The decision core can be proved in Rust | Per the TDFLite plan's gates plus the audit checks. Intake and release become their own nodes after it | — | T6a, P2 | Fable |

## Track S: an honest stress target

TDFLite alone cannot show the approach generalises.

| Node | Hypothesis | Test | Pass / fail | Needs | Model |
|---|---|---|---|---|---|
| S1 | The chain works on idiomatic Rust it was not designed around | A real open-source crate with an independent expert specification. First choice: Cedar's authoriser and evaluator, whose headline properties already exist as expert Lean statements. State them as English rules through the vocabulary | Pass: ≥ 4 properties expressed with no one-off frame and proved equivalent to the expert statement. Report the share of the code that translated and Lean lines per Rust line | K3, V3 | Fable; Opus 5.5 review |
| S2 | Proofs survive real change | Starting from proofs at one commit, replay about 50 later real commits. The policy for a red build is fixed beforehand. One agent repair attempt per broken proof | Pass: ≥ 90% of commits end green with no human proof work. Fail: > 20% need a person, or > 30% of breaks are brittleness with no change in behaviour | S1 | Fable; smaller model for the replay |

## Track M: mathematics (long-term bet, with checkpoints)

Five structure-scoring ideas have now failed: the hiding ratio, small goal state, reuse in Mathlib, dominators predicting blueprint nodes, and reuse in the machine corpus. What survives is tooling (sound lifting, corpus exporters), some cheap observations (a third of the Navier–Stokes theorems are unused by any headline result; hundreds of copy-and-modify families), and one lead: the interface a reader cannot skip is the definitions.

The claim that this track serves software verification is untested, and is not used to justify it until M6 tests it. The owner wants to keep investing here for the long term; the checkpoints are for deciding how, not whether.

| Node | Hypothesis | Test | Pass / fail | Needs | Model |
|---|---|---|---|---|---|
| M1 | — | Collect and review the corpus, reuse and friction results. Criteria for what would count as "packets help" are written before the numbers are read | Running | — | Fable |
| M2 | An outline built around definitions is readable where a lemma-based one was not | The same readers rate both outlines blind, with a written rubric, on at least 30 entries each | Pass: the definition-centred outline has a clearly higher share of "recognisable milestone" (intervals do not overlap) | M1 | Fable builds; at least two readers, one human if available |
| M3 | The outline helps people do tasks | 12 fixed questions about the Navier–Stokes development; outline against the standard documentation and search | Pass: ≥ 25% less time or ≥ 20 points more correct | M2 | People |
| M4 | "What you need not read" is a cheap, real win | Report unused declarations, cloned modules and copy-and-modify families; confirm by deleting a sample and rebuilding; include a negative control (delete something used) | Pass: sample confirmed; control fails as it should | M1 | Smaller model |
| M6 | The tooling serves software proofs | Run the outline and the report on a real software proof development (Cedar's Lean, the S1 proofs) | Pass: an engineer new to it answers fixed questions faster with it | M4, S1 | People |

Checkpoint: review M2, M3 and M6 with the owner in spring 2027 and decide the next shape of the track.

## Order

1. **Now:** K1 (paper prototype), K2, K3, F1, T0, X2. Ask the owner for the OK to read the Go source. Finish M1.
2. **Next:** T1a blind, then T1b and T2. P2. V2 against wallet, ledger and TDFLite. M4.
3. **Then:** T4 (as soon as access allows), T3, T5, G1. V3, V4, V9. X1a. M2.
4. **Then:** S1. V5, V6. T6a. X3.
5. **Later:** S2, T6, V7, V8, M3, M6.

## Where people are needed

- **Owner:** (OK to read the TDFLite Go source: given 2026-11-10); sign the glossaries (G1 and the slice's 44 entries); confirm readings (T5); judge survivors and differences (T3, T4); rulings (T2).
- **Other engineers and a mathematician (deferred):** K1, V4, V5, M2, M3 run on subagent proxies for now, labelled as such, with the trial infrastructure kept ready for people.

## Use existing tools where they exist

| Need | Borrow |
|---|---|
| Counterexample search | Property-based testing with shrinking on both the Lean and Rust sides; bounded model checking on the Rust. Keep the hand-built grid as a regression baseline |
| Mutants | A mutation tool, with hand-written mutants only as targeted probes |
| Frame catalogue and echo format | Published property patterns; FRET's slot-structured echo |
| Ambiguity questions | A solver query for an input on which two readings differ |
| Differential testing | Cedar's recipe |
| Signing and provenance | A standard attestation format over content digests |

## Open programme questions (no node yet)

- **Code that is not Rust.** TDFLite's production is Go. "Differentially tested against a Lean model" should be a named evidence level with its own pass bars, not a stopgap.
- **Effects, I/O and concurrency.** No frame and no link covers the shell around a pure core, and one TDFLite defect lives there.
- **How a loop is fully specified.** Either a small signed reference model in the vocabulary, or two-run rules. Until decided, each loop's exact behaviour lives in unsigned lemmas.
- **Who may sign what.** Separate roles for domain words and for the Lean behind them; more than one signer for shared frames.
- **Red builds.** Blocking or advisory, and who owns them. Must be fixed before S2.
- **Presenting evidence to an auditor**, and a disclosure policy for evidence about unresolved defects.
- **An inventory of the trusted base** (standard-library models, audit code, parsers, pins) with versions and digests in every report.
- **Budget and stop rule** per track.

## Model allocation

No measurements yet; P2 supplies the first.

- **Fable** for design, proofs and fix-and-report passes.
- **Opus 5.5** for sceptical review, scoring and as a second author. This gives a reader who has not seen the builder's context. It does not give statistical independence, so it never replaces a person on a judgement node.
- **A smaller model** for bulk mechanical runs.

## Deliberately not yet

- **Compiler and hardware links.** Stated as assumptions in every report.
- **Temporal frames.** No current target needs them.
- **More graph or size scoring for proof structure.**
- **Free-form English with no signed vocabulary.** K1 includes it only as a comparison arm.

## What changed in draft 3 (owner's steer)

- Added the Stance section: destination fixed, report don't gate, do not overfit to the wallet, rules come in suites, a restricted Rust profile and tool forks are acceptable, people tests deferred to proxies.
- Track K renamed from "falsify" to "map the trades"; K2 and K3 produce maps and a supported profile, not verdicts.
- The hollowness gate became a suite-level adequacy note.
- The kill clause on the cost track was removed.

## What changed from draft 1

1. Added Track K: three cheap tests that could falsify the thesis, run first.
2. Added the hollowness gate (F1) after a critic showed the flagship rule is true of a ledger that rejects everything.
3. TDFLite pilot made blind and moved ahead of the frame library; it now feeds the frame library instead of waiting for it. Added the defect-layer census, the glossary sign-off and a toolchain spike; the differential test moved earlier.
4. Added Track S: a harder real target and a replay of real commit history.
5. Proof-cost track rebuilt so it can fail: a new crate, no lemma library, rules by a different author, counted per function.
6. Sample sizes and cutoffs changed so pass and fail are distinguishable; authorship of test items specified; people decide judgement nodes.
7. Maths reframed as a dated bet with a task-based test, counting five failures, not three.
8. Frame catalogue grown from about 8 to 14 from the prior-art check.
9. Added clean-room re-check, CI with negative controls, and a list of programme questions with no node yet.
