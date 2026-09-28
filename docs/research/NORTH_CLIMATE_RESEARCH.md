# Future North: çok modelli iklim katmanı

Araştırma tarihi: 23 Eylül 2026 (Türkiye). UTC erişim zamanları her ham dosyanın metadata kaydındadır. Bu çalışma dış kaynaklı iklim simülasyonlarını işler; gelecekte ölçülmüş hava koşulu veya ekibin saha ölçümü üretmez.

## Önceki durum ve yeni seçim

Mevcut `data/north/` içindeki EC_Earth3P_HR 1995–2014 / 2030–2049 tek-model serileri ve `u9_acquisition/` içindeki ACCESS-CM2 2035 tek-yıl SSP alt kümesi korunur. Bunlar yeni çok-modelli veri paketinin yerine kullanılmaz. Tek yılın iklim dönemi diye sunulması ve tek modelin belirsizliği temsil etmesi engellenir.

Yeni bağımsız paket `data/north/rebuild_climate/` altındadır ve **tamamlandı**: 1.680 ham NetCDF, 36 katalog, 7 iklim bağlamı, 21 ayrı model/dönem günlük serisi; 420 model-yılı ve 153.399 günlük model-nokta kaydı (613.596 kaynak değişken değeri). `acquisition_progress.json` ve `manifest.json` hazır durumdadır. İlk üç dönemin her model serisi 7.305, 2081–2100 serisi 7.304 gündür; 2100 Gregoryen artık yıl değildir.

## Soru, kaynak ve karar rolü

| Araştırma sorusu | Gerekli değişken | Seçilen kaynak / yedek | Ölçek ve dönüşüm | Model rolü / sınırlama |
|---|---|---|---|---|
| Hangi dönemde ne kadar sıcaklık birikimi mümkün? | Günlük Tmin, Tmax | NASA NEX-GDDP-CMIP6 v2; eski HighResMIP yalnız tarihsel karşılaştırma | 0,25° hücre, günlük; K → °C, sonra model-yıl bazında GDD | Ürün aday taraması; çeşide özgü olgunluk veya yerel verim kanıtı değil |
| Don olmayan dönem nasıl değişiyor? | Günlük Tmin | Aynı NASA paketi | Her yıl Tmin > 0°C ardışık en uzun seri | Tanımlayıcı don penceresi; her ürün için evrensel don toleransı değil |
| Mevsimsel su girdisi ne? | Günlük yağış akısı | NASA; gelecekte yerel hidroloji için ayrı model | kg m⁻² s⁻¹ × 86.400 → mm/gün; aylık/yıllık toplam | Yağış/kar su eşdeğeri; çekilebilir sulama suyu veya akış değil |
| Kontrollü üretimde dış ortam yükü ne? | Tmin/Tmax, yüzeye gelen kısa dalga radyasyon | NASA rsds; yerel bina/sera parametreleri ayrı | W/m² × 0,0864 → MJ/m²/gün; günlük sıcaklık profili korunur | Isıtma/aydınlatma hesabına girdi; bina kaybı ve PAR dönüşümü ayrı açık varsayım |
| Yerel kaynak hücresi ne kadar temsil edici? | İstasyon / yüksek çözünürlüklü geçmiş reanalysis | CARRA/CARRA2 ve ERA5-Land | Bağımsız geçmiş karşılaştırma, aynı dönem ve yükselti denetimi gerekir | Bu tur NASA'ya ek bias düzeltmesi yapılmadı; aşağıdaki çalışma bağımlılığı açık |

## Dönem, SSP ve modeller

[IPCC AR6 WGI §1.4.1](https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-1/) değişimi göstermek için 20 yıllık çok-modelli pencereleri kullanır. Biz de aynı yakın/orta/uzak dönemleri ve 1995–2014 karşılaştırma dönemini seçtik. Bu seçim WMO'nun 30 yıllık meteorolojik normal tanımıyla aynı iddia değildir.

| API ufku | Arayüzün göstereceği dönem | Deney |
|---|---|---|
| `historical` | Geçmiş iklim · 1995–2014 | CMIP6 historical; gözlem veya bugün değil |
| `near` | Yakın dönem · 2021–2040 | SSP2-4.5 veya SSP5-8.5 |
| `mid` | Yüzyıl ortası · 2041–2060 | SSP2-4.5 veya SSP5-8.5 |
| `late` | Yüzyıl sonu · 2081–2100 | SSP2-4.5 veya SSP5-8.5 |

Model alt kümesi: ACCESS-CM2 (CSIRO-ARCCSS), MPI-ESM1-2-HR (MPI-M), MRI-ESM2-0 (MRI); her biri `r1i1p1f1`. Ayrı kurum/model aileleri, gerekli dört değişkenin iki SSP ve geçmiş deneyde bulunması ve yeniden üretilebilir sınırlı indirme büyüklüğü seçimin gerekçesidir. Bu üçlü tam CMIP6 dağılımını, bütün duyarlılık aralığını veya bölge için performans-optimal bir ensemble'ı temsil etmez. Sonuçlar görülerek model seçilmedi; performansa göre ağırlık atanmadı.

Öncelikli konum Longyearbyen isteği 78,2232°K / 15,6469°D; kaynak merkez hücresi 78,125°K / 15,625°D. Tromsø 69,6492°K / 18,9553°D için 69,625°K / 18,875°D hücre şeması tanımlıdır; indirilmemiş konum hiçbir hazır listede görünmez. Planlama hücresi TASE gemi istasyonu değildir.

## Güncel NASA sürümü ve kullanım sınırı

[NASA v2 teknik notu](https://www.nccs.nasa.gov/wp-content/uploads/2025/06/NEX-GDDP-CMIP6-v2-Tech_Note.pdf) 31 Mayıs 2025 güncellemesidir. Veri günlük, 0,25° ve 1950–2100 kapsamındadır; 2015 sonrası SSP deneyidir. BCSD geçmiş referansa göre istatistiksel düzeltme ve mekânsal ayrıştırma uygular. Not küçük adalarda temsil hatasına ayrıca dikkat çeker. Bu nedenle Longyearbyen hücresi tarla, vadi veya havza çözünürlüğünde yerel doğrulama sayılmaz. NASA özet web sayfasında eski sürüm numaraları da görünür; uygulama her dosyanın gerçek `version=2.0` başlığını ve `_v2.0.nc` katalog yolunu doğrular. Dosya lisansı da metadata'da tutulur; tek varsayılan lisans uydurulmaz.

Yöntem/data tanımlayıcısı: [Thrasher vd. 2022](https://doi.org/10.1038/s41597-022-01393-4); [veri DOI](https://doi.org/10.7917/OFSG3345). NASA Earth Exchange / NASA Ames Climate Analytics Group, dağıtıcı NASA NCCS ve CMIP6 modelleme kurumları kaynak gösterilmelidir. Ham NCSS dosyalarında kurum, lisans, model üyesi, üretim tarihi, tracking_id ve kaynak yöntem saklanır.

## Bizim hesaplarımız

Günlük sıcaklık ortalaması `(Tmin+Tmax)/2` yaklaşımıdır; ayrı `tas` değişkeni indirilmiş gibi sunulmaz. Her model ve yıl kendi kronolojisi içinde hesaplanır:

- GDD0 = Σ max(Tortalama, 0); GDD5 = Σ max(Tortalama−5, 0). Üst sıcaklık sınırı uygulanmaz; bunlar tanımlayıcı göstergelerdir.
- Don olmayan gün sayısı: Tmin > 0°C. En uzun kesintisiz seri yıl sınırında sıfırlanır. 0°C günü don olmayan gün sayılmaz.
- `growing_season_5c_run_days`: Tortalama > 5°C olan en uzun seri; agronomik onaylı ekim/hasat penceresi değildir.
- Isıtma derece-gün: Σ max(18−Tortalama, 0). 18°C açık referans olup ürüne özgü optimum veya gerçek kWh değildir.
- Aylık yağış ve radyasyon: önce her yılın aylık toplamı, ardından 20 yılın ortalaması. Yirmi yıl toplamı bir yıllık su olarak kullanılmaz.
- GDD/don gibi doğrusal olmayan metrikler günlük modeller ortalanmadan hesaplanır. Sonra model dönem ortalamalarının eşit ağırlıklı ortalaması ve min–max aralığı alınır.

Üç model min–max aralığı güven aralığı veya olay olasılığı değildir. Aynı iklim dosyalarında 20 yılın tamamı ve model kimlikleri korunur; ürün eşiği geçen model-yıl sayısı ayrıca hesaplanabilir. SSP'ler birbirine karıştırılmaz. Kısa vadede iki SSP farkı doğal/model içi değişkenlik nedeniyle monoton olmak zorunda değildir.

## Kuzeye tarım kayması makalesiyle ilişki

[Xu vd. 2026](https://www.nature.com/articles/s43247-026-03702-w) yöntemleri doğrudan incelendi: CHELSA v2.1, 5 GCM, SSP1-2.6/SSP5-8.5, yedi ürün ve MaxEnt 3.4.4 ile uygunluk; 63 başlangıç çevresel değişkeni, ayrıca permafrost/zemin buzu değerlendirmesi. Dönemleri 1980–2010, 2041–2070 ve 2071–2100'dür. Bu çalışma iklimsel uygunluğun permafrostla sınırlanabileceğini destekler; bizim üç model/günlük GDD elememiz makalenin replikasyonu veya oradan doğrulanmış ürün eşiği değildir. Makalenin haritası kendi model çıktımız gibi alınmadı.

## ERA5-Land ve CARRA araştırma sonucu

[ERA5-Land resmi katalog](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land?tab=overview): 1950'den günümüze saatlik, dağıtım 0,1°, doğal grid yaklaşık 9 km; atmosferik ERA5 zorlamalı kara yeniden analizi. Geçmiş kar/toprak/su süreçleri için yararlıdır; gelecek projeksiyonu değildir. Mevcut eski ERA5 indirmesini bu tur ERA5-Land diye yeniden adlandırmadık.

Ayrıca **gerçekten indirilen bağımsız karşılaştırma serisi**: Open-Meteo Archive üzerinde açık `models=era5_land`, 1995–2014 günlük Tmin/Tmax, 7.305 eksiksiz UTC gün. Ham JSON ve hash `historical_check/` içinde. Sağlayıcı 78,2°K / 15,600006°D hücre ve 7 m DEM yükseltisi döndürdü; [belgelenmiş varsayılan kara hücresi/yükseklik düzeltmesi](https://open-meteo.com/en/docs/historical-weather-api) uygulanır. Bu nedenle çıplak ERA5-Land grid dosyası veya hava istasyonu diye sunulmaz. Bu paketin Tortalama yaklaşımı −5,764°C, temmuz 6,440°C, yıllık GDD5 ortalaması 85,89'dur. NASA ile aynı dönemin karşılaştırması `historical_check/comparison.json` içinde; farklı grid ve referans düzeltmesi bulunduğundan fark “ölçülmüş model hatası” değildir. NASA geleceği bu seriyle sessizce düzeltilmedi. API'deki ERA5-Land yağış/radyasyon kapsamı sıcaklıktan farklı olduğundan bunlar bu bağımsız pakete alınmadı.

[Copernicus CARRA/CARRA2 resmi sayfası](https://climate.copernicus.eu/copernicus-arctic-regional-reanalysis-service) 2,5 km atmosferik yeniden analiz ve CARRA2 için pan-Arktik kapsam bildirir. İlk CARRA2 yayını Aralık 2025'tir; sayfa 40 yıllık serinin 2026 ortasında tamamlanması beklentisini anlatır. Katalog/ürün varlığı tek başına eksiksiz dosya erişimini kanıtlamaz. Bu tur CARRA/CARRA2 ham veri indirilmedi, yerel bias düzeltmesinde kullanılmadı. Tam dönem ve yükselti eşleştirilmiş yerel karşılaştırma sonraki bağımsız doğrulama adımıdır.

## Yeniden üretim ve bütünlük

```powershell
.\.venv\Scripts\python.exe scripts/ingest_north_rebuild_climate.py --workers 6
.\.venv\Scripts\python.exe scripts/ingest_north_rebuild_climate.py --offline
.\.venv\Scripts\python.exe scripts/check_north_historical_temperature.py
.\.venv\Scripts\python.exe -m pytest tests/test_north_climate_rebuild.py -q
```

`--sites longyearbyen tromso` her iki konumu tam edinir; `--limit N` yalnız erişim denemesi yapar ve hazır paket yayımlamaz. İşçi sayısı 1–8 aralığında sınırlıdır. Her dosya en fazla üç kez denenir; başarısız URL/hata saklanır. Daha önce doğrulanmış dosya tekrar indirilmez.

Denetimler: dosya SHA256, versiyon/model/SSP/üye/birim/grid, bütün Gregoryen günler ve artık günler, Tmin ≤ Tmax, sonlu değer, negatif olmayan yağış/radyasyon. Ham veri sessizce doldurulmaz, sıcaklıklar yer değiştirilmez, eksik model/yıl atılmaz. Herhangi bir eksik varsa tam iklim paketi yayımlanmaz.

Backend `get_climate_context()` sonuç kopyası döndürür; kullanıcı işlemi cache içeriğini değiştiremez. `load_climate_frame()` modeli seçebilir veya model sütunuyla üç ayrı seriyi üst üste döndürür; gizli bir sentetik ensemble günü oluşturmaz. API ham dosyaları her istekte tekrar indirmez; manifest/özet/günlük dosyalarını yerel hash ile doğrular.

## Doğrulama durumu

**23 Eylül 2026 01:00:35 +03:00**, Python 3.12.14: 21 test geçti, 0 hata/atlama, 2,649 saniye. Ham/işlenmiş dosya hashleri, tam 20 yıllık yedi bağlamın bütün üç modeli, fiziksel/birim/takvim tutarlılığı, türetilen göstergelerin günlük veriden yeniden üretimi, bozuk dosyanın reddi ve çağıranın cache'i değiştirememesi sınandı. Eski ACCESS-CM2 2035 iki SSP serisiyle ortak günler, eski float32 dönüşüm hassasiyeti içinde aynı; eski bilimsel paket korunmuştur.

Kanıt: `data/north/rebuild_climate/verification.json`, `verification-junit.xml`, `test-results.log`, `offline-rebuild.log`. Final manifest SHA256: `dbdbb8cb2ff959d6fb8574b522428fdc8d4a8f22eb4c7ecafe228c6ee5dec69b`. Çevrimdışı katalog/ham veri denetimi ve son türetme başarıyla yeniden çalıştırıldı. Veri değişmeden kaynak API'ye yeniden istek yapılmaz.

Aynı geçmiş dönemde NASA üç-model yıllık sıcaklık ortalaması −7,929°C; ayrı ERA5-Land yerel kontrolü −5,764°C. Fark −2,165°C'dir. Bu fark mekânsal/referans belirsizliğinin model-arası aralıktan ayrı olduğunu gösteren bir karşılaştırmadır; istasyon hatası tahmini veya NASA projeksiyonuna uygulanmış düzeltme değildir. Backend `local_reference_check` içinde kaynak/hash ve bu karşılaştırmayı taşır.

Bu doğrulama veri/işlem ve yazılım doğrulamasıdır; yerel ürün verimi, gerçek sera işletmesi veya geleceğin iklimi doğrulanmış sayılmaz. NASA dış senaryo kaynağıdır; GDD, don penceresi ve üretim hesabı projenin analizidir. TASE deniz profili bu iklim serisini doğrudan kalibre etmez.

Ürün entegrasyonu için ek operasyon kontrolü: `scripts/warm_north_climate_plans.py` ile historical/245, near/245, near/585, mid/585 ve late/245 gerçek iklim bağlamlarında `plan_north(..., with_sensitivity=False)` çalıştırıldı. Önceki hazırlıklar 115,827 / 119,453 / 122,484 saniyede tamamlandı. Son çeşitlilik/üretim politikası ve aday uygunluğu entegrasyonunun ardından **23 Eylül 2026 02:06:01 +03:00** tarihinde beş bağlam güncel kodla tekrar hazırlandı: hepsi `conditional`, toplam 121,547 saniye, hata çıktısı boş. Beş kaydın da `planning_code` hash'i son `backend/north_planning.py` ile (`4b21ad6f8d2dc5fbccc96e29c0704cc888f88451ca65b776749162a8ca9435e8`), `candidate_code` hash'i `195a37916dc0f29705d3fbf27b493326ad658d93eca985ca8b97036c80cae2c5` ile, iklim hash'i yukarıdaki değişmeyen manifest ile eşleşiyor. Bunun amacı disk katsayı önbelleğini hazırlamaktır, bağımsız bilimsel validasyon veya iklim testlerinin yeniden çalıştırılması değildir. Güncel süreler, kaynak/hesap kodu hashleri ve kaynak toplamları `plan-prewarm.json` içinde. Mid/245 ve late/585 ayrı entegrasyon testlerinin sorumluluğundadır.

Ek karar-özeti entegrasyon kontrolü: gerçek mid/SSP245 verisinde kaynak payları %99,12 toplanan yağış/kar erimesi, %0,88 arıtılmış deniz suyu, %0 tatlı su tahsisi; aylık kaynak dengesi kapalıdır. Üç modelin günlük tekrarlarından türeyen aylık klimatolojilerde en yüksek yedek su hacmi Mayıs/MPI-ESM1-2-HR, 0,07586 m³'tür. Seçilen depo 10 m³, modelde en yüksek doluluk 10 m³; minimum gerekli depo hesabı yapılmamıştır. Yıllık yedek gereği model ortalaması 0,20104 m³, model-yıl maksimumu MRI-ESM2-0/2041'de 5,57598 m³'tür. Bu ilk model yılı, boş depo başlangıcını da içerir; tek başına kurak yıl kanıtı değildir. Göreli yüksek fark ayrıntı verisinde kalır; eylem kartı ilk yıl su güvencesini mutlak hacimlerle anlatır. `backend/north_decision_story.py` pure özet katmanı için 17 bağımsız test geçti; gerçek sonuçtaki kaynak kapanışı, kritik ay kapsamı, depo ayrımı ve başlangıç-yılı uyarısı da kontrol edildi. Güncel saat ve kod hash'i `data/north/rebuild_climate/decision-story-smoke.json` içindedir.
