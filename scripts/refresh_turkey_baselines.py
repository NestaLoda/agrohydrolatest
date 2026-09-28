from pathlib import Path
import json,hashlib
if (Path.cwd()/'data/agriculture/snapshots/manifest_before_teslim008.json').exists():
 raise SystemExit('TESLIM008 source migration already recorded; do not replay.')
root=Path.cwd(); folder=root/'data/agriculture';p=folder/'region_baselines.json';raw=p.read_bytes();h=hashlib.sha256(raw).hexdigest();(folder/'snapshots').mkdir(exist_ok=True);(folder/'snapshots'/f'region_baselines_{h}.json').write_bytes(raw);(folder/'snapshots'/'manifest_before_teslim008.json').write_bytes((folder/'manifest.json').read_bytes())
d=json.loads(raw);downloads=json.loads((root/'docs/verification/turkey-reference/new-source-downloads.json').read_text())
for r in d['regions']:
 if r['region_id'] not in ['konya','gediz_manisa']:continue
 src=downloads[0 if r['region_id']=='konya' else 1]; old=r['sources'][0];sid=src['key']+'_'+src['sha256'][:12]
 r['sources']=[{**old,**{k:src[k] for k in ['url','sha256','local_path']},'id':sid,'title':'Konya Tarımı — Ocak 2026' if r['region_id']=='konya' else 'Manisa 2025 Yılı Faaliyet Raporu','year':2026 if r['region_id']=='konya' else 2025,'data_year':2024,'page':'PDF/basılı s.11–12, Tablo4, 2024 sütunları' if r['region_id']=='konya' else 'PDF/basılı s.24, Tablo9, 2024 sütunları'}]
 r['year']=2024
 values={'wheat':(6378828,1824540),'barley':(3517522,891907),'maize_grain':(1589939,2011729),'sugar_beet':(850642,6971829),'potato':(187849,753717)} if r['region_id']=='konya' else {'wheat':(776594,196893),'barley':(355479,74365),'cotton':(146791,81684),'maize_grain':(135971,151830)}
 for c in r['crops']:
  a,t=values[c['crop_id']];c.update(area_ha=a/10,production_tonnes=t,yield_kg_ha=t*1000/(a/10),source_id=sid,original_area_value=a,original_area_unit='da',aggregation_note='2024 tablosundaki ürün satırı; verim üretim/alan hesabıyla türetildi. Silaj/yeşil ot ayrı tutuldu.')
  if r['region_id']=='konya' and c['crop_id'] in ['wheat','barley']:
   c['name_tr']='Buğday' if c['crop_id']=='wheat' else 'Arpa'; c['source_reported_yield_kg_da']=323 if c['crop_id']=='wheat' else 407;c['aggregation_note']+=' Kaynakta hazır verim sütunu alan ve üretimle tutarsız; motor hazır verimi kullanmaz. Alt tür toplamı ayrıca eklenmedi.'
 r['selected_crop_area_ha']=sum(c['area_ha'] for c in r['crops'])
 if r['region_id']=='konya':r['limitations'].append('2026 yayınındaki 2024 alan/üretim tablosu kullanıldı. Buğday ve arpa hazır verim sütunu üretim/alan ile tutarsızdır; hesaplanmış verim kullanılır, kaynak hatası yerel doğrulama ihtiyacını artırır.')
 r['freshness_review']={'checked_on':'2026-09-22','note':'Yeni yayın kontrol edildi; tablo veri yılı 2024. Canlı 2026 ürün sayımı değildir.'}
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');m=json.loads((folder/'manifest.json').read_text());m['files']['region_baselines.json']['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();(folder/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=root/'tests/test_agriculture.py';s=p.read_text(encoding='utf-8').replace('("Konya", 2023)','("Konya", 2024)');p.write_text(s,encoding='utf-8')
print([(r['region_id'],r['year'],r['selected_crop_area_ha']) for r in d['regions']])
