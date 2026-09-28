import assert from 'node:assert/strict';
import { test } from 'node:test';
import { calculateEconomics, economicTone, type EconomicsInputs, type EconomicsRow } from '../src/economics.ts';

const inputs: EconomicsInputs = {
  waterCostPerM3: 2,
  crops: {
    wheat: { salePricePerKg: 10, productionCostPerHa: 100 },
    maize: { salePricePerKg: 20, productionCostPerHa: 300 },
  },
};
const before: EconomicsRow[] = [
  { crop_id: 'wheat', area_ha: 10, production_kg: 1000, water_m3: 500 },
  { crop_id: 'maize', area_ha: 5, production_kg: 1500, water_m3: 1500 },
];
const after: EconomicsRow[] = [
  { crop_id: 'maize', area_ha: 3, production_kg: 900, water_m3: 900 },
  { crop_id: 'wheat', area_ha: 12, production_kg: 1200, water_m3: 600 },
];

test('matches explicit arithmetic and signed savings, independent of crop order', () => {
  const value = calculateEconomics(inputs, before, after);
  assert.deepEqual(value.before, {
    revenueTl: 40000, cultivationCostTl: 2500, waterCostTl: 4000,
    operatingMarginTl: 33500, profitComplete: true,
  });
  assert.deepEqual(value.after, {
    revenueTl: 30000, cultivationCostTl: 2100, waterCostTl: 3000,
    operatingMarginTl: 24900, profitComplete: true,
  });
  assert.deepEqual(value.delta, {
    revenueTl: -10000, cultivationCostTl: -400, waterCostTl: -1000, operatingMarginTl: -8600,
  });
  assert.deepEqual(value.savings, { waterCostTl: 1000, cultivationCostTl: 400, totalCostTl: 1400 });
  assert.equal(value.profitComplete, true);
  assert.deepEqual(value.missingInputs, []);
  assert.deepEqual(calculateEconomics(inputs, [...before].reverse(), [...after].reverse()), value);
});

test('blank crop prices stay unknown while water-charge savings remain computable', () => {
  const value = calculateEconomics({ waterCostPerM3: 2, crops: {} }, before, after);
  assert.equal(value.before.revenueTl, null);
  assert.equal(value.before.cultivationCostTl, null);
  assert.equal(value.before.operatingMarginTl, null);
  assert.equal(value.delta.operatingMarginTl, null);
  assert.equal(value.savings.waterCostTl, 1000);
  assert.equal(value.savings.totalCostTl, null);
  assert.equal(value.profitComplete, false);
  assert.deepEqual(value.coverage.before.revenue, { knownRows: 0, totalRows: 2 });
  assert.ok(value.missingInputs.some(item => item.cropId === 'wheat' && item.field === 'salePricePerKg'));
});

test('missing water tariff is not treated as free irrigation', () => {
  const value = calculateEconomics({ ...inputs, waterCostPerM3: null }, before, after);
  assert.equal(value.before.revenueTl, 40000);
  assert.equal(value.before.waterCostTl, null);
  assert.equal(value.before.operatingMarginTl, null);
  assert.equal(value.savings.waterCostTl, null);
  assert.equal(value.missingInputs.filter(item => item.field === 'waterCostPerM3').length, 2);
});

test('zero activity needs no price and explicit zero prices are preserved', () => {
  const zero: EconomicsRow[] = [{ crop_id: 'absent', area_ha: 0, production_kg: 0, water_m3: 0 }];
  const value = calculateEconomics({ waterCostPerM3: null, crops: {} }, zero, zero);
  assert.deepEqual(value.before, {
    revenueTl: 0, cultivationCostTl: 0, waterCostTl: 0, operatingMarginTl: 0, profitComplete: true,
  });
  assert.deepEqual(value.missingInputs, []);
  const free = calculateEconomics({ waterCostPerM3: 0, crops: {
    wheat: { salePricePerKg: 0, productionCostPerHa: 0 },
  } }, [before[0]], [after[1]]);
  assert.equal(free.after.operatingMarginTl, 0);
  assert.equal(free.profitComplete, true);
});

test('partial rice water coverage blocks the full margin and full water savings', () => {
  const withRice: EconomicsInputs = { ...inputs, crops: {
    ...inputs.crops, rice: { salePricePerKg: 25, productionCostPerHa: 1000 },
  } };
  const rice: EconomicsRow = { crop_id: 'rice', area_ha: 1, production_kg: 500, water_m3: null };
  const value = calculateEconomics(withRice, [...before, rice], [...after, rice]);
  assert.equal(value.before.revenueTl, 52500);
  assert.equal(value.before.waterCostTl, null);
  assert.equal(value.savings.waterCostTl, null);
  assert.equal(value.after.operatingMarginTl, null);
  assert.deepEqual(value.coverage.after.water, { knownRows: 2, totalRows: 3 });
  assert.ok(value.missingInputs.some(item => item.cropId === 'rice' && item.field === 'water_m3'));
});

test('explicit zero water tariff permits zero charge, without requiring an unknown water volume', () => {
  const rows = [{ ...before[0], water_m3: null }];
  const value = calculateEconomics({ ...inputs, waterCostPerM3: 0 }, rows, rows);
  assert.equal(value.before.waterCostTl, 0);
  assert.equal(value.before.operatingMarginTl, 9000);
  assert.equal(value.profitComplete, true);
  assert.equal(rows[0].water_m3, null);
});

test('negative and nonfinite unit values are unknown rather than generating fictional returns', () => {
  for (const invalid of [-1, Number.NaN, Number.POSITIVE_INFINITY]) {
    const value = calculateEconomics({
      waterCostPerM3: invalid,
      crops: { wheat: { salePricePerKg: invalid, productionCostPerHa: invalid } },
    }, [before[0]], [after[1]]);
    assert.equal(value.before.revenueTl, null);
    assert.equal(value.before.cultivationCostTl, null);
    assert.equal(value.before.waterCostTl, null);
    assert.equal(value.profitComplete, false);
  }
});

test('crop removal/addition and empty selections are calculated by crop ID', () => {
  const value = calculateEconomics(inputs, [before[0]], [after[0]]);
  assert.equal(value.before.revenueTl, 10000);
  assert.equal(value.after.revenueTl, 18000);
  assert.equal(value.savings.waterCostTl, -800);
  const empty = calculateEconomics({ waterCostPerM3: null, crops: {} }, [], []);
  assert.equal(empty.profitComplete, true);
  assert.equal(empty.after.operatingMarginTl, 0);
});

test('invalid quantity and arithmetic overflow never escape as numeric results', () => {
  const invalid = calculateEconomics(inputs, [{ ...before[0], area_ha: -1 }], after);
  assert.equal(invalid.before.cultivationCostTl, null);
  assert.equal(invalid.before.operatingMarginTl, null);
  const overflow = calculateEconomics(inputs, [{ ...before[0], production_kg: Number.MAX_VALUE }], after);
  assert.equal(overflow.before.revenueTl, null);
  assert.equal(overflow.before.operatingMarginTl, null);
  assert.ok(overflow.missingInputs.some(item => item.field === 'calculationOverflow'));
});

test('does not mutate frozen scenario inputs or quantities', () => {
  const frozenInputs = Object.freeze({ ...inputs, crops: Object.freeze({ ...inputs.crops }) });
  const frozenRows = before.map(row => Object.freeze({ ...row }));
  const snapshot = JSON.stringify({ frozenInputs, frozenRows });
  calculateEconomics(frozenInputs, frozenRows, after);
  assert.equal(JSON.stringify({ frozenInputs, frozenRows }), snapshot);
});

test('economic display stays red when an improvement still leaves a modeled loss', () => {
  const unit: EconomicsInputs = {
    waterCostPerM3: 1,
    crops: { wheat: { salePricePerKg: 1, productionCostPerHa: 0 } },
  };
  const lossBefore: EconomicsRow[] = [{ crop_id: 'wheat', area_ha: 1, production_kg: 10, water_m3: 100 }];
  const lossAfter: EconomicsRow[] = [{ crop_id: 'wheat', area_ha: 1, production_kg: 10, water_m3: 50 }];
  const value = calculateEconomics(unit, lossBefore, lossAfter);
  assert.equal(value.delta.operatingMarginTl, 50);
  assert.equal(value.after.operatingMarginTl, -40);
  assert.equal(economicTone(value), 'bad');
});

test('economic display distinguishes positive improvement, deterioration and unknown results', () => {
  const improvement = calculateEconomics(inputs, after, before);
  assert.ok(improvement.after.operatingMarginTl! > 0);
  assert.ok(improvement.delta.operatingMarginTl! > 1);
  assert.equal(economicTone(improvement), 'good');
  assert.equal(economicTone(calculateEconomics(inputs, before, after)), 'bad');
  assert.equal(economicTone(calculateEconomics(inputs, before, before)), 'neutral');
  assert.equal(economicTone(calculateEconomics({ waterCostPerM3: null, crops: {} }, before, after)), 'neutral');
});

test('1 TL visual tolerance leaves accounting amounts untouched', () => {
  const unit: EconomicsInputs = {
    waterCostPerM3: 0,
    crops: { wheat: { salePricePerKg: 1, productionCostPerHa: 0 } },
  };
  const row: EconomicsRow = { crop_id: 'wheat', area_ha: 1, production_kg: 10, water_m3: 0 };
  for (const change of [-1, -0.5, 0, 0.5, 1]) {
    const value = calculateEconomics(unit, [row], [{ ...row, production_kg: 10 + change }]);
    assert.equal(value.delta.operatingMarginTl, change);
    assert.equal(economicTone(value), 'neutral');
  }
  assert.equal(economicTone(calculateEconomics(unit, [row], [{ ...row, production_kg: 11.01 }])), 'good');
  assert.equal(economicTone(calculateEconomics(unit, [row], [{ ...row, production_kg: 8.99 }])), 'bad');
});
