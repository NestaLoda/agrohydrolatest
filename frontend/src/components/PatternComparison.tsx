import { Badge, Card, Empty, number, Status } from '../ui'

/** Presentation model: ha and kg-capacity rows remain separate physical groups. */
export interface PatternRowView {
  id: string
  name: string
  method: string
  unit: 'ha' | 'm2'
  current: number | null
  optimized: number | null
  currentProductionKg?: number | null
  optimizedProductionKg?: number | null
  explanation: string[]
  status?: string
  currentShare?:number|null
  recommendedShare?:number|null
  currentWater?:number|null
  recommendedWater?:number|null
  summary?:string
}

export default function PatternComparison({ rows, available, status, north = false }: {
  rows: PatternRowView[]
  available: boolean
  status?: string
  north?: boolean
}) {
  return <Card
    title={north ? 'Geleceğin üretim deseni' : available?'Mevcut ürün deseni → önerilen ürün deseni':'Mevcut ürün deseni'}
    action={status ? <Status value={status} /> : <Badge>Hesap bekliyor</Badge>}
    className={`pattern-hero ${north?'pattern-north':'pattern-turkiye'} ${available?'pattern-computed':'pattern-baseline'}`}
  >
    <div className="pattern-key">{!north&&<span><i />Mevcut desen</span>}{available&&<span><i />{north?'Hesaplanan senaryo deseni':'Önerilen desen'}</span>}</div>
    {(['ha', 'm2'] as const).map(unit => {
      const group = rows.filter(row => row.unit === unit)
      if (!group.length) return null
      const max = Math.max(1, ...group.flatMap(row => [row.current || 0, row.optimized || 0]))
      return <div className="pattern-group" key={unit}>
        <div className="pattern-group-title"><h3>{unit === 'ha' ? 'Açık tarla · ürün alanları' : 'Kontrollü üretim · yetiştirme yüzeyi'}</h3><span>{unit === 'ha' ? 'hektar' : 'm² yetiştirme yüzeyi'}</span></div>
        <div className="pattern-column-labels"><span>Ürün / yöntem</span><span>{north?'Hesaplanan kapasite':'Desen karşılaştırması'}</span><span>{north?'Alan / yetiştirme yüzeyi':available?'Mevcut → önerilen':'Mevcut'}</span></div>
        {group.map(row => <article className="pattern-row" key={row.id}>
          <div className="pattern-crop"><strong>{row.name}</strong><small>{row.method}</small></div>
          <div className="pattern-bars" role="img" aria-label={north?`${row.name}: hesaplanan ${number(row.optimized)} ${unit}`:`${row.name}: mevcut ${number(row.current)} ${unit}, önerilen ${number(row.optimized)} ${unit}`}>
            {!north&&<div><i style={{ width: `${Math.max(0, (row.current || 0) / max * 100)}%` }} /></div>}
            {available&&<div className="pattern-recommended-bar"><i style={{ width: `${Math.max(0, (row.optimized || 0) / max * 100)}%` }} /></div>}
          </div>
          <div className="pattern-values">{!north&&<span>{number(row.current, 2)}</span>}{!north&&available&&<b>→</b>}{(north||available)&&<strong>{available ? number(row.optimized, 2) : '—'}</strong>}<small>{unit==='m2'?'m²':unit}</small></div>
          {available && <><div className="pattern-facts">{unit==='ha'&&!north&&<span>Pay <b>{number(row.currentShare)} → {number(row.recommendedShare)}%</b></span>}{!north&&<span>Fark <b>{row.current===null?'—':number((row.optimized||0)-row.current,2)} {unit==='m2'?'m²':'ha'}</b></span>}<span>Su · m³ <b>{!north&&<>{number(row.currentWater)} → </>}{number(row.recommendedWater)}</b></span><span>Üretim · kg <b>{!north&&<>{number(row.currentProductionKg)} → </>}{number(row.optimizedProductionKg)}</b></span></div>{!north&&<div className="pattern-explanation"><p>{row.summary||row.explanation[0]||'Bu ürün için açıklama kaydı bulunmuyor.'}</p><details><summary>Hesabın ayrıntısı</summary>{row.explanation.map((reason,i)=><p key={i}>{reason}</p>)}</details></div>}</>}
        </article>)}
      </div>
    })}
    {!rows.length && <Empty>Bölge verisi ve aday ürünler yükleniyor. Veri olmadan ürün alanı oluşturulmaz.</Empty>}
    {!available && rows.length > 0 && <p className="small muted">Senaryoyu düzenleyin ve simüle edin. Önerilen alanlar yalnız gerçek çözücü sonucuyla doldurulur.</p>}
    {north && <p className="small muted">Açık tarla hektarı ve kontrollü üretim yetiştirme yüzeyi ayrı gösterilir; ortak bir sahte alan yüzdesine dönüştürülmez.</p>}
  </Card>
}

