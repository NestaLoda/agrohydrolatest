export type JsonRecord = Record<string, unknown>
import type { PlanningContext, SimulationRequest, SimulationResult } from './planning'
export interface Site extends JsonRecord { id: string; name: string; lat: number; lon: number; role?: string; classification?: string }
export interface Dataset extends JsonRecord { id?: string; label?: string; title?: string; name?: string; provider?: string; classification?: string; source_url?: string; url?: string }
export interface Overview {
  pilot: { crops: { name: string; area_da: number; original_share_pct: number; optimized_share_pct: number }[]; pressure_before: number; pressure_after: number; reduction_pct: number; source?: string; source_url?: string; [key: string]: unknown };
  sites: Site[]; datasets: Dataset[];
  future: { label: string; classification: string; period: string; scenarios: { id: string; label: string; northward_shift_km: number; [key: string]: unknown }[]; source_url: string; [key: string]: unknown };
}
export interface TransferSite extends JsonRecord { site_id: string; name: string; year: number; annual_precipitation_mm: number | null; gdd_base5_c_days: number | null; frost_free_longest_days: number | null; water_balance?: JsonRecord }
export interface Transfer extends JsonRecord { sites: TransferSite[] }
export interface DecisionInput {
  region_id: string; scenario_id: string; output_target_kg: number; freshwater_capacity_m3: number;
  energy_budget_kwh: number; seawater_salinity_psu: number; seawater_temperature_c: number;
  open_field_climate_suitable: boolean | null; soil_suitable: boolean | null;
  desalination_capacity_m3: number; production_capacity_kg: number; recovery_fraction: number; energy_margin_fraction: number;
}
export interface Decision {
  status: string; crop: string; classification: string; run_id: string;
  allocations: { option_id: string; label: string; production_kg: number; share_pct: number; water_m3: number; energy_kwh: number }[];
  totals: { production_kg: number; freshwater_m3: number; desalinated_water_m3: number; feed_seawater_m3: number; energy_kwh: number } | null;
  options: { id: string; label: string; status: string; reason: string; water_m3_per_kg: number; energy_kwh_per_kg: number }[];
  frontier: { id: string; label: string; status: string; reason?: string; [key: string]: unknown }[];
  pareto: { objective: string; status: string; energy_kwh?: number; freshwater_m3?: number }[];
  assumptions: string[]; reasons: string[]; sources: { label: string; url: string }[]; treatment: JsonRecord;
  constraints?: { id: string; label: string; unit: string; capacity: number; used: number | null; slack: number | null; binding: boolean }[];
  explanation?: unknown;
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`/api${path}`, { ...options, headers: { ...(options?.body instanceof FormData ? {} : { 'Content-Type': 'application/json' }), ...options?.headers } })
  if (!response.ok) {
    let detail: unknown
    try { detail = (await response.json()).detail } catch { /* non-json server response */ }
    const validation = Array.isArray(detail) ? detail.map(item => typeof item?.msg === 'string' ? item.msg : '').filter(Boolean).join(' · ') : ''
    throw new Error(typeof detail === 'string' ? detail : validation || `İstek tamamlanamadı (${response.status}). Girdileri ve yerel hizmeti kontrol edin.`)
  }
  return response.json() as Promise<T>
}
export const api = {
  automaticNorth: (id:string) => request<JsonRecord>(`/automatic-north?climate_context_id=${encodeURIComponent(id)}`),
  northEvidence: () => request<JsonRecord>('/north-evidence'),
  planningContext: (regionId:string) => request<PlanningContext>(`/planning-context?region_id=${encodeURIComponent(regionId)}`),
  simulate: (input:SimulationRequest) => request<SimulationResult>('/simulate',{method:'POST',body:JSON.stringify(input)}),
  informationValue: (input:SimulationRequest) => request<JsonRecord>('/decision-information',{method:'POST',body:JSON.stringify(input)}),
  patternFieldUpdate: (input:JsonRecord) => request<JsonRecord>('/pattern-field-update',{method:'POST',body:JSON.stringify(input)}),
  overview: () => request<Overview>('/overview'),
  sources: () => request<{datasets: Dataset[]}>('/sources'),
  transfer: () => request<Transfer>('/transfer'),
  benchmarks: () => request<Transfer>('/benchmarks'),
  benchmarkComparison: (input: JsonRecord) => request<Transfer>('/benchmark-comparison', { method: 'POST', body: JSON.stringify(input) }),
  northContext: () => request<JsonRecord>('/north-context'),
  fieldComparison: (input: JsonRecord) => request<JsonRecord>('/field-comparison', { method: 'POST', body: JSON.stringify(input) }),
  decision: (input: DecisionInput) => request<Decision>('/decision', { method: 'POST', body: JSON.stringify(input) }),
  sensitivity: (input: JsonRecord) => request<JsonRecord>('/sensitivity', { method: 'POST', body: JSON.stringify(input) }),
  pwnExample: () => request<JsonRecord>('/pwn/example'),
  pwn: (file: File, metadata: Record<string, string>) => {
    const data = new FormData(); data.append('file', file); Object.entries(metadata).forEach(([key, value]) => data.append(key, value))
    return request<JsonRecord>('/pwn/analyze', { method: 'POST', body: data })
  },
}
