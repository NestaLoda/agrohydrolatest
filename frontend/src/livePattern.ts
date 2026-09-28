import type {SimulationRequest} from './planning'
import type {JsonRecord} from './api'

// Only changes that alter water/ha need a new daily water balance. Area changes
// use the matching coefficients immediately, never coefficients for old weather.
export function waterKey(q:SimulationRequest){
  return JSON.stringify([q.mode,q.region_id,q.climate_basis,q.temperature_delta_c??0,q.rainfall_factor,q.et0_factor,q.soil_capacity_mm,q.initial_storage_mm,q.irrigation_efficiency,
    q.crops.map(c=>[c.crop_id,c.season_start,c.stage_days,c.manual_net_irrigation_mm])])
}
export function waterFor(area:number,row:JsonRecord|undefined):number|null{
  if(area===0)return 0
  return typeof row?.gross_water_m3_ha==='number'&&Number.isFinite(row.gross_water_m3_ha)?area*row.gross_water_m3_ha:null
}
