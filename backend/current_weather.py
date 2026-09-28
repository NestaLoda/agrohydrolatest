"""Timestamped weather context, deliberately excluded from seasonal optimization."""
import json
import math
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import urlopen
from scripts.ingest_data import SITES
from .provenance import ROOT, digest, immutable_write
from .runtime import writable_path, SERVERLESS

_cache = {}

def current_weather(region_id):
    site = next((s for s in SITES[:5] if s['site_id'] == region_id), None)
    if site is None:
        raise ValueError('Kayıtlı Türkiye bölgesi gerekli.')
    now = datetime.now(timezone.utc)
    previous = _cache.get(region_id)
    if previous and (now - previous[0]).total_seconds() < 600:
        return previous[1]
    url = 'https://api.open-meteo.com/v1/forecast?' + urlencode({
        'latitude':site['latitude'], 'longitude':site['longitude'],
        'current':'temperature_2m', 'timezone':'UTC', 'forecast_days':1})
    try:
        raw = urlopen(url, timeout=6).read()
        p = json.loads(raw)
        value = p['current']['temperature_2m']
        if isinstance(value, bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
            raise ValueError('Sıcaklık eksik veya geçersiz.')
        if p['current_units']['temperature_2m'] != '°C' or p['utc_offset_seconds'] != 0:
            raise ValueError('Birim veya zaman dilimi uyuşmuyor.')
        stamp = datetime.fromisoformat(p['current']['time']).replace(tzinfo=timezone.utc)
        if abs((now-stamp).total_seconds()) > 7200:
            raise ValueError('Sağlayıcı zaman damgası güncel değil.')
        sha = digest(raw)
        path = f'data/raw/current_weather/{region_id}_{sha}.json'
        immutable_write(writable_path(path, local_root=ROOT), raw)
        result = {'status':'available','region_id':region_id,'temperature_c':value,
            'valid_at':stamp.isoformat(),'retrieved_at':now.isoformat(),
            'classification':'MODEL_NOWCAST','source_url':url,'provider':'Open-Meteo',
            'sha256':sha,'local_raw_path':path,'used_in_optimizer':False,
            'storage_scope':'ephemeral' if SERVERLESS else 'local_persistent',
            'note':'Güncel model hava bilgisi; istasyon ölçümü veya sezonluk iklim yerine geçmez.'}
        snapshot = writable_path(f'data/metadata/snapshots/weather_{region_id}_{sha}.json', local_root=ROOT)
        if not snapshot.exists():
            immutable_write(snapshot,json.dumps(result,ensure_ascii=False,sort_keys=True).encode('utf-8'))
        _cache[region_id] = (now,result)
        return result
    except (OSError,ValueError,KeyError,TypeError):
        return {'status':'unavailable','region_id':region_id,'temperature_c':None,
            'used_in_optimizer':False,'note':'Güncel hava bilgisi alınamadı; sezon hesabı kaynaklı ERA5 ile devam eder.'}
