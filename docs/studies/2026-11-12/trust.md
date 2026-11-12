# Design study: who is trusted for what in Clausal

Read-only study at commit `a7325a1`; nothing was built, compiled or run. The data model below is implementable now, and the cheapest moment to adopt the record format is before H1, because no sign-off file exists yet. Paths are relative to `/Users/will/dev/lean-rosette`.

## 0. How it works today

- **Two sign-off stores, neither populated.**
  - The old glossary uses `clausal/glossary.signoff.json` with `{reviewer, date, phrase, target}` (`clausal/clausal/report.py:1988-2013`).
  - Pieces use `clausebook/<book>.signoff.json` with `{reviewer, date, digest}`, stored beside the defining book (`clausal/clausal/vreport.py:197-228`).
  - No such file exists under `clausal/` or `clausal/clausebook/`.
- **What a piece signature covers.** `piece_digest` hashes the entry's YAML text, the text of each Lean definition in its `defs:`, and the defaults it names; separations add both pieces and the compiled Lean (`vreport.py:182-194`).
- **The signer is a free string.** `clausal review <id> --reviewer NAME` accepts anything. For old glossary entries the code prepends `human:` to whatever was typed and emits `human-asserted` evidence (`report.py:865-871`).
- **Piece sign-offs never reach the graph as evidence.** They appear only as `attrs.reading.pieces[].signed/by` (`vreport.py:283-285`).
- **Negative: rule verdicts read `pass` in the graph with nothing signed.** Rule verdicts are written with `"unreviewed": []` and `"chain": []` (`report.py:916-918`). In the committed `clausal/out/graph.json`, 34 `group:rule:` verdicts are `pass` / PROVED-FOR-ALL while the report says "27 Clausebook pieces, 0 signed [NOT ASSERTED by anyone]". Scenario verdicts correctly go to `review`.
- **Schema.** There are four evidence kinds; the agent pattern is `^(human|tool|model):.+`; `human-asserted` requires `human:`; `review.by` may be any agent (`clausal/schema/refinement-graph.v2.schema.json`).
- **Staleness.** It is computed from `evidence.inputs` digests in `clausal/clausal/graphlint.py`. The piece sign-off path does not go through it.
- **Non-standard axioms already block a proof.** `lclean` requires `axioms ⊆ {propext, Classical.choice, Quot.sound}` (`vreport.py:104-107`). An external `verify` that Aeneas emits as a Lean `axiom` (`census/PROFILE.md` §5) therefore yields "non-standard axioms", not PROVED. This is the natural hook for the ledger.
- **Strict mode.** It fails a PROVED rule with any unsigned piece (`vreport.py:316`, `report.py:292-295`). It has never been exercised with a real signature (`docs/HANDOFF.md` decision 2).
- **Sequences.** `tied` with `same_input` is in core (`clausal/clausebook/core.yaml:336-352`). An invariant over any sequence of calls is not; `reachable_always` is only a candidate in `docs/studies/2026-11-12/signal.md`.
- **Stale doc.** `docs/SCHEMA.md` still quotes 109 nodes and 15 verdicts; the committed graph has 940 nodes, 1474 edges and 120 verdicts.

## 1. Data model

### 1a. Attestation record

Replaces both `.signoff.json` shapes. One file per book, `clausebook/<book>.attest.json`, holding a list. Records for ledger entries and policies go in `clausal/trust/<project>.attest.json`.

```json
{
  "subject": {"kind": "piece", "book": "local/intake", "id": "in.verifies",
              "digest": {"alg": "sha256-text", "value": "<piece_digest today>"}},
  "act": "reviewed",
  "signer": {"kind": "model", "id": "model:claude-fable-5-2", "name": "Fable 5.2"},
  "on_behalf_of": "human:will-ackerly",
  "at": "2026-11-12T02:10:00-05:00",
  "scope": "entry text and Lean definition read against each other; 216-point grid of the Rust reading run",
  "context": {"commit": "a7325a1", "run": "run:clausal", "toolchain": "<lean-toolchain>"},
  "signature": null
}
```

- **`subject.kind`:** `piece | separation | assumption | specialist-term | external-proof | join | policy`.
- **`act`:** `authored | tested | reviewed | approved | vouched | refereed`.
- **`signer.kind`:** `person | model | tool | organisation`. It is derived from the id prefix and refused if the two disagree.
- **`on_behalf_of`** records delegation and never changes the kind.
- **`signature`** is optional: an SSH signature over the canonical bytes of the other fields (`ssh-keygen -Y sign`), checked against keys named in the policy.
- **A person's placeholder is not a record.** It is an unmet requirement in the policy, printed as "awaited". A placeholder record in this file would be a laundering surface.

Fit to the graph, as schema 2.1 (additive: every v2 graph still validates):

| Change | Rule enforced in the schema |
|---|---|
| Agent prefix `org:` added | — |
| Kind `model-asserted` | `by` matches `^model:` |
| Kind `specialist-asserted` | `by` matches `^(human\|org):`; `artifact` (the pointer) required |
| Kind `externally-checked` | `artifact` and `method` required; `axioms` forbidden, so it can never read as checked here |
| Kind `assumed` | `artifact` is the ledger id; allowed only on the new `assumes` relation |
| `human-asserted` | Unchanged |

- Model attestations with act `authored` or `tested` map to existing fields: `origin.by` and `tested` evidence.
- For any of this to reach the graph, pieces must become `phrase`/`definition` nodes with `binds` edges, as old glossary entries are.
- Rule verdicts must carry `unreviewed` and take outcome `review` when requirements are unmet. This fixes the section 0 defect and is a prerequisite.

### 1b. Trust policy

One file per project, named from `clausal/projects.yaml` by a new key `trust: trust/intake.yaml`. Its sha256 goes in `runs[].config.trust_policy`, which is already a free object.

```yaml
version: 1
project: intake
roots:
  - id: owner
    signer: human:will-ackerly
    ssh_key: null            # none registered: a record is then "claims to be", printed so
  - id: fable
    signer: model:claude-fable-5-2
    on_behalf_of: [human:will-ackerly]
  - id: crypto
    signer: null             # AWAITED: nobody named
    roles: [specialist:cryptography]
requirements:
  meaning.core:      {subject: piece, books: [core.yaml],          act: approved, kinds: [person], roots: [owner]}
  meaning.domain:    {subject: piece, books: [local/intake.yaml],  act: approved, kinds: [person], roots: [owner]}
  separation:        {subject: separation, act: approved, kinds: [person], roots: [owner]}
  assumption.vouch:  {subject: assumption, act: vouched,  kinds: [person, organisation], roles: [specialist:cryptography]}
  assumption.usage:  {every_condition: PROVED-FOR-ALL}
  specialist.term:   {subject: specialist-term, act: approved, kinds: [person, organisation], roles: [specialist:cryptography]}
recorded_not_counted:        # shown under its own label, satisfies nothing above
  - {act: [authored, tested, reviewed], kinds: [model, tool]}
strict:
  demands: [meaning.core, meaning.domain, assumption.vouch, assumption.usage, nothing-stale]
  unsigned_person_record: refuse     # once ssh_key is set
```

- A policy may list `model` under a requirement; the owner's steer leaves that per project.
- Two things are fixed in code, not policy: the evidence kind printed is always the signer's own, and a meaning requirement met only by models sets the flag `MEANING-MODEL-ONLY`, which ranks in the top tier of section 3.
- Counts such as `min: 2` count distinct roots listed here, never distinct strings.

### 1c. Assumption ledger entry

File `clausal/trust/assumptions.yaml`. A book entry points to it with a new key `assumes: [A.sig.unforgeable]`, which sits inside the entry text and therefore under `piece_digest`.

```yaml
assumptions:
  - id: A.sig.unforgeable
    statement: "Without the signing key, nobody can produce a message and tag that verify under the matching public key."
    class: property              # or opaque-function: a Lean axiom standing for external code
    lean_axioms: []              # opaque-function entries list the axiom names lclean may admit
    stand_in: true               # the fixture's verifier is a toy; never printed as a claim about a real scheme
    attached_to: [in.verifies]
    usage_conditions:
      - {id: U1, rule: Rule.intake.accept_only_if_verified}
      - {id: U2, rule: Rule.intake.unverified_rejected_unchanged}
      - {id: U3, rule: Rule.intake.unsigned_part_ignored}
      - {id: U4, rule: null, unstated: "no counter is accepted twice over ANY sequence of intakes; no frame for it"}
    not_covered: ["the expected key is the right key", "the library's verify is the scheme's verify"]
    external_proof: null         # or {pointer, commit, sha256, theorem}
    review_by: 2027-11-12
```

- Each condition's verdict is read from the graph at report time and never stored.
- The entry is an `assumption` node (a new node kind). It links by `assumes` from the `definition` of the word, and by the existing `requires` relation to each condition's statement.
- `lean_axioms` extends the allow-list in `lclean`. A proof using one stays PROVED-FOR-ALL with flag `ASSUMES:<id>` and `assumed` in `rests_on`.
- Unforgeability itself never appears in a proof term. It attaches to the meaning of a word, which is why it hangs off the piece and not the theorem.

### 1d. Specialist term

A book entry, so it uses the existing loader, digest and `terms.lock.json` machinery.

```yaml
  - id: x.forward_secrecy
    kind: specialist
    cat: external                 # fills no hole of any frame yet (see section 7)
    forms: ["forward secrecy as stated in the Signal verification"]
    pointer: {repo: "<not looked up>", commit: "<40 hex>", file: "<path>", decl: "<Lean name>"}
    sha256: "<of the vendored bytes>"
    vendored: clausebook/external/<sha256>.lean
    requires_role: specialist:cryptography
    echo: "(meaning held elsewhere; not read or checked by this project)"
```

- Its `binds` edge can carry only `specialist-asserted` evidence.
- An external proof is a statement node whose `realises` evidence is `externally-checked`.
- **The join** is an ordinary local rule, typically `agrees_with` against the model the external theorem is about, plus a record:
  `{external: <sha256>, contract: <statement digest>, discharged_by: [rule ids], gap: "<what is not joined>"}`.
- For the Signal report specifically the external theorems are about the compiled binary (`docs/studies/2026-11-12/signal.md` §1), so there is no Rust-level contract to join. The `gap` field would say that.

## 2. Staleness

| Item | Void or stale when | Mechanism |
|---|---|---|
| Attestation | Subject digest differs from current | As today |
| Attestation (`tested`) | `context.toolchain` differs from the run's | New |
| Attestation (signer) | Signer is no longer a root | Not stale; "not admitted", computed against the policy at read time |
| Policy | Its sha256 differs from `runs[].config.trust_policy` | Verdicts stale; attestations are never touched |
| Ledger entry (vouch) | Digest changes. Digest = statement, condition list, each condition rule's `lean_sha256` from `terms.lock.json`, `not_covered`, external hash | Rewording, adding or dropping a condition voids the vouch |
| Ledger entry (conditions) | A condition's verdict changes | Vouch stays; entry becomes "conditions not met"; every verdict whose chain has the `assumes` edge is flagged |
| Ledger entry (time) | `review_by` has passed | The first time-based rule; marks the vouch stale |
| Specialist term | Hash or pointer changes | It is under `piece_digest`, so approvals void and sentences listing it in `terms.lock.json` are reported |
| Specialist term (upstream) | Fetched bytes differ from `sha256` | `book check` reports MOVED and fails |
| External proof and join | Contract digest or external hash changes, or the local model changes | Join rules re-run under the existing rule |

Known hole, from reading `piece_digest` (not run): it hashes only the definitions named in `defs:`. A change to a helper those definitions call leaves the digest unchanged. The graph's "suspect" rule would catch it, but sign-offs do not go through the graph. Routing validity through `graphlint.staleness` once pieces are nodes closes it.

## 3. The report's "rests on" block

Today the block prints every piece inline: 27 ids for one rule at `clausal/out/report.md:378-390` in the committed copy. Proposed: the three heaviest items, one line of counts, and the full list folded.

**Ranking key:** `(tier, −reach, id)`.

- **Tier 0, open:** stale, or a policy requirement unmet. This includes model-only where a person is required, an unvouched assumption, and a usage condition not proved.
- **Tier 1, nothing here checks it:** an assumption that is vouched with conditions met; by-reference terms and proofs; tool-trusted links with no tested cross-check.
- **Tier 2:** everything else.
- **Reach** is the number of this project's verdicts whose chain contains the item (what `graphlint --what-if` already counts).

Tier 0 is shown first, up to three; any remainder is counted, never dropped. Tiers ask whether anything in this run checked the item. They do not rank the evidence kinds against each other, so §2 of `docs/SCHEMA.md` (no single scale) stands.

```
  Rests on   3 heaviest of 31 (full list below)
    1 ASSUMED      nobody can forge a signature without the key (A.sig.unforgeable; stand-in verifier)
                   vouched by: nobody this project accepts     usage: 3 of 4 proved here, 1 cannot be stated
                   6 other rules of this project rest on it                                      [assumed]
    2 MEANING      "the signature of the message verifies under the expected key" (in.verifies)
                   reviewed by Fable 5.2 for Will Ackerly, 2026-11-12; no person has signed      [model-asserted]
    3 TRANSLATION  Lean model of intake, charon + aeneas (patched); same result on 216 inputs    [tool-trusted, tested]
    and 28 more: 26 core pieces (0 person, 26 model), kernel proof (standard axioms only), rustc
```

Counts are never summed across kinds.

## 4. Threats

| Threat | Defence | Undefended |
|---|---|---|
| **Laundering** (model attestation shown as review) | Kind derived from the id prefix and enforced by the schema. `on_behalf_of` never upgrades. `clausal review` becomes `clausal attest --as` and refuses a bare name. No cross-kind totals. `MEANING-MODEL-ONLY` flag. | Without a key, identity is a typed string: an agent can type `human:will-ackerly`, exactly as `--reviewer` allows today. Only the SSH signature closes it, with a key agents cannot read. Until then person records print as "claims to be". Related: the code itself assigns `human:aeneas-authors` and `human:rust-std-authors` as origins (`report.py:848-850`). |
| **Ledger makes "assumed" look settled** | No stored status. An assumed item is never below tier 1, so it is always in the top block. The verdict line reads "PROVED, GIVEN 1 ASSUMPTION". Outcome is `review` unless vouched and all conditions proved. `unstated` conditions and `not_covered` are printed. `review_by` expiry. A word naming a missing entry stops `book check`. | Whether the usage conditions are the right ones or complete; that is the voucher's judgement. Reader habituation; W5 measures it. |
| **Sybil contributions** | Contributions carry no weight until a listed root attests. No reputation or signer counts from an open set. | Review load from spam. Capture of a curated set's referees. Not built. |
| **Specialist term changes behind a stable name** | Hash inside the entry and under the digest. Vendored bytes. Fetch-and-compare in `book check`. Commit pinned. | The hash pins the file, not its meaning: that depends on every definition it imports and on the toolchain. No closure hash exists (`docs/SCHEMA.md` §8 question 1). |
| **Replay of an old attestation onto changed text** | Subject digest (existing; selftest covers entry, default, coverage and retired-form changes, and per-book storage, `clausal/clausal/selftest.py:448-464, 840, 883-900`). `act`, `subject.book` and `context` inside the signed bytes. | The helper-definition hole in section 2 until validity goes through the graph. Edited dates or fields in unsigned records. |

## 5. First tests

**Test 1: signed intake on a toy verifier.** Frozen before any code is written: the rules, the ledger entry, the policy and the controls.

- **Fixture.** A fourth project `intake`, about 40 lines of in-profile Rust. State is (expected key, last counter); the message is (payload, counter, tag, unsigned hint). `verify` is a toy function with a body, so it translates without an axiom.
- **Rules.** SM-1, 2, 3, 5, 8 and 9 from `docs/studies/2026-11-12/packs.md` §2b, plus SM-10 written with `tied` / `the same input`. The study marks 1, 2, 3, 5, 9 "yes" and 8 "likely"; none has been compiled.
- **Ledger.** `A.sig.unforgeable` as in 1c, with `stand_in: true`.
- **Attestations.** One model record as in 1a. The owner's approval and the specialist's vouch are unmet requirements, printed "awaited".
- **Controls:**
  1. A mutant that accepts before verifying: U1 is REFUTED and every rule using `in.verifies` is flagged.
  2. A mutant that takes the key from the message.
  3. Editing the word's Lean definition voids the model record.
  4. A record with `kind: person` and a `model:` id is refused.
  5. `--strict` fails, naming the two awaited items.
  6. Deleting the ledger entry stops the run.
  7. A variant with `verify` declared external: not PROVED without `lean_axioms`, and PROVED with the flag once listed.

**Test 2: TDFLite permit and key release (T9.5).** Source: `docs/studies/2026-11-12/tdf-core.md` lines 104, 122, 140-144 only; `private/` was not read.

- **Assumptions:** the key-wrap primitive, and collision resistance of the binding hash that `release(permit, dek)` compares.
- **Usage conditions:** release only with a `Permit` built by `decide` (compile-fail test), and "A rejected key release gives the same answer whatever the data key".
- **Expected to be uncomfortable.** Under O12 key material stays in Go. The two-run rule on the Rust core is then true by typing and proves nothing, and the real condition is Route B tested at best. The ledger should show exactly that; if it shows three green conditions, the design has failed.

## 6. Plan nodes

The track letter W is provisional. Each row gives its test and the result that counts against the design.

| Node | What | Test | Counts against |
|---|---|---|---|
| W0 | Freeze: record format, kinds table, policy keys, test 1 rules and controls | Committed before code | — |
| W1 | Attestation records replace both sign-off files; `clausal attest`. Needs to land before H1 | Existing sign-off selftests pass in the new format; 6 malformed or kind-mismatched records refused | A check now passing needs the old format |
| W2 | Schema 2.1; pieces as nodes with `binds`; rule verdicts carry `unreviewed` | Committed graph validates unchanged; refusals in `clausal/schema/selftest.py` grow from 10 to at least 16; the 34 rule verdicts become `review` | Piece nodes more than double the graph, or any verdict code changes |
| W3 | Policy file and strict mode from policy | Two policies over one tree give different outcomes and identical evidence | Evidence or verdict codes differ between policies |
| W4 | Ledger, `assumes:`, axiom allow-list | Controls 1, 6, 7 | A seeded misuse leaves the assumption line unchanged |
| W5 | Ranked block | Readers (models as labelled proxies, then people with H2) name the heaviest item and say whether the rule is "verified", against the full list | No better at naming it; or more readers call an assumed rule verified with the ledger than without |
| W6 | Test 1 | 7 of 7 controls | Fewer than 3 of 4 usage conditions compile with today's pieces; or the model record appears in any count labelled sign-off |
| W7 | Test 2 | Conditions show their real evidence class | All conditions green while O12 holds |
| W8 | Specialist term and external-proof link, used only as a ledger statement | Changed vendored byte reported; approval voided | The term's hash is stable while an imported definition changed and nothing reports it (expected; recorded as the boundary) |
| W9 | SSH signatures for person roots | A record typed by an agent under a person's id is refused in strict mode | The key is readable by agents on this machine |

**Would not build yet:**

- Curated sets and referees.
- Multi-signer thresholds.
- Any key registry or transparency log.
- Specialist terms filling a frame's hole. That would put an unreviewed definition under a one-line cover, which `signal.md` §2 argues against and steer (a) excludes.
- Export to a standard attestation envelope (`docs/PLAN.md:448`). The record is shaped to map to one later.
- A frame for invariants over arbitrary sequences. Without it "nonce never reused" stays `unstated`, which is the main weakness of "prove the usage conditions" today.

## Not checked

- Nothing was compiled or run; the "stateable" claims for the SM rules are taken from `packs.md`, which also did not compile them.
- `piece_digest`'s helper-definition hole is from reading the code, not from a test.
- The working tree's `clausal/out/` was mid-run with files deleted. Graph facts are from the committed copy, extracted to `<scratchpad>/trust-graph.json`.
- `clausal/DESIGN.md`, `clausal/clausal/rules.py` beyond the grep hits, and `book.py` were not read.
- `graphlint.py` was read to line 80 only; its staleness function was taken from its docstring.
- `private/`, `tdflite-ideas/` and `docs/TDFLITE.md` were not opened.
- The DeepMind Lean repository was not opened; its pointer and hash are placeholders.
- The `ssh-keygen -Y` and in-toto details are from memory, not a fresh check.
- I did not check whether a track letter W or a `clausal/trust/` directory already exists on a wave branch.