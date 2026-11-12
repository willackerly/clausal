# Clausebook split (plan node C1): the assignment, written before anything is moved

This file was committed before `clausal/clausebook.yaml` was touched. It assigns each of the 96 entries of the flat
book to `core`, to the `ledger` pack, or to a fixture's local book, with the reason. The split itself follows it; any
deviation found while building is listed at the end under "Changes made while building", never edited in above.

## Layout (chosen: `clausal/clausebook/`, not a directory at the repository root)

```
clausal/clausebook/
  project.yaml        the list of books this project loads, in order
  core.yaml           frames, modifiers, defaults, coverage lines: no fixture noun
  ledger.yaml         the ledger pack: accounting words general enough to reuse
  local/wallet.yaml   the wallet fixture's own words and operations
  local/ledger.yaml   the ledger fixture's own words and operations
  <book>.signoff.json sign-offs, one file beside each book (none exists today)
```

Reason for `clausal/clausebook/`: every path the pipeline reads is relative to `clausal/` (`pipeline.ROOT`),
`mutation/workcopy.sh` and the mutation harness copy `clausal/` and nothing above it, and `spec_digest` hashes files
under it. A directory at the repository root would be outside every scratch copy. Lean module names do not change:
`Frames.*` is core's Lean side, `Ledger.Pieces` (namespace `L`) serves both the pack and the ledger's local book,
`Wallet.Pieces` (namespace `W`) the wallet's local book.

## The rule used to assign a domain entry

An entry goes to the **ledger pack** only if all three hold:

- **P1** it says what an accounting state is or holds (balances, accounts, one balance), or what a transfer names
  (sender, receiver, amount), or it is a composition of such words and core pieces only;
- **P2** it is not tied to one operation (an operation entry, `for_op:`) nor to the type of one operation's answer
  (`answer:`);
- **P3** its meaning carries no policy or limit of this crate (which transfers are allowed, a machine maximum, how a
  batch stops).

Otherwise it is **local** to the fixture that defines it.

## Core (48 of the 53 entries the plan counts, plus the header sections)

- All 25 frames (`always_answers` … `same_answer_if`), unchanged.
- 23 of the 28 modifiers: `zero`, `is`, `not_more_than`, `more_than`, `exceeds`, `at_most_value`, `sum_within`,
  `sum_exceeds`, `not`, `aggregate`, `all_of`, `holds_of`, `every`, `the_first`, `no_such`, `some_of`, `given`,
  `rejected`, `successful`, `internal`, `and_then`, `beside`, `accepted`.
- `defaults:` (D1 to D10), `coverage:` (3 entries), `frames_without_surface:` (1 entry).

**Five modifiers leave core** (scout finding 4). Each is "a literal of type X read as a value", and X is a type the
fixtures define (`amount`, `index`, `balances` in `glossary.yaml`, `param_types`). A book that names them cannot load
without those types, so they cannot stay in a core that a third project loads alone:

| Entry | Goes to | Reason |
|---|---|---|
| `amount_value` | ledger pack | an amount of money read as a number; used by both fixtures |
| `amount_result` | ledger pack | an amount read as a value that may be absent; same literal type |
| `index_number` | ledger pack | an account number read as an account |
| `balances_value` | ledger pack | a written list of balances read as balances |
| `index_count` | ledger, local | no surface form; exists only for the local idiom `i.exactly_applied` |

So core holds 48 pieces, not 53. Their ids, text and Lean are unchanged, so every reading that uses them is unchanged.

**Other fixture dependence in core, and what is done about each:**

| Where | Dependence | Decision |
|---|---|---|
| `changes_only` (frame 3) | its holes are typed `parts<acct>` and `term<acct>`; `acct` is the ledger's sort | generalise the hole types to `<T>` (the Lean frame `Frames.ChangesOnly` is already polymorphic); if any reading or refusal changes, revert and state the dependence instead |
| `internal` (modifier) | reads `{member}` and `{parties}` from a per-operation `internal:` field; the echo "every account the … names is an account of the …" is a Python string | the piece says in the book that the operation supplies the two definitions and the echo; the Python string moves into the operation's `internal:` field (local book) |
| header `lean_imports`, `lean_files` | names `Wallet.Pieces`, `Ledger.Pieces` | each book lists its own; core lists `Frames.Lemmas` and the two `Frames` files only |
| header `literal_lean`, `type_echo` | all six types are fixture types | move to the book that owns the type (pack or local) |
| `vocab.py` `TYPES = [num, balances, optnum, acct, transfer]` | the sorts `<T>` ranges over are a Python list naming fixture sorts | each book declares its `sorts:`; core declares `num` only |
| `vocab.py` `Ctx.say`: "the transfer …", "the batch …" | two fixture type names in Python | a per-book list `introduced_by_kind:` in the book that owns the type |
| literal and actor types (`amount`, `ledger`, …) | defined in `glossary.yaml`, shared with the old glossary | stays there; each book states the types its holes need (`uses_types:`), core needs none |
| comments in the YAML | examples name wallets and ledgers | core's comments are rewritten without fixture nouns; entry text is not touched |

Not changed, and stated as remaining dependence in `clausebook/README.md`: the per-piece Rust readings
(`wallet-bdd/src/pieces.rs`, `evidence/src/typed.rs`, `evgen.py`) mix core and fixture pieces in one file; the
generated proof scripts name fixture lemmas (`L.mkBatch_val`, `Vocab.mkWallet` in `links.py`, `oblig.py`);
`rsearch.py` imports `Wallet.Vocab` and `Ledger.Vocab`.

## Ledger pack (16 entries)

| Entry | Kind | Reason |
|---|---|---|
| `l.ledger` | measure | P1: the balances of a ledger, account by account |
| `l.balances_of` | collection of numbers | P1: the balances to be totalled; what conservation rules are stated over |
| `l.bal_of` | measure | P1: the balance of one account (0 if absent) |
| `l.balance_at` | value | P1: the balance of one account, absent if there is no such account |
| `l.accounts` | parts | P1: the accounts of a ledger; what "changes only" ranges over |
| `l.is_account` | condition | P1: an account number exists |
| `l.the_transfer` | item | P1: names one transfer |
| `l.sender`, `l.receiver`, `l.amount_of` | values | P1: what a transfer names |
| `i.holds` | idiom | composition of `is` (core) and `l.ledger` (pack) only |
| `i.moved` | idiom | the conservation statement itself: `decreases_by`, `increases_by`, `changes_only` (core) over `l.bal_of`, `l.sender`, `l.receiver`, `l.amount_of`, `l.accounts` (pack) |
| `amount_value`, `amount_result`, `index_number`, `balances_value` | modifiers | literal readings of the pack's value types (see Core above) |

**Stated limit.** The pack is a pack in the book only. Its Lean definitions are the ledger fixture's
(`lean/Ledger/Pieces.lean`, namespace `L`) and are stated on the generated types `ledger.Ledger` and
`ledger.Transfer`; its literal and actor types are the fixture's (`glossary.yaml`). A second crate cannot use it
until those definitions are stated over an interface. That is not built here.

## Local: ledger fixture (25 entries)

| Entry | Reason |
|---|---|
| operations `l.apply_batch`, `l.apply_all`, `l.apply`, `l.total`, `l.lookup` | P2: each is bound to one function of this crate's model |
| `l.valid` | P3: this crate's policy (accounts must differ, the receiver stays within 2^64 − 1) |
| `l.maximum` | P3: the machine limit of this crate's `total` |
| `l.transfers`, `l.length` | P2: read off the batch, the input type of two of this crate's operations |
| `l.applied`, `l.stopped_at` | P2: read off the answer of `apply_batch` |
| `l.result`, `l.found` | P2: answer words of the operations answering `Option U64` |
| `l.accepted` | P2: answer word of the operations answering `Bool` |
| `l.smaller_amount`, `l.larger_amount`, `l.only_amount_differs`, `l.agrees_at_account`, `l.extended` | P2: variations of one operation (`for_op`) |
| `l.ref_lookup`, `l.ref_lookup_zero`, `l.ref_whole_by_batch`, `l.ref_batch_by_transfers` | P2: reference functions of one operation (`for_op`) |
| `i.exactly_applied` | P2: an idiom over `l.applied` |
| `index_count` | used only by `i.exactly_applied` |

## Local: wallet fixture (7 entries)

| Entry | Reason |
|---|---|
| operations `w.transfer`, `w.deposit`, `w.withdraw` | P2: each is bound to one function of this crate's model |
| `w.balance` | not P1 as stated: a wallet is one balance, not a state of accounts; its Lean is on `wallet.Wallet` |
| `w.maximum` | P3: the machine limit of a wallet |
| `w.succeeds`, `w.rejected_with` | P2: answer words of this crate's `Result<(), WalletError>` |

The wallet's sentences use two pack entries (`amount_value`, and through the shared literal type, `amount_result`),
so the wallet project loads the ledger pack. That is the only reuse the split shows today.

## Checks the split has to pass

1. Every entry's sign-off digest (entry text plus the Lean definitions it names) is the same before and after the
   move, except `changes_only` and the operations whose `internal:` field gains the echo.
2. Every compiled reading of `features/` and `controls/` is the same text (Lean, echo, pieces used).
3. `core.yaml` loads alone, with no glossary, and contains none of the fixtures' nouns; `lean/Frames` builds alone.
4. One full `./run.sh`: every scenario, rule-group and function verdict code equal to the baseline.

## Changes made while building

**At the split (C1):**

- Nothing in the assignment above changed: 48 pieces in core, 16 entries in the ledger pack, 25 in the ledger's local
  book, 7 in the wallet's.
- `changes_only` was generalised to `<T>` as planned. No compiled reading, refusal or echo of `features/` or
  `controls/` changed (`python3 compare/against/readings.py dc38b56`: 0 differ), so it stays.
- Check 1 result (`PYTHONPATH=. python3 clausebook/split-check/digests.py` at the split commit): of 99 digests, 2
  differ, `changes_only` and `l.apply`, the two named in advance.
- The sort `transfer` is declared by the pack, not by the ledger's local book as the table above implies: the pack's
  own entries (`l.the_transfer`, an `item<transfer>`) need it.
- Three comments in `lean/Frames/Core.lean` and `lean/Frames/Narrowing.lean` named wallets, ledgers and transfers as
  examples. They were reworded so that the frame library's files contain no fixture noun; no definition changed.
- Book order in `project.yaml` is core, ledger pack, ledger local, wallet local. The operations are therefore listed
  ledger first where they used to be wallet first; the only generated file this reorders is `lean/Run/Narrowing.lean`
  (the numbering of its `fact_N` theorems).
- Not kept: the comment that listed the seven retired idioms (it is in the history of `clausebook.yaml`).

## Added by plan node L2 (2026-11-12), after the split

Four entries, all in **core**. Rule used: an entry is core if its form, its Lean text and its echo name no word, sort
or type of any one project, and `core.yaml` still loads alone and `lean/Frames` still builds alone with it
(`python3 -m clausal book check --lean`). The ledger pack and the local books are unchanged.

| Entry | Kind | Why core |
|---|---|---|
| `equals` | modifier, condition | equality of two values known before the call, on any one sort (`term<T>`); Lean `=`. Which values exist is the packs' business (`l.sender`, `l.amount_of`, `zero`, a literal) |
| `each_at_most` | frame 17 | a bound on every number of a `nums` collection, the category "the total of" already sums; Lean `Frames.EachAtMost`. The collections are the packs' (`l.balances_of`) or core's (`all_of`) |
| `tied` | modifier on the operation | derives the second input of a two-call sequence from the first; Lean `Frames.Op.tied`, stated for any operation |
| `same_input` | modifier, the new category `tie` | the identity tie; needs the two operations to take the same input type and nothing else. A tie that is about one project's inputs ("the transfer reversed") would go to a pack or a local book; none is built |
