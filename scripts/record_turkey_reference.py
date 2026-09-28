import json,copy,urllib.request
from pathlib import Path
from datetime import datetime,timezone
root=Path.cwd();base='http://127.0.0.1:8011';runs=[]
presets=[('reference',1,1,1,0),('water10',.9,1,1,0),('water20',.8,1,1,0),('water30',.7,1,1,0),('drought',.8,.8,1.1,0),('dryrain',1,.8,1,0),('efficient',1,1,1,.1),('waterplus',1.1,1,1,0)]
for region in ['konya','seyhan_adana','gediz_manisa','gap_sanliurfa','trakya_edirne']:
 context=json.load(urllib.request.urlopen(base+'/api/planning-context?region_id='+region));q=context['default_scenario']
 for name,w,r,e,eff in presets:
  p=copy.deepcopy(q)
  for s in p['water_sources']:s['capacity_m3']*=w
  p['rainfall_factor']*=r;p['et0_factor']*=e;p['irrigation_efficiency']=min(1,p['irrigation_efficiency']+eff)
  req=urllib.request.Request(base+'/api/simulate',data=json.dumps(p).encode(),headers={'Content-Type':'application/json'})
  result=json.load(urllib.request.urlopen(req));runs.append({'region':region,'preset':name,'result':result})
  assert result['optimized'] is not None,(region,name,result['status'])
  totals=result['optimized']['totals'];known=totals.get('known_water_m3',totals['water_m3']);assert known<=sum(s['capacity_m3'] for s in p['water_sources'] if s['enabled'])+1
  if name=='reference':print(region,[(c['crop_id'],round(c['area_share_pct'],2)) for c in result['optimized']['crops']],round(known),flush=True)
(root/'docs/verification/turkey-reference/engine-results.json').write_text(json.dumps({'recorded_at':datetime.now(timezone.utc).isoformat(),'runs':runs},ensure_ascii=False,indent=2),encoding='utf-8')
print('40 source-backed regional scenario calculations recorded')
