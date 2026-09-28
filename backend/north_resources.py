"""Traceable resource scenarios per square metre of single-level growing area.

These are engineering screening calculations, not measured Svalbard capacity or
locally calibrated crop/building models. Bounds are scenario envelopes, not CIs.
Only one climate model may enter a calculation; weather is processed daily before
annual averaging. Thermal and electrical energy always remain separate.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime
from math import acos, cos, exp, isfinite, pi, sin, sqrt, tan
from pathlib import Path
import hashlib
import json
import re

VERSION = "north-resources-physics-2"
EVIDENCE_PATH = Path(__file__).resolve().parents[1] / "data/north/resource_evidence.json"
FAO = "https://www.fao.org/4/x0490e/x0490e06.htm"
MIT = "https://web.mit.edu/seawater/"
DUPONT = "https://www.dupont.com/content/dam/water/amer/us/en/water/public/documents/en/RO-NF-FilmTec-Manual-45-D01504-en.pdf"


def _number(value, name, lo=None, hi=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
        raise ValueError(f"{name}: a finite number is required")
    value = float(value)
    if (lo is not None and value < lo) or (hi is not None and value > hi):
        raise ValueError(f"{name}: outside [{lo}, {hi}]")
    return value


def _records(daily, *, radiation=False, precipitation=False, contiguous=False):
    if hasattr(daily, "to_dict"):
        daily = daily.to_dict("records")
    rows = list(daily)
    if not rows:
        raise ValueError("At least one daily record is required")
    if len({r.get("model") for r in rows if r.get("model") is not None}) > 1:
        raise ValueError("Process climate ensemble members separately before averaging outputs")
    out, last = [], None
    for r in rows:
        d = date.fromisoformat(str(r["date"])[:10])
        if last is not None and (d <= last or (contiguous and (d-last).days != 1)):
            raise ValueError("Daily dates must be unique, increasing and (for storage) contiguous")
        last = d
        tmin = _number(r.get("tmin_c", r.get("tmin")), "tmin_c", -90, 65)
        tmax = _number(r.get("tmax_c", r.get("tmax")), "tmax_c", -90, 65)
        if tmin > tmax:
            raise ValueError("tmin exceeds tmax")
        row = {"date": d, "tmin_c": tmin, "tmax_c": tmax}
        if radiation:
            row["shortwave"] = _number(r.get("shortwave_mj_m2", r.get("shortwave_mj_m2_day")), "shortwave_mj_m2", 0, 60)
        if precipitation:
            row["precip"] = _number(r.get("precipitation_mm", r.get("precip_mm")), "precipitation_mm", 0, 1000)
        out.append(row)
    return out


def _envelope(values):
    return {"low": min(values), "central": values[1], "high": max(values)}


def get_resource_evidence():
    raw = EVIDENCE_PATH.read_bytes()
    result = json.loads(raw)
    result["sha256"] = hashlib.sha256(raw).hexdigest()
    return result


# Parameter order: efficient/middle/resource-intensive engineering configurations.
# Sourced material/equipment ranges and project design choices are separated in JSON.
_COMMON = {
    "envelope_area_per_floor_m2": [2.2, 2.2, 2.2],
    "height_m": [3, 3, 3],
    "led_umol_j": [3.0, 2.6, 2.1],
    "relative_humidity": [.8, .7, .6],
    "canopy_resistance_s_m": [250, 150, 70],
    "aerodynamic_resistance_s_m": [200, 120, 70],
    "canopy_radiation_absorptance": [.65, .75, .85],
    "dehumidifier_l_kwh": [3.81, 2.22, 1.7],
    "drainage_fraction": [.1, .2, .3],
    "drainage_recovery_fraction": [.98, .95, .9],
    "condensate_reuse_fraction": [.95, .9, .8],
    "pump_flow_l_min_m2": [.1, .2, .3],
    "pump_head_m": [2, 3, 4],
    "pump_efficiency": [.65, .5, .35],
    "fan_w_m2": [1, 2, 4],
    "cooling_cop": [4, 3, 2.5],
    "biomass_water_l_m2_day": [.03, .05, .08],
    "latitude_deg": [78.2232]*3,
}
_METHOD = {
    "greenhouse": {
        "u_w_m2_k": [2.84, 3.12, 3.97], "air_changes_h": [.5, .75, 1],
        "solar_transmission": [.75, .65, .55],
        "condensed_fraction": [.3, .2, .1],
    },
    "indoor": {
        "u_w_m2_k": [.3, .45, .6], "air_changes_h": [.1, .2, .3],
        "solar_transmission": [0, 0, 0],
        "condensed_fraction": [.95, .9, .8],
    },
}


def _parameters(method, overrides):
    params = {k: list(v) for k, v in {**_COMMON, **_METHOD[method]}.items()}
    for k, v in (overrides or {}).items():
        if k not in params:
            raise ValueError(f"Unknown resource parameter {k}")
        values = list(v) if isinstance(v, (list, tuple)) else [v]*3
        if len(values) != 3:
            raise ValueError(f"{k}: expected three engineering configurations")
        params[k] = [_number(x, k, 0) for x in values]
    fractions = {"relative_humidity", "canopy_radiation_absorptance", "drainage_fraction", "drainage_recovery_fraction", "condensate_reuse_fraction", "pump_efficiency", "solar_transmission", "condensed_fraction"}
    for k, values in params.items():
        if k in fractions and max(values) > 1:
            raise ValueError(f"{k}: must not exceed one")
        if k in {"canopy_resistance_s_m", "aerodynamic_resistance_s_m", "led_umol_j", "dehumidifier_l_kwh", "pump_efficiency", "cooling_cop"} and min(values) <= 0:
            raise ValueError(f"{k}: must be positive")
    if max(params["drainage_fraction"]) >= 1 or max(params["latitude_deg"]) >= 90:
        raise ValueError("Drainage fraction <1 and latitude <90 required")
    return params


def _daylight_hours(day, latitude):
    # FAO-56 Eqs 24/25/34. Polar night/day handled by acos domain limits.
    declination = .409*sin(2*pi*day.timetuple().tm_yday/365 - 1.39)
    x = -tan(latitude*pi/180)*tan(declination)
    return 24/pi*acos(max(-1, min(1, x)))


def _canopy_transpiration(temp, dli, p):
    """Bulk PM Eq3: Pa/K, W/m² and s/m; returns kg(=L)/m²/day.

    Controlled-canopy resistance, humidity and intercepted radiation are explicit
    scenario parameters. This is NOT FAO reference-grass ET0 or calibrated crop ET.
    """
    es = 610.8*exp(17.27*temp/(temp+237.3))
    slope = 4098*es/(temp+237.3)**2
    gamma = 66.5  # Pa/K at reference ~101.3 kPa pressure
    rn = dli*.219e6/86400*p["canopy_radiation_absorptance"]
    latent_flux = (slope*rn + 1.2*1006*es*(1-p["relative_humidity"])/p["aerodynamic_resistance_s_m"])/(slope+gamma*(1+p["canopy_resistance_s_m"]/p["aerodynamic_resistance_s_m"]))
    return max(0, latent_flux*86400/2.45e6)


def controlled_energy(daily, method="greenhouse", target_temp_c=18.,
                      target_dli_mol_m2_day=14., photoperiod_h=16., overrides=None):
    """Daily building/lighting/water screening, per m² of one growing layer.

    Top-level and ``monthly`` results are mean annual selected-period totals;
    ``annual`` retains each year's actual totals. Missing months contribute zero
    operating days, not zero weather. ``daily`` reports central configuration.
    Photoperiod sizes light power; a fixed DLI fixes total photon energy.
    """
    if method not in _METHOD:
        raise ValueError("method must be greenhouse or indoor")
    target = _number(target_temp_c, "target_temp_c", 5, 35)
    dli = _number(target_dli_mol_m2_day, "target_dli_mol_m2_day", 0, 60)
    hours = _number(photoperiod_h, "photoperiod_h", 1, 24)
    rows = _records(daily, radiation=True)
    overrides = dict(overrides or {})
    active_months = overrides.pop("active_months", None)
    night_target = _number(overrides.pop("target_temp_c_night",target), "target_temp_c_night",5,35)
    if active_months is not None:
        if not active_months or any(type(m) is not int or m not in range(1,13) for m in active_months):
            raise ValueError("active_months must contain calendar months 1..12")
        active_months = set(active_months)
    params = _parameters(method, overrides)
    light_start, light_end = 12-hours/2, 12+hours/2
    light_weights = [max(0, min(h+1,light_end)-max(h,light_start))/hours for h in range(24)]
    annual, monthly, output_daily = defaultdict(lambda: defaultdict(lambda: [0., 0., 0.])), defaultdict(lambda: defaultdict(lambda: [0., 0., 0.])), []
    for row in rows:
        daily_variants = []
        for variant in range(3):
            p = {k: v[variant] for k, v in params.items()}
            solar_mj = row["shortwave"]*p["solar_transmission"]
            natural_dli = solar_mj*.45/.219
            # Adjustable shading maintains the target instead of assuming that
            # unlimited Arctic summer daylight is harmless for every crop.
            shading = min(1., dli/natural_dli) if natural_dli else 1.
            solar_mj *= shading
            artificial_dli = max(0, dli-natural_dli)
            lighting = artificial_dli/(3.6*p["led_umol_j"])
            # Dark-period net radiation is zero; vapour-pressure-driven water
            # loss can remain. Day and night setpoints are stated design targets.
            transpiration = (_canopy_transpiration(target, dli*24/hours, p)*hours/24
                             + _canopy_transpiration(night_target, 0, p)*(24-hours)/24)
            condensate = transpiration*p["condensed_fraction"]
            recovered = condensate*p["condensate_reuse_fraction"]
            dehum = condensate/p["dehumidifier_l_kwh"]
            consumption = transpiration+p["biomass_water_l_m2_day"]
            gross = consumption/(1-p["drainage_fraction"])
            drainage = gross*p["drainage_fraction"]
            fresh = gross-drainage*p["drainage_recovery_fraction"]-recovered
            # Hydraulic pump input rho*g*Q*H/eff, continuous circulation.
            pump_w = 1000*9.80665*(p["pump_flow_l_min_m2"]/60000)*p["pump_head_m"]/p["pump_efficiency"]
            pump = pump_w*24/1000
            fan = p["fan_w_m2"]*24/1000
            heat_coefficient = p["u_w_m2_k"]*p["envelope_area_per_floor_m2"] + 1.2*1006*p["height_m"]*p["air_changes_h"]/3600
            daylight = _daylight_hours(row["date"], p["latitude_deg"])
            solar_shape = [max(0, cos((h+.5-12)*pi/max(daylight, .001))) if abs(h+.5-12) < daylight/2 else 0 for h in range(24)]
            # Daily radiation inconsistent with an ideal polar-night horizon can
            # arise from grid/time conventions: retain its energy, flag via docs.
            if sum(solar_shape) <= 0:
                solar_shape = [1]*24
            solar_sum = sum(solar_shape)
            heat = cooling = envelope_loss = 0.
            peak_electricity = peak_heat = 0.
            for h in range(24):
                outdoor = (row["tmin_c"]+row["tmax_c"])/2 + (row["tmax_c"]-row["tmin_c"])/2*cos(2*pi*(h+.5-14)/24)
                indoor_target = night_target+(target-night_target)*light_weights[h]*hours
                loss = heat_coefficient*(indoor_target-outdoor)/1000
                lamp_hour = lighting*light_weights[h]
                solar_hour = solar_mj/3.6*solar_shape[h]/solar_sum
                # Condensation returns latent heat to the enclosure; only water
                # vapour exhausted outdoors is a net latent heat loss.
                latent_exhaust = (transpiration-condensate)*2.45/3.6/24
                balance = loss+latent_exhaust-solar_hour-lamp_hour-(pump+fan+dehum)/24
                heat += max(0, balance)
                cooling += max(0, -balance)/p["cooling_cop"]
                peak_heat = max(peak_heat, max(0, balance))
                peak_electricity = max(peak_electricity, lamp_hour+(pump+fan+dehum)/24+max(0, -balance)/p["cooling_cop"])
                envelope_loss += max(0, loss)
            electricity = lighting+pump+fan+dehum+cooling
            values = {
                "heat_kwh_th_m2": heat, "electricity_kwh_m2": electricity,
                "equivalent_electricity_kwh_m2": electricity+heat,
                "lighting_kwh_m2": lighting, "pumping_kwh_m2": pump,
                "fans_kwh_m2": fan, "dehumidification_kwh_m2": dehum,
                "cooling_kwh_m2": cooling, "gross_envelope_heat_kwh_th_m2": envelope_loss,
                "transpiration_l_m2": transpiration, "fresh_makeup_m3_m2": fresh/1000,
                "recovered_condensate_m3_m2": recovered/1000,
                "recovered_drainage_m3_m2": drainage*p["drainage_recovery_fraction"]/1000,
                "discharged_drainage_m3_m2": drainage*(1-p["drainage_recovery_fraction"])/1000,
            }
            if active_months is not None and row["date"].month not in active_months:
                values = {k:0. for k in values}
            for k, v in values.items():
                annual[row["date"].year][k][variant] += v
                monthly[(row["date"].year, row["date"].month)][k][variant] += v
            daily_variants.append(values)
            if variant == 1:
                operating=active_months is None or row['date'].month in active_months
                central_peaks = {'peak_electricity_kw_m2':peak_electricity if operating else 0.,'peak_heat_kw_th_m2':peak_heat if operating else 0.}
        output_daily.append({"date": row["date"].isoformat(), **daily_variants[1], **central_peaks})
    years = sorted(annual)
    names = next(iter(annual.values())).keys()
    result = {k: _envelope([sum(annual[y][k][i] for y in years)/len(years) for i in range(3)]) for k in names}
    result.update({
        "model_version": VERSION, "status": "MODELLED_ENGINEERING_SCENARIO", "method": method,
        "normalization": "one_m2_single_layer_growing_area", "aggregation": "mean_annual_selected_operating_days",
        "years": years, "days": len(rows), "active_months": sorted(active_months) if active_months else list(range(1,13)),
        "mean_operating_days": sum(active_months is None or r["date"].month in active_months for r in rows)/len(years),
        "annual": [{"year": y, **{k: _envelope(v) for k, v in annual[y].items()}} for y in years],
        "monthly": [{"month": m, **{k: _envelope([sum(monthly[(y,m)][k][i] for y in years)/len(years) for i in range(3)]) for k in names}} for m in range(1,13)],
        "monthly_configurations": [{"month": m, **{k: [sum(monthly[(y,m)][k][i] for y in years)/len(years) for i in range(3)] for k in names}} for m in range(1,13)],
        "daily": output_daily,
        "water_monthly_m3_m2": [sum(monthly[(y,m)]["fresh_makeup_m3_m2"][1] for y in years)/len(years) for m in range(1,13)],
        "parameters": params,
        "setpoints": {"target_temp_c": target, "target_temp_c_night": night_target, "dli_mol_m2_day": dli, "photoperiod_h": hours, "maximum_supplemental_ppfd_umol_m2_s": dli*1e6/(hours*3600)},
        "range_meaning": "Envelope of three declared engineering configurations; not a statistical confidence interval or exhaustive independent-parameter bound",
        "equivalent_electricity_definition": "electricity + heat/COP with reference COP=1; not local supply, tariff or measured system efficiency",
        "sources": [FAO, "https://www.purdue.edu/hla/sites/cea/article/calculating-greenhouse-heating-requirements/", "https://fieldreport.caes.uga.edu/wp-content/uploads/2025/08/B-792_6.pdf", "https://www.energystar.gov/products/dehumidifiers/key_efficiency_criteria"],
        "limitations": [
            "Building geometry, indoor insulation, resistance/humidity, drainage, pumps and condensate reuse are visible uncalibrated design scenarios.",
            "Hourly air temperature/radiation/light schedules are reconstructed from daily climate, not measured hourly weather.",
            "Bulk canopy Penman-Monteith is a water sensitivity model; no crop-specific resistance calibration or staged canopy growth is claimed.",
            "Heat gains, sensible envelope loss, vapour exhaust and condensation are balanced approximately; no validated building simulator, foundation/ground loss, snow load or heat-distribution losses.",
            "Condensate reuse assumes suitable treatment; nutrient dosing, sanitation, cleaning/changeover losses and material chemistry need pilot measurement.",
            "Inactive months mean no growing operation or water use; idle-building freeze protection/standby energy is not included.",
            "No available land, municipal agricultural water right, grid capacity, price, crop profit or future yield is inferred.",
        ],
    })
    return result


def recirculation_makeup(gross_irrigation_m3, drainage_fraction, recovered_fraction):
    gross = _number(gross_irrigation_m3, "gross_irrigation_m3", 0)
    drain = _number(drainage_fraction, "drainage_fraction", 0, 1)
    recovery = _number(recovered_fraction, "recovered_fraction", 0, 1)
    reused = gross*drain*recovery
    return {"gross_irrigation_m3": gross, "makeup_m3": gross-reused, "reused_m3": reused,
            "discharged_m3": gross*drain*(1-recovery), "consumptive_m3": gross*(1-drain),
            "accounting": "Reused drainage reduces makeup once; it is not an independent freshwater source."}


def roof_storage_balance(daily, demand_m3, roof_m2=1., storage_m3=.1,
                         collection_efficiency=.8, initial_storage_m3=0.,
                         melt_factor_mm_c_day=3., initial_snow_mm=0.):
    """Chronological snow-equivalent roof capture and finite-tank mass balance.

    At Tmean<=0 precipitation enters snowpack; melt=min(SWE,DDF*positive T).
    Capture occurs after melting. Same-day captured water first serves demand,
    then fills the tank; surplus spills. This explicit within-day ordering is a
    screening assumption. Physical demand may be any nonnegative daily sequence.
    """
    rows = _records(daily, precipitation=True, contiguous=True)
    demand = [_number(v, "demand_m3", 0) for v in demand_m3]
    if len(demand) != len(rows):
        raise ValueError("One daily demand value is required per climate date")
    roof = _number(roof_m2, "roof_m2", 0)
    capacity = _number(storage_m3, "storage_m3", 0)
    efficiency = _number(collection_efficiency, "collection_efficiency", 0, 1)
    stock = _number(initial_storage_m3, "initial_storage_m3", 0, capacity)
    snow = _number(initial_snow_mm, "initial_snow_mm", 0)
    melt_factor = _number(melt_factor_mm_c_day, "melt_factor_mm_c_day", 0, 10)
    daily_out, monthly = [], defaultdict(lambda: defaultdict(float))
    totals = defaultdict(float)
    for row, need in zip(rows, demand):
        temp = (row["tmin_c"]+row["tmax_c"])/2
        snowfall = row["precip"] if temp <= 0 else 0.
        rain = row["precip"]-snowfall
        snow += snowfall
        melt = min(snow, max(0, temp)*melt_factor)
        snow -= melt
        captured = (rain+melt)*roof/1000*efficiency
        available = stock+captured
        supplied = min(need, available)
        stock = min(capacity, available-supplied)
        spill = max(0, available-supplied-capacity)
        values = {"precipitation_m3": row["precip"]*roof/1000, "captured_m3": captured,
                  "supplied_m3": supplied, "deficit_m3": need-supplied, "spill_m3": spill,
                  "demand_m3": need, "liquid_uncollected_m3": (rain+melt)*roof/1000*(1-efficiency)}
        for k, v in values.items():
            totals[k] += v
            monthly[(row["date"].year, row["date"].month)][k] += v
        daily_out.append({"date": row["date"].isoformat(), **values, "storage_m3": stock, "snowpack_mm": snow, "snowfall_mm": snowfall, "melt_mm": melt})
    years = sorted({r["date"].year for r in rows})
    names = list(totals)
    totals.update({"final_storage_m3": stock, "final_snow_mm": snow,
                   "storage_balance_residual_m3": initial_storage_m3+totals["captured_m3"]-totals["supplied_m3"]-totals["spill_m3"]-stock,
                   "precipitation_balance_residual_m3": initial_snow_mm*roof/1000+totals["precipitation_m3"]-totals["captured_m3"]-totals["liquid_uncollected_m3"]-snow*roof/1000})
    return {"model_version": VERSION, "status": "MODELLED_ENGINEERING_SCENARIO", "totals": dict(totals),
            "daily": daily_out, "monthly": [{"year": y, "month": m, **dict(v)} for (y,m),v in sorted(monthly.items())],
            "mean_annual": {k: totals[k]/len(years) for k in names},
            "climatology_monthly": [{"month": m, **{k: sum(monthly[(y,m)][k] for y in years)/len(years) for k in names}} for m in range(1,13)],
            "parameters": {"roof_m2": roof, "storage_m3": capacity, "collection_efficiency": efficiency, "initial_storage_m3": initial_storage_m3, "initial_snow_mm": initial_snow_mm, "melt_factor_mm_c_day": melt_factor, "phase_threshold_c": 0},
            "sources": ["https://www.twdb.texas.gov/innovativewater/rainwater/faq.asp", "https://www.hec.usace.army.mil/confluence/hmsdocs/hmstrm/snow-accumulation-and-melt/temperature-index-method"],
            "limitations": ["Roof and tank are explicit engineering sizes, not discovered local infrastructure.", "Temperature-index snow bucket omits roof heat, wind redistribution, refreezing, sublimation and ice blockage; DDF is not calibrated in Svalbard.", "Collection efficiency comes from a non-Arctic system range, not guaranteed cold-roof performance.", "Chronological balance is computed before climatological averaging; monthly averages alone do not establish daily reliability.", "Captured water needs quality assessment/treatment; capture is not automatically usable irrigation water."]}


def _osmotic_pressure_bar(salinity, temperature):
    """Published seawater osmotic-coefficient correlation (Sharqawy et al. 2010).

    S in g/kg reference-composition mass salinity, T 0..200°C, S<=120.
    Equations transcribed, not a PSU-to-mass-salinity conversion. Low S uses the
    continuous dilute extension documented by the MIT seawater property library.
    """
    s, t = salinity, temperature
    if not 0 <= s <= 120 or not 0 <= t <= 200:
        raise ValueError("Osmotic correlation requires 0..120 g/kg, 0..200°C")
    a = [.89453233003, .00041560737424, -4.6262121398e-6, 2.2211195897e-11, -.00011445456438, -1.4783462366e-6, -1.3526263499e-11, 7.0132355546e-6, 5.6960486681e-8, -2.8624032584e-10]
    def phi(x):
        return a[0]+a[1]*t+a[2]*t*t+a[3]*t**4+a[4]*x+a[5]*t*x+a[6]*x*t**3+a[7]*x*x+a[8]*x*x*t+a[9]*x*x*t*t
    coefficient = phi(s)
    if s < 10:
        m10 = 10/990*31.843280
        dm = 31.843280*(1/990+10/990**2)
        derivative = a[4]+a[5]*t+a[6]*t**3+20*a[7]+20*a[8]*t+20*a[9]*t*t
        beta = -2*((phi(10)-1)/sqrt(m10)-derivative*sqrt(m10)/dm)
        lam = (phi(10)+beta*sqrt(m10)-1)/m10
        m = s/(1000-s)*31.843280
        coefficient = 1-beta*sqrt(m)+lam*m
    rho_w = 999.92293295+.020341179217*t-.0061624591598*t*t+.000022614664708*t**3-4.6570659168e-8*t**4
    molality = 1000*s/((1000-s)*31.4038218)
    return 8.3144598*coefficient*molality*(t+273.15)*rho_w/1e5


def ro_treatment(salinity_g_kg, temperature_c, recovery=.45, product_water_m3=1., overrides=None):
    """Single-pass SWRO screening with salinity/temperature/recovery sensitivity.

    Source T below 0°C is conditioned to 0°C; sensible heat is reported separately.
    Membrane choice/chemistry are unresolved, so successful numeric calculation
    means 'conditional', never a permit or guaranteed water quality/capacity.
    """
    s = _number(salinity_g_kg, "mass_salinity_g_kg", 0, 45)
    t = _number(temperature_c, "in_situ_temperature_c", -2.5, 40)
    r = _number(recovery, "recovery", .1, .65)
    volume = _number(product_water_m3, "product_water_m3", 0)
    params = {"ndp_25c_bar": [5.,10.,15.], "pump_efficiency": [.85,.8,.75],
              "erd_efficiency": [.98,.95,.9], "pressure_drop_bar": [1.,2.,3.],
              "auxiliary_kwh_m3": [.2,.4,.8], "max_pressure_bar": [83.,83.,83.],
              "minimum_process_c": [0.,0.,0.]}
    for k,v in (overrides or {}).items():
        if k not in params:
            raise ValueError(f"Unknown RO parameter {k}")
        vals = list(v) if isinstance(v,(list,tuple)) else [v]*3
        if len(vals) != 3:
            raise ValueError("RO range must contain three configurations")
        params[k] = [_number(x,k,0) for x in vals]
    for k in ["pump_efficiency","erd_efficiency"]:
        if max(params[k]) > 1 or (k == "pump_efficiency" and min(params[k]) <= 0):
            raise ValueError("Invalid efficiency")
    if max(params["minimum_process_c"]) > 40:
        raise ValueError("Process conditioning temperature >40°C unsupported")
    brine_s = s/(1-r)
    if brine_s > 120:
        raise ValueError("Brine exceeds osmotic correlation range")
    energies, pressures, conditioning, feasible, process = [],[],[],[],[]
    for i in range(3):
        pt = max(t,params["minimum_process_c"][i])
        process.append(pt)
        # DuPont Rev20 August2026 Eqs73/74 use 298 and 273 exactly.
        tcf = exp((3020 if pt <= 25 else 2640)*(1/298-1/(273+pt)))
        pressure = _osmotic_pressure_bar(brine_s,pt)+params["ndp_25c_bar"][i]/tcf+params["pressure_drop_bar"][i]
        sec = pressure/(36*params["pump_efficiency"][i])*(1-params["erd_efficiency"][i]*(1-r))/r+params["auxiliary_kwh_m3"][i]
        energies.append(sec)
        pressures.append(pressure)
        conditioning.append(1000*4.0*(pt-t)/(3600*r))
        feasible.append(pressure <= params["max_pressure_bar"][i])
    return {"model_version":VERSION, "status":"CONDITIONAL" if feasible[1] else "PRESSURE_LIMIT_EXCEEDED",
            "input_definitions":{"salinity":"mass_salinity_g_kg_reference_composition","temperature":"in_situ_c"},
            "salinity_g_kg":s,"temperature_c":t,"recovery":r,"process_temperature_c":_envelope(process),
            "specific_energy_kwh_m3":_envelope(energies),"electricity_kwh":_envelope([v*volume for v in energies]),
            "pressure_bar":_envelope(pressures),"pressure_feasible_by_configuration":feasible,
            "conditioning_heat_kwh_th_m3":_envelope(conditioning),"conditioning_heat_kwh_th":_envelope([v*volume for v in conditioning]),
            "feed_water_m3":volume/r,"product_water_m3":volume,"brine_water_m3":volume*(1-r)/r,"brine_salinity_g_kg":brine_s,
            "salt_balance_approximation":"Equal-density incompressible volume balance with zero-salt permeate; not detailed ion rejection or a brine discharge design",
            "temperature_regime":"conditioned_to_zero" if t<0 else ("cold_membrane_validation_required" if t<5 else "manufacturer_correlation_scenario"),
            "liquid_phase_and_freeze_protection_validation_required":t<5,
            "parameters":params,"sources":[MIT,DUPONT],
            "limitations":["NDP, pump/ERD efficiencies, auxiliary pretreatment energy and pressure drop are declared design ranges; no selected installed membrane or Arctic pilot exists.","Subzero source water is not extrapolated through a warm-water-only correlation: explicit heating to at least 0°C is required, with freeze protection still unresolved. Only sensible liquid-water heat is included, not sea-ice melting; source liquid phase requires verification.","Manufacturer temperature correction is a permeability sensitivity, not proof of cold-water membrane suitability.","Boron, specific ions, organics, turbidity, fouling, scaling, disinfection, remineralisation/nutrient conditioning and brine permits require laboratory/design work.","Mass salinity g/kg is not Practical Salinity/PSU; no silent conversion is permitted.","Pressure-limit failure is reported, not silently clamped; heat remains separate from electricity."]}


def model_profile_provenance(metadata, points):
    """Validate a real numeric model profile contract; never create a fake cast.

    Preserves native temperature/salinity definitions. Only in-situ temperature
    and mass salinity are eligible for this RO routine without a documented
    thermodynamic conversion; even then spatial/temporal field matching is a
    separate gate owned by the field-comparison layer.
    """
    required = ["product_id","dataset_id","dataset_version","source_url","license","sha256",
                "time_start_utc","time_end_utc","aggregation","requested_position","grid_position",
                "horizontal_resolution_km","vertical_coordinate","temperature_kind","salinity_kind",
                "temperature_unit","salinity_unit","dimensions","dimensions_verified","retrieved_at_utc"]
    missing = [k for k in required if k not in metadata or metadata[k] is None or metadata[k] == ""]
    if missing:
        raise ValueError("Missing model-profile metadata: "+", ".join(missing))
    if not re.fullmatch(r"[0-9a-fA-F]{64}",str(metadata["sha256"])):
        raise ValueError("Real downloaded-file SHA256 required")
    if metadata["dimensions_verified"] is not True or "depth" not in metadata["dimensions"]:
        raise ValueError("Verify the downloaded variable's depth dimension; a surface pixel is not a profile")
    if metadata["aggregation"] not in {"instantaneous","daily_mean","monthly_mean"}:
        raise ValueError("Explicit supported temporal aggregation required")
    def utc(value):
        parsed = datetime.fromisoformat(value.replace("Z","+00:00"))
        if parsed.utcoffset() is None or parsed.utcoffset().total_seconds() != 0:
            raise ValueError("Explicit UTC time required")
        return parsed
    if utc(metadata["time_start_utc"]) > utc(metadata["time_end_utc"]):
        raise ValueError("Invalid model averaging time window")
    utc(metadata["retrieved_at_utc"])
    for key in ["requested_position","grid_position"]:
        _number(metadata[key].get("latitude"),key+" latitude",-90,90)
        _number(metadata[key].get("longitude"),key+" longitude",-180,180)
    _number(metadata["horizontal_resolution_km"],"horizontal_resolution_km",0)
    if metadata["temperature_kind"] not in {"in_situ","potential","conservative"} or metadata["temperature_unit"] != "degC":
        raise ValueError("Explicit recognized temperature definition/unit required")
    units = {"mass_salinity":"g/kg","practical_salinity":"1","model_sea_water_salinity":"1e-3"}
    if units.get(metadata["salinity_kind"]) != metadata["salinity_unit"]:
        raise ValueError("Salinity kind/unit mismatch; PSU is not mass salinity")
    values, last = [], -1.
    for point in points:
        depth = _number(point.get("depth_m"),"depth_m",0)
        if depth <= last:
            raise ValueError("Distinct strictly increasing profile depths required")
        last = depth
        values.append({"depth_m":depth,"temperature_c":_number(point.get("temperature_c"),"temperature_c",-5,45),"salinity":_number(point.get("salinity"),"salinity",0,120)})
    if len(values) < 2:
        raise ValueError("At least two actual depth samples required; do not clone surface values")
    compatible = metadata["temperature_kind"] == "in_situ" and metadata["salinity_kind"] == "mass_salinity"
    return {"status":"SOURCED_MODEL_PROFILE","metadata":dict(metadata),"points":values,
            "ro_definition_compatible":compatible,"field_matching_required":True,
            "comparison_note":"A time-averaged model grid profile is not an instantaneous ship cast; resolve representativeness and thermodynamic definitions before updating the same decision engine."}
