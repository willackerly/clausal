# Reviewer's refusal probes (V2/V3 review, second pass): each should be refused, never guessed.
Feature: Refusals

  @id:q9_bystander_given
  Scenario: a Given about an actor the When does not name
    Given Alice has a balance of 10
    When Bob deposits 5
    Then Alice's balance is unchanged

  @id:q10_illtyped_step
  Scenario: a number where a ledger is needed
    Given ledger Main holds the balances [1, 2]
    When the total of ledger Main is computed
    Then the result is ledger Main

  @id:q11_unbound_step
  Scenario: an unknown word in a Then
    Given Alice has a balance of 10
    When Alice deposits 5
    Then Alice's balance is credited with 5

  @id:q1_illtyped_actor_for_number
  Rule: A deposit increases the wallet's balance by exactly the wallet

  @id:q2_illtyped_balances_for_number
  Rule: A batch never leaves the ledger below zero

  @id:q3_unbound_time_word
  Rule: A deposit eventually increases the wallet's balance by exactly the amount

  @id:q4_unbound_synonym
  Rule: A withdrawal never alters the wallet's balance

  @id:q5_two_domains
  Rule: A transfer is rejected and changes nothing

  @id:q6_two_domains_answers
  Rule: A transfer always answers

  @id:q7_answer_word_of_other_op
  Rule: A deposit is accepted only if there is a result
