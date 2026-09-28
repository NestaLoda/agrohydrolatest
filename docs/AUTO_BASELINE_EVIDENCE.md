# Otomatik kuzey başlangıcı: neyi gerçekten hesaplayabiliriz?

22 Eylül 2026 · U12. Yeni parametre kaydı [auto_baseline_parameters.json](../data/auto_baseline_parameters.json). Mevcut sabitlenmiş veri dosyaları değiştirilmedi. Amaç, hazır gerçek girdilerden hesap yapmak; elle doldurulmuş bir senaryoya “otomatik kaynak verisi” etiketi koymak değil.

## Otomatik hesaplanabilecekler

1. NASA günlük Tmin/Tmax/yağış + enlem/tarih → sıcaklık ortalaması, don göstergesi, yetişme penceresi ve **araştırma amaçlı Hargreaves ET0**.
2. Kaynaklı ürün takvimi/Kc → seçilen dönemde ETc; kalibre edilmemiş kuzey su gereksinimi tahmini olarak.
3. Ürün bazında kaynaklı tarihsel sıcaklık/mevsim zarfı → açıklanabilir ilk aday taraması. Geçmek yerel uygunluk onayı değildir.
4. Yerel su arzı yoksa otomatik **gereken kaynak miktarı**, birim kapasite gereksinimi veya açık dış-referans teknoloji karşılaştırması. Kullanılabilir su varmış gibi sahte m³ üretmeye gerek yok.

## Hargreaves: birim ve kutup sınırı

FAO-56 Eq52: `ET0 = 0.0023 × (Tmean + 17.8) × sqrt(Tmax − Tmin) × Ra_mm`. Astronomik Ra MJ/m²/gün hesaplanırsa **0.408 ile bir kez çevrilir**. Güneş sabiti 0.0820 MJ/m²/dakikadır. [FAO-56 Bölüm3, Eq20–25 ve52](https://www.fao.org/4/X0490E/x0490e07.htm).

Kaynak bu eksik-meteoroloji yaklaşımının yeni bölgede Penman–Monteith ile kontrol/kalibrasyonunu ister; yüksek rüzgâr ve yüksek nem sapma yaratabilir. Kutupta arccos girdisini [-1,1]'e sınırlayarak 24 saat gündüz/geceyi ele almak uygulama seçimidir. Donlu dönemde hesaplanan sıfır değeri kar/buz süblimleşmesi veya bütün hidrolojik kayıpların sıfır olduğu anlamına gelmez. İlk kullanım büyüme dönemi gereksinim taramasıdır. Negatif/nonfinite sıcaklık farkı reddedilir; negatif ET0 sınırlandırılıyorsa bu işlem ayrıca kaydedilir. Gerçek yüzey ışınımı/nem/rüzgâr hazır olduğunda Penman–Monteith yolu tercih edilir.

## Termal aday taraması

| Ürün | Kaynaklı tür zarfı | Dönem | Kullanım |
|---|---|---|---|
| Arpa | Mutlak 2–40°C; optimum15–20°C |90–240 gün |Tarihsel tür zarfı; çeşit olgunlaşması veya günlük don toleransı değil. |
| Patates |Mutlak7–30°C; optimum15–25°C |90–160 gün |Tarihsel zarf. FAO ayrıca10°C altında yumru gelişiminin kuvvetle baskılandığını belirtir;7 ve10 farklı anlamdadır. |

Kaynaklar: [FAO ECOCROP arpa](https://ecocrop.apps.fao.org/ecocrop/srv/en/dataSheet?id=1232), [patates](https://ecocrop.apps.fao.org/ecocrop/srv/en/dataSheet?id=1971), [FAO patates rehberi](https://www.fao.org/4/i0500e/i0500e.pdf). ECOCROP yaklaşık2015'te sonlandırılmış tarihsel veritabanıdır; güncel çeşit deneyi değildir. [FAO durum açıklaması](https://www.fao.org/geospatial/data-and-tools/data-portals/ecocrop/).

Önerilen açık uygulama kuralı: adayın minimum döngü süresindeki hareketli sıcaklık ortalamasını zarfla karşılaştır; en iyi pencereyi ve başarısızlığı göster. Bu hareketli-pencere kuralı **bizim tarama tasarımımızdır**, FAO tarafından yerel doğrulanmış algoritma değildir. Don/gelişme evresi, GDD, fotoperiyot, zemin ve sulama ayrıca bilinmiyorsa `screening_pass_not_validated` verilir; `climate_suitable=true` ve `soil_suitable=true` otomatik verilmez.

Yerel2035 NASA serisinden hesap: en yüksek90gün ortalaması SSP245'te3,37°C, SSP585'te4,18°C; ortalama≥10°C gün sayısı ikisinde0. En uzun Tmin>0 kesintisiz dizisi45/47gün. Bunlar bir model yılının tarama göstergeleridir;2060sonucu veya kesin ürün imkânsızlığı değil. Patatesin7°C zarfına uyan90gün penceresi yoktur. Arpanın2°C alt zarfını geçmek olgun tane üretimini kanıtlamaz. Kaynak: [mevcut NASA noktaCSV](../data/north/u9_acquisition/daily_point_2035.csv).

## Su gereği, su arzı değil

FAO kaba sezon aralıkları arpa450–650mm, patates500–700mm'dir; iklime bağlı toplam gereksinim için bağlam sunar. Kuzey ETc hesabına zorunlu alt sınır veya sulama tahsisi olarak konmaz. [FAO Tablo14](https://www.fao.org/4/s2022e/s2022e07.htm).

Günlük NASA yağışı katı+sıvı toplamıdır. Donlu gün yağışını aynı gün bitkinin kök suyuna eklemek yanıltır. Kar/rain partition, erime, akış, depo ve erişim yokken otomatik sulama arzı üretilemez. Basit üst-sınır karşılaştırması gerekiyorsa `max(ETc−P,0)` açıkça depolamasız, bütünP'yi kullanılabilir sayan iyimser yaklaşım olarak etiketlenir; tercih edilen ilk çıktı ETc gereksinimi ve ayrı bilinmeyen tahsistir.

## Kontrollü marul için doğrudan kaynaklı teknoloji örneği

[Barbosa2015](https://doi.org/10.3390/ijerph120606879) yıllık Arizona mühendislik karşılaştırmasında hidroponik41kg/m²/yıl;20L/kg ve90.000kJ/kg, yani0,020m³/kg ve25kWh/kg verir. Mevcut kaynak kaydı `data/literature_parameters.json` içindedir. Bu değerler **dış-referans teknoloji senaryosu** olarak otomatik gelebilir; Arctic yerel sera modeli olmaz. PMC tam sayfası bu tur tarayıcı kontrolü verdi; önceki doğrulanmış tablo kaydı korundu.

Yıllık41kg/m² katsayısını75günlük marul veya130günlük karışık tarla dönemiyle birleştirmeyin. Ya açık yıllık teknoloji referansı gösterin ya çevrim üretkenliği ölçeklemesini yeni varsayım olarak kaydedin. Yerel elektrik/ısı/LED/nem profili olmadan Arctic kWh/kg aralığı uydurulamaz.

## Karar sınırı

Kaynaklar otomatik yüklenebilir ve bilinenlerden gereksinim/eleme üretilebilir. Verinin olmadığı yerde kaynak kapasitesini keşfeden gerçek yerel optimum hesaplanamaz; bunun yerine gereken kapasiteyi hesaplamak kullanıcıyı30boşalana zorlamadan fayda sağlar. Araştırma başlangıcı ile onaylı yerel üretim önerisi arasında görünür ayrım korunmalıdır.
