from copy import deepcopy
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path

import pytest

from backend.north_resources import (
    controlled_energy, roof_storage_balance, recirculation_makeup, ro_treatment,
    model_profile_provenance, get_resource_evidence, _osmotic_pressure_bar,
)


def weather(n=5, start="2041-01-01", temp=-10., rain=0., solar=0., model="member1"):
    first = date.fromisoformat(start)
    return [{"date":(first+timedelta(days=i)).isoformat(),"tmin_c":temp-2,"tmax_c":temp+2,
             "precipitation_mm":rain,"shortwave_mj_m2":solar,"model":model} for i in range(n)]


def test_electricity_components_and_heat_remain_separate():
    result = controlled_energy(weather(), method="greenhouse")
    components = ["lighting_kwh_m2","pumping_kwh_m2","fans_kwh_m2","dehumidification_kwh_m2","cooling_kwh_m2"]
    assert result["electricity_kwh_m2"]["central"] == pytest.approx(sum(result[k]["central"] for k in components))
    assert result["equivalent_electricity_kwh_m2"]["central"] == pytest.approx(result["electricity_kwh_m2"]["central"]+result["heat_kwh_th_m2"]["central"])
    assert result["heat_kwh_th_m2"]["central"] > 0


def test_colder_climate_increases_greenhouse_heat():
    cold = controlled_energy(weather(temp=-20))
    mild = controlled_energy(weather(temp=0))
    assert cold["heat_kwh_th_m2"]["central"] > mild["heat_kwh_th_m2"]["central"]


def test_night_setpoint_is_optional_and_changes_heat_and_water():
    steady=controlled_energy(weather(),target_temp_c=21)
    day_night=controlled_energy(weather(),target_temp_c=21,overrides={"target_temp_c_night":16})
    assert day_night["heat_kwh_th_m2"]["central"] < steady["heat_kwh_th_m2"]["central"]
    assert day_night["fresh_makeup_m3_m2"]["central"] < steady["fresh_makeup_m3_m2"]["central"]


def test_light_energy_exact_photon_conversion_and_photoperiod():
    a = controlled_energy(weather(1), method="indoor", photoperiod_h=1.5)
    b = controlled_energy(weather(1), method="indoor", photoperiod_h=24)
    assert a["lighting_kwh_m2"]["central"] == pytest.approx(14/(3.6*2.6))
    assert a["lighting_kwh_m2"] == b["lighting_kwh_m2"]
    assert a["setpoints"]["maximum_supplemental_ppfd_umol_m2_s"] > b["setpoints"]["maximum_supplemental_ppfd_umol_m2_s"]


def test_sunlight_reduces_greenhouse_lighting_but_not_opaque_indoor():
    dark = weather(1, start="2041-06-01", solar=0)
    sunny = weather(1, start="2041-06-01", solar=20)
    assert controlled_energy(sunny)["lighting_kwh_m2"]["central"] < controlled_energy(dark)["lighting_kwh_m2"]["central"]
    assert controlled_energy(sunny,method="indoor")["lighting_kwh_m2"] == controlled_energy(dark,method="indoor")["lighting_kwh_m2"]


def test_season_mask_retains_chronology_and_zeroes_inactive_operation():
    result = controlled_energy(weather(40), overrides={"active_months":[2]})
    assert len(result["daily"]) == 40
    assert all(r["fresh_makeup_m3_m2"] == 0 for r in result["daily"][:31])
    assert result["mean_operating_days"] == 9
    assert result["monthly"][0]["heat_kwh_th_m2"]["central"] == 0
    assert result["water_monthly_m3_m2"][1] > 0


def test_years_average_outputs_after_daily_simulation():
    a, b = weather(2,start="2041-01-01",temp=-20), weather(2,start="2042-01-01",temp=0)
    joint = controlled_energy(a+b)
    expected = (controlled_energy(a)["heat_kwh_th_m2"]["central"]+controlled_energy(b)["heat_kwh_th_m2"]["central"])/2
    assert joint["heat_kwh_th_m2"]["central"] == pytest.approx(expected)
    assert len(joint["annual"]) == 2
    assert joint["monthly"][0]["heat_kwh_th_m2"]["central"] == pytest.approx(expected)


def test_monthly_configurations_reconstruct_masked_season_without_mixing_bounds():
    rows=weather(60)
    annual=controlled_energy(rows)
    season=controlled_energy(rows,overrides={"active_months":[2]})
    for key in ["heat_kwh_th_m2","electricity_kwh_m2","fresh_makeup_m3_m2"]:
        values=annual["monthly_configurations"][1][key]
        assert season[key] == pytest.approx({"low":min(values),"central":values[1],"high":max(values)})


def test_water_makeup_subtracts_distinct_reuse_streams_once():
    result = controlled_energy(weather(1),method="indoor")
    row = result["daily"][0]
    consumption = row["transpiration_l_m2"]/1000 + .05/1000
    expected = consumption+row["discharged_drainage_m3_m2"]-row["recovered_condensate_m3_m2"]
    assert row["fresh_makeup_m3_m2"] == pytest.approx(expected)
    assert row["fresh_makeup_m3_m2"] > 0


@pytest.mark.parametrize("bad", [None,float("nan"),float("inf"),-1])
def test_invalid_radiation_is_not_zeroed(bad):
    rows=weather(1);rows[0]["shortwave_mj_m2"]=bad
    with pytest.raises(ValueError): controlled_energy(rows)


def test_ensemble_members_cannot_be_merged_into_fake_daily_weather():
    rows=weather(2);rows[1]["model"]="member2"
    with pytest.raises(ValueError,match="separately"): controlled_energy(rows)


def test_roof_snow_is_delayed_and_both_mass_balances_close():
    rows=weather(3,temp=-5,rain=10)
    rows[1].update(tmin_c=0,tmax_c=2,precipitation_mm=0)
    rows[2].update(tmin_c=8,tmax_c=12,precipitation_mm=0)
    result=roof_storage_balance(rows,[.004]*3,roof_m2=1,storage_m3=.01)
    assert result["daily"][0]["captured_m3"] == 0
    assert result["daily"][0]["snowpack_mm"] == 10
    assert result["daily"][1]["melt_mm"] == 3
    assert result["daily"][2]["melt_mm"] == 7
    assert result["totals"]["captured_m3"] == pytest.approx(.008)
    assert result["totals"]["storage_balance_residual_m3"] == pytest.approx(0,abs=1e-12)
    assert result["totals"]["precipitation_balance_residual_m3"] == pytest.approx(0,abs=1e-12)


def test_tank_demand_order_and_spill():
    result=roof_storage_balance(weather(2,temp=5,rain=100),[.02,0],roof_m2=1,storage_m3=.01,collection_efficiency=1)
    assert result["totals"]["supplied_m3"] == pytest.approx(.02)
    assert result["totals"]["spill_m3"] == pytest.approx(.17)
    assert result["totals"]["final_storage_m3"] == pytest.approx(.01)


def test_roof_cross_year_snow_carries_forward_before_averaging():
    rows=weather(2,start="2041-12-31",temp=-5,rain=10)
    rows[1].update(tmin_c=5,tmax_c=5,precipitation_mm=0)
    result=roof_storage_balance(rows,[0,0])
    assert result["daily"][1]["captured_m3"] == pytest.approx(.008)
    assert result["climatology_monthly"][0]["captured_m3"] == pytest.approx(.004)


def test_storage_rejects_missing_days_and_unknown_precipitation():
    rows=weather(3)
    with pytest.raises(ValueError,match="contiguous"): roof_storage_balance([rows[0],rows[2]],[0,0])
    rows[0]["precipitation_mm"]=None
    with pytest.raises(ValueError): roof_storage_balance(rows,[0,0,0])


def test_recirculation_conserves_water_and_does_not_create_resource():
    result=recirculation_makeup(100,.3,.9)
    assert result["reused_m3"] == pytest.approx(27)
    assert result["makeup_m3"] == pytest.approx(73)
    assert result["makeup_m3"] == pytest.approx(result["consumptive_m3"]+result["discharged_m3"])


def test_osmotic_pressure_reference_and_dilute_continuity():
    assert _osmotic_pressure_bar(0,25) == 0
    assert 25 < _osmotic_pressure_bar(35,25) < 29
    assert _osmotic_pressure_bar(9.999999,25) == pytest.approx(_osmotic_pressure_bar(10,25),rel=1e-6)


def test_ro_salinity_and_cold_temperature_affect_energy():
    warm=ro_treatment(35,25)
    cold=ro_treatment(35,0)
    dilute=ro_treatment(25,25)
    assert cold["specific_energy_kwh_m3"]["central"] > warm["specific_energy_kwh_m3"]["central"] > dilute["specific_energy_kwh_m3"]["central"]


def test_subzero_ro_explicit_conditioning_heat_not_fake_warm_extrapolation():
    cold,zero=ro_treatment(35,-1),ro_treatment(35,0)
    assert cold["temperature_regime"] == "conditioned_to_zero"
    assert cold["specific_energy_kwh_m3"] == zero["specific_energy_kwh_m3"]
    assert cold["conditioning_heat_kwh_th_m3"]["central"] == pytest.approx(4000/(3600*.45))
    assert zero["conditioning_heat_kwh_th_m3"]["central"] == 0


def test_ro_feed_product_brine_and_salt_balance():
    result=ro_treatment(32,5,recovery=.4,product_water_m3=10)
    assert result["feed_water_m3"] == 25
    assert result["brine_water_m3"] == 15
    assert result["feed_water_m3"]*32 == pytest.approx(result["brine_water_m3"]*result["brine_salinity_g_kg"])
    assert result["electricity_kwh"]["central"] == pytest.approx(10*result["specific_energy_kwh_m3"]["central"])


def test_ro_pressure_failure_is_not_hidden_by_clamping():
    result=ro_treatment(45,0,recovery=.6)
    assert result["status"] == "PRESSURE_LIMIT_EXCEEDED"
    assert result["pressure_bar"]["central"] > 83


@pytest.mark.parametrize("kwargs", [{"salinity_g_kg":None},{"salinity_g_kg":-1},{"temperature_c":float('nan')},{"recovery":1},{"product_water_m3":-1}])
def test_ro_rejects_invalid_inputs(kwargs):
    args={"salinity_g_kg":35,"temperature_c":5};args.update(kwargs)
    with pytest.raises(ValueError): ro_treatment(**args)


def profile():
    meta=dict(product_id="real-product",dataset_id="native-3d",dataset_version="v1",source_url="https://example.org/data.nc",license="CC-BY",sha256="a"*64,
        time_start_utc="2026-08-01T00:00:00Z",time_end_utc="2026-08-01T23:59:59Z",aggregation="daily_mean",
        requested_position={"latitude":78,"longitude":16},grid_position={"latitude":78.1,"longitude":16.1},horizontal_resolution_km=12,
        vertical_coordinate="depth_m",temperature_kind="potential",salinity_kind="model_sea_water_salinity",temperature_unit="degC",salinity_unit="1e-3",
        dimensions=["time","depth","y","x"],dimensions_verified=True,retrieved_at_utc="2026-09-23T00:00:00Z")
    return meta,[dict(depth_m=0,temperature_c=2,salinity=33),dict(depth_m=10,temperature_c=1,salinity=34)]


def test_native_topaz_definitions_are_preserved_not_silently_ro_compatible():
    meta,points=profile(); result=model_profile_provenance(meta,points)
    assert result["ro_definition_compatible"] is False
    assert result["metadata"]["temperature_kind"] == "potential"
    meta.update(temperature_kind="in_situ",salinity_kind="mass_salinity",salinity_unit="g/kg")
    assert model_profile_provenance(meta,points)["ro_definition_compatible"] is True


def test_surface_pixel_cannot_be_called_water_column():
    meta,points=profile();meta["dimensions"]=["time","y","x"]
    with pytest.raises(ValueError,match="surface pixel"):model_profile_provenance(meta,points)
    meta,points=profile()
    with pytest.raises(ValueError,match="two actual"):model_profile_provenance(meta,points[:1])


def test_profile_requires_real_hash_utc_units_and_unique_depths():
    for field,value in [("sha256","placeholder"),("time_start_utc","2026-08-01T00:00:00"),("salinity_unit","PSU"),("dimensions_verified",False)]:
        meta,points=profile();meta[field]=value
        with pytest.raises(ValueError):model_profile_provenance(meta,points)
    meta,points=profile();points[1]["depth_m"]=0
    with pytest.raises(ValueError):model_profile_provenance(meta,points)


def test_evidence_has_no_invented_local_supply_and_cached_sources_match():
    evidence=get_resource_evidence()
    assert evidence["local_context"]["agricultural_freshwater_allocation_m3_year"] is None
    assert evidence["local_context"]["agricultural_energy_allocation_kwh_year"] is None
    root=Path(__file__).resolve().parents[1]
    for source in evidence["downloaded_sources"]:
        if source["status"] == "downloaded":
            assert hashlib.sha256((root/source["local_path"]).read_bytes()).hexdigest() == source["sha256"]
