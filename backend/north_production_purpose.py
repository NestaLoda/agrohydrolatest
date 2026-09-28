"""Explicit, single-metric production objectives and sourced food composition.

There are no dietary reference targets, hidden nutrient weights, invented prices
or assumed local demand. These coefficients transfer generic edible composition
to modeled fresh harvest and must not be called measured Arctic nutrition.
"""
import json
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / 'data/north/food_composition.json'
PURPOSES = {
    'fresh_mass': {'label': 'Taze ürün miktarı', 'unit': 'kg', 'coefficient': None},
    'protein': {'label': 'Bitkisel protein miktarı', 'unit': 'g protein', 'coefficient': 'protein_g_per_100g_edible'},
    'food_energy': {'label': 'Besin enerjisi', 'unit': 'kcal food', 'coefficient': 'food_kcal_per_100g_edible'},
}


def composition():
    return json.loads(PATH.read_text(encoding='utf-8'))


def purpose_coefficients(options, purpose):
    if purpose not in PURPOSES:
        raise ValueError('Unknown production purpose')
    metadata = composition()
    by_crop = {row['crop_id']: row for row in metadata['crops']}
    factor_key = PURPOSES[purpose]['coefficient']
    factors = []
    for option in options:
        if factor_key is None:
            factors.append(1.)
        else:
            row = by_crop.get(option['crop_id'])
            if row is None:
                raise ValueError('Sourced edible composition required for crop: '+option['crop_id'])
            factors.append(10*row[factor_key])  # 1 kg = ten 100 g edible portions.
    return factors, {**PURPOSES[purpose], 'id': purpose,
                     'source': metadata['provider'], 'source_url': metadata['documentation_url'],
                     'coefficients': [by_crop[crop] for crop in sorted({o['crop_id'] for o in options}) if crop in by_crop],
                     'limitation': 'Raw edible composition × modeled harvest; not balanced nutrition, consumer demand, profit, digestible protein or locally measured food quality.'}


def nutritional_outputs(allocations):
    rows = {row['crop_id']: row for row in composition()['crops']}
    known = [a for a in allocations if a['crop_id'] in rows]
    return {'protein_kg': sum(a['production_kg']*rows[a['crop_id']]['protein_g_per_100g_edible']/100 for a in known),
            'food_energy_kcal': sum(a['production_kg']*rows[a['crop_id']]['food_kcal_per_100g_edible']*10 for a in known),
            'composition_covered_production_kg': sum(a['production_kg'] for a in known),
            'complete_composition_coverage': len(known) == len(allocations)}
