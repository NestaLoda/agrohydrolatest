"""Climate acquisition/derivation invariants, plus the real cached ensemble.

Run after `scripts/ingest_north_rebuild_climate.py` completes. These tests do not
contact a network or substitute fixtures for a missing production data package.
"""
from pathlib import Path
import hashlib
import json

import numpy as np
import pandas as pd
import pytest

from backend import north_climate as climate
from scripts.ingest_north_rebuild_climate import annual_metrics, period_metrics, longest_run


def constant_years(start=2000, end=2019):
    dates = pd.date_range(f'{start}-01-01', f'{end}-12-31')
    return pd.DataFrame({'date': dates, 'tmin_c': np.full(len(dates), 2.), 'tmax_c': np.full(len(dates), 18.),
                         'precipitation_mm': np.full(len(dates), 2.), 'shortwave_mj_m2': np.full(len(dates), 10.)})


def test_calendar_degree_days_and_monthly_accumulations_are_not_20_year_totals():
    frame = constant_years()
    result = period_metrics(frame)
    assert result['years'] == 20
    assert result['daily_rows'] == 7305
    assert result['annual'][0]['days'] == 366
    assert result['annual'][0]['gdd5_degree_days'] == 366 * 5
    assert result['annual'][1]['gdd5_degree_days'] == 365 * 5
    assert result['summary']['frost_free_run_days'] == 365.25
    assert result['monthly'][0]['precipitation_mm'] == 31 * 2
    assert result['monthly'][1]['precipitation_mm'] == 28.25 * 2
    assert result['monthly'][0]['heating_degree_days_18c'] == 31 * 8
    assert sum(row['precipitation_mm'] for row in result['monthly']) == result['summary']['precipitation_mm']


def test_frost_free_run_resets_on_frost_and_at_year_boundary():
    assert longest_run([True, True, False, True, True, True, False]) == 3
    frame = constant_years(2000, 2001)
    frame['tmin_c'] = -1.
    frame.loc[frame.date.between('2000-12-29', '2001-01-04'), 'tmin_c'] = 1.
    rows = annual_metrics(frame)
    assert rows[0]['frost_free_run_days'] == 3
    assert rows[1]['frost_free_run_days'] == 4


def test_partial_or_duplicate_year_is_rejected_instead_of_called_climatology():
    frame = constant_years(2000, 2000)
    with pytest.raises(ValueError, match='complete ordered'):
        annual_metrics(frame.iloc[:-1])
    with pytest.raises(ValueError, match='complete ordered'):
        annual_metrics(pd.concat([frame, frame.iloc[:1]], ignore_index=True))


def test_non_linear_climate_indicators_must_precede_ensemble_average():
    cold = constant_years(2001, 2001)
    warm = cold.copy()
    cold[['tmin_c', 'tmax_c']] = 0.
    warm[['tmin_c', 'tmax_c']] = 10.
    calculated_then_averaged = (annual_metrics(cold)[0]['gdd5_degree_days'] + annual_metrics(warm)[0]['gdd5_degree_days']) / 2
    mean_weather = cold.copy()
    mean_weather[['tmin_c', 'tmax_c']] = 5.
    assert calculated_then_averaged == 912.5
    assert annual_metrics(mean_weather)[0]['gdd5_degree_days'] == 0


@pytest.mark.parametrize('horizon,scenario', [('bad', 'ssp245'), ('mid', 'historical'), ('mid', 'ssp999')])
def test_invalid_climate_selection_does_not_fall_back_silently(horizon, scenario):
    with pytest.raises(ValueError):
        climate.get_climate_context(horizon_id=horizon, scenario_id=scenario)


def test_real_package_has_full_windows_models_and_file_hashes():
    manifest = json.loads((climate.CLIMATE_DIR / 'manifest.json').read_text(encoding='utf-8'))
    assert manifest['status'] == 'ready'
    assert manifest['raw_file_count'] == 1680 * len(climate.list_climate_contexts()['sites'])
    for record in manifest['raw_files'] + manifest['derived_files']:
        raw = (climate.ROOT / record.get('local_path', record.get('path'))).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == record['sha256']
    contexts = json.loads((climate.CLIMATE_DIR / 'climate_contexts.json').read_text(encoding='utf-8'))['contexts']
    assert len(contexts) == 7 * len(climate.list_climate_contexts()['sites'])
    for context in contexts:
        assert context['years'] == 20
        assert tuple(row['model'] for row in context['models']) == climate.MODELS
        for key, band in context['ensemble'].items():
            expected = [member['summary'][key] for member in context['models']]
            assert band['mean'] == pytest.approx(np.mean(expected))
            assert band['min'] <= band['mean'] <= band['max']


@pytest.mark.parametrize('horizon,scenario', [('historical', 'ssp245'), ('near', 'ssp245'), ('mid', 'ssp245'),
                                             ('late', 'ssp245'), ('near', 'ssp585'), ('mid', 'ssp585'), ('late', 'ssp585')])
def test_real_daily_data_are_complete_finite_and_reproduce_indicators(horizon, scenario):
    context = climate.get_climate_context('longyearbyen', horizon, scenario)
    frame = climate.load_climate_frame('longyearbyen', horizon, scenario)
    assert frame.model.nunique() == 3
    for member in context['models']:
        data = frame.loc[frame.model == member['model']]
        expected_days = len(pd.date_range(f'{context["period"][0]}-01-01', f'{context["period"][1]}-12-31'))
        assert len(data) == member['daily_rows'] == expected_days
        if horizon == 'late':
            assert expected_days == 7304  # 2100 is not a Gregorian leap year.
        assert (data.tmin_c <= data.tmax_c).all()
        assert (data[['precipitation_mm', 'shortwave_mj_m2']] >= 0).all().all()
        recomputed = annual_metrics(data)
        for old, new in zip(member['annual'], recomputed):
            for key in new:
                assert new[key] == pytest.approx(old[key], abs=1e-4)


def test_horizon_changes_real_data_not_only_labels_and_historical_is_common():
    historical = climate.get_climate_context(horizon_id='historical', scenario_id='ssp585')
    assert historical['scenario_id'] == 'historical'
    assert historical['change_from_historical']['mean_temperature_c'] == 0
    near = climate.get_climate_context(horizon_id='near', scenario_id='ssp245')
    late = climate.get_climate_context(horizon_id='late', scenario_id='ssp585')
    assert near['models'][0]['daily_sha256'] != late['models'][0]['daily_sha256']
    assert near['ensemble']['mean_temperature_c']['mean'] != late['ensemble']['mean_temperature_c']['mean']
    assert 'not a probability interval' in near['ensemble_method']


def test_local_historical_reference_exposes_grid_disagreement_without_adjusting_projection():
    context = climate.get_climate_context()
    reference = context['local_reference_check']
    assert reference['period'] == [1995, 2014]
    assert reference['classification'] == 'REANALYSIS_COMPARISON_ONLY'
    assert reference['projection_adjustment_applied'] is False
    assert reference['mean_temperature_c'] == pytest.approx(-5.764154688569473)
    historical = climate.get_climate_context(horizon_id='historical')
    assert reference['nasa_minus_reanalysis_temperature_c'] == pytest.approx(
        historical['ensemble']['mean_temperature_c']['mean'] - reference['mean_temperature_c'])
    frame = climate.load_climate_frame(model_id=climate.MODELS[0])
    original = pd.read_csv(climate.ROOT / context['models'][0]['daily_path'])
    np.testing.assert_array_equal(frame.tmin_c.to_numpy(), original.tmin_c.to_numpy())


@pytest.mark.parametrize('scenario', ['ssp245', 'ssp585'])
def test_shared_2035_year_reproduces_the_preserved_earlier_nasa_subset(scenario):
    original = pd.read_csv(climate.ROOT / 'data/north/u9_acquisition/daily_point_2035.csv', parse_dates=['date'])
    original['date'] = original.date.dt.normalize()  # The old CSV retained the source's daily noon timestamp.
    original = original.loc[original.scenario == scenario].sort_values('date')
    current = climate.load_climate_frame('longyearbyen', 'near', scenario, 'ACCESS-CM2')
    current = current.loc[current.date.dt.year == 2035].sort_values('date')
    assert len(current) == len(original) == 365
    assert current.date.to_list() == original.date.to_list()
    np.testing.assert_allclose(current[['tmin_c', 'tmax_c', 'precipitation_mm']].to_numpy(),
                               original[['tmin_c', 'tmax_c', 'precipitation_mm']].to_numpy(), atol=3e-5, rtol=1e-6)


def test_callers_cannot_mutate_cached_climate_context_or_daily_values():
    context = climate.get_climate_context()
    original = context['models'][0]['summary']['gdd5_degree_days']
    context['models'][0]['summary']['gdd5_degree_days'] = -1
    assert climate.get_climate_context()['models'][0]['summary']['gdd5_degree_days'] == original
    frame = climate.load_climate_frame(model_id=climate.MODELS[0])
    initial = frame.loc[0, 'tmin_c']
    frame.loc[0, 'tmin_c'] = 9999
    assert climate.load_climate_frame(model_id=climate.MODELS[0]).loc[0, 'tmin_c'] == initial


def test_corrupted_daily_artifact_is_rejected(tmp_path, monkeypatch):
    path = tmp_path / 'data/north/rebuild_climate/daily/corrupt.csv.gz'
    path.parent.mkdir(parents=True)
    path.write_bytes(b'altered climate data')
    monkeypatch.setattr(climate, 'ROOT', tmp_path)
    monkeypatch.setattr(climate, 'CLIMATE_DIR', path.parent.parent)
    climate._read_frame.cache_clear()
    with pytest.raises(ValueError, match='hash mismatch'):
        climate._read_frame('data/north/rebuild_climate/daily/corrupt.csv.gz', 'not-the-sha', (0, 0))
