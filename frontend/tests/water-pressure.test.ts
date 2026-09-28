import assert from 'node:assert/strict'
import {test} from 'node:test'
import {effectiveWaterBudget,waterPressure} from '../src/waterPressure.ts'

test('budget ratio has a real 100% boundary and an exact deficit',()=>{
  assert.equal(waterPressure(80,100).percent,80)
  assert.equal(waterPressure(100,100).status,'within')
  assert.deepEqual(waterPressure(150,100),{status:'over',percent:150,displayPercent:150,overflow:false,zeroBudget:false,deficitM3:50})
})
test('zero budgets never become Infinity, NaN or false green',()=>{
  assert.deepEqual(waterPressure(100,0),{status:'over',percent:null,displayPercent:200,overflow:true,zeroBudget:true,deficitM3:100})
  assert.equal(waterPressure(0,0).status,'empty')
  assert.equal(waterPressure(0,0).percent,null)
})
test('partial or missing water never appears within budget',()=>{
  for(const state of [waterPressure(10,100,true),waterPressure(null,100),waterPressure(10,null),waterPressure(NaN,100),waterPressure(-1,100),waterPressure(10,-1)]){
    assert.equal(state.status,'unknown');assert.equal(state.percent,null);assert.equal(state.deficitM3,null)
  }
})
test('arc overflow preserves the ratio and all SVG inputs stay finite',()=>{
  assert.equal(waterPressure(350,100).percent,350)
  assert.equal(waterPressure(350,100).displayPercent,200)
  assert.equal(waterPressure(350,100).overflow,true)
  const enormous=waterPressure(Number.MAX_VALUE,Number.MIN_VALUE)
  assert.equal(enormous.status,'over');assert.equal(enormous.percent,null);assert.ok(Number.isFinite(enormous.displayPercent));assert.equal(enormous.overflow,true)
})
test('eligible scenario capacity excludes disabled or unproven-quality sources',()=>{
  const sources=[{enabled:true,quality_suitable:true,capacity_m3:70},{enabled:true,quality_suitable:true,capacity_m3:30},{enabled:false,quality_suitable:true,capacity_m3:900},{enabled:true,quality_suitable:null,capacity_m3:800},{enabled:true,quality_suitable:false,capacity_m3:700}]
  assert.equal(effectiveWaterBudget(sources),100)
  assert.equal(effectiveWaterBudget([{enabled:true,quality_suitable:true,capacity_m3:null}]),null)
  assert.equal(effectiveWaterBudget([]),0)
})
test('immutable prior-run budget stays independent of edited live sources',()=>{
  const snapshot=Object.freeze([Object.freeze({enabled:true,quality_suitable:true,capacity_m3:100})])
  const edited=[{...snapshot[0],capacity_m3:50}]
  assert.equal(waterPressure(80,effectiveWaterBudget(snapshot)).percent,80)
  assert.equal(waterPressure(80,effectiveWaterBudget(edited)).percent,160)
  assert.equal(snapshot[0].capacity_m3,100)
})
