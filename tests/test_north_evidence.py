import json
import shutil
from pathlib import Path

import pytest

from backend.north_evidence import ROOT, load_north_evidence


def copy_evidence(tmp_path):
    manifest = ROOT / 'data/north/u9_acquisition/manifest.json'
    records = json.loads(manifest.read_text(encoding='utf-8'))['files']
    for relative in [r['path'] for r in records] + ['data/north/u9_acquisition/manifest.json']:
        dst = tmp_path / relative
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, dst)
    return tmp_path


def test_review_keeps_local_unknowns_and_real_two_scenario_scope():
    result = load_north_evidence()
    assert result['production_input'] is False
    assert result['integrity']['files_checked'] == 10
    assert result['climate_2035']['point_rows'] == 730
    assert {r['scenario'] for r in result['climate_2035']['scenarios']} == {'ssp245', 'ssp585'}
    assert all(not r['locally_validated'] for r in result['candidates'])
    assert next(x for x in result['layers'] if x['id'] == 'marine_profile')['status'] == 'catalog_only'


@pytest.mark.parametrize('relative', ['data/north/u9_acquisition/ssp245_tasmin_2035.nc',
    'data/north/u9_acquisition/daily_point_2035.csv',
    'data/north/u9_acquisition/validated_summary.json'])
def test_raw_or_derived_tampering_rejected(tmp_path, relative):
    root = copy_evidence(tmp_path)
    with (root / relative).open('ab') as file:
        file.write(b' altered')
    with pytest.raises(ValueError, match='SHA256 mismatch'):
        load_north_evidence(root)


def test_manifest_cannot_drop_raw_records(tmp_path):
    root = copy_evidence(tmp_path)
    path = root / 'data/north/u9_acquisition/manifest.json'
    data = json.loads(path.read_text())
    data['files'].pop()
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match='required files'):
        load_north_evidence(root)
