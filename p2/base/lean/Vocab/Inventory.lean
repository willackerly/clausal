/-
THE GLOSSARY, Lean side, for the inventory crate. Hand-written and HUMAN-ASSERTED: each
definition is the intended meaning of one English phrase in ../../glossary.yaml.

Rule (checked by the audit): no definition here may mention a function of the generated
model (inventory.Warehouse.stock_of, inventory.Warehouse.take, ...). Types, constructors and
field projections are fine.

REFERENCE DEFINITIONS. A loop's exact result cannot be stated without saying what it should be.
Three definitions below are small pure references written for that purpose, each meant to be
obviously simpler than the Rust it describes (plain structural recursion or a sum over a list):
  * `stockIn` / `stock`  the units of one product, summed over all bins (no bound)
  * `takeFrom`           the bins after taking units of one product, earliest bins first
  * `fillFrom`           orders filled in turn; uses `stockIn` and `takeFrom`
Every other definition is a plain predicate on lists and numbers.
-/
import Generated.Inventory
import Bdd.Basic
open Aeneas Aeneas.Std

namespace IVocab
open inventory

deriving instance DecidableEq for Bin
deriving instance DecidableEq for Order

/-- The bins as plain pairs (product, units), bin 0 first. -/
def view (w : Warehouse) : List (Nat × Nat) := w.bins.val.map fun b => (b.product.val, b.qty.val)

/-- The orders as plain pairs (product, units), first order first. -/
def orderView (os : Slice Order) : List (Nat × Nat) := os.val.map fun o => (o.product.val, o.qty.val)

/-- REFERENCE. The units of product `p` in the bins `bs`, summed, as an unbounded natural number. -/
def stockIn (p : Nat) (bs : List (Nat × Nat)) : Nat := ((bs.filter fun b => b.1 = p).map (·.2)).sum

/-- The units of product `p` the warehouse holds in all bins together. -/
def stock (w : Warehouse) (p : U32) : Nat := stockIn p.val (view w)

/-- REFERENCE. The bins after taking `need` units of product `p`, earliest bins first: each bin of `p`, in
    order, gives as much as it holds of what is still needed. Bins of other products are left as they are. -/
def takeFrom (p : Nat) : Nat → List (Nat × Nat) → List (Nat × Nat)
  | _, [] => []
  | need, (q, u) :: rest =>
    if q = p then (q, u - min u need) :: takeFrom p (need - min u need) rest
    else (q, u) :: takeFrom p need rest

/-- REFERENCE. Orders (product, units) filled in turn from the bins: an order is filled when the bins hold at
    least its units of its product at that point, and filling it takes them with `takeFrom`; otherwise it is
    skipped. Returns (how many orders were filled, the bins afterwards). -/
def fillFrom : List (Nat × Nat) → List (Nat × Nat) → Nat × List (Nat × Nat)
  | bs, [] => (0, bs)
  | bs, (p, u) :: os =>
    if u ≤ stockIn p bs then
      let r := fillFrom (takeFrom p u bs) os
      (r.1 + 1, r.2)
    else fillFrom bs os

/-- Bin `b` holds product `p` and at least `n` units of it. -/
@[reducible] def binHolds (p : U32) (n : U64) (b : Bin) : Prop := b.product = p ∧ n.val ≤ b.qty.val

/-- How many bins hold product `p`. -/
def binsOf (w : Warehouse) (p : U32) : Nat := (w.bins.val.filter fun b => b.product = p).length

-- Givens
@[reducible] def holds (w : Warehouse) (bs : List Bin) : Prop := w.bins.val = bs
@[reducible] def stockFits (w : Warehouse) (p : U32) : Prop := stock w p ≤ U64.max
@[reducible] def stockTooBig (w : Warehouse) (p : U32) : Prop := U64.max < stock w p
@[reducible] def someBinHolds (w : Warehouse) (p : U32) (n : U64) : Prop := ∃ b ∈ w.bins.val, binHolds p n b
@[reducible] def noBinHolds (w : Warehouse) (p : U32) (n : U64) : Prop := ¬ ∃ b ∈ w.bins.val, binHolds p n b
/-- Product `p` is held by more than half of the bins. -/
@[reducible] def inMoreThanHalf (w : Warehouse) (p : U32) : Prop := w.bins.val.length < 2 * binsOf w p
/-- No product is held by more than half of the bins (a product held by no bin is held by none of them,
    so it is enough to look at the products the bins hold). -/
@[reducible] def noneInMoreThanHalf (w : Warehouse) : Prop :=
  ∀ b ∈ w.bins.val, ¬ w.bins.val.length < 2 * binsOf w b.product

-- Thens
@[reducible] def resultIsStock (o : Option U64) (w : Warehouse) (p : U32) : Prop := o.map (·.val) = some (stock w p)
@[reducible] def noCount (o : Option U64) : Prop := o = none
/-- The result is a bin number `i`; bin `i` holds at least `n` units of `p`, and no bin before it does. -/
def firstBinIs (o : Option Usize) (w : Warehouse) (p : U32) (n : U64) : Prop :=
  match o with
  | some i => (∃ b ∈ w.bins.val[i.val]?, binHolds p n b) ∧ ∀ b ∈ w.bins.val.take i.val, ¬ binHolds p n b
  | none => False
instance (o : Option Usize) (w : Warehouse) (p : U32) (n : U64) : Decidable (firstBinIs o w p n) := by
  unfold firstBinIs; split <;> infer_instance
@[reducible] def noBinFound (o : Option Usize) : Prop := o = none
/-- Same bins in the same order with the same products; each bin of `p` has gained `a` units, but holds
    no more than the maximum; every other bin is as it was. -/
@[reducible] def restocked (pre post : Warehouse) (p : U32) (a : U64) : Prop :=
  view post = (view pre).map fun (q, u) => (q, if q = p.val then min (u + a.val) U64.max else u)
@[reducible] def countIsBinsOf (n : Usize) (pre : Warehouse) (p : U32) : Prop := n.val = binsOf pre p
@[reducible] def takenIsMin (t : U64) (pre : Warehouse) (p : U32) (want : U64) : Prop :=
  t.val = min want.val (stock pre p)
@[reducible] def stockDownBy (t : U64) (pre post : Warehouse) (p : U32) : Prop := stock post p + t.val = stock pre p
@[reducible] def takenEarliestFirst (pre post : Warehouse) (p : U32) (want : U64) : Prop :=
  view post = takeFrom p.val want.val (view pre)
@[reducible] def filledCount (n : Usize) (pre : Warehouse) (os : Slice Order) : Prop :=
  n.val = (fillFrom (view pre) (orderView os)).1
@[reducible] def filledState (pre post : Warehouse) (os : Slice Order) : Prop :=
  view post = (fillFrom (view pre) (orderView os)).2
@[reducible] def filledAtMost (n : Usize) (os : Slice Order) : Prop := n.val ≤ os.val.length
/-- The number of different products among the bins (a product held in several bins counts once). -/
@[reducible] def differentProducts (n : Usize) (w : Warehouse) : Prop :=
  n.val = ((view w).map (·.1)).toFinset.card
@[reducible] def atMostBins (n : Usize) (w : Warehouse) : Prop := n.val ≤ w.bins.val.length
@[reducible] def resultIsProduct (o : Option U32) (p : U32) : Prop := o = some p
@[reducible] def noDominant (o : Option U32) : Prop := o = none

/-- Constructors used only to build concrete values for row evaluation, search and witnesses.
    A list too long for the machine (never the case for a literal) gives the empty value. -/
def mkWarehouse (bs : List Bin) : Warehouse :=
  if h : bs.length ≤ Usize.max then { bins := .from bs h } else { bins := .from [] (by simp) }
def mkOrders (os : List Order) : Slice Order :=
  if h : os.length ≤ Usize.max then .from os h else .from [] (by simp)

/-- NOT definitions: facts about the two constructors above, for the generated proof scripts
    (glossary `proof_hints.simp`). A literal list is always short enough. -/
theorem mkWarehouse_val (bs : List Bin) (h : bs.length ≤ 4294967295) : (mkWarehouse bs).bins.val = bs := by
  have : bs.length ≤ Usize.max := by scalar_tac
  simp [mkWarehouse, this]
theorem mkOrders_val (os : List Order) (h : os.length ≤ 4294967295) : (mkOrders os).val = os := by
  have : os.length ≤ Usize.max := by scalar_tac
  simp [mkOrders, this]

/-- Printing, for counterexample reports only. -/
def showWarehouse (w : Warehouse) : String := s!"bins {view w}"
def showCount (n : Usize) : String := s!"{n.val}"
def showU64 (n : U64) : String := s!"{n.val}"
def showOptU64 : Option U64 → String
  | some s => s!"Some({s.val})"
  | none => "None"
def showOptUsize : Option Usize → String
  | some s => s!"Some({s.val})"
  | none => "None"
def showOptU32 : Option U32 → String
  | some s => s!"Some({s.val})"
  | none => "None"

end IVocab
