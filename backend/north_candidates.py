"""Source-led northern candidates and an explicit conservative site gate.

This does not reproduce Xu et al.'s MaxEnt models. A crop's positive climate
screen is not agronomic validation, and a normalized controlled system is not
permission to construct a greenhouse on a particular parcel.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import date
import hashlib
import json
import math
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def get_catalog(root: Path | None = None) -> dict:
    """Return fresh copies of the research catalogue; callers cannot mutate it."""
    base = root or ROOT
    catalog = json.loads((base / "data/north/crop_evidence_v2.json").read_text(encoding="utf-8"))
    seen = set()
    for crop in catalog["crops"]:
        if crop["crop_id"] in seen:
            raise ValueError("Duplicate crop in northern evidence catalogue")
        seen.add(crop["crop_id"])
        if any(ref not in catalog["sources"] for ref in crop["source_ids"]):
            raise ValueError("Unresolved northern crop source")
        production = crop.get("production")
        if production:
            bounds = production["yield_kg_m2_cycle"]
            values = [bounds[k] for k in ("low", "central", "high")]
            if any(not math.isfinite(v) or v <= 0 for v in values) or values != sorted(values):
                raise ValueError("Invalid northern yield interval")
            if not math.isfinite(production["cycle_days"]) or production["cycle_days"] <= 0:
                raise ValueError("Invalid northern cultivation cycle")
    return catalog


def get_ground_evidence(site_id: str = "longyearbyen", root: Path | None = None) -> dict:
    data = json.loads(((root or ROOT) / "data/north/ground_evidence.json").read_text(encoding="utf-8"))
    if site_id not in data["sites"]:
        raise ValueError(f"Unsupported ground evidence site: {site_id}")
    return {"site_id": site_id, **data["sites"][site_id], "sources": data["sources"],
            "acquisition": data["acquisition"]}


def complete_cycle_capacity(crop: dict, season_days: float, area_m2: float = 100) -> dict:
    """Complete-cycle capacity, never partial harvest or annualized by stealth.

    Uses reported mean cycle duration as a transparent scheduling approximation.
    Reported min/max yield is sensitivity context, not a confidence interval.
    """
    for name, value in (("season_days", season_days), ("area_m2", area_m2)):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
            raise ValueError(f"{name} must be a finite nonnegative number")
    production = crop.get("production")
    if not production:
        return {"complete_cycles": None, "yield_kg": None, "area_m2": area_m2,
                "season_days": season_days, "reason": "No area-based yield for this method is resolved."}
    duration = production["cycle_days"]
    count = math.floor((season_days + 1e-9) / duration)
    bounds = production["yield_kg_m2_cycle"]
    return {"complete_cycles": count, "season_days": season_days, "area_m2": area_m2,
            "occupied_days": count * duration, "remaining_days": max(0, season_days - count * duration),
            "yield_kg": {key: bounds[key] * area_m2 * count for key in ("low", "central", "high")},
            "range_kind": bounds["range_kind"], "classification": "NORMALIZED_ANALOGUE_CALCULATION",
            "limitations": "Mean cycle duration; no nursery, turnaround or site-specific failure allowance. Not annual demand fulfilment."}


def _finite_number(value: Any) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value):
        return float(value)
    return None


def _climate_metrics(context: dict) -> dict:
    """Accept explicit summaries or real daily rows, keeping missing values null."""
    if context.get("models"):
        annual = []
        models = set()
        for member in context["models"]:
            model = member["model"]
            if model in models:
                raise ValueError("Duplicate climate model")
            models.add(model)
            years = set()
            for row in member.get("annual", []):
                year = row["year"]
                if year in years:
                    raise ValueError("Duplicate climate model/year")
                years.add(year)
                values = [_finite_number(row.get(k)) for k in
                          ("gdd0_degree_days", "gdd5_degree_days", "frost_free_run_days")]
                if any(v is None or v < 0 for v in values):
                    raise ValueError("Annual climate diagnostics must be finite and nonnegative")
                expected = (date(year + 1, 1, 1) - date(year, 1, 1)).days
                annual.append({"model": model, "year": year,
                               "gdd_base0_c_days": values[0], "gdd_base5_c_days": values[1],
                               "frost_free_days": values[2], "days_available": row.get("days"),
                               "complete_year": row.get("days") == expected})
        complete = [row for row in annual if row["complete_year"]]
        keys = ("gdd_base0_c_days", "gdd_base5_c_days", "frost_free_days")
        metrics = {key: mean(mean(row[key] for row in complete if row["model"] == model)
                             for model in models if any(row["model"] == model for row in complete))
                   if complete else None for key in keys}
        return {**metrics, "annual": annual,
                "basis": "equal model means of complete annual diagnostics; trajectories stay separate",
                "classification": "MODELED_CLIMATE_CONTEXT"}
    daily = context.get("daily")
    if daily is not None and hasattr(daily, "to_dict"):
        daily = daily.to_dict("records")
    if daily:
        years: dict[int, list[tuple[date, float, float]]] = {}
        dates = set()
        for item in daily:
            day = date.fromisoformat(str(item["date"])[:10])
            if day in dates:
                raise ValueError("Daily climate must contain one series, not duplicate model/date rows")
            dates.add(day)
            low = _finite_number(item.get("tmin_c"))
            high = _finite_number(item.get("tmax_c"))
            if low is None or high is None or low > high:
                raise ValueError("Climate daily Tmin/Tmax must be finite and ordered")
            years.setdefault(day.year, []).append((day, low, high))
        annual = []
        for year, rows in sorted(years.items()):
            rows.sort()
            gdd0 = sum(max(0, (lo + hi) / 2) for _, lo, hi in rows)
            gdd5 = sum(max(0, (lo + hi) / 2 - 5) for _, lo, hi in rows)
            longest = current = 0
            previous = None
            for day, lo, _ in rows:
                consecutive = previous is None or (day - previous).days == 1
                current = (current + 1 if consecutive else 1) if lo > 0 else 0
                longest = max(longest, current)
                previous = day
            expected_days = (date(year + 1, 1, 1) - date(year, 1, 1)).days
            annual.append({"year": year, "gdd_base0_c_days": gdd0, "gdd_base5_c_days": gdd5,
                           "frost_free_days": longest, "days_available": len(rows),
                           "complete_year": len(rows) == expected_days})
        complete = [r for r in annual if r["complete_year"]]
        return {"gdd_base0_c_days": mean(r["gdd_base0_c_days"] for r in complete) if complete else None,
                "gdd_base5_c_days": mean(r["gdd_base5_c_days"] for r in complete) if complete else None,
                "frost_free_days": mean(r["frost_free_days"] for r in complete) if complete else None,
                "annual": annual, "basis": "mean of complete years; annual heat sums do not add across years",
                "classification": "MODELED_CLIMATE_CONTEXT"}
    summary = context.get("summary", context)
    def value(*keys: str):
        for key in keys:
            v = _finite_number(summary.get(key))
            if v is not None:
                if v < 0:
                    raise ValueError(f"{key} cannot be negative")
                return v
        return None
    return {"gdd_base0_c_days": value("gdd_base0_c_days", "gdd0_c_days", "gdd0"),
            "gdd_base5_c_days": value("gdd_base5_c_days", "gdd5_c_days", "gdd5"),
            "frost_free_days": value("frost_free_days", "longest_frost_free_days"),
            "annual": [], "basis": "caller-supplied explicit summary; no GDD base substitution",
            "classification": "MODELED_CLIMATE_CONTEXT"}


def _field_screen(crop: dict, metrics: dict) -> dict:
    thermal = crop["climate"]
    requirement = thermal.get("gdd_requirement_c_days")
    actual = metrics["gdd_base0_c_days"] if thermal.get("gdd_base_c") == 0 else None
    if requirement is not None and actual is not None:
        below = actual < requirement
        yearly = metrics.get("annual", [])
        complete = [r for r in yearly if r["complete_year"]]
        return {"status": "screened_out" if below else "requires_agronomic_validation",
                "gdd_base_c": 0, "gdd_requirement_c_days": requirement,
                "gdd_available_c_days": actual,
                "years_meeting_heat_target": sum(r["gdd_base0_c_days"] >= requirement for r in complete) if complete else None,
                "years_evaluated": len(complete) or None,
                "reason": "Ortalama yıllık ısı birikimi, Alaska kaynaklı yaklaşık arpa olgunlaşma hedefinin altında."
                if below else "Yaklaşık arpa ısı hedefi karşılanıyor; çeşit, don, toprak ve su doğrulaması sürüyor.",
                "source_ids": [thermal["source_id"]], "classification": "TRANSFERRED_RESEARCH_SCREEN"}
    return {"status": "requires_agronomic_validation", "gdd_available_c_days": None,
            "gdd_requirement_c_days": requirement, "source_ids": crop["source_ids"],
            "reason": "Bu ürün için kuzeye aktarılabilir çeşit bazlı ısı/don eşiği doğrulanmadı; kontrollü ortam verimi açık tarlaya taşınmıyor.",
            "classification": "EVIDENCE_BOUNDARY"}


def _frontier_daily_years(daily: Any, context: dict) -> list[dict]:
    """Keep each GCM/year separate for nonlinear rolling-window screens."""
    if daily is None:
        return []
    if hasattr(daily, "to_dict"):
        daily = daily.to_dict("records")
    groups: dict[tuple[str, int], list] = {}
    dates = set()
    expected_models = {m["model"] for m in context.get("models", [])}
    period = context.get("period")
    for item in daily:
        day = date.fromisoformat(str(item["date"])[:10])
        model = str(item.get("model", "single_series"))
        if expected_models and model not in expected_models:
            raise ValueError("Frontier daily model does not match selected climate context")
        if period and not period[0] <= day.year <= period[1]:
            raise ValueError("Frontier daily period does not match selected climate context")
        key = (model, day)
        if key in dates:
            raise ValueError("Duplicate frontier climate model/date")
        dates.add(key)
        low, high = _finite_number(item.get("tmin_c")), _finite_number(item.get("tmax_c"))
        if low is None or high is None or low > high:
            raise ValueError("Frontier daily Tmin/Tmax must be finite and ordered")
        groups.setdefault((model, day.year), []).append((day, (low + high) / 2))
    if dates and expected_models and {model for model, _ in groups} != expected_models:
        raise ValueError("Frontier daily ensemble is missing a selected climate model")
    result = []
    for (model, year), rows in sorted(groups.items()):
        rows.sort()
        expected = (date(year + 1, 1, 1) - date(year, 1, 1)).days
        if len(rows) != expected:
            continue  # A truncated season cannot prove absence of a viable window.
        result.append({"model": model, "year": year, "days": rows,
                       "gdd_base0_c_days": sum(max(temperature, 0) for _, temperature in rows)})
    return result


def _window_test(crop_id: str, annual_daily: list[dict], parameters: dict) -> dict | None:
    cycle = parameters.get(crop_id + "_crop_cycle_days")
    envelope = parameters.get(crop_id + "_temperature_absolute_c")
    if not cycle or not envelope:
        return None
    duration = cycle["value"][0]
    low, high = envelope["value"]
    if (isinstance(duration, bool) or not isinstance(duration, int) or duration <= 0
            or _finite_number(low) is None or _finite_number(high) is None or low > high):
        raise ValueError("Invalid source-backed crop window")
    annual = []
    for item in annual_daily:
        rows = item["days"]
        rolling_sum = 0.0
        matching = 0
        warmest = None
        warmest_end = None
        for i, (day, temperature) in enumerate(rows):
            rolling_sum += temperature
            if i >= duration:
                rolling_sum -= rows[i - duration][1]
            if i < duration - 1:
                continue
            value = rolling_sum / duration
            matching += low <= value <= high
            if warmest is None or value > warmest:
                warmest, warmest_end = value, day
        annual.append({"model": item["model"], "year": item["year"],
                       "passed": matching > 0, "matching_windows": matching,
                       "warmest_window_mean_c": warmest,
                       "warmest_window_end": warmest_end.isoformat() if warmest_end else None})
    return {"id": "species_temperature_window", "status": "evaluated" if annual else "unknown",
            "minimum_window_days": duration, "temperature_envelope_c": [low, high],
            "annual": annual, "model_years_evaluated": len(annual) or None,
            "model_years_passing": sum(row["passed"] for row in annual) if annual else None,
            "source_url": envelope["source_url"], "source_locator": envelope["source_locator"],
            "source_parameter_ids": [cycle["id"], envelope["id"]],
            "classification": "SPECIES_ENVELOPE_RESEARCH_SCREEN",
            "interpretation": "Tür düzeyindeki en kısa kaynak çevrimi boyunca ortalama sıcaklık zarfı; çeşit olgunlaşması, don ve fotoperiyot doğrulaması değildir."}


def _climate_frontier(catalog: dict, ground: dict, metrics: dict, context: dict, daily: Any) -> dict:
    """Climate-only evidence first; no soil/energy/water inference in this gate.

    A pass of the available broad/ transferred screen is merely ``potential``.
    ``candidate`` is reserved for sufficient crop-specific climate evidence;
    none of the current outdoor entries satisfies that stronger condition.
    Frequencies are counts of modeled trajectories, never probabilities.
    """
    source_path = ROOT / "data/auto_baseline_parameters.json"
    parameter_raw = source_path.read_bytes()
    parameters = {row["id"]: row for row in json.loads(parameter_raw)["parameters"]}
    annual_daily = _frontier_daily_years(daily, context)
    rows = []
    sources = {}
    for crop in catalog["crops"]:
        tests = []
        requirement = crop["climate"].get("gdd_requirement_c_days")
        if requirement is not None and crop["climate"].get("gdd_base_c") == 0:
            records = annual_daily or [r for r in metrics["annual"] if r["complete_year"]]
            annual = [{"model": r.get("model", "single_series"), "year": r["year"],
                       "gdd_available_c_days": r["gdd_base0_c_days"],
                       "passed": r["gdd_base0_c_days"] >= requirement} for r in records]
            available = metrics["gdd_base0_c_days"]
            tests.append({"id": "heat_sum", "status": "evaluated" if annual or available is not None else "unknown",
                          "gdd_base_c": 0, "gdd_requirement_c_days": requirement,
                          "gdd_available_c_days": available,
                          "summary_passed": available >= requirement if available is not None else None,
                          "annual": annual, "model_years_evaluated": len(annual) or None,
                          "model_years_passing": sum(r["passed"] for r in annual) if annual else None,
                          "source_id": crop["climate"]["source_id"],
                          "classification": "TRANSFERRED_RESEARCH_SCREEN"})
        window = _window_test(crop["crop_id"], annual_daily, parameters)
        if window:
            source_id = "FAO_ECOCROP_" + crop["crop_id"].upper()
            window["source_id"] = source_id
            sources[source_id] = {"url": window["source_url"], "locator": window["source_locator"],
                                  "classification": "EXTERNAL_SPECIES_ENVELOPE", "locally_validated": False}
            tests.append(window)
        evaluated = [test for test in tests if test["status"] == "evaluated"]
        annual_tests = [test for test in evaluated if test["annual"]]
        simultaneous = []
        if annual_tests:
            by_test = [{(r["model"], r["year"]): r["passed"] for r in test["annual"]}
                       for test in annual_tests]
            common = set.intersection(*(set(r) for r in by_test))
            simultaneous = [{"model": model, "year": year,
                             "passed": all(test[(model, year)] for test in by_test)}
                            for model, year in sorted(common)]
            # Every applicable, evaluable test must pass in the SAME trajectory/year.
            possible = any(r["passed"] for r in simultaneous) if simultaneous else None
        else:
            summary_checks = [test["summary_passed"] for test in evaluated
                              if test.get("summary_passed") is not None]
            possible = all(summary_checks) if summary_checks else None
        status = "unknown" if possible is None else "potential" if possible else "screened_out"
        if status == "potential":
            reason = "Mevcut iklim ön elemesinin ısı koşulları bazı model yıllarında karşılanıyor; çeşit, don ve gün uzunluğu uygunluğu henüz doğrulanmadı." if simultaneous else "Mevcut ısı ön elemesi karşılanıyor; çeşit, don ve gün uzunluğu uygunluğu henüz doğrulanmadı."
        elif status == "screened_out":
            reason = "İncelenen model yıllarında mevcut ısı ön elemesi birlikte karşılanmıyor; bu, tüm çeşitler için yetiştirilemez hükmü değildir." if simultaneous else "Verilen dönem ortalaması mevcut ısı ön elemesini karşılamıyor; yıllar arası uygunluk bundan çıkarılamaz."
        elif crop.get("production"):
            reason = "Kaynak verimi kontrollü iç ortamdan geliyor; dış ortam iklim uygunluğu için doğrulanmış eşik bulunmuyor."
        else:
            reason = "Bu ürünün dış ortam uygunluğunu sınıflamak için kaynaklı çeşit eşiği veya gereken günlük iklim hesabı henüz tamamlanmadı."
        ground_gate = {"status": ground["method_policy"]["open_field"]["status"],
                       "eligible_for_normalized_plan": False,
                       "reason": ground["method_policy"]["open_field"]["reason"],
                       "source_ids": ground["permafrost"]["source_ids"],
                       "classification": "EXPLICIT_CONSERVATIVE_PLANNING_POLICY"}
        rows.append({"crop_id": crop["crop_id"], "name_tr": crop["name_tr"], "status": status,
                     "reason": reason, "tests": tests,
                     "source_ids": list(dict.fromkeys(crop["source_ids"] + [test["source_id"] for test in tests])),
                     "model_years_evaluated": len(simultaneous) or None,
                     "model_years_passing": sum(r["passed"] for r in simultaneous) if simultaneous else None,
                     "annual": simultaneous, "climate_suitable": None,
                     "outdoor_agronomically_validated": False,
                     "unresolved_climate_dimensions": ["cultivar_maturity", "frost_tolerance", "photoperiod"],
                     "ground_gate": ground_gate,
                     "controlled_environment_status": "candidate" if crop.get("production") else "evidence_needed",
                     "resource_gate": {"status": "not_evaluated_here", "evaluated_by": "north_planning"}})
    return {"scope": "outdoor_climate_only", "crops": rows, "sources": sources,
            "source_parameter_sha256": hashlib.sha256(parameter_raw).hexdigest(),
            "counts": {status: sum(row["status"] == status for row in rows)
                       for status in ("candidate", "potential", "screened_out", "unknown")},
            "status_meanings": {"candidate": "Yeterli ürüne özgü iklim kanıtıyla aday; mevcut katalogda bu düzeyde açık alan kararı yok.",
                                "potential": "Kaynaklı kısmi iklim ön elemesini geçer; yerel yetiştirme uygunluğu doğrulanmamıştır.",
                                "screened_out": "Uygulanan kaynaklı ön elemede elenir; tüm çeşitlerin imkânsızlığı anlamına gelmez.",
                                "unknown": "İklim uygunluğu için eşik veya gerekli iklim girdisi çözülmemiştir."},
            "classification": "EVIDENCE_BOUNDED_CLIMATE_FRONTIER",
            "limitations": ["Ön eleme sonucu zemin, su tahsisi, enerji veya yapı izni kararı değildir.",
                            "Model-yıl geçiş sayısı başarı olasılığı veya güven aralığı değildir.",
                            "Tür sıcaklık zarfında hareketli ortalama kullanımı açık araştırma kuralıdır; FAO tarafından doğrulanmış çeşit fenolojisi modeli değildir.",
                            "Xu et al. MaxEnt uygunluk haritası bu eşik hesabıyla yeniden üretilmiş değildir."]}


def evaluate_candidates(climate_context: dict, site_id: str = "longyearbyen", daily_frame: Any = None) -> dict:
    """Generate crop × method candidate records from research and site evidence.

    The caller owns resource feasibility and optimization. Status ``candidate``
    is conditional on engineered root isolation and maintained indoor setpoints.
    It does not say that energy/water/infrastructure has already been allocated.
    """
    catalog = get_catalog()
    ground = get_ground_evidence(site_id)
    metrics = _climate_metrics(climate_context)
    frontier = _climate_frontier(catalog, ground, metrics, climate_context,
                               daily_frame if daily_frame is not None else climate_context.get("daily"))
    candidates = []
    for entry in catalog["crops"]:
        crop = deepcopy(entry)
        screen = _field_screen(crop, metrics)
        field_status = "screened_out" if screen["status"] == "screened_out" else "requires_site_validation"
        methods = [{"method": "open_field", "status": field_status,
                    "eligible_for_normalized_plan": False,
                    "reason": screen["reason"] if field_status == "screened_out" else ground["method_policy"]["open_field"]["reason"],
                    "climate_screen": screen, "source_ids": list(dict.fromkeys(crop["source_ids"] + ground["permafrost"]["source_ids"])),
                    "classification": "EXPLICIT_CONSERVATIVE_PLANNING_POLICY"}]
        for method in ("greenhouse", "hydroponics"):
            valid = method in crop["compatible_methods"] and crop.get("production") is not None
            methods.append({"method": method, "status": "candidate" if valid else "evidence_needed",
                            "eligible_for_normalized_plan": valid,
                            "reason": "Yayımlanmış kutup kontrollü üretim verimi var; yalıtılmış kök ortamı, belirtilen ışık/sıcaklık ve kaynak koşullarıyla karşılaştırılabilir."
                            if valid else "Bu yöntem için alan ve çevrim başına üretim kanıtı katalogda henüz doğrulanmadı.",
                            "root_isolation_required": True, "construction_validated": False,
                            "source_ids": crop["source_ids"], "classification": "CONTROLLED_POLAR_ANALOGUE" if valid else "UNRESOLVED_METHOD_EVIDENCE"})
        crop["methods"] = methods
        crop["climate_screen"] = screen
        crop["climate_frontier"] = next(row for row in frontier["crops"] if row["crop_id"] == crop["crop_id"])
        crop["normalized_plan_eligible"] = any(m["eligible_for_normalized_plan"] for m in methods)
        candidates.append(crop)
    return {"schema_version": "2.0", "site_id": site_id, "candidates": candidates,
            "climate_metrics": metrics, "climate_frontier": frontier,
            "ground_evidence": ground, "sources": {**catalog["sources"], **frontier["sources"]},
            "planning_basis": catalog["planning_basis"], "policy": ground["method_policy"],
            "counts": {"catalogued": len(candidates),
                       "controlled_evidence_candidates": sum(c["normalized_plan_eligible"] for c in candidates)},
            "locally_validated_production_plan": False}
