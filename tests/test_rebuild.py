"""Rebuild: evidence-to-decision behavior, objective invariants and field continuity."""
import copy
import pytest
from backend.planning import planning_context, simulate
from backend.planning_contracts import SimulationRequest
from backend.information_value import analyze_information


def scenario(objective='balanced', resolved=False):
    data=copy.deepcopy(planning_context('longyearbyen')['illustrative_scenario'])
    data.update(planning_objective=objective,quantity_basis='capacity',
                climate_context_id='nasa_ssp245_2035',
                north_input_policy='source_resolved' if resolved else 'explicit_scenario')
    return SimulationRequest.model_validate(data)


def test_source_screen_reaches_optimizer_but_does_not_create_local_coefficients():
    request=scenario(resolved=True)
    result=simulate(request)
    assert request.crops[1].climate_suitable is True
    assert result['request']['crops'][1]['climate_suitable'] is True
    assert result['effective_request']['crops'][1]['climate_suitable'] is False
    assert result['optimized']['crops'][1]['production_kg']==0
    assert any(c['crop_id']=='potato' for c in result['input_resolution']['changes'])
    assert result['input_resolution']['locally_validated_production_plan'] is False
    assert result['provenance']['north_resolution_hashes']


def test_default_unknowns_stay_unknown_after_real_climate_screen():
    request=SimulationRequest.model_validate(planning_context('longyearbyen')['default_scenario'])
    result=simulate(request)
    assert result['optimized'] is None
    assert result['status']=='insufficient_data'
    ledger=result['input_resolution']['evidence_ledger']
    assert next(p for p in ledger if p['variable']=='barley.yield_kg_ha')['state']=='UNKNOWN'
    assert next(p for p in ledger if p['variable']=='seasonal_freshwater')['field_measurable'] is False
    assert next(p for p in ledger if p['variable']=='source_chemistry')['field_measurable']=='POSSIBLE'


@pytest.mark.parametrize('objective',['water_priority','energy_priority'])
def test_resource_priority_calculates_nonzero_quantities_independent_of_demand(objective):
    request=scenario(objective)
    first=simulate(request)
    for crop in request.crops:
        crop.target_production_kg*=150
        crop.min_production_kg*=500
    second=simulate(request)
    assert first['optimized']==second['optimized']
    assert first['optimized']['totals']['water_m3']>0
    for crop in first['optimized']['crops']:
        actual=crop['production_kg']/first['objective']['normalization_kg'][crop['crop_id']]
        assert actual>=first['objective']['balanced_floor']*.8-1e-6
    assert first['objective']['stages'][2]==('min_water' if objective=='water_priority' else 'min_energy')


def test_priority_fraction_is_real_constraint_not_decorative_control():
    request=scenario('water_priority')
    high=simulate(request)
    request.resource_priority_fraction=.5
    low=simulate(request)
    assert low['optimized']['totals']['water_m3']<high['optimized']['totals']['water_m3']*.7


def test_methods_can_be_disabled_without_silently_restoring_last_method():
    request=scenario()
    request.crops[0].methods=[]
    result=simulate(request)
    assert result['optimized']['crops'][0]['production_kg']==0


def test_temperature_sensitivity_preserves_source_policy_and_terrestrial_budget():
    request=scenario(resolved=True)
    information=analyze_information(request,simulate)
    assert information['baseline']['request']['north_input_policy']=='source_resolved'
    temperature=next(p for p in information['parameters'] if p['id']=='temperature')
    assert len(temperature['trials'])==2
    assert next(p for p in information['parameters'] if p['id']=='salinity')['status']=='MODEL_LINK_NEEDED'
    assert request.water_sources[0].capacity_m3==2000
