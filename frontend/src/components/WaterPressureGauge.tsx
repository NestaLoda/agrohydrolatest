import {number} from '../ui'
import {waterPressure} from '../waterPressure'
import './water-pressure.css'

type Props={demand:number|null;budget:number|null;partial?:boolean;pending?:boolean;stale?:boolean;scopeLabel?:string}
export default function WaterPressureGauge({demand,budget,partial=false,pending=false,stale=false,scopeLabel}:Props){
  // A named partial scope may display its own ratio, always in neutral gray.
  // It never asserts that the full region is within its water budget.
  const pressure=waterPressure(demand,budget,pending||(partial&&!scopeLabel))
  const neutral=partial||stale||pressure.status==='unknown'||pressure.status==='empty'
  const tone=neutral?'neutral':pressure.status==='over'?'bad':'good'
  const value=pending?'…':pressure.status==='unknown'?'—':pressure.zeroBudget?demand===0?'0 / 0':'SU SINIRI 0':pressure.percent===null||pressure.percent>9999?'>%200':`%${number(pressure.percent,1)}`
  const state=pending?'Hesaplanıyor':pressure.status==='unknown'?'Ayrı hesap gerekir':pressure.status==='empty'?'Oran tanımsız':stale?'Önceki koşu':partial?scopeLabel||'Kısmi kapsam':pressure.status==='over'?'Su sınırı aşılıyor':'Su sınırı içinde'
  const description=`Su sınırı kullanımı: model su ihtiyacı / sulama için belirlenen su sınırı. ${partial?`Kapsam: ${scopeLabel||'su hesabı yapılan ürünler'}; tüm bölgenin su yeterliliğini göstermez. `:''}İhtiyaç ${number(demand,2)} m³; su sınırı ${number(budget,2)} m³. ${pressure.status==='unknown'?'Toplam ihtiyaç veya su sınırı belirlenmeden oran hesaplanmaz.':pressure.zeroBudget?'Su sınırı sıfır olduğundan yüzde oranı tanımsız.':pressure.percent===null?'Oran sayısal ölçekte %200’ün üzerinde.':`Oran ${number(pressure.percent,2)}%.`}${pressure.overflow?' Kadran %200’de sonlanır; aşım üst sınırla gizlenmez.':''}${stale?' Önceki koşunun dondurulmuş girdileri.':''} Hidrolojik risk olasılığı veya ölçüm değildir.`
  return <figure className={`water-pressure-gauge pressure-${tone}`} title={description}>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 90" role="img" aria-label={`${state} · ${value}. ${description}`}>
      <title>{description}</title>
      <path d="M18 60 A42 42 0 0 1 60 18" fill="none" stroke={neutral?'#c4ccc2':'#a7c5ad'} strokeWidth="8"/>
      <path d="M60 18 A42 42 0 0 1 102 60" fill="none" stroke={neutral?'#c4ccc2':'#d7afa2'} strokeWidth="8"/>
      <line x1="60" y1="10" x2="60" y2="25" stroke="#5b7061" strokeWidth="1.5"/>
      <text x="60" y="8" textAnchor="middle" fontSize="8" fill="#637463">%100 sınırı</text>
      {pressure.status!=='unknown'&&pressure.status!=='empty'&&<line className="water-pressure-pointer" x1="60" y1="10" x2="60" y2="28" stroke="currentColor" strokeWidth="3" strokeLinecap="round" style={{transform:`rotate(${pressure.displayPercent/200*180-90}deg)`}}/>}
      <text x="60" y="51" textAnchor="middle" fontSize={value.length>8?11:16} fontWeight="650" fill="currentColor">{value}</text>
      <text x="60" y="64" textAnchor="middle" fontSize="8" fill="#71806f">{state}</text>
      <text x="9" y="72" textAnchor="middle" fontSize="7" fill="#7c8878">%0</text><text x="109" y="72" textAnchor="middle" fontSize="7" fill="#7c8878">%200</text>
      <text x="60" y="85" textAnchor="middle" fontSize="9" fill="#58725b">Su sınırı kullanımı</text>
    </svg>
  </figure>
}
