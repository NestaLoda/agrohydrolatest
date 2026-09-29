import type {PlanningContext,SimulationResult} from '../planning'
import {Icon,number,str} from '../ui'
import {effectiveWaterBudget,waterPressure} from '../waterPressure'
import './water-pressure.css'

type Props={context:PlanningContext;result:SimulationResult|null;stale?:boolean}
const finite=(value:unknown):value is number=>typeof value==='number'&&Number.isFinite(value)

export default function TurkeyDecisionSupport({context,result,stale=false}:Props){
  // Before calculation the live simulator owns the climate → pressure → action story.
  if(!result)return null
  const q=result.request,plan=result.optimized,land=q.land_area_ha
  const budget=effectiveWaterBudget(q.water_sources)
  const partial=!!result.regional_scope||result.current.totals.water_m3===null||!!plan&&plan.totals.water_m3===null
  const currentWater=partial?result.current.totals.known_water_m3:result.current.totals.water_m3
  const plannedWater=partial?plan?.totals.known_water_m3:plan?.totals.water_m3
  const pressure=waterPressure(finite(currentWater)?currentWater:null,budget,partial)
  let summary:string,recommendation:string,reason:string,action:string
  let tone='neutral',verdict='Bu koşullarda bütün hedefler birlikte karşılanamıyor'

  if(!plan){
    tone=result.status==='infeasible'?'bad':'neutral'
    const disabledMinimum=q.crops.find(c=>!c.enabled&&c.min_production_kg>0)
    const name=disabledMinimum?str(context.crop_catalog.find(c=>c.crop_id===disabledMinimum.crop_id)?.name_tr):''
    const excess=pressure.percent!==null?pressure.percent-100:null
    summary=pressure.zeroBudget&&pressure.status==='over'?'Sulama suyu sınırı sıfır, seçilen desen ise sulama gerektiriyor.':excess!==null&&excess>0?`Seçilen desen sulama suyu sınırını %${number(excess,1)} aşıyor.`:'Üretim hedefleri, izin verilen ürünler ve kaynak sınırları birlikte karşılanamadı.'
    recommendation='Bu koşul için yeni bir ürün dağılımı önerilmiyor.'
    reason=disabledMinimum?`${name} kapatılmış, fakat bu ürünün en az üretim hedefi korunmuş.`:pressure.status==='over'?'Mevcut paylarla sulama suyu sınırı yetmiyor; üretim hedefleri de aynı anda korunmak zorunda.':'Hesap, korunacak en az üretim miktarlarını veya kaynak sınırlarını kendiliğinden gevşetmez.'
    action=disabledMinimum?`${name} için ürün izni ile en az üretim hedefini uyumlu hale getirip yeniden hesaplayın.`:pressure.status==='over'?'Sulama suyu sınırıni gerçek tahsise göre kontrol edin; ardından zorunlu üretim paylarını gözden geçirip yeniden hesaplayın.':'Ürün izinlerini ve zorunlu üretim paylarını kontrol edip yeniden hesaplayın.'
  }else{
    const changes=plan.crops.map(c=>({...c,delta:c.area_ha-c.current_area_ha})).filter(c=>Math.abs(c.delta)>Math.max(.01,land*.0005))
    const increase=changes.filter(c=>c.delta>0).sort((a,b)=>b.delta-a.delta)[0]
    const decrease=changes.filter(c=>c.delta<0).sort((a,b)=>a.delta-b.delta)[0]
    const shifts=[decrease,increase].filter(c=>c!==undefined).map(c=>`${c.name_tr} payı${stale?'':c.delta>0?'nı artırın':'nı azaltın'}: %${number(c.current_area_ha/Math.max(land,1)*100,1)} → %${number(c.area_share_pct,1)}`)
    const held=plan.crops.filter(c=>c.held_for_missing_water).map(c=>c.name_tr)
    const saving=finite(currentWater)&&finite(plannedWater)?currentWater-plannedWater:null
    const savingPercent=saving!==null&&finite(currentWater)&&currentWater>0?saving/currentWater*100:null
    const unassigned=Math.max(0,land-plan.totals.open_field_area_ha)/Math.max(land,1)*100
    const proposedPressure=waterPressure(finite(plannedWater)?plannedWater:null,budget,partial)
    const visiblyChanged=savingPercent!==null&&Math.abs(savingPercent)>=.05
    tone=partial||!visiblyChanged?'neutral':savingPercent!>0?'good':'bad'
    verdict=partial?(held.length?`${held.join(', ')} korunuyor; öneri diğer ürünleri kapsıyor`:'Su sonucu hesabı tamamlanan ürünlerle sınırlı'):visiblyChanged?savingPercent!>0?'Aynı koşullarda daha az su isteyen desen':'Daha fazla su isteyen desen':'Su ihtiyacında belirgin değişim yok'
    summary=visiblyChanged?`${partial?'Kapsamdaki ürünlerde ':''}%${number(Math.abs(savingPercent!),1)} ${savingPercent!>0?'daha az':'daha fazla'} su ihtiyacı; ürün dağılımı değişiminin ek etkisi. İklim ve sulama verimi aynı.`:saving!==null?'Seçilen ve önerilen desenin su ihtiyacı bu koşullarda benzer.':'Bu sonuçtan bölgenin toplam su yeterliliği çıkarılamaz.'
    if(currentWater===0&&finite(plannedWater)&&plannedWater>0){
      tone=partial?'neutral':'bad'
      if(!partial)verdict='Yeni üretim sulama gerektiriyor'
      summary=`${partial?'Kapsamdaki ürünlerde ':''}Başlangıç su ihtiyacı sıfır olduğu için yüzde farkı hesaplanmaz; önerilen üretim sulama gerektiriyor.`
    }
    if(unassigned>=.05)summary+=` Üretime ayrılmayan alan: %${number(unassigned,1)}.`
    recommendation=shifts.length?`${stale?'Önceki senaryoda: ':''}${shifts.join('; ')}.`:'Mevcut ürün payları korunuyor; belirgin bir dağılım değişimi önerilmiyor.'

    const increaseWater=increase?result.crop_water.find(c=>c.crop_id===increase.crop_id)?.gross_water_m3_ha:null
    const decreaseWater=decrease?result.crop_water.find(c=>c.crop_id===decrease.crop_id)?.gross_water_m3_ha:null
    const relativeWater=increase&&decrease&&finite(increaseWater)&&finite(decreaseWater)&&decreaseWater>0?(1-increaseWater/decreaseWater)*100:null
    reason=relativeWater!==null&&relativeWater>=.05?`Birim alan su ihtiyacı, ${increase!.name_tr} için ${decrease!.name_tr} değerinden %${number(relativeWater,1)} düşük; her ürün için belirlenen en az üretim miktarı korunuyor.`:'Önce ekili alanı mümkün olduğunca koruyan, ardından daha az su isteyen dağılım seçiliyor.'

    const binding=result.constraints.filter(c=>c.binding&&c.capacity>0)
    const minimumCrop=decrease&&binding.some(c=>c.id===`crop_min_output_${decrease.crop_id}`)?decrease:plan.crops.find(c=>binding.some(b=>b.id===`crop_min_output_${c.crop_id}`))
    const before=minimumCrop?result.current.crops.find(c=>c.crop_id===minimumCrop.crop_id)?.production_kg:null
    const minimum=minimumCrop?q.crops.find(c=>c.crop_id===minimumCrop.crop_id)?.min_production_kg:null
    const minimumPercent=finite(minimum)&&finite(before)&&before>0?minimum/before*100:null
    if(held.length)action=`${held.join(', ')} için sulama hesabı tamamlanmadan bütün bölgenin su yeterliliği hakkında sonuç çıkarmayın.`
    else if(proposedPressure.status==='over'){
      tone='bad';verdict='Önerilen ihtiyaç sulama suyu sınırını aşıyor'
      action='Öneri hâlâ su sınırına sığmıyor; gerçek su tahsisini ve zorunlu üretim paylarını kontrol ederek yeniden hesaplayın.'
    }else if(minimumCrop&&minimumPercent!==null)action=`${minimumCrop.name_tr} için seçilen desendeki üretimin en az %${number(minimumPercent,1)} düzeyi korunuyor; bu hedefi değiştirmeden payını daha da azaltmayın.`
    else if(binding.some(c=>c.id.startsWith('water_')))action='Sulama suyu sınırı tamamen kullanılıyor; ek üretim planlamadan önce kullanılabilir suyu doğrulayın.'
    else action='Önerilen payları gerçek su tahsisi ve işletme koşullarıyla doğrulayın; daha az su ihtiyacı tek başına kâr artışı değildir.'
  }

  if(stale){tone='neutral';verdict='Önceki senaryonun sonucu';action='İklim veya ürün payları değişti; bu öneriyi kullanmadan önce en uygun deseni yeniden hesaplayın.'}

  return <section className={`turkey-decision-support verdict-${tone}`} aria-label="Karar desteği">
    <header className="decision-support-heading"><h2><Icon name={tone==='bad'?'close':tone==='good'?'check':'compare'} size={17}/> Karar vericiye eylem</h2><small className="decision-support-status">{stale?'ÖNCEKİ SENARYO':plan?partial?'SINIRLI KAPSAM':'HESAPLANAN ÖNERİ':'HEDEFLER UYUŞMUYOR'}</small></header>
    <p className="decision-primary-action">{recommendation}</p>
    <p className="decision-guardrail"><Icon name={tone==='bad'?'close':'source'} size={14}/>{action}</p>
    <details className="decision-action-details"><summary>Detaylı eylem hesabı</summary>
      <p className="decision-support-summary"><strong className="decision-support-verdict">{verdict}</strong> · {summary}</p><p><b>Neden bu karar?</b> {reason}</p>
      <p>Karşılaştırma aynı koşunun seçilen ve önerilen deseni arasındadır. {String(context.region.year)} yılı il kayıtları başlangıç dayanağıdır; su ve üretim sonuçları model hesabıdır.</p>
      <p>{partial?'Hesabı tamamlanan ürünlerde ':''}Seçilen su: {number(currentWater,1)} m³ · Önerilen su: {number(plannedWater,1)} m³ · Sulama suyu sınırı: {number(budget,1)} m³{pressure.status==='over'?` · Seçilen desenin eksik kalan suyu: ${number(pressure.deficitM3,1)} m³`:''}.</p>
      {plan?<div className="table-scroll"><table><thead><tr><th>Ürün</th><th>Seçilen → önerilen alan</th><th>Birim alan su ihtiyacı</th><th>Korunacak en az / seçilen üretim</th></tr></thead><tbody>{plan.crops.map(c=>{
        const before=result.current.crops.find(row=>row.crop_id===c.crop_id),minimum=q.crops.find(row=>row.crop_id===c.crop_id)?.min_production_kg,water=result.crop_water.find(row=>row.crop_id===c.crop_id)?.gross_water_m3_ha
        return <tr key={c.crop_id}><th>{c.name_tr}{c.held_for_missing_water?' · alan sabit':''}</th><td>{number(c.current_area_ha,2)} → {number(c.area_ha,2)} ha</td><td>{finite(water)?`${number(water,2)} m³/ha`:'Sulama hesabı tamamlanmalı'}</td><td>{number(minimum,0)} / {number(before?.production_kg,0)} kg</td></tr>
      })}</tbody></table></div>:<ul>{[...new Set(result.excluded_options.map(row=>str(row.reason)).filter(Boolean))].map(reason=><li key={reason}>{reason}</li>)}</ul>}
      {partial&&<p>Toplam su yeterliliği bu kısmi hesapla doğrulanmaz. Sabit tutulan ürünün sulama gereksinimi, su sınırı değerlendirmesine ayrıca eklenmelidir.</p>}
    </details>
  </section>
}
