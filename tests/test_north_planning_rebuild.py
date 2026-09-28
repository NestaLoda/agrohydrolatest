"""Decision integration checks with explicit fixtures and the actual NASA package.

`pytest ... -k 'not real'` runs the compact synthetic integration while the real
acquisition is in progress. The real tests assert a ready verified package; they
never download or replace missing production climate with fixture weather.
"""
from copy import deepcopy
import json
from math import pi

import numpy as np
import pandas as pd
import pytest

from backend import north_planning as planning
from backend.north_climate import CLIMATE_DIR, get_climate_context
from backend.north_contracts import NorthRequest
from backend.north_field import rerun_source


CROP_IDS = {"lettuce", "arugula", "radish", "kohlrabi", "swiss_chard", "basil"}


def assert_water_conservation(result):
    plan = result["plan"]
    totals = plan["totals"]
    assert totals["water_m3"] == pytest.approx(
        totals["stored_water_m3"] + totals["desalinated_m3"] + totals["freshwater_m3"], abs=1e-5)
    previous = 0.
    for row in plan["monthly"]:
        assert row["demand_m3"] == pytest.approx(
            row["stored_water_used_m3"] + row["desalinated_m3"] + row["freshwater_m3"], abs=1e-5)
        assert previous + row["capture_m3"] == pytest.approx(
            row["stored_water_used_m3"] + row["spill_m3"] + row["storage_end_m3"], abs=1e-5)
        assert row["storage_end_m3"] <= result["basis"]["storage_m3"] + 1e-5
        previous = row["storage_end_m3"]


@pytest.fixture(scope="class")
def compact_planner(tmp_path_factory):
    """Real crop/resource/LP pipeline, synthetic daily weather, isolated cache."""
    mp = pytest.MonkeyPatch()
    root = tmp_path_factory.mktemp("north-plan-synthetic")
    dates = pd.date_range("2001-01-01", "2001-12-31")
    frames = {}
    def frame(site, horizon, scenario, model, target_year=None):
        key = (horizon, model)
        if key not in frames:
            offset = {"historical": -8., "near": -5., "mid": -2., "late": 2.}[horizon]
            offset += list(planning.MODELS).index(model)-1
            seasonal = np.sin(2*pi*(np.arange(len(dates))-90)/365)
            centre = offset+10*seasonal
            frames[key] = pd.DataFrame({"date": dates, "model": model, "tmin_c": centre-2,
                                       "tmax_c": centre+2, "precipitation_mm": np.full(len(dates), 1.),
                                       "shortwave_mj_m2": np.maximum(0., 5.+8*seasonal)})
        return frames[key].copy()
    def context(site, horizon, scenario, target_year=None):
        values = [frame(site, horizon, scenario, m) for m in planning.MODELS]
        gdd0 = np.mean([np.maximum(0, (v.tmin_c+v.tmax_c)/2).sum() for v in values])
        gdd5 = np.mean([np.maximum(0, (v.tmin_c+v.tmax_c)/2-5).sum() for v in values])
        return {"site_id": site, "horizon_id": horizon, "scenario_id": scenario,
                "models": [{"model": m} for m in planning.MODELS],
                "manifest_sha256": "SYNTHETIC_TEST_WEATHER_NOT_NASA", "period": [2001, 2001],
                "ensemble": {"gdd0_degree_days": {"mean": gdd0},
                             "gdd5_degree_days": {"mean": gdd5},
                             "frost_free_run_days": {"mean": 100}}}
    planning._coefficient_package.cache_clear(); planning._inflows.cache_clear()
    mp.setattr(planning, "ROOT", root)
    mp.setattr(planning, "get_climate_context", context)
    mp.setattr(planning, "load_climate_frame", frame)
    mp.setattr(planning, "_hashes", lambda: {"crops": "real-catalog-synthetic-weather-test"})
    cache = {}
    def run(*, with_sensitivity=False, **params):
        request = NorthRequest(**params)
        key = (request.model_dump_json(), with_sensitivity)
        if key not in cache:
            cache[key] = planning.plan_north(request, with_sensitivity=with_sensitivity)
        return deepcopy(cache[key])
    yield run
    planning._coefficient_package.cache_clear(); planning._inflows.cache_clear()
    mp.undo()


class TestCompactIntegration:
    def test_six_crops_are_calculated_from_candidates_not_demand_inputs(self, compact_planner):
        result = compact_planner()
        assert result["plan"]["status"] == "conditional"
        assert set(result["plan"]["crop_outputs_kg"]) == CROP_IDS
        assert all(value > 0 for value in result["plan"]["crop_outputs_kg"].values())
        assert result["plan"]["totals"]["area_m2"] == pytest.approx(100, abs=1e-3)
        assert not any(a["method"] == "open_field" for a in result["plan"]["allocations"])
        assert result["basis"]["local_farm_capacity_claimed"] is False
        assert_water_conservation(result)

    def test_normalized_area_scaling_does_not_change_crop_shares_or_double_count_years(self, compact_planner):
        one = compact_planner(area_m2=100)
        two = compact_planner(area_m2=200)
        for crop, mass in one["plan"]["crop_outputs_kg"].items():
            assert two["plan"]["crop_outputs_kg"][crop] == pytest.approx(2*mass, rel=2e-5)
        for key in ("area_m2", "water_m3", "heat_kwh_th", "equivalent_electricity_kwh"):
            assert two["plan"]["totals"][key] == pytest.approx(2*one["plan"]["totals"][key], rel=2e-5)
        assert two["basis"]["roof_area_m2"] == 2*one["basis"]["roof_area_m2"]
        assert two["basis"]["storage_m3"] == 2*one["basis"]["storage_m3"]
        assert_water_conservation(two)

    def test_no_water_sources_cannot_create_water_or_output(self, compact_planner):
        result = compact_planner(roof_ratio=0, freshwater_m3=0, desalination=False)
        assert result["plan"]["status"] == "infeasible"
        assert result["plan"]["allocations"] == []
        assert not result["plan"].get("totals")

    def test_energy_limit_is_a_hard_constraint_and_does_not_invent_capacity(self, compact_planner):
        base = compact_planner()
        ceiling = base["plan"]["totals"]["equivalent_electricity_kwh"]*.5
        limited = compact_planner(energy_limit_kwh=ceiling)
        assert limited["plan"]["totals"]["equivalent_electricity_kwh"] <= ceiling+1e-3
        constraint=next(c for c in limited["plan"]["resource_constraints"] if c["name"]=="Enerji sınırı")
        assert constraint["slack"] == pytest.approx(ceiling-limited["plan"]["totals"]["equivalent_electricity_kwh"],abs=1e-3)
        assert limited["plan"]["totals"]["production_kg"] <= base["plan"]["totals"]["production_kg"]+1e-3
        assert limited["plan"]["totals"]["production_kg"] >= limited["plan"]["objective_policy"]["balanced_mass_floor_kg"]-1e-3

    def test_horizon_weather_changes_resource_inputs_without_forcing_crop_change(self, compact_planner):
        cold = compact_planner(horizon_id="historical")
        warm = compact_planner(horizon_id="late")
        assert cold["climate"]["horizon_id"] != warm["climate"]["horizon_id"]
        cold_options = {o["id"]: o for o in cold["engine_inputs"]["options"]}
        warm_options = {o["id"]: o for o in warm["engine_inputs"]["options"]}
        assert cold_options.keys() == warm_options.keys()
        assert any(cold_options[k]["heat_kwh_th_m2"] != warm_options[k]["heat_kwh_th_m2"] for k in cold_options)
        assert all(cold_options[k]["yield_kg_m2"] == warm_options[k]["yield_kg_m2"] for k in cold_options)
        assert cold["plan"]["totals"]["equivalent_electricity_kwh"] != warm["plan"]["totals"]["equivalent_electricity_kwh"]

    def test_source_only_rerun_preserves_climate_crop_and_water_coefficients(self, compact_planner):
        before = compact_planner()
        original = deepcopy(before)
        after = rerun_source(before, 8., 25., before["request"]["recovery"])
        assert before == original
        allowed = {"ro_kwh_m3", "ro_heat_kwh_th_m3", "desalination"}
        for key in before["engine_inputs"]:
            if key not in allowed:
                assert after["engine_inputs"][key] == before["engine_inputs"][key]
        assert after["plan"]["solver"]["version"] == before["plan"]["solver"]["version"]

    def test_engineering_ranges_average_all_models_not_first_model(self, compact_planner):
        result = compact_planner()
        for o in result["engine_inputs"]["options"]:
            for key in ("heat_kwh_th_m2", "electricity_kwh_m2"):
                assert o["resource_configurations"][key][1] == pytest.approx(o[key])
                assert o["resource_ranges"][key]["low"] <= o[key] <= o["resource_ranges"][key]["high"]
            assert sum(o["water_monthly_m3_m2"]) == pytest.approx(
                o["resource_ranges"]["fresh_makeup_m3_m2"]["central"])
            for month, amount in enumerate(o["water_monthly_m3_m2"], 1):
                if month not in o["active_months"]:
                    assert amount == 0

    def test_sensitivity_names_field_scope_and_keeps_infeasible_cases_out_of_numeric_ranges(self, compact_planner):
        result = compact_planner(with_sensitivity=True)
        sensitivity = {row["id"]: row for row in result["sensitivity"]}
        assert sensitivity["temperature"]["tase_measurable"] is True
        assert sensitivity["salinity"]["tase_measurable"] is True
        assert sensitivity["climate"]["tase_measurable"] is False
        assert sensitivity["yield"]["status"] == "SENSITIVE"
        assert sensitivity["yield"]["production_change_pct"] > 5
        assert sensitivity["freshwater"]["tase_measurable"] is False
        assert sensitivity["ground"]["tase_measurable"] is False
        assert result["range_infeasible_cases"] >= 0
        assert "significance" in result["provenance"]["sensitivity_threshold"]
        for band in result["ranges"].values():
            assert 0 < band["min"] <= band["max"]


@pytest.fixture(scope="class")
def real_planner():
    path = CLIMATE_DIR/"manifest.json"
    assert path.exists(), "Real NASA acquisition not complete; run -k 'not real' only while downloading"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    assert manifest["status"] == "ready"
    assert manifest["raw_file_count"] == 1680
    cache = {}
    def run(**params):
        request = NorthRequest(**params)
        key = request.model_dump_json()
        if key not in cache:
            cache[key] = planning.plan_north(request, with_sensitivity=False)
        return deepcopy(cache[key])
    return run


class TestRealNASAIntegration:
    def test_real_nasa_plan_has_twenty_year_three_model_provenance_and_six_outputs(self, real_planner):
        result = real_planner()
        assert result["climate"]["period"] == [2041, 2060]
        assert result["climate"]["years"] == 20
        assert len(result["climate"]["models"]) == 3
        assert result["provenance"]["climate_manifest_sha256"] == result["climate"]["manifest_sha256"]
        assert set(result["plan"]["crop_outputs_kg"]) == CROP_IDS
        assert all(v > 0 for v in result["plan"]["crop_outputs_kg"].values())
        assert_water_conservation(result)

    def test_real_nasa_area_normalization_scales_each_crop_and_resources(self, real_planner):
        one = real_planner(area_m2=100)
        two = real_planner(area_m2=200)
        for crop, kg in one["plan"]["crop_outputs_kg"].items():
            assert two["plan"]["crop_outputs_kg"][crop] == pytest.approx(kg*2, rel=2e-5)
        for key in ("water_m3", "equivalent_electricity_kwh", "heat_kwh_th"):
            assert two["plan"]["totals"][key] == pytest.approx(one["plan"]["totals"][key]*2, rel=2e-5)

    def test_real_horizon_changes_weather_and_resource_coefficients_not_a_label_only(self, real_planner):
        middle = real_planner()
        late = real_planner(horizon_id="late", scenario_id="ssp585")
        assert late["climate"]["period"] == [2081, 2100]
        assert middle["climate"]["ensemble"]["mean_temperature_c"]["mean"] != late["climate"]["ensemble"]["mean_temperature_c"]["mean"]
        mo = {o["id"]: o for o in middle["engine_inputs"]["options"]}
        lo = {o["id"]: o for o in late["engine_inputs"]["options"]}
        assert any(abs(mo[key]["heat_kwh_th_m2"]-lo[key]["heat_kwh_th_m2"]) > .1 for key in mo)
        assert middle["plan"]["totals"]["equivalent_electricity_kwh"] != late["plan"]["totals"]["equivalent_electricity_kwh"]
        assert_water_conservation(late)

    def test_real_no_authorized_water_sources_has_no_fake_positive_plan(self, real_planner):
        result = real_planner(roof_ratio=0, freshwater_m3=0, desalination=False)
        assert result["plan"]["status"] == "infeasible"
        assert result["plan"]["allocations"] == []
        assert not result["plan"].get("totals")

    def test_real_source_rerun_changes_only_allowed_coefficients(self, real_planner):
        before = real_planner()
        after = rerun_source(before, 8., 25., before["request"]["recovery"])
        for key in before["engine_inputs"]:
            if key not in {"ro_kwh_m3", "ro_heat_kwh_th_m3", "desalination"}:
                assert before["engine_inputs"][key] == after["engine_inputs"][key]
        assert before["plan"]["solver"]["version"] == after["plan"]["solver"]["version"]
