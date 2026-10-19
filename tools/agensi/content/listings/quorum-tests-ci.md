# Quorum Tests: CI — make the regression suite a merge gate

**Summary:** Generates or extends a CI workflow that runs your full suite, and explains the branch-protection setting that makes it blocking.

**Suggested introductory price:** $5 — same reasoning as quorum-tests-run: small prompt-only skill, free upstream.

**Open source disclosure:** This software is also available free and open source at https://github.com/AiFirstDevelopment/quorum. The marketplace edition contains no exclusive functionality; you are paying for convenience and packaging.

## Description
A Claude Code skill that detects your CI host, writes or extends the workflow (stable job name, pinned runtime, cached dependencies, distinct install/build/test steps, failure artifacts), refuses to add non-blocking shortcuts, and gives the exact branch-protection command — which it asks before running, since it changes repository settings.

## Key features
- Detects GitHub Actions, GitLab CI, Azure Pipelines, CircleCI, Jenkins
- Extends existing CI rather than adding a competing file
- Never invents or commits secrets
- Explicit that the gate is unproven until it runs on a real PR

## Intended audience
Teams who have tests but no enforced merge gate.

## Requirements and compatibility
Claude Code. Claude Code with Agent Skills support; `gh` CLI for the optional branch-protection step. No scripts bundled.

## Installation
Unzip so `quorum-tests-ci/` is in `~/.claude/skills/` or `<repo>/.claude/skills/`.

## What's included
`SKILL.md`, `README.md`.

## Limitations
- Cannot apply branch protection itself without your approval and permissions
- Does not verify a workflow runs until a real PR does
- Mentions `/tests:run` and Quorum commands as context; those are not included
- No guarantee of results

## Keywords / tags
ci, github actions, merge gate, branch protection, regression testing, claude code

## Links
Public repository: https://github.com/AiFirstDevelopment/quorum
