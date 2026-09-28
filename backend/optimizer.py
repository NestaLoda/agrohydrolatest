"""Transparent HiGHS LP: same-crop production with water and energy budgets."""
import numpy as np
from scipy.optimize import linprog
from .contracts import DecisionRequest, ProductionSystemPattern, MODEL_VERSION
from .science import suitability, treatment_energy, kj_to_kwh

LETTUCE_SOURCE="https://pmc.ncbi.nlm.nih.gov/articles/PMC4483736/"

def solve_decision(request: DecisionRequest):
    r=request
    treatment=treatment_energy(r.seawater_temperature_c,r.seawater_salinity_psu,r.energy_margin_fraction)
    # Arizona literature transfer: not a local Arctic yield/energy calibration.
    options=[]
    for method,water,energy in [("open_field",0.250,kj_to_kwh(1100)),("hydroponics",0.020,kj_to_kwh(90000))]:
        screen=suitability(r.open_field_climate_suitable,r.soil_suitable,method)
        for source in ["freshwater","desalinated_seawater"]:
            label=("Açık tarla" if method=="open_field" else "Hidroponik")+" · "+("yerel tatlı su" if source=="freshwater" else "arıtılmış deniz suyu")
            status,reason=screen["status"],screen["reason"]
            sec=0.0
            if source=="desalinated_seawater":
                if treatment["status"]=="insufficient_data":
                    if status!="unsuitable":status="insufficient_data"
                    reason+=" "+treatment["reason"]
                else:
                    sec=treatment["interval_kwh_m3"][1]
                    reason+=" Arıtma enerjisi senaryo aralığının üst ucuyla sınırlandı."
            options.append({"id":method+"_"+source,"label":label,"method":method,"water_source":source,
                "status":status,"reason":reason,"water_m3_per_kg":water,
                "energy_kwh_per_kg":None if source=="desalinated_seawater" and treatment["status"]=="insufficient_data" else energy+water*sec,
                "classification":"SIMULATION / EXPLANATORY"})
    eligible=[o for o in options if o["status"]=="conditional"]
    def run(objective):
        n=len(eligible)
        if not n:return None
        water=np.array([o["water_m3_per_kg"] for o in eligible])
        fresh=water*np.array([o["water_source"]=="freshwater" for o in eligible])
        desal=water-fresh
        energy=np.array([o["energy_kwh_per_kg"] for o in eligible])
        c=energy if objective=="energy" else fresh
        result=linprog(c,A_ub=np.array([fresh,desal,energy,np.ones(n)]),
             b_ub=[r.freshwater_capacity_m3,r.desalination_capacity_m3,r.energy_budget_kwh,r.production_capacity_kg],
             A_eq=np.ones((1,n)),b_eq=[r.output_target_kg],bounds=[(0,None)]*n,method="highs")
        if not result.success:return None
        return result.x
    solution=run("energy")
    allocations=[]
    pattern=[]
    totals={"production_kg":0.0,"freshwater_m3":0.0,"desalinated_water_m3":0.0,"feed_seawater_m3":0.0,"energy_kwh":0.0}
    if solution is not None:
        for o,x in zip(eligible,solution):
            if x<1e-8:continue
            w,e=float(x*o["water_m3_per_kg"]),float(x*o["energy_kwh_per_kg"])
            allocations.append({"option_id":o["id"],"label":o["label"],"production_kg":float(x),"share_pct":float(x/r.output_target_kg*100),"water_m3":w,"energy_kwh":e})
            pattern.append(ProductionSystemPattern(production_method=o["method"],water_source=o["water_source"],production_kg=float(x),production_share_fraction=min(1.0,float(x/r.output_target_kg)),water_m3=w,energy_kwh=e).model_dump())
            totals["production_kg"]+=float(x)
            totals["energy_kwh"]+=e
            totals["freshwater_m3" if o["water_source"]=="freshwater" else "desalinated_water_m3"]+=w
        totals["feed_seawater_m3"]=totals["desalinated_water_m3"]/r.recovery_fraction
    pareto=[]
    for objective in ["energy","freshwater"]:
        x=run(objective)
        pareto.append({"objective":objective,"status":"conditional" if x is not None else "unsuitable",
                      "energy_kwh":None if x is None else float(sum(v*o["energy_kwh_per_kg"] for o,v in zip(eligible,x))),
                      "freshwater_m3":None if x is None else float(sum(v*o["water_m3_per_kg"] for o,v in zip(eligible,x) if o["water_source"]=="freshwater"))})
    status="conditional" if solution is not None else ("insufficient_data" if not eligible else "unsuitable")
    constraints=[]
    for key,label,unit,capacity,used in [
        ("freshwater","Tatlı su","m³",r.freshwater_capacity_m3,totals["freshwater_m3"]),
        ("desalinated_water","Arıtılmış ürün suyu","m³",r.desalination_capacity_m3,totals["desalinated_water_m3"]),
        ("energy","Enerji","kWh",r.energy_budget_kwh,totals["energy_kwh"]),
        ("production","Üretim kapasitesi","kg",r.production_capacity_kg,totals["production_kg"])]:
        slack=capacity-used if solution is not None else None
        constraints.append({"id":key,"label":label,"unit":unit,"capacity":capacity,
             "used":used if solution is not None else None,"slack":slack,
             "binding":None if slack is None else abs(slack)<=max(1e-6,abs(capacity)*1e-8)})
    maximum=None
    if eligible:
        water=np.array([o["water_m3_per_kg"] for o in eligible])
        fresh=water*np.array([o["water_source"]=="freshwater" for o in eligible])
        energy=np.array([o["energy_kwh_per_kg"] for o in eligible])
        max_result=linprog(-np.ones(len(eligible)),A_ub=np.array([fresh,water-fresh,energy,np.ones(len(eligible))]),
            b_ub=[r.freshwater_capacity_m3,r.desalination_capacity_m3,r.energy_budget_kwh,r.production_capacity_kg],bounds=[(0,None)]*len(eligible),method="highs")
        if max_result.success:maximum=float(max_result.x.sum())
    binding=[c["label"] for c in constraints if c["binding"]]
    explanation={"preferred":" + ".join(f"{a['label']}: {a['production_kg']:.0f} kg" for a in allocations) if allocations else "Bu koşullarda hedefi sağlayan plan yok.",
        "why":"Aynı üretim hedefi ve seçilen seçenekler içinde toplam enerjiyi en aza indiren çözüm; maliyet/ekoloji için genel üstünlük iddiası değil.",
        "why_not":[{"id":o["id"],"label":o["label"],"reason":o["reason"] if o["status"]!="conditional" else ("Hedef/bütçeler altında daha düşük enerji sağlayan bileşim seçildi; eşdeğer alternatifler olabilir." if not any(a["option_id"]==o["id"] for a in allocations) else "Çözümde kullanılıyor.")} for o in options],
        "binding_constraints":binding,
        "binding_definition":"Bağlayıcı: optimumda kalan kapasite sıfıra yakın. Bu, tek başına kaynak artışının mutlaka fayda sağlayacağını kanıtlamaz."}
    return {"status":status,"crop":"Marul","classification":"SIMULATION / EXPLANATORY","model_version":MODEL_VERSION,
       "region_id":r.region_id,"scenario_id":r.scenario_id,"period":"2071–2100 — dış literatür bağlamı",
       "allocations":allocations,"production_system_pattern":pattern,"totals":totals if solution is not None else None,"options":options,"frontier":options,"pareto":pareto,
       "treatment":treatment,
       "constraints":constraints,"explanation":explanation,
       "failure_diagnostics":{"max_supported_production_kg":maximum,"target_shortfall_kg":None if maximum is None else max(0,r.output_target_kg-maximum),
         "scope":"Yalnız değerlendirmeye alınabilen yöntemler ve beyan edilen bütçeler; gerçek çiftlik kapasitesi değil."},
       "reasons":["Belirtilen varsayımsal bütçeler altında uygulanabilir üretim bileşimi bulundu." if solution is not None else "Verilen veri ve bütçelerle hedefi sağlayan plan bulunamadı.",
                  "SSP seçimi dış literatür bağlamını değiştirir; yerel gelecek sıcaklığı veya verimi uydurularak optimizasyona aktarılmaz."],
       "assumptions":["Ürün hedefi, su/enerji/üretim kapasitesi ve geri kazanım kullanıcı senaryosudur; yerel ölçüm değildir.",
          "Marul su/enerji katsayıları Arizona kaynaklı karşılaştırmadan aktarılmıştır; Arktik ısıtma/ışık kalibrasyonu yoktur.",
          "Hidroponik 20 L/kg ve 25 kWh/kg; açık tarla 250 L/kg ve 1100/3600 kWh/kg kaynak değerleri.",
          "Yalnız aynı ürünün kilogramı karşılaştırılır. Su kaynağının hedef kaliteyi arıtma sonrası sağladığı senaryo varsayımıdır.",
          "Bu çözüm seçilen üretim dönemi için toplam kapasite hesabıdır; çok dönemli depolama veya yerel yıllık su güvenliği doğrulaması değildir.",
          "Toprak/permafrost ve yerel gelecek iklimi bilinmiyorsa açık tarla uygun sayılmaz.",
          "Arıtma enerji aralığı istatistiksel güven aralığı değildir; tuzluluk etkisi henüz kalibre edilmedi."],
       "sources":[{"label":"Barbosa vd. 2015 — Arizona marul karşılaştırması","url":LETTUCE_SOURCE},{"label":"RO sıcaklık deneyi 2025","url":treatment["source_url"]}],
       "solver":{"name":"SciPy linprog / HiGHS","objective":"minimize_energy","units":"kg, m³, kWh","success":solution is not None}}
