import {useEffect,useState} from 'react'
import type {PlanningContext,SimulationRequest,SimulationResult} from '../planning'
import type {JsonRecord} from '../api'
import {waterFor,waterKey} from '../livePattern'
import {Icon,number,str} from '../ui'
import FieldPattern,{cropColor} from './FieldPattern'
import './jury-flow.css'
import WaterPressureGauge from './WaterPressureGauge'
import {effectiveWaterBudget,waterPressure} from '../waterPressure'

const compact=(v:number)=>new Intl.NumberFormat('tr-TR',{notation:'compact',maximumFractionDigits:1}).format(v)
function Waterfall({base,condition,selected}:{base:number;condition:number;selected:number}){
  const top=Math.max(base,condition,selected,1)*1.12,y=(v:number)=>155-v/top*125
  const rows=[{label:'Başlangıç',from:0,to:base,value:base},{label:'Koşul etkisi',from:base,to:condition,value:condition-base},{label:'Desen etkisi',from:condition,to:selected,value:selected-condition},{label:'Seçilen',from:0,to:selected,value:selected}]
  return <svg viewBox="0 0 580 192" className="live-waterfall" role="img" aria-label="Su gereği değişimi: başlangıç, koşul etkisi, desen etkisi ve seçilen senaryo"><line x1="12" x2="568" y1="155" y2="155" stroke="#cfdad6"/>{rows.map((r,i)=><g key={r.label}><rect x={25+i*142} y={y(Math.max(r.from,r.to))} width="104" height={Math.max(1,Math.abs(y(r.from)-y(r.to)))} rx="3" fill={i===0||i===3?'#538794':r.value>0?'#b37f62':'#80adb7'}/><text x={77+i*142} y={y(Math.max(r.from,r.to))-8} textAnchor="middle">{i===1||i===2?r.value>0?'+':r.value<0?'−':'':''}{compact(Math.abs(r.value))}</text><text x={77+i*142} y="177" textAnchor="middle">{r.label}</text><title>{r.label}: {number(r.value,0)} m³</title>{i<3&&<line x1={129+i*142} x2={167+i*142} y1={y(r.to)} y2={y(r.to)} stroke="#a0b6b8" strokeDasharray="3 3"/>}</g>)}</svg>
}
export default function LivePattern({context,scenario:q,result,busy=false,onRun}:{context:PlanningContext;scenario:SimulationRequest;result:SimulationResult|null;busy?:boolean;onRun:()=>void}){
  const key=waterKey(q),baseKey=waterKey(context.default_scenario),inputKey=JSON.stringify(q)
  const [view,setView]=useState<'live'|'recommended'>(result?.optimized?'recommended':'live')
  useEffect(()=>{setView('live')},[inputKey])
  useEffect(()=>{setView(result?.optimized&&JSON.stringify(result.request)===inputKey?'recommended':'live')},[result])
  const [cache,setCache]=useState<{key:string;rows:JsonRecord[]}|null>(null),[error,setError]=useState(''),[selected,setSelected]=useState<string|null>(null)
  useEffect(()=>{
    if(key===baseKey)return
    const control=new AbortController()
    const timer=setTimeout(()=>{setError('');fetch('/api/scenario-preview',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(q),signal:control.signal}).then(async r=>{if(!r.ok)throw Error('Önizleme hesaplanamadı');return r.json()}).then(data=>{if(!control.signal.aborted)setCache({key,rows:data.crop_water})}).catch(()=>{if(!control.signal.aborted)setError('Su önizlemesi alınamadı')})},180)
    return ()=>{clearTimeout(timer);control.abort()}
  },[key,baseKey])
  const coefficients=key===baseKey?context.baseline_analysis.crop_water:cache?.key===key?cache.rows:null
  const showRecommended=view==='recommended'&&!!result?.optimized
  const pending=!showRecommended&&!coefficients
  const rows=q.crops.map(c=>({id:c.crop_id,name:str(context.crop_catalog.find(k=>k.crop_id===c.crop_id)?.name_tr),area:c.current_area_ha,color:cropColor(c.crop_id)}))
  const originals=rows.map(c=>({...c,area:context.baseline_analysis.current.crops.find(b=>b.crop_id===c.id)?.area_ha||0}))
  const recommendation=result?.optimized?.crops.map(c=>({...rows.find(r=>r.id===c.crop_id)!,id:c.crop_id,name:c.name_tr,area:c.area_ha}))
  const sourceArea=context.default_scenario.land_area_ha
  const shownRows=showRecommended?recommendation!:rows,shownArea=showRecommended?result!.request.land_area_ha:q.land_area_ha
  const water=shownRows.map(c=>({id:c.id,name:c.name,color:c.color,value:showRecommended?result!.optimized!.crops.find(r=>r.crop_id===c.id)?.held_for_missing_water?null:result!.optimized!.allocations.filter(a=>a.crop_id===c.id).reduce((t,a)=>t+a.water_m3,0):coefficients?waterFor(c.area,coefficients.find(w=>w.crop_id===c.id)):null}))
  const knownIds=water.filter(w=>w.value!==null&&Number.isFinite(w.value)).map(w=>w.id)
  const partial=water.some(w=>w.value===null||!Number.isFinite(w.value))||(showRecommended&& (!!result!.regional_scope||result!.optimized!.totals.water_m3===null))
  const hasKnown=!partial||water.some((w,i)=>w.value!==null&&shownRows[i].area>0)
  const selectedWater=water.reduce((sum,w)=>sum+(w.value!==null&&Number.isFinite(w.value)?w.value:0),0)
  // All three columns use the same known crop subset. Missing water never
  // becomes zero or a claim about total provincial water security.
  const baseWater=originals.filter(c=>knownIds.includes(c.id)).map(c=>context.baseline_analysis.current.crops.find(b=>b.crop_id===c.id)?.water_m3??null)
  const comparable=baseWater.every(v=>v!==null&&Number.isFinite(v))
  const start=baseWater.reduce<number>((t,v)=>t+(v??0),0)
  const condition=showRecommended?result!.current.crops.filter(c=>knownIds.includes(c.crop_id)).reduce((t,c)=>t+(c.water_m3??0),0):coefficients?originals.filter(c=>knownIds.includes(c.id)).reduce((sum,c)=>sum+(waterFor(c.area,coefficients.find(w=>w.crop_id===c.id))??0),0):0
  const sum=shownRows.reduce((s,c)=>s+c.area,0)
  const peak=Math.max(1,...water.map(w=>w.value!==null&&Number.isFinite(w.value)?w.value:0))
  const resultIsCurrent=result&&JSON.stringify(result.request)===JSON.stringify(q)
  const shownRequest=showRecommended?result!.request:q
  const waterBudget=effectiveWaterBudget(shownRequest.water_sources)
  const demandForBudget=pending||!hasKnown?null:selectedWater
  const pressure=waterPressure(demandForBudget,waterBudget,partial)
  const oldRecommendation=showRecommended&&!resultIsCurrent
  const temperature=shownRequest.temperature_delta_c??0,rainChange=(shownRequest.rainfall_factor-1)*100
  const excludedNames=water.filter(w=>w.value===null).map(w=>w.name)
  const scopeLabel=partial?(excludedNames.length?`${excludedNames.join(', ')} hariç`:'Hesaptaki ürünler'):undefined
  // Keep the headline denominator fixed when switching from preview to advice.
  // The optimizer's additional effect has a separate, explicitly named denominator.
  const improvement=!pending&&comparable&&hasKnown&&start>0?(start-selectedWater)/start*100:null
  const patternImprovement=showRecommended&&hasKnown&&condition>0?(condition-selectedWater)/condition*100:null
  const waterStages=showRecommended&&improvement!==null?[
    {label:'Başlangıç',value:100},
    {label:'Hesap öncesi seçim',value:condition/start*100},
    {label:'Önerilen desen',value:selectedWater/start*100},
  ]:null
  const stageMax=Math.max(100,...(waterStages?.map(s=>s.value)||[]))
  const climateParts=[temperature!==0?`sıcaklık ${number(Math.abs(temperature),1)}°C ${temperature>0?'artarsa':'düşerse'}`:'',Math.abs(rainChange)>.01?`yağış %${number(Math.abs(rainChange),0)} ${rainChange<0?'azalırsa':'artarsa'}`:''].filter(Boolean)
  const efficiencyChanged=Math.abs(shownRequest.irrigation_efficiency-context.default_scenario.irrigation_efficiency)>1e-8
  const climateStory=(climateParts.length?`Bu senaryoda ${climateParts.join(', ')}…`:'İklim başlangıçtakiyle aynı.')+(efficiencyChanged?` Sulama verimi: %${number(context.default_scenario.irrigation_efficiency*100,0)} → %${number(shownRequest.irrigation_efficiency*100,0)}.`:'')
  const waterHeadline=pending?error||'Su etkisi hesaplanıyor…':!hasKnown?'Ürüne özel su hesabını tamamlayın':!result&&key===baseKey&&Math.abs(selectedWater-start)<.5?'Mevcut desen · başlangıç su ihtiyacı':!partial&&pressure.status==='over'?(pressure.percent===null?'Sulama suyu sınırı yeterli değil':`Su ihtiyacı sınırı %${number(pressure.percent-100,1)} aşıyor`):improvement===null||Math.abs(improvement)<.05?'Su ihtiyacında belirgin değişim yok':`%${number(Math.abs(improvement),1)} ${improvement>0?'daha az':'daha fazla'} su gerekiyor`
  const previewTone=oldRecommendation||partial||pending?'neutral':pressure.status==='over'?'bad':improvement===null||Math.abs(improvement)<.05?'neutral':improvement>0?'good':'bad'
  const waterCaption=showRecommended?'Başlangıçtaki ürünler ve sulama koşullarına göre toplam değişim.':'Başlangıçtaki ürünler ve sulama koşullarıyla karşılaştırılıyor.'
  const patternCaption=patternImprovement===null?'':Math.abs(patternImprovement)<.05?'Ürün dağılımı değişiminin ek su etkisi belirgin değil.':`Ürün dağılımı değişiminden ayrıca %${number(Math.abs(patternImprovement),1)} ${patternImprovement>0?'daha az':'daha fazla'} su. İklim ve sulama verimi aynı.`
  return <section className={`live-pattern${busy?' simulating':''}`} aria-label="Canlı senaryo görseli" aria-busy={busy}><div className="live-heading"><h2><Icon name="seed" size={18}/> Ürün deseni simülasyonu</h2><span><i/> {busy?'HESAPLANIYOR':showRecommended?'MODEL ÖNERİSİ':'CANLI SENARYO'}</span></div>
    <div className="field-toolbar"><span>İklim senaryosu <b className="field-climate-stamp" title={oldRecommendation?'Önceki koşunun iklim girdileri':'Görünen desenin iklim girdileri'}>ΔT {temperature>0?'+':''}{number(temperature,1)}°C · yağış {rainChange<0?'−':rainChange>0?'+':''}%{number(Math.abs(rainChange),1)}</b></span><div role="group" aria-label="Tarla görünümü"><button type="button" aria-pressed={view==='live'} onClick={()=>setView('live')}>Canlı seçim</button><button type="button" aria-pressed={view==='recommended'} disabled={!recommendation} onClick={()=>setView('recommended')}>{!recommendation?'Öneri bekleniyor':resultIsCurrent?'Hesaplanan öneri':'Son öneri'}</button></div></div>
    <p className="climate-story">{climateStory}</p>
    <div className="farm-comparison">
      <FieldPattern label="Mevcut" rows={originals} area={sourceArea} selected={selected} onSelect={setSelected}/>
      <span className="farm-arrow"><Icon name="arrow" size={20}/></span>
      <FieldPattern label={view==='recommended'&&recommendation?resultIsCurrent?'Hesaplanan öneri':'Son öneri · önceki koşu':'Seçilen · canlı'} rows={shownRows} area={shownArea} selected={selected} onSelect={setSelected} active/>
    </div>
    <div className="live-legend">{shownRows.map(c=><button type="button" key={c.id} aria-pressed={selected===c.id} onClick={()=>setSelected(selected===c.id?null:c.id)}><i style={{background:c.color}}/>{c.name}<b>%{number(c.area/Math.max(shownArea,1)*100,1)}</b></button>)}</div>
    {sum<shownArea-.05&&<div className="field-unassigned-note">Alanın %{number((shownArea-sum)/shownArea*100,1)}'i bu planda ekilmiyor</div>}
    <div className={`live-water-heading with-pressure verdict-${previewTone}`}><div className="live-water-readout"><span><Icon name="water" size={14}/> {showRecommended?'BAŞLANGICA GÖRE TOPLAM SU DEĞİŞİMİ':'BAŞLANGICA GÖRE SU DEĞİŞİMİ'}{partial&&!pending?' · '+scopeLabel:''}</span><strong>{waterHeadline}</strong><small>{waterCaption}</small>{showRecommended&&<small className="pattern-water-effect">{patternCaption}</small>}{waterStages&&<div className="water-stage-comparison" role="group" aria-label={`Su ihtiyacı karşılaştırması · başlangıç 100${partial?' · '+scopeLabel:''}`}><div className="water-stage-bars">{waterStages.map(s=><div key={s.label}><span>{s.label}<b>{number(s.value,1)}</b></span><i><em style={{width:`${s.value/stageMax*100}%`}}/></i></div>)}</div><small>Başlangıçta gereken su = 100 · model hesabı</small></div>}{!pending&&partial?<small>{excludedNames.length?`${excludedNames.join(', ')} için ayrı su hesabı gerekir; bu karşılaştırma diğer ürünleri kapsar.`:'Bu karşılaştırma yalnız su hesabı yapılan ürünleri kapsar.'}</small>:pressure.status==='over'&&<small className={oldRecommendation?'':'water-budget-deficit'}>{oldRecommendation?'Önceki senaryonun sonucu.':'Bu desen su sınırını aşar. Daha az su isteyen dağılımı hesaplayın.'}</small>}</div><WaterPressureGauge demand={demandForBudget} budget={waterBudget} partial={partial} scopeLabel={scopeLabel} pending={pending} stale={!!oldRecommendation}/></div>
    <details className="live-water-details"><summary>Su hesabını aç · miktarlar ve ürün katkıları</summary><p>İhtiyaç: {pending?'Hesaplanıyor…':!hasKnown?'Ürüne özel hesap bekleniyor':`${number(selectedWater,0)} m³`} · Sulama suyu sınırı: {waterBudget===null?'Su sınırını belirleyin':`${number(waterBudget,0)} m³`}{partial?` · ${scopeLabel}`:''}</p><p>Su sınırı, senaryoda sulama için kullanılabileceğini kabul ettiğiniz miktardır. Başlangıçta mevcut desenin hesaplanan ihtiyacına eşittir; ölçülmüş su rezervi veya resmî tahsis değildir. Sulama verimi, çekilen suyun bitkinin ihtiyacını karşılayan payıdır; ürün verimi değildir.</p>{!pending&&<><div className="live-contributions">{water.map(w=><div key={w.id}><span>{w.name}</span><div><i style={{width:`${(w.value??0)/peak*100}%`}}/></div><b>{w.value===null?'Ayrı su hesabı':`${compact(w.value)} m³`}</b></div>)}</div>{hasKnown&&comparable&&<Waterfall base={start} condition={condition} selected={selectedWater}/>}</>}<p>{partial&&!pending?'Yalnız su hesabı yapılan ürünlerin alt toplamı; tüm bölgenin su toplamı değildir. ':''}{showRecommended?'Hesaplanmış öneri · model su gereği.':'Canlı model hesabı; öneri için en uygun deseni hesaplayın.'}</p></details>
    {!resultIsCurrent&&<div className="simulation-next"><span><b>{pressure.status==='over'&&!partial?'Su sınırına uygun bir desen bulalım.':'Bu koşullarda ne ekmeliyiz?'}</b><small>Model ürün paylarını hesaplasın; suyu azaltırken üretim sınırlarını korusun.</small></span><button type="button" className="button primary" disabled={busy} onClick={onRun}><Icon name="arrow" size={16}/>{busy?'Hesaplanıyor…':'Deseni optimize et'}</button></div>}
  </section>
}
