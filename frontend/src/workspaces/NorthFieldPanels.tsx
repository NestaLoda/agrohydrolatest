import type {JsonRecord} from '../api'
import {Icon,list,number,obj} from '../ui'

const text=(x:unknown)=>typeof x==='string'?x:''
const positive=(x:unknown)=>typeof x==='number'&&x>1e-7

export function FieldResearchSummary({result}:{result:JsonRecord|null}){
  const request=obj(result?.request),water=obj(obj(result?.decision_story).water_security)
  const sea=list(water.sources).find(row=>row.id==='desalinated_seawater')
  return <div className="north-field-summary">
    <h2>Saha Güncellemesi · suyun fiziksel kanıtı</h2>
    <p><b>Polar Water Node (PWN)</b>, suyun farklı derinliklerdeki özelliklerini ölçüp kaydetmek için geliştirdiğimiz taşınabilir su ölçüm cihazıdır. Arktik araştırmamızda yeni su verileri üretmek, ölçüm çözümünü gerçek koşullarda denemek ve uygun numune çalışmalarını desteklemek için kullanmayı hedefliyoruz.</p>
    <div className="north-field-states"><div><strong>MEVCUT PROTOTİP · v0.1</strong><span>Kayıt ve profil analiz yazılımı mevcut. Depodaki PWN örneği sentetik olarak etiketli; fiziksel cihazın ve kontrollü su deneyi sonucunun doğrulandığına dair kayıt yok. Bu veri Arktik gözlemi sayılmaz.</span></div><div><strong>ARKTİK SÜRÜMÜNDE HEDEF</strong><span>Deniz ortamında sıcaklık, iletkenlik ve basınç; uygun kalibrasyonla tuzluluk/derinlik hesabı, UTC/konum, yerel kayıt ve kalite metaverisi. Son mühendislik uzman ve sefer görüşüyle belirlenecek.</span></div></div>
    <div className="north-field-links"><b>Kaynak suyu bilgisi karara nasıl bağlanır?</b><span><Icon name="source" size={14}/> Şimdi: model/literatür ve açık kaynak senaryosu · {number(request.source_temperature_c)} °C, {number(request.salinity_g_kg)} g/kg; gerçek sefer ölçümü değil.</span><span><Icon name="sensor" size={14}/> PWN: eşleşmiş su sütununda sıcaklık/iletkenlik/basınç. Fiziksel numune ayrı örneklemedir; izinle kullanılabilirlik ve arıtma kimyası incelenir.</span><span><Icon name="water" size={14}/> Karar bağı: temsil ilişkisi doğrulanırsa yalnız desteklenen kaynak suyu/arıtma girdileri yeniden hesaplanır. {positive(sea?.m3)?'Bu planda deniz suyu arıtımı seçili.':'Bu planda deniz suyu tahsisi yok; gözlem üretim desenini zorunlu değiştirmez.'}</span></div>
    <small>PWN yıllık karasal tatlı suyu, geleceğin havasını veya hasadı ölçmez. Longyearbyen model hücresi kesin TASE istasyonu değildir; konum, zaman, derinlik ve su alma kaynağı eşleşmelidir.</small>
  </div>
}

export function ControlledPilotPanel({result}:{result:JsonRecord|null}){
  const req=obj(result?.request),totals=obj(obj(result?.plan).totals),production=obj(obj(result?.decision_story).production)
  const cropNames=list(production.crops).map(row=>text(row.name)).filter(Boolean).join(', ')
  const rows=[['Sisteme eklenen yeni su',totals.water_m3,'m³/yıl'],['Elektrik tüketimi',totals.electricity_kwh,'kWh/yıl'],['Ayrı ısı gereği',totals.heat_kwh_th,'kWh ısıl/yıl'],['Model hasadı',totals.production_kg,'kg/yıl']] as const
  return <section className="north-controlled-pilot"><h2>Kontrollü üretim deneyi</h2><p>Modelin önerdiği yöntemin gerçek su tüketimini, enerji ihtiyacını ve hasadını karşılaştırıyoruz.</p><p>Hocamızın mevcut topraksız tarım düzeneğini seçtiğimiz ürün ve araştırma koşullarına uyarlamayı planlıyoruz. Amaç yalnız bitki yetiştirmek değil, üretim modelindeki varsayımları gerçek ölçümlerle değerlendirmek.</p>
    <div className="north-pilot-context"><b>Model bağlamı</b><span>{number(req.target_year,0)} · {number(req.area_m2,0)} m² planlama alanı · {cropNames||'Ürün kararı hesaplanamadı'}</span></div>
    <table><thead><tr><th>Gösterge</th><th>MODELİN HESAPLADIĞI</th><th>DENEYDE ÖLÇÜLEN</th></tr></thead><tbody>{rows.map(([label,value,unit])=><tr key={label}><th>{label}</th><td>{number(value,1)} {unit}</td><td>Henüz ölçülmedi</td></tr>)}</tbody></table>
    <p>Doğrudan fark, pilotun ürünü, alanı, süresi, yetiştirme yöntemi ve su hazırlama koşullarıyla eşleşen beklenti deneyden önce kaydedildiğinde hesaplanır. Bu yıllık plan, küçük pilotun gerçekleşmiş ölçümü değildir.</p>
    <p>Uygunluğu incelenip gerekli işlemlerden geçirilmiş fiziksel numune ya da ölçülen kimyaya göre <b>yeniden oluşturulmuş deney suyu</b> kullanılabilir. İkincisi Arktik'ten alınmış numune değildir. Bu deney bütün Arktik tarımını doğrulamaz; kayıtlar model katsayılarını otomatik değiştirmez.</p>
  </section>
}
