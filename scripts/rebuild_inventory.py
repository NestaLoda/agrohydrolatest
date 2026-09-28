"""Read-only source inventory; archive pre-rebuild UI and record immutable assets."""
from pathlib import Path
import hashlib
import json
import zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/verification/rebuild'
OUT.mkdir(parents=True, exist_ok=True)
skip = {'.git', 'node_modules', '.venv', '__pycache__', '.pytest_cache', 'dist'}
files = sorted(p for p in ROOT.rglob('*') if p.is_file() and not skip.intersection(p.relative_to(ROOT).parts) and 'docs/verification/rebuild' not in p.relative_to(ROOT).as_posix())
manifest = []
for path in files:
    raw = path.read_bytes()
    manifest.append({'path': path.relative_to(ROOT).as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
(OUT / 'before-inventory.json').write_text(json.dumps({'at': datetime.now(timezone.utc).isoformat(), 'excluded_generated_directories': sorted(skip), 'files': manifest}, ensure_ascii=False, indent=2), encoding='utf-8')
(OUT / 'repository-tree.txt').write_text('\n'.join(x['path'] for x in manifest), encoding='utf-8')
with zipfile.ZipFile(OUT / 'before-product.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    for path in files:
        if path.relative_to(ROOT).parts[0] in {'frontend', 'backend'} or path.name == 'ANA_CHAT_TESLIM.txt':
            archive.write(path, path.relative_to(ROOT))
print(f'{len(manifest)} source files inventoried; UI/backend/handoff archived.')
