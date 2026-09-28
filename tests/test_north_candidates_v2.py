"""Scientific-boundary and dimensional checks for the northern catalogue."""
from datetime import date, timedelta
import math

import pytest

from backend.north_candidates import (
    complete_cycle_capacity,
    evaluate_candidates,
    get_catalog,
    get_ground_evidence,
)


def crop(crop_id):
    return next(c for c in get_catalog()["crops"] if c["crop_id"] == crop_id)


def days(year, low, high):
    day = date(year, 1, 1)
    end = date(year + 1, 1, 1)
    result = []
    while day < end:
        result.append({"date": day.isoformat(), "tmin_c": low, "tmax_c": high})
        day += timedelta(days=1)
    return result


def test_more_than_three_research_candidates_have_traceable_yield_ranges():
    catalog = get_catalog()
    controlled = [c for c in catalog["crops"] if c["production"]]
    assert len(catalog["crops"]) == 9
    assert len(controlled) == 6
    for c in controlled:
        p = c["production"]
        assert p["replicate_cycles"] >= 2
        assert p["yield_kg_m2_cycle"]["range_kind"] == "reported_observed_min_max"
        assert p["source_id"] in catalog["sources"]
        assert c["water"]["makeup_m3_kg"] is None


def test_eden_light_ramps_do_not_inflate_dli_by_counting_seventeen_full_hours():
    p = crop("lettuce")["production"]
    assert p["photoperiod_h"] == 17
    assert p["equivalent_full_light_hours"] == 16
    assert p["dli_mol_m2_day"] == pytest.approx(19.008)
    assert p["dli_mol_m2_day"] < p["ppfd_umol_m2_s"] * 17 * 3600 / 1e6
    assert crop("radish")["production"]["dli_mol_m2_day"] == pytest.approx(34.56)


def test_partial_cultivation_cycle_does_not_yield_a_fractional_harvest():
    result = complete_cycle_capacity(crop("lettuce"), 75, 100)
    assert result["complete_cycles"] == 1
    assert result["yield_kg"]["central"] == pytest.approx(238)
    assert result["remaining_days"] == 37
    two = complete_cycle_capacity(crop("lettuce"), 76, 100)
    assert two["complete_cycles"] == 2
    assert two["yield_kg"]["central"] == pytest.approx(476)


def test_multiple_harvest_basil_is_one_long_cycle_not_121_harvests():
    result = complete_cycle_capacity(crop("basil"), 120)
    assert result["complete_cycles"] == 0
    assert result["yield_kg"]["central"] == 0
    result = complete_cycle_capacity(crop("basil"), 242)
    assert result["complete_cycles"] == 2
    assert result["yield_kg"]["central"] == pytest.approx(1460)


@pytest.mark.parametrize("value", [-1, math.nan, math.inf, True])
def test_capacity_rejects_invalid_area_or_time(value):
    with pytest.raises(ValueError):
        complete_cycle_capacity(crop("lettuce"), value)
    with pytest.raises(ValueError):
        complete_cycle_capacity(crop("lettuce"), 100, value)


def test_unresolved_field_yield_stays_null_instead_of_zero():
    result = complete_cycle_capacity(crop("potato"), 100)
    assert result["yield_kg"] is None
    assert result["complete_cycles"] is None


def test_annual_climate_heat_does_not_sum_two_years_into_one_season():
    result = evaluate_candidates({"daily": days(2023, 2, 4) + days(2024, 2, 4)})
    metrics = result["climate_metrics"]
    assert metrics["gdd_base0_c_days"] == pytest.approx((365 * 3 + 366 * 3) / 2)
    barley = next(c for c in result["candidates"] if c["crop_id"] == "barley")
    assert barley["climate_screen"]["status"] == "screened_out"
    assert barley["climate_screen"]["gdd_requirement_c_days"] == pytest.approx(2500 * 5 / 9)
    assert barley["climate_screen"]["years_meeting_heat_target"] == 0


def test_no_gdd5_to_gdd0_substitution_and_missing_climate_not_zero():
    result = evaluate_candidates({"summary": {"gdd5": 1500}})
    assert result["climate_metrics"]["gdd_base0_c_days"] is None
    barley = next(c for c in result["candidates"] if c["crop_id"] == "barley")
    assert barley["climate_screen"]["gdd_available_c_days"] is None
    assert barley["climate_screen"]["status"] != "screened_out"


def test_incomplete_daily_year_not_presented_as_full_annual_gdd():
    result = evaluate_candidates({"daily": days(2023, 10, 12)[:20]})
    assert result["climate_metrics"]["gdd_base0_c_days"] is None
    assert result["climate_metrics"]["annual"][0]["complete_year"] is False


def test_hot_climate_does_not_override_unvalidated_ground():
    result = evaluate_candidates({"gdd0": 2500, "frost_free_days": 200})
    barley = next(c for c in result["candidates"] if c["crop_id"] == "barley")
    assert barley["climate_screen"]["status"] == "requires_agronomic_validation"
    field = next(m for m in barley["methods"] if m["method"] == "open_field")
    assert field["status"] == "requires_site_validation"
    assert field["eligible_for_normalized_plan"] is False


def test_cold_outside_does_not_veto_engineered_indoor_candidates():
    result = evaluate_candidates({"gdd0": 0, "frost_free_days": 0})
    assert result["counts"]["controlled_evidence_candidates"] == 6
    for c in result["candidates"]:
        if c["production"]:
            assert all(m["construction_validated"] is False for m in c["methods"] if m["method"] != "open_field")
            assert c["normalized_plan_eligible"] is True


def test_ground_observation_is_point_context_not_field_soil_or_future_projection():
    g = get_ground_evidence()
    observations = g["active_layer_observations"]["rows"]
    assert len(observations) == 27
    assert observations[-1] == {"year": 2024, "value": 218}
    assert g["permafrost"]["source_distance_km_approx"] == 20
    assert g["permafrost"]["current_site_parcel_verified"] is False
    assert g["permafrost"]["future_permafrost_projected"] is False
    assert g["soil"]["soil_ph"] is None
    assert g["acquisition"]["esa_cci"]["selected_pixel_value"] is None


def test_unknown_site_does_not_inherit_longyearbyen_soil():
    with pytest.raises(ValueError, match="Unsupported"):
        evaluate_candidates({}, "unverified_site")


def test_callers_cannot_mutate_next_catalog_or_candidate_result():
    catalog = get_catalog()
    catalog["crops"][0]["production"]["cycle_days"] = 1
    assert crop("lettuce")["production"]["cycle_days"] == 38
    first = evaluate_candidates({})
    first["candidates"][0]["methods"][1]["eligible_for_normalized_plan"] = False
    assert evaluate_candidates({})["candidates"][0]["methods"][1]["eligible_for_normalized_plan"] is True


def test_daily_ensemble_duplicate_dates_must_be_summarized_before_screening():
    with pytest.raises(ValueError, match="duplicate"):
        evaluate_candidates({"daily": days(2023, 5, 7) + days(2023, 6, 8)})


def test_xu_scope_is_pinned_and_not_claimed_as_reproduced_maxent():
    xu = get_catalog()["xu_2026"]
    assert xu["gcm_count"] == 5
    assert len(xu["crops"]) == 7
    assert xu["scenarios"] == ["SSP1-2.6", "SSP5-8.5"]
    assert xu["periods"] == ["1980-2010", "2041-2070", "2071-2100"]
