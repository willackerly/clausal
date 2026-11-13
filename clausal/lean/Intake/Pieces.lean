/-
THE VOCABULARY, Lean side, for the sigintake crate (the fourth project, plan node W6): DOMAIN WORDS.
Hand-written and HUMAN-ASSERTED: each definition is the intended meaning of one domain word of the intake's
local book (../../clausebook/local/intake.yaml, kind `domain`). Modifiers and frames are not here: they are
shared, in lean/Frames.

  condition   on the expected key and the message              (`verifies`)
  measure     a quantity of the last counter                   (`last`)
  term        a value read off the message                     (`counterOf`)
  relation    between two calls                                (`unsignedDiffers`)
  answer      which returned values count as accepted          (`said`)
  operation   a `Frames.Op` bound to ONE function of the Aeneas-generated model through a fixed
              constructor of lean/Bdd/Ops.lean. Nothing else in this file may mention a model function.

`verifies` IS A STAND-IN. It is the toy relation the fixture's `verify` computes, written out without the code:
the tag is three hex digits, one each from the key, the payload and the counter. It is not a signature check, and
that a verifying tag was made by the holder of a key is the assumption A.sig.unforgeable (../../trust/assumptions.yaml),
which nothing here proves.

`mkKey`, `mkCounter`, `showKey` and `showCounter` are not vocabulary: they build and print concrete states for the
search scripts (glossary.yaml, `actors.sigkey`, `actors.sigcounter`).
-/
import Generated.Sigintake
import Bdd.Ops
open Aeneas Aeneas.Std

deriving instance DecidableEq for sigintake.Key
deriving instance DecidableEq for sigintake.Counter
deriving instance DecidableEq for sigintake.Message

namespace In
open sigintake

/-- "the signature of <message> verifies under <key>" (STAND-IN): the tag is the toy tag of the payload and the counter under the key. -/
@[reducible] def verifies (k : Key) (m : Message) : Prop :=
  m.tag.val = (k.id.val % 16) * 256 + (m.payload.val % 16) * 16 + m.counter.val % 16

/-- "the last counter": the number it holds. -/
@[reducible] def last (c : Counter) : Nat := c.last.val

/-- "the counter of <message>": the counter written in it. -/
@[reducible] def counterOf (m : Message) : Nat := m.counter.val

/-- "is accepted" for an operation that answers yes or no: it answered yes. -/
@[reducible] def said (r : Bool) : Prop := r = true

/-- "only the unsigned part of the message differs": the same expected key and last counter, and a message with the same payload, counter and tag. -/
@[reducible] def unsignedDiffers : Frames.Variation (Key × Counter) Message :=
  fun s a s₂ a₂ => s₂ = s ∧ a₂.payload = a.payload ∧ a₂.counter = a.counter ∧ a₂.tag = a.tag

/-- "intake": state = (the expected key, the last counter), input = the message. -/
@[reducible] def intake : Frames.Op (Key × Counter) Message Bool := Bdd.opMut2 sigintake.intake said

/-- Constructors used only to build concrete states for search and witnesses. -/
@[simp] def mkKey (n : U64) : Key := { id := n }
@[simp] def mkCounter (n : U64) : Counter := { last := n }

/-- Printing, for counterexample reports only. -/
def showKey (k : Key) : String := s!"key {k.id.val}"
def showCounter (c : Counter) : String := s!"last {c.last.val}"

end In
