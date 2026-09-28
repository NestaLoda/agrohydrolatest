# Güncel iklim referansı: 2015–2025

Bu paket 23 Eylül 2026'da edinilen **ERA5 yeniden analizini** kullanır. Kendi saha ölçümümüz, hava istasyonu gözlemi veya 2025'in tek bir günü değildir. Son tamamlanmış yıl 2025 dahil 11 yıl, 4.018 kesintisiz günlük kayıt vardır. Otuz yıllık iklim normali olarak sunulmaz.

Kaynak: [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api), [Copernicus ERA5](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview). Model açıkça `era5`; otomatik `best_match` yoktur. Günlük minimum/maksimum sıcaklık °C, toplam yağış mm su eşdeğeri, kısa dalga güneş radyasyonu MJ/m² olarak alınır. UTC günleri kullanılır. `elevation=nan` ile istatistiksel yükseklik düzeltmesi kapalıdır. Dönen kara hücresi 78,25°N / 15,75°E, model yüksekliği 217 m'dir; parselin gerçek yüksekliği veya yerel istasyon değildir.

`metadata.json` tam URL, erişim UTC'si, sınıflandırma, lisans ve ham SHA-256 değerini korur. `manifest.json` ham ve türetilmiş dosyaları hash ile bağlar. Günlük veride eksik, yinelenen gün, yanlış birim, NaN, negatif yağış/radyasyon veya Tmin>Tmax kabul edilmez. Açığı doldurarak paket hazır ilan edilmez.

`era5_1995_2025.json` ham dosyası 11.323 gün içerir: 1995–2014 bölümü aynı sağlayıcıda tarihsel kıyas için, 2015–2025 bölümü güncel üretim senaryosu için kullanılır. `longyearbyen_recent_ERA5.csv.gz` aynı üretim motoruna verilen 4.018 günlük dizidir. Çatı kar/yağış deposu, enerji ve ürün katsayıları bu gerçek günlük diziden yeniden hesaplanır; NASA üyesi kopyalanıp ERA5 diye etiketlenmez.

## Karşılaştırmanın sınırı

NASA NEX-GDDP-CMIP6 ve ERA5 farklı veri setleri ve hücrelerdir. Aynı 1995–2014 döneminde NASA üç-model ortalaması, bu ERA5 hücresine göre ortalama sıcaklıkta yaklaşık −1,65 °C, yıllık radyasyonda +1.274 MJ/m² fark gösterir. Bu nedenle **gelecek NASA planı ile güncel ERA5 planının farkı yalnız iklim değişikliğine bağlanamaz**. Veri seti/işleme farkını da içerir. Tarihsel NASA 1995–2014 planı, aynı veri seti içindeki gelecek karşılaştırması için korunur. `context.json/cross_dataset_check` farkları sayısal olarak saklar. Otomatik öteleme/bias düzeltmesi uygulanmaz.

Tek ERA5 dizisi için arayüz şemasındaki min=ortalama=max, belirsizliğin sıfır olduğu anlamına gelmez. Üç GCM belirsizliği yakın/orta/uzak gelecek ve NASA tarihsel katmanında korunur. Yağış; akış, kullanılabilir su veya tarım tahsisi değildir. Üretim çıktısı, aynı tesis/alan/ürün kanıtlarıyla **hesaplanan koşullu plan** olup günümüzdeki gerçek ekiliş değildir.

## Yeniden üretim

Depo kökünde `.venv/Scripts/python.exe -m scripts.ingest_north_recent_reference --offline` kayıtlı ham veriyi doğrular ve türetir. İlk edinim için `--offline` kaldırılır. Ağ erişimi testlerin bir parçası değildir. `tests/test_north_recent_reference.py` gerçek veri/üniteler/tarihler/hash, ayrı model kimliği, eş dönem veri seti farkı ve bozulmuş veriyle hata verme davranışını sınar.
