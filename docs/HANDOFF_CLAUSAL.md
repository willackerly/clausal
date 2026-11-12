# Worktree Handoff (`feat/platform-readme` → `main`): Clausal, Clausebook & Phase 2 Strategy

Prepared 2026-11-11 on isolated worktree `.worktrees/platform` (branch `feat/platform-readme`, rebased cleanly onto `main` at `ad31f89`).

## 1. Executive Summary: Decisions Resolved with the Owner

In parallel with Phase 1 closeout on `main`, the owner worked in `.worktrees/platform` to settle project identity, scope, language design, README positioning, and core architecture diagrams (resolving `docs/HANDOFF.md` open decision #1 and shaping Phase 2):

1. **Language-First Identity (`Clausal` + `the Clausebook` + `clausal` / `cargo clausal`):**
   - **The Language — `Clausal`:** A strict, compositional formal-English dialect of Gherkin (`features/*.feature`, 100% valid Gherkin syntax) where every sentence carries one fail-closed formal (`Lean 4`) and executable (`Rust`) meaning.
   - **The Public Standard Library — `the Clausebook`:** An open, versioned, content-hashed public library of logical frames (`clausebook/core`), typed modifiers, domain packs (`clausebook/ledger`, `clausebook/abac`, `clausebook/quota`), dual Lean/Rust adapters, and `@[step]` Lean lemmas shared across repositories.
   - **The Toolchain — `the Clausal compiler` (`clausal` / `cargo clausal`):** `clausal compose` (interactive/suggest Clausebook sentence builder), `cargo clausal test` (Tiers 1–3: `cucumber-rs` + `proptest` + bounded `Kani` on any Rust crate without needing Lean open), and `clausal prove` (Tier 4: unbounded Lean 4 kernel proof + spec-gaming audit).
   - **Namespace Audit Completed:** `clausal` and `cargo-clausal` are free on crates.io; `clausebook` is free across crates.io, PyPI, npm, Lean Reservoir, and `github.com/clausebook` (`clausal.dev`, `clausebook.dev`, `clausebook.org` unregistered). Note small disambiguation neighbors: PyPI `clausal` (`neurosymbolica/clausal-prolog`), `clausal.ai` (healthcare claims), and `clausebook.com` (legal Word add-in)—keep framed consistently as *"Clausal — formal-English Gherkin built from the Clausebook."*
2. **Retiring "Readback" as a Separate Drifting Artifact:**
   - Rather than accepting loose Gherkin and emitting a separate post-hoc "readback / echo" string in `report.md` that drifts from `.feature` files, **canonical Clausal lives directly inside `features/*.feature`**.
   - `clausal compose` moves disambiguation to authoring time (proposing canonical Clausebook sentences, showing separating witnesses when ambiguous, and writing explicit fail-closed Clausal—e.g., *"accepted or rejected"*—directly into `features/*.feature`), so steady-state BDD and Lean 4 execute and prove the exact same sentence.
3. **High-Conviction README (`GOAL` vs. `SCOPE`, Check-Cashing Architecture, Honest Inventory at Bottom):**
   - `README.md` opens with the thesis, explicitly separates `GOAL` from formal `SCOPE`, shows multi-domain reuse across financial ledgers and ABAC (`TDFLite`), cashes the check with 4 architectural pillars + 5 deterministic Vector180 `0.1` diagrams, and inventories exact reproducible Phase 1 closeout state at the bottom.
4. **Upgraded Vector180 `0.1` Diagrams (`docs/diagrams/`):**
   - Regenerated deterministically via `docs/diagrams/gen_diagrams.py` (all pass `vector180 validate`, `resolve`, `text-fit` with `0 near-limit, 0 overflow`, and `compile`):
     - `how-it-works.vector180.svg`: Polished hero adding `Clausal compiler` and vertical `cargo clausal test` execution path.
     - `chain.vector180.svg`: **Symmetric H-Bridge Meet-in-the-Middle** 5-link loop (`Domain Intent` from far left, `Engineer / AI Agent -> Rust Source Code` from far right, straight vertical risers to `Lean 4 Kernel + Spec Audit` above and drops to `Binary BDD & Replay` below, converging into `CLAUSAL VERDICT` at `X = 800`). *(An alternative Two-Arena Spine layout without the center verdict box is preserved at `brainstorm/diagrams/chain-spine.vector180.svg`.)*
     - `vocabulary.vector180.svg`: **The Clausebook** public library & per-project dual bindings.
     - `compiler.vector180.svg`: **New — Inside the Clausal compiler** (tokenized `.feature` sentence → Clausebook + slot/sort checker + `UNBOUND` refusal gate → dual Lean 4 & Rust targets + conformance grid check).
     - `evidence.vector180.svg`: **Upgraded 4-tier evidence pipeline** explicitly drawing `Clausal (.feature) -> Clausal compiler` splitting into the Rust Executable Backend (Tiers 1–3) and Lean 4 Backend (Tier 4).

> [!IMPORTANT]
> **Privacy & TDFLite Check Before Pushing Publicly:** In `.worktrees/platform`, the owner explicitly asked to include **TDFLite** by name in `README.md` as an early-adopter worked example (de-emphasized alongside financial ledgers, showing `clausebook/abac` reuse). `README.md` uses **only** public OpenTDF/ABAC concepts (`allOf`, `anyOf`, hierarchy, FQN intake, `Permit`/`Dek`) and the already-public Phase 1 counts (`~400,000` cases, `6` known edge cases, `15` divergences)—zero content from `private/`, `tdflite-ideas/`, or `docs/TDFLITE.md` was read or copied. Confirm with the owner whether naming TDFLite in public `README.md` is cleared for `origin/main` alongside `docs/HANDOFF.md` item #6.

---

## 2. Recommended Adjustments to the Phase 2 Execution Strategy (`docs/PLAN.md` & `TODO.md`)

Phase 1's headline empirical finding (`0 of 48` cold-authored sentences compiled as written; `27` after rewriting; `18` needed a missing piece) and the new `Clausal` + `Clausebook` architecture reinforce each other directly—with **six concrete adjustments** to Phase 2's execution plan:

### Adjustment 1: Reframe Track L ("Close the Phrasing Gap") Around `clausal compose` + `L2`, Not Loose Parser Sprawl (`L1`)
- **Risk in current `L1`:** Widening the static `.feature` parser to accept dozens of free-form synonyms, gerunds, and word-order permutations makes `.feature` specs inconsistent across projects, increases cross-piece ambiguity (`L3`), and *still* fails roughly half the time for authors who haven't seen the vocabulary (`L4`'s 50% target).
- **Recommended shift:**
  1. **Keep `.feature` Clausal canonical, explicit, and strict** (one canonical surface phrasing per Clausebook composition, with fail-closed defaults explicit in the sentence itself).
  2. **Execute `L2` (missing Clausebook pieces) immediately**—the 3 multi-rule pieces surfaced by the 48-sentence trial (pre-call two-value comparisons, universal `"every balance"` quantification inside quantity claims, and tied call sequences) are high-value **Clausebook** primitives.
  3. **Pull `V7` (`clausal compose` interactive/suggest builder) + `L3` (separating-witness disambiguation) into Phase 2 Wave 1** in place of loose parser synonyms: `clausal compose` accepts rough English / synonyms (optionally ranked by an untrusted local/API model strictly constrained to valid Clausebook ASTs), shows concrete separating inputs whenever two readings diverge, and writes **canonical Clausal** into `features/*.feature`.
  4. **Measure `L4` two ways on the frozen 48 sentences:** (a) strict canonical compilation after `L2` piece additions, and (b) guided `clausal compose` resolution accuracy against each author's 5 recorded test cases.

### Adjustment 2: Partition the 96 Flat Entries into `clausebook/core` vs. Domain Packs Before `H1` Sign-Off
- Currently `slice/` has 96 unsigned entries in a flat namespace (`25` frames + modifiers + `40` fixture domain words).
- Before asking the owner to run `H1` (`python3 -m slicegen review`), split the catalogue into:
  1. **`clausebook/core`** (~56 shared frames and modifiers — universal across all projects),
  2. **`clausebook/ledger`** (reusable accounting/conservation pieces), and
  3. **Local crate bindings** (`wallet` / `ledger` fixture nouns).
- Having the owner sign **`clausebook/core` first** cuts `H1` review fatigue immediately and unlocks `H3` (strict mode + staleness propagation) without blocking on toy fixture nouns.

### Adjustment 3: Refocus `H2` (Human Meaning Trial) on Canonical Clausal + Separating Witnesses
- Proxy echo trials caught ~92% of mutated echoes (an 8% slip rate when comparing two separate English sentences).
- Since Clausal eliminates the separate echo artifact by making canonical Clausal *be* the `.feature` sentence, structure `H2` so human participants test:
  1. Direct comprehension of **canonical Clausal** sentences against concrete scenario cases, and
  2. Whether **separating-witness disambiguation** during `clausal compose` catches subtle scope traps (`accepted only` vs. `accepted or rejected`, `>` vs. `>=`) at higher than 92% accuracy.

### Adjustment 4: Pair `R1` → `R2` (External Open-Source Crate) with TDFLite Stage 2 (`tdf-core`) to Prove Multi-Pack Clausebook Reuse
- Wire the 5-patch Aeneas fork (`census/fork/`) into the pipeline first (`R1`), keeping upstream PRs (`A2`) strictly non-blocking in the background.
- Then run **`R2` (external open-source crate from the census)** and **TDFLite Stage 2 (`tdf-core`, profiled Rust + patched Aeneas, contributing `clausebook/abac`)** against the **exact same `clausebook/core` package**. Proving zero-modification reuse of `clausebook/core` across ledgers, an external open-source crate, and cryptographic ABAC is the strongest empirical validation of the Clausebook thesis.

### Adjustment 5: Elevate Route B ("Differential Oracle Against Proved Lean Model") to a Named Evidence Tier in `SCHEMA.md` (`X4`)
- When updating `docs/SCHEMA.md` in `X4`, make Route B (polyglot production binary differentially tested + witness-replayed against a kernel-proved Lean reference model, as done on Go TDFLite) an explicit first-class evidence class alongside Route A (Aeneas MIR extraction), rather than treating non-Rust targets as second-class stopgaps.

### Adjustment 6: Defer the Mechanical Repo/CLI Rename to One Atomic Commit & Spin Out the 150 GB Math Corpus
- **Mechanical rename (`lean-rosette` → `clausal`, `slicegen` → `clausal`):** Update docs/positioning now (done on this branch), and perform the mechanical directory/package rename in **one atomic commit when no background agents have dirty worktrees**.
- **Math strand (`HANDOFF.md` #7 & `X4` disk pruning):** Move the ~150+ GB Navier–Stokes / Mathlib corpus experiments (`corpora/`, `out/corpus/`, `M10`–`M11`) to a dedicated companion repository while keeping the general dead-code/allowlist Lean utilities (`tools/deadcode/` closure checks) that support Clausal's proof auditor.

---

## 3. How to Fold `feat/platform-readme` into `main`

`feat/platform-readme` sits cleanly 1 commit ahead of `main` (`ad31f89`) and touches **zero** code in `slice/`, `Rosette/`, `trials/`, or `tools/`:

```sh
# 1. Inspect the exact diff from main repo root:
git log --stat main..feat/platform-readme
git diff main..feat/platform-readme

# 2. Fast-forward main to fold everything in:
git merge --ff-only feat/platform-readme

# 3. (Optional) Remove the temporary worktree once merged:
git worktree remove .worktrees/platform
git branch -d feat/platform-readme
```

Follow-up doc syncs after merging (`X4`):
- Update `docs/ARCHITECTURE.md` prose to adopt the `Clausal` / `Clausebook` terminology (its diagram paths `diagrams/{chain,vocabulary,evidence}.vector180.svg` already point to the upgraded figures!).
- Update `TODO.md` and `docs/PLAN.md` if adopting Adjustments 1–6 above.
