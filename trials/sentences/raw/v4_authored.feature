Feature: V4 authored
  Rules written by proxy authors (models), reworded by the trial runner so that they compile. Scratch copy only.

  @id:t_total
  Rule: A transfer never changes the total of all balances of the ledger

  @id:t_total_ok
  Rule: A successful transfer never changes the total of all balances of the ledger

  @id:t_moved
  Rule: For a successful transfer, the amount of the transfer has moved between its accounts in the ledger and no other balance changed

  @id:t_rej
  Rule: A rejected transfer never changes the ledger

  @id:t_valid
  Rule: A transfer is accepted exactly when the transfer is valid on the ledger

  @id:t_short
  Rule: A transfer for which the amount of the transfer is more than the balance of account the sender of the transfer of the ledger is always rejected

  @id:t_only
  Rule: For a successful transfer, of the accounts of the ledger, only the sender of the transfer and the receiver of the transfer change

  @id:t_over
  Rule: A transfer for which the balance of account the receiver of the transfer of the ledger plus the amount of the transfer exceeds the maximum is always rejected

  @id:b_step
  Rule: A batch agrees with its transfers applied one at a time until one is rejected

  @id:b_whole
  Rule: A batch applied as a whole agrees with the same batch applied transfer by transfer and kept only if every transfer is applied

  @id:b_whole_ok
  Rule: A successful batch applied as a whole agrees with the same batch applied transfer by transfer and kept only if every transfer is applied

  @id:b_count
  Rule: For a batch, the number of transfers applied is at most the length of the batch

  @id:b_count_step
  Rule: For a batch, the number of transfers applied is at most the length of the batch, and a batch agrees with its transfers applied one at a time until one is rejected

  @id:l_both
  Rule: For a lookup for which the account is not an account of the ledger, there is no result, and for a lookup, the result is the balance of the account in the ledger

  @id:l_zero
  Rule: For a lookup for which the balance of account the account of the ledger is zero, there is no result

  @id:total_always
  Rule: A computation of the total is always accepted

  @id:total_fits
  Rule: A computation of the total is accepted exactly when the total of the balances of the ledger is at most the maximum

  @id:l_both_total_fits
  Rule: For a lookup for which the account is not an account of the ledger, there is no result, and for a lookup, the result is the balance of the account in the ledger, and a computation of the total is accepted exactly when the total of the balances of the ledger is at most the maximum

  @id:w_total
  Rule: A transfer never changes the total of all balances

  @id:w_total_ok
  Rule: Any successful transfer never changes the total of all balances
