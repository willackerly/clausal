Feature: TDFLite decision core
  Guarantees 1 to 5 of the TDFLite key-release decision, at the ID level, as canonical Clausal Rule lines about the
  Rust decision core `tdf-core` as Aeneas extracted it (plan node T9.7a). Every line is compiled from the pieces of
  clausebook/core.yaml (unchanged), the access-control pack clausebook/abac.yaml and the local book
  clausebook/local/tdf.yaml. The expected verdict of each was committed before anything was compiled or run
  (tdf/expected.json).

  This file is read only for the project `tdf` of the local overlay (projects.local.yaml; tdf/README.md): the crate
  is not in the tracked repository. It is not under features/, which holds the feature files of the tracked projects.

  A line tagged @expect-unbound is a guarantee, or a part of one, written the way it would be said, that today's
  pieces cannot say: it stays stated here and is reported as not shown, with the missing piece named
  (tdf/expected.json, `missing`).

  # ====================================================================== Guarantee 1: deny is the default
  # T9.3 `core_g1`: entitlement has exactly two grounds. Said here as three lines, one per kind of object.
  @id:g1_unresolved
  Rule: An entitlement decision for which the request is unresolved is always rejected

  @id:g1_unlabelled
  Rule: An entitlement decision for which the request carries no label is accepted only if the policy admits unlabelled objects

  @id:g1_labelled
  Rule: An entitlement decision for which the request carries a label is accepted only if the subject of the request holds something

  # the guarantee in one line, as T9.3 states it: needs "or" (and "and") between two conditions
  @id:g1_two_grounds @expect-unbound
  Rule: An entitlement decision is accepted only if the request carries no label and the policy admits unlabelled objects, or the request carries a label and the subject of the request holds something

  # ====================================================================== Guarantee 2: only values the policy defines can grant
  # T9.3 `core_g2`.
  @id:g2_defined
  Rule: An entitlement decision is accepted only if every label of the request is defined by the policy

  # the same of the release (the wording of the planning study): through `core_g5` (released implies entitled)
  @id:g2_defined_release
  Rule: A key release is accepted only if every label of the request is defined by the policy

  # ====================================================================== Guarantee 3: the three rule kinds
  # T9.3 `core_g3_entitled` with `core_g3_hierarchy`, `core_g3_allOf`, `core_g3_anyOf` and the no-rule case. The three
  # kinds are in the MEANING of "is satisfied by the subject ... under the policy" (clausebook/abac.yaml, `abac.satisfied`).
  @id:g3_entitled
  Rule: An entitlement decision for which the request carries a label is accepted exactly when every label of the request is satisfied by the subject of the request under the policy

  # one line per rule kind, about the check of ONE attribute (`tdf_core::rules::satisfied`): that function takes a
  # subject, an attribute and the bound values, and an operation of this compiler takes one input
  @id:g3_hierarchy @expect-unbound
  Rule: An attribute check of a hierarchy attribute is accepted exactly when the level of the subject is at or above every bound level of the attribute

  @id:g3_all_of @expect-unbound
  Rule: An attribute check of an allOf attribute is accepted exactly when every bound value of the attribute is held by the subject

  @id:g3_any_of @expect-unbound
  Rule: An attribute check of an anyOf attribute is accepted exactly when some bound value of the attribute is held by the subject

  # (fix round) one line per rule kind about the DECISION, for a request all of whose labels are of that kind. T9.3 has no
  # statement of exactly this: each follows from `core_g3_entitled` with the statement of that kind.
  @id:g3_all_of_decision
  Rule: An entitlement decision for which the request carries only labels of allOf attributes of the policy is accepted exactly when every label of the request is held by the subject of the request

  @id:g3_any_of_decision
  Rule: An entitlement decision for which the request carries only labels of anyOf attributes of the policy is accepted exactly when every label of the request shares its attribute under the policy with a label held by the subject of the request

  @id:g3_hierarchy_decision
  Rule: An entitlement decision for which the request carries only labels of hierarchy attributes of the policy is accepted exactly when every label of the request is at or below the level of the subject of the request under the policy

  # (fix round) the allOf line with the scope said as "every label ... is of an allOf attribute": FALSE, because a request
  # with no label is in that scope (an unresolved one is never entitled). Core has no `and` to add "carries a label".
  @id:g3_all_of_unscoped @expect-refuted
  Rule: An entitlement decision for which every label of the request is of an allOf attribute of the policy is accepted exactly when every label of the request is held by the subject of the request

  # ====================================================================== Guarantee 4: more never takes access away
  # T9.3 `core_g4` (the restricted form: the same levels, more values), for the entitlement and for the release.
  @id:g4_more_values
  Rule: An entitlement decision never loses acceptance when the subject holds more values

  @id:g4_more_values_release
  Rule: A key release never loses acceptance when the subject holds more values

  # T9.3 `core_g4b` (default O2: also a subject with higher levels).
  @id:g4b_higher
  Rule: An entitlement decision never loses acceptance when the subject holds more values or higher levels

  @id:g4b_higher_release
  Rule: A key release never loses acceptance when the subject holds more values or higher levels

  # ====================================================================== Guarantee 5: obligations
  # T9.3 `core_g5`: released exactly when entitled and every listed obligation was declared; nothing is listed for a
  # subject that is not entitled; what is listed for one that is, is what the specification requires.
  @id:g5_released_entitled
  Rule: For an accepted key release, the subject is entitled

  @id:g5_released_declared
  Rule: For an accepted key release, every listed obligation is a declared obligation of the request

  @id:g5_none_listed
  Rule: For a rejected entitlement decision, the number of listed obligations is zero

  @id:g5_listed_required
  Rule: For an accepted entitlement decision, the obligation list is the required obligation list of the request under the policy

  # (fix round) the "if" half of the first part: entitled, and every required obligation declared, gives the release. With
  # the four lines above this is the whole of `core_g5` (tdf/links.yaml, link g5).
  @id:g5_entitled_declared_released
  Rule: For an accepted entitlement decision for which every required obligation of the request under the policy is declared by the client of the request, the key is released

  # (fix round) the "only if" half said of what is REQUIRED (not of what the decision lists): follows from `core_g5`
  @id:g5_release_required_declared
  Rule: A key release is accepted only if every required obligation of the request under the policy is declared by the client of the request

  # the first part of the guarantee in one line, as T9.3 states it: an equivalence between the release and two facts
  # about the SAME answer. Core's "exactly when" takes a condition on the input, not a class of the answer
  @id:g5_exact @expect-unbound
  Rule: A key release is accepted exactly when the subject is entitled and every listed obligation is a declared obligation of the request

  # ====================================================================== Witnesses: each kind of answer is reached
  # T9.3 `witness_release`, `witness_withheld`, `witness_denied`, at the inputs those theorems are proved at.
  # (a) as scenarios at a named policy and a named request (tdf/types.yaml; tdf/lean/Tdf/Pieces.lean)
  @id:w_released
  Scenario: a labelled object is released to a cleared subject whose client declares the obligation
    Given policy Demo is the two-level policy
    When policy Demo decides the key release for the cleared request declaring obligation 7
    Then the key is released
    And the subject is entitled

  @id:w_withheld
  Scenario: an entitled subject is refused the key over an undeclared obligation
    Given policy Demo is the two-level policy
    When policy Demo decides the key release for the cleared request declaring nothing
    Then the key is withheld
    And the subject is entitled

  @id:w_denied
  Scenario: a labelled object is denied to a subject that holds something
    Given policy Demo is the two-level policy
    And the subject of the request without a level holds something
    When policy Demo decides the entitlement for the request without a level
    Then the subject is not entitled

  # (b) as the universal sentence each witness refutes: the falsifying input is the witness
  @id:w_not_always_withheld @expect-refuted
  Rule: A key release for which the request carries a label is always rejected

  @id:w_entitled_not_released @expect-refuted
  Rule: For an accepted entitlement decision, the key is released

  @id:w_holding_not_enough @expect-refuted
  Rule: An entitlement decision for which the request carries a label is accepted whenever the subject of the request holds something

  # (c) as it would be said: core has no frame that says a call of some kind EXISTS
  @id:w_sometimes @expect-unbound
  Rule: A key release for which the request carries a label is sometimes accepted
