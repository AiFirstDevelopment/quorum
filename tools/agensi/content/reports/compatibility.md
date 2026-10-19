# Agensi compatibility

Sources: Agensi Terms of Service, /sell, /learn/skill-md-creator-checklist, /learn/how-agensi-security-scan-works. The /learn/skill-md-format spec page and the seller terms on bundles were not retrievable in text; nothing below is assumed from them.

## Documented
- Upload is a zip containing a valid `SKILL.md` (ToS 6.2). Checklist: **one top-level folder, SKILL.md at its root**, no double nesting, **text only, no symlinks/binaries**, no `.DS_Store`.
- Scripts and reference files are allowed if safe and readable. Scan: prompt injection, exfiltration, dangerous commands, hardcoded secrets, obfuscation, network access, zip integrity, SKILL.md validity; then AI review and human review (24–48h).
- Bundles of several skills exist as a listing type.
- Price min $1.00; under $5 credit-only; 70/30 split net of tax; refunds are Agensi's, sellers cannot set their own (ToS 6.3–6.5, 7.1). Payout setup/KYC required before paid listings.
- Listings may not link to paid versions elsewhere; links to your own source repo are allowed (6.3a). Seller keeps ownership, grants Agensi a non-exclusive license (8.1) and represents it has the rights (6.3).

## Not documented (ask Agensi)
1. Are Claude Code **plugins / marketplaces** (plugin.json, hooks, agents, `${CLAUDE_PLUGIN_ROOT}`) supported, or only loose skills? The delivery model ("agents load latest instructions on demand via MCP") suggests loose skills.
2. Is a **nested** `marketplace/` tree with a root `SKILL.md` accepted, or is it treated as unusual structure by the scan?
3. Will a **PreToolUse hook** and bundled Python helpers be allowed, and how is "dangerous commands" judged?
4. Does the installer **preserve executable bits** and subdirectories? (Not required by Quorum: hooks call `python3 <file>`.)
5. Size/file-count limits.
6. Does MCP-based delivery serve the bundle's extra files, or only `SKILL.md`?
7. Can one account list a bundle of products it sells individually, and what are bundle price rules?
8. Treatment of **open-source** content: ToS has no open-source clause. With no LICENSE in the repo, which license does a buyer receive?
9. Are naming rules/trademark checks applied to the name "Quorum"?
10. May a calibration fixture containing a planted `'dev-secret'` default pass the secret scan?

## Risks
- The complete bundle is the **nearest valid alternative** to a plugin package; it may be rejected or delivered without the hook/agents working, which would silently break the pipeline. Treat as unproven until a test purchase installs and runs.
- Only tested with Claude Code 2.1.296; other agents untested.
