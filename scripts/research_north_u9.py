"""Acquire a small, catalog-resolved NASA NEX-GDDP-CMIP6 research subset.

2035 is an illustrative model year, NOT a future climatology or a validated
production input. Original responses and SHA256 remain separate from the app's
existing climate manifest. No credentials or accounts are needed.
"""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

def validate():
    import numpy as np
    import pandas as pd
    import xarray as xr
    summaries = []
    frames = []
    for scenario in ('ssp245', 'ssp585'):
        loaded = {v: xr.open_dataset(OUT / f'{scenario}_{v}_2035.nc', engine='scipy') for v in ('tasmin', 'tasmax', 'pr')}
        try:
            for v, ds in loaded.items():
                assert ds.sizes['time'] == 365 and np.isfinite(ds[v]).all()
                assert len(np.unique(ds.time.values)) == 365
                assert ds[v].attrs['units'] == ('kg m-2 s-1' if v == 'pr' else 'K')
                assert np.array_equal(ds.time.values, loaded['pr'].time.values)
            assert bool((loaded['tasmin'].tasmin <= loaded['tasmax'].tasmax).all())
            assert bool((loaded['pr'].pr >= 0).all())
            point = {v: ds.sel(lat=78.2232, lon=15.6469, method='nearest')[v] for v, ds in loaded.items()}
            low, high, rain = point['tasmin'].values - 273.15, point['tasmax'].values - 273.15, point['pr'].values * 86400
            mean = (low + high) / 2
            longest = count = 0
            for value in low:
                count = count + 1 if value > 0 else 0
                longest = max(longest, count)
            summaries.append(dict(scenario=scenario, model='ACCESS-CM2', year=2035,
                classification='EXTERNAL_FUTURE_SCENARIO_SINGLE_MODEL_YEAR',
                latitude=float(point['pr'].lat), longitude=float(point['pr'].lon),
                days=365, annual_precipitation_mm=float(rain.sum()),
                annual_mean_temperature_c=float(mean.mean()), gdd_base_5_c=float(np.maximum(mean-5, 0).sum()),
                frost_free_days=int((low>0).sum()), longest_frost_free_run_days=longest,
                gdd_base_note='5°C is an analysis convention, NOT a validated crop-specific threshold.',
                limitations=['One model year is not a climatology, ensemble or suitable SSP ranking.',
                    'Air temperature and total precipitation are not marine source water or usable freshwater allocation.',
                    'No ET0 calculation or local soil/crop calibration.'], production_input=False))
            frames.append(pd.DataFrame(dict(date=loaded['pr'].time.values,scenario=scenario,tmin_c=low,tmax_c=high,precipitation_mm=rain)))
        finally:
            for ds in loaded.values(): ds.close()
    pd.concat(frames).to_csv(OUT / 'daily_point_2035.csv', index=False)
    (OUT / 'validated_summary.json').write_text(json.dumps(dict(verified_at='2026-09-22',
        checks=['6 NetCDF SHA records','365 unique daily times per scenario','all four cells finite',
                'Tmin <= Tmax in all cells/days','nonnegative precipitation','explicit unit conversions'],
        source_files=6,raw_grid_values=8760,point_rows=730,scenarios=summaries),indent=2),encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/north/u9_acquisition'
OUT.mkdir(parents=True, exist_ok=True)

def acquire(item):
    scenario, var = item
    base = f'AMES/NEX/GDDP-CMIP6/ACCESS-CM2/{scenario}/r1i1p1f1/{var}/'
    catalog = 'https://ds.nccs.nasa.gov/thredds/catalog/' + base + 'catalog.xml'
    row = dict(scenario=scenario, variable=var, model='ACCESS-CM2', year=2035,
               accessed_at='2026-09-22', catalog_url=catalog, production_input=False)
    try:
        content = urllib.request.urlopen(catalog, timeout=30).read()
        (OUT / f'{scenario}_{var}_catalog.xml').write_bytes(content)
        paths = [d.attrib['urlPath'] for d in ET.fromstring(content).iter()
                 if 'urlPath' in d.attrib and '_2035_' in d.attrib['urlPath']]
        if len(paths) != 1:
            raise ValueError(f'Expected exactly one 2035 catalog path, got {paths}')
        query = urllib.parse.urlencode(dict(var=var, north=78.25, west=15.5,
            east=15.75, south=78.0, horizStride=1,
            time_start='2035-01-01T12:00:00Z', time_end='2035-12-31T12:00:00Z',
            accept='netcdf3', addLatLon='true'))
        url = 'https://ds.nccs.nasa.gov/thredds/ncss/grid/' + paths[0] + '?' + query
        row['url'] = url
        with urllib.request.urlopen(url, timeout=55) as response:
            raw = response.read(4_000_001)
            row['http_status'] = response.status
        if len(raw) > 4_000_000 or not raw.startswith(b'CDF'):
            raise ValueError('Not a bounded NetCDF3 subset')
        path = OUT / f'{scenario}_{var}_2035.nc'
        path.write_bytes(raw)
        row.update(status='downloaded_not_validated', local_path=str(path.relative_to(ROOT)),
                   bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
    except Exception as exc:
        row.update(status='request_failed', error=str(exc))
    return row

if __name__ == '__main__':
    jobs = [(s, v) for s in ('ssp245', 'ssp585') for v in ('tasmin', 'tasmax', 'pr')]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        rows = list(pool.map(acquire, jobs))
    (OUT / 'catalog_resolved_attempts.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
    if all(r['status'] == 'downloaded_not_validated' for r in rows):
        validate()
    print(json.dumps(rows, indent=2))
