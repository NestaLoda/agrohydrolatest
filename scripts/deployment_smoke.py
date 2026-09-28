"""Exercise a deployed full-stack app without creating durable field records."""
import argparse
from datetime import datetime, timezone
from io import BytesIO
import json
from pathlib import Path
import time

import httpx
from pypdf import PdfReader


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('--output', default='docs/verification/deployment-033/api-smoke.json')
    args = parser.parse_args()
    report = {'url': args.url, 'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'checks': []}
    with httpx.Client(base_url=args.url.rstrip('/'), timeout=300, follow_redirects=True) as client:
        def check(method, path, body=None, pdf=False, expected=200):
            start = time.monotonic()
            response = client.request(method, path, json=body) if body is not None else client.request(method, path)
            entry = {'method': method, 'path': path, 'status': response.status_code,
                     'seconds': round(time.monotonic()-start, 2), 'bytes': len(response.content)}
            report['checks'].append(entry)
            assert response.status_code == expected, (entry, response.text[:500])
            if pdf:
                assert response.content.startswith(b'%PDF-')
                reader = PdfReader(BytesIO(response.content))
                text = '\n'.join(page.extract_text() for page in reader.pages)
                assert 'model' in text.lower()
                entry['pages'] = len(reader.pages)
                out = Path(args.output).parent / ('turkiye.pdf' if 'turkiye' in path else 'north.pdf')
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(response.content)
                return None
            return response.json() if 'application/json' in response.headers.get('content-type', '') else response.text

        try:
            html = check('GET', '/')
            assert 'root' in html
            health = check('GET', '/api/health')
            assert health['status'] == 'ok' and health['persistent_field_records'] is False
            for path in ['/api/overview', '/api/sources', '/api/benchmarks', '/api/north-context',
                         '/api/north-evidence', '/api/north/status', '/api/north/validation/readiness']:
                check('GET', path)
            for region in ['konya', 'gediz_manisa']:
                context = check('GET', '/api/planning-context?region_id='+region)
                scenario = context['default_scenario']
                result = check('POST', '/api/simulate', scenario)
                assert result['optimized']['crops']
                if region == 'konya':
                    check('POST', '/api/decision-report/turkiye', scenario, pdf=True)
            north_request = {'target_year': 2051}
            result = check('POST', '/api/north/plan', north_request)
            assert result['plan']['totals']['water_m3'] > 0
            report['north_totals'] = result['plan']['totals']
            check('POST', '/api/north/reference', north_request)
            check('POST', '/api/north/report', north_request, pdf=True)
            check('POST', '/api/north/freeze', {}, expected=409)
            report['passed'] = True
        except Exception as exc:
            report['passed'] = False
            report['error'] = str(exc)
            raise
        finally:
            output = Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
            print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
