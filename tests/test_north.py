"""North ingestion checks: synthetic unit fixtures, never field observations."""
import copy
import json
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from scripts.ingest_north import aggregate, digest, immutable, metrics, validate, VARIABLES


def synthetic_year(year=2001):
    start, end = date(year, 1, 1), date(year, 12, 31)
    count = (end - start).days + 1
    return {"utc_offset_seconds": 0, "daily_units": dict(VARIABLES), "daily": {
        "time": [(start + timedelta(days=i)).isoformat() for i in range(count)],
        "temperature_2m_min": [0.0] * count,
        "temperature_2m_max": [10.0] * count,
        "precipitation_sum": [1.0] * count}}


class NorthDataTests(unittest.TestCase):
    def test_leap_year_and_strict_frost_threshold(self):
        p = synthetic_year(2000)
        self.assertEqual(validate(p, "2000-01-01", "2000-12-31"), 366)
        result = metrics(p, "baseline")[0]
        self.assertTrue(result["complete"])
        self.assertEqual(result["gdd5_degree_days"], 0)
        self.assertEqual(result["frost_free_run_days"], 0)
        self.assertEqual(result["precipitation_mm"], 366)

    def test_known_gdd_and_frost_runs(self):
        p = synthetic_year()
        p["daily"]["temperature_2m_min"][10:13] = [2, 2, 2]
        p["daily"]["temperature_2m_min"][20:22] = [4, 4]
        result = metrics(p, "baseline")[0]
        self.assertEqual(result["gdd5_degree_days"], 7)
        self.assertEqual(result["frost_free_run_days"], 3)

    def test_missing_values_are_not_zero_filled_or_partial_year_averaged(self):
        p = synthetic_year()
        p["daily"]["temperature_2m_min"][0] = None
        validate(p, "2001-01-01", "2001-12-31")
        rows = metrics(p, "future")
        self.assertFalse(rows[0]["complete"])
        self.assertIsNone(rows[0]["gdd5_degree_days"])
        result = aggregate(rows, "2001-01-01", "2001-12-31")
        self.assertEqual(result["complete_years"], 0)
        self.assertIsNone(result["mean_annual_precipitation_mm"])

    def test_inverted_temperatures_are_rejected_without_silent_swap(self):
        p = synthetic_year()
        p["daily"]["temperature_2m_min"][0] = 11
        with self.assertRaises(ValueError):
            validate(p, "2001-01-01", "2001-12-31")
        self.assertEqual(p["daily"]["temperature_2m_min"][0], 11)

    def test_bad_units_dates_and_numbers_rejected(self):
        bad = []
        p = synthetic_year(); p["daily_units"]["precipitation_sum"] = "inch"; bad.append(p)
        p = synthetic_year(); p["daily"]["time"][1] = p["daily"]["time"][0]; bad.append(p)
        for value in (-1, float("nan"), float("inf"), True):
            p = synthetic_year(); p["daily"]["precipitation_sum"][0] = value; bad.append(p)
        for p in bad:
            with self.subTest(payload=p["daily"]["precipitation_sum"][0]), self.assertRaises(ValueError):
                validate(p, "2001-01-01", "2001-12-31")

    def test_raw_snapshot_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "raw.json"
            immutable(path, b"original")
            immutable(path, b"original")
            with self.assertRaises(ValueError):
                immutable(path, b"changed")
            self.assertEqual(path.read_bytes(), b"original")

    def test_committed_summary_is_traceable_complete_single_model_projection(self):
        root = Path(__file__).resolve().parents[1]
        summary = json.loads((root / "data/north/summary.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["status"], "ready")
        self.assertEqual(summary["source_kind"], "EXTERNAL_CLIMATE_MODEL")
        self.assertIsNone(summary["ssp"])
        self.assertFalse(summary["marine_observations_available"])
        self.assertEqual(summary["future"]["period"], "2030–2049")
        self.assertEqual(summary["requested_future_period"], "2031–2050")
        for period, metadata in zip(("baseline", "future"), summary["provenance"]):
            raw = (root / metadata["raw_path"]).read_bytes()
            self.assertEqual(digest(raw), metadata["sha256"])
            payload = json.loads(raw)
            self.assertEqual(validate(payload, *metadata["period"]), 7305)
            self.assertEqual(metadata["model"], summary["model"])
            self.assertTrue(metadata["disable_bias_correction"])
            self.assertEqual(aggregate(metrics(payload, period), *metadata["period"]), summary[period])


if __name__ == "__main__":
    unittest.main()
