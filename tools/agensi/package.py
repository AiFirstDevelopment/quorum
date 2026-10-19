#!/usr/bin/env python3
"""Build Agensi marketplace ZIPs from this repository.

Reads the source tree, never modifies it. Stages in a temp dir outside the repo,
writes reproducible ZIPs (sorted entries, fixed timestamps, normalised modes) to
dist/agensi/packages/, and copies listing/report text from tools/agensi/content/.

    python3 tools/agensi/package.py            # build everything
    python3 tools/agensi/validate.py           # then validate
"""
import json, os, re, shutil, stat, sys, tempfile, zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CONTENT = Path(__file__).resolve().parent / 'content'
OUT = REPO / 'dist' / 'agensi'
FIXED_TIME = (2026, 1, 1, 0, 0, 0)
EXCLUDE_NAMES = {'.DS_Store', 'Thumbs.db', '__pycache__', '.git', '.env', '.pytest_cache', 'node_modules'}
EXCLUDE_SUFFIXES = ('.pyc', '.pyo', '.swp', '.log')

def version_of(plugin):
    return json.loads((REPO / 'plugins' / plugin / '.claude-plugin' / 'plugin.json').read_text())['version']

# Standalone skills: only those whose SKILL.md works with no plugin runtime.
# (name, source plugin, source skill, extra files {dest: src}, text substitutions)
STANDALONE = [
    dict(slug='quorum-tests-run', plugin='tests', skill='run', extras={}, subs=[]),
    dict(slug='quorum-tests-ci', plugin='tests', skill='ci', extras={}, subs=[]),
    dict(slug='quorum-tests-add', plugin='tests', skill='add',
         extras={'references/diff-scope.md': REPO / 'plugins/tests/reference/diff-scope.md'},
         subs=[('${CLAUDE_PLUGIN_ROOT}/reference/diff-scope.md', 'references/diff-scope.md')]),
]

def want(p: Path):
    return p.name not in EXCLUDE_NAMES and not p.name.endswith(EXCLUDE_SUFFIXES)

def walk(root: Path):
    for p in sorted(root.rglob('*')):
        if any(part in EXCLUDE_NAMES for part in p.relative_to(root).parts) or not want(p):
            continue
        if p.is_symlink():
            sys.exit(f'refusing symlink: {p}')
        if p.is_file():
            yield p

def copy_tree(src: Path, dst: Path):
    for p in walk(src):
        t = dst / p.relative_to(src)
        t.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, t)

def rename_frontmatter(text, slug):
    new, n = re.subn(r'(?m)\A(---\n(?:.*\n)*?)name:\s*\S+', lambda m: f'{m.group(1)}name: {slug}', text, count=1)
    if n != 1:
        sys.exit('could not rewrite frontmatter name')
    return new

def write_zip(stage: Path, top: str, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest.unlink()
    with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(stage.rglob('*')):
            if not p.is_file():
                continue
            arc = f'{top}/{p.relative_to(stage).as_posix()}'
            zi = zipfile.ZipInfo(arc, FIXED_TIME)
            executable = bool(p.stat().st_mode & stat.S_IXUSR)
            zi.external_attr = (0o755 if executable else 0o644) << 16
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, p.read_bytes())

def build_standalone(spec, work):
    ver = version_of(spec['plugin'])
    stage = work / spec['slug']
    stage.mkdir()
    text = (REPO / 'plugins' / spec['plugin'] / 'skills' / spec['skill'] / 'SKILL.md').read_text()
    for a, b in spec['subs']:
        if a not in text:
            sys.exit(f'substitution target missing in {spec["slug"]}: {a}')
        text = text.replace(a, b)
    (stage / 'SKILL.md').write_text(rename_frontmatter(text, spec['slug']))
    for dest, src in spec['extras'].items():
        (stage / dest).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, stage / dest)
    (stage / 'README.md').write_text((CONTENT / 'skill-readmes' / f'{spec["slug"]}.md').read_text().replace('{{VERSION}}', ver))
    zp = OUT / 'packages' / f'{spec["slug"]}-{ver}.zip'
    write_zip(stage, spec['slug'], zp)
    return zp

def build_complete(work):
    ver = version_of('quorum')
    stage = work / 'quorum-complete'
    stage.mkdir()
    (stage / 'SKILL.md').write_text((CONTENT / 'quorum-complete-SKILL.md').read_text().replace('{{VERSION}}', ver))
    (stage / 'README.md').write_text((CONTENT / 'skill-readmes' / 'quorum-complete.md').read_text().replace('{{VERSION}}', ver))
    mk = stage / 'marketplace'
    (mk / '.claude-plugin').mkdir(parents=True)
    shutil.copy2(REPO / '.claude-plugin' / 'marketplace.json', mk / '.claude-plugin' / 'marketplace.json')
    shutil.copy2(REPO / 'README.md', mk / 'README.md')
    copy_tree(REPO / 'plugins', mk / 'plugins')
    zp = OUT / 'packages' / f'quorum-complete-{ver}.zip'
    write_zip(stage, 'quorum-complete', zp)
    return zp

def main():
    (OUT / 'packages').mkdir(parents=True, exist_ok=True)
    for old in (OUT / 'packages').glob('*.zip'):
        old.unlink()
    with tempfile.TemporaryDirectory(prefix='agensi-stage-') as w:
        work = Path(w)
        built = [build_complete(work)] + [build_standalone(s, work) for s in STANDALONE]
    for sub in ('listings', 'reports'):
        (OUT / sub).mkdir(exist_ok=True)
        for f in sorted((CONTENT / sub).glob('*.md')):
            shutil.copy2(f, OUT / sub / f.name)
    shutil.copy2(CONTENT / 'README.md', OUT / 'README.md')
    for b in built:
        print(b.relative_to(REPO))

if __name__ == '__main__':
    main()
