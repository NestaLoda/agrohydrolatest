"""Small explicit physical calculations; absent evidence is never zero."""
import math
import numpy as np

FAO56 = "https://www.fao.org/4/X0490E/x0490e0b.htm"
FAO56_HARGREAVES = "https://www.fao.org/4/X0490E/x0490e07.htm"
TEMPERATURE_SCENARIO_LIMITATIONS = [
    'FAO-56 Denklem 52 sıcaklık teriminden türetilen oran kaynak ET0 üzerine uygulanır; tam Penman–Monteith yeniden hesabı veya kalibre edilmiş iklim projeksiyonu değildir.',
    'Günlük Tmin ve Tmax aynı farkla kayar; gün içi sıcaklık aralığı ve dünya dışı radyasyon sabit varsayılır. Nem, rüzgâr ve radyasyon değişimi hesaplanmaz.',
    'Ürün verimi, gelişim takvimi, Kc, don/ısı hasarı ve kar erimesi bu sıcaklık senaryosuyla değiştirilmez; yerel duyarlılık doğrulaması gereklidir.',
]
RO_SOURCE = "https://doi.org/10.1016/j.dwt.2025.101157"


def temperature_scenario_et0(et0_mm, tmin_c, tmax_c, temperature_delta_c):
    """Apply only the Eq.52 temperature-term ratio to existing source ET0.

    This ratio is our uncalibrated scenario derivation, not a FAO-endorsed
    adjustment of Penman–Monteith ET0. Zero delta preserves source values even
    where temperature is absent; nonzero delta must never fill missing data.
    """
    et0 = np.asarray(et0_mm, dtype=float)
    if et0.ndim != 1 or not len(et0) or not np.isfinite(et0).all() or np.any(et0 < 0):
        raise ValueError('DATA_NEEDED: kaynak ET0 serisi eksik, negatif veya geçersiz.')
    delta = float(temperature_delta_c)
    if not math.isfinite(delta) or not -3 <= delta <= 6:
        raise ValueError('Sıcaklık farkı -3 ile +6 °C arasında sonlu olmalı.')
    meta = {
        'temperature_delta_c': delta,
        'classification': 'DERIVED_TEMPERATURE_SENSITIVITY_SCENARIO' if delta else 'SOURCE_ET0_UNCHANGED',
        'method': 'FAO56_EQ52_TEMPERATURE_TERM_RATIO' if delta else 'SOURCE_ET0_UNCHANGED',
        'applied': delta != 0,
        'source_url': FAO56_HARGREAVES,
        'source_equation': 52,
        'formula': 'ET0_scenario = ET0_source × max(Tmean + delta_C + 17.8, 0) / (Tmean + 17.8); Tmean = (Tmin + Tmax) / 2',
        'ratio_is_project_scenario_derivation': True,
        'locally_validated': False,
        'limitations': TEMPERATURE_SCENARIO_LIMITATIONS.copy(),
    }
    if delta == 0:
        return et0.copy(), {**meta, 'factor_min': 1., 'factor_max': 1., 'factor_mean': 1., 'clamped_numerator_days': 0}
    lo, hi = np.asarray(tmin_c, dtype=float), np.asarray(tmax_c, dtype=float)
    if lo.shape != et0.shape or hi.shape != et0.shape or not np.isfinite(lo).all() or not np.isfinite(hi).all() or np.any(lo > hi):
        raise ValueError('DATA_NEEDED: sıcaklık farkı için kaynak günlük Tmin/Tmax eksiksiz, sonlu ve sıralı olmalı.')
    mean = (lo + hi) / 2
    denominator = mean + 17.8
    if np.any(denominator <= 0):
        raise ValueError('DATA_NEEDED: Tmean + 17,8 ≤ 0 günlerinde sıcaklık-terimi oranı uygulanamaz; farklı doğrulanmış ET0 yöntemi gerekli.')
    numerator = np.maximum(mean + delta + 17.8, 0)
    factors = numerator / denominator
    adjusted = et0 * factors
    if not np.isfinite(adjusted).all():
        raise ValueError('DATA_NEEDED: sıcaklık senaryosu sonlu ET0 üretemedi.')
    return adjusted, {**meta, 'factor_min': float(factors.min()), 'factor_max': float(factors.max()),
        'factor_mean': float(factors.mean()), 'clamped_numerator_days': int(np.sum(mean + delta + 17.8 < 0)),
        'source_mean_temperature_c': float(mean.mean()), 'scenario_mean_temperature_c': float(mean.mean() + delta)}

def nonnegative(value, name):
    if value is None or not math.isfinite(float(value)) or value < 0:
        raise ValueError(f"{name}: sonlu ve negatif olmayan sayı gerekli.")
    return float(value)

def mm_to_m3(mm: float, area_ha: float) -> float:
    return nonnegative(mm, "mm") * nonnegative(area_ha, "ha") * 10

def kj_to_kwh(kj: float) -> float:
    return nonnegative(kj, "kJ") / 3600

def climate_metrics(tmin, tmax, base=5.0):
    lo, hi = np.asarray(tmin, dtype=float), np.asarray(tmax, dtype=float)
    if len(lo) == 0 or lo.shape != hi.shape or not np.isfinite(lo).all() or not np.isfinite(hi).all():
        raise ValueError("İklim serisi boş, eşleşmiyor veya eksik değer içeriyor.")
    if np.any(lo > hi):
        raise ValueError("Tmin Tmax'tan büyük olamaz.")
    longest = current = 0
    for value in lo:
        current = current + 1 if value > 0 else 0
        longest = max(longest, current)
    return {"gdd_base5_c_days": float(np.maximum((lo+hi)/2-base, 0).sum()), "gdd_base_C": base,
            "frost_free_longest_days": longest, "mean_temperature_C": float(((lo+hi)/2).mean())}

def kc_curve(initial=0.7):
    """FAO56 illustrative Mediterranean winter wheat: 30/140/40/30 days."""
    return np.r_[np.full(30, initial), np.linspace(initial, 1.15, 140), np.full(40, 1.15), np.linspace(1.15, 0.25, 30)]

def water_balance(precipitation_mm, et0_mm, kc, capacity_mm=60, initial_mm=30):
    p, e, k = (np.asarray(v, dtype=float) for v in (precipitation_mm, et0_mm, kc))
    if not (len(p) and p.shape == e.shape == k.shape):
        raise ValueError("Su dengesi serilerinin boyutu eşleşmeli.")
    if not all(np.isfinite(v).all() and np.all(v >= 0) for v in (p, e, k)):
        raise ValueError("Su dengesinde eksik/negatif değer sıfırla doldurulamaz.")
    capacity, storage = nonnegative(capacity_mm,"kapasite"), nonnegative(initial_mm,"ilk stok")
    if storage > capacity:
        raise ValueError("İlk stok kapasiteyi aşamaz.")
    rows=[]
    for rain, et0, coeff in zip(p,e,k):
        start=storage
        drainage=max(0.0,storage+rain-capacity)
        available=min(capacity,storage+rain)
        demand=float(et0*coeff)
        actual=min(available,demand)
        storage=available-actual
        rows.append({"start_storage_mm":start,"precipitation_mm":float(rain),"potential_et_mm":demand,
                     "actual_et_mm":actual,"deficit_mm":demand-actual,"drainage_mm":drainage,"storage_mm":storage})
    totals={key:sum(row[key] for row in rows) for key in ("precipitation_mm","potential_et_mm","actual_et_mm","deficit_mm","drainage_mm")}
    totals.update(initial_storage_mm=float(initial_mm),final_storage_mm=float(storage),capacity_mm=float(capacity),
                  deficit_m3_per_ha=mm_to_m3(totals["deficit_mm"],1))
    return {"totals":totals,"daily":rows,"method":"rainfed_single_bucket_v1",
            "limitation":"Toplam yağış (karın su eşdeğeri dahil) aynı gün depoya girer; kar birikimi/erimesi modellenmedi. Sulamasız standart deneydir; drenaj çekilebilir su arzı değildir. Yeraltı suyu ve yerel toprak kalibrasyonu yok."}

def suitability(climate: bool | None, soil: bool | None, method="open_field"):
    if method != "open_field":
        return {"status":"conditional","reason":"Kontrollü üretimde dış ortam/zemin filtresi yerine enerji ve altyapı koşulları değerlendirilir."}
    if climate is False or soil is False:
        return {"status":"unsuitable","reason":"Açık tarla için seçilen iklim veya zemin koşulu sağlanmıyor."}
    if climate is None or soil is None:
        return {"status":"insufficient_data","reason":"Yerel gelecek iklimi ve/veya zemin uygunluğu doğrulanmadı."}
    return {"status":"conditional","reason":"İklim/zemin uygunluğu kullanıcı senaryo varsayımı; yerel doğrulama yok."}

def treatment_energy(temperature_c, salinity_sp=35, margin=0.15):
    if not math.isfinite(temperature_c) or not math.isfinite(salinity_sp):
        raise ValueError("Sonlu sıcaklık ve tuzluluk gerekli.")
    base={"source_url":RO_SOURCE,"classification":"SIMULATION / EXPLANATORY", "temperature_C":temperature_c,
          "salinity_sp":salinity_sp,"salinity_used_in_energy_model":False,
          "method":"5 ve 18°C literatür uçları arasında açıklayıcı doğrusal interpolasyon; ± senaryo payı",
          "margin_fraction":margin,"margin_is_statistical_confidence":False,
          "limitation":"Arktik'te kalibre değil. Tuzluluk etkisi bu ilk modelde sayısallaştırılmadı; su kalitesi/geri kazanım ayrı varsayım."}
    if not 5 <= temperature_c <= 18:
        return {**base,"status":"insufficient_data","specific_energy_kwh_m3":None,"interval_kwh_m3":None,
                "reason":"Kaynaklı 5–18°C aralığı dışında extrapolasyon yapılmadı; uzman/teknoloji verisi gerekli."}
    estimate=10.5+(temperature_c-5)/(18-5)*(6.7-10.5)
    return {**base,"status":"conditional","specific_energy_kwh_m3":estimate,
            "interval_kwh_m3":[estimate*(1-margin),estimate*(1+margin)],
            "reason":"Tek deneysel düzeneğin uçlarına dayanan duyarlılık hesabı; evrensel kWh/m³ veya güven aralığı değil."}
