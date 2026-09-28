import pytest
from backend.planning import planning_context, simulate
from backend.planning_contracts import SimulationRequest
from backend.scenario_preview import scenario_preview

@pytest.mark.parametrize('region',['konya','seyhan_adana','gediz_manisa','gap_sanliurfa','trakya_edirne'])
def test_live_water_is_the_same_scientific_coefficient_used_by_optimizer(region):
    q=SimulationRequest.model_validate(planning_context(region)['default_scenario'])
    q.rainfall_factor=.8;q.irrigation_efficiency=.95
    preview=scenario_preview(q);result=simulate(q)
    assert preview['optimization_performed'] is False
    assert preview['crop_water']==result['crop_water']
    for c,w in zip(q.crops,preview['crop_water']):
        current=next(row for row in result['current']['crops'] if row['crop_id']==c.crop_id)
        if w['gross_water_m3_ha'] is None:assert current['water_m3'] is None
        else:assert current['water_m3']==pytest.approx(c.current_area_ha*w['gross_water_m3_ha'])

def test_area_change_does_not_change_water_per_hectare():
    q=SimulationRequest.model_validate(planning_context('konya')['default_scenario'])
    first=scenario_preview(q)
    q.crops[0].current_area_ha/=2
    assert scenario_preview(q)['crop_water']==first['crop_water']

def test_unknown_calendar_and_rice_remain_unknown_not_zero():
    q=SimulationRequest.model_validate(planning_context('trakya_edirne')['default_scenario'])
    q.crops[0].season_start=q.crops[0].season_start.replace(year=2040)
    rows=scenario_preview(q)['crop_water']
    assert next(r for r in rows if r['crop_id']==q.crops[0].crop_id)['gross_water_m3_ha'] is None
    assert next(r for r in rows if r['crop_id']=='rice')['gross_water_m3_ha'] is None

def test_preview_does_not_invent_northern_current_pattern():
    q=SimulationRequest.model_validate(planning_context('longyearbyen')['default_scenario'])
    with pytest.raises(ValueError):scenario_preview(q)
