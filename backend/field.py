"""Collocation gate for an explicit model/profile comparison, not an AI calibration."""
import math
from pathlib import Path
from urllib.parse import urlparse
from .contracts import FieldComparisonRequest, FieldPoint
from .provenance import ROOT, digest
from .pwn import parse_profile
from .optimizer import solve_decision

def distance_km(a,b):
    lat1,lat2=map(math.radians,[a.latitude,b.latitude])
    dlat=lat2-lat1; dlon=math.radians(b.longitude-a.longitude)
    h=math.sin(dlat/2)**2+math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 6371.0088*2*math.asin(math.sqrt(min(1,max(0,h))))

def compare_field(q:FieldComparisonRequest,store):
    observed=q.observed
    observation_provenance=None
    real=q.evidence_kind=="EXTERNAL_OBSERVATION"
    if real:
        if not q.observed_dataset_id or q.observed_sample_index is None:
            raise ValueError("Gerçek karşılaştırma için kaynaklı dış profil dataset_id ve sample_index gerekli.")
        if not q.model_source_url or urlparse(q.model_source_url).scheme not in {"http","https"} or not urlparse(q.model_source_url).hostname:
            raise ValueError("Model beklentisinin kaynak URL'si gerekli; beklenen değer kullanıcı beyanı olarak saklanır.")
        meta=next((d for d in store.datasets() if d["dataset_id"]==q.observed_dataset_id),None)
        if not meta or meta["classification"]!="EXTERNAL_OBSERVATION":
            raise ValueError("Yalnız kaynaklı dış gözlem kullanılabilir; tank/simülasyon deniz gözlemi değildir.")
        if meta.get("depth_method")!="pressure_derived":
            raise ValueError("Bu deniz karşılaştırmasında basınç/enlemden derinlik gerekli; tank kablo mesafesi kullanılamaz.")
        if meta.get("temperature_kind")!="in_situ":
            raise ValueError("Gözlem sıcaklığı tanımı açıkça in_situ olmalı; potansiyel/korunumlu sıcaklık dönüştürülmeden çıkarılamaz.")
        raw_path=(ROOT/meta["local_raw_path"]).resolve()
        if not raw_path.is_relative_to((ROOT/"data/pwn/raw").resolve()):raise ValueError("PWN kaynak yolu geçersiz.")
        try:raw=raw_path.read_bytes()
        except FileNotFoundError as exc:raise ValueError("Kayıtlı PWN ham dosyası bulunamadı.") from exc
        if digest(raw)!=meta["content_sha256"]:raise ValueError("PWN kaynağının bütünlüğü bozuldu.")
        profile=parse_profile(raw,"EXTERNAL_OBSERVATION",meta["units"]["raw_conductivity_signal"],meta["depth_method"])
        row=next((r for r in profile["rows"] if r["sample_index"]==q.observed_sample_index),None)
        if not row or row["quality_flag"]!="OK":raise ValueError("Seçilen profil satırı yok veya kalite işareti OK değil.")
        if row.get("temperature_kind") not in (None,"in_situ"):raise ValueError("CSV sıcaklık tanımı kaynak beyanıyla uyuşmuyor.")
        mapping={"temperature_C":"temperature_C","latitude":"latitude","longitude":"longitude","depth_m":"derived_depth_m","timestamp_utc":"timestamp_utc"}
        if any(row.get(k) is None for k in mapping.values()):raise ValueError("Eşleştirme için sıcaklık, konum, UTC ve derinlik eksiksiz olmalı.")
        observed=FieldPoint(**{key:row[value] for key,value in mapping.items()},temperature_kind=meta["temperature_kind"])
        observation_provenance={"dataset_id":meta["dataset_id"],"sample_index":q.observed_sample_index,"sha256":meta["content_sha256"],"source_url":meta["source_url"]}
    separation=distance_km(q.expected,observed)
    hours=abs((q.expected.timestamp_utc-observed.timestamp_utc).total_seconds())/3600
    depth=abs(q.expected.depth_m-observed.depth_m)
    checks=[{"label":"Konum","passed":separation<=q.max_distance_km,"difference":separation,"tolerance":q.max_distance_km,"unit":"km"},
            {"label":"Zaman","passed":hours<=q.max_time_hours,"difference":hours,"tolerance":q.max_time_hours,"unit":"saat"},
            {"label":"Derinlik","passed":depth<=q.max_depth_difference_m,"difference":depth,"tolerance":q.max_depth_difference_m,"unit":"m"}]
    checks.append({"label":"Aynı sıcaklık tanımı (yerinde)","passed":q.expected.temperature_kind==observed.temperature_kind=="in_situ",
                   "expected":q.expected.temperature_kind,"observed":observed.temperature_kind})
    matched=all(c["passed"] for c in checks)
    before=solve_decision(q.decision.model_copy(update={"seawater_temperature_c":q.expected.temperature_C})) if matched else None
    after=solve_decision(q.decision.model_copy(update={"seawater_temperature_c":observed.temperature_C})) if matched else None
    both=matched and before["totals"] is not None and after["totals"] is not None
    mix=lambda result:[(a["option_id"],round(a["production_kg"],6)) for a in result["allocations"]]
    changed=matched and (before["status"]!=after["status"] or mix(before)!=mix(after))
    return {"status":"conditional" if matched else "not_comparable","classification":"SIMULATION / EXPLANATORY",
       "observation_evidence":"EXTERNAL OBSERVATION" if real else "SIMULATION / EXPLANATORY",
       "model_expectation_evidence":"USER-DECLARED MODEL VALUE" if real else "SIMULATION / EXPLANATORY",
       "expected":q.expected.model_dump(mode="json"),"observed":observed.model_dump(mode="json"),
       "model_source_url":q.model_source_url,"observation_provenance":observation_provenance,
       "collocation":{"distance_km":separation,"time_difference_hours":hours,"depth_difference_m":depth,"checks":checks,"passed":matched},
       "residual_temperature_C":observed.temperature_C-q.expected.temperature_C if matched else None,
       "before":before,"after":after,"changed_decision":bool(changed) if matched else None,
       "energy_delta_kwh":after["totals"]["energy_kwh"]-before["totals"]["energy_kwh"] if both else None,
       "confidence_score":None,"calibration_applied":False,
       "reason":"Eşleşen sıcaklık girdisinin karar duyarlılığı hesaplandı; otomatik model kalibrasyonu yapılmadı." if matched else "Konum/zaman/derinlik veya sıcaklık tanımı eşleşmedi; fark kalibrasyon veya karar güncellemesi olarak kullanılmadı.",
       "limitations":["Toleranslar kullanıcı senaryosudur; sefer için uzman onaylı eşleme protokolü değildir.",
          "Model grid değeri ile tek profil aynı örnekleme hacmini temsil etmez; eşleşme tek başına tüm temsil hatasını gidermez.",
          "Kaynak sıcaklığı yalnız arıtma alt hesabına aktarılır; kara su bütçesi, yıllık güvenilir arz veya besleme noktasını temsil ettiği kanıtlanmış değildir.",
          "Gerçek gözlemde bile beklenen model değeri ve kaynak URL'si kullanıcı beyanıdır; bu sürüm deniz modeli dosyasını otomatik indirmez.",
          "Bir çiftle güven yüzdesi/öğrenilmiş kalibrasyon üretilmez. 5–18°C dışı arıtma koşullarında veri yetersiz kalır."]}
