# Submission checklist

**Do not upload until the blockers are resolved. Nothing has been uploaded.**

## Blockers / decisions for the owner
- [ ] **Add a LICENSE to the repository.** None exists. Without one, the open-source status described in the listings is unclear and ToS 6.3 requires you to confirm rights.
- [ ] Confirm you (or AiFirstDevelopment) own all content, including docs by co-authors, and that selling a copy of open-source work under the same name is intended.
- [ ] Decide whether the marketplace listing should carry the "Quorum" name.
- [ ] Approve prices (`reports/pricing.md`).
- [ ] Optional: fix the source's 0.25.0 vs 0.25.1 version mismatch (not touched here).

## Before each upload
1. `python3 tools/agensi/package.py && python3 tools/agensi/validate.py`; confirm no FAIL.
2. Create a seller account, set up Stripe/KYC payout (required for paid skills).
3. Submit via https://www.agensi.io/dashboard/submit — one product per zip in `dist/agensi/packages/`, text from `dist/agensi/listings/<name>.md`.
4. Submit **quorum-tests-run** and **quorum-tests-ci** first (PASS). Wait for scan results.
5. Ask Agensi the questions in `reports/compatibility.md` **before** submitting `quorum-complete`.
6. After approval, buy/install each as an outside user and run it: a plain skill folder in `~/.claude/skills/`, and for the bundle the three install commands.
7. Re-run the checks above after every Quorum release; versions come from `plugin.json`.
