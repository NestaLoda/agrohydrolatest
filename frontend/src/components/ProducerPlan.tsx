import {useState} from 'react'
import {Download,number,Icon} from '../ui'
import type {ProducerContext} from './ProducerRecommendation'

export type ProducerSelection={goal:string;selected_services:string[];comparison_months:number}
const modules=[
 ['education','Tanış ve öğren','Gençler için topraksız tarım, su devridaimi ve temel bakım eğitimi.'],
 ['equipment','Kurulumu kolaylaştır','Modüler sistem ve servis tekliflerini karşılaştır; dönemlik ekipman desteğini tanımla.'],
 ['technical','Üretim boyunca destekle','Su kalitesi, besin çözeltisi, enerji ve bitki gelişimini takip et; sorunlarda teknik destek planla.'],
 ['market','Hasadı alıcıya ulaştır','Üreticiden alım ve market/manavlara dağıtım için kalite, miktar, fiyat ve teslim koşullarını belirle.'],
 ['coverage','Risk kapsamını netleştir','Bakım hizmeti ile poliçeye bağlı teminatı ayır; uygun sigorta tarafıyla kapsamı araştır.'],
] as const
const methodNames:Record<string,string>={hydroponics:'Topraksız kapalı ortam',greenhouse:'Güneş alan sera',open_field:'Açık tarla'}
export default function ProducerPlan({context,onScenario}:{context?:ProducerContext;onScenario:(crop:ProducerContext['crops'][number],selection:ProducerSelection)=>void}){
 const [selected,setSelected]=useState<string[]>(modules.map(m=>m[0]))
 const [cropId,setCropId]=useState(context?.crops[0]?.id||'')
 const [goal,setGoal]=useState('Öğrenme ve küçük pilot')
 const crop=context?.crops.find(c=>c.id===cropId)
 return <div className="producer-plan"><span className="producer-tag">DÖNEMLİK DESTEK · KATILIM TASLAĞI</span><h3>{context?`${context.label} üretim önerisinden uygulamaya`:'Gençleri yeni tarımla buluştur'}</h3><p>Tarım Güvencesi fikri, üreticiyi eğitimden hasadın alıcıya ulaşmasına kadar destekleyen bir işleyiştir. Aşağıda seçilenler tasarlanan hizmetlerdir; kayıt, ödeme veya sözleşme oluşturmaz.</p>
 {context&&<div className="producer-model-context"><Icon name="greenhouse"/><div><b>{context.region} · {context.label} · {number(context.area_m2,0)} m² model planı</b><p>Topraksız %{number(context.hydroponic_share_pct)} · sera %{number(context.greenhouse_share_pct)}. Bu plan saha ve pilotla sınanacak; ticari tesis veya ölçülmüş hasat değildir.</p></div></div>}
 <div className="producer-plan-controls"><label>Katılım amacı<select value={goal} onChange={e=>setGoal(e.target.value)}><option>Öğrenme ve küçük pilot</option><option>Mevcut üretimi iyileştirme</option><option>Doğrulanan pilotu yaygınlaştırma</option></select></label><span><b>12 aylık karşılaştırma</b><small>Hizmet süresi ve bedeli henüz sözleşmeye bağlanmadı.</small></span></div>
 <details className="producer-optional-services"><summary>Program hizmetlerini özelleştir · isteğe bağlı</summary><small>Seçilen hizmetler taslağa kaydedilir. Hizmet bedeli veya indirim, seçimlerden otomatik türetilmez; teklif koşullarıyla ayrıca girilir.</small><div className="producer-module-list">{modules.map(([id,title,description])=><label key={id}><input type="checkbox" checked={selected.includes(id)} onChange={e=>setSelected(old=>e.target.checked?[...old,id]:old.filter(x=>x!==id))}/><span><b>{title}</b><small>{description}</small></span></label>)}</div></details>
 {crop&&<div className="producer-crop-transfer"><label>Bu plandaki hangi ürünü inceleyelim?<select value={cropId} onChange={e=>setCropId(e.target.value)}>{context?.crops.map(c=><option key={c.id} value={c.id}>{c.name}</option>)}</select></label><p><b>{crop.name} · {number(crop.production_kg)} kg/yıl model beklentisi</b><br/>{crop.methods.map(m=>methodNames[m]||m).join(' + ')}</p><button className="producer-primary" onClick={()=>onScenario(crop,{goal,selected_services:[...selected],comparison_months:12})}>Bu ürünle desteğin etkisini hesapla →</button><small>Yalnız bu ürünün model hasadı aktarılır. Fiyat, alıcı kapasitesi ve giderleri siz girersiniz.</small></div>}
 <details><summary>Program neyi değiştirmeyi hedefliyor?</summary><p>Gençlerin eğitim ve ekipmana erişimini kolaylaştırmak; ilk kurulum giderini düşürmek; teknik sorunlara müdahaleyi ve ürünün satışa ulaşmasını iyileştirmek. Bunlar hedeflerdir. Katılan kişi sayısı, indirimin tutarı, teknik destek süresi ve satılan ürün gerçek pilotta kaydedilir; gerçekleşmemiş başarı yüzdesi yazılmaz.</p><p>Ürünleri doğrudan satın alıp dağıtma seçeneğinde satış geliri ile üreticiye ödeme, ambalaj, taşıma, soğuk zincir, fire ve işletme gideri birlikte değerlendirilir. Önerilen programın şu an gerçek alım taahhüdü yoktur.</p><p>Kapalı üretim su, ışık, uygun sıcaklık, besin ve bakım ister. Çöl/kutup gibi ortamlar için basit boru kurulumu tek başına yeterlilik kanıtı değildir. Topraksız üretim susuz üretim değildir. Organik nitelemesi ayrıca belgelenmeden kullanılmaz.</p></details>
 <Download data={{classification:'PROPOSED_SUPPORT_PLAN',program:'Tarım Güvencesi',goal,comparison_months:12,selected_services:selected,model_context:context||null,selected_crop:crop||null,registration_created:false,payment_collected:false,contracts_verified:false,credit_service:false,seedling_development:false,claim:'Eğitim, kurulum, teknik destek, alım/dağıtım ve yetkili tarafla risk kapsamı tasarımı; kazanç garantisi değildir.'}} filename="tarim-guvencesi-katilim-taslagi.json">Destek planı taslağını indir</Download>
 </div>
}
