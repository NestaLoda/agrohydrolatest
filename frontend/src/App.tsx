import { useCallback, useEffect, useState } from 'react'
import { api, type Overview, type Transfer, type JsonRecord } from './api'
import type { PlanningSession, SimulationRequest } from './planning'
import { Icon, Notice, obj, list } from './ui'
import Simulation from './workspaces/Simulation'
import NorthConsole from './workspaces/NorthConsole'
import PatternField from './workspaces/PatternField'
import ResearchMission from './components/ResearchMission'
import Pwn from './workspaces/Pwn'
import Evidence from './workspaces/Evidence'
import ProducerSupport from './components/ProducerSupport'
import RegionGlobePicker from './components/RegionGlobePicker'
import JuryDemo from './JuryDemo'
import './decision-refinement.css'
import type {ProducerContext} from './components/ProducerRecommendation'

const workspaces=[{id:'turkiye',title:'BUGÜN / TÜRKİYE',icon:'layers'},{id:'north',title:'GELECEK / KUZEY',icon:'compare'},{id:'pwn',title:'SAHA / PWN',icon:'wave'},{id:'evidence',title:'KANIT / VERİ',icon:'source'}]
function initialWorkspace(){const hash=location.hash.slice(1);return hash==='pwn'||hash==='evidence'?hash:'simulation'}
export default function App(){
  const [producerOpen,setProducerOpen]=useState(false)
  const [producerContext,setProducerContext]=useState<ProducerContext|undefined>()
  function openProducer(context?:ProducerContext){setProducerContext(context);setProducerOpen(true)}
  const [northFieldRequest,setNorthFieldRequest]=useState(0)
  const [active,setActive]=useState('simulation'),[overview,setOverview]=useState<Overview|null>(null),[benchmarks,setBenchmarks]=useState<Transfer|null>(null),[northContext,setNorthContext]=useState<JsonRecord|null>(null),[northEvidence,setNorthEvidence]=useState<JsonRecord|null>(null)
  const [automaticNorth,setAutomaticNorth]=useState<JsonRecord|null>(null),[automaticBusy,setAutomaticBusy]=useState(false),[automaticError,setAutomaticError]=useState('')
  const [sessions,setSessions]=useState<Record<string,PlanningSession>>({}),[region,setRegion]=useState(location.hash==='#north'?'longyearbyen':'konya'),[turkeyRegion,setTurkeyRegion]=useState('konya')
  const [contextLoading,setContextLoading]=useState(false),[contextError,setContextError]=useState(''),[loadError,setLoadError]=useState(''),[drawer,setDrawer]=useState(false),[fieldTab,setFieldTab]=useState('research'),[busy,setBusy]=useState(false),[calcError,setCalcError]=useState('')
  const [fieldOpen,setFieldOpen]=useState(initialWorkspace()==='pwn')
  const [northFieldOpen,setNorthFieldOpen]=useState(false)
  const [juryOpen,setJuryOpen]=useState(false),[juryMode,setJuryMode]=useState<'turkiye'|'north'>('turkiye'),[juryRegion,setJuryRegion]=useState('konya')
  const juryContext=useCallback((mode:'turkiye'|'north',id:string)=>{setJuryMode(mode);setJuryRegion(id)},[])
  const [pwnVisited,setPwnVisited]=useState(initialWorkspace()==='pwn')
  const session=sessions[region]||null,north=region==='longyearbyen'
  const stale=!!session?.result&&JSON.stringify(session.scenario)!==JSON.stringify(session.submitted)
  function navigate(id:string){if(id==='north')selectRegion('longyearbyen');if(id==='turkiye')selectRegion(turkeyRegion);setActive('simulation');if(id==='evidence')setDrawer(true);if(id==='pwn')setFieldOpen(true);if(id==='pwn')setPwnVisited(true);location.hash=id;window.scrollTo({top:0,behavior:'instant'})}
  function selectRegion(id:string){if(id!=='longyearbyen')setTurkeyRegion(id);setRegion(id);setCalcError('')}
  function edit(next:SimulationRequest,reason:string){const nextScenario={...next,overrides:[...new Set([...next.overrides,reason])].slice(-100)};setSessions(old=>({...old,[region]:{...old[region],scenario:nextScenario}}))}
  const climateId=session?.scenario.climate_context_id||'ec_earth_2030_2049'
  const nasaScenario=climateId.includes('ssp585')?'ssp585':'ssp245'
  const nasaRow=list(obj(northEvidence?.climate_2035).scenarios).find(s=>s.scenario===nasaScenario)
  const selectedNorthContext=climateId.startsWith('nasa')?{...northContext,model:'ACCESS-CM2',scenario:nasaScenario,context_only:true,baseline:{period:'Tek model yılı; tarihsel eş dönem yok'},future:{period:`2035 · ${nasaScenario.toUpperCase()}`,mean_annual_temperature_c:nasaRow?.annual_mean_temperature_c,mean_annual_gdd5_degree_days:nasaRow?.gdd_base_5_c,mean_annual_frost_free_run_days:nasaRow?.longest_frost_free_run_days,mean_annual_precipitation_mm:nasaRow?.annual_precipitation_mm},source_record:nasaRow,monthly:obj(obj(northEvidence?.climate_2035).monthly)[nasaScenario]}:northContext
  function climateSelect(id:'ec_earth_2030_2049'|'nasa_ssp245_2035'|'nasa_ssp585_2035'){
    if(!session)return
    const label=id==='ec_earth_2030_2049'?'2030–2049 · EC_Earth3P_HR':`2035 · ACCESS-CM2 · ${id.includes('585')?'SSP585':'SSP245'}`
    edit({...session.scenario,climate_context_id:id,period_label:label+' · iklim kanıtı',climate_scenario_label:label+'; kaynaklı ön tarama. Yerel su/verim/enerji katsayıları doğrulanmadı.'},'Kaynaklı iklim bağlamı seçildi: '+id)
  }
  function reset(){if(session)setSessions(old=>({...old,[region]:{...old[region],scenario:structuredClone(session.context.default_scenario),...(session.scenario.mode==='turkiye'?{result:null,submitted:null}:{})}}));setCalcError('')}
  async function calculate(){if(!session)return;setBusy(true);setCalcError('');const request=structuredClone(session.scenario),target=region;try{const result=await api.simulate(request);setSessions(old=>({...old,[target]:{...old[target],result,submitted:request}}))}catch(e){setCalcError(e instanceof Error?e.message:'Simülasyon tamamlanamadı')}finally{setBusy(false)}}
  useEffect(()=>{let live=true;Promise.allSettled([api.overview(),api.benchmarks(),api.northContext(),api.northEvidence()]).then(([o,b,n,e])=>{if(!live)return;if(o.status==='fulfilled')setOverview(o.value);else setLoadError('Ana veri kaydı yüklenemedi.');if(b.status==='fulfilled')setBenchmarks(b.value);if(n.status==='fulfilled')setNorthContext(n.value);if(e.status==='fulfilled')setNorthEvidence(e.value)});return()=>{live=false}},[])
  useEffect(()=>{if(region==='longyearbyen'){setContextLoading(false);return;}if(sessions[region]){setContextLoading(false);setContextError('');return;}let live=true;setContextLoading(true);setContextError('');api.planningContext(region).then(context=>{if(!live)return;const initial=structuredClone(context.default_scenario);setSessions(old=>({...old,[region]:{context,scenario:initial,result:null,submitted:null}}))}).catch(e=>{if(live)setContextError(e instanceof Error?e.message:'Planlama bağlamı yüklenemedi')}).finally(()=>{if(live)setContextLoading(false)});return()=>{live=false}},[region])
  useEffect(()=>{const onHash=()=>{const hash=location.hash.slice(1);if(hash==='north')selectRegion('longyearbyen');if(hash==='turkiye')selectRegion(turkeyRegion);const id=initialWorkspace();setActive('simulation');if(id==='pwn'){setPwnVisited(true);setFieldOpen(true)}if(id==='evidence')setDrawer(true)};window.addEventListener('hashchange',onHash);return()=>window.removeEventListener('hashchange',onHash)},[turkeyRegion])
  useEffect(()=>{if(!drawer&&!fieldOpen)return;const prior=document.activeElement as HTMLElement|null,dialog=document.querySelector<HTMLElement>(drawer?'.evidence-drawer':'.field-drawer'),overflow=document.body.style.overflow;document.body.style.overflow='hidden';dialog?.querySelector<HTMLElement>('button')?.focus();const key=(e:KeyboardEvent)=>{if(e.key==='Escape'){setDrawer(false);setFieldOpen(false);return}if(e.key!=='Tab'||!dialog)return;const nodes=[...dialog.querySelectorAll<HTMLElement>('button,a[href],summary,input,select,textarea')].filter(el=>el.getClientRects().length),first=nodes[0],last=nodes[nodes.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last?.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first?.focus()}};document.addEventListener('keydown',key);return()=>{document.removeEventListener('keydown',key);document.body.style.overflow=overflow;prior?.focus()}},[drawer,fieldOpen])
  useEffect(()=>{const header=document.querySelector<HTMLElement>(".workbench-topbar");if(!header)return;const sync=()=>document.documentElement.style.setProperty("--workbench-header-height",`${header.getBoundingClientRect().height}px`);const observer=new ResizeObserver(sync);observer.observe(header);sync();return()=>observer.disconnect()},[])
  return <div className="dashboard lab-app"><a className="skip-link" href="#main">İçeriğe geç</a>
    <div className="dashboard-body"><header className="global-bar workbench-topbar instrument-topbar">
      <div className="instrument-brand"><Icon name="wave" size={24}/><span>DESENDEN DENGEYE<small>SU / ÜRETİM KARAR DESTEK SİSTEMİ</small></span></div>
      <nav className="instrument-modes" aria-label="Planlama modu">
        <button aria-label="BUGÜN / TÜRKİYE" aria-pressed={juryOpen?juryMode==='turkiye':!fieldOpen&&!north&&!producerOpen} onClick={()=>{if(!juryOpen)navigate('turkiye')}}><Icon name="globe" size={15}/>BUGÜN / TÜRKİYE</button>
        <div className="north-nav-branch">
          <button aria-label="GELECEK / KUZEY" aria-pressed={juryOpen?juryMode==='north':!fieldOpen&&!northFieldOpen&&north&&!producerOpen} onClick={()=>{if(!juryOpen)navigate('north')}}><Icon name="north" size={15}/>GELECEK / KUZEY</button>
          <button className="north-nav-child" aria-label="Tarım Güvencesi" aria-pressed={!juryOpen&&producerOpen} onClick={()=>{if(!juryOpen)openProducer()}}><Icon name="seed" size={15}/>TARIM GÜVENCESİ</button>
        </div>
        <button aria-pressed={!juryOpen&&(fieldOpen||northFieldOpen)} onClick={()=>{if(!juryOpen){navigate('north');setNorthFieldRequest(x=>x+1)}}}><Icon name="sensor" size={15}/>SAHA GÜNCELLEMESİ</button>
      </nav>
      <button className="jury-mode-trigger" aria-pressed={juryOpen} title={juryOpen?`Jüri gösterimi: ${juryRegion}`:'Rehberli canlı önizleme'} onClick={()=>setJuryOpen(open=>!open)}><Icon name="layers" size={15}/>JÜRİ MODU</button>
      <div className="context-actions" hidden={north}><button className="icon-button" aria-label="Senaryoyu kaydet" title="Senaryoyu kaydet" onClick={()=>{if(!session)return;const url=URL.createObjectURL(new Blob([JSON.stringify({classification:'USER_SCENARIO',scenario:session.scenario},null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=`senaryo-${region}.json`;a.click();URL.revokeObjectURL(url)}}><Icon name="source" size={16}/></button><button className="button small evidence-button" onClick={()=>setDrawer(true)}>Kanıt</button></div>
    </header>
    <div className="instrument-context-bar" hidden={juryOpen}><RegionGlobePicker north={north} region={region} sites={overview?.sites||[]} onSelect={selectRegion}/>{north?<span>Longyearbyen çevresi · 0,25° iklim hücresi · çok modelli araştırma hesabı</span>:<span>{String(session?.context.region.year||'')} ürün deseni · {String(session?.context.climate_context.period||'')} hava koşulları</span>}<span className={`instrument-run-status ${stale?'stale':''}`} aria-live="polite">{north?'GELECEK ÜRETİM SİMÜLASYONU':busy?'Hesaplanıyor…':stale?'SENARYO DEĞİŞTİ · HESAPLA':session?.result?'ÖNERİ HAZIR':'MEVCUT DURUM'}</span></div>
    <main id="main" className="main" tabIndex={-1} hidden={juryOpen}>{loadError&&<Notice warn>{loadError}</Notice>}<div hidden={active!=='simulation'}>{north?<NorthConsole fieldRequested={northFieldRequest} onFieldChange={setNorthFieldOpen} onProducer={openProducer}/>:<Simulation onProducer={openProducer} session={session} overview={overview} benchmarks={benchmarks} northContext={selectedNorthContext} northEvidence={northEvidence} onEdit={edit} onReset={reset} onRun={()=>void calculate()} busy={busy} error={calcError||contextError} loading={contextLoading} automaticNorth={automaticNorth} automaticBusy={automaticBusy} automaticError={automaticError} onResearch={()=>{setFieldOpen(true);setPwnVisited(true);setFieldTab('research')}}/>}</div>
    </main></div>
    {juryOpen&&<JuryDemo overview={overview} benchmarks={benchmarks} onContext={juryContext} onExit={()=>setJuryOpen(false)}/>}
    {!juryOpen&&producerOpen&&<ProducerSupport context={producerContext} onClose={()=>setProducerOpen(false)}/>}
    {!juryOpen&&pwnVisited&&<div hidden={!fieldOpen} className="drawer-overlay" onClick={e=>{if(e.currentTarget===e.target)setFieldOpen(false)}}><section className="field-drawer" role="dialog" aria-modal="true" aria-label="Saha girdisi güncelleme"><div className="drawer-head"><span>MODEL → SAHA GİRDİSİ → AYNI OPTİMİZASYON MOTORU</span><button className="icon-button" aria-label="Saha çekmecesini kapat" onClick={()=>setFieldOpen(false)}><Icon name="close"/></button></div><div className="workspace-tabs"><button aria-pressed={fieldTab==='research'} onClick={()=>setFieldTab('research')}>Araştırma / karar belirsizliği</button><button aria-pressed={fieldTab==='update'} onClick={()=>setFieldTab('update')}>PRE-TASE / gözlem sonrası</button><button aria-pressed={fieldTab==='profile'} onClick={()=>setFieldTab('profile')}>PWN profil / CSV</button></div>{fieldOpen&&fieldTab==='research'&&<ResearchMission session={session} onCompare={()=>setFieldTab('update')}/>}<div hidden={fieldTab!=='profile'}><Pwn/></div><div hidden={fieldTab!=='update'}><PatternField session={session} onNorth={()=>{navigate('north');setFieldOpen(false)}}/></div></section></div>}
    {!juryOpen&&drawer&&<div className="drawer-overlay" onClick={e=>{if(e.currentTarget===e.target)setDrawer(false)}}><section className="evidence-drawer" role="dialog" aria-modal="true" aria-label="Kanıt çekmecesi"><div className="drawer-head"><span>KARARIN DAYANAKLARI</span><button className="icon-button" aria-label="Kanıt çekmecesini kapat" onClick={()=>setDrawer(false)}><Icon name="close"/></button></div><Evidence overview={overview}/></section></div>}</div>
}
