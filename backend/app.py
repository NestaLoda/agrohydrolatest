import json
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from .contracts import DecisionRequest, SensitivityRequest, BenchmarkRequest, FieldComparisonRequest, MODEL_VERSION
from .provenance import ROOT, ProvenanceStore, immutable_write, canonical, digest
from .repository import register_sources, overview, transfer, load_manifest, benchmarks, north_context
from .field import compare_field
from .optimizer import solve_decision
from .science import treatment_energy
from .pwn import analyze_profile, simulated_profile_csv
from .planning_contracts import SimulationRequest, PatternFieldUpdate
from .planning import simulate, planning_context, read_agriculture
from .runtime import SERVERLESS, writable_path
from fastapi.responses import JSONResponse

store=ProvenanceStore(writable_path("data/metadata/provenance.sqlite"))

@asynccontextmanager
async def lifespan(app):
    register_sources(store)
    for region in read_agriculture('region_baselines.json')['regions']:
        for source in region['sources']:
            raw=(ROOT/source['local_path']).read_bytes()
            store.register({'dataset_id':source['id'],'provider':source.get('publisher','Official agriculture statistics'),
               'source_url':source['url'],'classification':'OFFICIAL_STATISTICS','access_date':source['access_date'],
               'units':{'area':'ha','production':'tonnes','derived_yield':'kg/ha'},'license':source.get('license','Source terms'),
               'content_sha256':source['sha256'],'local_raw_path':source['local_path'],'title':source['title'],
               'year':region['year'],'geography':region['geography_name'],'page':source['page']},raw)
    yield

app=FastAPI(title="Sustainable Production Frontier",version=MODEL_VERSION,lifespan=lifespan)

@app.middleware('http')
async def persistent_records_require_local_storage(request, call_next):
    # A disposable serverless disk must never claim to preserve research evidence.
    persistent_paths = {'/api/pwn/analyze', '/api/pattern-field-update',
                        '/api/field-comparison', '/api/north/freeze',
                        '/api/north/observe', '/api/north/validation/pilot/freeze',
                        '/api/north/validation/pilot/compare'}
    if SERVERLESS and request.method == 'POST' and request.url.path.rstrip('/') in persistent_paths:
        return JSONResponse(status_code=409, content={'detail':
            'Bu çevrimiçi sürümde kalıcı saha kaydı tutulmaz. PWN yükleme ve PRE/POST kayıtları için yerel uygulamayı kullanın; simülasyon ve PDF hesapları çevrimiçi çalışır.'})
    return await call_next(request)

@app.get("/api/health")
def health():
    return {"status":"ok","version":MODEL_VERSION,"offline_core":True,
            "persistent_field_records":not SERVERLESS}

@app.get("/api/overview")
def get_overview():return overview()

@app.get('/api/current-weather/{region_id}')
def get_current_weather(region_id: str):
    from .current_weather import current_weather
    try:return current_weather(region_id)
    except ValueError as exc:raise HTTPException(status_code=422,detail=str(exc))

@app.get("/api/sources")
def sources():return {"datasets":store.datasets()}

@app.get("/api/transfer")
def get_transfer():
    try:return transfer()
    except ValueError as e:raise HTTPException(422,str(e)) from e

@app.post("/api/decision")
def decision(request:DecisionRequest):
    result=solve_decision(request)
    payload={"parameters":request.model_dump(),"model_version":MODEL_VERSION,
             "model_code_sha256":digest(b"".join((ROOT/"backend"/p).read_bytes() for p in ["contracts.py","science.py","optimizer.py"])),
             "literature_parameters_sha256":digest((ROOT/"data/literature_parameters.json").read_bytes()),
             "datasets":[{"id":d["dataset_id"],"sha256":d["content_sha256"]} for d in load_manifest()["datasets"]]}
    return {**result,"run_id":store.record_run(payload,result),"provenance":payload}

@app.get("/api/benchmarks")
def get_benchmarks():return benchmarks()

@app.post("/api/benchmark-comparison")
def compare_benchmarks(request:BenchmarkRequest):
    try:return benchmarks(request)
    except ValueError as e:raise HTTPException(422,str(e)) from e

@app.get("/api/north-context")
def get_north():
    try:return north_context()
    except ValueError as e:raise HTTPException(422,str(e)) from e

@app.post("/api/field-comparison")
def field_comparison(request:FieldComparisonRequest):
    try:
        result=compare_field(request,store)
        return {**result,"run_id":store.record_run({"parameters":request.model_dump(mode="json"),"model_version":MODEL_VERSION,
           "code_sha256":digest(b"".join((ROOT/"backend"/p).read_bytes() for p in ["contracts.py","field.py","pwn.py","optimizer.py","science.py"])),
           "literature_parameters_sha256":digest((ROOT/"data/literature_parameters.json").read_bytes())},result)}
    except ValueError as e:raise HTTPException(422,str(e)) from e

@app.post("/api/sensitivity")
def sensitivity(request:SensitivityRequest):
    if request.source_kind=="OUR_NEW_MEASUREMENT_TANK":
        raise HTTPException(422,"Tank kaydı deniz kaynak suyu sayılmaz. Bu panelde ayrı açıklayıcı deniz senaryosu seçin.")
    after=treatment_energy(request.temperature_C,request.salinity_sp)
    before=treatment_energy(request.reference_temperature_C,request.reference_salinity_sp)
    valid=after["interval_kwh_m3"] is not None and before["interval_kwh_m3"] is not None
    return {"status":"conditional" if valid else "insufficient_data","classification":"SIMULATION / EXPLANATORY",
        "input_source_kind":request.source_kind,"before":before,"after":after,"product_water_m3":request.product_water_m3,
        "energy_delta_kwh":None if not valid else (after["specific_energy_kwh_m3"]-before["specific_energy_kwh_m3"])*request.product_water_m3,
        "reason":"Bu, kaynak sıcaklığı duyarlılığıdır; gözlemle kalibre edilmiş Arktik modeli değildir. Tuzluluk yalnız bağlamda gösterilir.",
        "confidence":"Belirsizlik payı kullanıcı senaryosu; istatistiksel güven yüzdesi üretilmedi."}

@app.get("/api/pwn/example.csv")
def example_csv():
    return Response(simulated_profile_csv(),media_type="text/csv",headers={"Content-Disposition":"attachment; filename=SIMULATION_EXPLANATORY_profile.csv"})

@app.get("/api/pwn/example")
def example():return analyze_profile(simulated_profile_csv(),"SIMULATION_EXPLANATORY","arbitrary_unit","encoder_vertical_tank")

@app.post("/api/pwn/analyze")
async def pwn_analyze(file:UploadFile=File(...),source_kind:str=Form(...),raw_conductivity_unit:str=Form(...),
                      depth_method:str=Form("unavailable"),source_url:str=Form(""),provider:str=Form(""),license_or_permission:str=Form(""),temperature_kind:str=Form("unspecified")):
    if temperature_kind not in {"unspecified","in_situ","potential","conservative"}:raise HTTPException(422,"Sıcaklık tanımı tanınmıyor.")
    raw=await file.read(2_000_001)
    if len(raw)>2_000_000:raise HTTPException(413,"CSV 2 MB sınırını aşıyor.")
    if source_kind=="EXTERNAL_OBSERVATION" and not all([source_url,provider,license_or_permission]):
        raise HTTPException(422,"Dış gözlem için kaynak URL, sağlayıcı ve kullanım izni/lisans gerekli.")
    try:result=analyze_profile(raw,source_kind,raw_conductivity_unit,depth_method)
    except ValueError as e:raise HTTPException(422,str(e)) from e
    raw_path=ROOT/"data/pwn/raw"/(result["sha256"]+".csv")
    immutable_write(raw_path,raw)
    # Source bytes are immutable; different analysis declarations receive separate metadata versions.
    declaration={"source_kind":source_kind,"raw_unit":raw_conductivity_unit,"depth_method":depth_method,
                 "source_url":source_url,"provider":provider,"license":license_or_permission,"temperature_kind":temperature_kind}
    dataset_id="pwn_"+result["sha256"][:20]+"_"+digest(canonical(declaration).encode())[:12]
    prior=next((d for d in store.datasets() if d["dataset_id"]==dataset_id),None)
    metadata={"dataset_id":dataset_id,"content_sha256":result["sha256"],
              "provider":provider or ("team_declared" if source_kind=="OUR_NEW_MEASUREMENT_TANK" else "explicit_simulation"),
              "source_url":source_url or "local:pwn-upload","classification":source_kind,"access_date":prior["access_date"] if prior else datetime.now(timezone.utc).date().isoformat(),
              "units":{"raw_conductivity_signal":raw_conductivity_unit,"temperature_C":"°C","cable_out_m":"m"},
              "license":license_or_permission or "local-user-declared","local_raw_path":str(raw_path.relative_to(ROOT)),"depth_method":depth_method,"temperature_kind":temperature_kind}
    try:store.register(metadata,raw)
    except ValueError as e:raise HTTPException(409,str(e)) from e
    immutable_write(ROOT/"data/pwn/metadata"/(metadata["dataset_id"]+".json"),canonical(metadata).encode())
    return {**result,"dataset_id":metadata["dataset_id"],"raw_saved":True}

@app.get("/api/pilot-source")
def pilot_source():
    path=ROOT/"data/references/konya_original_report.pdf"
    if not path.exists():raise HTTPException(404,"Orijinal rapor bu bilgisayarda bulunamadı; docs kaynak kaydına bakın.")
    return FileResponse(path,media_type="application/pdf")

@app.get('/api/planning-context')
def get_planning_context(region_id:str='konya'):
    try:return planning_context(region_id)
    except ValueError as e:raise HTTPException(422,str(e)) from e

def recorded_simulation(request:SimulationRequest):
    result=simulate(request)
    return {**result,'run_id':store.record_run({'parameters':request.model_dump(mode='json'),'provenance':result['provenance']},result)}

@app.post('/api/simulate')
def run_simulation(request:SimulationRequest):
    try:return recorded_simulation(request)
    except ValueError as e:raise HTTPException(422,str(e)) from e

@app.post('/api/decision-report/turkiye')
def turkey_decision_report(request:SimulationRequest):
    if request.mode!='turkiye':raise HTTPException(422,'Türkiye raporu için Türkiye senaryosu gerekir.')
    from .decision_pdf import turkey_pdf
    try:
        result=simulate(request)
        context=planning_context(request.region_id)
        content=turkey_pdf(context,result)
    except ValueError as exc:raise HTTPException(422,str(exc)) from exc
    return Response(content,media_type='application/pdf',headers={'Content-Disposition':f'attachment; filename="{request.region_id}-karar-raporu.pdf"'})

@app.post('/api/scenario-preview')
def preview_scenario(request:SimulationRequest):
    from .scenario_preview import scenario_preview
    try:return scenario_preview(request)
    except ValueError as e:raise HTTPException(422,str(e)) from e

@app.get('/api/automatic-north')
def automatic_north(climate_context_id:str='ec_earth_2030_2049'):
    from .automatic_baseline import analyze_northern_baseline
    try:return analyze_northern_baseline(climate_context_id)
    except ValueError as e:raise HTTPException(422,str(e)) from e

@app.post('/api/decision-information')
def decision_information(request:SimulationRequest):
    from .information_value import analyze_information
    try:return analyze_information(request,recorded_simulation)
    except ValueError as e:raise HTTPException(422,str(e)) from e

@app.post('/api/pattern-field-update')
def pattern_field_update(request:PatternFieldUpdate):
    try:
        gate=compare_field(request.observation,store)
        before=recorded_simulation(request.simulation.model_copy(update={'seawater_temperature_c':gate['expected']['temperature_C']}))
        after=recorded_simulation(request.simulation.model_copy(update={'seawater_temperature_c':gate['observed']['temperature_C']})) if gate['collocation']['passed'] else None
        comparison={k:v for k,v in gate.items() if k not in {'before','after','changed_decision','energy_delta_kwh'}}
        def mix(result):
            if not result or not result['optimized']:return None
            return sorted((a['crop_id'],a['method'],a['water_source'],round(a['production_kg'],3)) for a in result['optimized']['allocations'])
        changes=[]
        if after:
            if before['status']!=after['status']:changes.append(f"Uygulanabilirlik: {before['status']} → {after['status']}")
            if before['optimized'] and after['optimized']:
                for b,a in zip(before['optimized']['crops'],after['optimized']['crops']):
                    if abs(a['production_kg']-b['production_kg'])>1e-3:changes.append(f"{a['name_tr']}: {b['production_kg']:.2f} → {a['production_kg']:.2f} kg")
                eb,ea=before['optimized']['totals']['energy_kwh'],after['optimized']['totals']['energy_kwh']
                if eb is not None and ea is not None:changes.append(f'Enerji: {eb:.2f} → {ea:.2f} kWh')
            if mix(before)==mix(after):changes.append('Ürün/yöntem/su tahsisi değişmedi; otomatik güven artışı veya kalibrasyon iddia edilmez.')
        else:changes.append('Gözlem eşleşmedi; aynı motorla saha sonrası hesap yapılmadı.')
        result={'comparison':comparison,'before':before,'after':after,'changed_pattern':mix(before)!=mix(after) if after else None,
          'change_summary':changes,'classification':'SIMULATION_EXPLANATORY','invariants':['production targets','constraint definitions','all inputs except source temperature'],
          'limitations':['Marine sıcaklık gözlemi karasal su miktarını değiştirmez. Kaynak-temsil bağı ayrıca doğrulanmalı.','Saha panelindeki örnek simülasyondur; gerçek dış profil için kayıtlı ham veri gereklidir.']}
        return {**result,'run_id':store.record_run({'parameters':request.model_dump(mode='json'),'code_sha256':digest((ROOT/'backend/app.py').read_bytes())},result)}
    except ValueError as e:raise HTTPException(422,str(e)) from e

@app.get('/api/north-evidence')
def north_evidence():
    from .north_evidence import load_north_evidence
    try:return load_north_evidence()
    except (ValueError,FileNotFoundError) as e:raise HTTPException(422,str(e)) from e

from .north_api import router as north_router
app.include_router(north_router)
from .north_validation import router as north_validation_router
app.include_router(north_validation_router)
from .producer_support import router as producer_support_router
app.include_router(producer_support_router)

# Built frontend is served by the same local process, without a CDN or cloud API.
dist=ROOT/"frontend/dist"
if dist.exists():app.mount("/",StaticFiles(directory=dist,html=True),name="frontend")
