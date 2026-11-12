"""Fix pass after the review of the frame library: the reviewer's 12 frame mutants (rv_tools/fmut.py) against the toy tests
alone, in a core-Lean scratch copy of lean/Frames + lean/Run/FrameToyTests.lean (argument: a directory holding `fl/` with a
lakefile that builds the library `Frames`). Not blind: the toy lines were extended until X6 and Y5 were caught."""
import sys, subprocess, shutil, os, importlib.util, json
S=sys.argv[1]; SL="/Users/will/dev/lean-rosette/clausal"
spec=importlib.util.spec_from_file_location("fmut", SL+"/review/frames/rv_tools/fmut.py"); fm=importlib.util.module_from_spec(spec); spec.loader.exec_module(fm)
fl=S+"/fl"
def sync():
    for f in ("Core","Frames","Check","Lemmas"): shutil.copy2(f"{SL}/lean/Frames/{f}.lean", f"{fl}/Frames/{f}.lean")
    shutil.copy2(f"{SL}/lean/Run/FrameToyTests.lean", f"{fl}/Run/FrameToyTests.lean")
def run():
    full=subprocess.run(["lake","build"],cwd=fl,capture_output=True,text=True)
    note=""
    if full.returncode:
        note=" [the library build also fails: "+", ".join(sorted({l.split(':')[1].split('/')[-1] for l in full.stdout.splitlines() if l.startswith('error: Frames')}))+"]"
    b=subprocess.run(["lake","build","Frames.Check"],cwd=fl,capture_output=True,text=True)
    if b.returncode: return "BUILD OF THE CHECKERS FAILS"+note
    r=subprocess.run(["lake","env","lean","Run/FrameToyTests.lean"],cwd=fl,capture_output=True,text=True)
    bad=[l.split("\t") for l in r.stdout.splitlines() if l.startswith("FTEST") and l.split("\t")[3]!=l.split("\t")[4]]
    n=sum(1 for l in r.stdout.splitlines() if l.startswith("FTEST"))
    if r.returncode or n==0: return "TOY SCRIPT FAILS: "+(r.stdout+r.stderr)[:300]+note
    return (f"{len(bad)} of {n} toy lines disagree: "+", ".join(sorted({b[1] for b in bad})) if bad else f"NOT CAUGHT ({n} lines agree)")+note
sync(); print("pristine:", run())
res={}
for mid,fname,what,old,new in fm.M:
    sync()
    p=f"{fl}/Frames/{fname}.lean"; src=open(p).read()
    if src.count(old)!=1: res[mid]=f"PATCH-NOT-APPLIED ({src.count(old)})"; print(mid,what,res[mid]); continue
    open(p,"w").write(src.replace(old,new))
    res[mid]=run(); print(mid,"|",what,"|",res[mid],flush=True)
sync(); print("restored:", run())
json.dump(res,open(S+"/toymut_results.json","w"),indent=1)
