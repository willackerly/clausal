#!/usr/bin/env python3
"""Guards against a silently wrong Lean build of the generated file (review finding on S1a).

Aeneas writes the absolute path of cargo's OUT_DIR files (the prost and spqr build-script outputs, which live under
work/) into Lean block comments, about 1650 times in this file. Lean block comments nest: a path holding "/-" opens a
comment that is never closed, the rest of the file becomes one comment, Lean reports a single "unterminated comment"
error at the last line, and every function after that point has no error attributed to it, so the census join counts it
as through (267 instead of 250 in a copy under ".../claude-501/-Users-..."). A path holding "-/" would close a comment
early instead. Both are refused before anything is run, and the build step fails if Lean reports an unterminated
comment anyway.

    guard.py path <dir>...      exit 1 if a directory (as given, or with symlinks resolved) holds "/-" or "-/"
    guard.py lake <lake.log>    exit 1 if the log holds an "unterminated comment" error
    guard.py --self-test
"""
import os, re, sys

BAD = ('/-', '-/')


def bad_paths(dirs):
    """The (path, token) pairs that would break a Lean block comment; each directory is tried as given and resolved."""
    out = []
    for d in dirs:
        for p in dict.fromkeys((os.path.abspath(d) + os.sep, os.path.realpath(d) + os.sep)):
            out += [(p, t) for t in BAD if t in p]
    return out


def check_path(*dirs):
    bad = bad_paths(dirs)
    if bad:
        sys.exit('census/signal: refusing to run: the work path %r contains %r.\n'
                 'Aeneas copies absolute paths under work/ into Lean block comments, where "/-" opens a nested comment '
                 'and "-/" closes one; the Lean build would then be wrong without the join noticing (see guard.py).\n'
                 'Run from a checkout whose path has no directory name that starts or ends with "-".' % bad[0])


UNTERMINATED = re.compile(r'^.*\berror\b.*unterminated comment.*$', re.M)


def unterminated(text):
    m = UNTERMINATED.search(text)
    return m.group(0).strip() if m else None


def lake_log_hit(path):
    """None, or the message to stop with."""
    hit = unterminated(open(path, errors='replace').read()) if os.path.exists(path) else None
    return hit and ('census/signal: the Lean build is not usable: %s\n(%s)\nPart of the generated file was read as a comment, so '
                    'functions in it have no Lean error and would be counted as through. The result of this build was removed.' % (hit, path))


def check_lake_log(path):
    hit = lake_log_hit(path)
    if hit:
        sys.exit(hit)


def self_test():
    assert bad_paths(['/Users/x/dev/repo/census/signal']) == []
    assert bad_paths(['/Users/x/my-repo/census/signal']) == []                      # a "-" inside a name is harmless
    assert [t for _, t in bad_paths(['/private/tmp/claude-501/-Users-x/scratchpad/repo/census/signal'])] == ['/-']
    assert [t for _, t in bad_paths(['/tmp/copy-/census/signal'])][:1] == ['-/']
    assert [t for _, t in bad_paths(['/tmp/copy-'])][:1] == ['-/']                  # work/ comes below it
    assert unterminated('error: Generated/LibsignalProtocol.lean:79400:0: unterminated comment\n')
    assert unterminated('info: x\nerror: Generated/LibsignalProtocol.lean:12:3: unknown identifier\n') is None
    assert unterminated('') is None
    print('guard.py self-test ok')


if __name__ == '__main__':
    if sys.argv[1:] == ['--self-test']:
        self_test()
    elif len(sys.argv) > 2 and sys.argv[1] == 'path':
        check_path(*sys.argv[2:])
    elif len(sys.argv) == 3 and sys.argv[1] == 'lake':
        check_lake_log(sys.argv[2])
    else:
        sys.exit(__doc__)
