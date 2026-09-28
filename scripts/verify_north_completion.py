"""Real API regression for the five PC-side completion packages; no fake observations."""
from datetime import datetime,timezone
from pathlib import Path
import json
import httpx as requests

out=Path('docs/verification/north-completion');out.mkdir(parents=True,exist_ok=True)
base='http://127.0.0.1:8011/api/north/'
def post(path,payload):
    r=requests.post(base+path,json=payload,timeout=600);r.raise_for_status();return r.json()
checks=[];results={}
for purpose in ['fresh_mass','protein','food_energy']:
    result=post('plan',{'production_purpose':purpose})
    (out/f'plan-{purpose}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    assert result['plan']['status']!='infeasible'
    energy=result['infrastructure']['energy']
    assert abs(energy['component_closure_residual_kwh'])<1e-5
    assert energy['operation_power_upper_bound_kw']>0
    assert not energy['local_supply_verified']
    results[purpose]=result
    checks.append({'purpose':purpose,'crops':result['plan']['crop_areas_m2'],
                   'energy_closure':energy['component_closure_residual_kwh']})
    print(purpose, result['plan']['crop_areas_m2'],flush=True)
assert results['fresh_mass']['plan']['crop_areas_m2']!=results['protein']['plan']['crop_areas_m2']
line=post('timeline',{})
assert [p['horizon_id'] for p in line['points']]==['historical','recent','near','mid','late']
assert line['baseline_horizon_id']=='recent'
(out/'timeline.json').write_text(json.dumps(line,ensure_ascii=False,indent=2),encoding='utf-8')
no_water=post('plan',{'roof_ratio':0,'desalination':False})
assert no_water['plan']['status']=='infeasible'
assert no_water['infrastructure']['energy']['classification']=='NOT_APPLICABLE'
limited=post('plan',{'available_power_kw':.001})
assert limited['infrastructure']['energy']['power_screen_status']=='DESIGN_REVIEW'
for path in ['validation/readiness','validation/templates']:
    r=requests.get(base+path,timeout=30);r.raise_for_status();assert r.json()
bad=requests.post(base+'validation/sample-review',json={'source_kind':'seawater'},timeout=30)
assert bad.status_code==422
summary={'verified_at_utc':datetime.now(timezone.utc).isoformat(),'purpose_cases':checks,
         'timeline_periods':5,'empty_plan_not_zero_supply':True,'power_limit_screen':True,
         'validation_endpoints':True,'incomplete_observation_rejected':True,'real_field_data_created':False}
(out/'api-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False),flush=True)
