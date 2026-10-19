# Quorum complete bundle (v{{VERSION}})

Unmodified Quorum Claude Code marketplace (`quorum` and `tests` plugins) under
`marketplace/`, plus `SKILL.md` that explains installation.

    claude plugin marketplace add "<this folder>/marketplace"
    claude plugin install quorum@quorum
    claude plugin install tests@quorum

Requires Claude Code with plugin support and Python 3 (helper scripts use only
the standard library). The same software is free and open source at
https://github.com/AiFirstDevelopment/quorum.
