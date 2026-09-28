"""Real recent weather provenance and chronology, never a disguised GCM clone."""
from copy import deepcopy
import json
import hashlib
import shutil

import numpy as np
import pandas as pd
import pytest

from backend import north_climate as climate
from scripts.ingest_north_recent_reference import parse_payload
from scripts.ingest_north_rebuild_climate import period_metrics


FOLDER = climate.CLIMATE_DIR / 'recent_reference'


def test_complete_recent_reanalysis_contains_all_inputs_and_explicit_provenance():
    context = climate.get_climate_context(horizon_id='recent', scenario_id='ssp585')
    assert context['period'] == [2015, 2025]
    assert context['scenario_id'] == 'recent'
    assert context['classification'] == 'SOURCED_REANALYSIS_NOT_FIELD_OBSERVATION'
    assert context['years'] == 11
    assert [m['model'] for m in context['models']] == ['ERA5']
    frame = climate.load_climate_frame(horizon_id='recent', model_id='ERA5')
    assert len(frame) == 4018
    assert pd.DatetimeIndex(frame.date).equals(pd.date_range('2015-01-01', '2025-12-31'))
    assert set(frame.model) == {'ERA5'}
    assert np.isfinite(frame[['tmin_c', 'tmax_c', 'precipitation_mm', 'shortwave_mj_m2']]).all().all()
    recomputed = period_metrics(frame)
    for key, value in recomputed['summary'].items():
        assert context['ensemble'][key]['mean'] == pytest.approx(value)
    metadata = json.loads((FOLDER / 'metadata.json').read_text(encoding='utf-8'))
    assert metadata['requested_model'] == 'era5'
    assert 'models=era5&' in metadata['url']
    assert 'elevation=nan' in metadata['url']
    assert 'zero uncertainty' in ' '.join(context['limitations'])


def test_raw_and_all_derived_artifacts_are_immutable_hash_verified():
    manifest = json.loads((FOLDER / 'manifest.json').read_text(encoding='utf-8'))
    assert manifest['raw_days'] == 11323
    assert manifest['recent_days'] == 4018
    for entry in manifest['raw_files'] + manifest['derived_files']:
        assert hashlib.sha256((climate.ROOT / entry['path']).read_bytes()).hexdigest() == entry['sha256']


def test_historical_provider_difference_is_exposed_without_bias_adjustment():
    context = climate.get_climate_context(horizon_id='recent')
    diagnostic = context['cross_dataset_check']
    assert diagnostic['projection_adjustment_applied'] is False
    assert diagnostic['period'] == [1995, 2014]
    historic = climate.get_climate_context(horizon_id='historical')
    for key, value in diagnostic['era5_summary'].items():
        assert diagnostic['nasa_minus_era5'][key] == pytest.approx(historic['ensemble'][key]['mean'] - value)
        assert diagnostic['recent_minus_era5_historical'][key] == pytest.approx(context['ensemble'][key]['mean'] - value)
    assert 'cannot be attributed solely' in ' '.join(context['limitations'])
    assert climate.get_climate_context(horizon_id='recent', scenario_id='ssp245') == context
    with pytest.raises(ValueError, match='selected dataset'):
        climate.load_climate_frame(horizon_id='recent', model_id=climate.MODELS[0])
    with pytest.raises(ValueError, match='selected dataset'):
        climate.load_climate_frame(horizon_id='mid', model_id='ERA5')


@pytest.mark.parametrize('defect', ['null_radiation', 'wrong_unit', 'duplicate_day', 'missing_day', 'negative_rain', 'inverted_temperature'])
def test_missing_or_invalid_forcing_is_rejected_not_filled(defect):
    payload = json.loads((FOLDER / 'era5_1995_2025.json').read_text(encoding='utf-8'))
    if defect == 'null_radiation': payload['daily']['shortwave_radiation_sum'][100] = None
    if defect == 'wrong_unit': payload['daily_units']['shortwave_radiation_sum'] = 'W/m²'
    if defect == 'duplicate_day': payload['daily']['time'][1] = payload['daily']['time'][0]
    if defect == 'missing_day': payload['daily']['time'].pop()
    if defect == 'negative_rain': payload['daily']['precipitation_sum'][100] = -1
    if defect == 'inverted_temperature': payload['daily']['temperature_2m_min'][100] = 100
    with pytest.raises(ValueError): parse_payload(payload)


def test_mutating_a_recent_context_does_not_affect_future_callers():
    context = climate.get_climate_context(horizon_id='recent')
    original = deepcopy(context)
    context['models'][0]['annual'][0]['mean_temperature_c'] = 999
    assert climate.get_climate_context(horizon_id='recent') == original


def test_tampered_recent_artifact_fails_closed(tmp_path, monkeypatch):
    root = tmp_path / 'data/north/rebuild_climate'
    shutil.copytree(FOLDER, root / 'recent_reference')
    monkeypatch.setattr(climate, 'ROOT', tmp_path)
    monkeypatch.setattr(climate, 'CLIMATE_DIR', root)
    (root / 'recent_reference/era5_1995_2025.json').write_text('{}')
    with pytest.raises(ValueError, match='hash mismatch'):
        climate.get_climate_context(horizon_id='recent')
