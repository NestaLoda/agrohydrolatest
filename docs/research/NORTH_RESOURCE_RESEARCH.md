# Future North: su ve enerji araştırması / hesap sözleşmesi

23 Eylül 2026 · `north-resources-physics-1` · Birincil kaynak araştırması, açık mühendislik senaryosu ve yazılım doğrulaması. **Saha ölçümü veya yerel tesis fizibilite onayı değildir.**

## Ön inceleme ve korunan bilim

Yeni rebuild sözleşmesi, `SCIENTIFIC_ARCHITECTURE.md`, `FUTURE_PRODUCTION_MODEL.md`, `DATA_REQUIREMENTS.md`, `EVIDENCE_MAP.md`, `NORTH_WATER_SECURITY.md`, `PWN_VALIDATION_PLAN.md`, `hardware/pwn-v0.1/DATA_SCHEMA.md` ve Arctic sensör gereksinimleri; çalışan `science.py`, eski optimizer ve `literature_parameters.json` birlikte incelendi. Türkiye'nin test edilmiş hesapları ve önceki kaynak paketleri değiştirilmedi.

Korunan sınırlar: iklimsel uygunluk sürdürülebilir üretim uygunluğu değildir; fiziksel su varlığı tahsis edilmiş kullanılabilir su değildir; PWN yıllık karasal suyu veya gelecek verimi ölçmez. Ham C/T/p, kalibrasyon, UTC/konum ve türetilmiş tuzluluk ayrı tutulur. Konya'nın tarihsel yaklaşık %8,7 sonucu göreli su baskısıdır. Barbosa'nın Arizona marulu su/enerji katsayıları Arktik işletme katsayısı yapılmadı. Yeni kaynak modülü önceki 5–18°C açıklayıcı RO interpolasyonunu kullanmıyor; eski dosyalardaki geçmiş kapsam kendi tarihiyle geçerlidir.

Yeni iş: günlük gelecek iklimi → bina/ışık/bitki-su hesabı → kar gecikmeli çatı toplama ve depo → eksik kaynak suyu için RO enerjisi. Ortak optimizasyon ve PRE/POST orkestrasyonu ana ajana aittir. Bu belgede yalnız kaynak alt modelinin uygulanmış kapsamı anlatılır.

## Planlama birimi ve yerel bağlam

Hesap **tek yetiştirme katında 1 m²**, arayüz örneği **100 m²** üzerinden yapılır. Bu, kullanılabilir yerel arazi veya sera kapasitesi keşfi değildir. Yetiştirme alanı; koridor, fide alanı, ekipman veya bütün tesis taban alanı sayılmaz. Referans geometrisi açık tasarım tercihidir: 10×10×3 m örnek yapıdan 2,2 m² örtü/m² taban ve 3 m³ hava/m² oranı. Gerçek inşaat boyutu/zemin ve temel ısı kayıpları ayrıca araştırılmalıdır.

[SINTEF'in 25 Mart 2026 açıklaması](https://www.sintef.no/en/latest-news/2026/securing-the-water-supply-in-longyearbyen-is-critical/) Isdammen'i Longyearbyen'in tek içme suyu kaynağı olarak tanımlar. SINTEF–UNIS–UiB çalışması 2025–2027 dönemindedir; su dengesi, kaynakların izotoplarla incelenmesi, mangan ve olası permafrost kaynaklı akış değişiklikleri araştırılır. Rapor 2027 ikinci çeyreğinde beklenmektedir. Bunlardan tarıma ayrılabilecek yıllık m³ çıkarılmadı.

`agricultural_freshwater_allocation_m3_year = null`. Referans plandaki belediye suyundan tarımsal çekim **0**, bir koruma politikasıdır; Isdammen'in fiziksel hacmi veya yenilenmesi sıfır demek değildir. Gerçek tahsis, diğer kullanıcılar ve çevresel gereksinimler bilinmeden belediye rezervi tarıma dağıtılamaz.

[Svalbard Energi'nin 16 Ocak 2026 güncel kaydı](https://www.svalbard-energi.no/svalbard-energi-as.587394.no.html) elektrik için dizel, ısı için dizel kazanı ve elektrik üretiminden ısı geri kazanımı bildirir. Kömür santrali Ekim 2023'te kapandı. Tarıma kullanılabilir enerji kapasitesi ve ticari tarife bu kaynakta yoktur; `agricultural_energy_allocation_kwh_year = null`. Konut bölgesel ısı sübvansiyonları tarım fiyatına çevrilmedi. Gelecek altyapı yatırımları bugünkü çalışan kapasite sayılmadı.

## Kontrollü üretimde enerji ve su

`controlled_energy(daily, method, target_temp_c, target_dli_mol_m2_day, photoperiod_h, overrides)` iki yöntem kabul eder: `greenhouse` (ışık geçiren örtü) ve `indoor` (opak kontrollü yetiştirme ortamı). Ana uygulama hidroponik seçeneği `indoor` ile eşler; hidroponik teknik tek başına opak bina anlamına gelmez, bu uygulamanın açık yöntem tanımıdır.

Girdiler tek iklim üyesinin sıralı günlük `date,tmin_c,tmax_c,shortwave_mj_m2` serisidir. Eksik/geçersiz değer sıfıra çevrilmez. Birden çok modelin günlük serileri karıştırılırsa işlev reddeder. Dışarıdaki günlük sıcaklıkla içerideki hedef sıcaklık ayrı kavramlardır.

Hesap zinciri:

1. Örtü iletim kaybı `U × örtü alanı × ΔT`; hava değişimi duyulur kaybı `ρ_air × cp_air × hacim × ACH × ΔT / 3600`.
2. Günlük Tmin/Tmax'tan sinüsle saatlik hava; günlük kısa dalgadan astronomik gün uzunluğuna dağıtılmış saatlik ışınım kurulur. Bunlar ölçülmüş saatlik hava değildir. Kutup günü/gecesi FAO gün uzunluğu hesabının sınır durumlarıdır.
3. Doğal DLI, kısa dalganın görünür PAR payı ve örtü geçirgenliğiyle hesaplanır. PAR payı 0,45 ve 550 nm eşdeğer foton başına 0,219 MJ/mol açık spektral yaklaşımlardır. Fazla güneş için ayarlanabilir gölgelemenin hedef DLI'yi koruduğu varsayılır.
4. LED enerjisi `eksik DLI / (3,6 × LED μmol/J)` kWh/m²/gün. Fotoperiyot gerekli ışık gücünü ve ısının gün içindeki zamanını değiştirir; aynı DLI'yi kısa sürede vermek foton enerjisini kendiliğinden azaltmaz.
5. Genel Penman–Monteith birleşim denklemi canopy su akısını hesaplar: `λE = [Δ Rn + ρ cp VPD/ra] / [Δ + γ(1+rs/ra)]`. Pa/K, W/m² ve s/m tutarlı kullanılır; λ=2,45 MJ/kg. Bu, FAO referans çim ET₀'su değildir. İç nem, yüzey/aerodinamik direnç, canopy radyasyon soğurması açık tasarım hipotezidir. Nem ve dirençlere ürüne özel saha kalibrasyonu yapıldığı iddia edilmez. Gün/gece sıcaklık seçeneği varsa ışıklı ve karanlık dönemler ayrılır.
6. Canopy su kaybı ve ürüne taşınan su, drenaj geri dönüşü ve toplanmış yoğuşma birlikte bilanço oluşturur. Yoğuşmanın geri kazanımı makyaj/tamamlama suyu gereğini yalnız bir kez azaltır. Kalan buharın dışarı atılması ısı gerektirir; içeride yoğuşan kısmın gizli ısısı içeride kalır. Nem alma elektriği ekipmanın L/kWh performansıyla hesaplanır.
7. Pompa elektriği `ρgQH/η`, fan gücü ve nem alma ayrıdır. Saatlik güneş/lamba/pompa/nem alma ısısı ile net ısıtma veya soğutma yükü hesaplanır. Isı pompası soğutma COP'u tasarım parametresidir.

Kaynak–varsayım ayrımı:

| Parametre | Dayanak | Aktarım sınırı |
|---|---|---|
| Çift örtü U=2,84–3,97 W/m²K | [Purdue ısı hesabı](https://www.purdue.edu/hla/sites/cea/article/calculating-greenhouse-heating-requirements/), [UGA B792](https://fieldreport.caes.uga.edu/wp-content/uploads/2025/08/B-792_6.pdf) | Gerçek seçilmiş Arktik yapının ölçümü değil. |
| Sera hava değişimi 0,5–1,0/h | Aynı UGA tablosu, yeni çift plastik | Rüzgâr, kapı kullanımı ve örtü sızıntısı yerelde doğrulanmadı. |
| LED 2,1–3 μmol/J | [Biosystems Engineering CEA bölümü](https://doi.org/10.21061/introbiosystemsengineering/plant_controlled_environment) | Belirli armatür seçimi ve spektrumu değildir. |
| Nem alma 1,70/2,22/3,81 L/kWh | [EPA ENERGY STAR v6](https://www.energystar.gov/products/dehumidifiers/key_efficiency_criteria) | Farklı ekipman sınıflarının standart test ölçütleri; işletme garantisi değil. |
| rs=70–250, ra=70–200 s/m | Genel denklem [FAO56 Bölüm2](https://www.fao.org/4/x0490e/x0490e06.htm); sayısal aralık projenin hipotezi | FAO bu değerleri bizim kontrollü ürünlerimiz için doğrulamaz. |
| Opak yalıtım, pompa/fan, drenaj, yoğuşma, canopy soğurma ve biyokütle suyu | Açık mühendislik senaryoları | Tüm değerler `resource_evidence.json` içinde; pilotla sınanmalıdır. |

[Cornell'in marul rehberi](https://cea.cals.cornell.edu/files/2019/06/Cornell-CEA-Lettuce-Handbook-.pdf) DLI'nin çeşit ve hava hareketine bağlılığını gösterir; tek bir ışık eşiği bütün ürünlere taşınmaz. Ürün katalog setpointleri fonksiyona geçirilmelidir. [EDEN ISS enerji araştırması](https://elib.dlr.de/186936/1/EDEN%20ISS%20Energy_final_v2.pdf) nem/ısıl kontrol ve aydınlatmanın önemini destekler; Antarktika tesisinin toplam kWh/kg değeri Svalbard'a sabit katsayı yapılmadı.

Çıktılar `heat_kwh_th_m2`, `electricity_kwh_m2`, `fresh_makeup_m3_m2` ve ayrı ışık/pompa/fan/nem alma/soğutma bileşenleridir. Her biri `{low,central,high}` taşır. Bunlar **üç beyan edilmiş mühendislik konfigürasyonunun zarfı**, istatistiksel güven aralığı değildir. `equivalent_electricity = electricity + heat/COP` yalnız COP=1 karşılaştırma temelidir; yerel bölgesel ısıyı gerçek elektrik tüketimi gibi göstermez.

`annual` her yılın sonucunu korur; top-level ve `monthly` günlük işlemden sonra yıllar ortalamasıdır. `monthly_configurations` her ay/metrik için üç ham konfigürasyon ortalamasını verir; seçilen aylar **önce aynı konfigürasyonda toplanmalı, sonra zarf alınmalıdır**. Her metrik/ayın farklı minimumunu toplamak tek bir gerçek tesis tasarımı değildir. `daily` merkez konfigürasyondaki gereksinimi verir. `active_months` dışındaki işletim sıfırdır; boş binanın kış don koruması ve bekleme yükü kapsam dışında ayrıca belirtilir.

## Çatı, kar, depo ve yeniden kullanım

`roof_storage_balance(daily,demand_m3,roof_m2,storage_m3,collection_efficiency,initial_storage_m3,melt_factor_mm_c_day,initial_snow_mm)` kronolojik, kesintisiz tek model serisi ister.

Tortalama≤0°C yağışını kar su eşdeğeri deposuna koyar. Sıcak günün erimesi `min(SWE, derece-gün-katsayısı × max(Tort,0))`; erimeden toplama yoktur. [USACE HEC-HMS](https://www.hec.usace.army.mil/confluence/hmsdocs/hmstrm/snow-accumulation-and-melt/temperature-index-method) kuru erime için tipik 2,29–4,57 mm/°C/gün aralığı verir; merkez 3 bir aktarım seçimi. Bu basit kova modeli tam HEC-HMS soğuk içeriği/refreeze hesabı değildir; çatı ısısı, rüzgârla kar kaybı, buz tıkanması ve süblimleşme de yoktur.

`yakalanan_m³ = (yağmur_mm + erime_mm) × yatay_çatı_m² × toplama_verimi / 1000`.

[Texas Water Development Board](https://www.twdb.texas.gov/innovativewater/rainwater/faq.asp) sistem verimi %75–85 aralığını destekler. Arktik çatı performansına kalibre edilmedi. Bu verim zaten toplama kayıplarını temsil eder; aynı kayıp ikinci kez uygulanmaz. Aynı gün gelen su önce talebi karşılar, kalan depoyu doldurur, fazlası taşar. Gün içi yağış/talep zamanlaması bilinmediği için bu sıralama açık yaklaşımdır.

Hem su deposu hem yağış/kar bilançosu artık değeri çıktıda bulunur. Kar ve depo yıllar arasında taşınır; gerçek günlük işlem tamamlanmadan ortalama yıl yaratılmaz. `climatology_monthly[].captured_m3` aylık LP girişidir; seçilen deseni gerçek günlük kronolojide yeniden oynatmak ayrıca gerekir. `deficit_m3` depolanmış yağış dışından gerekecek tamamlama suyudur; otomatik olarak susuzluk veya RO kapasitesi başarısızlığı demek değildir.

100 L/m² varsayılan depo ve 25–250 L/m² karşılaştırmaları **tasarım seçenekleridir**, yerel depo verisi değildir. Çatıdan toplanan suyun kalitesi, hijyeni ve arıtma gereği ayrıca değerlendirilmelidir. `recirculation_makeup` drenajın geri dönüşünü net talepten düşürür; yeniden kullanım yeni ve bağımsız kaynak hacmi yaratmaz.

## RO: tuzluluk, sıcaklık ve geri kazanım

`ro_treatment(salinity_g_kg,temperature_c,recovery=.45,product_water_m3=1,overrides=None)` g/kg **kütlesel tuzluluk**, yerinde °C ve hacimsel geri kazanım ister. PSU/Practical Salinity'yi g/kg diye kabul etmez; bu ayrım gözlem eşleştirme katmanında da doğrulanmalıdır.

Osmotik basınç, [MIT seawater özellikleri](https://web.mit.edu/seawater/) / [Sharqawy 2010](https://doi.org/10.5004/dwt.2010.1079) korelasyonuyla referans deniz suyu bileşimi için hesaplanır. Kullanılan aralık 0–200°C ve ≤120 g/kg'dır. Geri kazanımla konsantre tuzluluğu yaklaşık `S/(1-R)`; gerekli basınç `π_konsantre + NDP25/TCF + ΔP`. Konsantre sonundaki basıncı kullanmak ortalama membran basıncından daha korumacı bir tarama yaklaşımıdır.

[DuPont FilmTec Rev20, Ağustos2026](https://www.dupont.com/content/dam/water/amer/us/en/water/public/documents/en/RO-NF-FilmTec-Manual-45-D01504-en.pdf) Denklem73/74 sıcaklık çarpanı kullanılır: `exp(A × (1/298 − 1/(273+T)))`; A=3020 (T≤25°C), 2640 (T≥25°C). Bu geçirgenlik duyarlılığıdır; sıfıra yakın suda seçilmiş membran yeterliliğinin kanıtı değildir. Çoğu deniz membranı için verilen 83 bar sınırı genel tarama sınırıdır; gerçek element şartı ayrıca seçilmelidir.

Elektrik gereksinimi, ideal basınç değiştirici bilançosu ve açık kayıplarla:

`SEC = Pbar/(36ηpump) × [1 − ηERD(1−R)]/R + Eaux`.

NDP25=5/10/15 bar, pompa verimi=.85/.80/.75, ERD=.98/.95/.90, ΔP=1/2/3 bar ve yardımcı enerji=.2/.4/.8 kWh/m³ **seçilmemiş tesis için açık mühendislik konfigürasyonlarıdır**. [DOE2017 çalışması](https://www.energy.gov/sites/default/files/2017/12/f46/Seawater_desalination_bandwidth_study_2017.pdf) açık deniz örneğinde ön arıtma toplamı .27, son işlemler .11 kWh/m³ verir; alım/konsantre taşınması kot farkına bağlıdır. Bizim .4 merkezimiz bu büyüklükte bir tarama tercihidir, Arktik için ölçülmüş katsayı değildir. Çalışmadaki içme suyu reçetesi doğrudan besin çözeltisi reçetesi yapılmaz.

Sıfır altındaki **sıvı** kaynak suyu, korelasyonun dışında kullanılmak yerine en az0°C'ye koşullandırılır. Isı `ρ cp ΔT/R` ile ayrı `conditioning_heat_kwh_th_m3` çıktısıdır. Deniz buzu eritmenin gizli ısısı hesaplanmaz; sıvı fazın varlığı ve don koruması doğrulanmalıdır. Soğuk membran deneyine duyulan ihtiyaç sonuçtan kaldırılmaz.

Basınç aşılırsa sonuç `PRESSURE_LIMIT_EXCEEDED`; değer83'e kırpılmaz. Örnek 35g/kg,2°C,R=.45 merkez koşulu sınırın altındadır; üst mühendislik konfigürasyonu sınırı aşabilir. 35g/kg/2°C ve duyarlılıkta25–37g/kg/−1…8°C değerleri **seçilmiş stres senaryoları**, yerel deniz profili/olasılık aralığı değildir.

Besleme `Vürün/R`; konsantre `Vürün(1−R)/R`. Tuz bilançosu eşit yoğunluk ve sıfır tuzlu ürün varsayımıyla yaklaşık korunur. Gerçek iyon geçişi, bor, alkalinite, kirlilik, fouling, antiscalant, remineralizasyon/besin koşullandırma ve konsantre deşarjı bu toplam tuzluluk modelinden belirlenmez. Uzman/laboratuvar paneli karar bağlantısına göre seçilmeli; panel/derinlik/numune sayısı burada kilitlenmedi.

## Gerçek deniz modeli beklentisi ve saha kapıları

Doğrulanan [Copernicus ürün](https://data.marine.copernicus.eu/product/ARCTIC_MULTIYEAR_PHY_002_003/description) `ARCTIC_MULTIYEAR_PHY_002_003`. [PUM Kasım2025](https://documentation.marine.copernicus.eu/PUM/CMEMS-ARC-PUM-002-003.pdf) günlük `cmems_mod_arc_phy_my_topaz4_P1D-m` ve aylık `cmems_mod_arc_phy_my_topaz4_P1M` T/S verisini3B listeler; ~12km,40 teslim derinliği ve100 üyeli model ortalaması. Günlük zaman ortası12:00UTC'dir. QUID'nin bazı bölümleri eski günlük yüzey ürününü anlatır; **indirilen değişken boyutları doğrulanmadan iki belgeden birine dayanarak sahte kolon kurulmaz**.

`thetao` potansiyel sıcaklıktır; `so` metadata birimi `1e-3` olan model sea-water salinity'dir. Bunlar otomatik yerinde sıcaklık ve RO için kütlesel tuzluluk sayılmaz. Belgelendirilmiş termodinamik dönüşüm veya tanımları eşleştirilmiş kaynak gerekir. Bu kaynak ajanı sayısal TOPAZ profili indirmedi; katalog/PUM edinimi numeric profile gibi sunulmadı. Kimlik bilgisi/abonelik varlığı varsayılmadı.

`model_profile_provenance(metadata,points)` en aziki gerçek derinlik, sıralı derinlikler, SHA256, ürün/veri sürümü, kaynak/lisans, istek/hücre konumu, yatay çözünürlük, derinlik boyutunun doğrulandığı kayıt, UTC ortalama penceresi ve açık değişken tanımlarını ister. Yüzey pikselini kolon diye kabul etmez. Bu şema doğrulaması, dışarıdan ileri sürülen hash/kalite bilgisinin tek başına doğru olduğunu kanıtlamaz; çağıran edinim katmanı gerçek dosyayla bağı kurmalıdır. Yerinde sıcaklık + kütlesel tuzluluk dışındaki tanımlar RO'ya doğrudan uyumlu bayrağı alamaz.

Saha güncellemesi için ek kapılar kalır: aynı yer/zaman/derinlik, ölçüm kalibrasyonu/QC, model ortalaması–anlık cast temsiliyeti ve senaryo alım noktası–gemi istasyonu aktarımı. PWN sıcaklık/tuzluluğu ilgili arıtma deneyine bağlayabilir; karasal su tahsisi, geleceğin iklimi, toprak veya ürün verimine aynı gözlemden güncelleme yapılmaz. Numune kimyası ve izotoplar ayrı yöntem/laboratuvar kararıdır. Aynı desenin kalması geçerli sonuçtur.

## Dosyalar ve doğrulama

- `backend/north_resources.py`: saf hesap ve profil metadata kapıları; ağ erişimi yok.
- `data/north/resource_evidence.json`: yerel bağlam,29 parametre, kaynak/varsayım ayrımı, RO ve saha ölçülebilirliği.
- `data/north/resource_sources/download_manifest.json`:16 başarılı birincil kaynak indirmesi; URL, gerçek erişim zamanı, finalURL, byte ve SHA256. Ham PDF/HTML/ZIP korunur; PDF metinleri yerel pypdf türevidir.
- `tests/test_north_resources.py`:33 anlamlı test.

**Son doğrulama:** 2026-09-23T00:50:37+03:00, Windows, `.venv/Scripts/python.exe` Python3.12.14, `-m pytest tests/test_north_resources.py -q`: **33 passed**. Elektrik bileşenleri, ısı birimleri, DLI/fotoperiyot, gün/gece hedefi, kaynak eksikliği, çoklu model reddi, günlük/aylık/yıllık eşdeğerlik, kar gecikmesi ve iki su bilançosu, tekrar kullanımın çift sayılmaması, RO tuz/hacim dengesi, basınç/soğuk koşullandırma, profil tanım/boyut/UTC kapıları ve16 ham kaynak hash'i test edildi. Bu sonuç bütün uygulamanın uçtan uca testi veya fiziksel doğrulama değildir; ana ajan birleşik QA'yı ayrıca kaydeder.

`north_planning.py` bağlantısı okundu: normalize alan, ayrı ısı/elektrik, kaynak katsayıları, kar gecikmiş aylık girişler, gerçek günlük depo tekrar koşusu ve RO basınç kapısı alan adlarıyla uyumludur. Isdammen'in tam kaynak bağlantısı ve aralık senaryolarını aynı konfigürasyonla eşleme notu ana ajana iletildi. Agent-reach araştırma akışı kullanıldı; bitiş kontrolü v1.5.0 güncel sonucunu verdi.

Sonraki bilimsel adım: gerçek yerel yapı/sensör/pompa ve kaynak-kimya ile bu açık mühendislik parametrelerini daraltmak; kontrollü üretim pilotunda su, yoğuşma, elektrik/ısı ve ürün yanıtını birlikte ölçmek. Aralık daralmasını ölçüm olmadan gerçekleşmiş sonuç gibi yazmamak.
