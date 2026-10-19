---
name: quorum-complete
description: Use when the user asks to install, set up, or learn about the Quorum plugins (quorum and tests) bundled in this folder - a plan, build, multi-lens review and adjudication pipeline for Claude Code, plus a regression-testing plugin. This skill only installs and explains the bundle; it does not run the pipeline itself.
---

# Quorum — complete bundle (v{{VERSION}})

This folder contains the full, unmodified Quorum Claude Code marketplace in
`marketplace/`: the `quorum` plugin (skills, agents, a PreToolUse hook, Python
helpers, workflow scripts) and the `tests` plugin. The pipeline only works when
installed as a **Claude Code plugin** — the skills reference
`${CLAUDE_PLUGIN_ROOT}`, which exists only for installed plugins. Copying single
skills out of `marketplace/` will not work.

## Install

Run these in a terminal (they register a local marketplace and install from it;
ask the user before running them for them):

```bash
claude plugin marketplace add "<path to this folder>/marketplace"
claude plugin install quorum@quorum
claude plugin install tests@quorum
```

Then restart Claude Code. The commands appear as `/quorum:1-plan`,
`/quorum:pipeline`, `/quorum:audit`, `/quorum:guard`, `/tests:run`, and so on.

## What the plugin does at runtime

- A `PreToolUse` hook (`marketplace/plugins/quorum/hooks/hooks.json`) runs
  `bin/plan-lock-hook.py` before Edit/Write/MultiEdit. Read it before installing.
- Skills run local Python helpers in `bin/` and work records under `docs/work/`
  of the repository you use it in.

Full documentation: `marketplace/README.md` and `README.md` in this folder.
Source and issues: https://github.com/AiFirstDevelopment/quorum
