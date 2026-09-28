"""Keep unresolved crops fixed; optimize only the explicitly known-water subset.

The subset budget is NOT the province's total available water. Unknown crop water
and total water stay null, including when a feasible partial solution is found.
"""
def partial_region(r, knowledge, water_rows, baseline, current, runner):
    unknown={w['crop_id'] for w in water_rows if w.get('gross_water_m3_ha') is None}
    held=[c for c in r.crops if c.crop_id in unknown and c.enabled and c.current_area_ha>0]
    if not held or len(held)==len(r.crops) or r.energy_budget_kwh is not None:return None
    for c in held:
        if c.yield_kg_ha is None or c.climate_suitable is not True or c.soil_suitable is not True:return None
        if not c.min_share*r.land_area_ha<=c.current_area_ha<=c.max_share*r.land_area_ha:return None
        if c.current_area_ha*c.yield_kg_ha<c.min_production_kg:return None
    ids={c.crop_id for c in held};reserved=sum(c.current_area_ha for c in held)
    remaining=r.land_area_ha-reserved
    if remaining<=0:return None
    sub=r.model_copy(deep=True)
    sub.crops=[c for c in sub.crops if c.crop_id not in ids]
    sub.land_area_ha=remaining
    sub.min_cultivated_fraction=max(0,(r.land_area_ha*r.min_cultivated_fraction-reserved)/remaining)
    for c in sub.crops:
        c.min_share=c.min_share*r.land_area_ha/remaining
        c.max_share=min(1,c.max_share*r.land_area_ha/remaining)
        if c.min_share>c.max_share:return None
    sub=type(r).model_validate(sub.model_dump())
    result=runner(sub)
    scope={'kind':'KNOWN_WATER_SUBSET','held_crop_ids':sorted(ids),'reserved_area_ha':reserved,
           'optimized_area_capacity_ha':remaining,'budget_scope':'Known-water crops only; unresolved crop supply is not included.',
           'total_water_known':False,'note':'Su hesabı eksik ürünler mevcut senaryo alanında sabit. Bütçe yalnız suyu hesaplanabilen ürünlere aittir; bölgenin toplam su yeterliliği doğrulanmadı.'}
    result.update(regional_scope=scope,request=r.model_dump(mode='json'),effective_request=r.model_dump(mode='json'),baseline=baseline,current=current,crop_water=water_rows)
    result['provenance']['regional_scope']=scope
    result['provenance']['subset_effective_request']=sub.model_dump(mode='json')
    result['limitations'].insert(0,scope['note'])
    available=sum(s.capacity_m3 for s in r.water_sources if s.enabled and s.quality_suitable is True)
    for pat in [baseline,current]:
        known=sum(c['water_m3'] or 0 for c in pat['crops'] if c['crop_id'] not in ids)
        pat['totals'].update(water_m3=None,water_deficit_m3=None,known_water_m3=known,available_water_m3=available)
    if result['optimized']:
        result['status']='partial_conditional'
        plan=result['optimized'];known=plan['totals']['water_m3']
        for row in plan['crops']:row['area_share_pct']=row['area_ha']/r.land_area_ha*100
        for c in held:
            reason='Su gereksinimi eksik: mevcut senaryo alanı sabit tutuldu; optimize edilmedi.'
            plan['crops'].append({'crop_id':c.crop_id,'name_tr':knowledge[c.crop_id]['name_tr'],
                'area_ha':c.current_area_ha,'area_share_pct':c.current_area_ha/r.land_area_ha*100,
                'production_kg':c.current_area_ha*c.yield_kg_ha,'current_area_ha':c.current_area_ha,
                'delta_area_ha':0,'summary_reason':reason,'reasons':[reason],'held_for_missing_water':True,
                'target_production_kg':c.target_production_kg,'target_achievement_fraction':None})
        order={c.crop_id:i for i,c in enumerate(r.crops)}
        plan['crops'].sort(key=lambda c:order[c['crop_id']])
        plan['totals'].update(known_water_m3=known,water_m3=None,energy_kwh=None,
                            open_field_area_ha=plan['totals']['open_field_area_ha']+reserved)
    return result
