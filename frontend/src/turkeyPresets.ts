import type { SimulationRequest } from './planning'

// Explicit what-if conditions, not probabilities or regional forecasts.
export const turkeyPresets = [
  {id:'reference',label:'Mevcut',icon:'reset',detail:'ΔT 0°C · yağış %0',temperature:0,rain:1,water:1,efficiency:0},
  {id:'warming',label:'Isınan sezon',icon:'sun',detail:'Sıcaklık +1°C',temperature:1,rain:1,water:1,efficiency:0},
  {id:'dryrain',label:'Azalan yağış',icon:'rain',detail:'Yağış −%20',temperature:0,rain:.8,water:1,efficiency:0},
  {id:'drought',label:'Sıcak ve kurak',icon:'sun',detail:'+2°C · yağış −%20',temperature:2,rain:.8,water:1,efficiency:0},
  {id:'water20',label:'Su kısıntısı',icon:'water',detail:'Su sınırı −%20',temperature:0,rain:1,water:.8,efficiency:0},
  {id:'rainy',label:'Yağışlı sezon',icon:'rain',detail:'Yağış +%20',temperature:0,rain:1.2,water:1,efficiency:0},
  {id:'coolwet',label:'Serin ve yağışlı',icon:'snow',detail:'−1°C · yağış +%10',temperature:-1,rain:1.1,water:1,efficiency:0},
  {id:'efficient',label:'Verimli sulama',icon:'sprinkler',detail:'Sulama verimi +10 puan',temperature:0,rain:1,water:1,efficiency:.1},
  {id:'ideal',label:'İyi koşullar',icon:'seed',detail:'Yağış +%10 · sulama verimi %95',temperature:0,rain:1.1,water:1,efficiency:0},
]

export function presetScenario(base:SimulationRequest,id:string,current:SimulationRequest=base):SimulationRequest {
  const p=turkeyPresets.find(x=>x.id===id)
  if(!p)throw new Error('Bilinmeyen senaryo')
  // A climate choice never overwrites crop areas or production limits.
  const next=structuredClone(current)
  next.temperature_delta_c=(base.temperature_delta_c??0)+p.temperature
  next.rainfall_factor=base.rainfall_factor*p.rain
  next.et0_factor=base.et0_factor
  next.water_sources=next.water_sources.map(s=>({...s,capacity_m3:(base.water_sources.find(b=>b.source_id===s.source_id)?.capacity_m3??s.capacity_m3)*p.water}))
  next.irrigation_efficiency=p.id==='ideal'?.95:Math.min(1,base.irrigation_efficiency+p.efficiency)
  next.climate_scenario_label=p.id==='reference'?base.climate_scenario_label:`${p.label} · ${p.detail} · varsayımsal senaryo`
  return next
}

export function activePreset(base:SimulationRequest,q:SimulationRequest){
  const signature=(s:SimulationRequest)=>JSON.stringify([s.temperature_delta_c??0,s.rainfall_factor,s.et0_factor,s.irrigation_efficiency,s.water_sources.map(w=>[w.source_id,w.capacity_m3,w.enabled])])
  return turkeyPresets.find(p=>signature(presetScenario(base,p.id))===signature(q))
}
