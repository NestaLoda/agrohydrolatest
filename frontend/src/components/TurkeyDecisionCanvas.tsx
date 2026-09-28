import type {PlanningContext,SimulationRequest,SimulationResult} from '../planning'
import {Download,Icon} from '../ui'
import TurkeyDecisionSupport from './TurkeyDecisionSupport'
import TurkeyOutcome from './TurkeyOutcome'
import CurrentWeather from './CurrentWeather'
import SimulationResults from './SimulationResults'
import TurkeyAnalysisExplorer from './TurkeyAnalysisExplorer'
import TurkeyEconomics from './TurkeyEconomics'

export default function TurkeyDecisionCanvas({context,scenario,result,stale=false}:{context:PlanningContext;scenario:SimulationRequest;result:SimulationResult|null;stale?:boolean}){
  return <div className="turkey-decision-canvas">
    <TurkeyDecisionSupport context={context} result={result} stale={stale}/>
    {result?.optimized&&<TurkeyOutcome context={context} result={result} compact/>}
    {result?.optimized&&<TurkeyEconomics key={result.request.region_id} result={result}/>}
    {result?.optimized&&<TurkeyAnalysisExplorer context={context} result={result}/>}
    <details className="result-audit"><summary><Icon name="source" size={14}/> Veri, varsayımlar ve hesap kaydı{result&&<span>· {result.run_id.slice(0,10)}</span>}</summary>
      <div className="evidence-lines"><span><b>KAYNAK</b>{String(context.region.year)} resmî il deseni · ERA5</span><span><b>HESAP</b>FAO-56 su gereği · matematiksel optimizasyon</span><span><b>SENARYO</b>Su sınırı · ekim takvimi · sulama verimi · üretim sınırları</span><span><b>UYGULAMA ÖNCESİ</b>Gerçek su tahsisi ve saha koşullarıyla doğrulanır</span></div>
      <p className="small muted">İklim sürgüleri kaynak hava serisine göre varsayımsal değişimlerdir. Sıcaklık etkisi, <a href="https://www.fao.org/4/X0490E/x0490e07.htm" target="_blank" rel="noreferrer">FAO-56 Denklem 52</a> sıcaklık teriminin oranıyla günlük kaynak ET₀ üzerine uygulanır; yerel kalibrasyon gerektiren bir duyarlılık hesabıdır. Yağış ayrı ölçeklenir. Verim, ekim takvimi ve diğer meteoroloji değişkenleri sabit kalır; bölgesel iklim tahmini değildir. Elle girilmiş net sulama iklim sürgülerinden etkilenmez.</p>
      <CurrentWeather key={scenario.region_id} region={scenario.region_id}/>
      {result&&<Download data={result} filename={`plan-${result.run_id}.json`}/>}
      <SimulationResults context={context} scenario={scenario} result={result}/>
    </details>
  </div>
}
