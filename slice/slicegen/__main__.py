"""slicegen CLI.

  python3 -m slicegen gen      parse features, bind steps, write Statements/Checks/Search, append proof stubs
  python3 -m slicegen derive   read out/search.log, write Run/Audit.lean (sat / unsat / refuted / trivial-Then + audit)
  python3 -m slicegen report   write out/graph.json and out/report.md, print the per-scenario report
  python3 -m slicegen steps    print the cucumber regex of every glossary entry; check wallet-bdd/tests/steps.rs
  python3 -m slicegen review <entry-id|all> --reviewer NAME    record a glossary sign-off
"""
import sys

from . import pipeline

if __name__ == "__main__":
    sys.exit(pipeline.main(sys.argv[1:]))
