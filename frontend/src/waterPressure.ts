type BudgetSource={enabled:boolean;quality_suitable:boolean|null;capacity_m3:number|null}
export type WaterPressure={status:'unknown'|'empty'|'within'|'over';percent:number|null;displayPercent:number;overflow:boolean;zeroBudget:boolean;deficitM3:number|null}
const valid=(value:number|null):value is number=>typeof value==='number'&&Number.isFinite(value)&&value>=0

// Matches the decision engine's available-water eligibility. Unknown quality
// is not assumed usable; a missing capacity on an eligible source stays unknown.
export function effectiveWaterBudget(sources:readonly BudgetSource[]):number|null{
  const usable=sources.filter(source=>source.enabled&&source.quality_suitable===true)
  if(usable.some(source=>!valid(source.capacity_m3)))return null
  const total=usable.reduce((sum,source)=>sum+source.capacity_m3!,0)
  return Number.isFinite(total)?total:null
}

// This is a budget ratio, not a probability of hydrological or crop failure.
// displayPercent is capped only for the 0–200% arc; the reported value is not.
export function waterPressure(demand:number|null,budget:number|null,partial=false):WaterPressure{
  const unknown:WaterPressure={status:'unknown',percent:null,displayPercent:0,overflow:false,zeroBudget:false,deficitM3:null}
  if(partial||!valid(demand)||!valid(budget))return unknown
  if(budget===0)return demand===0?{...unknown,status:'empty',zeroBudget:true,deficitM3:0}:{status:'over',percent:null,displayPercent:200,overflow:true,zeroBudget:true,deficitM3:demand}
  const raw=demand/budget*100,percent=Number.isFinite(raw)?raw:null
  return {status:demand<=budget?'within':'over',percent,displayPercent:Math.min(200,percent??200),overflow:percent===null||percent>200,zeroBudget:false,deficitM3:Math.max(0,demand-budget)}
}
