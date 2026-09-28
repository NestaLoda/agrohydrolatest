"""Deterministic one-at-a-time decision sensitivity, not probabilistic EVSI."""
import math
from typing import Callable
from .planning_contracts import SimulationRequest


def signature(result):
    pattern=result.get('optimized')
    if pattern is None:return None
    return {f"{a['crop_id']}|{a['method']}|{a['water_source']}":a['production_kg'] for a in pattern['allocations']}


def difference(before, after):
    a,b=signature(before),signature(after)
    feasibility=(a is None)!=(b is None)
    delta=None if a is None or b is None else sum(abs(a.get(k,0)-b.get(k,0)) for k in a.keys()|b.keys())
    changed=feasibility or (delta is not None and delta>max(.01,sum(a.values())*1e-6))
    # This L1 distance is ONLY an allocation-difference diagnostic, not nutrition/value.
    resources={}
    for key in ['water_m3','energy_kwh','open_field_area_ha']:
        x=(before.get('optimized') or {}).get('totals',{}).get(key)
        y=(after.get('optimized') or {}).get('totals',{}).get(key)
        resources[key]=None if x is None or y is None else y-x
    binding=lambda r:sorted(c['id'] for c in r.get('constraints',[]) if c.get('binding') and c['capacity']>0)
    return {'pattern_changed':changed,'feasibility_changed':feasibility,'allocation_l1_kg':delta,
            'resource_delta':resources,'binding_changed':binding(before)!=binding(after),
            'binding_before':binding(before),'binding_after':binding(after)}


def analyze_information(request:SimulationRequest, runner:Callable):
    if request.mode!='north':raise ValueError('Karar belirsizliği incelemesi için Gelecek / Kuzey seçin.')
    baseline=runner(request)
    freshwater=next((s for s in request.water_sources if s.source_id=='freshwater'),None)
    specs=[{'id':'freshwater','label':'Mevsimsel karasal tatlı su','base':freshwater.capacity_m3 if freshwater else None,
            'unit':'m³','measurable':False,'method':'Hidroloji, depolama, erişim ve tahsis kaydı',
            'range_source':'USER_SCENARIO: mevcut bütçenin ±%20 stres aralığı; olasılık/güven aralığı değil.'},
           {'id':'energy','label':'Üretim dönemi enerji bütçesi','base':request.energy_budget_kwh,'unit':'kWh','measurable':False,
            'method':'Üretim tesisi ve enerji altyapısı kaydı','range_source':'USER_SCENARIO: bütçenin ±%20 stres aralığı.'},
           {'id':'temperature','label':'Deniz kaynak suyu sıcaklığı','base':request.seawater_temperature_c,'unit':'°C','measurable':True,
            'method':'PWN sıcaklık + derinlik/UTC/konum, referans CTD karşılaştırması',
            'range_source':'LITERATURE_DOMAIN: bağlı arıtma ilişkisinin 5–18°C alanı; Arktik beklenen sıcaklık aralığı değildir.'}]
    rows=[]
    for spec in specs:
        base=spec['base'];trials=[]
        values=([5.,18.] if spec['id']=='temperature' else [base*.8,base*1.2]) if base is not None else []
        for value in sorted(set(values)):
            if not math.isfinite(value):raise ValueError('Sonlu duyarlılık girdisi gerekli.')
            payload=request.model_dump(mode='json')
            if spec['id']=='freshwater':
                for source in payload['water_sources']:
                    if source['source_id']=='freshwater':source['capacity_m3']=value
            elif spec['id']=='energy':payload['energy_budget_kwh']=value
            else:payload['seawater_temperature_c']=value
            result=runner(SimulationRequest.model_validate(payload))
            trials.append({'value':value,'status':result['status'],'run_id':result.get('run_id'),
                           'difference':difference(baseline,result),'optimized':result.get('optimized')})
        supported=bool(trials) and (baseline.get('optimized') is not None or any(t.get('optimized') is not None for t in trials))
        changes=any(t['difference']['pattern_changed'] for t in trials)
        rows.append({**spec,'trials':trials,'status':'ASSESSED' if supported else 'DATA_NEEDED',
                     'decision_impact':'DESEN / UYGULANABİLİRLİK DEĞİŞTİ' if supported and changes else 'TARANAN ARALIKTA DESEN DEĞİŞMEDİ' if supported else 'ÖNCE GEÇERLİ REFERANS DESENİ GEREKLİ'})
    for id,label,method in [('salinity','Deniz tuzluluğu / iletkenlik','Kalibre PWN iletkenlik/sıcaklık/basınç; uygun salinite dönüşümü'),
                             ('chemistry','Kaynak suyu kimyası','İzinli derinlik numunesi; laboratuvar onaylı sınırlı analiz paneli')]:
        rows.append({'id':id,'label':label,'base':None,'unit':'','measurable':True,'method':method,'trials':[],
                     'status':'MODEL_LINK_NEEDED','decision_impact':'BİLİNMİYOR · SAYISAL BAĞLANTI YOK',
                     'range_source':'Arıtma/üretim tepkisi bağlı değil; duyarlılık etkisi uydurulmadı.'})
    return {'classification':'SCENARIO_SENSITIVITY','baseline_run_id':baseline.get('run_id'),'baseline':baseline,'parameters':rows,
            'method':'Tek değişkeni değiştir, aynı motoru çalıştır; diğer girdiler ve planlama amacı sabit.',
            'limitations':['Olasılıksal bilgi değeri, beklenen ekonomik fayda veya güven yüzdesi hesaplanmaz.',
                            'Yalnız iki uç nokta taranır; etkileşimleri ve aradaki tüm eşikleri kapsamaz.',
                            'Kapasite/dengeli amaçta tek-ürün potansiyelleri değişen kaynaklarla yeniden hesaplanır; amaç kuralı sabit, normalizasyon katsayıları sabit değildir.',
                            'Modelden modele senaryo deneyi gerçek saha ölçümü değildir.',
                            'Mevcut sıcaklık bağlantısı yerel deniz kaynağı ve arıtma senaryosuna koşulludur; karasal yıllık suyu değiştirmez.']}
