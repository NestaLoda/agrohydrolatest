import {useEffect, useState} from 'react'
import {Icon, list, obj, number} from '../ui'
import type {JsonRecord} from '../api'
import './north-simulation.css'
import './north-decision-pass.css'
import ProducerRecommendation, {contextFromNorth,type ProducerContext} from '../components/ProducerRecommendation'
import NorthWaterStrategy from './NorthWaterStrategy'
import NorthEnergyExplanation from './NorthEnergyExplanation'
import DecisionReportButton from '../components/DecisionReportButton'

const n=(v:unknown)=>typeof v==='number'?v:0
const s=(v:unknown)=>typeof v==='string'?v:''
const methodNames:Record<string,string>={hydroponics:'Topraksız · kapalı ortam',greenhouse:'Güneş alan sera',open_field:'Açık tarla'}
const cropColors:Record<string,string>={kohlrabi:'#24734f',lettuce:'#83a947',arugula:'#519a70',radish:'#b56b64',swiss_chard:'#b1963e',basil:'#3d8b85'}
const timelineCache=new Map<string,Promise<JsonRecord>>()
function useTimeline(request:JsonRecord,referenceOnly=false){
  const body=JSON.stringify({...request,horizon_id:'mid'})
  const endpoint=referenceOnly?'reference':'timeline',key=endpoint+body
  const [state,setState]=useState<{key:string,data?:JsonRecord,error?:string}>({key})
  useEffect(()=>{let active=true;setState({key});let pending=timelineCache.get(key)
    if(!pending){pending=fetch('/api/north/'+endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body}).then(async r=>{if(!r.ok)throw new Error('Dönem karşılaştırması alınamadı.');return await r.json() as JsonRecord});timelineCache.set(key,pending);pending.catch(()=>timelineCache.delete(key))}
    pending.then(data=>{if(active)setState({key,data})}).catch(e=>{if(active)setState({key,error:e.message})});return()=>{active=false}
  },[key,body,endpoint])
  return state.key===key?state:{key}
}

export function ClimateInputs({request}:{request:JsonRecord}){
  const year=request.target_year,scenario=request.scenario_id
  const [state,setState]=useState<{key:string,data?:JsonRecord,error?:string}>({key:''})
  const key=`${year}:${scenario}`
  useEffect(()=>{const abort=new AbortController();setState({key});const timer=setTimeout(()=>{fetch(`/api/north/climate?year=${year}&scenario_id=${scenario}`,{signal:abort.signal}).then(async r=>{const body=await r.json();if(!r.ok)throw new Error(typeof body.detail==='string'?body.detail:'İklim girdileri alınamadı.');return body}).then(data=>setState({key,data})).catch(e=>{if(e.name!=='AbortError')setState({key,error:e.message})})},250);return()=>{clearTimeout(timer);abort.abort()}},[key,year,scenario])
  const data=state.key===key?state.data:undefined,context=obj(data?.context||data),current=obj(context.ensemble),delta=obj(context.change_from_historical)
  const temperature=n(delta.mean_temperature_c),rainBase=n(obj(current.precipitation_mm).mean)-n(delta.precipitation_mm),rain=rainBase>0?n(delta.precipitation_mm)/rainBase*100:null
  return <div className="ns-climate" aria-label="Seçilen yılın otomatik iklim girdileri"><span><Icon name="sun" size={14}/>{String(year)} · kaynaklı iklim senaryosu</span>{data?<div><label>Sıcaklık farkı<b>{temperature>=0?'+':''}{number(temperature)} °C</b></label><label>Yağış farkı<b>{rain===null?'—':`${rain>=0?'+':''}${number(rain,0)}%`}</b></label><label>Donsuz dönem<b>{number(obj(current.frost_free_run_days).mean,0)} gün</b></label></div>:<p role="status">{state.key===key&&state.error||'İklim verileri yükleniyor…'}</p>}<small>1995–2014’e göre · 3 model. Seçilen yılın senaryosu; ölçülmüş hava değil.</small></div>
}

export function NorthSimulation({result,onDetail,onProducer,stale=false}:{result:JsonRecord,onDetail:(id:string)=>void,onProducer:(context?:ProducerContext)=>void,stale?:boolean}){
  const request=obj(result.request),plan=obj(result.plan),totals=obj(plan.totals),story=obj(result.decision_story),production=obj(story.production)
  const crops=list(production.crops),methods=list(production.methods),area=n(request.area_m2)
  const allocations=list(plan.allocations)
  const cropWater=(id:unknown)=>{const rows=allocations.filter(a=>a.crop_id===id);return rows.length&&rows.every(a=>typeof a.water_m3==='number')?rows.reduce((sum,a)=>sum+n(a.water_m3),0):null}
  const risk=list(story.actions).find(a=>a.id==='sensitivity')
  const selectedLabel=request.target_year?String(request.target_year):({recent:'Yakın dönem',historical:'Tarihsel',near:'2030',mid:'2050',late:'2090'} as Record<string,string>)[s(request.horizon_id)]
  if(!crops.length)return <div className="ns-no-plan" role="status"><Icon name="water"/><h2>Bu koşullarda üretim kurulamıyor.</h2><p>Soldan su kaynaklarını, enerji sınırını ve etkin ürünleri gözden geçirip simülasyonu yeniden çalıştırın.</p></div>
  return <>
    <div className="ns-decision-grid">
      <NorthWaterStrategy result={result} onDetail={onDetail}/>
      <div className="ns-production-panel"><div className="ns-production-link"><span><Icon name="seed" size={16}/><b>B · ÖNERİLEN ÜRETİM PLANI</b></span><span>Hedef: {({fresh_mass:'taze ürün',protein:'bitkisel protein',food_energy:'besin enerjisi'} as Record<string,string>)[s(request.production_purpose)]||'taze ürün'}</span></div>
        <div className="ns-main-grid">
          <section className="ns-crops"><header><h3><Icon name="seed" size={17}/>Önerilen ürün deseni <abbr title="Hangi ürünün ne kadar üretileceğini gösteren dağılım." aria-label="Ürün deseni: hangi ürünün ne kadar üretileceğini gösteren dağılım">ⓘ</abbr></h3><span>Alan payı · model hasadı</span></header><div className="ns-field" role="img" aria-label={crops.map(c=>`${s(c.name)} yüzde ${number(n(c.area_m2)/area*100)}`).join(', ')}>{crops.map(c=><i key={s(c.crop_id)} style={{width:`${n(c.area_m2)/area*100}%`,backgroundColor:cropColors[s(c.crop_id)]||'#577c51'}} title={`${s(c.name)} · alan payı %${number(n(c.area_m2)/area*100)}`}/>)}{n(totals.area_m2)<area-.01&&<i className="ns-unused" style={{width:`${(1-n(totals.area_m2)/area)*100}%`}} title="Kullanılmayan alan"/>}</div><div className="ns-crop-list">{crops.map(c=><div key={s(c.crop_id)}><i style={{background:cropColors[s(c.crop_id)]||'#577c51'}}/><b>{s(c.name)}</b><strong>%{number(n(c.area_m2)/area*100)}</strong><span>{number(c.area_m2)} m² · {number(c.production_kg,0)} kg/yıl · {cropWater(c.crop_id)===null?'Yeni su hesaplanmadı':`${number(cropWater(c.crop_id),1)} m³/yıl yeni su`} · {(Array.isArray(c.methods)?c.methods:[]).map(m=>methodNames[String(m)]).join(' + ')}</span></div>)}</div><button className="ns-inline" onClick={()=>onDetail('production')}>Ürün × yöntem × sezon ayrıntısı <Icon name="arrow" size={13}/></button></section>
          <section className="ns-methods"><header><h3><Icon name="greenhouse" size={17}/>Üretim yöntemleri <abbr title="Hidroponik: bitkilerin toprak yerine besin içeren suyla yetiştirildiği yöntem." aria-label="Hidroponik yöntemi açıklaması">ⓘ</abbr></h3></header>{methods.map(m=><div className={`ns-method ${s(m.id)}`} key={s(m.id)}><div><span>{methodNames[s(m.id)]}</span><b>%{number(n(m.area_m2)/area*100)} alan</b></div><div className="ns-track"><i style={{width:`${n(m.area_m2)/area*100}%`}}/></div></div>)}<p>Su kaynağı tesis toplamında tahsis edilir; ürünlere ayrı kaynak payı yazılmaz. Enerji gereği: {number(totals.equivalent_electricity_kwh,0)} kWh/yıl elektrik eşdeğeri.</p><button className="ns-inline" onClick={()=>onDetail('crops')}>Açık tarla adayları ve zemin sınırı <Icon name="arrow" size={13}/></button></section>
        </div>
      </div>
    </div>
    <ReferenceChange request={request}/>
    <div className="ns-pilot-note"><Icon name="energy" size={16}/><span><b>{obj(obj(result.infrastructure).energy).power_screen_status==='DESIGN_REVIEW'?'Elektrik gücü sınırını doğrula.':obj(risk?.metrics).id==='yield'?'Ölçekleme öncesi pilot verisi gerekli.':s(risk?.title)||'Yerel üretim koşullarını doğrula.'}</b> Su kaynağı, arıtma ve gerçek enerji/hasat kaydı uygulama kararı için gerekli.</span><button onClick={()=>onDetail('sensitivity')}>Kararın sınırları ↗</button></div>
    <DecisionReportButton kind="north" request={request} disabled={stale}/>
    <ProducerRecommendation context={contextFromNorth(result)} stale={stale} onOpen={onProducer}/>
    <NorthEnergyExplanation result={result}/>
    {!request.target_year&&<EvolutionSummary request={request} label={selectedLabel}/>}
    <div className="ns-basis"><span><Icon name="source" size={13}/>Model önerisi · {number(area,0)} m² planlama birimi · {request.objective==='balanced'?'Hasat + su + enerji dengesi':request.objective==='water'?'Su önceliği':'Enerji önceliği'}</span><button onClick={()=>onDetail('evidence')}>Neden bu ürünler?</button></div>
  </>
}

function ReferenceChange({request}:{request:JsonRecord}){
  const {data,error}=useTimeline(request,true),points=list(data?.points),before=points.find(p=>p.horizon_id==='baseline_2026'),after=points.find(p=>p.horizon_id===(request.target_year===2026?'baseline_2026':request.target_year?'year':request.horizon_id))
  if(!data)return <div className="ns-change" role="status">{error||'Sabit iklim referansıyla karşılaştırılıyor…'}</div>
  if(!before||!after)return <div className="ns-change">Referans karşılaştırması tamamlanamadı.</div>
  if(request.target_year===2026)return <div className="ns-change"><b>2026 model yılı · başlangıç üretim planı</b><small>Bu, ölçülmüş hava veya mevcut ekiliş değil; aynı üç iklim modelinin 2026 yılına göre koşullu üretim hesabıdır.</small></div>
  if(before.status==='infeasible'||after.status==='infeasible')return <div className="ns-change"><b>{s(before.period)} → {s(after.label)}</b><span>Bu dönemlerden birinde üretim kurulamıyor; uygulanamayan plan sıfır üretim kabul edilmez.</span></div>
  const oldCrops=list(before.crops),newCrops=list(after.crops)
  const changes=[...new Set([...oldCrops,...newCrops].map(c=>s(c.id)))].map(id=>{const old=oldCrops.find(c=>c.id===id),next=newCrops.find(c=>c.id===id);return {name:s(next?.name)||s(old?.name),delta:n(next?.share_pct)-n(old?.share_pct)}}).filter(c=>Math.abs(c.delta)>=.1).sort((a,b)=>Math.abs(b.delta)-Math.abs(a.delta))
  const a=obj(before.totals),b=obj(after.totals),oldWater=n(a.water_m3),newWater=n(b.water_m3),waterDelta=oldWater>0?(newWater/oldWater-1)*100:null
  const oldHydro=n(obj(before.method_shares_pct).hydroponics),newHydro=n(obj(after.method_shares_pct).hydroponics)
  const energyDelta=n(a.equivalent_electricity_kwh)>0?(n(b.equivalent_electricity_kwh)/n(a.equivalent_electricity_kwh)-1)*100:null
  return <div className="ns-change" aria-label="Sabit iklim referansına göre değişim"><div className="ns-reference-title"><b>2026 model yılına göre değişim</b><span>{s(before.period)} → {s(after.label)}</span></div><div><span>{changes.length?changes.slice(0,2).map(c=>`${c.name} ${c.delta>0?'+':''}${number(c.delta)} puan`).join(' · '):'Ürün oranları aynı kaldı.'}</span><span>Topraksız üretim %{number(oldHydro)} → %{number(newHydro)}</span><strong className={waterDelta!==null&&waterDelta>0?'ns-increase':'ns-decrease'}>{waterDelta===null?'Referans su ihtiyacı sıfır; yüzde karşılaştırılmaz.':Math.abs(waterDelta)<.1?'Yeni su ihtiyacı aynı düzeyde.':`Yeni su ihtiyacı %${number(Math.abs(waterDelta))} ${waterDelta>0?'arttı':'azaldı'}.`}</strong><span>{energyDelta===null?'Enerji yüzdesi karşılaştırılamıyor.':Math.abs(energyDelta)<.1?'Enerji gereği aynı düzeyde.':`Enerji gereği %${number(Math.abs(energyDelta))} ${energyDelta>0?'arttı':'azaldı'}.`}</span></div><small>Aynı alan, amaç ve altyapı. 2026 ve seçili yıl aynı CMIP6 model ailesinin tekil model yıllarıdır; ölçülmüş hava veya bugünkü ekiliş değildir. Fark koşullu simülasyon farkıdır. Enerji: elektrik eşdeğeri.</small></div>
}

function EvolutionSummary({request,label}:{request:JsonRecord,label:string}){
  const {data,error}=useTimeline(request),points=list(data?.points),chosen=points.find(p=>p.horizon_id===(request.target_year?'year':request.horizon_id)),base=points.find(p=>p.horizon_id==='recent')
  const valid=chosen&&base&&chosen.status!=='infeasible'&&base.status!=='infeasible',before=n(obj(base?.method_shares_pct).greenhouse),after=n(obj(chosen?.method_shares_pct).greenhouse)
  const sameCrops=valid&&[...new Set([...list(chosen.crops),...list(base.crops)].map(c=>s(c.id)))].every(id=>Math.abs(n(list(chosen.crops).find(c=>c.id===id)?.share_pct)-n(list(base.crops).find(c=>c.id===id)?.share_pct))<.1)
  return <section className="ns-evolution"><header><h3><Icon name="north" size={17}/>Gelecek değiştikçe plan nasıl uyarlanıyor?</h3><span>Aynı kaynak koşulları · {request.scenario_id==='ssp585'?'yüksek':'orta'} emisyon</span></header>{!data?<p role="status">{error||'Dönemler karşılaştırılıyor…'}</p>:<><div className="ns-year-bars">{points.filter(p=>!['historical','recent'].includes(s(p.horizon_id))).map(p=><div key={s(p.horizon_id)} className={p.horizon_id===(request.target_year?'year':request.horizon_id)?'selected':''}><b>{s(p.label)}</b>{p.status==='infeasible'?<span>Üretim kurulamıyor</span>:<><div className="ns-track"><i style={{width:`${n(obj(p.method_shares_pct).hydroponics)}%`}}/><i className="greenhouse" style={{width:`${n(obj(p.method_shares_pct).greenhouse)}%`}}/><i className="open-field" style={{width:`${n(obj(p.method_shares_pct).open_field)}%`}}/></div><span>Sera %{number(obj(p.method_shares_pct).greenhouse)} · topraksız %{number(obj(p.method_shares_pct).hydroponics)}</span><span className="ns-future-water">Depodan karşılanan: %{number(p.stored_share_pct)}</span></>}</div>)}</div><p>{valid?<><b>{s(base.label)} → {label}:</b> {Math.abs(after-before)<.1?'Sera payı korunuyor.':`Sera payı %${number(before)} → %${number(after)} ${after>before?'artıyor':'azalıyor'}.`} {sameCrops?`Ürün oranları korunuyor. Depolanan suyun katkısı %${number(base?.stored_share_pct)} → %${number(chosen?.stored_share_pct)}.`:'Ürün dağılımı da değişiyor; ayrıntılı karşılaştırmayı açabilirsiniz.'}</>: 'Dönemlerin uygulanabilirliği farklı; üretilemeyen plan sıfır üretim gibi karşılaştırılmaz.'}</p></>}</section>
}
