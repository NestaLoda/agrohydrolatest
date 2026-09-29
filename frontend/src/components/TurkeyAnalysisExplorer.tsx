import {useRef,useState} from 'react'
import type {PlanningContext,SimulationResult} from '../planning'
import {Icon,number} from '../ui'
import './turkey-analysis.css'

type Props={context:PlanningContext;result:SimulationResult}
type Cell={value:number|null;note?:string;color?:string}
type Row={id:string;label:string;cells:Cell[]}
type Series={label:string;color:string}
type Chart={id:string;label:string;title:string;unit:string;note:string;series:Series[];rows:Row[];kind?:'diverging'|'waterfall';threshold?:number;empty?:string}
const green='#347b52',paleGreen='#aabea0',blue='#3f849c',paleBlue='#9fbdc5',gray='#aab7aa',rust='#a86850'
const numeric=(value:unknown):number|null=>typeof value==='number'&&Number.isFinite(value)?value:null
const cell=(value:unknown,note?:string):Cell=>({value:numeric(value),note})
const compact=(value:number)=>new Intl.NumberFormat('tr-TR',{notation:'compact',maximumFractionDigits:1}).format(value)
const ratio=(value:number|null,capacity:number|null)=>value!==null&&capacity!==null&&capacity>0?value/capacity*100:null
const shorten=(text:string)=>text.length>25?`${text.slice(0,23)}…`:text
const W=720,H=260,L=146,R=102,TOP=24,BOTTOM=220,PW=W-L-R
function comparisonRequirement(chart:Chart,row:Row){
  if(['crop-water','intensity','net-gross'].includes(chart.id))return 'Ürünün sulama hesabı gerekli'
  if(chart.id==='areas'||chart.id==='shift')return 'Karşılaştırma için alan payı gerekli'
  if(chart.id==='production'||chart.id==='minima')return 'Önerilen üretim hesabı gerekli'
  if(chart.id==='limits')return 'Kapasite ve kullanım gerekli'
  return 'Bu karşılaştırma için ürün hesabı gerekli'
}

function Legend({series}:{series:Series[]}){
  return <div className="analysis-explorer-legend">{series.map(s=><span key={s.label}><i style={{background:s.color}}/>{s.label}</span>)}</div>
}

function Bars({chart}:{chart:Chart}){
  const all=chart.rows.flatMap(row=>row.cells.flatMap(c=>c.value===null?[]:[c.value]))
  const max=Math.max(chart.threshold??0,1,...all)*1.06,plotHeight=BOTTOM-TOP,step=plotHeight/Math.max(chart.rows.length,1)
  const barHeight=Math.min(17,(step-9)/Math.max(chart.series.length,1)-2),x=(value:number)=>L+value/max*PW
  return <svg xmlns="http://www.w3.org/2000/svg" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`${chart.title} · ${chart.unit}`}>
    <title>{chart.title}</title><desc>{chart.note}</desc>
    {[0,.25,.5,.75,1].map(f=><g key={f}><line x1={L+f*PW} x2={L+f*PW} y1={TOP-5} y2={BOTTOM} stroke="#dce4dc"/><text x={L+f*PW} y={BOTTOM+17} textAnchor="middle" fontSize="11" fill="#748275">{compact(f*max)}</text></g>)}
    {chart.threshold!==undefined&&<g><line x1={x(chart.threshold)} x2={x(chart.threshold)} y1={TOP-7} y2={BOTTOM} stroke="#6f7c72" strokeDasharray="4 3"/><text x={x(chart.threshold)} y={TOP-11} textAnchor="middle" fontSize="10" fill="#596f5d">%{number(chart.threshold,0)} sınırı</text></g>}
    {chart.rows.map((row,i)=>{
      const y=TOP+i*step+(step-chart.series.length*(barHeight+2))/2
      return <g key={row.id}><text x={L-10} y={TOP+(i+.5)*step+4} textAnchor="end" fontSize="12" fill="#3d5d48"><title>{row.label}</title>{shorten(row.label)}</text>{row.cells.map((c,j)=>{
        const yy=y+j*(barHeight+2),text=c.value===null?c.note||comparisonRequirement(chart,row):`${number(c.value,2)} ${chart.unit}${c.note?' · '+c.note:''}`
        return <g key={j}><title>{row.label} · {chart.series[j].label}: {text}</title>{c.value===null?<text x={L+5} y={yy+barHeight-1} fontSize="10" fill="#7b837c">{c.note||comparisonRequirement(chart,row)}</text>:<><rect x={L} y={yy} width={Math.max(0,c.value/max*PW)} height={Math.max(3,barHeight)} rx="2" fill={c.color||chart.series[j].color}/><text x={x(Math.max(0,c.value))+6} y={yy+barHeight-1} fontSize="10" fill="#41634e">{compact(c.value)}</text></>}</g>
      })}</g>
    })}
    <text x={L+PW/2} y={H-3} textAnchor="middle" fontSize="11" fill="#647b6a">{chart.unit}</text>
  </svg>
}

function Diverging({chart}:{chart:Chart}){
  const max=Math.max(1,...chart.rows.map(row=>Math.abs(row.cells[0].value??0)))*1.1,center=L+PW/2,x=(value:number)=>center+value/max*PW/2
  const step=(BOTTOM-TOP)/Math.max(chart.rows.length,1)
  return <svg xmlns="http://www.w3.org/2000/svg" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`${chart.title} · yüzde puan`}>
    <title>{chart.title}</title><desc>{chart.note}</desc>
    {[-1,-.5,0,.5,1].map(f=><g key={f}><line x1={x(f*max)} x2={x(f*max)} y1={TOP-4} y2={BOTTOM} stroke={f===0?'#7d9180':'#dce4dc'}/><text x={x(f*max)} y={BOTTOM+17} textAnchor="middle" fontSize="11" fill="#70816f">{f>0?'+':''}{number(f*max,1)}</text></g>)}
    {chart.rows.map((row,i)=>{
      const v=row.cells[0].value,y=TOP+(i+.5)*step
      return <g key={row.id}><text x={L-10} y={y+4} textAnchor="end" fontSize="12" fill="#3d5d48"><title>{row.label}</title>{shorten(row.label)}</text>{v===null?<text x={center+5} y={y+4} fontSize="11" fill="#788276">Alan payı hesaplanmalı</text>:<><rect x={x(Math.min(0,v))} y={y-8} width={Math.abs(v)/max*PW/2} height="16" rx="2" fill={v>=0?green:gray}/><text x={v>=0?x(v)+6:x(v)-6} y={y+4} textAnchor={v>=0?'start':'end'} fontSize="11" fill="#3f614a">{v>0?'+':''}{number(v,1)}</text><title>{row.label}: {v>0?'+':''}{number(v,3)} yüzde puan</title></>}</g>
    })}<text x={L+PW/2} y={H-3} textAnchor="middle" fontSize="11" fill="#647b6a">Önerilen − seçilen · yüzde puan</text>
  </svg>
}

function Waterfall({chart}:{chart:Chart}){
  const values=chart.rows.map(row=>row.cells[0].value!)
  const max=Math.max(1,...values)*1.15,left=76,right=650,base=200,y=(v:number)=>base-v/max*160,step=(right-left)/values.length
  return <svg xmlns="http://www.w3.org/2000/svg" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`${chart.title} · m³`}>
    <title>{chart.title}</title><desc>{chart.note}</desc>
    {[0,.25,.5,.75,1].map(f=><g key={f}><line x1={left-12} x2={right} y1={y(f*max)} y2={y(f*max)} stroke="#dce4dc"/><text x={left-20} y={y(f*max)+4} textAnchor="end" fontSize="10" fill="#70816f">{compact(f*max)}</text></g>)}
    {values.map((value,i)=>{
      const total=i===0||i===values.length-1,previous=total?0:values[i-1],delta=total?value:value-previous,xx=left+i*step+8,barWidth=step-30
      return <g key={chart.rows[i].id}><rect x={xx} y={y(Math.max(previous,value))} width={barWidth} height={Math.abs(y(value)-y(previous))} rx="2" fill={total?blue:delta>0?rust:paleBlue}/><text x={xx+barWidth/2} y={y(Math.max(previous,value))-7} textAnchor="middle" fontSize="10" fill="#41634e">{!total&&delta>0?'+':!total&&delta<0?'−':''}{compact(Math.abs(delta))}</text><text x={xx+barWidth/2} y="220" textAnchor="middle" fontSize="10" fill="#41634e">{chart.rows[i].label}</text><title>{chart.rows[i].label}: {number(delta,2)} m³{!total?`; sonuç: ${number(value,2)} m³`:''}</title>{i<values.length-1&&<line x1={xx+barWidth} x2={xx+step} y1={y(value)} y2={y(value)} stroke="#869b9b" strokeDasharray="3 3"/>}</g>
    })}<text x="24" y="19" fontSize="11" fill="#647b6a">m³</text><text x="363" y="247" textAnchor="middle" fontSize="11" fill="#647b6a">Aynı ürün kümesi · başlangıç → koşul → seçim → optimizasyon</text>
  </svg>
}

function makeCharts(context:PlanningContext,r:SimulationResult):Chart[]{
  const q=r.request,plan=r.optimized,base=context.baseline_analysis.current
  const items=q.crops.map(c=>({input:c,name:r.current.crops.find(row=>row.crop_id===c.crop_id)?.name_tr||String(context.crop_catalog.find(row=>row.crop_id===c.crop_id)?.name_tr||c.crop_id),current:r.current.crops.find(row=>row.crop_id===c.crop_id),source:base.crops.find(row=>row.crop_id===c.crop_id),next:plan?.crops.find(row=>row.crop_id===c.crop_id),water:r.crop_water.find(row=>row.crop_id===c.crop_id)}))
  const proposedWater=(id:string):number|null=>{
    const crop=plan?.crops.find(c=>c.crop_id===id)
    if(!crop||crop.held_for_missing_water)return null
    const values=plan!.allocations.filter(a=>a.crop_id===id).map(a=>numeric(a.water_m3))
    return values.every(v=>v!==null)?values.reduce<number>((sum,v)=>sum+(v??0),0):null
  }
  const cropRows=(fn:(item:typeof items[number])=>Cell[])=>items.map(item=>({id:item.input.crop_id,label:item.name,cells:fn(item)}))
  const productionSeries=[{label:'Seçilen senaryo',color:paleGreen},{label:'Önerilen',color:green}]
  const waterSeries=[{label:'Seçilen senaryo',color:paleBlue},{label:'Önerilen',color:blue}]
  const noPlan=plan?undefined:'Bu koşulda bir öneri oluşmadı; karşılaştırma için uygulanabilir ürün deseni gerekli.'
  const omittedWaterNames=items.filter(c=>numeric(c.water?.gross_water_m3_ha)===null).map(c=>c.name).join(', ')
  const waterScope=omittedWaterNames?`${omittedWaterNames} suyu kapsam dışında; bu grafik tam toplamı göstermez.`:''
  const waterRequirement=(item:typeof items[number])=>numeric(item.water?.gross_water_m3_ha)===null?`${item.name} suyu kapsam dışında`:undefined
  const charts:Chart[]=[
    {id:'areas',label:'01 · Üç desen',title:'Kaynak → seçilen → önerilen alan payları',unit:'% alan',series:[{label:`Kaynak ${String(context.region.year)}`,color:gray},...productionSeries],note:'Kaynak payı resmî seçili ürün alanına, seçilen ve önerilen paylar bu koşunun alan kapasitesine bölünür; atanmayan alan payı %100’e tamamlanmaz.',rows:cropRows(c=>[cell(ratio(numeric(c.source?.area_ha),numeric(context.default_scenario.land_area_ha))),cell(ratio(numeric(c.current?.area_ha),numeric(q.land_area_ha))),cell(ratio(numeric(c.next?.area_ha),numeric(q.land_area_ha)))])},
    {id:'shift',label:'02 · Pay değişimi',title:'Öneriyle hangi ürünün alan payı değişiyor?',unit:'yüzde puan',kind:'diverging',series:[{label:'Alan artışı',color:green},{label:'Alan azalışı',color:gray}],note:'Önerilen pay − aynı koşunun seçilen payı; yüzde değişim değildir ve tek başına üretim veya kâr değişimini göstermez.',empty:noPlan,rows:cropRows(c=>[cell(c.next&&c.current?ratio(c.next.area_ha-c.current.area_ha,q.land_area_ha):null)])},
    {id:'crop-water',label:'03 · Ürünlerin suyu',title:'Aynı koşullarda ürünlere göre su gereği',unit:'m³',series:waterSeries,note:`Aynı iklim, takvim ve sulama verimi altında alan kararı değişir. ${waterScope}`.trim(),rows:cropRows(c=>[cell(c.current?.water_m3,waterRequirement(c)),cell(proposedWater(c.input.crop_id),plan?waterRequirement(c):'Önerilen desen hesaplanmalı')])},
    {id:'production',label:'04 · Üretim miktarı',title:'Ürün bazında üretim miktarı',unit:'kg',series:productionSeries,note:'Her ürün kendi içinde karşılaştırılır; farklı ürünlerin kilogramları toplam performans veya gelir göstergesi olarak toplanmaz. Verim girdileri aynı koşuya aittir.',rows:cropRows(c=>[cell(c.current?.production_kg),cell(c.next?.production_kg)])},
    {id:'intensity',label:'05 · Hektara su',title:'Ürünlerin modellenmiş brüt su gereği',unit:'m³/ha',series:[{label:'Brüt sulama suyu',color:blue}],note:'Bu koşunun iklimi, takvimi, toprağı ve sulama verimiyle hesaplanır; düşük m³/ha tek başına ürün uygunluğu veya ekonomik üstünlük değildir.',rows:cropRows(c=>[cell(c.water?.gross_water_m3_ha,waterRequirement(c))])},
    {id:'net-gross',label:'06 · Net / brüt su',title:'Net ve brüt sulama suyu gereği',unit:'mm',series:[{label:'Net sulama',color:paleBlue},{label:'Brüt sulama gereği',color:blue}],note:`Brüt mm = brüt m³/ha ÷ 10 = net mm ÷ sulama verimi; sulama verimi %${number(q.irrigation_efficiency*100,1)}. Net sulama ETc’nin tamamı değildir; yağış / toprak suyu hesabından sonra kalan gereksinimdir.`,rows:cropRows(c=>[cell(c.water?.net_irrigation_mm,waterRequirement(c)),cell(numeric(c.water?.gross_water_m3_ha)!==null?Number(c.water?.gross_water_m3_ha)/10:null,waterRequirement(c))])},
    {id:'minima',label:'07 · En az üretim',title:'Korunması istenen en az üretimin karşılanması',unit:'% alt sınır',series:[{label:'Öneri / en az üretim',color:green}],threshold:100,note:'Alt sınırdır: %100 ve üzeri karşılar, %100 altı karşılamaz. En az üretim miktarı sıfırsa oran tanımsızdır; hedef talep, kâr veya verimlilik skoru değildir.',rows:cropRows(c=>{
      const value=ratio(numeric(c.next?.production_kg),numeric(c.input.min_production_kg))
      return [{value,note:c.input.min_production_kg===0?'Alt sınır tanımlanmadı':value===null?'Önerilen üretim hesabı gerekli':`${number(c.next?.production_kg,0)} / ${number(c.input.min_production_kg,0)} kg`,color:value!==null&&value<100-.001?rust:green}]
    })},
  ]
  const resourceIds=['land','greenhouse','hydroponics','energy']
  const resources=r.constraints.filter(c=>(resourceIds.includes(c.id)||c.id.startsWith('water_'))&&(c.capacity===null||c.capacity>0||(c.used!==null&&c.used>0)))
  charts.push({id:'limits',label:'08 · Kaynak sınırları',title:'Azami kaynak kapasitesinin kullanımı',unit:'% kapasite',series:[{label:'Kullanım / üst sınır',color:blue}],threshold:100,empty:resources.length?undefined:'Pozitif kapasitesi tanımlı kaynak sınırı yok.',note:`Yalnız üst sınırlardır: %100 kapasite dolu, üzeri aşım; alt sınırlar bu grafiğe karıştırılmaz. Sıfır / kapalı kapasiteler çıkarılır.${r.regional_scope?' Kısmi koşuda alan ve su sınırları yalnız optimize edilen ürün kümesine aittir.':''}`,rows:resources.map(c=>{
    const value=ratio(numeric(c.used),numeric(c.capacity))
    return {id:c.id,label:c.label,cells:[{value,note:value===null?'Bu karşılaştırma için kapasite ve kullanım gerekli':`${number(c.used,2)} / ${number(c.capacity,2)} ${c.unit}${c.binding?' · bağlayıcı':''}`,color:value!==null&&value>100+.001?rust:blue}]}
  })})
  // Freeze one fully known crop subset across every waterfall stage. Never
  // compare different subsets or backfill missing rice water with zero.
  const comparable=items.filter(c=>numeric(c.source?.water_m3)!==null&&numeric(c.source?.area_ha)!==null&&numeric(c.water?.gross_water_m3_ha)!==null&&numeric(c.current?.water_m3)!==null&&proposedWater(c.input.crop_id)!==null)
  const omitted=items.filter(c=>!comparable.includes(c)).map(c=>c.name)
  const start=comparable.reduce((sum,c)=>sum+Number(c.source!.water_m3),0)
  const condition=comparable.reduce((sum,c)=>sum+Number(c.source!.area_ha)*Number(c.water!.gross_water_m3_ha),0)
  const current=comparable.reduce((sum,c)=>sum+Number(c.current!.water_m3),0)
  const after=comparable.reduce((sum,c)=>sum+Number(proposedWater(c.input.crop_id)),0)
  charts.push({id:'waterfall',label:'09 · Su etkisi zinciri',title:'Su gereği değişiminin ayrıştırılması',unit:'m³',kind:'waterfall',series:[{label:'Toplam',color:blue},{label:'Su azalışı',color:paleBlue},{label:'Su artışı',color:rust}],empty:comparable.length?undefined:'Bu karşılaştırma için başlangıçtan öneriye kadar aynı ürünlerin su hesabı gerekli.',note:`Kaynak deseni → aynı alanların koşul etkisi → seçilen alanların etkisi → optimizasyon → öneri. Her aşama aynı ${comparable.length} ürünü kullanır.${omitted.length?` Karşılaştırma kapsamı dışında: ${omitted.join(', ')}; grafik tam toplamı göstermez.`:''} Ölçülmüş tasarruf değildir.`,rows:[{id:'start',label:'Başlangıç',cells:[cell(start)]},{id:'condition',label:'Koşul etkisi',cells:[cell(condition)]},{id:'selected',label:'Seçim etkisi',cells:[cell(current)]},{id:'optimized',label:'Öneri etkisi',cells:[cell(after)]},{id:'end',label:'Öneri',cells:[cell(after)]}]})
  const fullCurrent=numeric(r.current.totals.water_m3),fullNext=numeric(plan?.totals.water_m3)
  const budget=q.water_sources.filter(s=>s.enabled&&s.quality_suitable===true).reduce((sum,s)=>sum+s.capacity_m3,0)
  charts.push({id:'budget',label:'10 · Su ihtiyacı / sınırı',title:'Toplam su ihtiyacı ve sulama suyu sınırı',unit:'m³',series:[{label:'Hesaplanan su / belirlenen su sınırı',color:blue}],empty:fullCurrent===null||fullNext===null?`${waterScope||'Bu karşılaştırma için tüm ürünlerin su hesabı ve uygulanabilir öneri gerekli.'} Ürünlerin suyu grafiğinde hesaplanan ürünleri karşılaştırabilirsiniz.`:undefined,note:'Su sınırı, kullanımda ve kalitesi uygun kabul edilen kaynaklar için senaryoda belirlenen miktardır; resmî tahsis değildir. Aynı koşudaki mevcut / önerilen desen toplamları karşılaştırılır.',rows:[{id:'current',label:'Seçilen senaryo',cells:[cell(fullCurrent)]},{id:'proposed',label:'Önerilen desen',cells:[cell(fullNext)]},{id:'budget',label:'Sulama suyu sınırı',cells:[{value:budget,color:gray}]}]})
  return charts
}

export default function TurkeyAnalysisExplorer({context,result}:Props){
  const [selected,setSelected]=useState('areas'),[opened,setOpened]=useState(true),chartRef=useRef<HTMLDivElement>(null)
  const charts=makeCharts(context,result),chart=charts.find(c=>c.id===selected)||charts[0]
  function download(){
    const svg=chartRef.current?.querySelector('svg')
    if(!svg)return
    const copy=svg.cloneNode(true) as SVGSVGElement
    copy.setAttribute('font-family','Segoe UI, sans-serif')
    const url=URL.createObjectURL(new Blob([new XMLSerializer().serializeToString(copy)],{type:'image/svg+xml;charset=utf-8'}))
    const anchor=document.createElement('a');anchor.href=url;anchor.download=`${result.request.region_id}-${chart.id}-${result.run_id.slice(0,10)}.svg`;anchor.click()
    setTimeout(()=>URL.revokeObjectURL(url),1000)
  }
  return <details open={opened} className="turkey-analysis-explorer" onToggle={e=>setOpened(e.currentTarget.open)}>
    <summary><Icon name="layers" size={16}/> Analiz laboratuvarı · {charts.length} grafik</summary>
    {opened&&<div className="analysis-explorer-body"><div className="analysis-explorer-toolbar"><label>Grafik<select aria-label="Analiz grafiği" value={chart.id} onChange={e=>setSelected(e.target.value)}>{charts.map(c=><option key={c.id} value={c.id}>{c.label}</option>)}</select></label><button type="button" onClick={download} disabled={!!chart.empty}>SVG indir</button></div>
      <div className="analysis-explorer-title"><h3>{chart.title}</h3><span>Son koşu · {result.run_id.slice(0,8)}</span></div>
      <Legend series={chart.series}/><div className="analysis-explorer-chart" ref={chartRef}>{chart.empty?<p className="analysis-explorer-empty">{chart.empty}</p>:chart.kind==='diverging'?<Diverging chart={chart}/>:chart.kind==='waterfall'?<Waterfall chart={chart}/>:<Bars chart={chart}/>}</div>
      <p className="analysis-explorer-note">{chart.note}</p>
    </div>}
  </details>
}
