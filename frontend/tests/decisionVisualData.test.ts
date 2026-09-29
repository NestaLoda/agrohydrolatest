import assert from 'node:assert/strict'
import {test} from 'node:test'
import {waterDifference,monthlyWaterPoint} from '../src/decisionVisualData.ts'

test('water change retains direction and missing values instead of claiming savings',()=>{
  assert.equal(waterDifference(100,70),30)
  assert.equal(waterDifference(70,100),-30)
  assert.equal(waterDifference(0,0),0)
  for(const missing of [undefined,null,NaN,Infinity,'100']){
    assert.equal(waterDifference(missing,100),null)
    assert.equal(waterDifference(100,missing),null)
  }
})
test('monthly source sum excludes capture and remaining storage, preserving inputs',()=>{
  const row=Object.freeze({month:5,demand_m3:8,stored_water_used_m3:3,freshwater_m3:2,desalinated_m3:3,storage_end_m3:20,capture_m3:50})
  assert.deepEqual(monthlyWaterPoint(row),{month:5,demand:8,stored:3,fresh:2,sea:3,supplied:8,stock:20,capture:50})
  assert.equal(monthlyWaterPoint({...row,desalinated_m3:undefined}).supplied,null)
  assert.equal(monthlyWaterPoint({...row,stored_water_used_m3:0,freshwater_m3:0,desalinated_m3:0}).supplied,0)
})
