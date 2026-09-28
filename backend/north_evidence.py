"""Read pinned U9 external evidence; never silently promote it to model inputs."""
import hashlib
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def load_north_evidence(root: Path | None = None) -> dict:
    base = (root or ROOT).resolve()
    manifest_path = base / 'data/north/u9_acquisition/manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    required = {'data/north_evidence.json', 'data/north/u9_acquisition/daily_point_2035.csv',
                'data/north/u9_acquisition/validated_summary.json',
                'data/north/u9_acquisition/catalog_resolved_attempts.json'}
    required |= {f'data/north/u9_acquisition/{s}_{v}_2035.nc'
                 for s in ('ssp245', 'ssp585') for v in ('tasmin', 'tasmax', 'pr')}
    records = manifest['files']
    if {r['path'] for r in records} != required or len(records) != len(required):
        raise ValueError('North evidence manifest does not match required files')
    for record in records:
        path = (base / record['path']).resolve()
        if not path.is_relative_to(base / 'data') or not path.is_file():
            raise ValueError('Invalid north evidence path')
        if hashlib.sha256(path.read_bytes()).hexdigest() != record['sha256']:
            raise ValueError('North evidence SHA256 mismatch: ' + record['path'])
    review = json.loads((base / 'data/north_evidence.json').read_text(encoding='utf-8'))
    summary = json.loads((base / 'data/north/u9_acquisition/validated_summary.json').read_text(encoding='utf-8'))
    rows = pd.read_csv(base / 'data/north/u9_acquisition/daily_point_2035.csv')
    if len(rows) != 730 or set(rows.scenario) != {'ssp245', 'ssp585'}:
        raise ValueError('Unexpected north point data scope')
    for scenario, group in rows.groupby('scenario'):
        dates = pd.to_datetime(group.date)
        if len(group) != 365 or dates.nunique() != 365 or set(dates.dt.year) != {2035}:
            raise ValueError('Unexpected north point dates')
        numeric = group[['tmin_c', 'tmax_c', 'precipitation_mm']]
        if numeric.isna().any().any() or not numeric.abs().lt(1e6).all().all():
            raise ValueError('Invalid north point values')
        if (group.tmin_c > group.tmax_c).any() or (group.precipitation_mm < 0).any():
            raise ValueError('Invalid north climate ordering')
        item = next(x for x in summary['scenarios'] if x['scenario'] == scenario)
        if item['production_input'] is not False or item['year'] != 2035:
            raise ValueError('North climate scope improperly promoted')
        if abs(float(group.precipitation_mm.sum()) - item['annual_precipitation_mm']) > .01:
            raise ValueError('North precipitation summary mismatch')
    monthly={}
    for scenario,group in rows.groupby('scenario'):
        group=group.copy();group['month']=pd.to_datetime(group.date).dt.month
        monthly[scenario]=[{'month':int(month),'tmin_c':float(g.tmin_c.mean()),'tmax_c':float(g.tmax_c.mean()),'precipitation_mm':float(g.precipitation_mm.sum())} for month,g in group.groupby('month')]
    return {**review, 'climate_2035': {**summary,'monthly':monthly},
            'integrity': {'verified': True, 'files_checked': len(records),
                          'manifest_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest()},
            'production_input': False}
