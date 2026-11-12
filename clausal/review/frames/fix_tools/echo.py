import sys
sys.path.insert(0,'.')
from pathlib import Path
from slicegen import vocab, vreport
from slicegen.core import load_glossary, parse_feature, Problem
from slicegen.pipeline import ROOT
gl = load_glossary(ROOT / "glossary.yaml", "glossary.yaml")
voc = vocab.Vocabulary(ROOT / "vocabulary.yaml", "vocabulary.yaml", gl)
comp = vocab.Compiler(voc)
want = sys.argv[2:] 
for p in sys.argv[1].split(","):
    f = parse_feature(ROOT / p, p)
    for r in f.rules:
        rds = {sc.id: comp.scenario(sc) for sc in r.scenarios}
        hint = next((x.info["ops"][0]["domain"] for x in rds.values() if isinstance(x, vocab.Reading)), None)
        items = [(r.id, "Rule: " + r.name, comp.rule(r, hint))] + [(sc.id, sc.name, rds[sc.id]) for sc in r.scenarios]
        for i, t, rd in items:
            if want and not any(w in i for w in want): continue
            print("=====", i, "|", t)
            if isinstance(rd, Problem): print("  ", rd.status, rd.message[:300]); continue
            print("\n".join(vreport.echo_lines(rd)))
