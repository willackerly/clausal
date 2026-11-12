# TDFLite policy core: formal verification plan

Nov 9, 2026 · @Will Ackerly

## Position

The decision that releases a data key in TDFLite is small, pure and already isolated, so it can be specified mathematically and machine-checked. This paper argues that it should be, and lays out how.

Today the claim behind a key release is "we tested it against a large corpus on several engines." The proposal upgrades that, for the decision core only, to "for every possible input, the function cannot do otherwise." Everything else in the platform (policy authoring, identity sources, admin surfaces) can stay under ordinary engineering discipline, because all of it funnels into this one decision.

The paper asks for three things:

1. **Six rulings.** The code review found six edge cases where today's behaviour is a side effect of implementation rather than a stated rule. Each is written out below as a concrete scenario with a suggested ruling. They can be resolved later, but nothing can be proven until they are.
2. **A first stage that touches no production code.** Write the policy model in Lean and use it as an independent oracle against the existing Go implementation. This stage stands on its own.
3. **A second stage, gated on the first.** Rewrite the decision core in Rust with machine-checked contracts (hax), and put it behind the existing decision seam.

Two things the code review changed about the plan:

- **The model is smaller than expected.** The live decision is a flat rule evaluation, not a boolean condition tree. That shrinks the proof.
- **The specification work comes first.** A proof is only as good as the statement being proven, and six parts of that statement are currently undecided.

## Why this codebase is ready

Four properties of TDFLite at commit `4aca7ca` make this practical. Most codebases have none of them.

| Property | Where it shows | Why it matters for proof |
| --- | --- | --- |
| The decision is a pure function | `pkg/pdp` owns no I/O, no mutable state and no clock; the caller supplies time | A pure function can be modelled exactly. There is no hidden state to abstract away. |
| All policy is signed | ADR-0012, the Signed-State Principle: the platform serves only from signed objects | The proof can start from "a verified bundle" and needs no model of a mutable database. |
| The decision runs on an immutable compiled snapshot | `pkg/pdp/snapshot`: values interned to integer IDs, swapped atomically on reload | The proven core works over integers and sets. That is the easy case for a prover. |
| There is a conformance corpus and a culture of differential testing | `tests/conformance`, replayed through several engines | The corpus is a ready-made bridge between a formal model and running code. |

One more point for architects: a named chokepoint already exists for key release (ADR-0016, KeyGate). The proof has a single place to attach.

## How a key release is decided today

Every key release follows one path of four stages, fed by a snapshot compiled from the signed bundle. The plan proves the stages where policy is interpreted and the key is let go, and treats authentication and cryptography as tested assumptions.

&#91;embedded content: key-release path · 4 stages, 2 outcomes, 1 policy input\]

Read it top to bottom: a request must pass stages 1 to 4 in order, and the snapshot on the right is the only source of policy that stages 3 and 4 consult.

The same path in the code, at commit `4aca7ca`:

1. **Before any request.** The signed bundle is verified and compiled by `snapshot.Compile` into an immutable structure: every attribute value becomes an integer ID, hierarchy levels become ranks. A reload swaps the whole snapshot atomically.
2. **Authenticate.** `internal/lite/kasauth` verifies the access token, the proof-of-possession and the signed request.
3. **Unwrap and check the binding.** `verifyRewrapRequests` in `internal/lite/kas/rewrap.go` unwraps the data key with the KAS's own key, then checks the policy binding. The unwrap has to come first because the binding is keyed by the data key.
4. **Intake.** The caller's claims are read from the verified token by attribute name. The object's labels are parsed from the policy body.
5. **Decide.** `SnapshotDecider.Decide` groups the object's values by attribute, applies each attribute's rule, and requires every attribute to pass. It then collects the obligations triggered for the read action and checks that the client declared it can fulfil them. Access is granted only if both halves pass.
6. **Outcome.** On Permit, the data key is re-encrypted to the caller's public key and an audit event is emitted. On Deny, the caller gets a 403; required obligations are listed only if the caller was entitled.

One thing is not on this path: boolean subject-condition sets. As far as traced, they appear only in the read and provisioning surfaces (`policyread`, `provision`), not in the lite-plane decision.

## What we would prove

Eight guarantees, each stated once for product readers and once for architects. "Holds today" reflects the code review and probe, not a proof.

| # | Guarantee in plain language | Formal statement | Holds today? |
| --- | --- | --- | --- |
| 1 | Deny is the default. Nothing releases a key by accident. | `Permit` has exactly one constructor; every error path returns `Deny`. | Appears to; unproven |
| 2 | Only values defined in the signed policy can grant access. | Permit implies every bound FQN resolves in the signed snapshot, namespace included. | No: D1, D2, D3 |
| 3 | Each rule means what its name says. | Hierarchy is dominance, allOf is subset, anyOf is non-empty intersection; attributes are ANDed. | Yes for defined values; D2 and D4 qualify it |
| 4 | Giving a subject more entitlements never takes access away. | Subject monotonicity: if claims grow, Permit stays Permit. | No: D4 |
| 5 | Obligations are enforced, not advisory. | Permit implies Required ⊆ Fulfillable; the response lists obligations only if entitled. | Appears to; unproven |
| 6 | A denied request learns nothing about the key. | On Deny, the response is the same for any two data keys. | Appears to; unproven |
| 7 | Only verified, current policy decides. | The deciding snapshot is `compile(b)` for a bundle verified under the pinned anchor, with `(epoch, revision)` never decreasing. | By design (ADR-0012); unproven |
| 8 | The fast engine and the readable spec always agree. | For all inputs, the compiled decision equals the reference decision. | No: D5 |

Two subtleties architects will want stated:

- **Guarantee 4 is one-sided by design.** Adding a new attribute to an object can only restrict access. Adding a value to an existing anyOf group widens it, because anyOf means "hold at least one." The model states this as intended behaviour, not a defect.
- **Guarantee 6 is conditional.** `rewrap.go` unwraps the data key before deciding, because the policy-binding check is keyed by it. The theorem therefore says: given the same binding-check outcome, a Deny response does not depend on the key.

## What stays assumed

"100% provable" applies to the decision logic and to non-release. It does not apply to the following, which the model states as explicit assumptions so a reviewer can see exactly where trust rests.

| Assumption | Why it is outside the proof | How it is covered instead |
| --- | --- | --- |
| Signatures, HMAC and key encapsulation are secure | Cryptographic strength is not a property of this code | Standard primitives; modelled as ideal functions |
| The compiler and runtime are correct | Proving a compiler is a separate, very large project | Pinned toolchains; differential testing across Go and Rust |
| No side channels (timing, memory) | The model reasons about values, not physical behaviour | Constant-time primitives where it matters; outside this paper |
| The network and async shell route requests correctly | HTTP, token transport and concurrency are not modelled | Existing wire-parity and end-to-end tests |
| Anti-rollback memory survives | ADR-0012 already notes a wiped data directory loses the revision floor | Stated as an operating condition, as the ADR does |

One item sits in between: **token and JSON parsing.** It can be proven, but the cost is high. The plan tests it differentially first and revisits proof later.

## Six rulings to make first

Each ruling below is open. None needs resolving now; the scenarios are here so the choice is clear when it is made. Every scenario was run against both evaluators directly at commit `4aca7ca`: the compiled snapshot engine that the lite KAS uses, and the string-based reference engine. They were not run through the HTTP rewrap path, and earlier wire-level checks were not traced, so some may be unreachable in a real deployment.

### The example policy used throughout

A small signed bundle in namespace `defense.local`, modelled on the defense template:

| Attribute | Rule | Values | Meaning |
| --- | --- | --- | --- |
| `classification` | hierarchy | TOP\_SECRET > SECRET > CONFIDENTIAL > UNCLASSIFIED | Subject's level must be at or above the object's |
| `releasability` | anyOf | USA, FVEY | Subject must hold at least one of the object's values |
| `need` | allOf | A, B | Subject must hold every one of the object's values |

How to read a scenario:

- **Resource** is the list of attribute values bound to the encrypted object, written as FQNs: `https://<namespace>/attr/<name>/value/<value>`.
- **Subject** is the set of claims in the caller's verified access token: attribute name, then the values held.
- **Result today** is the verdict and the reason string the engine returned.

### D1. Does the namespace in a resource label have to match the policy?

| Element | Value |
| --- | --- |
| Policy | `defense.local` defines `classification` as above |
| Resource | `https://evil.example/attr/classification/value/SECRET` |
| Subject | `classification: [SECRET]` |
| Result today | **Permit**, "holds SECRET ≥ SECRET", in both engines |
| Variant | `https://defense.local/attr/classification/value/SECRET/extra` also permits; the trailing segment is ignored |

**What is happening.** The engine parses the namespace out of the label and then never compares it to anything. It matches on the attribute name alone.

**Why it matters.** The namespace is what says *whose* definition of SECRET applies. Today a label issued under another authority is judged by local rules as if it were local. This is not an obvious privilege escalation, since the subject still needs a local SECRET. It becomes a real problem with multiple namespaces or federation: two authorities with an attribute of the same name are indistinguishable.

**Options.**

- (a) Deny any label whose namespace is not one the signed bundle defines.
- (b) Allow foreign namespaces only through an explicit, signed mapping ("their SECRET equals our SECRET").
- (c) Keep today's behaviour and document that namespaces are informational.

**Suggestion: (a) now, (b) when federation needs it.** Also reject labels with extra path segments. Status: open.

### D2. What if an object carries a hierarchy value the policy does not define?

| Element | Value |
| --- | --- |
| Policy | `classification` as above; there is no value `COSMIC` |
| Resource | `.../classification/value/UNCLASSIFIED` and `.../classification/value/COSMIC` |
| Subject | `classification: [UNCLASSIFIED]` |
| Result today | **Permit**, "holds UNCLASSIFIED ≥ UNCLASSIFIED", in both engines |
| Contrast | With `COSMIC` alone the result is Deny, "value not in attribute set" (from reading the code; not run) |

**What is happening.** For a hierarchy attribute the engine takes the highest level among the object's values *that it recognises* and silently skips the rest. An unknown value only denies when it is the only one.

**Why it matters.** An unknown level is most likely one of two things: a typo, or a level added in a newer policy revision that this node has not loaded. In the second case the unknown value could be the highest one, and the object is released to an UNCLASSIFIED subject. The doc comment on the evaluator says an unknown value denies; that is only true when it stands alone.

**Options.**

- (a) Deny if any bound value fails to resolve.
- (b) Keep today's behaviour.

**Suggestion: (a).** It matches the documented intent and is the fail-closed reading. Status: open.

### D3. Can a value the policy never defined grant access?

| Element | Value |
| --- | --- |
| Policy | `releasability` allows USA and FVEY; there is no value `MARS` |
| Resource | `.../releasability/value/MARS` |
| Subject | `releasability: [MARS]` |
| Result today | **Permit**, "holds MARS", in both engines |
| Same for allOf | Resource `.../need/value/Z`, subject `need: [Z]`: **Permit**, "holds all 1 required" |

**What is happening.** For anyOf and allOf attributes, the engine compares the object's value with the subject's value as plain text. If both sides carry the same string, it matches, whether or not the signed policy ever defined that string.

**Why it matters.** This is the clearest gap against the Signed-State Principle: a grant that rests on no signed object. The scenario needs a token that carries an undefined value. If idplite is the only token minter and it mints strictly from the bundle, that cannot happen. With an external or federated identity provider it can. Reachability was not traced.

**Options.**

- (a) Deny whenever a bound value is not in the signed vocabulary.
- (b) Allow it only for attributes the signed bundle explicitly marks as open-vocabulary.
- (c) Keep today's behaviour and rely on the token minter.

**Suggestion: (a).** Choose (b) only if there is a real need for free-form values, such as per-project tags. Status: open.

### D4. Which value counts when a subject holds several hierarchy levels?

| Element | Subject A | Subject B |
| --- | --- | --- |
| Policy | `classification` as above | Same |
| Resource | `.../classification/value/SECRET` | Same |
| Subject | `classification: [TOP_SECRET, UNCLASSIFIED]` | `classification: [UNCLASSIFIED, TOP_SECRET]` |
| Result today | **Permit**, "holds TOP\_SECRET ≥ SECRET" | **Deny**, "holds UNCLASSIFIED < SECRET" |

**What is happening.** Only the first value in the list is read. The code says so deliberately ("element 0 is load-bearing, never sorted"), and both engines agree.

**Why it matters.** Two subjects with identical entitlements get opposite answers depending on array order in the token. It also means adding an entitlement can remove access, which breaks guarantee 4. Order inside a JSON array is a fragile thing to hang a classification decision on, because any intermediate system that re-serialises the token can change it.

**Options.**

- (a) Reject a hierarchy claim with more than one value at intake. A subject has one level.
- (b) Use the highest held level. Natural reading: TOP\_SECRET clearance covers everything below.
- (c) Use the lowest held level. Most conservative.
- (d) Keep first-wins and document it.

**Suggestion: (a).** It removes the ambiguity instead of resolving it by convention, and it is the easiest rule to prove things about. (b) is the reasonable alternative if existing tokens legitimately carry several levels. Status: open.

### D5. Does the capitalisation of a claim name matter?

| Element | Scenario 1 (anyOf) | Scenario 2 (hierarchy) |
| --- | --- | --- |
| Policy | `releasability` as above | `classification` as above |
| Resource | `.../releasability/value/USA` | `.../classification/value/SECRET` |
| Subject | `Releasability: [USA]` (capital R) | `Classification: [SECRET]` (capital C) |
| Snapshot engine | **Permit**, "holds USA" | **Deny**, "value not in attribute set" |
| Reference engine | **Deny** | **Deny** |

**What is happening.** The reference engine looks up claim names by exact spelling. The snapshot engine folds case when it builds the subject's value set, so anyOf and allOf match regardless of capitalisation. Its hierarchy branch still reads the claim by exact spelling. The result is one disagreement between the two engines, and one inconsistency inside the snapshot engine.

**Why it matters.** This is the only finding where the two engines return different verdicts for the same input, which breaks guarantee 8. The code comments call the case-folding a deliberate normalisation and note that corpus vectors use exact-case names, which is why the corpus does not catch it. ADR-0028 covers case canonicalisation; this finding was not checked against it.

**Options.**

- (a) Fold case for claim names everywhere, in both engines, for all three rule kinds.
- (b) Require exact case everywhere and reject tokens whose claim names differ only by case.
- (c) Keep the split.

**Suggestion: (a)**, subject to what ADR-0028 already rules. Add corpus vectors with mixed-case names so the engines can never drift on this again. Status: open.

### D6. Who can open an object with no attributes?

| Element | Value |
| --- | --- |
| Policy | Any |
| Resource | No attribute values bound |
| Subject | Any authenticated caller, with no claims at all |
| Result today | **Permit**, "no bound attributes", in both engines |
| In the rewrap path | `canAccess` grants a policy with no data attributes without calling the decision engine; a dissemination list, if present, is logged and not evaluated (upstream parity) |

**What is happening.** An unlabelled object is treated as open to every authenticated caller. This matches upstream OpenTDF behaviour and is intentional.

**Why it matters.** It is a legitimate rule, but an important one to leave implicit: "no labels" means "public within the deployment," not "unreadable." Labels cannot be silently stripped in transit, because the policy body is tied to the key by the policy-binding check. The risk is an authoring one: an object encrypted without labels by mistake is readable by everyone.

**Options.**

- (a) Keep the permit and state it as an explicit rule in the model.
- (b) Add a signed bundle setting that lets a deployment deny unlabelled objects.
- (c) Always deny unlabelled objects. This breaks upstream parity.

**Suggestion: (a), plus (b) as an opt-in.** Status: open.

### All six suggestions at a glance

| # | Question | Suggested ruling | Changes today's behaviour? |
| --- | --- | --- | --- |
| D1 | Must the label's namespace match? | Yes; deny unknown namespaces and extra path segments | Yes, Permit becomes Deny |
| D2 | Unknown hierarchy value beside a known one? | Deny if any bound value is unresolved | Yes, Permit becomes Deny |
| D3 | Can an undefined value grant? | No; only the signed vocabulary grants | Yes, Permit becomes Deny |
| D4 | Several hierarchy levels held? | Reject at intake; a subject has one level | Yes, for multi-valued claims |
| D5 | Claim-name capitalisation? | Fold case everywhere | Yes, in the reference engine and the hierarchy branch |
| D6 | Unlabelled objects? | Keep the permit, make it explicit, add an opt-in deny | No, by default |

D1 to D4 move toward Deny. D5 is the exception: folding case lets some tokens with mixed-case claim names succeed where they fail today.

## How we get there

Eight steps in two stages. Each step is small enough to review on its own and ends at a gate that either passes or does not. Stage 1 (steps 1–3) adds no new language to production and is worth doing even if stage 2 never happens.

### Stage 1: specify and cross-check

#### Step 1. Rule on D1–D6 and pin each ruling as corpus vectors

- **What happens.** Each ruling becomes a handful of new vectors in the existing `abac_decide` corpus: the scenario from this paper as input, the ruled verdict as the expected output. Where a ruling changes behaviour, the Go engines are changed to match.
- **Output.** New vectors and, where needed, small Go changes.
- **Gate.** Each vector fails before the Go change and passes after it, on both engines.
- **Why first.** It is cheap, it uses a mechanism the team already trusts, and it fixes the meaning of the policy before anyone formalises it.

#### Step 2. Write the security policy model in Lean

- **What happens.** The decision is written as a short, readable, executable function in Lean 4, together with the theorems from "What we would prove." Lean checks every proof mechanically. A reviewer needs to read only the definitions and theorem statements, not the proofs.
- **Output.** A Lean package, estimated at 300–500 lines for guarantees 1–5. The six rulings appear as named parameters, so changing one is a one-line edit and Lean reports which theorems it affects.
- **Gate.** `lake build` succeeds; no `sorry` (Lean's marker for an unfinished proof); `#print axioms` on each theorem shows only Lean's three standard axioms; `native_decide` is banned because it adds the compiler to what must be trusted.

A sketch of what the model looks like. This is illustrative, not compiled:

```lean
inductive Rule | hierarchy | allOf | anyOf

structure Attr where
  name   : String
  rule   : Rule
  values : List String          -- hierarchy: highest level first

structure Policy where          -- the contents of a verified bundle
  ns    : String
  attrs : List Attr

inductive Verdict | deny | permit

def decide (p : Policy) (subject : Claims) (resource : List Label) : Verdict := ...

-- Guarantee 2: only the signed vocabulary can grant
theorem permit_confined (h : decide p s r = .permit) :
    ∀ l ∈ r, l.ns = p.ns ∧ p.defines l.attr l.value := ...

-- Guarantee 4: more entitlements never remove access
theorem subject_monotone (hsub : s ⊆ s') (h : decide p s r = .permit) :
    decide p s' r = .permit := ...
```

#### Step 3. Use the model as a differential oracle against the Go engines

- **What happens.** Lean compiles the model to a native executable. A Go test feeds the same inputs to the model and to both Go engines: first the whole corpus, then large volumes of randomly generated policies, subjects and resources. Any disagreement is reported with the input that caused it.
- **Output.** A CI job. This is the approach AWS uses for its Cedar policy language: a Lean model, cross-checked against the production implementation by random testing.
- **Gate.** Zero unexplained divergences. Every divergence is classified as a Go defect, a model defect, or a seventh ruling.
- **What stage 1 delivers.** A machine-checked statement of the access policy, proof that the policy has the stated properties, and continuous evidence that the Go code agrees with it on every input tried. That is already the security-policy-model and functional-specification evidence an EAL7-style evaluation asks for.

### Stage 2: a proven implementation

Stage 2 replaces "the Go code agrees with the model on everything we tried" with "the code is proven to implement the model." It introduces Rust for the decision core only.

**How the tooling fits together.** The engineer writes ordinary Rust and adds contracts as attributes: what must be true before a function runs, and what it guarantees after. A tool called hax translates the Rust and its contracts into Lean. Lean then checks two things: that each function meets its contract, and that the translated `decide` is equal to the model's `decide` from step 2. The contracts live in the Rust file where reviewers see them; the longer proofs live in separate `.lean` files.

#### Step 4. Rust decision core over interned IDs, with hax contracts

- **What happens.** A new crate, `tdf-core`, implements the decision over integer IDs and sorted sets, mirroring today's compiled snapshot. It has no dependencies, no `unsafe`, no async and no hash-map iteration, which keeps it inside the subset the tools translate reliably.
- **Output.** The crate, its extracted Lean, and a refinement proof against the step 2 model.
- **Gate.** `cargo hax` and `lake build` pass in CI; the corpus replays through the Rust core; a fuzzer finds no difference between Rust and Go.

A sketch of an inline contract, using hax's attribute syntax. The real contracts tie `decide` to the model:

```rust
#[hax_lib::ensures(|ok| ok == (subject_rank >= 0
                            && floor_rank >= 0
                            && subject_rank <= floor_rank))]
pub fn hierarchy_satisfied(subject_rank: i32, floor_rank: i32) -> bool {
    subject_rank >= 0 && floor_rank >= 0 && subject_rank <= floor_rank
}
```

#### Step 5. Intake: from strings to IDs

- **What happens.** The layer that parses labels, folds case and looks values up in the vocabulary moves to Rust. Four of the six rulings (D1, D2, D3, D5) live here, so this layer is in the model from step 2 onward.
- **Output.** Intake functions with contracts.
- **Gate.** Differential fuzzing against the model from day one. Full proof follows when the tooling's string support allows; hax's documentation says extraction can fail where its Lean model of the Rust standard library is incomplete.

#### Step 6. Make key release impossible without a permit

- **What happens.** The data key and the permit become types that outside code cannot construct. Only `decide` can produce a `Permit`, and `release` cannot be called without one. The Rust compiler enforces this; Lean then proves guarantee 6 over the extracted handler.
- **Output.** The release function and the non-release theorem.
- **Gate.** Guarantee 6 proven; no public constructor for `Permit` or `Dek`.

```rust
pub struct Dek(/* private */);
pub struct Permit { policy_hash: [u8; 32] /* private */ }

pub fn release(permit: Permit, dek: Dek, recipient: &PublicKey) -> WrappedKey
```

#### Step 7. Integrate behind the existing decision seam, in shadow mode

- **What happens.** The lite KAS already calls its engine through a `Decider` interface. The Rust core is added as a second implementation. Both run on every request; Go's answer is used and any disagreement is logged.
- **Output.** A shadow-mode build, then a flip.
- **Gate.** No divergence in shadow mode for an agreed period before Rust becomes authoritative.
- **Packaging choice.** WebAssembly under wazero, a pure-Go runtime, keeps the single static binary. cgo is faster but complicates cross-compilation.

#### Step 8. Bundle verification and anti-rollback

- **What happens.** The rule for accepting a new bundle is modelled and proven: the signature verifies under the pinned anchor, and `(epoch, revision)` never goes backwards. Signature security itself stays an assumption.
- **Output.** Guarantee 7.
- **Gate.** Theorem proven; the acceptance rule in code is the extracted one.

## Alternatives considered

The recommended route is Lean for the model, then Rust with hax contracts for the implementation. Four other routes were weighed.

| Route | What it is | For | Against |
| --- | --- | --- | --- |
| Go plus Lean oracle only | Stop after step 3 | Cheapest; no new production language; already yields the model and specification evidence | No proof about the code itself, only agreement on tested inputs |
| Plain Aeneas, no hax | Translate unannotated Rust to Lean; all specifications live in Lean files | Clean split between engineers and proof engineers | Contracts are invisible to Rust reviewers; drift is easier |
| Anneal | Lean specifications and proofs inside Rust doc comments | Everything in one file; designed for unsafe code | Newer; its exact syntax was not verified for this paper; the core has no unsafe code to justify it |
| Verus | Contracts and proofs in Rust syntax, checked by an SMT solver | More mature for Rust; more automation | Not Lean, so the model and the code proof would live in different systems; adds the solver to what must be trusted |

**Why hax.** The contracts sit beside the code, the proofs are checked by the same Lean kernel as the model, and its current Lean backend is built on Aeneas, so the choice does not close off the plain-Aeneas route.

**The fallback.** If the stage 2 tooling proves too immature, stopping at stage 1 is a complete and defensible result.

## Risks and open questions

| Risk | Likelihood and impact | Mitigation |
| --- | --- | --- |
| hax's Lean backend is experimental | Real; could stall step 4 or 5 | Stage 1 does not depend on it; plain Aeneas and Verus are fallbacks |
| Proofs lag behind code changes | Certain without discipline | The verify step runs in CI and blocks merge; `cargo build` alone does not check proofs |
| Lean and its libraries change quickly | Moderate | Pin the toolchain; treat upgrades as planned work |
| A ruling changes behaviour a consumer depends on | Unknown until D1–D6 are checked against real tokens and objects | Shadow-log would-be denials before enforcing each ruling |
| Lean has no known certification precedent | Matters only if formal certification is the goal | Raise it with an evaluation lab early; the model is portable in principle |
| A second language in the build | Moderate operational cost | Scope Rust to one small crate behind one interface |

Open questions this paper could not answer from the code:

- Can a token ever carry a value outside the signed vocabulary? This decides how urgent D3 is.
- Do any live tokens carry more than one hierarchy level? This decides between options (a) and (b) for D4.
- What does ADR-0028 already rule on claim-name case? This may settle D5.
- Is the boolean subject-condition tree wanted in the proven core later, for external identity sources? It is not in the lite decision path today. If it is added, it is a small, easily proven component.

## How this maps to EAL7-style evidence

This is a mapping of artifacts to the kinds of evidence the highest Common Criteria level asks for. It is not a certification plan, and the family names are given from memory, not checked against the current standard.

| Evidence asked for | Common Criteria family | Artifact in this plan |
| --- | --- | --- |
| A formal model of the security policy | ADV\_SPM | The Lean model and its theorems (step 2) |
| A formal functional specification of the interfaces | ADV\_FSP | Five interfaces (load bundle, intake, decide, release, audit) with contracts and the ADR-0005 reason codes as the error set |
| A formal high-level design and its correspondence to the specification | ADV\_TDS | The module split (intake, decide, release) and the refinement proofs between model and extracted code |
| A mapping from design to implementation | ADV\_IMP | hax extraction plus the refinement proof (steps 4–6). This goes further than the level requires, which asks for a mapping and testing, not code proof |
| Independent testing | ATE | The conformance corpus and the differential oracle (step 3) |

Stage 1 alone covers the first two rows.

## Terms

| Term | Meaning here |
| --- | --- |
| ABAC | Attribute-based access control: access is decided by comparing attributes of the subject with attributes of the object |
| Bundle | TDFLite's signed policy object; the only source of policy the platform serves from |
| Snapshot | The bundle compiled into an immutable in-memory form with values turned into integer IDs |
| FQN | Fully qualified name of an attribute value: `https://<namespace>/attr/<name>/value/<value>` |
| hierarchy / allOf / anyOf | The three attribute rules: at-or-above a level; hold every value; hold at least one |
| Subject, resource | The caller (as claims in a verified token) and the encrypted object (as its bound attribute values) |
| DEK | Data encryption key: the key that encrypts one object's payload |
| KAS, rewrap | Key access service; "rewrap" is the request in which it re-encrypts the DEK to the caller if policy allows |
| Obligation | A duty the client must be able to fulfil (for example, watermarking) before access is granted |
| Lean | A proof assistant: a language for writing definitions and proofs that a small trusted kernel checks |
| Security policy model | The formal statement of what the access policy is and which properties it has |
| hax | A tool that translates annotated Rust into Lean (and other provers) so its contracts can be proven |
| Aeneas | The underlying translator from Rust to pure functional Lean code |
| Refinement proof | A proof that an implementation behaves exactly as a simpler model says it should |
| Differential oracle | An independent implementation used to cross-check another by running both on the same inputs |

## Sources

- The repository: [willackerly/TDFLite](https://github.com/willackerly/tdflite) at commit `4aca7ca`; ADR-0012, ADR-0016, `pkg/pdp`, `internal/lite/kas`.
- hax contract and proof attributes: [Verifying a real-world Rust crate](https://hax.cryspen.com/blog/2026/01/19/verifying-a-real-world-rust-crate/) and the [hax 0.4 release notes](https://hax.cryspen.com/blog/).
- hax Lean backend limits: [Lean quick start](https://hax.cryspen.com/manual/lean/quick_start/).
- Aeneas: [lean-lang.org use case](https://lean-lang.org/use-cases/aeneas).
- The Cedar comparison and the Common Criteria mapping are from memory and were not looked up for this paper.
