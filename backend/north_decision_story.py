"""Pure, evidence-bounded explanations of an already calculated northern plan.

This module neither runs an optimizer nor reads weather, files or the network.
Water-source allocation belongs to the monthly LP; backup needs belong to the
separate chronological roof/tank replay. These quantities are never equated.
"""
from copy import deepcopy
from math import floor, isfinite
from statistics import mean

VERSION = "north-decision-story-1.0"
DRY_YEAR_DISPLAY_THRESHOLD_PCT = 5.0
MONTHS = ("Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz",
          "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık")
METHODS = {"greenhouse": "sera", "hydroponics": "kontrollü hidroponik üretim", "open_field": "açık tarla"}
SOURCES = (("stored_water_m3", "stored_precipitation", "Toplanan yağış / kar erimesi"),
           ("desalinated_m3", "desalinated_seawater", "Arıtılmış deniz suyu"),
           ("freshwater_m3", "allocated_freshwater", "Açıkça tanımlanan tatlı su tahsisi"))


def _number(value):
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError("A scientific quantity cannot be a boolean")
    number = float(value)
    if not isfinite(number) or number < -1e-7:
        raise ValueError("Scientific quantities must be finite and nonnegative")
    return max(0., number)


def _fmt(value, digits=1):
    return f"{value:.{digits}f}".replace(".", ",")


def _sources(totals):
    rows = [{"id": ident, "label": label, "m3": _number(totals.get(key)), "share_pct": None}
            for key, ident, label in SOURCES]
    demand = _number(totals.get("water_m3"))
    complete = all(r["m3"] is not None for r in rows)
    allocated = sum(r["m3"] for r in rows) if complete else None
    if complete:
        if allocated > 0:
            # Largest remainder rounding: visible shares close at exactly 100.00%.
            raw = [10000*r["m3"]/allocated for r in rows]
            points = [floor(v) for v in raw]
            for i in sorted(range(len(rows)), key=lambda i: (raw[i]-points[i], -i), reverse=True)[:10000-sum(points)]:
                points[i] += 1
            for row, value in zip(rows, points):
                row["share_pct"] = value/100
        else:
            for row in rows:
                row["share_pct"] = 0.
    residual = allocated-demand if allocated is not None and demand is not None else None
    return {"sources": rows, "allocated_source_total_m3": allocated,
            "source_share_basis": "Actual allocated source total; not physical source-water availability.",
            "source_balance_residual_m3": residual,
            "source_balance_status": "NOT_COMPUTED" if residual is None else (
                "CLOSED" if abs(residual) <= max(1e-5, demand*1e-6) else "INCONSISTENT")}


def _critical_month(plan, reliability):
    rows = []
    complete_replay = bool(reliability) and all(r.get("monthly") for r in reliability)
    if complete_replay:
        basis = "MAX_MODEL_CLIMATOLOGICAL_MONTH_FROM_DAILY_REPLAY"
        for model in reliability:
            for row in model["monthly"]:
                rows.append((row, model.get("model"), _number(row.get("deficit_m3"))))
    else:
        basis = "MONTHLY_MEAN_PLAN_FALLBACK"
        for row in plan.get("monthly", []):
            sea, fresh = _number(row.get("desalinated_m3")), _number(row.get("freshwater_m3"))
            rows.append((row, None, sea+fresh if sea is not None and fresh is not None else None))
    values = []
    for row, model, backup in rows:
        demand = _number(row.get("demand_m3"))
        month = row.get("month")
        if month not in range(1, 13) or demand is None or backup is None:
            continue
        if backup > demand+max(1e-5, demand*1e-6):
            raise ValueError("Monthly backup cannot exceed the corresponding demand")
        values.append({"month": month, "label": MONTHS[month-1], "model": model,
                       "backup_m3": backup, "demand_m3": demand,
                       "backup_share_pct": 100*backup/demand if demand > 0 else None})
    if not values:
        return None
    selected = max(values, key=lambda r: (r["backup_m3"], r["backup_share_pct"] or 0, -r["month"]))
    # No artificial 'critical month' when every modeled month needs zero backup.
    if selected["backup_m3"] <= 1e-7:
        return None
    return {**selected, "basis": basis,
            "selection_rule": "Largest monthly backup volume; tied volumes use highest backup/demand ratio.",
            "meaning": "Roof/tank shortfall before backup sources; not an unserved deficit after desalination.",
            "is_single_worst_year_month": False}


def _backup(reliability):
    rows = []
    for row in reliability:
        annual = row.get("topup_m3_per_year", {})
        band = {key: _number(annual.get(key)) for key in ("min", "mean", "max")}
        if any(v is None for v in band.values()):
            continue
        if not band["min"] <= band["mean"] <= band["max"]:
            raise ValueError("Annual backup min/mean/max are not ordered")
        rows.append({"model": row.get("model"), "annual_m3": band,
                     "worst_year": row.get("worst_topup_year"),
                     "maximum_daily_m3": _number(row.get("maximum_daily_topup_m3")),
                     "days_with_backup": row.get("days_with_topup")})
    if not rows:
        return {"status": "NOT_COMPUTED", "annual_m3": None, "models": []}
    worst = max(rows, key=lambda row: row["annual_m3"]["max"])
    daily = [r["maximum_daily_m3"] for r in rows if r["maximum_daily_m3"] is not None]
    return {"status": "COMPUTED" if len(rows) == len(reliability) else "PARTIAL",
            "annual_m3": {"min": min(r["annual_m3"]["min"] for r in rows),
                          "mean": mean(r["annual_m3"]["mean"] for r in rows),
                          "max": worst["annual_m3"]["max"]},
            "worst_model": worst["model"], "worst_year": worst["worst_year"],
            "worst_model_annual_m3": deepcopy(worst["annual_m3"]),
            "maximum_daily_m3": max(daily) if daily else None, "models": rows,
            "aggregation": "Min/max across modeled years and models; mean of model annual means. Equal periods required for pooled-mean interpretation.",
            "meaning": "Additional water after roof/tank supply, before freshwater/desalination; not measured unreliability.",
            "probability_claimed": False}


def _dry_year(backup):
    band = backup.get("annual_m3")
    average, worst = (band["mean"], band["max"]) if band else (None, None)
    delta = worst-average if band else None
    percent = 100*delta/average if average is not None and average > 1e-7 else None
    sensitive = percent > DRY_YEAR_DISPLAY_THRESHOLD_PCT if percent is not None else (
        bool(worst > 1e-7) if worst is not None else None)
    return {"status": backup["status"], "annual_mean_backup_m3": average,
            "worst_model_year_backup_m3": worst, "increase_m3": delta, "increase_pct": percent,
            "is_sensitive": sensitive, "display_threshold_pct": DRY_YEAR_DISPLAY_THRESHOLD_PCT,
            "comparison": "(Largest modeled annual backup - equal-weight mean annual backup) / mean annual backup.",
            "threshold_kind": "Explicit display convention, not a physical failure threshold or significance test.",
            "interpretation": "Highest backup-demand year; not necessarily the lowest-precipitation year.",
            "worst_year_is_first_modeled_year": backup.get("worst_year_is_first_modeled_year"),
            "initial_condition_warning": backup.get("initial_condition_warning"),
            "probability_claimed": False}


def _storage(result, reliability):
    basis, request = result.get("basis", {}), result.get("request", {})
    configured = _number(basis.get("storage_m3"))
    if configured is None and request.get("area_m2") is not None and request.get("storage_m3_per_m2") is not None:
        configured = _number(request["area_m2"])*_number(request["storage_m3_per_m2"])
    peaks = [_number(r.get("modeled_peak_storage_m3")) for r in reliability]
    if peaks and all(p is not None for p in peaks):
        peak, scope = max(peaks), "MAX_DAILY_OCCUPIED_STORAGE_ACROSS_MODELS"
    else:
        monthly = [_number(r.get("storage_end_m3")) for r in result.get("plan", {}).get("monthly", [])]
        peak = max(monthly) if monthly and all(p is not None for p in monthly) else None
        scope = "MONTH_END_OCCUPIED_STORAGE_IN_MEAN_PLAN" if peak is not None else "NOT_COMPUTED"
    return {"configured_m3": configured, "modeled_peak_occupied_m3": peak,
            "minimum_required_m3": None, "basis": scope, "capacity_optimized": False,
            "meaning": "Selected tank size and simulated occupied volume are different. Neither is a calculated minimum tank size."}


def _production(plan):
    crops, methods = {}, {}
    for row in plan.get("allocations", []):
        area, quantity = _number(row.get("area_m2")), _number(row.get("production_kg"))
        if area is None or area <= 1e-7:
            continue
        crop, method = row.get("crop_id"), row.get("method")
        c = crops.setdefault(crop, {"crop_id": crop, "name": row.get("name", crop), "area_m2": 0.,
                                   "production_kg": 0., "methods": [], "seasons": []})
        c["area_m2"] += area
        c["production_kg"] = c["production_kg"]+quantity if c["production_kg"] is not None and quantity is not None else None
        for key, value in (("methods", method), ("seasons", row.get("season"))):
            if value is not None and value not in c[key]:
                c[key].append(value)
        m = methods.setdefault(method, {"id": method, "label": METHODS.get(method, method), "area_m2": 0.})
        m["area_m2"] += area
    return {"crops": sorted(crops.values(), key=lambda r: (-r["area_m2"], str(r["crop_id"]))),
            "methods": sorted(methods.values(), key=lambda r: (-r["area_m2"], str(r["id"])))}


def summarize_decision(result):
    """Return JSON-ready water security and actions, without mutating ``result``.

    Missing diagnostics remain uncomputed. No minimum-storage sizing, income,
    freshwater allocation, failure probability or untested breakpoint is inferred.
    """
    plan, request = result.get("plan", {}), result.get("request", {})
    totals, reliability = plan.get("totals", {}), result.get("daily_reliability", [])
    backup = _backup(reliability)
    period = result.get("climate", {}).get("period", [])
    first_year = period[0] if period else None
    backup["first_modeled_year"] = first_year
    backup["worst_year_is_first_modeled_year"] = (
        backup.get("worst_year") == first_year if first_year is not None and backup.get("worst_year") is not None else None)
    backup["initial_condition_warning"] = (
        "İlk model yılında boş depo başlangıcı etkisi bulunuyor; bu bir kurak yıl kanıtı değildir."
        if backup["worst_year_is_first_modeled_year"] else None)
    water = {"annual_demand_m3": _number(totals.get("water_m3")), **_sources(totals),
             "critical_month": _critical_month(plan, reliability), "storage": _storage(result, reliability),
             "backup": backup, "dry_year_sensitivity": _dry_year(backup)}
    production, actions = _production(plan), []
    feasible = plan.get("status") != "infeasible" and bool(production["crops"])
    if feasible:
        methods = "; ".join(f"{_fmt(m['area_m2'])} m² {m['label']}" for m in production["methods"])
        crops = ", ".join(f"{c['name']} {_fmt(c['area_m2'])} m²" for c in production["crops"])
        actions.append({"id": "production", "kind": "production", "tone": "positive",
                        "title": "Hesaplanan üretim dağılımını uygula",
                        "text": f"{methods}. Ürün alanları: {crops}. Yerel pilotta verim ve çevrim koşullarını doğrula.",
                        "metrics": deepcopy(production), "evidence_basis": "Actual selected allocations; conditional yield transfer."})
    else:
        actions.append({"id": "production", "kind": "production", "tone": "danger", "title": "Bu koşullarla üretime geçme",
                        "text": plan.get("reason", "Seçilen kaynak ve yöntemlerle uygulanabilir pozitif üretim hesaplanmadı."),
                        "metrics": {"plan_status": plan.get("status")}, "evidence_basis": "Actual optimizer outcome."})
    used = [r for r in water["sources"] if r["m3"] is not None and r["m3"] > 1e-7]
    if used:
        text = "; ".join(f"{r['label']}: {_fmt(r['m3'])} m³"+(f" (%{_fmt(r['share_pct'])})" if r['share_pct'] is not None else "") for r in used)
        closed = water["source_balance_status"] == "CLOSED"
        actions.append({"id": "water_sources", "kind": "water", "tone": ("warning" if any(r["id"] == "desalinated_seawater" for r in used) else "neutral") if closed else "danger",
                        "title": "Su kaynaklarını bu paylarla hazırla" if closed else "Su tahsisi dengesini doğrulamadan uygulama",
                        "text": text+(". Toplanan suyun kalitesini ve gerekli koşullandırmayı doğrula." if closed else ". Kaynak toplamı ve talep dengesi henüz doğrulanmadı."),
                        "metrics": {"sources": deepcopy(water["sources"]), "balance_status": water["source_balance_status"]},
                        "evidence_basis": "Monthly LP allocated usable-water volumes, not surveyed source capacity."})
    critical = water["critical_month"]
    if critical:
        actions.append({"id": "seasonal_backup", "kind": "water", "tone": "warning", "title": f"{critical['label']} için yedek suyu planla",
                        "text": f"En yüksek ortalama aylık yedek gereği {_fmt(critical['backup_m3'])} m³; aynı ayın talebinin %{_fmt(critical['backup_share_pct'])}. Bu açık çatı/depo sonrası, yedek kaynak verilmeden öncedir.",
                        "metrics": deepcopy(critical), "evidence_basis": critical["basis"]})
    infrastructure = {key: _number(totals.get(key)) for key in ("heat_kwh_th", "electricity_kwh", "equivalent_electricity_kwh", "treatment_electricity_kwh", "treatment_heat_kwh_th")}
    infrastructure.update(configured_storage_m3=water["storage"]["configured_m3"],
                          modeled_peak_occupied_storage_m3=water["storage"]["modeled_peak_occupied_m3"],
                          configured_energy_limit_kwh=_number(request.get("energy_limit_kwh")),
                          heat_cop=_number(request.get("heat_cop")))
    pieces = []
    if infrastructure["heat_kwh_th"] is not None:
        pieces.append(f"Yıllık ısı gereği {_fmt(infrastructure['heat_kwh_th'], 0)} kWh ısıl")
    if infrastructure["electricity_kwh"] is not None:
        pieces.append(f"ısıtma dönüşümü dışındaki elektrik {_fmt(infrastructure['electricity_kwh'], 0)} kWh")
    if infrastructure["equivalent_electricity_kwh"] is not None:
        pieces.append(f"seçilen ısıtma katsayısıyla toplam {_fmt(infrastructure['equivalent_electricity_kwh'], 0)} kWh elektrik eşdeğeri")
    if infrastructure["configured_storage_m3"] is not None:
        pieces.append(f"hesapta seçilen depo {_fmt(infrastructure['configured_storage_m3'])} m³; minimum depo hesabı yapılmadı")
    if pieces:
        actions.append({"id": "infrastructure", "kind": "infrastructure", "tone": "warning", "title": "Enerji ve depo kurulumunu doğrula",
                        "text": "; ".join(pieces)+". Bunlar enerji miktarlarıdır; cihaz gücü veya mevcut yerel kapasite değildir.",
                        "metrics": infrastructure, "evidence_basis": "Calculated annual energy; explicit configured tank and energy ceiling."})
    sensitive = [deepcopy(r) for r in result.get("sensitivity", []) if r.get("status") == "SENSITIVE"]
    unresolved = [deepcopy(r) for r in result.get("sensitivity", []) if r.get("status") == "UNRESOLVED"]
    dry = water["dry_year_sensitivity"]
    if dry["is_sensitive"]:
        increase = f"%{_fmt(dry['increase_pct'])}" if dry["increase_pct"] is not None else f"{_fmt(dry['increase_m3'])} m³"
        startup = bool(dry["worst_year_is_first_modeled_year"])
        text = (dry["initial_condition_warning"]+f" Başlangıç dahil sınanan yıllarda en yüksek yedek gereği {_fmt(dry['worst_model_year_backup_m3'])} m³; yıllık model ortalaması {_fmt(dry['annual_mean_backup_m3'], 2)} m³."
                if startup else f"En yüksek yedek gereği olan model-yılda ihtiyaç yıllık ortalamadan {increase} fazla. Bu model aralığıdır; gerçekleşme olasılığı değildir.")
        actions.append({"id": "dry_year", "kind": "risk", "tone": "warning", "title": "İlk üretim yılı için yedek suyu hazırla" if startup else "Yalnız ortalama yıla göre su güvencesi verme",
                        "text": text,
                        "metrics": deepcopy(dry), "evidence_basis": "Daily replay model-year envelope; explicit 5% display threshold."})
    if sensitive:
        strongest = max(sensitive, key=lambda r: (r.get("area_reallocated_m2", 0), r.get("production_change_pct", 0), r.get("energy_change_pct", 0)))
        actions.append({"id": "sensitivity", "kind": "risk", "tone": "warning", "title": f"{strongest.get('name', strongest.get('id'))} varsayımını önce doğrula",
                        "text": strongest.get("effect", "Sınanan değerler planı veya kaynak gereksinimini değiştirdi."),
                        "metrics": strongest, "evidence_basis": "Actual bounded reruns of the same decision engine; no inferred breakpoint."})
    if unresolved:
        actions.append({"id": "unresolved", "kind": "risk", "tone": "neutral", "title": "Uygulama öncesi açık bağımlılıkları tamamla",
                        "text": "; ".join(r.get("name", r.get("id", "")) for r in unresolved)+".",
                        "metrics": {"items": unresolved}, "evidence_basis": "Declared unresolved inputs; no assumed numerical value."})
    return {"version": VERSION, "classification": "CALCULATED_DECISION_EXPLANATION", "plan_status": plan.get("status"),
            "water_security": water, "production": production, "actions": actions,
            "risk": {"sensitivity_computed": bool(result.get("sensitivity")), "sensitive_inputs": sensitive,
                     "unresolved_inputs": unresolved, "infeasible_test_cases": result.get("range_infeasible_cases"),
                     "reporting_rule": result.get("provenance", {}).get("sensitivity_threshold"),
                     "tested_breakpoints": [], "breakpoint_analysis_performed": False},
            "limitations": ["Üretim ve kaynak gereksinimleri koşullu model sonuçlarıdır; yerel işletme veya yeni saha ölçümü değildir.",
                            "Aylık kaynak tahsisi ve günlük çatı/depo sonrası yedek gereksinimi farklı hesaplardır.",
                            "Depo kapasitesi optimize edilmedi; seçilen kapasite ve doluluk minimum depo gereksinimi değildir.",
                            "Model-yıl aralığı ve gösterim eşikleri olasılık, güven aralığı veya kanıtlanmış başarısızlık eşiği değildir."]}
