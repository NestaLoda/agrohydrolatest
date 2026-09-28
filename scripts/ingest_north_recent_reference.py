"""Pinned ERA5 daily recent reference, plus a same-provider historical check.

No best-match provider switching, weather filling, station-observation claim,
or automatic bias correction of NASA projections is performed.
"""
from datetime import datetime, timezone
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd

from scripts.ingest_north_rebuild_climate import period_metrics

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/north/rebuild_climate/recent_reference'
VARIABLES = {'temperature_2m_min': ('tmin_c', '°C'), 'temperature_2m_max': ('tmax_c', '°C'),
             'precipitation_sum': ('precipitation_mm', 'mm'), 'shortwave_radiation_sum': ('shortwave_mj_m2', 'MJ/m²')}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def parse_payload(payload):
    dates = pd.DatetimeIndex(payload['daily']['time'])
    if not dates.equals(pd.date_range('1995-01-01', '2025-12-31')) or payload.get('utc_offset_seconds') != 0:
        raise ValueError('Recent reference requires the complete UTC 1995–2025 chronology')
    columns = {'date': dates}
    for variable, (name, unit) in VARIABLES.items():
        if payload['daily_units'].get(variable) != unit:
            raise ValueError(f'Wrong reference unit: {variable}')
        values = np.asarray(payload['daily'][variable], dtype=float)
        if len(values) != len(dates) or not np.isfinite(values).all():
            raise ValueError(f'Missing/nonfinite recent reference values: {variable}')
        columns[name] = values
    frame = pd.DataFrame(columns)
    if (frame.tmin_c > frame.tmax_c).any() or (frame[['precipitation_mm', 'shortwave_mj_m2']] < 0).any().any():
        raise ValueError('Invalid recent reference physical values')
    return frame


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def main(offline=False):
    OUT.mkdir(parents=True, exist_ok=True)
    raw_path, meta_path = OUT / 'era5_1995_2025.json', OUT / 'metadata.json'
    params = {'latitude': 78.2232, 'longitude': 15.6469, 'start_date': '1995-01-01', 'end_date': '2025-12-31',
              'models': 'era5', 'daily': ','.join(VARIABLES), 'timezone': 'GMT', 'cell_selection': 'land',
              'elevation': 'nan', 'temperature_unit': 'celsius', 'precipitation_unit': 'mm'}
    url = 'https://archive-api.open-meteo.com/v1/archive?' + urlencode(params)
    if raw_path.exists() and meta_path.exists():
        raw = raw_path.read_bytes()
        metadata = json.loads(meta_path.read_text(encoding='utf-8'))
        if sha(raw) != metadata['sha256'] or metadata['url'] != url:
            raise ValueError('Recent reference raw hash/request mismatch')
    else:
        if offline:
            raise ValueError('No complete cached reference; network acquisition required')
        with urlopen(Request(url, headers={'User-Agent': 'AgroHydro-North-Research/1.0'}), timeout=120) as response:
            raw = response.read()
        parse_payload(json.loads(raw))
        metadata = {'url': url, 'accessed_at_utc': datetime.now(timezone.utc).isoformat(), 'sha256': sha(raw),
                    'requested_model': 'era5', 'classification': 'SOURCED_REANALYSIS_NOT_FIELD_OBSERVATION',
                    'period': [1995, 2025], 'variables': list(VARIABLES),
                    'elevation_processing': 'elevation=nan: statistical altitude downscaling disabled; land-cell selection.',
                    'raw_path': raw_path.relative_to(ROOT).as_posix(),
                    'documentation': 'https://open-meteo.com/en/docs/historical-weather-api',
                    'dataset_documentation': 'https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview',
                    'license': 'Open-Meteo CC BY 4.0; Copernicus ERA5 attribution',
                    'upstream_version': None, 'version_note': 'Provider has no upstream version identifier; hash pins retrieved snapshot.'}
        raw_path.write_bytes(raw)
        write_json(meta_path, metadata)
    payload = json.loads(raw)
    frame = parse_payload(payload)
    recent = frame.loc[frame.date.dt.year >= 2015].copy()
    daily_path = OUT / 'longyearbyen_recent_ERA5.csv.gz'
    recent.to_csv(daily_path, index=False, compression={'method': 'gzip', 'mtime': 0}, float_format='%.8f')
    member = {'model': 'ERA5', 'member': 'reanalysis', 'daily_path': daily_path.relative_to(ROOT).as_posix(),
              'daily_sha256': sha(daily_path.read_bytes()), **period_metrics(recent)}
    history = period_metrics(frame.loc[frame.date.dt.year <= 2014])
    band = lambda value: {'mean': value, 'min': value, 'max': value}
    nasa = json.loads((OUT.parent / 'climate_contexts.json').read_text(encoding='utf-8'))
    historical = next(c for c in nasa['contexts'] if c['horizon_id'] == 'historical' and c['site_id'] == 'longyearbyen')
    limitation = ['2015–2025 is an 11-year recent reference, not a 30-year climate normal or a 2025 station observation.',
                  'ERA5 reanalysis and NASA bias-adjusted CMIP6 are different datasets/grids. Direct plan differences include dataset effects and cannot be attributed solely to climate change.',
                  'Single reanalysis member has no inter-model spread; equal min/max is not zero uncertainty.',
                  'Precipitation includes snow water equivalent, not accessible catchment flow or agricultural allocation.',
                  'No automatic bias correction or replacement of future NASA daily series was applied.']
    context = {'site_id': 'longyearbyen', 'horizon_id': 'recent', 'scenario_id': 'recent', 'period': [2015, 2025],
               'years': 11, 'models': [member], 'ensemble': {k: band(v) for k, v in member['summary'].items()},
               'monthly': [{'month': m['month'], **{k: band(v) for k, v in m.items() if k != 'month'}} for m in member['monthly']],
               'dataset': 'ERA5 via Open-Meteo', 'dataset_version': 'retrieval-sha256',
               'site': {'label': 'Longyearbyen / Svalbard', 'latitude': 78.2232, 'longitude': 15.6469,
                        'grid_latitude': payload['latitude'], 'grid_longitude': payload['longitude'], 'grid_elevation_m': payload['elevation']},
               'classification': 'SOURCED_REANALYSIS_NOT_FIELD_OBSERVATION', 'limitations': limitation,
               'ensemble_method': 'One ERA5 trajectory; min=max is the point estimate, not an uncertainty bound.',
               'temperature_mean_method': '(daily Tmin + daily Tmax) / 2; same approximation as future model.',
               'sources': [metadata['documentation'], metadata['dataset_documentation']],
               'change_from_historical': {k: v['mean'] - historical['ensemble'][k]['mean'] for k, v in {k: band(v) for k, v in member['summary'].items()}.items()},
               'cross_dataset_check': {'period': [1995, 2014], 'era5_summary': history['summary'],
                   'nasa_minus_era5': {k: historical['ensemble'][k]['mean'] - v for k, v in history['summary'].items()},
                   'recent_minus_era5_historical': {k: member['summary'][k] - v for k, v in history['summary'].items()},
                   'projection_adjustment_applied': False, 'classification': 'COMPARABILITY_DIAGNOSTIC_NOT_VALIDATION'},
               'reference_policy': 'Same-engine resource scenario under recent reanalysis; not observed present agriculture. Future-vs-recent deltas are cross-dataset scenario comparisons.'}
    context_path = OUT / 'context.json'
    write_json(context_path, context)
    write_json(OUT / 'manifest.json', {'status': 'ready', 'built_at_utc': datetime.now(timezone.utc).isoformat(),
                'period': [2015, 2025], 'raw_period': [1995, 2025], 'raw_days': len(frame), 'recent_days': len(recent),
                'raw_files': [{'path': raw_path.relative_to(ROOT).as_posix(), 'sha256': sha(raw)},
                              {'path': meta_path.relative_to(ROOT).as_posix(), 'sha256': sha(meta_path.read_bytes())}],
                'derived_files': [{'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p.read_bytes())} for p in [daily_path, context_path]],
                'nasa_context_sha256': sha((OUT.parent / 'climate_contexts.json').read_bytes())})
    print(json.dumps({'status': 'ready', 'recent_days': len(recent), 'summary': member['summary'], 'cross_dataset_check': context['cross_dataset_check']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--offline', action='store_true')
    main(parser.parse_args().offline)
