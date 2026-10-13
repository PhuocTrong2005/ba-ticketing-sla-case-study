"""Install portable Node and pinned Newman in ignored, project-local tooling.

Does not change Python/backend dependencies or the machine PATH.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / '.postman-tools'


def main():
    TOOLS.mkdir(exist_ok=True)
    base = 'https://nodejs.org/dist/latest-v22.x/'
    sums = urllib.request.urlopen(base + 'SHASUMS256.txt', timeout=60).read().decode()
    sha, name = next(line.split() for line in sums.splitlines() if re.search(r'node-v[\d.]+-win-x64\.zip$', line))
    target = TOOLS / name
    if not target.exists():
        urllib.request.urlretrieve(base + name, target)
    actual = hashlib.sha256(target.read_bytes()).hexdigest()
    if actual != sha:
        raise RuntimeError('Official Node archive SHA-256 mismatch')
    node_dir = TOOLS / name.removesuffix('.zip')
    if not node_dir.exists():
        with zipfile.ZipFile(target) as archive:
            for item in archive.infolist():
                path = (TOOLS / item.filename).resolve()
                if not path.is_relative_to(TOOLS.resolve()):
                    raise RuntimeError('Archive path outside tooling directory')
            archive.extractall(TOOLS)
    node = node_dir / 'node.exe'
    cli = TOOLS / 'newman/node_modules/newman/bin/newman.js'
    command = [str(node), str(node_dir / 'node_modules/npm/bin/npm-cli.js'),
               'install', '--prefix', str(TOOLS / 'newman'), '--cache', str(TOOLS / 'npm-cache'),
               '--ignore-scripts', '--no-audit', '--no-fund', 'newman@6.2.1']
    if not cli.exists():
        subprocess.run(command, cwd=ROOT, check=True)
    record = {'node_download': base + name, 'node_archive_sha256': actual,
              'node_version': subprocess.check_output([str(node), '--version'], text=True).strip(),
              'npm_version': subprocess.check_output([str(node), str(node_dir / 'node_modules/npm/bin/npm-cli.js'), '--version'], text=True).strip(),
              'newman_version': subprocess.check_output([str(node), str(cli), '--version'], text=True).strip(),
              'install_options': ['--ignore-scripts', '--no-audit', '--no-fund', 'newman@6.2.1'],
              'scope': 'Ignored .postman-tools only; no backend dependencies or global PATH changes.'}
    (TOOLS / 'tool-paths.json').write_text(json.dumps({'node': str(node), 'newman': str(cli)}, indent=2), encoding='utf8')
    path = ROOT / ('tests/evidence/postman-tools-' + time.strftime('%Y%m%d-%H%M%S', time.gmtime()) + '.json')
    path.write_text(json.dumps(record, indent=2), encoding='utf8')
    print(json.dumps(record, indent=2))
    print(path)


if __name__ == '__main__':
    main()
