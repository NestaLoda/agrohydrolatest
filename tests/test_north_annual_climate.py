"""Exact source-year chronology and solver propagation, no interpolated weather."""
from datetime import datetime, timezone
import hashlib
import json
import shutil
import pandas as pd
import pytest
from pydantic import ValidationError
from backend import north_climate as climate
from backend.north_contracts import NorthRequest
from backend.north_planning import plan_north
from backend.north_timeline import build_timeline
from scripts.ingest_north_rebuild_climate import period_metrics, parse_raw


@pytest.mark.parametrize('year',[datetime.now(timezone.utc).year,2028,2037,2061,2072,2080,2100])
@pytest.mark.parametrize('scenario',['ssp245','ssp585'])
def test_exact_year_complete_daily_source_values_and_recomputed_metrics(year,scenario):
    context=climate.get_climate_context(horizon_id='recent',scenario_id=scenario,target_year=year)
    assert context['horizon_id']=='year'
    assert context['period']==[year,year]
    assert context['years']==1
    assert 'NOT_WEATHER_FORECAST' in context['classification']
    for member in context['models']:
        model=member['model']
        frame=climate.load_climate_frame(scenario_id=scenario,model_id=model,target_year=year)
        assert pd.DatetimeIndex(frame.date).equals(pd.date_range(f'{year}-01-01',f'{year}-12-31'))
        source=climate.CLIMATE_DIR/'raw'/'longyearbyen'/model/scenario/f'tasmin_{year}.nc'
        _, kelvin,_=parse_raw(source.read_bytes(),'tasmin',year,'longyearbyen',model,scenario)
        assert frame.tmin_c.to_numpy()==pytest.approx(kelvin-273.15,abs=1e-8)
        computed=period_metrics(frame)
        assert member['summary']==pytest.approx(computed['summary'])
    historical=climate.get_climate_context(horizon_id='historical')
    assert context['change_from_historical']['precipitation_mm']==pytest.approx(context['ensemble']['precipitation_mm']['mean']-historical['ensemble']['precipitation_mm']['mean'])


def test_full_annual_package_has_no_gaps_or_unverified_artifacts():
    manifest=json.loads((climate.CLIMATE_DIR/'annual/manifest.json').read_bytes())
    assert manifest['raw_file_count']==75*2*3*4
    assert len(manifest['derived_files'])==75*2*3+1
    for item in manifest['raw_files']+manifest['derived_files']:
        path=item.get('path',item.get('local_path'))
        assert hashlib.sha256((climate.ROOT/path).read_bytes()).hexdigest()==item['sha256']
    assert climate.list_climate_contexts()['annual_years']['ready'] is True


@pytest.mark.parametrize('year',[2025,2101,2030.5,True])
def test_invalid_years_fail_instead_of_clamping_or_interpolating(year):
    with pytest.raises((ValueError,ValidationError)):
        NorthRequest(target_year=year)
    with pytest.raises(ValueError):
        climate.get_climate_context(target_year=year)


def test_annual_plan_recomputes_year_specific_resource_inputs_and_conserves_water():
    plans=[plan_north(NorthRequest(target_year=year),with_sensitivity=False) for year in (2037,2072)]
    for year,result in zip((2037,2072),plans):
        assert result['climate']['period']==[year,year]
        assert result['request']['target_year']==year
        assert all(row['worst_topup_year']==year for row in result['daily_reliability'])
        totals=result['plan']['totals']
        assert totals['water_m3']==pytest.approx(totals['stored_water_m3']+totals['desalinated_m3']+totals['freshwater_m3'])
        assert result['provenance']['climate_manifest_sha256']==result['climate']['manifest_sha256']
    assert plans[0]['engine_inputs']['inflow_m3']!=plans[1]['engine_inputs']['inflow_m3']
    one={o['id']:o for o in plans[0]['engine_inputs']['options']}
    two={o['id']:o for o in plans[1]['engine_inputs']['options']}
    assert any(one[k]['heat_kwh_th_m2']!=two[k]['heat_kwh_th_m2'] for k in one)


def test_timeline_reference_periods_clear_target_year_selected_year_remains():
    received=[]
    def calculate(request):
        received.append(request)
        return {'request':request.model_dump(),'plan':{'status':'infeasible','allocations':[]},
                'climate':{'ensemble':{}},'candidates':{'candidates':[]},'provenance':{'engine_version':'TEST'}}
    result=build_timeline(NorthRequest(target_year=2037),calculate)
    assert [r.target_year for r in received]==[None,None,None,None,None,2037]
    assert result['points'][-1]['horizon_id']=='year'
    assert result['points'][-1]['period']=='2037'
    assert result['baseline_horizon_id']=='recent'


def test_annual_daily_tampering_fails_before_cached_plan_can_be_used(tmp_path,monkeypatch):
    context=climate.get_climate_context(target_year=2037)
    paths=['manifest.json','climate_contexts.json','annual/manifest.json','annual/contexts.json']
    root=tmp_path/'data/north/rebuild_climate'
    for relative in paths:
        target=root/relative; target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(climate.CLIMATE_DIR/relative,target)
    for member in context['models']:
        target=tmp_path/member['daily_path']; target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(climate.ROOT/member['daily_path'],target)
    target=tmp_path/context['models'][0]['daily_path']
    target.write_bytes(b'corrupt-source')
    monkeypatch.setattr(climate,'ROOT',tmp_path)
    monkeypatch.setattr(climate,'CLIMATE_DIR',root)
    climate._annual_package.cache_clear(); climate._read_package.cache_clear(); climate._read_frame.cache_clear()
    with pytest.raises(ValueError,match='hash mismatch'):
        climate.get_climate_context(target_year=2037)


def test_climate_endpoint_is_lightweight_and_rejects_outside_coverage():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from backend.north_api import router
    app=FastAPI(); app.include_router(router)
    with TestClient(app) as client:
        response=client.get('/api/north/climate?year=2072&scenario_id=ssp585')
        assert response.status_code==200
        assert response.json()['period']==[2072,2072]
        assert 'plan' not in response.json()
        assert client.get('/api/north/climate?year=2025').status_code==422
        assert client.get('/api/north/climate?year=2101').status_code==422
        assert client.get('/api/north/climate?year=2072&scenario_id=fake').status_code==422
