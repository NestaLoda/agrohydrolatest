from backend.north_contracts import NorthRequest
from backend.north_timeline import build_timeline, period_summary


def fixture(request):
    factor={'historical':1,'recent':1.5,'near':2,'mid':3,'late':4}[request.horizon_id]
    return {'request':request.model_dump(),
            'plan':{'status':'conditional','allocations':[{'crop_id':'barley','name':'Arpa','method':'greenhouse','area_m2':50,'production_kg':factor*100}],
                    'totals':{'water_m3':factor*10,'stored_water_m3':factor*7}},
            'climate':{'ensemble':{'temperature':factor}},
            'candidates':{'candidates':[{}],'climate_frontier':{'counts':{'candidate':factor}}},
            'provenance':{'engine_version':'test-only'}}


def test_timeline_preserves_every_non_climate_input_and_ssp():
    original=NorthRequest(scenario_id='ssp585',area_m2=1000,minimum_crop_share=.03,storage_m3_per_m2=.2,
                         objective='water',energy_limit_kwh=200000,disabled_crops=['basil'])
    received=[]
    def calculate(request):
        received.append(request.model_dump())
        return fixture(request)
    result=build_timeline(original,calculate)
    assert [r['horizon_id'] for r in received]==['historical','recent','near','mid','late']
    assert [r['scenario_id'] for r in received]==['ssp245','ssp245','ssp585','ssp585','ssp585']
    for row in received:
        for key,val in original.model_dump().items():
            if key not in ('horizon_id','scenario_id'):assert row[key]==val
    assert len(result['points'])==5
    assert result['baseline_horizon_id']=='recent'
    assert result['points'][1]['period']=='2015–2025'
    assert 'cross-dataset' in result['comparison_policy']
    assert result['points'][-1]['totals']['water_m3']==40
    assert result['points'][0]['period']=='1995–2014'
    assert original.horizon_id=='mid'


def test_percent_denominator_is_planning_area_and_unassigned_is_retained():
    result=period_summary(fixture(NorthRequest(area_m2=100)))
    assert result['method_shares_pct']['greenhouse']==50
    assert result['unassigned_share_pct']==50
    assert result['stored_share_pct']==70
    assert result['crops'][0]['share_pct']==50


def test_infeasible_is_not_zero_water_claim():
    data=fixture(NorthRequest())
    data['plan']={'status':'infeasible','allocations':[]}
    result=period_summary(data)
    assert result['status']=='infeasible'
    assert result['totals']=={}
    assert result['stored_share_pct'] is None


def test_focused_reference_comparison_uses_same_model_2026_and_selected_year():
    original=NorthRequest(target_year=2037,scenario_id='ssp585',area_m2=1250,roof_ratio=2,objective='water')
    received=[]
    def calculate(request):
        received.append(request.model_dump())
        return fixture(request)
    result=build_timeline(original,calculate,focused=True)
    assert [r['horizon_id'] for r in result['points']]==['baseline_2026','year']
    assert [r['target_year'] for r in received]==[2026,2037]
    assert [r['scenario_id'] for r in received]==['ssp585','ssp585']
    for request in received:
        for key,value in original.model_dump().items():
            if key not in ('horizon_id','target_year','scenario_id'): assert request[key]==value
    assert result['baseline_horizon_id']=='baseline_2026'
    assert 'not measured current weather' in result['comparison_policy']
    assert result['points'][-1]['period']=='2037'


def test_focused_legacy_period_selection_remains_distinct_without_duplicate_reference():
    selected=build_timeline(NorthRequest(horizon_id='late'),fixture,focused=True)
    assert [r['horizon_id'] for r in selected['points']]==['historical','recent','late']
    baseline=build_timeline(NorthRequest(horizon_id='recent'),fixture,focused=True)
    assert [r['horizon_id'] for r in baseline['points']]==['historical','recent']


def test_focused_2026_has_one_point_without_false_delta():
    calls=[]
    def calculate(request):
        calls.append(request)
        return fixture(request)
    result=build_timeline(NorthRequest(target_year=2026),calculate,focused=True)
    assert [p['horizon_id'] for p in result['points']]==['baseline_2026']
    assert len(calls)==1


def test_reference_endpoint_keeps_points_contract_and_uses_period_cache(monkeypatch):
    import json
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from backend import north_api
    received=[]
    def cached(request_json,artifact_stamp,code_stamp):
        request=NorthRequest(**json.loads(request_json))
        received.append(request)
        assert artifact_stamp and code_stamp
        return fixture(request)
    monkeypatch.setattr(north_api,'_period_cached',cached)
    app=FastAPI();app.include_router(north_api.router)
    with TestClient(app) as client:
        response=client.post('/api/north/reference',json={'target_year':2072,'scenario_id':'ssp585'})
    assert response.status_code==200
    assert [r['horizon_id'] for r in response.json()['points']]==['baseline_2026','year']
    assert [r.target_year for r in received]==[2026,2072]
