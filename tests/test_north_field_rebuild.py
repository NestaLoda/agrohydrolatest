"""PRE/POST audit tests. All profiles/coefficients below are synthetic fixtures."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json
import math
from types import ModuleType
import sys

from pydantic import ValidationError
import pytest

from backend import north_field as field
from backend.north_contracts import ModelExpectation, NorthRequest, Observation, ObserveRequest
from backend.north_optimizer import solve_pattern


BASE = datetime(2026, 9, 23, 12, tzinfo=timezone.utc)


class Clock(datetime):
    value = BASE

    @classmethod
    def now(cls, tz=None):
        return cls.value if tz else cls.value.replace(tzinfo=None)


def option():
    return {"crop_id": "synthetic_crop", "method": "hydroponics", "season": "annual",
            "yield_kg_m2": 2., "water_monthly_m3_m2": [1 / 12] * 12,
            "heat_kwh_th_m2": 10., "electricity_kwh_m2": 1.}


def expectation():
    return {"model_id": "synthetic-fixture", "version": "test-1",
            "source_url": "https://example.invalid/synthetic-model",
            "generated_at_utc": (BASE-timedelta(hours=1)).isoformat(),
            "valid_from_utc": (BASE-timedelta(hours=2)).isoformat(),
            "valid_to_utc": (BASE+timedelta(hours=2)).isoformat(),
            "latitude": 78.22, "longitude": 15.65, "temperature_kind": "in_situ",
            "salinity_kind": "absolute_mass_g_kg", "temporal_support": "instantaneous",
            "points": [{"depth_m": 0., "temperature_c": 1., "salinity_g_kg": 34.},
                       {"depth_m": 20., "temperature_c": 3., "salinity_g_kg": 36.}]}


def observation():
    return {"measured_at_utc": (BASE+timedelta(minutes=30)).isoformat(),
            "latitude": 78.22, "longitude": 15.65, "temperature_kind": "in_situ",
            "salinity_kind": "absolute_mass_g_kg", "calibration_record": "SYNTHETIC calibration fixture",
            "quality": "accepted", "instrument_id": "SYNTHETIC-instrument",
            "evidence_record": "Synthetic test only; not an Arctic observation",
            "points": deepcopy(expectation()["points"])}


@pytest.fixture(autouse=True)
def frozen_clock_and_source_model(monkeypatch):
    Clock.value = BASE
    monkeypatch.setattr(field, "datetime", Clock)
    # The rebuild's planning/resource modules can be absent while these isolated
    # field tests run. The stub is explicit; no physical RO accuracy is tested.
    monkeypatch.setattr(field, "code_hash", lambda: "synthetic-test-engine-version")
    resource = ModuleType("backend.north_resources")
    resource.ro_treatment = lambda s, t, recovery: {
        "specific_energy_kwh_m3": {"central": 4 + .1*(s-35) - .05*(t-2)},
        "conditioning_heat_kwh_th_m3": {"central": max(0., -t)},
        "status": "CONDITIONAL",
        "classification": "SYNTHETIC_TEST_FIXTURE", "recovery": recovery}
    monkeypatch.setitem(sys.modules, "backend.north_resources", resource)


def frozen_pair(tmp_path, *, model=None):
    scenario = NorthRequest().model_dump()
    inputs = {"options": [option()], "ro_kwh_m3": 4.}
    result = {"engine_inputs": inputs, "plan": solve_pattern(**inputs), "request": scenario}
    frozen = field.freeze_plan(scenario, result, expectation() if model is None else model,
                               directory=tmp_path, intake_depth_m=10.)
    Clock.value = BASE+timedelta(hours=1)
    request = ObserveRequest(freeze_id=frozen["freeze_id"], observation=observation(), intake_depth_m=10.,
                             connection_evidence="Synthetic physical-source linkage fixture; not a real claim.",
                             interpretation="present_source_scenario_transfer")
    return frozen, request, result


def test_frozen_source_equals_model_value_at_exact_frozen_intake(tmp_path):
    frozen, _, _ = frozen_pair(tmp_path)
    record = json.loads((tmp_path/(frozen["freeze_id"]+".json")).read_text())
    assert record["intake_depth_m"] == 10
    assert record["scenario"]["source_temperature_c"] == 2
    assert record["scenario"]["salinity_g_kg"] == 35
    assert field.profile_at_depth(record["expectation"], 10) == {
        "temperature_c": 2, "salinity_g_kg": 35}


def test_expectation_freeze_requires_intake_and_matching_pre_source(tmp_path):
    with pytest.raises(ValueError, match="derinliği"):
        field.freeze_plan(NorthRequest().model_dump(), {}, expectation(), directory=tmp_path)
    scenario = NorthRequest(salinity_g_kg=34).model_dump()
    with pytest.raises(ValueError, match="eşleşmiyor"):
        field.freeze_plan(scenario, {}, expectation(), directory=tmp_path, intake_depth_m=10)
    assert not list(tmp_path.glob("*.json"))


def test_post_cannot_change_frozen_intake_even_within_both_profiles(tmp_path):
    _, request, _ = frozen_pair(tmp_path)
    request.intake_depth_m = 5
    with pytest.raises(ValueError, match="derinli"):
        field.observe_plan(request, directory=tmp_path)


def test_identical_observation_no_pattern_change_is_valid_and_pre_is_immutable(tmp_path):
    frozen, request, result = frozen_pair(tmp_path)
    path = tmp_path/(frozen["freeze_id"]+".json")
    original_bytes = path.read_bytes()
    original_inputs = deepcopy(result["engine_inputs"])
    post = field.observe_plan(request, directory=tmp_path)
    assert path.read_bytes() == original_bytes
    assert field.digest(original_bytes) == frozen["sha256"]
    assert result["engine_inputs"] == original_inputs
    assert post["post_id"] != frozen["freeze_id"]
    assert len(list(tmp_path.glob("*.json"))) == 2
    assert post["comparison"]["residuals"] == {"temperature_c": 0., "salinity_g_kg": 0.}
    assert post["changes"]["changed_pattern"] is False
    assert post["changes"]["water_delta_m3"] == pytest.approx(0)
    assert post["changes"]["equivalent_electricity_delta_kwh"] == pytest.approx(0)
    assert "geçerli" in post["changes"]["message"]


def test_rerun_changes_only_ro_coefficient_and_preserves_same_solver_inputs():
    inputs = {"options": [option()], "ro_kwh_m3": 4., "objective": "water",
              "production_retention": .8, "freshwater_m3": 7., "area_m2": 100.}
    before = {"engine_inputs": deepcopy(inputs), "plan": solve_pattern(**inputs),
              "request": NorthRequest().model_dump()}
    after = field.rerun_source(before, 5., 40., .45)
    changed = {key for key in inputs if inputs[key] != after["engine_inputs"][key]}
    assert changed == {"ro_kwh_m3"}
    assert before["engine_inputs"] == inputs
    assert after["engine_inputs"]["ro_kwh_m3"] == pytest.approx(4.35)
    assert after["plan"]["solver"]["version"] == before["plan"]["solver"]["version"]
    assert after["plan"]["crop_outputs_kg"] == pytest.approx(before["plan"]["crop_outputs_kg"], abs=1e-4)


def test_source_observation_never_promotes_future_or_terrestrial_inputs(tmp_path):
    _, request, _ = frozen_pair(tmp_path)
    request.observation.points[0].salinity_g_kg += 2
    request.observation.points[1].salinity_g_kg += 2
    post = field.observe_plan(request, directory=tmp_path)
    assert set(post["updated_inputs"]) == {
        "marine_source_temperature_c", "marine_source_salinity_g_kg", "derived_ro_specific_energy_kwh_m3",
        "derived_ro_conditioning_heat_kwh_th_m3", "derived_ro_pressure_feasibility"}
    assert {"future_climate", "terrestrial_freshwater", "soil_permafrost", "crop_yields",
            "crop_water", "objective", "constraints"} <= set(post["unchanged_inputs"])
    assert post["classification"] == "FIELD_INFORMED_CONDITIONAL_SOURCE_SCENARIO"


@pytest.mark.parametrize("stamp", [(BASE-timedelta(seconds=1)).isoformat(), BASE.isoformat(),
                                   (BASE+timedelta(hours=3)).isoformat(), "2026-09-23T12:30:00",
                                   "2026-09-23T15:30:00+03:00"])
def test_observation_temporal_gate(stamp):
    Clock.value = BASE+timedelta(hours=1)
    observed = observation(); observed["measured_at_utc"] = stamp
    with pytest.raises(ValueError):
        field.compare_profiles(expectation(), observed, BASE.isoformat(), 10)


def test_outside_model_validity_is_rejected_even_after_freeze():
    Clock.value = BASE+timedelta(hours=4)
    observed = observation(); observed["measured_at_utc"] = (BASE+timedelta(hours=3)).isoformat()
    with pytest.raises(ValueError, match="zaman aralığı"):
        field.compare_profiles(expectation(), observed, BASE.isoformat(), 10)


@pytest.mark.parametrize("change", ["generation_future", "expired", "reversed_validity"])
def test_invalid_model_freeze_is_not_written(tmp_path, change):
    model = expectation()
    if change == "generation_future": model["generated_at_utc"] = (BASE+timedelta(minutes=1)).isoformat()
    if change == "expired": model["valid_to_utc"] = (BASE-timedelta(minutes=1)).isoformat()
    if change == "reversed_validity": model["valid_from_utc"] = (BASE+timedelta(hours=3)).isoformat()
    with pytest.raises(ValueError):
        field.freeze_plan(NorthRequest().model_dump(), {}, model, directory=tmp_path, intake_depth_m=10)
    assert not list(tmp_path.glob("*.json"))


def test_model_generated_after_freeze_cannot_be_relabelled_as_pre():
    Clock.value = BASE+timedelta(hours=1)
    model = expectation(); model["generated_at_utc"] = (BASE+timedelta(minutes=1)).isoformat()
    with pytest.raises(ValueError, match="önce"):
        field.compare_profiles(model, observation(), BASE.isoformat(), 10)


def test_location_mismatch_and_no_profile_extrapolation():
    Clock.value = BASE+timedelta(hours=1)
    observed = observation(); observed["latitude"] += .02
    with pytest.raises(ValueError, match="1 km"):
        field.compare_profiles(expectation(), observed, BASE.isoformat(), 10)
    with pytest.raises(ValueError, match="aralığında"):
        field.compare_profiles(expectation(), observation(), BASE.isoformat(), 21)


@pytest.mark.parametrize("points", [[{"depth_m": 0., "temperature_c": 1., "salinity_g_kg": 34.}]*2,
                                    list(reversed(expectation()["points"]))])
def test_profile_depths_must_be_unique_and_ordered(points):
    Clock.value = BASE+timedelta(hours=1)
    observed = observation(); observed["points"] = points
    with pytest.raises(ValueError, match="tekil"):
        field.compare_profiles(expectation(), observed, BASE.isoformat(), 0)


@pytest.mark.parametrize("key,value", [("temperature_kind", "potential"), ("salinity_kind", "practical_psu"),
                                      ("quality", "unverified"), ("calibration_record", "")])
def test_incompatible_quantity_or_unaccepted_quality_rejected(key, value):
    observed = observation(); observed[key] = value
    with pytest.raises(ValidationError):
        Observation.model_validate(observed)


def test_daily_mean_support_is_visible_and_not_claimed_as_instantaneous_model_error():
    Clock.value = BASE+timedelta(hours=1)
    model = expectation(); model["temporal_support"] = "daily_mean"
    comparison = field.compare_profiles(model, observation(), BASE.isoformat(), 10)
    assert comparison["temporal_support"] == "daily_mean"
    assert any("yalnız model hatası değildir" in limit for limit in comparison["limits"])


def test_engine_version_change_blocks_same_engine_claim(tmp_path, monkeypatch):
    _, request, _ = frozen_pair(tmp_path)
    monkeypatch.setattr(field, "code_hash", lambda: "different-engine")
    with pytest.raises(ValueError, match="sürümü"):
        field.observe_plan(request, directory=tmp_path)
    assert len(list(tmp_path.glob("*.json"))) == 1


def test_plan_only_freeze_cannot_be_promoted_to_before_observation_expectation(tmp_path):
    frozen = field.freeze_plan(NorthRequest().model_dump(), {}, directory=tmp_path)
    Clock.value = BASE+timedelta(hours=1)
    request = ObserveRequest(freeze_id=frozen["freeze_id"], observation=observation(), intake_depth_m=10,
                             connection_evidence="Synthetic source linkage fixture record",
                             interpretation="present_source_scenario_transfer")
    with pytest.raises(ValueError, match="beklentisi yok"):
        field.observe_plan(request, directory=tmp_path)


def test_pattern_change_counts_unallocated_area_and_feasibility_honestly():
    before = solve_pattern([option()])
    after = {"status": "infeasible", "allocations": []}
    changes = field.pattern_changes(before, after)
    assert changes["area_reallocated_m2"] == pytest.approx(before["totals"]["area_m2"], abs=1e-4)
    assert changes["area_reduced_m2"] == pytest.approx(before["totals"]["area_m2"], abs=1e-4)
    assert changes["feasibility_changed"] is True
    assert changes["water_delta_m3"] is None


def test_water_source_or_energy_change_does_not_force_crop_change():
    before = solve_pattern([option()], ro_kwh_m3=4.)
    after = solve_pattern([option()], ro_kwh_m3=5.)
    changes = field.pattern_changes(before, after)
    assert changes["changed_pattern"] is False
    assert changes["equivalent_electricity_delta_kwh"] == pytest.approx(before["totals"]["desalinated_m3"]*(5.-4.), abs=1e-3)
    assert changes["water_source_deltas_m3"]["desalinated_m3"] == pytest.approx(0, abs=1e-5)


@pytest.mark.parametrize("key", ["area_m2", "production_retention", "storage_m3", "freshwater_m3", "ro_kwh_m3", "ro_heat_kwh_th_m3", "heat_cop", "energy_limit_kwh"])
@pytest.mark.parametrize("value", [math.nan, math.inf, True])
def test_lp_rejects_nonfinite_resources_at_its_own_boundary(key, value):
    with pytest.raises(ValueError):
        solve_pattern([option()], **{key: value})


def test_binding_energy_and_freshwater_constraints_are_reported():
    # Exactly enough energy for the explicit five m2 diversity floor: binding.
    energy_limited = solve_pattern([option()], energy_limit_kwh=75.)
    assert "Enerji sınırı" in energy_limited["binding_constraints"]
    assert "Yetiştirme alanı" not in energy_limited["binding_constraints"]
    freshwater_limited = solve_pattern([option()], desalination=False, freshwater_m3=5.)
    assert "Karasal su tahsisi" in freshwater_limited["binding_constraints"]
    assert freshwater_limited["totals"]["area_m2"] == pytest.approx(5, abs=1e-4)
    # The declared 95% production policy may leave resource slack; do not label
    # an offered ceiling as binding merely because it limited maximum production.
    slack = solve_pattern([option()], energy_limit_kwh=150.)
    assert "Enerji sınırı" not in slack["binding_constraints"]
    assert slack["totals"]["equivalent_electricity_kwh"] == pytest.approx(142.5, abs=1e-4)
    energy_constraint = next(c for c in slack["resource_constraints"] if c["name"] == "Enerji sınırı")
    assert energy_constraint["slack"] == pytest.approx(7.5, abs=1e-4)


def test_profile_nan_and_extra_terrestrial_updates_are_not_accepted():
    observed = observation(); observed["points"][0]["temperature_c"] = math.nan
    with pytest.raises(ValidationError): Observation.model_validate(observed)
    observed = observation(); observed["terrestrial_freshwater_m3"] = 1000
    with pytest.raises(ValidationError): Observation.model_validate(observed)


def test_treatment_heat_is_thermal_and_cop_applies_once_to_electric_equivalent():
    result = solve_pattern([option()], ro_kwh_m3=4., ro_heat_kwh_th_m3=6., heat_cop=2.)
    totals = result["totals"]
    volume, area = totals["desalinated_m3"], totals["area_m2"]
    assert totals["treatment_heat_kwh_th"] == pytest.approx(volume*6., abs=1e-3)
    assert totals["treatment_electricity_kwh"] == pytest.approx(volume*4., abs=1e-3)
    assert totals["heat_kwh_th"] == pytest.approx(area*10.+volume*6., abs=1e-3)
    assert totals["electricity_kwh"] == pytest.approx(area+volume*4., abs=1e-3)
    assert totals["equivalent_electricity_kwh"] == pytest.approx(totals["electricity_kwh"]+totals["heat_kwh_th"]/2., abs=1e-3)


def test_subzero_source_rerun_updates_derived_conditioning_heat_too():
    inputs = {"options": [option()], "ro_kwh_m3": 4., "ro_heat_kwh_th_m3": 0., "heat_cop": 2.}
    before = {"engine_inputs": deepcopy(inputs), "plan": solve_pattern(**inputs),
              "request": NorthRequest().model_dump()}
    after = field.rerun_source(before, -1., 35., .45)
    assert after["engine_inputs"]["ro_heat_kwh_th_m3"] == 1.
    assert after["engine_inputs"]["heat_cop"] == 2.
    assert before["engine_inputs"]["ro_heat_kwh_th_m3"] == 0.
    assert after["plan"]["totals"]["treatment_heat_kwh_th"] == pytest.approx(after["plan"]["totals"]["desalinated_m3"]*1., abs=1e-3)


def test_observation_never_enables_a_source_the_user_disabled():
    request = NorthRequest(desalination=False, freshwater_m3=100.).model_dump()
    inputs = {"options": [option()], "desalination": False, "freshwater_m3": 100., "ro_kwh_m3": 4.}
    before = {"engine_inputs": deepcopy(inputs), "plan": solve_pattern(**inputs), "request": request}
    after = field.rerun_source(before, 5., 30., .45)
    assert after["engine_inputs"]["desalination"] is False
    assert after["plan"]["totals"]["desalinated_m3"] == 0.


def test_pressure_failure_can_remove_source_and_change_feasibility(monkeypatch):
    resource = sys.modules["backend.north_resources"]
    monkeypatch.setattr(resource, "ro_treatment", lambda s, t, recovery: {
        "specific_energy_kwh_m3": {"central": 4.},
        "conditioning_heat_kwh_th_m3": {"central": 0.}, "status": "INFEASIBLE"})
    inputs = {"options": [option()], "desalination": True, "ro_kwh_m3": 4.}
    before = {"engine_inputs": deepcopy(inputs), "plan": solve_pattern(**inputs),
              "request": NorthRequest().model_dump()}
    after = field.rerun_source(before, 2., 40., .45)
    assert after["engine_inputs"]["desalination"] is False
    assert after["plan"]["status"] == "infeasible"
    assert field.pattern_changes(before["plan"], after["plan"])["feasibility_changed"] is True
