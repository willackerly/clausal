Feature: Reviewer's candidate rule lines

  @id:withdrawal_v2
  Rule: A withdrawal always answers, and a successful withdrawal decreases the wallet's balance by exactly the amount, and a rejected withdrawal never changes the wallet's balance

  @id:deposit_v2
  Rule: A deposit always answers, and a successful deposit increases the wallet's balance by exactly the amount, and a rejected deposit never changes the wallet's balance

  @id:total_value
  Rule: For a computation of the total for which the total of the balances of the ledger is at most the maximum, the result is the total of the balances of the ledger

  @id:whole_complete
  Rule: For a successful batch applied as a whole, every transfer of the batch is applied
