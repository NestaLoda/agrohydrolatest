"""Regional baseline is a source record, not a ceiling on the recommendation."""
import copy
import pytest
from backend.planning import planning_context, simulate
from backend.planning_contracts import SimulationRequest

REGIONS=['konya','seyhan_adana','gediz_manisa','gap_sanliurfa','trakya_edirne']

@pytest.mark.parametrize('site',REGIONS)
def test_all_regions_keep_official_baseline_and_can_expand_a_crop(site):
    context=planning_context(site)
    request=SimulationRequest.model_validate(context['default_scenario'])
    result=simulate(request)
    assert result['optimized'] is not None
    assert any(c['delta_area_ha']>1 for c in result['optimized']['crops'])
    assert sum(c['area_ha'] for c in result['optimized']['crops'])<=request.land_area_ha+1e-3
    for source,actual in zip(context['region']['crops'],context['baseline_analysis']['current']['crops']):
        assert actual['area_ha']==source['area_ha']
    assert result['request']==request.model_dump(mode='json')
    if site=='trakya_edirne':
        assert result['status']=='partial_conditional'
        assert result['optimized']['totals']['water_m3'] is None
        rice=next(c for c in result['optimized']['crops'] if c['crop_id']=='rice')
        assert rice['held_for_missing_water'] and rice['delta_area_ha']==0
        assert result['optimized']['totals']['known_water_m3']>0
        assert 'rice' in result['regional_scope']['held_crop_ids']
    else:
        assert result['optimized']['totals']['water_m3']<result['current']['totals']['water_m3']

def tiny():
    q=SimulationRequest.model_validate(planning_context('konya')['default_scenario'])
    q.crops=q.crops[:2];q.land_area_ha=10
    for i,c in enumerate(q.crops):
        c.current_area_ha=5;c.yield_kg_ha=1000
        c.target_production_kg=5000;c.min_production_kg=2500
        c.manual_net_irrigation_mm=100*(i+1)
    q.water_sources[0].capacity_m3=20000
    return q

def test_area_then_water_has_independently_known_optimum_beyond_reference():
    q=tiny();r=simulate(q)
    assert r['optimized']['crops'][0]['area_ha']==pytest.approx(7.5,abs=1e-5)
    assert r['optimized']['crops'][1]['area_ha']==pytest.approx(2.5,abs=1e-5)
    assert r['optimized']['totals']['water_m3']==pytest.approx(16666.6667,abs=.01)
    assert r['objective']['stages'][:2]==['max_cultivated_area','min_water']
    before=copy.deepcopy(r['optimized'])
    for c in q.crops:c.target_production_kg*=100;c.priority=10
    assert simulate(q)['optimized']['totals']==pytest.approx(before['totals'])

def test_budget_cut_preserves_minima_and_reports_unallocated_area():
    q=tiny();q.water_sources[0].capacity_m3=14000
    r=simulate(q)
    assert r['optimized']['totals']['water_m3']<=14000.01
    assert r['optimized']['totals']['unallocated_land_ha']>1
    assert all(c['production_kg']>=2500-1e-4 for c in r['optimized']['crops'])
    q.water_sources[0].capacity_m3=1
    assert simulate(q)['optimized'] is None

def test_missing_crop_can_rejoin_when_its_water_is_explicitly_supplied():
    q=SimulationRequest.model_validate(planning_context('trakya_edirne')['default_scenario'])
    rice=next(c for c in q.crops if c.crop_id=='rice')
    rice.manual_net_irrigation_mm=500
    q.water_sources[0].capacity_m3+=rice.current_area_ha*500*10/q.irrigation_efficiency
    r=simulate(q)
    assert r['status']=='conditional' and not r.get('regional_scope')
    assert r['optimized']['totals']['water_m3'] is not None

def test_partial_plan_does_not_relax_conflicting_held_crop_minimum():
    q=SimulationRequest.model_validate(planning_context('trakya_edirne')['default_scenario'])
    rice=next(c for c in q.crops if c.crop_id=='rice')
    rice.min_production_kg=rice.current_area_ha*rice.yield_kg_ha*2
    assert simulate(q)['optimized'] is None
