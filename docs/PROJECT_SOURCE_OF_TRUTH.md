## 23 Eylül 2026 — Coğrafya seçimi (TESLİM 025)

Türkiye bölge seçimi `data/sites.json` araştırma noktalarını kullanan küçük haritadadır. Kuzey hedef görünümü yalnız Longyearbyen ve kaynak NASA 0,25° iklim hücresini gösterir; başka Kuzey bölgesi için hesap paketi bulunmaz. Harita noktaları üretim sınırı veya saha ölçümü değildir. Ayrıntı: `REGION_GLOBE_025.md`.

# 23 Eylül 2026 — TESLİM 024 güncellemesi

Kuzey ana ekranı artık mevcut yıldan 2100’e girilebilir tek yıl hesabı kullanır; 20 yıllık dönem seçimi ana akış değildir. Kaynak NASA CMIP6 model-yıl günlük dizileri yeniden hesaplanır, interpolasyon yapılmaz. Açılış 2026 senaryosu canlı hava değildir; ERA5 referansı 2015–2025 kalır. Su kaynakları kaydırıcı, alan girilebilir ve Tarım Güvencesi Kuzey başlığının yan dalıdır. Ayrıntı ve sınırlamalar: `NORTH_YEAR_CONTROLS_024.md`; jüri/model anlatımı: `MODEL_NASIL_CALISIYOR.md`. Önceki dönem anlatımları aşağıda tarihsel bağlamdır.

# Güncel yön — 23 Eylül 2026 / TESLİM 023

Özellik adı **Tarım Güvencesi**: gençlere eğitim, modüler kurulum, dönemlik teknik destek ve ürün alımı/dağıtım fikri simülasyon sonucuna bağlandı. Kredi/banka ve fide geliştirme kapsam dışı. Gerçek üyelik veya poliçe değil, destek planı taslağı. Güncel anlatım ve demo: [TARIM_GUVENCESI_JURI_ANLATIMI.md](TARIM_GUVENCESI_JURI_ANLATIMI.md). Uygulama/test kapsamı: [TARIM_GUVENCESI_INTEGRATION_023.md](TARIM_GUVENCESI_INTEGRATION_023.md). Aşağıdaki önceki kısa adlar ve giriş yolu yerine bu güncel ad/akış kullanılır; kaynak ve hesap sınırları korunur.

---

# Güncel ek — 23 Eylül 2026 / TESLİM 022

Üreticiye geçiş, model → saha → kontrollü pilot zincirinin uygulama/yaygınlaştırma devamıdır. Ana araştırmanın yerine geçmez. Program ekipman/teknik destek/pazar erişimini ayrı, sigortayı yetkili tarafla koşullu ele alır. Yeni mali hesap sadece kullanıcı senaryosudur; bilimsel optimizera ticari ağırlık yazmaz.

Uygulama, sınırlar ve doğrulama: [PRODUCER_SUPPORT_COMPLETION_022.md](PRODUCER_SUPPORT_COMPLETION_022.md).

---

# Güncel ek · TESLİM021 · 23 Eylül 2026

Beş PC geliştirmesi uygulandı:2015–2025 ERA5 yakın dönem karşılaştırması,kaynaklı taze ürün/protein/besin enerjisi hedefleri,günlük sabit plan için döngüsel depo ve toplama stresleri,ayrıntılı enerji ve işletim güç taraması,numune/pilot kayıt ve karşılaştırma akışı. Güncel hesap,kaynak,sınır ve saha işleri [NORTH_PC_COMPLETION_021](NORTH_PC_COMPLETION_021.md) içinde; [doğrulama iş akışı](NORTH_VALIDATION_WORKFLOW.md) uygulanmıştır.

Önceki “güncel referans yok”,“yalnız kg amacı var” ve“hiç minimum depo hesaplanmıyor” ifadeleri eski sürüme aittir. Yeni depo hesabı ilk dolum hariç sabit üretimin döngüsel taramasıdır;LP'de depo yatırımı veya güç optimize edildiği anlamına gelmez. Yıllık enerji kısıtı LP'de,yeni kW beyanı ayrı taramadadır. Yakın ERA5/gelecek NASA farkı veri seti/hücre etkisini de içerir;aynı NASA tarihsel karşılaştırma korunur. Kaynaklı besin bileşimi dengeli diyet/kâr/talep değildir. Gerçek Arktik ölçümü veya pilot yapılmış sayılmaz.

Sunum gerekçesi:bilgisayarda planı ve test edilecek belirsizliği belirle;gerçek sefer zaman/konumundaki suyu modelle kıyaslamak ve kaynak suyunun kullanım/arıtma özelliklerini sınamak için izinli saha gözlemi ve numune topla;desteklenen girdiyi aynı motorda güncelle. Kara suyu,zemin ve enerji tahsisi ayrıca doğrulanır. Tek sefer tüm gelecek tarımını doğrulamaz.

---

Önceki geliştirme kayıtları aşağıdadır;021ekinin değiştirdiği ifadeler tarihsel kalır.

# Sabit referans, su numunesi ve enerji · TESLİM020 · 23 Eylül 2026

Ana kıyas önceki çalıştırma yerine aynı koşullardaki1995–2014 model iklimine sabitlenmiştir. Bu, bugünkü gözlenmiş üretim değildir;2025 etiketi kullanılmaz. Tam güncel üretim referansı için yeni eksiksiz hava paketi ve veri aileleri arasında karşılaştırılabilirlik gerekir. Önceki “son simülasyona göre” akışı artık geçerli değildir.

Enerji açıklaması: üretim elektriği + arıtma elektriği + ısı/COP; ihtiyaç kWh/yıl, fatura veya kurulu güç değil. Su tasarrufu yanında üretim ortamının enerji ihtiyacı değerlendirilir. Yağış/karın mevsimsel miktarı modelden; numunenin tuzluluk/kullanılabilirliği izinli saha ve laboratuvardan gelir. Deniz örneği kar suyunu temsil etmez. Planlanan örnek/üretim deneyi yapılmış ölçüm değildir. Sunum metni: [Su ve enerji notu](SUNUM_SU_VE_ENERJI_NOTU.md).

---

# Su yönetimiyle geleceğin tarımını şekillendirme · TESLİM019 · 23 Eylül 2026

Gelecek iklimi kaynaklı otomatik veri katmanıdır; ürünün ana çıktısı su yönetimine bağlı üretim sistemi önerisidir. Soldan gelecek/amaç/koşullar seçilir, “Simülasyonu çalıştır” ile uygulanır. Ana karar zinciri: su kaynakları ve payları → üretime uygun kalite/koşullandırma → depolama/aylık yedek/devridaim → ürün oranları ve üretim yöntemleri. Üretim ve su birlikte aynı motorla hesaplanır; çizim sırası tek yönlü yeni solver anlamına gelmez. Kimya ve saha doğrulamaları yapılmış gibi gösterilmez.

---

Önceki geliştirme ve bilimsel temel kayıtları:

# Kuzey karar anlatımı güncellemesi · TESLİM017 · 23 Eylül 2026

Güncel motor ürünleri eşit altı paya ayırmaz: açık çeşitlilik tabanı (%5/ürün), en yüksek taze hasadın %95'ini koruma ve su–enerji normalize uzaklık dengesi kullanır. Aynı koşullarla tarihsel/2030/2050/2090 karşılaştırması, ayrı iklim ön elemesi ve somut üretim/su/altyapı eylemleri eklendi. Tür iklim penceresi yerel tarım uygunluğu değildir; depo hacmi hâlâ tasarım girdisidir. Güncel denklemler ve sınırlar [FUTURE_NORTH_REBUILD](FUTURE_NORTH_REBUILD.md), son doğrulama [BUILD_STATUS](BUILD_STATUS.md). Aşağıdaki TESLİM016 eşit göreli pay amacı ve örnek sonuçlar önceki sürüme aittir.

---

# Future North güncel uygulama · 23 Eylül 2026

Kuzey artık 20 yıllık NASA v2.0 çoklu-model projeksiyonları, kaynaklı dokuz ürün kataloğu ve normalize tesis hesabını kullanır. Altı kontrollü ürünün miktarı, yöntem/sezon, aylık su ve enerji birlikte optimize edilir. Varsayılan 100 m² gerçek yerel kapasite değildir. Türkiye mevcut desenle açılır; otomatik ilk öneri davranışı yalnız yeni Kuzey ekranındadır.

Yöntem, kaynak, varsayım ve sınırların güncel ortak kaydı: [FUTURE_NORTH_REBUILD](FUTURE_NORTH_REBUILD.md). Son doğrulama ve teslim: [BUILD_STATUS](BUILD_STATUS.md). Aşağıdaki eski Kuzey uygulama tarifleri kendi tarihleriyle tarihsel kayıttır; bu güncel akışın yerine geçmez. Türkiye ve PWN donanımına ait geçerli kaynak/test kayıtları korunur.

---

# Su sınırı ve anlaşılır karşılaştırma · TESLİM 015

22 Eylül 2026: Türkiye arayüzünde “bütçe” yerine “Sulama suyu sınırı”, “randıman” yerine “sulama verimi” kullanılır. Ana su yüzdesi hem canlı seçimde hem öneride daima kaynak başlangıcına göredir. Optimizasyonun ek etkisi aynı iklim/sulama koşulundaki hesap öncesi seçime göre ayrıca gösterilir. Örnek Verimli sulama: 100 → 88,2 → 81; %11,8 ilk etki, %8,2 ek desen etkisi, %19 toplam. Yüzdeler toplanmaz. Kaynak başlangıcı, hesap öncesi seçim ve öneri ayrı etiketlenir; kadran ise ihtiyacı senaryo su sınırına böler. Su sınırı varsayımı gerçek rezerv/tahsis değildir; sonuç ölçülmüş tasarruf veya kâr garantisi değildir.

9 masaüstü kontrolü, 23 mevcut frontend testi, 1 gerçek Konya API hesabı ve üretim derlemesi bu turda doğrulandı; tam 199 backend testinin son koşusu önceki TESLİM014 tarihindedir. Ayrıntı [BUILD_STATUS.md](BUILD_STATUS.md). Eski etiketler ve karşılaştırma tarifleri tarihsel bağlamdır.

# İklimden eyleme / jüri akışı · TESLİM 014

22 Eylül 2026: Türkiye açılışı kaynaklı mevcut desendir; otomatik ilk öneri kaldırıldı. Önce açık sıcaklık/yağış senaryoları, sonra su bütçesi; ürün payları isteğe bağlı. Mevcut düğmesi başlangıcı geri getirir. En uygun deseni hesapla / Deseni optimize et aynı gerçek motoru çalıştırır. Ana ekran yüzdeler ve uygulanabilir artır/azalt önerileriyle konuşur; m³/ha/kg ve kaynaklar açılır hesaplarda durur. İyi koşullar hazır bir optimum değildir ve minimumları değiştirmez.

Yeni ΔT girdisi kaynak ERA5 ET0 üzerine FAO56 Denklem52 sıcaklık teriminden projece türetilen oranı uygular; kalibre edilmemiş duyarlılıktır, tam Penman–Monteith veya gelecek iklim projeksiyonu değildir. Kaynak baseline ΔT0 kalır. Kadran ihtiyaç/senaryo bütçesidir, risk olasılığı değildir. Trakya'da adlandırılmış çeltik-hariç kapsam gri gösterilir; tam bölge su toplamı bilinmeyen kalır. Genel veri-yok sloganı yerine gerçek kapsam anlaşılır anlatılır; bilinmeyen sıfıra çevrilmez. Ekonomi kullanıcı fiyatlarıyla, kâr garantisi vermeden çalışır.

199 backend,23 frontend,10 bölgesel API ve12 son jüri masaüstü kontrolü kendi tarihleriyle [BUILD_STATUS.md](BUILD_STATUS.md) ve [ANA_CHAT_TESLIM.txt](ANA_CHAT_TESLIM.txt) içinde. Mobil test yok. Güncel [DEMO_PLAN.md](DEMO_PLAN.md) bu düğmeli akışı anlatır. Aşağıdaki önceki açılış/UI tarifleri tarihsel bağlamdır.

# Nesnel karar / ekonomi / analiz · TESLİM 013

22 Eylül 2026: Öneriler net azalt/artır oranları verir; su/uygulanabilirlik ve ekonomi kendi kriterlerinde renklenir. On açılır SVG grafik gerçek koşu verisinden gelir. Ekonomi kontrolü kullanıcı fiyat/maliyetleriyle karşılaştırma yapar; kaynaklı fiyatlar yok, boşlar DATA NEEDED. Faaliyet marjı net kâr değildir; su odaklı optimizer kâr optimizasyonuna dönüşmedi. Test varsayımları temizlendi. Masaüstü tercihi sürer. Güncel kanıt: [BUILD_STATUS.md](BUILD_STATUS.md).

# Kısa masaüstü karar desteği · TESLİM 012

22 Eylül 2026: Ana Türkiye akışı canlı tarla → su → Öneri/Neden/Dikkat → iki kısa grafik. Ayrıntılı tablolar/kanıtlar açılır, ayrı grafik sekmesinde tarla tekrarlanmaz. Gerekçeler aynı koşu çıktısından hesaplanır; mevcut motor matematiksel optimizasyon, AI/LLM entegrasyonu değildir. Kullanıcının yeni açık tercihi: yalnız masaüstü, bundan sonra mobil test yok (AGENTS.md). Güncel kanıt: [BUILD_STATUS.md](BUILD_STATUS.md).

# Canlı tarla katmanı · TESLİM 011

22 Eylül 2026: Türkiye ana tuvalinde kaynaklı mevcut tarla ile canlı seçim / hesaplanan öneri, orantılı ve ürüne özgü ekim dokuları üzerinden karşılaştırılır. Sürgüyle parseller kayar; 010 halka/karışım tasarımı kaldırılmıştır. Bu şematik dağılımdır, gerçek parsel haritası değildir. Su bandı görünümdeki desenle eşleşir; bilinmeyen veri sıfır yapılmaz. Simülasyon motoru ve kaynaklı başlangıç korunmuştur. Güncel kanıt: [BUILD_STATUS.md](BUILD_STATUS.md).

# Güncel Türkiye düzeltmesi · TESLİM 008

Türkiye: referans kaynaklı mevcut desen, öneri mevcut üretimle sınırlandırılmayan sıralı bölgesel optimum. Önce ekili alan, sonra su; açık %50 üretim tabanı. Beş il için 2024 resmî başlangıç; ERA5 2024–2025. Canlı 2026 ekiliş sayımı veya 81 il kapsaması değildir.

Detay ve son doğrulama: [BUILD_STATUS.md](BUILD_STATUS.md). Aşağıdaki 007 ve daha eski kayıtlar kendi tarihleriyle tarihsel durumdur.

---

# Güncel rebuild kaydı · 22 Eylül 2026

Yeni ana metin ve en yeni kullanıcı düzeltmeleri eski uygulama önceliklerinin üzerindedir. Tek çizgi: Konya → Türkiye → Future North → PRE-TASE → TASE → aynı motorla POST → kontrollü üretim doğrulaması. Türkiye kaynak baseline ile otomatik ilk hesabı açar. Kuzeyde kaynaklı iklim olumsuz aday elemesini motora taşır; eksik yerel katsayıları doğrulamaz. Güncel ana UI ScenarioLab + DecisionCanvas. Aşağıdaki U11/U10/U9 uygulama kararları tarihsel bağlamdır; güncel UI/öncelik talimatı değildir.

Bağlayıcı sözleşme: [REBUILD_CONTRACT.md](REBUILD_CONTRACT.md). Çalışan/eksik ayrımı: [REBUILD_EVIDENCE_AUDIT.md](REBUILD_EVIDENCE_AUDIT.md), [BUILD_STATUS.md](BUILD_STATUS.md).

---

## Önceki ayrıntılı kayıt (tarihsel uygulama durumları kendi tarihleriyle okunur)

# U11 uygulama önceliği

22 Eylül 2026: Bilimsel gerçekler bu belgede; güncel ürün/araştırma uygulama sözleşmesi [FINAL_PRODUCT_CONTRACT.md](FINAL_PRODUCT_CONTRACT.md). U11 önceki UI talimatlarının önündedir. AUTO/MANUAL ve düzenleme kilidi kaldırıldı; açık planlama amaçları ve duyarlılık/araştırma çekmecesi eklendi. Tarihsel notlar güncel UI gereği değildir.



U10 GÜNCEL ETKİLEŞİM — 22 EYLÜL 2026
- Kalıcı 355 px sol model kontrol paneli, sağda desen ve analiz. Büyük sayfa gezinmesi kaldırıldı.
- İlk açılış Konya: ürünler doğrudan üstte; yüzde/hektar, tek alan kilidi, hızlı su stresi ve sabit hesaplama altlığı.
- İlk açılışta LP çalıştırmadan mevcut alan/üretim ve modellenmiş su hesabı yüklenir. Başlangıç su bütçesi açık senaryodur. Henüz öneri üretilmez. Eksik çeltik suyu ve Kuzey mevcut desen verisi uydurulmaz.
- Hesapla sonrası mevcut → önerilen, kaynaklar ve NEDEN BU DESEN? motor açıklamaları. Veri/grafik, bölge karşılaştırması ve pilot incelemesi ikincil sekmelerdir.
- Kuzey aynı kontrol/hesap/sonuç düzenini kullanır. SAHA VERİSİYLE GÜNCELLE çekmecesi PRE-TASE kaydı, aynı motorla gözlem sonrası hesap ve PWN CSV profilini içerir. Mevcut yerel suyun yıllık miktarını PWN sağlıyor iddiası yok.
- Senaryoyu kaydet düğmesi mevcut kullanıcı girdilerinin JSON dosyasını indirir; sunucuya yeni resmî veri olarak yazmaz.
- Gerçek Arktik gözlemi yok. Mevcut kuzey deseni açıklayıcı varsayım simülasyonudur; gelecek yerel ürün önerisi olarak sunulmaz.

# Projenin güncel kaynak ve kapsam belgesi

Tarih: 22 Eylül 2026. **Uygulama onayı [U6] ile durum güncellendi; FINAL MASTER SYNC [U5] bilimsel kapsamı korunuyor.** Güncel sürüm U9 ile kalıcı Scenario Lab ve ortak ürün deseni simülatörü 0.4.0 oldu; beş ilde resmî başlangıç verisi ve kullanıcı senaryosuyla çalışan çok ürünlü hesap eklendi. Tamamlanan işler ve testler [BUILD_STATUS.md](BUILD_STATUS.md), hesap sınırları [MODEL_METHODS.md](MODEL_METHODS.md), indirilen veriler [DATA_ACCESS_LOG.md](DATA_ACCESS_LOG.md) üzerinden izlenir. Fiziksel PWN, tank deneyi, araştırma sınıfı CTD veya Arktik saha sonucu tamamlanmış değildir. İlk 19 belge tasarım temelidir; teknik öneriler uygulandığı ölçüde ayrıca durum kaydına geçirilir.

## Öncelik ve çalışma biçimi

1. Güncel etkileşim yönü FINAL UX + ARCTIC LOGIC CORRECTION [U9]: aynı motoru koruyarak sol kalıcı Scenario Lab / sağ desen ve veri-grafik incelemesi. AUTO/MANUAL ve tek alan override; dört üst alan Türkiye/Kuzey/Saha/Kanıt. U8 çok ürünlü motor, U7 dashboard ilkesi ve U6 kodlama onayı geçerli. Kullanıcının son yönlendirmesi: kullanım sadeleşirken bilimsel/analitik kapsam azaltılmayacak. [SIMULATOR_UX](SIMULATOR_UX.md).
2. FINAL MASTER SYNC [U5] ve onunla çelişmeyen diğer açık kararlar [U1–U4].
3. Orijinal/final 2204-D raporu: geçmişte gerçekten yapılan iş için authoritative source [F2].
4. Resmî TASE/TÜBİTAK KARE/Ulusal Kutup Bilim Stratejisi belgeleri [F5–F6].
5. Hakemli ve güncel bilimsel literatür.
6. Eski final sunum: geçmiş ürünün anlatım kaydı [F3].
7. Full TXT: brainstorming, gerekçe ve karar tarihi; tekrar sayısı güncellik kanıtı değildir [F1].

Bu sıra projenin kapsamını senkronize eder; kullanıcının planı yapılmış deneyin veya dış bilimsel kanıtın yerine geçmez. F/W kodları belge ve dış kaynakları, **Öneri** bizim tasarımımızı ayırır. Profesyonel çağrının bütün başvuru hükümleri öğrenci seçimine otomatik uygulanmaz. Kritik iddiaların kanıt gücü ve sınırları [EVIDENCE_MAP.md](EVIDENCE_MAP.md) içindedir.

Kullanıcının yönlendirmesi: Mülakat hazırlığını kusursuz bir akademik çalışma tamamlama şartına bağlamayacağız. Öncelik, **neden Arktik'e gitmemiz gerektiğini somut, güçlü ve doğru bir hikâyeyle göstermek**. Bilimsel ayrıntılar bu hikâyeyi destekleyecek. U6 yazılım/firmware ve veri işine açık onay verdi; yeniden kodlama onayı beklenmiyor. Bu onay, yapılmamış fiziksel deneyi veya tamamlanmamış yazılımı yapılmış saymaz [U3,U6].

## Proje 13 cümlede

1. Bu proje, iklim değişikliği altında suyu ve üretimi birlikte planlayan ikinci nesil bir karar destek sistemi kurmayı amaçlıyor [U1].
2. Konya gerçekten ilk pilot bölgeydi; ekip burada iklim baskısını, ürün desenini, göreli su gereksinimini ve optimizasyonu birleştirdi [U1; F2, s.1, 6–13].
3. Türkiye birinciliği bu geçmiş çalışmanın başarısıdır; yeni Arktik sisteminin tamamlandığı anlamına gelmez [U1].
4. Eski yazılımı dönüştürmek yerine yeni veri mimarisi, model, arayüz ve karar motoru sıfırdan kurulacak [U1].
5. İlk uygulama Türkiye olacak ve farklı birkaç bölgede yaklaşımın aktarılabilirliği sınanacak [U1].
6. Gelecek sorumuz, bazı ürünler için iklimsel uygunluğun kuzeye genişlemesinin ne kadarının sürdürülebilir üretime dönüşebileceği [U1; W1].
7. Sıcaklık açısından yetişebilir olmak, güvenilir suya, uygun zemine ve sürdürülebilir enerjiye sahip olmakla aynı şey değil [W1; Öneri: birlikte değerlendirme çerçevemiz].
8. Bu nedenle ürün desenini; ürün, üretim yöntemi, su kaynağı ve üretim zamanının birlikte seçildiği bir üretim sistemi desenine genişletiyoruz [U1].
9. Hedef, üretim veya beslenme çıktısını korurken su açığını, enerji gereksinimini, iklim riskini ve çevresel baskıyı azaltmak [U1].
10. Arktik'te gemiden kullanılacak Polar Water Node, ana projenin gerçek saha gözlem katmanı olacak [U1; F5, s.6].
11. PWN ile alınan profiller ve uygun fiziksel numuneler, belirli zaman ve konumdaki kaynak suyu özelliklerini modelin öngördüğü durumla karşılaştırmamızı sağlayacak [U1; W2–W3; Öneri: araştırma tasarımı].
12. Bu gözlemleri uygun kıyısal senaryolarda su arıtma ve enerji hesabına bağlayacağız; denizdeki düşük tuzluluk sinyalini doğrudan sulama suyu saymayacağız [U1; W6].
13. Mülakata kadar PWN v0.1, gerçek deney grafikleri, ayrı Arctic v1 tasarımı ve dar kapsamlı yeni platform demosu hedefleniyor; yazılımın ilk kesiti çalışıyor, fiziksel deney ve nihai mülakat paketi hâlâ hedef aşamasında [U5,U6; BUILD_STATUS].

## Korunan bilimsel kimlik

**Ana konu:** iklim değişikliği altında su yönetimi, sürdürülebilir üretim ve karar desteği.

**Evrim:** Konya pilot → Türkiye transfer/genelleme testleri → kuzeye genişleyebilecek üretim potansiyeli → su güvenliği → üretim sistemi deseni → Arktik saha doğrulaması → gerektiğinde AI ile kalibre edilen karar desteği → Sustainable Production Frontier [U1].

**Ana araştırma sorusu:** İklim değişikliğiyle kuzeye kayan üretim potansiyelinin ne kadarı su ve enerji açısından sürdürülebilir; hangi üretim sistemi bunu mümkün kılar?

**Vizyon:** “İklim değişikliği üretimin sınırını kuzeye taşıyor; biz o sınırın su açısından gerçekten nerede olması gerektiğini belirlemek istiyoruz.” Bu bir vizyon cümlesidir. Teknik metinde, bütün üretimin kesin taşınması yerine bazı ürünlerin **iklimsel uygunluğunun senaryoya bağlı değişmesi** denir [U1; W1].

## Eski projeden güvenle taşınacak gerçekler

| Konu | Belgedeki durum |
|---|---|
| Pilot | Konya ili; buğday, arpa, dane mısır, şeker pancarı; 2023 ekim alanları [F2, s.4, 7] |
| Model | Alan × göreli su katsayısı × iklim çarpanı; tam hidrolojik bilanço değil [F2, s.8–10] |
| Yöntem | Kısıtlı ürün oranı optimizasyonu; SciPy/SLSQP; Streamlit arayüz [F2, s.11–14] |
| Rapor sonucu | Göreli baskı 15.702.550 → 14.338.276; raporda yaklaşık %8,7 azalma [F2, s.17] |
| Sınır | Ekonomik getiri, çiftçi davranışı, toprak su kapasitesi ve yerel sulama altyapısı doğrudan modele dahil değil [F2, s.19] |
| Sunum eki | Ekonomik yorum ve AI raporu gösteriliyor; bunların rapordaki modelden farklı sürüm/bileşen kapsamı ayrıca açıklanmalı [F3, slayt 21–22, 28–30] |

%8,7, sahada ölçülmüş su hacmi tasarrufu diye aktarılmaz. Sunumun havuz/içme suyu eşdeğerleri, ayrı hacim dayanağı görülmeden yeni anlatıya alınmaz. Eski rapor ve sunum değiştirilmedi; yalnız kullanım sınırları kaydedildi [F2, s.8–9, 17; F3, slayt 25].

## Yeni platformun dokuz katmanı

1. **Future Climate Frontier:** gelecek senaryoları, GDD, don olmayan dönem, sıcaklık/yağış ve ürün gereksinimleri.
2. **Soil / Permafrost Filter:** açık tarla için zemin, toprak ve donmuş zemin koşulları; diğer yöntemlere uygun ayrı fiziksel kısıtlar.
3. **Water Security:** yağış, kar erimesi, akış, toprak nemi, evapotranspirasyon, mevsimsellik, depolama ve güvenilirlik.
4. **Water Source / Usability:** yerel tatlı su, depolanmış yağmur/erime suyu, geri kullanım; uygun kıyısal senaryoda arıtılmış deniz suyu.
5. **Production Method:** açık tarla, sera, hidroponik, kontrollü ortam/dikey üretim.
6. **Energy / Resource Constraints:** ısıtma, aydınlatma, pompaj, arıtma ve diğer kaynak bütçeleri; enerji erişimi ve çevresel sınırlar.
7. **Production Pattern Optimizer:** ürün, oran, yöntem, su kaynağı ve dönem kararları.
8. **AI Decision / Uncertainty:** klasik karşılaştırma, bağımsız doğrulama ve açıklanabilirlik; yarar sağlamazsa klasik yöntem.
9. **Arctic Ground Truth / PWN:** fiziksel profiller, metadata ve uygun fiziksel numuneler [U5 §9].

Bu liste uzun vadeli mimari kapsamıdır; dokuz günlük teslim listesi değildir. Ayrıntılar [SCIENTIFIC_ARCHITECTURE.md](SCIENTIFIC_ARCHITECTURE.md) içindedir.

## PWN'nin iki sürümü

**V0.1:** düşük maliyetli/DIY iletkenlik, su geçirmez sıcaklık ölçümü, encoder ile tank derinliği, ESP32 veya Deneyap, yerel kayıt, profil grafiği ve iletkenlik geçişi tespiti. Kontrollü su kolonunda prensip gösterimi. Araştırma sınıfı CTD değil [U1].

**Arctic v1 konsepti:** soğuğa uygun sensörler, gerçek basınç/derinlik, referans CTD karşılaştırması, uygun deniz taşıyıcısı/halatı, örnekleme ve kalibrasyon protokolü. Hassasiyet, çalışma derinliği ve analiz paneli uzmanlarla belirlenir. Conductivity/salinity, sıcaklık, basınç/derinlik, GPS/zaman hedef; turbidity bilimsel yarar ve uygulama koşullarına bağlı [U1].

**İki ayrı bağlantı:** (A) PWN → yerel model–gözlem karşılaştırması → temsil/belirsizlik değerlendirmesi → ilgili su sistemi alt modeli → karar güvenilirliği. (B) PWN → temsil ettiği kaynak suyunun karakterizasyonu → arıtma/koşullandırma → kullanılabilir su → enerji/su maliyeti → üretim seçeneği. A yolu karasal su arzına kendiliğinden bağlanmaz; B yolu ölçüm noktasının kaynakla ilişkisi gösterilmeden saha doğrulaması olmaz. Her ikisi de araştırma planıdır; gözlem kararın değişmesini veya belirsizliğin azalmasını garanti etmez [U5 §14,34; E13,E19].

Fiziksel numunelerde δ18O/δ2H kaynak izleme; EC/tuzluluk, Na, Cl, Ca, Mg, bor, alkalinite vb. kullanım/arıtma değerlendirmesi için adaydır. Kesin panel henüz yoktur [U1].

## Kişisel anlatı ve ekip

Ali Baha Demir'in 2204-D Su Yönetimi Türkiye birinciliği ve 2204-C Türkiye ikinciliği kullanıcının beyanıdır. Bu pakette ayrı bir ödül belgesi veya 2204-C raporu bulunmadı. Diğer öğrencilerin adları sunumda Cem Ural ve Ferit Bora Akman olarak yer alıyor [U1; F3, slayt 1].

**Ali Baha'nın kişisel omurgası:** kutup araştırmaları → iklim değişikliği/su yönetimi → Arktik'te iki hattın birleşmesi. 2204-C geçmişi anlatının temel süreklilik unsuru; yalnız CV maddesi değildir. Proje adı, yıl, alan ve ekip ayrıntıları doğrulanmadan eklenmez [U5 §22; E14]. Şerif Efe Dartar'dan aktarılan tavsiyeler seçim/iletişim stratejisi girdisidir; resmî seçim ölçütü veya bilimsel kanıt değildir [U5 §25].

Doğru anlatı: Kutup araştırmaları, iklim değişikliği ve su yönetimi çizgileri şimdi birleşiyor. “2204-D'yi baştan Arktik için yaptık” denmez. Üç motivasyon mektubunda proje aynı, kişisel geçmiş/rol/katkı farklı olur. Gerçek yetkinlikler alınmadan rol veya sertifika uydurulmaz. Adı geçen araştırmacılar danışmanımız veya işbirliği ortağımız değildir; çalışmalarını inceleyip görüş almayı planlıyoruz [U1].

## Kaynak envanteri ve okuma kapsamı

Bu belge kümesindeki sayfa numaraları, aksi belirtilmedikçe **PDF dosyasının 1'den başlayan sayfa sırasıdır**. TXT satırları orijinal UTF-8 dosyanın satırlarıdır. DOCX için paragraf/soru başlığı kullanılır; sayfa numarası tahmin edilmez.

| Kod | Kaynak | İnceleme |
|---|---|---|
| U1 | Bu konuşmadaki ilk kullanıcı isteği ve CURRENT PROJECT SOURCE OF TRUTH | Güncel kapsamın tamamı |
| U2 | “tüm alt ajanları kullanabilisin tüm izinlerin var” | Alt ajanlı okumaya izin; kodlama yasağını kaldıran açık talimat yok |
| U3 | Aşırı akademik/mükemmeliyetçi olmama, gitme nedenini anlatma yönlendirmesi | Teslim ve üslup önceliği |
| U4 | Gerekliliklerin bilişim ve teknoloji öğretmenlerine anlatılmak üzere hazırlanması | PWN belgesi malzeme/araç/görev ihtiyaç listesi olarak düzenlendi; envanter ve tarih teyidi yerine geçmez |
| U5 | [FINAL MASTER SYNC](C:/Users/bahao/.codex/attachments/a3cea6f3-4119-4ad0-b9c5-a701aa3e10f3/pasted-text.txt) | Bilimsel kapsam; 30 Eylül 2026 tarihi ve 48 saat kuralı teyitli, kesin saat açık. Bu aşamadaki kod/firmware bekleme kararı daha sonra U6 ile kaldırıldı. |
| U6 | [Uygulama onayı ve ilk yapım kapsamı](C:/Users/bahao/.codex/attachments/1cc580a8-6bcb-4076-a685-cf64fe1a2c75/pasted-text.txt) | 22 Eylül 2026: yazılım/firmware/veri geliştirmesi açıkça onaylandı; greenfield yaklaşım ve bilimsel sınırlar korundu. Öğretmen/hardware iletişim paketi ilk teslim; tamamlanma kaydı BUILD_STATUS üzerinden izlenir. |
| F1 | [2204D_TO_KUUTP.txt](C:/Users/bahao/Downloads/2204D_TO_KUUTP.txt) | 8.659 satır tamamı: ana okuma 1–1800, alt ajan okumaları 1801–5100 ve 5101–8659; kesilen çıktılar yeniden okundu |
| F2 | [agrohydroraporu (5).pdf](<C:/Users/bahao/Downloads/agrohydroraporu (5).pdf>) | 20 sayfa tam metin; şekil ve tablolar ayrıca görsel incelendi |
| F3 | [Final sunum PDF](<C:/Users/bahao/Downloads/SÜRDÜRÜLEBİLİR BİR GELECEK DESENDEN DENGEYE (7).pdf>) | 36 slayt tam metin ve tüm slaytların görsel incelemesi; ekran görüntüleri kaynak kodu denetimi değildir |
| F4 | [Detaylı Motivasyon Mektubu formu](<C:/Users/bahao/Downloads/Arktik için Detaylı Motivasyon Mektubu.docx>) | 164 paragraf, boş alanlar dahil OOXML metni ve render edilen 5 sayfanın tamamı; kişisel cevaplar doldurulmamış |
| F5 | [2027 Kutup Araştırmaları çağrısı](C:/Users/bahao/Downloads/kutup_arastirmalari_cagri_metni_2027.pdf) | 10 sayfanın tamamı |
| F6 | [Ulusal Kutup Bilim Stratejisi 2023–2035](C:/Users/bahao/Downloads/ulusal_kutup_bilim_stratejisi_2023_2035_1.pdf) | 44 sayfanın tamamının metni; temel atıflar s.25 ve 34 |

İlk altı kaynak dosya ve yeni master metni kaynak paketidir. Ayrıca yüklenmiş 2204-C raporu, ham eski veri/kod, PWN deney kaydı veya yapılmış uzman görüşmesi tutanağı bulunmadı. İlk turda tam okunan dosyalar bu senkronizasyonda yeniden gözden geçirildi; TXT karar çatışmaları ve kişisel anlatı kayıtları yeniden kontrol edildi. İlk dokuz belgenin tamamı yeniden okundu. Yerel kaynak dosyaları dış servislere yüklenmedi.

## Dış kaynak kayıtları

Erişim tarihi: 22 Eylül 2026. Bunlar F1'deki eski ChatGPT iddialarının yerine yeniden kontrol edilen dış kaynaklardır. Her kaynağın kanıtladığı kapsam sınırlıdır.

| Kod | Birincil kaynak ve desteklediği kullanım |
|---|---|
| W1 | [Xu vd., 2026, Communications Earth & Environment](https://www.nature.com/articles/s43247-026-03702-w): senaryoya bağlı kuzeye genişleyen iklimsel ürün uygunluğu ve permafrost kısıtı. Gerçekleşmiş tarım göçü veya projemizin sonucu değildir. |
| W2 | [TÜBİTAK, 19.07.2024, TASE-IV'te 16 proje](https://tubitak.gov.tr/tr/haber/4-ulusal-arktik-bilimsel-arastirma-seferinde-16-projeye-yonelik-calismalar-gerceklestiriliyor): İncili, Nasıf Dondurur ve Biçer'in geçmiş araştırma başlıkları. |
| W3 | [DEÜ İMST, 30.07.2024](https://imst.deu.edu.tr/tr/news/4-ulusal-arktik-bilimsel-arastirma-seferi-30-07-2024/): Nasıf Dondurur'un Svalbard açıklarında yaklaşık 90 m su kolonundaki tatlı su girişlerine ilişkin veri toplaması. |
| W4 | [Copernicus Marine Arctic Ocean Physics Reanalysis](https://data.marine.copernicus.eu/product/ARCTIC_MULTIYEAR_PHY_002_003/description): TOPAZ ürün kapsamı, 12,5 km dağıtım ızgarası, 40 standart derinlik ve gözlem asimilasyonu. |
| W5 | [FAO-56](https://www.fao.org/4/X0490E/X0490E00.htm): ETo, dönemsel ürün katsayısı ve toprak su dengesi için yöntem başlangıcı. |
| W6 | [FAO Water Quality for Agriculture](https://www.fao.org/4/T0234e/T0234E01.htm): su uygunluğunun kullanım koşuluna, tuzluluğa, infiltrasyona ve iyon etkilerine bağlı olması. |
| W7 | [NASA NEX-GDDP-CMIP6](https://www.nccs.nasa.gov/data-collections/nex-gddp-cmip6/): günlük, 0,25° ölçekli senaryo veri adayı; katalog/sürüm kaydı ayrıca tutulacak. |
| W8 | [ERA5-Land kataloğu](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land?tab=overview): geçmiş kara iklimi ve su değişkenleri için reanalysis adayı. |
| W9 | [CARRA2 kataloğu](https://cds.climate.copernicus.eu/datasets/reanalysis-pan-carra?tab=overview) ve [ilk veri duyurusu](https://climate.copernicus.eu/first-carra2-data-release-offers-new-insights-arctic-extremes): Arktik atmosferik bağlam; sürüm/dönem erişimi indirme anında kontrol edilecek. |
| W10 | [ISRIC SoilGrids](https://isric.org/explore/soilgrids) ve [katman açıklaması](https://docs.isric.org/globaldata/soilgrids/SoilGrids_faqs_01.html): 250 m tahmini toprak özellikleri, derinlikler ve belirsizlik katmanları. |
| W11 | [ESA Permafrost CCI](https://climate.esa.int/en/projects/permafrost/): donmuş zemin sıcaklığı/aktif tabaka ürünleri; model destekli ürünlerdir. |
| W12 | [DSİ Akım Gözlem Yıllıkları](https://www.dsi.gov.tr/sayfa/detay/744): Türkiye akım gözlem arşivinin erişim noktası. |
| W13 | [MGM veri erişimi](https://www.mgm.gov.tr/site/bilgi-edinme.aspx): MEVBİS üzerinden veri talep/erişim yolu. Ücretsiz ve sınırsız API varsayılmaz. |
| W14 | [TÜİK Bitkisel Üretim İstatistikleri 2023](https://veriportali.tuik.gov.tr/Bulten/Index?dil=1&p=Bitkisel-%C3%9Cretim-%C4%B0statistikleri-2023-49535): bitkisel üretim istatistikleri ve derleme kapsamı. |
| W15 | [TEOS-10 GSW](https://teos-10.org/pubs/gsw/html/gsw_contents.html): deniz suyu için C/T/p dönüşümleri ve değişken tanımları. DIY NaCl deneyini otomatik okyanus tuzluluğu ölçümüne dönüştürmez. |
| W16 | [KARE Kutup Veri Merkezi üyeleri](https://polardata.tubitak.gov.tr/members/): uzmanlık eşleştirmeleri; dinamik sayfa erişimi sınırlı olduğundan indekslenen resmî kayıt kullanıldı, güncel görev/destek teyidi yok. |
| W17 | [FastAPI resmî belgeleri](https://fastapi.tiangolo.com/tutorial/metadata/) ve [MapLibre GL JS](https://maplibre.org/projects/gl-js/): önerilen API ve harita bileşenlerinin dokümantasyonu. Projenin bunları kullandığına dair iddia değil. |
| W18 | [GSW SP_from_C teknik belgesi](https://teos-10.org/pubs/gsw/html/gsw_SP_from_C.html): C/T/p girdileri, birimler ve pratik tuzluluk hesabı. |
| W19 | [Crocker vd., 2020, Ocean Science](https://os.copernicus.org/articles/16/831/2020/): okyanus model değerlendirmesinde mekânsal eşleşme ve temsil ölçeğinin önemi. |
| W20 | [Yamamoto-Kawai vd., 2005, JGR Oceans](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2004JC002793): izotop/alkalinite/tuzlulukla kaynak ayrıştırması ve uç bileşen varsayımları. |
| W21 | [Copernicus TOPAZ kalite belgesi](https://documentation.marine.copernicus.eu/QUID/CMEMS-ARC-QUID-002-003.pdf): ürün hata/değerlendirme bağlamı; uygulamada sürüm sabitlenecek. |
| W22 | [Analog Devices DS18B20](https://www.analog.com/en/products/ds18b20.html) ve [veri sayfası](https://www.analog.com/media/en/technical-documentation/data-sheets/DS18B20.pdf): sıcaklık çipi özellikleri; satılan su geçirmez probun gövde/deniz dayanımı için kanıt değil. |
| W23 | [Espressif ESP32 ADC kalibrasyon belgesi](https://docs.espressif.com/projects/esp-idf/en/v6.0/esp32/api-reference/peripherals/adc/adc_calibration.html): ADC gürültüsü ve kalibrasyon ihtiyacı; kart seçildikten sonra doğru sürüm kullanılacak. |
| W24 | [Deneyap Kart resmî belgesi](https://deneyapkart.org/docs/deneyap-kart): kart seçeneklerinin donanım bilgisi; tüm Deneyap modelleri aynı kabul edilmez. |

## Bu paketteki belgeler

**U7 — 22 Eylül 2026, bu konuşmadaki PRODUCT + SCIENCE REFOCUS kullanıcı talimatı.** Projeyi yeniden başlatmaz; lineer sunum akışını karar çalışma alanına dönüştürür. Ürün denetimi [PRODUCT_REFOCUS.md](PRODUCT_REFOCUS.md), beş bölge [TURKIYE_BENCHMARKS.md](TURKIYE_BENCHMARKS.md), edinilen bölgesel iklim modeli [NORTH_DATA_PLAN.md](NORTH_DATA_PLAN.md) içindedir. Tek modelin göstergeleri, yerel tarım veya deniz suyu gözlemi değildir.

- [Bilimsel ve teknik mimari](SCIENTIFIC_ARCHITECTURE.md)
- [Kararlar ve geçmişteki çatışmalar](DECISIONS.md)
- [Açık sorular](OPEN_QUESTIONS.md)
- [Veri gereksinimleri](DATA_REQUIREMENTS.md)
- [PWN v0.1 şartnamesi](PWN_SPEC_V0.1.md)
- [PWN Arctic v1 konsepti](PWN_ARCTIC_V1_CONCEPT.md)
- [TASE ve strateji uyumu](TASE_ALIGNMENT.md)
- [Dokuz günlük ve sonraki uygulama planı](IMPLEMENTATION_ROADMAP.md)
- [Doğal mülakat anlatıları](INTERVIEW_STORY.md)
- [Sunum stratejisi](PRESENTATION_STRATEGY.md)
- [Üç mektubun ortak ve kişisel hikâyesi](THREE_LETTERS_STORY.md)
- [Jüri soru-cevap bankası](JURY_QA.md)
- [İddia–kanıt haritası](EVIDENCE_MAP.md)
- [Araştırmacı doğrulama ve görüşme gündemi](RESEARCHER_OUTREACH.md)
- [Arktik saha planı](ARCTIC_FIELD_PLAN.md)
- [Gelecek üretim modeli ve hipotez denetimi](FUTURE_PRODUCTION_MODEL.md)
- [PWN doğrulama planı](PWN_VALIDATION_PLAN.md)
- [Mülakat demo planı](DEMO_PLAN.md)

## Tüm belgelerde kullanılacak iş durumu

| İfade | Bu projedeki karşılığı |
|---|---|
| Yaptık | Konya pilotu; araştırma/dokümantasyon; kaynaklı ilk veri paketi ve çalışan ilk yazılım kesiti — ayrıntı BUILD_STATUS |
| Şu anda geliştiriyoruz | İkinci nesil yazılım ve mülakat paketi; yazılım testi fiziksel donanım/saha doğrulaması anlamına gelmez |
| Mülakata kadar hedefliyoruz | Dar demonun prova edilmiş teslimi, Türkiye transfer gösterimi, kaynaklı kuzey örneği, PWN deney/grafik, Arctic v1 CAD, üç kişisel form |
| Seçilirsek planlıyoruz | Arktik v1 geliştirme, referans CTD karşılaştırması, izinli sefer gözlemi ve sefer sonrası analiz |
| Araştırmacı görüşüyle kesinleşecek | Hassasiyet/derinlik, donanım, örnek sayısı/paneli, laboratuvar ve gemi operasyonu |

**Uygulama durumu:** U5 §48'deki durdurma noktası U6 ile kaldırıldı. Bu belgelerde tanımlı dar kapsam uygulanıyor; yeni özellik sayısından önce ölçüm–hesap–karar zincirinin çalışması ve kanıtın doğru etiketlenmesi gelir. Güncel tamamlanma kaydı [BUILD_STATUS.md](BUILD_STATUS.md).
