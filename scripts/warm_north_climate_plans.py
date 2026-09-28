"""Prepare five remaining source-backed contexts; test agent owns mid245/late585.

This is an operational cache preparation, not independent scientific validation.
Outputs retain durations, climate/evidence hashes, solver status and resource totals.
"""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.north_contracts import NorthRequest
from backend.north_planning import plan_north

OUT = ROOT / 'data/north/rebuild_climate'
SELECTIONS = [('historical', 'ssp245'), ('near', 'ssp245'), ('near', 'ssp585'), ('mid', 'ssp585'), ('late', 'ssp245')]


def main():
    results = []
    for horizon, scenario in SELECTIONS:
        began = time.monotonic()
        try:
            result = plan_north(NorthRequest(horizon_id=horizon, scenario_id=scenario), with_sensitivity=False)
            row = {'horizon': horizon, 'scenario': scenario, 'seconds': round(time.monotonic() - began, 3),
                   'status': result['plan']['status'], 'totals': result['plan'].get('totals'),
                   'climate_manifest_sha256': result['provenance']['climate_manifest_sha256'],
                   'evidence_sha256': result['provenance']['evidence_sha256'], 'classification': result['classification']}
        except Exception as exc:
            row = {'horizon': horizon, 'scenario': scenario, 'seconds': round(time.monotonic() - began, 3),
                   'status': 'error', 'error': str(exc)}
        results.append(row)
        print(json.dumps(row, ensure_ascii=False), flush=True)
        (OUT / 'plan-prewarm.json').write_text(json.dumps({'completed_at_utc': datetime.now(timezone.utc).isoformat(),
            'complete': len(results) == len(SELECTIONS), 'with_sensitivity': False, 'contexts': results}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if any(row['status'] == 'error' for row in results):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
