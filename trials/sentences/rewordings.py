"""V4 rewordings, written by the trial runner (a model, not a person) after reading the vocabulary.

For each authored rule that did not compile as written: the smallest rewording found that compiles and keeps the author's
meaning as shown by their five cases, or None when no existing composition says it, with the missing piece named generically.

  text      the reworded Rule line (None: no rewording keeps the meaning)
  fit       exact     the compiled reading says what the sentence says, as far as the five cases show
            more      it says more than the sentence (named in `note`), consistently with all five cases
            less      it says only part of the sentence: `missing` names the piece the rest would need
  missing   generic names of the pieces that would be needed (for text None, or for the dropped part when fit is less)
"""
T_TOTAL = "A transfer never changes the total of all balances of the ledger"
T_TOTAL_OK = "A successful transfer never changes the total of all balances of the ledger"
T_MOVED = "For a successful transfer, the amount of the transfer has moved between its accounts in the ledger and no other balance changed"
T_REJ = "A rejected transfer never changes the ledger"
T_VALID = "A transfer is accepted exactly when the transfer is valid on the ledger"
B_STEP = "A batch agrees with its transfers applied one at a time until one is rejected"
B_WHOLE = "A batch applied as a whole agrees with the same batch applied transfer by transfer and kept only if every transfer is applied"
B_WHOLE_OK = "A successful batch applied as a whole agrees with the same batch applied transfer by transfer and kept only if every transfer is applied"
B_COUNT = "For a batch, the number of transfers applied is at most the length of the batch"
L_BOTH = "For a lookup for which the account is not an account of the ledger, there is no result, and for a lookup, the result is the balance of the account in the ledger"
TOTAL_FITS = "a computation of the total is accepted exactly when the total of the balances of the ledger is at most the maximum"

# generic names of missing pieces (kind: name)
P_TERM_EQ = "modifier: comparison between two values known before the call (X is Y / X is not Y, for two parties or for an amount and a number)"
P_COND_AND = "modifier: conjunction of two conditions (for which A and B)"
P_EVERY_PART = "modifier: 'every <part> of <state>' inside a claim about a quantity (every balance is at most ...)"
P_INVARIANT = "frame: holds after any sequence of any operations (invariant of the state)"
P_SEQ_TIED = "modifier: a sequence of calls whose inputs are tied to each other (the same input again, the reverse, the two in the other order)"
P_SEQ_COMPARE = "frame: compare the answers or final states of two sequences / of the two calls of a sequence"
P_OTHER_OP_COND = "domain word: a condition that names what ANOTHER operation of the same code answers on the same input"
P_ANSWER_COND = "modifier: scope a claim by a class of answers other than accepted / rejected (if <answer class>, ...)"
P_ANSWER_CLASS = "domain word: an answer class for the operation ('stopped early')"
P_REFERENCE = "domain word: a further reference function"
P_MEASURE = "domain word: a further measure of the state"
P_RESULT_TERM = "modifier: a quantity of the state before the call used as the expected result (the result is <measure>)"
P_SUM_IS = "modifier: an exact-sum condition (X plus Y is Z)"

R = {
 # ---------------------------------------------------------------- opus-1
 "opus-1/r1": dict(text=T_TOTAL, fit="exact",
    note="'whether it is accepted or rejected' is default D2 and is printed in the echo. Dropping only the words the grammar has no place for "
         "('Applying a single', the whether-clause) gives 'A transfer never changes the total of all balances', which COMPILES AS THE WALLET'S transfer; "
         "'of the ledger' is what selects the ledger operation (see the probes)."),
 "opus-1/r2": dict(text=T_MOVED, fit="exact", note="said with the idiom i.moved (three frames: decreased by, increased by, changes only)"),
 "opus-1/r3": dict(text=None, missing=[P_TERM_EQ], note="'from an account to itself': no condition compares the sender with the receiver"),
 "opus-1/r4": dict(text="A transfer for which the amount of the transfer is more than the balance of account the sender of the transfer of the ledger is always rejected",
    fit="exact", note="the author's third and fifth cases (accepted at equality; nothing changes after a rejection) go beyond the sentence, in either wording"),
 "opus-1/r5": dict(text=None, missing=[P_INVARIANT, P_EVERY_PART], note="every balance is a u64 and the maximum is 2^64 - 1 in the fixture, so the rule cannot be false there"),
 "opus-1/r6": dict(text=B_COUNT + ", and a batch agrees with its transfers applied one at a time until one is rejected", fit="more",
    note="'the first that many transfers are exactly those that took effect' is read as agreement with the transfers applied one at a time; that reference also fixes the reported count"),
 "opus-1/r7": dict(text=B_WHOLE, fit="more",
    note="the sentence is an either/or that does not say when each side applies; the reading says when (accepted and applied iff every transfer applies in order). No either/or frame exists"),
 "opus-1/r8": dict(text=L_BOTH, fit="exact"),
 "opus-1/r9": dict(text=None, missing=[P_SEQ_TIED], note="'a deposit followed by a withdrawal' is refused: both operations call their input 'the amount', and nothing says the two amounts are the same"),
 "opus-1/r10": dict(text=None, missing=[P_OTHER_OP_COND], note="a condition on what the whole-batch operation answers, inside a rule about the step-by-step one"),
 "opus-1/r11": dict(text="A computation of the total is always accepted", fit="more",
    note="'as long as every individual balance is within the maximum' is dropped: no piece says it (" + P_EVERY_PART + "), and in the fixture it is true of every ledger (u64 balances, maximum 2^64 - 1)",
    missing=[P_EVERY_PART]),
 "opus-1/r12": dict(text=None, missing=[P_SEQ_TIED], note="'the reverse transfer of the same amount ... right after'"),
 # ---------------------------------------------------------------- sonnet-1
 "sonnet-1/R1": dict(text=T_TOTAL, fit="exact"),
 "sonnet-1/R2": dict(text=T_MOVED, fit="exact"),
 "sonnet-1/R3": dict(text=T_REJ, fit="exact"),
 "sonnet-1/R4": dict(text=T_VALID, fit="exact", note="the four listed conditions are the one domain word 'is valid on the ledger'; the echo spells them out"),
 "sonnet-1/R5": dict(text=None, missing=[P_EVERY_PART], note="also 'any transfer or batch' would be two clauses; cannot be false in the fixture (u64)"),
 "sonnet-1/R6": dict(text=B_STEP, fit="exact"),
 "sonnet-1/R7": dict(text=B_WHOLE, fit="exact"),
 "sonnet-1/R8": dict(text=B_WHOLE_OK, fit="less",
    note="the author's condition ('every transfer is acceptable in sequence') has no piece; 'successful' scopes by the ANSWER of the whole-batch call instead, so a "
         "whole-batch operation that wrongly rejects is not caught by this reading", missing=["domain word: a condition 'every transfer of the batch can be applied in order'"]),
 "sonnet-1/R9": dict(text=L_BOTH + ", and " + TOTAL_FITS, fit="less",
    note="'the total is the sum of all balances' is not said: the reading only says when the computation is accepted", missing=[P_RESULT_TERM]),
 "sonnet-1/R10": dict(text=None, missing=[P_TERM_EQ, P_COND_AND], note="'of zero', 'a different account': no comparison of the amount with a number or of the two parties; and two conditions at once"),
 "sonnet-1/R11": dict(text=None, missing=[P_SEQ_TIED, P_SEQ_COMPARE]),
 "sonnet-1/R12": dict(text=None, missing=[P_SEQ_TIED]),
 # ---------------------------------------------------------------- haiku-1
 "haiku-1/R01": dict(text=T_TOTAL_OK, fit="exact"),
 "haiku-1/R02": dict(text=T_REJ, fit="exact"),
 "haiku-1/R03": dict(text=None, missing=[P_TERM_EQ]),
 "haiku-1/R04": dict(text=None, missing=[P_INVARIANT, P_EVERY_PART], note="cannot be false in the fixture (u64)"),
 "haiku-1/R05": dict(text=B_WHOLE, fit="exact"),
 "haiku-1/R06": dict(text=B_STEP, fit="more", note="the reference also fixes the ledger the call leaves; the author's cases give final balances, so they intend it"),
 "haiku-1/R07": dict(text=L_BOTH, fit="exact"),
 "haiku-1/R08": dict(text=B_WHOLE_OK, fit="exact",
    note="exact on correct code only: the reference is another operation of the same code (apply_batch), where the author wrote 'applying its transfers one at a time'; the reading is a relation between two code operations, and a mistake they share is not seen (review finding)"),
 "haiku-1/R09": dict(text="For a successful transfer, of the accounts of the ledger, only the sender of the transfer and the receiver of the transfer change", fit="exact",
    note="'changes exactly two balances' is read as 'no other balance changes': the author's fourth case (amount 0, nothing changes) is meant to satisfy the rule"),
 "haiku-1/R10": dict(text="A transfer for which the balance of account the receiver of the transfer of the ledger plus the amount of the transfer exceeds the maximum is always rejected",
    fit="less", note="the second half ('a receiving balance that lands exactly on the maximum is accepted') is dropped: it needs an exact-sum condition, and it is true only "
                     "together with the other conditions of acceptance, which need a conjunction", missing=[P_SUM_IS, P_COND_AND]),
 "haiku-1/R11": dict(text=None, missing=[P_REFERENCE], note="a reference 'the batch applied skipping rejected transfers' (the rule is meant false)"),
 "haiku-1/R12": dict(text="For a lookup for which the balance of account the account of the ledger is zero, there is no result", fit="exact",
    note="'the balance of account the account of the ledger' reads a missing account as 0, so the missing-account lookups are in scope too, as the sentence's 'the same as a missing account' has it"),
 # ---------------------------------------------------------------- default-1
 "default-1/R01": dict(text=T_TOTAL_OK, fit="exact"),
 "default-1/R02": dict(text=T_REJ, fit="exact"),
 "default-1/R03": dict(text=T_MOVED, fit="exact"),
 "default-1/R04": dict(text=None, missing=[P_TERM_EQ]),
 "default-1/R05": dict(text=None, missing=[P_EVERY_PART], note="cannot be false in the fixture (u64)"),
 "default-1/R06": dict(text=B_COUNT, fit="exact"),
 "default-1/R07": dict(text=B_WHOLE, fit="exact"),
 "default-1/R08": dict(text=None, missing=[P_MEASURE], note="'the number of accounts' (or the set of accounts) as a quantity that never changes; also two operations, so two clauses"),
 "default-1/R09": dict(text=T_VALID, fit="exact"),
 "default-1/R10": dict(text=None, missing=[P_TERM_EQ], note="'of amount zero': the amount is a value of the input, and the only comparisons are between a state quantity and a value"),
 "default-1/R11": dict(text=None, missing=[P_ANSWER_COND, P_ANSWER_CLASS], note="'stops early' is a property of the answer of an operation that never rejects"),
 "default-1/R12": dict(text=None, missing=[P_SEQ_TIED, P_SEQ_COMPARE]),
}

# Probes: the smallest compiling rewordings that do NOT keep the author's meaning (reported, not counted).
PROBES = {
 "opus-1/r1": dict(text="A transfer never changes the total of all balances",
    note="the author's sentence with only the words the grammar has no place for removed. Compiles, as the WALLET's two-party transfer"),
 "haiku-1/R01": dict(text="Any successful transfer never changes the total of all balances",
    note="'Applying' dropped, accepted -> successful, 'leaves ... unchanged' -> 'never changes ...'. Compiles, as the WALLET's two-party transfer"),
}
