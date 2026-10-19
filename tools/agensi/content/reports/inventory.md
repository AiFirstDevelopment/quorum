# Inventory

Source: `AiFirstDevelopment/quorum` — marketplace v0.25.0 (`marketplace.json`), `quorum` plugin v0.25.1, `tests` plugin v0.2.0. (The 0.25.0/0.25.1 mismatch is in the source; `claude plugin validate` warns about it. Left untouched.)

**13 skills discovered** (10 in `quorum`, 3 in `tests`), 6 agents, 1 hook, 8 Python helpers in `bin/`, 3 workflow scripts, 2 reference docs per plugin area, 2 calibration cases. **No LICENSE file exists in the repository.**

| Skill | Standalone? | Why |
|---|---|---|
| tests:run | **Yes** | Prose only; no plugin-root references |
| tests:ci | **Yes** | Prose only |
| tests:add | **Yes, with one path rewrite** | Reads `${CLAUDE_PLUGIN_ROOT}/reference/diff-scope.md`; bundled as `references/diff-scope.md` |
| quorum:1-plan | No | `bin/state.py`, `bin/guard.py`, `reference/contract.md`, plan-lock hook, sibling commands |
| quorum:2-build | No | `state.py`, `contract.md`, hook, `/quorum:1-plan` |
| quorum:3-review | No | `state.py`, `contract.md`, reviewer/scribe agents |
| quorum:4-quorum | No | `guard.py`, `state.py`, judge agent |
| quorum:pipeline | No | `workflow/pipeline.js`, 6 agents, `watch.py`, `state.py` |
| quorum:audit | No | `audit.py`, `workflow/audit.js`, auditor/scribe agents |
| quorum:calibrate | No | `calibrate.py`, `workflow/calibrate.js`, calibration cases |
| quorum:guard | No | `guard.py` (959 lines), `selftest.py`, work-item layout |
| quorum:history | No | `history.py`, `contract.md` |
| quorum:status | No | `contract.md`, `state.json` layout |

Every `quorum:` skill resolves its helpers through `${CLAUDE_PLUGIN_ROOT}`, which exists only for installed plugins. Rewriting those paths would change the product, so they ship only inside the complete bundle, unmodified.

Mechanism for the standalone renames: frontmatter `name` becomes `quorum-tests-<x>` (`run`/`ci`/`add` are not meaningful slugs outside a plugin namespace). Nothing else changes except the one path above.
