"""Offline checks of the actual scientific package and source boundary behavior."""
import copy
import csv
import hashlib
import io
import json
import shutil
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

from scripts import ingest_data as ingest

ROOT = Path(__file__).resolve().parents[1]


class RealClimatePackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / "data/manifest.json").read_text(encoding="utf-8"))
        with (ROOT / "data/processed/climate.csv").open(encoding="utf-8", newline="") as handle:
            cls.rows = list(csv.DictReader(handle))

    def test_raw_provenance_and_grid_selection_are_explicit(self):
        records = self.manifest["datasets"]
        self.assertEqual(len(records), 6)
        self.assertEqual({m["requested_location"]["site_id"] for m in records}, {"konya", "seyhan_adana", "gediz_manisa", "gap_sanliurfa", "trakya_edirne", "longyearbyen"})
        for metadata in records:
            with self.subTest(dataset=metadata["dataset_id"]):
                raw_path = (ROOT / metadata["local_raw_path"]).resolve()
                self.assertTrue(raw_path.is_relative_to((ROOT / "data/raw").resolve()))
                content = raw_path.read_bytes()
                self.assertEqual(hashlib.sha256(content).hexdigest(), metadata["content_sha256"])
                payload = json.loads(content)
                self.assertEqual(metadata["returned_grid_location"], {key: payload[key] for key in ("latitude", "longitude", "elevation")})
                query = parse_qs(urlparse(metadata["source_url"]).query)
                self.assertEqual(query["models"], ["era5"])
                self.assertEqual(query["elevation"], ["nan"])
                self.assertEqual(query["timezone"], ["UTC"])
                self.assertEqual(metadata["classification"], "MODEL / REANALYSIS")
                self.assertIn("CC BY 4.0", metadata["license"])
                for key in ("provider", "version", "access_date", "temporal_resolution", "spatial_resolution", "access_limits"):
                    self.assertTrue(metadata[key], key)

    def test_processed_values_match_source_bytes_without_unit_changes(self):
        self.assertEqual(len(self.rows), 4380)
        observed_keys = {(r["site_id"], r["date"]) for r in self.rows}
        self.assertEqual(len(observed_keys), len(self.rows), "Duplicate dates would distort sums and seasonal balances")
        source_to_column = {
            "temperature_2m_min": ("tmin_c", "°C"),
            "temperature_2m_max": ("tmax_c", "°C"),
            "precipitation_sum": ("precipitation_mm", "mm"),
            "et0_fao_evapotranspiration": ("et0_mm", "mm"),
        }
        expected_dates = [(date(2022, 1, 1) + timedelta(days=i)).isoformat() for i in range(730)]
        for metadata in self.manifest["datasets"]:
            site = metadata["requested_location"]["site_id"]
            rows = [r for r in self.rows if r["site_id"] == site]
            self.assertEqual([r["date"] for r in rows], expected_dates)
            payload = json.loads((ROOT / metadata["local_raw_path"]).read_bytes())
            self.assertEqual(payload["utc_offset_seconds"], 0)
            for source, (column, unit) in source_to_column.items():
                self.assertEqual(payload["daily_units"][source], unit)
                self.assertEqual(metadata["units"][column], unit)
                for i, row in enumerate(rows):
                    with self.subTest(site=site, date=row["date"], variable=column):
                        expected = payload["daily"][source][i]
                        self.assertEqual(None if row[column] == "" else float(row[column]), expected)
                        self.assertEqual(row["dataset_id"], metadata["dataset_id"])

    def test_cached_acquisition_needs_no_network_and_changes_no_raw_bytes(self):
        def no_network(*args, **kwargs):
            raise AssertionError("Cached dataset attempted a network call")
        with patch.object(ingest, "urlopen", side_effect=no_network):
            for site in ingest.SITES:
                metadata, payload = ingest.acquire(site, refresh=False)
                self.assertEqual(ingest.validate(payload), 730)
                self.assertEqual(hashlib.sha256((ROOT / metadata["local_raw_path"]).read_bytes()).hexdigest(), metadata["content_sha256"])

    def test_parquet_and_csv_deliver_identical_scientific_values(self):
        import pandas as pd

        readable = pd.read_csv(ROOT / "data/processed/climate.csv", float_precision="round_trip")
        columnar = pd.read_parquet(ROOT / "data/processed/climate.parquet")
        pd.testing.assert_frame_equal(readable, columnar, check_exact=True)


class IngestBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        manifest = json.loads((ROOT / "data/manifest.json").read_text(encoding="utf-8"))
        cls.example = json.loads((ROOT / manifest["datasets"][0]["local_raw_path"]).read_bytes())

    def test_wrong_units_bad_time_series_and_physical_errors_are_rejected(self):
        for error in ("units", "timezone", "duplicate_date", "missing_date", "unequal_length", "negative_precipitation", "inverted_temperature"):
            bad = copy.deepcopy(self.example)
            if error == "units": bad["daily_units"]["precipitation_sum"] = "inch"
            elif error == "timezone": bad["utc_offset_seconds"] = 10800
            elif error == "duplicate_date": bad["daily"]["time"][1] = bad["daily"]["time"][0]
            elif error == "missing_date": bad["daily"]["time"].pop()
            elif error == "unequal_length": bad["daily"]["et0_fao_evapotranspiration"].pop()
            elif error == "negative_precipitation": bad["daily"]["precipitation_sum"][0] = -1
            else: bad["daily"]["temperature_2m_min"][0] = bad["daily"]["temperature_2m_max"][0] + 1
            with self.subTest(error=error), self.assertRaises(ValueError):
                ingest.validate(bad)

    def test_nonfinite_numbers_are_not_accepted_as_measurements(self):
        for value in (float("nan"), float("inf"), -float("inf"), True, False):
            bad = copy.deepcopy(self.example)
            bad["daily"]["et0_fao_evapotranspiration"][0] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                ingest.validate(bad)

    def test_missing_value_stays_missing(self):
        missing = copy.deepcopy(self.example)
        missing["daily"]["et0_fao_evapotranspiration"][0] = None
        ingest.validate(missing)
        self.assertIsNone(missing["daily"]["et0_fao_evapotranspiration"][0])

    def test_immutable_writer_rejects_conflicting_content(self):
        with tempfile.TemporaryDirectory(prefix="spf_data_test_") as folder:
            target = Path(folder) / "raw.json"
            ingest.write_immutable(target, b'{"temperature": 1}')
            ingest.write_immutable(target, b'{"temperature": 1}')
            with self.assertRaises(ValueError):
                ingest.write_immutable(target, b'{"temperature": 99}')
            self.assertEqual(target.read_bytes(), b'{"temperature": 1}')

    def test_tampered_cached_file_is_rejected_before_use(self):
        with tempfile.TemporaryDirectory(prefix="spf_data_test_") as folder:
            root = Path(folder)
            data = root / "data"
            (data / "metadata").mkdir(parents=True)
            dataset_id = "open_meteo_era5_konya_2022_2023"
            (data / "broken.json").write_bytes(b"changed content")
            (data / "metadata" / f"{dataset_id}.json").write_text(json.dumps({"local_raw_path": "data/broken.json", "content_sha256": "0" * 64}), encoding="utf-8")
            with patch.object(ingest, "ROOT", root), patch.object(ingest, "DATA", data):
                with self.assertRaisesRegex(ValueError, "integrity"):
                    ingest.acquire(ingest.SITES[0], refresh=False)

    def test_changed_refresh_creates_new_identity_without_overwriting_history(self):
        first = json.dumps(self.example).encode()
        modified = copy.deepcopy(self.example)
        modified["daily"]["precipitation_sum"][0] += 0.1
        second = json.dumps(modified).encode()
        with tempfile.TemporaryDirectory(prefix="spf_refresh_test_") as folder:
            root = Path(folder)
            with patch.object(ingest, "ROOT", root), patch.object(ingest, "DATA", root / "data"):
                with patch.object(ingest, "urlopen", return_value=io.BytesIO(first)):
                    one, _ = ingest.acquire(ingest.SITES[0], refresh=True)
                with patch.object(ingest, "urlopen", return_value=io.BytesIO(second)):
                    two, _ = ingest.acquire(ingest.SITES[0], refresh=True)
                self.assertNotEqual(one["dataset_id"], two["dataset_id"])
                self.assertEqual((root / one["local_raw_path"]).read_bytes(), first)
                self.assertEqual((root / two["local_raw_path"]).read_bytes(), second)
                self.assertEqual(len(list((root / "data/metadata/snapshots").glob("*.json"))), 2)
                with patch.object(ingest, "urlopen", side_effect=AssertionError("No network allowed")):
                    cached, _ = ingest.acquire(ingest.SITES[0], refresh=False)
                    self.assertEqual(cached, two)

    def test_processed_edit_is_rejected_even_after_successful_startup(self):
        from backend import repository
        from backend.provenance import ProvenanceStore

        with tempfile.TemporaryDirectory(prefix="spf_derivative_test_") as folder:
            root = Path(folder)
            (root / "data/processed").mkdir(parents=True)
            shutil.copyfile(ROOT / "data/manifest.json", root / "data/manifest.json")
            shutil.copyfile(ROOT / "data/processed/climate.csv", root / "data/processed/climate.csv")
            for metadata in json.loads((root / "data/manifest.json").read_text(encoding="utf-8"))["datasets"]:
                target = root / metadata["local_raw_path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / metadata["local_raw_path"], target)
            shutil.copyfile(ROOT / "data/manifest_turkey_recent.json", root / "data/manifest_turkey_recent.json")
            shutil.copyfile(ROOT / "data/processed/climate_turkey_recent.csv", root / "data/processed/climate_turkey_recent.csv")
            for metadata in json.loads((root / "data/manifest_turkey_recent.json").read_text(encoding="utf-8"))["datasets"]:
                target = root / metadata["local_raw_path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / metadata["local_raw_path"], target)
            with patch.object(repository, "ROOT", root):
                repository.register_sources(ProvenanceStore(root / "provenance.sqlite"))
                self.assertEqual(len(repository.load_verified_climate()), 4380)
                path = root / "data/processed/climate.csv"
                with path.open(encoding="utf-8", newline="") as handle:
                    reader = csv.DictReader(handle)
                    fields, rows = reader.fieldnames, list(reader)
                rows[0]["precipitation_mm"] = str(float(rows[0]["precipitation_mm"]) + 20)
                with path.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=fields)
                    writer.writeheader()
                    writer.writerows(rows)
                with self.assertRaisesRegex(ValueError, "kaynak değerleri"):
                    repository.transfer()


if __name__ == "__main__":
    unittest.main()
