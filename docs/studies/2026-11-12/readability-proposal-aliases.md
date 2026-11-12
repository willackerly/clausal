# Proved aliases: proposal for more readable Clausal without a second meaning

Paths use the renamed tree (`clausal/`, `clausal/clausebook.yaml`, `clausal/clausal/`); the rename landed while I worked. Line numbers in `clausebook.yaml` and `vocab.py` were re-checked after it; `vreport.py` (only `:174` re-checked), the feature files, the Lean files and `Readings.lean` were read before it.

## 1. Findings that shape the design

1. **The owner's example is not a Clausal sentence.** The registered forms of the monotone frame are `never loses acceptance when {v:variation}` and `never loses that {c:class} when {v:variation}` (`clausal/clausebook.yaml:938`). "more-never-loses" in `README.md:67` is the frame's name used as a verb. No `abac` pack exists in `clausal/clausebook.yaml`, so none of the TDFLite rows in `README.md:66-69` compiles today.
2. **Putting "accepted" on the subject of that frame is vacuous.** A probe on a scratch copy compiled "A successful transfer never loses acceptance when the amount is larger" to `Frames.Monotone (L.apply).successful L.largerAmount …`. By `clausal/lean/Frames/Core.lean:87-88` the accepted branch already assumes the second call is accepted, so the claim is trivially true. The same rule without "successful" is marked `@expect-refuted` (`clausal/features/ledger_rules.feature:74-75`). The vacuity is my reading of the definition, not kernel-checked.
3. **Aliases already exist, unregistered and outside any sign-off.** The probe gave byte-identical Lean for each pair:
   - "Any transfer always succeeds" and "Every transfer is always accepted" (`clausal/clausal/vocab.py:37`, `:1009`).
   - "is never accepted" and "is always rejected" (`vocab.py:1010`).
   - "A rejected transfer never changes the ledger" and "For a transfer, if it is rejected, the ledger is unchanged" (`vocab.py:1015`, `:1049`).
   - `ledger_rules.feature:14` and `:29` (`clausal/lean/Wallet/Readings.lean:701`, `:706`), through "fund transfer" (`clausebook.yaml:172`), "the aggregate" (`:592`) and four forms of `l.balances_of` (`:255`).
   
   The sign-off digest hashes the YAML entry and the Lean definitions (`clausal/clausal/vreport.py:147-178`). Forms hard-coded in `vocab.py` are covered by no signature.
4. **One modifier has two stems.** `successful` is written "successful" before the noun (`vocab.py:1049`) but "if it is accepted," in a Then (`vocab.py:1015`), and echoed as "accepted calls only" (`clausebook.yaml:664`).
5. **Two meanings share one skeleton, separated only by hole type.**
   - `l.bal_of` and `l.balance_at` both read "the balance of account {…} of {l}" (`clausebook.yaml:267`, `:275`); one is 0 for a missing account, the other is absent.
   - `more_than` and `exceeds` both read "… is more than …" with the arguments reversed (`clausebook.yaml:551-562`).
   - ", if it is rejected" after a two-run frame is a condition on the first answer (`Readings.lean:766`); "if it is rejected, " before a claim is the scope modifier.
6. **One meaning already has two Lean terms.** `ledger_rules.feature:67` ("every … is not valid") is `Frames.EveryOf … (¬ valid)`, and `:166` ("no … is valid") is `Frames.NoneOf … valid` (`Readings.lean:726`, `:846`). Default D9 (`clausebook.yaml:83`) says these mean the same.
7. **There is no ambiguity check at registration.** `Vocabulary._check` (`vocab.py:170-185`) checks hole categories and idiom names only. Ambiguity is found per sentence at compile time (`vocab.py:589`, `:936`, `:1000`).
8. **There is no tree-to-sentence function.** I found none by grep in `clausal/clausal/`, so `clausal fmt` has nothing to build on. No sign-off file exists.

So the "one canonical sentence per meaning" rule is not true of the present book. The choice is between unregistered aliases and registered ones.

## 2. The mechanism

**What "proved" covers.** An alias has no `lean:` field. It parses to the same tree node as its piece, so the emitted term is the same text by construction and cannot drift. That the English words mean that term stays human-asserted, as for every form; no kernel proof can check it.

**Schema.** A separate `aliases:` section holds one entry per alias: `id`, `of` (piece id), `position`, `form`, `class`, `status` (live or deprecated). It sits outside the piece's entry so that adding an alias does not void the piece's sign-off under `vreport.py:147`. The hard-coded forms in `vocab.py:37`, `:1009-1010`, `:1015`, `:1049` move into the book.

**Admission classes (closed list).**

| Class | What it is | Meaning identical because |
|---|---|---|
| P, positional | The same piece in another syntactic position: before the noun, after the subject, fronted, Then-claim | Same node, same holes |
| G, grammatical | Genitive or "of", active or passive, of the same stem | Same node |
| D, domain name | A project's second noun for a domain word, in local bindings or a pack, never in core | Same node |
| C, composite | Today's idioms (`clausebook.yaml:1035-1050`) | The `means:` composition |
| E, equivalent term | Two existing Lean terms shown equal by a frame-level theorem for all operations and holes, axioms listed | Kernel theorem; `fmt` rewrites to the canonical term's sentence |
| X, deprecated | A former form; accepted with a warning; `fmt` rewrites it | Same node |

**Not admitted:** a second form for the same piece in the same position. That is the plan's "synonym" (`docs/PLAN.md:78`): sum/total, larger/more than, succeeds/accepted.

**Checks at registration (`clausal book check`); any failure refuses the alias.**
1. Holes are the piece's holes exactly: same names, same categories, none filled by a literal.
2. Holes may be reordered only if their categories are pairwise different, so a swap cannot type-check.
3. Position is unique: at most one live form per piece per position.
4. Reserved words (never, always, only if, exactly when, whenever, every, no, some, not, accepted, rejected, at most, at least) appear the same number of times as in the canonical form. Domain-word forms may contain none.
5. Homographs: no two forms of different pieces share a literal skeleton, unless a separating input is shown and the pair is signed as such.
6. Every existing `.feature` recompiles to the same term.
7. Bounded round trip: generate typed trees to a stated depth, linearise with every alias combination, and parse; each must yield exactly one tree, the original. CFG ambiguity is undecidable in general, so this is a bounded check. The guarantee stays the per-sentence refusal at compile time.

**Stored as written.** The compiler reads the alias form directly, so the text in the file is the text tested and proved; no second copy exists to drift.
- `clausal fmt` rewrites only deprecated and class E forms.
- `clausal fmt --canonical` prints the normal form, for comparing projects.
- A project may set `style: canonical`, making any live alias a CI failure.

**Who signs.** The signer of the pack the alias lives in: the owner for core, the pack owner otherwise. The digest is the alias text, its position and the piece's digest, so changing the piece voids its aliases. An alias cannot be signed before its piece. In strict mode an unsigned alias counts as an unsigned piece.

**Report.** The rule is shown as written. Beneath it, when different: "Normal form: …" marked as generated, then "Aliases used: id, class, signer, date". Verdicts are keyed on the term, so two rules with one term (`ledger_rules.feature:14` and `:29`) are listed as duplicates.

**What stops sprawl.**
- The closed class list and the one-form-per-position rule.
- A frozen cap of 12 live core aliases in the first signed edition; raising it is an owner decision logged in `DECISIONS.md`.
- A new core alias needs the "helped" result in section 5.
- Each alias costs a signature and trial items.

**Answer to the earlier rule's reasons (`docs/PLAN.md:41`).**
- Inconsistency across projects: bounded by one form per position, `fmt --canonical` and the style switch.
- Ambiguity: checks 5 to 7 at registration, where today there are none.
- Authors who have not seen the vocabulary: conceded. Aliases are for readers; `clausal compose` stays the answer for authors.

## 3. The ten sentences

The TDFLite words (operation "key release", variations, `satisfies under its rule`) are assumed `clausebook/abac` entries that do not exist. Rows 1 to 3 are designs, not compiled.

| # | Source | Under the mechanism | Lean term, and why unchanged |
|---|---|---|---|
| 1 | `README.md:67` | Canonical: "A key release never loses acceptance when the subject gains an entitlement." P alias: "When the subject gains an entitlement, a key release never loses acceptance." | `Frames.Monotone release gainsEntitlement (accepted)`. Same `monotone` node, two holes of different categories. |
| 2 | `README.md:68` | Canonical: "A key release gives the same answer when only the order of the attributes differs." P alias: "When only the order of the attributes differs, a key release gives the same answer." | `Frames.IndependentOf release reordered (fun ans _ => ans)` (`clausebook.yaml:959-972`). Same node. |
| 3 | `README.md:66` | Canonical: "A key release is accepted only if every attribute of the data is satisfied by the subject under its rule." G alias: "… only if the subject satisfies every attribute of the data under its rule." | `Frames.OnlyIf release accepted (Frames.every attrs satisfied)`. Same `only_if`, `every` and item-predicate nodes. |
| 4 | Two-run, `ledger_rules.feature:98` | "A transfer, if it is rejected, gives the same answer when the amount is larger." (P) | `Frames.IndependentGiven L.apply L.largerAmount (¬ L.said ans) …` (`Readings.lean:766`). Same node. |
| 5 | Narrowed to rejected, `ledger.feature:238`, first clause | "If a batch applied as a whole is rejected, it never changes the ledger." (P, same stem) | `Frames.NeverChanges (L.applyAll).rejected …`, by the template the probe showed for `L.apply`. |
| 6 | Nested condition, `ledger_rules.feature:115` | "Given that some transfer of the batch is not valid on the ledger, a batch applied as a whole is always rejected." (P for `given`) | `Frames.Never ((L.applyAll).given (someOf … ¬ valid)) accepted` (`Readings.lean:791`). Same `given` node and condition tree. |
| 7 | `only_if`, `ledger_rules.feature:32` | "A transfer is accepted only if the amount of the transfer is not more than the balance of the transfer's sender in the ledger." (G on `l.sender` and `l.bal_of`) | `Frames.OnlyIf L.apply accepted (amountOf inp ≤ bal st (sender inp))` (`Readings.lean:711`). Same five nodes. |
| 8 | `wallet.feature:75` | "A withdrawal always answers, and an accepted withdrawal decreases the wallet's balance by exactly the amount, and a rejected withdrawal never changes the wallet's balance." ("successful" becomes X) | Unchanged conjunction (`Readings.lean:629-631`); the `successful` node gets one stem. |
| 9 | `agrees_with`, `ledger_rules.feature:123` | "A batch applied as a whole agrees with the all-or-nothing replay of the batch." (D) | `Frames.AgreesWith L.applyAll L.refWholeByBatch` (`Readings.lean:796`). Same reference node. |
| 10 | `ledger_rules.feature:67` | "For a batch, no transfer at which the batch stopped is valid on the ledger afterwards." (E; this is `:166` verbatim) | The term changes from `EveryOf … ¬valid` to `NoneOf … valid`. It needs a theorem that the two are equivalent for every operation; both unfold to the same body (`Frames.lean:125-133`). Not compiled. |

Notes on the rows:
- **Row 1.** The gain comes from using the real frame form and a well-worded variation, not from the alias. Any form beginning "An accepted key release …" is refused by check 4, because of finding 2. Guarantee 4 is recorded as not holding today (`tdflite-ideas/TDFLite policy core formal verification plans.md:63`), so the rule would be refuted on the present code whatever its wording.
- **Row 2.** The README labels this `never changes`, but that frame compares one measure before and after a single call (`clausal/lean/Frames/Frames.lean:26-29`). Order-independence is the two-run frame. An alias "never changes the answer when …" is refused: it starts with another frame's head.
- **Row 3.** The active form is not registered under negation, where English is scope-ambiguous (default D9). The bare "Key release" stays refused.
- **Row 7.** The form "the balance of {k} in {l}" collides with the second form of `l.balance_at` (`clausebook.yaml:275`). Check 5 refuses it until that existing pair is resolved.
- **Row 9.** The current reference form contains "only if" and "every" (`clausebook.yaml:485`), which check 4 forbids in a domain word. The shorter name moves the meaning into the definition, so the report must print the definition beneath the rule.

**The 48 frozen sentences.** I read the sentence list in `trials/sentences/authors.json` and `trials/sentences/RESULTS.md`. No alias above was chosen to make one of them compile; each follows from the class rules or from a defect in section 1. One overlap: unifying "successful" and "accepted" (row 8) is justified by finding 4, but would also move some of the 48, such as the 4-word case at `RESULTS.md:49`. Any change in L4(a) from it must be reported as contaminated, not as evidence for aliases.

## 4. What could go wrong

- **A natural alias can be vacuous or mean another frame** (findings 2 and 5). The checks catch reserved words and shared skeletons; they do not catch an alias that merely suggests a different meaning to a reader.
- **Check 7 is bounded.** An alias can make a deeper sentence ambiguous. That sentence is then refused, not misread.
- **Two styles can coexist in one file** unless the project sets `style: canonical`.
- **Fronted forms need a third clause shape.** `vocab.py:952-966` has two; each shape multiplies the cuts tried, and ambiguity counts will rise.
- **Class E adds trusted-looking theorems.** The axiom list must be printed. Contrapositive pairs would need classical logic; I recommend against admitting them.
- **Moving hard-coded forms into the book changes digests.** With nothing signed today this costs nothing; after H1 it would void signatures, so do it before H1.
- **Short domain names hide content** (row 9).
- **The mechanism may add little.** Rows 1 to 3 improve mainly by using the real frames and better domain wording.

## 5. Measuring whether it helped

Build a new bank `trials/meaning/banks/alias-v1/` on the pattern of `banks/generated-echoes-v1/make_bank.py`. Scoring is unchanged: `score.py` already splits by part kind (`trials/meaning/score.py:320-350`).

- **Items.** `first` is a Rule in one arm's form (parts "canonical" and "alias"). `second` is one concrete call with a stated verdict, "breaks the rule" or "does not". The true verdict comes from the executable reading in `clausal/lean/Frames/Check.lean`. Half the stated verdicts are flipped by a seeded rule; "faithful" means the stated verdict is right.
- **Trap kinds.** A rejected call; a call outside the stated condition; a boundary value; the second run of a two-run rule; a rule narrowed to accepted or rejected calls. At least eight trees per kind per arm, as in `docs/PLAN.md:96`.
- **Counterbalance.** Two reader kits; each tree is canonical in one and alias in the other; a reader takes one kit.
- **Readers.** At least four model readers from two families, labelled proxy; the owner and two others in their own column.
- **Frozen before the run.** The alias list, the seed, the tree selection rule, the case generator and these thresholds:
  - **Hurt:** the alias arm's catch rate on flipped items is lower by more than 5 points pooled, or by more than 10 points on any one trap kind.
  - **Helped:** not hurt; the alias arm's error rate is at most 0.75 times the canonical arm's; and the interval for the difference, resampling items and readers, excludes zero.
  - **No measurable difference:** anything else.
  - For people only: median seconds per item not more than 20% higher.
- **Use of the result.** A new core alias is recommended only on "helped". Existing positional forms stay on "no measurable difference". "Hurt" withdraws the alias. The owner decides.

**Expected limit.** Proxy readers already catch about 92% (`RESULTS.md:81`). With about 160 judgements per arm, this trial will probably return "no measurable difference" for most aliases. It has power only on the two kinds proxies missed (narrowed calls 10 of 12, dropped conditions 9 of 12; `RESULTS.md:92-93`) and with people.

## 6. Cost to build

These are estimates, not measurements, in agent-days including a second-model review.

| Piece | Days |
|---|---|
| Schema, and moving existing forms out of `vocab.py` | 1 |
| `clausal book check` (checks 1 to 7) | 2 |
| Linearizer and `clausal fmt` | 2 |
| Fronted clause shape | 1 |
| Report and sign-off changes | 1 |
| Lean file for class E theorems with axiom audit (one `lake build`) | 0.5 to 1 |
| Trial bank and proxy run | 1 to 2 |

- **Total:** about 8 to 10 days.
- **Owner time:** a signature per alias, and about 80 trial items.
- **Order:** after C1, because aliases need the core and local split, and before H1.

## 7. Not checked

- **Nothing was built in Lean.** The vacuity in finding 2 and the equivalence in row 10 are readings of the definitions.
- **The pipeline was not run.** The probe is `/private/tmp/claude-501/-Users-will-dev-lean-rosette/5dc3e5ea-13c5-4c6a-8f82-442d3e8f83b7/scratchpad/proved-aliases/probe/run.py` with `p.feature` beside it. It ran against a copy of the compiler taken mid-rename, with `clausebook.yaml` copied to the old file name.
- **Report duplicates.** I checked only the two table rows at `clausal/out/report.md:38-39` for whether the report flags duplicate terms.
- **Not read:** `trials/sentences/raw/`, and the keys, responses and full reports under `trials/meaning/`; `private/`.
- **Partly read:** `docs/HANDOFF_CLAUSAL.md` and `out/prior_art_vocabulary.md` past line 60 were only searched; `wallet.feature` and `ledger.feature` only by their Rule lines.
- **Prior art.** ACE and Grammatical Framework are listed as unopened in `out/prior_art_vocabulary.md:337`. I did not look them up, so no claim here rests on them.
- **Equivalences not verified.** Whether `L.said` and `(L.apply).accepted` coincide (row 4), and whether "is always rejected" stays equivalent to "is never accepted" for an operation with more than two answer kinds beyond what `Frames.lean:46-49` states.
- **Privacy.** Row 1's note and the wording of guarantee 4 draw on `tdflite-ideas/`. Check the privacy rule in `AGENTS.md` before copying them into a tracked file.