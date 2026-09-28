from datetime import datetime, timedelta, timezone
import json

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError
import pytest

from backend.north_validation import (
    PilotDesign, PilotObservation, SampleReview, assess_sample, compare_pilot,
    freeze_pilot, readiness, router, templates,
)
from backend.provenance import canonical, digest


def evidence():
    return dict(record_id='TEST_ONLY_REPORT', content_sha256='a' * 64,
                reviewer='Test reviewer', quality='accepted', classification='observed')


def sample(**changes):
    data = dict(sample_id='TEST_ONLY_SAMPLE', source_kind='seawater',
                source_connection='Test-only source connection',
                collected_at_utc='2026-01-01T00:00:00Z', latitude=78, longitude=15, depth_m=10,
                permit_record='Test permit', custody_record='Test custody', protocol_record='Test protocol',
                expert_reviewer='Test reviewer', intended_use='Test only selected treatment review',
                measurements=[dict(parameter='test_parameter', value=5, unit='test_unit', uncertainty=.1,
                                   method='Test method', instrument_id='Test instrument',
                                   calibration_record='Test calibration', evidence=evidence())],
                criteria=[dict(parameter='test_parameter', unit='test_unit', minimum=0, maximum=10,
                               decision_link='Test-only treatment decision', source='Test-only invented boundary; not scientific threshold')])
    data.update(changes)
    return data


def totals(**changes):
    return dict(new_water_m3=1, electricity_kwh=10, heat_kwh_th=20, harvested_fresh_mass_kg=2, **changes)


def design():
    return PilotDesign(crop_id='test_crop', production_method='hydroponics', water_origin='reconstructed',
                       source_water_record='Test water recipe record', treatment_record='Test treatment record',
                       protocol_record='Test protocol record', model_run_record='Test model expectation',
                       area_m2=2, duration_days=1, measurement_boundary='whole_pilot_including_water_treatment',
                       expected=totals())


def frozen_past(tmp_path):
    # Test fixture only: controlled old PRE timestamp; production never backdates PRE.
    result = freeze_pilot(design(), tmp_path)
    path = tmp_path / (result['freeze_id'] + '.json')
    record = json.loads(path.read_bytes())
    record['created_at_utc'] = '2026-01-01T00:00:00+00:00'
    raw = canonical(record).encode()
    path.write_bytes(raw)
    path.with_suffix('.sha256').write_text(digest(raw))
    return result['freeze_id']


def observation(freeze_id, **changes):
    value = dict(freeze_id=freeze_id, started_at_utc='2026-01-02T00:00:00Z', ended_at_utc='2026-01-03T00:00:00Z',
                 area_m2=2, measurement_boundary='whole_pilot_including_water_treatment',
                 protocol_record='Test protocol record', calibration_record='Test calibration record',
                 source_water_record='Test water recipe record', treatment_record='Test treatment record',
                 evidence=evidence(), measured=totals(), deviations='No test deviations')
    value.update(changes)
    return PilotObservation(**value)


def test_selected_checks_do_not_certify_water_or_update_engine():
    result = assess_sample(SampleReview(**sample()))
    assert result['status'] == 'selected_checks_met'
    assert result['updated_model_inputs'] == []
    assert 'belgesi değildir' in result['limits'][0]
    assert result['classification'] == 'SUBMITTED_SAMPLE_SCOPE_REVIEW'


@pytest.mark.parametrize('value,uncertainty,expected', [
    (11, .2, 'outside_selected_range'), (9.9, .2, 'uncertainty_crosses_limit'),
    (10, 0, 'within_selected_range'), (0, .2, 'uncertainty_crosses_limit'),
])
def test_uncertainty_interval_controls_sample_result(value, uncertainty, expected):
    data = sample()
    data['measurements'][0].update(value=value, uncertainty=uncertainty)
    assert assess_sample(SampleReview(**data))['checks'][0]['status'] == expected


def test_missing_measurement_is_not_zero_or_pass():
    result = assess_sample(SampleReview(**sample(measurements=[])))
    assert result['status'] == 'further_evidence_needed'
    assert result['checks'][0]['measurement'] is None
    assert result['checks'][0]['status'] == 'measurement_needed'


def test_units_not_silently_converted():
    data = sample()
    data['measurements'][0]['unit'] = 'dS/m'
    assert assess_sample(SampleReview(**data))['checks'][0]['status'] == 'unit_mismatch'


@pytest.mark.parametrize('change', ['simulation', 'no_calibration', 'future', 'naive', 'duplicate', 'reconstructed', 'nan'])
def test_invalid_sample_record_rejected(change):
    data = sample()
    if change == 'simulation': data['measurements'][0]['evidence']['classification'] = 'simulated'
    if change == 'no_calibration': data['measurements'][0]['calibration_record'] = ''
    if change == 'future': data['collected_at_utc'] = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    if change == 'naive': data['collected_at_utc'] = '2026-01-01T00:00:00'
    if change == 'duplicate': data['measurements'] *= 2
    if change == 'reconstructed': data['source_kind'] = 'reconstructed'
    if change == 'nan': data['measurements'][0]['value'] = float('nan')
    with pytest.raises(ValidationError): SampleReview(**data)


def test_criteria_have_real_declared_boundary_and_order():
    for bounds in ({'minimum': None, 'maximum': None}, {'minimum': 11, 'maximum': 10}):
        data = sample()
        data['criteria'][0].update(bounds)
        with pytest.raises(ValidationError): SampleReview(**data)


def test_pilot_difference_and_intensity_arithmetic(tmp_path):
    measured = dict(new_water_m3=.8, electricity_kwh=12, heat_kwh_th=15, harvested_fresh_mass_kg=4)
    result = compare_pilot(observation(frozen_past(tmp_path), measured=measured), tmp_path)
    rows = {row['metric']: row for row in result['comparisons']}
    assert rows['new_water_m3']['delta_percent'] == pytest.approx(-20)
    assert rows['electricity_kwh']['delta'] == 2
    assert rows['heat_kwh_th']['delta'] == -5
    assert result['per_kg_fresh_mass']['observed']['new_water_m3'] == .2
    assert result['water_origin'] == 'reconstructed'
    assert result['updated_model_inputs'] == []
    assert (tmp_path / (result['post_id'] + '.sha256')).exists()


def test_zero_harvest_is_not_infinite_efficiency(tmp_path):
    measured = dict(new_water_m3=1, electricity_kwh=10, heat_kwh_th=20, harvested_fresh_mass_kg=0)
    result = compare_pilot(observation(frozen_past(tmp_path), measured=measured), tmp_path)
    assert all(value is None for value in result['per_kg_fresh_mass']['observed'].values())


def test_zero_expected_metric_has_no_percent(tmp_path):
    freeze_id = frozen_past(tmp_path)
    path = tmp_path / (freeze_id + '.json')
    record = json.loads(path.read_bytes())
    record['design']['expected']['heat_kwh_th'] = 0
    raw = canonical(record).encode()
    path.write_bytes(raw)
    path.with_suffix('.sha256').write_text(digest(raw))
    result = compare_pilot(observation(freeze_id), tmp_path)
    assert next(row for row in result['comparisons'] if row['metric'] == 'heat_kwh_th')['delta_percent'] is None


@pytest.mark.parametrize('changes', [
    {'area_m2': 3}, {'ended_at_utc': '2026-01-04T00:00:00Z'},
    {'started_at_utc': '2025-12-31T00:00:00Z'},
    {'started_at_utc': '2026-01-02T00:00:00'},
    {'protocol_record': 'Different protocol record'},
    {'source_water_record': 'Different source record'},
    {'treatment_record': 'Different treatment record'},
    {'ended_at_utc': '2099-01-01T00:00:00Z'},
])
def test_pilot_invalid_time_or_scope_rejected(tmp_path, changes):
    with pytest.raises(ValueError):
        compare_pilot(observation(frozen_past(tmp_path), **changes), tmp_path)


def test_cannot_create_pre_after_actual_pilot(tmp_path):
    current = freeze_pilot(design(), tmp_path)
    with pytest.raises(ValueError, match='dondurmadan sonra'):
        compare_pilot(observation(current['freeze_id']), tmp_path)


def test_modified_frozen_data_rejected(tmp_path):
    freeze_id = frozen_past(tmp_path)
    path = tmp_path / (freeze_id + '.json')
    path.write_text('{}')
    with pytest.raises(ValueError, match='özeti uyuşmuyor'):
        compare_pilot(observation(freeze_id), tmp_path)


def test_simulated_pilot_evidence_rejected():
    simulated = evidence()
    simulated['classification'] = 'simulated'
    with pytest.raises(ValidationError): observation('a' * 32, evidence=simulated)


def test_readiness_and_templates_never_contain_fake_observations():
    assert readiness()['classification'] == 'RESEARCH_READINESS_PLAN_NOT_FIELD_RESULTS'
    exported = templates()
    assert exported['classification'] == 'BLANK_PROTOCOL_TEMPLATES_NOT_OBSERVATIONS'
    assert len(exported['csv_templates']) == 4
    assert all(len(text.strip().splitlines()) == 1 for text in exported['csv_templates'].values())
    assert len(readiness()['research_tasks']) == 6


def test_api_schemas_get_export_and_reject_invalid_post():
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)
    assert client.get('/api/north/validation/templates').status_code == 200
    assert client.get('/api/north/validation/readiness').status_code == 200
    assert client.post('/api/north/validation/sample-review', json=sample()).status_code == 200
    assert client.post('/api/north/validation/sample-review', json={}).status_code == 422
