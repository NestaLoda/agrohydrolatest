"""One named HighResMIP model, paired periods; external projections, not observations.

Run online once, then rerun offline from verified immutable raw snapshots.
--refresh downloads a new snapshot without replacing earlier raw bytes.
Only writes data/north/. No SSP or ensemble is inferred from the API model name.
"""
from __future__ import annotations

import argparse
import calendar
import csv
import hashlib
import io
import json
import math
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "north"
MODEL = "EC_Earth3P_HR"
DISABLE_BIAS_CORRECTION = True
PERIODS = {"baseline": ("1995-01-01", "2014-12-31"),
           "future": ("2030-01-01", "2049-12-31")}
VARIABLES = {"temperature_2m_min": "°C", "temperature_2m_max": "°C", "precipitation_sum": "mm"}
DOC_URL = "https://open-meteo.com/en/docs/climate-api"
MODEL_DOI = "https://doi.org/10.22033/ESGF/CMIP6.2323"
SCENARIO = "HighResMIP forcing; provider describes it as close to RCP8.5; no selectable SSP"
LIMITATIONS = [
    "External single-model projection; neither observation nor multi-model ensemble.",
    "The baseline is historical model output, not observed weather or the separate ERA5 series.",
    "Both periods use the same named model with bias correction disabled; raw model-grid biases remain, and member/version are not exposed by this API response.",
    "Annual spread describes simulated interannual variability, not model/scenario uncertainty or a confidence interval.",
    "GDD5 and frost-free run are descriptive climate indicators, not a crop yield or suitability validation.",
    "Precipitation includes snow water equivalent; it is not runoff, stored supply or available irrigation water.",
    "One model grid point is not all of Svalbard, Barents or the Arctic, and not a confirmed expedition station.",
    "Atmospheric air-temperature projections cannot be substituted for marine source-water temperature or PWN observations.",
    "Requested future 2031–2050 had an entirely missing 2050; comparison explicitly uses 2030–2049, not 2031–2050.",
    "The first bias-corrected baseline had 108 Tmin>Tmax days and was rejected; both retained periods use bias correction disabled, without swapping values.",
]


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def immutable(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as out:
            out.write(raw)
    except FileExistsError:
        if path.read_bytes() != raw:
            raise ValueError(f"Immutable content differs: {path}")


def validate(payload, start, end):
    if payload.get("error"):
        raise ValueError(payload.get("reason", "Provider error"))
    a, b = date.fromisoformat(start), date.fromisoformat(end)
    dates = [(a + timedelta(days=i)).isoformat() for i in range((b - a).days + 1)]
    daily = payload["daily"]
    if daily["time"] != dates:
        raise ValueError("Missing, duplicate, truncated or out-of-order dates")
    if payload.get("utc_offset_seconds") != 0:
        raise ValueError("UTC daily output required")
    for key, unit in VARIABLES.items():
        if payload["daily_units"].get(key) != unit or len(daily[key]) != len(dates):
            raise ValueError(f"Unit/length mismatch: {key}")
        for value in daily[key]:
            if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value)):
                raise ValueError(f"Invalid numeric value: {key}")
    for low, high, rain in zip(*(daily[k] for k in VARIABLES)):
        if low is not None and high is not None and low > high:
            raise ValueError("Tmin exceeds Tmax")
        if rain is not None and rain < 0:
            raise ValueError("Negative precipitation")
    return len(dates)


def metrics(payload, period):
    daily = payload["daily"]
    grouped = {}
    for i, stamp in enumerate(daily["time"]):
        grouped.setdefault(int(stamp[:4]), []).append(i)
    annual = []
    for year, indices in sorted(grouped.items()):
        expected = 366 if calendar.isleap(year) else 365
        missing = sum(any(daily[k][i] is None for k in VARIABLES) for i in indices)
        complete = len(indices) == expected and missing == 0
        gdd = precip = 0.0
        run = longest = 0
        if complete:
            for i in indices:
                low, high, rain = (daily[k][i] for k in VARIABLES)
                gdd += max((low + high) / 2 - 5, 0)
                precip += rain
                run = run + 1 if low > 0 else 0
                longest = max(longest, run)
        annual.append({"year": year, "period": period, "day_count": len(indices),
                       "missing_day_count": missing, "complete": complete,
                       "gdd5_degree_days": round(gdd, 6) if complete else None,
                       "frost_free_run_days": longest if complete else None,
                       "precipitation_mm": round(precip, 6) if complete else None})
    return annual


def aggregate(annual, start, end):
    valid = [row for row in annual if row["complete"]]
    out = {"period": f"{start[:4]}–{end[:4]}", "start_date": start, "end_date": end,
           "years": len(annual), "complete_years": len(valid), "complete": len(valid) == len(annual)}
    for name in ("gdd5_degree_days", "frost_free_run_days", "precipitation_mm"):
        values = [row[name] for row in valid]
        # Never label a partial-period mean as the full 20-year comparison.
        out["mean_annual_" + name] = round(sum(values) / len(values), 6) if values and out["complete"] else None
        out["annual_range_" + name] = [min(values), max(values)] if values and out["complete"] else None
    return out


def acquire(period, refresh=False):
    start, end = PERIODS[period]
    pointer = DATA / f"{period}_metadata.json"
    if pointer.exists() and not refresh:
        metadata = json.loads(pointer.read_text(encoding="utf-8"))
        if metadata["model"] != MODEL or metadata["period"] != [start, end] or metadata["disable_bias_correction"] is not DISABLE_BIAS_CORRECTION:
            raise ValueError("Cached model/period/correction contract mismatch")
        raw = (ROOT / metadata["raw_path"]).read_bytes()
        if digest(raw) != metadata["sha256"]:
            raise ValueError("Cached raw hash mismatch")
        payload = json.loads(raw)
        validate(payload, start, end)
        return metadata, payload
    params = {"latitude": 78.22, "longitude": 15.65, "start_date": start, "end_date": end,
              "models": MODEL, "daily": ",".join(VARIABLES), "disable_bias_correction": str(DISABLE_BIAS_CORRECTION).lower(),
              "cell_selection": "land", "temperature_unit": "celsius", "precipitation_unit": "mm"}
    url = "https://climate-api.open-meteo.com/v1/climate?" + urlencode(params)
    access = datetime.now(timezone.utc).isoformat()
    try:
        with urlopen(Request(url, headers={"User-Agent": "SustainableProductionFrontier-Research/0.2"}), timeout=50) as response:
            raw = response.read()
        # Preserve even rejected provider responses for an auditable failure trail.
        immutable(DATA / "raw" / f"{period}_{MODEL}_{digest(raw)}.json", raw)
        payload = json.loads(raw)
        count = validate(payload, start, end)
    except Exception as exc:
        attempt = {"accessed_at_utc": access, "url": url, "status": "failed", "error": str(exc)}
        content = encode(attempt)
        immutable(DATA / "attempts" / f"{digest(content)}.json", content)
        raise
    sha = digest(raw)
    path = DATA / "raw" / f"{period}_{MODEL}_{sha}.json"
    immutable(path, raw)
    metadata = {"dataset_id": f"open_meteo_highresmip_{MODEL}_longyearbyen_{period}",
                "source_kind": "EXTERNAL_CLIMATE_MODEL", "provider": "Open-Meteo / EC-Earth Consortium / CMIP6 HighResMIP",
                "model": MODEL, "scenario_label": SCENARIO, "ssp": None, "member_id": None,
                "upstream_version": None, "version_note": "API does not expose member/upstream version; immutable retrieval snapshot used",
                "period": [start, end], "disable_bias_correction": DISABLE_BIAS_CORRECTION,
                "bias_correction": "Disabled for both periods; uncorrected model-grid output",
                "requested_coordinate": {"latitude": 78.22, "longitude": 15.65},
                "returned_coordinate": {k: payload[k] for k in ("latitude", "longitude", "elevation")},
                "utc_offset_seconds": payload["utc_offset_seconds"], "units": payload["daily_units"],
                "row_count": count, "missing_values": {k: sum(v is None for v in payload["daily"][k]) for k in VARIABLES},
                "source_url": url, "documentation_url": DOC_URL, "model_doi": MODEL_DOI,
                "accessed_at_utc": access, "license": "CC BY 4.0; acknowledge Open-Meteo, CMIP6 and EC-Earth Consortium",
                "raw_path": path.relative_to(ROOT).as_posix(), "sha256": sha, "limitations": LIMITATIONS}
    content = encode(metadata)
    immutable(DATA / "metadata_snapshots" / f"{digest(content)}.json", content)
    pointer.write_bytes(content)
    return metadata, payload


def main(refresh=False):
    DATA.mkdir(parents=True, exist_ok=True)
    provenance, annual, periods, all_daily = [], [], {}, []
    for period, (start, end) in PERIODS.items():
        metadata, payload = acquire(period, refresh)
        provenance.append(metadata)
        yearly = metrics(payload, period)
        annual.extend(yearly)
        periods[period] = aggregate(yearly, start, end)
        for i, stamp in enumerate(payload["daily"]["time"]):
            all_daily.append([period, stamp, *(payload["daily"][k][i] for k in VARIABLES), metadata["dataset_id"]])
    if provenance[0]["returned_coordinate"] != provenance[1]["returned_coordinate"]:
        raise ValueError("Baseline and future grid/elevation differ")
    delta = {}
    for name in ("gdd5_degree_days", "frost_free_run_days", "precipitation_mm"):
        key = "mean_annual_" + name
        before, after = periods["baseline"][key], periods["future"][key]
        delta[name] = round(after - before, 6) if before is not None and after is not None else None
    summary = {"schema_version": "1.0", "status": "ready" if all(p["complete"] for p in periods.values()) else "incomplete",
               "source_kind": "EXTERNAL_CLIMATE_MODEL", "site_id": "longyearbyen", "model": MODEL,
               "requested_future_period": "2031–2050", "period_adjustment_reason": "2050 returned dates but all 365 daily values were null; two complete 20-year periods use 2030–2049 instead",
               "scenario_label": SCENARIO, "ssp": None, "bias_correction": provenance[0]["bias_correction"],
               **periods, "delta": delta, "annual_metrics": annual, "provenance": provenance,
               "limitations": LIMITATIONS, "marine_observations_available": False,
               "method": {"gdd5": "sum(max((Tmin+Tmax)/2 - 5, 0))", "frost_free_run": "longest consecutive Tmin > 0 run within each calendar year",
                          "precipitation": "annual sum; includes snow water equivalent", "period_comparison": "difference of 20 annual means; no significance/uncertainty claim"}}
    content = encode(summary)
    immutable(DATA / "summary_snapshots" / f"{digest(content)}.json", content)
    (DATA / "summary.json").write_bytes(content)
    for name, fields, rows in (("daily.csv", ["period", "date", "tmin_c", "tmax_c", "precipitation_mm", "dataset_id"], all_daily),
                               ("annual_metrics.csv", list(annual[0]), [list(row.values()) for row in annual])):
        buff = io.StringIO(newline="")
        writer = csv.writer(buff, lineterminator="\n")
        writer.writerow(fields)
        writer.writerows(rows)
        (DATA / name).write_text(buff.getvalue(), encoding="utf-8")
    print(json.dumps({"status": summary["status"], "model": MODEL, **periods, "delta": delta}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true")
    main(parser.parse_args().refresh)
