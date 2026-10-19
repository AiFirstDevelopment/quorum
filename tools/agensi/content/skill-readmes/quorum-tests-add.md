# quorum-tests-add (v{{VERSION}})

Writes behavioral regression tests for the current change through the
application's outermost user-facing surface, and proves each new test fails when
the behavior it guards is broken.

Install: unzip so the `quorum-tests-add/` folder sits in `~/.claude/skills/` or
`<repo>/.claude/skills/`.

Contents: `SKILL.md` and `references/diff-scope.md` (how "the change under test"
is determined). Pairs well with `quorum-tests-run` (the skill falls back to the
repo's own test command if it is absent).

It is the `add` skill of the `tests` plugin in
https://github.com/AiFirstDevelopment/quorum (open source). One packaging edit:
the plugin-relative path to `diff-scope.md` is rewritten to `references/diff-scope.md`.
