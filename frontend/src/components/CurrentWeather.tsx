import {useEffect,useState} from 'react'
import {Icon,number} from '../ui'
type Weather={status:string;temperature_c:number|null;valid_at?:string;source_url?:string}
export default function CurrentWeather({region}:{region:string}){
  const [weather,setWeather]=useState<Weather|null>(null)
  useEffect(()=>{
    const control=new AbortController();setWeather(null)
    fetch(`/api/current-weather/${encodeURIComponent(region)}`,{signal:control.signal})
      .then(r=>{if(!r.ok)throw Error('weather');return r.json()}).then(setWeather)
      .catch(()=>{if(!control.signal.aborted)setWeather({status:'unavailable',temperature_c:null})})
    return ()=>control.abort()
  },[region])
  return <div className="current-weather"><Icon name="sun" size={14}/>{weather?.status==='available'?<><b>{number(weather.temperature_c,1)} °C</b><span>{new Date(weather.valid_at!).toLocaleString('tr-TR',{day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit',timeZone:'Europe/Istanbul'})} TSİ · güncel model hava bilgisi</span><a href={weather.source_url} target="_blank" rel="noreferrer">Open-Meteo</a></>:<span>{weather?'Güncel hava: veri alınamadı':'Güncel hava yükleniyor…'}</span>}<small>Sezon hesabından ayrı</small></div>
}
