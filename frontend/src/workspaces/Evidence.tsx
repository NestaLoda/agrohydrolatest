import { useEffect, useState } from 'react'
import { api, type Dataset, type Overview } from '../api'
import { Badge, Card, SourceLink, str, obj } from '../ui'
function datasetPeriod(d:Dataset){
  const start=str(d.temporal_start)||str(d.start_date),end=str(d.temporal_end)||str(d.end_date)
  if(start||end)return `${start||'—'} — ${end||'—'}`
  const period=d.period||d.date_range
  if(Array.isArray(period))return period.map(String).join(' — ')
  if(typeof period==='string')return period
  const range=obj(period)
  return str(range.start)||str(range.end)?`${str(range.start)||'—'} — ${str(range.end)||'—'}`:'Kayıtta dönem belirtilmemiş'
}
export default function Evidence({ overview }: { overview: Overview | null }) {
  const [datasets,setDatasets]=useState<Dataset[]>([]),[error,setError]=useState('')
  async function refresh(){try{setDatasets((await api.sources()).datasets);setError('')}catch{setError('Tam kaynak kaydı yüklenemedi; ana veri kaynakları gösteriliyor.')}}
  useEffect(()=>{void refresh()},[])
  return <><div className="workspace-heading"><div><h1>Kanıt ve veri kaydı</h1><p>Her veri türü, kullanım sınırı ve kaynak birlikte görünür.</p></div><button className="button small" onClick={()=>void refresh()}>Kaynak kaydını yenile</button></div>{error&&<p className="small muted">{error}</p>}<div className="evidence-legend">{['OUR_HISTORICAL_RESULT','MODEL_REANALYSIS','FUTURE_SCENARIO','SIMULATION_EXPLANATORY','PLANNED_ARCTIC_OBSERVATION'].map(kind => <Badge key={kind} kind={kind} />)}</div><Card title="Araştırma dayanakları"><div className="evidence-entry"><div><Badge kind="OUR_HISTORICAL_RESULT" /><h3>Konya · 2204-D final raporu</h3><p>Göreli model baskısı. Ölçülmüş su hacmi tasarrufu değildir.</p></div><SourceLink url={overview?.pilot.source_url}>{overview?.pilot.source || 'Orijinal rapor'}</SourceLink></div><div className="evidence-entry"><div><Badge kind="EXTERNAL_LITERATURE_RESULT" /><h3>Gelecekte iklimsel uygunluk · Xu vd. 2026</h3><p>2071–2100 dönemi, yedi ürünün ortalama kuzey sınırı. Yerel tarım uygunluğu değildir.</p></div><SourceLink url={overview?.future.source_url}>Yayın</SourceLink></div></Card><div className="data-cards">{(datasets.length?datasets:overview?.datasets||[]).map((d: Dataset, i) => <Card key={str(d.dataset_id) || i} title={d.label || d.title || str(obj(d.requested_location).name) || str(d.dataset_id)} action={<Badge kind={d.classification} />}><dl className="provenance"><dt>Sağlayıcı</dt><dd>{d.provider}</dd><dt>Dönem</dt><dd>{datasetPeriod(d)}</dd><dt>Çözünürlük</dt><dd>{str(d.spatial_resolution)||str(d.spatial_resolution_note)||"Kayıt ayrıntılarında"}</dd><dt>Lisans</dt><dd>{str(d.license)}</dd></dl><SourceLink url={d.source_url}>Kaynak veri</SourceLink><details><summary>Teknik kayıt / hash / dönüşümler</summary><pre>{JSON.stringify(d, null, 2)}</pre></details></Card>)}</div></>
}
