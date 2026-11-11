"""The authors' five cases per rule, encoded as inputs of the compiled reading by the trial runner (a model).

One entry per case, in the author's order:  C(unit, values, expect, ans, after, note, scaled, chosen)
  unit     which unique reading the case is put to (see work/unique_ids.json); most rules have one
  values   {variable: literal} for the generated replay (`rule-evidence --replay`), or None: NOT ENCODABLE (note says why)
  expect   what the author says of the RULE at this case: 'holds', 'fails', or 'silent' (the rule does not apply here)
  ans      the outcome the author states, if any: True/False (accepted/rejected), a count, a looked-up value, 'none' (no result)
  after    the balances the author states afterwards, if any
  scaled   the author used an illustrative maximum (100, 1000, ...); the fixture's maximum is 2^64 - 1, so the balance whose
           headroom matters is moved to the same distance below 2^64 - 1 (the stated `after` is then not compared)
  chosen   the author left a balance, amount or account open and the runner chose one
M is 2^64 - 1. Accounts A, B, C, ... are 0, 1, 2, ...; a missing account is a number past the end.
"""
M = 18446744073709551615

def C(unit, values, expect="holds", ans=None, after=None, note="", scaled=False, chosen=False):
    if values:
        values = {k: v.replace("M-", "M - ") for k, v in values.items()}
        out = {}
        for k, v in values.items():
            import re
            v = re.sub(r"M - (\d+)", lambda m: str(M - int(m.group(1))), v)
            out[k] = v.replace("M", str(M))
        values = out
    return dict(unit=unit, values=values, expect=expect, ans=ans, after=after, note=note, scaled=scaled, chosen=chosen)

def T(l, t): return {"the_ledger": l, "the_transfer": t}
def B(l, b): return {"the_ledger": l, "the_batch": b}
def L(l, a): return {"the_ledger": l, "the_account": a}
def S(l): return {"the_ledger": l}
def W(s, r, a): return {"the_sender": s, "the_receiver": r, "the_amount": a}

CASES = {
 "opus-1/r1": [
  C("T_TOTAL", T("[50, 30]", "0->1:20")),
  C("T_TOTAL", T("[50, 30]", "0->1:60"), ans=False),
  C("T_TOTAL", T("[0, 0, 10]", "2->0:10")),
  C("T_TOTAL", T("[10, M-5]", "0->1:10"), ans=False, scaled=True),
  C("T_TOTAL", T("[50, 30]", "0->9:1"), chosen=True, note="balances and amount chosen; account 9 is the missing one"),
 ],
 "opus-1/r2": [
  C("T_MOVED", T("[50, 30, 7]", "0->1:20"), after=[30, 50, 7]),
  C("T_MOVED", T("[5, 0]", "0->1:5"), after=[0, 5]),
  C("T_MOVED", T("[100, 0, 1]", "0->1:1"), after=[99, 1, 1]),
  C("T_MOVED", T("[3, 4]", "0->1:0"), after=[3, 4]),
  C("T_MOVED", T("[40, M-40]", "0->1:40"), ans=True, scaled=True),
 ],
 "opus-1/r4": [
  C("T_SHORT", T("[10, 0]", "0->1:11"), ans=False),
  C("T_SHORT", T("[0, 0]", "0->1:1"), ans=False),
  C("T_SHORT", T("[10, 0]", "0->1:10"), ans=True, note="'accepted (must happen)': the author states the boundary; the sentence itself is silent at equality"),
  C("T_SHORT", T("[99, 0]", "0->1:100"), ans=False),
  C("T_SHORT", T("[10, 0]", "0->1:11"), ans=False, after=[10, 0], note="'after rejection A=10 and B=0 still': the same input as case 1; that nothing changes is not in the sentence"),
 ],
 "opus-1/r6": [
  C("B_COUNT_STEP", B("[10, 0]", "[0->1:1, 0->1:1, 0->1:1]"), ans=3, chosen=True),
  C("B_COUNT_STEP", B("[10, 0]", "[0->1:1, 0->1:20, 0->1:1]"), ans=1, chosen=True),
  C("B_COUNT_STEP", B("[10, 0]", "[]"), ans=0, chosen=True),
  C("B_COUNT_STEP", B("[10, 0]", "[0->1:20, 0->1:1]"), ans=0, after=[10, 0], chosen=True),
  C("B_COUNT_STEP", B("[10, 0]", "[0->1:1, 0->1:1, 0->1:1, 0->1:20]"), ans=3, chosen=True),
 ],
 "opus-1/r7": [
  C("B_WHOLE", B("[50, 0]", "[0->1:20, 1->0:5]"), after=[35, 15]),
  C("B_WHOLE", B("[50, 0]", "[0->1:20, 0->1:40]"), ans=False, after=[50, 0]),
  C("B_WHOLE", B("[50, 0]", "[]"), ans=True, after=[50, 0], chosen=True),
  C("B_WHOLE", B("[10, 0, 0]", "[0->1:10, 1->2:10]"), ans=True, chosen=True),
  C("B_WHOLE", B("[50, 0]", "[0->0:1]"), ans=False, after=[50, 0], chosen=True),
 ],
 "opus-1/r8": [
  C("L_BOTH", L("[5]", "9"), ans="none"),
  C("L_BOTH", L("[5]", "0"), ans=5),
  C("L_BOTH", L("[]", "0"), ans="none"),
  C("L_BOTH", L("[3, 2]", "1"), ans=2, note="the ledger after the author's transfer of 2 on [5, 0]"),
  C("L_BOTH", L("[5, 0]", "0"), ans=5, chosen=True, note="the ledger a rejected transfer leaves is the ledger before it"),
 ],
 "opus-1/r11": [
  C("TOTAL_ALWAYS", S("[M, M]"), expect="fails", ans="none"),
  C("TOTAL_ALWAYS", S("[5, 5]"), ans=10),
  C("TOTAL_ALWAYS", S("[]"), ans=0),
  C("TOTAL_ALWAYS", S("[M, M, M]"), expect="fails", ans="none"),
  C("TOTAL_ALWAYS", S("[M]"), ans=M),
 ],
 "sonnet-1/R1": [
  C("T_TOTAL", T("[50, 20]", "0->1:30"), ans=True, after=[20, 50]),
  C("T_TOTAL", T("[10, 5]", "0->1:10"), after=[0, 15]),
  C("T_TOTAL", T("[10, 5]", "0->1:50"), ans=False, after=[10, 5]),
  C("T_TOTAL", T("[60, M-10]", "0->1:20"), ans=False, scaled=True),
  C("T_TOTAL", T("[7, 3]", "0->1:0")),
 ],
 "sonnet-1/R2": [
  C("T_MOVED", T("[50, 20, 9]", "0->1:30"), ans=True, after=[20, 50, 9]),
  C("T_MOVED", T("[5, 0, 40]", "0->1:5"), after=[0, 5, 40]),
  C("T_MOVED", T("[80, 10]", "0->1:80"), ans=True, after=[0, 90], note="the author's maximum of 100 is not reached"),
  C("T_MOVED", T("[100, 0]", "0->1:1"), after=[99, 1], note="the author's maximum of 100 concerns the sender only"),
  C("T_MOVED", T("[10, 20, 30]", "2->0:4"), after=[14, 20, 26], note="the author numbers accounts from 1 here"),
 ],
 "sonnet-1/R3": [
  C("T_REJ", T("[10, 5]", "0->1:20"), ans=False, after=[10, 5]),
  C("T_REJ", T("[10]", "0->7:3"), ans=False, after=[10]),
  C("T_REJ", T("[10, 5]", "0->0:4"), ans=False, after=[10, 5]),
  C("T_REJ", T("[50, M-5]", "0->1:10"), ans=False, scaled=True),
  C("T_REJ", T("[10]", "9->0:1"), ans=False, after=[10], chosen=True),
 ],
 "sonnet-1/R4": [
  C("T_VALID", T("[30, 60]", "0->1:30"), ans=True, after=[0, 90]),
  C("T_VALID", T("[30, 60]", "0->1:41"), ans=False),
  C("T_VALID", T("[50, M-40]", "0->1:41"), ans=False, scaled=True, note="the author's second half (40 is accepted, landing exactly on the maximum) was also run: see extra"),
  C("T_VALID", T("[30, 60]", "0->0:5"), ans=False),
  C("T_VALID", T("[30, 60]", "0->2:1"), ans=False, chosen=True),
 ],
 "sonnet-1/R6": [
  C("B_STEP", B("[10, 0]", "[0->1:4, 0->1:4, 0->1:4, 0->1:1]"), ans=2, after=[2, 8]),
  C("B_STEP", B("[10, 0]", "[0->1:1, 0->1:1, 0->1:1]"), ans=3, chosen=True),
  C("B_STEP", B("[10, 0]", "[]"), ans=0, after=[10, 0], chosen=True),
  C("B_STEP", B("[10, 0]", "[0->1:20, 0->1:1]"), ans=0, after=[10, 0], chosen=True),
  C("B_STEP", B("[5, 0]", "[0->1:5, 0->1:1, 1->0:0]"), ans=1, after=[0, 5]),
 ],
 "sonnet-1/R7": [
  C("B_WHOLE", B("[10, 0]", "[0->1:4, 0->1:4]"), ans=True, after=[2, 8]),
  C("B_WHOLE", B("[10, 0]", "[0->1:4, 0->1:4, 0->1:4]"), ans=False, after=[10, 0]),
  C("B_WHOLE", B("[10, 0]", "[]"), ans=True, after=[10, 0], chosen=True),
  C("B_WHOLE", B("[10, 0]", "[0->1:4, 0->5:1]"), ans=False, after=[10, 0], chosen=True),
  C("B_WHOLE", B("[10, 0, 0]", "[0->1:10, 1->2:10]"), ans=True, after=[0, 0, 10]),
 ],
 "sonnet-1/R8": [
  C("B_WHOLE_OK", B("[10, 0]", "[0->1:3, 0->1:3]"), after=[4, 6]),
  C("B_WHOLE_OK", B("[10, 0]", "[0->1:3]"), chosen=True),
  C("B_WHOLE_OK", B("[10, 0]", "[]"), after=[10, 0], chosen=True),
  C("B_WHOLE_OK", B("[10, 0, 0]", "[0->1:5, 1->2:5]"), after=[5, 0, 5]),
  C("B_WHOLE_OK", B("[10, 0]", "[0->1:4, 0->1:4, 0->1:4]"), expect="silent", after=[10, 0]),
 ],
 "sonnet-1/R9": [
  C("L_BOTH", L("[10, 20, 30]", "1"), ans=20),
  C("L_BOTH", L("[10, 20, 30]", "5"), ans="none"),
  C("TOTAL_FITS", S("[10, 20, 30]"), ans=60, note="that the total IS 60 is the part of the sentence the reading does not say"),
  C("TOTAL_FITS", S("[]"), ans=0, note="as above: the reading says only that the computation is accepted"),
  C("TOTAL_FITS", S("[M, 1]"), ans="none", chosen=True),
 ],
 "haiku-1/R01": [
  C("T_TOTAL_OK", T("[5, 3]", "0->1:2"), ans=True),
  C("T_TOTAL_OK", T("[10, 0]", "0->1:10"), ans=True),
  C("T_TOTAL_OK", T("[4, 4]", "1->0:1"), ans=True),
  C("T_TOTAL_OK", T("[7, 2]", "0->2:3"), ans=False, note="the author adds a rejected call as a case of a rule about accepted transfers"),
  C("T_TOTAL_OK", T("[6, 1]", "0->1:6"), ans=True),
 ],
 "haiku-1/R02": [
  C("T_REJ", T("[2, 9]", "0->1:5"), ans=False, after=[2, 9]),
  C("T_REJ", T("[3, 4]", "0->0:1"), ans=False, after=[3, 4], chosen=True),
  C("T_REJ", T("[5, M]", "0->1:1"), ans=False, after=[5, M]),
  C("T_REJ", T("[8, 1]", "0->9:1"), ans=False, after=[8, 1], chosen=True),
  C("T_REJ", T("[0, 0]", "0->1:0"), after=[0, 0], note="the author: 'accepted or rejected but balances are 0 and 0 either way'; the code accepts it"),
 ],
 "haiku-1/R05": [
  C("B_WHOLE", B("[10, 0]", "[0->1:4, 0->1:4]"), ans=True, after=[2, 8]),
  C("B_WHOLE", B("[10, 0]", "[0->1:4, 0->1:7]"), after=[10, 0]),
  C("B_WHOLE", B("[5, 5]", "[]"), ans=True, after=[5, 5]),
  C("B_WHOLE", B("[3, 3]", "[0->1:1, 1->9:1]"), ans=False, after=[3, 3]),
  C("B_WHOLE", B("[6, 0]", "[0->1:6, 1->0:6]"), ans=True, after=[6, 0]),
 ],
 "haiku-1/R06": [
  C("B_STEP", B("[10, 0]", "[0->1:3, 0->1:3, 0->1:9, 0->1:1]"), ans=2, after=[4, 6]),
  C("B_STEP", B("[1, 0]", "[0->1:5]"), ans=0, after=[1, 0]),
  C("B_STEP", B("[5, 0]", "[0->1:1, 0->1:1, 0->1:1]"), ans=3),
  C("B_STEP", B("[5, 0]", "[0->1:2, 0->0:1, 0->1:1]"), ans=1, after=[3, 2]),
  C("B_STEP", B("[9, 0]", "[]"), ans=0, after=[9, 0]),
 ],
 "haiku-1/R07": [
  C("L_BOTH", L("[12]", "0"), ans=12),
  C("L_BOTH", L("[12]", "9"), ans="none"),
  C("L_BOTH", L("[7, 5]", "0"), ans=7, note="the ledger after the author's transfer of 5 on [12, 0]"),
  C("L_BOTH", L("[12]", "3"), ans="none"),
  C("L_BOTH", L("[12, 0]", "1"), ans=0),
 ],
 "haiku-1/R08": [
  C("B_WHOLE_OK", B("[10, 0]", "[0->1:3, 1->0:1]"), after=[8, 2]),
  C("B_WHOLE_OK", B("[5, 5]", "[0->1:5, 1->0:5]"), after=[5, 5]),
  C("B_WHOLE_OK", B("[4, 0, 0]", "[0->1:2, 1->2:2]"), after=[2, 0, 2]),
  C("B_WHOLE_OK", B("[2, 8]", "[1->0:3]"), after=[5, 5]),
  C("B_WHOLE_OK", B("[7, 1]", "[0->1:7]"), after=[0, 8]),
 ],
 "haiku-1/R09": [
  C("T_ONLY", T("[5, 2, 9]", "0->1:1"), ans=True),
  C("T_ONLY", T("[5, 2]", "1->0:3"), ans=True),
  C("T_ONLY", T("[1, 1, 1, 1]", "2->3:1"), ans=True),
  C("T_ONLY", T("[6, 0, 4]", "0->1:0"), ans=True, after=[6, 0, 4]),
  C("T_ONLY", T("[2, 2, 2]", "0->2:2"), ans=True),
 ],
 "haiku-1/R10": [
  C("T_OVER", T("[10, M-10]", "0->1:10"), ans=True, scaled=True, chosen=True, note="the half of the sentence the reading drops (lands exactly on the maximum: accepted)"),
  C("T_OVER", T("[11, M-10]", "0->1:11"), ans=False, scaled=True, chosen=True),
  C("T_OVER", T("[1, M]", "0->1:1"), ans=False, scaled=True, chosen=True),
  C("T_OVER", T("[50, M-50]", "0->1:50"), ans=True, scaled=True, chosen=True, note="the dropped half again"),
  C("T_OVER", T("[51, M-50]", "0->1:51"), ans=False, scaled=True, chosen=True),
 ],
 "haiku-1/R12": [
  C("L_ZERO", L("[0]", "0"), expect="fails", ans=0),
  C("L_ZERO", L("[5, 0]", "1"), expect="fails", ans=0, chosen=True),
  C("L_ZERO", L("[0]", "5"), ans="none", chosen=True, note="'true, but not the claim'"),
  C("L_ZERO", L("[5]", "0"), ans=5, note="'true, not the claim'"),
  C("L_ZERO", L("[3, 0]", "1"), expect="fails", ans=0, chosen=True),
 ],
 "default-1/R01": [
  C("T_TOTAL_OK", T("[100, 50]", "0->1:30"), ans=True, after=[70, 80]),
  C("T_TOTAL_OK", T("[10, 0, 5]", "0->2:10"), ans=True, after=[0, 0, 15]),
  C("T_TOTAL_OK", T("[M-500, 500]", "1->0:500"), ans=True, scaled=True),
  C("T_TOTAL_OK", T("[7, 3]", "0->1:0"), ans=True, after=[7, 3]),
  C("T_TOTAL_OK", T("[1, 2, 3, 4]", "3->0:4"), ans=True, after=[5, 2, 3, 0]),
 ],
 "default-1/R02": [
  C("T_REJ", T("[100, 50]", "0->1:200"), ans=False, after=[100, 50]),
  C("T_REJ", T("[100, 50]", "0->5:10"), ans=False, after=[100, 50]),
  C("T_REJ", T("[100, 50]", "1->1:10"), ans=False, after=[100, 50]),
  C("T_REJ", T("[100, M-10]", "0->1:20"), ans=False, scaled=True),
  C("T_REJ", T("[0, 0, 0]", "2->0:1"), ans=False, after=[0, 0, 0]),
 ],
 "default-1/R03": [
  C("T_MOVED", T("[100, 50, 25]", "0->1:30"), after=[70, 80, 25]),
  C("T_MOVED", T("[100, 50, 25]", "2->0:25"), after=[125, 50, 0]),
  C("T_MOVED", T("[9, 9, 9, 9]", "3->2:1"), after=[9, 9, 10, 8]),
  C("T_MOVED", T("[40, 60]", "0->1:0"), after=[40, 60]),
  C("T_MOVED", T("[M-1000, 1000]", "1->0:1000"), ans=True, scaled=True),
 ],
 "default-1/R06": [
  C("B_COUNT", B("[100, 0]", "[0->1:10, 0->1:10, 0->1:10]"), ans=3),
  C("B_COUNT", B("[15, 0]", "[0->1:10, 0->1:10, 0->1:10]"), ans=1),
  C("B_COUNT", B("[0, 0]", "[0->1:5, 0->1:5]"), ans=0),
  C("B_COUNT", B("[100, 0]", "[]"), ans=0, chosen=True),
  C("B_COUNT", B("[100, 0]", "[0->1:10, 0->1:10, 0->1:10, 0->9:10, 0->1:10]"), ans=3, chosen=True),
 ],
 "default-1/R07": [
  C("B_WHOLE", B("[100, 0]", "[0->1:10, 0->1:20]"), ans=True, after=[70, 30]),
  C("B_WHOLE", B("[15, 0]", "[0->1:10, 0->1:10]"), ans=False, after=[15, 0]),
  C("B_WHOLE", B("[0, 50]", "[1->0:20, 0->1:20]"), ans=True, after=[0, 50]),
  C("B_WHOLE", B("[30, 30]", "[]"), ans=True, after=[30, 30]),
  C("B_WHOLE", B("[100, 0]", "[0->1:10, 1->1:5]"), ans=False, after=[100, 0]),
 ],
 "default-1/R09": [
  C("T_VALID", T("[100, 50]", "0->1:100"), ans=True),
  C("T_VALID", T("[100, 50]", "0->1:101"), ans=False),
  C("T_VALID", T("[100, M-50]", "0->1:50"), ans=True, scaled=True),
  C("T_VALID", T("[100, M-50]", "0->1:51"), ans=False, scaled=True),
  C("T_VALID", T("[100, 50]", "0->2:10"), ans=False),
 ],
}

# extra inputs run beside a case (a second input the author names in the same case)
EXTRA = {
 "sonnet-1/R4": [C("T_VALID", T("[50, M-40]", "0->1:40"), ans=True, scaled=True, note="case 3, second half: 40 is accepted, landing exactly on the maximum")],
}

# the probes: the authors' cases put to the WALLET reading their near-verbatim sentence compiles to
PROBE_CASES = {
 "opus-1/r1": [
  C("W_TOTAL", W("50", "30", "20")),
  C("W_TOTAL", W("50", "30", "60")),
  C("W_TOTAL", W("10", "0", "10"), note="the third account (B = 0) is no part of a wallet transfer; it is left out"),
  C("W_TOTAL", W("10", "M-5", "10"), scaled=True),
  C("W_TOTAL", None, note="NOT ENCODABLE: a transfer between two wallets has no account that can be missing"),
 ],
 "haiku-1/R01": [
  C("W_TOTAL_OK", W("5", "3", "2")),
  C("W_TOTAL_OK", W("10", "0", "10")),
  C("W_TOTAL_OK", W("4", "4", "1")),
  C("W_TOTAL_OK", None, note="NOT ENCODABLE: a transfer between two wallets has no third account C that can be missing"),
  C("W_TOTAL_OK", W("6", "1", "6")),
 ],
}
