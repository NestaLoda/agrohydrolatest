# PWN v0.1 — Kartal’dan temin planı

22 Eylül 2026 web kontrolü. Satıcı sayfasındaki fiyat/stok bilgisi; telefonla stok ayırtılmadı, satın alma yapılmadı. Bu dosya önceki alışveriş PDF’sindeki EC fiyatını ve buna bağlı toplamı günceller. Cihaz yönü değişmedi: DFR0300 K1 + ESP32 + DS18B20 + encoder + yerel SD kayıt.

## 1. Önce EC kiti

| Seçenek | Görülen KDV dahil fiyat | Sonuç |
|---|---:|---|
| [Gümrük Sepeti DFR0300](https://www.gumruksepeti.com/products/dfrobot-gravity-analog-electrical-conductivity-sensor-dfr0300) | 5.500 TL | Sayfada sıfır, stok 1 ve sepete ekle. Mağazadan teslim seçeneği duyuruluyor. Prob + V2 kart + kablolar + standart çözeltilerin dahil olduğu satıcıdan teyit edilmeli. |
| [Direnc.net DFR0300 K1](https://www.direnc.net/iletkenlik-sensoru-olcer-olcum-cihazi-k1-dfrobot) | 8.124,83 TL | Güncel Türkçe sayfada sepete ekle. Eski arama kayıtlarının fiyat/stok bilgisi farklı; güncel sayfa esas alındı. Anlık elden teslim teyitsiz. |
| [Emes EMSDF2](https://www.emesrobotik.com/urun/dfrobot-gravity-elektriksel-iletkenlik-ec-sensoru-kiti-k-1-dfr0300) | 1.950 TL | Önceki listede kullanılan ilan. Aynı sitedeki diğer kit ilanıyla fiyat/içerik farkı açıklığa kavuşmadı. Kesin bütçe olarak kullanılmamalı. |
| [Emes EMSDOF](https://www.emesrobotik.com/urun/dfrobot-gravity-elektriksel-iletkenlik-ec-sensoru-kit-k-1) | 8.900 TL | Açıklama prob, V2 kart, kablo, 1413 µS/cm ve 12,88 mS/cm standartlarını sayıyor. İki Emes ilanının farkını satıcı açıklamalı. |

Robotistan’da doğrulanmış DFR0300 ürün sayfası bulunamadı. Bu, firmanın hiçbir şekilde temin edemeyeceğini kanıtlamaz. TDS/pH modülü veya tek başına yedek EC probu, tam DFR0300 kitinin yerine seçilmedi.

Gerçek alternatif [DFRobot SEN0451](https://www.dfrobot.com/product-2565.html) farklı ölçüm aralığına sahip: önerilen 100–2000 µS/cm; mevcut K1 tasarımının önerilen 1–15 mS/cm aralığıyla aynı değil. [E-komponent ilanı](https://www.e-komponent.com/gravity-industrial-analog-electrical-conductivity-meter-kit-sen0451) 15.155,71 TL, yurt dışı stok ve 7–10 iş günü belirtiyor. Bu ilk sürüm için fiyat/elden temin avantajı yok; aynı DFR0300 ile devam önerilir.

## 2. Diğer parçalar — Direnc.net sepeti

| Parça | Adet | KDV dahil fiyat / durum |
|---|---:|---|
| [ESP32-WROOM-32D geliştirme kartı](https://www.direnc.net/esp32-wroom-32d-wifi-bluetooth-gelistirme-board) | 1 | 377,76 TL; sepete ekle. Önceki 30 pin kartla pin/boyut/USB birebir varsayılmaz; usta yerleşimi eşleştirir. |
| [Su geçirmez DS18B20, 1,2 m](https://www.direnc.net/ds18b20-sicaklik-sensoru-su-gecirmez) | 1 | 58,12 TL; stok teyidi gerekli. |
| [SPI microSD modülü](https://www.direnc.net/arduino-micro-sd-kart-modulu) | 1 | 29,06 TL; sepete ekle. SD bellek kartı dahil değil. |
| [830 nokta breadboard](https://www.direnc.net/tekli-breadboard) | 1 | 55,21 TL; sepete ekle. |
| [40’lı erkek–erkek jumper](https://www.direnc.net/40-adet-erkek-erkek-jumper-20cm) | 1 paket | 49,40 TL; sepete ekle. |
| [40’lı dişi–erkek jumper](https://www.direnc.net/40-adet-disi-erkek-jumper-20cm-1) | 1 paket | 49,40 TL; sepete ekle. |
| [4,7 kΩ direnç](https://www.direnc.net/47k-14w-direnc-1) | 10 | Fiyat/ambalaj teyidi; 47 kΩ ile karıştırılmayacak. |
| [10 kΩ metal film direnç](https://www.direnc.net/10k-14w-metalfilm-direnc-paketi-100-adet-en) | İhtiyaç 4 | İlan minimum 100 adet, aramada 0,56 TL/adet. Okuldaki stok tercih. |
| [100 nF seramik](https://www.direnc.net/100nf-63v-seramik) | 10 | Minimum 10 adet; aramada 1,05 TL/adet. Başlık 100 V, URL 63 V; gerçek ürün kontrol edilir. |
| [100 µF 16 V](https://www.direnc.net/100uf16v) | 2 | Aramada 1,05 TL/adet; canlı fiyat teyidi. |

Bu tablodaki ilk altı kalemin toplamı 618,95 TL (hesap). EC, encoder, SD bellek, kablo, dirençler ve mekanik dahil değildir. Modül besleme/lojik uyumu fiziksel montajda kontrol edilecek; yapılmış devre testi yok.

## 3. Robotistan’da kalacaklar / diğer tamamlayıcılar

- [600 darbe NPN encoder](https://www.robotistan.com/doner-encoder-600d): önceki kontrolde 608,31 TL. Direnc’in [600 pulse ürünü](https://www.direnc.net/rotary-encoder-e6b2-cwz6c-600-pulse) 678,04 TL fakat kategoride tükendi; aynı model varsayılmaz. Robotistan stoğu sipariş sırasında yeniden kontrol edilmeli.
- [16 GB microSD](https://www.robotistan.com/micro-sd-kart-16gb): önceki kontrolde 374,02 TL; uygun mevcut kart varsa alınmaz.
- [Veri aktarabilen Micro-USB kablo](https://www.robotistan.com/mikro-usb-kablo-1): alınacak kartın USB soketiyle eşleştirilecek. Direnc kablo adayında tükendi görüldü.
- [20 kΩ %1 metal film](https://www.fevaris.com/urun/20k-ohm-20k-1-4w-1-metal-film-direnc): ihtiyaç 4 adet. Direnc’te doğrulanmış uygun bacaklı ürün bulunamadı; 22 kΩ açıklamasız ikame edilmez.
- Diğer mekanik/sarf, standart çözelti ve atölye kalemleri [tam bağlantılı listede](PWN_V01_LINKLI_ALISVERIS.md) korunur. Gövde/braket/teker 3D baskı; vida/pul/rulman/taşıma ipi gerçek ölçüyle alınır. Kartal’da bunların tamamını stoklayan belirli bir mağaza doğrulanmadı; yerel nalbur adı uydurulmadı.

## 4. Kartal’dan fiziksel temin

### Öncelik: Dudullu tarafı

**Gümrük Sepeti:** Necip Fazıl Mahallesi, Çorbacıyolu Caddesi No:4 Daire:1, Dudullu / Ümraniye. Telefon: 0533 141 33 13 veya 0531 681 98 76. Ürün sayfası mağazadan teslim seçeneği duyuruyor. [Resmî iletişim](https://www.gumruksepeti.com/pages/iletisim).

**Direnc.net:** Yukarı Dudullu, Eser Sokak No:7/A, 34775 Ümraniye / İstanbul. Telefon: 0850 450 47 47. [Güncel resmî iletişim](https://www.direnc.net/iletisim). Eski Maltepe adresine göre yola çıkılmamalı. Resmî adreste aynı gün bankodan satış/teslim bu araştırmada doğrulanmadı; gitmeden teyit gerekli.

### Robotistan: ofisten teslim var, Başakşehir’de

İkitelli Organize Sanayi, Atatürk Bulvarı No:108/8, Başakşehir / İstanbul. Telefon: 0850 766 0 425. [İletişim](https://www.robotistan.com/iletisim). [Teslimat koşuluna](https://www.robotistan.com/kargo-ve-teslimat) göre İstanbul teslimat adresiyle internetten sipariş/ödeme yapılıp “Ofisten Teslim Al” seçilir. Ofiste sipariş oluşturulacağı varsayılmamalı. Kartal’dan Dudullu seçeneklerine göre daha uzak coğrafi alternatif; rota/süre hesaplanmadı.

## 5. Yapacak kişiye net tedarik talimatı

“Önce Gümrük Sepeti’ne DFR0300’ın fiziksel olarak mevcut olduğunu, prob + V2 dönüştürücü kart + kabloların dahil olduğunu, iki EC standardını ve mağazadan teslimi sorun. Tam kit ve stok doğrulanırsa 5.500 TL seçeneği öncelikli. Eksikse veya bulunamazsa Direnc’te aynı DFR0300’ı teyit edin. ESP32, sıcaklık probu, SD modülü ve küçük elektronik için Direnc listesini kullanın. Encoderi Robotistan’dan tamamlayın. Aynı işlev için iki sensör/kart alınmayacak.”

Önceki 3.423,50 TL ana parça toplamı, belirsiz 1.950 TL EC ilanına dayanıyordu; güncel kesin bütçe değildir. Yeni tam cihaz toplamı, kit içeriği ve mekanik ölçüler netleşmeden verilmedi. Bu iş yalnız tedarik araştırmasıdır; uygulama testleri tekrar çalıştırılmadı, gerçek su ölçümü yapılmadı.
