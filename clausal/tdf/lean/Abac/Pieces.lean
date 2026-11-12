/-
THE VOCABULARY, Lean side, of the access-control pack (../../../clausebook/abac.yaml, plan node T9.7a): DOMAIN WORDS.
Hand-written and HUMAN-ASSERTED: each definition is the intended meaning of one word of the pack.

STATED LIMIT (the same as the ledger pack's): this is a pack in the book only. The definitions are stated on the
types Aeneas extracted from the one crate that uses the pack today (`tdf_core.snapshot.Snapshot`,
`tdf_core.request.Request`, `tdf_core.decide.Decision`); a second crate cannot use them until they are stated
over an interface. That crate is not in the tracked repository, so this file builds only in the overlay
workspace (../../README.md).

No definition here mentions a function of the model: every word is about the VALUES a policy, a request and a
decision are made of. The three rule kinds (hierarchy, allOf, anyOf) are stated once, in `ruleSatisfied`.
-/
import Generated.TdfCore
import Frames.Frames
open Aeneas Aeneas.Std

namespace Abac
open tdf_core

/-! WHAT THIS LAYER SEES OF THE OBJECT. A request carries either the mark `Unresolved` or a list of identifiers.
    Whether a string bound to the object was a label of the policy, and which identifier it became, is settled by the
    intake before `decide` is called and is NOT a statement of this layer: the three words below are about the mark
    and the list, and about nothing else. In particular an identifier in the list need not be a value of the policy
    (`defined` says that it is). -/

/-- "label of the request": the identifiers the request records for its object, in order, repeats kept; none if
    the request records its labels as not resolved. -/
@[reducible] def labels (r : request.Request) : List Std.U32 :=
  match r.bound with
  | .Unresolved => []
  | .Labels ids => ids.val

/-- "the request is unresolved": the request carries the mark that the labels of its object did not resolve. -/
@[reducible] def unresolved (r : request.Request) : Prop := r.bound = .Unresolved

/-- "the request carries no label": the request records a list of labels, and the list is empty. -/
@[reducible] def unlabelled (r : request.Request) : Prop :=
  ∃ ids : alloc.vec.Vec Std.U32, r.bound = .Labels ids ∧ ids.val = []

/-- "the request carries a label": the request records a list of labels with at least one in it. -/
@[reducible] def labelled (r : request.Request) : Prop :=
  ∃ ids : alloc.vec.Vec Std.U32, r.bound = .Labels ids ∧ ids.val ≠ []

/-- "the policy admits unlabelled objects": its signed setting does not deny an object that carries no label. -/
@[reducible] def admitsUnlabelled (p : snapshot.Snapshot) : Prop := p.deny_unlabelled = false

/-- "the subject of the request holds something": a value, or a level for some attribute. -/
@[reducible] def holdsSomething (r : request.Request) : Prop :=
  r.subject.held.val ≠ [] ∨ ∃ (a : Nat) (n : Std.U32), r.subject.level.val[a]? = some (.At n)

/-- "is defined by the policy" (of a label): it is a value of the policy, of an attribute the policy gives one of
    the three rules; and under a hierarchy the value has a rank. -/
@[reducible] def defined (p : snapshot.Snapshot) (i : Std.U32) : Prop :=
  ∃ (a : Std.U32) (ru : snapshot.Rule),
    p.value_attr.val[i.val]? = some a ∧ p.attr_rule.val[a.val]? = some (some ru) ∧
    (ru = .Hierarchy → ∃ k, p.rank.val[i.val]? = some k)

/-- THE THREE RULE KINDS. Attribute `a` is satisfied by a subject for an object that binds the values `ids`
    (only the bound values that belong to `a` are looked at):

    * hierarchy: the subject has a level for the attribute and it is at or above the level of every bound
      value of the attribute (a rank that is `≤`; rank 0 is the highest);
    * allOf: every bound value of the attribute is held;
    * anyOf: some bound value of the attribute is held;
    * no rule, or no such attribute: never. -/
@[reducible] def ruleSatisfied (p : snapshot.Snapshot) (sub : subject.Subject) (ids : List Std.U32) (a : Std.U32) : Prop :=
  match p.attr_rule.val[a.val]? with
  | some (some .Hierarchy) =>
      ∃ mine : Std.U32, sub.level.val[a.val]? = some (.At mine) ∧
        ∀ i ∈ ids, p.value_attr.val[i.val]? = some a → ∃ k : Std.U32, p.rank.val[i.val]? = some k ∧ mine.val ≤ k.val
  | some (some .AllOf) => ∀ i ∈ ids, p.value_attr.val[i.val]? = some a → i ∈ sub.held.val
  | some (some .AnyOf) => ∃ i ∈ ids, p.value_attr.val[i.val]? = some a ∧ i ∈ sub.held.val
  | _ => False

/-- "is satisfied by the subject of the request under the policy" (of a label): the label belongs to an attribute,
    and the subject satisfies that attribute, under its rule, for all the labels the request carries. -/
@[reducible] def satisfied (p : snapshot.Snapshot) (r : request.Request) (i : Std.U32) : Prop :=
  ∃ a : Std.U32, p.value_attr.val[i.val]? = some a ∧ ruleSatisfied p r.subject (labels r) a

/-! ## The three rule kinds, one at a time (fix round of T9.7a) -/

/-- "is of a <kind> attribute of the policy" (of a label): a value of the policy, of an attribute the policy gives
    that rule. -/
@[reducible] def ofKind (p : snapshot.Snapshot) (k : snapshot.Rule) (i : Std.U32) : Prop :=
  ∃ a : Std.U32, p.value_attr.val[i.val]? = some a ∧ p.attr_rule.val[a.val]? = some (some k)

/-- "the request carries only labels of allOf attributes of the policy": it carries a label, and every label is of
    an allOf attribute. -/
@[reducible] def onlyAllOf (p : snapshot.Snapshot) (r : request.Request) : Prop :=
  labelled r ∧ ∀ i ∈ labels r, ofKind p .AllOf i

/-- "the request carries only labels of anyOf attributes of the policy". -/
@[reducible] def onlyAnyOf (p : snapshot.Snapshot) (r : request.Request) : Prop :=
  labelled r ∧ ∀ i ∈ labels r, ofKind p .AnyOf i

/-- "the request carries only labels of hierarchy attributes of the policy". -/
@[reducible] def onlyHierarchy (p : snapshot.Snapshot) (r : request.Request) : Prop :=
  labelled r ∧ ∀ i ∈ labels r, ofKind p .Hierarchy i

/-- "is held by the subject of the request" (of a label): one of the values the subject holds. -/
@[reducible] def heldBy (r : request.Request) (i : Std.U32) : Prop := i ∈ r.subject.held.val

/-- "shares its attribute under the policy with a label held by the subject of the request" (of a label): it is a
    value of an attribute, and some label of the request of that same attribute is held. -/
@[reducible] def sharesHeld (p : snapshot.Snapshot) (r : request.Request) (i : Std.U32) : Prop :=
  ∃ a : Std.U32, p.value_attr.val[i.val]? = some a ∧
    ∃ j ∈ labels r, p.value_attr.val[j.val]? = some a ∧ j ∈ r.subject.held.val

/-- "is at or below the level of the subject of the request under the policy" (of a label): it is a value of an
    attribute for which the subject has a level, it has a rank, and the level is at or above it (a rank that is
    `≤`; rank 0 is the highest). -/
@[reducible] def atOrBelowLevel (p : snapshot.Snapshot) (r : request.Request) (i : Std.U32) : Prop :=
  ∃ (a mine k : Std.U32), p.value_attr.val[i.val]? = some a ∧ r.subject.level.val[a.val]? = some (.At mine) ∧
    p.rank.val[i.val]? = some k ∧ mine.val ≤ k.val

/-- "the subject is entitled": the decision's entitlement bit. -/
@[reducible] def entitled (d : decide.Decision) : Prop := d.entitled = true

/-- "the key is released": the decision's release bit. -/
@[reducible] def released (d : decide.Decision) : Prop := d.release = true

/-- "listed obligation": the identifiers of the obligations the decision lists, in order, repeats kept. -/
@[reducible] def listed (d : decide.Decision) : List Nat := d.listed.val.map (·.val)

/-- "the number of listed obligations". -/
@[reducible] def listedCount (d : decide.Decision) : Nat := d.listed.val.length

/-- "declared obligation of the request": the identifiers of the obligations the client declared it can fulfil. -/
@[reducible] def declared (r : request.Request) : List Nat := r.declared.val.map (·.val)

/-- "is declared by the client of the request" (of an obligation): one of the declared obligations. -/
@[reducible] def declaredBy (r : request.Request) (o : Nat) : Prop := o ∈ declared r

/-- "the subject holds more values": the second call is under the same policy, about the same object, client and
    declared obligations; the subject has the SAME levels and holds every value the first subject holds. -/
@[reducible] def holdsMore : Frames.Variation snapshot.Snapshot request.Request := fun p r p₂ r₂ =>
  p₂ = p ∧ r₂.bound = r.bound ∧ r₂.client = r.client ∧ r₂.declared = r.declared ∧
  r₂.subject.level = r.subject.level ∧ ∀ i ∈ r.subject.held.val, i ∈ r₂.subject.held.val

/-- "the subject holds more values or higher levels": the second call is under the same policy, about the same
    object, client and declared obligations; the subject holds every value the first subject holds, and wherever
    the first subject has a level the second has a level at or above it (a rank that is `≤`). -/
@[reducible] def atOrAbove : Frames.Variation snapshot.Snapshot request.Request := fun p r p₂ r₂ =>
  p₂ = p ∧ r₂.bound = r.bound ∧ r₂.client = r.client ∧ r₂.declared = r.declared ∧
  (∀ i ∈ r.subject.held.val, i ∈ r₂.subject.held.val) ∧
  ∀ (a : Nat) (n : Std.U32), r.subject.level.val[a]? = some (.At n) →
    ∃ n' : Std.U32, r₂.subject.level.val[a]? = some (.At n') ∧ n'.val ≤ n.val

end Abac
