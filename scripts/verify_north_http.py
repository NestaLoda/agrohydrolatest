"""Read-only smoke verification of all seven sourced North contexts on localhost."""
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/verification/north-rebuild'


def post(path, body):
    request = Request('http://127.0.0.1:8011/api/north/' + path,
                      json.dumps(body).encode(), {'Content-Type': 'application/json'})
    with urlopen(request, timeout=180) as response:
        return json.load(response)


def main():
    rows = []
    contexts = [('historical', 'ssp245')] + [
        (h, s) for h in ('near', 'mid', 'late') for s in ('ssp245', 'ssp585')]
    for horizon, scenario in contexts:
        result = post('plan', {'horizon_id': horizon, 'scenario_id': scenario})
        plan = result['plan']
        totals = plan['totals']
        assert len(result['climate']['models']) == 3
        assert len(plan['monthly']) == 12
        assert len([v for v in plan['crop_outputs_kg'].values() if v > 0]) == 6
        assert abs(totals['water_m3'] - sum(totals[k] for k in
            ('stored_water_m3', 'desalinated_m3', 'freshwater_m3'))) < 1e-5
        rows.append({'horizon': horizon, 'scenario': scenario,
                     'period': result['climate']['period'], 'status': plan['status'],
                     'totals': totals, 'provenance': result['provenance']})
        if (horizon, scenario) in [('mid', 'ssp245'), ('late', 'ssp585')]:
            name = 'default-plan.json' if horizon == 'mid' else 'late585-plan.json'
            (OUT / name).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    demo = post('demo', {})
    assert demo['classification'] == 'SIMULATION_EXPLANATORY'
    assert 'future_climate' in demo['unchanged_inputs']
    report = {'verified_at_utc': datetime.now(timezone.utc).isoformat(),
              'contexts': rows, 'synthetic_comparison': demo}
    (OUT / 'http-smoke.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'{len(rows)}/7 HTTP contexts verified; explicitly synthetic same-engine comparison passed.')


if __name__ == '__main__':
    main()
