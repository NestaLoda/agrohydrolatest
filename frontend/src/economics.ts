/**
 * Scenario accounting only: all unit prices/costs are user assumptions.
 * Cultivation costs EXCLUDE irrigation water/service costs to avoid counting
 * the water charge twice. Operating margin is revenue minus these modeled
 * costs; it is not net profit (finance, tax and fixed capital are not modeled).
 * Values stay unrounded; format currency only at the display boundary.
 */
export type EconomicsInputs = {
  waterCostPerM3: number | null;
  crops: Record<string, {
    salePricePerKg: number | null;
    productionCostPerHa: number | null;
  }>;
};

export type EconomicsRow = {
  crop_id: string;
  area_ha: number;
  production_kg: number;
  water_m3: number | null;
};

export type MissingEconomicInput = {
  side: 'before' | 'after';
  cropId: string | null;
  field: 'salePricePerKg' | 'productionCostPerHa' | 'waterCostPerM3'
    | 'area_ha' | 'production_kg' | 'water_m3' | 'calculationOverflow';
};

export type EconomicAmounts = {
  revenueTl: number | null;
  cultivationCostTl: number | null;
  waterCostTl: number | null;
  operatingMarginTl: number | null;
};

export type EconomicCoverage = {
  revenue: { knownRows: number; totalRows: number };
  cultivation: { knownRows: number; totalRows: number };
  water: { knownRows: number; totalRows: number };
};

export type EconomicsResult = {
  before: EconomicAmounts & { profitComplete: boolean };
  after: EconomicAmounts & { profitComplete: boolean };
  /** Signed changes, always AFTER minus BEFORE. Positive cost means extra cost. */
  delta: EconomicAmounts;
  /** Signed savings, always BEFORE minus AFTER. Negative means extra cost. */
  savings: {
    waterCostTl: number | null;
    cultivationCostTl: number | null;
    totalCostTl: number | null;
  };
  /** True only when both scenarios have complete modeled operating margins. */
  profitComplete: boolean;
  coverage: { before: EconomicCoverage; after: EconomicCoverage };
  missingInputs: MissingEconomicInput[];
};

/**
 * Display status only; the 1 TL tolerance suppresses insignificant visual
 * changes and never changes the accounting. A smaller loss is still a loss.
 */
export function economicTone(result: EconomicsResult): 'good' | 'bad' | 'neutral' {
  const marginAfter = result.after.operatingMarginTl;
  const marginChange = result.delta.operatingMarginTl;
  if (!result.profitComplete || marginAfter === null || marginChange === null
    || !Number.isFinite(marginAfter) || !Number.isFinite(marginChange)) return 'neutral';
  if (marginAfter < -1 || marginChange < -1) return 'bad';
  return marginChange > 1 ? 'good' : 'neutral';
}

const nonnegative = (value: unknown): number | null =>
  typeof value === 'number' && Number.isFinite(value) && value >= 0 ? value : null;

const finite = (value: number): number | null => Number.isFinite(value) ? value : null;

const difference = (left: number | null, right: number | null): number | null =>
  left === null || right === null ? null : finite(left - right);

const sum = (values: Array<number | null>): number | null =>
  values.some(value => value === null)
    ? null
    : finite((values as number[]).reduce((total, value) => total + value, 0));

/**
 * Prices missing from the form remain UNKNOWN, including a missing water tariff.
 * Known zero activity needs no unit price. An explicitly entered zero tariff
 * produces zero water charge even when water volume is unknown; this makes no
 * assertion about water availability or volume. Crop order does not matter.
 */
export function calculateEconomics(
  inputs: EconomicsInputs,
  rowsBefore: EconomicsRow[],
  rowsAfter: EconomicsRow[],
): EconomicsResult {
  const missingInputs: MissingEconomicInput[] = [];
  const missingKeys = new Set<string>();
  const recordMissing = (entry: MissingEconomicInput) => {
    const key = `${entry.side}:${entry.cropId ?? '*'}:${entry.field}`;
    if (!missingKeys.has(key)) {
      missingKeys.add(key);
      missingInputs.push(entry);
    }
  };

  function assess(rows: EconomicsRow[], side: 'before' | 'after') {
    function product(
      amountRaw: unknown,
      rateRaw: unknown,
      cropId: string,
      amountField: MissingEconomicInput['field'],
      rateField: MissingEconomicInput['field'],
    ): number | null {
      const amount = nonnegative(amountRaw);
      const rate = nonnegative(rateRaw);
      if (amount === 0 || rate === 0) return 0;
      if (amount === null) recordMissing({ side, cropId, field: amountField });
      if (rate === null) recordMissing({
        side, cropId: rateField === 'waterCostPerM3' ? null : cropId, field: rateField,
      });
      if (amount === null || rate === null) return null;
      const value = finite(amount * rate);
      if (value === null) recordMissing({ side, cropId, field: 'calculationOverflow' });
      return value;
    }

    const revenue = rows.map(row => product(
      row.production_kg, inputs.crops[row.crop_id]?.salePricePerKg,
      row.crop_id, 'production_kg', 'salePricePerKg',
    ));
    const cultivation = rows.map(row => product(
      row.area_ha, inputs.crops[row.crop_id]?.productionCostPerHa,
      row.crop_id, 'area_ha', 'productionCostPerHa',
    ));
    const water = rows.map(row => product(
      row.water_m3, inputs.waterCostPerM3,
      row.crop_id, 'water_m3', 'waterCostPerM3',
    ));
    const revenueTl = sum(revenue);
    const cultivationCostTl = sum(cultivation);
    const waterCostTl = sum(water);
    const operatingMarginTl = difference(difference(revenueTl, cultivationCostTl), waterCostTl);
    const totals = { revenueTl, cultivationCostTl, waterCostTl, operatingMarginTl };
    if (Object.values(totals).some(value => value === null)
      && [...revenue, ...cultivation, ...water].every(value => value !== null)) {
      recordMissing({ side, cropId: null, field: 'calculationOverflow' });
    }
    const coverageFor = (values: Array<number | null>) => ({
      knownRows: values.filter(value => value !== null).length, totalRows: rows.length,
    });
    return {
      totals: { ...totals, profitComplete: operatingMarginTl !== null },
      coverage: { revenue: coverageFor(revenue), cultivation: coverageFor(cultivation), water: coverageFor(water) },
    };
  }

  const before = assess(rowsBefore, 'before');
  const after = assess(rowsAfter, 'after');
  const delta: EconomicAmounts = {
    revenueTl: difference(after.totals.revenueTl, before.totals.revenueTl),
    cultivationCostTl: difference(after.totals.cultivationCostTl, before.totals.cultivationCostTl),
    waterCostTl: difference(after.totals.waterCostTl, before.totals.waterCostTl),
    operatingMarginTl: difference(after.totals.operatingMarginTl, before.totals.operatingMarginTl),
  };
  return {
    before: before.totals,
    after: after.totals,
    delta,
    savings: {
      waterCostTl: difference(before.totals.waterCostTl, after.totals.waterCostTl),
      cultivationCostTl: difference(before.totals.cultivationCostTl, after.totals.cultivationCostTl),
      totalCostTl: difference(
        sum([before.totals.cultivationCostTl, before.totals.waterCostTl]),
        sum([after.totals.cultivationCostTl, after.totals.waterCostTl]),
      ),
    },
    profitComplete: before.totals.profitComplete && after.totals.profitComplete,
    coverage: { before: before.coverage, after: after.coverage },
    missingInputs,
  };
}
