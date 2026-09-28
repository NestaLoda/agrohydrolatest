import json
from pathlib import Path
import pandas as pd
from .provenance import ROOT, ProvenanceStore, digest
from .science import climate_metrics, kc_curve, water_balance

def load_manifest(recent=False):
    return json.loads((ROOT/("data/manifest_turkey_recent.json" if recent else "data/manifest.json")).read_text(encoding="utf-8"))

def load_verified_climate(recent=False):
    """Verify derivatives against immutable sources, then return those same bytes.

    Validation runs on every read so post-startup edits cannot keep an authentic
    source label. Raw source checks also protect against altered source files.
    """
    import csv
    import hashlib
    import io
    import math
    from scripts.ingest_data import validate

    mapping = {"temperature_2m_min": "tmin_c", "temperature_2m_max": "tmax_c",
               "precipitation_sum": "precipitation_mm", "et0_fao_evapotranspiration": "et0_mm"}
    expected = {}
    for metadata in load_manifest(recent)["datasets"]:
        raw_path = (ROOT / metadata["local_raw_path"]).resolve()
        if not raw_path.is_relative_to((ROOT / "data/raw").resolve()):
            raise ValueError("İklim kaynak dosyası data/raw dizininde olmalı.")
        raw = raw_path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != metadata["content_sha256"]:
            raise ValueError("Ham iklim verisi kaynak SHA256 kaydıyla uyuşmuyor.")
        payload = json.loads(raw)
        validate(payload, "2024-01-01", "2025-12-31") if recent else validate(payload)
        site = metadata["requested_location"]["site_id"]
        for index, day in enumerate(payload["daily"]["time"]):
            key = (site, day)
            if key in expected:
                raise ValueError("Kaynak paketinde yinelenen bölge/tarih var.")
            expected[key] = {"dataset_id": metadata["dataset_id"], **{column: payload["daily"][source][index] for source, column in mapping.items()}}
    csv_bytes = (ROOT / ("data/processed/climate_turkey_recent.csv" if recent else "data/processed/climate.csv")).read_bytes()
    reader = csv.DictReader(io.StringIO(csv_bytes.decode("utf-8")))
    required = {"site_id", "date", "dataset_id", *mapping.values()}
    if set(reader.fieldnames or []) != required:
        raise ValueError("İşlenmiş iklim verisinin sütunları kaynak sözleşmesiyle uyuşmuyor.")
    seen = set()
    for row in reader:
        key = (row["site_id"], row["date"])
        if key not in expected or key in seen:
            raise ValueError("İşlenmiş iklim verisinde ek/yinelenen veya yanlış bölge/tarih var.")
        seen.add(key)
        original = expected[key]
        if row["dataset_id"] != original["dataset_id"]:
            raise ValueError("İşlenmiş iklim verisinin kaynak kimliği uyuşmuyor.")
        for column in mapping.values():
            value = None if row[column] == "" else float(row[column])
            if value is not None and not math.isfinite(value):
                raise ValueError("İşlenmiş iklim verisinde sonlu olmayan değer var.")
            if value != original[column]:
                raise ValueError("İşlenmiş iklim verisi değiştirilemez kaynak değerleriyle uyuşmuyor.")
    if seen != set(expected):
        raise ValueError("İşlenmiş iklim verisinde kaynak günleri eksik.")
    return pd.read_csv(io.BytesIO(csv_bytes), parse_dates=["date"])

def register_sources(store: ProvenanceStore):
    load_verified_climate()
    load_verified_climate(recent=True)
    for dataset in load_manifest()["datasets"] + load_manifest(recent=True)["datasets"]:
        path=(ROOT/dataset["local_raw_path"]).resolve()
        if not path.is_relative_to((ROOT/"data").resolve()):raise ValueError("Kaynak dosyası data dizininde olmalı.")
        store.register(dataset,path.read_bytes())
    northern=north_context()
    for source in northern.get("provenance",[]):
        metadata={**source,"dataset_id":source["dataset_id"]+"_"+source["sha256"][:12],
          "content_sha256":source["sha256"],"classification":"EXTERNAL CLIMATE MODEL",
          "access_date":source["accessed_at_utc"],"local_raw_path":source["raw_path"]}
        store.register(metadata,(ROOT/source["raw_path"]).read_bytes())

def overview():
    sites=json.loads((ROOT/"data/sites.json").read_text(encoding="utf-8"))
    for s in sites:s.update(id=s["site_id"],lat=s["latitude"],lon=s["longitude"])
    literature=json.loads((ROOT/"data/literature_parameters.json").read_text(encoding="utf-8"))["future_frontier"]
    areas=[5966866,3852011,1855054,1019473]; total=sum(areas)
    return {"pilot":{"question":"Mevcut bir bölgede hangi ürün deseni su baskısını azaltabilir?",
        "classification":"OUR HISTORICAL RESULT","pressure_before":15702550,"pressure_after":14338276,
        "reduction_pct":(15702550-14338276)/15702550*100,
        "crops":[{"name":name,"area_da":a,"original_share_pct":a/total*100,"optimized_share_pct":share} for name,a,share in zip(["Buğday","Arpa","Dane mısır","Şeker pancarı"],areas,[47,45,5,3])],
        "source":"Orijinal 2204-D raporu, s.7–13,17","source_url":"/api/pilot-source",
        "limitation":"Göreli model sonucu; sahada ölçülmüş m³ su tasarrufu değil.","formula":"Alan × göreli su katsayısı × iklim çarpanı"},
        "sites":sites,"datasets":load_manifest()["datasets"],
        "future":{"label":"EXTERNAL LITERATURE RESULT","classification":"FUTURE SCENARIO","period":"2071–2100",
            "scenarios":[{"id":key,"label":s["scenario"],"northward_shift_km":s["mean_northward_climate_frontier_shift_km"]} for key,s in zip(["ssp126","ssp585"],literature["scenarios"])],
            "source_url":literature["source_url"],"limitation":literature["limitation"],"local_future_climate_available":False},
        "status":{"application":"working_vertical_slice","pwn_hardware":"not_built","arctic_observation":"planned","ai":"classical_baselines_only"}}

def transfer(capacity_mm=60, initial_mm=30):
    frame=load_verified_climate()
    sites=json.loads((ROOT/"data/sites.json").read_text(encoding="utf-8"))
    output=[]
    for s in sites:
        df=frame[frame.site_id==s["site_id"]].sort_values("date").copy()
        current=df[df.date.dt.year==2023].copy()
        complete=(len(current)==365 and not current[["tmin_c","tmax_c","precipitation_mm","et0_mm"]].isna().any().any())
        if not complete:
            output.append({"site_id":s["site_id"],"name":s["name"],"status":"insufficient_data","reason":"Tam günlük seri gerekli."});continue
        metrics=climate_metrics(current.tmin_c,current.tmax_c)
        current["month"]=current.date.dt.month
        monthly=current.groupby("month").agg(precipitation_mm=("precipitation_mm","sum"),et0_mm=("et0_mm","sum"),tmin_c=("tmin_c","mean"),tmax_c=("tmax_c","mean")).reset_index().to_dict("records")
        balance=None
        if s["site_id"]!="longyearbyen":
            start=pd.Timestamp("2022-11-01")
            season=df[(df.date>=start)&(df.date<start+pd.Timedelta(days=240))]
            if len(season)==240:
                variants=[water_balance(season.precipitation_mm,season.et0_mm,kc_curve(k),capacity_mm,initial_mm) for k in [.4,.7]]
                balance={**variants[1],"deficit_interval_mm":[v["totals"]["deficit_mm"] for v in variants],
                         "season_start":"2022-11-01","season_end":season.date.iloc[-1].strftime("%Y-%m-%d"),
                         "crop":"Kış buğdayı","classification":"SIMULATION / EXPLANATORY",
                         "parameter_source":"FAO56 Tablo 11/12","initial_kc_range":[.4,.7]}
        output.append({"site_id":s["site_id"],"name":s["name"],"year":2023,"status":"transfer_demonstration" if balance else "historical_context",
            **metrics,"annual_precipitation_mm":float(current.precipitation_mm.sum()),"annual_et0_mm":float(current.et0_mm.sum()),
            "monthly":monthly,"water_balance":balance,"dataset_id":str(current.dataset_id.iloc[0]),"classification":"MODEL / REANALYSIS",
            "lettuce_frost_screen":{"conservative_screen_days":60,"observed_frost_free_days":metrics["frost_free_longest_days"],
                "status":"conditional" if metrics["frost_free_longest_days"]>=60 else "insufficient_data",
                "reason":"Tasarım varsayımı: 60 gün Tmin>0°C ihtiyatlı taraması; biyolojik zorunlu eşik veya verim kanıtı değil. FAO baş marul için 60–85 gün, yetişkin için −1°C öldürücü sıcaklık bildirir. Yerel çeşit, ışık ve su değerlendirmesi gerekir.",
                "source_url":"https://ecocrop.apps.fao.org/ecocrop/srv/en/cropView?id=1313"}})
    return {"sites":output,"comparison_crop":"Kış buğdayı","label":"TRANSFER DEMONSTRATION",
        "assumptions":["FAO Akdeniz 240 günlük örnek takvim karşılaştırılan Türkiye bölgelerinde aynı tutuldu; yerel fenoloji ölçümü değil.",
                       "İlk Kc 0.4–0.7 duyarlılığı; Kc_mid=1.15 ve Kc_end=0.25. Yerel iklim düzeltmesi yok.",
                       f"{capacity_mm:g} mm depo, {initial_mm:g} mm ilk stok, 1 ha alan senaryo parametreleridir; yerel toprak ölçümü değil.",
                       "Kar erimesi, yeraltı suyu, sulama tahsisi ve rakip kullanımlar veriyle modellenmedi; yıllık su güvenliği doğrulanmadı.",
                       "Bu karşılaştırma transfer gösterimidir; bağımsız saha validasyonu değildir."],
        "source_url":"https://www.fao.org/4/X0490E/x0490e0b.htm"}

def benchmarks(request=None):
    from .contracts import BenchmarkRequest
    r=request or BenchmarkRequest()
    context=json.loads((ROOT/"data/benchmark_context.json").read_text(encoding="utf-8"))
    available={x["site_id"] for x in context["regions"]}
    if any(s not in available for s in r.site_ids):raise ValueError("Karşılaştırma için kayıtlı Türkiye benchmark'ı seçin.")
    result=transfer(r.soil_capacity_mm,r.initial_storage_mm)
    selected=[]
    for site in result["sites"]:
        if site["site_id"] not in r.site_ids:continue
        wb=site.get("water_balance")
        if wb:
            deficit=wb["totals"]["deficit_mm"]
            gap=max(0,deficit-r.net_irrigation_budget_mm)
            site["budget_screen"]={"reference_deficit_mm":deficit,"budget_mm":r.net_irrigation_budget_mm,
              "gap_mm":gap,"covered_fraction":min(1,r.net_irrigation_budget_mm/deficit) if deficit else 1,
              "status":"budget_gap" if gap>1e-7 else "within_reference_budget",
              "classification":"SIMULATION / EXPLANATORY",
              "explanation":f"Referans ET açığına göre {gap:.1f} mm bütçe farkı. Bu net ek su bütçesi karşılaştırmasıdır; sulama programı veya verim sonucu değildir."}
        selected.append(site)
    return {**result,"sites":selected,"context":context,"parameters":r.model_dump(),
       "comparison_basis":"Aynı dönem, aynı ürün/Kc, aynı depo ve aynı net su bütçesi; iklim girdileri bölgeye göre değişir.",
       "ranking":sorted([{"site_id":s["site_id"],"name":s["name"],"gap_mm":s["budget_screen"]["gap_mm"],"reference_deficit_mm":s["budget_screen"]["reference_deficit_mm"]} for s in selected if "budget_screen" in s],key=lambda x:x["reference_deficit_mm"])}

def north_context():
    path=ROOT/"data/north/summary.json"
    if not path.exists():return {"status":"insufficient_data","limitations":["Yerel gelecek model paketi henüz hazırlanmadı."]}
    from scripts.ingest_north import validate, metrics, aggregate
    raw_summary=path.read_bytes()
    summary=json.loads(raw_summary)
    annual=[]
    for period,meta in zip(["baseline","future"],summary["provenance"]):
        source=(ROOT/meta["raw_path"]).resolve()
        if not source.is_relative_to((ROOT/"data/north/raw").resolve()):raise ValueError("Kuzey kaynak yolu geçersiz.")
        raw=source.read_bytes()
        if digest(raw)!=meta["sha256"]:raise ValueError("Kuzey model kaynağının bütünlüğü bozuldu.")
        payload=json.loads(raw)
        validate(payload,*meta["period"])
        yearly=metrics(payload,period)
        annual.extend(yearly)
        if aggregate(yearly,*meta["period"])!=summary[period]:raise ValueError("Kuzey dönem özeti ham modelden farklı.")
    if len(summary["provenance"])!=2 or annual!=summary["annual_metrics"]:raise ValueError("Kuzey dönem/yıl kaydı uyuşmuyor.")
    for key in ("gdd5_degree_days","frost_free_run_days","precipitation_mm"):
        expected=round(summary["future"]["mean_annual_"+key]-summary["baseline"]["mean_annual_"+key],6)
        if summary["delta"][key]!=expected:raise ValueError("Kuzey değişim özeti ham modelden farklı.")
    return {**summary,"summary_sha256":digest(raw_summary)}
