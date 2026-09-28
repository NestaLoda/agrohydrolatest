"""One native-capacity LP for regional crop and future production-system patterns.

Open-field x is hectares; greenhouse/hydroponics x is growing-surface m².
No cross-crop nutrition equivalence is inferred from kilograms.
"""
import json
from datetime import timedelta
import numpy as np
import pandas as pd
from scipy.optimize import linprog
from .provenance import ROOT, digest
from .repository import load_verified_climate, load_manifest, north_context
from .science import water_balance, treatment_energy, temperature_scenario_et0, FAO56_HARGREAVES, TEMPERATURE_SCENARIO_LIMITATIONS
from .planning_contracts import SimulationRequest, CropPlanInput

METHODS={'open_field':'Açık tarla','greenhouse':'Sera','hydroponics':'Hidroponik'}
SOURCES={'freshwater':'Yerel tatlı su','stored_water':'Depolanmış yağmur/erime suyu','reuse':'Yeniden kullanım','desalinated_seawater':'Arıtılmış deniz suyu'}
STARTS={'wheat':'2024-11-01','barley':'2025-03-15','maize_grain':'2025-04-15','sugar_beet':'2025-05-01','cotton':'2025-04-15','sunflower':'2025-04-15','rice':'2025-05-01','potato':'2025-05-01','lettuce':'2025-04-01'}

def read_agriculture(name):
    path=ROOT/'data/agriculture'/name
    if not path.exists():raise ValueError(f'Tarımsal veri paketi henüz hazır değil: {name}')
    raw=path.read_bytes()
    manifest=json.loads((ROOT/'data/agriculture/manifest.json').read_text(encoding='utf-8'))
    if digest(raw)!=manifest['files'][name]['sha256']:raise ValueError('Tarımsal türetilmiş kayıt incelenmiş sürüm hash kaydıyla uyuşmuyor; kullanıcı değişikliklerini senaryoda yapın.')
    return json.loads(raw.decode('utf-8-sig'))

def catalog():return {c['crop_id']:c for c in read_agriculture('crops.json')['crops']}

def baseline_region(region_id):
    if region_id=='longyearbyen':return {'region_id':region_id,'name':'Kuzey aday saha · Longyearbyen veri bağlamı','classification':'NO_CURRENT_AGRICULTURAL_BASELINE','crops':[], 'sources':[], 'limitations':['Mevcut tarımsal desen tanımlanmadı; açık tarla uygunluğu doğrulanmış değil.']}
    regions=read_agriculture('region_baselines.json')['regions']
    region=next((r for r in regions if r['region_id']==region_id),None)
    if region is None:raise ValueError('Kayıtlı bölgesel ürün deseni bulunamadı.')
    for source in region.get('sources',[]):
        if not source.get('local_path') or not source.get('sha256'):raise ValueError('Tarım kaynağının ham dosya/hash kaydı eksik.')
        path=(ROOT/source['local_path']).resolve()
        if not path.is_relative_to((ROOT/'data').resolve()):raise ValueError('Tarım kaynağı data içinde olmalı.')
        if digest(path.read_bytes())!=source['sha256']:raise ValueError('Tarım kaynağının bütünlüğü bozuldu.')
    return region

def stages(crop,knowledge):
    days=crop.stage_days or knowledge.get('growing_period',{}).get('stage_days')
    if not days or len(days)!=4 or min(days)<1 or sum(days)>366:raise ValueError('Kaynaklı veya kullanıcı tarafından belirtilmiş dört gelişim aşaması gerekli.')
    return days

def crop_water(r,crop,knowledge,frame):
    days=stages(crop,knowledge)
    end=crop.season_start+timedelta(days=sum(days)-1)
    base={'crop_id':crop.crop_id,'season_start':crop.season_start.isoformat(),'season_end':end.isoformat(),'stage_days':days,
          'classification':'SIMULATION_EXPLANATORY','irrigation_efficiency':r.irrigation_efficiency,
          'temperature_delta_c':r.temperature_delta_c,
          'temperature_scenario':{'temperature_delta_c':r.temperature_delta_c,'applied':False,'method':'NOT_APPLIED_NO_CLIMATE_WATER_CALCULATION'}}
    if crop.manual_net_irrigation_mm is not None:
        return {**base,'status':'conditional','net_irrigation_mm':crop.manual_net_irrigation_mm,'gross_water_m3_ha':crop.manual_net_irrigation_mm*10/r.irrigation_efficiency,
          'etc_mm':None,'source':'USER_SCENARIO','reason':'Dönemsel net sulama gereksinimi kullanıcı girdisi; iklim modelinden türetilmedi. Sıcaklık, yağış ve ET0 değişimi bu manuel net sulamayı değiştirmez.',
          'temperature_scenario':{'temperature_delta_c':r.temperature_delta_c,'applied':False,'method':'MANUAL_NET_IRRIGATION_NOT_CLIMATE_DERIVED'}}
    if crop.crop_id=='rice':return {**base,'status':'insufficient_data','net_irrigation_mm':None,'gross_water_m3_ha':None,'etc_mm':None,'source':'FAO56','reason':'Çeltikte ETc dışındaki tava/derine sızma/tesviye suyu eksik. Toplam net gereksinim senaryo olarak belirtilmeli.'}
    if r.mode=='north':return {**base,'status':'insufficient_data','net_irrigation_mm':None,'gross_water_m3_ha':None,'etc_mm':None,'source':'INSUFFICIENT_DATA','reason':'Kuzey gelecek paketinde ET0/kar-erime yok. Hava sıcaklığı veya tarihsel yağıştan gelecek sulama suyu uydurulmaz; net gereksinim senaryosu gerekli.'}
    d=frame[(frame.site_id==r.region_id)&(frame.date>=pd.Timestamp(crop.season_start))&(frame.date<=pd.Timestamp(end))]
    if len(d)!=sum(days):raise ValueError(f'{crop.crop_id}: seçilen takvim için eksiksiz kaynak hava serisi bulunamadı.')
    kc=knowledge['kc']; initial,mid,last=kc['initial'],kc['mid'],kc['end']
    if any(v is None for v in [initial,mid,last]):raise ValueError(f'{crop.crop_id}: Kc parametresi eksik.')
    curve=np.r_[np.full(days[0],initial),np.linspace(initial,mid,days[1]),np.full(days[2],mid),np.linspace(mid,last,days[3])]
    try:
        et0,temperature_meta=temperature_scenario_et0(d.et0_mm.to_numpy(),d.get('tmin_c'),d.get('tmax_c'),r.temperature_delta_c)
    except ValueError as exc:
        return {**base,'status':'insufficient_data','net_irrigation_mm':None,'gross_water_m3_ha':None,'etc_mm':None,'source':'DATA_NEEDED','reason':str(exc),
            'temperature_scenario':{**base['temperature_scenario'],'status':'DATA_NEEDED','source_url':FAO56_HARGREAVES,'limitations':TEMPERATURE_SCENARIO_LIMITATIONS}}
    wb=water_balance(d.precipitation_mm.to_numpy()*r.rainfall_factor,et0*r.et0_factor,curve,r.soil_capacity_mm,r.initial_storage_mm)
    t=wb['totals']; net=t['deficit_mm']
    return {**base,'status':'conditional','net_irrigation_mm':net,'gross_water_m3_ha':net*10/r.irrigation_efficiency,'etc_mm':t['potential_et_mm'],
        'rainfall_mm':t['precipitation_mm'],'retained_rainfall_mm':t['precipitation_mm']-t['drainage_mm'],
        'initial_storage_mm':t['initial_storage_mm'],'final_storage_mm':t['final_storage_mm'],'drainage_mm':t['drainage_mm'],
        'source':'ERA5 + FAO56 + USER_SCENARIO','dataset_id':str(d.dataset_id.iloc[0]),'kc_source':kc.get('source_url'),
        'temperature_scenario':{**temperature_meta,'additional_manual_et0_factor':r.et0_factor},
        'reason':'ETc=Kc×ET0; yağış/depo sonrası karşılanmamış ET, zamanında tamamlama varsayımıyla net sulama gereksinimi. Randımanla brüt çekime çevrilir; verim-su tepki modeli değil.'
          + (' Sıcaklık farkı, FAO56 Denklem 52 sıcaklık-terimi oranıyla kaynak ET0 üzerine uygulanmış kalibre edilmemiş duyarlılık senaryosudur; tam Penman–Monteith yeniden hesabı değildir.' if r.temperature_delta_c else '')}

def _crop_water_rows(r,knowledge,frame):
    rows=[]
    for c in r.crops:
        try:rows.append(crop_water(r,c,knowledge[c.crop_id],frame))
        except (KeyError,ValueError) as exc:rows.append({'crop_id':c.crop_id,'status':'insufficient_data','gross_water_m3_ha':None,'net_irrigation_mm':None,'etc_mm':None,'reason':str(exc)})
    return rows

def northern_candidates(knowledge):
    from .north_evidence import load_north_evidence
    review=load_north_evidence();rows=[]
    for candidate in review['candidates']:
        compatible=[m for m in candidate['methods'] if m in knowledge.get(candidate['id'],{}).get('compatible_methods',[])]
        sources=[sid for sid in candidate.get('source_ids',[]) if sid in review['sources']]
        reasons=[]
        if not candidate.get('default_candidate'):reasons.append('Araştırma değerlendirmesinde ilk portföy adayı değil.')
        if candidate['id'] not in knowledge:reasons.append('Ortak ürün kataloğunda hesap parametreleri yok.')
        if not compatible:reasons.append('Kaynak incelemesi ile katalog arasında desteklenen yöntem yok.')
        if not sources:reasons.append('İnceleme kaydında doğrulanmış kaynak kimliği yok.')
        retained=not reasons
        rows.append({**candidate,'retained':retained,'compatible_methods':compatible,'verified_source_ids':sources,
          'readiness':'locally_parameterized' if candidate.get('optimizer_parameter_ready') and candidate.get('locally_validated') else 'DATA_NEEDED',
          'exclusion_reasons':reasons})
    return {'candidates':rows,'selected_ids':[c['id'] for c in rows if c['retained']],
      'integrity':review['integrity'],'policy':'Kaynaklı araştırma adayı + katalog/yöntem kesişimi. Yerel iklim/zemin/su uygunluğu doğrulaması değildir.'}

def planning_context(region_id='konya'):
    knowledge=catalog();region=baseline_region(region_id);north=region_id=='longyearbyen'
    candidate_evidence=northern_candidates(knowledge) if north else None
    crops=[]
    if north:
        # Numeric example is explicitly a user scenario, not a locally calibrated forecast.
        example_parameters={'barley':(3000,3000),'potato':(10000,20000),'lettuce':(1000,None)}
        for cid in candidate_evidence['selected_ids']:
            target,yield_=example_parameters.get(cid,(1,None))
            crops.append(CropPlanInput(crop_id=cid,target_production_kg=target,min_production_kg=target,
              yield_kg_ha=yield_,season_start='2035-05-01',methods=['hydroponics'] if cid=='lettuce' else ['open_field'],
              controlled_yield_kg_m2=3 if cid=='lettuce' else None,controlled_water_m3_kg=.02 if cid=='lettuce' else None,
              controlled_energy_kwh_kg=25 if cid=='lettuce' else None,field_energy_kwh_ha=500 if cid!='lettuce' else None,
              manual_net_irrigation_mm={'barley':150,'potato':250}.get(cid)))
    else:
        for item in region['crops']:
            cid=item['crop_id']
            if cid not in knowledge:continue
            y=item.get('yield_kg_ha'); target=(y or 1)*item['area_ha']
            crops.append(CropPlanInput(crop_id=cid,current_area_ha=item['area_ha'],yield_kg_ha=y,season_start=STARTS.get(cid,'2025-04-01'),
                target_production_kg=max(1,target),min_production_kg=target*.5 if y else 0,climate_suitable=True,soil_suitable=True))
    if not crops:raise ValueError('Ortak ürün veritabanına eşleşen bölgesel ürün yok.')
    area=sum(c.current_area_ha for c in crops) if not north else 3
    req=SimulationRequest(mode='north' if north else 'turkiye',region_id=region_id,land_area_ha=area,crops=crops,
        period_label='2030–2049 · saha öncesi kapasite senaryosu' if north else f"{region.get('year','?')} tarımsal desen / 2024–2025 tamamlanmış hava referansı",
        climate_basis='user_scenario' if north else 'era5_2024_2025',min_cultivated_fraction=0,climate_context_id='ec_earth_2030_2049' if north else None,
        climate_scenario_label='Gelecek sulama/yield/enerji kullanıcı varsayımı; iklim modeli ayrı kanıt' if north else 'ERA5 referansı + FAO örnek takvim',
        energy_budget_kwh=40000 if north else None,hydroponics_capacity_m2=400 if north else 0,
        water_sources=[{'source_id':'freshwater','capacity_m3':2000 if north else 0,'quality_suitable':True,'energy_kwh_m3':0},
          {'source_id':'stored_water','capacity_m3':500 if north else 0,'enabled':north,'quality_suitable':True,'energy_kwh_m3':0},
          {'source_id':'reuse','capacity_m3':0,'enabled':False,'quality_suitable':None,'energy_kwh_m3':None},
          {'source_id':'desalinated_seawater','capacity_m3':2000 if north else 0,'enabled':north,'quality_suitable':True,'energy_kwh_m3':None}])
    if not north:
        frame=load_verified_climate(recent=True);wr=_crop_water_rows(req,knowledge,frame)
        demand=sum((w.get('gross_water_m3_ha') or 0)*c.current_area_ha for w,c in zip(wr,crops))
        req.water_sources[0].capacity_m3=demand
        req.planning_objective='regional_water'
    example=req.model_copy(deep=True)
    if north:
        for c in example.crops:
            c.climate_suitable=True;c.soil_suitable=True
        example.overrides=['USER_SCENARIO: açık tarla iklim/zemin uygun varsayıldı; Longyearbyen uygunluğu kanıtlanmadı.','USER_SCENARIO: arpa/patates verim, net sulama ve enerji; hidroponik tek dönem kapasitesi.']
    if north:
        req.planning_objective='capacity'
        req.north_input_policy='source_resolved'
        req.quantity_basis='capacity'
        for c in req.crops:
            c.target_production_kg=1;c.min_production_kg=0
            c.yield_kg_ha=None;c.manual_net_irrigation_mm=None;c.field_energy_kwh_ha=None
            c.controlled_yield_kg_m2=None;c.controlled_water_m3_kg=None;c.controlled_energy_kwh_kg=None
    return {'candidate_evidence':candidate_evidence,'region':region,'crop_catalog':list(knowledge.values()),'default_scenario':req.model_dump(mode='json'),'illustrative_scenario':example.model_dump(mode='json') if north else None,
       'baseline_analysis':baseline_analysis(req,knowledge,region),
       'climate_context':north_context() if north else {'period':'2024–2025','kind':'MODEL_REANALYSIS','agricultural_year':region.get('year')},
       'limitations':['İl tarımsal deseni ile nokta reanalizi aynı coğrafi ölçek değildir; bu gösterim yerel validasyon değildir.',
        'Takvim/Kc ve yerel toprak/uygunluk varsayımları düzenlenebilir; resmî üretim alanları bilimsel su tüketimi ölçümü değildir.',
        'Başlangıç su bütçesi Türkiye için mevcut desenin modellenmiş gereksinimidir; gerçek su tahsisi değildir.',
        'Ürün başına hedef ve %50 üretim tabanı tasarım senaryosudur; boş kalan alan ayrıca raporlanır, gıda/nutrition eşdeğerliği değildir.' if not north else 'Gelecek iklim göstergesi su/yield/enerji katsayısı üretmez. Çok ürünlü örnek uygun saha varsayımıyla ayrıca açılır.',
        'Başlangıç planlama kapasitesi seçilen ekilişlerin toplamından alınan kullanıcı senaryosudur; benzersiz fiziksel il arazi kapasitesi değildir.']}

def _pattern_current(r,knowledge,water_rows,official=None):
    crop_out=[];water_total=0;energy_total=0;complete=True;energy_complete=True
    for c,w in zip(r.crops,water_rows):
        ref=next((x for x in (official or []) if x['crop_id']==c.crop_id),None) if official is not None else None
        area=(ref['area_ha'] if ref else 0) if official is not None else c.current_area_ha
        y=(ref.get('yield_kg_ha') if ref else None) if official is not None else c.yield_kg_ha
        water=area*w['gross_water_m3_ha'] if w.get('gross_water_m3_ha') is not None else (0 if area==0 else None)
        energy=area*c.field_energy_kwh_ha if c.field_energy_kwh_ha is not None else (0 if area==0 else None)
        complete &= water is not None;energy_complete &= energy is not None
        water_total+=water or 0;energy_total+=energy or 0
        crop_out.append({'crop_id':c.crop_id,'name_tr':knowledge[c.crop_id]['name_tr'],'area_ha':area,'production_kg':area*y if y is not None else None,'water_m3':water})
    return {'crops':crop_out,'totals':{'open_field_area_ha':sum(c['area_ha'] for c in crop_out),'water_m3':water_total if complete else None,'energy_kwh':energy_total if energy_complete else None},
      'classification':'SIMULATION_EXPLANATORY','note':'Alan/üretim kaydı ile modellenmiş su gereksinimi ayrı kanıttır; enerji yalnız beyan edilen üretim katsayısını içerir.'}

def baseline_analysis(r,knowledge,region):
    """Describe the sourced starting pattern without calling the optimizer.

    Water is a conditional calculation, never official measured consumption.
    A northern candidate portfolio is not an existing agricultural baseline.
    """
    frame=load_verified_climate(recent=r.climate_basis=='era5_2024_2025')
    water_rows=_crop_water_rows(r,knowledge,frame)
    official=region.get('crops',[])
    current=_pattern_current(r,knowledge,water_rows,official)
    available=sum(s.capacity_m3 for s in r.water_sources if s.enabled and s.quality_suitable is True)
    if not official:
        current['crops']=[]
        current['totals'].update(water_m3=None,energy_kwh=None)
    for row in current['crops']:
        source=next(c for c in official if c['crop_id']==row['crop_id'])
        row.update(area_classification='OFFICIAL_STATISTICS',production_classification='DERIVED_FROM_OFFICIAL_STATISTICS',
                   water_classification='SIMULATION_EXPLANATORY',source_id=source.get('source_id'))
    water=current['totals']['water_m3']
    current['totals'].update(available_water_m3=available,water_deficit_m3=max(0,water-available) if water is not None else None)
    current['classification']='MIXED_EVIDENCE_BASELINE' if official else 'NO_CURRENT_AGRICULTURAL_BASELINE'
    return {'status':'baseline_only' if official else 'no_current_baseline','classification':'BASELINE_ANALYSIS',
      'current':current,'crop_water':water_rows,
      'provenance':{'official_sources':region.get('sources',[]),'climate_dataset_ids':sorted({w['dataset_id'] for w in water_rows if w.get('dataset_id')}),
        'agriculture_sha256':{name:digest((ROOT/'data/agriculture'/name).read_bytes()) for name in ['crops.json','region_baselines.json']},
        'available_water_classification':'USER_SCENARIO','optimization_performed':False},
      'limitations':['Mevcut alan/üretim kaynaklıdır; su gereksinimi ERA5, Kc, örnek takvim ve toprak/randıman varsayımlarıyla hesaplanır.',
        'Gösterilen kullanılabilir su başlangıç senaryo bütçesidir; resmî tahsis veya fiziksel ölçüm değildir.',
        'Eksik ürün su ihtiyacı toplam gereksinimi bilinmiyor bırakır; bilinen alt toplam tam toplam yerine geçmez.',
        'Önerilen desen henüz hesaplanmadı; optimizasyon yalnız Hesapla komutuyla çalıştırılır.' if official else 'Kuzey için mevcut tarımsal desen yok; aday hedefler mevcut üretim gibi gösterilmez.']}

def simulate(r:SimulationRequest):
    if r.mode=='north' and r.temperature_delta_c!=0:
        raise ValueError('Sıcaklık farkı senaryosu bu sürümde yalnız Türkiye içindir; Kuzey için desteklenmiyor.')
    original_request=r.model_copy(deep=True)
    r=r.model_copy(deep=True)
    resolution=None
    if r.mode=='north' and r.north_input_policy=='source_resolved':
        from .north_resolution import resolve_north
        r,resolution=resolve_north(r)
    regional=r.planning_objective=='regional_water'
    priority_capacity=r.quantity_basis=='capacity' and r.planning_objective in {'water_priority','energy_priority'}
    capacity_mode=r.planning_objective in {'capacity','balanced'} or priority_capacity
    if capacity_mode:
        for c in r.crops:c.min_production_kg=0
    elif r.planning_objective in {'water_priority','energy_priority'}:
        for c in r.crops:
            if c.enabled:c.min_production_kg=max(c.min_production_kg,c.target_production_kg)
    knowledge=catalog();region=baseline_region(r.region_id)
    if any(c.crop_id not in knowledge for c in r.crops):raise ValueError('Ürün kimliği kaynaklı ürün kataloğunda bulunamadı.')
    frame=load_verified_climate(recent=r.climate_basis=='era5_2024_2025')
    water_rows=_crop_water_rows(r,knowledge,frame);water_by={w['crop_id']:w for w in water_rows}
    reference=r.model_copy(update={'rainfall_factor':1.,'et0_factor':1.,'temperature_delta_c':0.})
    baseline=_pattern_current(reference,knowledge,_crop_water_rows(reference,knowledge,frame),region.get('crops',[]))
    current=_pattern_current(r,knowledge,water_rows)
    if regional:
        from .regional_scope import partial_region
        partial=partial_region(r,knowledge,water_rows,baseline,current,simulate)
        if partial is not None:return partial
    options=[];excluded=[];sec=treatment_energy(r.seawater_temperature_c)
    for crop in r.crops:
        k=knowledge[crop.crop_id];w=water_by[crop.crop_id]
        for method in crop.methods:
            reason=None; open_=method=='open_field'
            if not crop.enabled:reason='Ürün kullanıcı senaryosunda kapatıldı.'
            elif method not in k.get('compatible_methods',[]):reason='Bu ürün/yöntem için katalogda desteklenen kapsam yok.'
            elif open_ and (crop.climate_suitable is not True or crop.soil_suitable is not True):reason='Açık tarla iklim/zemin uygunluğu olumsuz veya bilinmiyor.'
            elif open_ and crop.yield_kg_ha is None:reason='Açık tarla verim girdisi eksik.'
            elif open_ and w.get('gross_water_m3_ha') is None:reason=w.get('reason','Sulama gereksinimi eksik.')
            elif not open_ and (crop.controlled_yield_kg_m2 is None or crop.controlled_water_m3_kg is None):reason='Kontrollü üretim için dönemsel kg/m² ve m³/kg girdisi eksik.'
            y=crop.yield_kg_ha if open_ else crop.controlled_yield_kg_m2
            water=w.get('gross_water_m3_ha') if open_ else (crop.controlled_water_m3_kg or 0)*(y or 0)
            prod_energy=crop.field_energy_kwh_ha if open_ else (None if crop.controlled_energy_kwh_kg is None else crop.controlled_energy_kwh_kg*(y or 0))
            for src in r.water_sources:
                cause=reason
                if not cause and (not src.enabled or src.capacity_m3<=0):cause='Su kaynağı kapalı veya kapasitesi sıfır.'
                if not cause and src.quality_suitable is not True:cause='Kaynak suyu hedef kalitesi bilinmiyor/uygun değil.'
                source_sec=src.energy_kwh_m3
                if src.source_id=='desalinated_seawater':
                    source_sec=sec['interval_kwh_m3'][1] if sec['interval_kwh_m3'] else None
                    if not cause and source_sec is None:cause='Arıtma enerji ilişkisinin 5–18°C kaynak aralığı dışında.'
                energy=None if prod_energy is None or source_sec is None else prod_energy+(water or 0)*source_sec
                if not cause and (r.energy_budget_kwh is not None or r.planning_objective=='energy_priority') and energy is None:cause='Enerji bütçesi/önceliği uygulanırken eksik enerji katsayısı sıfır sayılamaz.'
                if cause:excluded.append({'crop_id':crop.crop_id,'method':method,'source':src.source_id,'reason':cause});continue
                options.append({'crop_id':crop.crop_id,'name_tr':k['name_tr'],'method':method,'water_source':src.source_id,
                    'capacity_unit':'ha' if open_ else 'm2','yield':y,'water':water,'energy':energy,'season_start':w.get('season_start',crop.season_start.isoformat()),'season_end':w.get('season_end')})
    n=len(options); m=len(r.crops); size=n+m
    vectors=[];caps=[];metadata=[]
    def add(id,label,unit,coef,capacity,sense='max'):
        vectors.append(np.array(coef,dtype=float));caps.append(float(capacity));metadata.append({'id':id,'label':label,'unit':unit,'sense':sense})
    def vec(fn):return [float(fn(o)) for o in options]+[0.]*m
    open_v=vec(lambda o:o['method']=='open_field')
    add('land','Açık tarla alanı','ha',open_v,r.land_area_ha)
    add('min_land','En az ekilen alan','ha',[-x for x in open_v],-r.land_area_ha*r.min_cultivated_fraction,'min')
    for meth,cap in [('greenhouse',r.greenhouse_capacity_m2),('hydroponics',r.hydroponics_capacity_m2)]:
        add(meth,meth+' yetiştirme yüzeyi','m²',vec(lambda o:o['method']==meth),cap)
    for src in r.water_sources:add('water_'+src.source_id,SOURCES[src.source_id],'m³',vec(lambda o:o['water'] if o['water_source']==src.source_id else 0),src.capacity_m3 if src.enabled else 0)
    if r.energy_budget_kwh is not None:add('energy','Toplam beyan edilen enerji','kWh',vec(lambda o:o['energy'] or 0),r.energy_budget_kwh)
    normalization={c.crop_id:c.target_production_kg for c in r.crops}
    if capacity_mode:
        # Per-crop upper potential under the same shared upper resource limits;
        # lower-bound portfolio obligations do not define single-crop potential.
        resource_rows=[i for i,meta in enumerate(metadata) if meta['sense']=='max']
        resource_A=np.array([vectors[i][:n] for i in resource_rows])
        resource_b=np.array([caps[i] for i in resource_rows])
        for c in r.crops:
            value=0.
            if n and c.enabled:
                area_row=np.array([float(o['crop_id']==c.crop_id and o['method']=='open_field') for o in options])
                local_A=np.vstack([resource_A,area_row]);local_b=np.r_[resource_b,c.max_share*r.land_area_ha]
                scale=np.maximum(1,np.maximum(np.max(np.abs(local_A),axis=1),np.abs(local_b)))
                production=np.array([o['yield'] if o['crop_id']==c.crop_id else 0. for o in options])
                single=linprog(-production/max(1,float(max(production))),A_ub=local_A/scale[:,None],b_ub=local_b/scale,
                    bounds=[(0,None) if o['crop_id']==c.crop_id else (0,0) for o in options],method='highs')
                if single.success:value=max(0,float(production@single.x))
            normalization[c.crop_id]=value
            c.target_production_kg=value if value>0 else 1
    for i,c in enumerate(r.crops):
        av=vec(lambda o:o['crop_id']==c.crop_id and o['method']=='open_field')
        pv=vec(lambda o:o['yield'] if o['crop_id']==c.crop_id else 0)
        add('crop_min_area_'+c.crop_id,knowledge[c.crop_id]['name_tr']+' minimum alan','ha',[-x for x in av],-c.min_share*r.land_area_ha,'min')
        add('crop_max_area_'+c.crop_id,knowledge[c.crop_id]['name_tr']+' maksimum alan','ha',av,c.max_share*r.land_area_ha)
        add('crop_min_output_'+c.crop_id,knowledge[c.crop_id]['name_tr']+' minimum üretim','kg',[-x for x in pv],-c.min_production_kg,'min')
        achievement=[-x/c.target_production_kg for x in pv];achievement[n+i]=1
        add('target_'+c.crop_id,knowledge[c.crop_id]['name_tr']+' hedef karşılanması','oran',achievement,0)
    A=np.array(vectors); b=np.array(caps)
    bounds=[(0,None)]*n+[(0,None) if regional else (0,1)]*m
    # Row scaling protects very large provincial area/production coefficients.
    scales=np.maximum(1,np.maximum(np.max(np.abs(A),axis=1),np.abs(b)))
    weights=[c.priority if not capacity_mode or normalization[c.crop_id]>0 else 0. for c in r.crops]
    objective=np.r_[np.zeros(n),[-w for w in weights]]
    if regional:objective=-np.array(open_v)/max(1,r.land_area_ha)
    balanced_floor=None
    if (r.planning_objective=='balanced' or priority_capacity) and any(normalization.values()):
        fair_rows=[]
        for i,c in enumerate(r.crops):
            if normalization[c.crop_id]>0:
                row=np.zeros(size+1);row[n+i]=-1;row[-1]=1;fair_rows.append(row)
        fair=linprog(np.r_[np.zeros(size),-1.],A_ub=np.vstack([np.c_[A/scales[:,None],np.zeros(len(A))],fair_rows]),
            b_ub=np.r_[b/scales,np.zeros(len(fair_rows))],bounds=bounds+[(0,1)],method='highs')
        if fair.success:
            balanced_floor=float(fair.x[-1])
            required_floor=balanced_floor*(r.resource_priority_fraction if priority_capacity else 1.)
            for row in fair_rows:
                A=np.vstack([A,row[:-1]]);b=np.r_[b,-max(0,required_floor-1e-8)]
            scales=np.maximum(1,np.maximum(np.max(np.abs(A),axis=1),np.abs(b)))
    if priority_capacity:objective=np.zeros(size)
    solution=linprog(objective,A_ub=A/scales[:,None],b_ub=b/scales,bounds=bounds,method='highs')
    optimal_score=None
    stage_names=(['max_min_single_crop_capacity_fraction'] if r.planning_objective=='balanced' or priority_capacity else [])+(
        [f'preserve_{r.resource_priority_fraction:g}_of_feasible_common_fraction'] if priority_capacity else [
        'max_weighted_single_crop_capacity_fraction' if capacity_mode else 'max_capped_demand_achievement'])
    if regional:stage_names=['max_cultivated_area','min_water_at_preserved_area'][:1]
    if solution.success:
        optimal_score=-float(solution.fun)
        extra=np.array(open_v)/max(1,r.land_area_ha) if regional else np.r_[np.zeros(n),weights]
        preserve_A=A/scales[:,None] if priority_capacity else np.vstack([A/scales[:,None],-extra])
        preserve_b=b/scales if priority_capacity else np.r_[b/scales,-optimal_score+1e-8]
        water_obj=np.r_[[o['water'] for o in options],np.zeros(m)]
        energy_obj=np.r_[[o['energy'] or 0 for o in options],np.zeros(m)]
        sequence=[('min_water',water_obj)]
        if all(o['energy'] is not None for o in options):sequence.append(('min_energy',energy_obj))
        if r.planning_objective=='energy_priority':sequence=list(reversed(sequence))
        for stage,resource_obj in sequence:
            denominator=max(1,float(max(resource_obj,default=1)))
            refined=linprog(resource_obj/denominator,A_ub=preserve_A,b_ub=preserve_b,bounds=bounds,method='highs')
            if not refined.success:break
            solution=refined;stage_names.append(stage)
            optimum=float(resource_obj@solution.x)
            preserve_A=np.vstack([preserve_A,resource_obj/denominator])
            preserve_b=np.r_[preserve_b,(optimum+max(1e-5,abs(optimum)*1e-9))/denominator]
    valid=bool(solution.success and (options or not capacity_mode))
    if valid:
        violation=A@solution.x-b
        if np.any(violation>np.maximum(1e-4,np.maximum(1,np.abs(b))*2e-7)):raise ValueError('Çözücü sonucu fiziksel kısıt toleransını aştı; plan gösterilmedi.')
    constraints=[]
    for j,meta in enumerate(metadata):
        if meta['id'].startswith('target_'):continue
        sign=-1 if meta['sense']=='min' else 1
        used=float(A[j]@solution.x)*sign if valid else None
        cap=float(b[j])*sign;slack=float(b[j]-A[j]@solution.x) if valid else None
        constraints.append({**meta,'used':used,'capacity':cap,'slack':slack,'binding':abs(slack)<=max(1e-5,abs(cap)*1e-7) if valid else None})
    optimized=None
    if valid:
        allocations=[]
        for o,x in zip(options,solution.x[:n]):
            if x<1e-7:continue
            allocations.append({'crop_id':o['crop_id'],'name_tr':o['name_tr'],'method':o['method'],'water_source':o['water_source'],'capacity_unit':o['capacity_unit'],
              'capacity_used':float(x),'area_ha':float(x) if o['method']=='open_field' else None,'production_kg':float(x*o['yield']),
              'water_m3':float(x*o['water']),'energy_kwh':None if o['energy'] is None else float(x*o['energy']),
              'season_start':o['season_start'],'season_end':o['season_end']})
        crops=[]
        binding_ids={c['id'] for c in constraints if c['binding']}
        for i,c in enumerate(r.crops):
            aa=[a for a in allocations if a['crop_id']==c.crop_id];area=sum(a['area_ha'] or 0 for a in aa);prod=sum(a['production_kg'] for a in aa)
            reasons=[]
            if not c.enabled:reasons.append('Ürün aday listesinde kapalı; minimum kısıtları varsa kendiliğinden silinmez.')
            if 'crop_min_output_'+c.crop_id in binding_ids:reasons.append(f'Minimum üretim kısıtı bağlayıcı: {c.min_production_kg:g} kg; daha aşağı indirilemez.')
            if 'crop_max_area_'+c.crop_id in binding_ids:reasons.append('Kullanıcının maksimum alan payına ulaşıldı.')
            if 'crop_min_area_'+c.crop_id in binding_ids and c.min_share>0:reasons.append('Kullanıcının minimum alan payı bağlayıcı.')
            if not aa:reasons.extend(sorted({x['reason'] for x in excluded if x['crop_id']==c.crop_id}))
            if area<c.current_area_ha-1e-5:reasons.append(f'Alan {c.current_area_ha-area:.2f} ha azaldı; seçilen kaynak kısıtları altında normalize ürün hedeflerinin toplamı en yükseğe çıkarıldı.')
            elif area>c.current_area_ha+1e-5:reasons.append(f'Alan {area-c.current_area_ha:.2f} ha arttı; hedef karşılanması ve alan/su kısıtlarının birlikte çözümü.')
            elif r.mode=='turkiye':reasons.append('Mevcut alan bu koşullarda değişmedi.')
            wm=water_by[c.crop_id].get('gross_water_m3_ha')
            if wm is not None:reasons.append(f'Hesaplanan brüt su gereksinimi {wm:.1f} m³/ha; verim girdisi {c.yield_kg_ha if c.yield_kg_ha else "eksik"} kg/ha.')
            if capacity_mode:
                reasons.append(f"Tek ürün kaynak potansiyeli {normalization[c.crop_id]:.2f} kg; karşılanan oran {prod/normalization[c.crop_id]*100 if normalization[c.crop_id] else 0:.1f}%. Bu bir talep hedefi değildir.")
            if not capacity_mode and not regional and wm is not None and c.yield_kg_ha:
                target_water=wm*c.target_production_kg/c.yield_kg_ha
                reasons.append(f'Bu ürünün tam tarla hedefi {target_water:.1f} m³ gerektirir; hedef ağırlığı {c.priority:g}. Çözücü yalnız ha başına suyu değil, bu hedeflerin karşılanmasını karşılaştırır.')
            active_water=[x['label'] for x in constraints if x['id'].startswith('water_') and x['binding'] and x['capacity']>0]
            if active_water:reasons.append('Çözümde dolan su bütçeleri: '+', '.join(active_water)+'. Tek başına nedensellik/duyarlılık katsayısı değildir.')
            if not aa:
                summary_reason=next((x['reason'] for x in excluded if x['crop_id']==c.crop_id),'Bu koşullarda ürüne üretim kapasitesi ayrılmadı.')
            elif 'crop_min_output_'+c.crop_id in binding_ids and area<c.current_area_ha-1e-5:
                summary_reason='Alan, seçilen kaynak bütçelerinde minimum üretim sınırına kadar azaltıldı.'
            elif 'crop_min_output_'+c.crop_id in binding_ids and abs(area-c.current_area_ha)<=1e-5:
                summary_reason='Alan değişmedi; minimum üretim sınırı bağlayıcı.'
            elif 'crop_max_area_'+c.crop_id in binding_ids:
                summary_reason='Kullanıcının azami alan payına ulaşıldı.'
            elif area<c.current_area_ha-1e-5:
                summary_reason='Kaynak bütçeleri altında ürün hedeflerini birlikte karşılamak için alan azaldı.'
            elif prod>=c.target_production_kg*(1-1e-6):
                summary_reason='Seçilen kaynak ve yöntemlerle ürün hedefi karşılandı.'
            else:
                summary_reason='Seçilen bütçe ve ürün öncelikleri altında kısmi üretim hedefi karşılandı.'
            if regional:
                reasons=[text for text in reasons if 'normalize ürün hedeflerinin' not in text and 'hedef karşılanması ve' not in text]
                reasons.append('Önce ekili alan korundu, sonra su minimize edildi. Mevcut üretim hedef tavanı değildir; minimum üretim kısıtları korunur.')
            if regional and aa:
                summary_reason='Ekili alanı koruyup su gereğini azaltan çözümde alan '+('arttı.' if area>c.current_area_ha+1 else 'azaldı.' if area<c.current_area_ha-1 else 'korundu.')
            if capacity_mode and aa:
                summary_reason='Seçilen kaynaklarla hesaplanan üretim potansiyeli payı; kullanıcı tarafından verilmiş kg talebi değil.'
            crops.append({'crop_id':c.crop_id,'name_tr':knowledge[c.crop_id]['name_tr'],'area_ha':area,'area_share_pct':area/r.land_area_ha*100 if r.land_area_ha else 0,
               'production_kg':prod,'current_area_ha':c.current_area_ha,'delta_area_ha':area-c.current_area_ha,'target_production_kg':c.target_production_kg,
               'target_achievement_fraction':min(1,prod/c.target_production_kg),'summary_reason':summary_reason,'reasons':reasons})
        area=sum(a['area_ha'] or 0 for a in allocations);water=sum(a['water_m3'] for a in allocations)
        optimized={'crops':crops,'allocations':allocations,'totals':{'open_field_area_ha':area,'greenhouse_area_m2':sum(a['capacity_used'] for a in allocations if a['method']=='greenhouse'),
         'hydroponics_area_m2':sum(a['capacity_used'] for a in allocations if a['method']=='hydroponics'),'water_m3':water,'energy_kwh':sum(a['energy_kwh'] for a in allocations) if all(a['energy_kwh'] is not None for a in allocations) else None,'unallocated_land_ha':max(0,r.land_area_ha-area)},
         'water_sources':[{'source_id':s.source_id,'used_m3':sum(a['water_m3'] for a in allocations if a['water_source']==s.source_id),'capacity_m3':s.capacity_m3 if s.enabled else 0,
          'share_pct':100*sum(a['water_m3'] for a in allocations if a['water_source']==s.source_id)/water if water else 0} for s in r.water_sources]}
    available=sum(s.capacity_m3 for s in r.water_sources if s.enabled and s.quality_suitable is True)
    for pat in [baseline,current]:
        pat['totals']['available_water_m3']=available
        pat['totals']['water_deficit_m3']=None if pat['totals']['water_m3'] is None else max(0,pat['totals']['water_m3']-available)
    evidence_integrity=None
    if r.climate_context_id and r.climate_context_id.startswith('nasa_'):
        from .north_evidence import load_north_evidence
        evidence_integrity=load_north_evidence()['integrity']
    hashes={p:digest((ROOT/p).read_bytes()) for p in ['data/agriculture/crops.json','data/agriculture/region_baselines.json','data/literature_parameters.json']}
    return {'status':'conditional' if valid else ('insufficient_data' if not options else 'infeasible'),'classification':'SIMULATION_EXPLANATORY','model_version':'0.5.0',
      'input_resolution':resolution,
      'objective':{'mode':r.planning_objective,'quantity_basis':'cultivated_area' if regional else 'capacity' if capacity_mode else 'demand','resource_priority_fraction':r.resource_priority_fraction if priority_capacity else None,'stages':stage_names,'normalization_kg':normalization,'priority_weights':{c.crop_id:c.priority for c in r.crops},'balanced_floor':balanced_floor,
        'minima_policy':'Declared kg minima ignored for capacity exploration; area-share minima retained.' if capacity_mode else ('Full enabled crop demand enforced.' if r.planning_objective in {'water_priority','energy_priority'} else 'Declared production minima retained.'),
        'normalization_basis':'Area first, water second; historical production is not a cap.' if regional else 'Single-crop resource-constrained upper potential, lower portfolio obligations excluded.' if capacity_mode else 'User demand target',
        'label':{'regional_water':'Ekili alanı koru, suyu azalt','capacity':'Kaynak kapasitesini keşfet','demand':'Talebi karşıla','balanced':'Dengeli plan','water_priority':'Su öncelikli','energy_priority':'Enerji öncelikli'}[r.planning_objective]},
      'baseline':baseline,'current':current,'optimized':optimized,'constraints':constraints,'crop_water':water_rows,'excluded_options':excluded,
      'explanations':['Açık sıralı amaç: '+ ' → '.join(stage_names)+'.',
       'Bölgesel amaç: beyan edilen ürün alt sınırlarında ekili alanı en yükseğe çıkar, aynı alan için suyu en aza indir. Mevcut desen öneriye tavan değildir.' if regional else 'Kapasite/dengeli modda kg hedefleri ve kg minimumları kullanılmaz; normalizasyon kaynaklarla tek ürünün ulaşabileceği hesaplanmış üst potansiyeldir.' if capacity_mode else 'Talep hedefleri kullanılır; su/enerji önceliği modlarında etkin ürünlerin tam talebi zorunludur.',
       'Türkiye bölgesel amaçta mevcut üretim tavan değildir; önce ekili alan, sonra en az su. Ürün minimumları korunur.' if regional else 'Hedefler ve ağırlıklar kullanıcı planlama tercihleridir; farklı ürünlerin kilogramları besin/değer eşdeğeri diye toplanmaz.',
       'Uygulanabilir plan bulundu.' if valid else 'Seçilen minimumlar, uygunluk ve kaynak bütçeleri birlikte sağlanmıyor; minimumlar sessizce gevşetilmedi.'],
      'limitations':['ETc/depo hesabı ürün su gereksinimi senaryosudur; yerel sulama/verim validasyonu değildir.',
       *TEMPERATURE_SCENARIO_LIMITATIONS,
       'Açık tarla ha, kontrollü üretim m² yetiştirme yüzeyi ve ürün kg ayrı tutulur. Tek ortak alan/pay yüzdesi yok.',
       'Kc/takvim FAO örneği; kar erimesi, yeraltı suyu, çeltik ek suyu ve çiftlik tahsisi kendiliğinden modellenmez.',
       'Verim sabit katsayıdır; su stresi altında gerçekleşecek verimi tahmin etmez. Plan gereken sulamanın zamanında sağlandığını varsayar.',
       'Kontrollü üretim enerji/alan/su katsayıları açık senaryo veya literatür aktarımıdır; Arktik ısıtma/ışık kalibrasyonu değildir.',
       'Kaynak kalitesinin uygunluğu ve depolanmış/yeniden kullanılan hacimler senaryodur; gerçek hidrolojik arz değildir.',
       'Bütçe doluluğu bağlayıcılığı gösterir; tek başına kaynak artışının nedensel faydasını kanıtlamaz.'],
      'solver':{'name':'SciPy HiGHS','objective':r.planning_objective,'target_score':optimal_score,'success':bool(valid)},
      'request':original_request.model_dump(mode='json'),'effective_request':r.model_dump(mode='json'),'provenance':{'input_classification':'USER_SCENARIO','regional_source_classification':region['classification'],'baseline_sources':region.get('sources',[]),
       'temperature_scenario':{'temperature_delta_c':r.temperature_delta_c,'source_url':FAO56_HARGREAVES,'source_equation':52,'method':'FAO56_EQ52_TEMPERATURE_TERM_RATIO' if r.temperature_delta_c else 'SOURCE_ET0_UNCHANGED','classification':'DERIVED_TEMPERATURE_SENSITIVITY_SCENARIO' if r.temperature_delta_c else 'SOURCE_ET0_UNCHANGED','locally_validated':False},
       'data_hashes':hashes,'planning_objective':r.planning_objective,'climate_datasets':[{ 'id':d['dataset_id'],'sha256':d['content_sha256']} for d in load_manifest(recent=r.climate_basis=='era5_2024_2025')['datasets'] if d['requested_location']['site_id']==r.region_id],
       'climate_context_id':r.climate_context_id,'climate_context_integrity':evidence_integrity,'climate_context_role':'Source-based research screen applied to open-field candidates; no automatic yield/water/energy coefficient' if resolution else 'Evidence context only; not applied to crop suitability, ET0 or marine water temperature','north_resolution_hashes':resolution['analysis']['source']['hashes'] if resolution else None,'overrides':r.overrides,'code_sha256':digest(b''.join((ROOT/'backend'/p).read_bytes() for p in ['planning.py','planning_contracts.py','regional_scope.py','science.py','north_resolution.py','automatic_baseline.py']))}}
