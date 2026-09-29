// Presentation units only. Never substitutes a missing measurement with zero.
export function annualEnergy(kwh:unknown):{value:number|null;unit:string} {
  if(typeof kwh!=='number'||!Number.isFinite(kwh)||kwh<0)return {value:null,unit:'kWh/yıl'}
  return kwh>=1000?{value:kwh/1000,unit:'MWh/yıl'}:{value:kwh,unit:'kWh/yıl'}
}
