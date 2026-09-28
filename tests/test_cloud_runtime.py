from fastapi.testclient import TestClient

import backend.app as application
from backend.runtime import ROOT, writable_path


def test_local_runtime_retains_project_storage():
    assert writable_path('data/metadata/provenance.sqlite') == ROOT / 'data/metadata/provenance.sqlite'


def test_cloud_blocks_durable_evidence_writes_but_keeps_calculations(monkeypatch):
    monkeypatch.setattr(application, 'SERVERLESS', True)
    client = TestClient(application.app)
    for path in ['/api/north/freeze', '/api/north/observe', '/api/pwn/analyze',
                 '/api/north/validation/pilot/freeze', '/api/north/validation/pilot/compare']:
        response = client.post(path, json={})
        assert response.status_code == 409
        assert 'kalıcı saha kaydı tutulmaz' in response.json()['detail']
    assert client.get('/api/health').json()['persistent_field_records'] is False
    context = client.get('/api/planning-context?region_id=konya')
    assert context.status_code == 200
    result = client.post('/api/simulate', json=context.json()['default_scenario'])
    assert result.status_code == 200
    assert 'optimized' in result.json()
