import pytest
from pydantic import ValidationError
from backend.north_contracts import NorthRequest
from backend.north_optimizer import solve_pattern


def option(crop, water=1., heat=10., yield_=2.):
    return dict(crop_id=crop, method='greenhouse', season='annual', yield_kg_m2=yield_,
                water_monthly_m3_m2=[water/12]*12, heat_kwh_th_m2=heat, electricity_kwh_m2=1.)


def test_balanced_uses_yield_and_diversity_floor_not_equal_crop_shares():
    r=solve_pattern([option('a'),option('b',yield_=4.)], inflow_m3=[2.]*12)
    assert r['crop_areas_m2']['a']==pytest.approx(5,abs=1e-4)
    assert r['crop_areas_m2']['b']==pytest.approx(90.125,abs=1e-4)
    assert r['objective_policy']['maximum_fresh_mass_kg']==pytest.approx(390)
    assert r['totals']['production_kg']==pytest.approx(390*.95,abs=1e-4)
    assert r['crop_outputs_kg']['a']==pytest.approx(10,abs=1e-4)
    assert r['crop_outputs_kg']['b']==pytest.approx(360.5,abs=1e-4)
    assert r['totals']['stored_water_m3']+r['totals']['desalinated_m3']==pytest.approx(r['totals']['water_m3'])
    prior=0.
    for m in r['monthly']:
        assert prior+m['capture_m3']==pytest.approx(m['stored_water_used_m3']+m['spill_m3']+m['storage_end_m3'], abs=1e-6)
        prior=m['storage_end_m3']
    assert r['solver']['max_equality_residual']<1e-6


def test_no_water_and_no_desal_gives_no_production_not_invented_water():
    r=solve_pattern([option('a')],desalination=False)
    assert r['status']=='infeasible'
    assert r['allocations']==[]


def test_resource_goal_respects_explicit_crop_floors():
    r=solve_pattern([option('a'),option('b')], objective='water', production_retention=.8)
    for crop, balanced in r['balanced_crop_outputs_kg'].items():
        assert r['crop_outputs_kg'][crop]>=.8*balanced-1e-5
    assert all(a>=5-1e-6 for a in r['crop_areas_m2'].values())
    assert r['totals']['water_m3'] < solve_pattern([option('a'),option('b')])['totals']['water_m3']


def test_energy_limit_changes_feasible_scale():
    r=solve_pattern([option('a')], energy_limit_kwh=150.)
    assert r['totals']['equivalent_electricity_kwh']<=150.0001
    assert r['totals']['area_m2']==pytest.approx(9.5, abs=1e-4)
    assert r['objective_policy']['maximum_fresh_mass_kg']==pytest.approx(20,abs=1e-4)


def test_ro_source_change_uses_same_engine_and_no_change_is_valid():
    before=solve_pattern([option('a')], ro_kwh_m3=3.)
    after=solve_pattern([option('a')], ro_kwh_m3=5.)
    assert before['crop_outputs_kg']==pytest.approx(after['crop_outputs_kg'],abs=1e-4)
    assert after['totals']['electricity_kwh']>before['totals']['electricity_kwh']


def test_no_withdrawal_policy_does_not_use_freshwater():
    r=solve_pattern([option('a')], freshwater_m3=0.)
    assert r['totals']['freshwater_m3']==0
    assert r['totals']['desalinated_m3']>0


@pytest.mark.parametrize('change',[{'production_retention':0},{'area_m2':-1},{'inflow_m3':[1]*11},{'heat_cop':0},
    {'minimum_crop_share':-.01},{'minimum_crop_share':.21},{'minimum_crop_share':True},
    {'minimum_crop_share':float('nan')},{'minimum_crop_share':float('inf')}])
def test_invalid_resource_inputs(change):
    with pytest.raises(ValueError): solve_pattern([option('a')],**change)


def test_regret_balance_between_measured_resource_tradeoff_anchors():
    # Same crop/yield, two physical methods with opposing resource intensities.
    water_saver=option('a',water=1,heat=9,yield_=1);water_saver['method']='hydroponics'
    energy_saver=option('a',water=10,heat=0,yield_=1);energy_saver['method']='greenhouse'
    r=solve_pattern([water_saver,energy_saver],ro_kwh_m3=0)
    assert r['totals']['production_kg']==pytest.approx(95,abs=1e-4)
    by_method={a['method']:a['area_m2'] for a in r['allocations']}
    assert by_method==pytest.approx({'hydroponics':47.5,'greenhouse':47.5},abs=1e-4)
    anchors=r['objective_policy']['regret_anchors']
    assert anchors['water']['minimum']==pytest.approx(95,abs=1e-4)
    assert anchors['water']['at_other_minimum']==pytest.approx(950,abs=1e-3)
    assert anchors['energy']['minimum']==pytest.approx(95,abs=1e-4)
    water_regret=(r['totals']['water_m3']-anchors['water']['minimum'])/anchors['water']['normalization_span']
    energy_regret=(r['totals']['equivalent_electricity_kwh']-anchors['energy']['minimum'])/anchors['energy']['normalization_span']
    assert water_regret==pytest.approx(.5,abs=1e-6)
    assert energy_regret==pytest.approx(.5,abs=1e-6)


def test_water_and_energy_modes_retain_new_balanced_crop_amounts_with_distinct_methods():
    options=[option('a',water=1,heat=9,yield_=1),option('a',water=10,heat=0,yield_=1)]
    balanced=solve_pattern(options,ro_kwh_m3=0)
    water=solve_pattern(options,ro_kwh_m3=0,objective='water')
    energy=solve_pattern(options,ro_kwh_m3=0,objective='energy')
    for result in [water,energy]:
        assert result['balanced_crop_outputs_kg']==pytest.approx(balanced['crop_outputs_kg'],abs=1e-4)
        assert result['crop_outputs_kg']['a']>=balanced['crop_outputs_kg']['a']-1e-5
    assert water['totals']['water_m3']<balanced['totals']['water_m3']<energy['totals']['water_m3']
    assert energy['totals']['equivalent_electricity_kwh']<balanced['totals']['equivalent_electricity_kwh']<water['totals']['equivalent_electricity_kwh']


def test_coincident_resource_optima_are_pinned_without_division_by_zero():
    r=solve_pattern([option('a')])
    assert r['totals']['area_m2']==pytest.approx(95,abs=1e-4)
    assert r['objective_policy']['balanced_max_normalized_regret']==pytest.approx(0,abs=1e-6)
    assert not any(a['active_regret_dimension'] for a in r['objective_policy']['regret_anchors'].values())


def test_explicit_zero_diversity_can_choose_single_higher_yield_crop():
    r=solve_pattern([option('a'),option('b',yield_=4)],minimum_crop_share=0)
    assert r['crop_areas_m2']['a']==pytest.approx(0,abs=1e-5)
    assert r['crop_areas_m2']['b']==pytest.approx(95,abs=1e-4)


def test_diversity_floor_applies_to_crop_across_methods_not_each_option():
    options=[option('a'),option('a',heat=20),option('b',yield_=4)]
    r=solve_pattern(options)
    assert r['crop_areas_m2']['a']==pytest.approx(5,abs=1e-4)
    assert len([a for a in r['allocations'] if a['crop_id']=='a'])==1


def test_diversity_sum_and_resource_conflicts_are_not_silently_relaxed():
    with pytest.raises(ValueError,match='exceed'):
        solve_pattern([option(str(i)) for i in range(6)],minimum_crop_share=.2)
    # A five m2 floor is explicitly infeasible under this tiny energy cap.
    result=solve_pattern([option('a')],energy_limit_kwh=1)
    assert result['status']=='infeasible'
    assert result['minimum_crop_share']==.05


def test_zero_water_intensity_and_ro_heat_stay_finite_and_unit_consistent():
    dry=solve_pattern([option('a',water=0)],desalination=False)
    assert dry['totals']['water_m3']==0
    assert dry['objective_policy']['regret_anchors']['water']['active_regret_dimension'] is False
    treated=solve_pattern([option('a')],ro_heat_kwh_th_m3=6,heat_cop=2)
    assert treated['totals']['treatment_heat_kwh_th']==pytest.approx(6*treated['totals']['desalinated_m3'])
    assert treated['totals']['equivalent_electricity_kwh']==pytest.approx(treated['totals']['electricity_kwh']+treated['totals']['heat_kwh_th']/2)


def test_policy_request_defaults_and_bounds_are_explicit():
    request=NorthRequest()
    assert request.minimum_crop_share==.05
    assert request.production_retention==1
    assert 'declared diversity policy' in NorthRequest.model_json_schema()['properties']['minimum_crop_share']['description']
    for value in [-1,.3,float('nan')]:
        with pytest.raises(ValidationError):NorthRequest(minimum_crop_share=value)
