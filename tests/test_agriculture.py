"""Integrity checks for the actual provincial crop-pattern evidence package."""
import copy
import hashlib
import json
import math
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class AgricultureEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baselines = json.loads((ROOT / "data/agriculture/region_baselines.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((ROOT / "data/agriculture/crops.json").read_text(encoding="utf-8"))

    def test_five_original_sources_are_hash_pinned_inside_raw_directory(self):
        sources = [s for r in self.baselines["regions"] for s in r["sources"]]
        self.assertEqual(len(sources), 5)
        self.assertEqual(len({s["id"] for s in sources}), 5)
        raw_root = (ROOT / "data/agriculture/raw").resolve()
        for source in sources:
            with self.subTest(source=source["id"]):
                relative = Path(source["local_path"])
                self.assertFalse(relative.is_absolute())
                path = (ROOT / relative).resolve()
                self.assertTrue(path.is_relative_to(raw_root))
                payload = path.read_bytes()
                self.assertEqual(hashlib.sha256(payload).hexdigest(), source["sha256"])
                self.assertIn(source["sha256"], path.name)
                self.assertTrue(payload.startswith(b"%PDF") if path.suffix == ".pdf" else payload.startswith(b"PK"))
                for key in ("url", "title", "year", "data_year", "page", "access_date"):
                    self.assertTrue(source[key], key)

    def test_province_year_and_selected_scope_do_not_become_basin_statistics(self):
        expected = {"konya": ("Konya", 2024), "seyhan_adana": ("Adana", 2024),
                    "gediz_manisa": ("Manisa", 2024), "gap_sanliurfa": ("Şanlıurfa", 2024),
                    "trakya_edirne": ("Edirne", 2024)}
        regions = self.baselines["regions"]
        self.assertEqual(len(regions), len(expected))
        self.assertEqual({r["region_id"] for r in regions}, set(expected))
        self.assertEqual(sum(len(r["crops"]) for r in regions), 21)
        for region in regions:
            self.assertEqual((region["geography_name"], region["year"]), expected[region["region_id"]])
            self.assertEqual(region["geography_level"], "province")
            self.assertEqual(region["area_scope"], "selected_crops_only")
            self.assertEqual(region["classification"], "OFFICIAL_STATISTICS")
            self.assertTrue(region["limitations"])
            self.assertTrue(all(s["data_year"] == region["year"] for s in region["sources"]))

    def test_21_records_keep_source_units_and_derived_yield_identity(self):
        for region in self.baselines["regions"]:
            sources = {s["id"] for s in region["sources"]}
            self.assertEqual(len({c["crop_id"] for c in region["crops"]}), len(region["crops"]))
            self.assertAlmostEqual(sum(c["area_ha"] for c in region["crops"]), region["selected_crop_area_ha"])
            for crop in region["crops"]:
                with self.subTest(region=region["region_id"], crop=crop["crop_id"]):
                    self.assertIn(crop["source_id"], sources)
                    for key in ("area_ha", "production_tonnes", "yield_kg_ha", "original_area_value"):
                        value = crop[key]
                        self.assertIsInstance(value, (int, float))
                        self.assertNotIsInstance(value, bool)
                        self.assertTrue(math.isfinite(value) and value > 0)
                    self.assertIn(crop["original_area_unit"], ("da", "ha"))
                    scale = 0.1 if crop["original_area_unit"] == "da" else 1
                    self.assertAlmostEqual(crop["original_area_value"] * scale, crop["area_ha"])
                    self.assertEqual(crop["original_production_unit"], "tonnes")
                    self.assertEqual(crop["yield_classification"], "DERIVED_FROM_OFFICIAL_STATISTICS")
                    self.assertTrue(math.isclose(crop["area_ha"] * crop["yield_kg_ha"] / 1000,
                                                 crop["production_tonnes"], rel_tol=1e-12))

    def test_every_baseline_crop_resolves_to_source_backed_knowledge(self):
        crops = self.catalog["crops"]
        ids = {c["crop_id"] for c in crops}
        self.assertEqual(len(ids), len(crops))
        for region in self.baselines["regions"]:
            self.assertTrue({c["crop_id"] for c in region["crops"]}.issubset(ids))
        for crop in crops:
            self.assertTrue(crop["sources"])
            self.assertTrue(crop["kc"]["source_url"])
            self.assertFalse(crop["growing_period"]["locally_validated"])
            self.assertEqual(sum(crop["growing_period"]["stage_days"]), crop["growing_period"]["total_days"])

    def test_unresolved_crop_parameters_remain_missing_not_zero_or_universal(self):
        # This release has no sourced universal GDD, salinity or local harvest threshold.
        # New evidence must deliberately update this boundary, not silently fill defaults.
        for crop in self.catalog["crops"]:
            self.assertIsNone(crop["harvest_window"])
            self.assertIsNone(crop["salinity_sensitivity"])
            for key in ("gdd_base_c", "gdd_requirement", "temperature_limits", "frost_sensitivity"):
                self.assertIsNone(crop["climate"][key], (crop["crop_id"], key))
            if crop["crop_id"] != "lettuce":
                self.assertEqual(crop["yield_basis"], [], "Provincial yield must not become a universal crop parameter")

    def test_runtime_rejects_outside_source_path_and_changed_hash(self):
        from backend import planning

        for violation in ("outside_path", "changed_hash"):
            forged = copy.deepcopy(self.baselines)
            source = forged["regions"][0]["sources"][0]
            if violation == "outside_path":
                source["local_path"] = "../not-an-agriculture-source.pdf"
            else:
                source["sha256"] = "0" * 64
            with self.subTest(violation=violation), patch.object(planning, "read_agriculture", return_value=forged):
                with self.assertRaises(ValueError):
                    planning.baseline_region("konya")


if __name__ == "__main__":
    unittest.main()
