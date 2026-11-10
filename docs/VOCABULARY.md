# Composable vocabulary for behaviour: design note

How plain-English behavioural claims should be built from reusable, formally defined pieces. This records a design conversation between the owner and Claude on 2026-11-10, the decisions taken, and what is still open. Nothing here is implemented yet; the slice (`slice/`) currently binds whole phrases, not pieces.

## The problem

The slice's glossary has one entry per step phrase: "conserves the total" is a single opaque binding to one Lean definition. Every new sentence needs a new entry and a new human sign-off. That does not scale, and it puts the weakest link in the chain, the reading of the English, under the most load.

The aim is that most new sentences compile from pieces that already exist, so that trust grows with the size of the vocabulary and not with the number of sentences.

## The model

A sentence is assembled from three kinds of piece. Each has a type, so a composition either type-checks or is rejected.

| Kind | Examples | Becomes in Lean | Scope of reuse | Signed off |
|---|---|---|---|---|
| Domain word | account, account value, fund transfer | A type, a measure on states, an operation bound to the implementation | One system | Per project |
| Modifier | internal, aggregate, per-account, successful | A function from a piece to a piece of the same kind | Many systems | Once, shared |
| Logical frame | never changes, always, only if, at most once | A statement shape with holes for operations, measures and conditions | Every system | Once, shared |

**Granularity rule.** Split a phrase where a part would be reused with a different partner. "Aggregate" is its own piece because "aggregate fees" and "aggregate exposure" will follow. "Account value" stays atomic until something forces a split. When in doubt, start coarse and split on the second use.

## Worked example

> Internal fund transfers can never result in a change in aggregate account value.

| Phrase | Kind | Reading |
|---|---|---|
| fund transfer | Domain word (operation) | The ledger's `transfer`, bound to the Rust function |
| internal | Modifier on an operation | Restrict to transfers where both parties are accounts of this ledger |
| account value | Domain word (measure) | The balance of one account |
| aggregate | Modifier on a measure | Sum the measure over all accounts |
| can never result in a change in | Logical frame | For every starting state and every input, the measure afterwards equals the measure before |

Compiled reading: **internal(transfer) preserves aggregate(account value)**.

An illustrative sketch, not compiled:

```lean
-- Shared frame library (defined and signed once, for all projects)
/-- "op can never result in a change in m": for EVERY state and input, accepted or
    rejected, the operation returns and the measure is unchanged. -/
def NeverChanges (op : Operation σ α) (m : σ → Nat) : Prop :=
  ∀ s a, ∃ s', op.run s a = .returns s' ∧ m s' = m s

-- Shared modifiers
def aggregate (measure : Account → Nat) : Ledger → Nat :=
  fun l => (l.accounts.map measure).sum
def internal (op : Operation Ledger Transfer) : Operation Ledger Transfer :=
  op.restrict (fun l t => t.src ∈ l ∧ t.dst ∈ l)

-- Project glossary (signed per project)
--   "account value" ↦ Account.balance      "fund transfer" ↦ ledger.transfer

-- The sentence, compiled; no new definition, no new sign-off
theorem s1 : NeverChanges (internal ledger.transfer) (aggregate Account.balance)
```

A second sentence, "deposits always increase aggregate account value by the amount deposited", would reuse *aggregate* and *account value*, and add one frame.

## Decisions (owner, 2026-11-10)

1. **One frame library shared across projects.** Frames and generic modifiers are designed once, carefully, and reused. This is where reuse and single sign-off come from.
2. **Fail-closed defaults.** Common words get a default reading, and the default is the strict one. "Never" and "always" quantify over every input, including inputs the operation rejects and paths where it fails partway. A weaker reading must be asked for explicitly ("successful transfers never …").
3. **First audience: product-minded senior engineers.** A controlled grammar is acceptable to start. Moving to product and compliance authors is an explicit roadmap item, not an afterthought.
4. **Two modes of use.**
   - **Suggest.** A loosely worded or weak sentence is taken as a suggestion. The tool proposes one or more precise sentences it could mean, strongest first, and the author accepts or edits. Only accepted sentences are proved.
   - **Interpret.** A source that is already fixed, such as a signed contract in a PDF, is not rewritten. The tool produces a companion set of formal sentences stating how each clause will be interpreted, each traced to the clause it reads. The source stays authoritative; the companion is what gets signed off and proved.

## Handling ambiguity

English is ambiguous in the places that matter. In the worked example:

- **"Never"**: including rejected transfers? Covered by the default (yes).
- **"Change"**: compared before and after, or at every intermediate moment? Default: before and after one operation. Intermediate states need a different frame.
- **"Internal"**: who defines inside? A modifier whose definition is signed once.

Rule: the tool does not resolve an ambiguity silently. When a phrase has more than one formal reading, it finds a concrete input on which the readings give different answers and asks which was meant. The answer is recorded as a ruling. This is the same job the D1–D6 rulings do by hand in the TDFLite plan, and it extends the slice's existing "two readings" check from detecting disagreement to generating the question.

## Trust model

- A sentence's trust is the trust in its pieces plus the trust in the composition.
- Pieces are human-asserted and signed, with the signature void when the definition changes (already implemented for whole phrases in the slice).
- The composition is mechanical and type-checked. The human confirms only that the parse is the intended one; the tool echoes the compiled reading back in plain English for that purpose.
- An unbound word, an ill-typed composition or an unconfirmed ambiguity yields no statement. It never yields a guess.

## Roadmap

1. **Frames first.** A small catalogue (target: a dozen to start) with Lean definitions and an English paraphrase for each: never changes, always, only if, if-then, at most, at least, exactly once, rejected-and-unchanged.
2. **Recompile the existing scenarios.** Express the wallet and ledger scenarios through frames and modifiers; every existing verdict must be reproduced. This is the regression test for the design.
3. **Echo-back.** Print the compiled reading in English beside each sentence.
4. **Ambiguity questions.** Generate a distinguishing input for each pair of candidate readings.
5. **Suggest mode**, then **Interpret mode** on a real fixed document.
6. **Looser input** for product and compliance authors, with echo-back as the safeguard.

Implementation is queued behind the loops experiment, which is still changing `slice/`.

## Open questions

- Should frames be Lean definitions (as sketched) or generated statement templates? Definitions are auditable in one place; templates give flatter statements for proof automation.
- How are modifiers that change quantification ("each", "any", "some") typed so that scope is unambiguous?
- Time and sequences: "eventually", "until", "before" need frames over traces, not single operations. The slice supports one operation per scenario today.
- Two-run properties (secrecy, "reveals nothing about") do not fit a single-run frame.
- Is Gherkin's Given / When / Then the surface, or is a sentence form like the worked example better? The frame library does not depend on the answer.
- How large can the shared library get before authors cannot find the right frame? This is the navigation problem again.
- In Interpret mode, what happens when a clause has no faithful formal reading? Proposed: say so, list it as uninterpreted, never approximate silently.

## Related work to consult

Named from memory, not looked up for this note: compositional (Montague-style) semantics and Grammatical Framework for typed composition of meanings; Attempto Controlled English; the property specification patterns of Dwyer, Avrunin and Corbett (absence, universality, existence, response, precedence, with scopes); the EARS requirements syntax. A prior-art check like `out/prior_art.md` should be done before building the frame catalogue.
