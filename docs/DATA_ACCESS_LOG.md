# Gerçek veri erişim kaydı

22 Eylül 2026 — güncel altı noktalı yeniden analiz paketi ve ayrı kuzey gelecek model paketi. Bu kayıt, önceden tanımlanan aday kataloglarla **gerçekte indirilmiş dosyaları** ayırır. Aynı günkü ilk 2.190 satırlık paket aşağıdaki genişlemeyle 4.380 satıra ulaşmıştır.

## Çalışan paket

`data/processed/climate.csv`: **4.380 günlük satır**, altı noktanın her birinde 2022-01-01–2023-12-31 arasında 730 gün. Türkiye benchmark kümesi beş noktadır; Longyearbyen ayrı kuzey bağlamıdır. Sütunlar `site_id, date, tmin_c, tmax_c, precipitation_mm, et 0_mm, dataset_id`. Dört değişkende bütün noktalarda eksik değer sayısı sıfırdır; kod eksik gelirse boş/null bırakır, sıfır doldurmaz.

Kaynak **Open-Meteo Archive API üzerinden ERA5**, `models=era5` açıkça seçildi. Varsayılan karışık model kullanılmadı. Saatlik reanalizden günlük UTC özet; 0,25° ızgara; `elevation=nan` ile yükseklik düzeltmesi kapalı. Tmin/Tmax °C, günlük yağış/ET₀ mm. ET₀ servis tarafından FAO-56 referans çim için hesaplanır; gerçek bitki evapotranspirasyonu veya çekilebilir sulama suyu değildir. [API yöntem ve değişken belgesi](https://open-meteo.com/en/docs/historical-weather-api)

| Nokta / site_id | İstenen koordinat | Gerçek kaynak hücresi | 2023 yağış toplamı | 2023 ET₀ toplamı | Kullanım |
|---|---|---|---|---|---|
| Konya / `konya` | 37,87°K; 32,49°D | 37,75°K; 32,50°D; 1.189 m | 368,70 mm | 1.342,66 mm | Yeni hesap için geçmiş pilot bölgesindeki karşılaştırma noktası |
| Seyhan–Adana / `seyhan_adana` | 37,00°K; 35,32°D | 37,00°K; 35,25°D; 95 m | 668,90 mm | 1.449,40 mm | Türkiye transfer demonstrasyonu |
| Gediz–Manisa / `gediz_manisa` | 38,61°K; 27,43°D | 38,50°K; 27,50°D; 323 m | 988,60 mm | 1.273,79 mm | Türkiye transfer demonstrasyonu |
| GAP–Harran / `gap_sanliurfa` | 36,87°K; 39,03°D | 36,75°K; 39,00°D; 369 m | 332,80 mm | 1.842,57 mm | Türkiye transfer demonstrasyonu |
| Trakya–Edirne / `trakya_edirne` | 41,68°K; 26,56°D | 41,75°K; 26,50°D; 125 m | 473,70 mm | 1.237,75 mm | Türkiye transfer demonstrasyonu |
| Longyearbyen / `longyearbyen` | 78,22°K; 15,65°D | 78,25°K; 15,75°D; 217 m | 573,20 mm | 262,80 mm | Kuzey üretim senaryosunun tarihsel atmosfer bağlamı |

Tablodaki toplamlar indirilen günlük dosyanın toplamıdır; bağımsız istasyon ölçümü veya uzun dönem iklim normali değildir. Konya ve Adana hücrelerinin temsil ettiği arazi ile gerçek tarlalar aynı değildir. Kuzeyde yağış karı da içerir: bir yıllık yağış toplamı kullanıma hazır su deposu gibi kullanılamaz. Buradaki farklar havzaların tamamına genellenmez.

## Dosya ve yeniden üretim sözleşmesi

- `data/manifest.json`: veri seti listesi, kaynak URL, DOI, sürüm sınırı, erişim zamanı, koordinatlar/çözünürlük, değişken/birim, lisans ve kullanım sınırları, sınıflandırma, eksiklik sayıları, ham dosya yolu ve SHA256.
- `data/metadata/*.json`: her noktanın etkin metadata kaydı; `metadata/snapshots/` hash ile adreslenen metadata sürümleri.
- `data/raw/open_meteo/`: sağlayıcıdan gelen **orijinal JSON baytları**, içerik hash'li dosya adı, üzerine yazılamayan kayıt.
- `scripts/ingest_data.py`: önbellekteki kaydı yeniden kullanır, hash/birim/tarih/Tmin≤Tmax/negatif su değeri kontrollerini yapar; `--refresh` yeni kaynak anlık görüntüsü alır ve eskisini saklar.
- `data/processed/climate.parquet`: pandas/pyarrow ortamıyla aynı tablo; CSV uygulamanın bağımsız ve insan tarafından okunabilir eşidir.
- `data/literature_parameters.json`: dış literatürden elle doğrulanmış sayısal parametreler ve geleceğe ilişkin özet sonuçlar; sağlayıcıdan indirilmiş raster veya kendi model çıktımız değildir.

Open-Meteo veri lisansı CC BY 4.0; Open-Meteo ve ERA5/Copernicus atıfları görünür tutulur. Ücretsiz API ticari olmayan kullanım içindir; günlük 10.000, saatlik 5.000, dakikalık 600 sınırlarının altında kalınır. Bu eğitim/araştırma paketinde ücretli servis veya kimlik bilgisi kullanılmadı. Kaynak veri DOI: `10.24381/cds.adbb2d47`. [Kullanım şartları](https://open-meteo.com/en/terms)

## Neden Seyhan?

Ortak ürün **buğday**: Adana İl Tarım ve Orman Müdürlüğünün 23 Haziran 2020 tarihli birincil kaydı Seyhan/Camuzcu'da beş ekmeklik buğday çeşidinin denemesini ve hasadını bildirir. Bu kayıt ürünün bölgede yetiştirildiğini destekler; 2023 verimi veya bütün havzanın üretim katsayısı olarak aktarılmaz. [Resmî deneme kaydı](https://adana.tarimorman.gov.tr/Haber/697/Seyhan-Ilce-Tarim-Ve-Orman-Mudurlugu-Bugday-Cesit-Verim-Demonstrasyonu-Kurdu)

Seyhan için bakanlıkta kuraklık ve sektörel su planları bulunur; su bütçesi cildi ayrı bir veri erişim yoludur. Aynı üründe, aynı günlerde, aynı fiziksel birimlerle farklı yeniden analiz iklim girdilerini işleyebiliriz. **Bu aşama transfer demonstrasyonudur; doğrulama değildir.** Bağımsız yerel sulama/verim gözlemi ve fiilî su tahsisi henüz sayısal modele alınmadı. [Kuraklık planları](https://www.tarimorman.gov.tr/SYGM/Sayfalar/Detay.aspx?SayfaId=61), [su tahsis planları](https://www.tarimorman.gov.tr/SYGM/Sayfalar/Detay.aspx?SayfaId=10)

**İndirilen havza belgesi:** 88 sayfalık *Seyhan Havzası Kuraklık Yönetim Planı Yönetici Özeti*, kapakta **Ankara 2019**. URL klasöründeki 2023 yayın yılı değildir. Ham PDF SHA256 ile `data/raw/references/` altında korundu. PDF s.45/basılı4-8 Tablo4.4'te planın mevcut durum hesabı için havza tarım kullanımı 1.920,5 hm³/yıl, tüm sektörler toplamı 2.104,53 hm³/yıl. Yalnız **tarihsel plan bağlamı** olarak `data/seyhan_water_context.json` içine işlendi; 2023 gözlemi, bir hektarın tahsisi veya çekilebilir güvenilir arz değildir. Kaynak HTML ve PDF erişim kayıtları `data/reference_manifest.json` içindedir. FAO sayfası web okumasında erişildi, doğrudan dosya indirmesi HTTP403 verdi; ham dosyası varmış gibi kaydedilmedi.

## Ürün parametreleri ve kuzey yolu

**Buğday:** FAO-56 Tablo 11'de Akdeniz kış buğdayı için Kasım başlangıçlı 30/140/40/30 gün örneği; Tablo 12'de başlangıç Kc donmuş toprakta 0,4, donmamışta 0,7; orta dönem 1,15, son dönem 0,25–0,4. Bunlar yerel kalibrasyon değildir. Toprak deposu, başlangıç suyu, tahsis ve sulama randımanı ayrıca açık senaryo girdisidir. [FAO-56 Bölüm 6](https://www.fao.org/4/X0490E/x0490e0b.htm)

**Yöntem karşılaştırması:** Barbosa 2015 Tablo 1'in aynı ürün/marul açık alan ve hidroponik sera su/enerji/verim değerleri ve S.D.'leri kaynak kapsamıyla kaydedildi. Arizona yıllık model hesabı Longyearbyen katsayısı değildir; yalnız kaynaklı yöntem örneği/duyarlılık girdisi olabilir. kJ→kWh için 3.600'e, L→m³ için 1.000'e bölünür; kaynakta yıllık üretime bölünmüş yoğunluk bir kez daha 365'e bölünmez. [Özgün makale](https://pmc.ncbi.nlm.nih.gov/articles/PMC4483736/)

**Kuzey:** Longyearbyen, tarihsel yerel kontrollü üretim fizibilitesi nedeniyle seçildi; sera sahasına erişim veya TASE rotası varsayılmadı. Güncel iki yıllık yeniden analiz geleceğe ait değildir. [2019 fizibilitesi](https://www.miljovernfondet.no/wp-content/uploads/2020/01/18-33-feasibility-study_polarpermaculture.pdf)

Gelecek probleminin literatür dayanağı Xu vd. çalışmasının **2071–2100, SSP1-2.6 / SSP5-8.5, 331 / 739 km** sonucudur. Yedi ürünün 30°–83°K kapsamındaki iklimsel sınır özeti Longyearbyen'e özel bir projeksiyon değildir. [Xu vd. 2026](https://www.nature.com/articles/s43247-026-03702-w)

**Güncel ek veri:** `data/north/` altında Longyearbyen çevresindeki tek EC_Earth3P_HR hücresi için Open-Meteo Climate API'den indirilen **1995–2014 / 2030–2049** günlük dış iklim modeli çıktıları ve bunlardan hesaplanan göstergeler vardır. Bu HighResMIP/CMIP6 kapsamındaki tek modeldir; kendi iklim modelimiz, SSP ensemble'ı veya saha ölçümü değildir. İstenen dönemden yapılan açık değişiklik, kalite kontrolleri, ham hash'ler, model/senaryo sınırları ve 7.305 + 7.305 günlük paketin ayrıntısı [NORTH_DATA_PLAN.md](NORTH_DATA_PLAN.md) içindedir. Kuzey verisi 4.380 satırlık tarihsel ERA5 dosyasına karıştırılmaz.

## Açık erişim ve bilimsel sınırlar

ERA5-Land/CDS kullanıcı hesabı bu oturumda kurulmadı; erişilemez olduğu iddia edilmez. Açık, kimliksiz ve belgeli ERA5 API yolu küçük paketi hemen sağlar. MGM/TÜİK/DSİ istasyon veya tahsis serileri, SoilGrids, ESA permafrost rasterleri, TOPAZ ve CARRA henüz indirilmedi. Bunlar arayüzde **veri yetersiz/henüz bağlı değil** olarak kalır; sahte yerel değerlerle doldurulmaz.

Reanaliz yağış ve ET₀, ürünün fiziksel talep/yağış dengesi için kullanılabilir. Güvenilir kaynak hacmi, depolama işletmesi, başka kullanıcıların payı ve kalite olmadan havza su arzını kanıtlamaz. PWN profili bu eksikleri kapatmaz.

## 22 Eylül 2026 — beş Türkiye benchmark noktasına genişleme

Önceki 2.190 satırlık paket bu bölümden itibaren **4.380 satıra** genişletildi: beş Türkiye noktası (Konya, Seyhan/Adana, Gediz/Manisa, GAP/Harran–Şanlıurfa, Trakya/Edirne) ve ayrı kuzey bağlamı Longyearbyen. Her noktada aynı 2022–2023 döneminin 730 günü ve dört değişken bulunur; eksik değer sayısı sıfırdır. Önceki üç ham kaynak ve metadata kaydı değişmeden önbellekten kullanıldı. Seçim gerekçeleri/resmî kaynak tarihleri `docs/TURKIYE_BENCHMARKS.md` ve `data/benchmark_context.json` içindedir.

| Yeni nokta | Gerçek grid; yükselti | SHA256 |
|---|---|---|
| Gediz/Manisa | 38,50 / 27,50; 323 m | `a 082 a 5 d 7937 a 552 e 6 bfe 7 abeefab 70 ee 0 e 8 dd 35 bab 5 bc 982 f 1315470 c 9754 bd 1` |
| GAP/Harran–Şanlıurfa | 36,75 / 39,00; 369 m | `4 ec 9 fa 9 c 3621 e 5 a 088 e 3479045 e 48 b 8 e 98086 b 5 c 7 ab 8 c 1 f 231 d 6 a 0168 fd 52214` |
| Trakya/Edirne | 41,75 / 26,50; 125 m | `aa 7 b 8 cd 4 e 52198691942 e 01 fd 05 b 59 bcb 9 c 46 d 99340 bc 91636 e 646 acccafea 0 b` |

Yeni kayıtlarda dataset kimliği içerik hash'inin ilk 12 karakterini taşır. Değişen içerik yeni kimlik ve korunmuş metadata snapshot'ı alır; sabit metadata dosyası güncel önbellek işaretçisidir. Tam sorgu URL'leri, UTC erişim zamanı, lisans ve birimler manifesttedir. API'deki geçici bağlantı sıfırlaması ilk denemeyi durdurdu; yeniden çalıştırmada tamamlanmış dosyalar tekrar indirilmeden üç yeni nokta tamamlandı. Sahte veya doldurulmuş değer kullanılmadı.

**Doğrulama:** `tests/test_data.py` içindeki 11 test geçti. Altı ham kaynağın hash'leri, 730 günlük kesintisiz tarihleri, birimleri ve tüm CSV sayısal değerleri ham kayıtla eşleşti. CSV/Parquet tabloları 4.380 satır ve bütün değerler için tam eşit bulundu. Önbellek çevrimdışı çalıştı; bozuk kaynak/sonradan değiştirilmiş CSV, yanlış birim/tarih ve sonlu olmayan değerler reddedildi. Bu kontroller veri hattı bütünlüğünü sınar; agronomik doğrulama değildir.

Lisans ve sağlayıcı değişmedi: [Open-Meteo tarihsel API](https://open-meteo.com/en/docs/historical-weather-api), [CC BY 4.0 veri ve ücretsiz API koşulları](https://open-meteo.com/en/terms). Noktalar havza ortalaması değildir; iki yıllık veri uzun dönem iklim normali değildir.

## 22 Eylül 2026 — resmî tarımsal desen ve ürün bilgi tabanı / U8

Beş il için dört özgün PDF ve bir DOCX, `data/agriculture/raw/` altında indirilen özgün baytların SHA256 içeren adlarıyla saklandı. Konya2023, Adana/Manisa/Şanlıurfa/Edirne2024 sütunlarından toplam21 ürün satırı elle kontrol edilerek aktarıldı. Her kayıtta kaynak URL, tablo/sayfa, veri yılı, yayın yılı, ham dosya yolu, hash ve birimler bulunur. [Tam kaynak listesi ve tablo](TURKIYE_REGIONAL_SIMULATOR.md), [işlenmiş kayıt](../data/agriculture/region_baselines.json).

İkinci işlenmiş kayıt `data/agriculture/crops.json`, dokuz ürün için FAO-56 örnek dört aşama ve Kc girdisi; kuzey adayları için NIBIO/UAF/özgün patates çalışması ve ayrı kontrollü üretim katsayı kaydı taşır. Evrensel GDD/don/tuzluluk eşikleri doldurulmadı. [Kuzey adaylarının birincil kaynakları](FUTURE_NORTH_CROP_SET.md).

İki işlenmiş JSON da `data/agriculture/manifest.json` ile incelemiş sürüm hash'ine bağlandı. Uygulama hem ham resmî belge hash'ini hem bu iki tabloda işlenmiş sürüm hash'ini kontrol eder. Kullanıcı senaryosu ayrı kaydedilir. Bu kaynak aktarımı denetimi, yerel tarımsal model validasyonu değildir. Resmî tabloların yeniden dağıtım lisansı ayrıca kesinleştirilmedi.

## U9 — NASA iki SSP tek yıl alt kümesi

22 Eylül 2026: NASA NEX-GDDP-CMIP6 belgelenmiş THREDDS yolu, ACCESS-CM2 v2.0, SSP245/SSP585,2035 Tmin/Tmax/yağış. İlk sürüm eki olmayan URL404 verdi; katalogdan v2.0 çözülerek altı NetCDF alındı. `scripts/research_north_u9.py`; ilk/başarılı denemeler ve kataloglar `data/north/u9_acquisition/` altında saklandı. 2×2 hücrede 8.760 ham değer; en yakın 78,125°K/15,625°D noktasında 730 günlük satır. Kaynak [NASA NEX-GDDP](https://www.nccs.nasa.gov/data-collections/nex-gddp-cmip6/).

Birimler ve Tmin≤Tmax, yağış≥0, sonlu sayılar, yıl/datescope denetlendi. Altı ham dosya, günlük türetim, özet, edinim kaydı ve araştırma JSON'u 10 dosyalı SHA manifestine bağlı. Aylık yağış toplamının yıllık toplamı koruması ayrıca testli. Kaynak bağlamı seçiminin kendi başına optimumu değiştirmemesi testli; bunun için henüz bağlı olmayan agronomik tepki uydurulmaz.

Bir modelin tek yılı uzun dönem SSP sıralaması veya ensemble değildir. Su tahsisi, ET₀ ve yerel uygunluğa doğrudan çevrilmez. TOPAZ gerçek sayısal profil/NVE tahsis/ESA permafrost rasteri bu tur alınmadı; birincil katalog ve gereksinimler [NORTH_WATER_SECURITY](NORTH_WATER_SECURITY.md).
