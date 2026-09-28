"""Water coefficients for live visualization; no optimization or source mutation."""
from .planning import catalog, baseline_region, _crop_water_rows
from .repository import load_verified_climate

def scenario_preview(request):
    if request.mode != 'turkiye':
        raise ValueError('Canlı bölgesel önizleme Türkiye içindir.')
    region = baseline_region(request.region_id)
    frame = load_verified_climate(recent=request.climate_basis == 'era5_2024_2025')
    return {
        'classification':'SIMULATION_PREVIEW',
        'optimization_performed':False,
        'region_id':request.region_id,
        'crop_water':_crop_water_rows(request,catalog(),frame),
        'source_year':region['year'],
        'note':'Günlük su dengesi katsayıları; alan × m³/ha canlı senaryo gereğidir. Ölçüm veya yeni optimum değildir.'
    }
