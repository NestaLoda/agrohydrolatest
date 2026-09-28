"""Comparable period plans: same resources/objective/SSP, changing climate only."""
from .north_contracts import NorthRequest

HORIZONS = [('historical', 'Tarihsel iklim', '1995–2014'), ('recent', 'Güncel referans', '2015–2025'),
            ('near', '2030', '2021–2040'), ('mid', '2050', '2041–2060'),
            ('late', '2090', '2081–2100')]


def period_summary(result):
    plan = result['plan']
    area = result['request']['area_m2']
    methods = {key: 0. for key in ('open_field', 'greenhouse', 'hydroponics')}
    crops = {}
    for row in plan.get('allocations', []):
        methods[row['method']] += row['area_m2'] / area * 100
        crop = crops.setdefault(row['crop_id'], {'id': row['crop_id'], 'name': row['name'], 'share_pct': 0., 'kg': 0.})
        crop['share_pct'] += row['area_m2'] / area * 100
        crop['kg'] += row['production_kg']
    totals = plan.get('totals', {})
    water = totals.get('water_m3', 0.)
    return {'status': plan['status'], 'totals': totals, 'method_shares_pct': methods,
            'crops': list(crops.values()), 'unassigned_share_pct': max(0., 100-sum(methods.values())),
            'stored_share_pct': totals.get('stored_water_m3', 0.)/water*100 if water else None,
            'climate': result['climate']['ensemble'], 'frontier': result['candidates'].get('climate_frontier', {}),
            'candidate_count': len(result['candidates']['candidates']),
            'plan_crop_count': sum(c['kg'] > 1e-5 for c in crops.values()),
            'water_security': result.get('decision_story', {}).get('water_security', {}),
            'engine_version': result['provenance']['engine_version']}


def build_timeline(request: NorthRequest, calculate, *, focused=False):
    """Focused mode compares references + selection without unrelated future runs."""
    if focused and request.target_year is not None:
        base_request = request.model_copy(update={'target_year': 2026})
        base_result = calculate(base_request)
        base = {'horizon_id': 'baseline_2026', 'target_year': 2026, 'label': '2026', 'period': '2026',
                **period_summary(base_result), 'climate_dataset': base_result['climate'].get('dataset'),
                'climate_classification': base_result['climate'].get('classification'),
                'comparison_limitations': base_result['climate'].get('limitations', [])}
        points = [base]
        if request.target_year != 2026:
            result = calculate(request)
            points.append({'horizon_id': 'year', 'target_year': request.target_year,
                           'label': str(request.target_year), 'period': str(request.target_year),
                           **period_summary(result), 'climate_dataset': result['climate'].get('dataset'),
                           'climate_classification': result['climate'].get('classification'),
                           'comparison_limitations': result['climate'].get('limitations', [])})
        return {'classification': 'COMPARABLE_CONDITIONAL_YEAR_PLANS', 'points': points,
                'scenario_id': request.scenario_id, 'request': request.model_dump(),
                'baseline_horizon_id': 'baseline_2026',
                'comparison_policy': 'Both years use the same SSP and engineering inputs. 2026 is a three-model CMIP6 model-year baseline, not measured current weather or observed agriculture. Individual years are model realizations, not climate normals or exact forecasts.',
                'unchanged': ['area', 'objective', 'diversity_floor', 'engineering', 'storage', 'water_rights', 'energy_limit', 'crop_yield_analogue']}
    points = []
    horizons = HORIZONS if not focused else [row for row in HORIZONS
        if row[0] in ('historical','recent') or (request.target_year is None and row[0]==request.horizon_id)]
    for horizon, label, period in horizons:
        context = request.model_copy(update={'horizon_id': horizon,
                    'target_year': None,
                    'scenario_id': 'ssp245' if horizon in ('historical', 'recent') else request.scenario_id})
        result = calculate(context)
        points.append({'horizon_id': horizon, 'label': label, 'period': period, **period_summary(result),
                       'climate_dataset': result['climate'].get('dataset'),
                       'climate_classification': result['climate'].get('classification'),
                       'comparison_limitations': result['climate'].get('limitations', []),
                       'cross_dataset_check': result['climate'].get('cross_dataset_check')})
    if request.target_year is not None:
        result = calculate(request)
        points.append({'horizon_id': 'year', 'target_year': request.target_year,
                       'label': str(request.target_year), 'period': str(request.target_year), **period_summary(result),
                       'climate_dataset': result['climate'].get('dataset'),
                       'climate_classification': result['climate'].get('classification'),
                       'comparison_limitations': result['climate'].get('limitations', [])})
    return {'classification': 'COMPARABLE_CONDITIONAL_PERIOD_PLANS', 'points': points,
            'scenario_id': request.scenario_id, 'request': request.model_dump(),
            'baseline_horizon_id': 'recent',
            'comparison_policy': 'All non-climate inputs held constant. Recent ERA5 reference is 2015–2025 reanalysis, not observed agriculture. Future-versus-recent deltas include cross-dataset/grid differences and cannot be attributed solely to climate change. Historical NASA 1995–2014 is retained for same-dataset climate comparisons. The optional selected year is three model-year realizations, not actual future weather or a multi-year climate normal. Fixed period points are period summaries, not exact 2030/2050/2090 years. No interpolation or automatic bias correction.',
            'unchanged': ['area', 'objective', 'diversity_floor', 'engineering', 'storage', 'water_rights', 'energy_limit', 'crop_yield_analogue']}
