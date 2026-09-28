"""Connect verified climate screening to the shared optimizer without inventing coefficients.

A failed research screen excludes an open-field option under this policy.
A passing screen NEVER establishes local suitability, yield or water allocation.
"""
from .automatic_baseline import analyze_northern_baseline


def resolve_north(request):
    resolved = request.model_copy(deep=True)
    analysis = analyze_northern_baseline(request.climate_context_id or 'ec_earth_2030_2049')
    screens = {c['crop_id']: c for c in analysis['candidate_analysis']}
    changes = []
    for crop in resolved.crops:
        screen = screens.get(crop.crop_id)
        if screen and screen['thermal_screen']['status'] == 'screened_out' and 'open_field' in crop.methods:
            crop.climate_suitable = False
            changes.append({'crop_id': crop.crop_id, 'method': 'open_field',
                            'reason': 'Seçili günlük iklimde kaynak sıcaklık zarfına uyan minimum çevrim bulunamadı.',
                            'classification': 'MODELED', 'policy': 'Research screen exclusion; not proof of agronomic impossibility.'})
    ledger = [
        {'variable': 'future_climate', 'state': 'SOURCED', 'field_measurable': False,
         'value': analysis['source']['period'], 'source': analysis['source']},
        {'variable': 'crop_thermal_screen', 'state': 'MODELED', 'field_measurable': False,
         'value': 'Günlük seri + kaynaklı tür zarfı; yerel validasyon değildir.'},
        {'variable': 'seasonal_freshwater', 'state': 'ASSUMED', 'field_measurable': False,
         'value': next((s.capacity_m3 for s in request.water_sources if s.source_id == 'freshwater'), None),
         'unit': 'm³ / plan dönemi', 'needed': 'Mevsimsellik, tahsis, depolama, erişim ve mevcut kullanımlar'},
        {'variable': 'energy_budget', 'state': 'ASSUMED' if request.energy_budget_kwh is not None else 'UNKNOWN',
         'field_measurable': False, 'value': request.energy_budget_kwh, 'unit': 'kWh / plan dönemi'},
        {'variable': 'marine_temperature', 'state': 'ASSUMED', 'field_measurable': True,
         'value': request.seawater_temperature_c, 'unit': '°C',
         'needed': 'Eşleşmiş model profili + PWN/CTD; mevcut varsayım geleceğin deniz sıcaklığı değildir.'},
        {'variable': 'marine_salinity', 'state': 'UNKNOWN', 'field_measurable': True,
         'value': None, 'needed': 'Kalibre C/T/p; arıtma modeline sayısal bağlantı gerekli'},
        {'variable': 'source_chemistry', 'state': 'UNKNOWN', 'field_measurable': 'POSSIBLE',
         'value': None, 'needed': 'İzinli numune; uzman/laboratuvarla kesinleşecek analiz paneli'},
    ]
    for crop in resolved.crops:
        ledger.append({'variable': f'{crop.crop_id}.climate_suitable', 'value': crop.climate_suitable,
                       'state': 'MODELED' if any(c['crop_id']==crop.crop_id for c in changes) else 'UNKNOWN' if crop.climate_suitable is None else 'ASSUMED',
                       'field_measurable': False})
        for key in ['soil_suitable', 'yield_kg_ha', 'manual_net_irrigation_mm', 'field_energy_kwh_ha',
                    'controlled_yield_kg_m2', 'controlled_water_m3_kg', 'controlled_energy_kwh_kg']:
            value = getattr(crop, key)
            ledger.append({'variable': f'{crop.crop_id}.{key}', 'value': value,
                           'state': 'UNKNOWN' if value is None else 'ASSUMED', 'field_measurable': False})
    return resolved, {'policy': 'source_resolved', 'production_input_applied': True,
                      'applied_scope': 'Candidate open-field exclusion only; positive screening is not suitability approval.',
                      'changes': changes, 'evidence_ledger': ledger, 'analysis': analysis,
                      'water_security': ['Fiziksel varlık', 'Mevsimsel miktar', 'Depolama', 'Erişim',
                                         'Kalite', 'Arıtma', 'Enerji', 'Kullanılabilir üretim suyu'],
                      'locally_validated_production_plan': False}
