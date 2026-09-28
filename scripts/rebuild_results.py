"""Capture reproducible engine outputs for the rebuild demo; no external observations."""
from pathlib import Path
from datetime import datetime, timezone
import copy
import json
import urllib.request

BASE='http://127.0.0.1:8011'
def call(path, payload=None):
    request=urllib.request.Request(BASE+path,data=None if payload is None else json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(request,timeout=30) as response:return json.load(response)

context=call('/api/planning-context?region_id=longyearbyen')
q=copy.deepcopy(context['illustrative_scenario'])
q.update(north_input_policy='source_resolved',quantity_basis='capacity',climate_context_id='nasa_ssp245_2035',planning_objective='balanced',resource_priority_fraction=.8)
records={}
for objective in ['capacity','balanced','water_priority','energy_priority']:
    q['planning_objective']=objective
    records[objective]=call('/api/simulate',q)
q['planning_objective']='balanced'
information=call('/api/decision-information',q)
field=call('/api/pattern-field-update',{'simulation':q})
assert field['before']['request']['north_input_policy']=='source_resolved'
assert field['after']['request']['north_input_policy']=='source_resolved'
records.update(information=information,field=field)
out=Path(__file__).resolve().parents[1]/'docs/verification/rebuild/engine-results.json'
out.write_text(json.dumps({'at':datetime.now(timezone.utc).isoformat(),'classification':'EXPLICIT SCENARIO; NOT ARCTIC OBSERVATION OR VALIDATED LOCAL PLAN','results':records},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({key:{'run_id':records[key]['run_id'],'water_m3':records[key]['optimized']['totals']['water_m3'],'energy_kwh':records[key]['optimized']['totals']['energy_kwh'],'crops':{c['crop_id']:c['production_kg'] for c in records[key]['optimized']['crops']}} for key in ['capacity','balanced','water_priority','energy_priority']},ensure_ascii=False))
