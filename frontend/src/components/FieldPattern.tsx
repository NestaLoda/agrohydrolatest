import type {CSSProperties} from 'react'
import {number} from '../ui'

export type FieldSlice={id:string;name:string;area:number;color:string}

// Stable crop identities across regions. These are schematic planted rows,
// not a parcel map, observed crop health, or a second agricultural model.
const crops:Record<string,{color:string;soil:string;plant:string}>={
  wheat:{color:'#8c965b',soil:'#d6d6a8',plant:'<path d="M12 21V5m0 5L8 7m4 7L8 11m4 7l-4-3m4-4 4-3m-4 7 4-3"/>'},
  barley:{color:'#759659',soil:'#b7ce96',plant:'<path d="M12 22V6m0 6L7 6m5 10L7 10m5 9L7 14m5-2 5-6m-5 10 5-6m-5 9 5-5"/>'},
  maize_grain:{color:'#39754e',soil:'#7faa78',plant:'<path d="M12 24V5M12 13Q4 12 5 7q7 0 7 6M12 19q8-1 8-7-7 0-8 7"/><path d="m10 5 2-3 2 3"/>'},
  sugar_beet:{color:'#638876',soil:'#a6c2ae',plant:'<path d="M12 21v-9m0 3C4 16 4 7 6 7q6 0 6 8m0 0c8 1 8-8 6-8q-6 0-6 8"/><ellipse cx="12" cy="21" rx="3" ry="2"/>'},
  cotton:{color:'#859a84',soil:'#bdcfb3',plant:'<path d="M12 23V13m0 5-5-3m5 1 5-3"/><path fill="#f5f3df" d="M8 7a4 4 0 0 1 8 0c7 1 4 8-1 7-3 4-7 0-6-1-6-1-5-6-1-6Z"/>'},
  sunflower:{color:'#8b984d',soil:'#c7ce91',plant:'<path d="M12 23V11m0 8-5-4m5 3 5-4"/><circle cx="12" cy="8" r="5" fill="#d4cd8d"/><circle cx="12" cy="8" r="2"/>'},
  rice:{color:'#4d8b7e',soil:'#a2c7b4',plant:'<path d="M2 25h20M12 23V9m0 10L7 9m5 11 5-13m-5 7 4-8m-4 5L9 5"/>'},
  potato:{color:'#647f52',soil:'#a8bb8c',plant:'<path d="M12 23V10"/><ellipse cx="8" cy="10" rx="4" ry="2" transform="rotate(35 8 10)"/><ellipse cx="16" cy="14" rx="4" ry="2" transform="rotate(-35 16 14)"/>'},
  lettuce:{color:'#58805b',soil:'#a3c396',plant:'<path d="M12 20C2 21 3 8 8 9 5 1 19 1 16 9c7-2 8 12-4 11Zm0 0V9m0 7-4-4m4 3 4-4"/>'},
}
const fallback={color:'#728875',soil:'#b8c8aa',plant:'<path d="M12 23V10m0 5C3 15 4 5 4 5q8 0 8 10m0-3q0-9 8-9 0 9-8 9"/>'}
export const cropColor=(id:string)=>(crops[id]||fallback).color
const texture=(id:string)=>{
  const c=crops[id]||fallback
  return `url("data:image/svg+xml,${encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" width="24" height="30" viewBox="0 0 24 30"><path d="M1 0v30M23 0v30" stroke="#fff" stroke-opacity=".15"/><g fill="none" stroke="${c.color}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">${c.plant}</g></svg>`)}")`
}

export default function FieldPattern({label,rows,area,selected,onSelect,active=false}:{label:string;rows:FieldSlice[];area:number;selected:string|null;onSelect:(id:string|null)=>void;active?:boolean}){
  const total=rows.reduce((s,r)=>s+r.area,0),scale=Math.max(area,total,1),unassigned=Math.max(0,area-total)
  const focus=rows.find(r=>r.id===selected),overflow=total>area+.01
  return <figure className={`crop-farm${active?' active':''}`}>
    <figcaption><span><i/>{label}</span><small title={`${number(area,0)} ha`}>Ürünlerin alan payı</small></figcaption>
    <div className="farm-ground">
      <div className="planted-field" role="group" aria-label={`${label} · tarla dağılımı`}>
        {rows.map(r=>{
          const share=r.area/scale*100,percentage=r.area/Math.max(area,1)*100
          const description=`${label} · ${r.name}: %${number(percentage,1)}, ${number(r.area,1)} ha`
          return <button type="button" key={r.id} data-crop={r.id} className={`planted-zone${selected===r.id?' selected':selected?' dim':''}`} style={{flexBasis:`${share}%`,'--crop-soil':(crops[r.id]||fallback).soil,'--crop-texture':texture(r.id)} as CSSProperties} title={description} aria-label={description} tabIndex={r.area>0?0:-1} onMouseEnter={()=>onSelect(r.id)} onMouseLeave={()=>onSelect(null)} onFocus={()=>onSelect(r.id)} onBlur={()=>onSelect(null)} onClick={()=>onSelect(r.id)}>
            <span className="plot-label">{share>=17&&<b>{r.name}</b>}{share>=9&&<small>%{number(percentage,1)}</small>}</span>
          </button>
        })}
        <div className="unplanted-zone" style={{flexBasis:`${unassigned/scale*100}%`}} title={`Atanmayan: ${number(unassigned,1)} ha`} aria-label={`Atanmayan: ${number(unassigned,1)} ha`}>{unassigned/scale>=.2&&<span>Atanmayan</span>}</div>
      </div>
    </div>
    <div className="farm-readout">{focus?<><b>{focus.name}</b><span title={`${number(focus.area,1)} ha`}>Alanın %{number(focus.area/Math.max(area,1)*100,1)}'i</span></>:<><span>Ekili alan</span><b title={`${number(total,0)} ha`}>%{number(total/Math.max(area,1)*100,1)}</b></>}</div>
    {overflow&&<small className="farm-overflow">Alan kapasitesi aşıldı · parseller ekili toplamına göre ölçeklendi.</small>}
  </figure>
}
