"""PWN CSV import and a transparent gradient baseline; no inferred salinity."""
import csv
import io
import math
from datetime import datetime
import numpy as np
from .provenance import digest

KINDS={"OUR_NEW_MEASUREMENT_TANK","EXTERNAL_OBSERVATION","SIMULATION_EXPLANATORY"}
UNITS={"adc_count_12bit","mV","V","arbitrary_unit"}
NUMERIC=("raw_conductivity_signal","temperature_C","encoder_count","cable_out_m","pressure_dbar","latitude","longitude","elapsed_ms")

def parse_profile(raw: bytes, source_kind: str, raw_unit: str, depth_method="unavailable"):
    if source_kind not in KINDS:
        raise ValueError("Kaynak türü gerçek tank/dış gözlem/açık simülasyon olmalı; planlanan gözlem veri değildir.")
    if raw_unit not in UNITS:raise ValueError("Ham iletkenlik sinyalinin birimini seçin; bu değer EC değildir.")
    if depth_method not in {"encoder_vertical_tank","manual_reference","pressure_derived","unavailable"}:
        raise ValueError("Derinlik yöntemi tanınmıyor.")
    try:text=raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:raise ValueError("UTF-8 CSV gerekli.") from exc
    reader=csv.DictReader(io.StringIO(text))
    if reader.fieldnames and len(reader.fieldnames)!=len(set(reader.fieldnames)):
        raise ValueError("CSV başlıkları yinelenemez.")
    fields=set(reader.fieldnames or [])
    required={"device_id","sample_index","raw_conductivity_signal","temperature_C","quality_flag"}
    if not required<=fields or not {"cast_id","experiment_id"}&fields or not {"timestamp_utc","elapsed_ms"}&fields:
        raise ValueError("PWN başlıkları eksik: cihaz, cast/deney, sample_index, zaman, ham sinyal, sıcaklık, kalite gerekli.")
    rows=[]; warnings=[]; prev_index=-1; prev_ms=None; prev_time=None; identities=set()
    for line,row in enumerate(reader,start=2):
        if len(rows)>=20_000:raise ValueError("Tek profil için 20.000 satır sınırı aşıldı.")
        if None in row or any(value is None for value in row.values()):raise ValueError(f"Satır {line}: virgül/sütun sayısı hatalı.")
        if row.get("schema_version") not in (None,"","1.0"):raise ValueError("Desteklenen CSV sürümü 1.0.")
        if row.get("source_kind") not in (None,"",source_kind):raise ValueError("Seçilen kaynak türü CSV ile uyuşmuyor.")
        device=(row.get("device_id") or "").strip()
        cast=(row.get("cast_id") or row.get("experiment_id") or "").strip()
        if not device or not cast:raise ValueError(f"Satır {line}: cihaz/cast kimliği boş.")
        identities.add((device,cast))
        if len(identities)>1:raise ValueError("Bir dosyada tek cihaz ve tek cast olmalı; tekrarları ayrı yükleyin.")
        try:idx=int(row["sample_index"])
        except (ValueError,TypeError) as exc:raise ValueError("sample_index tam sayı olmalı.") from exc
        if idx<=prev_index:raise ValueError("sample_index monoton artmalı ve yinelenmemeli.")
        prev_index=idx
        parsed={"device_id":device,"cast_id":cast,"sample_index":idx,"quality_flag":row.get("quality_flag") or "UNSPECIFIED",
                "calibration_id":row.get("calibration_id") or None,"timestamp_utc":row.get("timestamp_utc") or None}
        parsed["temperature_kind"]=row.get("temperature_kind") or None
        for key in NUMERIC:
            value=row.get(key)
            if value is None or not value.strip():parsed[key]=None;continue
            try:number=float(value)
            except ValueError as exc:raise ValueError(f"Satır {line}, {key}: sayı gerekli.") from exc
            if not math.isfinite(number):raise ValueError(f"Satır {line}: NaN/Inf gözlem değildir; boş ve kalite işareti kullanın.")
            if key in {"elapsed_ms","encoder_count"} and not number.is_integer():raise ValueError(f"{key} tam sayı olmalı.")
            if key in {"elapsed_ms","cable_out_m","pressure_dbar"} and number<0:raise ValueError(f"{key} negatif olamaz.")
            if key=="latitude" and not -90<=number<=90:raise ValueError("Enlem aralık dışında.")
            if key=="longitude" and not -180<=number<=180:raise ValueError("Boylam aralık dışında.")
            parsed[key]=number
        if parsed["elapsed_ms"] is None and parsed["timestamp_utc"] is None:raise ValueError("Her satırda UTC veya elapsed_ms gerekli.")
        if parsed["elapsed_ms"] is not None:
            if prev_ms is not None and parsed["elapsed_ms"]<prev_ms:raise ValueError("elapsed_ms geriye gidiyor; yeni cast kullanın.")
            prev_ms=parsed["elapsed_ms"]
        if parsed["timestamp_utc"]:
            try:stamp=datetime.fromisoformat(parsed["timestamp_utc"].replace("Z","+00:00"))
            except ValueError as exc:raise ValueError("Geçerli ISO8601 UTC gerekli.") from exc
            if stamp.utcoffset() is None or stamp.utcoffset().total_seconds()!=0:raise ValueError("timestamp_utc UTC olmalı.")
            if prev_time is not None and stamp<prev_time:raise ValueError("UTC zaman geriye gidiyor.")
            prev_time=stamp
        depth=None
        if depth_method in {"encoder_vertical_tank","manual_reference"}:
            depth=parsed["cable_out_m"]
        elif depth_method=="pressure_derived" and parsed["pressure_dbar"] is not None and parsed["latitude"] is not None:
            import gsw
            depth=float(-gsw.z_from_p(parsed["pressure_dbar"],parsed["latitude"]))
        parsed["derived_depth_m"]=depth
        rows.append(parsed)
    if not rows:raise ValueError("CSV gözlem satırı içermiyor.")
    if any(r["raw_conductivity_signal"] is None or r["temperature_C"] is None for r in rows):warnings.append("Eksik ölçümler korunuyor; eksik değerler sıfıra çevrilmedi.")
    if depth_method=="unavailable":warnings.append("Geçerli derinlik yöntemi seçilmedi; kablo mesafesi derinlik sayılmadı.")
    if depth_method in {"encoder_vertical_tank","manual_reference"}:warnings.append("Derinlik, yüzey sıfırı ve prob ofseti düzeltilmiş dikey tank mesafesi beyanına dayanır; gemide kablo boyu derinlik değildir.")
    warnings.append("Ham sinyalden otomatik EC/tuzluluk üretilmedi; kalibrasyon ve su matrisi gerekir.")
    return {"rows":rows,"sample_count":len(rows),"cast_id":rows[0]["cast_id"],"device_id":rows[0]["device_id"],
            "source_kind":source_kind,"raw_conductivity_unit":raw_unit,"depth_method":depth_method,"warnings":warnings,"sha256":digest(raw)}

def detect_layers(depth,signal):
    z,y=np.array(depth,dtype=float),np.array(signal,dtype=float)
    if len(z)<5 or z.shape!=y.shape or not np.isfinite(z).all() or not np.isfinite(y).all():
        return {"status":"insufficient_data","layers":[],"reason":"Gradient için en az beş geçerli derinlik/sinyal çifti gerekli."}
    if np.all(np.diff(z)<0):z,y=z[::-1],y[::-1]
    if not np.all(np.diff(z)>0):
        return {"status":"insufficient_data","layers":[],"reason":"Ayrı, tek yönlü ve farklı derinlikli cast gerekli; iniş/çıkış karıştırılmaz."}
    smoothed=np.array([np.median(y[max(0,i-1):min(len(y),i+2)]) for i in range(len(y))])
    gradient=np.gradient(smoothed,z)
    absolute=np.abs(gradient)
    med=float(np.median(absolute)); mad=float(np.median(np.abs(absolute-med)))
    threshold=max(med+6*1.4826*mad,float(np.max(absolute))*0.25,1e-9)
    candidates=np.flatnonzero(absolute>threshold)
    groups=np.split(candidates,np.where(np.diff(candidates)>1)[0]+1) if len(candidates) else []
    layers=[]
    for group in groups:
        ix=int(group[np.argmax(absolute[group])])
        if ix in (0,len(z)-1):continue
        layers.append({"depth_m":float(z[ix]),"gradient":float(gradient[ix]),"interval_m":[float(z[group[0]]),float(z[group[-1]])],
                       "label":"Ham iletkenlik sinyali geçiş adayı"})
    return {"status":"analyzed","layers":layers,"threshold":threshold,"threshold_units":"raw_signal_unit/m",
            "depth_m":z.tolist(),"gradient":gradient.tolist(),"method":"median3 + |gradient| > max(median+6·1.4826·MAD, 0.25·max, 1e-9)",
            "boundary_error_m":None,"confidence":None,"reason":"Sıcaklık etkisi ayrıştırılmadı; haloklin veya kaynak kökeni kanıtı değildir."}

def analyze_profile(raw,source_kind,raw_unit,depth_method):
    parsed=parse_profile(raw,source_kind,raw_unit,depth_method)
    valid=[r for r in parsed["rows"] if r["derived_depth_m"] is not None and r["raw_conductivity_signal"] is not None and r["quality_flag"]=="OK"]
    analysis=detect_layers([r["derived_depth_m"] for r in valid],[r["raw_conductivity_signal"] for r in valid])
    return {**parsed,"analysis":analysis,"excluded_from_gradient":len(parsed["rows"])-len(valid),"derived_ec":None,"derived_salinity":None,
            "adaptive_sampling":{"method":"gradient baseline","recommended_depths_m":[x["depth_m"] for x in analysis["layers"]],"status":"proposal_only","ai_trained":False}}

def simulated_profile_csv():
    """Deterministic software fixture, visibly never a measurement."""
    buff=io.StringIO(); writer=csv.writer(buff,lineterminator="\n")
    writer.writerow(["schema_version","source_kind","device_id","experiment_id","cast_id","sample_index","timestamp_utc","elapsed_ms","raw_conductivity_signal","temperature_C","encoder_count","cable_out_m","pressure_dbar","latitude","longitude","calibration_id","quality_flag"])
    for i in range(61):
        z=i/100
        value=0.2+1.4/(1+math.exp(-(z-0.3)/0.012))
        writer.writerow(["1.0","SIMULATION_EXPLANATORY","SIMULATOR","software-fixture","SIM-001",i,"",i*1000,f"{value:.6f}",20,i,f"{z:.2f}","","","","","OK"])
    return buff.getvalue().encode()
