"""Independent numerical fixtures for the pure explanation layer, not new climate data."""
from copy import deepcopy
import json

import pytest

from backend.north_decision_story import summarize_decision


@pytest.fixture
def result():
    return {
        "request": {"area_m2": 100., "storage_m3_per_m2": .1, "heat_cop": 2., "energy_limit_kwh": None},
        "basis": {"storage_m3": 10.},
        "climate": {"period": [2041, 2060]},
        "plan": {"status": "conditional", "totals": {"water_m3": 30., "stored_water_m3": 20.,
            "desalinated_m3": 10., "freshwater_m3": 0., "heat_kwh_th": 200., "electricity_kwh": 80.,
            "equivalent_electricity_kwh": 180., "treatment_electricity_kwh": 10., "treatment_heat_kwh_th": 0.},
            "allocations": [{"crop_id": "lettuce", "name": "Marul", "method": "greenhouse", "season": "summer", "area_m2": 40., "production_kg": 50.},
                            {"crop_id": "lettuce", "name": "Marul", "method": "hydroponics", "season": "annual", "area_m2": 20., "production_kg": 80.},
                            {"crop_id": "radish", "name": "Turp", "method": "hydroponics", "season": "annual", "area_m2": 40., "production_kg": 100.}],
            "monthly": [{"month": 1, "demand_m3": 10., "desalinated_m3": 8., "freshwater_m3": 0., "storage_end_m3": 1.},
                        {"month": 7, "demand_m3": 20., "desalinated_m3": 2., "freshwater_m3": 0., "storage_end_m3": 4.}]},
        "daily_reliability": [
            {"model": "A", "topup_m3_per_year": {"min": 4., "mean": 8., "max": 12.}, "maximum_daily_topup_m3": .5,
             "days_with_topup": 300, "worst_topup_year": 2044, "modeled_peak_storage_m3": 7.,
             "monthly": [{"month": 1, "demand_m3": 10., "deficit_m3": 3.}, {"month": 7, "demand_m3": 20., "deficit_m3": 5.}]},
            {"model": "B", "topup_m3_per_year": {"min": 6., "mean": 10., "max": 15.}, "maximum_daily_topup_m3": .7,
             "days_with_topup": 500, "worst_topup_year": 2050, "modeled_peak_storage_m3": 8.,
             "monthly": [{"month": 1, "demand_m3": 10., "deficit_m3": 2.}, {"month": 7, "demand_m3": 20., "deficit_m3": 8.}]},
            {"model": "C", "topup_m3_per_year": {"min": 5., "mean": 9., "max": 13.}, "maximum_daily_topup_m3": .6,
             "days_with_topup": 400, "worst_topup_year": 2049, "modeled_peak_storage_m3": 6.,
             "monthly": [{"month": 1, "demand_m3": 10., "deficit_m3": 4.}, {"month": 7, "demand_m3": 20., "deficit_m3": 5.}]}],
        "sensitivity": [{"id": "yield", "name": "Aktarılan verim", "status": "SENSITIVE", "area_reallocated_m2": 0., "production_change_pct": 18., "energy_change_pct": 0., "effect": "Hasat %18 değişti; alan aynı kaldı."},
                        {"id": "ground", "name": "Parsel zemini", "status": "UNRESOLVED", "tase_measurable": False}],
        "range_infeasible_cases": 1,
        "provenance": {"sensitivity_threshold": "Explicit reporting convention, not significance."}}


def test_month_is_max_model_volume_not_ensemble_plan_or_ratio_only(result):
    result["daily_reliability"][0]["monthly"][0] = {"month": 1, "demand_m3": 2., "deficit_m3": 2.}
    month = summarize_decision(result)["water_security"]["critical_month"]
    assert (month["month"], month["model"], month["backup_m3"]) == (7, "B", 8.)
    assert month["backup_share_pct"] == 40.
    assert month["basis"] == "MAX_MODEL_CLIMATOLOGICAL_MONTH_FROM_DAILY_REPLAY"
    assert month["is_single_worst_year_month"] is False


def test_month_fallback_does_not_claim_daily_or_model_scope(result):
    del result["daily_reliability"][1]["monthly"]
    month = summarize_decision(result)["water_security"]["critical_month"]
    assert month["month"] == 1 and month["backup_m3"] == 8.
    assert month["model"] is None
    assert month["basis"] == "MONTHLY_MEAN_PLAN_FALLBACK"


def test_tank_size_peak_occupation_and_minimum_are_separate(result):
    storage = summarize_decision(result)["water_security"]["storage"]
    assert storage["configured_m3"] == 10.
    assert storage["modeled_peak_occupied_m3"] == 8.
    assert storage["minimum_required_m3"] is None
    assert storage["capacity_optimized"] is False
    assert storage["basis"] == "MAX_DAILY_OCCUPIED_STORAGE_ACROSS_MODELS"
    for row in result["daily_reliability"]:
        del row["modeled_peak_storage_m3"]
    old = summarize_decision(result)["water_security"]["storage"]
    assert old["modeled_peak_occupied_m3"] == 4.
    assert old["basis"] == "MONTH_END_OCCUPIED_STORAGE_IN_MEAN_PLAN"


def test_annual_backup_envelope_retains_model_year_and_daily_peak(result):
    water = summarize_decision(result)["water_security"]
    assert water["backup"]["annual_m3"] == {"min": 4., "mean": 9., "max": 15.}
    assert water["backup"]["maximum_daily_m3"] == .7
    assert water["backup"]["worst_model"] == "B"
    assert water["backup"]["worst_year"] == 2050
    dry = water["dry_year_sensitivity"]
    assert dry["increase_m3"] == 6.
    assert dry["increase_pct"] == pytest.approx(100*6/9)
    assert dry["annual_mean_backup_m3"] == 9.  # Not the LP's 10 m³ allocation.
    assert dry["display_threshold_pct"] == 5.
    assert dry["is_sensitive"] is True and dry["probability_claimed"] is False


def test_exact_five_percent_is_a_declared_display_boundary(result):
    for row in result["daily_reliability"]:
        row["topup_m3_per_year"] = {"min": 95., "mean": 100., "max": 105.}
    assert summarize_decision(result)["water_security"]["dry_year_sensitivity"]["is_sensitive"] is False
    result["daily_reliability"][1]["topup_m3_per_year"]["max"] = 105.1
    assert summarize_decision(result)["water_security"]["dry_year_sensitivity"]["is_sensitive"] is True


def test_first_year_maximum_is_not_attributed_to_drought_alone(result):
    assert summarize_decision(result)["water_security"]["dry_year_sensitivity"]["initial_condition_warning"] is None
    result["daily_reliability"][1]["worst_topup_year"] = 2041
    story = summarize_decision(result)
    dry = story["water_security"]["dry_year_sensitivity"]
    assert dry["worst_year_is_first_modeled_year"] is True
    assert dry["initial_condition_warning"] == "İlk model yılında boş depo başlangıcı etkisi bulunuyor; bu bir kurak yıl kanıtı değildir."
    action = next(a for a in story["actions"] if a["id"] == "dry_year")
    assert "kurak yıl kanıtı değildir" in action["text"]
    assert "İlk üretim yılı" in action["title"]
    assert "%" not in action["text"]  # Large relative rise stays in the numeric detail.
    assert dry["worst_model_year_backup_m3"] == 15.  # Keep the actual startup requirement.


def test_visible_source_shares_close_without_inventing_freshwater(result):
    water = summarize_decision(result)["water_security"]
    assert [r["share_pct"] for r in water["sources"]] == [66.67, 33.33, 0.]
    assert sum(r["share_pct"] for r in water["sources"]) == 100.
    assert water["source_balance_status"] == "CLOSED"
    assert water["source_balance_residual_m3"] == 0.
    result["plan"]["totals"].update(water_m3=3., stored_water_m3=1., desalinated_m3=1., freshwater_m3=1.)
    shares = summarize_decision(result)["water_security"]["sources"]
    assert [r["share_pct"] for r in shares] == [33.34, 33.33, 33.33]


def test_nonclosing_source_balance_is_not_presented_as_ready_allocation(result):
    result["plan"]["totals"]["water_m3"] = 35.
    story = summarize_decision(result)
    assert story["water_security"]["source_balance_status"] == "INCONSISTENT"
    action = next(a for a in story["actions"] if a["id"] == "water_sources")
    assert action["tone"] == "danger"
    assert "doğrulamadan" in action["title"]


def test_missing_diagnostics_remain_unknown_and_json_finite():
    story = summarize_decision({"plan": {"status": "infeasible", "allocations": []}})
    assert story["water_security"]["annual_demand_m3"] is None
    assert story["water_security"]["source_balance_status"] == "NOT_COMPUTED"
    assert story["water_security"]["critical_month"] is None
    assert story["water_security"]["backup"]["annual_m3"] is None
    assert story["water_security"]["storage"]["configured_m3"] is None
    assert story["water_security"]["dry_year_sensitivity"]["is_sensitive"] is None
    assert story["risk"]["sensitivity_computed"] is False
    assert story["risk"]["tested_breakpoints"] == []
    assert story["actions"][0]["tone"] == "danger"
    json.dumps(story, allow_nan=False)


def test_zero_water_produces_no_percentage_or_fake_critical_month(result):
    result["plan"]["totals"].update(water_m3=0., stored_water_m3=0., desalinated_m3=0., freshwater_m3=0.)
    for row in result["daily_reliability"]:
        row["topup_m3_per_year"] = dict.fromkeys(("min", "mean", "max"), 0.)
        for month in row["monthly"]:
            month["deficit_m3"] = 0.
    water = summarize_decision(result)["water_security"]
    assert all(row["share_pct"] == 0 for row in water["sources"])
    assert water["critical_month"] is None
    assert water["dry_year_sensitivity"]["increase_pct"] is None
    assert water["dry_year_sensitivity"]["is_sensitive"] is False


def test_actions_use_actual_mixed_methods_and_deduplicate_crop(result):
    story = summarize_decision(result)
    crops = {c["crop_id"]: c for c in story["production"]["crops"]}
    assert crops["lettuce"]["area_m2"] == 60.
    assert crops["lettuce"]["production_kg"] == 130.
    assert set(crops["lettuce"]["methods"]) == {"greenhouse", "hydroponics"}
    assert {m["id"]: m["area_m2"] for m in story["production"]["methods"]} == {"greenhouse": 40., "hydroponics": 60.}
    assert "açık tarla" not in story["actions"][0]["text"]
    metrics = next(a for a in story["actions"] if a["id"] == "infrastructure")["metrics"]
    assert metrics["heat_kwh_th"] == 200.
    assert metrics["electricity_kwh"] == 80.
    assert metrics["equivalent_electricity_kwh"] == 180.
    assert metrics["configured_storage_m3"] == 10.
    assert metrics["configured_energy_limit_kwh"] is None


def test_yield_sensitivity_with_stable_allocation_still_has_action(result):
    story = summarize_decision(result)
    risk = next(a for a in story["actions"] if a["id"] == "sensitivity")
    assert risk["metrics"]["production_change_pct"] == 18.
    assert risk["metrics"]["area_reallocated_m2"] == 0.
    assert story["risk"]["infeasible_test_cases"] == 1
    assert story["risk"]["tested_breakpoints"] == []
    assert story["risk"]["breakpoint_analysis_performed"] is False


def test_summary_neither_mutates_input_nor_returns_mutable_aliases(result):
    before = deepcopy(result)
    story = summarize_decision(result)
    assert result == before
    story["risk"]["sensitive_inputs"][0]["name"] = "changed"
    story["production"]["crops"][0]["methods"].append("fake")
    assert result == before
    json.dumps(story, allow_nan=False)


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -3., True])
def test_invalid_scientific_quantities_are_rejected(result, bad):
    result["plan"]["totals"]["water_m3"] = bad
    with pytest.raises(ValueError):
        summarize_decision(result)
