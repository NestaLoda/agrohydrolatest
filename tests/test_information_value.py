from copy import deepcopy
import pytest
from backend.information_value import analyze_information, difference
from backend.planning import planning_context, simulate
from backend.planning_contracts import SimulationRequest


def test_information_sweep_changes_only_one_supported_input_and_preserves_baseline():
    request=SimulationRequest.model_validate(planning_context('longyearbyen')['illustrative_scenario'])
    original=request.model_dump(); calls=[]
    def runner(r):
        calls.append(r.model_dump());return simulate(r)
    result=analyze_information(request,runner)
    assert request.model_dump()==original and len(calls)==7
    allowed={'water_sources','energy_budget_kwh','seawater_temperature_c'}
    for call in calls[1:]:
        changed={k for k in original if original[k]!=call[k]}
        assert len(changed)==1 and changed<=allowed
    rows={r['id']:r for r in result['parameters']}
    assert rows['freshwater']['measurable'] is False
    assert rows['temperature']['measurable'] is True
    assert rows['salinity']['status']=='MODEL_LINK_NEEDED' and rows['salinity']['trials']==[]
    assert rows['chemistry']['trials']==[]


def test_identical_pattern_and_no_reference_are_not_false_information_gain():
    r=simulate(SimulationRequest.model_validate(planning_context('longyearbyen')['illustrative_scenario']))
    assert difference(r,deepcopy(r))['pattern_changed'] is False
    empty={'optimized':None,'constraints':[]}
    assert difference(empty,empty)['allocation_l1_kg'] is None
    assert difference(r,empty)['feasibility_changed'] is True


def test_information_not_turkey_marine_campaign():
    r=SimulationRequest.model_validate(planning_context('konya')['default_scenario'])
    with pytest.raises(ValueError,match='Kuzey'):analyze_information(r,simulate)


def test_infeasible_reference_can_reveal_a_feasible_trial():
    request=SimulationRequest.model_validate(planning_context('longyearbyen')['illustrative_scenario'])
    def runner(r):
        feasible=r.energy_budget_kwh>request.energy_budget_kwh
        return {'status':'conditional' if feasible else 'infeasible','constraints':[],
                'optimized':{'allocations':[],'totals':{}} if feasible else None}
    result=analyze_information(request,runner)
    energy=next(row for row in result['parameters'] if row['id']=='energy')
    assert energy['status']=='ASSESSED'
    assert any(t['difference']['feasibility_changed'] for t in energy['trials'])
