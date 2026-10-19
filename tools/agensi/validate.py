#!/usr/bin/env python3
"""Validate every ZIP in dist/agensi/packages and write reports/validation.md.

Non-destructive: extracts into temp dirs, uses a throwaway CLAUDE_CONFIG_DIR for
any `claude` call, and never touches the working tree or the user's real config.
"""
import json, os, re, shutil, stat, subprocess, sys, tempfile, zipfile, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / 'dist' / 'agensi'
SECRET_PATTERNS = [
    re.compile(r'AKIA[0-9A-Z]{16}'), re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----'),
    re.compile(r'gh[pousr]_[A-Za-z0-9]{30,}'), re.compile(r'sk-[A-Za-z0-9]{20,}'),
    re.compile(r'xox[baprs]-[A-Za-z0-9-]{10,}'),
    re.compile(r'(?i)\b(api[_-]?key|password|secret|token)\b\s*[:=]\s*[\'"][^\'"\s]{12,}[\'"]'),
]
FORBIDDEN_NAMES = {'.env', '.DS_Store', 'Thumbs.db', 'id_rsa', 'credentials.json', '.npmrc'}
RISKY = [re.compile(p) for p in (r'rm\s+-rf\s+/', r'curl[^\n]*\|\s*(ba)?sh', r'\bsudo\b', r'chmod\s+777')]
ROOT_REF = re.compile(r'\$\{CLAUDE_PLUGIN_ROOT\}/([A-Za-z0-9_./-]+)')

# Not verifiable offline; a package with any of these can be at best REVIEW REQUIRED.
UNVERIFIED = {
    'quorum-complete': ['Agensi has not documented support for plugin bundles (marketplace + hooks + agents); its 8-point scan may flag the hook or Python helpers.'],
    'quorum-tests-add': ['The rewritten relative path references/diff-scope.md is resolved by the agent from the skill folder; not verifiable without Agensi\'s install path.'],
}

def run(cmd, env=None, cwd=None, timeout=900):
    r = subprocess.run(cmd, env=env, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout + r.stderr).strip()

def isolated_env(tmp):
    e = dict(os.environ)
    e['CLAUDE_CONFIG_DIR'] = str(Path(tmp) / 'claude-config')
    e['HOME'] = str(Path(tmp) / 'home')
    Path(e['HOME']).mkdir(parents=True, exist_ok=True)
    return e

def frontmatter(text):
    m = re.match(r'---\n(.*?)\n---\n', text, re.S)
    if not m:
        return None
    return dict(re.findall(r'(?m)^([A-Za-z_-]+):\s*(.*)$', m.group(1)))

def check_zip(zp, res, tmp):
    chk = res['checks']
    def ok(name, cond, detail=''):
        chk.append((name, bool(cond), detail))
        return cond
    z = zipfile.ZipFile(zp)
    infos = z.infolist()
    names = [i.filename for i in infos]
    ok('zip integrity', z.testzip() is None)
    bad = [n for n in names if n.startswith('/') or '..' in Path(n).parts or '\\' in n or ':' in n.split('/')[0]]
    ok('no path traversal / absolute paths', not bad, str(bad))
    syml = [i.filename for i in infos if stat.S_ISLNK(i.external_attr >> 16)]
    ok('no symlinks', not syml, str(syml))
    tops = {n.split('/')[0] for n in names}
    ok('single top-level folder', len(tops) == 1, str(tops))
    top = next(iter(tops))
    ok('SKILL.md at folder root', f'{top}/SKILL.md' in names)
    ok('no nested SKILL.md double-nesting', f'{top}/{top}/SKILL.md' not in names)
    ok('no OS/junk/credential files', not [n for n in names if Path(n).name in FORBIDDEN_NAMES or '__pycache__' in n or n.endswith('.pyc')])
    ok('deterministic timestamps', all(i.date_time == (2026, 1, 1, 0, 0, 0) for i in infos))
    ex = Path(tmp) / zp.stem
    z.extractall(ex)
    root = ex / top
    files = [p for p in root.rglob('*') if p.is_file()]
    res['files'] = len(files); res['bytes'] = sum(p.stat().st_size for p in files)
    binary = [str(p.relative_to(root)) for p in files if b'\0' in p.read_bytes()]
    ok('text only (no binaries)', not binary, str(binary))
    fm = frontmatter((root / 'SKILL.md').read_text())
    ok('SKILL.md frontmatter has name+description', fm and fm.get('name') and fm.get('description'))
    ok('frontmatter name is slug-style', fm and re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', fm['name']), fm and fm['name'])
    hits = []
    for p in files:
        t = p.read_text(errors='replace')
        for pat in SECRET_PATTERNS:
            for m in pat.finditer(t):
                hits.append(f'{p.relative_to(root)}: {m.group(0)[:50]}')
    # Known, intentional: planted-defect calibration fixture with a dev default.
    hits = [h for h in hits if 'calibration/cases/token-refresh' not in h]
    ok('no secret-like strings (excluding documented fixture)', not hits, '; '.join(hits[:5]))
    risky = [f'{p.relative_to(root)}: {pat.pattern}' for p in files for pat in RISKY if pat.search(p.read_text(errors='replace'))]
    ok('no obviously dangerous shell patterns', not risky, '; '.join(risky[:5]))
    res['warnings'] = []
    if any('calibration/cases/token-refresh' in str(p) for p in files):
        res['warnings'].append("calibration fixture tokens.js contains `process.env.SESSION_SECRET || 'dev-secret'` (planted-defect test data); a secret scanner may flag it.")
    return root, top

def check_standalone(root, res, tmp, env):
    chk = res['checks']
    t = (root / 'SKILL.md').read_text()
    chk.append(('no ${CLAUDE_PLUGIN_ROOT} references (works outside a plugin)', '${CLAUDE_PLUGIN_ROOT}' not in t, ''))
    missing = [r for r in re.findall(r'`((?:references|scripts|examples)/[A-Za-z0-9_./-]+)`', t) if not (root / r).exists()]
    chk.append(('relative file references resolve', not missing, str(missing)))
    # `claude plugin validate` only accepts plugins, so wrap the skill in a throwaway one.
    wrap = Path(tmp) / 'wrap'
    (wrap / '.claude-plugin').mkdir(parents=True)
    (wrap / '.claude-plugin' / 'plugin.json').write_text('{"name":"agensi-validate","version":"0.0.0","description":"throwaway"}')
    shutil.copytree(root, wrap / 'skills' / root.name)
    code, out = run(['claude', 'plugin', 'validate', str(wrap)], env=env)
    chk.append(('claude plugin validate (skill wrapped in throwaway plugin)', code == 0, out[-300:]))

def check_complete(root, res, tmp, env):
    chk = res['checks']
    mk = root / 'marketplace'
    plugins = mk / 'plugins'
    miss = []
    for sk in plugins.glob('*/skills/*/SKILL.md'):
        plug = sk.parents[2]
        for ref in ROOT_REF.findall(sk.read_text()):
            if not (plug / ref).exists():
                miss.append(f'{sk.relative_to(plugins)} -> {ref}')
    for f in list(plugins.glob('*/agents/*.md')):
        for ref in ROOT_REF.findall(f.read_text()):
            if not (f.parents[1] / ref).exists():
                miss.append(f'{f.relative_to(plugins)} -> {ref}')
    chk.append(('all ${CLAUDE_PLUGIN_ROOT}/… references resolve', not miss, '; '.join(miss[:5])))
    hooks = json.loads((plugins / 'quorum/hooks/hooks.json').read_text())
    cmds = [h['command'] for g in hooks['hooks']['PreToolUse'] for h in g['hooks']]
    hm = [ROOT_REF.search(c).group(1) for c in cmds]
    chk.append(('hook command targets exist', all((plugins / 'quorum' / h).exists() for h in hm), str(hm)))
    agents = {p.stem for p in (plugins / 'quorum/agents').glob('*.md')}
    used = set(re.findall(r'quorum-(?:auditor|builder|judge|publisher|reviewer|scribe)', (plugins / 'quorum/workflow/pipeline.js').read_text()))
    chk.append(('workflow agents exist', used <= agents, str(used - agents)))
    mj = json.loads((mk / '.claude-plugin/marketplace.json').read_text())
    srcs_ok = all((mk / p['source']).is_dir() for p in mj['plugins'])
    chk.append(('marketplace.json sources exist', srcs_ok, ''))
    # exec bits preserved in the zip, matching the source tree
    zi = {i.filename: i for i in zipfile.ZipFile(res['zip']).infolist()}
    bad = []
    for src in (REPO / 'plugins').rglob('*'):
        if src.is_file() and (src.stat().st_mode & stat.S_IXUSR):
            arc = f"{root.name}/marketplace/plugins/{src.relative_to(REPO / 'plugins').as_posix()}"
            if not (zi[arc].external_attr >> 16) & stat.S_IXUSR:
                bad.append(arc)
    chk.append(('executable bits preserved for bin/*.py', not bad, str(bad)))
    code, out = run(['claude', 'plugin', 'validate', str(mk)], env=env)
    chk.append(('claude plugin validate (marketplace)', code == 0, out[-400:]))
    code, out = run(['claude', 'plugin', 'marketplace', 'add', str(mk)], env=env)
    chk.append(('isolated: marketplace add', code == 0, out[-300:]))
    if code == 0:
        for pl in ('quorum', 'tests'):
            c2, o2 = run(['claude', 'plugin', 'install', f'{pl}@quorum'], env=env)
            chk.append((f'isolated: install {pl}@quorum', c2 == 0, o2[-300:]))
    st = REPO / 'plugins/quorum/bin/selftest.py'
    code, out = run([sys.executable, str(plugins / 'quorum/bin/selftest.py')], cwd=str(tmp))
    chk.append(('extracted plugin selftest.py passes', code == 0, out[-300:]))

def main():
    zips = sorted((OUT / 'packages').glob('*.zip'))
    if not zips:
        sys.exit('no packages; run package.py first')
    before = subprocess.run(['git', 'status', '--porcelain'], cwd=REPO, capture_output=True, text=True).stdout
    results = []
    for zp in zips:
        with tempfile.TemporaryDirectory(prefix='agensi-val-') as tmp:
            env = isolated_env(tmp)
            res = dict(zip=str(zp), name=zp.name, checks=[], warnings=[])
            root, top = check_zip(zp, res, tmp)
            slug = re.sub(r'-\d+\.\d+\.\d+$', '', zp.stem)
            (check_complete if slug == 'quorum-complete' else check_standalone)(root, res, tmp, env)
            res['slug'] = slug
            failed = [c for c in res['checks'] if not c[1]]
            unv = UNVERIFIED.get(slug, [])
            res['unverified'] = unv
            res['status'] = 'FAIL' if failed else ('REVIEW REQUIRED' if unv else 'PASS')
            results.append(res)
    after = subprocess.run(['git', 'status', '--porcelain'], cwd=REPO, capture_output=True, text=True).stdout
    allowed = ('tools/', 'dist/', '.gitignore')
    changed = [l for l in after.splitlines() if not l[3:].startswith(allowed)]
    repo_ok = not changed
    lines = ['# Validation report', '', f'Generated by `tools/agensi/validate.py` on {datetime.date.today()}.', '',
             '| Package | Status | Files | Size |', '|---|---|---|---|']
    for r in results:
        lines.append(f"| {r['name']} | **{r['status']}** | {r['files']} | {r['bytes']/1024:.0f} KB |")
    lines += ['', f"Source repository unchanged except packaging additions: **{'yes' if repo_ok else 'NO'}**", '']
    if not repo_ok:
        lines += ['```', *changed, '```', '']
    for r in results:
        lines += [f"## {r['name']} — {r['status']}", '', '| Check | Result | Detail |', '|---|---|---|']
        for n, c, d in r['checks']:
            d = (d or '').replace('\n', ' ').replace('|', '\\|')[:160]
            lines.append(f"| {n} | {'pass' if c else '**FAIL**'} | {d} |")
        if r['unverified']:
            lines += ['', 'Unverified (blocks PASS):', *[f'- {u}' for u in r['unverified']]]
        if r['warnings']:
            lines += ['', 'Warnings:', *[f'- {w}' for w in r['warnings']]]
        lines.append('')
    (OUT / 'reports').mkdir(exist_ok=True)
    (OUT / 'reports' / 'validation.md').write_text('\n'.join(lines))
    for r in results:
        print(f"{r['status']:16} {r['name']}")
        for n, c, d in r['checks']:
            if not c: print('   FAIL', n, d[:200])
    if not repo_ok: print('REPO CHANGED', changed)
    sys.exit(1 if any(r['status'] == 'FAIL' for r in results) or not repo_ok else 0)

if __name__ == '__main__':
    main()
