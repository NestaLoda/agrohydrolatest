"""Automatic, source-selected northern climate diagnosis; no invented production inputs."""
import json
import numpy as np
import pandas as pd
from .provenance import ROOT, digest
from .repository import north_context
from .north_evidence import load_north_evidence

CONTEXTS={'ec_earth_2030_2049','nasa_ssp245_2035','nasa_ssp585_2035'}


def _longest_window(group):
    best=[];run=[]
    for row in group.itertuples():
        if row.tmin_c>0:run.append(row.date)
        else:run=[]
        if len(run)>len(best):best=list(run)
    return {'days':len(best),'start':best[0].date().isoformat() if best else None,
            'end':best[-1].date().isoformat() if best else None}


def analyze_northern_baseline(climate_context_id='ec_earth_2030_2049'):
    if climate_context_id not in CONTEXTS:raise ValueError('Bilinmeyen otomatik Kuzey iklim bağlamı.')
    parameter_path=ROOT/'data/auto_baseline_parameters.json'
    parameter_raw=parameter_path.read_bytes()
    parameters={p['id']:p for p in json.loads(parameter_raw)['parameters']}
    review=load_north_evidence()
    if climate_context_id.startswith('nasa_'):
        scenario='ssp245' if climate_context_id=='nasa_ssp245_2035' else 'ssp585'
        path=ROOT/'data/north/u9_acquisition/daily_point_2035.csv'
        frame=pd.read_csv(path);frame=frame[frame.scenario==scenario].copy()
        source={'model':'ACCESS-CM2','scenario':scenario,'period':'2035','classification':'EXTERNAL_FUTURE_SCENARIO_SINGLE_MODEL_YEAR',
          'latitude':78.125,'longitude':15.625,'url':review['sources']['nasa']['url'],
          'hashes':{'daily_point_2035.csv':digest(path.read_bytes()),'manifest':review['integrity']['manifest_sha256']}}
    else:
        context=north_context();meta=context['provenance'][1]
        raw=(ROOT/meta['raw_path']).read_bytes()
        if digest(raw)!=meta['sha256']:raise ValueError('Kuzey ham veri hash kaydı değişti.')
        daily=json.loads(raw)['daily']
        frame=pd.DataFrame({'date':daily['time'],'tmin_c':daily['temperature_2m_min'],
                            'tmax_c':daily['temperature_2m_max'],'precipitation_mm':daily['precipitation_sum']})
        source={'model':meta['model'],'scenario':meta['scenario_label'],'period':'2030–2049',
          'classification':'EXTERNAL_CLIMATE_MODEL','latitude':meta['returned_coordinate']['latitude'],
          'longitude':meta['returned_coordinate']['longitude'],'url':meta['source_url'],
          'hashes':{'raw':meta['sha256'],'summary':context['summary_sha256']}}
    frame['date']=pd.to_datetime(frame.date).dt.normalize();frame=frame.sort_values('date')
    numeric=frame[['tmin_c','tmax_c','precipitation_mm']].to_numpy()
    if not len(frame) or not np.isfinite(numeric).all() or (frame.tmin_c>frame.tmax_c).any() or (frame.precipitation_mm<0).any():
        raise ValueError('Otomatik analiz için iklim serisi eksik/geçersiz.')
    expected=pd.date_range(frame.date.min(),frame.date.max(),freq='D')
    if len(frame)!=len(expected) or frame.date.nunique()!=len(expected):raise ValueError('Otomatik analiz eksiksiz günlük seri gerektirir.')
    frame['year']=frame.date.dt.year;frame['month']=frame.date.dt.month
    frame['mean_c']=(frame.tmin_c+frame.tmax_c)/2
    # FAO56 Eq52; Ra MJ is converted to equivalent mm exactly once.
    doy=frame.date.dt.dayofyear.to_numpy();latitude=np.deg2rad(source['latitude'])
    dr=1+.033*np.cos(2*np.pi*doy/365);declination=.409*np.sin(2*np.pi*doy/365-1.39)
    sunset=np.arccos(np.clip(-np.tan(latitude)*np.tan(declination),-1,1))
    radiation=24*60/np.pi*parameters['solar_constant']['value']*dr*(sunset*np.sin(latitude)*np.sin(declination)+np.cos(latitude)*np.cos(declination)*np.sin(sunset))
    raw_et0=parameters['hargreaves_coefficient']['value']*(frame.mean_c.to_numpy()+parameters['hargreaves_temperature_offset_c']['value'])*np.sqrt(frame.tmax_c-frame.tmin_c)*parameters['radiation_mj_to_equivalent_mm']['value']*np.maximum(radiation,0)
    frame['et0_proxy_mm']=np.maximum(raw_et0,0)
    negative_estimates=int((raw_et0<0).sum())
    source['hashes']['automatic_parameters']=digest(parameter_raw)
    frame['gdd5']=np.maximum(frame.mean_c-5,0)
    frame['heating_degree_hours_18c']=np.maximum(18-frame.mean_c,0)*24
    annual=[]
    for year,g in frame.groupby('year'):
        annual.append({'year':int(year),'days':len(g),'mean_temperature_c':float(g.mean_c.mean()),
          'precipitation_mm':float(g.precipitation_mm.sum()),'et0_proxy_mm':float(g.et0_proxy_mm.sum()),'gdd5_c_days':float(g.gdd5.sum()),
          'frost_free_days':int((g.tmin_c>0).sum()),'longest_frost_free_window':_longest_window(g),
          'heating_degree_hours_18c':float(g.heating_degree_hours_18c.sum())})
    monthly=[]
    for month,g in frame.groupby('month'):
        # Average of monthly annual sums; not a 20-year cumulative water volume.
        monthly.append({'month':int(month),'mean_temperature_c':float(g.mean_c.mean()),
          'tmin_c':float(g.tmin_c.mean()),'tmax_c':float(g.tmax_c.mean()),
          'precipitation_mm':float(g.groupby('year').precipitation_mm.sum().mean()),'et0_proxy_mm':float(g.groupby('year').et0_proxy_mm.sum().mean()),
          'heating_degree_hours_18c':float(g.groupby('year').heating_degree_hours_18c.sum().mean())})
    from .planning import catalog
    knowledge=catalog();candidates=[]
    for candidate in review['candidates']:
        cid=candidate['id'];crop=knowledge.get(cid)
        if not candidate.get('default_candidate') or not crop:continue
        methods=[m for m in candidate['methods'] if m in crop.get('compatible_methods',[])]
        if not methods or not any(s in review['sources'] for s in candidate.get('source_ids',[])):continue
        days=sum(crop['growing_period']['stage_days']);open_field='open_field' in methods
        windows=[{'year':a['year'],**a['longest_frost_free_window'],
          'reference_calendar_fits':a['longest_frost_free_window']['days']>=days if open_field else None} for a in annual]
        thermal={'status':'NOT_APPLICABLE_CONTROLLED_ENVIRONMENT','locally_validated':False}
        cycle=parameters.get(cid+'_crop_cycle_days');envelope=parameters.get(cid+'_temperature_absolute_c')
        if open_field and cycle and envelope:
            minimum=int(cycle['value'][0]);low,high=envelope['value'];screen_years=[]
            for year,g in frame.groupby('year'):
                rolling=g.mean_c.rolling(minimum).mean();eligible=rolling.between(low,high)
                index=rolling.idxmax()
                screen_years.append({'year':int(year),'maximum_window_mean_c':float(rolling.loc[index]),
                  'warmest_start':(frame.loc[index,'date']-pd.Timedelta(days=minimum-1)).date().isoformat(),
                  'warmest_end':frame.loc[index,'date'].date().isoformat(),'matching_windows':int(eligible.sum()),
                  'status':'screening_pass_not_validated' if eligible.any() else 'screened_out'})
            thermal={'status':'screening_pass_not_validated' if any(x['matching_windows'] for x in screen_years) else 'screened_out',
              'minimum_window_days':minimum,'mean_temperature_envelope_c':[low,high],'annual':screen_years,
              'source_url':envelope['source_url'],'classification':'DERIVED_RESEARCH_SCREEN',
              'locally_validated':False,'policy':'Minimum documented cycle rolling mean within species envelope; our screening aggregation, not cultivar maturity/frost validation.'}
        candidates.append({'crop_id':cid,'thermal_screen':thermal,'name_tr':candidate['name_tr'],'methods':methods,
          'reference_calendar_days':days,'calendar_source':crop['growing_period']['source_url'],
          'calendar_classification':crop['growing_period']['classification'],
          'frost_free_calendar_screen':'REFERENCE_WINDOW_DIAGNOSTIC' if open_field else 'NOT_APPLICABLE_CONTROLLED_ENVIRONMENT',
          'annual_windows':windows,'years_with_reference_window':sum(w['reference_calendar_fits'] is True for w in windows) if open_field else None,
          'climate_suitable':None,'soil_suitable':None,'local_yield_kg_ha':None,
          'interpretation':'Tmin>0°C kesintisiz günleri ile aktarılmış örnek takvim karşılaştırmasıdır; ürünün don toleransı/olgunluk eşiği veya yerel uygunluk kararı değildir.' if open_field else 'Kontrollü üretimin çevrimi dış ortam don olmayan günleriyle belirlenmez; yerel iç ortam ve enerji modeli gerekir.',
          'missing':candidate.get('missing',[])})
    mean=lambda key:float(np.mean([a[key] for a in annual]))
    return {'status':'automatic_analysis_ready','climate_context_id':climate_context_id,
      'classification':'DERIVED_FROM_VERIFIED_FUTURE_CLIMATE','source':source,'row_count':len(frame),
      'annual':annual,'monthly':monthly,'summary':{'years':len(annual),'mean_temperature_c':float(frame.mean_c.mean()),
        'mean_annual_precipitation_mm':mean('precipitation_mm'),'mean_annual_et0_proxy_mm':mean('et0_proxy_mm'),'mean_annual_gdd5_c_days':mean('gdd5_c_days'),
        'mean_annual_heating_degree_hours_18c':mean('heating_degree_hours_18c'),
        'longest_frost_free_window':max((a['longest_frost_free_window'] for a in annual),key=lambda x:x['days'])},
      'et0_method':{'name':'FAO56_HARGREAVES_RESEARCH_PROXY','source_url':parameters['hargreaves_coefficient']['source_url'],
        'formula':'0.0023*(Tmean+17.8)*sqrt(Tmax-Tmin)*(0.408*Ra_MJ)',
        'negative_estimates_clipped':negative_estimates,'polar_day_night_handling':'astronomical acos argument clipped [-1,1]',
        'locally_validated':False,'irrigation_or_allocation':False},
      'candidate_analysis':candidates,'production_input_applied':False,
      'field_evidence':{'temperature_precipitation':'EXTERNAL_FUTURE_SCENARIO','gdd_frost_windows':'DERIVED_CLIMATE_DIAGNOSTIC',
        'heating_degree_hours':'DESIGN_INDICATOR_18C_DAILY_MEAN_APPROXIMATION','crop_calendar':'EXTERNAL_LITERATURE_TRANSFER',
        'soil_permafrost':'DATA_NEEDED','terrestrial_allocation':'DATA_NEEDED','local_yield':'DATA_NEEDED',
        'et0_crop_water':'DERIVED_ET0_PROXY_CROP_WATER_STILL_MISSING','energy_kwh':'DATA_NEEDED'},
      'blockers':[{'id':'et0_snow','needed':'ET0 vekilinin yerel doğrulaması ve kar birikimi/erimesi ürün su dengesi','blocks':'future_crop_irrigation'},
        {'id':'ground','needed':'Yerel toprak, drenaj, permafrost ve kullanılabilir alan','blocks':'open_field_approval'},
        {'id':'crop_response','needed':'Çeşide özgü sıcaklık/don/olgunluk ve yerel verim','blocks':'crop_suitability_and_yield'},
        {'id':'water_access','needed':'Debi/tahsis, erişim, depolama ve mevcut kullanımlar','blocks':'reliable_freshwater_budget'},
        {'id':'building_energy','needed':'Bina ısı kaybı, aydınlatma ve işletme katsayıları','blocks':'heating_degree_hours_to_kwh'}],
      'limitations':['18°C açık tasarım referansıdır; günlük ortalama sıcaklıkla hesaplanan derece-saat enerji veya ürün için optimum sıcaklık değildir.',
        'GDD5 genel tanımlayıcı göstergedir; doğrulanmış ürüne özgü gelişme eşiği değildir.',
        'Yağış kar su eşdeğerini içerebilir; akış, aynı gün sıvı su veya kullanılabilir sulama tahsisi değildir.',
        'Takvimin don olmayan pencereye sığmaması ürünün kesin yetişemeyeceğini; sığması uygun olduğunu kanıtlamaz.',
        'ET0 sıcaklık temelli araştırma vekilidir; kar/yüzey enerjisi ve yerel doğrulama eksik. ETc, sulama ihtiyacı veya su arzı olarak kullanılmadı.',
        'İklim seçimi bu analizi gerçekten yeniden hesaplar; eksik fiziksel katsayıların yerine üretim sayısı oluşturmaz.',
        'Tek model 2035 yılı klimatoloji değildir; 20 yıllık tek model dönemi de ensemble belirsizliğini kapsamaz.']}
