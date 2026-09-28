import { useEffect, useRef, useState } from 'react'
import * as maplibregl from 'maplibre-gl'
import mapWorkerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url'
import 'maplibre-gl/dist/maplibre-gl.css'
import type { Site } from './api'

// MapLibre 6 resolves its default worker relative to the final JS module.
// Vite must bundle that worker and its shared module before its URL is assigned.
maplibregl.setWorkerUrl(mapWorkerUrl)

export default function ResearchMap({ sites, focus, onSelect, fitAll = false }: { sites: Site[]; focus: string; onSelect?: (id: string) => void; fitAll?: boolean }) {
  const container = useRef<HTMLDivElement>(null)
  const mapRef = useRef<maplibregl.Map | null>(null)
  const [failed, setFailed] = useState(false)
  useEffect(() => {
    if (!container.current) return
    try {
      const map = new maplibregl.Map({
        container: container.current, center: [26, 56], zoom: 2.1, maxZoom: 7, minZoom: 1,
        attributionControl: { compact: true },
        style: { version: 8, sources: { land: { type: 'geojson', data: '/land.geojson', attribution: 'Natural Earth · Kamu malı · 1:110m' } }, layers: [
          { id: 'water', type: 'background', paint: { 'background-color': '#e1ecea' } },
          { id: 'land', type: 'fill', source: 'land', paint: { 'fill-color': '#faf8f0', 'fill-outline-color': '#b9cfca' } },
        ] },
      })
      map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'bottom-right')
      map.scrollZoom.disable()
      mapRef.current = map
      const resize = new ResizeObserver(() => { if(container.current && container.current.clientWidth > 0) map.resize() })
      resize.observe(container.current)
      return () => { resize.disconnect(); map.remove(); mapRef.current = null }
    } catch { setFailed(true) }
  }, [])
  useEffect(() => {
    if (!mapRef.current) return
    const markers = sites.map(site => {
      const node = document.createElement('div'); node.className = `map-pin ${site.id === focus ? 'is-focused' : ''}`
      const dot = document.createElement('span'); dot.className = 'map-dot'
      const label = document.createElement('span'); label.className = 'map-label'; label.textContent = site.name
      if (site.id === 'seyhan_adana') label.style.transform = 'translateY(19px)'
      node.append(dot, label)
      if (onSelect) { node.tabIndex = 0; node.setAttribute('role','button'); node.setAttribute('aria-label',`${site.name} bölgesini seç`); node.onclick = () => onSelect(site.id); node.onkeydown = event => { if(event.key === 'Enter' || event.key === ' ') {event.preventDefault();onSelect(site.id)} } }
      return new maplibregl.Marker({ element: node, anchor: 'left' }).setLngLat([site.lon, site.lat]).addTo(mapRef.current!)
    })
    const active = sites.find(s => s.id === focus)
    if (fitAll && sites.length) mapRef.current.fitBounds([[Math.min(...sites.map(s=>s.lon))-2,Math.min(...sites.map(s=>s.lat))-1],[Math.max(...sites.map(s=>s.lon))+2,Math.max(...sites.map(s=>s.lat))+1]],{padding:45,duration:0})
    else if (active) mapRef.current.flyTo({ center: [active.lon, active.lat], zoom: active.lat > 70 ? 3.2 : 4, duration: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 700 })
    return () => { markers.forEach(marker => marker.remove()) }
  }, [sites, focus, fitAll, onSelect])
  return <div className="map-wrap">
    <div className="map-canvas" ref={container} aria-label="Araştırma noktaları haritası" role="img" />
    <div className="map-top"><span className="tiny-label">ARAŞTIRMA COĞRAFYASI</span><span className="map-local"><i /> Çevrimdışı harita</span></div>
    <div className="map-caption">{failed ? 'Bu cihazda harita görüntülenemiyor. Araştırma noktaları aşağıdaki listede.' : 'Noktalar araştırma bağlamını gösterir; hesaplanmış üretim sınırı veya sefer rotası değildir.'}</div>
    <div className="sr-only">{sites.map(site => <p key={site.id}>{site.name}: {site.lat}, {site.lon}. {site.role}</p>)}</div>
  </div>
}
