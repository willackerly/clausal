/-
Support for the proofs of the overlay project `tdf` (plan node T9.7a). Hand-written.

NOTHING HERE PROVES A FACT ABOUT THE MODEL FROM SCRATCH. Every lemma about what `tdf_core.decide.decide` or
`tdf_core.rules.satisfied` returns is obtained from a theorem of T9.3 (`T93.*`, each of type exactly its frozen
statement `T93.<name>.stmt`); what is added is the passage between the words of the pack (Abac/Pieces.lean) and the
terms those statements are written in.
-/
import Local.Obligations
import T93.Proofs
open Aeneas Aeneas.Std Result

namespace TdfProofs
open tdf_core

/-- The pack's "is satisfied under its rule", for one attribute, is what `rules::satisfied` answers:
    `T93.core_g3_hierarchy`, `T93.core_g3_allOf`, `T93.core_g3_anyOf` for the three kinds, and
    `T93.satisfied_refines` with `T93.idspec_g3_norule` for an attribute with none of them. -/
theorem satisfied_iff (s : snapshot.Snapshot) (sub : subject.Subject) (a : Std.U32) (ids : alloc.vec.Vec Std.U32) :
    rules.satisfied s sub a (alloc.vec.Vec.deref ids) = ok true ↔ Abac.ruleSatisfied s sub ids.val a := by
  have norule : (∀ r, s.attr_rule.val[a.val]? ≠ some (some r)) →
      rules.satisfied s sub a (alloc.vec.Vec.deref ids) = ok false := by
    intro h
    rw [T93.satisfied_refines s sub a (alloc.vec.Vec.deref ids)]
    congr 1
    apply T93.idspec_g3_norule
    intro r hr
    simp only [T93.absSnapshot, List.getElem?_map] at hr
    cases h' : s.attr_rule.val[a.val]? with
    | none => simp [h'] at hr
    | some o =>
      cases o with
      | none => simp [h'] at hr
      | some r' => exact h r' h'
  unfold Abac.ruleSatisfied
  cases h : s.attr_rule.val[a.val]? with
  | none =>
    rw [norule (by intro r hr; rw [h] at hr; cases hr)]
    simp
  | some o =>
    cases o with
    | none =>
      rw [norule (by intro r hr; rw [h] at hr; cases hr)]
      simp
    | some r =>
      cases r with
      | Hierarchy =>
        obtain ⟨b, hb, hiff⟩ := T93.core_g3_hierarchy s sub a (alloc.vec.Vec.deref ids) h
        rw [hb]
        simp only [T93.deref_val] at hiff
        dsimp only
        constructor
        · intro e; exact hiff.mp (by simpa using e)
        · intro e; rw [hiff.mpr e]
      | AllOf =>
        obtain ⟨b, hb, hiff⟩ := T93.core_g3_allOf s sub a (alloc.vec.Vec.deref ids) h
        rw [hb]
        simp only [T93.deref_val] at hiff
        dsimp only
        constructor
        · intro e; exact hiff.mp (by simpa using e)
        · intro e; rw [hiff.mpr e]
      | AnyOf =>
        obtain ⟨b, hb, hiff⟩ := T93.core_g3_anyOf s sub a (alloc.vec.Vec.deref ids) h
        rw [hb]
        simp only [T93.deref_val] at hiff
        dsimp only
        constructor
        · intro e; exact hiff.mp (by simpa using e)
        · intro e; rw [hiff.mpr e]

/-- The pack's "holds more values or higher levels", on the subjects, is T9.3's `AtOrAbove` on their readings. -/
theorem atOrAbove_abs (sub sub' : subject.Subject)
    (hh : ∀ i ∈ sub.held.val, i ∈ sub'.held.val)
    (hl : ∀ (a : Nat) (n : Std.U32), sub.level.val[a]? = some (.At n) →
      ∃ n' : Std.U32, sub'.level.val[a]? = some (.At n') ∧ n'.val ≤ n.val) :
    T93.AtOrAbove (T93.absSubject sub) (T93.absSubject sub') := by
  refine ⟨?_, ?_⟩
  · intro i hi
    obtain ⟨x, hx, rfl⟩ := T93.mem_of_mem_nats hi
    exact List.mem_map.mpr ⟨x, hh x hx, rfl⟩
  · intro a m hm
    simp only [T93.absSubject, List.getElem?_map] at hm ⊢
    cases h : sub.level.val[a]? with
    | none => simp [h] at hm
    | some lv =>
      cases lv with
      | None => simp [h, T93.absLevel] at hm
      | At n =>
        simp [h, T93.absLevel] at hm
        obtain ⟨n', h', hle⟩ := hl a n h
        exact ⟨n'.val, by simp [h', T93.absLevel], by omega⟩

/-- The converse: T9.3's `AtOrAbove` on the readings of two subjects is the pack's relation on the subjects. -/
theorem atOrAbove_of_abs (sub sub' : subject.Subject)
    (h : T93.AtOrAbove (T93.absSubject sub) (T93.absSubject sub')) :
    (∀ i ∈ sub.held.val, i ∈ sub'.held.val) ∧
    ∀ (a : Nat) (n : Std.U32), sub.level.val[a]? = some (.At n) →
      ∃ n' : Std.U32, sub'.level.val[a]? = some (.At n') ∧ n'.val ≤ n.val := by
  obtain ⟨hh, hl⟩ := h
  refine ⟨?_, ?_⟩
  · intro i hi
    have h1 : i.val ∈ T93.nats sub'.held.val := hh i.val ((T93.mem_nats sub.held.val i).mpr hi)
    exact (T93.mem_nats sub'.held.val i).mp h1
  · intro a n hn
    have h1 : (T93.absSubject sub).level[a]? = some (some n.val) := by
      simp [T93.absSubject, List.getElem?_map, hn, T93.absLevel]
    obtain ⟨m', hm', hle⟩ := hl a n.val h1
    simp only [T93.absSubject, List.getElem?_map] at hm'
    cases h : sub'.level.val[a]? with
    | none => simp [h] at hm'
    | some lv =>
      cases lv with
      | None => simp [h, T93.absLevel] at hm'
      | At n' =>
        simp [h, T93.absLevel] at hm'
        exact ⟨n', rfl, by omega⟩

/-- A call returns one value. -/
theorem ok_eq {α : Type} {x : Result α} {a b : α} (h1 : x = ok a) (h2 : x = ok b) : a = b := by
  rw [h1] at h2
  exact Result.ok_injective h2

/-- The labels of a request that records a list. -/
theorem labels_of {r : request.Request} {ids : alloc.vec.Vec Std.U32} (hb : r.bound = .Labels ids) :
    Abac.labels r = ids.val := by
  simp [Abac.labels, hb]

/-- Guarantee 3 for a labelled request in the pack's words, from `T93.core_g3_entitled` and `satisfied_iff`
    (for the one-way sentences about one rule kind; the link `g3` does not use this). -/
theorem g3_labelled (st : snapshot.Snapshot) (inp : request.Request) (hu : Abac.labelled inp) :
    ∃ d, decide.decide st inp = ok d ∧
      (d.entitled = true ↔ ∀ x ∈ Abac.labels inp, Abac.satisfied st inp x) := by
  obtain ⟨d, hd⟩ := T93.decide_total st inp
  refine ⟨d, hd, ?_⟩
  obtain ⟨ids, hb, hne⟩ := hu
  have key := T93.core_g3_entitled st inp d ids hd hb hne
  have hl : Abac.labels inp = ids.val := labels_of hb
  constructor
  · intro he x hx
    rw [hl] at hx
    obtain ⟨a, ha, hs⟩ := key.mp he x hx
    exact ⟨a, ha, by rw [hl]; exact (satisfied_iff st inp.subject a ids).mp hs⟩
  · intro H
    refine key.mpr ?_
    intro i hi
    obtain ⟨a, ha, hs⟩ := H i (by rw [hl]; exact hi)
    rw [hl] at hs
    exact ⟨a, ha, (satisfied_iff st inp.subject a ids).mpr hs⟩

/-- The pack's rule for one attribute, one kind at a time (the definition `Abac.ruleSatisfied`, read off). -/
theorem ruleSatisfied_allOf {p : snapshot.Snapshot} {sub : subject.Subject} {ids : List Std.U32} {a : Std.U32}
    (h : p.attr_rule.val[a.val]? = some (some .AllOf)) :
    Abac.ruleSatisfied p sub ids a ↔ ∀ i ∈ ids, p.value_attr.val[i.val]? = some a → i ∈ sub.held.val := by
  simp only [Abac.ruleSatisfied, h]

theorem ruleSatisfied_anyOf {p : snapshot.Snapshot} {sub : subject.Subject} {ids : List Std.U32} {a : Std.U32}
    (h : p.attr_rule.val[a.val]? = some (some .AnyOf)) :
    Abac.ruleSatisfied p sub ids a ↔ ∃ i ∈ ids, p.value_attr.val[i.val]? = some a ∧ i ∈ sub.held.val := by
  simp only [Abac.ruleSatisfied, h]

theorem ruleSatisfied_hierarchy {p : snapshot.Snapshot} {sub : subject.Subject} {ids : List Std.U32} {a : Std.U32}
    (h : p.attr_rule.val[a.val]? = some (some .Hierarchy)) :
    Abac.ruleSatisfied p sub ids a ↔
      ∃ mine : Std.U32, sub.level.val[a.val]? = some (.At mine) ∧
        ∀ i ∈ ids, p.value_attr.val[i.val]? = some a → ∃ k : Std.U32, p.rank.val[i.val]? = some k ∧ mine.val ≤ k.val := by
  simp only [Abac.ruleSatisfied, h]

/-! ## The fixtures: what the model answers at them, through `T93.decide_refines`

The fixtures of Tdf/Pieces.lean are the values T9.3's witnesses are proved at. -/

theorem policy_eq : Tdf.twoLevelPolicy = T93.wSnapshot := rfl
theorem request_eq (level : subject.Level) (declared : List Std.U32) (h : declared.length ≤ 3) :
    Tdf.requestWith level declared h = T93.wRequest level declared h := rfl

theorem at_clearedDeclaring (d : decide.Decision) (hd : decide.decide Tdf.twoLevelPolicy Tdf.clearedDeclaring = ok d) :
    d.entitled = true ∧ d.release = true := by
  obtain ⟨he, hr, _⟩ := T93.decide_refines _ _ d hd
  have he' : d.entitled = Tdf.IdSpec.entitled (T93.absSnapshot Tdf.twoLevelPolicy)
      (T93.absRequest Tdf.clearedDeclaring).bound (T93.absRequest Tdf.clearedDeclaring).subject := he
  simp only [Tdf.clearedDeclaring, policy_eq, request_eq] at he' hr
  rw [T93.wSnapshot_abs, T93.wRequest_abs] at he' hr
  simp [T93.absLevel, T93.nats] at he' hr
  exact ⟨by rw [he']; decide, by rw [hr]; decide⟩

theorem at_clearedSilent (d : decide.Decision) (hd : decide.decide Tdf.twoLevelPolicy Tdf.clearedSilent = ok d) :
    d.entitled = true ∧ d.release = false := by
  obtain ⟨he, hr, _⟩ := T93.decide_refines _ _ d hd
  have he' : d.entitled = Tdf.IdSpec.entitled (T93.absSnapshot Tdf.twoLevelPolicy)
      (T93.absRequest Tdf.clearedSilent).bound (T93.absRequest Tdf.clearedSilent).subject := he
  simp only [Tdf.clearedSilent, policy_eq, request_eq] at he' hr
  rw [T93.wSnapshot_abs, T93.wRequest_abs] at he' hr
  simp [T93.absLevel, T93.nats] at he' hr
  exact ⟨by rw [he']; decide, by rw [hr]; decide⟩

theorem at_noLevel (d : decide.Decision) (hd : decide.decide Tdf.twoLevelPolicy Tdf.noLevel = ok d) :
    d.entitled = false := by
  obtain ⟨he, _, _⟩ := T93.decide_refines _ _ d hd
  have he' : d.entitled = Tdf.IdSpec.entitled (T93.absSnapshot Tdf.twoLevelPolicy)
      (T93.absRequest Tdf.noLevel).bound (T93.absRequest Tdf.noLevel).subject := he
  simp only [Tdf.noLevel, policy_eq, request_eq] at he'
  rw [T93.wSnapshot_abs, T93.wRequest_abs] at he'
  simp only [T93.absLevel] at he'
  rw [he']; decide

theorem labelled_fixture (level : subject.Level) (declared : List Std.U32) (h : declared.length ≤ 3) :
    Abac.labelled (Tdf.requestWith level declared h) :=
  ⟨_, rfl, by simp [Tdf.vec3]⟩

/-- The one label of every fixture request is value 1. -/
theorem labels_fixture (level : subject.Level) (declared : List Std.U32) (h : declared.length ≤ 3) :
    Abac.labels (Tdf.requestWith level declared h) = [1#u32] := by
  simp [Abac.labels, Tdf.requestWith, Tdf.vec3]

/-- The two-level policy with its one attribute given another rule (for the scope of the sentences about one kind). -/
def policyOfKind (k : snapshot.Rule) : snapshot.Snapshot :=
  { Tdf.twoLevelPolicy with attr_rule := Tdf.vec3 [some k] (by simp) }

theorem ofKind_fixture (k : snapshot.Rule) : Abac.ofKind (policyOfKind k) k 1#u32 :=
  ⟨0#u32, by simp [policyOfKind, Tdf.twoLevelPolicy, Tdf.vec3], by simp [policyOfKind, Tdf.vec3]⟩

end TdfProofs
