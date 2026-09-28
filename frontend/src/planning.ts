import type { JsonRecord } from './api'
export type Method = 'open_field' | 'greenhouse' | 'hydroponics'
export interface CropScenario {
  crop_id:string; enabled:boolean; current_area_ha:number; yield_kg_ha:number|null; season_start:string; stage_days:number[]|null;
  min_share:number; max_share:number; min_production_kg:number; target_production_kg:number; priority:number;
  climate_suitable:boolean|null; soil_suitable:boolean|null; methods:Method[]; field_energy_kwh_ha:number|null;
  controlled_yield_kg_m2:number|null; controlled_water_m3_kg:number|null; controlled_energy_kwh_kg:number|null; manual_net_irrigation_mm:number|null;
}
export interface WaterSourceScenario {source_id:'freshwater'|'stored_water'|'reuse'|'desalinated_seawater';capacity_m3:number;enabled:boolean;quality_suitable:boolean|null;energy_kwh_m3:number|null}
export type PlanningObjective = 'regional_water'|'capacity'|'demand'|'balanced'|'water_priority'|'energy_priority'
export interface SimulationRequest {
  north_input_policy?:'explicit_scenario'|'source_resolved';quantity_basis?:'demand'|'capacity';resource_priority_fraction?:number;
  planning_objective?:PlanningObjective;
  mode:'turkiye'|'north';region_id:string;period_label:string;climate_basis:'era5_2022_2023'|'era5_2024_2025'|'user_scenario';climate_scenario_label:string;climate_context_id?:'ec_earth_2030_2049'|'nasa_ssp245_2035'|'nasa_ssp585_2035'|null;
  temperature_delta_c?:number;rainfall_factor:number;et0_factor:number;land_area_ha:number;min_cultivated_fraction:number;soil_capacity_mm:number;initial_storage_mm:number;irrigation_efficiency:number;
  energy_budget_kwh:number|null;greenhouse_capacity_m2:number;hydroponics_capacity_m2:number;seawater_temperature_c:number;
  water_sources:WaterSourceScenario[];crops:CropScenario[];overrides:string[];
}
export interface BaselineAnalysis {status:'baseline_only'|'no_current_baseline';classification:'BASELINE_ANALYSIS';current:PatternAnalysis;crop_water:JsonRecord[];provenance:JsonRecord;limitations:string[]}
export interface PlanningContext {candidate_evidence?:JsonRecord;region:JsonRecord;crop_catalog:JsonRecord[];default_scenario:SimulationRequest;illustrative_scenario?:SimulationRequest;climate_context:JsonRecord;baseline_analysis:BaselineAnalysis;limitations:string[]}
export interface PatternTotals {known_water_m3?:number;open_field_area_ha:number;water_m3:number|null;energy_kwh:number|null;greenhouse_area_m2?:number;hydroponics_area_m2?:number;unallocated_land_ha?:number;available_water_m3?:number;water_deficit_m3?:number|null}
export interface PatternAnalysis {crops:{crop_id:string;name_tr:string;area_ha:number;production_kg:number;water_m3:number}[];totals:PatternTotals}
export interface SimulationResult {
  regional_scope?:{kind:string;held_crop_ids:string[];note:string};
  input_resolution?:JsonRecord|null;
  objective?:JsonRecord;effective_request?:SimulationRequest;status:string;classification:string;baseline:PatternAnalysis;current:PatternAnalysis;
  optimized:{crops:{crop_id:string;name_tr:string;area_ha:number;area_share_pct:number;production_kg:number;current_area_ha:number;delta_area_ha:number;held_for_missing_water?:boolean;summary_reason?:string;reasons:string[]}[];
    allocations:{crop_id:string;name_tr:string;method:Method;water_source:string;capacity_unit:'ha'|'m2';capacity_used:number;area_ha:number|null;production_kg:number;water_m3:number;energy_kwh:number|null;season_start:string;season_end:string}[];
    totals:PatternTotals;water_sources:{source_id:string;used_m3:number;capacity_m3:number;share_pct:number}[]}|null;
  constraints:{id:string;label:string;unit:string;used:number|null;capacity:number;slack:number|null;binding:boolean|null}[];
  crop_water:JsonRecord[];excluded_options:JsonRecord[];explanations:string[];limitations:string[];run_id:string;provenance:unknown;request:SimulationRequest;
}
export interface PlanningSession {context:PlanningContext;scenario:SimulationRequest;result:SimulationResult|null;submitted:SimulationRequest|null}
export const methodName:Record<string,string>={open_field:'Açık tarla',greenhouse:'Sera',hydroponics:'Hidroponik'}
export const sourceName:Record<string,string>={freshwater:'Yerel tatlı su',stored_water:'Depolanmış su',reuse:'Yeniden kullanım',desalinated_seawater:'Arıtılmış deniz suyu'}
