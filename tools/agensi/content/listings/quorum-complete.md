# Quorum — plan, build, review, adjudicate for Claude Code (complete bundle)

**Summary:** The full Quorum workflow: approved plans, autonomous build, six independent review lenses, adjudication, mechanical guard checks, and the tests plugin.

**Suggested introductory price:** $29 — largest offering, ~50 files of orchestration, helpers and docs, with a 326-case self-test; priced as a convenience bundle because the identical source is free on GitHub.

**Open source disclosure:** This software is also available free and open source at https://github.com/AiFirstDevelopment/quorum. The marketplace edition contains no exclusive functionality; you are paying for convenience and packaging.

## Description
Quorum makes the AI write a falsifiable plan before code, then holds the work to it. This bundle ships the unmodified Quorum marketplace: the `quorum` plugin (plan, build, review, quorum/adjudicate, pipeline, audit, calibrate, guard, history, status) and the `tests` plugin (run, add, ci). Review runs in fresh context across six lenses; a judge adjudicates findings and is prohibited from weakening tests or narrowing criteria; a read-only recheck covers the judge's own commits; `guard` performs mechanical checks and can install them as a CI gate with no agent involved.

## Key features
- Structured planning with explicit approval gate
- Autonomous pipeline after plan approval (build → six review lenses → adjudication → recheck → pull request)
- Independent review perspectives, run blind to each other
- Adjudication with a verdict file and a required green suite
- Regression testing via the tests plugin; CI enforcement via guard and tests:ci
- Self-test of the enforcement layer (326 checks pass in the packaging validation)

## Intended audience
Teams using Claude Code on real repositories who want a checkable delivery discipline.

## Requirements and compatibility
Claude Code. Claude Code with plugin support (verified with 2.1.296); Python 3 (standard library only); git. The pipeline requires installation as a plugin — it cannot be used as loose skills.

## Installation
1. Unzip `quorum-complete/` anywhere.
2. `claude plugin marketplace add <folder>/marketplace`
3. `claude plugin install quorum@quorum` and `claude plugin install tests@quorum`
4. Restart Claude Code; run `/quorum:1-plan <what to build>`.

## What's included
Unmodified `marketplace/` tree (both plugins with agents, hook, bin helpers, workflow scripts, reference docs, calibration cases), the marketplace README, a bundle `SKILL.md` and `README.md`.

## Limitations
- Autonomous runs consume significant model usage; only plan approval is human-gated
- Review quality is not guaranteed; `calibrate` exists to measure it
- Installs a PreToolUse hook (`plan-lock-hook.py`) — read before installing
- No security or correctness guarantees
- Whether Agensi's installer delivers plugin bundles intact is unconfirmed

## Keywords / tags
claude code, plugin, code review, planning, pipeline, adjudication, ci, regression testing, agentic workflow

## Links
Public repository: https://github.com/AiFirstDevelopment/quorum
