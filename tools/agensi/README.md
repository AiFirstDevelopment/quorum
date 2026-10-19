# tools/agensi

Builds and validates the Agensi marketplace packages. Outputs go to `dist/agensi/`.

    python3 tools/agensi/package.py
    python3 tools/agensi/validate.py

`content/` holds listing copy, static reports, the bundle's installer `SKILL.md`, and per-package READMEs. Edit those, not `dist/`. Source plugins are only read. See `dist/agensi/README.md`.
