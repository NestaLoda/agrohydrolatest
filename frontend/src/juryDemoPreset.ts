// Guided preview configuration. Every displayed quantity is read from the live API.
export const juryDemoPreset = {
  turkey: {pilotRegion:'konya',waterPreset:'water20',transferRegion:'gediz_manisa'},
  north: {
    request:{site_id:'longyearbyen',horizon_id:'mid',scenario_id:'ssp245',objective:'balanced',production_purpose:'fresh_mass',
      available_power_kw:null,production_retention:1,minimum_crop_share:.05,area_m2:100,roof_ratio:1,
      storage_m3_per_m2:.1,collection_efficiency:.8,desalination:true,freshwater_m3:0,heat_cop:1,
      energy_limit_kwh:null,salinity_g_kg:35,source_temperature_c:2,recovery:.45,
      disabled_crops:[],disabled_methods:[]},
    referenceYear:2026,yearOffsets:[0,10,25,50],defaultYearOffset:25,
  },
  steps: [
    {id:'konya-baseline',title:'KONYA — İLK PİLOT',caption:'İlk projemizde mevcut ürün deseninin su baskısını karar destek sistemiyle inceliyoruz.',focus:'baseline',seconds:9},
    {id:'konya-water',title:'SU KOŞULU DEĞİŞİYOR',caption:'Aynı bölge, su sınırı %20 daha düşük: sistem ürün desenini yeniden hesaplıyor.',focus:'turkey-decision',seconds:12},
    {id:'turkey-transfer',title:'TÜRKİYE — AYNI MOTOR',caption:'Konya’daki karar mantığı farklı ürün ve su koşullarında yeniden çalışıyor.',focus:'turkey-decision',seconds:11},
    {id:'future-change',title:'2026 MODEL YILI → GELECEK',caption:'Zamanla iklim koşulları değişiyor; aynı kaynak kısıtlarıyla karar yeniden hesaplanıyor.',focus:'north-climate',seconds:13},
    {id:'north-plan',title:'GELECEĞİN ÜRETİM VE SU YÖNETİMİ PLANI',caption:'Mevcut verilerle ürün miktarını, yöntemi ve yeni suyun kaynağını birlikte hesaplıyoruz.',focus:'north-decision',seconds:19},
    {id:'field',title:'KARARIN SAHADA SINANACAK GİRDİLERİ',caption:'PWN ile su profili, ayrı numuneyle kaynak kimyası; yalnız desteklenen girdileri güncelleyeceğiz.',focus:'field',seconds:14},
    {id:'pilot',title:'KONTROLLÜ ÜRETİM DENEYİ',caption:'Model yöntemini gerçek yeni su, elektrik, ısı ve hasat ölçümleriyle değerlendireceğiz.',focus:'pilot',seconds:11},
    {id:'continuity',title:'TEK ARAŞTIRMA HATTI',caption:'Modelle → ölç → yeniden hesapla → doğrula.',focus:'continuity',seconds:10},
  ],
} as const

export const juryDemoYears = juryDemoPreset.north.yearOffsets.map(offset =>
  Math.min(2100, juryDemoPreset.north.referenceYear + offset))
export const juryDemoDefaultYear = Math.min(2100,
  juryDemoPreset.north.referenceYear + juryDemoPreset.north.defaultYearOffset)
export const juryDemoDurationSeconds = juryDemoPreset.steps.reduce((total,step)=>total+step.seconds,0)
