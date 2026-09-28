"""Monthly resource LP. The same function is used before and after field updates.

No monetary or hidden nutritional weights. A declared minimum area share protects
diversity, then a selected single output is maximized: fresh edible mass, protein
or food energy. Balanced preserves 95% of that maximum and minimizes the largest
normalized regret between water and energy.
Resource goals retain a selected fraction of that balanced crop vector.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import linprog
from .north_production_purpose import purpose_coefficients, nutritional_outputs

VERSION = 'north-explicit-production-purpose-regret-3'
BALANCED_MASS_RETENTION = .95  # Public policy, not an agronomic constant or fitted weight.


def solve_pattern(options, *, area_m2=100., inflow_m3=None, storage_m3=10.,
                  freshwater_m3=0., desalination=True, ro_kwh_m3=4., ro_heat_kwh_th_m3=0.,
                  heat_cop=1., energy_limit_kwh=None, objective='balanced',
                  production_retention=1., minimum_crop_share=.05, production_purpose='fresh_mass'):
    if objective not in {'balanced', 'water', 'energy'}:
        raise ValueError('Unknown planning objective')
    coefficients = [area_m2, production_retention, storage_m3, freshwater_m3, ro_kwh_m3,
                    ro_heat_kwh_th_m3, heat_cop, minimum_crop_share]
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) or not np.isfinite(value)
           for value in coefficients):
        raise ValueError('Resource coefficients must be finite numbers')
    if not 0 < production_retention <= 1 or not 0 < area_m2 or heat_cop <= 0:
        raise ValueError('Invalid area, COP or production retention')
    if min(storage_m3, freshwater_m3, ro_kwh_m3, ro_heat_kwh_th_m3) < 0:
        raise ValueError('Negative resource coefficient')
    if not 0 <= minimum_crop_share <= .2:
        raise ValueError('minimum_crop_share must be between zero and 0.2')
    if energy_limit_kwh is not None and (isinstance(energy_limit_kwh, bool)
            or not isinstance(energy_limit_kwh, (int, float))
            or not np.isfinite(energy_limit_kwh) or energy_limit_kwh < 0):
        raise ValueError('Invalid energy limit')
    if not options:
        return {'status': 'infeasible', 'reason': 'Seçilen koşullarda nicel hesabı desteklenen aday kalmadı.', 'allocations': []}
    inflow = np.asarray(inflow_m3 if inflow_m3 is not None else [0.]*12, dtype=float)
    if inflow.shape != (12,) or not np.isfinite(inflow).all() or min(inflow) < 0:
        raise ValueError('Twelve finite nonnegative monthly inflows required')
    n = len(options)
    output_factors, purpose_metadata = purpose_coefficients(options, production_purpose)
    # area, rain use, desalinated product, freshwater, end storage, spill, regret
    rain, sea, fresh, stock, spill, z = [n + 12*k for k in range(6)]
    size = z + 1
    vector = lambda: np.zeros(size)
    water, heat, electricity, energy = (vector() for _ in range(4))
    for i, o in enumerate(options):
        monthly = np.asarray(o['water_monthly_m3_m2'], dtype=float)
        vals = [o['yield_kg_m2'], o['heat_kwh_th_m2'], o['electricity_kwh_m2'], *monthly]
        if monthly.shape != (12,) or not np.isfinite(vals).all() or min(vals) < 0 or o['yield_kg_m2'] <= 0:
            raise ValueError('Option coefficients must be finite, nonnegative and have positive yield')
        water[i] = sum(monthly)
        heat[i], electricity[i] = o['heat_kwh_th_m2'], o['electricity_kwh_m2']
        energy[i] = heat[i] / heat_cop + electricity[i]
    energy[sea:sea+12] = ro_kwh_m3 + ro_heat_kwh_th_m3 / heat_cop
    electricity[sea:sea+12] = ro_kwh_m3
    heat[sea:sea+12] = ro_heat_kwh_th_m3
    ub, rhs, eq, equal = [], [], [], []
    area = vector(); area[:n] = 1
    ub.append(area); rhs.append(area_m2)
    annual_fresh = vector(); annual_fresh[fresh:fresh+12] = 1
    ub.append(annual_fresh); rhs.append(freshwater_m3)
    if energy_limit_kwh is not None:
        if not np.isfinite(energy_limit_kwh) or energy_limit_kwh < 0:
            raise ValueError('Invalid energy limit')
        ub.append(energy); rhs.append(energy_limit_kwh)
    for m in range(12):
        row = vector()
        row[:n] = [o['water_monthly_m3_m2'][m] for o in options]
        row[rain+m] = row[sea+m] = row[fresh+m] = -1
        eq.append(row); equal.append(0.)
        row = vector(); row[stock+m] = row[rain+m] = row[spill+m] = 1
        if m: row[stock+m-1] = -1
        eq.append(row); equal.append(inflow[m])
    bounds = [(0., None)]*size
    for m in range(12):
        bounds[stock+m] = (0., storage_m3)
        if not desalination: bounds[sea+m] = (0., 0.)
    crops = sorted({o['crop_id'] for o in options})
    if minimum_crop_share*len(crops) > 1+1e-12:
        raise ValueError('Minimum crop shares exceed available area; reduce minimum_crop_share or active crops')
    outputs, crop_areas = {}, {}
    for crop in crops:
        row = vector()
        row[:n] = [o['yield_kg_m2'] if o['crop_id'] == crop else 0. for o in options]
        outputs[crop] = row
        crop_area = vector(); crop_area[:n] = [float(o['crop_id'] == crop) for o in options]
        crop_areas[crop] = crop_area
        ub.append(-crop_area); rhs.append(-minimum_crop_share*area_m2)

    def run(cost, extra=()):
        rows = ub + [r for r, _ in extra]
        values = rhs + [v for _, v in extra]
        return linprog(cost, A_ub=np.array(rows), b_ub=values, A_eq=np.array(eq),
                       b_eq=np.array(equal), bounds=bounds, method='highs')

    mass = sum(outputs.values())
    output = vector()
    output[:n] = [o['yield_kg_m2']*factor for o, factor in zip(options, output_factors)]
    first = run(-output)
    if not first.success:
        return {'status': 'infeasible', 'reason': 'Açık çeşitlilik tabanları, su, alan ve enerji sınırları birlikte sağlanamıyor.', 'allocations': [],
                'minimum_crop_share': minimum_crop_share, 'objective': objective}
    maximum_output = float(output @ first.x)
    if maximum_output <= 1e-8:
        return {'status': 'infeasible', 'reason': 'Mevcut su ve enerji sınırlarında pozitif üretim sağlanamıyor.', 'allocations': []}
    maximum_mass = float(mass @ first.x) if production_purpose == 'fresh_mass' else float(mass @ run(-mass).x)
    production_floor = BALANCED_MASS_RETENTION*maximum_output
    floors = [(-output, -production_floor)]

    def tolerance(value):
        return max(1e-8,abs(value)*1e-9)

    def lexicographic(targets, extra):
        constraints = list(extra)
        result = None
        for target in targets:
            result = run(target, constraints)
            if not result.success:
                raise ValueError('Lexicographic follow-up failed: '+result.message)
            optimum = float(target @ result.x)
            constraints.append((target, optimum+tolerance(optimum)))
        return result, constraints

    # Payoff anchors use the SAME production/diversity/physical feasible set.
    # The secondary objective removes arbitrary alternative-optimum anchors.
    water_anchor,_ = lexicographic([water,energy],floors)
    energy_anchor,_ = lexicographic([energy,water],floors)
    min_water, min_energy = float(water@water_anchor.x), float(energy@energy_anchor.x)
    water_at_energy, energy_at_water = float(water@energy_anchor.x), float(energy@water_anchor.x)
    anchors = {
        'water': {'unit':'m³','minimum':min_water,'at_other_minimum':water_at_energy},
        'energy': {'unit':'kWh electric equivalent','minimum':min_energy,'at_other_minimum':energy_at_water},
    }
    regret_constraints = list(floors)
    for target, name in [(water,'water'),(energy,'energy')]:
        anchor = anchors[name]
        span = max(0.,anchor['at_other_minimum']-anchor['minimum'])
        anchor['normalization_span'] = span
        if span <= max(1e-7,abs(anchor['minimum'])*1e-7):
            # Both resource optima coincide in this dimension. Pin its common
            # minimum; dividing by ~zero or ignoring it would reward waste.
            regret_constraints.append((target,anchor['minimum']+tolerance(anchor['minimum'])))
            anchor['active_regret_dimension'] = False
        else:
            row = target/span; row[z] = -1
            regret_constraints.append((row,anchor['minimum']/span))
            anchor['active_regret_dimension'] = True
    regret = vector(); regret[z] = 1
    balanced, _ = lexicographic([regret,-output,energy,water],regret_constraints)
    balanced_x = balanced.x.copy()
    chosen = balanced
    if objective != 'balanced':
        resource_floors = [(-row,-float(row@balanced_x)*production_retention) for row in outputs.values()]
        chosen,_ = lexicographic([water,energy] if objective=='water' else [energy,water],resource_floors)
    x = chosen.x
    clean = lambda v: float(max(0., v))
    allocations = []
    for i, o in enumerate(options):
        if x[i] < 1e-5: continue
        allocations.append({**o, 'area_m2': clean(x[i]), 'share_pct': clean(100*x[i]/area_m2),
                            'production_kg': clean(x[i]*o['yield_kg_m2']),
                            'water_m3': clean(x[i]*water[i]),
                            'heat_kwh_th': clean(x[i]*heat[i]),
                            'electricity_kwh': clean(x[i]*o['electricity_kwh_m2'])})
    monthly = [{'month': m+1, 'capture_m3': float(inflow[m]), 'stored_water_used_m3': clean(x[rain+m]),
                'desalinated_m3': clean(x[sea+m]), 'freshwater_m3': clean(x[fresh+m]),
                'storage_end_m3': clean(x[stock+m]), 'spill_m3': clean(x[spill+m]),
                'demand_m3': clean(sum(x[i]*o['water_monthly_m3_m2'][m] for i,o in enumerate(options)))} for m in range(12)]
    total = {'area_m2': clean(area @ x), 'production_kg': sum(a['production_kg'] for a in allocations),
             'water_m3': clean(water @ x), 'heat_kwh_th': clean(heat @ x),
             'electricity_kwh': clean(electricity @ x), 'equivalent_electricity_kwh': clean(energy @ x),
             'stored_water_m3': clean(sum(x[rain:rain+12])), 'desalinated_m3': clean(sum(x[sea:sea+12])),
             'freshwater_m3': clean(sum(x[fresh:fresh+12])),
             'treatment_electricity_kwh': clean(sum(x[sea:sea+12])*ro_kwh_m3),
             'treatment_heat_kwh_th': clean(sum(x[sea:sea+12])*ro_heat_kwh_th_m3)}
    nutrition = nutritional_outputs(allocations)
    total.update(nutrition)
    total['selected_production_output'] = clean(output @ x)
    constraints = []
    def resource_constraint(name, used, limit, unit, *, report_zero_limit=False):
        if limit is None:
            return
        tolerance = max(1e-4, abs(limit) * 1e-6)
        binding = abs(used-limit) <= tolerance
        constraints.append({'name': name, 'used': used, 'limit': limit,
                            'slack': max(0., limit-used), 'unit': unit, 'binding': binding,
                            'reported_as_binding': binding and (limit > 0 or report_zero_limit)})
    resource_constraint('Yetiştirme alanı', total['area_m2'], area_m2, 'm²')
    resource_constraint('Enerji sınırı', total['equivalent_electricity_kwh'], energy_limit_kwh,
                        'kWh elektrik eşdeğeri', report_zero_limit=True)
    resource_constraint('Karasal su tahsisi', total['freshwater_m3'], freshwater_m3, 'm³')
    resource_constraint('Depolama hacmi', max(m['storage_end_m3'] for m in monthly), storage_m3, 'm³')
    return {'status': 'conditional' if total['production_kg'] > 1e-6 else 'infeasible',
            'allocations': allocations, 'totals': total, 'monthly': monthly,
            'crop_outputs_kg': {crop: clean(row @ x) for crop,row in outputs.items()},
            'balanced_crop_outputs_kg': {crop: clean(row @ balanced_x) for crop,row in outputs.items()},
            'objective': objective, 'production_retention': production_retention,
            'minimum_crop_share':minimum_crop_share,
            'production_purpose': purpose_metadata,
            'crop_areas_m2':{crop:clean(row@x) for crop,row in crop_areas.items()},
            'objective_policy': {
                'name':'diversity_selected_output_resource_minimax_regret',
                'production_purpose':production_purpose,
                'selected_output_label':purpose_metadata['label'],
                'selected_output_unit':purpose_metadata['unit'],
                'maximum_selected_output':maximum_output,
                'balanced_output_retention':BALANCED_MASS_RETENTION,
                'balanced_selected_output_floor':production_floor,
                'balanced_selected_output':clean(output@balanced_x),
                'minimum_crop_share':minimum_crop_share,
                'minimum_area_per_active_crop_m2':minimum_crop_share*area_m2,
                'balanced_mass_retention':BALANCED_MASS_RETENTION,
                'maximum_fresh_mass_kg':maximum_mass,
                'balanced_mass_floor_kg':production_floor if production_purpose=='fresh_mass' else None,
                'balanced_fresh_mass_kg':clean(mass@balanced_x),
                'balanced_max_normalized_regret':clean(balanced_x[z]),
                'regret_anchors':anchors,
                'tie_breaks':['maximize selected production output at optimum regret','minimize equivalent energy','minimize water'],
                'resource_mode_floor':'each crop amount of the newly calculated balanced plan × production_retention, with the same diversity area floor',
                'interpretation':'The explicitly selected single output is maximized; this is not nutritional adequacy, economic profit or validated Arctic harvest. A 5% maximum-output concession is a declared planning policy, not a fitted scientific weight. Protein is crude composition-table protein, not digestible protein. Food kcal are distinct from facility kWh.',
            },
            'binding_constraints': [c['name'] for c in constraints if c['reported_as_binding']],
            'resource_constraints': constraints,
            'solver': {'name': 'SciPy / HiGHS', 'version': VERSION, 'max_equality_residual': float(max(abs(np.array(eq) @ x-equal)))},
            'policy': f'Dengeli: her etkin ürüne toplam alanın en az %{100*minimum_crop_share:g} payı; seçilen {purpose_metadata["label"].lower()} maksimumunun %95’ini koru; ayrı su ve enerji optimumları arasındaki en büyük normalize kaybı küçült. Eşit ürün payı veya gizli ağırlık yok. Su/enerji önceliği yeni dengeli ürün miktarlarının seçilen payını korur. Tam beslenme, gelir veya talep optimumu değildir.'}
