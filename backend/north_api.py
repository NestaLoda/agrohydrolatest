"""New northern console endpoints; legacy Turkey/field contracts are retained."""
from functools import lru_cache
import json
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from .north_contracts import NorthRequest, FreezeRequest, ObserveRequest
from .provenance import ROOT, digest, canonical

router=APIRouter(prefix='/api/north')


@lru_cache(maxsize=48)
def _cached(request_json, artifact_stamp, code_stamp):
    from .north_planning import plan_north
    from .north_decision_story import summarize_decision
    result=plan_north(NorthRequest.model_validate_json(request_json))
    result['decision_story']=summarize_decision(result)
    return result


@lru_cache(maxsize=80)
def _period_cached(request_json, artifact_stamp, code_stamp):
    from .north_planning import plan_north
    from .north_decision_story import summarize_decision
    result=plan_north(NorthRequest.model_validate_json(request_json),with_sensitivity=False)
    result['decision_story']=summarize_decision(result)
    return result


def calculate(request):
    from .north_field import code_hash
    paths=['data/north/rebuild_climate/manifest.json','data/north/resource_evidence.json',
           'data/north/crop_evidence_v2.json','data/north/ground_evidence.json','data/auto_baseline_parameters.json',
           'data/north/food_composition.json','data/north/rebuild_climate/recent_reference/manifest.json']
    if request.target_year is not None: paths.append('data/north/rebuild_climate/annual/manifest.json')
    stamp=digest(b''.join((ROOT/p).read_bytes() for p in paths))
    return _cached(canonical(request.model_dump()),stamp,code_hash())


@router.get('/status')
def status():
    from .north_climate import list_climate_contexts
    try:return {'ready':True,**list_climate_contexts()}
    except (ValueError,FileNotFoundError) as e:
        path=ROOT/'data/north/rebuild_climate/acquisition_progress.json'
        return {'ready':False,'reason':str(e),'acquisition':json.loads(path.read_text()) if path.exists() else None}


@router.post('/plan')
def plan(request:NorthRequest):
    try:return calculate(request)
    except (ValueError,FileNotFoundError) as e:raise HTTPException(422,str(e)) from e

@router.post('/report')
def decision_report(request:NorthRequest):
    from .decision_pdf import north_pdf
    try:content=north_pdf(calculate(request))
    except (ValueError,FileNotFoundError) as e:raise HTTPException(422,str(e)) from e
    year=request.target_year or request.horizon_id
    return Response(content,media_type='application/pdf',headers={'Content-Disposition':f'attachment; filename="kuzey-{year}-karar-raporu.pdf"'})


@router.get('/climate')
def climate(year: int = Query(..., ge=2026, le=2100), scenario_id: str = 'ssp245'):
    from .north_climate import get_climate_context
    try:return get_climate_context('longyearbyen','mid',scenario_id,target_year=year)
    except (ValueError,FileNotFoundError) as e:raise HTTPException(422,str(e)) from e


@router.post('/timeline')
def timeline(request:NorthRequest):
    return _comparison(request)


@router.post('/reference')
def reference(request:NorthRequest):
    return _comparison(request,focused=True)


def _comparison(request:NorthRequest,*,focused=False):
    from .north_timeline import build_timeline
    from .north_field import code_hash
    paths=['data/north/rebuild_climate/manifest.json','data/north/resource_evidence.json',
           'data/north/crop_evidence_v2.json','data/north/ground_evidence.json','data/auto_baseline_parameters.json',
           'data/north/food_composition.json','data/north/rebuild_climate/recent_reference/manifest.json']
    if request.target_year is not None: paths.append('data/north/rebuild_climate/annual/manifest.json')
    stamp=digest(b''.join((ROOT/p).read_bytes() for p in paths))
    code=code_hash()
    try:return build_timeline(request,lambda r:_period_cached(canonical(r.model_dump()),stamp,code),focused=focused)
    except (ValueError,FileNotFoundError) as e:raise HTTPException(422,str(e)) from e


@router.post('/freeze')
def freeze(request:FreezeRequest):
    from .north_field import freeze_plan,profile_at_depth
    try:
        scenario=request.scenario
        if request.expectation:
            if request.intake_depth_m is None:raise ValueError('Su alma derinliği gerekli.')
            source=profile_at_depth(request.expectation.model_dump(),request.intake_depth_m)
            scenario=NorthRequest.model_validate({**scenario.model_dump(),'source_temperature_c':source['temperature_c'],'salinity_g_kg':source['salinity_g_kg']})
        result=calculate(scenario)
        return freeze_plan(scenario.model_dump(),result,request.expectation.model_dump() if request.expectation else None,intake_depth_m=request.intake_depth_m)
    except (ValueError,FileNotFoundError) as e:raise HTTPException(422,str(e)) from e


@router.post('/observe')
def observe(request:ObserveRequest):
    from .north_field import observe_plan
    try:return observe_plan(request)
    except (ValueError,FileNotFoundError) as e:raise HTTPException(422,str(e)) from e


@router.get('/frozen/{freeze_id}')
def frozen(freeze_id:str):
    from .north_field import read_frozen
    try:return read_frozen(freeze_id)
    except (ValueError,FileNotFoundError) as e:raise HTTPException(422,str(e)) from e


@router.post('/demo')
def demo(request:NorthRequest):
    from .north_field import rerun_source,pattern_changes
    try:
        before=calculate(request)
        temp=min(30.,request.source_temperature_c+3.)
        salinity=max(1.,request.salinity_g_kg-3.)
        after=rerun_source(before,temp,salinity,request.recovery)
        return {'classification':'SIMULATION_EXPLANATORY','before':before['plan'],'after':after['plan'],
                'changes':pattern_changes(before['plan'],after['plan']),
                'synthetic_inputs':{'source_temperature_c':temp,'salinity_g_kg':salinity},
                'unchanged_inputs':['future_climate','terrestrial_water','soil','crop_yield','crop_water','objective','constraints'],
                'limits':['Sentetik kaynak senaryosu; gerçek saha ölçümü veya model doğrulaması değildir.','PRE/POST motor aynıdır; dağılımın değişmemesi geçerli sonuçtur.']}
    except (ValueError,FileNotFoundError) as e:raise HTTPException(422,str(e)) from e
