import hashlib
from pathlib import Path

import pytest
from pydantic import ValidationError

from backend.north_contracts import NorthRequest
from backend.north_optimizer import solve_pattern
from backend.north_production_purpose import composition, nutritional_outputs, purpose_coefficients


def option(crop, yield_=1., water=1., heat=1.):
    return {'crop_id': crop, 'method': 'hydroponics', 'season': 'annual',
            'yield_kg_m2': yield_, 'water_monthly_m3_m2': [water/12]*12,
            'heat_kwh_th_m2': heat, 'electricity_kwh_m2': 1.}


def test_official_raw_source_checksums_and_six_explicit_food_mappings():
    data = composition()
    root = Path(__file__).resolve().parents[1]
    assert {r['crop_id'] for r in data['crops']} == {'lettuce','arugula','radish','kohlrabi','swiss_chard','basil'}
    for source in data['raw_files']:
        assert hashlib.sha256((root/source['path']).read_bytes()).hexdigest() == source['sha256']
        assert source['url'].startswith('https://www.matvaretabellen.no/api/en/')


def test_per_100g_to_per_kg_conversion_does_not_apply_edible_fraction_twice():
    # Published coefficient is 1.7 g/100g edible kohlrabi; yield is already edible kg.
    factors, meta = purpose_coefficients([option('kohlrabi')], 'protein')
    assert factors == [17.]
    assert meta['unit'] == 'g protein'
    outputs = nutritional_outputs([{'crop_id':'kohlrabi','production_kg':100.}])
    assert outputs['protein_kg'] == pytest.approx(1.7)
    assert outputs['food_energy_kcal'] == pytest.approx(23000)
    assert outputs['complete_composition_coverage'] is True


def test_purpose_changes_real_choice_not_only_label_or_display():
    # Kohlrabi yields 25% more fresh kg, rocket has more protein per edible kg.
    options = [option('kohlrabi',yield_=1.25), option('arugula')]
    fresh = solve_pattern(options)
    protein = solve_pattern(options, production_purpose='protein')
    assert fresh['crop_areas_m2']['kohlrabi'] > fresh['crop_areas_m2']['arugula']
    assert protein['crop_areas_m2']['arugula'] > protein['crop_areas_m2']['kohlrabi']
    assert protein['totals']['protein_kg'] > fresh['totals']['protein_kg']
    policy = protein['objective_policy']
    assert policy['balanced_mass_floor_kg'] is None
    assert policy['balanced_selected_output'] >= .95*policy['maximum_selected_output']-1e-5
    assert protein['totals']['selected_production_output'] == pytest.approx(protein['totals']['protein_kg']*1000)


def test_food_energy_is_not_facility_energy_and_units_close():
    result = solve_pattern([option('lettuce'),option('basil')],production_purpose='food_energy')
    assert result['crop_areas_m2']['basil'] > result['crop_areas_m2']['lettuce']
    assert result['totals']['selected_production_output'] == pytest.approx(result['totals']['food_energy_kcal'])
    assert result['production_purpose']['unit'] == 'kcal food'
    assert result['totals']['equivalent_electricity_kwh'] != result['totals']['food_energy_kcal']


@pytest.mark.parametrize('objective', ['balanced','water','energy'])
def test_resource_constraints_and_per_crop_retention_survive_new_purpose(objective):
    result = solve_pattern([option('arugula'),option('basil',water=2)],
                           production_purpose='protein',objective=objective,
                           energy_limit_kwh=400, production_retention=.8)
    assert result['solver']['max_equality_residual'] < 1e-6
    assert result['totals']['equivalent_electricity_kwh'] <= 400.0001
    assert all(area >= 5-1e-5 for area in result['crop_areas_m2'].values())
    if objective != 'balanced':
        for crop, before in result['balanced_crop_outputs_kg'].items():
            assert result['crop_outputs_kg'][crop] >= .8*before-1e-5


def test_missing_composition_never_becomes_zero_and_unknown_goal_rejected():
    with pytest.raises(ValueError,match='Sourced edible composition'):
        solve_pattern([option('unknown')],production_purpose='protein')
    generic = solve_pattern([option('unknown')])
    assert generic['totals']['complete_composition_coverage'] is False
    assert generic['totals']['composition_covered_production_kg'] == 0
    with pytest.raises(ValidationError):
        NorthRequest(production_purpose='profit')
    with pytest.raises(ValueError,match='Unknown production purpose'):
        solve_pattern([option('lettuce')],production_purpose='profit')


def test_default_request_keeps_original_goal_explicit():
    assert NorthRequest().production_purpose == 'fresh_mass'
    assert NorthRequest(production_purpose='protein').model_dump()['production_purpose'] == 'protein'
