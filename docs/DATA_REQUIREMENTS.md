# Güncel ek — 23 Eylül 2026 / TESLİM 022

Üretici destek senaryosu için aynı yıllık kapsamda hasat, kalite/fire, alıcı kapasitesi, fiyat, işletme gideri, kurulum teklifi, indirim, yayma yılı ve hizmet bedeli gerekir. Fiyatlar/taahhütler otomatik doğrulanmaz. Gerçek teklifler, alım şartları, tahsilat ve pilot kayıtları dış bağımlılıktır.

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

Yeni hesap veri-yok duvarı yerine kaynaklı analoğu, fiziksel model ve açık mühendislik aralıklarını kullanır. Yerel tarımsal tatlı su tahsisi, parsel/yapı zemini, gerçek enerji arzı, CO₂ ve işletme katsayıları hâlâ doğrulanacak bağımlılıktır. Normalize gereken kapasite bunları mevcut saymaz. Gerçek saha için ölçümden önce dondurulmuş eşleşebilir model profili gereklidir.

Yöntem, kaynak, varsayım ve sınırların güncel ortak kaydı: [FUTURE_NORTH_REBUILD](FUTURE_NORTH_REBUILD.md). Son doğrulama ve teslim: [BUILD_STATUS](BUILD_STATUS.md). Aşağıdaki eski Kuzey uygulama tarifleri kendi tarihleriyle tarihsel kayıttır; bu güncel akışın yerine geçmez. Türkiye ve PWN donanımına ait geçerli kaynak/test kayıtları korunur.

---

# Güncel Türkiye düzeltmesi · TESLİM 008

Türkiye yeni varsayılan: 2024 il ekiliş/üretim + 2024–2025 ERA5 günlük seri. Anlık sıcaklık ayrı zaman damgalı model hava bağlamı. Eksikler: gerçek tahsis, sulu/kuru ayrımı, yerel fenoloji/toprak, münavebe/üretim zorunlulukları, çeltik ek suyu. 81 il veri paketi yok.

Detay ve son doğrulama: [BUILD_STATUS.md](BUILD_STATUS.md). Aşağıdaki 007 ve daha eski kayıtlar kendi tarihleriyle tarihsel durumdur.

---

# Veri gereksinimleri ve kaynak planı

**U7 güncel erişim:** ERA5 paketi beş Türkiye noktası + Longyearbyen, 4.380 güne genişledi. Ayrıca EC_Earth3P_HR tek modelinden 1995–2014 / 2030–2049 için 14.610 günlük kuzey iklim kaydı işlendi. Aşağıdaki ilk paket notları tarihsel aşamayı anlatır; güncel kaynaklar DATA_ACCESS_LOG ve NORTH_DATA_PLAN içindedir. Yerel toprak/permafrost, gerçek su tahsisi ve deniz model–gözlem çifti hâlâ eksik.

22 Eylül 2026 — U6 durum güncellemesi. Kaynak kodları [ana kaynak kaydında](PROJECT_SOURCE_OF_TRUTH.md). Bu belge geniş veri gereksinimlerini tanımlar. Gerçekte indirilen ilk paket: Konya, Seyhan–Adana ve Longyearbyen için 2022–2023 ERA5 günlük reanalizi; ayrıca kaynaklı literatür parametreleri ve tarihsel Seyhan plan bağlamı. Kapsam, ham dosya ve sınırlar [DATA_ACCESS_LOG.md](DATA_ACCESS_LOG.md) içindedir. Aşağıdaki diğer katalogların listede olması indirildikleri anlamına gelmez; başlangıç pencereleri/çözünürlük ihtiyaçları öneridir.

## İlk gösterim için en küçük paket

1. Eski Konya çalışmasının dört ürün ve göreli endeks sonuçları: yalnız geçmiş/pilot kartı [F2].
2. Türkiye'de sınırlı bölge ve ortak geçmiş dönem için sıcaklık, yağış ve ETo girdileri; ürün/takvim; mümkünse bağımsız su gözlemi [W5, W8, W12–W14].
3. Bir gelecek dönemi için en az iki senaryo üzerinden iklim uygunluğu örneği; tek gelecek kesin tahmin diye sunulmaz [W7; Öneri].
4. Gerçek PWN tank kaydı, kontrol deneyi ve kalibrasyon notu [U1; henüz üretilmedi].
5. İlgili kıyısal senaryoda su kaynağı → arıtma/enerji → üretim seçeneği ilişkisini anlatan küçük parametre tablosu. Literatür/üretici dayanağı olmayan değer `varsayım` olur [Öneri].

## Kategorilere göre veri

| Kategori | Gerekli değişkenler | Kaynak adayı | Ölçek/zaman ihtiyacı | Kullanım ve dikkat |
|---|---|---|---|---|
| Geçmiş iklim | Tmin/Tmax, yağış, nem, rüzgâr, radyasyon, basınç | MGM/MEVBİS; ERA5/ERA5-Land [W8,W13] | Günlük; bağımsız yıllar içeren ortak dönem | ETo/GDD/don. Reanalysis istasyon gözlemi değildir; değişkenlerin hangi ürün içinde olduğu kontrol edilir. |
| Gelecek iklim | Aynı iklim girdileri; model, SSP, ensemble üyesi | CMIP6/NEX-GDDP-CMIP6 [W7] | Günlük; aday 2041–2060, gerekirse 2071–2100 | NEX katalog çözünürlüğü 0,25°. Kıyı/tarla ölçümü gibi yorumlanmaz. |
| Ürün uygunluğu | GDD tabanı/üst sınırı, don hassasiyeti, fenoloji, fotoperiyot, ekim/hasat penceresi | Ürün agronomi yayınları, yerel denemeler; W1 yalnız frontier örneği | Çeşit × yer × dönem | “Buğday” için tek evrensel eşik atanmamalı; ilk ürün seti küçük. |
| Tarımsal üretim | Ekim alanı, üretim, verim, sulanan alan, takvim | TÜİK, il/ilçe tarım verileri [W14; F2 s.7] | İl/ilçe/yıl; gerektiğinde işletme | İl sınırı ile havza sınırı aynı değil; örtüşme ağırlıkları gerekir. |
| Toprak/zemin | Doku, organik karbon, yoğunluk, derinlik; su tutma parametreleri | SoilGrids ve yerel profil verisi [W10] | Katmanlı toprak profili | SoilGrids tahminidir. Su tutma kapasitesi türetilecekse kullanılan dönüşüm de kaynaklandırılır. |
| Permafrost | Olasılık/dağılım, zemin sıcaklığı, aktif tabaka | ESA CCI [W11] | Kuzey kara alanı; yıllık ürün ve sürüm | Gözlemle eşdeğer değil; açık tarla/altyapı kısıtı. Sera iklim uygunluğu açık tarladan ayrı. |
| Su arzı | Akım, yeraltı suyu, kar/kar erimesi, rezervuar hacmi, çekimler | DSİ, havza planları, uygun hidrolojik modeller [W12]; ERA5-Land bağlamı [W8] | Günlük/aylık, talep dönemine uyumlu | Model runoff'ı doğrudan çekilebilir su hacmine çevirme. Havza alanı, yönlendirme ve kullanım gerekir. |
| Su talebi | ETo/Kc, kök derinliği, stres, sulama kaybı/verimi | FAO-56 + yerel doğrulama [W5] | Ürün gelişme dönemi/gün | Eski göreli ağırlıklar yeni ET katsayısı değildir. |
| Su güvenilirliği | Kurak dönem, bakım/kesinti, depolama kapasitesi, ekosistem/yerel kullanım payı | İşletme/havza kayıtları; açık varsayımlar | Dönemsel | Kapasite ile fiilen güvenilir temin ayrı değişken. |
| Üretim yöntemi | Su girdisi/geri dönüş/tahliye, verim, alan, ısıtma/aydınlatma | Açık tarla/sera/hidroponik deneyleri; ölçüm/üretici belgeleri | Yöntem × ürün × mevsim | Bu görevde yeterli sayısal veri seti henüz seçilmedi. Tek su tasarrufu yüzdesi taşınmaz. |
| Enerji | Elektrik/ısı yükü, kaynak, mevsimsel arz, emisyon, kesinti | Meteoroloji/enerji kayıtları; saha/tesis verisi | En az aylık, kontrollü üretimde daha ayrıntılı | kWh ile kgCO2e ayrı; yenilenebilir kapasite kesintisiz güç varsayımı değildir. |
| Kaynak suyu/arıtma | EC/S/T, iyonlar; hedef su kalitesi; geri kazanım, enerji, kapasite, iletim | PWN/numune; arıtma uzmanı/teknik veri [W6,W15] | Kaynak ve teknoloji özelinde | Soğuk/deniz matrisi için sayısal ilişki henüz seçilmedi; fiziksel örnekle karar bağlantısının ana açığı. |
| Deniz bağlamı | T/S profili, akıntı, deniz buzu, karışım katmanı | Copernicus Marine TOPAZ [W4] | Modelin mevcut günlük/katmanlı alanı | 12,5 km/40 dağıtım seviyesi, yerel ölçüm değil; native 50 katmanla karıştırma. |
| Arktik atmosfer | Sıcaklık, yağış, rüzgâr, radyasyon ve yüzey koşulları | CARRA/CARRA2 [W9] | 2,5 km aday bağlam; erişilen dönem doğrulanacak | Su kolonunu vermez; geleceğin iklim senaryosu değildir. |
| Deniz referansı | CTD C/T/p, kalibrasyon dosyası, zaman/koordinat, iniş hızı | KARE/TASE imkânları ve geçmiş veri | Eşzamanlı/eşkonumlu mümkün olduğunca | Erişim teyit edilmedi. Seferde CTD var diye kesin konuşulmaz. |
| İzotop | δ18O, δ2H, standart, analitik belirsizlik, kaynak uç bileşenleri | Uzmanla seçilecek laboratuvar | Belirli istasyon/derinlik örnekleri | Panel/hacim/saklama kilitli değil. Kaynak izi, doğrudan kullanılabilir su hacmi değildir [W20]. |
| Çevresel bağlam | Arazi örtüsü, koruma alanı, karbon/habitat, yerel kullanım | İlgili ülkenin resmî arazi/koruma kayıtları | Üretim lokasyonuna uygun | Yeni tarımsal alan açmayı otomatik olumlu varsayma. |

Uydu verisi, arazi/kar/buz/yüzey bağlamı için ayrı adaydır. Sentinel veya başka bir ürün yalnız hangi değişkeni ve hangi ölçeği temsil edeceği belirlenince seçilecek; su kolonunun ayrıntılı profilini kendiliğinden sağlamaz [Öneri].

## Türkiye benchmark seçimi

Master sync sonrası kaynaklı senaryo girdileri: Svalbard yerel üretim için tarihsel fizibilite [E03]; hidroponik su–enerji karşılaştırması için Arizona model çalışması [E04]; Arktik WEF bağlamı [E05]; T/S/arıtma bağlantısı için deneysel RO çalışması [E06]. Bunlar otomatik olarak Arktik üretim katsayısı değildir. Her aktarımda ürün, yöntem, sıcaklık aralığı, teknoloji ve maliyet yılı saklanacak. E kodlarının tam URL/kanıt/sınırları [EVIDENCE_MAP.md](EVIDENCE_MAP.md) içindedir.

**Mülakat öncesi inandırıcı Türkiye örneği:** Konya ile veri bulunan ikinci bölge için aynı ürün, ortak dönem, aynı hesap sözleşmesi; girdilerin ve bir kaynak kısıtının kararı nasıl değiştirdiği gösterilsin. Bağımsız sonuç gözlemi yoksa buna transfer/gösterim denir; tamamlanmış validation denmez. Gelecek kuzey örneği, mevcut makalenin kaynaklı sonucu veya yeni hesap açıkça ayrılarak sunulur. Yalnız bir makale grafiğinin gösterilmesi bizim yeniden ürettiğimiz model sonucu değildir [U5 §36; E01,E18,E19].

**Gözlem etkisi karşılaştırma paketi:** dondurulmuş model snapshot'ı, sensör kalibrasyonu, ayrı eğitim/test cast kimlikleri, gözlem öncesi/sonrası aynı hedef/kısıtlar ve çıktı farkı. Veri model asimilasyonuna girdiyse aynı veriye karşı bağımsız başarı iddia edilmez [E13,E19].

**Öneri:** Konya'yı geçmişle karşılaştırma noktası olarak tut; farklı su/iklim/üretim koşullarını temsil eden iki ek bölge seç. Gediz ve Çukurova/Seyhan aday havuzudur, onaylanmış örneklem değildir.

Seçim ölçütleri: ortak ürün bulunması, gözlem/verim/sulama verisine erişim, yeterli geçmiş süre, farklılık gösteren mevsimsellik ve karşılaştırılabilir ölçek. Bir bölgeye ayarlanan parametrelerin başka bölgede ne kadar değişiklik istediği ayrıca raporlanır. Sadece Türkiye haritasına veri yüklemek transfer testi sayılmaz [U1; Öneri].

## Ölçüm ve veri sözleşmeleri

Her veri paketinde asgari metadata:

- kaynak URL/kurum, erişim tarihi, lisans/izin, ürün ve sürüm;
- gözlem/model/senaryo/laboratuvar/demo statüsü;
- konum, koordinat sistemi, zaman dilimi/UTC, takvim, yatay ve düşey çözünürlük;
- değişken adı, birim, eksik veri kodu, kalite işareti ve belirsizlik;
- kullanılan dönüşüm, parametre sürümü ve ham dosya özeti [Öneri; F6 s.21 FAIR yaklaşımı].

**PWN ham kayıt adayı:** device_id, cast_id, sample_index, timestamp_utc/elapsed_ms, raw_conductivity_signal, measured_temperature_C, encoder_count/cable_out_m, pressure_dbar (yalnız varsa), lat/lon (gemi/deck), calibration_id, quality_flag. Kalibre EC, temperature compensation ve practical salinity türetilmiş ayrı sütunlardır; hangi dönüşümün yapıldığı saklanır [Öneri; W15].

**Numune kaydı:** sample_id → cast_id → UTC/konum/örnekleme derinliği → şişe/işlem/saklama → laboratuvar yöntem ve belirsizlik → sonuç. PWN'nin önerdiği derinlik ile fiilî örnekleme derinliği ayrı tutulur [Öneri].

**Karar kaydı:** girdi snapshot'ları + bölge/dönem + üretim hedefi + kısıtlar + model/parametre sürümü + seçilen seçenekler + su/enerji/çıktı aralıkları + açıklama. Sonucu güncellemek önceki sonucu silmez [Öneri].

## Birim ve eşleştirme kuralları

- Yağış mm, alan ha/dekar/m² ve arz m³ açık dönüştürülür; yüzde değişim ile kesir karıştırılmaz [F2 s.8–10'daki eski sürüm farkından çıkarım].
- Akış m³/s ise dönem hacmine çevrilir. Toprak nemi m³/m³ ise kök derinliği olmadan su hacmi değildir.
- C ölçümü µS/cm veya mS/cm olabilir; GSW işlevi beklediği birimle çağrılır. Pratik tuzluluk SP ile Absolute Salinity aynı değişken değildir [W15,W18].
- Basınç/derinlik, gövde/sensör offset'i ve referans yüzey açık belirtilir; encoder denizde gerçek derinlik yerine geçmez [Öneri].
- CMIP6 takvimleri, günlük ortalama/minimum/maksimum ayrımı, yağış akısı dönüşümü ve zaman kapsamı kontrol edilir [Öneri].
- Model–PWN eşlemesinde en yakın hücre veya enterpolasyon yöntemi, zaman farkı ve derinlik düzlemi saklanır [W19; Öneri].

## Veri eksikse davranış

Eksik kalite paneli → “uygun su” sonucu yok; kapsamı sınırlı kaynak karakterizasyonu var. Eksik debi → su miktarı senaryosu açık varsayım. Eksik enerji → su avantajı gösterilebilir, toplam sürdürülebilirlik sonucu verilemez. Eksik bağımsız referans → prensip/tekrar gösterimi yapılır, doğruluk sertifikası iddia edilmez. Bu etiketler arayüzde ve mülakat materyalinde aynı olacaktır [U1; Öneri].

## Güncel edinim ve açıklar — 22 Eylül 2026 / v0.3

- Altı nokta, 2022–2023, **4.380 günlük ERA5**: Tmin/Tmax, yağış, servis kaynaklı FAO-56 ET₀. Nokta reanalizidir; alan/havza ölçümü değildir. CSV/Parquet, ham yanıt ve manifest saklı.
- **Beş ilde 21 resmî ürün alanı/üretim kaydı**: Konya2023; Adana, Manisa, Şanlıurfa, Edirne2024. Yıllar ve coğrafyalar tek yıla/tek havzaya dönüştürülmedi. `production_tonnes*1000/area_ha` ile türetilmiş il ortalama verimi, kaynaklı alan/üretimden ayrı etiketli. Dekar/ha dönüşümleri ve seçili alt küme kapsamı kayıtta. [Kaynaklar ve tablo sayfaları](TURKIYE_REGIONAL_SIMULATOR.md).
- **Dokuz ürün bilgi kaydı**: FAO-56 dört aşama ve Kc örnekleri. GDD/don/tuzluluk/toprak eşikleri yerel doğrulama olmadan doldurulmadı. [Ürün bilgi tabanı](../data/agriculture/crops.json).
- Kuzey: EC_Earth3P_HR, 1995–2014/2030–2049, **14.610 günlük kayıt**; tek model ve düzeltme kapalı. GDD5/don olmayan pencere/yağış bağlamı var. Gelecek ET₀ ve kar-erime hesabı yok; 2041–2060 veya SSP seçimi bu pakette yok. Dönem etiketini değiştirmek veri indirmez. [NORTH_DATA_PLAN](NORTH_DATA_PLAN.md).
- Türkiye hesabında resmî desen/verim ile 2022–2023 hava referansı birlikte kullanılan açık karşı-olgusal senaryo var; 2024 su çekimi ölçümü yok. Takvim, depo, randıman, %50 minimum hedef ve su bütçesi varsayım olarak kayıtlı.
- Kuzeyde dönemsel net su, verim, alan ve enerji kullanıcı senaryosudur; yerel tarımsal uygunluk ve çekilebilir tatlı su miktarı henüz doğrulanmış değil. Sera ısı/ışık modeli, besin bileşimi, maliyet ve toprak/permafrost filtreleri veri bekliyor.
- Gerçek PWN/tank/Arktik verisi hâlâ yok. Deniz modeli profili ve eş zamanlı kayıtlı gözlem için kaynak/UTC/konum/derinlik/kalite gerekir. Deniz kolonundan tarla arz hacmi çıkarılmaz.

İşlenmiş tarım tabloları `data/agriculture/manifest.json` ile; resmî ham dosyalar kaynak başına SHA256 ile korunur. Senaryo düzenlemesi resmî tabloyu değiştirmez. Kaynak erişimi [DATA_ACCESS_LOG](DATA_ACCESS_LOG.md), tamamlanma [BUILD_STATUS](BUILD_STATUS.md) üzerinden izlenir.

## U9 güncellemesi — 22 Eylül 2026

NASA ACCESS-CM2 v2.0 SSP245/585 2035 için 730 günlük nokta kaydı ve altı ham NetCDF edinildi. Önceki “SSP seçimi yok” ifadesi uzun dönem üretim modeli için geçerliliğini korur; arayüzde artık **tek yıllık kaynaklı SSP iklim bağlamı seçimi** vardır. Çok yıllı/çok modelli üretim zinciri değildir. Aylık Tmin/Tmax ortalamaları ve yağış toplamları doğrulanmış günlük CSV'den üretilir; yıllık sıcaklık özeti günlük (Tmin+Tmax)/2 yaklaşımıdır, bağımsız tas değişkeni değildir.

Toprak/aktif katman, gerçek debi/tahsis, yerel CEA enerji aralığı ve sayısal deniz profili hâlâ eksiktir. Katalog/rapor incelenmesi dosya edinimi sayılmaz. Kaynak ve eksikler [NORTH_WATER_SECURITY](NORTH_WATER_SECURITY.md); edinim ve test `data/north/u9_acquisition/manifest.json`, `backend/north_evidence.py`, `tests/test_north_evidence.py`.
