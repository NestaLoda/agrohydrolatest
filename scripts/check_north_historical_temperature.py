"""Independent same-period reanalysis temperature check, no projection adjustment.

ERA5-Land temperature only: the provider's precipitation/radiation availability
differs, so no ERA5 forcing values are mislabelled ERA5-Land output here.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/north/rebuild_climate/historical_check'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / 'era5_land_1995_2014.json'
    meta_path = OUT / 'metadata.json'
    variables = ['temperature_2m_min', 'temperature_2m_max']
    params = {'latitude': 78.2232, 'longitude': 15.6469, 'start_date': '1995-01-01', 'end_date': '2014-12-31',
              'models': 'era5_land', 'daily': ','.join(variables), 'timezone': 'GMT', 'cell_selection': 'land',
              'temperature_unit': 'celsius'}
    url = 'https://archive-api.open-meteo.com/v1/archive?' + urlencode(params)
    if path.exists():
        raw = path.read_bytes()
        metadata = json.loads(meta_path.read_text(encoding='utf-8'))
        if hashlib.sha256(raw).hexdigest() != metadata['sha256']:
            raise ValueError('Historical reanalysis raw hash mismatch')
    else:
        with urlopen(Request(url, headers={'User-Agent': 'AgroHydro-North-Research/1.0'}), timeout=80) as response:
            raw = response.read()
        path.write_bytes(raw)
        metadata = {'url': url, 'accessed_at_utc': datetime.now(timezone.utc).isoformat(), 'sha256': hashlib.sha256(raw).hexdigest(),
                    'provider': 'Open-Meteo', 'requested_model': 'era5_land', 'classification': 'EXTERNAL_REANALYSIS_NOT_OBSERVATION',
                    'period': [1995, 2014], 'variables': variables,
                    'elevation_processing': 'Open-Meteo default 90 m DEM land-cell selection and statistical altitude downscaling; source elevation returned below.',
                    'projection_adjustment_applied': False, 'raw_path': path.relative_to(ROOT).as_posix(),
                    'documentation': 'https://open-meteo.com/en/docs/historical-weather-api',
                    'dataset_documentation': 'https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land?tab=overview',
                    'license': 'Open-Meteo CC BY 4.0; ERA5-Land Copernicus attribution',
                    'upstream_version': None, 'version_note': 'Provider does not expose upstream release; immutable retrieval hash identifies snapshot.'}
        meta_path.write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
    payload = json.loads(raw)
    daily = payload['daily']
    expected = pd.date_range('1995-01-01', '2014-12-31')
    if not pd.DatetimeIndex(daily['time']).equals(expected) or payload.get('utc_offset_seconds') != 0:
        raise ValueError('Incomplete UTC historical temperature chronology')
    for var in variables:
        if payload['daily_units'][var] != '°C' or not np.isfinite(daily[var]).all():
            raise ValueError('Wrong units or missing temperatures')
    tmin, tmax = (np.asarray(daily[var]) for var in variables)
    if np.any(tmin > tmax):
        raise ValueError('Invalid Tmin/Tmax')
    frame = pd.DataFrame({'date': expected, 'tmean_c': (tmin + tmax) / 2})
    summary = {'days': len(frame), 'mean_temperature_c': float(frame.tmean_c.mean()),
               'monthly_temperature_c': {str(m): float(part.tmean_c.mean()) for m, part in frame.groupby(frame.date.dt.month)},
               'mean_annual_gdd5_degree_days': float(np.maximum(frame.tmean_c - 5, 0).sum() / 20),
               'source_grid_and_elevation': {key: payload.get(key) for key in ['latitude', 'longitude', 'elevation']},
               'source_sha256': metadata['sha256'], 'status': 'validated_reanalysis_comparison_only',
               'projection_adjustment_applied': False,
               'limitations': ['Different grid/height selection and bias-reference datasets; difference is not measured forecast error.',
                               'Reanalysis is not an independent weather-station observation.',
                               'No future climate values are corrected or replaced using this comparison.']}
    package_path = OUT.parent / 'climate_contexts.json'
    if package_path.exists():
        package = json.loads(package_path.read_text(encoding='utf-8'))
        baseline = next(r for r in package['contexts'] if r['site_id'] == 'longyearbyen' and r['horizon_id'] == 'historical')
        summary['nasa_historical_mean_temperature_c'] = baseline['ensemble']['mean_temperature_c']['mean']
        summary['nasa_minus_reanalysis_temperature_c'] = summary['nasa_historical_mean_temperature_c'] - summary['mean_temperature_c']
        summary['nasa_context_sha256'] = hashlib.sha256(package_path.read_bytes()).hexdigest()
    (OUT / 'comparison.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
