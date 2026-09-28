import { type ReactNode } from 'react'
import type { JsonRecord } from './api'

export const number = (value: unknown, digits = 1) => typeof value === 'number' && Number.isFinite(value) ? new Intl.NumberFormat('tr-TR', { maximumFractionDigits: digits }).format(value) : '—'
export const str = (value: unknown) => typeof value === 'string' ? value : ''
export const obj = (value: unknown): JsonRecord => value && typeof value === 'object' && !Array.isArray(value) ? value as JsonRecord : {}
export const list = (value: unknown): JsonRecord[] => Array.isArray(value) ? value.map(obj) : []
export const labels: Record<string, string> = {
  OUR_HISTORICAL_RESULT: 'Geçmiş sonuç', MODEL_REANALYSIS: 'Model / reanalysis', FUTURE_SCENARIO: 'Gelecek senaryosu', EXTERNAL_LITERATURE_RESULT: 'Dış literatür',
  SIMULATION_EXPLANATORY: 'Simülasyon / açıklayıcı', OUR_NEW_MEASUREMENT_TANK: 'Kendi tank ölçümümüz', EXTERNAL_OBSERVATION: 'Dış gözlem',
  PLANNED_ARCTIC_OBSERVATION: 'Planlanan gözlem', LITERATURE_TRANSFER_ASSUMPTION: 'Literatürden aktarım', ENGINEERING_CONCEPT: 'Mühendislik konsepti',
  partial_conditional: 'Kısmi öneri', conditional: 'Koşullu', suitable: 'Uygun', unsuitable: 'Uygun değil', insufficient_data: 'Veri yetersiz', unknown: 'Bilinmiyor', excluded: 'Dışarıda',
  energy: 'En düşük enerji', freshwater: 'En düşük tatlı su', analyzed: 'Analiz edildi', transfer_demonstration: 'Transfer gösterimi', historical_context: 'Tarihsel bağlam',
  budget_gap: 'Bütçe açığı', within_reference_budget: 'Referans bütçe içinde', EXTERNAL_CLIMATE_MODEL: 'Dış iklim modeli',
  infeasible:'Kısıtlar sağlanmıyor', USER_SCENARIO:'Kullanıcı senaryosu', OFFICIAL_STATISTICS:'Resmî istatistik',
}
export const label = (value: string) => labels[value] || labels[value.replaceAll(' / ', '_').replaceAll(' ', '_')] || value.replaceAll('_', ' ')
export function Icon({ name, size = 18 }: { name: string; size?: number }) {
  const paths: Record<string, ReactNode> = {
    reset: <path d="M3 10a9 9 0 1 1 2 9M3 3v7h7" />,
    sun: <><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l2 2m10 10 2 2M5 19l2-2M17 7l2-2"/></>,
    rain: <path d="M5 14a4 4 0 0 1 0-8 6 6 0 0 1 11-2 5 5 0 0 1 3 10M7 17l-1 4m6-4-1 4m6-4-1 4" />,
    sprinkler: <path d="M12 22v-9M7 22h10M9 13h6M12 4v2M5 5l2 2m12-2-2 2M2 11h3m14 0h3" />,
    energy: <path d="m13 2-9 12h7l-1 8 10-13h-8Z" />,
    snow: <path d="M12 2v20M3.3 7l17.4 10M3.3 17 20.7 7M9 4l3 3 3-3M9 20l3-3 3 3M3 10l4-1-1-4M18 19l-1-4 4-1" />,
    soil: <path d="M3 8h18M3 13h18M3 18h18M6 5l2 3m7 3 2 2m-9 2 2 3" />,
    greenhouse: <path d="M3 21V9l9-7 9 7v12ZM3 9h18M8 21V9m8 12V9M12 2v7" />,
    sensor: <path d="M8 6h8v14H8ZM10 2v4m4-4v4M5 10H2m3 5H2m17-5h3m-3 5h3M11 10h2m-2 4h2" />,
    sample: <path d="M8 2h8M9 2v8L4 19q-1 3 3 3h10q4 0 3-3l-5-9V2M7 16h10" />,
    north: <><path d="M12 21V3m-6 6 6-6 6 6M4 20h3m10 0h3" /></>,
    map: <path d="m3 5 6-2 6 2 6-2v16l-6 2-6-2-6 2ZM9 3v16M15 5v16" />,
    globe: <><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c-3 3-4.5 6-4.5 9s1.5 6 4.5 9m0-18c3 3 4.5 6 4.5 9s-1.5 6-4.5 9"/></>,
    seed: <path d="M12 21V10M12 14C5 14 3 10 3 5c6 0 9 3 9 9ZM12 10c0-5 3-8 9-8 0 5-3 8-9 8Z" />,
    wave: <path d="M3 5h18M3 11c3-5 6 5 9 0s6 5 9 0M3 17c3-5 6 5 9 0s6 5 9 0M12 3v18" />,
    source: <path d="M14 3H5v18h14V8ZM14 3v5h5M8 12h8M8 16h5" />,
    arrow: <path d="M4 12h16m-6-6 6 6-6 6" />,
    close: <path d="m6 6 12 12M6 18 18 6" />,
    compare: <><path d="M5 3v18M19 3v18M5 7h10m-3-3 3 3-3 3M19 17H9m3-3-3 3 3 3" /></>,
    check: <path d="m4 12 5 5L20 6" />,
    layers: <path d="m12 3 10 5-10 5L2 8ZM2 12l10 5 10-5M2 16l10 5 10-5" />,
    water: <path d="M12 2s-7 8-7 13a7 7 0 0 0 14 0c0-5-7-13-7-13Z" />,
  }
  return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{paths[name] || paths.layers}</svg>
}
export function Badge({ kind, children }: { kind?: string; children?: ReactNode }) { return <span className={`badge ${kind?.includes('SIMULATION') || kind?.includes('ASSUMPTION') ? 'amber' : ''}`}>{children || label(kind || '')}</span> }
export function Status({ value }: { value: string }) { return <span className={`status ${value}`}><i />{label(value)}</span> }
export function Card({ title, eyebrow, action, children, className = '' }: { title?: string; eyebrow?: string; action?: ReactNode; children: ReactNode; className?: string }) { return <section className={`card ${className}`}>{(title || action) && <div className="card-head"><div>{eyebrow && <span className="eyebrow">{eyebrow}</span>}{title && <h2>{title}</h2>}</div>{action}</div>}{children}</section> }
export function Metric({ name, value, unit, foot }: { name: string; value: unknown; unit?: string; foot?: string }) { return <div className="metric"><span>{name}</span><strong>{typeof value === 'string' ? value : number(value)}<small>{unit}</small></strong>{foot && <p>{foot}</p>}</div> }
export function Notice({ children, warn = false }: { children: ReactNode; warn?: boolean }) { return <div className={`notice ${warn ? 'warning' : ''}`} role={warn ? 'status' : undefined}><span>i</span><div>{children}</div></div> }
export function Empty({ children }: { children: ReactNode }) { return <div className="empty"><Icon name="layers" size={25} /><p>{children}</p></div> }
export function SourceLink({ url, children }: { url?: string; children: ReactNode }) { return url && (/^https?:\/\//.test(url) || url.startsWith('/api/')) ? <a className="source-link" href={url} target="_blank" rel="noreferrer">{children} ↗</a> : <span className="source-link">{children}</span> }
export function NumberField({ name, value, set, unit, min = 0, max, step = 'any', help }: { name: string; value: number; set: (v: number) => void; unit: string; min?: number; max?: number; step?: number | 'any'; help?: string }) { return <label className="field"><span>{name}</span><div className="input-unit"><input aria-label={name} type="number" value={value} min={min} max={max} step={step} onChange={e => { if (e.target.value !== '') set(Number(e.target.value)) }} required /><small>{unit}</small></div>{help && <small>{help}</small>}</label> }
export function Download({ data, filename, children }: { data: unknown; filename: string; children?: ReactNode }) { return <button className="button small" onClick={() => { const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })); const anchor = document.createElement('a'); anchor.href = url; anchor.download = filename; anchor.click(); URL.revokeObjectURL(url) }}><Icon name="source" size={14} />{children || 'Kaydı indir'}</button> }
