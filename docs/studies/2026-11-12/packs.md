# Design study: Clausal packs

Read-only study; nothing was built, compiled or run. Paths are relative to `/Users/will/dev/lean-rosette`, and the directory was still `slice/` when I read it. Every "stateable today" below comes from reading the sentence forms in `slice/vocabulary.yaml`, not from compiling a sentence.

## 0. Position, as a trade

- **What a pack can be:** an authoring-time template plus a checklist. That fits the existing design with no change to the grammar or the frames.
- **What it should not be:** a semantic layer, an abstract interface that systems "implement", or a new verdict such as "conforms to pack".
- **Where the content actually sits:** the draft packs lean on a few project-supplied domain words ("the input is well-formed", "the signature verifies under the expected key"). The pack cannot check those words mean the right thing.
- **Stateability:** about two thirds of the draft sentences have a frame and a form today. The ones that do not are round trip, replay as a sequence, and a multi-condition progress rule, and those are the ones that make a suite complete rather than merely safe.
- **Naming collision:** `docs/PLAN.md:42,94` and `docs/HANDOFF.md:48` already say "ledger pack" for a Clausebook domain pack. Suggest "word pack" (Clausebook, supplies pieces) and "rule pack" (Clausal, supplies sentences) internally.

## 1. Definition and instantiation

| | Clausebook domain pack (words) | Clausal pack (rules) |
|---|---|---|
| Supplies | Domain words with Lean definitions and second readings | Rule lines with typed slots; no Lean definitions of meaning |
| Trusted | Yes, signed (`docs/ARCHITECTURE.md` §4, §8) | No; its output is ordinary sentences compiled like any other |
| Example | `clausebook/ledger`, `clausebook/abac` | "validated input", "signed message intake" |

A Clausal pack is a versioned directory with five parts:

1. **Slots.** Each has a Clausebook category from the list in `slice/vocabulary.yaml:22-40` (operation, `cond`, `term<num>`, `variation`, `reference`, and so on) and one line saying what the project's word must mean.
2. **Template rules.** Each is a canonical Rule line with `{slot}` holes and a stable id. A policy axis (for example unknown fields: reject, ignore or preserve) is a choice among whole sentences, never a parameter inside one.
3. **Applicability conditions.** Kernel-checkable facts about the bindings, for example that "well-formed" is both satisfiable and refutable.
4. **Adequacy expectations.** Named trivial implementations the instantiated suite must exclude, written as Lean lambdas in the manner of `trivial.extra` (`slice/glossary.yaml:130-141`).
5. **Lemmas and assumptions.** Lemmas over the abstract `Frames.Op` whose hypotheses are readings of pack rules, as `ExactlyWhen_iff` already is (`slice/lean/Frames/Lemmas.lean:80`), plus a list of named assumptions.

**Instantiation is text expansion at authoring time:**

- `clausal pack apply` substitutes each slot with the surface form of an existing piece of that category in the project's Clausebook.
- It writes the resulting Rule lines into the project's `.feature` file, tagged `@pack:validated-input@1 @pack-rule:VI-2`.
- The ordinary compiler then reads the file. A bad fill is refused as unbound, ill-typed or ambiguous like any hand-written sentence (`slice/DESIGN.md` §14.2).
- Bindings, chosen variants and waivers with reasons sit in a small file beside the feature.

**Invariants that keep meaning out of the pack:**

- Deleting the pack directory and stripping the tags changes no verdict.
- A pack adds no grammar and no synonyms (the track L rule, `docs/PLAN.md:78`).
- Tags drive only two informational outputs, in the style of the adequacy note (`slice/DESIGN.md` §13.3): a drift check (re-expand and compare text) and a completeness line.
- The completeness line always counts unstated members, for example "9 members: 6 stated, 1 waived (reason), 2 cannot be stated (piece missing)".

**What comes with each rule is mostly what exists already:**

- **Tests.** The property test and bounded check are generated from the compiled reading (`slice/DESIGN.md` §16). A pack adds nothing except seed inputs, and those belong with the format's word pack.
- **Adequacy.** Today's four kinds are built from listed result values (`slice/slicegen/adequacy.py:40-46`, `slice/DESIGN.md:1152-1165`). A parser's success value is structured, so pack-specific trivial models must be written out.
- **Proofs.** The proof that a given parser rejects malformed input is about that parser's code. The reusable part is small: derivations between rules.

## 2. Two draft packs

"Today" means a frame and a form exist and only project domain words are needed.

### 2a. Validated input

Slots: operation `{parse}` (role "the input"), cond `{well-formed}`, term "the length of the input", named value "the size limit", and for some rules a second operation `{encode}`.

| Id | Sentence | Today? | Missing or caveat |
|---|---|---|---|
| VI-1 | A parse always answers | Yes: `always_answers` (`vocabulary.yaml:695-700`) | Covers panic and non-return in the model only; stack depth and allocation are outside it. Already implied by every default-scope frame (`slice/lean/Frames/Core.lean:66-77`) |
| VI-2 | A parse is accepted only if the input is well-formed | Yes: `only_if` (`:771-776`) | All content is in the `well-formed` word |
| VI-3 | A parse is accepted whenever the input is well-formed | Yes: `if_then` (`:759-764`) | This is the progress rule that excludes reject-all. With a size limit it needs two conditions; see the conjunction note below |
| VI-4 | A parse is accepted only if the length of the input is not more than the size limit | Yes, modelled on `ledger_rules.feature:32` | Says oversize input is rejected. Cannot say the parser reads bounded bytes or uses bounded memory or time (`docs/ARCHITECTURE.md` §15, "Effects") |
| VI-5 | For a parse, the number of fields of the result is at most the field limit | Yes: `result_at_most` (`:858-862`) | — |
| VI-6 | A parse for which the input is not well-formed is rejected and changes nothing | Yes, same shape as `ledger_rules.feature:157` | Only meaningful for a parser with state |
| VI-7a | An encoding followed by a parse of its result gives back the value | **No** | `Op.andThen` takes independent inputs (`Core.lean:108-114`). Feeding one call's answer to the next is not among the three ties L2 names (`docs/PLAN.md:82`) |
| VI-7b | For a successful parse, the encoding of the result is the input | Workaround: `result_is` (`:847-851`) | Needs a domain word that hides a second call, as the E1 references do (`vocabulary.yaml:477-495`). True only of a parser that accepts canonical input only; a lenient one needs a spec-level canonical form |
| VI-8 reject | A parse is accepted only if every field of the input is a known field | Likely: `only_if` | "Field of the input" read before the call is a tokeniser inside the specification |
| VI-8 ignore | A parse gives the same answer when the input differs only in unknown fields | Yes: `same_answer` (`:959-965`) | Same dependence, in a variation word |
| VI-8 preserve | For a successful parse, every unknown field of the input is an extra field of the result | Yes: `covers` (`:985-989`) | — |
| VI-9 | A parse is accepted only if no key of the input is repeated | Workaround | `CountOf` has no sentence form (`slice/DESIGN.md:1376`); needs an item condition "is repeated" as a domain word |
| VI-10 | A parse agrees with the reference parse | Yes: `agrees_with` (`:947-952`) | Pins everything, but the reference is a full signed definition of the format: cheap for a path grammar, large for JSON |

- **Conjunction.** "A conjunction of two conditions" is a recorded missing piece (`trials/sentences/RESULTS.md`, pieces table). The workaround for two conditions is "A parse for which C1 is accepted whenever C2", using the grammar in `slice/DESIGN.md:1447-1450`.
- **Deliberately excluded.** "Same input, same answer" is true by construction, because `run` is a function (`Core.lean:42-52`). It would add a green line that says nothing.
- **Adequacy expectations.** The suite must exclude:
  - reject-all (by VI-3);
  - accept-all with a fixed value (by VI-2, given a witness that a malformed input exists);
  - accept well-formed but return a default value (only by VI-7 or VI-10);
  - a parser that drops a field (only by VI-7b or VI-10).
- **Consequence.** Without a round-trip or reference rule the suite is satisfied by a parser that returns the wrong value, and the only clean round-trip sentence is not stateable.
- **Adequacy gap.** The note is per operation (`slice/DESIGN.md:1323`), so a trivial parse and encode pair is not examined.

### 2b. Signed message intake

Slots: operation `{intake}` with state (expected key, last counter) and input (message), cond "the signature of the message verifies under the expected key", measure "the last counter", term "the counter of the message".

| Id | Sentence | Today? | Missing or caveat |
|---|---|---|---|
| SM-1 | An intake always answers | Yes | — |
| SM-2 | An intake is accepted only if the signature of the message verifies under the expected key | Yes: `only_if` | The provable content is control flow: no accepting path without the check returning true, on the key taken from state and not from the message |
| SM-3 | An intake for which the signature of the message does not verify under the expected key is rejected and changes nothing | Yes | "Nothing acted on" means state only. Sends, logs and I/O are outside one pure call (`docs/ARCHITECTURE.md` §15) |
| SM-4 | For a successful intake, the result is the reading of the signed bytes of the message | Yes: `result_is` | States that what is acted on is what was verified |
| SM-5 | An intake gives the same answer when only the unsigned part of the message differs | Yes: `same_answer` | Catches an unsigned header that influences the answer |
| SM-6 | Canonical form: either the payload parse is canonical-only (VI-7b), or "A parse gives the same answer when the canonical form of the input is the same" | Second: yes. First: workaround | As VI-7b |
| SM-7 | An intake is accepted only if the algorithm of the message is the expected algorithm | **No** | Equality of two values known before the call is L2's first missing piece (`docs/PLAN.md:82`) |
| SM-8 | An intake is accepted only if the counter of the message is more than the last counter | Likely | Not checked that "is more than" takes a measure read before the call |
| SM-9 | For a successful intake, the last counter is now the counter of the message | Yes: `becomes` (`:835-838`) | — |
| SM-10 | An accepted intake followed by the same message again is rejected | **No** | "The same input again" is L2's third piece. It follows from SM-8 and SM-9 as a pack lemma, but must not be printed as a rule until it has a sentence |
| SM-11 | An intake is accepted whenever the signature verifies, the counter is fresh and the payload is well-formed | **No** | Three conditions. Folding them into one word "admissible" hides the conjunction in an unsigned definition |
| SM-A | The holder of the key signed it | **Cannot be a frame** | See below |

**Unforgeability must be an assumption.** A frame quantifies over every state and input of one deterministic call, or two (`slice/lean/Frames/Frames.lean`, `Core.lean:66-94`). Unforgeability is a probability bound over adversaries that lack a key. "Every input" includes the input carrying a valid forgery, and on it the code correctly accepts. So the list must name three assumptions, each with evidence class "assumed":

- the scheme is unforgeable;
- the model of the library's verify function is faithful;
- the expected key is the right key.

An idealised variant is possible: put the set of issued messages in the state and say "accepted only if the message is an issued message". That is an ordinary `only_if`, but it is a theorem about the idealisation.

**A second gap follows from the first.** An external verify function is extracted as an axiom (`census/PROFILE.md` §5 shows this for `str` methods). The interpreter cannot evaluate an axiom, so:

- the adequacy search (`slice/lean/Run/Adequacy.lean`) cannot run the restated rules;
- the vacuity witness that a non-verifying message exists cannot be produced;
- the pack therefore needs an executable stand-in signature for the model side, and no such mechanism exists.

## 3. Relation to TDFLite intake

- **Where the defects are.** Four of the six known edge cases are in string intake by the plan's own classification (`docs/PLAN.md:328`); `private/tdflite-pilot/OWNER_SUMMARY.md:64` (private, not to be copied into a tracked file) counts five.
- **Where T9 looks.** T9 covers `tdf-core`, the integer decision logic (`docs/PLAN.md:105`). Intake is deferred to "its own node after it" (`docs/PLAN.md:337`), so a pack exercised on TDFLite needs a new intake node, not T9.

Mapping, using only `tdflite-ideas/TDFLite policy core formal verification plans.md`:

| Pack member | TDFLite intake | Ruling it forces into the open |
|---|---|---|
| VI-2 / VI-7b on "parse a label" | Trailing segment after the value is ignored | D1 variant: VI-7b is false on `.../SECRET/extra` with no TDFLite-specific sentence |
| VI-2 with "the namespace of the label is a namespace of the policy" | Namespace parsed, never compared | D1 |
| VI-8 (reject / ignore) on "every label of the resource resolves in the snapshot" | Unknown hierarchy value skipped; undefined value matched as text | D2, D3: today's code is the "ignore" variant, chosen by nobody |
| VI-8 ignore with variation "claim names differ only by case", or VI-10 against the reference engine | Case folded in one engine and one branch | D5, guarantee 8 |
| VI-9 | Several hierarchy levels in one claim | D4 at intake |
| SM-2, SM-8, SM-9 | Bundle acceptance: pinned anchor; (epoch, revision) never decreasing | Guarantee 7, step 8; needs an order on a pair |

- **The useful property.** The owner's rulings D1, D2, D3 and D5 are variant choices of one generic pack. That is the test of whether a pack would have surfaced them.
- **Provability.** `str` operations translate as axioms and the profile says to take bytes (`census/PROFILE.md` §5). So intake is provable through extraction only if written over `&[u8]`. Otherwise the first exercise is Route B (`docs/HANDOFF.md:51`) against the pilot's Lean model, which includes intake over strings (`private/tdflite-pilot/MODEL.md`).
- **Second, public target.** R2's candidate list includes "a version-parsing crate" (`docs/PLAN.md:104`). If chosen, it gives the pack two unrelated instantiations and keeps TDFLite out of the public fixture.

## 4. Risks

1. **Green and incomplete.** "9 of 9 proved" will be read as "input validation is verified", and it is not:
   - a `well-formed` word that is too weak makes VI-2 and VI-3 a matching pair that proves nothing;
   - the adequacy list is finite, and "none found" means none of those (`slice/DESIGN.md:1314-1316`);
   - on the toy ledger a known suite gap stayed open because the closing sentence could not be stated (`slice/DESIGN.md:1266-1271`), and VI-7a, SM-10 and SM-11 are in that position now;
   - parsers fail on large inputs, which every tested layer can miss (`docs/HANDOFF.md:23`, node E2).
2. **An instance only under a hypothesis it does not carry.** In the families study two members fit the primitive only with an extra hypothesis (`out/families/FAMILIES.md` §5.1-5.2). A streaming, lenient or stateful parser bound to this pack gives false or vacuous sentences unless applicability conditions are checked.
3. **Parameter explosion.** Validated input already has five axes (unknown fields, duplicates, canonical or lenient, size, state) and signed intake four. The families study found:
   - merged primitives carry more parameters than their members (Result 2);
   - statements grew 27% (Result 4);
   - six of seven families broke even, with one giving 99% of the net saving (Result 3);
   - the lightest form worked each time (§9, "On 'like a class'").
   
   The mitigations are: variants as whole sentences, no pack inheritance, a slot cap, and no pack before a second real use (`docs/ARCHITECTURE.md:126-128`).
4. **Little reusable proof.** The reusable lemmas are a handful of derivations. Per-system proofs stay per-system, at about 6 Lean lines per Rust line for loops (`p2/RESULTS.md` via `docs/HANDOFF.md:22`).
5. **Drift and versioning.** A template change leaves instantiated text stale. This is the same open question as versioning the frame library (`docs/ARCHITECTURE.md` §15).
6. **Smuggling through slot words.** A cond such as "admissible" moves the suite's content into one unsigned definition; 0 pieces are signed today (`docs/HANDOFF.md:19`).

## 5. Roadmap node

**K1 "rule pack: validated input"** (needs C1; L2 for VI-7a and SM-7; R1 for real code). Signed intake waits for K1's result and for a stand-in mechanism for opaque functions.

- **Freeze first.** Commit the template, slot list, variant list and a seeded bug list before any target code is read for this purpose. The seeded list:
  - trailing garbage accepted;
  - unknown item skipped;
  - duplicate key, last wins;
  - case mismatch;
  - length off by one;
  - default value returned.
- **Contamination.** This draft was written after reading D1 to D6, so TDFLite is a recall check only. The unbiased measurement is the second target, with sentences instantiated by an agent that has not seen this report's mapping table.
- **Step a.** A toy byte parser in the Rust profile, in a scratch copy.
- **Step b.** TDFLite label intake (Route B first) and R2's parse function, both with the same template.

| Test | Signal for | Result that counts against |
|---|---|---|
| Strip tags, delete the pack | Every verdict identical | Any verdict changes: the pack carries meaning |
| Reuse across two targets | Most template sentences instantiate with slot fills only | Fewer than half survive unedited on the second target; or more sentence text lives in per-project variants than in the template; or the second target adds more than two slots |
| Against a hand-written suite by an author blind to the pack, same target, same mutants | Pack suite shows more mutants false, or the same in less authoring time | No more mutants shown false and no difference in the adequacy note |
| Seeded bug list | Each seeded bug is shown false by a stated rule, or its rule is printed as unstated or waived | A seeded bug survives while the pack line reads complete. This is the main negative result |
| TDFLite recall | D1, D2, D3 and D5 behaviour refuted by pack sentences with the owner's variants | Any of the four needs a TDFLite-specific sentence |
| Stateability after L2 | At most a third of members still unstateable | More than a third; or a change to `clausebook/core` that only the pack uses |

## Not checked

- No sentence was compiled.
- `slice/slicegen/vocab.py` was not read, so the "likely" rows (SM-8, VI-8 reject, and whether a rule-line form exists for "rejected with a named error") are unverified.
- `slice/lean/Run/Adequacy.lean` was read only at its head; it is generated.
- `slice/slicegen/newrules.py` and `rules.py` were read at their headers only.
- The TDFLite Go source was not read; `private/tdflite-pilot/` was only searched for intake terms.
- The DeepMind Signal paper was not read.
- Whether the generator's "model target" mode (`docs/PLAN.md:329`) exists was not checked.
- The current state of the `slice/` to `clausal/` rename was not rechecked after reading.