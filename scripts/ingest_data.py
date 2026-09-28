"""Small real ERA5 package. Raw bytes are content-addressed, never overwritten.

Run once online; subsequent runs verify cached source files and work offline.
Use --refresh to acquire a new immutable snapshot, keeping previous raw data.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
START, END = "2022-01-01", "2023-12-31"
SITES = [
    {"site_id": "konya", "name": "Konya", "latitude": 37.87, "longitude": 32.49, "role": "historical_pilot_comparison"},
    {"site_id": "seyhan_adana", "name": "Seyhan / Adana", "latitude": 37.00, "longitude": 35.32, "role": "transfer_demonstration"},
    {"site_id": "gediz_manisa", "name": "Gediz / Manisa", "latitude": 38.61, "longitude": 27.43, "role": "transfer_demonstration"},
    {"site_id": "gap_sanliurfa", "name": "GAP / Harran–Şanlıurfa", "latitude": 36.87, "longitude": 39.03, "role": "transfer_demonstration"},
    {"site_id": "trakya_edirne", "name": "Trakya / Edirne", "latitude": 41.68, "longitude": 26.56, "role": "transfer_demonstration"},
    {"site_id": "longyearbyen", "name": "Longyearbyen", "latitude": 78.22, "longitude": 15.65, "role": "northern_controlled_production_context"},
]
VARIABLES = {"temperature_2m_min": "tmin_c", "temperature_2m_max": "tmax_c", "precipitation_sum": "precipitation_mm", "et0_fao_evapotranspiration": "et0_mm"}
UNITS = {"temperature_2m_min": "°C", "temperature_2m_max": "°C", "precipitation_sum": "mm", "et0_fao_evapotranspiration": "mm"}


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def write_immutable(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(content)
    except FileExistsError:
        if path.read_bytes() != content:
            raise ValueError(f"Immutable content mismatch: {path}")


def validate(payload: dict, start: str = START, end: str = END) -> int:
    if payload.get("error"):
        raise ValueError(payload.get("reason", "Provider error"))
    daily = payload["daily"]
    expected = [(date.fromisoformat(start) + timedelta(days=i)).isoformat() for i in range((date.fromisoformat(end) - date.fromisoformat(start)).days + 1)]
    if daily["time"] != expected:
        raise ValueError("Dates are incomplete, duplicated or out of order")
    if payload["utc_offset_seconds"] != 0:
        raise ValueError("Expected UTC daily aggregation")
    for key, unit in UNITS.items():
        if payload["daily_units"].get(key) != unit:
            raise ValueError(f"Unexpected unit for {key}")
        if len(daily[key]) != len(expected):
            raise ValueError(f"Length mismatch for {key}")
        for value in daily[key]:
            if value is not None and (isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value)):
                raise ValueError(f"Non-finite or non-numeric source value in {key}")
    for i, (low, high) in enumerate(zip(daily["temperature_2m_min"], daily["temperature_2m_max"])):
        if low is not None and high is not None and low > high:
            raise ValueError(f"Tmin exceeds Tmax at row {i}")
    for key in ("precipitation_sum", "et0_fao_evapotranspiration"):
        if any(v is not None and v < 0 for v in daily[key]):
            raise ValueError(f"Negative {key}")
    return len(expected)


def acquire(site: dict, refresh: bool, start: str = START, end: str = END) -> tuple[dict, dict]:
    dataset_id = f"open_meteo_era5_{site['site_id']}_{start[:4]}_{end[:4]}"
    metadata_path = DATA / "metadata" / f"{dataset_id}.json"
    if metadata_path.exists() and not refresh:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        raw = (ROOT / metadata["local_raw_path"]).read_bytes()
        if digest(raw) != metadata["content_sha256"]:
            raise ValueError(f"Raw integrity failure: {dataset_id}")
        payload = json.loads(raw)
        validate(payload, start, end)
        return metadata, payload
    params = {"latitude": site["latitude"], "longitude": site["longitude"], "start_date": start, "end_date": end, "daily": ",".join(VARIABLES), "models": "era5", "timezone": "UTC", "temperature_unit": "celsius", "precipitation_unit": "mm", "elevation": "nan", "cell_selection": "land"}
    url = "https://archive-api.open-meteo.com/v1/archive?" + urlencode(params)
    with urlopen(Request(url, headers={"User-Agent": "SustainableProductionFrontier-Research/0.1"}), timeout=90) as response:
        raw = response.read()
    payload = json.loads(raw)
    count = validate(payload, start, end)
    sha = digest(raw)
    relative = Path("data/raw/open_meteo") / f"{dataset_id}_{sha}.json"
    write_immutable(ROOT / relative, raw)
    metadata = {
        "dataset_id": f"{dataset_id}_{sha[:12]}", "provider": "Open-Meteo; underlying ERA5: ECMWF / Copernicus Climate Change Service",
        "source_url": url, "documentation_url": "https://open-meteo.com/en/docs/historical-weather-api",
        "upstream_doi": "10.24381/cds.adbb2d47", "version": "Archive API v1; models=era5; provider does not expose numerical processing build; SHA256 pins returned bytes",
        "access_date": datetime.now(timezone.utc).isoformat(), "temporal_resolution": "daily UTC aggregation of hourly reanalysis", "temporal_start": start, "temporal_end": end,
        "spatial_resolution": "ERA5 0.25 degree grid; point extraction, not basin average; elevation downscaling disabled",
        "requested_location": site, "returned_grid_location": {key: payload[key] for key in ("latitude", "longitude", "elevation")},
        "units": {VARIABLES[key]: unit for key, unit in UNITS.items()}, "variables": list(VARIABLES.values()),
        "license": "Open-Meteo API data CC BY 4.0; attribution to Open-Meteo and ERA5/Copernicus", "license_url": "https://open-meteo.com/en/terms",
        "access_limits": "Free API non-commercial only; <10000 calls/day, <5000/hour, <600/minute; no credential used",
        "classification": "MODEL / REANALYSIS", "content_sha256": sha, "local_raw_path": relative.as_posix(), "row_count": count,
        "missing_values": {VARIABLES[key]: sum(x is None for x in payload["daily"][key]) for key in VARIABLES},
        "transformations": "Rename variables only; temperature degC, daily precipitation and ET0 mm; missing values retained as null/empty, never zero-filled",
        "limitations": ["ET0 is provider-derived FAO56 grass reference evapotranspiration, not crop ET, actual ET, available irrigation water or runoff.", "Precipitation includes snowfall water equivalent; precipitation is not immediately usable supply, especially in Arctic snow conditions.", "One grid cell cannot validate a basin; two years are a demonstration, not a climate normal or future projection.", "Local terrain/coastal representativeness remains unresolved; actual returned grid coordinate preserved."]
    }
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    encoded = (json.dumps(metadata, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    snapshot_path = DATA / "metadata" / "snapshots" / f"{dataset_id}_{sha}.json"
    if snapshot_path.exists():
        # A provider may return identical bytes on refresh. Preserve first access.
        encoded = snapshot_path.read_bytes()
        metadata = json.loads(encoded)
    else:
        write_immutable(snapshot_path, encoded)
    metadata_path.write_bytes(encoded)
    return metadata, payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    datasets, rows = [], []
    for site in SITES:
        metadata, payload = acquire(site, args.refresh)
        datasets.append(metadata)
        for index, timestamp in enumerate(payload["daily"]["time"]):
            rows.append({"site_id": site["site_id"], "date": timestamp, **{output: payload["daily"][source][index] for source, output in VARIABLES.items()}, "dataset_id": metadata["dataset_id"]})
        print(f"{site['site_id']}: {metadata['row_count']} real daily records; sha256={metadata['content_sha256']}", flush=True)
    processed = DATA / "processed"
    processed.mkdir(parents=True, exist_ok=True)
    with (processed / "climate.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (DATA / "manifest.json").write_text(json.dumps({"schema_version": "1.0", "datasets": datasets}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DATA / "sites.json").write_text(json.dumps(SITES, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    import pandas as pd
    pd.DataFrame(rows).to_parquet(processed / "climate.parquet", index=False)
    print(f"Completed {len(rows)} rows; missing values retained; CSV + Parquet + manifest.")


if __name__ == "__main__":
    main()
