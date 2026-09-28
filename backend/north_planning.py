"""Evidence -> candidates -> engineering requirements -> monthly decision LP.

The default is a normalized facility comparison, not an allocated local farm.
Climate trajectories remain distinct until nonlinear daily coefficients have
been computed. Range cases rerun the same optimizer; no probability is implied.
"""
from copy import deepcopy
from functools import lru_cache
import json
from statistics import mean
import numpy as np

from .north_contracts import NorthRequest
from .north_climate import get_climate_context, load_climate_frame, MODELS
from .north_candidates import evaluate_candidates, complete_cycle_capacity
from .north_optimizer import solve_pattern, VERSION
from .north_resources import controlled_energy, roof_storage_balance, ro_treatment
from .provenance import ROOT, canonical, digest
from .north_infrastructure import storage_design, energy_supply
from .runtime import writable_path

SEASONS = {'summer': [5,6,7,8,9], 'extended': list(range(3,11)), 'annual': list(range(1,13))}
SEASON_DAYS = {'summer':153, 'extended':245, 'annual':365}


def _average_options(groups):
    result=[]
    for index in range(len(groups[0])):
        rows=[group[index] for group in groups]
        o=deepcopy(rows[0])
        for key in ('heat_kwh_th_m2','electricity_kwh_m2','yield_kg_m2'):
            o[key]=mean(row[key] for row in rows)
        o['water_monthly_m3_m2']=[mean(row['water_monthly_m3_m2'][m] for row in rows) for m in range(12)]
        o['resource_ranges']={key:{bound:mean(row['resource_ranges'][key][bound] for row in rows)
                                 for bound in ('low','central','high')} for key in o['resource_ranges']}
        o['water_active_day_m3_m2']=mean(row['water_active_day_m3_m2'] for row in rows)
        o['resource_configurations']={key:[mean(row['resource_configurations'][key][i] for row in rows) for i in range(3)] for key in o['resource_configurations']}
        o['energy_components_monthly']=[{'month':m['month'],**{k:mean(row['energy_components_monthly'][j][k] for row in rows) for k in m if k!='month'}} for j,m in enumerate(o['energy_components_monthly'])]
        # Max across model trajectories is conservative; annual coefficients average.
        for key in ('electricity_peak_bound_kw_m2','heat_peak_bound_kw_th_m2'):
            o[key]=max(row[key] for row in rows)
        result.append(o)
    return result


@lru_cache(maxsize=24)
def _coefficient_package(site, horizon, scenario, climate_hash, resource_hash, crop_hash, target_year=None):
    cache_key=digest(canonical([site,horizon,scenario,climate_hash,resource_hash,crop_hash,target_year]).encode())
    cache_path=writable_path('data/north/derived_plans')/('coefficients-'+cache_key+'.json')
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding='utf-8'))
    context=get_climate_context(site,horizon,scenario,target_year)
    from pandas import concat
    models=[m['model'] for m in context['models']]
    frames={model:load_climate_frame(site,horizon,scenario,model,target_year) for model in models}
    candidates=evaluate_candidates(context,site,concat(list(frames.values()),ignore_index=True))
    trajectories={}; resource_cache={}
    for model in models:
        frame=frames[model]
        daily=frame.to_dict('records')
        options=[]
        for crop in candidates['candidates']:
            if not crop['normalized_plan_eligible']: continue
            p=crop['production']
            for method in crop['methods']:
                if not method['eligible_for_normalized_plan']: continue
                m=method['method']
                for season,months in SEASONS.items():
                    # Exact calendar length in annual mode, including leap days.
                    season_days=int(frame.date.dt.month.isin(months).sum()) if target_year is not None else SEASON_DAYS[season]
                    capacity=complete_cycle_capacity(crop,season_days,area_m2=1.)
                    if not capacity['complete_cycles']: continue
                    key=(model,m,p['target_temperature_c_day'],p['target_temperature_c_night'],p['dli_mol_m2_day'],p['photoperiod_h'],p['relative_humidity_pct'])
                    if key not in resource_cache:
                        resource_cache[key]=controlled_energy(daily,method='indoor' if m=='hydroponics' else 'greenhouse',
                            target_temp_c=p['target_temperature_c_day'],
                            target_dli_mol_m2_day=p['dli_mol_m2_day'],photoperiod_h=p['photoperiod_h'],
                            overrides={'relative_humidity':p['relative_humidity_pct']/100,'target_temp_c_night':p['target_temperature_c_night']})
                    annual_resource=resource_cache[key]
                    configurations={k:[sum(row[k][v] for row in annual_resource['monthly_configurations'] if row['month'] in months) for v in range(3)] for k in ('heat_kwh_th_m2','electricity_kwh_m2','fresh_makeup_m3_m2')}
                    resource={k:{'low':min(values),'central':values[1],'high':max(values)} for k,values in configurations.items()}
                    resource['monthly']=[row for row in annual_resource['monthly'] if row['month'] in months]
                    resource['daily']=annual_resource['daily']
                    option={'id':f'{crop["crop_id"]}:{m}:{season}', 'crop_id':crop['crop_id'],'name':crop['name'],
                            'method':m,'season':season,'active_months':months,'cycles':capacity['complete_cycles'],
                            'yield_kg_m2':capacity['yield_kg']['central'],
                            'yield_range_kg_m2':capacity['yield_kg'],
                            'heat_kwh_th_m2':resource['heat_kwh_th_m2']['central'],
                            'electricity_kwh_m2':resource['electricity_kwh_m2']['central'],
                            'water_monthly_m3_m2':[0.]*12,
                            'water_active_day_m3_m2':next(row['fresh_makeup_m3_m2'] for row in resource['daily'] if int(row['date'][5:7]) in months),
                            'resource_configurations':configurations,
                            'resource_ranges':{key:resource[key] for key in ('heat_kwh_th_m2','electricity_kwh_m2','fresh_makeup_m3_m2')},
                            'source_ids':crop['source_ids'],'classification':'MODELED_ENGINEERING_REQUIREMENT / POLAR_YIELD_ANALOGUE'}
                    components=('lighting_kwh_m2','pumping_kwh_m2','fans_kwh_m2','dehumidification_kwh_m2','cooling_kwh_m2','heat_kwh_th_m2')
                    option['energy_components_monthly']=[{'month':r['month'],**{k:r[k]['central'] for k in components}} for r in annual_resource['monthly'] if r['month'] in months]
                    active_days=[r for r in annual_resource['daily'] if int(r['date'][5:7]) in months]
                    option['electricity_peak_bound_kw_m2']=max(r['peak_electricity_kw_m2'] for r in active_days)
                    option['heat_peak_bound_kw_th_m2']=max(r['peak_heat_kw_th_m2'] for r in active_days)
                    for monthly in resource['monthly']:
                        option['water_monthly_m3_m2'][monthly['month']-1]=monthly['fresh_makeup_m3_m2']['central']
                    options.append(option)
        trajectories[model]={'options':options}
    package={'context':context,'candidates':candidates,'trajectories':trajectories}
    cache_path.parent.mkdir(parents=True,exist_ok=True)
    from .provenance import immutable_write
    immutable_write(cache_path,canonical(package).encode())
    return package


@lru_cache(maxsize=128)
def _inflows(site,horizon,scenario,model,climate_hash,roof_m2,efficiency,target_year=None):
    frame=load_climate_frame(site,horizon,scenario,model,target_year)
    balance=roof_storage_balance(frame.to_dict('records'),[0.]*len(frame),roof_m2=roof_m2,
                                 storage_m3=0.,collection_efficiency=efficiency)
    result=[0.]*12
    for row in balance['climatology_monthly']:
        result[row['month']-1]=row['captured_m3']
    return result


def _hashes():
    return {name:digest((ROOT/path).read_bytes()) for name,path in {
        'resources':'data/north/resource_evidence.json','crops':'data/north/crop_evidence_v2.json',
        'ground':'data/north/ground_evidence.json','resource_code':'backend/north_resources.py',
        'agronomic_envelopes':'data/auto_baseline_parameters.json',
        'planning_code':'backend/north_planning.py','candidate_code':'backend/north_candidates.py',
        'climate_code':'backend/north_climate.py',
        'infrastructure_code':'backend/north_infrastructure.py',
        'composition':'data/north/food_composition.json','purpose_code':'backend/north_production_purpose.py'}.items()}


def _engine(request, options, inflow, treatment):
    return {'options':[deepcopy(o) for o in options if o['crop_id'] not in request.disabled_crops and o['method'] not in request.disabled_methods],
            'area_m2':request.area_m2,'inflow_m3':inflow,'storage_m3':request.area_m2*request.storage_m3_per_m2,
            'freshwater_m3':request.freshwater_m3,'desalination':request.desalination and treatment['status']=='CONDITIONAL',
            'ro_kwh_m3':treatment['specific_energy_kwh_m3']['central'],'heat_cop':request.heat_cop,
            'ro_heat_kwh_th_m3':treatment['conditioning_heat_kwh_th_m3']['central'],
            'energy_limit_kwh':request.energy_limit_kwh,'objective':request.objective,'production_retention':request.production_retention,
            'minimum_crop_share':request.minimum_crop_share,'production_purpose':request.production_purpose}


def _case_change(base,case,area):
    from .north_field import pattern_changes
    changes=pattern_changes(base,case)
    bt,ct=base.get('totals',{}),case.get('totals',{})
    ratio=abs(ct.get('equivalent_electricity_kwh',0)-bt.get('equivalent_electricity_kwh',0))/max(bt.get('equivalent_electricity_kwh',0),1)
    source=abs(ct.get('desalinated_m3',0)-bt.get('desalinated_m3',0))
    production=abs(ct.get('production_kg',0)-bt.get('production_kg',0))/max(bt.get('production_kg',0),1)
    pattern_changed=changes['area_reallocated_m2']>max(.01,area*.001) or case['status']!=base['status']
    resource_changed=ratio>.05 or source/max(bt.get('water_m3',0),.001)>.05 or production>.05
    return {'status':'SENSITIVE' if pattern_changed or resource_changed else 'ROBUST', 'pattern_changed':pattern_changed,'area_reallocated_m2':changes['area_reallocated_m2'],
            'energy_change_pct':100*ratio,'production_change_pct':100*production,'source_change_m3':source,'plan':case}


def plan_north(request:NorthRequest, with_sensitivity=True):
    hashes=_hashes(); context=get_climate_context(request.site_id,request.horizon_id,request.scenario_id,request.target_year)
    package=_coefficient_package(request.site_id,request.horizon_id,request.scenario_id,context['manifest_sha256'],canonical(hashes),hashes['crops'],request.target_year)
    models=[m['model'] for m in context['models']]
    options=_average_options([package['trajectories'][m]['options'] for m in models])
    inflows={m:_inflows(request.site_id,request.horizon_id,request.scenario_id,m,context['manifest_sha256'],request.area_m2*request.roof_ratio,request.collection_efficiency,request.target_year) for m in models}
    inflow=[mean(inflows[m][month] for m in models) for month in range(12)]
    treatment=ro_treatment(request.salinity_g_kg,request.source_temperature_c,recovery=request.recovery)
    engine=_engine(request,options,inflow,treatment)
    plan=solve_pattern(**engine)
    sensitivity=[]; cases=[]
    if with_sensitivity and plan.get('totals'):
        def check(id,name,engines,measurable,range_label):
            runs=[_case_change(plan,solve_pattern(**e),request.area_m2) for e in engines]
            cases.extend(r['plan'] for r in runs)
            worst=max(runs,key=lambda r:(r['status']=='SENSITIVE',r['area_reallocated_m2'],r['energy_change_pct']))
            sensitivity.append({'id':id,'name':name,'status':worst['status'],'tase_measurable':measurable,
                'range':range_label,'area_reallocated_m2':worst['area_reallocated_m2'],
                'energy_change_pct':max(r['energy_change_pct'] for r in runs),
                'production_change_pct':max(r['production_change_pct'] for r in runs),
                'effect':f"{range_label} · sınananlarda en çok {max(r['area_reallocated_m2'] for r in runs):.2f} m² alan, %{max(r['production_change_pct'] for r in runs):.1f} hasat, %{max(r['energy_change_pct'] for r in runs):.2f} elektrik eşdeğeri ve {max(r['source_change_m3'] for r in runs):.2f} m³ arıtılmış su farkı.",
                'source_allocation_delta_m3':max(r['source_change_m3'] for r in runs)})
        check('climate','İklim verisi',[_engine(request,package['trajectories'][m]['options'],inflows[m],treatment) for m in models],False,f'{len(models)} ayrı iklim modeli' if len(models)>1 else 'Tek yeniden analiz; modeller arası belirsizlik sınanmadı')
        for key,name,bounds,measurable in [('salinity','Deniz kaynak tuzluluğu',(25.,37.),True),('temperature','Deniz kaynak sıcaklığı',(-1.,8.),True)]:
            variants=[]
            for value in bounds:
                e=deepcopy(engine)
                ro=ro_treatment(value if key=='salinity' else request.salinity_g_kg,value if key=='temperature' else request.source_temperature_c,recovery=request.recovery)
                e['ro_kwh_m3']=ro['specific_energy_kwh_m3']['central'];variants.append(e)
                e['ro_heat_kwh_th_m3']=ro['conditioning_heat_kwh_th_m3']['central']
                e['desalination']=request.desalination and ro['status']=='CONDITIONAL'
            check(key,name,variants,measurable,f"Kaynak senaryosu {bounds[0]}–{bounds[1]} {'g/kg' if key=='salinity' else '°C'}; yerel ölçüm değil")
        variants=[]
        for bound in ('low','high'):
            e=deepcopy(engine)
            for o in e['options']:o['yield_kg_m2']=o['yield_range_kg_m2'][bound]
            variants.append(e)
        check('yield','Aktarılan ürün verimi',variants,False,'EDEN ISS gözlenen min–maks; güven aralığı değil')
        variants=[]
        for config in (0,2):
            e=deepcopy(engine)
            for o in e['options']:
                for key in ('heat_kwh_th_m2','electricity_kwh_m2'):o[key]=o['resource_configurations'][key][config]
                central=o['resource_ranges']['fresh_makeup_m3_m2']['central']
                ratio=o['resource_configurations']['fresh_makeup_m3_m2'][config]/central if central else 1.
                o['water_monthly_m3_m2']=[v*ratio for v in o['water_monthly_m3_m2']]
            variants.append(e)
        check('engineering','Yapı / kontrollü su-enerji parametreleri',variants,False,'Kaynaklı fizik ve açık mühendislik aralıkları')
        variants=[]
        for factor in (.5,1.5):
            e=deepcopy(engine);e['inflow_m3']=[v*factor for v in inflow];variants.append(e)
        check('capture','Toplama / kullanılabilir yağış',variants,False,'Toplanabilir su ×0,5–1,5; mühendislik stres testi')
        sensitivity.extend([
            {'id':'freshwater','name':'Mevsimsel karasal tatlı su tahsisi','status':'UNRESOLVED','tase_measurable':False,
             'effect':'Varsayılan tahsis 0 bir koruma politikasıdır. Isdammen hacmi tarımsal tahsis sayılmaz; havza, depolama, diğer kullanımlar ve altyapı gerekir.'},
            {'id':'ground','name':'Parsel toprağı / permafrost / yapı zemini','status':'UNRESOLVED','tase_measurable':False,
             'effect':'Açık tarla planına alan verilmedi. MOSJ çevresel gözlemi, parsel uygunluğu veya geleceğin zemin onayı değildir.'},
            {'id':'chemistry','name':'Kaynak suyu kimyası / ön arıtma','status':'UNRESOLVED','tase_measurable':True,
             'effect':'İzinli fiziksel örnek ve uzman onaylı panel gerekir. İyonlar, kirlenme ve membran uyumu yalnız tuzlulukla çözülmez.'}])
        sensitivity.sort(key=lambda r:({'SENSITIVE':0,'ROBUST':1,'UNRESOLVED':2}[r['status']],-r.get('area_reallocated_m2',0),-r.get('energy_change_pct',0)))
        field_links={
            'temperature':('Açık kaynak sıcaklığı senaryosu; yerel model profili henüz içe alınmadı.','Kalibre C/T/p profili, UTC/konum ve eşleşmiş model beklentisi','RO geçirgenliği, basınç, elektrik ve soğuk su koşullandırma ısısı'),
            'salinity':('Açık kütlesel tuzluluk senaryosu; yerel gelecek dağılımı ölçülmüş değil.','Kalibre iletkenlik/sıcaklık/basınç + tanımlı tuzluluk dönüşümü','RO ozmotik basıncı, geri kazanım sınırı, arıtma elektrik gereği'),
            'chemistry':('Sadece bulk tuzluluk modeli; ayrıntılı kaynak kimyası yok.','İzinli fiziksel numune; uzman/laboratuvar onaylı hedef panel','Ön arıtma, iyon giderimi, membran uyumu ve koşullandırılmış üretim testi')}
        for row in sensitivity:
            evidence,method,link=field_links.get(row['id'],('Kaynak ve hesap ayrıntıları kanıt kaydında.','PWN doğrudan ölçmez; ilgili iklim/havza/zemin/tesis veya üretim verisi gerekir.','Aday uygunluğu, üretim miktarı veya kaynak sınırı'))
            row.update(current_evidence=evidence,measurement_method=method,expected_decision_link=link)
    totals=plan.get('totals',{})
    reliability=[]; storage_records=[]
    if totals:
        for model in models:
            frame=load_climate_frame(request.site_id,request.horizon_id,request.scenario_id,model,request.target_year)
            demand=[sum(a['area_m2']*a['water_active_day_m3_m2'] for a in plan['allocations'] if day.month in a['active_months']) for day in frame.date]
            replay=roof_storage_balance(frame.to_dict('records'),demand,roof_m2=request.area_m2*request.roof_ratio,
                                       storage_m3=request.area_m2*request.storage_m3_per_m2,collection_efficiency=request.collection_efficiency)
            byyear={}
            storage_records.append({'model':model,'capture':[r['captured_m3'] for r in replay['daily']], 'demand':demand,'dates':[r['date'] for r in replay['daily']]})
            for row in replay['daily']:
                year=int(row['date'][:4]);byyear.setdefault(year,0.);byyear[year]+=row['deficit_m3']
            reliability.append({'model':model,'topup_m3_per_year':{'min':min(byyear.values()),'mean':mean(byyear.values()),'max':max(byyear.values())},
                                'maximum_daily_topup_m3':max(row['deficit_m3'] for row in replay['daily']),
                                'days_with_topup':sum(row['deficit_m3']>1e-8 for row in replay['daily']),
                                'monthly':replay['climatology_monthly'],
                                'modeled_peak_storage_m3':max(row['storage_m3'] for row in replay['daily']),
                                'worst_topup_year':max(byyear,key=byyear.get)})
    valid_cases=[r for r in [plan,*cases] if r.get('totals') and r['status']!='infeasible']
    ranges={key:{'min':min(r['totals'][key] for r in valid_cases),'max':max(r['totals'][key] for r in valid_cases)}
            for key in ('production_kg','water_m3','equivalent_electricity_kwh')} if valid_cases else {}
    reasons=[f"Açık çeşitlilik güvencesiyle { {'balanced':'hasat ve su–enerji dengesi','water':'su önceliği','energy':'enerji önceliği'}[request.objective] } politikası uygulandı; alanlar üretim ve kaynak tüketimleriyle hesaplandı.",
             'Yerel arazi doğrulanana kadar yalıtılmış kök ortamı ve kontrollü üretim seçenekleri karşılaştırıldı.',
             f"Depolanan yağış {totals.get('stored_water_m3',0):.1f} m³ karşılıyor; kalan kaynak ihtiyacı ve arıtma enerjisi aynı dengede hesaplandı."]
    method_comparison=None
    selected_methods={a['method'] for a in plan.get('allocations',[])}
    if 'hydroponics' in selected_methods and 'greenhouse' not in request.disabled_methods:
        alternate=deepcopy(engine);alternate['options']=[o for o in alternate['options'] if o['method']=='greenhouse']
        alternate_plan=solve_pattern(**alternate)
        same_outputs=all(abs(alternate_plan.get('crop_outputs_kg',{}).get(crop,0)-quantity)<.001 for crop,quantity in plan.get('crop_outputs_kg',{}).items())
        if alternate_plan.get('totals') and alternate_plan['status']!='infeasible' and same_outputs:
            old=alternate_plan['totals']['equivalent_electricity_kwh'];new=totals['equivalent_electricity_kwh']
            if old > 0 and (old-new)/old >= .0005:
                reasons[0]=f"Seçilen yöntem dağılımı, aynı ürün miktarlarıyla yalnız sera seçeneğine göre %{100*(old-new)/old:.1f} daha az elektrik eşdeğeri gerektiriyor."
            method_comparison={'alternative':'greenhouse_only','same_crop_quantities':True,'plan':alternate_plan}
    if treatment['status']!='CONDITIONAL':
        reasons[-1]='Arıtma basınç sınırı aşıldığı için deniz kaynağı elendi; yalnız kalan suyla hesaplandı.'
    if not request.desalination and any(r['topup_m3_per_year']['max']>request.freshwater_m3+1e-6 for r in reliability):
        reasons[-1]='Ortalama ay dengesi günlük kurak dönemleri karşılamıyor: ek depolama veya yedek kaynak olmadan plan uygulanamaz.'
    evidence=[
        {'id':'climate','name':'Gelecek iklimi','status':'MODELED / SOURCED','source':'NASA NEX-GDDP-CMIP6 v2.0','url':'https://www.nccs.nasa.gov/services/data-collections/land-based-products/nex-gddp-cmip6',
         'detail':f"{context['period'][0]}–{context['period'][1]}, 3 GCM, günlük Tmin/Tmax/yağış/kısa dalga. 0,25° hücre; yerel tarla hava ölçümü değil. Tarihsel yerel ERA5-Land kontrolü projeksiyona otomatik düzeltme olarak uygulanmadı."},
        {'id':'yield','name':'Üretim miktarı','status':'SOURCED / TRANSFERRED','source':'EDEN ISS 2018 / Zabel 2020','url':'https://doi.org/10.3389/fpls.2020.00656',
         'detail':'6 ürünün alan ve tam çevrim başına verimi. 21/19 °C, ışık/nem ve CO₂ 1000 ppm deney koşulları. Yerel hasat değil; fide, koridor, çevrim arası kayıp ve CO₂ tedariki ayrıca gerekir.'},
        {'id':'ground','name':'Zemin ve permafrost','status':'SOURCED / SITE UNKNOWN','source':'MOSJ Janssonhaugen','url':'https://mosj.no/en/indikator/climate/land/permafrost/',
         'detail':'1998–2024 gerçek aktif tabaka serisi; 2024:218 cm. Yaklaşık 20 km uzaktaki nokta, parsel tarım/toprak onayı değil. SoilGrids nokta sorgusu null; ESA CCI metadata incelendi, raster yerel değer çekilmedi.'},
        {'id':'water','name':'Karasal su güvenliği','status':'UNKNOWN / POLICY','source':'SINTEF / UNIS Isdammen araştırması','url':'https://www.sintef.no/en/latest-news/2026/securing-the-water-supply-in-longyearbyen-is-critical/',
         'detail':'Gerçek tarımsal tahsis doğrulanmadı. Başlangıçta yerel içme suyundan çekim yok politikası; çatı ve depo ölçüleri açık normalize tasarım tercihi.'},
        {'id':'resources','name':'Su ve enerji gereksinimi','status':'MODELED / ASSUMED','source':'Fiziksel denklemler ve kaynak aralıkları','url':'',
         'detail':'Bina ısı kaybı, ışık açığı, Penman–Monteith kontrollü ortam su dengesi, yoğuşma, günlük yağış/kar ve RO kaynak suyu hesabı. Mühendislik parametreleri Arktik işletme kalibrasyonu değildir.'},
        {'id':'field','name':'Yeni saha kanıtı','status':'FIELD-MEASURABLE / PLANNED','source':'PRE / POST doğrulama protokolü','url':'',
         'detail':'Henüz kendi Arktik ölçümümüz yok. PWN günümüz C/T/p profilini sınar. Fiziksel örnek ve kimya paneli uzman/sefer/laboratuvar iznine bağlı.'}]
    if request.horizon_id=='recent' and request.target_year is None:
        evidence[0].update(name='Yakın dönem iklimi',status='SOURCED / REANALYSIS',source='ERA5 / Open-Meteo',url='https://open-meteo.com/en/docs/historical-weather-api',
            detail='2015–2025, günlük sıcaklık/yağış/radyasyon yeniden analizi. Yerinde ölçülmüş tarla veya gerçek ekiliş değildir; NASA geleceğiyle farklar veri ailesi/hücre farkını da içerir.')
    if request.target_year is not None:
        evidence[0].update(name=f'{request.target_year} iklim senaryosu',
            detail=f'{request.target_year} yılının 3 ayrı kaynak modelindeki günlük dizisi kullanıldı; yıllar arasında oranlama yapılmadı. Gerçekte o yıl yaşanacak hava tahmini veya uzman onayı değildir. Başlangıç karı ve depo suyu 0 kabul edilmiştir; önceki yıl kar devri bu tek yıllık taramada temsil edilmez.')
    return {'classification':'NORMALIZED_CONDITIONAL_PRODUCTION_PLAN','request':request.model_dump(),'plan':plan,
            'climate':context,'candidates':package['candidates'],'treatment':treatment,'engine_inputs':engine,
            'infrastructure':{'water':storage_design(storage_records,request.area_m2*request.storage_m3_per_m2),
                              'energy':energy_supply(plan,options,request.heat_cop,request.energy_limit_kwh,request.available_power_kw)},
            'sensitivity':sensitivity,'ranges':ranges,'range_infeasible_cases':sum(r['status']=='infeasible' for r in cases),'reasons':reasons,'evidence':evidence,'daily_reliability':reliability,'method_comparison':method_comparison,
            'basis':{'cultivated_area_m2':request.area_m2,'roof_area_m2':request.area_m2*request.roof_ratio,
                     'storage_m3':request.area_m2*request.storage_m3_per_m2,'local_farm_capacity_claimed':False,
                     'freshwater_policy':'No agricultural allocation assumed from municipal water; zero is a policy, not a water-volume measurement.'},
            'provenance':{'engine_version':VERSION,'climate_manifest_sha256':context['manifest_sha256'],
                          'evidence_sha256':hashes,'sources':package['candidates']['sources'],
                          'resource_evidence_path':'data/north/resource_evidence.json',
                          'uncertainty':'Deterministic bounded reruns; no probability/confidence intervals.',
                          'sensitivity_threshold':'SENSITIVE if area reallocation > max(0.01 m²,0.1% area), feasibility changes, harvest or equivalent energy >5%, or desalinated source change >5% total water. Explicit reporting thresholds, not significance tests.',
                          'temperature_approximation':'21/19°C day/night targets, 17h flat light schedule preserving published ramp-integrated DLI. Daily outdoor weather reconstructed hourly, not hourly observation.',
                          'normalization':'Single growing layer, 100 m² default; cultivated area != complete facility footprint.',
                          'season_policy':'May–September / March–October / annual engineering schedules, not projected natural growing seasons.',
                          'capacity_policy':'No local energy/land permit/water right assumed. Optional explicit resource ceilings only.'}}
