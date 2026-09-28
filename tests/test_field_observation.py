"""External-profile pathway tests using temporary, explicitly synthetic fixtures.

EXTERNAL_OBSERVATION is exercised as an API classification, not asserted as the
scientific origin of these numbers. Nothing is written to repository data/.
"""
import csv
import importlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import gsw
from fastapi.testclient import TestClient
from pydantic import ValidationError

from backend.contracts import FieldComparisonRequest, FieldPoint
from backend.field import compare_field
from backend.provenance import ProvenanceStore, digest


def unit_fixture_csv(**changes):
    """One invented sample; pressure permits a real GSW conversion code path."""
    row = {
        "schema_version": "1.0", "source_kind": "EXTERNAL_OBSERVATION",
        "device_id": "UNIT_FIXTURE_NOT_A_REAL_DEVICE", "experiment_id": "UNIT_FIXTURE",
        "cast_id": "UNIT_FIXTURE_NOT_AN_OBSERVATION", "sample_index": 0,
        "timestamp_utc": "2026-09-22T12:00:00Z", "elapsed_ms": 0,
        "raw_conductivity_signal": 100, "temperature_C": 8,
        "encoder_count": "", "cable_out_m": "", "pressure_dbar": 5,
        "latitude": 78.22, "longitude": 15.65, "calibration_id": "",
        "quality_flag": "OK",
    }
    row.update(changes)
    buff = io.StringIO(newline="")
    writer = csv.DictWriter(buff, fieldnames=list(row), lineterminator="\n")
    writer.writeheader()
    writer.writerow(row)
    return buff.getvalue().encode("utf-8")


class RegisteredExternalProfileTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="pwn-unit-fixture-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.store = ProvenanceStore(self.root / "unit-fixture.sqlite")
        self.root_patch = patch("backend.field.ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def register_fixture(self, row_changes=None, **metadata_changes):
        raw = unit_fixture_csv(**(row_changes or {}))
        path = self.root / "data/pwn/raw" / (digest(raw) + ".csv")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        metadata = {
            "dataset_id": "unit_fixture_" + str(len(self.store.datasets())),
            "content_sha256": digest(raw), "classification": "EXTERNAL_OBSERVATION",
            "provider": "SYNTHETIC UNIT FIXTURE — NOT A SCIENTIFIC OBSERVATION",
            "source_url": "https://example.invalid/unit-fixture/no-real-data",
            "access_date": "2026-09-22", "license": "UNIT TEST ONLY",
            "units": {"raw_conductivity_signal": "arbitrary_unit", "temperature_C": "°C"},
            "local_raw_path": path.relative_to(self.root).as_posix(),
            "depth_method": "pressure_derived", "temperature_kind": "in_situ",
            "fixture_only": True,
        }
        metadata.update(metadata_changes)
        self.store.register(metadata, raw)
        return metadata, path

    def request_for(self, metadata, **changes):
        request = {
            "evidence_kind": "EXTERNAL_OBSERVATION",
            "observed_dataset_id": metadata["dataset_id"], "observed_sample_index": 0,
            "model_source_url": "https://example.invalid/unit-fixture/model-expectation",
            "expected": FieldPoint(temperature_C=10, depth_m=float(-gsw.z_from_p(5, 78.22))),
        }
        request.update(changes)
        return FieldComparisonRequest(**request)

    def test_registered_pressure_sample_overrides_user_observation_and_keeps_hash(self):
        metadata, path = self.register_fixture()
        raw_before = path.read_bytes()
        q = self.request_for(metadata, observed=FieldPoint(temperature_C=40, latitude=0, depth_m=900))
        result = compare_field(q, self.store)
        self.assertTrue(result["collocation"]["passed"])
        self.assertEqual(result["observed"]["temperature_C"], 8)
        self.assertEqual(result["observed"]["latitude"], 78.22)
        self.assertAlmostEqual(result["observed"]["depth_m"], -gsw.z_from_p(5, 78.22))
        self.assertEqual(result["residual_temperature_C"], -2)
        self.assertEqual(result["observation_provenance"]["sha256"], digest(raw_before))
        self.assertEqual(path.read_bytes(), raw_before)
        self.assertEqual(result["observation_evidence"], "EXTERNAL OBSERVATION")
        self.assertEqual(result["model_expectation_evidence"], "USER-DECLARED MODEL VALUE")
        self.assertEqual(result["classification"], "SIMULATION / EXPLANATORY")
        self.assertIsNone(result["confidence_score"])
        self.assertFalse(result["calibration_applied"])

    def test_tampered_raw_file_is_rejected(self):
        metadata, path = self.register_fixture()
        path.write_bytes(path.read_bytes().replace(b",8,", b",9,"))
        self.assertNotEqual(digest(path.read_bytes()), metadata["content_sha256"])
        with self.assertRaises(ValueError):
            compare_field(self.request_for(metadata), self.store)

    def test_registered_path_outside_pwn_raw_is_rejected(self):
        metadata, _ = self.register_fixture(local_raw_path="../outside.csv")
        with self.assertRaises(ValueError):
            compare_field(self.request_for(metadata), self.store)

    def test_missing_location_utc_temperature_or_pressure_is_rejected(self):
        for field in ("latitude", "longitude", "timestamp_utc", "temperature_C", "pressure_dbar"):
            with self.subTest(field=field):
                metadata, _ = self.register_fixture({field: ""})
                with self.assertRaises(ValueError):
                    compare_field(self.request_for(metadata), self.store)

    def test_elapsed_only_tank_style_time_is_not_sufficient_for_collocation(self):
        metadata, _ = self.register_fixture({"timestamp_utc": "", "elapsed_ms": 5000})
        with self.assertRaises(ValueError):
            compare_field(self.request_for(metadata), self.store)

    def test_non_utc_or_naive_source_timestamps_are_rejected(self):
        for stamp in ("2026-09-22T15:00:00+03:00", "2026-09-22T12:00:00", "invalid"):
            with self.subTest(stamp=stamp):
                metadata, _ = self.register_fixture({"timestamp_utc": stamp})
                with self.assertRaises(ValueError):
                    compare_field(self.request_for(metadata), self.store)

    def test_non_utc_expected_timestamp_fails_request_validation(self):
        for stamp in ("2026-09-22T12:00:00", "2026-09-22T15:00:00+03:00"):
            with self.subTest(stamp=stamp), self.assertRaises(ValidationError):
                FieldPoint(timestamp_utc=stamp)

    def test_tank_and_simulation_registration_cannot_be_used_as_marine_evidence(self):
        for kind in ("OUR_NEW_MEASUREMENT_TANK", "SIMULATION_EXPLANATORY"):
            with self.subTest(kind=kind):
                metadata, _ = self.register_fixture({"source_kind": kind}, classification=kind)
                with self.assertRaises(ValueError):
                    compare_field(self.request_for(metadata), self.store)

    def test_cable_depth_registration_is_rejected_even_with_external_label(self):
        for method in ("encoder_vertical_tank", "manual_reference", "unavailable"):
            with self.subTest(method=method):
                metadata, _ = self.register_fixture(depth_method=method)
                with self.assertRaises(ValueError):
                    compare_field(self.request_for(metadata), self.store)

    def test_non_ok_selected_sample_is_rejected(self):
        for quality in ("ADC_SATURATED", "MISSING_TEMPERATURE", "OK;SENSOR_NOT_VALIDATED", ""):
            with self.subTest(quality=quality):
                metadata, _ = self.register_fixture({"quality_flag": quality})
                with self.assertRaises(ValueError):
                    compare_field(self.request_for(metadata), self.store)

    def test_unknown_sample_or_dataset_is_rejected(self):
        metadata, _ = self.register_fixture()
        for changes in ({"observed_sample_index": 8}, {"observed_dataset_id": "unknown-fixture"},
                        {"observed_sample_index": None}, {"observed_dataset_id": None}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                compare_field(self.request_for(metadata, **changes), self.store)

    def test_expected_potential_or_conservative_temperature_blocks_residual(self):
        metadata, _ = self.register_fixture()
        for kind in ("potential", "conservative"):
            result = compare_field(self.request_for(metadata, expected=FieldPoint(temperature_kind=kind)), self.store)
            self.assertEqual(result["status"], "not_comparable")
            self.assertIsNone(result["residual_temperature_C"])
            self.assertIsNone(result["after"])

    def test_registered_potential_temperature_cannot_default_to_in_situ(self):
        metadata, _ = self.register_fixture(temperature_kind="potential")
        try:
            result = compare_field(self.request_for(metadata), self.store)
        except ValueError:
            return  # Explicitly rejecting this unsupported source is also valid.
        self.assertEqual(result["status"], "not_comparable")
        self.assertIsNone(result["residual_temperature_C"])

    def test_unknown_registered_temperature_definition_is_rejected(self):
        metadata, _ = self.register_fixture(temperature_kind="unspecified")
        with self.assertRaises(ValueError):
            compare_field(self.request_for(metadata), self.store)

    def test_csv_temperature_definition_cannot_contradict_metadata(self):
        for kind in ("potential", "conservative", "unspecified"):
            with self.subTest(kind=kind):
                metadata, _ = self.register_fixture({"temperature_kind": kind})
                with self.assertRaises(ValueError):
                    compare_field(self.request_for(metadata), self.store)

    def test_model_source_url_requires_http_and_a_host(self):
        metadata, _ = self.register_fixture()
        for url in (None, "", "https://", "file:///unit-fixture.csv", "not-a-url"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                compare_field(self.request_for(metadata, model_source_url=url), self.store)

    def test_coordinate_time_or_depth_mismatch_blocks_real_profile_update(self):
        metadata, _ = self.register_fixture()
        for expected in (FieldPoint(latitude=75), FieldPoint(depth_m=100),
                         FieldPoint(timestamp_utc="2026-09-23T12:00:00Z")):
            result = compare_field(self.request_for(metadata, expected=expected), self.store)
            self.assertFalse(result["collocation"]["passed"])
            self.assertIsNone(result["residual_temperature_C"])
            self.assertIsNone(result["energy_delta_kwh"])

    def test_cold_real_path_does_not_extrapolate_treatment(self):
        metadata, _ = self.register_fixture({"temperature_C": -1})
        result = compare_field(self.request_for(metadata), self.store)
        self.assertEqual(result["residual_temperature_C"], -11)
        self.assertIsNone(result["after"]["treatment"]["specific_energy_kwh_m3"])
        self.assertIsNone(result["energy_delta_kwh"])

    def client(self):
        # Import cannot create the app's normal repository-backed SQLite store.
        with patch("backend.provenance.ProvenanceStore", return_value=self.store):
            module = importlib.import_module("backend.app")
        store_patch = patch.object(module, "store", self.store)
        store_patch.start()
        self.addCleanup(store_patch.stop)
        client = TestClient(module.app)  # No lifespan; no source registration side effects.
        self.addCleanup(client.close)
        return client

    def test_api_returns_external_evidence_and_run_id(self):
        metadata, _ = self.register_fixture()
        response = self.client().post("/api/field-comparison", json=self.request_for(metadata).model_dump(mode="json"))
        self.assertEqual(response.status_code, 200, response.text)
        self.assertTrue(response.json()["run_id"])
        self.assertEqual(response.json()["observation_evidence"], "EXTERNAL OBSERVATION")

    def test_api_returns_422_for_missing_registered_sample(self):
        metadata, _ = self.register_fixture()
        response = self.client().post("/api/field-comparison", json=self.request_for(metadata, observed_sample_index=99).model_dump(mode="json"))
        self.assertEqual(response.status_code, 422)
        self.assertIn("detail", response.json())

    def test_api_returns_422_when_registered_raw_file_is_missing(self):
        metadata, path = self.register_fixture()
        path.unlink()  # Only the TemporaryDirectory fixture is removed.
        response = self.client().post("/api/field-comparison", json=self.request_for(metadata).model_dump(mode="json"))
        self.assertEqual(response.status_code, 422)

    def test_api_rejects_naive_expected_utc(self):
        metadata, _ = self.register_fixture()
        payload = self.request_for(metadata).model_dump(mode="json")
        payload["expected"]["timestamp_utc"] = "2026-09-22T12:00:00"
        self.assertEqual(self.client().post("/api/field-comparison", json=payload).status_code, 422)


if __name__ == "__main__":
    unittest.main()
