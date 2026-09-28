# Kuzey için gerçek model verisi ve saha bağlantısı

**22 Eylül 2026 / U9 güncel ek:** Etkileşim artık kalıcı Scenario Lab + sağ desen/veri/grafik alanıdır. [SIMULATOR_UX](SIMULATOR_UX.md). NASA SSP245/5852035 kaynak bağlamı eklendi; yerel hidroloji/uygunluk yerine geçmez. [Güncel durum](BUILD_STATUS.md), [su güvenliği](NORTH_WATER_SECURITY.md). Önceki aşama anlatıları bu güncel kayıtla birlikte okunur.
22 Eylül 2026. **İlk bölgesel gelecek model paketi indirildi ve işlendi.** Bu bir dış iklim modelinin çıktısından yaptığımız gösterge hesabıdır; kendi iklim modelimizi çalıştırdığımız, Arktik gözlemi aldığımız veya üretim uygunluğunu doğruladığımız anlamına gelmez.

## Gelen veri ve açık dönem değişikliği

Kaynak: Open-Meteo Climate API üzerinden tek model **EC_Earth3P_HR**. HighResMIP, CMIP6 kapsamındadır; API farklı SSP seçtirmez. Sağlayıcı zorlamayı RCP8.5'e yakın olarak tarif eder. Bu pakete SSP1-2.6/SSP5-8.5 seçimi veya ensemble etiketi verilmez. Her iki dönemde `disable_bias_correction=true`; yerel bias düzeltmesi uygulanmış ürün olarak sunulmaz. [API belgesi](https://open-meteo.com/en/docs/climate-api), [model veri atıf kaydı](https://doi.org/10.22033/ESGF/CMIP6.2323).

İstenen Longyearbyen koordinatı 78,22°K/15,65°D; API'nin döndürdüğü model hücresi **78,046875°K/15,8203125°D**. Bir bölgenin tüm alanını temsil eden ortalama veya sefer istasyonu değildir. EC-Earth3P-HR'nin yapısı [özgün model makalesinde](https://gmd.copernicus.org/articles/13/3507/2020/) açıklanır; API yanıtı deney/ensemble üyesi ve özgün veri sürümünü vermediğinden bunlar metadata'da `null` bırakıldı.

İlk istek **1995–2014 / 2031–2050** idi. Veri incelemesinde iki sorun bulundu:

1. Bias correction açık tarihsel seride **108 gün Tmin>Tmax** çıktı. Ham dosya korundu; değerler yer değiştirilmedi. İlk cevap reddedildi ve her iki dönem için düzeltmesi kapalı aynı modele geçildi. Sorunun nedeninin bias algoritması olduğu kanıtlanmadı; yalnız elde edilen veri sorunu kaydedildi.
2. 2050 tarihleri dönmesine rağmen o yılın **365 gününde üç değişken de null** çıktı. İlk eksik çıktı/snapshot saklandı. İki tam 20 yıllık dönemi karşılaştırmak için gelecek dönem açıkça **2030–2049** olarak değiştirildi; 2031–2050 tamamlanmış gösterilmez.

Son pakette her dönemde **7.305 günlük satır**, üç değişkende eksik değer sıfır ve aynı kaynak hücresi var. Kanıt: [baseline metadata](../data/north/baseline_metadata.json), [future metadata](../data/north/future_metadata.json); ham dosyaların SHA256 ve tam istek URL'leri bu kayıtlardadır. İlk başarısız erişim/kalite kontrolleri `data/north/attempts/`, önceki ham cevaplar `raw/` ve hesaplar `summary_snapshots/` altında korunur.

## İlk hesap

| Yıllık gösterge ortalaması | 1995–2014 | 2030–2049 | Fark |
|---|---:|---:|---:|
| GDD5, °C·gün | 17,9300 | 48,1425 | +30,2125 |
| En uzun kesintisiz Tmin>0 dönemi, gün | 39,55 | 69,70 | +30,15 |
| Toplam yağış, mm/yıl | 496,305 | 571,845 | +75,540 |

Hesap kaynağı [summary.json](../data/north/summary.json); yıllık sonuçlar [annual_metrics.csv](../data/north/annual_metrics.csv), günlük işlenmiş veri [daily.csv](../data/north/daily.csv).

GDD5 = günlük `max((Tmin+Tmax)/2−5,0)` toplamı. Don olmayan pencere her takvim yılı içindeki en uzun kesintisiz `Tmin>0` dizisi; don günü toplamının tersini kullanmıyoruz. Dönem karşılaştırması 20 yıllık ortalamaların farkıdır. Yıllar arası min–max aralığı güven aralığı veya model belirsizliği değildir. Eksik yılı sıfır doldurup ortalamaya katma yok.

**Jüriye doğru ifade:** “Longyearbyen çevresindeki tek bir model hücresinde, aynı iklim modeliyle geçmiş ve yakın gelecek dönemlerini karşılaştırdık. Don olmayan pencere uzuyor; şimdi bunun su, zemin ve enerji koşullarında uygulanabilir üretime dönüşüp dönüşmediğini ayrı değerlendiriyoruz.” Tek modelin bu sonucu bütün kuzeye genellenmez; GDD5 bir ürünün doğrulanmış eşik testi değildir. Yağış karı da içerir; depolanmış veya çekilebilir sulama suyu değildir. [Değişken tanımları](https://open-meteo.com/en/docs/climate-api#daily-parameter-definition).

## Arayüz / veri sözleşmesi

`data/north/summary.json`: `status`, `source_kind=EXTERNAL_CLIMATE_MODEL`, `model`, `scenario_label`, `ssp=null`, `bias_correction`, `requested_future_period`, `period_adjustment_reason`, `baseline`, `future`, `delta`, `annual_metrics`, `provenance`, `limitations`, `marine_observations_available=false`.

`baseline`/`future` içinde gerçek `period`, tarihler, `years`, `complete_years`, `complete`, `mean_annual_gdd5_degree_days`, `mean_annual_frost_free_run_days`, `mean_annual_precipitation_mm` ve her göstergenin yıllık min–max alanı bulunur. `delta` aynı üç gösterge adını kullanır. Arayüz sabit 2050/SSP metni yazmamalı; JSON'un gerçek dönem/model/etiketini göstermeli. `status=incomplete` veya null ortalama olduğunda hazır sonuç kartı üretilmez.

`scripts/ingest_north.py` ilk kez çevrimiçi alır; sonraki çalıştırmada ham hash'i doğrulayarak çevrimdışı yeniden hesaplar. `--refresh` eski raw/metadata/summary snapshot'larının üzerine yazmaz; yeni snapshot ve güncel gösterim dosyası oluşturur. Atıf: Open-Meteo, CMIP6, EC-Earth Consortium; lisans kaydı metadata'dadır. [API atıf koşulları](https://open-meteo.com/en/docs/climate-api#citation-acknowledgement).

## Saha neden ayrı ve hâlâ gerekli?

Yukarıdaki paket **kara üstündeki hava sıcaklığı ve yağışın iklim bağlamıdır**. PWN'nin hedefi ise izinli sefer istasyonunda **su kolonunun gerçek C/T/p durumu**. Hava sıcaklığını deniz suyu sıcaklığı diye arıtma hesabına taşımıyoruz. Mevcut veriler gelecek problemini kurar; sefer ölçümü farklı bir model–gözlem sorusunu sınar. [Bilimsel mimari](SCIENTIFIC_ARCHITECTURE.md), [saha planı](ARCTIC_FIELD_PLAN.md).

Planlanan somut zincir:

1. **Beklenti:** istasyona ait deniz modeli profilini ürün/sürüm, üretim ve geçerlilik zamanı, koordinat, derinlik, birimler ve raw hash ile sakla. Sonradan alınmış reanalysis, önceden yapılmış tahmin diye gösterilmez. İklim modelinin günlük hava sıcaklığı bu baseline değildir.
2. **Gözlem:** izinli cast'te kalibrasyonlu PWN C/T/p, GPS/UTC ve varsa referans CTD; cast/sensör/sample kimliği, ölçüm belirsizliği ve kalite bayrakları. Şu anda böyle bir Arktik kaydımız yok.
3. **Eşleştirme:** gerçek zaman ve koordinat farkı, gemi GPS'i–sualtı probu farkı, düşey aralık ve derinlik referansı kaydedilir. Modelin potansiyel sıcaklığı ile sensörün yerinde sıcaklığı gibi farklı değişkenler doğrudan çıkarılmaz; gerekli geçerli dönüşüm ayrı kaydedilir. °C, dbar, m, mS/cm ve salinity tanımları eşleştirilir. Uyumsuz eşleşme reddedilir; toleranslar uzmanla seçilir. [TEOS-10 GSW](https://teos-10.org/pubs/gsw/html/gsw_contents.html), [Copernicus Arctic ürün tanımı](https://data.marine.copernicus.eu/product/ARCTIC_MULTIYEAR_PHY_002_003/description).
4. **Fark:** aynı değişken/derinlik/zamanda `observed−modelled` residual hesapla; ölçüm ve temsil farkını model hatası diye otomatik adlandırma. Tek profilden tüm deniz modelini düzelttiğimiz sonucu çıkmaz.
5. **Desteklenen karar etkisi:** yalnız gözlem ilgili kıyısal kaynak suyunu temsil ediyorsa, gerçek **su sıcaklığının** mevcut kaynaklı sıcaklık–arıtma enerji duyarlılığındaki etkisini incele. İlk hesap yalnız kaynak çalışmanın 5–18°C aralığında tanımlı; daha soğuk Arktik su için `veri yetersiz`. Tuzluluk residual'ı kaydedilebilir fakat doğrulanmış bir tuzluluk–enerji fonksiyonu yokken enerji katsayısı üretilmez. [Çalışan modelin sınırları](MODEL_METHODS.md).

Bu zincir karasal yıllık su arzını, çekilebilir hacmi, tarla verimini veya suyun buzul kökenini doğrudan vermez. Kaynak-temsil bağı yoksa sonuç **deniz modeli karşılaştırması ve yöntem gösterimi** olarak kalır. Mevcut kuzey iklim paketinden, simülasyondan veya planlanan gözlem satırından gerçek deniz residual'ı üretilmez.
