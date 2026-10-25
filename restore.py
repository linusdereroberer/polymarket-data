"""Restore private release assets with Python 3's standard library and gh CLI."""
import argparse
import hashlib
import json
import shutil
import subprocess
import time
import zipfile
from pathlib import Path, PurePosixPath

def sha256(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def safe_path(root, name):
    p = PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or '\\' in name or ':' in name:
        raise ValueError('Unsafe manifest path')
    result = root.joinpath(*p.parts).resolve()
    if not result.is_relative_to(root.resolve()):
        raise ValueError('Path escapes destination')
    return result

def extract_archive(path, archive, manifest, dest, min_free=0):
    if path.stat().st_size != archive['size'] or sha256(path) != archive['sha256']:
        raise ValueError('Archive hash/size mismatch: ' + archive['name'])
    expected = {}
    for f in manifest['files']:
        for part in f['parts']:
            if part['archive'] == archive['name']:
                expected[part['member']] = (f, part)
    with zipfile.ZipFile(path) as z:
        if sorted(z.namelist()) != sorted(expected):
            raise ValueError('Unexpected or missing archive members')
        for member, (f, part) in expected.items():
            target = safe_path(dest, f['path'])
            target.parent.mkdir(parents=True, exist_ok=True)
            h = hashlib.sha256(); count = 0
            with z.open(member) as src, target.open('r+b' if target.exists() else 'w+b') as out:
                out.seek(part['offset'])
                while chunk := src.read(1024 * 1024):
                    if min_free and shutil.disk_usage(dest).free < min_free + len(chunk) + 128*1024**2:
                        raise RuntimeError('Disk reserve reached during restore')
                    if count + len(chunk) > part['size']:
                        raise ValueError('Oversized member')
                    h.update(chunk); out.write(chunk); count += len(chunk)
                if part['offset'] + part['size'] == f['size']:
                    out.truncate(f['size'])
            if count != part['size'] or h.hexdigest() != part['sha256']:
                raise ValueError('Member hash/size mismatch: ' + f['path'])

def verify_files(manifest, dest, selected=None):
    checked = 0
    for f in manifest['files']:
        if selected is not None and not all(p['archive'] in selected for p in f['parts']):
            continue
        target = safe_path(dest, f['path'])
        if target.stat().st_size != f['size'] or sha256(target) != f['sha256']:
            raise ValueError('Restored file hash/size mismatch: ' + f['path'])
        checked += 1
    return checked

def download(repo, tag, name, cache):
    for attempt in range(5):
        p = subprocess.run(['gh','release','download',tag,'--repo',repo,'--pattern',name,'--dir',str(cache),'--clobber'])
        if p.returncode == 0:
            return
        time.sleep(min(5 * (attempt+1), 30))
    raise RuntimeError('Download failed: ' + name)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest', type=Path, default=Path(__file__).with_name('MANIFEST.json'))
    p.add_argument('--destination', type=Path, default=Path('restored-data'))
    p.add_argument('--archives', nargs='*', help='Optional subset for restore testing')
    p.add_argument('--min-free-gib', type=float, default=12)
    a = p.parse_args()
    m = json.loads(a.manifest.read_text(encoding='utf-8'))
    dest = a.destination.resolve()
    if dest.exists() and any(dest.iterdir()):
        raise ValueError('Choose an empty destination to protect existing data')
    dest.mkdir(parents=True, exist_ok=True)
    cache = dest / '.release-download'; cache.mkdir()
    selected = set(a.archives) if a.archives else {x['name'] for x in m['archives']}
    if selected - {x['name'] for x in m['archives']}:
        raise ValueError('Unknown archive requested')
    for arc in m['archives']:
        if arc['name'] not in selected:
            continue
        needed = arc['size'] + sum(part['size'] for f in m['files'] for part in f['parts'] if part['archive'] == arc['name'])
        if shutil.disk_usage(dest).free < needed + int(a.min_free_gib*1024**3) + 128*1024**2:
            raise RuntimeError('Insufficient disk for next archive plus reserve')
        download(m['repository'], m['tag'], arc['name'], cache)
        local = cache / arc['name']
        extract_archive(local, arc, m, dest, int(a.min_free_gib*1024**3))
        local.unlink()
        print('Restored and verified ' + arc['name'], flush=True)
    checked = verify_files(m, dest, selected)
    cache.rmdir()
    print(f'Verified {checked} complete files; split members verified individually. Selection: {len(selected)} archives.')

if __name__ == '__main__':
    main()
