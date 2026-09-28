import {useEffect,useState} from 'react'
import type {SimulationResult} from '../planning'
import {calculateEconomics,economicTone,type EconomicsInputs} from '../economics'
import {Download,Icon,number} from '../ui'

const blank=():EconomicsInputs=>({waterCostPerM3:null,crops:{}})
const value=(raw:string)=>raw===''?null:Number(raw)
const money=(n:number|null,missing='Hesap için tutar girin')=>n===null?missing:`${number(n,0)} TL`

export default function TurkeyEconomics({result}:{result:SimulationResult}){
  const storageKey=`agrohydro-economics-v1:${result.request.region_id}`
  const [inputs,setInputs]=useState<EconomicsInputs>(()=>{
    try{const data=JSON.parse(sessionStorage.getItem(storageKey)||'null');return data&&typeof data==='object'&&data.crops&&typeof data.crops==='object'?data:blank()}catch{return blank()}
  })
  useEffect(()=>{try{sessionStorage.setItem(storageKey,JSON.stringify(inputs))}catch{/* Input still works when storage is unavailable. */}},[storageKey,inputs])
  const plan=result.optimized
  if(!plan)return null
  const before=result.current.crops.map(c=>({crop_id:c.crop_id,area_ha:c.area_ha,production_kg:c.production_kg,water_m3:c.water_m3??null}))
  const after=plan.crops.map(c=>({crop_id:c.crop_id,area_ha:c.area_ha,production_kg:c.production_kg,water_m3:c.held_for_missing_water?null:plan.allocations.filter(a=>a.crop_id===c.crop_id).reduce((sum,a)=>sum+a.water_m3,0)}))
  const financial=calculateEconomics(inputs,before,after),gain=financial.delta.operatingMarginTl,waterSaving=financial.savings.waterCostTl
  const tone=economicTone(financial)
  const riceOutside=before.some(c=>c.crop_id==='rice'&&c.water_m3===null&&c.area_ha>0)||after.some(c=>c.crop_id==='rice'&&c.water_m3===null&&c.area_ha>0)
  const missingWater=inputs.waterCostPerM3===null?'Sulama birim fiyatını girin':riceOutside?'Çeltik suyu kapsam dışında':'Sulama miktarıyla hesaplanır'
  const status=gain!==null?`${gain<0?'−':'+'}${money(Math.abs(gain))} faaliyet farkı`:waterSaving!==null?`${money(Math.abs(waterSaving))} ${waterSaving<0?'ek sulama gideri':'sulama gideri azalması'}`:'İsteğe bağlı gelir / gider hesabı'
  const setCrop=(id:string,key:'salePricePerKg'|'productionCostPerHa',next:number|null)=>setInputs({...inputs,crops:{...inputs.crops,[id]:{...(inputs.crops[id]??{salePricePerKg:null,productionCostPerHa:null}),[key]:next}}})
  return <details className={`economics-panel verdict-${tone}`}>
    <summary><span><Icon name="energy" size={14}/> Ekonomi kontrolü</span><b>{status}</b></summary>
    <div className="economics-body">
      <p>Seçilen fiyat ve maliyetlerle mevcut senaryo → öneri. Bu kontrol, su odaklı önerinin ekonomik sonucunu hesaplar.</p>
      <div className="water-cost-input"><label>Sulama birim maliyeti<input type="number" min="0" step="any" aria-label="Sulama birim maliyeti TL/m³" placeholder="Birim fiyatı girin" value={inputs.waterCostPerM3??''} onChange={e=>setInputs({...inputs,waterCostPerM3:value(e.target.value)})}/><small>TL/m³ · su + pompalama / hizmet</small></label><div><small>Desen değişiminden sulama gideri farkı</small><strong>{waterSaving===null?missingWater:`${waterSaving<0?'Ek gider: ':'Azalma: '}${money(Math.abs(waterSaving))}`}</strong></div></div>
      <div className="table-scroll"><table><thead><tr><th>Ürün</th><th>Satış fiyatı · TL/kg</th><th>Sulama hariç üretim gideri · TL/ha</th></tr></thead><tbody>{plan.crops.map(c=><tr key={c.crop_id}><th>{c.name_tr}</th><td><input type="number" min="0" step="any" placeholder="Birim fiyatı girin" aria-label={`${c.name_tr} satış fiyatı TL/kg`} value={inputs.crops[c.crop_id]?.salePricePerKg??''} onChange={e=>setCrop(c.crop_id,'salePricePerKg',value(e.target.value))}/></td><td><input type="number" min="0" step="any" placeholder="Hesap için tutar girin" aria-label={`${c.name_tr} sulama hariç üretim gideri TL/ha`} value={inputs.crops[c.crop_id]?.productionCostPerHa??''} onChange={e=>setCrop(c.crop_id,'productionCostPerHa',value(e.target.value))}/></td></tr>)}</tbody></table></div>
      <div className="economics-comparison"><table><thead><tr><th>Sezon hesabı</th><th>Mevcut senaryo</th><th>Öneri</th><th>Öneri − mevcut</th></tr></thead><tbody>{[
        {label:'Satış geliri',key:'revenueTl' as const,missing:'Satış fiyatlarını girin'},{label:'Sulama hariç üretim gideri',key:'cultivationCostTl' as const,missing:'Üretim giderlerini girin'},{label:'Sulama gideri',key:'waterCostTl' as const,missing:missingWater},{label:'Modellenmiş faaliyet marjı',key:'operatingMarginTl' as const,missing:riceOutside?'Tam sulama hesabı gerekli':'Fiyat ve giderleri girin'},
      ].map(row=><tr key={row.key}><th>{row.label}</th><td>{money(financial.before[row.key],row.missing)}</td><td>{money(financial.after[row.key],row.missing)}</td><td>{money(financial.delta[row.key],row.missing)}</td></tr>)}</tbody></table></div>
      <p className={`economics-verdict verdict-${tone}`}>{financial.profitComplete?financial.after.operatingMarginTl!==null&&financial.after.operatingMarginTl< -1?`Bu varsayımlarda önerinin faaliyet marjı ${money(financial.after.operatingMarginTl)}: giderler geliri aşıyor. ${gain!==null&&gain>1?'Önceki desene göre iyileşme var, ancak marj hâlâ negatif.':'Fiyat ve gider varsayımları uygulamadan önce yeniden değerlendirilmeli.'}`:gain!==null&&gain< -1?'Su odaklı öneri bu fiyatlarda faaliyet marjını düşürüyor. Uygulamadan önce ürün sınırlarını ve maliyetleri yeniden değerlendirin.':gain!==null&&gain>1?`Bu varsayımlarda faaliyet marjı artıyor.${financial.delta.revenueTl!==null&&financial.delta.revenueTl>=0?' Satış geliri de korunuyor.':' Satış geliri azalması gider tasarrufuyla karşılanıyor.'}`:'Bu varsayımlarda belirgin faaliyet marjı farkı yok.':'Su gideri azalması tek başına kâr artışı değildir; eksik fiyat / gider değerleri tamamlanmalı.'}</p>
      <footer><span>{inputs.waterCostPerM3!==null||Object.values(inputs.crops).some(c=>c.salePricePerKg!==null||c.productionCostPerHa!==null)?'Kullanıcı fiyat / gider senaryosu':'Fiyatları girerek karşılaştırın'} · aynı birim fiyat/maliyet, iki desene uygulanır. Marj = gelir − üretim gideri − sulama. Yatırım, finansman ve vergi dahil net kâr hesabı değildir.</span><Download data={{classification:'USER_SCENARIO',region_id:result.request.region_id,run_id:result.run_id,inputs,before,after,financial,units:{money:'TL',price:'TL/kg',cultivation_excluding_water:'TL/ha',water_cost:'TL/m3'},scope:'Revenue minus cultivation (excluding irrigation) and water/service cost; fixed capital, financing and taxes not included.'}} filename={`ekonomi-${result.request.region_id}-${result.run_id.slice(0,10)}.json`}>Ekonomi kaydını indir</Download><button type="button" onClick={()=>setInputs(blank())}>Ekonomi girdilerini temizle</button></footer>
    </div>
  </details>
}
