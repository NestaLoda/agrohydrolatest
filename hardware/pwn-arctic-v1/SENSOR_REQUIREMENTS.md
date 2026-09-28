# Arctic v1 sensör gereksinimleri

Bu liste kesin sensör seçimi değildir. Önce gözlemlemek istediğimiz anlamlı değişim ve sefer koşulu, sonra katalog ve referans testi gelir. Katalog çözünürlüğü toplam cihaz doğruluğu sayılmaz [E13/E16](../../docs/EVIDENCE_MAP.md).

| Kanal | İstenen işlev | Uzmanla belirlenecek |
|---|---|---|
| Conductivity | Deniz suyu kaynak özelliği ve tabakalaşma | Aralık, doğruluk, drift, soğuk sınırı, hücre akışı/tepki |
| Temperature | Su kolonunu ve C dönüşümünü birlikte değerlendirme | Doğruluk, tepki, C ile zaman/yer uyumu |
| Pressure | Gerçek ölçüm derinliğinin dayanağı | Maksimum derinlik, yüzey referansı, basınç birimi ve derinlik dönüşümü |
| Turbidity | Yalnız araştırma sorusuna ek bilgi varsa | Gereklilik, kalibrasyon, sensör yerleşimi; çekirdek şart değil |
| GPS/UTC | Profilin zaman/yer kimliği | Gemi/deck erişimi, saat sapması ve eşleştirme |
| Kayıt/güç | İnternetsiz ham veri | Tüketim, soğukta pil, bellek ve bakım |

C/T/p ham verisi ve kalibrasyon kimliği saklanır. Practical salinity türetmek için doğru birim ve geçerli dönüşüm kullanılır; [GSW SP_from_C](https://teos-10.org/pubs/gsw/html/gsw_SP_from_C.html). Tuzluluk tek başına suyun kaynağını, arıtma sonrası bütün kullanım uygunluğunu veya yıllık miktarı vermez.

Model/marka, salinity accuracy, basınç rating ve çalışma derinliği bu dosyada bilerek sayılandırılmıyor; bunlar mevcut somut uzman/gemi bilgisi olmadan verilemez. [Görüşme gündemi](../../docs/RESEARCHER_OUTREACH.md), [numune/arıtma dayanağı E06/E10](../../docs/EVIDENCE_MAP.md).
