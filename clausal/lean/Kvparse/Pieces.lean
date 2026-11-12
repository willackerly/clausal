/-
THE VOCABULARY, Lean side, for the kvparse crate (the fourth project, plan node K1): DOMAIN WORDS.
Hand-written and HUMAN-ASSERTED: each definition is the intended meaning of one domain word of the parser's local
book (../../clausebook/local/kvparse.yaml, kind `domain`). Modifiers and frames are not here: they are shared, in
lean/Frames.

Rule (as for the ledger): apart from the operation at the end, nothing here may mention a function of the generated
model. THE FORMAT IS WRITTEN OUT AGAIN HERE, on plain lists of numbers (the bytes of the input): it is the
specification, not the code. It is a second parser by the same author as the first.

  the format     a record is one or two fields separated by `;` (59). A field is three bytes: a key, `=` (61), one
                 decimal digit (48 to 57). The keys are `a` (97) and `b` (98); each at most once, `a` before `b`.

`mkInput`, `mkParser`, `showParser` are not vocabulary: they build and print concrete values for the search scripts
(glossary.yaml, `param_types.bytes`, `actors.parser`).
-/
import Generated.Kvparse
import Bdd.Ops
open Aeneas Aeneas.Std

deriving instance DecidableEq for kvparse.Record
deriving instance DecidableEq for kvparse.Parser

namespace KV
open kvparse

-- the input and its parts, read before the call (a tokeniser inside the specification)
/-- the bytes of an input, as numbers -/
@[reducible] def bytes (i : Slice U8) : List Nat := i.val.map (·.val)
/-- "the length of the input", in bytes -/
@[reducible] def length (i : Slice U8) : Nat := i.val.length
/-- the pieces of a list of bytes between its `;` (a list with no `;` is one piece) -/
def split : List Nat → List (List Nat)
  | [] => [[]]
  | b :: bs =>
    if b = 59 then [] :: split bs
    else match split bs with
      | f :: fs => (b :: f) :: fs
      | [] => [[b]]
/-- "the fields of the input": what stands between its `;`, in order. The empty input has no field. -/
def fields (i : Slice U8) : List (List Nat) := if bytes i = [] then [] else split (bytes i)
/-- the key of a field: its bytes before the first `=` -/
def keyOf (f : List Nat) : List Nat := f.takeWhile (· ≠ 61)
/-- "the keys of the input": the key of every field, in order, with repetitions -/
def keys (i : Slice U8) : List (List Nat) := (fields i).map keyOf
/-- "is a known field": its key is `a` or `b` -/
def known (f : List Nat) : Prop := keyOf f = [97] ∨ keyOf f = [98]
instance (f : List Nat) : Decidable (known f) := by unfold known; infer_instance
/-- "is repeated in the input": the key is the key of more than one field -/
def repeated (i : Slice U8) (k : List Nat) : Prop := 2 ≤ (keys i).count k
instance (i : Slice U8) (k : List Nat) : Decidable (repeated i k) := by unfold repeated; infer_instance
/-- a field of the format: a known key, `=`, one decimal digit, and nothing else -/
def shaped (f : List Nat) : Prop :=
  match f with
  | [k, e, d] => (k = 97 ∨ k = 98) ∧ e = 61 ∧ 48 ≤ d ∧ d ≤ 57
  | _ => False
instance (f : List Nat) : Decidable (shaped f) := by
  unfold shaped
  split <;> infer_instance
/-- "the input is well-formed": it is a record of the format. Every field is a field of the format, and the keys are
    `a`, or `b`, or `a` then `b` (so: at least one field, no key twice, `a` before `b`). The size limit is NOT part of
    this word: it is a quantity of the parser, said separately. -/
def wellFormed (i : Slice U8) : Prop :=
  (∀ f ∈ fields i, shaped f) ∧ (keys i = [[97]] ∨ keys i = [[98]] ∨ keys i = [[97], [98]])
instance (i : Slice U8) : Decidable (wellFormed i) := by unfold wellFormed; infer_instance

-- the parser
/-- "the parser's size limit": the longest input it accepts, in bytes -/
@[reducible] def limit (p : Parser) : Nat := p.limit.val
/-- "the field limit": the largest number of fields a record has -/
@[reducible] def fieldLimit : Nat := 2

-- answers
/-- "accepted" for a parse: it answers a record. -/
@[reducible] def found (o : Option Record) : Prop := o ≠ none
/-- "the number of fields of the result": how many keys the answered record gives (0 if there is no record) -/
def count (o : Option Record) : Nat :=
  match o with
  | some r => (if r.has_a then 1 else 0) + (if r.has_b then 1 else 0)
  | none => 0
/-- a record written back in the format: the specification's own encoder -/
def encode (r : Record) : List Nat :=
  (if r.has_a then [97, 61, 48 + r.a.val] else []) ++ (if r.has_a ∧ r.has_b then [59] else [])
    ++ (if r.has_b then [98, 61, 48 + r.b.val] else [])
/-- "the encoding of the result": the answered record written back in the format (absent if there is no record) -/
def encoding (o : Option Record) : Option (List Nat) := o.map encode
/-- an input standing where an encoding is wanted: its bytes -/
@[reducible] def asEncoding (i : Slice U8) : Option (List Nat) := some (bytes i)

-- the reference parse: the whole answer for every input, written without the code
/-- a number as a byte (0 if it is not one; never the case for a digit's value) -/
def byte (n : Nat) : U8 := if h : n ≤ U8.max then U8.ofNatCore n (by scalar_tac) else 0#u8
/-- the digit value of the field with key `k` among the fields, if there is one -/
def valueOf (fs : List (List Nat)) (k : Nat) : Option Nat :=
  (fs.find? (fun f => f.head? = some k)).map (fun f => f.getD 2 48 - 48)
/-- the record a well-formed input stands for -/
def recordOf (i : Slice U8) : Record :=
  let fs := fields i
  { has_a := (valueOf fs 97).isSome, a := byte ((valueOf fs 97).getD 0),
    has_b := (valueOf fs 98).isSome, b := byte ((valueOf fs 98).getD 0) }
/-- "the reference parse": the record of the input if the input is within the parser's limit and well-formed,
    otherwise no record; the parser left as it was. -/
def refParse : Frames.Term Parser (Slice U8) (Option Record × Parser) := fun p i =>
  (if length i ≤ limit p ∧ wellFormed i then some (recordOf i) else none, p)

-- the operation (the only definition that mentions the generated model)
/-- "an input is parsed": state = the parser (read, never changed), input = the bytes, answer = the record or none. -/
@[reducible] def parse : Frames.Op Parser (Slice U8) (Option Record) := Bdd.opRead kvparse.Parser.parse found

/-- How an input written out for the search (`"a=1;b=2"`) becomes a value: the UTF-8 bytes of the text. A text too long
    for the machine (never the case for a literal) gives the empty input. -/
def mkInput (s : String) : Slice U8 :=
  let bs : List U8 := s.toUTF8.toList.map (fun b => byte b.toNat)
  if h : bs.length ≤ Usize.max then .from bs h else .from [] (by simp)
/-- Constructor used only to build concrete parsers for search and witnesses. -/
@[simp] def mkParser (n : Usize) : Parser := { limit := n }
/-- Printing, for counterexample reports only. -/
def showParser (p : Parser) : String := s!"limit {p.limit.val}"

end KV
