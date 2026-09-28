from datetime import timedelta

import numpy as np
import pandas as pd
import pytest
from pydantic import ValidationError

from backend.planning import catalog, crop_water, planning_context, simulate
from backend.planning_contracts import SimulationRequest
from backend.repository import load_verified_climate
from backend.scenario_preview import scenario_preview
from backend.science import FAO56_HARGREAVES, temperature_scenario_et0, water_balance


@pytest.fixture(scope='module')
def climate():
    return load_verified_climate(recent=True)


@pytest.fixture(scope='module')
def knowledge():
    return catalog()


@pytest.fixture(scope='module')
def contexts():
    return {region: planning_context(region) for region in ['konya', 'seyhan_adana', 'gediz_manisa', 'gap_sanliurfa', 'trakya_edirne', 'longyearbyen']}


def request(contexts, region='konya'):
    return SimulationRequest.model_validate(contexts[region]['default_scenario'])


def test_zero_temperature_delta_preserves_source_et0_exactly_without_needing_temperature():
    original = np.array([0., .125, 2.234567890123, 7.5])
    adjusted, meta = temperature_scenario_et0(original, None, None, 0)
    np.testing.assert_array_equal(adjusted, original)
    assert adjusted is not original
    assert meta['applied'] is False
    assert meta['method'] == 'SOURCE_ET0_UNCHANGED'


def test_hargreaves_temperature_term_ratio_uses_daily_temperatures_not_a_fixed_percent():
    original = np.array([2., 4., 6.])
    before = original.copy()
    lo, hi = np.array([0., 10., 20.]), np.array([10., 20., 30.])
    warm, meta = temperature_scenario_et0(original, lo, hi, 3)
    cool, _ = temperature_scenario_et0(original, lo, hi, -3)
    expected = np.array([25.8 / 22.8, 35.8 / 32.8, 45.8 / 42.8])
    np.testing.assert_allclose(warm, original * expected, rtol=1e-14)
    assert np.all(cool < original)
    assert np.all(warm > original)
    assert meta['source_url'] == FAO56_HARGREAVES
    assert meta['source_equation'] == 52
    assert meta['locally_validated'] is False
    assert meta['ratio_is_project_scenario_derivation'] is True
    assert 'Penman' in ' '.join(meta['limitations'])
    np.testing.assert_array_equal(original, before)


def test_negative_shift_clamps_only_numerator_and_reports_days():
    adjusted, meta = temperature_scenario_et0([1.], [-17.], [-15.], -3)
    assert adjusted.tolist() == [0.]
    assert meta['clamped_numerator_days'] == 1


@pytest.mark.parametrize('lo,hi', [
    (None, None), ([np.nan], [5]), ([0], [np.inf]), ([10], [5]),
    ([-20], [-20]), ([-18.8], [-16.8]),
])
def test_missing_or_invalid_temperature_and_nonpositive_denominator_need_data(lo, hi):
    with pytest.raises(ValueError, match='DATA_NEEDED'):
        temperature_scenario_et0([2.], lo, hi, 1)


def test_zero_delta_keeps_original_crop_water_calculation(contexts, climate, knowledge):
    q = request(contexts)
    assert q.temperature_delta_c == 0
    c = q.crops[0]
    k = knowledge[c.crop_id]
    days = c.stage_days or k['growing_period']['stage_days']
    end = c.season_start + timedelta(days=sum(days) - 1)
    d = climate[(climate.site_id == q.region_id) & (climate.date >= pd.Timestamp(c.season_start)) & (climate.date <= pd.Timestamp(end))]
    kc = k['kc']
    curve = np.r_[np.full(days[0], kc['initial']), np.linspace(kc['initial'], kc['mid'], days[1]),
                  np.full(days[2], kc['mid']), np.linspace(kc['mid'], kc['end'], days[3])]
    legacy = water_balance(d.precipitation_mm.to_numpy() * q.rainfall_factor,
                           d.et0_mm.to_numpy() * q.et0_factor, curve, q.soil_capacity_mm, q.initial_storage_mm)
    actual = crop_water(q, c, k, climate)
    assert actual['net_irrigation_mm'] == legacy['totals']['deficit_mm']
    assert actual['etc_mm'] == legacy['totals']['potential_et_mm']
    assert actual['gross_water_m3_ha'] == legacy['totals']['deficit_mm'] * 10 / q.irrigation_efficiency


def test_temperature_and_rainfall_combine_in_the_same_water_balance(contexts, climate, knowledge):
    q = request(contexts)
    c = q.crops[0]
    base = crop_water(q, c, knowledge[c.crop_id], climate)
    warm = crop_water(q.model_copy(update={'temperature_delta_c': 3.}), c, knowledge[c.crop_id], climate)
    cool = crop_water(q.model_copy(update={'temperature_delta_c': -3.}), c, knowledge[c.crop_id], climate)
    dry_warm = crop_water(q.model_copy(update={'temperature_delta_c': 3., 'rainfall_factor': .7}), c, knowledge[c.crop_id], climate)
    assert cool['etc_mm'] < base['etc_mm'] < warm['etc_mm']
    assert cool['net_irrigation_mm'] < base['net_irrigation_mm'] < warm['net_irrigation_mm']
    assert dry_warm['etc_mm'] == warm['etc_mm']
    assert dry_warm['rainfall_mm'] == pytest.approx(base['rainfall_mm'] * .7)
    assert dry_warm['net_irrigation_mm'] > warm['net_irrigation_mm']
    extra_et0 = crop_water(q.model_copy(update={'temperature_delta_c': 3., 'et0_factor': 1.2}), c, knowledge[c.crop_id], climate)
    assert extra_et0['etc_mm'] == pytest.approx(warm['etc_mm'] * 1.2)
    assert extra_et0['temperature_scenario']['additional_manual_et0_factor'] == 1.2


def test_missing_temperature_becomes_unknown_crop_water_without_touching_zero_delta(contexts, climate, knowledge):
    q = request(contexts)
    c = q.crops[0]
    no_temperature = climate.drop(columns=['tmin_c', 'tmax_c'])
    base = crop_water(q, c, knowledge[c.crop_id], no_temperature)
    warm = crop_water(q.model_copy(update={'temperature_delta_c': 2.}), c, knowledge[c.crop_id], no_temperature)
    assert base['gross_water_m3_ha'] is not None
    assert warm['gross_water_m3_ha'] is None
    assert warm['status'] == 'insufficient_data'
    assert warm['source'] == 'DATA_NEEDED'
    assert warm['temperature_scenario']['applied'] is False


@pytest.mark.parametrize('region', ['konya', 'seyhan_adana', 'gediz_manisa', 'gap_sanliurfa', 'trakya_edirne'])
def test_live_preview_matches_optimizer_and_current_baseline_stays_unshifted(contexts, region):
    q = request(contexts, region)
    base = simulate(q)
    q.temperature_delta_c = 2.
    q.rainfall_factor = .85
    preview = scenario_preview(q)
    result = simulate(q)
    assert preview['crop_water'] == result['crop_water']
    assert result['baseline'] == base['baseline']
    assert result['current']['crops'][0]['water_m3'] > base['current']['crops'][0]['water_m3']
    assert result['current']['crops'][0]['production_kg'] == base['current']['crops'][0]['production_kg']
    assert result['request']['temperature_delta_c'] == 2
    assert result['provenance']['temperature_scenario']['temperature_delta_c'] == 2
    assert result['provenance']['temperature_scenario']['source_url'] == FAO56_HARGREAVES
    if region == 'trakya_edirne':
        rice = next(row for row in result['crop_water'] if row['crop_id'] == 'rice')
        assert rice['gross_water_m3_ha'] is None
        assert rice['temperature_scenario']['applied'] is False
        assert result['current']['totals']['water_m3'] is None
        assert result['optimized']['totals']['water_m3'] is None


def test_manual_net_irrigation_is_not_mislabeled_as_a_temperature_response(contexts, climate, knowledge):
    q = request(contexts)
    c = q.crops[0].model_copy(update={'manual_net_irrigation_mm': 333.})
    base = crop_water(q, c, knowledge[c.crop_id], climate)
    changed = crop_water(q.model_copy(update={'temperature_delta_c': 6., 'rainfall_factor': .1, 'et0_factor': 3.}), c, knowledge[c.crop_id], climate)
    assert changed['net_irrigation_mm'] == base['net_irrigation_mm'] == 333
    assert changed['gross_water_m3_ha'] == base['gross_water_m3_ha']
    assert changed['source'] == 'USER_SCENARIO'
    assert changed['temperature_scenario']['applied'] is False
    assert changed['temperature_scenario']['method'] == 'MANUAL_NET_IRRIGATION_NOT_CLIMATE_DERIVED'
    assert 'manuel' in changed['reason']


@pytest.mark.parametrize('invalid', [-3.01, 6.01, None, float('nan'), float('inf')])
def test_temperature_request_rejects_invalid_values(contexts, invalid):
    data = {**contexts['konya']['default_scenario'], 'temperature_delta_c': invalid}
    with pytest.raises(ValidationError):
        SimulationRequest.model_validate(data)


def test_temperature_request_accepts_bounds_and_rejects_north_nonzero(contexts):
    for delta in [-3, 0, 6]:
        assert SimulationRequest.model_validate({**contexts['konya']['default_scenario'], 'temperature_delta_c': delta}).temperature_delta_c == delta
    north = request(contexts, 'longyearbyen')
    assert north.temperature_delta_c == 0
    with pytest.raises(ValidationError, match='yalnız Türkiye'):
        SimulationRequest.model_validate({**north.model_dump(), 'temperature_delta_c': 1})
    with pytest.raises(ValueError, match='yalnız Türkiye'):
        simulate(north.model_copy(update={'temperature_delta_c': 1}))
