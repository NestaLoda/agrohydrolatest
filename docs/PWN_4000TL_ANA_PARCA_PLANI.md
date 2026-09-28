# PWN v0.1 — 4.000 TL sınırında ana elektronik önerisi

22 Eylül 2026. Kullanıcı bütçeyi yaklaşık 4.000 TL olarak sensör/kart/algılayıcılar için belirledi; mekanik, 3D baskı ve montajı okulda karşılayacak. DFR0300 zorunlu değil. Bu belge yeni bütçeye yönelik mühendislik önerisidir; satın alma ve fiziksel doğrulama yapılmadı.

## Karar önerisi

İlk gösterim için DFR0300 yerine düşük aralıklı analog TDS probu+kartı kullanılsın. Kontrollü düşük tuzluluklu suda, sıcaklık ve okulun belirleyeceği derinlik yöntemiyle derinliğe bağlı sinyal profili gösterilsin. Önceki “TDS almayın” ifadesi birebir muadil olmama durumunu gereğinden geniş ifade ediyordu: deniz suyu EC cihazının muadili değildir, ancak kapsamı daraltılmış PoC için kullanılabilir.

## Ana sepet — her birinden 1 adet

| Parça | Fiyat, KDV dahil | Kaynak |
|---|---:|---|
| Analog TDS modülü + su probu | 261,53 TL | https://www.direnc.net/arduino-tds-sivi-iletkenlik-ve-kalite-sensoru |
| ESP32-WROOM-32D | 377,76 TL | https://www.direnc.net/esp32-wroom-32d-wifi-bluetooth-gelistirme-board |
| Su geçirmez DS18B20 | 58,12 TL | https://www.direnc.net/ds18b20-sicaklik-sensoru-su-gecirmez |
| ADS1115 ADC modülü | 309,77 TL | https://www.direnc.net/ads1115-16-bit-i2c-4-kanal-modul |
| SPI microSD modülü | 29,06 TL | https://www.direnc.net/arduino-micro-sd-kart-modulu |
| 16 GB microSD bellek | 374,02 TL | https://www.robotistan.com/micro-sd-kart-16gb |

Hesaplanan toplam: 1.410,26 TL. 4.000 TL sınırına kalan: 2.589,74 TL. ADS1115 ölçüm okumasını ayrı bir ADC üzerinden yapma önerisidir; sensörün doğruluğunu 16 bit doğruluk seviyesine yükseltmez. ESP32 ADC ile de başlangıç mümkündür. Mevcut uygun SD bellek varsa 374,02 TL harcanmaz.

TDS ve ADS1115 bu tur canlı sayfalarda sepete ekle/fiyat ile kontrol edildi; diğer fiyatlar aynı gün önceki tedarik kontrolünden aktarıldı. DS18B20 stoğu, tüm ürünlerde elden teslim teyit edilecek. Sipariş verilmedi. Motor, sürücü, mekanik, sarf, kargo ve kalibrasyon çözeltileri bu toplama dahil değildir. V0.1 için motor zorunlu değil; derinlik yöntemi okul tarafından ayrıca belirlenecek; encoder satın alınmayacak. Okul motor eklerse elektromanyetik gürültü/bağlantı ayrıca ele alınacak.

## pH eklemek istersek

Direnc Arduino pH sensör modülü: 1.046,12 TL, https://www.direnc.net/arduino-ph-sensor-modulu . Sayfanın üstünde alım düğmesi görülmediği halde altında sepete ekle var; stok ve probun dahil olması teyit edilmeli. Tam kitse ana toplam + pH = 2.456,38 TL; 1.543,62 TL kalır. Tampon ve saklama çözeltileri, kablo/kargo bunun dışındadır. pH asitlik/bazlık için ayrı kanaldır, iletkenlik veya tuzluluk yerine kullanılamaz. İlk tercih pH almadan temel profili çalıştırmak; isteğe bağlı ikinci kanal olarak tutuldu. Sayfa tepki süresi <1 dakika diyor; hızlı hareket eden profilin anlık pH sonucu gibi kullanılmaz. 5 V modülün çıkış seviyesi ve iki elektrokimyasal probun etkileşimi ayrıca kontrol edilmeli.

## Ölçümü nasıl sunacağız?

Direnc TDS satıcı özelliği: 0–1000 ppm, 25°C'de ±%10 tam ölçek, 0–2,3 V analog çıkış, AC uyarma. Bu hassas deniz suyu/Arktik CTD’si değildir. Satıcının “temiz su” pazarlama ifadesi içilebilirlik kanıtı olarak kullanılmaz.

TDS modülleri iletkenliğe dayalı sinyalden çözünmüş madde tahmini üretir. DFRobot SEN0244 örnek yazılımında voltaj/sıcaklık işleme ve 0,5 dönüşüm katsayısı bulunur; bu yazılım Direnc markalı kartın birebir kalibrasyonunu kanıtlamaz. Direnc ürününde aynı eğri ve katsayı varsayılmayacak. Ham voltaj + sıcaklık + haricen belirlenen derinlik kaydedilecek; EC standardı/ödünç referans ile eşleştirme doğrulanınca “kalibre edilmiş EC tahmini” üretilecek. Doğrulanmadan EC µS/cm veya salinite PSU diye etiketlenmeyecek.

Kaynaklar:
- https://wiki.dfrobot.com/sen0244
- https://wiki.dfrobot.com/sen0244/docs/20305
- https://www.direnc.net/arduino-tds-sivi-iletkenlik-ve-kalite-sensoru

Gösterim aralık içinde kalacak; doygunlukta veri kullanılmayacak. DS18B20 sıcaklık kompanzasyonuna girdi sağlar; kompanzasyon katsayısı çözeltiye bağlı olarak doğrulanır. Ölçüm duraklarında sinyal oturması beklenecek; daha ince düşey yapı çözüldüğü iddiası fiziksel testten önce yapılmayacak. Prob kablo boyu satıcıdan öğrenilip kolon derinliği ona göre seçilecek, elektronik kart/konnektör suya indirilmeyecek. Mevcut kodda DFR0300 dönüşümü/kalibrasyonu varsa yeniden kullanılmaz; sensör türü/provenance ayrı kaydedilecek. Bu tur kod değişmedi.

Önceki DFR0300 için seçilen 12,88 mS/cm üst standart bu dar aralıklı modüle doğrudan taşınmayacak. Yeni sensörün aralığına uygun standartlar seçilecek; 1413 µS/cm adayı dahi kullanılmadan aralık ve modül yanıtı kontrol edilecek. Okuldan referans EC metre/standart ödünç almak öncelikli. Satın alınacaksa ayrı fiyat teyidi gerekli; kalan bütçe kesin çözeltı fiyatı değildir.

## Gerçek DIY alternatif

İki elektrot ve AC/bipolar uyarma + ölçüm devresiyle kendi iletkenlik hücremizi yapabiliriz. Elektrot geometrisi, hücre sabiti, polarizasyon, sıcaklık ve kalibrasyon ele alınmalı. Kaynak: https://www.analog.com/en/resources/reference-designs/circuits-from-the-lab/CN0411.html . İki metal çubuğa sürekli DC verip çıkan direnci doğrudan bilimsel EC saymak önerilmez. Hazır düşük maliyetli TDS kartı bu ilk sürüm için daha kısa yapım yolu; DIY devre için doğrulanmış şema/parça listesi bu tur üretilmedi.

## Sonraki adım

Usta ana sepetin stok/kutu içeriğini kontrol edecek. İlk fiziksel kontrolde birkaç farklı düşük iletkenlikli çözelti arasında monoton, tekrarlanabilir ve doygunlaşmayan yanıt aranacak. Sonra okulun derinlik yöntemi ve DS18B20 ile profil kaydı bağlanacak. Beklenen beceri gösterimi: kendi cihazımızdan derinliğe bağlı gerçek sensör verisi toplayıp tabakalar arasındaki farkı görselleştirmek. Çalıştığı henüz gösterilmedi; gerçek ölçüm değil, yapım hedefidir.

## Son kullanıcı düzeltmesi — encoder çıkarıldı

600 darbe encoder satın alınmayacak. Temel altı parça 1.410,26 TL. Direnc pH modülü eklenirse 2.456,38 TL (prob/kutu içeriği ve stok teyidi şart). pH isteğe bağlı ikinci ölçüm kanalı; kesin alım kararı değil. Derinlik yöntemi henüz tanımlanmadı, yapılmış gibi gösterilmeyecek.

Daha iyi belgelenmiş sensör alternatifi DFRobot SEN0244: https://www.robotsepeti.com/analog-tds-metre-su-kalite-olcum-sensoru-arduino-uyumlu-sen0244 . Bu tur sayfada 1.198,66 TL KDV dahil ve yaklaşık 7–12 İŞ günü tedarik süresi görüldü. Önceki arama kaydındaki stoktan gönderim bilgisi geçerli kabul edilmedi. 261,53 TL modül yerine alınırsa altı parça 2.347,39 TL; pH ile 3.393,51 TL. İki TDS kiti birlikte alınmaz. Üretici dokümantasyonu avantajı var; belirtilen aralık yine 0–1000 ppm, doğruluk ±%10 tam ölçek. Daha yüksek fiyatın daha yüksek ölçüm hassasiyeti sağladığı iddia edilmez. Mülakat öncesi kısa takvim için bu tedarik süresine güvenerek tek seçenek yapılmamalı.

Güncel pratik öneri: yerel ucuz TDS + ESP32 + DS18B20 + ADS1115 + SD modülü + SD bellek; ek özellik isteniyorsa stok/prob içeriği doğrulanmış pH. Deniz suyu ölçümü iddiası yok. Ek ADC sensör doğruluğunu artırmış sayılmaz. Ölçüm kartları kuru bölümde, yalnız uygun problar suya girecek. pH çıkışı 3,3 V ADC sınırına uyarlanacak, iki prob aynı suda çalışırken karşılıklı etkileşim test edilecek.

## Güncel öncelik — iletkenlik, pH sepet dışında

22 Eylül 2026: Kullanıcı TDS/EC sensöründe en çok 1.000 TL, tercihen Direnc; pH'a 1.000 TL harcamak istemiyor. Encoder ve pH güncel öneri sepetinden çıkarıldı. Önceki pH'lı toplamlar yalnız alternatif hesaplarıdır.

Yeni bulunan seçenek: DFRobot SEN0244, E-komponent'te KDV dahil 829,55 TL. https://www.e-komponent.com/dfrobot-sen0244-gravity-analog-tds-sensor-meter-for-arduino . Canlı sayfa 140 adet YURT DIŞI stok, 7–10 iş günü ve tahmini kargoya teslim 1–6 Ekim 2026 gösteriyor. Bu elden/yerel stok değildir. Üretici kitinde prob bulunur; satıcı teknik tablosu Board(s), Cable(s) dediği için prob dahil tam SEN0244 kutusu teyit edilmeli. SEN0244 üretici dokümantasyonu avantajıdır, yayınlanmış aralığı/doğruluğu ucuz seçeneğe göre daha iyi değildir (0–1000 ppm, ±%10 tam ölçek). Direnc'te 1.000 TL altında doğrulanmış daha yüksek performanslı EC/TDS kitine ulaşılamadı.

Bu 829,55 TL kit mevcut 261,53 TL TDS yerine alınırsa altı ana parça 1.978,28 TL. İkisi birlikte alınmaz. Hızlı temin gerekirse mevcut yerel TDS'li altı parça 1.410,26 TL korunur.

pH yerine ilgili ek işlev önerisi: DS3231 gerçek zaman saati, Direnc 174,35 TL: https://www.direnc.net/arduino-i2c-ds3231-real-time-clock-rtc-modulu . İnternetsiz tarih/saat kaydı için; yeni su parametresi ölçmez. Stok gösterimi üst/alt sayfada tutarsız, teyit gerekli. Uygun yedek pil ve modülün şarj devresi uyumu usta tarafından seçilecek; pil dahil varsayılmaz. SEN0244 + temel parçalar + RTC = 2.152,63 TL; yerel ucuz TDS + temel parçalar + RTC = 1.584,61 TL. Kargo/kalibrasyon/pil hariç. ADS1115 16 bit olması sensörü 16 bit doğrulukta yapmaz. Kalan bütçe yeni gereksiz kanal yerine EC standardı/referans doğrulamasına önceliklendirilecek. Gerçek su ölçümü/satın alma yok.
