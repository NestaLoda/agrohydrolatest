import type {JsonRecord} from '../api'
import {Icon, list, obj, number} from '../ui'
import './producer-support.css'

export type ProducerContext={
 label:string; region:string; area_m2:number; hydroponic_share_pct:number; greenhouse_share_pct:number;
 crops:{id:string;name:string;production_kg:number;methods:string[]}[];
 request:JsonRecord; provenance:JsonRecord;
}
export function contextFromNorth(result:JsonRecord):ProducerContext{
 const request=obj(result.request),production=obj(obj(result.decision_story).production)
 const area=Number(request.area_m2),methods=list(production.methods)
 const share=(id:string)=>area>0?100*Number(methods.find(m=>m.id===id)?.area_m2||0)/area:0
 return {label:request.target_year?String(request.target_year):({recent:'2015–2025',historical:'1995–2014',near:'2030',mid:'2050',late:'2090'} as Record<string,string>)[String(request.horizon_id)]||String(request.horizon_id),region:'Longyearbyen',area_m2:area,hydroponic_share_pct:share('hydroponics'),greenhouse_share_pct:share('greenhouse'),request,provenance:obj(result.provenance),crops:list(production.crops).map(c=>({id:String(c.crop_id),name:String(c.name),production_kg:Number(c.production_kg),methods:Array.isArray(c.methods)?c.methods.map(String):[]}))}
}
export default function ProducerRecommendation({context,stale=false,onOpen}:{context?:ProducerContext;stale?:boolean;onOpen:(context?:ProducerContext)=>void}){
 const controlled=!!context&&(context.hydroponic_share_pct+context.greenhouse_share_pct)>.01
 return <section className="producer-recommendation" aria-label="Üretim önerisine bağlı tarım güvencesi"><Icon name="greenhouse" size={22}/><div><span>TARIM GÜVENCESİ · PROGRAM TASARIMI</span><h3>{controlled?`${context.label} önerisini küçük bir üretim pilotuna taşı.`:'Üretim kararını eğitim, teknik destek ve alıcıyla tamamla.'}</h3><p>{controlled?`Bu planda topraksız alan payı %${number(context.hydroponic_share_pct)}, sera payı %${number(context.greenhouse_share_pct)}. Kurulum desteğini ve hasadın alıcıya ulaşmasını birlikte planla.`:'Bölgesel ürün deseni tek başına hidroponiğe geçiş kararı değildir. Yerel pilotun su, enerji ve ürün sonucuna göre destek yolunu seç.'}</p><div className="producer-benefit-tags"><b>Gençlere eğitim</b><b>Ekipman desteği</b><b>Teknik takip</b><b>Ürün alımı / dağıtım</b></div><small>{stale?'Ayarlar değişti; desteği güncel öneriye bağlamak için simülasyonu çalıştır.':'Destek koşullarının mali etkisi ayrıca hesaplanır; üretim veya kazanç artışı varsayılmaz.'}</small></div><button disabled={stale} onClick={()=>onOpen(context)}>Bu öneriyle destek planla <Icon name="arrow" size={14}/></button></section>
}
