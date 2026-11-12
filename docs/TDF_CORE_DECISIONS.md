# `tdf-core`: fourteen decisions for the owner

Self-contained. You should not need to open another file to answer. The numbering (O1–O14) matches `docs/studies/2026-11-12/tdf-core.md`.

**How to answer:** reply with the numbers you want changed, for example "O7: use the caller's identity; O13: cgo; rest stand". Anything you do not mention stays at its default. Every default is a parameter or a set of test vectors, so changing one means a re-run, not a rewrite.

**If you only have ten minutes:** read O4, O6, O7 and O12. Those are the four where a different answer changes what gets built. The rest confirm choices that follow from rulings you already made.

## Background you need

**What `tdf-core` is.** A small Rust crate that decides whether a key may be released. It takes a compiled policy and a request, and returns: is the subject entitled, should the key be released, and which obligations apply. It is written so it can be translated to Lean and proved.

**What is proved so far.** The Rust decision always returns, and equals a written specification, when policy and request are already numeric IDs. The step from the strings a caller sends to those IDs ("intake") is built and tested but only partly proved.

**The example policy** used below, in namespace `defense.local`:

| Attribute | Rule | Values | Meaning |
|---|---|---|---|
| `classification` | hierarchy | TOP_SECRET > SECRET > CONFIDENTIAL > UNCLASSIFIED | Subject's level must be at or above the object's |
| `releasability` | anyOf | USA, FVEY | Subject must hold at least one of the object's values |
| `need` | allOf | A, B | Subject must hold every one of the object's values |

An object carries labels such as `https://defense.local/attr/classification/value/SECRET`. A subject carries claims such as `classification: [SECRET]`.

**The eight guarantees**, in plain language:

1. Deny is the default; nothing releases a key by accident.
2. Only values defined in the signed policy can grant access.
3. Each rule means what its name says (hierarchy, allOf, anyOf).
4. Giving a subject more entitlements never takes access away.
5. Obligations are enforced: a key is released only if the client declared it can fulfil every required one.
6. A denied request learns nothing about the key.
7. Only verified, current policy decides (no rollback to an older bundle).
8. The fast engine and the readable specification always agree.

**What you already ruled on 2026-11-10** (you took all the recommendations, and asked for fail-closed choices):

- **D1:** deny a label outside the policy's namespace, or with extra segments after the value.
- **D2 / D3:** deny if any value bound to the object is not defined in the signed policy.
- **D4:** a hierarchy claim with more than one value is rejected.
- **D5:** claim names match regardless of capitalisation.
- **D6:** an object with no labels is permitted by an explicit rule, and a signed setting may deny instead.
- **R8:** refuse a policy whose names contain `/` or differ only by case.
- **R10:** obligation triggers scoped to a client are consulted; if the client is unknown, every such trigger is treated as applying.

## The decisions

### O1. Is a subject holding `[SECRET, MARS]` treated as having no classification level?

- **Context:** D4 says a hierarchy claim must have exactly one value. `MARS` is not a level the policy defines.
- **Default: yes, no level.** The subject is denied anything that needs a classification.
- **The other choice:** ignore `MARS` and treat the subject as SECRET. That grants access the default denies.
- **Today's Go** permits this case.
- **If you change it:** one test vector flips; the intake rule changes.
- **Recommendation:** keep. It is the fail-closed reading, and you were not shown this case when you ruled on D4.

### O2. What should guarantee 4 ("more entitlements never remove access") actually promise?

- **Context:** under D4, giving a subject a second classification value removes access, even a repeat of the same level. So guarantee 4 as originally worded is false by your own ruling. What does hold: extra `allOf`/`anyOf` values never remove access.
- **Default: state and prove two things.** (a) Extra `allOf`/`anyOf` values never remove access. (b) A subject with one higher level keeps access (replace SECRET with TOP_SECRET and nothing is lost).
- **The other choice:** only (a).
- **If you change it:** nothing is blocked; it decides what the access-control rule pack says.
- **Recommendation:** keep both. (b) is what most people think guarantee 4 means.

### O3. Three small readings under D1 and D4

- **Default, all three stand:**
  - The namespace in a label is compared ignoring case (`Defense.Local` matches `defense.local`).
  - A repeated identical level (`[SECRET, SECRET]`) counts as two values, so the subject has no level.
  - "Rejected" under D4 means the subject has no level for that attribute. The token as a whole is not refused; other attributes are still evaluated.
- **If you change one:** one or two test vectors flip.
- **Recommendation:** keep. The second is strict, but it is the simplest rule to state and audit.

### O4. Case folding in Rust: ASCII only, and anything non-ASCII fails closed?

This is the one to read carefully.

- **Context:** Go lowercases with full Unicode rules. The Rust that can be proved today works on bytes and has no modelled Unicode tables. A review found that a loose version of "ASCII only" fails open. Example: a policy with `rank: [high, low]`, and a token carrying both `rank: [high]` and a second claim named `ranK` written with the Kelvin sign (U+212A) holding `[low]`. Go folds the Kelvin sign to `k`, sees two values for `rank`, and gives the subject no level. A Rust intake that simply ignored the odd claim would see only `[high]` and release.
- **Default: ASCII only, and every non-ASCII byte withdraws access.** Precisely:
  - A non-ASCII character in any label on the object makes the whole object unresolved: deny.
  - A claim whose name contains a non-ASCII character withdraws every hierarchy level of the subject.
  - A non-ASCII value in a hierarchy claim still counts as a value, so it can only take a level away.
  - A policy with a non-ASCII value in a `read` obligation trigger is refused when loaded.
- **Effect:** the Rust never releases where the specification withholds (proved at the specification level, tested on 22,000 cases for the Rust). It does deny some requests the Go permits: any legitimate use of accented or non-Latin attribute names or values.
- **The other choice:** full Unicode folding in Rust, matching Go. That needs Unicode case tables inside the proved code, which is a large addition.
- **Question for you:** do any real policies or tokens use non-ASCII attribute names, values or claim names? If none do, the default costs nothing.
- **Recommendation:** keep, unless you know of non-ASCII use in the field.

### O5. Where does case folding happen?

- **Context:** your D5 ruling said fold case everywhere. Your own ADR-0028 says normalise once when input arrives.
- **Default: normalise once at intake.** A `strict_case` mode (refuse mixed-case input instead of folding it) is left as a later parameter.
- **If you change it:** the structure of the intake code changes; no verdict changes.
- **Recommendation:** keep. One place to fold is easier to prove and matches the ADR.

### O6. What does version 0 of the core cover?

- **Context:** the Go has several action types with their own rankings, and a list of subjects per request.
- **Default: the `read` action only, one subject, claims taken from the token.** Anything else is not offered by the core at all; it does not silently permit or deny it.
- **The other choice:** include other actions and multiple subjects now.
- **If you change it:** the core's types change, and the proofs done so far need extending.
- **Recommendation:** keep for now. With a Rust rewrite under investigation, say which actions and subject shapes the new service must support, and that becomes version 1.

### O7. Which client identity do obligation triggers use?

- **Context:** some obligations apply only to particular clients. R10 says that if the client is unknown, treat every such trigger as applying. The question is which identity counts: the caller's, or the enforcement point's. TDFLite's own decision log says the enforcement point's. Today's Go passes an empty client ID on this path.
- **Default: the core does not decide.** It takes one of three inputs: identity not established; known; or known but named by no trigger. The surrounding service chooses what to pass.
- **Consequence:** until the service passes a real identity, the core denies wherever a client-scoped trigger exists. That is correct under R10 but will look like extra denials in any side-by-side comparison with production.
- **Question for you:** which identity should the service pass?
- **Recommendation:** keep the core as is, and answer the question for the service.

### O8. Is the first value listed in a hierarchy the highest?

- **Default: yes.** `TOP_SECRET, SECRET, CONFIDENTIAL, UNCLASSIFIED` means TOP_SECRET is highest. Where an object carries several classification labels, the requirement is the highest of them.
- **If you change it:** one comparison reverses.
- **Recommendation:** confirm. Every model so far assumes it and nobody has said so explicitly.

### O9. Which translator: plain Aeneas or hax?

- **Context:** your original plan preferred hax, where contracts are written as attributes on the Rust. This project has exercised Aeneas (with five small patches), where the Rust is plain and the statements live in Lean.
- **Default: patched Aeneas.** The contracts are written as Clausal sentences. The Rust is kept in a shape that would let hax attributes be added later.
- **If you change it:** the proofs done so far (32 statements on the core) would be redone under hax.
- **Recommendation:** keep. It is working, and switching would cost the progress to date.

### O10. Where does the crate live?

- **Default: a local, unpublished git repository at `private/tdf-core/`** inside the Clausal checkout. The access-control rule pack is tracked in the Clausal repository.
- **The other choices:** a directory or branch in the TDFLite repository; or public in the Clausal repository.
- **If you change it:** a move; reversible until something is pushed.
- **Recommendation:** revisit now. If the Rust rewrite goes ahead, the crate belongs in the TDFLite repository as the decision core the new service depends on. Say which repository and branch.

### O11. What exactly does guarantee 6 ("a denied request learns nothing about the key") cover?

- **Context:** the service unwraps the data key before deciding, because the check that the policy is bound to the object is keyed by it. So a caller can already learn whether a wrapped key is valid here.
- **Default: the guarantee covers the response value only** (error code, obligation list, size). It does not cover timing or audit logs. It is stated as: given the same outcome of the binding check, a denied response is identical whatever the data key.
- **The other choice:** include timing, or treat "this wrapped key is valid here" as a leak to be closed.
- **If you change it:** the theorem statement changes. Timing is not something this method can prove.
- **Recommendation:** keep, and treat the binding-check leak as a design question for the rewrite.

### O12. Does key material enter the Rust core?

- **Context:** if unwrapping and re-encrypting stay in Go, a Rust "permit" type cannot constrain any Go code. The "no key without a permit" guarantee is then real only as far as Go honours it.
- **Default: no.** The core is generic over an opaque key type; cryptography stays in the surrounding service; the Go-side gate remains the enforcement.
- **The other choice:** key handling moves into Rust, so the permit type gates release in the same language as the proof.
- **If you change it:** guarantee 6 and the permit step become much stronger, and the Rust takes on key handling.
- **Recommendation:** this is the decision most affected by the Rust rewrite. If the service becomes Rust, change this to yes. If the service stays Go, keep the default and accept that guarantee 6 is weak.

### O13. How is the Rust core called from the service?

- **Default: compiled to WebAssembly and run under wazero** from Go, as your plan's step 7 says.
- **The other choice:** cgo. Or, if the service becomes Rust, an ordinary crate dependency and this question disappears.
- **If you change it:** only the hand-over step.
- **Recommendation:** leave until the rewrite investigation reports.

### O14. What does "enforced" mean in guarantee 5?

- **Default: "declared".** A key is released only if the client declared it can fulfil every required obligation. Whether the client really does (for example, really applies a watermark) is listed as an assumption in every report. Proof of capability is roadmapped as later work.
- **If you change it:** nothing in the core; it would open the deeper obligations work now.
- **Recommendation:** keep. This is your R10 ruling restated.

## Not for you to decide now

These belong to the surrounding service and do not affect the core:

- The refusal code when one call repeats an object ID, and which repeats count.
- What happens to an unlabelled object when a decider cannot report the D6 setting.
- Case folding in the authorisation service and the descope primitive.

## One correction to an earlier note

The handoff said there were "eight decisions" listed in the TDFLite pilot's notes. That section has eleven bullets, and which eight were meant could not be determined. This file replaces that reference.
