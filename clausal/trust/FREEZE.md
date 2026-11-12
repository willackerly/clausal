# W0 freeze: the trust track (plan nodes W0 to W3)

Committed before any code of W1 to W3 was written and before any run that measures them. Source: `docs/studies/2026-11-12/trust.md`
(sections 1a, 1b, 5, 6) and the owner's steer in `DECISIONS.md` ("Owner's steer on trust"). Where this file departs from the study
the line says so and says why. Nothing here is signed by a person; no person has signed anything.

## 1. Attestation record

One JSON object. A store is a JSON list of records.

| Store | Holds |
|---|---|
| `clausebook/<book>.attest.json` (beside the book) | records whose subject is an entry that book defines (`piece`, `separation`) |
| `glossary.attest.json` | records whose subject is an entry of the old whole-phrase glossary (`glossary-entry`) |
| `trust/<project>.attest.json` | records whose subject is that project's policy (`policy`); later ledger entries |

```json
{
  "subject": {"kind": "piece", "book": "core.yaml", "id": "always",
              "digest": {"alg": "sha256-text", "value": "<64 hex>"}},
  "act": "reviewed",
  "signer": {"kind": "model", "id": "model:<identifier>", "name": "<optional display name>"},
  "on_behalf_of": null,
  "at": "2026-11-12T02:10:00-05:00",
  "scope": "<what was looked at, in words>",
  "context": {"commit": "<optional>", "run": "<optional>", "toolchain": "<optional>"},
  "signature": null
}
```

Fields: `subject`, `act`, `signer`, `on_behalf_of`, `at`, `scope`, `signature` are required (the last and `on_behalf_of` may be
`null`); `context` is optional. No other field is allowed, at any level.

- `subject.kind`: `piece | separation | glossary-entry | policy` are built in W1 to W3. `assumption | specialist-term |
  external-proof | join` are reserved names of the study (W4, W8): a record with one of them is refused as "not built".
  `glossary-entry` is not in the study: it is added because the task replaces BOTH sign-off files and the old glossary's
  entries are not Clausebook pieces.
- `subject.book`: for `piece` and `separation`, the book that defines the entry, as `clausebook/project.yaml` writes it. For
  `glossary-entry` the string `glossary.yaml`; for `policy` the policy file's path relative to `clausal/`.
- `subject.digest`: what the attestation is OF.
  - `piece`, `separation`: `{"alg": "sha256-text", "value": piece_digest}`: the digest a sign-off covered before this change
    (`vreport.piece_digest`: the entry's text, the text of each Lean definition it names, the defaults it names; for a
    separation also both pieces and what each sentence compiles to). Unchanged by W1.
  - `glossary-entry`: `sha256-text` of the phrase node's identity value, a newline, the bound node's identity value (the two
    digests the old record stored side by side).
  - `policy`: `{"alg": "sha256", ...}` of the file's bytes.
- `act`: `authored | tested | reviewed | approved | vouched`. (The study also lists `refereed`; it belongs to curated sets,
  which the study says not to build yet, so it is not an act here and a record with it is refused.)
- `signer.kind`: `person | model | tool | organisation`. `signer.id` carries the kind as a prefix; the two must agree.
- `on_behalf_of`: `null` or an agent id. Records delegation. It never changes the kind and is never itself counted.
- `at`: ISO 8601 date and time with a UTC offset.
- `scope`: non-empty text.
- `signature`: must be `null` in this build. Checking SSH signatures is W9; a record that carries one is refused, because
  accepting it unchecked would let it read as verified.
- A person's placeholder is not a record. Whoever is awaited is an unmet requirement of the policy.

### Table of signer kinds

| Kind | Id prefix | Evidence kind in the graph (always the signer's own) | May perform |
|---|---|---|---|
| person | `human:` | `human-asserted` | authored, tested, reviewed, approved, vouched |
| model | `model:` | `model-asserted` | authored, tested, reviewed, approved, vouched |
| tool | `tool:` | `tested` (the existing kind; a tool has no asserted kind) | authored, tested |
| organisation | `org:` | `organisation-asserted` | authored, tested, reviewed, approved, vouched |

### Table of acts

| Act | Says | In the graph |
|---|---|---|
| authored | the signer wrote the subject | no evidence entry; listed on the subject's node (`attrs.attestations`) |
| tested | the signer ran the subject against something, named in `scope` | an evidence entry of the signer's own kind, `act: tested`. (Departure: the study maps a model's `tested` to the existing kind `tested`; here a model's statement that it tested something stays `model-asserted`, so it is never read as a tool's run.) |
| reviewed | the signer read the subject against what it binds to and found them to agree | evidence entry, `act: reviewed` |
| approved | the signer accepts the subject for use (what the old sign-off was) | evidence entry, `act: approved` |
| vouched | the signer answers for a fact nothing here checks (assumptions, W4) | evidence entry, `act: vouched` |

Fixed in code, not in any policy:

1. The evidence kind printed and stored is the signer's own kind. `on_behalf_of` never upgrades it.
2. A requirement whose `kinds` is `[person]` is met only by a record whose signer kind is `person`. A model's record never
   meets it, whatever its `on_behalf_of`.
3. The graph's `unreviewed` list and the outcome `review` are about persons: a piece is unreviewed unless a valid record of
   act `reviewed` or `approved` with signer kind `person` exists for its current digest. This is the same in every policy, so
   the graph does not depend on the policy. What a project's strict mode accepts is the policy's business (section 3).
4. Counts are never summed across kinds.

## 2. Records that must be refused (W1; target: at least 6; frozen list of 14)

"Refused" means: never counted towards anything, reported with the reason, and `clausal attest check` exits 1. R5 is the
exception in kind: a well-formed record whose subject has since changed is VOID (reported, counts for nothing, exit 0), as
a sign-off was.

| # | Record | Reason expected |
|---|---|---|
| R1 | `signer.kind: person` with `signer.id: model:claude-fable-5-2` | kind and id prefix disagree |
| R2 | `signer.kind: model` with `signer.id: human:someone` | kind and id prefix disagree |
| R3 | `signer.id: "Will"` (bare name, no prefix) | no kind prefix |
| R4 | `act: refereed` (or any act outside the table) | unknown act |
| R5 | subject digest that is not the entry's current digest | VOID: the subject changed since |
| R6 | `signer.kind: tool` with `act: approved` | a tool may only author or test |
| R7 | a misspelt field (`on_behalf`) or a missing required field (`scope`) | unknown / missing field |
| R8 | `at: "yesterday"` or a date with no offset | not ISO 8601 with an offset |
| R9 | `on_behalf_of: "Will Ackerly"` (no prefix), or equal to the signer's id | malformed delegation |
| R10 | `signature: "AAAA…"` | signatures are not checked in this build |
| R11 | a record for `l.bal_of` stored in `core.attest.json` (another book's store), or `subject.book` naming a book that does not define the entry | wrong store |
| R12 | `subject.kind: assumption` | reserved, not built |
| R13 | `scope: ""` | empty scope |
| R14 | `subject.digest.alg: md5` | unknown digest algorithm |

Kind-mismatch at the level of requirements (also W1, tested in the self-test, not a malformed record):

| # | Situation | Expected |
|---|---|---|
| K1 | every piece attested `approved` by `model:selftest-fixture` | every piece is still unreviewed; a `[person]` requirement is unmet |
| K2 | the same with `on_behalf_of: human:selftest-fixture` | the same: delegation does not upgrade |
| K3 | `clausal attest <id> --as "Some Name"` | the command refuses and writes nothing |

The existing sign-off self-tests (`clausal/clausal/selftest.py`: the coverage digest, the separation control with its seven
cases, the retired-form digest, the grammar and defaults digest, sign-offs stored per book) must pass with attestation records
in place of sign-off records, with their expectations unchanged. They sign as `human:selftest-fixture` in a temporary copy of
`clausebook/`; that is a fixture identity in a directory that is deleted, not a person, and nothing of it is stored in the tree.

## 3. Policy keys (W3)

One file per project, named by the key `trust:` of the project's entry in `projects.yaml` (path relative to `clausal/`).

```yaml
version: 1
project: <name of the project in projects.yaml>
roots:
  - id: <name used by requirements>
    signer: <agent id, or null: AWAITED, nobody named>
    ssh_key: null                 # W9; must be null in this build
    on_behalf_of: [<agent id>]    # optional: a record of this root is admitted only with one of these delegations
    roles: [<role>]               # optional
requirements:
  <name>: {subject: piece | separation | glossary-entry | assumption | specialist-term,
           books: [<book>],       # optional, pieces and separations only: the books whose entries it covers
           act: <act> | [<act>],
           kinds: [<signer kind>],
           roots: [<root id>],    # optional: default every root of the policy
           roles: [<role>]}       # optional: roots holding one of these roles
  <name>: {every_condition: <verdict code>}      # W4; a policy may state it, strict cannot evaluate it yet
recorded_not_counted:
  - {act: [<act>], kinds: [<signer kind>]}       # shown under its own label; satisfies nothing
strict:
  demands: [<requirement name> | nothing-stale]
  unsigned_person_record: accept-as-claim | refuse
```

Rules of evaluation, frozen:

- A record is ADMITTED for a requirement iff it is valid (section 2) for the subject's current digest, its act is one of the
  requirement's, its signer kind is one of the requirement's `kinds`, and its signer is the `signer` of a root the requirement
  allows (with one of that root's `on_behalf_of`, if the root lists any).
- A requirement naming a root whose kind is not among its `kinds` is a malformed policy: refused at load.
- A root with `signer: null` admits nothing and is printed AWAITED.
- Strict mode, per project: a verdict of that project with code `PROVED-*` FAILS strict iff, for some demanded requirement,
  some subject the verdict rests on that the requirement covers has no admitted record; or `nothing-stale` is demanded and
  the verdict is stale; or a demanded requirement cannot be evaluated by this build (fail closed).
- `unsigned_person_record: refuse`: no person record is admitted in strict mode (none can carry a checked signature before W9).
  Default `accept-as-claim`: admitted and printed "claims to be".
- A project with no `trust:` key gets the built-in policy that restates the old strict mode: every piece, separation and
  glossary entry needs `reviewed` or `approved` by a person; any `human:` signer is a root.
- The flag `MEANING-MODEL-ONLY` is printed for a verdict whose demanded meaning requirements are all met and at least one
  is met by model records only.
- Not built (study, "would not build yet"): `min:` counts, key registries, curated sets.
- Departure from the study: the policy's sha256 is NOT written into `out/graph.json` (`runs[].config.trust_policy`). The W3
  test asks for byte-identical evidence under two policies, and the graph is the evidence. The digest of each policy is
  written to `out/trust.json` with the digest of the graph it was evaluated over.

## 4. Schema 2.1 (W2): the probes that must be rejected

The ten probes of `schema/selftest.py` stay. Added, frozen (target: at least 16 in all; 10 + 9 listed):

| # | Invalid graph | 
|---|---|
| P11 | `model-asserted` evidence whose `by` is `human:` |
| P12 | `human-asserted` evidence whose `by` is `model:` (a model attestation written as a person's) |
| P13 | `organisation-asserted` evidence whose `by` is `tool:` |
| P14 | an attestation evidence entry (`model-asserted`) with no `act` |
| P15 | an evidence entry with an act outside the table (`refereed`) |
| P16 | an agent with an unknown prefix (`robot:x`) as `on_behalf_of` |
| P17 | a rule verdict whose `unreviewed` names a piece that is not a node of the graph |
| P18 | a verdict with outcome `pass`, code `PROVED-FOR-ALL` and a non-empty `unreviewed` list |
| P19 | a piece node (`attrs.clausebook_entry`) whose stored attestation has a digest other than the node's identity |

Expected of the W2 run, frozen:

- the graph committed before this change (`out/graph.json` at `492bba6`, schema `rosette.refinement-graph/2`) validates
  against the 2.1 schema with no edit;
- 0 of the baseline's 120 verdict codes change;
- the 34 rule verdicts that are `pass` / `PROVED-FOR-ALL` in the baseline become outcome `review`, each with a non-empty
  `unreviewed`; no other outcome changes;
- counts against the design: the nodes of the graph more than double (baseline 940).

Narrowed from the study's table for 2.1, stated: the evidence kinds `specialist-asserted`, `externally-checked` and `assumed`,
the node kind `assumption` and the relation `assumes` belong to W4 and W8 and are NOT added by W2. Added by W2: the agent
prefix `org:`, the evidence kinds `model-asserted` and `organisation-asserted`, the evidence fields `act` and
`on_behalf_of`, and piece nodes.

## 5. The W3 test, frozen

Two policies over one tree. Tree: this worktree after one `./run.sh --quick`, with the attestation stores as committed.

| Policy | What it demands in strict mode |
|---|---|
| `trust/tests/person.yaml` | every piece and glossary entry a proved verdict rests on is `approved` by a person root |
| `trust/tests/open.yaml` | nothing about meaning (`strict.demands: [nothing-stale]`) |

Expected: under `person.yaml` strict fails for every `PROVED-*` scenario and rule verdict (baseline: 33 scenarios, 34 rules);
under `open.yaml` strict passes for all of them; `out/graph.json` is byte-identical between the two (all of it, `generated_at`
excepted, which is the clock); verdict codes identical. Counts against: evidence or a verdict code differs.

A second pair, in a scratch copy of the tree in which a fixture model (`model:selftest-fixture`) has attested every entry
`reviewed` through `clausal attest`: `trust/tests/person.yaml` against `trust/tests/model.yaml` (meaning requirements with
`kinds: [person, model]`, the fixture model a root). Expected: person fails all, model passes all with `MEANING-MODEL-ONLY`
on each; graph byte-identical between the two; in that graph every piece is still listed unreviewed.

## 6. Test 1 (signed intake on a toy verifier): rules, ledger entry, policy and controls

Frozen here as the study's section 5 states them. Test 1 is W6; nothing of it is built or run by W0 to W3. The files are in
`trust/test1/` and are read by nothing.

- `test1/rules.txt`: SM-1, 2, 3, 5, 8, 9 as written in `docs/studies/2026-11-12/packs.md` section 2b, and SM-10 written with
  `tied` / "the same input". None has been compiled.
- `test1/assumptions.yaml`: `A.sig.unforgeable` as in the study's section 1c.
- `test1/intake.policy.yaml`: the policy of section 1b.
- `test1/controls.yaml`: the seven controls.
