"""slicegen CLI.

  python3 -m slicegen gen      parse features, bind steps, write Statements/Checks/Search/Adequacy, append proof stubs
  python3 -m slicegen derive   read out/search.log, write Run/Audit.lean (sat / unsat / refuted / trivial-Then + audit)
  python3 -m slicegen adequacy read out/adequacy.log, write Run/AdequacyAudit.lean (suite adequacy note; informational)
  python3 -m slicegen report   write out/graph.json and out/report.md, print the per-scenario and per-Rule report
  python3 -m slicegen rules [graph.json]   print the per-Rule blocks of a stored graph (reads the graph only)
  python3 -m slicegen steps    print the cucumber regex of every glossary entry; check bdd/tests/bdd.rs
  python3 -m slicegen review <entry-id|all> --reviewer NAME    record a glossary sign-off
"""
import sys

from . import pipeline

if __name__ == "__main__":
    sys.exit(pipeline.main(sys.argv[1:]))
