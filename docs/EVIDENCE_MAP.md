# Güncel ek — 23 Eylül 2026 / TESLİM 022

Üretici destek araştırması: data/producer_support/research/manifest.json içindeki dört resmî kaynak URL/UTC/SHA-256 ile arşivlendi. Resmî mevzuat/kapsam bilgisi, kullanıcı fikri ve mali senaryo ayrı statüdedir. TARSİM ilişkisi veya poliçe kabulü iddia edilmez.

Uygulama, sınırlar ve doğrulama: [PRODUCER_SUPPORT_COMPLETION_022.md](PRODUCER_SUPPORT_COMPLETION_022.md).

---

# Güncel ek · TESLİM021 · 23 Eylül 2026

Beş PC geliştirmesi uygulandı:2015–2025 ERA5 yakın dönem karşılaştırması,kaynaklı taze ürün/protein/besin enerjisi hedefleri,günlük sabit plan için döngüsel depo ve toplama stresleri,ayrıntılı enerji ve işletim güç taraması,numune/pilot kayıt ve karşılaştırma akışı. Güncel hesap,kaynak,sınır ve saha işleri [NORTH_PC_COMPLETION_021](NORTH_PC_COMPLETION_021.md) içinde; [doğrulama iş akışı](NORTH_VALIDATION_WORKFLOW.md) uygulanmıştır.

Önceki “güncel referans yok”,“yalnız kg amacı var” ve“hiç minimum depo hesaplanmıyor” ifadeleri eski sürüme aittir. Yeni depo hesabı ilk dolum hariç sabit üretimin döngüsel taramasıdır;LP'de depo yatırımı veya güç optimize edildiği anlamına gelmez. Yıllık enerji kısıtı LP'de,yeni kW beyanı ayrı taramadadır. Yakın ERA5/gelecek NASA farkı veri seti/hücre etkisini de içerir;aynı NASA tarihsel karşılaştırma korunur. Kaynaklı besin bileşimi dengeli diyet/kâr/talep değildir. Gerçek Arktik ölçümü veya pilot yapılmış sayılmaz.

Sunum gerekçesi:bilgisayarda planı ve test edilecek belirsizliği belirle;gerçek sefer zaman/konumundaki suyu modelle kıyaslamak ve kaynak suyunun kullanım/arıtma özelliklerini sınamak için izinli saha gözlemi ve numune topla;desteklenen girdiyi aynı motorda güncelle. Kara suyu,zemin ve enerji tahsisi ayrıca doğrulanır. Tek sefer tüm gelecek tarımını doğrulamaz.

---

Önceki geliştirme kayıtları aşağıdadır;021ekinin değiştirdiği ifadeler tarihsel kalır.

# Kuzey karar anlatımı güncellemesi · TESLİM017 · 23 Eylül 2026

Güncel motor ürünleri eşit altı paya ayırmaz: açık çeşitlilik tabanı (%5/ürün), en yüksek taze hasadın %95'ini koruma ve su–enerji normalize uzaklık dengesi kullanır. Aynı koşullarla tarihsel/2030/2050/2090 karşılaştırması, ayrı iklim ön elemesi ve somut üretim/su/altyapı eylemleri eklendi. Tür iklim penceresi yerel tarım uygunluğu değildir; depo hacmi hâlâ tasarım girdisidir. Güncel denklemler ve sınırlar [FUTURE_NORTH_REBUILD](FUTURE_NORTH_REBUILD.md), son doğrulama [BUILD_STATUS](BUILD_STATUS.md). Aşağıdaki TESLİM016 eşit göreli pay amacı ve örnek sonuçlar önceki sürüme aittir.

---

# Future North güncel uygulama · 23 Eylül 2026

Yeni kaynak paketleri: NASA NEX-GDDP-CMIP6 v2.0 üç GCM/20 yıllık pencereler; aynı tarihsel dönem ERA5-Land temsil kontrolü; EDEN ISS altı ürün; MOSJ gerçek aktif tabaka serisi; SoilGrids null yanıtı/ESA metadata; fiziksel CEA/RO kaynakları. Kaynak kayıtları ve hashler data/north altındadır. Kamu verisi kendi saha ölçümümüz değildir; TOPAZ sayısal profil indirilmiş sayılmaz.

Yöntem, kaynak, varsayım ve sınırların güncel ortak kaydı: [FUTURE_NORTH_REBUILD](FUTURE_NORTH_REBUILD.md). Son doğrulama ve teslim: [BUILD_STATUS](BUILD_STATUS.md). Aşağıdaki eski Kuzey uygulama tarifleri kendi tarihleriyle tarihsel kayıttır; bu güncel akışın yerine geçmez. Türkiye ve PWN donanımına ait geçerli kaynak/test kayıtları korunur.

---

# Türkiye iklim duyarlılığı · TESLİM 014

22 Eylül 2026. Bu ek güncel uygulamayı tarif eder; aşağıdaki eski UI tarifleri kendi tarihleriyle tarihsel kayıttır.

Türkiye girdilerine temperature_delta_c (−3…+6 °C, başlangıç 0) eklendi. Yağış günlük kaynak serisine ayrı çarpanla uygulanır. ΔT=0, kaynak ET₀ değerlerini aynen korur. ΔT≠0 için:

ET0_senaryo = ET0_kaynak × max(Tort + ΔT + 17,8; 0) / (Tort + 17,8)

Tort=(Tmin+Tmax)/2. Bu oran, [FAO-56 Denklem 52](https://www.fao.org/4/X0490E/x0490e07.htm) sıcaklık teriminden projenin türettiği, yerelde kalibre edilmemiş duyarlılık varsayımıdır. FAO tarafından önerilmiş bir Penman–Monteith düzeltmesi veya tam meteorolojik yeniden hesap değildir. Kaynaklı formül ile projenin aktarım varsayımı sonuç metadata'sında ayrılır. Tmin/Tmax aynı miktarda kaydırılır; günlük sıcaklık aralığı, radyasyon, nem/rüzgâr, verim, ekim takvimi/Kc ve zemin sabit kalır. Isı/don hasarı, kar erimesi veya gelecek verim etkisi hesaplanmaz. Payda sıfır/negatifse ya da sıcaklık eksik/geçersizse sayısal katsayı üretilmez. Elle girilmiş net sulama bu iklim değişiminden etkilenmez.

Su önizlemesi ve optimizasyon aynı crop_water fonksiyonunu kullanır; sıcaklık önizleme önbelleği anahtarına dahildir. Kaynak mevcut deseni karşılaştırmasında ΔT=0, yağış/ek ET0=1 tutulur. Ham kaynak veri dosyaları değişmedi. Backend request, crop_water ve provenance içinde yöntem, kaynak, değişim, uygulanma durumu, sınırlılıklar; uygun koşuda günlük çarpan min/max/ortalaması vardır. Kuzey'e bu Türkiye sıcaklık deneyi uygulanmaz; Kuzey'de sıfır dışı ΔT reddedilir.

Kadran, model su ihtiyacı / etkin senaryo bütçesidir; %100 kapasite sınırıdır. Gerçek hidrolojik risk olasılığı değildir. Kısmi bölgede adlandırılmış ürün kapsamının oranı gri gösterilir (ör. Çeltik hariç); tüm bölgeye su yeterliliği hükmü verilmez. Toplam su None olmaya devam eder. Artır/azalt önerileri aynı koşunun gerçek optimumundan gelir; verim/kâr veya arazi kullanımının tamamının korunması garanti edilmez.

Eski agrohydro-main/app.py yalnız iklim → kadran → eylem deneyimi için referans alındı. Eski +%5/°C varsayımı, %105/%125 alarm eşikleri, yeraltı suyunda geri dönüşsüz çöküş iddiaları ve hardcoded kotalar taşınmadı. Tarihsel yaklaşık %8,7 göreli baskı sonucudur; yeni m³ hesaplarına dönüştürülmez.

---

# Güncel Türkiye düzeltmesi · TESLİM 008

Yeni kanıt: Konya Ocak2026 yayını / 2024 tablo, Manisa2025 yayını / 2024 tablo, beş noktada 3.655 günlük ERA5 2024–2025. Eski paketler korunur. Güncel hava MODEL_NOWCAST; optimizatör girdisi değil. Çeltik toplam suyu UNKNOWN kalır. Konya hazır verim sütunu uyuşmazlığı kayıtlıdır.

Detay ve son doğrulama: [BUILD_STATUS.md](BUILD_STATUS.md). Aşağıdaki 007 ve daha eski kayıtlar kendi tarihleriyle tarihsel durumdur.

---

# Güncel rebuild kaydı · 22 Eylül 2026

Yeni evidence-to-decision katmanı backend/north_resolution.py: günlük iklim kaynağı SOURCED, eleme MODELED, girilmiş yerel katsayılar ASSUMED, eksikler UNKNOWN. FIELD-MEASURABLE ayrı niteliktir. Kaynak/etkin girdi/hash kayıtları üretilir. Sayısal demo koşullu LP hesabı; gerçek PWN/Arktik veya yerel üretim validasyonu değildir. Bu tur yeni bilimsel veri indirilmedi.

Bağlayıcı sözleşme: [REBUILD_CONTRACT.md](REBUILD_CONTRACT.md). Çalışan/eksik ayrımı: [REBUILD_EVIDENCE_AUDIT.md](REBUILD_EVIDENCE_AUDIT.md), [BUILD_STATUS.md](BUILD_STATUS.md).

---

## Önceki ayrıntılı kayıt (tarihsel uygulama durumları kendi tarihleriyle okunur)

# Kanıt haritası — U11 güncellemesi

22 Eylül 2026 · U11. Güncel ürün/araştırma kapsamı [FINAL_PRODUCT_CONTRACT.md](FINAL_PRODUCT_CONTRACT.md) ile belirlenir. Eski uygulama erişim notları tarihsel kayıttır; E26–E29 yeni edinimi/araştırmayı ekler. Bu belge **dışarıda gösterilmiş bulguyu, ekibin geçmiş sonucunu, kullanıcı beyanını ve yeni araştırma planını** ayırır. U6 uygulamayı açar; U5'in bilimsel kapsamını korur. Hiçbiri bilimsel hipotezin doğruluğunu belirlemez. F/U/W kodlarının envanteri [PROJECT_SOURCE_OF_TRUTH.md](PROJECT_SOURCE_OF_TRUTH.md) içindedir. E01–E19 diğer belgelerin kritik iddia bağlantılarıdır.

Durumlar: **Doğrulandı** = belirtilen kaynağın sınırlı kapsamıyla; **Tarihsel** = geçmiş tarih için; **Kısmi** = önemli bir ayrıntı açık; **Plan/Hipotez** = yapılmış sonuç değil; **Kullanıcı beyanı** = ayrı belgeyle teyit edilmedi.

## İddia → kanıt → kullanım

| CLAIM / ID | STATUS | SOURCE | SOURCE TYPE | EXACT SUPPORT | HOW WE USE IT | LIMITATION |
|---|---|---|---|---|---|---|
| **E01 — Bazı ürünlerin iklimsel uygunluğu kuzeye genişleyebilir.** | Doğrulandı; projeksiyon | [Xu vd. 2026](https://www.nature.com/articles/s43247-026-03702-w), [yazar kurumu PIK kaydı](https://publications.pik-potsdam.de/pubman/faces/ViewItemOverviewPage.jsp?itemId=item_34579) | Hakemli özgün model araştırması; kurum arşivi | Özet: yedi ürün, 30°–83°K; yüzyıl sonunda SSP1-2.6/SSP5-8.5 için yaklaşık 331/739 km iklimsel sınır değişimi. | Gelecek probleminin dış dayanağı. | Gerçek tarım göçü, bizim hesaplamamız veya TASE istasyonunda üretim kanıtı değil. Haritası bizim analizimiz diye sunulmaz. |
| **E02 — Permafrost, iklimsel uygunluğu üretim uygunluğundan ayırır.** | Doğrulandı; model kapsamıyla | E01'deki aynı çalışma; [ESA CCI](https://climate.esa.int/en/projects/permafrost/) | Özgün model araştırması; resmî veri programı | Çalışma permafrost kaynaklı sınırlamayı açıkça değerlendiriyor; ESA ürünleri donmuş zemin verisi için aday. | Ayrı fiziksel filtre ve belirsizlik. | Her permafrost hücresine evrensel sıfır/bir kuralı veya bütün yöntemlere aynı filtre atanmaz. |
| **E03 — Svalbard'da yerel kontrollü sebze üretimi denenmiş ve fizibilitesi incelenmiştir.** | Tarihsel doğrulama | [2019 Longyearbyen fizibilitesi](https://www.miljovernfondet.no/wp-content/uploads/2020/01/18-33-feasibility-study_polarpermaculture.pdf), s.5–6; [UNIS 21.04.2020](https://www.unis.no/news/internship-and-covid-19/) | Svalbard çevre fonunda barındırılan birincil teknik rapor; üniversite haberi | Rapor 2017 deneysel sera üretimini kaydeder ve üretimin enerji/ekonomi koşullarını inceler; UNIS 2020'de Polar Permaculture ile staj çalışmasını kaydeder. | Kuzeyde üretim yönteminin araştırılabilir olduğuna somut örnek. | Hakemli performans deneyi değil; işletmenin 2026'da faal olduğu doğrulanmadı. Eski enerji/fiyat bilgileri güncel katsayı olmaz. |
| **E04 — Hidroponik/CEA su avantajı enerji bedeliyle birlikte değerlendirilmelidir.** | Doğrulandı; bağlama özgü | [Barbosa vd. 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4483736/), DOI 10.3390/ijerph120606879, özet/Tablo1 | Hakemli özgün karşılaştırmalı model çalışması | Yuma/Arizona marulu için konvansiyonel veriler ile mühendislik denklemlerine dayalı hidroponik senaryo kıyaslanır; hidroponikte ürün başına su daha düşük, enerji daha yüksek bulunur. | Enerjiyi ayrı katman yapma gerekçesi. | Arktik deneyi değil; literatürdeki su/enerji oranları evrensel katsayı olarak taşınmaz. |
| **E05 — Arktik'te su, enerji ve gıda güvenliği birbirine bağlı bir araştırma alanıdır.** | Doğrulandı; bölgesel çeşitlilikle | [Arctic Council/SDWG 2025 rapor kaydı](https://oaarchive.arctic-council.org/items/2eae53e6-bf3a-48b7-bff2-bb3e7a922fc4); [Pond Inlet su sistemi araştırması](https://pubs.rsc.org/en/content/articlehtml/2020/ew/d0ew00019a) | Resmî araştırma raporu; hakemli özgün saha çalışması | SDWG raporu SDG2/6/7 bağlantısını ele alır; Pond Inlet çalışması bir Arktik yerleşiminde dağıtılan suyun kalite koşullarını inceler. | Su miktarı kadar kalite, erişim ve altyapıyı değerlendirmek. | Bütün Arktik susuzdur veya Barents'te aynı sorun vardır sonucu çıkmaz; içme suyu çalışması tarımsal su bütçesi değildir. |
| **E06 — Kaynak suyunun özellikleri arıtma performansını ve kaynak maliyetini etkileyebilir.** | Doğrulandı; kıyısal uygulama bizim planımız | [Camacho-Espino vd. 2025](https://www.sciencedirect.com/science/article/pii/S1944398625001730), DOI 10.1016/j.dwt.2025.101157; [FAO su kalitesi](https://www.fao.org/4/T0234e/T0234E01.htm) | Hakemli özgün deney; teknik rehber | Deneysel RO çalışması besleme sıcaklığını 5–45°C aralığında değiştirerek akı, ürün suyu iletkenliği ve enerji etkisini inceler; FAO tuzluluk/iyon etkilerini açıklar. | PWN kaynak karakterizasyonu → arıtma/kalite → enerji → üretim kararı için fiziksel gerekçe. | Sıfıra yakın Arktik sıcaklığına geçerlilik ve seçilecek membran doğrulanmalı. PWN bir RO performans testi değildir; tuzluluk tek başına tam kimya vermez. |
| **E07 — TASE-VII 2027 operasyonu deniz üstü ve rotaya bağlıdır.** | Resmî plan yeniden doğrulandı | [2027 resmî duyuru](https://tubitak.gov.tr/tr/duyuru/kutup-arastirmalari-2027-yili-cagrilari-acildi), [bağlı çağrı PDF](https://tubitak.gov.tr/sites/default/files/2026-06/kutup_arastirmalari_cagri_metni_2027_0.pdf); F5 | Resmî çağrı | s.6 md19: Haziran–Eylül 2027, Barents, yaklaşık 20–40 gün, deniz üstü; rota/süre değişebilir. s.5 md16/18: destek ve sefer değişiklikleri. | Rotadan bağımsız gemi protokolü; yerel kayıt/güç. | Plan garanti değildir. Profesyonel başvuru bütçe/personel hükümleri öğrenciye otomatik uygulanmaz. |
| **E08 — Önceki Türk Arktik araştırmaları fiziksel tabakalaşma, freshwater ve referans ölçüm konularında emsal sağlar.** | Geçmiş işler doğrulandı; bazı güncel görevler kısmi | [TÜBİTAK 19.07.2024](https://tubitak.gov.tr/tr/haber/4-ulusal-arktik-bilimsel-arastirma-seferinde-16-projeye-yonelik-calismalar-gerceklestiriliyor); [DEÜ 30.07.2024](https://imst.deu.edu.tr/tr/news/4-ulusal-arktik-bilimsel-arastirma-seferi-30-07-2024/); [güncel DEÜ personel](https://imst.deu.edu.tr/tr/akademik-personel/); [KARE üyeler](https://polardata.tubitak.gov.tr/members/) | Resmî haber, personel sayfası ve indekslenen üye kaydı | Haber İncili'nin tabakaları, Nasıf Dondurur'un freshwater/akıntı ilişkisini, Biçer'in meteorolojik ölçümlerini açıklar. DEÜ güncel sayfası Doç. Dr. Aslıhan Nasıf Dondurur'u listeler. | Sensör, referans CTD, numune ve gemi yöntemi için soru gündemi. | İncili/Biçer 2026 görevi açık; KARE canlı üye sayfası yükleme sınırı var. Hiçbiri danışmanımız değil; görüşme yapılmadı. |
| **E09 — Ulusal stratejiyle gerçek tematik uyum vardır.** | Yerel resmî PDF'den doğrulandı | [F6 strateji](C:/Users/bahao/Downloads/ulusal_kutup_bilim_stratejisi_2023_2035_1.pdf) | Resmî strateji | PDF25/basılı23 TEMA I: iklim öngörüleri ve iklime dayanıklı tarım; PDF34/basılı32 yenilikçi saha teknolojileri/model/veri; PDF38/basılı36 Stratejik Amaç II bilim-toplum. | Araştırma hedefi ve öğrenci iletişim katkısının strateji karşılığını göstermek. | Kurumsal kabul veya özel proje desteği kanıtı değil. Stratejiyi yalnız tarım belgesi gibi sunmayız. |
| **E10 — İzotop ve yardımcı kimya freshwater kaynaklarını araştırmada kullanılabilir.** | Yöntem emsali doğrulandı; panel açık | [Yamamoto-Kawai vd. 2005](https://doi.org/10.1029/2004JC002793) | Hakemli özgün araştırma | Başlık/çalışma kapsamı δ18O ve alkaliniteyle Arktik freshwater/brine davranışlarını inceler. | Kaynak ayrıştırma için literatür dayanağı; laboratuvara doğru soruları sormak. | Bu kaynak δ2H'nin bizim panelimizde ek değerini tek başına kanıtlamaz; uç bileşenler, deniz matrisi, saklama ve belirsizlik uzmanla kesinleşir. |
| **E11 — Adaptif deniz örneklemesi/GP modelleri önceki araştırmalarda vardır.** | Emsal doğrulandı | [Berget vd. 2018 kurum deposu](https://ntnuopen.ntnu.no/ntnu-xmlui/bitstream/handle/11250/2579599/1-s2.0-S2405896318321980-main.pdf?sequence=4); [3D adaptive sampling araştırması](https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2023.1319719/full) | Özgün konferans makalesi; hakemli özgün makale | İlk çalışma AUV üzerinde Gaussian proxy/GP ile bilgiye göre örneklemeyi; ikinci çalışma nehir plümü sınırında adaptif AUV örneklemesini ele alır. | Klasik sabit/gradient baseline ile karşılaştırılacak aday yöntem emsali. | Arktik PWN başarısı, özgün icat veya AUV geliştirme gerekçesi değil; eşit numune bütçesinde katkımız henüz sınanmadı. |
| **E12 — Konya pilotu ve yaklaşık %8,7 göreli baskı azalması.** | Ekibin geçmiş rapor sonucu | [F2 rapor](<C:/Users/bahao/Downloads/agrohydroraporu (5).pdf>), s.4,7–13,17,19 | Kullanıcının orijinal proje raporu | Konya dört ürün, göreli endeks, optimizasyon; s.17'de 15.702.550 → 14.338.276. | Bilimsel predecessor ve yönetilebilir karar yaklaşımının somut başlangıcı. | Sahada ölçülmüş m³ tasarruf değil; yeni platform doğrulaması değil. Sunumdaki farklı katsayılar DECISIONS'ta ayrıldı. |
| **E13 — PWN yerel fiziksel su durumunu sınar; yıllık karasal arzı tek başına ölçmez.** | Ölçüm kapsamı ve tasarım sınırı | [TEOS-10 GSW](https://teos-10.org/pubs/gsw/html/gsw_SP_from_C.html), [Copernicus TOPAZ](https://data.marine.copernicus.eu/product/ARCTIC_MULTIYEAR_PHY_002_003/description); U5 §12–14,34 | Teknik standart/ürün belgesi + bizim çıkarımımız | GSW iletkenlik/sıcaklık/basınç girdilerinden deniz tuzluluğu dönüşümünü tanımlar; model ürününün ölçeği gözlem noktasından farklıdır. | Kalite kontrollü T/S/p karşılaştırması ve uygun kaynak suyu senaryosu. | Bir profil debi, yıllık güvenilir hacim veya tarım alanını vermez. Bu sınır kaynakların ve ölçüm değişkenlerinin kapsamından çıkarımdır. |
| **E14 — Ekip ve Ali Baha'nın kutup sürekliliği.** | İsimler belgeli; ödüller kullanıcı beyanı | U5 §22–23; [F3 sunum](<C:/Users/bahao/Downloads/SÜRDÜRÜLEBİLİR BİR GELECEK DESENDEN DENGEYE (7).pdf>) slayt1; F1:577,5104 | Kullanıcı beyanı ve yüklenen sunum | Ali Baha Demir, Cem Ural, Ferit Bora Akman; kullanıcı 2204-D Su Yönetimi birinciliğini, Ali Baha için 2204-C ikinciliğini belirtiyor. | Ali Baha'da kutup → iklim/su → birleşme; üç kişisel mektup. | Ayrı ödül/2204-C raporu yok; yıl/alan/proje/rol/dil yetkinliği uydurulmaz. TXT957–958 kişisel rol önerisi gerçek görev kanıtı değildir. |
| **E15 — Mülakat ve form takvimi.** | Güncel kullanıcı teyidi; saat açık | U5 §35; F1:14–27 | Kullanıcı talimatı; TXT içindeki davet aktarımı | 30 Eylül 2026; formlar 48 saat önce; iç hedef 27 Eylül. | 22–30 Eylül dokuz takvim günü ve paralel form akışı. | Orijinal e-posta yok; kesin saat bilinmiyor. 28 Eylül gece yarısı varsayılmaz. |
| **E16 — PWN v0.1 ve Arctic v1 mühendislik seçimleri.** | Kullanıcı kapsamı + tasarım önerisi | U5 §15–16; [DS18B20](https://www.analog.com/en/products/ds18b20.html); [ESP32 ADC](https://docs.espressif.com/projects/esp-idf/en/v6.0/esp32/api-reference/peripherals/adc/adc_calibration.html) | Talimat, üretici teknik belgesi, bizim tasarımımız | Kart/prob temel özellikleri; v0.1 tank ve encoder, Arctic v1 gerçek basınç/reference CTD hedefi. | Öğretmen BOM'u, test/fallback ve sonraki tasarım. | Çip datasheet'i paketli probun deniz/sızdırmazlık onayı değil. Sayısal doğruluk veya Arctic-ready iddiası yok. |
| **E17 — Mevcut tamamlanma durumu.** | Doğrudan bu çalışma alanının güncel kaydı | [BUILD_STATUS](BUILD_STATUS.md), [DATA_ACCESS_LOG](DATA_ACCESS_LOG.md), [U6 uygulama onayı](C:/Users/bahao/.codex/attachments/1cc580a8-6bcb-4076-a685-cf64fe1a2c75/pasted-text.txt) | Çalışma kaydı | U5 audit anında yalnız dokümantasyon vardı; U6 sonrasında ilk çalışan yazılım kesiti, kaynaklı reanaliz paketi ve testler eklendi. Güncel kapsam BUILD_STATUS'tadır. | Yapılan–hedeflenen–seçilince ayrımı. | Yazılım testi fiziksel PWN/CTD/tank deneyi veya bilimsel saha doğrulaması değildir. Fiziksel sonuç yokken üretilmiş sayı yazılmaz. |
| **E18 — İklim, toprak, su ve üretim için ayrı veri kaynakları gerekir.** | Katalogları doğrulandı; veri paketi açık | [NASA NEX](https://www.nccs.nasa.gov/data-collections/nex-gddp-cmip6/), [ERA5-Land](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land?tab=overview), [SoilGrids](https://isric.org/explore/soilgrids), [DSİ](https://www.dsi.gov.tr/sayfa/detay/744), [FAO56](https://www.fao.org/4/X0490E/X0490E00.htm); DATA_REQUIREMENTS | Resmî veri/yöntem kaynakları | Her kaynak farklı değişken/ölçek sunar; katalog varlığı veri doğrulaması değildir. | Türkiye transfer ve kuzey modelinin izlenebilir girdileri. | Yerel kullanım, bağımsız ölçüm, enerji/arıtma katsayısı hâlâ gerekir; İlk audit sırasında veri işleme sonucu yoktu; sonradan edinilen paketler E20/E24/E26 ve BUILD_STATUS içinde kayıtlı. |
| **E19 — RQ1–RQ3 / H1–H3 araştırma tasarımı.** | Hipotez; sonuç yok | U5 §32–34; [FUTURE_PRODUCTION_MODEL.md](FUTURE_PRODUCTION_MODEL.md) | Kullanıcının araştırma soruları ve bizim test önerimiz | Alan/kapasite farkı; ayrı koşullarda dayanıklılık; gözlem öncesi/sonrası hata ve karar farkı ayrı ölçülür. | Test edilebilir, yanlış çıkabilecek bilimsel plan. | Hipotez kaynaklandırılmış olsa da doğrulanmış olmaz; daha dar aralık tek başına daha doğru belirsizlik değildir. |

## Okuma ve erişim notu

Bu turda yeni dış kaynakların iddiaya dayanak olan özet/yöntem veya belirtilen sayfaları incelendi; bütün yeni makaleler uçtan uca okunmuş diye iddia edilmiyor. Xu için yayıncı sayfasının doğrudan açılması zaman zaman engellendi; aynı DOI'nin yazar kurumu PIK kaydı ve yayıncı indeksli özeti karşılaştırıldı. Barbosa için yayıncı 429/PMC tarayıcı kontrolü verdi; DOI ve birincil tam metnin indekslenen özeti/Tablo1 kaydı kullanıldı. RO çalışmasının yayıncı başlığı/özeti Exa ve webde aynı DOI ile doğrulandı. KARE ve görev güncellik sınırları [RESEARCHER_OUTREACH.md](RESEARCHER_OUTREACH.md) içinde ayrı yazılıdır.

## Hâlâ doğrulanması veya uzmanla kesinleşmesi gerekenler

1. **Kişisel belge:** 2204-C yıl/proje/alan/ekip ve ödül kaydı; Cem/Ferit'in gerçek görevleri ve üç formdaki kişisel yanıtlar [E14].
2. **Güncel kişi/kurum:** İncili/Biçer'in bugünkü görevi; KARE indeksinin canlı güncelliği; uzmanların müsaitliği ve destek olasılığı [E08].
3. **Yerel kuzey senaryosu:** Seçilen ürün/yöntem, gerçek enerji ve su altyapısı, kıyısal su alma noktası, arazi/çevre sınırları. Tarihsel Svalbard örneği bunları bugüne taşımaz [E03–E06].
4. **Arıtma modeli:** Donmaya yakın su, membran/teknoloji, iyon kalitesi, geri kazanım, enerji ve konsantre yönetimi açık. İlk yazılımda kaynaklı 5–18°C açıklayıcı duyarlılık parametreleri var; Arktik için doğrulanmış set yok [E06; MODEL_METHODS].
5. **Saha:** İzinli derinlik/zaman, gemi arayüzü, reference CTD erişimi, sensör hedef doğruluğu ve tepki süresi [E07,E13,E16].
6. **Laboratuvar:** δ2H'nin ek bilgi değeri, uç bileşenler, analiz paneli, şişe/hacim/saklama/taşıma ve maliyet [E10].
7. **Veri/test:** Türkiye bağımsız test paketi, 2027 ile eşleşecek model snapshot'ı, gözlemin asimilasyon durumu ve sefer örnekleminin temsil sınırı [E13,E18–E19].
8. **Yeni sonuçlar:** PWN'nin algılama sınırı/tekrarları, model düzeltme katkısı, AI faydası ve üretim kararındaki değişim. Hiçbiri bu audit'te ölçülmedi [E16–E19].

Bu eksikler prototipin ilk deneyi veya mülakat anlatısının hazırlanmasını engellemez. Mülakatta hangi soruyu hangi veriyle cevaplayacağımızı bilmemizi sağlar.

## Uygulamada edinilen yeni kanıt — 22 Eylül 2026

**E20 — Gerçek tarihsel iklim paketi indirildi ve genişletildi.** [Open-Meteo Archive API](https://open-meteo.com/en/docs/historical-weather-api) üzerinden açıkça `models=era5` seçimiyle Konya, Seyhan–Adana, Gediz–Manisa, GAP–Harran, Trakya–Edirne ve Longyearbyen için 2022–2023 döneminde toplam **4.380 günlük kayıt** mevcut. İlk üç noktalı 2.190 satır korunarak genişletildi. [Yerel erişim kaydı](DATA_ACCESS_LOG.md), `data/manifest.json` ve hash ile sabitlenmiş ham JSON dosyaları işlemin kanıtıdır. Sınıf **MODEL / REANALYSIS**; nokta verileri bağımsız istasyon ölçümü, havza ortalaması veya gelecek iklim sonucu değildir. ET₀ hizmet tarafından hesaplanan referans değer; yağış/ET₀ farkı güvenilir çekilebilir su arzı değildir.

**E21 — Seyhan'da ortak ürün buğday için doğrudan resmî emsal var.** [Adana İl Tarım ve Orman Müdürlüğü, 23.06.2020](https://adana.tarimorman.gov.tr/Haber/697/Seyhan-Ilce-Tarim-Ve-Orman-Mudurlugu-Bugday-Cesit-Verim-Demonstrasyonu-Kurdu) Seyhan/Camuzcu'da beş ekmeklik buğday çeşidi denemesini ve hasadı bildirir. Bu, benchmark seçimini destekler; 2023 havza verimi veya yeni modelimizin doğrulanması olarak kullanılmaz. [Bakanlık havza planları](https://www.tarimorman.gov.tr/SYGM/Sayfalar/Detay.aspx?SayfaId=61) ayrıca resmî su bütçesi yolunu gösterir; sayısal tahsis serisi henüz uygulamaya bağlanmadı.

**E22 — İlk ürün katsayıları izlenebilir dış parametrelerdir.** [FAO-56 Bölüm 6](https://www.fao.org/4/X0490E/x0490e0b.htm) Tablo 11–12 kış buğdayının örnek evreleri/Kc değerlerini; [Barbosa 2015 Tablo 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC4483736/) Arizona marulunun yıllık model su/enerji/verim değerlerini destekler. `data/literature_parameters.json` kaynak kapsamı, birim ve standart sapmaları korur. Bunlar Türkiye'ye veya Arktik'e kalibre edilmiş saha katsayıları değildir; kullanılan yerel olmayan varsayım görünür kalmalıdır.

**E23 — Beş Türkiye benchmark'ı kaynaklı tasarım seçimi.** Konya, Seyhan, Gediz, Harran ve Edirne'deki buğday/su bağlamı resmî kurum kaynaklarıyla desteklendi. Kaynaklar, tarihleri ve hangi iddiayı destekledikleri [TURKIYE_BENCHMARKS.md](TURKIYE_BENCHMARKS.md) ve `data/benchmark_context.json` içinde. Aynı hesapta farklı iklim girdilerinin etkisi gösterilir; yerel tahsis veya tüm Türkiye genellenebilirliği doğrulanmış olmaz.

**E24 — Bölgesel kuzey iklim modeli verisi işlendi.** [Open-Meteo Climate](https://open-meteo.com/en/docs/climate-api) üzerinden EC_Earth3P_HR, düzeltme kapalı, 1995–2014 / 2030–2049: 14.610 tam günlük kayıt. [NORTH_DATA_PLAN.md](NORTH_DATA_PLAN.md) ve `data/north/summary.json` kaynak/hesap izidir. İklim göstergeleri kendi işlemimiz; iklim modeli dış kaynaklıdır. Tek model, belirsizlik ensemble'ı/ürün uygunluğu veya deniz suyu gözlemi değildir. Veri sorunları ve dönem değişimi açık kaydedildi.

**E25 — Saha katkısı için eşleştirme kapısı uygulandı.** `backend/field.py` konum/zaman/derinlik ve yerinde sıcaklık tanımını kontrol eder. UI örneği **SIMULATION / EXPLANATORY**; gerçek dış profil yolu kayıtlı kaynak, kalite, UTC/GPS ve basınçtan derinlik ister. Başarılı eşleşme dahi temsil/kalibrasyon kanıtı değildir; kullanıcı senaryo toleransı ve ilgili arıtma aralığı korunur. Kanıt: yazılım testleri ve [PRODUCT_REFOCUS.md](PRODUCT_REFOCUS.md).


## U11 araştırma ve edinim ekleri

**E26 — İki SSP için gerçek küçük iklim alt kümesi var.** [NASA NEX-GDDP-CMIP6](https://www.nccs.nasa.gov/data-collections/nex-gddp-cmip6/) belgelenmiş servisi üzerinden ACCESS-CM2 v2.0, SSP245/585, 2035 Tmin/Tmax/yağış: altı NetCDF, 730 nokta satırı. [Yerel manifest](../data/north/u9_acquisition/manifest.json), [QA özeti](../data/north/u9_acquisition/validated_summary.json), `backend/north_evidence.py` izlenebilirliği sağlar. **Dış gelecek senaryosu; tek yıl/model.** Çok yıllı SSP karşılaştırması, yerel ürün uygunluğu veya saha ölçümü değildir. U11 aday yan kaydı [candidate_review_u11.json](../data/candidate_review_u11.json), sabitlenmiş U9 veri dosyasını değiştirmeden ek kapsam sunar.

**E27 — Araştırılmış portföy, yerel validasyon değildir.** [NORA arpa deneyleri](https://www.nibio.no/prosjekter/northern-cereals--new-markets-for-a-changing-environment), [Tromsø patates deneyi](https://doi.org/10.1007/s11540-025-09854-0), [Alaska çeşit denemesi](https://www.uaf.edu/afes/publications/database/circulars/files/pdfs/C127.pdf), [EDEN ISS](https://doi.org/10.3389/fpls.2020.00656) yüksek enlem ve kontrollü üretim emsalleri sağlar. EDEN ISS Antarktika'dadır. Ispanak/roka/fesleğen yedek adaydır; mikro filizler için ortak parametre seti doğrulanmadı. Evrensel GDD, don, toprak veya yerel su/enerji değeri türetilmedi. [Aday matrisi](FUTURE_NORTH_CROP_SET.md).

**E28 — Numune korunması ve kaynak suyu besleme etkisi.** [IAEA örnekleme/laboratuvar bölümü](https://gnssn.iaea.org/main/ncp/Tunisia/lrae/documents/tracers/Volume_I.pdf) su izotoplarının saklama/buharlaşmadan etkilenebileceğini ve analiz laboratuvarının talimatının izlenmesini destekler. [Penn State hidroponik reçeteler](https://extension.psu.edu/hydroponics-systems-nutrient-solution-programs-and-recipes), kaynak sudaki besinlere göre reçete ayarlamasını destekler. Bu kaynaklar bizim numune hacmi, izin, taşıma, sterilizasyon veya büyüme protokolümüzün onayı değildir. EC eşitliği tam iyon/besin eşitliği olarak kullanılmaz.

**E29 — A/B/C saha programı ve RQ5 tasarımı yeni araştırma önerisidir.** [ARCTIC_RESEARCH_PROGRAM](ARCTIC_RESEARCH_PROGRAM.md) ve [SOURCE_WATER_TO_GROWTH_VALIDATION](SOURCE_WATER_TO_GROWTH_VALIDATION.md), U11 talimatı ve E06/E10/E13/E28 yöntem kapsamına dayanır. Profil/model, hedefli numune ve karar yeniden hesap ayrı çıktılardır. Bağımsız rezervuarlar, rastgele yerleşim ve gerçek/yeniden oluşturulmuş su ayrımı bizim önerilen deney tasarımımızdır; yapılmış deney, kesin örnek sayısı veya anlaşılmış laboratuvar değildir.

Güncel açıklar: gerçek Arktik profil/numune yok; 3B deniz modeli sayısal alt kümesi edinilmedi; yerel karasal tahsis ve permafrost/zemin paketi hazır değil; kutup CEA enerji aralığı/çeşit fenolojisi eksik; fiziksel taşıma ve analiz kabulü belirlenmedi. Bu eksikler arıtma gösterimini bütün saha gerekçesi yapmayı gerektirmez; A/B/C'nin sınanacak sorularını belirler.
