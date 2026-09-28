"""Immutable PRE record and restricted, colocated source-water updates.

Future climate, terrestrial water, soil and crop coefficients never change here.
Today's source observation tests today's expectation; transfer to a future source
scenario is conditional, not validation of future climate or water availability.
"""
from datetime import datetime, timezone
from copy import deepcopy
import json
import math
from pathlib import Path
import re
from uuid import uuid4
import numpy as np

from .north_contracts import ModelExpectation, Observation
from .north_optimizer import solve_pattern
from .provenance import ROOT, canonical, digest, immutable_write

RUN_DIR = ROOT/'data/north/frozen_runs'
ENGINE_FILES=('north_optimizer.py','north_planning.py','north_resources.py','north_candidates.py','north_field.py','north_contracts.py','north_climate.py','north_decision_story.py','north_infrastructure.py','north_production_purpose.py','north_timeline.py')


def utc(value):
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if dt.tzinfo is None or dt.utcoffset().total_seconds() != 0:
        raise ValueError('Saat UTC ve saat dilimiyle kaydedilmeli.')
    return dt


def code_hash():
    return digest(b''.join((ROOT/'backend'/name).read_bytes() for name in ENGINE_FILES)+(ROOT/'data/north/food_composition.json').read_bytes())


def _depths(points):
    depths = [p['depth_m'] for p in points]
    if depths != sorted(set(depths)):
        raise ValueError('Profil derinlikleri artan sırada ve tekil olmalı.')
    return depths


def freeze_plan(scenario, result, expectation=None, directory=RUN_DIR, intake_depth_m=None):
    now = datetime.now(timezone.utc)
    if expectation:
        expectation = ModelExpectation.model_validate(expectation).model_dump()
        _depths(expectation['points'])
        if intake_depth_m is None:
            raise ValueError('Model beklentisiyle birlikte su alma derinliği dondurulmalı.')
        expected_source = profile_at_depth(expectation, intake_depth_m)
        for name, key in [('temperature_c','source_temperature_c'), ('salinity_g_kg','salinity_g_kg')]:
            if abs(expected_source[name]-scenario[key]) > 1e-6:
                raise ValueError('PRE kaynak girdileri model beklentisinin su alma derinliğiyle eşleşmiyor.')
        if utc(expectation['generated_at_utc']) > now:
            raise ValueError('Model üretim tarihi gelecekte olamaz.')
        if utc(expectation['valid_to_utc']) < now or utc(expectation['valid_from_utc']) > utc(expectation['valid_to_utc']):
            raise ValueError('Ölçümden önce geçerli model beklentisini dondurun; geçmiş gözlem için geriye dönük PRE oluşturulmaz.')
    record = {'id': uuid4().hex, 'frozen_at_utc': now.isoformat(), 'classification': 'PRE_TASE_MODEL_PLAN',
              'scenario': scenario, 'result': result, 'expectation': expectation, 'intake_depth_m': intake_depth_m, 'code_sha256': code_hash()}
    import platform, scipy
    record['runtime']={'python':platform.python_version(),'scipy':scipy.__version__}
    for name in ENGINE_FILES:
        immutable_write(Path(directory)/'engine_versions'/record['code_sha256']/name,(ROOT/'backend'/name).read_bytes())
    immutable_write(Path(directory)/'engine_versions'/record['code_sha256']/'food_composition.json',(ROOT/'data/north/food_composition.json').read_bytes())
    raw = canonical(record).encode('utf-8')
    immutable_write(Path(directory)/(record['id']+'.json'), raw)
    immutable_write(Path(directory)/(record['id']+'.sha256'), digest(raw).encode())
    return {'freeze_id': record['id'], 'frozen_at_utc': record['frozen_at_utc'], 'sha256': digest(raw),
            'expectation_frozen': expectation is not None,
            'intake_depth_m':intake_depth_m,'source_temperature_c':scenario['source_temperature_c'],'salinity_g_kg':scenario['salinity_g_kg'],
            'production_kg':result.get('plan',{}).get('totals',{}).get('production_kg'),
            'message': 'Plan ve model beklentisi donduruldu.' if expectation else 'Plan donduruldu. Gerçek profil karşılaştırması için ölçümden önce ayrıca model beklentisi içeren PRE kaydı oluşturun.'}


def read_frozen(freeze_id,directory=RUN_DIR):
    if not re.fullmatch(r'[0-9a-f]{32}',freeze_id):raise ValueError('Geçersiz PRE kimliği.')
    path=Path(directory)/(freeze_id+'.json')
    if not path.exists():raise ValueError('PRE kaydı bulunamadı.')
    raw=path.read_bytes(); hash_path=path.with_suffix('.sha256')
    if not hash_path.exists() or hash_path.read_text().strip()!=digest(raw):raise ValueError('PRE içerik özeti uyuşmuyor.')
    record=json.loads(raw)
    if record.get('classification')!='PRE_TASE_MODEL_PLAN':raise ValueError('Bu bir PRE kaydı değil.')
    return {'freeze_id':freeze_id,'frozen_at_utc':record['frozen_at_utc'],'sha256':digest(raw),
            'expectation_frozen':record['expectation'] is not None,'intake_depth_m':record['intake_depth_m'],
            'source_temperature_c':record['scenario']['source_temperature_c'],'salinity_g_kg':record['scenario']['salinity_g_kg'],
            'production_kg':record['result'].get('plan',{}).get('totals',{}).get('production_kg'),
            'message':'Önceden dondurulmuş PRE kaydı yüklendi.'}


def profile_at_depth(profile, depth):
    depths = _depths(profile['points'])
    if not depths[0] <= depth <= depths[-1]:
        raise ValueError('Su alma derinliği model profilinin aralığında olmalı.')
    return {key: float(np.interp(depth, depths, [p[key] for p in profile['points']]))
            for key in ('temperature_c', 'salinity_g_kg')}


def compare_profiles(expectation, observation, frozen_at, depth):
    expected = ModelExpectation.model_validate(expectation).model_dump()
    observed = Observation.model_validate(observation).model_dump()
    measured = utc(observed['measured_at_utc'])
    if measured <= utc(frozen_at) or utc(expected['generated_at_utc']) > utc(frozen_at):
        raise ValueError('Model beklentisi gerçek ölçümden önce dondurulmuş olmalı.')
    if measured > datetime.now(timezone.utc):
        raise ValueError('Gelecekteki bir zaman gerçek gözlem olarak kaydedilemez.')
    if not utc(expected['valid_from_utc']) <= measured <= utc(expected['valid_to_utc']):
        raise ValueError('Gözlem modelin zaman aralığına uymuyor.')
    lat1,lat2 = map(math.radians,[expected['latitude'],observed['latitude']])
    dlat=lat2-lat1; dlon=math.radians(observed['longitude']-expected['longitude'])
    distance = 6371*2*math.asin(min(1., math.sqrt(math.sin(dlat/2)**2+math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2)))
    if distance > 1.:
        raise ValueError('Profil konumları 1 km eşleştirme sınırını aşıyor. Yeni eşleştirilmiş beklenti gerekli.')
    for profile in (expected, observed):
        depths = _depths(profile['points'])
        if not depths[0] <= depth <= depths[-1]:
            raise ValueError('Seçilen su alma derinliği her iki profilin ölçülen aralığında olmalı; dışa kestirim yapılmaz.')
    def at(profile):
        return {key: float(np.interp(depth,[p['depth_m'] for p in profile['points']],[p[key] for p in profile['points']]))
                for key in ('temperature_c','salinity_g_kg')}
    before,after = at(expected),at(observed)
    return {'expected': before, 'observed': after, 'depth_m': depth, 'distance_km': distance,
            'residuals': {k: after[k]-before[k] for k in before},
            'temporal_support': expected['temporal_support'],
            'limits': ['1 km eşik mühendislik eşleştirme politikasıdır; akıntı ve model hücre ölçeği temsil kontrolü ayrıca gerekir.',
                       'Günlük/aylık ortalama ile anlık profil farkı yalnız model hatası değildir.',
                       'Mutlak kütlesel tuzluluk ve yerinde sıcaklık zorunlu. TOPAZ potansiyel sıcaklık / salinity alanı doğrudan yapıştırılamaz.']}


def rerun_source(result, temperature_c, salinity_g_kg, recovery):
    from .north_resources import ro_treatment
    coefficients = deepcopy(result['engine_inputs'])
    treatment = ro_treatment(salinity_g_kg, temperature_c, recovery=recovery)
    coefficients['ro_kwh_m3'] = treatment['specific_energy_kwh_m3']['central']
    coefficients['ro_heat_kwh_th_m3'] = treatment['conditioning_heat_kwh_th_m3']['central']
    coefficients['desalination'] = result['request']['desalination'] and treatment['status']=='CONDITIONAL'
    return {'plan': solve_pattern(**coefficients), 'treatment': treatment, 'engine_inputs': coefficients}


def observe_plan(request, directory=RUN_DIR):
    if not re.fullmatch(r'[0-9a-f]{32}', request.freeze_id):
        raise ValueError('Geçersiz PRE kimliği.')
    path=Path(directory)/(request.freeze_id+'.json')
    if not path.exists(): raise ValueError('Dondurulmuş PRE kaydı bulunamadı.')
    raw=path.read_bytes()
    hash_path=path.with_suffix('.sha256')
    if not hash_path.exists() or hash_path.read_text().strip()!=digest(raw):
        raise ValueError('Dondurulmuş PRE kaydının içerik özeti uyuşmuyor.')
    record=json.loads(raw)
    if code_hash()!=record['code_sha256']:
        raise ValueError('Motor sürümü değişmiş. Aynı motorla karşılaştırmak için kayıtlı sürümü yeniden çalıştırın.')
    if not record['expectation']:
        raise ValueError('Bu PRE kaydında ölçümden önce dondurulmuş profil beklentisi yok.')
    if abs(request.intake_depth_m-record['intake_depth_m']) > 1e-6:
        raise ValueError('POST su alma derinliği dondurulmuş PRE derinliğiyle aynı olmalı.')
    comparison=compare_profiles(record['expectation'],request.observation.model_dump(),record['frozen_at_utc'],request.intake_depth_m)
    after=rerun_source(record['result'],comparison['observed']['temperature_c'],comparison['observed']['salinity_g_kg'],record['scenario']['recovery'])
    before=record['result']['plan']
    changes=pattern_changes(before,after['plan'])
    result={'classification':'FIELD_INFORMED_CONDITIONAL_SOURCE_SCENARIO','before':before,'after':after['plan'],
            'comparison':comparison,'changes':changes,'connection_evidence':request.connection_evidence,
            'updated_inputs':['marine_source_temperature_c','marine_source_salinity_g_kg','derived_ro_specific_energy_kwh_m3','derived_ro_conditioning_heat_kwh_th_m3','derived_ro_pressure_feasibility'],
            'unchanged_inputs':['future_climate','terrestrial_freshwater','soil_permafrost','crop_yields','crop_water','objective','constraints'],
            'limits':['Gözlem günümüz kaynak koşulunu test eder. Gelecek planına aktarım koşullu kaynak senaryosudur; 2050 doğrulaması değildir.',
                      'Su alma yeriyle fiziksel bağlantı kullanıcı tarafından kaynak kaydıyla beyan edilir; yazılım hidrolojik bağı bağımsız doğrulamış sayılmaz.']}
    post={'id':uuid4().hex,'pre_id':record['id'],'request':request.model_dump(),'result':result,'created_at_utc':datetime.now(timezone.utc).isoformat()}
    immutable_write(Path(directory)/(post['id']+'.json'),canonical(post).encode())
    return {**result,'post_id':post['id']}


def pattern_changes(before,after):
    def area(plan):
        result = {}
        for allocation in plan.get('allocations', []):
            key = (allocation['crop_id'], allocation['method'], allocation['season'])
            result[key] = result.get(key, 0.) + allocation['area_m2']
        return result
    b,a=area(before),area(after)
    # Include unassigned area in the L1 balance: removing 100 m² is a 100 m²
    # change, whereas moving 100 m² between crops must not be double counted.
    before_area, after_area = sum(b.values()), sum(a.values())
    shift=(sum(abs(b.get(k,0)-a.get(k,0)) for k in set(b)|set(a)) + abs(after_area-before_area))/2
    bt,at=before.get('totals',{}),after.get('totals',{})
    def delta(key):
        # An infeasible solve may have no resource totals. Absence is not zero.
        return at[key]-bt[key] if key in at and key in bt else None
    changed = shift > .01
    feasible_before = before.get('status') != 'infeasible'
    feasible_after = after.get('status') != 'infeasible'
    feasibility_changed = feasible_before != feasible_after
    if feasibility_changed:
        message = 'Gözlemle güncellenen kaynak koşulunda önceki üretim planı uygulanamıyor.' if not feasible_after else 'Gözlemle güncellenen kaynak koşulunda uygulanabilir üretim oluştu.'
    else:
        message = 'Üretim dağılımı değişti.' if changed else 'Üretim dağılımı değişmedi. Bu da geçerli bir sonuç; enerji ve su farkını ayrıca inceleyin.'
    return {'area_reallocated_m2':shift, 'area_expanded_m2':max(0., after_area-before_area),
            'area_reduced_m2':max(0., before_area-after_area), 'changed_pattern':changed,
            'feasibility_changed':feasibility_changed, 'status_before':before.get('status'),
            'status_after':after.get('status'),
            'electricity_delta_kwh':delta('electricity_kwh'),
            'heat_delta_kwh_th':delta('heat_kwh_th'),
            'equivalent_electricity_delta_kwh':delta('equivalent_electricity_kwh'),
            'water_delta_m3':delta('water_m3'),
            'water_source_deltas_m3':{key:delta(key) for key in ('stored_water_m3','desalinated_m3','freshwater_m3')},
            'binding_constraints_before':before.get('binding_constraints', []),
            'binding_constraints_after':after.get('binding_constraints', []),
            'message':message}
