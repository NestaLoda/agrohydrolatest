"""U9 explanations and evidence-context invariants, not UI implementation mirrors."""
import copy
from backend.planning import planning_context, simulate
from backend.planning_contracts import SimulationRequest


def test_reduced_area_minimum_explanation_has_solver_support():
    payload=planning_context('konya')['default_scenario']
    payload['planning_objective']='demand'  # Historical demand mode remains supported.
    for source in payload['water_sources']:
        if source['enabled']:source['capacity_m3']*=.5
    result=simulate(SimulationRequest.model_validate(payload))
    reduced=[c for c in result['optimized']['crops'] if c['delta_area_ha']<0 and any(k['id']=='crop_min_output_'+c['crop_id'] and k['binding'] for k in result['constraints'])]
    assert reduced, 'At least one crop must be reduced to its declared production floor.'
    assert all('minimum üretim sınırına kadar azaltıldı' in c['summary_reason'] for c in reduced)


def test_climate_evidence_selection_does_not_invent_agronomic_response():
    payload=planning_context('longyearbyen')['illustrative_scenario']
    first=simulate(SimulationRequest.model_validate(payload))
    other=copy.deepcopy(payload)
    other['climate_context_id']='nasa_ssp585_2035'
    second=simulate(SimulationRequest.model_validate(other))
    assert first['optimized']==second['optimized']
    assert second['provenance']['climate_context_id']=='nasa_ssp585_2035'
    assert 'not applied' in second['provenance']['climate_context_role']


def test_monthly_future_context_preserves_annual_precipitation_and_units():
    from backend.north_evidence import load_north_evidence
    evidence=load_north_evidence()['climate_2035']
    for item in evidence['scenarios']:
        months=evidence['monthly'][item['scenario']]
        assert [m['month'] for m in months]==list(range(1,13))
        assert abs(sum(m['precipitation_mm'] for m in months)-item['annual_precipitation_mm'])<.01
        assert all(m['tmin_c']<=m['tmax_c'] for m in months)
