# PWN v0.1 bağlantı planı

**Güncel kitli v0.1 düzeltmesi — 22 Eylül 2026:** [Tam malzeme listesi](../../docs/PWN_V01_TAM_MALZEME_LISTESI.md) önceliklidir. Aşağıdaki tablo eski DevKitC örneğidir; önerilen 30 pin ESP-32S fiziksel olarak doğrulanmış değildir. Seçilen encoder pasif kontak değildir: E38S6G5-600BG24N için 5 V besleme ve A/B hatlarında 3,3 V pull-up kullanılacak; aşağıdaki encoder `3V3` besleme örneği bu ürüne uygulanmaz. EC ölçüm zincirinde DFR0300 K1 kit, DIY elektrot/AC devresinin yerini alır. Önerilen OUT–10k–ADC–20k–GND bölücüsü ve yazılım ölçeği ölçülerek doğrulanacak. microSD modülü besleme/lojik uyumu henüz açık; bu belge tak-çalıştır devre iddiası değildir.

**Seçilen örnek konfigürasyon:** ESP32-DevKitC V4 + ESP32-WROOM-32E. Kartın fiziksel modeli bilinmiyor; bu tablo ancak kart üstündeki GPIO etiketleri ve şeması eşleşiyorsa kullanılacak. Pinler GPIO numarasıdır, konnektörde sıra numarası değildir. Deneyap/S3/C3 için yeniden eşleştir [kart belgesi](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html), [modül pin tablosu](https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.pdf).

## Kuru masadaki pin seçimi

| İşlev | Seçilen GPIO/hat | Karşı uç | Not |
|---|---|---|---|
| Sıcaklık 1-Wire | GPIO27 | DS18B20 DQ | Başlangıçta 4,7 kΩ DQ–3V3 pull-up; 3 telli harici besleme |
| Sıcaklık beslemesi | 3V3 / GND | Prob VDD / GND | Kablo rengine güvenme; satıcı uç tanımını teyit |
| Encoder A | GPIO32 | A/CLK | Pasif kontakta pull-up; elektronik modülde 3,3 V çıkış |
| Encoder B | GPIO33 | B/DT | A ile aynı referans; yön yazılımda kontrol |
| Encoder ortak | GND | Common/GND | VCC yalnız gerekiyorsa modül belgesine göre 3V3 |
| Analog ölçüm girişi | GPIO34 / ADC1_CH6 | Şartlandırılmış ön devre OUT | **Elektrota doğrudan bağlanmaz**; salt giriş pini |
| SPI SD saat | GPIO18 | SCK | Yalnız uyumlu modül |
| SPI SD giriş | GPIO19 | MISO | 3,3 V lojik |
| SPI SD çıkış | GPIO23 | MOSI | 3,3 V lojik |
| SPI SD seçim | GPIO21 | CS | Firmware bu özel CS seçimini açık kullanmalı |
| Seri veri | Kartın USB portu | Bilgisayar | GPIO1/3 harici sensöre ayrılmadı |
| İsteğe bağlı kayıt butonu | GPIO25 ve GND | Normalde açık buton | Pull-up + debounce; zorunlu değil |

Bu GPIO dağılımı proje mühendislik kararıdır. Üretici belgeleri pin işlevlerini doğrular; PWN donanımının çalıştığını doğrulamaz. Sıcaklık bağlantısı [DS18B20 veri sayfasındaki harici besleme düzenine](https://www.analog.com/media/en/technical-documentation/data-sheets/DS18B20.pdf) dayanır. Çip özellikleri paketli probun su/basınç dayanımı değildir.

## Analog giriş sınırı

Ön devre çıkışı ADC'nin seçilen attenuation ile ölçebildiği aralıkta kalmalı; rail'e yakın doyma kontrol edilmeli. Öğretmen çıkışı multimetre/osiloskopla doğrulamadan GPIO34'e bağlamaz. ESP32 pinine 5 V veya negatif sinyal verilmez. `analogRead` ham ADC sayısıdır; `analogReadMilliVolts` da EC değildir. [Espressif ADC belgesi](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/adc.html).

DIY hücrenin AC sürücüsü, akım sınırlama ve ölçüm/uyarım eşzamanlaması **bu tabloda hazır devre değildir**; [CONDUCTIVITY_CELL.md](CONDUCTIVITY_CELL.md) öğretmenin kararını tanımlar. Harici ADC seçilirse pin planı ve veri birimi ayrıca sürümlenir.

## Bağlantı sırası

1. Enerji kapalıyken kart modeli, tüm GND bağlantıları ve modül beslemelerini teyit et.
2. Yalnız USB ile karta enerji ver; sıcaklık probunu ve encoder'ı ayrı ayrı kuru masada dene.
3. SD modülünün besleme ve lojik seviyesini kendi ürün belgesinden doğrula. “Arduino modülü” olması 3,3 V uyum kanıtı değildir.
4. Kayıt dosyası aç/kapat/geri okuma kontrolünü yap.
5. Öğretmen onaylı EC ön devresinin çıkışını önce su dışında test et, sonra ADC'ye bağla.
6. Sensör başlığını kolona indir; kart, ön devre, batarya, SD ve USB bağlantıları kuru kalır.

DevKitC için USB/5V-header/3V3-header besleme yollarından **yalnız biri** kullanılır; üreticinin uyarısıdır [kart güç seçenekleri](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html#power-supply-options). Harici ön devrenin ek beslemesi gerekiyorsa ortak toprak/geri besleme düzenini öğretmen kontrol eder. Bu paket şebeke devresi tarif etmez.

## Hızlı arıza tablosu

| Sorun | İlk kontrol |
|---|---|
| Sıcaklık yok | Uç işlevi, pull-up, ortak GND, dönüşüm tamamlanması; hata kodunu ölçüm sanma |
| Encoder yönü ters | Pozitif iniş tanımı ve A/B yönü; değişikliği metadata'ya yaz |
| Encoder zıplıyor | Kontak sıçraması, gevşek bağlantı, mekanik kayma; debounce/state decoding |
| SD açılamıyor | Besleme/lojik, CS21 ayarı, SPI bağlantısı, kart; USB yedek kaydı ayrı statü |
| ADC sürekli uç değerde | Ön devre aralığı veya bağlantı; EC sonucu üretmeyi durdur |

Kart değişikliği kayıt kimliği ve firmware pin konfigürasyonunda görünür olacak; fiziksel test notu olmadan “bağlantı doğrulandı” yazılmaz.
