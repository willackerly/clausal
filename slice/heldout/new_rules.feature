# FIVE NEW RULES about the ledger that are in no fixture, written with the words of vocabulary.yaml as it
# stood when the frame library was finished. They are compiled by `python3 -m slicegen compile` (run.sh does
# it as an informational step): no entry of the vocabulary was added or changed for them. What each compiled
# to, and what happened to it, is in out/report.md under "New sentences".
#
# They were written by the builder of the vocabulary, in one go, WITHOUT running the compiler on drafts; the
# first-attempt wording is kept even where it does not compile. So this is not the held-out test of plan
# node V4 (authors who do not know the vocabulary); it shows what a new sentence costs someone who does.
Feature: New rules about the ledger

  @id:n1_internal_transfer
  Rule: An internal transfer never changes the total of all balances of the ledger

  @id:n2_accepted_only_if_covered
  Rule: A transfer is accepted only if the amount of the transfer is not more than the balance of account the sender of the transfer of the ledger

  @id:n3_lookup_missing_account
  Rule: For a lookup for which the account is not an account of the ledger, there is no result

  @id:n4_total_stays_within_maximum @expect-refuted
  Rule: A batch never leaves the total of all balances of the ledger above the maximum

  @id:n5_stopped_at_invalid
  Rule: For a batch, every transfer at which the batch stopped is not valid on the ledger afterwards
