"""Reproducible, resumable NASA NEX-GDDP-CMIP6 v2 point acquisition.

This downloads small annual NCSS subsets, never entire global grids. Raw bytes,
catalogs, URL, timestamps, file metadata and SHA256 are retained. A partial run
never becomes a ready climatology. Use --offline to validate/rebuild all outputs.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import io
import json
from pathlib import Path
import re
import time
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd
import xarray as xr

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/north/rebuild_climate'
BASE = 'https://ds.nccs.nasa.gov/thredds/'
MODELS = ['ACCESS-CM2', 'MPI-ESM1-2-HR', 'MRI-ESM2-0']
VARIABLES = {'tasmin': 'K', 'tasmax': 'K', 'pr': 'kg m-2 s-1', 'rsds': 'W m-2'}
SITES = {
    'longyearbyen': {'label': 'Longyearbyen / Svalbard', 'latitude': 78.2232, 'longitude': 15.6469,
                    'grid_latitude': 78.125, 'grid_longitude': 15.625},
    'tromso': {'label': 'Tromsø / Kuzey Norveç', 'latitude': 69.6492, 'longitude': 18.9553,
               'grid_latitude': 69.625, 'grid_longitude': 18.875},
}
PERIODS = {'historical': [1995, 2014], 'near': [2021, 2040], 'mid': [2041, 2060], 'late': [2081, 2100]}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    temporary.replace(path)


def read_url(url):
    request = Request(url, headers={'User-Agent': 'AgroHydro-North-Research/1.0'})
    with urlopen(request, timeout=80) as response:
        data = response.read(2_000_001)
    if len(data) > 2_000_000:
        raise ValueError('Unexpected large response for a one-cell subset')
    return data


def catalog(model, scenario, var, offline=False):
    path = OUT / 'catalogs' / f'{model}_{scenario}_{var}.xml'
    url = BASE + f'catalog/AMES/NEX/GDDP-CMIP6/{model}/{scenario}/r1i1p1f1/{var}/catalog.xml'
    if not path.exists():
        if offline:
            raise ValueError(f'Missing cached catalog: {path}')
        raw = read_url(url)
        ET.fromstring(raw)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        write_json(path.with_suffix('.json'), {'url': url, 'sha256': sha(raw), 'accessed_at_utc': datetime.now(timezone.utc).isoformat()})
    raw = path.read_bytes()
    meta = json.loads(path.with_suffix('.json').read_text(encoding='utf-8'))
    if sha(raw) != meta['sha256']:
        raise ValueError('Catalog hash mismatch')
    entries = {}
    for node in ET.fromstring(raw).iter():
        source = node.attrib.get('urlPath', '')
        match = re.search(r'_(\d{4})_v2\.0\.nc$', source)
        if match:
            year = int(match[1])
            if year in entries:
                raise ValueError(f'Duplicate v2 catalog year {year}')
            entries[year] = source
    return entries


def parse_raw(raw, var, year, site, model, scenario):
    if not raw.startswith(b'CDF'):
        raise ValueError('NCSS did not return NetCDF3')
    with xr.open_dataset(io.BytesIO(raw), engine='scipy') as ds:
        if ds[var].attrs.get('units') != VARIABLES[var]:
            raise ValueError(f'Wrong {var} units')
        if ds.attrs.get('version') != '2.0' or ds.attrs.get('cmip6_source_id') != model or ds.attrs.get('scenario') != scenario:
            raise ValueError('Dataset identity/version mismatch')
        if ds.attrs.get('variant_label') != 'r1i1p1f1':
            raise ValueError('Unexpected ensemble member')
        if ds.sizes.get('lat') != 1 or ds.sizes.get('lon') != 1:
            raise ValueError('Expected one explicit grid cell')
        if float(ds.lat.values[0]) != SITES[site]['grid_latitude'] or float(ds.lon.values[0]) != SITES[site]['grid_longitude']:
            raise ValueError('Unexpected returned grid')
        dates = pd.DatetimeIndex(ds.time.values).normalize()
        expected = pd.date_range(f'{year}-01-01', f'{year}-12-31')
        if not dates.equals(expected):
            raise ValueError(f'Incomplete/non-Gregorian/duplicate daily dates: {var} {year}')
        values = ds[var].values.reshape(-1).astype(float)
        if not np.isfinite(values).all() or (var in ('pr', 'rsds') and (values < 0).any()):
            raise ValueError(f'Invalid or negative values: {var}')
        if var in ('tasmin', 'tasmax') and ((values < 170) | (values > 340)).any():
            raise ValueError('Out-of-range Kelvin values')
        attrs = {key: ds.attrs.get(key) for key in ('version', 'variant_label', 'cmip6_source_id', 'cmip6_institution_id',
                    'cmip6_license', 'source', 'creation_date', 'tracking_id', 'resolution_id')}
        attrs['calendar'] = ds.time.encoding.get('calendar', 'standard')
    return dates, values, attrs


def acquire(job, offline=False):
    site, model, scenario, var, year, source = job
    stem = OUT / 'raw' / site / model / scenario / f'{var}_{year}'
    ncpath = stem.with_suffix('.nc')
    metapath = stem.with_suffix('.json')
    if ncpath.exists() and metapath.exists():
        raw = ncpath.read_bytes()
        meta = json.loads(metapath.read_text(encoding='utf-8'))
        if sha(raw) != meta['sha256']:
            raise ValueError(f'Raw hash mismatch: {ncpath}')
        parse_raw(raw, var, year, site, model, scenario)
        return meta
    if offline:
        raise ValueError(f'Missing cached raw: {ncpath}')
    loc = SITES[site]
    params = dict(var=var, north=loc['grid_latitude'], south=loc['grid_latitude'], west=loc['grid_longitude'],
                  east=loc['grid_longitude'], time_start=f'{year}-01-01T00:00:00Z', time_end=f'{year}-12-31T23:59:59Z',
                  accept='netcdf3', addLatLon='true')
    url = BASE + 'ncss/grid/' + source + '?' + urlencode(params)
    failures = []
    for attempt in range(3):
        try:
            accessed = datetime.now(timezone.utc).isoformat()
            raw = read_url(url)
            dates, _, attrs = parse_raw(raw, var, year, site, model, scenario)
            meta = {'site_id': site, 'model': model, 'scenario': scenario, 'variable': var, 'year': year,
                    'url': url, 'catalog_path': source, 'accessed_at_utc': accessed, 'sha256': sha(raw),
                    'local_path': ncpath.relative_to(ROOT).as_posix(), 'bytes': len(raw), 'day_count': len(dates),
                    'units': VARIABLES[var], 'grid': {'latitude': loc['grid_latitude'], 'longitude': loc['grid_longitude']},
                    'attributes': attrs, 'classification': 'SOURCED_CLIMATE_MODEL', 'previous_failed_attempts': failures}
            ncpath.parent.mkdir(parents=True, exist_ok=True)
            ncpath.write_bytes(raw)
            write_json(metapath, meta)
            return meta
        except Exception as exc:
            failures.append({'time_utc': datetime.now(timezone.utc).isoformat(), 'error': str(exc)})
            if attempt < 2:
                time.sleep(2 + attempt * 2)
    write_json(stem.with_suffix('.failed.json'), {'url': url, 'failures': failures})
    raise ValueError(f'Acquisition failed: {site}/{model}/{scenario}/{var}/{year}: {failures[-1]}')


def longest_run(mask):
    longest = current = 0
    for flag in mask:
        current = current + 1 if flag else 0
        longest = max(longest, current)
    return longest


def annual_metrics(frame):
    result = []
    for year, part in frame.groupby(frame.date.dt.year):
        if not pd.DatetimeIndex(part.date).equals(pd.date_range(f'{year}-01-01', f'{year}-12-31')):
            raise ValueError('Annual metrics require complete ordered Gregorian years')
        mean = (part.tmin_c + part.tmax_c) / 2
        result.append({'year': int(year), 'days': len(part), 'mean_temperature_c': float(mean.mean()),
                       'gdd0_degree_days': float(np.maximum(mean, 0).sum()),
                       'gdd5_degree_days': float(np.maximum(mean - 5, 0).sum()),
                       'frost_free_days': int((part.tmin_c > 0).sum()),
                       'frost_free_run_days': longest_run(part.tmin_c > 0),
                       'growing_season_5c_run_days': longest_run(mean > 5),
                       'precipitation_mm': float(part.precipitation_mm.sum()),
                       'shortwave_mj_m2': float(part.shortwave_mj_m2.sum()),
                       'heating_degree_days_18c': float(np.maximum(18 - mean, 0).sum()),
                       'summer_temperature_c': float(mean.loc[part.date.dt.month.isin([6, 7, 8])].mean())})
    return result


def period_metrics(frame):
    annual = annual_metrics(frame)
    year_count = len(annual)
    summary = {key: float(np.mean([row[key] for row in annual])) for key in annual[0] if key not in ('year', 'days')}
    monthly = []
    for month, part in frame.groupby(frame.date.dt.month):
        # Mean of each annual monthly total; one complete value per year.
        totals = part.groupby(part.date.dt.year)[['precipitation_mm', 'shortwave_mj_m2']].sum()
        monthly.append({'month': int(month), 'mean_temperature_c': float(((part.tmin_c + part.tmax_c) / 2).mean()),
                        'mean_tmin_c': float(part.tmin_c.mean()), 'mean_tmax_c': float(part.tmax_c.mean()),
                        'precipitation_mm': float(totals.precipitation_mm.mean()),
                        'shortwave_mj_m2': float(totals.shortwave_mj_m2.mean()),
                        'shortwave_daily_mj_m2': float(part.shortwave_mj_m2.mean()),
                        'heating_degree_days_18c': float(np.maximum(18 - (part.tmin_c + part.tmax_c) / 2, 0).sum() / year_count)})
    return {'years': len(annual), 'daily_rows': len(frame), 'annual': annual, 'summary': summary, 'monthly': monthly}


def build(sites, manifests):
    contexts, outputs = [], []
    for site in sites:
        for horizon, (start, end) in PERIODS.items():
            for scenario in (['historical'] if horizon == 'historical' else ['ssp245', 'ssp585']):
                members = []
                for model in MODELS:
                    years = []
                    for year in range(start, end + 1):
                        columns = {}
                        for var in VARIABLES:
                            raw = (OUT / 'raw' / site / model / scenario / f'{var}_{year}.nc').read_bytes()
                            dates, values, _ = parse_raw(raw, var, year, site, model, scenario)
                            columns[var] = values
                        if (columns['tasmin'] > columns['tasmax']).any():
                            raise ValueError(f'Tmin>Tmax: {site}/{model}/{scenario}/{year}')
                        years.append(pd.DataFrame({'date': dates, 'tmin_c': columns['tasmin'] - 273.15,
                                                   'tmax_c': columns['tasmax'] - 273.15, 'precipitation_mm': columns['pr'] * 86400,
                                                   'shortwave_mj_m2': columns['rsds'] * .0864}))
                    frame = pd.concat(years, ignore_index=True)
                    path = OUT / 'daily' / f'{site}_{horizon}_{scenario}_{model}.csv.gz'
                    path.parent.mkdir(parents=True, exist_ok=True)
                    frame.to_csv(path, index=False, compression={'method': 'gzip', 'mtime': 0}, float_format='%.8f')
                    outputs.append({'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(path.read_bytes()), 'rows': len(frame)})
                    members.append({'model': model, 'member': 'r1i1p1f1', 'daily_path': path.relative_to(ROOT).as_posix(),
                                    'daily_sha256': sha(path.read_bytes()), **period_metrics(frame)})
                def band(key, rows):
                    values = [row[key] for row in rows]
                    return {'mean': float(np.mean(values)), 'min': float(min(values)), 'max': float(max(values))}
                keys = members[0]['summary'].keys()
                ensemble = {key: band(key, [m['summary'] for m in members]) for key in keys}
                monthly = [{'month': month, **{key: band(key, [m['monthly'][month - 1] for m in members])
                             for key in members[0]['monthly'][0] if key != 'month'}} for month in range(1, 13)]
                contexts.append({'site_id': site, 'horizon_id': horizon, 'scenario_id': scenario, 'period': [start, end],
                                 'years': 20, 'models': members, 'ensemble': ensemble, 'monthly': monthly})
    package = {'schema_version': '1.0', 'status': 'ready', 'dataset': 'NASA NEX-GDDP-CMIP6', 'dataset_version': '2.0',
               'built_at_utc': datetime.now(timezone.utc).isoformat(), 'classification': 'SOURCED_CLIMATE_MODEL_AND_DERIVED_ANALYSIS',
               'sites': {site: SITES[site] for site in sites}, 'periods': PERIODS, 'model_ids': MODELS, 'contexts': contexts,
               'ensemble_method': 'Unweighted arithmetic mean; min/max of three model period means, not a probability interval.',
               'temperature_mean_method': '(daily Tmin + daily Tmax) / 2; an analysis approximation, not the independently downloaded tas variable.',
               'sources': ['https://doi.org/10.7917/OFSG3345', 'https://doi.org/10.1038/s41597-022-01393-4',
                           'https://www.nccs.nasa.gov/wp-content/uploads/2025/06/NEX-GDDP-CMIP6-v2-Tech_Note.pdf',
                           'https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-1/'],
               'limitations': ['Three GCM families and one member each do not span the full CMIP6 uncertainty.',
                               'Historical is bias-adjusted historical model output, not an observed present-day measurement.',
                               '0.25-degree coastal/island grid cells do not resolve a farm, valley, glacier or water catchment.',
                               'NASA cautions that small-island values may be unrealistic; local CARRA/station comparison remains required.',
                               'Precipitation includes snow water equivalent; it is not runoff, storage or usable agricultural water.',
                               'GDD0/GDD5 and frost-free runs are calculated indicators, not locally validated crop thresholds or yields.',
                               '18 C heating-degree-days are an explicit reference temperature, not a measured building energy need.',
                               'Monthly means are not a coherent actual growing year; daily per-model trajectories are retained.']}
    path = OUT / 'climate_contexts.json'
    write_json(path, package)
    outputs.append({'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(path.read_bytes())})
    write_json(OUT / 'manifest.json', {'schema_version': '1.0', 'status': 'ready', 'created_at_utc': datetime.now(timezone.utc).isoformat(),
                                      'raw_file_count': len(manifests), 'raw_files': manifests, 'derived_files': outputs,
                                      'source_value_count': sum(r['day_count'] for r in manifests),
                                      'daily_point_rows': sum(r.get('rows', 0) for r in outputs)})
    write_json(OUT / 'acquisition_progress.json', {'ready': True, 'downloaded_validated': len(manifests),
                                                  'total': len(manifests), 'failures': []})
    print(json.dumps({'status': 'ready', 'contexts': len(contexts), 'raw_files': len(manifests), 'daily_rows': sum(r.get('rows', 0) for r in outputs)}), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sites', nargs='+', choices=list(SITES), default=['longyearbyen'])
    parser.add_argument('--workers', type=int, default=6, choices=range(1, 9))
    parser.add_argument('--offline', action='store_true')
    parser.add_argument('--limit', type=int, help='Probe only: never builds ready outputs')
    args = parser.parse_args()
    requests = [(model, scenario, var) for model in MODELS for scenario in ['historical', 'ssp245', 'ssp585'] for var in VARIABLES]
    catalogs = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(args.workers, 4)) as pool:
        futures = {pool.submit(catalog, *key, args.offline): key for key in requests}
        for future in concurrent.futures.as_completed(futures):
            catalogs[futures[future]] = future.result()
    jobs = []
    for site in args.sites:
        for horizon, (start, end) in PERIODS.items():
            for year in range(start, end + 1):
                for scenario in (['historical'] if horizon == 'historical' else ['ssp245', 'ssp585']):
                    for model in MODELS:
                        for var in VARIABLES:
                            jobs.append((site, model, scenario, var, year, catalogs[(model, scenario, var)][year]))
    if args.limit:
        jobs = jobs[:args.limit]
    rows, failures = [], []
    began = time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(acquire, job, args.offline): job for job in jobs}
        for future in concurrent.futures.as_completed(futures):
            try:
                rows.append(future.result())
            except Exception as exc:
                failures.append({'job': futures[future][:-1], 'error': str(exc)})
                print('FAILED ' + str(exc), flush=True)
            completed = len(rows) + len(failures)
            if completed % 24 == 0 or completed == len(jobs):
                print(json.dumps({'downloaded_validated': len(rows), 'failed': len(failures), 'total': len(jobs), 'elapsed_seconds': round(time.monotonic() - began)}), flush=True)
                write_json(OUT / 'acquisition_progress.json', {'ready': False, 'downloaded_validated': len(rows), 'total': len(jobs), 'failures': failures})
    if failures:
        raise ValueError(f'{len(failures)} acquisition jobs failed; no ready dataset published')
    if not args.limit:
        build(args.sites, sorted(rows, key=lambda row: row['local_path']))


if __name__ == '__main__':
    main()
