import {useState} from 'react'
import type {SimulationResult} from '../planning'
import type {JsonRecord} from '../api'
import {list,number,obj} from '../ui'
import {finiteValue,monthlyWaterPoint,waterDifference} from '../decisionVisualData'
import './decision-visuals.css'

const compact=(value:number)=>new Intl.NumberFormat('tr-TR',{notation:'compact',maximumFractionDigits:1}).format(value)
const months=['Oca','Şub','Mar','Nis','May','Haz','Tem','Ağu','Eyl','Eki','Kas','Ara']

export function TurkeyDecisionVisual({result}:{result:SimulationResult}){
  const [mode,setMode]=useState<'area'|'water'>('area'),plan=result.optimized
  if(!plan)return null
  const area=result.request.land_area_ha
  const rows=plan.crops.map(c=>{
    const before=result.current.crops.find(r=>r.crop_id===c.crop_id)
    const allocations=plan.allocations.filter(a=>a.crop_id===c.crop_id)
    const water=c.held_for_missing_water||!allocations.length||allocations.some(a=>finiteValue(a.water_m3)===null)?null:allocations.reduce((sum,a)=>sum+a.water_m3,0)
    return {name:c.name_tr,before:area>0?c.current_area_ha/area*100:null,after:area>0?c.area_ha/area*100:null,saved:waterDifference(before?.water_m3,water)}
  })
  const maxShare=Math.max(10,...rows.flatMap(r=>[r.before??0,r.after??0]))*1.08
  const maxWater=Math.max(1,...rows.map(r=>Math.abs(r.saved??0)))*1.12
  const missing=rows.filter(r=>r.saved===null)
  const height=90+rows.length*64,x=(v:number)=>200+v/maxShare*490,center=450
  return <section className="decision-visual dv-turkey" aria-label="Ürün kararının görsel analizi">
    <header><div><span className="dv-eyebrow">KARARIN ETKİSİ</span><h2>{mode==='area'?'Hangi ürünü artırıyor, hangisini azaltıyoruz?':'Su ihtiyacındaki fark nereden geliyor?'}</h2><p>Aynı iklim ve sulama koşullarında hesap öncesi seçim → önerilen desen.</p></div><div className="dv-switch" aria-label="Karar grafiği"><button aria-pressed={mode==='area'} onClick={()=>setMode('area')}>Ürün payları</button><button aria-pressed={mode==='water'} onClick={()=>setMode('water')}>Su farkı</button></div></header>
    <div className="dv-legend">{mode==='area'?<><span>○ Hesap öncesi seçim</span><span>● Önerilen desen</span><b>Değişim: yüzde puan</b></>:<><span>← Su gereği artışı</span><span>Su gereği azalması →</span><b>Seçilen − önerilen · m³</b></>}</div>
    <svg className="dv-plot" viewBox={`0 0 860 ${height}`} role="img" aria-label={rows.map(r=>mode==='area'?`${r.name}: yüzde ${number(r.before)} → ${number(r.after)}`:`${r.name}: su farkı ${r.saved===null?'hesap kapsamı dışında':number(r.saved)+' m³'}`).join('; ')}>
      <title>{mode==='area'?'Ürünlerin alan payı değişimi':'Ürünlerin su gereği farkı'}</title>
      {mode==='area'?[0,.25,.5,.75,1].map(f=><g key={f}><line x1={x(maxShare*f)} x2={x(maxShare*f)} y1="30" y2={height-36} className="dv-grid"/><text x={x(maxShare*f)} y={height-12} textAnchor="middle">%{number(maxShare*f,0)}</text></g>):[-1,-.5,0,.5,1].map(f=><g key={f}><line x1={center+f*240} x2={center+f*240} y1="30" y2={height-36} className={f===0?'dv-zero':'dv-grid'}/><text x={center+f*240} y={height-12} textAnchor="middle">{f>0?'+':''}{compact(f*maxWater)}</text></g>)}
      {rows.map((r,i)=>{const y=60+i*64,delta=r.before===null||r.after===null?null:r.after-r.before;return <g key={r.name}>
        <text x="8" y={y+5} className="dv-crop-label">{r.name}</text>
        {mode==='area'&&r.before!==null&&r.after!==null?<><line x1={x(r.before)} x2={x(r.after)} y1={y} y2={y} stroke={delta!==null&&delta>=0?'#397c57':'#a16b4f'} strokeWidth="7" strokeLinecap="round"/><circle cx={x(r.before)} cy={y} r="7" fill="#fafbf6" stroke="#82988c" strokeWidth="3"/><circle cx={x(r.after)} cy={y} r="8" fill="#216a47"/><text x="718" y={y-5} className="dv-number">{number(r.before)} → {number(r.after)}</text><text x="718" y={y+17}>{delta!>0?'+':''}{number(delta)} puan</text></>:mode==='water'&&r.saved!==null?<><rect x={center+Math.min(0,r.saved)/maxWater*240} y={y-13} height="26" width={Math.abs(r.saved)/maxWater*240} rx="4" fill={r.saved>=0?'#29829a':'#b07950'}/><text x="718" y={y+5} className="dv-number">{r.saved>0?'+':''}{compact(r.saved)}</text></>:<text x="220" y={y+5}>Hesap kapsamı dışında</text>}
      </g>})}
    </svg>
    <footer>{mode==='area'?`Paylar ${number(area,0)} ha senaryo alanına göredir. Ekilmeyen alan: ${number(plan.totals.unallocated_land_ha,1)} ha; paylar yeniden %100'e tamamlanmaz.`:`Pozitif değer su gereğinin azaldığını, negatif değer arttığını gösterir. Ölçülmüş tasarruf değildir.${missing.length?' Kapsam dışında: '+missing.map(r=>r.name).join(', ')+'.':''}`}</footer>
  </section>
}

export function NorthWaterVisual({result}:{result:JsonRecord}){
  const rows=list(obj(result.plan).monthly).map(monthlyWaterPoint),[selected,setSelected]=useState(0)
  if(!rows.length)return null
  const point=rows[Math.min(selected,rows.length-1)],max=Math.max(.01,...rows.flatMap(r=>[r.demand??0,r.supplied??0]))*1.15
  const plotBottom=270,plotTop=40,left=65,step=720/rows.length,y=(v:number)=>plotBottom-v/max*(plotBottom-plotTop)
  const stockMax=Math.max(.01,...rows.map(r=>r.stock??0))*1.1
  return <section className="decision-visual dv-north" aria-label="Aylık su tahsis grafiği"><header><div><span className="dv-eyebrow">SU YÖNETİMİ · 12 AY</span><h2>Üretimin suyu hangi ay, hangi kaynaktan geliyor?</h2><p>Kaynak katkıları sütunlarda, üretimin yeni su ihtiyacı çizgide. Ay seçerek miktarları inceleyin.</p></div></header>
    <div className="dv-legend"><span><i style={{background:'#348da0'}}/>Depodan kullanılan</span><span><i style={{background:'#7eb4bf'}}/>Yerel tatlı su</span><span><i style={{background:'#345988'}}/>Arıtılmış deniz</span><span>◆ Yeni su ihtiyacı</span><b>m³ / ay</b></div>
    <svg className="dv-plot" viewBox="0 0 850 330" role="img" aria-label="Aylık kaynak tahsisleri ve yeni su ihtiyacı; ayrıntılı miktarlar ay düğmeleriyle okunabilir.">
      <title>Aylık su kaynakları ve üretim talebi</title>
      {[0,.25,.5,.75,1].map(f=><g key={f}><line x1="55" x2="800" y1={y(f*max)} y2={y(f*max)} className="dv-grid"/><text x="46" y={y(f*max)+5} textAnchor="end">{number(f*max,1)}</text></g>)}
      {rows.map((r,i)=>{const xx=left+i*step;let base=0;return <g key={i}><rect x={xx-7} y="30" width={step-4} height="255" rx="5" fill={i===selected?'#e0edef':'transparent'}/>{r.supplied===null?<text x={xx+16} y="240">?</text>:[{v:r.stored!,color:'#348da0'},{v:r.fresh!,color:'#7eb4bf'},{v:r.sea!,color:'#345988'}].map((part,j)=>{base+=part.v;return <rect key={j} x={xx+5} y={y(base)} width={Math.min(32,step-16)} height={part.v/max*(plotBottom-plotTop)} fill={part.color}/>})}<text x={xx+21} y="310" textAnchor="middle">{r.month?months[r.month-1]:'—'}</text></g>})}
      {rows.slice(1).map((r,i)=>r.demand!==null&&rows[i].demand!==null?<line key={i} x1={left+i*step+21} y1={y(rows[i].demand!)} x2={left+(i+1)*step+21} y2={y(r.demand)} stroke="#244c3d" strokeWidth="3" strokeDasharray="6 4"/>:null)}
      {rows.map((r,i)=>r.demand!==null?<path key={i} d={`M${left+i*step+21} ${y(r.demand)-5} l5 5 l-5 5 l-5 -5 Z`} fill="#244c3d" stroke="white" strokeWidth="1.5"/>:null)}
    </svg>
    <div className="dv-month-picker" aria-label="Su grafiğinde ay seçimi">{rows.map((r,i)=><button key={i} aria-pressed={selected===i} onClick={()=>setSelected(i)}>{r.month?months[r.month-1]:'—'}</button>)}</div>
    <div className="dv-month-readout" aria-live="polite"><span><small>Yeni su ihtiyacı</small><b>{number(point.demand,2)} <em>m³</em></b></span><span><small>Depodan kullanılan</small><b>{number(point.stored,2)} <em>m³</em></b></span><span><small>Tatlı su / arıtılmış deniz</small><b>{number(point.fresh,2)} / {number(point.sea,2)} <em>m³</em></b></span></div>
    <div className="dv-stock"><div><b>Ay sonu depo stoku</b><span>{number(point.stock,2)} m³ · {point.month?months[point.month-1]:''}</span></div><svg viewBox="0 0 850 105" role="img" aria-label={rows.map(r=>`${r.month?months[r.month-1]:''}: ay sonu stok ${number(r.stock,2)} m³`).join('; ')}><line x1="55" x2="800" y1="75" y2="75" className="dv-grid"/><text x="46" y="79" textAnchor="end">0</text><text x="46" y="15" textAnchor="end">{number(stockMax,1)}</text>{rows.map((r,i)=><g key={i}>{r.stock!==null&&<rect x={left+i*step+5} y={75-r.stock/stockMax*65} width={Math.min(32,step-16)} height={r.stock/stockMax*65} rx="3" fill={i===selected?'#267c85':'#a5c2bf'}/>}<text x={left+i*step+21} y="98" textAnchor="middle">{r.month?months[r.month-1]:''}</text></g>)}</svg></div>
    <footer>Üst grafik üretime tahsis edilen yeni suyu, alt grafik ay sonunda depoda kalan stoku gösterir. Stok, kaynaklara ikinci kez eklenmez. Aylık model planı; günlük yedek ihtiyacı aşağıdaki sınamada ayrıca değerlendirilir.</footer>
  </section>
}
