# Reviewer's sentences (V2/V3 review, second pass). Each is written so that its NATURAL English reading
# differs from what the composition rules produce. Not part of any fixture.
Feature: Natural readings that differ

  @id:r1_scope
  Rule: For a batch for which every transfer of the batch is not valid on the ledger, no transfer is applied

  @id:r2_whenever
  Rule: A withdrawal is accepted whenever the amount is not more than the wallet's balance

  @id:r3_timing
  Rule: A batch applied as a whole is accepted exactly when every transfer of the batch is valid on the ledger

  @id:r4_rejected_batch
  Rule: A rejected batch never changes the total of all balances of the ledger
