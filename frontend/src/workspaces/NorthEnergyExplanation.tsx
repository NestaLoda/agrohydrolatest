import type {JsonRecord} from '../api'
import {Icon, number, obj} from '../ui'
import './north-energy-explanation.css'

const finite=(value:unknown):value is number=>typeof value==='number'&&Number.isFinite(value)

export default function NorthEnergyExplanation({result}:{result:JsonRecord}) {
  const totals=obj(obj(result.plan).totals),request=obj(result.request)
  const electricity=totals.electricity_kwh,treatment=totals.treatment_electricity_kwh
  const heat=totals.heat_kwh_th,total=totals.equivalent_electricity_kwh,cop=request.heat_cop
  if(!finite(electricity)||!finite(treatment)||!finite(heat)||!finite(total)||!finite(cop)||cop<=0)return null
  const production=Math.max(0,electricity-treatment),heating=heat/cop
  const parts=[
    {key:'production',label:'Üretimi çalıştır',value:production,description:'Bitki ışıkları, su dolaşımı, havalandırma, nem alma ve soğutma.'},
    {key:'heating',label:'Gereken ısıyı sağla',value:heating,description:`Sistemin ${number(heat,0)} kWh ısı ihtiyacının, seçilen ısıtma verimiyle elektrik karşılığı.`},
    {key:'treatment',label:'Deniz suyunu arıt',value:treatment,description:'Planın kullandığı deniz suyundan tuzu ayırmak için gereken elektrik.'},
  ]
  const dominant=parts.reduce((largest,part)=>part.value>largest.value?part:largest)
  const message=dominant.key==='production'?'Bu planda en büyük enerji kalemi üretim ortamını çalıştırmak.':dominant.key==='heating'?'Bu planda en büyük enerji kalemi gereken ısıyı sağlamak.':'Bu planda en büyük enerji kalemi deniz suyunu arıtmak.'
  return <details open className="north-energy-explanation">
    <summary><Icon name="energy" size={18}/><span><b>Enerji neden gerekiyor?</b><small>{total>0?message:'Bu hesapta enerji ihtiyacı sıfır çıktı.'}</small></span><strong>{number(total,0)}<small>kWh / yıl · model hesabı</small></strong></summary>
    <div className="nee-content">
      <p>Kapalı üretimde suyu tekrar kullanabiliriz; bunun için ışık, pompalar ve ortam kontrolü çalışır. Model, <b>su ihtiyacını azaltırken gereken enerjiyi de</b> hesaba katar.</p>
      <div className="nee-visual"><svg viewBox="0 0 250 240" role="img" aria-label={parts.map(part=>`${part.label}: ${number(part.value,1)} kWh/yıl`).join('; ')}><title>Elektrik eşdeğeri enerji dağılımı</title><circle cx="125" cy="115" r="82" fill="none" stroke="#e6e8dc" strokeWidth="25"/>{parts.map((part,i)=><circle key={part.key} cx="125" cy="115" r="82" pathLength="100" fill="none" stroke={['#b28c35','#daae68','#39869a'][i]} strokeWidth="25" strokeDasharray={`${total>0?part.value/total*100:0} 100`} strokeDashoffset={-parts.slice(0,i).reduce((sum,p)=>sum+(total>0?p.value/total*100:0),0)} transform="rotate(-90 125 115)"/>)}<text x="125" y="110" textAnchor="middle" className="nee-ring-value">{number(total/1000,1)}</text><text x="125" y="135" textAnchor="middle">MWh / yıl</text><text x="125" y="232" textAnchor="middle">Elektrik eşdeğeri</text></svg><div><span className="nee-visual-label">EN BÜYÜK TÜKETİM KALEMİ</span><strong>{dominant.label}</strong><b>%{number(total>0?dominant.value/total*100:0,1)}</b><p>{dominant.description}</p></div></div>
      <div className="nee-parts">{parts.map(part=><div key={part.key}><span><i className={part.key}/><b>{part.label}</b></span><strong>{part.value>0&&part.value<.1?'<0,1':number(part.value,1)} <small>kWh/yıl</small></strong><p>{part.description}</p></div>)}</div>
      <p className="nee-accounting"><b>Toplam nasıl hesaplandı?</b> Üretim elektriği + arıtma elektriği + ısı ihtiyacı ÷ ısıtma verimi (COP {number(cop,1)}). Isı ve arıtma yukarıdaki toplamın içindedir; bir kez sayılır. COP {number(cop,1)}, modelde 1 kWh elektrikle {number(cop,1)} kWh ısı sağlandığı varsayımıdır. Soğuk kaynak suyunu ısıtmak gerekiyorsa o ısı da hesaba dahildir.</p>
      <p className="nee-decision"><b>Karar:</b> Ölçeği büyütmeden önce bu yıllık enerji ihtiyacını karşılayacak kaynağı ve en yoğun dönemde gereken gücü doğrula. Soldaki “Enerji önceliği” ile ürün miktarını ne kadar koruyacağını seçip su–enerji dengesini yeniden sına.</p>
      <small className="nee-unit">1 kWh, 1 kW gücündeki bir cihazın 1 saatlik enerji kullanımıdır. Buradaki değer seçilen dönemin ortalama yıllık ihtiyacıdır; elektrik faturası, kurulu güç veya yerelde hazır enerji kapasitesi değildir. Işık, pompa, havalandırma, nem alma ve soğutma ayrıntıları “Enerji hesabı” bölümündedir.</small>
    </div>
  </details>
}

