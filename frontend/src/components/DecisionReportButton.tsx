import {useState} from 'react'
import {Icon} from '../ui'
import './decision-report.css'

export default function DecisionReportButton({kind,request,disabled=false}:{kind:'turkiye'|'north';request:unknown;disabled?:boolean}){
  const [busy,setBusy]=useState(false),[error,setError]=useState('')
  async function download(){
    setBusy(true);setError('')
    try{
      const route=kind==='turkiye'?'/api/decision-report/turkiye':'/api/north/report'
      const response=await fetch(route,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(request)})
      if(!response.ok){const data=await response.json();throw new Error(typeof data.detail==='string'?data.detail:'Rapor oluşturulamadı.')}
      const blob=await response.blob(),url=URL.createObjectURL(blob),a=document.createElement('a')
      a.href=url;a.download=kind==='turkiye'?`${(request as {region_id:string}).region_id}-karar-raporu.pdf`:`kuzey-${(request as {target_year:number}).target_year}-karar-raporu.pdf`
      document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),30_000)
    }catch(e){setError(e instanceof Error?e.message:String(e))}finally{setBusy(false)}
  }
  return <section className={`decision-report-action ${kind}`} aria-label="Karar verici raporu"><div><span>KARAR VERİCİ ÇIKTISI</span><h3>{kind==='turkiye'?'Mevcut desen → uygulanabilir öneri':'Su + üretim + saha doğrulaması'}</h3><p>Ürün oranları, su hesabı, somut eylemler ve bilimsel sınırlar tek raporda.</p></div><button type="button" disabled={disabled||busy} onClick={()=>void download()}><Icon name="source" size={17}/>{busy?'PDF hazırlanıyor…':'Karar raporunu indir · PDF'}</button>{error&&<small role="alert">{error}</small>}</section>
}
