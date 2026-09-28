import {useEffect,useMemo,useRef,useState} from 'react'
import {api,type JsonRecord,type Overview,type Transfer} from './api'
import type {PlanningContext,PlanningSession,SimulationResult} from './planning'
import {presetScenario} from './turkeyPresets'
import {juryDemoDefaultYear,juryDemoDurationSeconds,juryDemoPreset,juryDemoYears} from './juryDemoPreset'
import {Icon,list,number,obj,str} from './ui'
import Simulation from './workspaces/Simulation'
import NorthConsole,{northDefaultRequest,type NorthRequest} from './workspaces/NorthConsole'
import './jury-demo.css'

const n=(x:unknown)=>typeof x==='number'&&Number.isFinite(x)?x:0
const yearText=(year:number)=>year===juryDemoPreset.north.referenceYear?'Şimdi':`+${year-juryDemoPreset.north.referenceYear} yıl`
type DemoMode='turkiye'|'north'

export default function JuryDemo({overview,benchmarks,onContext,onExit}:{overview:Overview|null;benchmarks:Transfer|null;onContext:(mode:DemoMode,region:string)=>void;onExit:()=>void}){
  const [started,setStarted]=useState(false),[stepIndex,setStepIndex]=useState(0),[playing,setPlaying]=useState(false)
  const [contexts,setContexts]=useState<Record<string,PlanningContext>>({})
  const [results,setResults]=useState<Record<string,SimulationResult>>({})
  const [northYear,setNorthYear]=useState(juryDemoDefaultYear),[northPlan,setNorthPlan]=useState<JsonRecord|null>(null),[reference,setReference]=useState<JsonRecord|null>(null)
  const [error,setError]=useState(''),[retry,setRetry]=useState(0)
  const step=juryDemoPreset.steps[stepIndex],north=stepIndex>=3
  const region=stepIndex===2?juryDemoPreset.turkey.transferRegion:juryDemoPreset.turkey.pilotRegion
  const northRequest=useMemo<NorthRequest>(()=>({...northDefaultRequest,...juryDemoPreset.north.request,
    disabled_crops:[...juryDemoPreset.north.request.disabled_crops],disabled_methods:[...juryDemoPreset.north.request.disabled_methods],
    target_year:northYear}),[northYear])
  const referenceKey=JSON.stringify(northRequest)

  useEffect(()=>{onContext(north?'north':'turkiye',north?'longyearbyen':region)},[north,region,onContext])
  useEffect(()=>{let active=true;setError('');Promise.all([
    api.planningContext(juryDemoPreset.turkey.pilotRegion),
    api.planningContext(juryDemoPreset.turkey.transferRegion),
  ]).then(([pilot,transfer])=>{if(active)setContexts({[juryDemoPreset.turkey.pilotRegion]:pilot,[juryDemoPreset.turkey.transferRegion]:transfer})})
    .catch(e=>{if(active)setError(e instanceof Error?e.message:'Bölge verileri yüklenemedi.')});return()=>{active=false}},[retry])
  useEffect(()=>{const pilot=contexts[juryDemoPreset.turkey.pilotRegion],transfer=contexts[juryDemoPreset.turkey.transferRegion];if(!pilot||!transfer)return
    let active=true;setError('');const water=presetScenario(pilot.default_scenario,juryDemoPreset.turkey.waterPreset)
    Promise.all([api.simulate(water),api.simulate(transfer.default_scenario)])
      .then(([pilotResult,transferResult])=>{if(active)setResults({water:pilotResult,transfer:transferResult})})
      .catch(e=>{if(active)setError(e instanceof Error?e.message:'Türkiye hesabı çalıştırılamadı.')});return()=>{active=false}
  },[contexts])
  useEffect(()=>{if(!north)return;const abort=new AbortController();setReference(null);setError('')
    fetch('/api/north/reference',{method:'POST',headers:{'Content-Type':'application/json'},body:referenceKey,signal:abort.signal})
      .then(async response=>{const body=await response.json();if(!response.ok)throw new Error(typeof body.detail==='string'?body.detail:'Gelecek yılı karşılaştırılamadı.');return body as JsonRecord})
      .then(value=>{if(!abort.signal.aborted)setReference(value)})
      .catch(e=>{if(e.name!=='AbortError')setError(e.message)});return()=>abort.abort()
  },[north,referenceKey,retry])
  useEffect(()=>{if(!started)return;const selectors:Record<string,string>={baseline:'.current-crop-pattern','turkey-decision':'.live-pattern','north-climate':'.ns-change','north-decision':'.ns-decision-grid'}
    const selector=selectors[step.focus];if(!selector)return;const timer=window.setTimeout(()=>document.querySelector(`.jury-demo-workspace ${selector}`)?.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'center'}),120)
    return()=>window.clearTimeout(timer)
  },[started,step.focus,stepIndex,northYear])

  const ready=stepIndex===0?Boolean(contexts[region]):stepIndex===1?Boolean(results.water):stepIndex===2?Boolean(results.transfer):Boolean(northPlan&&reference)
  const keyboardState=useRef({ready,started})
  keyboardState.current={ready,started}
  useEffect(()=>{if(!started||!playing||!ready||error)return;const timer=window.setTimeout(()=>{if(stepIndex<juryDemoPreset.steps.length-1)setStepIndex(i=>i+1);else setPlaying(false)},step.seconds*1000);return()=>window.clearTimeout(timer)},[started,playing,ready,error,stepIndex,step.seconds])
  useEffect(()=>{const key=(event:KeyboardEvent)=>{
    if(event.key==='ArrowRight'){event.preventDefault();if(!keyboardState.current.started)setStarted(true);else if(keyboardState.current.ready)setStepIndex(i=>Math.min(juryDemoPreset.steps.length-1,i+1))}
    if(event.key==='ArrowLeft'){event.preventDefault();setStepIndex(i=>Math.max(0,i-1))}
    if(event.key==='Escape'){event.preventDefault();onExit()}}
    window.addEventListener('keydown',key);return()=>window.removeEventListener('keydown',key)
  },[onExit])
  useEffect(()=>{if(error)setPlaying(false)},[error])
  const context=contexts[region],scenario=context?stepIndex===1?presetScenario(context.default_scenario,juryDemoPreset.turkey.waterPreset):context.default_scenario:null
  const result=stepIndex===1?results.water:stepIndex===2?results.transfer:null
  const session:PlanningSession|null=context&&scenario?{context,scenario,result:result||null,submitted:result?scenario:null}:null
  const points=list(reference?.points),before=points.find(p=>p.target_year===juryDemoPreset.north.referenceYear),after=points.find(p=>p.target_year===northYear)
  const beforeClimate=obj(before?.climate),afterClimate=obj(after?.climate)
  const northTotals=obj(obj(northPlan?.plan).totals),northStory=obj(northPlan?.decision_story),northProduction=obj(northStory.production)
  const northMethods=list(northProduction.methods)
  const changedCrops=before&&after?JSON.stringify(list(before.crops).map(c=>[c.id,Math.round(n(c.share_pct)*10)]))!==JSON.stringify(list(after.crops).map(c=>[c.id,Math.round(n(c.share_pct)*10)])):false
  const binding=result?.constraints.find(c=>c.binding)
  const waterBefore=result?.current.totals.water_m3,waterAfter=result?.optimized?.totals.water_m3

  const facts=stepIndex===0?[["KAYNAKLI DESEN",String(context?.region.year||'—')],["BÖLGE",str(context?.region.name)||'Konya']]
    :stepIndex===1?[["SU SINIRI",'−%20 · senaryo'],["MEVCUT DESENİN SU GEREĞİ",waterBefore==null?'—':`${number(waterBefore,0)} m³`],["ÖNERİLEN DESENİN SU GEREĞİ",waterAfter==null?'—':`${number(waterAfter,0)} m³`],["ETKİN SINIR",binding?.label||'Ayrıntıda']]
    :stepIndex===2?[["BÖLGE",str(context?.region.name)||'Gediz / Manisa'],["MODEL DURUMU",result?.status||'Hesaplanıyor'],["ÖNERİLEN İLK ÜRÜN",result?.optimized?.crops.find(c=>c.area_ha>0)?.name_tr||'—']]
    :stepIndex===3?[["ORTALAMA SICAKLIK",before&&after?`${number(obj(beforeClimate.mean_temperature_c).mean)} → ${number(obj(afterClimate.mean_temperature_c).mean)} °C`:'—'],["DONSÜZ PENCERE",before&&after?`${number(obj(beforeClimate.frost_free_run_days).mean,0)} → ${number(obj(afterClimate.frost_free_run_days).mean,0)} gün`:'—'],["YAĞIŞ BAĞLAMI",before&&after?`${number(obj(beforeClimate.precipitation_mm).mean,0)} → ${number(obj(afterClimate.precipitation_mm).mean,0)} mm`:'—'],["ÜRÜN PAYLARI",before&&after?changedCrops?'Değişti':'Korundu':'—']]
    :stepIndex===4?[["YENİ SU GEREĞİ",`${number(northTotals.water_m3)} m³/yıl`],["DEPO / YAĞIŞ-KAR",`${number(northTotals.stored_water_m3)} m³/yıl`],["ARITILMIŞ DENİZ",`${number(northTotals.desalinated_m3)} m³/yıl`],["EN ÇOK YEDEK GEREKEN AY",str(obj(obj(northStory.water_security).critical_month).label)||'Yok']]:[]

  function changeYear(year:number){setNorthPlan(null);setReference(null);setNorthYear(year)}
  function next(){setStarted(true);setStepIndex(i=>Math.min(juryDemoPreset.steps.length-1,i+1))}
  function previous(){setStepIndex(i=>Math.max(0,i-1))}
  return <div className="jury-demo" data-focus={started?step.focus:'intro'} aria-label="Jüri modu rehberli önizleme">
    <div className="jury-demo-context"><span><Icon name="globe" size={14}/>{north?'GELECEK / KUZEY · LONGYEARBYEN':`BUGÜN / TÜRKİYE · ${str(context?.region.name)||'KONYA'}`}</span><b>JÜRİ MODU · GERÇEK MODEL HESABI</b></div>
    <div className="jury-demo-workspace" aria-hidden={!started}>
      {north?<NorthConsole key={`jury-north-${northYear}-${retry}`} demoRequest={northRequest} onPlanResult={setNorthPlan} onPlanError={setError} onProducer={()=>{}}/>:
        <Simulation key="jury-turkiye" session={session} overview={overview} benchmarks={benchmarks} northContext={null} northEvidence={null} onEdit={()=>{}} onReset={()=>{}} onRun={()=>{}} busy={false} error={error} loading={!session} onResearch={()=>{}} automaticNorth={null} automaticBusy={false} automaticError="" onProducer={()=>{}}/>}
    </div>
    {started&&north&&stepIndex<=5&&<div className="jury-year-rail" role="group" aria-label="Jüri modu gelecek yılı">
      {juryDemoYears.map(year=><button key={year} aria-pressed={northYear===year} onClick={()=>changeYear(year)}>{yearText(year)} <small>{year}</small></button>)}
    </div>}
    {started&&stepIndex===5&&<aside className="jury-floating jury-field"><b><Icon name="sensor" size={17}/> ARAŞTIRMAYLA DOĞRULANACAK GİRDİLER</b><div><strong>PWN</strong><span>Polar Water Node: farklı derinliklerde su sıcaklığı, iletkenlik ve basınç profili hedefi.</span></div><div><strong>FİZİKSEL NUMUNE</strong><span>Ayrı örnekleme; kullanılabilirlik ve arıtma kimyası, izin ve uzman paneliyle.</span></div><div><strong>DİĞER ARAŞTIRMA</strong><span>Mevsimsel karasal su · zemin/permafrost · yerel enerji.</span></div><small>v0.1 kayıt/analiz yazılımı mevcut; fiziksel tank/Arktik ölçümü doğrulanmış değil. Deniz sürümü için UTC/konum, yerel kayıt ve kalite kontrolleri hedefleniyor.</small><div className="jury-prepost"><span>PRE-TASE<br/><small>Model planı</small></span><Icon name="arrow" size={14}/><span>TASE<br/><small>PWN + izinli numune</small></span><Icon name="arrow" size={14}/><span>POST-TASE<br/><small>Aynı motor</small></span></div><small>Kararın değişmesi zorunlu değildir; PWN karasal yıllık suyu doğrudan ölçmez.</small></aside>}
    {started&&stepIndex===6&&<aside className="jury-floating jury-pilot"><b><Icon name="greenhouse" size={17}/> KONTROLLÜ ÜRETİM DENEYİ</b><span>Hocamızın mevcut topraksız düzeneğini seçilen ürün/koşula uyarlamayı planlıyoruz: uygun işlem görmüş numune veya açıkça etiketli yeniden oluşturulmuş suyla yeni su, elektrik, ısı ve hasadı ölçeceğiz.</span><small>Henüz deney ölçümü yok. Tek pilot bütün Arktik tarım modelini doğrulamaz.</small></aside>}
    {started&&stepIndex===7&&<aside className="jury-floating jury-continuity"><b>TEK ARAŞTIRMA HATTI</b><div><span>Konya<small>Mevcut desen</small></span><Icon name="arrow" size={14}/><span>Türkiye<small>Aynı motor</small></span><Icon name="arrow" size={14}/><span>Kuzey<small>Üretim + su</small></span><Icon name="arrow" size={14}/><span>TASE<small>Fiziksel kanıt</small></span><Icon name="arrow" size={14}/><span>Pilot<small>Gerçek üretim</small></span></div></aside>}
    <div className="jury-dock" role="region" aria-label="Jüri modu denetimleri">
      <div className="jury-progress"><span>{started?`${stepIndex+1} / ${juryDemoPreset.steps.length}`:`${juryDemoPreset.steps.length} adım · ${juryDemoDurationSeconds} sn`}</span><div>{juryDemoPreset.steps.map((item,i)=><i key={item.id} className={started&&i<=stepIndex?'passed':''}/>)}</div><small>{started?`${step.seconds} sn`: 'Başlat ile canlı önizleme'}</small></div>
      <div className="jury-dock-copy"><b>{started?step.title:'JÜRİ MODU · REHBERLİ ÖNİZLEME'}</b><p>{started?step.caption:'Konya’dan Kuzey’e karar hattını kısa bir akışta göster.'}</p>{started&&facts.length>0&&<div className="jury-facts">{facts.map(([label,value])=><span key={label}><small>{label}</small><strong>{value}</strong></span>)}</div>}{started&&north&&<small>{northYear} · {northRequest.scenario_id.toUpperCase()} · {northRequest.area_m2} m² planlama birimi · dengeli amaç · model yılı/senaryo</small>}{started&&stepIndex===4&&northMethods.length>0&&<small>Yöntemler: {northMethods.map(m=>`${str(m.label)} %${number(n(m.area_m2)/n(northRequest.area_m2)*100,0)}`).join(' · ')} · elektrik eşdeğeri: {number(northTotals.equivalent_electricity_kwh,0)} kWh/yıl</small>}{started&&stepIndex===1&&result?.classification&&<small>{result.classification} · ölçülmüş su tasarrufu değil</small>}{error&&<small className="jury-error" role="alert">Hesap başarısız: {error} <button onClick={()=>setRetry(i=>i+1)}>Yeniden dene</button></small>}{started&&!ready&&!error&&<small role="status">Mevcut API ile hesaplanıyor…</small>}</div>
      <div className="jury-controls"><button className="jury-start" onClick={()=>{if(!started){setStarted(true);setStepIndex(0)}else previous()}}>{started?'Önceki':'Başlat'}</button><button disabled={!started||!ready||stepIndex===juryDemoPreset.steps.length-1} onClick={next}>Sonraki</button><button aria-pressed={playing} onClick={()=>{setStarted(true);setPlaying(p=>!p)}}>{playing?'Durdur':'Otomatik oynat'}</button><button className="jury-exit" onClick={onExit}>Jüri modundan çık</button></div>
    </div>
  </div>
}
