"""Record source-backed refinement HTTP checks, without creating field observations."""
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.request import Request, urlopen

OUT=Path(__file__).resolve().parents[1]/'docs/verification/north-story'


def post(endpoint, body):
    req=Request('http://127.0.0.1:8011/api/north/'+endpoint,json.dumps(body).encode(),{'Content-Type':'application/json'})
    with urlopen(req,timeout=240) as response:return json.load(response)


def save(name,result):
    (OUT/name).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    default=post('plan',{})
    save('default-plan.json',default)
    plan=default['plan']
    areas=list(plan['crop_areas_m2'].values())
    assert max(areas)-min(areas)>10
    assert min(areas)>=5-1e-4
    assert plan['totals']['production_kg']>=plan['objective_policy']['balanced_mass_floor_kg']-1e-3
    story=default['decision_story']
    assert story['water_security']['source_balance_status']=='CLOSED'
    assert story['water_security']['storage']['minimum_required_m3'] is None
    assert story['water_security']['critical_month']['basis']=='MAX_MODEL_CLIMATOLOGICAL_MONTH_FROM_DAILY_REPLAY'
    timelines={}
    for scenario in ('ssp245','ssp585'):
        timeline=post('timeline',{'scenario_id':scenario})
        assert len(timeline['points'])==4
        assert len({p['engine_version'] for p in timeline['points']})==1
        for point in timeline['points']:
            t=point['totals']
            assert abs(t['water_m3']-sum(t[k] for k in ('stored_water_m3','desalinated_m3','freshwater_m3')))<1e-5
        timelines[scenario]=timeline
        save('timeline-'+scenario+'.json',timeline)
    future=timelines['ssp585']['points'][-1]
    frontier={r['crop_id']:r for r in future['frontier']['crops']}
    assert frontier['potato']['model_years_passing']==51
    assert frontier['barley']['model_years_passing']==19
    assert future['method_shares_pct']['open_field']==0
    modes={}
    for objective in ('water','energy'):
        result=post('plan',{'objective':objective})
        for crop,quantity in plan['crop_outputs_kg'].items():
            assert result['plan']['crop_outputs_kg'][crop]>=quantity-1e-3
        modes[objective]=result
    save('resource-modes.json',modes)
    scaled=post('plan',{'area_m2':1000})
    for crop,quantity in plan['crop_outputs_kg'].items():
        assert abs(scaled['plan']['crop_outputs_kg'][crop]-10*quantity)<.01
    save('scale-1000.json',scaled)
    demo=post('demo',{})
    assert demo['classification']=='SIMULATION_EXPLANATORY'
    assert demo['before']['solver']['version']==demo['after']['solver']['version']
    save('synthetic-post.json',demo)
    summary={'verified_at_utc':datetime.now(timezone.utc).isoformat(),'timelines':2,'periods_each':4,
             'checks':['non-equal calculated crop allocation','diversity floor','95% harvest floor',
                       'source closure','daily critical month','no invented minimum storage','same engine over time',
                       'real frontier counts','no invented open field','water-energy crop floors','1000 m² scale','synthetic same-engine POST'],
             'default_totals':plan['totals'],'default_areas':plan['crop_areas_m2']}
    save('http-verification.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
