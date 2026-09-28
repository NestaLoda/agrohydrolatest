from pathlib import Path
import json,csv
from scripts.ingest_data import acquire,SITES,VARIABLES
root=Path.cwd();datasets=[]; rows=[]
for site in SITES[:5]:
 m,p=acquire(site,False,'2024-01-01','2025-12-31');datasets.append(m)
 for i,d in enumerate(p['daily']['time']): rows.append({'site_id':site['site_id'],'date':d,**{v:p['daily'][k][i] for k,v in VARIABLES.items()},'dataset_id':m['dataset_id']})
 print(site['site_id'],m['row_count'],flush=True)
(root/'data/manifest_turkey_recent.json').write_text(json.dumps({'schema_version':'1.0','datasets':datasets},ensure_ascii=False,indent=2),encoding='utf-8')
with (root/'data/processed/climate_turkey_recent.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
