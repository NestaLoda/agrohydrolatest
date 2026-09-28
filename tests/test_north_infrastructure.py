import pytest
from backend.north_infrastructure import minimum_cyclic_storage, replay, storage_design, energy_supply
from backend.north_resources import controlled_energy

def test_cyclic_storage_handles_boundary_and_volume_shortfall():
    assert minimum_cyclic_storage([0,6,0],[2,2,2])==4
    assert minimum_cyclic_storage([0,5,0],[2,2,2]) is None
    assert minimum_cyclic_storage([2,2],[2,2])==0
    # Dry spells cross the last/first day; capacity2 would fail.
    r=replay([0,6,0],[2,2,2],4,2)
    assert sum(r['deficits'])==0
    assert r['final_storage_m3']==2

def test_stress_replay_does_not_invent_water_or_probability():
    r=storage_design([{'model':'fixture','capture':[0,6,0],'demand':[2,2,2],
                      'dates':['2025-01-01','2025-01-02','2025-01-03']}],4)
    assert r['minimum_for_all_tested_records_m3']==4
    assert r['models'][0]['scenarios'][0]['backup_mean_m3_year']==0
    assert r['models'][0]['scenarios'][2]['minimum_cyclic_storage_m3'] is None
    assert r['models'][0]['scenarios'][2]['backup_mean_m3_year']>0

def test_no_plan_is_not_zero_need_and_wrap_backup_run():
    assert energy_supply({'status':'infeasible'},[],1)['power_screen_status']=='NOT_APPLICABLE'
    assert storage_design([],0)['classification']=='NOT_APPLICABLE'
    assert replay([0,5,0],[1,1,1],0,cyclic=True)['longest_backup_run_days']==2
    e=controlled_energy([{'date':'2025-01-01','tmin_c':-15,'tmax_c':-5,'shortwave_mj_m2':0}],overrides={'active_months':[6]})
    assert e['daily'][0]['peak_electricity_kw_m2']==0

def test_energy_split_closes_and_power_is_not_yearly_kwh():
    climate=[{'date':'2025-01-01','tmin_c':-15,'tmax_c':-5,'shortwave_mj_m2':0}]
    e=controlled_energy(climate)
    daily=e['daily'][0]
    assert daily['peak_electricity_kw_m2']>=daily['electricity_kwh_m2']/24
    assert daily['peak_heat_kw_th_m2']>=daily['heat_kwh_th_m2']/24
    keys=['lighting_kwh_m2','pumping_kwh_m2','fans_kwh_m2','dehumidification_kwh_m2','cooling_kwh_m2','heat_kwh_th_m2']
    o={'id':'a:greenhouse:annual','energy_components_monthly':[{'month':1,**{k:daily[k] for k in keys}}],
       'electricity_peak_bound_kw_m2':daily['peak_electricity_kw_m2'],'heat_peak_bound_kw_th_m2':daily['peak_heat_kw_th_m2']}
    total=2*(daily['electricity_kwh_m2']+daily['heat_kwh_th_m2']/3)+5
    plan={'allocations':[{'crop_id':'a','method':'greenhouse','season':'annual','area_m2':2}],
          'totals':{'equivalent_electricity_kwh':total,'heat_kwh_th':2*daily['heat_kwh_th_m2'],'treatment_electricity_kwh':5}}
    r=energy_supply(plan,[o],3,power_limit=.001)
    assert r['component_closure_residual_kwh']==pytest.approx(0,abs=1e-9)
    assert r['power_screen_status']=='DESIGN_REVIEW'
    assert r['local_supply_verified'] is False

@pytest.mark.parametrize('capture,demand',[([],[]),([1],[1,2]),([float('nan')],[1]),([-1],[1])])
def test_bad_chronology_rejected(capture,demand):
    with pytest.raises(ValueError):minimum_cyclic_storage(capture,demand)
