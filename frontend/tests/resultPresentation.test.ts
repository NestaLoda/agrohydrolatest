import assert from 'node:assert/strict'
import {test} from 'node:test'
import {annualEnergy} from '../src/resultPresentation.ts'

test('large annual energy uses MWh without changing its physical quantity',()=>{
  for(const kwh of [1000,117605.4455,119231.2615,1e8]){
    const shown=annualEnergy(kwh)
    assert.equal(shown.unit,'MWh/yıl')
    assert.ok(Math.abs(shown.value!*1000-kwh)<1e-6)
  }
})
test('zero is real but absent and invalid energy stay unknown',()=>{
  assert.deepEqual(annualEnergy(0),{value:0,unit:'kWh/yıl'})
  assert.deepEqual(annualEnergy(999),{value:999,unit:'kWh/yıl'})
  for(const missing of [null,undefined,NaN,Infinity,-1,'120'])assert.equal(annualEnergy(missing).value,null)
})
