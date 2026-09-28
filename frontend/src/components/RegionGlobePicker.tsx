import {useEffect, useRef, useState} from 'react'
import * as maplibregl from 'maplibre-gl'
import mapWorkerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url'
import 'maplibre-gl/dist/maplibre-gl.css'
import type {Site} from '../api'
import {Icon} from '../ui'
import './region-globe-picker.css'

maplibregl.setWorkerUrl(mapWorkerUrl)

const northSite:Site={id:'longyearbyen',name:'Longyearbyen',lat:78.22,lon:15.65,role:'northern_controlled_production_context'}
const climateCell:[number,number]=[15.625,78.125]

export default function RegionGlobePicker({north,region,sites,onSelect}:{north:boolean;region:string;sites:Site[];onSelect:(id:string)=>void}){
  const [open,setOpen]=useState(false),[failed,setFailed]=useState(false)
  const [worldView,setWorldView]=useState(false)
  const root=useRef<HTMLDivElement>(null),canvas=useRef<HTMLDivElement>(null),map=useRef<maplibregl.Map|null>(null)
  const visible=north?[northSite]:sites.filter(site=>site.lat<60)
  const selected=visible.find(site=>site.id===region)
  useEffect(()=>{setOpen(false);setWorldView(false)},[north])
  useEffect(()=>{
    if(!open)return
    const close=(event:PointerEvent)=>{if(root.current&&!root.current.contains(event.target as Node))setOpen(false)}
    const escape=(event:KeyboardEvent)=>{if(event.key==='Escape')setOpen(false)}
    document.addEventListener('pointerdown',close)
    document.addEventListener('keydown',escape)
    return()=>{document.removeEventListener('pointerdown',close);document.removeEventListener('keydown',escape)}
  },[open])
  useEffect(()=>{
    if(!open||!canvas.current)return
    let instance:maplibregl.Map
    try{
      instance=new maplibregl.Map({
        container:canvas.current,center:north?[15.65,78.22]:[33,39],zoom:north?4.5:4,
        minZoom:0,maxZoom:10,attributionControl:{compact:true},
        style:{version:8,sources:{land:{type:'geojson',data:'/land.geojson',attribution:'Natural Earth · public domain · 1:110m'}},layers:[
          {id:'sea',type:'background',paint:{'background-color':'#a5cad5'}},
          {id:'land',type:'fill',source:'land',paint:{'fill-color':'#f7f6eb','fill-outline-color':'#9db8ad'}},
        ]},
      })
      map.current=instance
      instance.scrollZoom.disable()
      if(north){
        instance.on('load',()=>{
          // The published NASA source is the 78.125°N, 15.625°E point of a 0.25° grid.
          // This square depicts its approximate cell footprint, not a field or expedition boundary.
          instance.addSource('source-cell',{type:'geojson',data:{type:'Feature',properties:{},geometry:{type:'Polygon',coordinates:[[[15.5,78],[15.75,78],[15.75,78.25],[15.5,78.25],[15.5,78]]]}}})
          instance.addLayer({id:'source-cell-fill',type:'fill',source:'source-cell',paint:{'fill-color':'#50b9c4','fill-opacity':0.28}})
          instance.addLayer({id:'source-cell-line',type:'line',source:'source-cell',paint:{'line-color':'#267d90','line-width':2,'line-dasharray':[2,2]}})
        })
      }
      const resize=new ResizeObserver(()=>instance.resize());resize.observe(canvas.current)
      return()=>{resize.disconnect();instance.remove();map.current=null}
    }catch{setFailed(true)}
  },[open,north])
  useEffect(()=>{
    if(!open||!map.current)return
    const activeMap=map.current
    const markers=visible.map(site=>{
      const button=document.createElement('button')
      button.type='button';button.className=`geo-map-pin ${site.id===region?'selected':''}`
      button.setAttribute('aria-label',north?'Longyearbyen hesap noktasını göster':`${site.name} bölgesini seç`)
      button.title=site.name
      button.dataset.name=site.name
      button.onclick=()=>{if(!north){onSelect(site.id);setOpen(false)}}
      return new maplibregl.Marker({element:button,anchor:'center'}).setLngLat([site.lon,site.lat]).addTo(activeMap)
    })
    if(north){
      const cell=document.createElement('span');cell.className='geo-source-cell';cell.title='NASA iklim modeli kaynak hücresi'
      markers.push(new maplibregl.Marker({element:cell,anchor:'center'}).setLngLat(climateCell).addTo(activeMap))
      activeMap.fitBounds([[7.5,76.5],[24,80.5]],{padding:34,duration:0})
    }else if(visible.length){
      activeMap.fitBounds([[Math.min(...visible.map(site=>site.lon))-1,Math.min(...visible.map(site=>site.lat))-1],[Math.max(...visible.map(site=>site.lon))+1,Math.max(...visible.map(site=>site.lat))+1]],{padding:42,duration:0})
    }
    return()=>markers.forEach(marker=>marker.remove())
  },[open,north,region,sites,onSelect])
  useEffect(()=>{
    if(!open||!map.current)return
    const activeMap=map.current
    const update=()=>{
      activeMap.setProjection({type:worldView?'globe':'mercator'})
      if(worldView)activeMap.easeTo({center:north?[15.65,56]:[33,36],zoom:0.4,duration:window.matchMedia('(prefers-reduced-motion: reduce)').matches?0:450})
      else if(north)activeMap.fitBounds([[7.5,76.5],[24,80.5]],{padding:34,duration:0})
      else if(visible.length)activeMap.fitBounds([[Math.min(...visible.map(site=>site.lon))-1,Math.min(...visible.map(site=>site.lat))-1],[Math.max(...visible.map(site=>site.lon))+1,Math.max(...visible.map(site=>site.lat))+1]],{padding:42,duration:0})
    }
    if(activeMap.isStyleLoaded())update()
    else activeMap.once('load',update)
    return()=>{activeMap.off('load',update)}
  },[open,worldView,north,sites])
  return <div ref={root} className="geo-picker">
    <button className="geo-trigger" aria-label={`Haritadan bölge seç: ${selected?.name||'bölge yükleniyor'}`} aria-expanded={open} aria-controls="geo-popover" onClick={()=>setOpen(value=>!value)}><Icon name="globe" size={16}/><span>{selected?.name||'Bölge'}</span><i aria-hidden="true">⌄</i></button>
    {open&&<section id="geo-popover" className="geo-popover" aria-label={north?'Kuzey araştırma coğrafyası':'Türkiye bölge seçimi'}>
      <header><div><b>{north?'Kuzey hedef alanı':'Türkiye · bölge seç'}</b><small>{north?'Longyearbyen çevresi':'Haritadaki noktaya basarak çalışmayı değiştir'}</small></div><button aria-label="Haritayı kapat" onClick={()=>setOpen(false)}><Icon name="close" size={15}/></button></header>
      <div className="geo-map" ref={canvas} role="img" aria-label={north?'Longyearbyen ve NASA iklim modeli hücresi haritası':'Türkiye araştırma noktaları haritası'}>{failed&&<span>Harita çizilemedi; bölge seçimi aşağıda kullanılabilir.</span>}<div className="geo-view-switch" aria-label="Harita ölçeği"><button aria-pressed={worldView} onClick={()=>setWorldView(true)}>Dünya</button><button aria-pressed={!worldView} onClick={()=>setWorldView(false)}>Bölge</button></div></div>
      {north?<div className="geo-scan"><div><span className="geo-scan-key"/><b>İklim verisi alınan hücre</b><small>78,125°K · 15,625°D · yaklaşık 0,25°</small></div><p>Longyearbyen için üretim simülasyonu bu iklim hücresini kullanır. İşaretli alan tarım arazisi, ölçülmüş su havzası veya sefer rotası değildir.</p></div>
        :<div className="geo-site-list">{visible.length?visible.map(site=><button key={site.id} aria-pressed={site.id===region} onClick={()=>{onSelect(site.id);setOpen(false)}}><span className="geo-site-dot"/>{site.name}</button>):<span>Bölgeler yükleniyor…</span>}</div>}
      <footer>{north?'Araştırma bağlamı · tek hesap noktası':'Noktalar bölgesel sınır değil, kaynak veri ve planlama temsil noktalarıdır.'}</footer>
    </section>}
  </div>
}
