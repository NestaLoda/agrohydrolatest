# PWN v0.1 — Direnc.net ağırlıklı satın alma listesi

22 Eylül 2026. Kullanıcının seçtiği senaryo: Direnc.net’te bulunanlar oradan alınacak; DFR0300 dahil. Fiyatlar aynı gün yapılan önceki web kontrolünden aktarılmıştır, bu listede yeniden stok sorgulanmadı. Sipariş verilmedi. KDV dahil görülen fiyatlar; kargo dahil değil.

## A — Direnc.net ana sepet

| Parça / ürün bağlantısı | Miktar | Görülen tutar |
|---|---:|---:|
| [DFRobot DFR0300 K1 EC tam kit](https://www.direnc.net/iletkenlik-sensoru-olcer-olcum-cihazi-k1-dfrobot) | 1 | 8.124,83 TL |
| [ESP32-WROOM-32D geliştirme kartı](https://www.direnc.net/esp32-wroom-32d-wifi-bluetooth-gelistirme-board) | 1 | 377,76 TL |
| [Su geçirmez DS18B20 sıcaklık probu](https://www.direnc.net/ds18b20-sicaklik-sensoru-su-gecirmez) | 1 | 58,12 TL — stok teyidi |
| [SPI microSD modülü](https://www.direnc.net/arduino-micro-sd-kart-modulu) | 1 | 29,06 TL |
| [830 nokta breadboard](https://www.direnc.net/tekli-breadboard) | 1 | 55,21 TL |
| [40’lı erkek–erkek jumper](https://www.direnc.net/40-adet-erkek-erkek-jumper-20cm) | 1 paket | 49,40 TL |
| [40’lı dişi–erkek jumper](https://www.direnc.net/40-adet-disi-erkek-jumper-20cm-1) | 1 paket | 49,40 TL |

**Bu 7 kalem: 8.743,78 TL.** Tam cihaz toplamı değildir. DS18B20 dışındaki ürünlerde önceki kontrolde sepete ekle görüldü; mağazada anlık teslim garantisi yok.

## B — Direnc.net küçük elektronik (ustanın elinde yoksa)

| Parça / bağlantı | Gerekli miktar | Satın alma notu |
|---|---:|---|
| [4,7 kΩ 1/4 W direnç](https://www.direnc.net/47k-14w-direnc-1) | 10 adet | Birim fiyat/ambalaj teyidi; 47 kΩ alınmayacak. |
| [10 kΩ metal film direnç](https://www.direnc.net/10k-14w-metalfilm-direnc-paketi-100-adet-en) | 4 adet | İlanda minimum 100 adet. Okulda varsa kullanın; aramada 0,56 TL/adet, 100 adet yaklaşık 56 TL. |
| [100 nF seramik kondansatör](https://www.direnc.net/100nf-63v-seramik) | 10 adet | Minimum 10; arama fiyatı 1,05 TL/adet, yaklaşık 10,50 TL. |
| [100 µF 16 V kondansatör](https://www.direnc.net/100uf16v) | 2 adet | Arama fiyatı 1,05 TL/adet, yaklaşık 2,10 TL. |

Bu bölümün fiyatları A toplamına dahil değildir. Arama fiyatları ödeme öncesi kontrol edilecek.

## C — Başka yerden tamamlanacaklar

| Parça / bağlantı | Miktar | Not |
|---|---:|---|
| [Robotistan 600 darbe NPN encoder](https://www.robotistan.com/doner-encoder-600d) | 1 | Önceki fiyat 608,31 TL. Direnc encoder kategoride tükendi; Robotistan stoğu yeniden kontrol edilecek. |
| [Robotistan 16 GB microSD bellek](https://www.robotistan.com/micro-sd-kart-16gb) | 1 | Önceki fiyat 374,02 TL. Uygun mevcut kart varsa alınmaz. |
| [Robotistan USB veri kablosu adayı](https://www.robotistan.com/mikro-usb-kablo-1) | 1 | ESP32’nin gerçek USB soketine uygun seçilecek. Mevcut kablo kullanılabilir. |
| [Fevaris 20 kΩ %1 metal film direnç](https://www.fevaris.com/urun/20k-ohm-20k-1-4w-1-metal-film-direnc) | 4 adet | Direnc’te uygun ürün doğrulanamadı; ustanın stoğunda varsa kullanılır. |

A sepeti + encoder + yeni 16 GB kart = **9.726,11 TL** hesaplanan ara toplam. Küçük elektronik, USB kablo, sarf, mekanik, kalibrasyon eksiği ve kargo dahil değil. SD modülü ile SD bellek farklı parçalardır; ikisi de gerekir.

## D — Ustaya / atölyeye verilecek tamamlayıcı kontrol listesi

Elde varsa tekrar alınmayacak. Bu kalemler için yeni Direnc ürün/stok doğrulaması yapılmadı; ayrıntılı mevcut ürün bağlantıları docs/PWN_V01_LINKLI_ALISVERIS.md içindedir.

- 1 adet 10×10 cm delikli plaket; 2 adet 1×40 dişi header; gereken erkek header; 3–4 adet 2 pin vidalı klemens.
- Yaklaşık 3–5 m montaj kablosu; lehim, elektronik flux, makaron, yalıtım bandı, kablo bağları; yaklaşık 8 adet M3 yükseltici.
- 3–5 m yaklaşık 2 mm taşıyıcı ip; 2 adet 608ZZ rulman; tasarıma göre 8 mm mil veya omuzlu cıvata; uygun boy M3/M4/M5 vida-somun-pul. Encoder milinin ölçüsü ayrı kontrol edilir.
- Gerçek kablo çapına uyan 3–4 rakor; teker için uygun kauçuk/O-ring; sağlam destek/stand ve bağlantıları. Mekanik parçaların nihai ölçüsünü yapacak kişi belirleyecek.
- 3D baskı: sensör başlığı, encoder braketi, ölçüm tekeri, baskı/kılavuz parçası, kuru elektronik kutusu/iç tablası. Mevcut yazıcı/filament kullanılacak; hazır STL henüz yok.
- Kitte yoksa 1413 µS/cm ve 12,88 mS/cm EC standartları; durulama için distile su, piset ve temiz küçük kaplar.
- Atölyede multimetre, havya, kumpas/cetvel ve el aletleri; mevcut bilgisayar ve USB güç. Ayrı powerbank zorunlu değil.

## Satıcıya ve yapacak kişiye tek not

DFR0300’ın prob + ölçüm kartı + bağlantı kablolarını ve iki kalibrasyon standardını içerdiğini kontrol edin. ESP32 kartının pinleri/USB türü/kutu ölçüsünü alınan ürüne göre eşleştirin. EC analog çıkışı doğrudan ESP32 ADC’ye bağlanmayacak; önceki gerilim bölücü tasarımı ve encoder lojik seviyeleri usta tarafından kontrol edilecek. Bu liste cihaz için; tank deneyinin ayrı alışverişi eklenmedi. Gerçek donanım testi yapılmış değildir.

Direnc.net güncel resmî adres: Yukarı Dudullu, Eser Sokak No:7/A, Ümraniye/İstanbul. Telefon: 0850 450 47 47. Gitmeden stok ve elden teslim teyidi: https://www.direnc.net/iletisim .
