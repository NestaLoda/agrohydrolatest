import {Icon, list, number, obj} from '../ui'
import type {JsonRecord} from '../api'

const v=(x:unknown)=>typeof x==='number'&&Number.isFinite(x)?x:0
const t=(x:unknown)=>typeof x==='string'?x:''
const months=['Oca','Şub','Mar','Nis','May','Haz','Tem','Ağu','Eyl','Eki','Kas','Ara']
const sourceNames:Record<string,string>={stored_precipitation:'Depolanan yağış / kar',desalinated_seawater:'Arıtılmış deniz',allocated_freshwater:'Ayrılan yerel tatlı su'}

export default function NorthWaterStrategy({result,onDetail}:{result:JsonRecord,onDetail:(id:string)=>void}){
  const story=obj(result.decision_story),water=obj(story.water_security),plan=obj(result.plan),totals=obj(plan.totals)
  const sources=list(water.sources).filter(row=>v(row.m3)>1e-7)
  const monthly=list(plan.monthly),critical=obj(water.critical_month),backup=obj(water.backup)
  const stored=sources.find(row=>row.id==='stored_precipitation'),sea=sources.find(row=>row.id==='desalinated_seawater')
  const maxDemand=Math.max(0.01,...monthly.map(row=>v(row.demand_m3)))
  const dailyBasis=critical.basis==='MAX_MODEL_CLIMATOLOGICAL_MONTH_FROM_DAILY_REPLAY'
  const advice:{text:string;why:string}[]=[]
  if(water.source_balance_status==='INCONSISTENT')advice.push({text:'Kaynak toplamı ve yeni su gereği eşleşmiyor; bu planı uygulama.',why:'Hesaplanan kaynak kapanışı tutarsız.'})
  if(typeof critical.month==='number')advice.push({text:`${t(critical.label)} için ${number(critical.backup_m3)} m³ yedek su erişimini planla.`,why:dailyBasis?'Günlük tekrarların aylık ortalamasında çatı/depo sonrası en yüksek yedek su gereği. Karşılanmamış nihai açık değil.':'Aylık ortalama planda çatı/depo sonrası en yüksek yedek kaynak gereği.'})
  if(backup.worst_year_is_first_modeled_year===true)advice.push({text:'İlk üretim dönemi için depo dolumu veya yedek kaynağı ayrıca doğrula.',why:'En yüksek yıllık yedek gereği, boş depoyla başlayan ilk model yılında oluştu; tek başına kuraklık kanıtı değil.'})
  if(v(sea?.m3)>0)advice.push({text:`Bu planda ${number(sea?.m3)} m³/yıl deniz suyu arıtımı tahsis edildi.`,why:`Arıtma elektriği ${number(totals.treatment_electricity_kwh,0)} kWh/yıl; kaynak suyu niteliği ve enerji erişimi yerelde doğrulanmalı.`})
  else advice.push({text:'Bu planda deniz suyundan arıtılmış su tahsis edilmiyor.',why:'Mevcut ortak optimizasyonun seçtiği deniz suyu tahsisi sıfır; PWN gözlemi üretim kararını zorunlu olarak değiştirmez.'})
  if(!advice.length&&v(stored?.m3)>0)advice.push({text:'Hesaplanan yağış/kar tahsisini üretim takvimiyle birlikte işlet.',why:'Model yalnız seçilen toplama alanı ve depo kapasitesi altında bu suyu tahsis etti.'})
  return <section className="nw-strategy" aria-label="Su yönetimi planı">
    <header><div><span><Icon name="water" size={16}/>A · SU YÖNETİMİ PLANI</span><h2>Üretim için suyu nasıl sağlayacağız?</h2></div><button onClick={()=>onDetail('water')}>Su ayrıntısı <Icon name="arrow" size={14}/></button></header>
    <div className="nw-demand"><div><small>YILLIK YENİ SU GEREĞİ</small><b>{number(water.annual_demand_m3,1)} <em>m³/yıl</em></b></div><p>Üretim sistemine dışarıdan sağlanması gereken yeni su. İç devridaim ikinci kez kaynak sayılmaz.</p></div>
    <div className="nw-source-summary" aria-label="Yıllık hesaplanan su kaynağı tahsisi"><b>Bu su nereden karşılanıyor?</b>{sources.length?sources.map(row=><div key={t(row.id)}><span><i className={t(row.id)}/>{sourceNames[t(row.id)]||t(row.label)}</span><strong>{number(row.m3,1)} m³ <small>· %{number(row.share_pct,0)}</small></strong></div>):<p>Bu koşullarda kullanılabilir yeni su tahsisi hesaplanmadı.</p>}</div>
    <div className="nw-season"><div className="nw-season-heading"><Icon name="snow" size={15}/><b>Hangi ayda zorlanıyoruz?</b><strong>{t(critical.label)||'Yedek gereği yok'}</strong></div>
      <div className="nw-months" role="img" aria-label={monthly.map(row=>`${months[v(row.month)-1]}: ihtiyaç ${number(row.demand_m3,2)} m³, depodan ${number(row.stored_water_used_m3,2)} m³, tatlı su ${number(row.freshwater_m3,2)} m³, arıtılmış deniz ${number(row.desalinated_m3,2)} m³`).join('; ')}>
        {monthly.map(row=>{const month=v(row.month),demand=v(row.demand_m3),storedUse=v(row.stored_water_used_m3),fresh=v(row.freshwater_m3),desal=v(row.desalinated_m3);return <div key={month} className={month===critical.month?'critical':''} title={`${months[month-1]} · ihtiyaç ${number(demand,2)} · depodan ${number(storedUse,2)} · tatlı su ${number(fresh,2)} · arıtılmış ${number(desal,2)} m³`}><div className="nw-month-columns"><i className="nw-demand-bar" style={{height:`${demand/maxDemand*100}%`}}/><span className="nw-source-stack" style={{height:`${(storedUse+fresh+desal)/maxDemand*100}%`}}><i className="stored_precipitation" style={{height:`${storedUse/Math.max(storedUse+fresh+desal,.000001)*100}%`}}/><i className="allocated_freshwater" style={{height:`${fresh/Math.max(storedUse+fresh+desal,.000001)*100}%`}}/><i className="desalinated_seawater" style={{height:`${desal/Math.max(storedUse+fresh+desal,.000001)*100}%`}}/></span></div><span>{months[month-1]}</span></div>})}
      </div>
      <div className="nw-legend"><span><i className="demand"/>Yeni su gereği</span><span><i className="stored_precipitation"/>Depodan</span><span><i className="allocated_freshwater"/>Tatlı su</span><span><i className="desalinated_seawater"/>Arıtılmış</span></div>
      <small className="nw-critical-definition">{critical.month?`${t(critical.label)}: ${dailyBasis?'günlük tekrarların aylık ortalamasında':'aylık ortalama planda'} çatı/depo sonrası en yüksek yedek su gereği; nihai karşılanmamış talep değil.`:'Sınanan koşullarda pozitif yedek su gereği belirlenmedi.'} Sütunlar aylık plan tahsisidir.</small>
    </div>
    <div className="nw-advice"><b>Bu senaryoda su yönetimi önerisi</b>{advice.slice(0,3).map(item=><details key={item.text}><summary>{item.text}<span>Neden?</span></summary><p>{item.why}</p></details>)}</div>
    <small className="nw-caption">Miktarlar seçilen toplama, depo ve tahsis koşullarının model sonucudur; ölçülmüş yerel su hakkı değildir. {typeof obj(water.storage).configured_m3==='number'?`Seçili depo ${number(obj(water.storage).configured_m3)} m³; asgari boyut hesabı değildir.`:''}</small>
  </section>
}
