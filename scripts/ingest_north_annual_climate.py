"""Fill the missing 2061–2080 source years; publish a separate 2026–2100 package.

Reuses verified NASA NCSS acquisition and unit/calendar validation. Legacy
20-year datasets/manifests are not changed. No interpolation or rescaling.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
import pandas as pd
import numpy as np
from ingest_north_rebuild_climate import (ROOT, OUT, MODELS, VARIABLES, SITES,
    acquire, catalog, parse_raw, period_metrics, sha, write_json)

ANNUAL = OUT / 'annual'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--offline', action='store_true')
    parser.add_argument('--workers', type=int, default=8, choices=range(1,9))
    args = parser.parse_args()
    jobs = []
    for model in MODELS:
        for scenario in ('ssp245','ssp585'):
            for var in VARIABLES:
                entries = catalog(model,scenario,var,args.offline)
                jobs += [('longyearbyen',model,scenario,var,year,entries[year]) for year in range(2061,2081)]
    failures=[]; count=0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures={pool.submit(acquire,job,args.offline):job for job in jobs}
        for future in as_completed(futures):
            try: future.result(); count+=1
            except Exception as exc: failures.append({'job':futures[future][:-1],'error':str(exc)})
            if (count+len(failures))%24==0:
                progress={'ready':False,'downloaded_validated':count,'total':len(jobs),'failures':failures}
                write_json(ANNUAL/'acquisition_progress.json',progress)
                print(json.dumps(progress),flush=True)
    if failures: raise ValueError(f'{len(failures)} acquisitions failed; annual package not published')
    contexts=[]; raw_records=[]; outputs=[]
    for scenario in ('ssp245','ssp585'):
        for year in range(2026,2101):
            members=[]
            for model in MODELS:
                columns={}
                for var in VARIABLES:
                    path=OUT/'raw'/'longyearbyen'/model/scenario/f'{var}_{year}.nc'
                    raw=path.read_bytes(); meta=json.loads(path.with_suffix('.json').read_bytes())
                    if sha(raw)!=meta['sha256']: raise ValueError('Raw source hash mismatch')
                    dates,values,_=parse_raw(raw,var,year,'longyearbyen',model,scenario)
                    columns[var]=values; raw_records.append(meta)
                if (columns['tasmin']>columns['tasmax']).any(): raise ValueError('Tmin exceeds Tmax')
                frame=pd.DataFrame({'date':dates,'tmin_c':columns['tasmin']-273.15,'tmax_c':columns['tasmax']-273.15,
                                    'precipitation_mm':columns['pr']*86400,'shortwave_mj_m2':columns['rsds']*.0864})
                path=ANNUAL/'daily'/f'longyearbyen_{year}_{scenario}_{model}.csv.gz'
                path.parent.mkdir(parents=True,exist_ok=True)
                frame.to_csv(path,index=False,compression={'method':'gzip','mtime':0},float_format='%.8f')
                # Metrics are recomputed from the exact published precision.
                published=pd.read_csv(path,parse_dates=['date'])
                item={'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path.read_bytes()),'rows':len(frame)}
                outputs.append(item)
                members.append({'model':model,'member':'r1i1p1f1','daily_path':item['path'],'daily_sha256':item['sha256'],**period_metrics(published)})
            def band(rows,key):
                v=[r[key] for r in rows]
                return {'mean':float(np.mean(v)),'min':float(min(v)),'max':float(max(v))}
            contexts.append({'site_id':'longyearbyen','horizon_id':'year','target_year':year,'scenario_id':scenario,'period':[year,year],
                'years':1,'models':members,'ensemble':{k:band([m['summary'] for m in members],k) for k in members[0]['summary']},
                'monthly':[{'month':i+1,**{k:band([m['monthly'][i] for m in members],k) for k in members[0]['monthly'][i] if k!='month'}} for i in range(12)]})
    path=ANNUAL/'contexts.json'
    write_json(path,{'status':'ready','schema_version':'1.0','start_year':2026,'end_year':2100,'model_ids':MODELS,
                     'scenarios':['ssp245','ssp585'],'contexts':contexts})
    outputs.append({'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path.read_bytes())})
    write_json(ANNUAL/'manifest.json',{'status':'ready','schema_version':'1.0','created_at_utc':datetime.now(timezone.utc).isoformat(),
         'start_year':2026,'end_year':2100,'raw_file_count':len(raw_records),'raw_files':raw_records,'derived_files':outputs,
         'method':'Exact source-model Gregorian year. No temporal interpolation, no linear production scaling, no date-specific weather forecast.'})
    write_json(ANNUAL/'acquisition_progress.json',{'ready':True,'downloaded_validated':count,'total':len(jobs),'failures':[]})
    print(json.dumps({'ready':True,'contexts':len(contexts),'raw_files':len(raw_records),'daily_files':len(outputs)-1}),flush=True)

if __name__=='__main__': main()
