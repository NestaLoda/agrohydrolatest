# Saha gözleminden üretim deseni güncellemesine

22 Eylül 2026 · U8. Çalışan yol `POST /api/pattern-field-update`; [app.py](../backend/app.py), [field.py](../backend/field.py), [planning.py](../backend/planning.py).

**Sefer öncesi model/varsayım → kaynak koşulu → üretim deseni → aynı yer/zaman/derinlik gözlemi → yalnız geçerli girdiyi değiştir → aynı motorla yeniden desen.** PWN bu iki hesap arasına fiziksel bilgi getirmek için tasarlanır. Deniz profili yıllık karasal su miktarını ölçmez.

## Bugün çalışan deney

Saha uç noktası önce beklenen ve gözlenen değerin eşleşmesini denetler. İlk desen beklenen kaynak sıcaklığıyla hesaplanır. Eşleşme geçerse gözlenen sıcaklık aynı simülasyon isteğine konur; diğer girdiler, üretim hedefleri ve kısıt tanımları korunur. Sonra ortak çok ürünlü motor tekrar çalışır. Önce/sonra desen, kaynak/yöntem tahsisi, enerji ve uygulanabilirlik karşılaştırılır; her iki koşu kaydedilir.

Şimdilik otomatik değişen değişken **kaynak suyu sıcaklığıdır**. Tuzluluk/iyonlardan yeni kimyasal uygunluk modeli, AI kalibrasyonu veya güven yüzdesi üretildiği iddia edilmez. Önceki tek marul hesabı saha güncellemesinin ana sonucu olmaktan çıkar; karşılaştırma arpa/patates/marul dâhil tüm desende yapılır.

## Gözlem kapıları

| Yol | Kabul / sınırlama |
|---|---|
| Açık sentetik örnek | `SIMULATION_EXPLANATORY`; yöntem ve karar duyarlılığını gösterir |
| Kayıtlı dış gözlem | Kaynak kimliği, korunmuş ham dosya/hash, satır seçimi, kalite OK, UTC, enlem/boylam, basınçtan derinlik, açık `in_situ` sıcaklık tanımı gerekir |
| Tank kaydı | Gerçek deniz gözlemi yerine geçmez |
| Eşleşmeyen zaman/konum/derinlik veya sıcaklık tanımı | Saha sonrası hesap yapılmaz; fark karar girdisine sokulmaz |

Başlangıç toleransları 5 km, 3 saat, 1 m olan düzenlenebilir tasarım girdileridir; uzman onaylı TASE protokolü değildir. Model beklentisi elle yazıldıysa kaynak URL'si ve kullanıcı beyanı olarak kalır; otomatik indirilmiş deniz modeli gibi sunulmaz. Eşleşen bir çift bağımsız model kalibrasyonu veya belirsizlik azalması kanıtı değildir.

## Gösterilebilir sonuç

[Kuzey örneğinde](FUTURE_NORTH_SIMULATOR.md) 10°C kaynak beklentisiyle 1 ha arpa, 0,5 ha patates ve 333,33 m² hidroponik marul; **38.084,49 kWh** ve **3.686,67 m³** hesaplanır. Aynı hedefler ve 40.000 kWh bütçesinde 5°C duyarlılık girdisi planı uygulanamaz yapar. Bu iki sayı 22 Eylül 2026 motor koşusudur, Arktik ölçümü değildir. Bütçe farklıysa plan değişmeyebilir; böyle sonuç da meşrudur.

## TASE sonrasında gerçekten sınanacak şey

İstasyonun seçilmiş kaynak/su alma koşulunu temsil ettiği ayrıca gösterilmeli. Güncel deniz profili 2035'in su sıcaklığını doğrudan ölçmez; ilgili model/arıtma varsayımını sınar ve gözlemle beslenen duyarlılık sağlar. Referans CTD, sensör kalibrasyonu, model ürününün asimilasyon durumu ve numune analizi bu ayrım için gerekir. Gözlem modelle uyuşabilir, deseni değiştirmeyebilir veya etkisi küçük kalabilir. Kaynak suyu miktarı için ayrı kara hidrolojisi/depolama/altyapı verisi gereksinimi değişmez.

Fiziksel PWN, gerçek tank ve TASE kaydı henüz yoktur. [PWN doğrulama planı](PWN_VALIDATION_PLAN.md) ve [Arktik saha planı](ARCTIC_FIELD_PLAN.md) bunların yapılacak yoludur.
