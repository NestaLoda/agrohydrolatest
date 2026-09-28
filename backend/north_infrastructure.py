"""Fixed-production storage and supply screening; no local allocation is inferred."""
from math import isfinite
from statistics import mean


def minimum_cyclic_storage(capture, demand):
    """Sequent-peak deficit over a repeated finite daily record.

    No backup; usable captured water follows the existing snow/roof model.
    Cyclic steady operation excludes first filling. It is not a probabilistic
    return-period design or a guarantee outside the supplied chronology.
    """
    if not capture or len(capture) != len(demand):
        raise ValueError('Equal nonempty capture and demand series required')
    if any(not isfinite(v) or v < 0 for v in [*capture,*demand]):
        raise ValueError('Daily volumes must be finite and nonnegative')
    if sum(capture)+1e-9 < sum(demand):
        return None
    deficit = capacity = 0.
    for _ in range(2):
        for c,d in zip(capture,demand):
            deficit=max(0.,deficit+d-c)
            capacity=max(capacity,deficit)
    return capacity


def replay(capture,demand,capacity,initial=0.,cyclic=False):
    stock=initial; deficits=[]; spill=0.; longest=run=0
    for c,d in zip(capture,demand):
        available=stock+c
        deficit=max(0.,d-available)
        spill+=max(0.,available-d-capacity)
        stock=min(capacity,max(0.,available-d))
        deficits.append(deficit)
        run=run+1 if deficit>1e-8 else 0
        longest=max(longest,run)
    if cyclic and deficits:
        prefix=0
        for v in deficits:
            if v<=1e-8:break
            prefix+=1
        longest=min(len(deficits),max(longest,prefix+run))
    return {'deficits':deficits,'final_storage_m3':stock,'spill_m3':spill,'longest_backup_run_days':longest}


def storage_design(records, selected_capacity):
    """records: per-model actual capture and fixed plan demand, dates retained."""
    if not records:return {'classification':'NOT_APPLICABLE','reason':'No feasible production plan'}
    results=[]
    for r in records:
        c,d=r['capture'],r['demand'];years=sorted(set(x[:4] for x in r['dates']))
        minimum=minimum_cyclic_storage(c,d)
        scenarios=[]
        for factor in (1.,.75,.5):
            amounts=[v*factor for v in c]
            first=replay(amounts,d,selected_capacity)
            cycle=replay(amounts,d,selected_capacity,first['final_storage_m3'],cyclic=True)
            annual={y:0. for y in years}
            for day,v in zip(r['dates'],cycle['deficits']):annual[day[:4]]+=v
            scenarios.append({'capture_factor':factor,'backup_mean_m3_year':mean(annual.values()),
                'backup_worst_m3_year':max(annual.values()),'backup_peak_m3_day':max(cycle['deficits']),
                'longest_backup_run_days':cycle['longest_backup_run_days'],
                'minimum_cyclic_storage_m3':minimum_cyclic_storage(amounts,d)})
        results.append({'model':r['model'],'minimum_cyclic_storage_m3':minimum,
            'initial_empty_backup_m3':sum(replay(c,d,selected_capacity)['deficits']),
            'record_years':len(years),'scenarios':scenarios})
    finite=[r['minimum_cyclic_storage_m3'] for r in results if r['minimum_cyclic_storage_m3'] is not None]
    sufficient=len(finite)==len(results) and bool(results)
    worst=max((s['backup_peak_m3_day'] for r in results for s in r['scenarios'] if s['capture_factor']==1.),default=0.)
    return {'classification':'FIXED_PLAN_CHRONOLOGICAL_STORAGE_SCREENING','selected_capacity_m3':selected_capacity,
        'minimum_for_all_tested_records_m3':max(finite) if sufficient else None,
        'capture_sufficient_for_all_records':sufficient,'backup_peak_m3_day':worst,'models':results,
        'assumptions':['Sabit hesaplanmış ürün/yöntem planı; depo değişirken ürünler yeniden optimize edilmez.',
            'Asgari depo, sınanan günlük kaydın döngüsel işletiminde yağış/kar ile talebi karşılamak içindir; ilk dolum hariçtir.',
            'Toplam toplama yetersizse hiçbir sonlu depo tek başına çözüm değildir.',
            '%75 ve %50 toplama mühendislik stres testidir; kuraklık olasılığı veya iklim tahmini değildir.',
            'Yedek ihtiyaç yağış/depo sonrası gerektir; belediye tahsisi günlere keyfî dağıtılmadı, arıtmanın günlük kapasitesi doğrulanmadı.',
            'Kayıt sınırları, kar başlangıcı, kalite kayıpları ve yerel don/çatıda birikim belirsizdir; fiziksel saha doğrulaması gerekir.']}


def energy_supply(plan,options,cop,annual_limit=None,power_limit=None):
    if not plan.get('totals') or plan.get('status')=='infeasible':
        return {'classification':'NOT_APPLICABLE','power_screen_status':'NOT_APPLICABLE','busiest_month':None,'operation_power_upper_bound_kw':None}
    keys=['lighting_kwh_m2','pumping_kwh_m2','fans_kwh_m2','dehumidification_kwh_m2','cooling_kwh_m2']
    byid={o['id']:o for o in options}; parts={k:0. for k in keys};monthly=[0.]*12
    power=0.
    for a in plan.get('allocations',[]):
        option=byid.get(f"{a['crop_id']}:{a['method']}:{a['season']}",{})
        profile=option.get('energy_components_monthly',[])
        for m in profile:
            for k in keys:parts[k]+=a['area_m2']*m[k]
            monthly[m['month']-1]+=a['area_m2']*(sum(m[k] for k in keys)+m['heat_kwh_th_m2']/cop)
        power+=a['area_m2']*(option.get('electricity_peak_bound_kw_m2',0.)+option.get('heat_peak_bound_kw_th_m2',0.)/cop)
    totals=plan.get('totals',{})
    treatment=totals.get('treatment_electricity_kwh',0.)
    heat=totals.get('heat_kwh_th',0.)/cop
    # Treatment heat is already part of total heat. Component residual exposes
    # old/incomplete coefficient packages rather than quietly inventing a split.
    residual=totals.get('equivalent_electricity_kwh',0.)-(sum(parts.values())+heat+treatment)
    for row in plan.get('monthly',[]):
        total_ro=totals.get('desalinated_m3',0.)
        if total_ro:monthly[row['month']-1]+=treatment*row['desalinated_m3']/total_ro
    return {'classification':'MODELED_SUPPLY_SCREENING','components_kwh_year':parts,
        'heating_electric_equivalent_kwh_year':heat,'treatment_electricity_kwh_year':treatment,
        'component_closure_residual_kwh':residual,'monthly_operation_kwh':monthly,
        'busiest_month':max(range(12),key=lambda i:monthly[i])+1,
        'operation_power_upper_bound_kw':power,'declared_power_limit_kw':power_limit,
        'power_screen_status':'UNCONFIRMED' if power_limit is None else 'WITHIN_OPERATION_BOUND' if power<=power_limit else 'DESIGN_REVIEW',
        'annual_limit_kwh':annual_limit,'local_supply_verified':False,
        'limits':['Güç, her seçili seçeneğin saatlik yeniden kurulan ısı ve elektrik azamilerinin toplamıdır; eşzamanlı ölçüm değildir.',
            'Arıtma debisi/çalışma saati, ilk çalıştırma akımı, yedekleme ve boş tesis don koruması güç sınırına dahil değildir.',
            'Aylık grafik üretim işletimi ve RO elektriğidir; kaynak suyu ön ısıtmasının aylık dağılımı dahil değildir.',
            'Beyan edilen güç sınırı tarama içindir; elektrik bağlantısı veya işletme izni kanıtı değildir.']}
