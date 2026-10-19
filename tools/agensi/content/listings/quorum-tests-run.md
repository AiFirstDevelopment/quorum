# Quorum Tests: Run — regression suite runner and failure classifier

**Summary:** Runs your full test suite and sorts each failure into code broken, test broken, environment, or flake.

**Suggested introductory price:** $5 — low-friction impulse price for a single prompt-only skill; it is free in the open-source repo, so the price should not exceed the convenience value. $5 is the lowest price that allows card purchase.

**Open source disclosure:** This software is also available free and open source at https://github.com/AiFirstDevelopment/quorum. The marketplace edition contains no exclusive functionality; you are paying for convenience and packaging.

## Description
A Claude Code skill that finds how a repository runs its tests (recorded recipe, plan, README, then manifests and CI workflows), runs the whole suite, re-runs failures once to detect flakes, and reports in a fixed table format. It never edits code or tests.

## Key features
- Discovers the test recipe from CI workflows and manifests, then records it for next time
- Classifies failures: code broken / test broken / environment / flake
- Surfaces skipped and filtered tests instead of hiding them
- Explicit partial-run reporting

## Intended audience
Developers using Claude Code who want honest, structured test reports.

## Requirements and compatibility
Claude Code. Agent Skills-compatible Claude Code. Not tested in other agents. No dependencies, scripts, or network access.

## Installation
Unzip so `quorum-tests-run/` is in `~/.claude/skills/` or `<repo>/.claude/skills/`.

## What's included
`SKILL.md`, `README.md`.

## Limitations
- Runs whatever test command the repo defines; it cannot make a repo testable
- Flake detection is a single re-run
- Its text references the open-source Quorum pipeline, which is not included in this package
- No guarantee of results

## Keywords / tags
regression testing, test runner, flaky tests, claude code, ci, test triage

## Links
Public repository: https://github.com/AiFirstDevelopment/quorum
