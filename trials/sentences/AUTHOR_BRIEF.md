# Writing rules for the ledger and the wallet: brief for an author

Thank you for helping. This takes about 45 minutes. You need no tools and no knowledge of how the code is built. Please do not look at any other file of this project first: the point is to see what rules people write when they have **not** seen the tool's vocabulary.

## The code you are writing rules about

Two small pieces of money-handling code. Amounts and balances are whole numbers from 0 up to a fixed maximum (18,446,744,073,709,551,615, the largest unsigned 64-bit number). Nothing can be negative or above the maximum.

**The wallet.** A wallet holds one balance. *Deposit* adds an amount; if the new balance would be above the maximum, the deposit is rejected. *Withdraw* takes an amount off; if the amount is more than the balance, it is rejected. A *wallet transfer* moves an amount from a sender wallet to a different receiver wallet; it is rejected if the sender has less than the amount or if the receiver's balance would go above the maximum.

**The ledger.** A ledger is a list of balances, one per account, numbered from 0. A *transfer* names a sender account, a receiver account and an amount. The ledger accepts it and moves the money when both accounts exist, they are different, the sender's balance is at least the amount, and the receiver's balance plus the amount is at most the maximum; otherwise it rejects it. A *batch* is a list of transfers applied in order: it stops at the first transfer that is rejected, keeps the ones already applied, and reports how many it applied. *Applying a batch as a whole* is all or nothing: either every transfer is applied or none is. *Computing the total* adds up all the balances and gives nothing if the sum is above the maximum. *Looking up* an account gives its balance, or nothing if there is no such account.

## What to write

**Twelve rules**, each one English sentence, saying something this code should always do or never do. Write them the way you would in a design document or a code review, in your own words.

- About **nine** should be rules you believe are **true** of code that works as described.
- About **three** should be rules that sound reasonable but are **false** of it (a rule a careless colleague might write down). Mark which are which.
- Spread them out: some about a single transfer, some about batches, some about totals or lookups, one or two about the wallet if you like.
- One sentence each. If you need "and", that is fine.

## For each rule, before anything else: five cases

Under each rule write **five concrete cases** that show what you mean: actual balances, an actual operation, and what you expect. For each case say one of:

- **the rule holds here** (and what happens),
- **the rule is false here** (for your false rules: the case that breaks it), or
- **the rule does not apply here** (a case someone might think is covered and is not).

Include the edge you care about most (exactly at the limit, a missing account, an empty batch, an amount of zero). You may use a small maximum such as 100 in your cases to keep the numbers readable; say so in the case.

The cases are the record of what you meant. They are written **before** you see how any tool reads your sentence, and they are not changed afterwards.

## What to send back

One file, in any of these forms: the filled-in `author_template.json`, or a plain text file with, for each rule, the sentence, "meant true" or "meant false", and the five cases. Use a name or a pseudonym; it appears in the results.

## What happens next

Your sentences are given, unchanged, to a tool that tries to read them using a fixed vocabulary, and your cases are used to check whether its reading is the one you meant. A sentence the tool cannot read is a result about the tool, not about your sentence. There are no right answers and nothing is scored against you.
