# quorum-tests-ci (v{{VERSION}})

Wires a repo's full regression suite into CI as a merge gate: detects the CI
host, writes or extends the workflow, and explains the branch-protection setting
(a repository setting the workflow alone does not apply; the skill asks before
running any `gh api` command).

Install: unzip so the `quorum-tests-ci/` folder sits in `~/.claude/skills/` or
`<repo>/.claude/skills/`.

Self-contained: no scripts or dependencies. It is the `ci` skill of the `tests`
plugin in https://github.com/AiFirstDevelopment/quorum (open source), renamed
for use outside a plugin. Its text mentions the Quorum pipeline only to say CI
must never run it.
