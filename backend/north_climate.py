"""Verified multi-model northern climate contexts for the rebuild decision engine.

Public-data climate simulations remain separate from observations. All derived
series are hash-checked, each GCM retains its own daily chronology, and missing
members/periods cannot silently become a smaller ensemble.
"""
from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CLIMATE_DIR = ROOT / 'data/north/rebuild_climate'
PERIODS = {'historical': (1995, 2014), 'near': (2021, 2040), 'mid': (2041, 2060), 'late': (2081, 2100)}
MODELS = ('ACCESS-CM2', 'MPI-ESM1-2-HR', 'MRI-ESM2-0')
SCENARIOS = ('ssp245', 'ssp585')
RECENT_PERIOD = (2015, 2025)
RECENT_MODEL = 'ERA5'


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _resolve(relative):
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(CLIMATE_DIR.resolve()):
        raise ValueError('Climate artifact path outside data directory')
    return path


@lru_cache(maxsize=4)
def _read_package(manifest_stamp, context_stamp):
    del manifest_stamp, context_stamp
    raw = (CLIMATE_DIR / 'manifest.json').read_bytes()
    manifest = json.loads(raw)
    if manifest.get('status') != 'ready':
        raise ValueError('Multi-model climate package is incomplete')
    context_path = CLIMATE_DIR / 'climate_contexts.json'
    context_raw = context_path.read_bytes()
    entry = next((r for r in manifest['derived_files'] if _resolve(r['path']) == context_path.resolve()), None)
    if entry is None or _sha(context_raw) != entry['sha256']:
        raise ValueError('Multi-model climate context hash mismatch')
    package = json.loads(context_raw)
    if package.get('status') != 'ready' or package.get('dataset_version') != '2.0' or tuple(package.get('model_ids', [])) != MODELS:
        raise ValueError('Wrong climate package version or model subset')
    expected = {(site, horizon, scenario) for site in package['sites'] for horizon in PERIODS
                for scenario in (['historical'] if horizon == 'historical' else SCENARIOS)}
    actual = [(r['site_id'], r['horizon_id'], r['scenario_id']) for r in package['contexts']]
    if len(set(actual)) != len(actual) or set(actual) != expected:
        raise ValueError('Missing or duplicate climate contexts')
    for row in package['contexts']:
        if tuple(row['period']) != PERIODS[row['horizon_id']] or row['years'] != 20:
            raise ValueError('Climate window is not the contracted 20-year period')
        if tuple(member['model'] for member in row['models']) != MODELS:
            raise ValueError('A climate context is missing a model')
        for member in row['models']:
            start, end = PERIODS[row['horizon_id']]
            if member['years'] != 20 or [r['year'] for r in member['annual']] != list(range(start, end + 1)):
                raise ValueError('Incomplete annual climate series')
    return package, _sha(raw), manifest


def _package():
    paths = [CLIMATE_DIR / name for name in ('manifest.json', 'climate_contexts.json')]
    if not all(path.exists() for path in paths):
        raise ValueError('Multi-model climate acquisition is not yet complete')
    stamps = [(p.stat().st_mtime_ns, p.stat().st_size) for p in paths]
    return _read_package(*stamps)


@lru_cache(maxsize=2)
def _reference_check(raw_stamp, metadata_stamp):
    del raw_stamp, metadata_stamp
    folder = CLIMATE_DIR / 'historical_check'
    raw = (folder / 'era5_land_1995_2014.json').read_bytes()
    metadata = json.loads((folder / 'metadata.json').read_text(encoding='utf-8'))
    if _sha(raw) != metadata['sha256'] or metadata['requested_model'] != 'era5_land':
        raise ValueError('Local historical reference hash/model mismatch')
    payload = json.loads(raw)
    daily = payload['daily']
    dates = pd.DatetimeIndex(daily['time'])
    if not dates.equals(pd.date_range('1995-01-01', '2014-12-31')) or payload.get('utc_offset_seconds') != 0:
        raise ValueError('Incomplete local historical temperature reference')
    if any(payload['daily_units'].get(key) != '°C' for key in ('temperature_2m_min', 'temperature_2m_max')):
        raise ValueError('Wrong local historical temperature units')
    low = np.asarray(daily['temperature_2m_min'], dtype=float)
    high = np.asarray(daily['temperature_2m_max'], dtype=float)
    if not np.isfinite(low).all() or not np.isfinite(high).all() or np.any(low > high):
        raise ValueError('Invalid local reference temperature values')
    mean = (low + high) / 2
    return {'classification': 'REANALYSIS_COMPARISON_ONLY', 'period': [1995, 2014], 'model': 'ERA5-Land via Open-Meteo',
            'mean_temperature_c': float(mean.mean()), 'july_temperature_c': float(mean[dates.month == 7].mean()),
            'source_grid': {key: payload[key] for key in ('latitude', 'longitude', 'elevation')},
            'source_url': metadata['url'], 'source_sha256': metadata['sha256'],
            'elevation_processing': metadata['elevation_processing'], 'projection_adjustment_applied': False,
            'interpretation': 'Different grids and reference processing; this comparison is not station validation or measured forecast error.'}


def list_climate_contexts():
    """Compact catalog; `historical` must not be labelled today's observation."""
    package, manifest_hash, _ = _package()
    return {'sites': deepcopy(package['sites']), 'horizons': {**deepcopy(package['periods']), 'recent': list(RECENT_PERIOD)}, 'scenarios': list(SCENARIOS),
            'models': list(MODELS), 'dataset': package['dataset'], 'dataset_version': package['dataset_version'],
            'recent_reference': {'period': list(RECENT_PERIOD), 'dataset': 'ERA5 via Open-Meteo', 'model': RECENT_MODEL,
                                 'classification': 'SOURCED_REANALYSIS_NOT_FIELD_OBSERVATION'},
            'annual_years': {'min': max(2026, datetime.now(timezone.utc).year), 'max': 2100,
                             'current_year': datetime.now(timezone.utc).year,
                             'ready': (CLIMATE_DIR / 'annual/manifest.json').exists()},
            'manifest_sha256': manifest_hash, 'limitations': deepcopy(package['limitations'])}


@lru_cache(maxsize=2)
def _annual_package(manifest_stamp, context_stamp):
    del manifest_stamp, context_stamp
    raw = (CLIMATE_DIR / 'annual/manifest.json').read_bytes()
    manifest = json.loads(raw)
    path = CLIMATE_DIR / 'annual/contexts.json'
    context_raw = path.read_bytes()
    declared = next((r for r in manifest['derived_files'] if _resolve(r['path']) == path.resolve()), None)
    if (manifest.get('status') != 'ready' or manifest.get('schema_version') != '1.0'
            or manifest.get('raw_file_count') != 1800 or len(manifest['derived_files']) != 451
            or declared is None or _sha(context_raw) != declared['sha256']):
        raise ValueError('Annual climate package incomplete or context hash mismatch')
    package = json.loads(context_raw)
    if package.get('status') != 'ready' or package.get('start_year') != 2026 or package.get('end_year') != 2100 or tuple(package['model_ids']) != MODELS:
        raise ValueError('Annual climate coverage/model identity mismatch')
    expected = {(year, scenario) for year in range(2026,2101) for scenario in SCENARIOS}
    actual = [(c['target_year'], c['scenario_id']) for c in package['contexts']]
    if len(set(actual)) != len(actual) or set(actual) != expected:
        raise ValueError('Annual climate has missing or duplicate years')
    for context in package['contexts']:
        year = context['target_year']
        if (context['site_id'] != 'longyearbyen' or context['horizon_id'] != 'year'
                or context['period'] != [year,year] or context['years'] != 1 or tuple(m['model'] for m in context['models']) != MODELS):
            raise ValueError('Annual climate context does not contain one exact year and three models')
        for member in context['models']:
            if member['years'] != 1 or [a['year'] for a in member['annual']] != [year]:
                raise ValueError('Annual climate member has wrong year')
            item = next((r for r in manifest['derived_files'] if r['path']==member['daily_path']),None)
            if item is None or item['sha256'] != member['daily_sha256']:
                raise ValueError('Annual daily artifact missing from manifest or hash differs')
    return package, _sha(raw)


def _annual_context(site_id, scenario_id, target_year):
    if site_id != 'longyearbyen' or scenario_id not in SCENARIOS:
        raise ValueError('Unknown annual climate location/scenario')
    if isinstance(target_year,bool) or not isinstance(target_year,int) or not max(2026,datetime.now(timezone.utc).year) <= target_year <= 2100:
        raise ValueError('Planning year must be an integer from the current year through 2100')
    paths = [CLIMATE_DIR / 'annual' / n for n in ('manifest.json','contexts.json')]
    package, manifest_hash = _annual_package(*[(p.stat().st_mtime_ns,p.stat().st_size) for p in paths])
    # Same-source historical reference, not the ERA5 recent reference.
    base = get_climate_context(site_id,'historical',scenario_id)
    result = deepcopy(next(c for c in package['contexts'] if c['target_year'] == target_year and c['scenario_id'] == scenario_id))
    for member in result['models']:
        path = _resolve(member['daily_path'])
        frame = _read_frame(member['daily_path'],member['daily_sha256'],(path.stat().st_mtime_ns,path.stat().st_size))
        if not pd.DatetimeIndex(frame.date).equals(pd.date_range(f'{target_year}-01-01',f'{target_year}-12-31')):
            raise ValueError('Annual daily series does not match requested year')
    for key in ('dataset','dataset_version','site','temperature_mean_method','sources','local_reference_check'):
        if key in base: result[key] = deepcopy(base[key])
    result.update(manifest_sha256=manifest_hash, classification='SOURCED_CLIMATE_MODEL_YEAR_NOT_WEATHER_FORECAST',
        ensemble_method='Unweighted mean and min/max across three exact model-year trajectories; not a probability interval.',
        temporal_method='Exact daily source-model year, recomputed independently per model. No interpolation or proportional scaling.',
        limitations=[*base['limitations'], 'A selected model year is one realization per model, not a prediction of actual weather in that calendar year. Interannual variability is preserved; consecutive-year changes need not be monotonic.',
                     'Single-year screening is not a long-term infrastructure design standard or an expert-approved yield forecast. Multi-year stress tests and local validation remain necessary.',
                     'Annual water screening starts with zero snowpack and an empty tank. Snow carried over from the previous year is not represented; this is an explicit initialization assumption, not measured source availability.'])
    result['change_from_historical'] = {k: result['ensemble'][k]['mean']-base['ensemble'][k]['mean'] for k in result['ensemble']}
    return result


def _recent_context(site_id):
    if site_id != 'longyearbyen':
        raise ValueError('Unknown recent climate location')
    folder = CLIMATE_DIR / 'recent_reference'
    manifest_raw = (folder / 'manifest.json').read_bytes()
    manifest = json.loads(manifest_raw)
    if manifest.get('status') != 'ready' or tuple(manifest.get('period', [])) != RECENT_PERIOD:
        raise ValueError('Incomplete recent climate reference')
    context_path = folder / 'context.json'
    declared = manifest.get('raw_files', []) + manifest.get('derived_files', [])
    if not any(_resolve(row['path']) == context_path.resolve() for row in declared):
        raise ValueError('Recent reference context missing from manifest')
    for record in declared:
        if _sha(_resolve(record['path']).read_bytes()) != record['sha256']:
            raise ValueError('Recent reference artifact hash mismatch')
    if _sha((CLIMATE_DIR / 'climate_contexts.json').read_bytes()) != manifest['nasa_context_sha256']:
        raise ValueError('Recent reference cross-dataset check is stale')
    context = json.loads(context_path.read_bytes())
    if (context.get('classification') != 'SOURCED_REANALYSIS_NOT_FIELD_OBSERVATION'
            or tuple(context.get('period', [])) != RECENT_PERIOD or context.get('years') != 11
            or [m['model'] for m in context['models']] != [RECENT_MODEL]
            or [r['year'] for r in context['models'][0]['annual']] != list(range(2015, 2026))):
        raise ValueError('Invalid recent reference context')
    context['manifest_sha256'] = _sha(manifest_raw)
    return context


def get_climate_context(site_id='longyearbyen', horizon_id='mid', scenario_id='ssp245', target_year=None):
    """Return per-model annual/monthly metrics and three-model mean/min/max.

Historical returns scenario_id='historical' for either recognized SSP selection,
because 1995–2014 is the common historical experiment, not an SSP future.
"""
    if target_year is not None:
        return _annual_context(site_id,scenario_id,target_year)
    if horizon_id == 'recent':
        if scenario_id not in (*SCENARIOS, 'recent'):
            raise ValueError('Unknown recent climate scenario')
        return _recent_context(site_id)
    if horizon_id not in PERIODS or scenario_id not in (*SCENARIOS, 'historical'):
        raise ValueError('Unknown climate horizon/scenario')
    if horizon_id != 'historical' and scenario_id == 'historical':
        raise ValueError('Future horizon requires an SSP')
    package, manifest_hash, _ = _package()
    scenario = 'historical' if horizon_id == 'historical' else scenario_id
    result = next((r for r in package['contexts'] if (r['site_id'], r['horizon_id'], r['scenario_id']) ==
                   (site_id, horizon_id, scenario)), None)
    if result is None:
        raise ValueError('Unknown climate location')
    context = deepcopy(result)
    context.update(dataset=package['dataset'], dataset_version=package['dataset_version'],
                   site=deepcopy(package['sites'][site_id]), classification=package['classification'],
                   ensemble_method=package['ensemble_method'], limitations=deepcopy(package['limitations']),
                   temperature_mean_method=package.get('temperature_mean_method', '(Tmin+Tmax)/2'),
                   sources=deepcopy(package['sources']), manifest_sha256=manifest_hash)
    historical = next(r for r in package['contexts'] if r['site_id'] == site_id and r['horizon_id'] == 'historical')
    context['change_from_historical'] = {key: context['ensemble'][key]['mean'] - historical['ensemble'][key]['mean']
                                         for key in context['ensemble']}
    reference_files = [CLIMATE_DIR / 'historical_check' / name for name in ('era5_land_1995_2014.json', 'metadata.json')]
    if site_id == 'longyearbyen' and all(path.exists() for path in reference_files):
        reference = deepcopy(_reference_check(*[(p.stat().st_mtime_ns, p.stat().st_size) for p in reference_files]))
        reference['nasa_minus_reanalysis_temperature_c'] = historical['ensemble']['mean_temperature_c']['mean'] - reference['mean_temperature_c']
        context['local_reference_check'] = reference
    return context


@lru_cache(maxsize=72)
def _read_frame(relative, expected_sha, stamp):
    del stamp
    path = _resolve(relative)
    if _sha(path.read_bytes()) != expected_sha:
        raise ValueError('Daily climate artifact hash mismatch')
    frame = pd.read_csv(path, parse_dates=['date'])
    columns = ['tmin_c', 'tmax_c', 'precipitation_mm', 'shortwave_mj_m2']
    if not np.isfinite(frame[columns].to_numpy()).all() or (frame.tmin_c > frame.tmax_c).any() or (frame[['precipitation_mm', 'shortwave_mj_m2']] < 0).any().any():
        raise ValueError('Daily climate contains invalid physical values')
    if not pd.DatetimeIndex(frame.date).equals(pd.date_range(frame.date.min(), frame.date.max())):
        raise ValueError('Daily climate chronology is incomplete or duplicated')
    return frame


def load_climate_frame(site_id='longyearbyen', horizon_id='mid', scenario_id='ssp245', model_id=None, target_year=None):
    """Daily C / mm day-1 / MJ m-2 day-1, with model and scenario columns.

When model_id is omitted, returns all three trajectories stacked with a model
column. Never averages weather chronologies before nonlinear crop/frost tests.
"""
    context = get_climate_context(site_id, horizon_id, scenario_id, target_year)
    if model_id is not None and model_id not in [member['model'] for member in context['models']]:
        raise ValueError('Unknown climate model for selected dataset')
    frames = []
    for member in context['models']:
        if model_id is not None and member['model'] != model_id:
            continue
        path = _resolve(member['daily_path'])
        stamp = (path.stat().st_mtime_ns, path.stat().st_size)
        frame = _read_frame(member['daily_path'], member['daily_sha256'], stamp).copy(deep=True)
        expected = pd.date_range(f'{context["period"][0]}-01-01', f'{context["period"][1]}-12-31')
        if not pd.DatetimeIndex(frame.date).equals(expected):
            raise ValueError('Daily data do not match selected climate window')
        frame['model'] = member['model']
        frame['scenario'] = context['scenario_id']
        frame['site_id'] = site_id
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)
