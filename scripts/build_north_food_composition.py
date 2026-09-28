"""Curate the six eligible crops from archived official Matvaretabellen API data.

Download the documented API foods/nutrients/sources JSON to food_composition/
before running. This script does not invent missing nutrient values.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / 'data/north/food_composition'
MAPPING = {'lettuce': '06.058', 'arugula': '06.100', 'radish': '06.054',
           'kohlrabi': '06.086', 'swiss_chard': '06.092', 'basil': '06.111'}


def main():
    foods = {f['foodId']: f for f in json.loads((DIR/'foods.json').read_text())['foods']}
    rows = []
    for crop, food_id in MAPPING.items():
        food = foods[food_id]
        protein = next(c for c in food['constituents'] if c['nutrientId'] == 'Protein')
        assert protein['unit'] == 'g' and food['calories']['unit'] == 'kcal'
        rows.append({'crop_id': crop, 'food_id': food_id, 'food_name': food['foodName'],
                     'url': food['uri'], 'protein_g_per_100g_edible': protein['quantity'],
                     'food_kcal_per_100g_edible': food['calories']['quantity'],
                     'protein_source_id': protein['sourceId'],
                     'food_energy_source_id': food['calories']['sourceId'],
                     'original_edible_percent': food['ediblePart']['percent'],
                     'mapping_status': 'SPECIES_RAW_EDIBLE_ANALOGUE',
                     'limitation': 'Not cultivar-specific Arctic composition. Existing yield is edible fresh mass; edible percentage is NOT applied a second time. No post-harvest/cooking loss or protein digestibility correction.'})
    manifest = {'schema_version': '1.0', 'retrieved_on': '2026-09-23',
                'provider': 'Norwegian Food Safety Authority / Matvaretabellen',
                'documentation_url': 'https://www.matvaretabellen.no/en/api/',
                'basis': 'Per 100 g raw edible food; food energy is distinct from facility electricity.',
                'classification': 'SOURCED_FOOD_COMPOSITION / MODELED_TRANSFER_TO_POLAR_YIELD',
                'raw_files': [{'path': 'data/north/food_composition/'+name,
                               'url': 'https://www.matvaretabellen.no/api/en/'+name,
                               'sha256': hashlib.sha256((DIR/name).read_bytes()).hexdigest()}
                              for name in ('foods.json', 'nutrients.json', 'sources.json')],
                'crops': rows}
    (ROOT/'data/north/food_composition.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f'Curated {len(rows)} crops with archived source hashes')


if __name__ == '__main__':
    main()
