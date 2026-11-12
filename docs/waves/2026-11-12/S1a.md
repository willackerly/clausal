# S1a: reports as returned by the agents

Builder, reviewer (Opus) and fix round, unedited apart from the session scratch path, written `<scratchpad>` (those files are not kept). Paths under `.worktrees/` are worktrees since removed; the commits are on `main`, or in the local `private/tdf-core` repository for T9.

## Builder

**S1a outcome: the frozen criterion for "not a Route A target" is NOT met.** None of the three entry points translate, but 24.3% of functions compile with no axiom beneath them, above the 10% threshold. That is not the same as "libsignal is a Route A target": the 24.3% is mostly three-line accessors, and by code lines the share is 9.1%.

On the relayed request about the repo rename to `clausal`: no objection, and it did not affect this step. Nothing was pushed and nothing used the remote URL.

## What I changed

All in the worktree `/Users/will/dev/lean-rosette/.worktrees/signal`, branch `wave/signal`, new directory `census/signal/` only:

- `frozen.json`: target commit, definitions, the three entry points, the ratchet file, the criterion.
- `run.sh`: the exact commands (`setup | tools | build | axioms | side | report | clean`).
- `signal_census.py`: imports `census/scripts/census.py` unchanged and points it at the workspace member with the patched Aeneas.
- `signal_report.py`: generates `RESULT.md`, `result.json`, `functions.tsv`.
- `axiom_check.py`: asks Lean itself which axioms each function depends on, and writes `axioms.json`.
- `README.md`: design notes and how to read the result.

Commits:
- `5ff3115` is the freeze, made before any tool ran on the crate.
- `419b689` is the result. `frozen.json` is unchanged between the two.

## Verification I ran

- **Charon and patched Aeneas** (`./run.sh tools`): `p5 shipped tools libsignal-protocol fns 589 charon_ok 472 aeneas_ok 268 ok 0 … rc [('charon', 0), ('aeneas', 1)] secs [16.1, 445.6]`
- **Lean build and join** (`./run.sh build`): `… ok 250 … lake {'rc': 1, 'secs': 22.5}`. Lean reported 888 errors, the last at line 79317 of 79400, so the whole file was elaborated.
- **Axiom cross-check** (`./run.sh axioms`): `{'counted': 523, 'through': 250, 'through_in_env_without_sorry_lean': 219, 'no_axiom_lean': 73, 'no_value_axiom_lean': 146, 'no_axiom_census': 127, 'census_only': 54, 'lean_only': 0 …}`
- **Side row** (`./run.sh side`): `pinned shipped build … as_is Aeneas aborted the whole crate (fatal exception): Unimplemented rc [('charon', 0), ('aeneas', 2)]`
- **One full `clausal/run.sh`** through `sem.sh 3`: `RESULT: every scenario got its expected verdict and every Rule statement its expected one`, exit 0. All 97 verdict codes in `out/graph.json` (39 scenarios, 46 rule groups, 12 functions) are identical to the baseline. I compared them with an inline script, not by calling `observe()`.
- **Bounded-check (Kani) differences under load**, with no verdict code changed:
  - Totals moved from 181 verified / 27 no answer to 172 verified / 36 no answer; 61 failed in both.
  - Rungs that changed between answered and no answer: `Rule.ledger.batch_total`, `Spec.ledger.batch_conserves`, `Spec.ledger.whole_conserves`, `Spec.ledger.batch_then_total_overflow`.
  - Different counterexample inputs only: `Rule.ledger_rules.mono_larger_amount`, `same_answer_any_amount`, `accepted_stays_accepted`, `Spec.ledger.batch_all_valid_all_applied`.
- I reverted the `clausal/out/*` files that run rewrote, so they are not in the commit.

## Not done or not verified

- No check that the translated Lean means what the Rust means; no Rust-against-Lean run was done.
- `spqr` v1.6.0 was not translated; it appears only as an opaque dependency.
- No `cw` row (Charon-side workarounds) was run, because Charon produced output as shipped.
- The row is not added to `pins.json` or the generated `CENSUS.md` tables. It was chosen by hand, not drawn by the seeded rule; it lives in `census/signal/RESULT.md`.
- `work/` is deleted, so a rerun re-fetches and re-translates (about 10 minutes plus the dependency download).

## What a reviewer should distrust

- **The function share over-reads the code.** The median no-axiom function is 3 lines. By code lines the frozen column is 9.1%, below 10%; the criterion counts functions.
- **The census "no axiom beneath" column over-counts.** It is a token scan and misses axioms reached through a structure field or trait instance. Lean's strict answer is 73 functions (14.0%), not 127. Much of the gap is opaque external types such as `libsignal_core::curve::PublicKey`.
- **The census "through" count over-counts.** Of 250, Lean has 219 in its environment free of `sorryAx`; the other 31 compile only over a silent `sorry`.
- **`aeneas-p5 -version` prints `81c0b10c-dirty`.** The binary was built before the fork's fifth commit, as `FORK.md` already notes.
- **The path mapping is mine.** I map Charon's and Aeneas's workspace-relative file names back to the crate root. If it were wrong, errors would go unattributed and counts would inflate. The join does show the expected messages on the expected functions, but 441 Aeneas log entries stayed unattributed; the ones I inspected were crate-level or in dependency sources.
- **The package version is 0.1.0.** `libsignal-protocol` is unpublished; the row is the workspace at tag v0.105.4, commit `b2a5c30f`.

## FOR DECISIONS.md

| What | Why | How to undo |
|:--|:--|:--|
| Read "translates" as: the function, including its async body, ends as compiling Lean; read "no axiom beneath" as the census field `ok_closure_no_axiom` over counted functions. Frozen in `5ff3115`. | The study's wording had to be made operational before the run. | Edit `frozen.json` and rerun `./run.sh report`; the alternative readings are already in `RESULT.md`. |
| Denominator is `rust/protocol/src` only. The 60 inventory functions in `test-support/` and `cross-version-testing/` are left out. | They are separate Cargo packages and not in Charon's output; `frozen.json` says "in rust/protocol/src". | Remove the `startswith('src/')` filter in `signal_report.py` and `axiom_check.py`; it changes only the "all source" figure. |
| Fetched from GitHub by tag (commit checked), not crates.io. | The crate is not published. | Not applicable. |
| Set `CARGO_HOME` to `census/signal/work/cargo-home`. | Keeps the dependency downloads deletable and out of `~/.cargo`. | Remove the line in `signal_census.py`. |
| Cloned (copy-on-write) `aeneas-p5`, `backends-pinned` and the Lake packages from the main checkout's `census/fork`, read-only. | The worktree has no fork build; rebuilding costs opam setup and disk. | `./run.sh clean`; set `MAIN_CENSUS` to point elsewhere. |
| Added an elaborator-based cross-check (`axiom_check.py`) with a strict and a middle reading, reported as sensitivity only. | AGENTS.md: data that can come from Lean must come from Lean; the census column is a token scan. | Delete `axiom_check.py` and `axioms.json`; the report omits the section when the file is absent. |
| Ran the unpatched release Aeneas as a side row on a copy of the same LLBC. | Isolates the effect of the patches. | Skip `./run.sh side`. |
| Reverted the `clausal/out/*` files rewritten by the full pipeline run. | Not part of this node; avoids merge conflicts. | Rerun `clausal/run.sh`. |
| Did not commit tool logs. | They contain absolute home paths and the task asked for small result tables only. | Rerun and copy `work/runs/*/work/run/libsignal-protocol/*.log`. |

No system-level installs. Nothing was written outside the worktree except `~/.cache/charon` and rustup's existing toolchains (cargo's registry went to `work/`); no `lake update`, no manifest or toolchain edit.

## FOR RESULTS

Reproduce everything with, in `census/signal/`: `./run.sh setup && ./run.sh tools && ./run.sh build && ./run.sh axioms && ./run.sh side && ./run.sh report`. All numbers are in `census/signal/RESULT.md` and `result.json`.

**Where functions stop** (patched translator p5, as shipped: one Charon run, one Aeneas run, nothing removed):

| | functions | share of counted |
|:--|--:|--:|
| In `src/` | 529 | |
| Not in Charon output (feature-gated `kyber768.rs`, `mlkem1024.rs`) | 6 | |
| Counted | 523 (6001 code lines) | |
| Stopped at Charon | 51 | 9.8% |
| Stopped at Aeneas | 204 | 39.0% |
| Stopped at Lean | 18 | 3.4% |
| Through all three | 250 (1432 lines, 23.9%) | 47.8% |
| Compile with every local callee | 217 (1156 lines, 19.3%) | 41.5% |
| No axiom beneath, census column (frozen definition) | 127 (548 lines, 9.1%) | 24.3% |

Over all 529 functions in `src/`, the no-axiom share is 24.0%.

**Lean cross-check** (`./run.sh axioms`):

| reading | functions | code lines |
|:--|--:|--:|
| Strict: nothing beyond `propext`, `Classical.choice`, `Quot.sound` | 73 (14.0%) | 345 (5.7%) |
| Middle: opaque external types allowed | 146 (27.9%) | 642 (10.7%) |
| Through, in the environment and free of `sorryAx` | 219 (41.9%) | |

Lean accepted 82 opaque types and 671 opaque values that Aeneas emitted as axioms.

**The named functions:**
- **Entry points:** `message_encrypt`, `message_decrypt` and `process_prekey_bundle` all stop at Charon, 0 of 3. Charon's message is "Coroutines are not supported".
- **Every `async fn`:** all 51 in `src/` stop at Charon, 0 through. This includes the helpers `message_decrypt_prekey`, `message_decrypt_signal`, `process_prekey` and `process_prekey_impl`.
- **`ratchet.rs`:** 1 of 7 through (`spqr_chain_params`, with an axiom beneath). The six `initialize_*` functions stop at Aeneas: four with "function called here is missing from the crate", two with "Uncaught exception: Not_found".
- **`ratchet/keys.rs`** (informational): 15 of 20 through, 11 with no axiom beneath; 4 stop at Aeneas and 1 at Lean.

**Largest causes:**
- 102 functions have as first message that the type `SignalProtocolError` could not be found. Aeneas rejects it with "Dynamic trait types are not supported yet"; the type holds a `Box<dyn Error …>` at `error.rs:87`.
- 51 stop on Charon coroutines.
- 27 stop on an uncaught `Not_found` in Aeneas.

**Side row:** the unpatched release Aeneas (nightly-2026.11.09) on the same LLBC aborts the whole crate with "Unimplemented" on the signature of trait `handshake::Handshake`. No Lean is produced: 0 of 529.

**Sizes and times:** the LLBC is 2.0 GB and the generated Lean is 79,400 lines with 768 axioms. Charon took 16.1 s, patched Aeneas 445.6 s, `lake build` 22.5 s.

**Disk:** `work/` peaked at about 20 GB apparent in `du`, of which about 14.5 GB were copy-on-write clones; new data was about 5 GB. Free space went from 84 GB at the start to 70 GB before clean (other agents were also writing) and 75 GB after. `work/` and `census/tools/fninv/target` are deleted.

**Pipeline regression:** `cd clausal && ../tools/sem.sh 3 -- ./run.sh` exits 0 with 97 of 97 verdict codes identical to the baseline at `5e6cfa7`.

## Reviewer

The builder's report holds. I reran the whole S1a pipeline from commit 419b689 in a scratch copy: the libsignal clone at b2a5c30f, Charon, the patched aeneas-p5 (81c0b10c-dirty), lake build, axiom_check, the side row and the report. After fixing an artifact of my own scratch path (it contains "/-", which breaks Lean comment nesting; see the should-fix), `functions.tsv`, `axioms.json` and the `RESULT.md` body are byte-identical to the commit, and `result.json` differs only in timings (Charon 46.8 s and Aeneas 243.6 s against the builder's 16.1 s and 445.6 s; lake 19.7 s against 22.5 s).

**Recount from the raw per-function JSON.** Of 529 functions in `src/`, 6 are absent (feature-gated kyber768 and mlkem1024), leaving 523 counted. 51 stop at Charon, 204 at Aeneas, 18 at Lean, and 250 get through. 217 compile with every local callee. 127 have no axiom beneath (24.3%; 548 of 6001 lines, 9.1%; median 3 lines). The 60 inventory functions outside `src/` (`test-support`, `cross-version-testing`) are all absent. The Lean cross-check reproduced exactly: 73 strict (14.0%), 146 middle, 219 of 250 through and free of sorryAx, 31 over a silent sorry, 82 opaque types and 671 opaque values accepted. The lake log has 887 errors located in the generated file plus a final 'build failed' line, 888 in all, the last at line 79317, so the whole file was elaborated.

**The three entry points, one by one.** `message_encrypt` (`session_management.rs:43`), `message_decrypt` (`:158`) and `process_prekey_bundle` (`session.rs:198`) are all `async fn`. Charon emits 'Coroutines are not supported' inside each body (51:32, 168:22, 206:17), and their LLBC declaration body is Error. The four helpers behave the same way. The Charon log has exactly 51 coroutine warnings, matching the 51 `async fn` in `src/`, none of which gets through.

**`ratchet.rs`.** 1 of 7 gets through: `spqr_chain_params`, with the axiom `spqr...ChainParams...default` beneath it. Of the six `initialize_*` functions, four stop at Aeneas with 'missing from the crate' and two with Not_found.

**Other claims checked.** The `SignalProtocolError` claim holds: 'Dynamic trait types are not supported yet' at `error.rs:19-107`, followed by 'Could not translate type decl'. The side row aborts the whole crate with Unimplemented at `src/handshake.rs:31-56`.

**Freeze and scope.** `frozen.json` is unchanged between the freeze (5ff3115) and the result commit. The changes made after the freeze do not move the outcome:
- the `src/` filter, which `frozen.json` already states;
- the Aeneas-log path mapping, which only attributes more errors;
- the side-row display.

Since base 5e6cfa7 only `census/signal/` changed: no rules, statements, Clausebook, expected verdicts or frozen test files. Nothing is tuned to the frozen 48 sentences, and no proofs are claimed.

**Outcome.** The negative half is reported as negative: 0 of 3 entry points translate. The 'not met' outcome follows the frozen function-count definition, and it stays above 10% under the strict Lean reading too (14.0%). The builder states plainly that the line share is below 10%.

**Commit hygiene.** The largest committed blob is 113 KB, and the committed files contain no absolute paths. `census/signal/work` and the fninv target were deleted and are git-ignored.

**My footprint.** My rerun peaked at about 20 GB apparent (mostly copy-on-write clones), with free space between 68 and 75 GB. I then deleted it. About 14 MB is kept in `<scratchpad>/review-S1a/`: the scratch copy's scripts and regenerated tables, the committed tables in `committed/`, and in `rerun-raw/` the raw per-function JSON, `charon.0.log` and `lake.log`.

**Relayed question.** `origin` already points to github.com/willackerly/clausal, and the rename is logged in DECISIONS.md on main, so the builder's 'did not affect this step' holds.

- **should-fix**: The reproduction depends on the absolute path of the work directory, and the census join over-counts without warning when that path contains "/-". Aeneas writes absolute OUT_DIR paths (the prost and spqr build-script outputs) into Lean block comments, 1650 of them in this file. Lean reads "/-" inside a comment as the start of a nested comment, so the rest of the file becomes an unterminated comment. The census join then counts 267 functions as through instead of 250 and prints no warning. Only `axiom_check.py` fails loudly ("no AXCHK lines"). Any copy under a Claude scratchpad path (".../claude-501/-Users-...") hits this, and AGENTS.md says to run pipelines in scratch copies. The builder's own run path had no "/-", and `axioms.json` shows 0 missing names, so the committed numbers are unaffected. Fix: make `run.sh`/`signal_census.py` refuse a work path containing "/-", or fail the build step on an `unterminated comment` error or on any through function missing from Lean's environment.
- **note**: The `run.sh axioms` step elaborates the whole 79,400-line generated file with `lake env lean` (about a minute) without going through `tools/sem.sh`. The other heavy steps (fninv, tools, build, side) use it. This goes against the HANDOFF rule that heavy builds take a slot.
- **note**: The raw per-function result (`work/runs/p5-shipped/results/libsignal-protocol.json`, 3.2 MB) and the Charon, Aeneas and lake logs were deleted with `work/`. Only the derived `functions.tsv` and `result.json` are tracked, so a recount from raw output needs a full rerun (about 20 GB apparent in `work/`, about 10 minutes of tools). The census keeps such per-function files as a tarball. The 3.2 MB raw JSON could have been kept, or tarred, without absolute paths.
- **note**: The side row runs the unpatched release Aeneas only as shipped, with one round and no peel. The census's ten rows were reported after the peel (`max_rounds=200` with surgery). The pinned run itself queued a removal (`surgery: 1`) and stopped. So the 0 of 529 says what the release tool gives as shipped, not what the census procedure would give for this crate. 'Isolates the effect of the patches' holds only under the as-shipped procedure.
- **note**: The full `clausal/run.sh` regression run is not evidence for this step. The commit changes only `census/signal/`, which `clausal` does not import, so the run could not fail because of this change. The 97 of 97 identical verdict codes are informational only.
- **note**: 442 Aeneas log entries were unattributed in my rerun, against 441 reported. The per-function results are byte-identical, so this does not matter. I ran the control the builder did not formalise: 57 of the 400 stored unattributed entries name files in `src/`, and none falls inside any inventoried function's span. They sit on trait or type declarations, impl headers, `lib.rs:1` and the `sealed_sender.rs:1048` macro site. The path mapping dropped no errors it could have attributed, at least in the stored 400.
- **note**: `git status` in the worktree shows `?? clausal/.tools`. It is a symlink made by `tools/wt.sh`, and the `.gitignore` pattern `/clausal/.tools/` has a trailing slash, so it does not match a symlink. A `git add -A` would commit it. It was not committed, and this is not the builder's doing. The worktree is still 6.3 GB, almost all of it git-ignored `clausal/` build output: APFS clones made by `wt.sh`, plus the builder's regression run. The census intermediates (`census/signal/work`, `census/tools/fninv/target`) are gone and are git-ignored by `census/.gitignore`.

## Fix round

## On the repo rename (the relayed user question)

No objection, and nothing here broke. The worktree's `origin` already points at `https://github.com/willackerly/clausal.git` for fetch and push. This step does not push or fetch from it, and I changed no git configuration. The local directory is still `/Users/will/dev/lean-rosette`, and all paths in this task use that.

## Defect: reproduction depends on the work path; a path containing "/-" over-counts silently

**Confirmed as a defect and fixed.** The census now refuses to run from such a path, and the build step fails if Lean reports an unterminated comment anyway. The generated Lean is not edited. The committed counts (250 through, 127 with no axiom beneath) are unchanged after a full rerun.

Commit: `f603f9c` on `wave/signal`, on top of `419b689`.

### What changed (all in `/Users/will/dev/lean-rosette/.worktrees/signal/census/signal/`)

- **`guard.py` (new):** `guard.py path <dir>` exits 1 if the path, as given or with symlinks resolved, contains `/-` or `-/`. `guard.py lake <log>` exits 1 on an `unterminated comment` error. It has a `--self-test`.
- **`run.sh`:** calls the path guard before every step except `clean`.
- **`signal_census.py`:** runs the path guard at start. After the build it scans `lake.log`; on `unterminated comment` it deletes the result file the join just wrote and exits 1, so the report cannot pick up a wrong join.
- **`axiom_check.py`:** runs the path guard, and exits without writing `axioms.json` if Lean's output has `unterminated comment`.
- **`README.md`:** a design note on the mechanism, a row for `guard.py`, and the second run's timings.
- **`RESULT.md`, `result.json`:** regenerated by the rerun; only timing fields differ.

I also refuse `-/`, which the reviewer did not ask for: it would close a comment early in the same way.

### Verification

1. **Self-test.** `python3 guard.py --self-test` prints `guard.py self-test ok`.

2. **Reviewer's scenario.** I copied `census/signal`, `census/scripts`, `census/lean-pinned` and `tools` under the scratchpad (path contains `/-Users-will-...`) and ran each step with `MAIN_CENSUS=/Users/will/dev/lean-rosette/census`:
   ```
   setup exit 1
   tools exit 1
   build exit 1
   axioms exit 1
   side exit 1
   report exit 1
   all exit 1
   census/signal: refusing to run: the work path '/private/tmp/claude-501/-Users-will-dev-lean-rosette/.../repo/census/signal/' contains '/-'.
   ```
   `python3 signal_census.py p5 shipped build` and `python3 axiom_check.py` called directly print the same refusal (the join exits 1). `./run.sh clean` still works there (exit 0). Nothing was fetched or built in that copy.

3. **Build-step guard, end to end.** In the worktree, after a real build, I replaced the worktree path in the 1650 comment lines of the generated Lean with `/private/tmp/claude-501/-Users-x/scratchpad/repo/` and ran the build step:
   ```
   census/signal: the Lean build is not usable: error: Generated/LibsignalProtocol.lean:79400:0: unterminated comment
   ... The result of this build was removed.
   build exit 1
   ```
   The results directory was then empty. After restoring the file: `p5 shipped build libsignal-protocol fns 589 charon_ok 472 aeneas_ok 268 ok 250 ... lake {'rc': 1, 'secs': 28.5}`, exit 0.

4. **Full census rerun in the worktree** (`./run.sh setup`, `tools`, `build`, `axioms`, `side`, `report`):
   ```
   p5 shipped tools libsignal-protocol fns 589 charon_ok 472 aeneas_ok 268 ok 0 ... secs [50.0, 194.1]
   p5 shipped build libsignal-protocol fns 589 charon_ok 472 aeneas_ok 268 ok 250 ...
   {'row': 'p5-shipped', 'constants_checked': 10070, 'counted': 523, 'through': 250, 'through_in_env_without_sorry_lean': 219, 'no_axiom_lean': 73, ... 'no_value_axiom_lean': 146, ... 'no_axiom_census': 127, 'agree_clean': 73, 'census_only': 54, 'lean_only': 0, 'through_but_not_clean_why': {'sorryAx': 31, 'crate axiom': 146}}
   pinned shipped build libsignal-protocol fns 589 charon_ok 0 aeneas_ok 0 ok 0 as_is Aeneas aborted the whole crate (fatal exception): Unimplemented
   criterion for "not a Route A target" not met
   ```
   `axioms.json` and `functions.tsv` are byte-identical to `419b689`. `RESULT.md` and `result.json` differ only in four timing fields. The guard does not fire on the real `lake.log`, which has ordinary errors.

5. **One full `clausal/run.sh`** under `tools/sem.sh 3`: exit 0, "RESULT: every scenario got its expected verdict and every Rule statement its expected one". All 97 verdict nodes (39 scenario, 12 function, 46 group) have the same code as the baseline `graph.json`: 0 differences.
   - Bounded-check totals moved from 181 verified / 61 failed / 27 no answer (baseline) to 173 / 61 / 35 under load.
   - Eight harnesses went from verified to timeout: `k9_r3`, `k26_r2`, `k31_r2`, `k32_r1`, `k35_r1`, `k42_r2`, `k42_r3`, `k68_r2`. None changed in the other direction.
   - This per-harness list is against the committed `clausal/out/evidence.json` at HEAD, which has the baseline's totals; the baseline directory holds no evidence file.
   - I restored the regenerated `clausal/out/*` files with `git checkout`, so they are not in the commit.

6. **Disk.** 73 GB free before, 67 GB at the lowest point, 71 GB after `./run.sh clean`. `work/` is deleted. What remains is `census/tools/fninv/target` (40 MB, git-ignored).

### Not done, not verified

- The `unterminated comment` branch inside `axiom_check.py` was not reached in the injection test: the build step had already removed the result file, so the script stopped earlier with `FileNotFoundError` (exit 1, no `axioms.json` written). That branch is covered only by the regex case in the self-test.
- I did not run a full pipeline from a `/-` path to reproduce the reviewer's 267. The refusal now prevents it, and the injection test stands in for it.
- `report` is also refused from a bad path, although it only reads results. I left it that way since no valid results can exist there.

### What a reviewer should distrust

- The path guard is conservative: it refuses any `/-` or `-/` in the checkout path, even if a future translator stopped writing paths into comments.
- The build-step guard catches only this one symptom (`unterminated comment`). Any other way for a region of the file to lose its errors is caught only by the axiom check's "not in the environment" count, which is reported but does not fail the run.
- The timings in `RESULT.md` are now from the second run (Charon 50 s, Aeneas 194 s) and differ from the first (16 s, 446 s). Both are machine-load dependent.

## FOR DECISIONS.md

1. **Refuse to run rather than sanitise.**
   - What: `census/signal` refuses a checkout path containing `/-` or `-/` (`guard.py`, called from `run.sh`, `signal_census.py`, `axiom_check.py`).
   - Why: Aeneas copies absolute `OUT_DIR` paths into nesting Lean block comments. A `/-` turns the rest of the file into one comment, and the join over-counts through functions (267 instead of 250) without warning. Rewriting the generated Lean would mean editing translator output.
   - Undo: remove the guard line in `run.sh` and the `guard.check_path(SIG)` lines in the two Python scripts.

2. **Second layer on the build step.**
   - What: `signal_census.py` deletes the join it just wrote and exits 1 if `lake.log` has an `unterminated comment` error.
   - Why: so that a wrong count cannot reach `signal_report.py` if the path guard is bypassed or the cause is something else.
   - Undo: remove the five lines after `C.finish(...)`.

3. **`-/` is refused as well as `/-`.**
   - What: an extension beyond the reviewer's finding.
   - Why: it would close a comment early by the same mechanism.
   - Undo: drop `'-/'` from `BAD` in `guard.py`.

4. **Regenerated tables committed.**
   - What: `RESULT.md` and `result.json` now carry the second run's timings; no count changed.
   - Why: they are generated files ("do not edit; rerun"), and the rerun is the verification of this fix.
   - Undo: `git checkout 419b689 -- census/signal/RESULT.md census/signal/result.json`.

5. **`clausal/out/*` not committed.**
   - What: the full `clausal/run.sh` rewrote the tracked outputs (timestamps, timings, Kani inputs); I restored them.
   - Why: this step changes nothing under `clausal/`.
   - Undo: nothing to undo.

6. **Carried from the previous step, unchanged:**
   - The row is the `signalapp/libsignal` workspace at tag `v0.105.4` (commit `b2a5c30f`, member `rust/protocol`, Cargo package version 0.1.0), because the crate is not published on crates.io.
   - Only `rust/protocol/src` is in the denominator.
   - An `async fn` counts as one function.
   - `CARGO_HOME` is inside `work/`.
   - The row is not added to the ten-crate tables.
   - The side row reuses the patched row's LLBC.
   - Undo for each is in `census/signal/README.md` and `frozen.json`.

## FOR RESULTS

Reproduce with `cd census/signal && ./run.sh setup && ./run.sh tools && ./run.sh build && ./run.sh axioms && ./run.sh side && ./run.sh report`, from a checkout path without `/-` or `-/`. It needs the fork build in the main checkout's `census/fork`. `./run.sh clean` removes `work/`. All numbers are in `census/signal/RESULT.md`, `result.json`, `functions.tsv` and `axioms.json`.

**Patched translator (p5), as shipped — libsignal-protocol v0.105.4**

| Measure | Count | Share of 523 counted |
|:--|--:|--:|
| Functions in `src/` | 529 | |
| Not in Charon output | 6 | |
| Counted | 523 | |
| Stopped at Charon | 51 | 9.8% |
| Stopped at Aeneas | 204 | 39.0% |
| Stopped at Lean | 18 | 3.4% |
| Through all three | 250 | 47.8% |
| Compile with every local callee | 217 | 41.5% |
| No axiom beneath (frozen definition, census column) | 127 | 24.3% |

- **No axiom beneath, other readings:** 24.0% of all 529 functions in `src/`. By Lean's `collectAxioms`, strict: 73 (13.96%). Allowing opaque external types: 146 (27.9%).
- **Lean cross-check detail:** 10,070 constants checked; 0 through functions missing from Lean's environment; 31 through functions sit on `sorryAx` and 146 on a crate axiom; the census column over-counts the strict Lean answer by 54.
- **By code lines:** 6,001 counted; through 1,432 (23.9%); with every local callee 1,156 (19.3%); no axiom beneath 548 (9.1%). The median no-axiom function is 3 lines.
- **Entry points:** `message_encrypt`, `message_decrypt` and `process_prekey_bundle` all stop at Charon ("no body in LLBC"). All 51 `async fn` stop at Charon; 0 come through.
- **`src/ratchet.rs`:** 1 of 7 through (`spqr_chain_params`, not axiom-free). The six `initialize_*` functions stop at Aeneas.
- **Generated Lean:** 79,400 lines, 768 axioms in the file; `lake build` exits 1.
- **Unpatched release Aeneas on the same LLBC (side row):** aborts the whole crate; 0 of 529 through.
- **Outcome against the frozen criterion:** not met. No entry point translates, but 24.3% is not below 10%, so the rule "not a Route A target" does not fire. This is not a finding that libsignal is a Route A target.
- **Timings, second run (2026-11-12, shared machine):** Charon 50.0 s, patched Aeneas 194.1 s, `lake build` 28.5 s, unpatched Aeneas 72.4 s. First run: 16.1 s, 445.6 s, 22.5 s, 78.0 s.
- **Fix-round checks:**
  - Bad-path copy: every `run.sh` step except `clean` exits 1 (reproduce by copying `census/signal`, `census/scripts`, `census/lean-pinned` and `tools` under any path containing `/-` and running `./run.sh setup`).
  - Injected `/-` in the generated Lean: build step exits 1 and removes the join.
  - `python3 census/signal/guard.py --self-test`: ok.
- **`clausal/run.sh` (full, `tools/sem.sh 3 -- ./run.sh` in `clausal/`):** exit 0; 97 of 97 verdict codes identical to the baseline; Kani 173 verified / 61 failed / 35 no answer against the baseline's 181 / 61 / 27, with the eight harnesses listed above.
