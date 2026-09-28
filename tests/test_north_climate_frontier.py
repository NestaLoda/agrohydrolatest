"""Climate emergence remains separate from site/resource permission.

Daily examples below are explicit synthetic test inputs, not new crop evidence.
The final tests exercise the repository's verified NASA trajectories.
"""
from copy import deepcopy
from datetime import date, timedelta

import pytest

from backend.north_candidates import evaluate_candidates
from backend.north_climate import get_climate_context, load_climate_frame


def daily(year, temperature, model=None):
    day = date(year, 1, 1)
    rows = []
    while day.year == year:
        row = {"date": day.isoformat(), "tmin_c": temperature, "tmax_c": temperature}
        if model is not None:
            row["model"] = model
        rows.append(row)
        day += timedelta(days=1)
    return rows


def frontier(result, crop_id):
    return next(row for row in result["climate_frontier"]["crops"] if row["crop_id"] == crop_id)


def test_unknown_threshold_never_becomes_suitable_from_hot_climate_or_long_reference_calendar():
    result = evaluate_candidates({"daily": daily(2023, 15)})
    wheat = frontier(result, "wheat")
    assert wheat["status"] == "unknown"
    assert wheat["tests"] == []
    assert wheat["climate_suitable"] is None
    assert wheat["model_years_passing"] is None
    assert frontier(result, "barley")["status"] == "potential"
    assert frontier(result, "potato")["status"] == "potential"
    assert result["climate_frontier"]["counts"]["candidate"] == 0


def test_summary_cannot_invent_daily_temperature_window_or_yearly_pass_count():
    result = evaluate_candidates({"summary": {"gdd0": 1800, "frost_free_days": 150}})
    barley = frontier(result, "barley")
    assert barley["status"] == "potential"
    assert barley["model_years_passing"] is None
    potato = frontier(result, "potato")
    assert potato["status"] == "unknown"
    assert potato["tests"][0]["status"] == "unknown"


def test_window_rule_uses_source_minimum_cycle_and_source_temperature_envelope():
    potato = frontier(evaluate_candidates({"daily": daily(2023, 7)}), "potato")
    window = potato["tests"][0]
    assert window["minimum_window_days"] == 90
    assert window["temperature_envelope_c"] == [7, 30]
    assert window["annual"][0]["matching_windows"] == 365 - 90 + 1
    assert window["annual"][0]["warmest_window_mean_c"] == pytest.approx(7)
    assert window["source_url"].startswith("https://ecocrop.apps.fao.org/")
    assert window["classification"] == "SPECIES_ENVELOPE_RESEARCH_SCREEN"
    assert potato["outdoor_agronomically_validated"] is False


def test_nonlinear_windows_are_not_calculated_after_averaging_model_weather():
    # Their average is 20°C and would pass; neither actual trajectory passes.
    frame = daily(2023, 0, "cold") + daily(2023, 40, "hot")
    result = evaluate_candidates({}, daily_frame=frame)
    potato = frontier(result, "potato")
    assert potato["status"] == "screened_out"
    assert potato["model_years_evaluated"] == 2
    assert potato["model_years_passing"] == 0
    assert {row["model"] for row in potato["annual"]} == {"cold", "hot"}


def test_daily_frontier_handles_celsius_degree_days_without_summing_different_years():
    result = evaluate_candidates({"daily": daily(2023, 3) + daily(2024, 3)})
    barley = frontier(result, "barley")
    heat = next(test for test in barley["tests"] if test["id"] == "heat_sum")
    assert heat["gdd_requirement_c_days"] == pytest.approx(2500 * 5 / 9)
    assert [row["gdd_available_c_days"] for row in heat["annual"]] == [1095, 1098]
    assert barley["model_years_passing"] == 0
    assert barley["status"] == "screened_out"


def test_heat_and_window_pass_must_coincide_in_the_same_year():
    # One year has insufficient heat; the other is above the species envelope.
    result = evaluate_candidates({"daily": daily(2023, 3) + daily(2024, 45)})
    barley = frontier(result, "barley")
    assert all(test["model_years_passing"] == 1 for test in barley["tests"])
    assert barley["model_years_passing"] == 0
    assert barley["status"] == "screened_out"


def test_incomplete_season_does_not_establish_failed_window():
    result = evaluate_candidates({}, daily_frame=daily(2023, 15)[:180])
    assert frontier(result, "potato")["status"] == "unknown"
    assert frontier(result, "potato")["model_years_evaluated"] is None


def test_daily_frame_duplicate_model_dates_are_rejected():
    frame = daily(2023, 10, "one")
    with pytest.raises(ValueError, match="Duplicate frontier"):
        evaluate_candidates({}, daily_frame=frame + frame)


def test_climate_positive_does_not_allocate_open_field_or_prove_water_and_energy():
    result = evaluate_candidates({"daily": daily(2023, 15)})
    for crop in result["candidates"]:
        row = crop["climate_frontier"]
        assert row["ground_gate"]["status"] == "requires_site_validation"
        assert row["ground_gate"]["eligible_for_normalized_plan"] is False
        assert row["resource_gate"]["status"] == "not_evaluated_here"
        assert next(m for m in crop["methods"] if m["method"] == "open_field")["eligible_for_normalized_plan"] is False
    assert result["counts"]["catalogued"] == 9
    assert result["counts"]["controlled_evidence_candidates"] == 6
    assert frontier(result, "lettuce")["status"] == "unknown"
    assert frontier(result, "lettuce")["controlled_environment_status"] == "candidate"


def test_frontier_sources_are_resolved_and_inputs_are_not_mutated():
    context = {"daily": daily(2023, 8)}
    before = deepcopy(context)
    result = evaluate_candidates(context)
    assert context == before
    assert len(result["climate_frontier"]["source_parameter_sha256"]) == 64
    for row in result["climate_frontier"]["crops"]:
        assert all(source in result["sources"] for source in row["source_ids"])


@pytest.fixture(scope="module")
def real_frontiers():
    results = {}
    for horizon, scenario in (("historical", "ssp245"), ("mid", "ssp245"), ("late", "ssp585")):
        context = get_climate_context("longyearbyen", horizon, scenario)
        frame = load_climate_frame("longyearbyen", horizon, scenario)
        results[(horizon, scenario)] = evaluate_candidates(context, "longyearbyen", frame)
    return results


def test_verified_nasa_horizons_change_only_supported_climate_screen(real_frontiers):
    observed = {}
    for key, result in real_frontiers.items():
        observed[key] = tuple(frontier(result, crop)["model_years_passing"] for crop in ("barley", "potato"))
        for crop in ("barley", "potato"):
            row = frontier(result, crop)
            assert row["model_years_evaluated"] == 60
            assert len({(r["model"], r["year"]) for r in row["annual"]}) == 60
            assert row["ground_gate"]["eligible_for_normalized_plan"] is False
        assert frontier(result, "wheat")["status"] == "unknown"
    assert observed == {("historical", "ssp245"): (0, 0),
                        ("mid", "ssp245"): (0, 3),
                        ("late", "ssp585"): (19, 51)}
    assert frontier(real_frontiers[("late", "ssp585")], "barley")["status"] == "potential"
    assert frontier(real_frontiers[("mid", "ssp245")], "barley")["status"] == "screened_out"


def test_multi_model_context_exposes_annual_not_twenty_year_cumulative_heat(real_frontiers):
    result = real_frontiers[("mid", "ssp245")]
    metrics = result["climate_metrics"]
    rows = metrics["annual"]
    assert len(rows) == 60
    assert metrics["gdd_base0_c_days"] == pytest.approx(sum(r["gdd_base0_c_days"] for r in rows) / 60)
    assert all(row["complete_year"] for row in rows)


def test_wrong_context_or_incomplete_model_set_cannot_silently_shrink_ensemble():
    context = get_climate_context("longyearbyen", "mid", "ssp245")
    with pytest.raises(ValueError, match="period"):
        evaluate_candidates(context, daily_frame=daily(2023, 10, context["models"][0]["model"]))
    with pytest.raises(ValueError, match="missing a selected climate model"):
        evaluate_candidates(context, daily_frame=daily(2041, 10, context["models"][0]["model"]))
