import assert from 'node:assert/strict'
import {test} from 'node:test'
import {turkeyPresets,presetScenario,activePreset} from '../src/turkeyPresets.ts'
import {waterKey} from '../src/livePattern.ts'
import type {SimulationRequest} from '../src/planning.ts'

const base={mode:'turkiye',region_id:'konya',temperature_delta_c:0,rainfall_factor:1,et0_factor:1,irrigation_efficiency:.75,climate_scenario_label:'Kaynak hava',water_sources:[{source_id:'freshwater',capacity_m3:1000,enabled:true}],crops:[{crop_id:'wheat',current_area_ha:100,min_production_kg:500,season_start:'2025-04-01'}],overrides:[]} as SimulationRequest

test('all climate choices preserve source crop quantities and production floors',()=>{
  const untouched=structuredClone(base)
  for(const p of turkeyPresets){const next=presetScenario(base,p.id);assert.deepEqual(next.crops,base.crops);assert.equal(activePreset(base,next)?.id,p.id)}
  assert.deepEqual(base,untouched)
})
test('preset selection preserves optional user crop edits and prior input objects',()=>{
  const current=structuredClone(base);current.crops[0].current_area_ha=40;current.crops[0].min_production_kg=200
  const snapshot=structuredClone(current),next=presetScenario(base,'drought',current)
  assert.deepEqual(next.crops,current.crops);assert.deepEqual(current,snapshot);assert.equal(next.temperature_delta_c,2);assert.equal(next.rainfall_factor,.8);assert.equal(next.water_sources[0].capacity_m3,1000)
})
test('favorable and resource scenarios expose distinct physical changes without hidden crop changes',()=>{
  const wet=presetScenario(base,'coolwet');assert.equal(wet.temperature_delta_c,-1);assert.equal(wet.rainfall_factor,1.1)
  const ideal=presetScenario(base,'ideal');assert.equal(ideal.irrigation_efficiency,.95);assert.equal(ideal.rainfall_factor,1.1)
  const scarce=presetScenario(base,'water20');assert.equal(scarce.water_sources[0].capacity_m3,800);assert.equal(scarce.temperature_delta_c,0);assert.equal(scarce.rainfall_factor,1)
})
test('custom climate unselects preset; climate preview invalidates for temperature, not area alone',()=>{
  const warmed={...base,temperature_delta_c:1.3}
  assert.equal(activePreset(base,warmed),undefined);assert.notEqual(waterKey(base),waterKey(warmed))
  assert.equal(waterKey(base),waterKey({...base,crops:base.crops.map(c=>({...c,current_area_ha:30}))}))
  assert.equal(waterKey(base),waterKey({...base,temperature_delta_c:undefined}))
})
