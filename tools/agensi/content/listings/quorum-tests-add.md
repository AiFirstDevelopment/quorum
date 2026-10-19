# Quorum Tests: Add — behavioral regression tests that are proven able to fail

**Summary:** Writes end-to-end behavioral tests for your current change and verifies each one fails when the behavior is broken.

**Suggested introductory price:** $9 — larger skill with a supporting reference file and a distinctive proof-of-failure procedure; still free upstream.

**Open source disclosure:** This software is also available free and open source at https://github.com/AiFirstDevelopment/quorum. The marketplace edition contains no exclusive functionality; you are paying for convenience and packaging.

## Description
A Claude Code skill that determines the change under test (branch diff plus uncommitted work), writes behavioral tests through the application's outermost user-facing surface, then mutates the code to confirm each test fails, and restores it. If a Quorum plan exists in the repo, its acceptance criteria become the checklist.

## Key features
- Tests the assembled application, not internals
- Mutation-style proof that each test can fail
- Flaky-test discipline
- Uses a Quorum plan's acceptance criteria when present

## Intended audience
Developers hardening a change before merge.

## Requirements and compatibility
Claude Code. Claude Code with Agent Skills support. Works best alongside a way to run your suite.

## Installation
Unzip so `quorum-tests-add/` is in `~/.claude/skills/` or `<repo>/.claude/skills/`.

## What's included
`SKILL.md`, `references/diff-scope.md`, `README.md`. One packaging edit versus the open-source plugin: the plugin-relative path to diff-scope is now relative to the skill folder.

## Limitations
- Not independently tested in a plain (non-plugin) install by the author; marked REVIEW REQUIRED
- Refers to `/tests:run` for running the suite; use `quorum-tests-run` or your own command
- No guarantee of results

## Keywords / tags
regression tests, e2e, behavioral testing, mutation check, claude code

## Links
Public repository: https://github.com/AiFirstDevelopment/quorum
