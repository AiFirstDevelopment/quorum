# quorum-tests-run (v{{VERSION}})

Runs a repository's full regression suite and reports failures classified as
code broken, test broken, environment, or flake. It runs and reports; it never
edits code or tests.

Install: unzip so the `quorum-tests-run/` folder sits in `~/.claude/skills/`
(personal) or `<repo>/.claude/skills/` (project). Then ask Claude to run the
regression suite.

Self-contained: no scripts, no network access, no dependencies. It is the `run`
skill of the `tests` plugin in https://github.com/AiFirstDevelopment/quorum
(open source), renamed so the name is unambiguous outside a plugin.
