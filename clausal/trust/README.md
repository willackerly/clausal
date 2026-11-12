# Who is trusted for what: attestation records, schema 2.1, trust policies (plan nodes W0 to W3)

Built from `docs/studies/2026-11-12/trust.md` and the owner's steer in `DECISIONS.md` ("Owner's steer on trust"). The formats,
the refusal lists and the expected outcomes were committed before the code (`FREEZE.md`, commit `09966fe`). This note says
what was built, where it departs from the study or the freeze, and what is not done.

**No person has signed anything.** The tree holds no record by a person. The only records in it are three by a model, about
its own authorship of the three policy files (`trust/<project>.attest.json`).

## What there is

| Piece | Where | What it does |
|---|---|---|
| Record format, refusals | `clausal/attest.py` | A record is {subject with its digest, act, signer with a kind, on-behalf-of, time, scope, signature: null}. `malformed` gives every reason a record is not one. Stores are sorted into valid, void (the subject changed since) and refused |
| Stores | `clausebook/<book>.attest.json`, `glossary.attest.json`, `trust/<project>.attest.json` | They replace `clausebook/<book>.signoff.json` and `glossary.signoff.json`. A file of the old format stops the load: it is neither read nor passed over |
| `clausal attest` | `clausal/report.py` (`cmd_attest`), `clausal/vreport.py` (`attest_entries`) | Writes one record per subject with the subject's digest as it is now. `clausal attest check` lists every record and what it counts for, and exits 1 on a refused record. `clausal review` is gone and says so |
| Schema 2.1 | `schema/refinement-graph.v2.1.schema.json`, `clausal/graphlint.py`, `schema/SCHEMA-2.1.md` | Every Clausebook entry a node; records as evidence under the signer's own kind; rule verdicts carry `unreviewed` |
| Trust policy, strict mode | `clausal/trust.py`, `trust/<project>.yaml`, key `trust:` in `projects.yaml` | Strict mode is computed from the finished graph and the policy. `clausal trust`, `clausal report --strict [--trust-policy F]`, `./run.sh --strict [--trust-policy=F]`; result in `out/trust.json` and in the report's section "Who is trusted for what" |
| Tests | `clausal/selftest.py`, `schema/selftest.py`, `trust/tests/two_policies.py`, `trust/tests/tampered_graph.py` | Below |

## The rules that no policy can change

1. **A signer's kind is read from its id** (`human:`, `model:`, `tool:`, `org:`) and must agree with the `kind` written. A bare
   name is not a signer: `clausal attest … --as "Some Name"` is refused and writes nothing.
2. **`on_behalf_of` records a delegation and changes nothing else.** A model's record on behalf of a person is a model's record.
3. **REVIEWED means a person.** An entry is reviewed iff a valid record of act `reviewed` or `approved` whose signer kind is
   `person` exists for its current digest (`attest.person_review`). That is what `unreviewed` in the graph, the outcome
   `review`, the report's "signed" counts and a separation being in force are about. A model's record of any act is kept,
   printed under `model-asserted`, and leaves the entry unreviewed.
4. **A requirement whose kinds are `[person]` is met only by a person's record.** A policy may list `model` for a requirement;
   then a verdict met by model records only is flagged `MEANING-MODEL-ONLY`.
5. **Counts are per kind and never summed.**
6. **The graph does not depend on the policy.** `clausal/report.py` builds `out/graph.json` without reading any policy; strict
   mode is evaluated afterwards, from the graph file.

A person's record carries no checked signature (signatures are plan node W9), so everywhere it is printed it reads
"claims to be; no signature is checked". An agent can type `human:<anyone>` today, exactly as it could type any name into
`--reviewer` before. Nothing here closes that; W9 is what does.

## What a record is of

- A Clausebook entry (`piece`, `separation`): the digest a sign-off covered (`vreport.piece_digest`: the entry's text, the text
  of each Lean definition it names, the defaults it names; for a separation also both pieces and what each sentence compiles
  to). The node `piece:<id>` of the graph has exactly that text as its interface, so its identity is this digest.
- An entry of the old glossary (`glossary-entry`): the phrase node's identity and the bound node's identity, as one digest.
- A policy (`policy`): the sha256 of the file.

## Measured (commands in the last section)

- **W1.** 18 malformed or misplaced records (the frozen R1 to R14, some in two variants) are each refused for the reason
  named; a record of a digest the entry no longer has is void. With every entry attested by a model, with and without a
  delegation to a person, no entry is reviewed. The sign-off self-tests that existed (coverage digest, the separation control
  with its seven cases, retired-form digest, grammar and defaults digest, storage per book) pass with records in place of
  sign-offs and their expectations unchanged.
- **W2.** The graph committed before this change validates under 2.1 unedited. Refusals in `schema/selftest.py`: 10 to 19 (the
  frozen P11 to P19, each for its reason), and 4 valid 2.1 shapes accepted. 0 of the baseline's verdict codes changed. 34 rule
  verdicts went from `pass` to `review`. Nodes 940 to 1171 (plus 24.6%), edges 1474 to 1619.
- **W3.** `trust/tests/two_policies.py`, 12 of 12 expectations. Tree as committed: `person.yaml` fails strict for 67 of 67
  proved verdicts (33 scenarios, 34 rules), `open.yaml` for 0; `out/graph.json` byte-identical (clock excepted). Scratch copy
  with a fixture model having attested all 166 entries: `person.yaml` still fails 67 of 67, `model.yaml` passes 67 of 67 with
  `MEANING-MODEL-ONLY` on each; graph byte-identical between the two; in it every proved verdict still lists its entries as
  unreviewed.
- **Strict mode under the three committed project policies fails all 67 proved verdicts**, and says why: the one root, the
  owner, is awaited. That is the state of the tree, not a regression: `--strict` failed before too (nothing was signed).

## Fix round 1 (after review; frozen in `FREEZE-fix1.md` before the code)

**The defect.** Strict mode reads the attestations stored on graph nodes (`attrs.attestations`), and believed the `kind`
written there. Nothing compared it with the signer id `by`: schema 2.1 ties kind to prefix on edge evidence only, the lint
compared digests only, and the built-in policy's root `human:*` did not look at `by` at all. A graph edited by hand to say
`{kind: person, by: model:selftest-fixture, act: approved}` on every entry was `valid` and passed strict mode under the
built-in policy, 67 of 67. No record could get there (records are checked when the stores are read); an edited
`out/graph.json` or a file given with `--graph` could.

**What changed.**

- `clausal/graphlint.py`: every stored attestation, on every node, must be by a signer id whose kind is the `kind` written
  (and `evidence_kind`, act and `on_behalf_of` are checked: `stored_attestation_errors`). A proved verdict must list every
  entry it rests on that stores no person's `reviewed` or `approved`, so `pass` with an empty `unreviewed` is refused too.
- `clausal/trust.py`: `Policy.admitted` admits no record whose written kind is not the kind of its `by` (under any policy,
  the built-in one included); `clausal trust` validates the graph it reads (schema and lint) and exits 2, computing nothing,
  if it is not valid.
- `schema/selftest.py`: P20 to P27. `trust/tests/tampered_graph.py`: T1 to T7 of the freeze and one more.

**A fault of this round, found by its own control.** The first version of the new lint compared a stored record's digest
with the node's identity on every node. An old-glossary phrase node's identity is the phrase, and its records name the
digest of the Lean definition it binds, so a tree in which a person HAD approved every glossary entry was refused as
"rests on phrase:…, which no person has reviewed". Control c10 (every entry approved by the fixture person, strict passes)
came back NOT AS EXPECTED in the first mutation run; that run was stopped, the comparison was limited to Clausebook entry
nodes (`graphlint.person_reviewed`), and the complete run was started again from fresh scratch copies. The must-accept case
is now in `tests/tampered_graph.py`.

**The complete mutation record was rerun** (`python3 mutation/run_mutants.py --jobs 4`, 1 h 45 min under load): see "Not done".

**Still true, and not closed by this.** The graph file is not signed and is not recomputed from the stores by `clausal trust`:
a hand-edited graph that is well-formed and says `{kind: person, by: human:someone, act: approved}` on every entry, with
the verdicts' `unreviewed` emptied to match, is a valid graph and passes strict mode under any policy that admits
`human:someone` (the built-in one admits any `human:` id). That is the same hole as typing `human:<anyone>` into
`clausal attest`: a person's record is an unchecked claim until W9. `clausal report --strict` and `./run.sh --strict` do
not have the graph-edit route: they build the graph from the stores in the same process.

## Departures from the study, each a judgement call

| # | What | Why |
|---|---|---|
| 1 | Subject kind `glossary-entry`, store `glossary.attest.json` | The task replaces both sign-off files; the old glossary's entries are not Clausebook pieces |
| 2 | Act `refereed` is not an act | It belongs to curated sets, which the study says not to build yet |
| 3 | A model's `tested` record is `model-asserted` with `act: tested`, not the evidence kind `tested` | So a model saying it tested something is never read as a tool's run |
| 4 | The policy's sha256 is not written into the graph (`runs[].config.trust_policy`); it is in `out/trust.json` beside the digest of the graph it was evaluated over | "Identical evidence under two policies" is then true of the whole graph file, byte for byte |
| 5 | `unreviewed` and the outcome `review` are fixed in code as "no person", in every policy | Needed for 4, and it is the steer: a model's record is never counted as a person's |
| 6 | The three project policies name NO signer for the owner root (`signer: null`, printed AWAITED) | Which identity the owner signs as is the owner's to say; the study's example names one |
| 7 | Schema 2.1 adds only what W1 to W3 use; `specialist-asserted`, `externally-checked`, `assumed`, the node kind `assumption` and the relation `assumes` are left to W4 and W8 | Nothing would exercise them |
| 8 | A tool's record is not evidence on a `binds` edge (the freeze's table said kind `tested`); it is listed on the entry's node | Version 2 forbids `tested` on `binds` (English to Lean is never tested), and 2.1 keeps that. Found after the freeze, when the schema refused it |
| 9 | `signature` must be null, and a policy's `ssh_key` must be null | Nothing checks a signature yet; carrying one unchecked would read as verified |
| 10 | A project with no `trust:` key gets a built-in policy equal to the old strict mode | So an undeclared project is not silently lenient |
| 11 | Mutation controls c9, c10, c11, c26 were rewritten for the new command and messages; c10, c11, c26 attest as the fixture `human:selftest-fixture` and run strict under `trust/tests/person.yaml` | Their old texts named `clausal review` and the old strict messages; under the project policies no fixture identity is a root. Exit codes expected are unchanged |

## Not done

- **No signature is checked** (W9). Person records are typed strings.
- **No assumption ledger, no specialist term, no external proof** (W4, W8). A policy may state requirements about them; strict
  mode then fails closed ("cannot be evaluated by this build").
- **Test 1** (signed intake) is frozen in `test1/` and not built (W6). None of its sentences has been compiled.
- **The ranked "rests on" block** (W5) is not built; the per-Rule block still lists every piece.
- **Validity does not go through `graphlint.staleness`.** A helper that an entry's Lean definition calls, and that the entry does
  not name in `defs:`, can change without voiding a record (the study's section 2 hole; unchanged).
- **No edges from a reading to its entries** (see `schema/SCHEMA-2.1.md`).
- **`tested` records are not voided by a toolchain change** (the study's staleness table); `context.toolchain` is stored if given
  and compared with nothing.
- `min:` counts, key registries, curated sets: not built, and a policy that uses `min:` is refused.
- `docs/SCHEMA.md` still describes version 2 only.
- **The mutation record was rerun in full in fix round 1** (it had not been when W1 to W3 were committed: `projects.yaml`
  gained the `trust:` keys, which changed the specification digest the record is stamped with, and four controls were
  rewritten). `python3 mutation/run_mutants.py --jobs 4`: 45 of 45 mutants with a scenario shown false, 49 of 49 controls as
  expected, c9, c10, c11 and c26 among them; per mutant and per control the same answers as the record at `492bba6`. The
  record's digest is the tree's, so the report carries the `MUTANTS-…` flags again.

## Commands

    python3 -m clausal attest <id|all|glossary:<id>|glossary:all|policy:<project>> --act <act> --as <human:|model:|tool:|org:>ID --scope "…"
    python3 -m clausal attest check                       # every store; exit 1 on a refused record
    python3 -m clausal trust [--policy F] [--strict]      # strict mode from out/graph.json and the policies
    ./run.sh --strict [--trust-policy=trust/tests/person.yaml]
    python3 -m clausal.selftest                           # W1 refusals and kind mismatch, W3 policy rules (and everything else)
    python3 schema/selftest.py                            # 27 invalid graphs rejected, 4 valid 2.1 shapes accepted
    python3 trust/tests/tampered_graph.py                 # strict mode over a graph edited by hand (fix round 1); seconds, no pipeline run
    python3 trust/tests/two_policies.py                   # the W3 test, in a scratch copy; writes trust/tests/two_policies.result.json
    python3 trust/tests/strict_controls.py                # mutation controls c9, c10, c11, c26 alone (four quick runs in a scratch copy)
    python3 compare/against/verdicts.py <graph.json|rev>  # verdict codes against a baseline
