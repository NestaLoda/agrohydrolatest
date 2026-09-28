# Future North yeniden yapımı — 23 Eylül 2026

Bu belge yeni Kuzey uygulamasının hesap sözleşmesidir. Son test sayıları ve teslim durumu [BUILD_STATUS](BUILD_STATUS.md) içindedir. Bağlayıcı kullanıcı isteğinin değişmemiş kopyası [23 Eylül sözleşmesi](archive/FUTURE_NORTH_REBUILD_CONTRACT_2026_09_23.txt). Daha eski Kuzey ekranı, tek 2035 yılı veya üç sabit ürün anlatımları tarihsel uygulama kayıtlarıdır.

## Ürün ve kapsam

Tek araştırma çizgisi: Konya mevcut desen → Türkiye bölgesel aktarım → Kuzey geleceğin üretim sistemi → PRE → günümüz saha kanıtı → aynı motorla POST → kontrollü üretim pilotu. Türkiye'nin mevcut desen, iklim senaryosu, düğmeyle hesap ve sabit su karşılaştırması akışı korunur. Yeni Kuzey arayüzü `/api/north/*` uçlarını kullanır; eski `/api/simulate` sözleşmesi Türkiye ve tarihsel yeniden üretim için tutulur. İki modun su/ürün kanıtları birbirine karıştırılmaz.

Kuzey ilk açılışında kullanıcı ürün miktarını yazmaz. Longyearbyen çevresinin seçilen gerçek projeksiyon dönemi, kaynaklı ürün kataloğu ve açık mühendislik koşulları kullanılarak ürün × yetiştirme alanı × üretim yöntemi × sezon ve su tahsisi hesaplanır. Türkiye'de ilk açılış otomatik öneri değildir; bu Kuzey davranışı Türkiye'ye taşınmamıştır.

**Hesap ölçeği varsayılan 100 m² tek kat yetiştirme yüzeyidir.** Bina koridoru, fide ve yardımcı tesis alanı bu sayıya dahil değildir. Çatı/yetiştirme alanı oranı 1, depo 0,1 m³/m² ve toplama verimi 0,8 görünür tasarım tercihleridir; mevcut Longyearbyen tesisi, tarımsal arazi izni, su hakkı veya elektrik kapasitesi değildir. Kullanıcı değiştirdiğinde MANUAL OVERRIDE olur. Normalleştirilmiş sonuç, tesis tasarımını karşılaştırmak için gereken üretim/su/enerjiyi verir; yerel yatırım uygulanabilirliği kanıtı değildir.

## Gerçekte bağlanan kanıt

| Katman | İşlenen kanıt | Sınır |
|---|---|---|
| İklim | NASA NEX-GDDP-CMIP6 **v2.0**, ACCESS-CM2, MPI-ESM1-2-HR, MRI-ESM2-0; günlük Tmin/Tmax/yağış/kısa dalga | Üç aileden birer üye; tam CMIP6 ensemble'ı değil |
| Dönem | 1995–2014; 2021–2040; 2041–2060; 2081–2100; SSP2-4.5/SSP5-8.5 | 2030/2050/2090 etiketleri dönem ufkudur, tek takvim yılı tahmini değil |
| Yerel kontrol | 1995–2014 ERA5-Land sıcaklık serisi, Open-Meteo üzerinden | Yeniden analiz; istasyon ölçümü değil. Projeksiyona gizli düzeltme uygulanmadı |
| Ürün | EDEN ISS 2018 deneyinin 6 ürününde alan/çevrim verimi, ışık, sıcaklık, nem/CO₂; üç açık tarla araştırma adayı | Antarktika kapalı üretim analoğu, yerel Arktik hasat değil |
| Zemin | MOSJ Janssonhaugen 1998–2024 aktif tabaka, gerçek 27 değer; 2024=218 cm | Yaklaşık 20 km uzaktaki nokta; parsel toprağı/izin/gelecek permafrost değil |
| Toprak | SoilGrids gerçek nokta yanıtı; üç topsoil değeri null; ESA CCI v5 metadata | SoilGrids null sıfır sayılmaz; CCI raster pikseli indirilmiş gibi sunulmaz |
| Su güvenliği | SINTEF/UNIS Isdammen araştırması, yağış-kar-depo fizik hesabı | İçme suyu hacmi tarımsal tahsis değildir; yerel tarımsal kapasite doğrulanmadı |
| Kaynak suyu | MIT deniz suyu termofiziği, DuPont membran sıcaklık/işletim korelasyonları | Sıcaklık/tuzluluk başlangıcı açık kaynak senaryosu; gerçek yerel TOPAZ profili indirilmedi |

İklim serileri her modelde ayrı işlenir. Günlük sıcaklıklar önce modeller arasında ortalanıp don/ısıtma eşiğine sokulmaz. Üç model min–maksı olasılık veya güven aralığı değildir. Yerel tarihsel yeniden analiz karşılaştırması NASA hücresinin soğuk temsil farkını gösterir. Hücre merkezi yaklaşık 78,125°N, 15,625°E; yerleşim meteorolojisi diye sunulmaz. Model altkümesinin kendi aralığı bu temsil hatasını kapsamak zorunda değildir.

Ayrıntılı birincil kaynak, DOI, değişken, sürüm, dönem, dosya, SHA-256 ve işlem:

- [İklim araştırması](research/NORTH_CLIMATE_RESEARCH.md)
- [Ürün ve zemin araştırması](research/NORTH_CROP_GROUND_RESEARCH.md)
- [Su ve enerji araştırması](research/NORTH_RESOURCE_RESEARCH.md)
- `data/north/rebuild_climate/manifest.json`, `crop_evidence_v2.json`, `ground_evidence.json`, `resource_evidence.json`.

NASA/Copernicus/ERA5 kamu verisi bizim Arktik saha ölçümümüz değildir. Xu 2026 çalışmasının MaxEnt/CHELSA/beş-GCM modeli yeniden üretilmiş değildir; kaynak makale iklim uygunluğu ile permafrost/üretim uygunluğu ayrımını temellendirir.

## Adaylar ve miktar

Marul, roka, turp, alabaş, pazı, fesleğen: tam çevrim sayısı `floor(sezon günü / deney ortalama çevrim günü)`. Hasat `alan × tam çevrim × kg/m²/çevrim`. Pazı/fesleğen çevriminin çoklu hasatları zaten deney verimine dahildir; tekrar gün başına yeni tam hasat sayılmaz. Son eksik çevrim sayılmaz. Yıllık takvim 365 gün kullanır; artık gün ek bir tamamlanmamış çevrim hasadı yaratmaz.

Mayıs–Eylül (153 gün), Mart–Ekim (245 gün), yıl boyu (365 gün) karşılaştırılan **işletme takvimleridir**; dış iklimin doğal yetişme sezonu diye etiketlenmez. Seçilen takvimin tüm günlerinde işletim gereksinimi hesaplanır; çevrim arası boşluk, fide veya arıza kaybı otomatik verim artışı yaratmaz. Bu kayıplar ve kapalı sezonda don koruma gerçek tasarım/pilot bağımlılığıdır.

Arpa, patates, buğday araştırma portföyündedir. Arpanın yaklaşık 2500 Fahrenheit derece-gün/32°F taban eşiği 1388,89 Celsius derece-gün/0°C tabana doğru çevrilir. GDD5 ile karşılaştırılmaz. Çeşit bazlı kaynak eşiği bulunmayan ürüne eşik uydurulmaz. Açık tarla için parsel/zemin doğrulaması henüz yoktur: alana sıfır atamak fiziksel olarak bütün Arktik tarımı imkânsız ilan etmek değil, açık bir muhafazakâr planlama politikasıdır.

Sera ve kapalı ortam burada kontrollü kök sistemiyle birlikte tanımlanmış iki **tesis seçeneğidir**. Hidroponik kök sistemi sera içinde de olabilir; bunlar fiziksel olarak birbirini dışlayan kök yöntemleri değildir. Uygulama `greenhouse` = güneş geçirgen kontrollü sera, `hydroponics` = yalıtılmış kapalı kontrollü tesis olarak gösterir. Her ikisinde yerel temel/yapı onayı gerekir.

## Kaynak denklemleri

`north_resources.py` denklemleri ve parametreler `resource_evidence.json` içinde kaynaklı değer, mühendislik varsayımı ve yerel bilinmeyen olarak ayrılır.

1. **Isı:** zarf iletim katsayısı × zarf alanı ve hava değişiminin duyulur kaybı; günlük Tmin/Tmax'tan yeniden kurulan saatlik dış sıcaklık. Gece/gündüz 19/21°C set noktaları. Güneş, LED, pompa, fan ve nemalma ısı kazançları; dışarı çıkan buharın gizli ısı kaybı. Gereken ısı ile elektrik ayrı tutulur. Günlük veriden saatlik şekil yeniden kurmak saatlik gözlem değildir. Temel/zemin kaybı, gerçek bina kontrolü ve yerel kalibrasyon yoktur.
2. **Işık:** kaynak DLI, yayınlanan 15 saat tam + iki 1 saat yarım ışığın toplamından gelir. Model aynı günlük foton toplamını 17 saatlik düz ışık penceresine dağıtır; yayın rampasının birebir elektrik/ısıl zamanlaması değildir. Doğal ışık hedefi aşarsa kontrollü gölgeleme varsayılır. Elektrik açığı LED foton verimiyle hesaplanır.
3. **Kontrollü su:** genel Penman–Monteith, belirtilmiş hava/kanope direnci, nem ve ışık üzerinden su duyarlılığı. Referans çim ET₀ veya kalibre edilmiş ürün ET'si değildir. Drenaj geri kazanımı ve geri kullanılan yoğuşma bir kez çıkarılır; devridaim ayrı bedelsiz dış su kaynağı sayılmaz. Kanope gelişimi, dezenfeksiyon/temizlik ve ayrıntılı besin bütçesi yerel pilotta sınanacaktır.
4. **Yağış/kar:** sıcaklık eşiğiyle faz ayrımı; kar deposu ve derece-gün erimesi; çatıda toplanabilir giriş. Günlük kronoloji korunur. Kar savrulması/çatı kar yükü, donmuş tesis ve gerçek yakalama tek bir katsayıyla doğrulanmış sayılmaz.
5. **RO:** tuzluluk, sıcaklık ve geri kazanımdan konsantre/ozmotik basınç; sıcaklığa bağlı geçirgenlik, net sürücü basıncı, pompa ve enerji geri kazanımı. Basınç sınırı aşılırsa deniz kaynağı LP'den çıkarılır. Sıfır altı kaynak suyu için 0°C'ye koşullandırma ısısı ayrıca eklenir. Isı `kWh_th`, elektrik `kWh_e`; COP yalnız eşdeğer elektrik hedefinde kullanılır. Özgül iyonlar, bor, fouling/scaling, mikrobiyoloji ve konsantre izinleri bu hesabın dışında laboratuvar/tasarım işidir.

35 g/kg ve 2°C başlangıcı yerel ölçüm veya doğrulanmış gelecek deniz profili değildir: görünür kaynak senaryosudur. Tuzluluk 25–37 g/kg ve −1…8°C duyarlılık aralıkları da bir yerel güven aralığı değil, açık stres senaryosudur. Kütlesel tuzluluk g/kg, Practical Salinity/PSU ile sessizce değiştirilemez.

## Optimizasyon

`north_optimizer.solve_pattern` SciPy/HiGHS doğrusal programını hem PRE hem POST için kullanır. Değişkenler: her ürün–yöntem–sezon seçeneğinin alanı; aylık depodan kullanım, arıtılmış deniz suyu, varsa beyan edilmiş tatlı su; ay sonu depo ve taşma.

`Σ alan ≤ seçilmiş yetiştirme alanı`.

Her ay: `Σ alan × yeni su katsayısı = depodan + arıtmadan + tatlı su`.

Depo: `S_ay = S_önceki + toplama − kullanım − taşma`, `0 ≤ S ≤ depo kapasitesi`. İlk depo sıfırdır; bedelsiz başlangıç suyu yoktur. Aynı fiziksel alan yılın farklı sezonları için iki kez atanmaz; sezon seçenekleri tam alan kapasitesinde birbirleriyle yarışır. Bu muhafazakâr tahsis, ayrıntılı ardışık münavebe planlayıcısı değildir.

Yerel tatlı su varsayılan tahsisi sıfırdır: **mevcut yerel su yok** demek değildir. Belediye suyuna doğrulanmamış tarımsal çekim yüklememe politikasıdır. Deniz kaynağı seçilmişse arıtma tesisinin gereken kapasitesi koşullu hesaplanır, tesis mevcut varsayılmaz. Kullanıcı ayrıca elektrik eşdeğeri üst sınırı verebilir; boşken gereken elektrik/ısı kapasitesi çıktı olur, yerel şebekenin bunu sağlayabildiği söylenmez.

**Güncel dengeli amaç — TESLİM017, 23 Eylül 2026:**

1. Her etkin nicel ürüne toplam planlama alanının en az `minimum_crop_share` payını ayır; varsayılan %5, kullanıcı tarafından görünür biçimde değiştirilebilir. Bütün ürün tabanları birlikte alanı aşarsa reddet; kaynaklar yetmezse sessizce taban gevşetme.
2. Bu çeşitlilik ve fiziksel sınırlarla en yüksek toplam taze yenebilir hasadı `Pmax` bul. Sonraki denge için `P ≥ 0,95 Pmax` koru. %95 bir planlama tercihidir, bilimsel sabit veya kanıtlanmış gıda yeterliliği değildir.
3. Aynı hasat tabanında ayrı su-minimum ve enerji-minimum uçlarını hesapla. `rW=(W−Wmin)/(W_at_Emin−Wmin)` ve `rE=(E−Emin)/(E_at_Wmin−Emin)`; en büyük normalize uzaklığı küçült. Gizli ağırlık yok; bu iki kaynağa eşit önem verme tercihi açıktır. Bir eksendeki uçlar çakışıyorsa sıfıra bölmek yerine ortak minimumu koru.
4. Aynı denge düzeyindeki eşit çözümler arasında hasadı artır, sonra enerji ve suyu azalt.

Eski max-min göreli ürün payı amacı kaldırılmıştır. Artık 1/6 eşitliği dayatılmaz; gerçek aynı katsayılar bunu gerektiriyorsa yine eşitlik çıkması yasaklanmaz. Taze kg amacı yüksek taze kütle veren ürünü öne çıkarabilir; kalori, protein, piyasa talebi veya kâr üstünlüğü iddiası değildir. Ana ekranda %95 hasat ve ürün başına %5 alan politikası; ayrıntıda tüm amaç/karşılaştırma uçları görünür.

Kaynak öncelikli amaçlarda önce bu yeni dengeli miktarlar hesaplanır; **her ürün için ekranda seçilen %50–100 koruma oranı** alt sınır olur. Çeşitlilik tabanı ayrıca korunur. Varsayılan üretim koruması %100. Su önceliği su→enerji; enerji önceliği enerji→su. Aynı çıktıyı verebilirler. Kaynak tasarrufu için alanın tamamının kullanılması zorunlu değildir; boş alan açık gösterilir.

Isı + elektrik toplanarak satış/ölçüm birimi yaratılmaz: yalnız açık COP ile `elektrik + ısı/COP` plan karşılaştırma hedefidir. Ana ekranda ikisi ayrı gösterilir. Gelir/fiyat verisi yokken kâr iddiası veya eğitilmiş model yokken AI iddiası yapılmaz.

## Belirsizlik ve günlük sınama

Aynı motor şu durumlarda yeniden çözülür: her gerçek GCM ayrı; EDEN gözlenen verim min/maksı; tutarlı verimli/merkez/yoğun mühendislik konfigürasyonları; toplama ×0,5/1,5 stres testi; deniz sıcaklık/tuzluluk senaryoları. Ürün verim aralığı gözlenen deney aralığıdır, geleceğin istatistiksel güven aralığı değildir. Model ailesi ve mühendislik konfigürasyonları gerçek olasılık ağırlıklarıyla örneklenmiş değildir.

DUYARLI raporlama eşiği: alan değişimi `max(0,01 m², alanın %0,1'i)` üzerinde, uygulanabilirlik değişimi, hasat miktarı veya elektrik eşdeğeri %5 üzerinde veya arıtma suyu farkı toplam suyun %5'i üzerinde. Bunlar açık ekran raporlama eşikleridir; istatistiksel anlamlılık testleri değildir. Desen aynı kalırken kaynak gereği değişebilir. İncelenen aralık dışında sağlamlık iddiası yoktur. Eksik/infeasible koşu sayısal sıfır enerji gibi belirsizlik aralığına alınmaz; ayrı belirtilir.

Ana LP ortalama aylarla çalışır. Seçilen alanların günlük su gereği **her modelin 20 yıllık tam kronolojisinde** çatı/kar/depo dengesinden yeniden geçirilir. Yıllık yağış sonrası yedek kaynak gereği min/ortalama/maks ve en yüksek günlük açık gösterilir. Bu sonuç henüz seçilmemiş arıtma tesisinin tasarım debisine bilgi verir. Tatlı su hakkı, tedarik kesintisi ve gerçek işletme güvenilirliği hâlâ ayrı doğrulama gerektirir; ortalama aylık plan günlük garanti değildir.

## Dönemler arası karar anlatımı — TESLİM017

`POST /api/north/timeline` tarihsel 1995–2014 → 2030 (2021–2040) → 2050 (2041–2060) → 2090 (2081–2100) için aynı motoru çözer. Gelecek dönemleri aynı SSP; alan, çeşitlilik/amaç, verim analoğu, kaynak hakkı, depo, çatı, enerji ve diğer mühendislik koşulları sabittir. Tarihsel nokta bugünkü gözlenmiş ekiliş değildir. Aradaki yıllara sahte interpolasyon yapılmaz. Farklar alan payında yüzde puan, yeni suda m³/yıl ve ısıda başlangıca göre yüzde olarak gösterilir; karşılaştırma başlangıcı seçilebilir. Hesaplanamayan plan sıfır kaynak tüketimi sayılmaz.

`climate_frontier` mevcut katalogdaki arpa ısı gereği ve FAO ECOCROP kaynaklı arpa/patates sıcaklık–süre zarfıyla **kısmi açık tarla araştırma ön elemesi** üretir. Her model-yıl ayrı işlenir, testler aynı model-yılda birlikte sağlanır; farklı modellerin test başarıları birleştirilmez. Tür sıcaklık zarfına hareketli pencere uygulanması açık araştırma kuralıdır, doğrulanmış çeşit fenolojisi değildir. Model-yıl sayısı olasılık sayılmaz. Kaynak `data/auto_baseline_parameters.json` hash'i de provenansa girer. Buğday için eksik eşik uydurulmaz. Kontrol edilen iklim boyutları olumlu olsa da çeşit/don/fotoperiyot/zemin/su doğrulanmadan açık tarla alanı atanmaz.

İklim ön elemesini geçen patates model-yılları: historical0/60; near2450, mid2453, late2458; near5852, mid58511, late58551. Arpa late2451/60, late58519/60; önceki pencerelerde0. Bunlar tam yetiştirme uygunluğu veya gerçekleşme olasılığı değildir. Ana ekran iklim sınırı → su/zemin/enerji filtresi → gerçek koşullu üretim planını ayırır.

`north_decision_story` mevcut hesabı değiştirmeden üretim, su, altyapı ve risk eylemlerini türetir. Ana su özeti aylık LP'nin kaynak paylarını; ayrıca her modelin günlük depo tekrarından en fazla yedek isteyen ortalama ayı, model-yıl yedek aralığını ve en yüksek günlük gereği gösterir. Seçilen depo ile gözlenen model doluluğu ayrı; `minimum_required_m3=null`, depo kapasitesi optimize edilmedi. En zor model-yıl, mutlaka en az yağışlı yıl değildir; boş başlangıç deposu özellikle ilk yıl sonucunu etkileyebilir. Fiziksel arıza eşiği taraması yapılmadı; sahte eşik uydurulmaz.

100 m² normalize birim yanında 1.000 m²/1 ha ölçekleri tekrar hesaplanır. Çatı/depo oranları alanla büyür; açık mutlak enerji ve tatlı su sınırları aynı kalır. Bu nedenle kullanıcı mutlak sınır koyduğunda her çıktı körlemesine çarpılmaz. Mevcut arazi veya tesis hakkı yaratılmaz. PWN / izinli numune / diğer araştırma üç ayrı kapsam etiketiyle planın altında görünür.

## Saha ile bağ

`north_field` PRE üretim girdisi, sonuç, model kod özeti, kaynak hashleri, zaman, model profili ve su alma derinliğini değişmez JSON + SHA256 olarak saklar. Motor Python dosyaları aynı kod özeti altında arşivlenir; Python/SciPy sürümü kaydedilir. Önceden indirilen PRE kimliğiyle kayıt tekrar açılabilir. Beklenti sunucuda gerçek gözlemden önce dondurulur. POST aynı derinlikle; UTC geçerlilik aralığı, ≤1 km eşleştirme politikası, derinlik kapsamı, tanım, cihaz, kalibrasyon ve kabul edilmiş kalite kaydıyla doğrulanır. 1 km eşik akıntı/temsil uzman değerlendirmesinin yerine geçmez.

Model beklentisinin seçilen derinliğindeki T/S, PRE hesap girdisine aktarılır; başka derinlikteki veya başka varsayımlı ilk planla gizlice kıyaslama yapılmaz. POST yalnız deniz kaynak sıcaklığı/tuzluluğu ve bunlardan türeyen RO elektrik, koşullandırma ısısı ve basınç uygulanabilirliğini günceller. Kaynak kullanımı yetkisi değişmez: kullanıcı deniz kaynağını kapattıysa gözlem bunu açamaz.

Geçmiş model beklentisi ile geçmiş gözlem yükleyip sonradan PRE üretmek kabul edilmez. Profil dışına derinlik kestirimi yapılmaz. Potansiyel sıcaklık doğrudan yerinde sıcaklık sayılmaz. Gerçek TOPAZ ithali öncesinde değişken tanımı/koordinatlar/zaman desteği ve gerekiyorsa TEOS dönüşümü kaynakça ve ham veriyle çözülmelidir. Güncel ürünün günlük ve aylık 3B ürünleri bulunması, indirilmiş bir profil olduğu anlamına gelmez. Günlük/aylık ensemble ortalaması anlık CTD profili değildir.

Saha konumu ile planlanan su alma noktası fiziksel bağı kaynaklı beyan ister; program bu hidrolojik bağı bağımsız kanıtlamış sayılmaz. Bir 2027 profili 2050 iklimini doğrulamaz. POST sonucu **günümüz kaynak gözlemiyle bilgilendirilmiş koşullu gelecek kaynak senaryosudur**. Gelecek iklimi, yıllık kara suyu, ürün verimi, zemin ve amaç değişmez. Alan/su/elektrik/ısı/uygulanabilirlik farkı raporlanır; değişmeyen desen geçerli sonuçtur.

Arayüzdeki sentetik örnek ayrı `SIMULATION_EXPLANATORY` sınıfıyla çalışır; ölçüm veya gerçek model–gözlem doğrulaması değildir. Gerçek profil ithali için JSON şemaları `/openapi.json` içindeki `ModelExpectation`, `Observation`, `FreezeRequest`, `ObserveRequest` sözleşmeleridir.

Fiziksel numunenin panel/sayı/derinlikleri henüz kesin değildir. İzotoplar veya seçilmiş kaynak/arıtma kimyası ancak karar bağlantısı, uzman/laboratuvar ve izinle belirlenir. Deney sonrası kaynak suyu → koşullandırma → besin çözeltisi → kontrollü bitki tepkisi hattı gerçek veya ölçülen kimyaya göre açıkça sentetik suyla kurulabilir. Bu tüm gelecek tarım modelini doğrulamaz.

## Dosyalar ve tekrar çalıştırma

- İklim: `scripts/ingest_north_rebuild_climate.py`, `scripts/check_north_historical_temperature.py`, `backend/north_climate.py`.
- Katalog/zemin: `backend/north_candidates.py`, ilgili kanıt JSON'ları.
- Fizik: `backend/north_resources.py`, `data/north/resource_evidence.json`, `data/north/resource_sources/` ham kaynak/hash kayıtları.
- Hesap: `north_planning.py` → `north_optimizer.py`; servis `north_api.py`; Pydantic `north_contracts.py`.
- Saha: `north_field.py`; yerel `data/north/frozen_runs/` değişmez PRE/POST kayıtları.
- Karar anlatımı: `north_timeline.py`, `north_decision_story.py`, `scripts/verify_north_story.py`.
- UI: `frontend/src/workspaces/NorthConsole.tsx`, `NorthDecisionStory.tsx`, `north-story.css`, `north-console.css`; `App.tsx` Kuzey yönlendirmesi.
- Önbellek: `data/north/derived_plans/`; iklim, ürün, kaynak, zemin ve hesap kodu özetleriyle anahtarlanır. Ham veri yerine geçmez; yeniden üretilebilir.

Derleme: `cd frontend; npm.cmd run build`. Python testleri: `.venv/Scripts/python.exe -m pytest tests -q`. Sunucu: `.venv/Scripts/python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8011`. Gerçek iklim edinimi eksikse sistem onu tam paket gibi göstermeyi reddeder. Mobil test yapılmaz.

Tamamlanmamış bilimsel işler: yerel klimatolojik referansla ayrı kalibrasyon/doğrulama; daha geniş GCM/bölge kapsamı; gerçek parsel ve tahsis; gerçek tedarik/sera tasarımı, CO₂/temizlik/işletme kayıpları; güncel ve eşleştirilmiş sayısal TOPAZ profili; uzman onaylı saha/lab protokolü; gerçek TASE gözlemi; yerel kontrollü tarım pilotu. Bunlar mevcut mühendislik hesabının koşulları olarak görünür, tamamlanmış ölçüm diye sunulmaz.
