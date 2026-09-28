import io
import json
from datetime import datetime, timezone, timedelta
import pytest
from backend import current_weather as weather
from backend.repository import load_verified_climate
from backend.planning import planning_context, simulate
from backend.planning_contracts import SimulationRequest

def test_recent_climate_is_complete_and_separate_from_historical_package():
    recent=load_verified_climate(recent=True)
    old=load_verified_climate()
    assert len(recent)==3655 and len(old)==4380
    assert recent.date.min().strftime('%Y-%m-%d')=='2024-01-01'
    assert recent.date.max().strftime('%Y-%m-%d')=='2025-12-31'
    assert set(recent.site_id)=={'konya','seyhan_adana','gediz_manisa','gap_sanliurfa','trakya_edirne'}
    assert not set(recent.dataset_id)&set(old.dataset_id)
    assert not recent.isna().any().any()
    q=SimulationRequest.model_validate(planning_context('konya')['default_scenario'])
    result=simulate(q)
    assert all('2024_2025' in x['dataset_id'] for x in result['crop_water'])
    assert all('2024_2025' in x['id'] for x in result['provenance']['climate_datasets'])

@pytest.mark.parametrize('kind',['ok','stale','null','wrong_unit','offline'])
def test_current_weather_is_timestamped_and_never_a_season_input(monkeypatch,tmp_path,kind):
    weather._cache.clear();monkeypatch.setattr(weather,'ROOT',tmp_path)
    stamp=datetime.now(timezone.utc)-(timedelta(days=1) if kind=='stale' else timedelta())
    payload={'current':{'time':stamp.replace(tzinfo=None).isoformat(),'temperature_2m':None if kind=='null' else 18.5},'current_units':{'temperature_2m':'K' if kind=='wrong_unit' else '°C'},'utc_offset_seconds':0}
    def fetch(*args,**kwargs):
        if kind=='offline':raise OSError('offline')
        return io.BytesIO(json.dumps(payload).encode())
    monkeypatch.setattr(weather,'urlopen',fetch)
    result=weather.current_weather('konya')
    assert result['used_in_optimizer'] is False
    assert result['status']==('available' if kind=='ok' else 'unavailable')
    if kind=='ok':
        assert result['temperature_c']==18.5
        assert (tmp_path/result['local_raw_path']).exists()
    else:assert result['temperature_c'] is None

def test_current_weather_rejects_unregistered_coordinates():
    with pytest.raises(ValueError):weather.current_weather('../unknown')
