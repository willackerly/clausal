Feature: Signed message intake on a toy verifier
  The fourth project (plan node W6, trust test 1): sigintake/src/lib.rs, declared in projects.yaml. The Rule lines are the
  signed-message rules SM-1, 2, 3, 5, 8, 9 and SM-10 as frozen in trust/test1/rules.txt (commit 09966fe), each compiled from
  the pieces of core and of the local book clausebook/local/intake.yaml alone. The verifier of this fixture is a toy with
  a body: NOTHING HERE IS A STATEMENT ABOUT A SIGNATURE SCHEME. The word "the signature of the message verifies under the
  expected key" rests on the ledger entry A.sig.unforgeable (trust/assumptions.yaml), a stand-in.
  Expected verdicts were written down before the pipeline was run on these lines (trust/FREEZE-w46.md).

  # SM-1
  @id:always_answers
  Rule: An intake always answers

  # SM-2 (usage condition U1 of A.sig.unforgeable)
  @id:accept_only_if_verified
  Rule: An intake is accepted only if the signature of the message verifies under the expected key

  # SM-3 (usage condition U2)
  @id:unverified_rejected_unchanged
  Rule: An intake for which the signature of the message does not verify under the expected key is rejected and changes nothing

  # SM-5 (usage condition U3)
  @id:unsigned_part_ignored
  Rule: An intake gives the same answer when only the unsigned part of the message differs

  # SM-8
  @id:accept_only_if_counter_above
  Rule: An intake is accepted only if the counter of the message is more than the last counter

  # SM-9 exactly as frozen. It says "successful", a form the book retired for "accepted" (core.yaml, `successful`, Q4):
  # expected to be refused, with the live form named.
  @id:counter_set_frozen_wording @expect-unbound
  Rule: For a successful intake, the last counter is now the counter of the message

  # SM-9 with that one word replaced by the live form the book names
  @id:counter_set
  Rule: For an accepted intake, the last counter is now the counter of the message

  # SM-10, in the wording W0 composed from `tied` / "the same input"
  @id:same_message_again_rejected
  Rule: An intake followed by an intake with the same input is always rejected
