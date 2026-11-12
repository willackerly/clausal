# Should the Clausebook be built out to cover DeepMind's Signal verification?

**Short answer: no, not as a coverage target.** The report's headline security theorems are outside the Clausebook's model, by construction. One layer underneath them, the per-run contract between the binary and its model, is the same shape as frames the Clausebook already has. That layer is worth one small probe.

Source read: the PDF itself (57 pages, dated 2026-11-10), downloaded and converted to text at `/private/tmp/claude-501/-Users-will-dev-lean-rosette/5dc3e5ea-13c5-4c6a-8f82-442d3e8f83b7/scratchpad/signal/pdf/signal.txt`. Its title is "AlphaProof Code: Verifying Signal's Security at the Machine-Code Level". Section and appendix numbers below refer to it.

## 1. What was verified

### Code
- **Target:** `libsignal-protocol` v0.105.4 with `spqr` v1.6.0, one-to-one sessions only: PQXDH session setup and Triple Ratchet messaging (§3, §4).
- **Form:** the unmodified Rust crates are wrapped in a small command-line harness, `libsignal-cli`. It is compiled by stock `rustc` 1.98.1 and statically linked with musl into one AArch64 Linux executable (§4, C.6).
- **Level:** the theorems are about whole runs of that executable, not about Rust functions. "Rather than reasoning about its Rust functions and in-memory state … we state our theorems about whole runs of its compiled AArch64 executable" (§4).
- **Size:** about 560 KB of verified code, about 140,000 AArch64 instructions (§7).
- **Operations:** `init`, `send` and `recv` are covered; `keygen` is not verified (§4).
- **No Rust-to-Lean extraction is used.** §8 names Aeneas, hax and Verus as source-level tools that "trust rustc, LLVM and a model of Rust's semantics, so we verify the compiler's output directly".

### Prover and scale
- **Prover:** Lean 4, with a 7,532-line semantics of user-mode AArch64 Linux covering 467 instructions and 31 system calls (§2.2). The symbolic side uses DyLean; the computational side uses VCVio.
- **Proof size:** about 6.5 million lines, all written by agents. Of these, 5.3 million are about the binary, 860,000 computational and 350,000 symbolic (§7).
- **Effort:** five people over four weeks; campaigns of 40 to 80 agents running 24 to 72 hours each (§2.3, §7).

### Properties and statement shapes

**(a) Binary-level functional refinement (§4.1, Lemma 4 in C.3).** For every operation, well-formed state σ, input x below 2^32 bytes and coins r:

> either run(op, enc(σ), x, r) = obs(step(σ, x; r)), an equality of outcomes including the error cases, or the run exhausts the machine's memory

In prose (§4.1): "If the model accepts the operation, the run exits with code 0, prints the model's output, and leaves exactly the model's new state in the party's files. If the model rejects it, the run exits with code 1, prints nothing, and leaves every file unchanged. If the model panics, the run ends with SIGABRT." A separate theorem shows no run within the limits exhausts memory.

**(b) Symbolic security (Theorem 1, §5.1.5).**

> ∃S. ∀τ ∈ Traces(r) with fresh coins: (Expl(τ) ≠ ∅ ∧ Safe(τ)) ∨ ∃τ1, e, τ2. τ = τ1 e τ2 ∧ Collision(τ1, e) ∧ Safe(τ1)

`Safe` is the conjunction of ten trace queries (Table 5). Each has the shape "if the attacker knows key k, then one of these compromise events is on the trace". Forward secrecy, for example: `m used, K(m) ∨ K(cipherKey(s,m))` implies `C(m) ∨ ∃ck⇝m. C(ck) ∨ ∃rk⇝ck⇝m. C(rk)`. The ten are: forward secrecy, post-compromise security, initiator and responder secrecy, authentication, peer authentication, KCI resistance, handshake forward secrecy, harvest-now-decrypt-later resistance and session independence.

**(c) Computational security (Theorem 2, §5.2.3).**

> There are cost-bounded reductions such that, for every adversary A that respects these budgets … Adv_bin(A) ≤ 2ε_KI + Σ_k Sess_k + 2·N_send·N_spk·δ_kem + 2ε_mlkem(A)

**(d) Specification tests.** These are non-vacuity theorems (hypotheses jointly satisfiable, honest sessions reachable) and Lean proofs that the symbolic theorem is false of two binaries with historical bugs re-injected (§2.1, §6).

### Trust assumptions (§5.3, Table 1)
- About 18,000 lines of trusted statements and definitions, plus about 8,000 lines of AArch64 and Linux process semantics.
- 39 hooked routines replaced by contracts: the low-level cryptography, five libc routines, the two output functions and a few Rust library routines.
- Algebraic laws assumed of the primitives, "trusted; we prove only that they are jointly satisfiable" (B.3).
- A fixed environment: fixed clock, no ASLR, 1 GiB of memory, software-only code paths (C.5).
- Not trusted: `rustc`, the Rust source and the proofs.

### What the report says was hard or left out
- **Specifications were the hard part:** "The majority of our effort went not into proofs but into specifications" (§7). The deviation catalogues have over 200 entries (computational) and about 35 (symbolic).
- **The source papers had errors:** fifteen gaps in the Double Ratchet analysis, and a ProVerif query that made receiver-side forward secrecy "false as printed" (§7).
- **Agents weaken goals:** this is why there is a held-out specification copy and a comparator (§2.4, §7).
- **Legibility:** "Left to themselves, agents produced specifications that were hard to audit" (§7).
- **Left out:** group messaging, multi-device, `keygen`, one-time Kyber prekeys, trust-on-first-use (symbolic), quantum adversaries (computational), SPQR's post-quantum healing, side channels and replay-based loss of forward secrecy (§5.1.6, §5.2.5).
- **Scale limit:** the computational bound is vacuous for single sessions of about 25,000 messages (§5.2.5).
- **Refuting the computational theorem** on a buggy binary is not feasible (§6).

## 2. Classification against today's Clausebook

The model, from `slice/lean/Frames/Core.lean:39-48`: an `Op σ α ρ` is `run : σ → α → Option (ρ × σ)`, one deterministic call. Frames quantify `∀ s a` over all states in scope (`slice/lean/Frames/Frames.lean`). `docs/ARCHITECTURE.md` §15 states "Frames describe one pure call" and "No current target needs 'eventually' or 'until'".

| Property class | Verdict | Detail |
|---|---|---|
| Per-run agreement with a reference model (Lemma 4, clause 1) | **Expressible today**, as a shape | Frame 13 `agrees_with` (`slice/vocabulary.yaml:947`; `Frames.AgreesWith`, `Frames.lean:163-167`): "the answer and the state after the call are exactly what the reference gives". The reference would be a domain word of kind `reference`. |
| Rejected run changes nothing (§4.1) | **Expressible today** | Frame 8 `rejected_unchanged` (`slice/vocabulary.yaml:795`), with `given` for the rejecting condition. |
| No fault, no divergence | **Expressible today** at the level of the extracted model | Frame 1 `always_answers`, also built into every frame by `Op.HoldsAt` with `calls = every` (`Core.lean:70-75`). It says nothing about memory exhaustion or machine faults. |
| Size-limit checks (stdin over 2^20 bytes gives exit 2) | **Expressible today** | `if_then` or `exactly_when` with a domain condition and an answer class. |
| Acceptance only when a check passes (MAC, signature, torsion check) | **Expressible today** | `only_if` with domain words. The check is an opaque domain function, like the paper's hooks. |
| Replay is rejected (Figure 5, last line) | **New piece, already planned** | Needs the same input twice. `Op.andThen` exists (`Core.lean:110-114`) but its surface form is only "two Whens in one scenario" (`slice/vocabulary.yaml:672-677`). "A sequence of calls whose inputs are tied" is one of the pieces five trial rules needed (`trials/sentences/RESULTS.md:57`; plan node L2, `docs/PLAN.md:82`). |
| Round trip: what Alice sends, Bob receives | **New modifier** | `andThen` passes a fixed input pair, so the second call's input cannot depend on the first call's answer. Candidate below. |
| Non-vacuity: premises can be met, honest sessions reachable | **Partly present** | The pipeline already requires a kernel-checked satisfiability witness per rule (`docs/ARCHITECTURE.md:193`, `slice/DESIGN.md:446`). `slice/FINDINGS.md:104` records that those witnesses were degenerate (empty ledger). There is no frame for "some call is accepted". Candidate below. |
| The ten symbolic queries on the model (Table 5) | **New frame in form; poor fit in substance** | They hold on every *reachable* trace of 23 attacker-scheduled transitions (Table 3). Frames quantify over all states, not reachable ones. "An invariant over any sequence of any operations" was needed by 2 trial rules (`trials/sentences/RESULTS.md:58`). Candidate below, with the reason the fit is poor. |
| Theorem 1 at the binary (refinement up to collisions) | **Outside the model** | See below. |
| Theorem 2 (advantage bound) | **Outside the model** | See below. |
| No out-of-memory; "for every placement of the code in memory" | **Outside the model** | Resource and machine-level facts. The Aeneas model has no memory bound or addresses. |
| Compiler not trusted | **Outside the model** | Route A trusts `rustc`, Charon and Aeneas (`docs/ARCHITECTURE.md` §8). This is a property of the chain, not of the vocabulary. |

### Candidate new pieces

**Modifier `feeding` (operation → operation).**
- Canonical sentence: "sending a message, then receiving what was sent, returns the message".
- Lean sketch: `Op.andThenWith (first : Op σ α ρ) (link : ρ → α₂) (second : Op σ α₂ ρ₂) : Op σ α ρ₂`, where `run s a` runs `first`, then runs `second` on the resulting state with input `link r`.
- A two-party round trip also needs each operation lifted to a product state (Alice's and Bob's). `Op.beside` (`Core.lean:118-124`) does half of that.

**Frame `sometimes` (existential).**
- Canonical sentence: "some send for which the session is established is accepted".
- Lean sketch: `∃ s a, op.scope s a ∧ ∃ r s', op.run s a = some (r, s') ∧ cls r`.
- This is the paper's reachability witness as a rule the author writes, instead of a side check.

**Frame `reachable_always` (multi-step invariant).**
- Canonical sentence: "in every state reached from a fresh session by any accepted or rejected sends and receives, the message counter is at least the number of messages sent".
- Lean sketch: `∀ s, Reach op init s → I s`, with `Reach` the reflexive-transitive closure of `op.run` from `init`.
- This is the first frame about more than two calls, and a real extension of §15's "Time" position.

### Why the symbolic queries fit poorly even with `reachable_always`
- The state would be DyLean's global trace and the condition would be "attacker knows k implies an excuse event".
- "Attacker knows" is the least set closed under an equational theory. The meaning sits in several thousand lines of trusted model, not in the frame.
- A Clausal sentence over it would be a one-line cover on definitions no reader of the sentence has reviewed. `docs/ARCHITECTURE.md:111` (no catch-all hole) exists to prevent that.
- The operation is a protocol model, not a function extracted from code. The link to code is the refinement theorem, which is outside.

### What breaks for the outside classes
- **Theorem 1.** The statement is `∃S ∀τ (∃ g ms, explains …) ∨ Collision`. It quantifies over traces of many runs by several parties with attacker actions between runs (leak, break, invert). It has existential witnesses chosen before the trace and a disjunct that excuses byte collisions. There is no place in `Op` for an adversary, an observation-versus-secret split, or a term-to-bytes map.
- **Theorem 2.** `Op.run` is a deterministic function to `Option`. There is no distribution, no probability, no adversary as a quantified algorithm, no cost semantics, and no "there exist reductions". Coins could be made an input, but the claim is about a measure over coins, which no frame can state.

## 3. Would the Rust pass through Charon and Aeneas?

**Not run.** The paper did not use them. What follows is a prediction from `census/CENSUS.md`, `census/PROFILE.md` and a grep of four public source files at tag `v0.105.4`, saved under `/private/tmp/claude-501/-Users-will-dev-lean-rosette/5dc3e5ea-13c5-4c6a-8f82-442d3e8f83b7/scratchpad/signal/src/`.

**The three verified entry points: predicted not to translate without redesign.**
- `rust/protocol/src/storage/traits.rs` has 17 `async fn` in store traits under `#[async_trait(?Send)]`.
- `rust/protocol/src/session.rs` has 10 `dyn` store parameters (for example `session_store: &mut dyn SessionStore`), 3 `async fn` and 13 `.await`.
- `census/PROFILE.md` rule 10 is "No trait objects". The census's trait-object family failed in 202 functions (`census/CENSUS.md:207`).
- Async is not measured at all: the census corpus excluded "async/network/logging stacks" (`census/CENSUS.md:23`) and `PROFILE.md` does not mention async.
- `census/CENSUS.md:630` says trait-object rewrites "change a design, not a function".

**The session record: partial at best.**
- `rust/protocol/src/state/session.rs` (970 lines) has 14 iterator-chain calls and prost-generated protobuf types.
- Rule 6 says iterator chains translate "only as axioms", and `copied`, `cloned` and `try_fold` abort the crate (`census/PROFILE.md:14`).

**Key-derivation code: plausibly translates, with axioms.**
- `rust/protocol/src/ratchet.rs` (191 lines) has no async, no `dyn` and no iterator chains by my grep.
- Its HKDF and HMAC calls go to external crates, which Aeneas emits as axioms (`census/PROFILE.md:16`). That is the analogue of the paper's hooked primitives.

**Whole-crate risk.** `PROFILE.md:14` says to expect the first run on a real crate to produce nothing. As shipped, six of ten census crates gave no Lean (`census/CENSUS.md:10`).

**Nearest census data points.** `untrusted` got 11 of 26 functions through and `zeroize` 27 of 32 (`census/CENSUS.md:193,196`). Both are far smaller and simpler than `libsignal-protocol`.

## 4. Recommendation

Do not adopt "cover the Signal properties" as a Clausebook goal. The fit is poor where the report's contribution lies: (b) and (c) are adversarial, multi-party and probabilistic, and their trusted base is 18,000 lines of specialist definitions. The fit is good only for layer (a), which is ordinary functional agreement and rejection behaviour that frames 1, 8 and 13 already state.

Three things from the report are worth taking regardless of Signal:
- **Tied sequences.** `feeding` and L2's tied-input sequences describe any encode/decode or sign/verify pair. This overlaps the owner's "packs for structured inputs over the wire" idea, and I would expect it to matter for TDFLite. I did not read the private TDFLite files to confirm.
- **Witnesses as first-class rules.** A `sometimes` frame, given that `slice/FINDINGS.md:104` already found the automatic witnesses degenerate.
- **Process.** A held-out copy of the specification with a comparator check (§2.4), and an amendment route that never weakens (§2.3), are stronger forms of the rule in `AGENTS.md` that agents may not edit statements.

### Roadmap node S1: Signal-shaped probe (one day, two independent halves)

**S1a, translation row.**
- Run `libsignal-protocol` v0.105.4 through the existing census scripts (`census/rerun.sh`) as an eleventh row, in a scratch copy.
- Output: functions stopped at Charon, at Aeneas, at Lean, and through; and specifically whether `message_encrypt`, `message_decrypt`, `process_prekey_bundle` and the functions in `ratchet.rs` get through.

**S1b, statement shapes.**
- Freeze a list of 14 shapes from the PDF before writing anything: the three accept/reject/panic clauses of §4.1, rejected-writes-nothing, replay-rejected, the two CLI size checks, send-then-receive round trip, out-of-order receive, MAC-failure rejection, and four of the Table 5 queries.
- Write each in Clausal against a toy symmetric chain ratchet of about 150 lines of in-profile Rust, with the MAC and KDF as opaque functions.
- Tally: compiles with today's pieces; compiles with `feeding`, `sometimes` or L2's tied sequence; refused.

**Outcome that counts as "no, not worth it" (any one):**
- S1a: none of the three entry points translate, and fewer than 10% of the crate's functions compile with no axiom beneath them. `libsignal` is then not a Route A target, and only a Route B model would reach it.
- S1b: fewer than 8 of the 10 non-query shapes compile with at most two new core pieces.
- S1b: any new piece is used only by the ratchet fixture and by nothing in the R2 crate or `tdf-core`. Under the "split on the second use" rule (`docs/ARCHITECTURE.md:128`) it does not enter `clausebook/core`.

The four Table 5 queries are expected to be refused. That is recorded as the boundary, not as a failure.

**If the outcome is "no":** keep the three takeaways above, add a paragraph to `docs/ARCHITECTURE.md` §15 stating that adversarial and probabilistic security is out of scope with this report as the reference, and stop.

## What I did not check

- I did not run Charon, Aeneas or any build. §3 is a prediction.
- I read four `libsignal` source files at the tag, by grep counts only. The file holding `message_encrypt` and `message_decrypt` was not fetched (my guessed path returned 404). I did not look at `spqr`.
- I did not open the paper's Lean repository, so statement shapes are from the PDF's prose and mathematics, not from Lean source.
- I did not read appendices A, C.1–C.2 and C.7–C.10 in full, nor the bibliography.
- I did not read `private/`, `tdflite-ideas/` or `docs/TDFLITE.md`, so the TDFLite overlap is an expectation, not a finding.
- I did not test whether the candidate pieces type-check or compose without ambiguity against existing forms.
- `clausal/` did not exist during my reads; all paths are under `slice/`.