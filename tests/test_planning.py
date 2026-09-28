"""Decision regressions on actual provincial baselines and explicit northern scenarios."""
import copy
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient
from pydantic import ValidationError
from backend import planning
from backend.app import app
from backend.planning_contracts import SimulationRequest
from backend.provenance import ProvenanceStore

ROOT = Path(__file__).resolve().parents[1]


class CropPatternEngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contexts = {site: planning.planning_context(site) for site in
                        ("konya", "gap_sanliurfa", "trakya_edirne", "longyearbyen")}

    def request(self, site="konya", illustrative=False):
        key = "illustrative_scenario" if illustrative else "default_scenario"
        return SimulationRequest.model_validate(copy.deepcopy(self.contexts[site][key]))

    def assert_feasible(self, result):
        self.assertEqual(result["status"], "conditional")
        self.assertTrue(result["solver"]["success"])
        self.assertIsNotNone(result["optimized"])
        for constraint in result["constraints"]:
            self.assertGreaterEqual(constraint["slack"], -max(1e-3, abs(constraint["capacity"]) * 2e-7))

    def test_context_baseline_analysis_never_runs_optimizer_or_invents_missing_water(self):
        with patch.object(planning, 'linprog', side_effect=AssertionError('Baseline must not optimize')):
            for site in ('konya', 'trakya_edirne', 'longyearbyen'):
                context=planning.planning_context(site)
                baseline=context['baseline_analysis']
                self.assertNotIn('optimized', baseline)
                self.assertNotIn('solver', baseline)
                self.assertFalse(baseline['provenance']['optimization_performed'])
                totals=baseline['current']['totals']
                self.assertEqual(baseline['provenance']['available_water_classification'], 'USER_SCENARIO')
                if site=='longyearbyen':
                    self.assertEqual(baseline['status'], 'no_current_baseline')
                    self.assertEqual(baseline['current']['crops'], [])
                    self.assertIsNone(totals['water_m3'])
                else:
                    self.assertEqual(baseline['status'], 'baseline_only')
                    self.assertEqual(len(baseline['current']['crops']),len(context['region']['crops']))
                    for crop in baseline['current']['crops']:
                        official=next(c for c in context['region']['crops'] if c['crop_id']==crop['crop_id'])
                        self.assertAlmostEqual(crop['area_ha'],official['area_ha'])
                        self.assertAlmostEqual(crop['production_kg'],official['production_tonnes']*1000,places=3)
                    if site=='trakya_edirne':
                        self.assertIsNone(totals['water_m3'])
                        self.assertIsNone(totals['water_deficit_m3'])
                    else:
                        self.assertGreater(totals['water_m3'],0)
                        self.assertAlmostEqual(totals['available_water_m3'],totals['water_m3'])

    def test_real_konya_and_urfa_patterns_change_under_twenty_percent_water_cut(self):
        for site in ("konya", "gap_sanliurfa"):
            with self.subTest(site=site):
                request = self.request(site)
                initial = planning.simulate(request)
                self.assert_feasible(initial)
                request.water_sources[0].capacity_m3 *= .8
                reduced = planning.simulate(request)
                self.assert_feasible(reduced)
                crops = reduced["optimized"]["crops"]
                self.assertEqual(len(crops), len(request.crops))
                self.assertTrue(any(c["delta_area_ha"] < -1 for c in crops))
                self.assertLess(reduced["optimized"]["totals"]["water_m3"], initial["current"]["totals"]["water_m3"] * .801)
                minima = {c.crop_id: c.min_production_kg for c in request.crops}
                for crop in crops:
                    self.assertGreaterEqual(crop["production_kg"], minima[crop["crop_id"]] * (1 - 1e-7))
                    self.assertGreater(crop["area_ha"], 0)
                    self.assertLess(crop["area_share_pct"], 100)
                water = next(c for c in reduced["constraints"] if c["id"] == "water_freshwater")
                self.assertTrue(water["binding"])
                self.assertEqual(request.min_cultivated_fraction, 0)

    def test_unknown_northern_climate_and_soil_do_not_produce_a_feasible_plan(self):
        request = self.request("longyearbyen")
        self.assertIsNone(request.crops[0].climate_suitable)
        result = planning.simulate(request)
        self.assertFalse(result["solver"]["success"])
        self.assertIsNone(result["optimized"])
        self.assertTrue(any("uygunluğu" in x["reason"] for x in result["excluded_options"]))

    def test_explicit_north_scenario_has_three_crops_and_native_capacity_units(self):
        request = self.request("longyearbyen", illustrative=True)
        result = planning.simulate(request)
        self.assert_feasible(result)
        by_crop = {c["crop_id"]: c for c in result["optimized"]["crops"]}
        self.assertAlmostEqual(by_crop["barley"]["area_ha"], 1, places=5)
        self.assertAlmostEqual(by_crop["potato"]["area_ha"], .5, places=5)
        self.assertAlmostEqual(by_crop["lettuce"]["production_kg"], 1000, places=4)
        totals = result["optimized"]["totals"]
        self.assertAlmostEqual(totals["open_field_area_ha"], 1.5, places=5)
        self.assertAlmostEqual(totals["hydroponics_area_m2"], 1000 / 3, places=5)
        self.assertAlmostEqual(totals["water_m3"], 150 * 10 / .75 + .5 * 250 * 10 / .75 + 1000 * .02, places=4)
        self.assertLessEqual(totals["energy_kwh"], request.energy_budget_kwh)
        for row in result["optimized"]["allocations"]:
            if row["method"] == "hydroponics":
                self.assertIsNone(row["area_ha"])
                self.assertEqual(row["capacity_unit"], "m2")
            else:
                self.assertEqual(row["capacity_unit"], "ha")

    def test_mm_to_m3_per_hectare_includes_irrigation_efficiency(self):
        request = self.request("longyearbyen", illustrative=True)
        result = planning.simulate(request)
        barley = next(c for c in result["crop_water"] if c["crop_id"] == "barley")
        self.assertEqual(barley["source"], "USER_SCENARIO")
        self.assertEqual(barley["net_irrigation_mm"], 150)
        self.assertEqual(barley["gross_water_m3_ha"], 2000)
        self.assertIsNone(barley["etc_mm"])

    def test_etc_responds_to_et0_factor_and_soil_balance_not_fake_supply(self):
        request = self.request()
        initial = planning.simulate(request)
        request.et0_factor = 1.2
        stressed = planning.simulate(request)
        for before, after in zip(initial["crop_water"], stressed["crop_water"]):
            self.assertAlmostEqual(after["etc_mm"], before["etc_mm"] * 1.2, places=7)
            self.assertGreaterEqual(after["net_irrigation_mm"], before["net_irrigation_mm"] - 1e-8)
            self.assertEqual(after["rainfall_mm"], before["rainfall_mm"])
        self.assertEqual(initial["request"]["water_sources"], stressed["request"]["water_sources"])

    def test_rice_total_water_stays_missing_without_explicit_scenario(self):
        request = self.request("trakya_edirne")
        result = planning.simulate(request)
        rice = next(c for c in result["crop_water"] if c["crop_id"] == "rice")
        self.assertEqual(rice["status"], "insufficient_data")
        self.assertIsNone(rice["gross_water_m3_ha"])
        self.assertIsNone(result["current"]["totals"]["water_m3"])
        self.assertEqual(result["status"], "partial_conditional")
        self.assertIsNone(result["optimized"]["totals"]["water_m3"])
        next(c for c in request.crops if c.crop_id == "rice").manual_net_irrigation_mm = 1000
        request.water_sources[0].capacity_m3 = 1e11
        complete = planning.simulate(request)
        self.assert_feasible(complete)
        self.assertEqual(next(c for c in complete["crop_water"] if c["crop_id"] == "rice")["source"], "USER_SCENARIO")

    def test_disabled_crop_does_not_silently_erase_its_production_minimum(self):
        request = self.request()
        request.crops[0].enabled = False
        result = planning.simulate(request)
        self.assertIsNone(result["optimized"])
        minimum = next(c for c in result["constraints"] if c["id"] == "crop_min_output_" + request.crops[0].crop_id)
        self.assertGreater(minimum["capacity"], 0)

    def test_unknown_source_quality_excludes_capacity(self):
        request = self.request("longyearbyen", illustrative=True)
        for source in request.water_sources:
            source.quality_suitable = None
        result = planning.simulate(request)
        self.assertIsNone(result["optimized"])
        self.assertEqual(result["current"]["totals"]["available_water_m3"], 0)
        self.assertTrue(any("kalitesi" in x["reason"] for x in result["excluded_options"]))

    def test_missing_energy_is_not_treated_as_zero_under_energy_budget(self):
        request = self.request("longyearbyen", illustrative=True)
        next(c for c in request.crops if c.crop_id == "lettuce").controlled_energy_kwh_kg = None
        result = planning.simulate(request)
        self.assertIsNone(result["optimized"])
        self.assertTrue(any("enerji katsayısı" in x["reason"] for x in result["excluded_options"] if x["crop_id"] == "lettuce"))

    def test_official_area_and_production_survive_user_pattern_edits(self):
        path = ROOT / "data/agriculture/region_baselines.json"
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        request = self.request()
        initial = planning.simulate(request)
        request.crops[0].current_area_ha *= .5
        request.crops[0].yield_kg_ha *= .8
        changed = planning.simulate(request)
        self.assertEqual(initial["baseline"]["crops"], changed["baseline"]["crops"])
        self.assertNotEqual(initial["current"]["crops"][0]["production_kg"], changed["current"]["crops"][0]["production_kg"])
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), sha)

    def test_impossible_budget_returns_no_fabricated_allocations_or_constraint_usage(self):
        request = self.request()
        request.water_sources[0].capacity_m3 = 1
        result = planning.simulate(request)
        self.assertFalse(result["solver"]["success"])
        self.assertIsNone(result["optimized"])
        self.assertTrue(all(c["used"] is None and c["slack"] is None and c["binding"] is None for c in result["constraints"]))

    def test_duplicate_crops_invalid_share_and_nonfinite_budget_are_rejected(self):
        original = self.contexts["konya"]["default_scenario"]
        for kind in ("duplicate", "share", "nan"):
            payload = copy.deepcopy(original)
            if kind == "duplicate": payload["crops"].append(copy.deepcopy(payload["crops"][0]))
            elif kind == "share": payload["crops"][0].update(min_share=.8, max_share=.2)
            else: payload["water_sources"][0]["capacity_m3"] = float("nan")
            with self.subTest(kind=kind), self.assertRaises(ValidationError):
                SimulationRequest.model_validate(payload)


class PatternFieldApiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store_patch = patch("backend.app.store", ProvenanceStore(Path(self.temp.name) / "runs.sqlite"))
        self.store_patch.start()
        self.addCleanup(self.store_patch.stop)
        self.client = TestClient(app)
        self.client.__enter__()
        self.addCleanup(self.client.__exit__, None, None, None)

    def test_context_and_simulate_use_shared_engine_and_record_reproducible_run(self):
        context = self.client.get("/api/planning-context", params={"region_id": "konya"})
        self.assertEqual(context.status_code, 200)
        payload = context.json()["default_scenario"]
        first = self.client.post("/api/simulate", json=payload)
        again = self.client.post("/api/simulate", json=payload)
        self.assertEqual(first.status_code, 200)
        self.assertEqual(first.json()["model_version"], "0.5.0")
        self.assertEqual(first.json()["run_id"], again.json()["run_id"])
        self.assertEqual(first.json()["solver"]["name"], "SciPy HiGHS")

    def test_matched_field_pair_reruns_same_engine_changing_only_source_temperature(self):
        context = self.client.get("/api/planning-context", params={"region_id": "longyearbyen"}).json()
        with patch("backend.app.simulate", wraps=planning.simulate) as shared:
            response = self.client.post("/api/pattern-field-update", json={"simulation": context["illustrative_scenario"]})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(shared.call_count, 2)
        result = response.json()
        self.assertTrue(result["comparison"]["collocation"]["passed"])
        before, after = result["before"], result["after"]
        self.assertEqual(before["model_version"], after["model_version"])
        b, a = before["request"], after["request"]
        self.assertNotEqual(b.pop("seawater_temperature_c"), a.pop("seawater_temperature_c"))
        self.assertEqual(b, a)
        self.assertEqual(before["provenance"]["code_sha256"], after["provenance"]["code_sha256"])
        self.assertFalse(result["comparison"]["calibration_applied"])

    def test_failed_field_collocation_cannot_create_after_plan(self):
        context = self.client.get("/api/planning-context", params={"region_id": "longyearbyen"}).json()
        response = self.client.post("/api/pattern-field-update", json={"simulation": context["illustrative_scenario"],
                                                                        "observation": {"observed": {"latitude": 20}}})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertFalse(response.json()["comparison"]["collocation"]["passed"])
        self.assertIsNone(response.json()["after"])
        self.assertIsNone(response.json()["changed_pattern"])


if __name__ == "__main__":
    unittest.main()
