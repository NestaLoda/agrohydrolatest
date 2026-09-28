# Firmware: ilk uygulanacak küçük logger

**Durum:** uygulama onayı var; bu dosya firmware mimarisidir. Bu pakette derlenmiş veya donanımda denenmiş firmware iddiası yok. ADC girişi ancak öğretmenin doğruladığı analog ön devreyle anlamlıdır. [Pin planı](WIRING.md), [CSV sözleşmesi](DATA_SCHEMA.md).

## İlk kart ve modüller

Mühendislik varsayılanı ESP32-DevKitC V4 / WROOM-32E; Arduino-ESP32 veya ESP-IDF sürümü kurulum sırasında kaydedilecek. Kart değişince pin konfigürasyonu ayrı olacak. İlk modüller: config, temperature_reader, encoder_reader, conductivity_input, clock, csv_logger, status/serial. [Espressif başlangıç](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html), [ADC API](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/adc.html).

## Durum makinesi

`BOOT → SELF_CHECK → IDLE → RECORDING → FLUSH/CLOSE → IDLE`; ciddi kayıt arızası `ERROR`. Kayıt başlamadan cihaz/cast kimliği, kaynak etiketi, ham birim, encoder parametreleri ve kayıt hedefi bilinir. Kalibre edilmemiş kanal çalışabilir ama `UNCALIBRATED` niteliği kaybolmaz. Uydurulmuş default EC/salinity yok.

1. Başlatmada seri bağlantı ve yerel kayıt kontrolü.
2. Encoder geçişleri arka planda sayılır; kesme içinde dosya yazılmaz. Kontak sıçraması geçerli quadrature state transition kontrolüyle ele alınır; sayım modunun gerçek counts_per_meter değeri cetvelle bulunur.
3. Sıcaklık dönüşümü başlatılır; tamamlanmadan yeni sıcaklık varmış gibi yazılmaz. DS18B20 çözünürlüğüne göre dönüşüm süresi değişir; örnekleme zamanı kaydedilir [DS18B20 veri sayfası](https://www.analog.com/media/en/technical-documentation/data-sheets/DS18B20.pdf).
4. Analog ön devre arayüzü hazır ve güvenliyse ADC okunur. Varsayılan 12-bit raw sonuç, EC değildir. Uyarıma faz kilitli okuma gerekiyorsa sürücü bunu ayrıca sağlar; yavaş ADC okumasını rastgele AC dalgaya uygulama.
5. Başlangıçta yaklaşık saniyelik kayıt mühendislik hedefi; gerçek çevrim ve prob gecikmesi ölçülür. Sensör okuma başarısızsa boş alan + kalite bayrağı.
6. CSV satırı SD/yerel dosyaya eklenir; seri görünüm aynı satırı/debug durumunu verir. Raw veriler yeniden adlandırılarak ezilmez.
7. STOP ile dosya flush/close; güç kesmeden önce kayıt tamamlandı durumu görünür.

## İlk kullanıcı komutları önerisi

`STATUS`, `START <cast_id>`, `STOP`, `ZERO_ENCODER`, `SET_UTC <ISO8601>`; encoder sıfırlama kayıt sırasında reddedilir veya yeni cast açılır. UTC verilmediyse timestamp boş, elapsed_ms dolu; seri debug satırları CSV'den ayrı tutulur. Wi-Fi/bulut logger için şart değildir.

## Uygulama sırası ve test statüsü

Önce seri + SD dosya/kimlik; sonra sıcaklık ve encoder; sonra öğretmen onaylı EC arayüzü. Bilgisayarda header/eksik değer ve durum makinesi testleri; kart üzerinde kuru sensör testi; son olarak [tank prosedürü](TEST_PROCEDURE.md). `Derlendi`, `karta yüklendi`, `kuru masada çalıştı`, `tankta denendi` ayrı statülerdir.

SD olmazsa USB bilgisayar kaydı mümkün; `LOGGING_FALLBACK` yazılır ve bağımsız yerel logger tamamlandı denmez. Firmware içine sentetik sinyal koyulursa yalnız ayrı demo modu ve `SIMULATION_EXPLANATORY` etiketi; gerçek cihaz modunun varsayılanı yapılamaz. [E16–E18](../../docs/EVIDENCE_MAP.md).
