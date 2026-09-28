# Kuzey ürün ve zemin kanıtı — 23 Eylül 2026

Bu paket dokuz ürün adayını, altı kontrollü üretim seçeneğinin yayımlanmış verimini ve Longyearbyen çevresinin gerçek zemin gözlemlerini karar akışına bağlar. Katalog bir ürün tercih listesi değildir; mahsul, yöntem ve araştırma koşulları ayrı alanlarda tutulur. Henüz yapılmış TASE veya yerel tarım deneyi içermez.

## Kaynak ve hesap ayrımı

- `data/north/crop_evidence_v2.json`: birincil kaynaklar, dönem, kapsam, yöntem, gözlenen aralık ve aktarım sınırı.
- `data/north/ground_evidence.json`: kamuya açık MOSJ çizelgesinden çıkarılmış gerçek değerler; SoilGrids nokta yanıtı; ESA CCI ürün metadata kaydı; bunlardan ayrı açık planlama politikası.
- `backend/north_candidates.py`: `get_catalog()`, `get_ground_evidence(site_id)`, `evaluate_candidates(climate_context, site_id)` ve `complete_cycle_capacity(crop, season_days, area_m2)`.

Kaynak hiyerarşisi: yerel bölge gözlemi → resmi/kurumsal ürün → kuzey tarla deneyi → kontrollü kutup analoğu → açıkça belirtilmiş model hesabı. Eksik yerel değeri sıfırla doldurmak veya analoğu yerel ölçüm diye sunmak yoktur.

## Hesaplanabilir kontrollü adaylar

[Zabel ve arkadaşlarının EDEN ISS çalışması](https://doi.org/10.3389/fpls.2020.00656), 2018'de Antarktika'da kontrollü, kapalı aeroponik üretimi raporlar. Aşağıdaki sayılar makalenin 3, 6, 7 ve 9 numaralı tablolarından gelir. Alan, bitkinin yetiştirildiği yüzeydir; bina taban alanı değildir. Aralıklar tekrarların minimum–maksimumudur; geleceğin verimine ait güven aralığı değildir.

| Ürün / deney varyantı | Çevrim gün | Tekrar | Taze yenebilir kg/m²/çevrim, ortalama [min–max] | PPFD µmol/m²/s |
|---|---:|---:|---:|---:|
| Marul / Expertise | 38 | 15 | 2,38 [1,50–3,50] | 330 |
| Roka / ilk düşük ışık uygulaması | 24,2 | 9 | 3,05 [1,87–4,34] | 330 |
| Turp / Raxe | 22,6 | 10 | 1,82 [1,10–3,21] | 600 |
| Alabaş | 58,71 | 6 | 8,11 [5,74–10,58] | 300–400 |
| Pazı | 90 | 3 | 9,26 [7,35–11,28] | 330 |
| Fesleğen / Dolly | 121 | 2 | 7,30 [6,37–8,22] | 330 |

Alabaş için 350 PPFD, kaynak aralığının açıkça belirtilmiş orta noktasıdır. Verim bir ışık-doz yanıtı modeli değildir. Roka yüksek ışık varyantı aynı tabloda bulunur, fakat düşük ışık verimiyle yüksek ışık tüketimi karıştırılmaz. Pazı ve fesleğen çevrimi birden çok hasadı içerir; her gün yeni bir tam çevrim sayılmaz.

Sıcaklık hedefleri aydınlıkta 21°C, karanlıkta 19°C; bağıl nem %65 ve CO₂ 1000 ppm'dir. **17 saat fotoperiyot, 17 saat tam güç değildir:** 15 saat tam ışık + iki kez 1 saat yarım ışık = 16 eşdeğer tam ışık saati. DLI, `PPFD × 16 × 3600 / 1e6` hesabıyla gelir. 330 PPFD için 19,008; 600 için 34,56 mol/m²/gün. Bu koşullar bir optimum iddiası değil, deneyi mümkün kılan koşullardır.

Bu kaynak ürün başına su tamamlama miktarı vermediği için katalogda `makeup_m3_kg` boştur. Devrede dolaşan su, taze su tüketimi değildir. Su hesabı ayrıca fiziksel bir denge veya açıkça etiketlenmiş aktarım gerektirir. Işık, CO₂ besleme, iklimlendirme, kök sistemi ve işletme şartları yerel pilota aktarılmadan aynı verim beklenemez. [UAF 2007 raporu](https://www.uaf.edu/afes/publications/database/variety-trials/files/pdfs/AES-2007.pdf), s.24–25'te NFT marul için ayrı kuzey yöntem öncülü sağlar; enerji katsayısı olarak kullanılmaz.

## Açık tarla adayları ve eşikler

Arpa, patates ve buğday görünür araştırma adaylarıdır. Bilinmeyen çeşide eşik veya verim uydurmak yerine açık araştırma sınırı gösterilir. [FAO-56 Tablo 11–12](https://www.fao.org/4/X0490E/x0490e0b.htm) açık tarla Kc ve örnek takvimlerini sağlar: arpa/bahar buğdayı 0,30–1,15–0,25, patates 0,50–1,15–0,75. Gelişme ve geç dönemler için doğrusal geçiş uygulanabilir; bu, otomatik olarak Arktik fenoloji takvimi değildir. Kc, hidroponik su tamamlama katsayısı olarak kullanılmaz.

[UAF IARC'nin 2022 açıklamasındaki](https://uaf-iarc.org/2022/02/03/climate-change-could-enable-alaska-to-grow-more-of-its-own-food-now-is-the-time-to-plan-for-it/) yaklaşık arpa olgunlaşma hedefi **2500 Fahrenheit derece-gün, taban 32°F**'dir. Doğru dönüşüm 1388,89 Celsius derece-gün, taban 0°C'dir. Taban 5°C toplamına veya Celsius olarak 2500'e çevrilmez. Bu hedef altında kalan ortalama yıllık GDD0, aktarılmış araştırma elemesidir; yerel çeşit denemesinin yerine geçmez. Tam günlük yıllar varsa yılların toplamı birbirine eklenmez; yıllık toplamların ortalaması ve hedefi karşılayan yıl sayısı ayrı raporlanır.

[NIBIO Northern Cereals raporu](https://www.nibio.no/prosjekter/northern-cereals--new-markets-for-a-changing-environment/_/attachment/inline/9b22f769-3666-463e-bcca-4c058231fc5d:1167bdffe36f245bedb4dcfa9c70a4a87315e953/NORA%20Northern%20Cereals%20Final%20Report.pdf) kuzey Norveç arpa denemelerine dayanak verir; tarihsel bir denemenin süresi evrensel minimum değildir. [Mølmann ve Johansen'in patates çalışması](https://doi.org/10.1007/s11540-025-09854-0), Tromsø'de 24 saat doğal fotoperiyot altında 12 litrelik saksılarda sıcaklık etkisini araştırır. Saksı kütlesi tarla kg/ha verimine çevrilmedi. Buğdaya Akdeniz kış takvimi, patatese 86 günlük deney süresi zorunlu kuzey eşiği olarak yüklenmedi.

Don olmayan dönem bağlam olarak tutulur. Katalogda doğrulanmış, çeşide özgü don-gün veya GDD eşiği olmayan bir ürün için `null`, geçer not sayılmaz. Aynı şekilde dış hava soğuğu, gerekli ısıtma ve ışığı hesaplanan yalıtılmış bir iç üretim seçeneğini tek başına veto etmez.

## Xu 2026 — tam yöntemin doğrulanması

[Xu ve arkadaşlarının makalesi](https://doi.org/10.1038/s43247-026-03702-w), 30 Mayıs 2026'da yayımlandı. Kuzey Yarımküre 30–83°N kapsamında yedi ürün (buğday, mısır, arpa, soya, ayçiçeği, şeker pancarı, patates) için **MaxEnt 3.4.4 / ENMeval 2.0.5** kullanır. İlk havuzda 63 çevresel değişken vardır; son analiz 5 yay-dakika çözünürlüktedir. CHELSA 2.1 girdileri 1980–2010, 2041–2070 ve 2071–2100 dönemlerini; SSP1-2.6/SSP5-8.5 ve beş CMIP6 modelini kapsar: GFDL-ESM4, MPI-ESM1-2-HR, MRI-ESM2-0, IPSL-CM6A-LR, UKESM1-0-LL.

Makalede %75 eğitim/%25 doğrulama ve on tekrarlı AUC değerlendirmesi, MaxEnt değişken/seçim süreci, MAAT temelli yüzeye yakın permafrost modeli ve NSIDC zemin buzu katmanı bulunur. Yüzyıl sonu kuzey sınır kayması senaryolara göre yaklaşık 331/739 km; yeni iklimsel sınır 4,86/11,64 milyon km²; bunların permafrost çözülmesiyle etkilenebilecek oranları %29/%18'dir. Bu yarımküre sayıları Longyearbyen'de yetiştirilebilir hektar veya verim değildir. [Kaynak veri/kod arşivi](https://doi.org/10.5281/zenodo.20282716) ayrı izlenir.

Uygulamanın GDD araştırma elemesi bu makalenin MaxEnt replikasyonu değildir. Aynı şekilde uygulamanın NASA çoklu model altkümesi, bu makalenin CHELSA ensemble'ı diye adlandırılmaz. Makale iklim uygunluğu ile toprak/permafrost uygunluğunun farklı olduğunu temellendirir; kontrollü marul verimi sağlamaz.

## Gerçek zemin verisi ve yöntem kararı

[Norveç Meteoroloji Enstitüsü/MOSJ Janssonhaugen kaydı](https://mosj.no/en/indikator/climate/land/permafrost/) Longyearbyen'den yaklaşık 20 km uzakta bir sondaj noktasını izler. Kamu sayfasının `wpDataCharts[207]` JSON'u 1998–2024 için **27 gerçek aktif-tabaka değeri** içerir: 1998=154 cm, 2023=204 cm, 2024=218 cm. Bunlar grafikten gözle tahmin edilmedi. Kaynak sayfasının eski açıklaması 2023'ü rekor olarak anarken tablo 2024'ü içeriyor; sürüm farkı kaydedildi. Ham HTML SHA256 ve çıkarma yöntemi veri dosyasındadır.

`wpDataCharts[208]` sıcaklık tablosu 1999-01-01–2024-09-19 arasında 9394 tarih içerir. İlk/son 15, 25, 40 m değerleri saklandı; son değerler sırasıyla −4,5287/−4,7639/−4,9726°C'dir. Kaynak bu seriyi 366 günlük kayan ortalama olarak açıklar; bağımsız ham günlük ölçümler denmedi. Aktif tabaka kalınlığı, tarımsal kök toprağı kalınlığı değildir.

[UNIS PermaMeteoCommunity](https://www.unis.no/project/permameteocommunity/) Longyeardalen'in zemin buzu ve tuzlu denizel killerindeki mekânsal değişkenliği gösterir. Bu yüzden çevresel permafrost gözlemi açık tarla için otomatik yerel onay sağlamaz; bütün bölgenin tarımı fiziksel olarak imkânsız demek de değildir.

**Açık planlama politikası:** parsel, kullanılabilir toprak, drenaj, zemin kararlılığı ve izin doğrulanana kadar açık tarla `requires_site_validation` durumunda tutulur ve normalize plana alan atanmaz. Yalıtılmış kök ortamlı kontrollü üretim karşılaştırılabilir; temeller ve yapı zemini ayrıca doğrulanacaktır. Sera zarfı ile hidroponik kök yöntemi fiziksel olarak farklı eksenlerdir; arayüz seçeneklerinde sera, kontrollü soilless zarfı ifade eder.

### ESA CCI v5.0 ve SoilGrids kontrolü

[ESA CCI resmi kataloğu](https://climate.esa.int/en/projects/permafrost/data/) 1997–2023 yılları, 1 km çözünürlük ve yıllık permafrost oranı/aktif tabaka/zemin sıcaklığı ürünlerini doğrular. Bunlar uydu/ERA5 ile zorlanan termal **model** ürünleridir. Bu pakette gerçek yerel MOSJ ölçümü kullanıldı; **CCI raster noktası çıkarılmadı**, alınmış piksel değeri iddia edilmiyor. Üç ürün DOI'si JSON'da bulunur. 2023 tarihsel katman geleceğin permafrost haritası değildir.

[SoilGrids resmi belgeleri](https://docs.isric.org/globaldata/soilgrids/) REST hizmetinin geçici sorunlarını bildiriyor. Buna rağmen 23 Eylül 2026'da 78,22°N/15,65°E için yapılan gerçek sorgu başarılı JSON döndürdü; 0–5 cm pH, kil ve organik karbon ortalamalarının **üçü de null**. Yanıt ve SHA256 saklandı; nokta değerleri uydurulmadı. [ISRIC kullanım sınırı](https://docs.isric.org/globaldata/soilgrids/SoilGrids_faqs_04.html) ürünün tarla ölçeği kararları için önerilmediğini belirtir. Gelecekte geoteknik/agrnomik yerel kontrolün yerini alamaz.

## Normalleştirme, amaç ve sonraki saha bağı

100 m² yetiştirme yüzeyi bir **analitik normalleştirmedir**, Longyearbyen'de tahsis edilmiş arazi veya yapılabilir yapı alanı değildir. Sezon başına kapasite açıkça `floor(sezon_günü / ortalama_çevrim_günü) × m² × kg/m²/çevrim` hesabından gelir. Tamamlanmamış son çevrim hasat sayılmaz. Fide alanı, çevrim arası boşluk ve işletme kayıpları gerçek pilota geçerken ayrıca eklenmelidir.

Ürünler arasındaki taze kütle toplamı beslenme yeterliliği/kâr değildir. Eşit göreli kapasite veya çeşitlilik tercihleri seçilirse bunlar açık planlama politikası olarak adlandırılmalı; bilimsel talep verisi gibi saklanmamalıdır. Gerçek bir talep sepeti yokken gizli ürün ağırlığıyla “en iyi” ilan edilmez. Ürün bazında kaynak/kütle ve tam-çevrim kapasitesi karşılaştırması, su/enerji Pareto sonuçları ve açık bir max–min çeşitlilik hedefi birbirinden ayrılabilir.

PWN, zemin veya GDD boşluğunu doldurmaz. Eşleşmiş C/T/p profili ve izinli uzman-onaylı numune, kaynak suyu/arıtma modelinin uygun değişkenlerini besler. Aynı karar motoru yeniden çalışır; değişmeyen karar geçerli sonuçtur. Kontrollü pilot bu analoğun yerel su, enerji ve üretim ölçümleriyle sınanacağı sonraki aşamadır.

## Doğrulama ve sınırlar

23 Eylül 2026: `.venv/Scripts/python.exe -m pytest tests/test_north_candidates_v2.py -q` — **19 geçti**. GDD taban/birim ayrımı, çok yıllı toplamın yanlış yığılmaması, eksik yıl, ışık rampası/DLI, kesirli son hasadın sayılmaması, açık tarla zemin kapısı, 27 gerçek aktif-tabaka kaydı, belirsiz değerin sıfırlaştırılmaması ve değişmez katalog kopyaları denetlendi. Fiziksel tarım doğrulaması veya mobil arayüz testi yapılmadı.

Açık bağımlılıklar: seçili parsel/izin/zemin; yerel cultivar deneyi; sera yapısı ve CO₂ tedariki; gerçek işletme kayıpları; ürün bazında kontrollü su tamamlama; yerel enerji ve mevsimsel kullanılabilir su tahsisi. Normalleştirilmiş kaynak hesabı bu bağımlılıkları yerel kapasiteye dönüştürmez.
