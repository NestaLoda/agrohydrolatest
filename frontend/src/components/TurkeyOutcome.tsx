import type {PlanningContext,SimulationResult} from '../planning'
import {Icon,number} from '../ui'

type Row={name:string;before:number|null;after:number|null;note?:string}
const compact=(v:number)=>new Intl.NumberFormat('tr-TR',{notation:'compact',maximumFractionDigits:1}).format(v)
function Comparison({title,unit,rows,dense=false}:{title:string;unit:string;rows:Row[];dense?:boolean}){
  const max=Math.max(1,...rows.flatMap(r=>[r.before??0,r.after??0]))
  if(dense)return <figure className="outcome-chart"><figcaption>{title}<small>{unit}</small></figcaption><svg viewBox={`0 0 430 ${rows.length*30+6}`} role="img" aria-label={title}>
    {rows.map((r,i)=><g key={r.name} transform={`translate(0 ${i*30})`}><text x="0" y="20" className="chart-label">{r.name}</text>{[r.before,r.after].map((v,j)=><g key={j}><rect x="120" y={5+j*11} width={v===null?0:Math.max(0,v/max*230)} height="8" rx="2" className={j?'after':'before'}/><text x="362" y={13+j*11}>{v===null?'—':compact(v)}</text><title>{r.name} · {j?'Önerilen':'Hesap öncesi seçim'}: {v===null?r.note||'Bu karşılaştırma için ürün hesabı gerekli':number(v,2)+' '+unit}</title></g>)}</g>)}
  </svg></figure>
  return <figure className="outcome-chart"><figcaption>{title}<small>{unit}</small></figcaption><svg viewBox={`0 0 400 ${rows.length*62+12}`} role="img" aria-label={title}>
    {rows.map((r,i)=><g key={r.name} transform={`translate(0 ${i*62})`}><text x="0" y="13" className="chart-label">{r.name}</text>{[r.before,r.after].map((v,j)=><g key={j}><rect x="0" y={22+j*17} width={v===null?0:Math.max(0,v/max*300)} height="11" rx="3" className={j?'after':'before'}/><text x="310" y={32+j*17}>{v===null?'—':compact(v)}</text><title>{r.name} · {j?'Önerilen':'Mevcut'}: {v===null?r.note||'Bu karşılaştırma için ürün hesabı gerekli':number(v,2)+' '+unit}</title></g>)}</g>)}
  </svg></figure>
}
export default function TurkeyOutcome({context,result:r,compact:condensed=false}:{context:PlanningContext;result:SimulationResult;compact?:boolean}){
  const plan=r.optimized
  if(!plan)return null
  const partial=!!r.regional_scope,q=r.request
  const heldIds=new Set(plan.crops.filter(c=>c.held_for_missing_water).map(c=>c.crop_id))
  const scopeNames=plan.crops.filter(c=>heldIds.has(c.crop_id)).map(c=>c.name_tr).join(', ')
  const total=(pattern:typeof r.current)=>partial?pattern.crops.filter(c=>!heldIds.has(c.crop_id)).reduce((sum,c)=>sum+(c.water_m3??0),0):pattern.totals.water_m3
  const start=total(context.baseline_analysis.current),current=total(r.current),after=partial?plan.totals.known_water_m3??null:plan.totals.water_m3
  const saving=current!==null&&after!==null?current-after:null
  const percent=saving!==null&&current!==null?(current>0?saving/current*100:saving===0?0:null):null
  const waterDirection=percent===null?'Ürün bazında karşılaştırma':Math.abs(percent)<.05?'Su ihtiyacı korunuyor':saving!==null&&saving<0?'daha fazla su':'daha az su'
  const waterRows=plan.crops.map(c=>({name:c.name_tr,before:r.current.crops.find(x=>x.crop_id===c.crop_id)?.water_m3??null,after:c.held_for_missing_water?null:plan.allocations.filter(a=>a.crop_id===c.crop_id).reduce((sum,a)=>sum+a.water_m3,0),note:c.crop_id==='rice'?'Çeltik suyu bu hesabın kapsamı dışında':'Bu karşılaştırma için ürünün sulama hesabı gerekli'}))
  // Both patterns share the current water denominator; missing crops stay null.
  const waterPercent=(value:number|null)=>value===null||current===null?null:current>0?value/current*100:value===0?0:null
  const waterPercentRows=waterRows.map(row=>({...row,before:waterPercent(row.before),after:waterPercent(row.after)}))
  const sourceShare=(area:number)=>q.land_area_ha>0?area/q.land_area_ha*100:0
  return <section className={`turkey-outcome${condensed?' condensed':''}`} aria-label="Simülasyon özeti">{!condensed&&<><h2><Icon name="water" size={18}/> Su yönetimi · simülasyon sonucu</h2>
    <div className={`water-gain ${saving!==null&&saving<0?'increase':''}`}><div><span>Mevcut → öneri{partial?` · ${scopeNames} hariç`:''}</span><strong>{percent===null?'—':`%${number(Math.abs(percent),1)}`} <small>{waterDirection}</small></strong></div></div>
    <p className="outcome-note">Bu yüzde yalnız ürün dağılımı değişiminin ek etkisidir. İklim ve sulama verimi aynı: sulama verimi %{number(q.irrigation_efficiency*100,0)} · her ürün için seçilen en az üretim miktarı korunur.</p>
    </>}
    <div className="outcome-legend">{condensed&&<b>Mevcut → öneri</b>}<span><i/> Hesap öncesi seçim</span><span><i/> Önerilen</span>{condensed&&<small>Model hesabı</small>}</div>
    <div className="outcome-charts"><Comparison dense={condensed} title="Ürün payları" unit="% alan" rows={plan.crops.map(c=>({name:c.name_tr,before:sourceShare(c.current_area_ha),after:c.area_share_pct}))}/><Comparison dense={condensed} title="Suya etkisi" unit={partial?`% hesap öncesi su · ${scopeNames} hariç`:'% hesap öncesi toplam su'} rows={waterPercentRows}/></div>
    {partial&&<p className="outcome-note">Su grafiği {scopeNames} dışındaki ürünleri karşılaştırır.</p>}
    <details className="outcome-table"><summary>Mevcut → öneri · ayrıntılı oranlar, alan ve su hesabı</summary>
      <div className="outcome-water-path"><span>Kaynak başlangıç<b>{number(start,0)} m³</b></span><span>→</span><span>Öneri<b>{number(after,0)} m³</b></span><span>Atanmayan alan<b>{number(plan.totals.unallocated_land_ha,1)} ha</b></span></div>
      <p className="outcome-note">Su grafiğinde hesap öncesi seçimin {partial?`${scopeNames} dışındaki `:''}toplam su gereği %100 kabul edilir; iki desen de aynı toplama bölünür. Hacimler model hesabıdır, ölçülmüş tasarruf değildir.{partial?` ${scopeNames} suyu kapsam dışında; aşağıdaki su toplamları bölgenin tamamını göstermez.`:''}</p>
      {start!==null&&current!==null&&after!==null&&<div className="gain-breakdown"><span>Başlangıç → seçilen senaryo <b>{number(start-current,0)} m³</b></span><span>Desen değişiminden <b>{number(current-after,0)} m³</b></span></div>}
      <div className="table-scroll"><table><thead><tr><th>Ürün</th><th>Mevcut pay</th><th>Önerilen pay</th><th>Mevcut alan · ha</th><th>Önerilen alan · ha</th><th>Üretim değişimi</th><th>Mevcut su · m³</th><th>Önerilen su · m³</th><th>Desenden su farkı · m³</th></tr></thead><tbody>{plan.crops.map((c,i)=>{const old=r.current.crops.find(x=>x.crop_id===c.crop_id),w=waterRows[i];return <tr key={c.crop_id}><th>{c.name_tr}</th><td>%{number(sourceShare(c.current_area_ha),1)}</td><td>%{number(c.area_share_pct,1)}</td><td>{number(c.current_area_ha,1)}</td><td>{number(c.area_ha,1)}</td><td>{old?.production_kg?`${number((c.production_kg/old.production_kg-1)*100,1)}%`:'Başlangıç üretimiyle hesaplanır'}</td><td>{w.before===null?w.note:number(w.before,0)}</td><td>{w.after===null?w.note:number(w.after,0)}</td><td>{w.before!==null&&w.after!==null?number(w.before-w.after,0):w.note}</td></tr>})}</tbody></table></div>
    </details>
  </section>
}
