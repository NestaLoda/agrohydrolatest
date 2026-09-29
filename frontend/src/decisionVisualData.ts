// Display-only transforms: no optimizer inputs or results are changed.
export const finiteValue=(value:unknown):number|null=>typeof value==='number'&&Number.isFinite(value)?value:null
export function waterDifference(before:unknown,after:unknown){
  const a=finiteValue(before),b=finiteValue(after)
  return a===null||b===null?null:a-b
}
export function monthlyWaterPoint(row:Record<string,unknown>){
  const stored=finiteValue(row.stored_water_used_m3),fresh=finiteValue(row.freshwater_m3),sea=finiteValue(row.desalinated_m3)
  return {month:finiteValue(row.month),demand:finiteValue(row.demand_m3),stored,fresh,sea,
    supplied:stored===null||fresh===null||sea===null?null:stored+fresh+sea,
    stock:finiteValue(row.storage_end_m3),capture:finiteValue(row.capture_m3)}
}
