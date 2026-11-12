Feature: Wallet rules
  NEW SENTENCES about the wallet (plan node L2). No Rule line in this file has an entry in the old whole-phrase
  glossary (glossary.yaml), a scenario beneath it, a hand-written cucumber step or a hand-written Rust predicate.
  Each is compiled from the pieces of the Clausebook (clausebook/) and gets its verdict the way the Rule lines of
  features/ledger_rules.feature do.

  # `tied`: a sequence of two calls in which the second is given the first call's input ("with the same input").
  # Without the tie the subject is refused: a deposit and a withdrawal both call their input "the amount".
  @id:l2_deposit_then_withdraw_answers
  Rule: A deposit followed by a withdrawal with the same input always answers

  @id:l2_deposit_then_withdraw_restores @expect-refuted
  Rule: A deposit followed by a withdrawal with the same input never changes the wallet's balance
    Deliberately false, and it sounds right: a deposit a full wallet has no room for is rejected, and the
    withdrawal of the same amount that follows it is not.
