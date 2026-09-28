# PWN v0.1 — cihaz için bağlantılı alışveriş listesi

**22 Eylül 2026 tedarik güncellemesi:** Aşağıdaki Emes 1.950 TL ilanı, aynı sitedeki 8.900 TL kit ilanıyla fiyat/içerik açısından açıklığa kavuşmadı. Buna dayanan 3.423,50 TL toplam kesin bütçe değildir. DFR0300 için Gümrük Sepeti 5.500 TL ve Direnc.net 8.124,83 TL alternatifleri, diğer Direnc parçaları ve güncel elden teslim adresleri: [Kartal’dan tedarik planı](PWN_KARTAL_TEDARIK.md). Önceden üretilen alışveriş PDF’sinin fiyatlarını bu güncellemeyle birlikte okuyun.

22 Eylül 2026. Kullanıcı acil ürün bağlantılarını istedi. Bu liste mevcut cihazı kurma yönünü korur; ayrıntılı tank deneyinin alışverişi sonraki aşamadır. Sayfalar web/Agent Reach araştırmasında bulundu; doğrudan açılan ana sayfalardaki fiyatlar aşağıda. Satıcıyla stok/kargo/içerik teyidi yapılmadı ve sipariş verilmedi. Ürün sonuçlarından alınan küçük parça linkleri elektriksel/mekanik olarak kurulmuş paket anlamına gelmez.

Okulda/ustanın elinde varsa yeniden alınmaz. **AL:** modele göre temel alım. **KOŞULLU:** kutu içeriği/eldeki malzeme kontrolü. **ÖLÇÜYLE:** CAD veya gerçek kablo/mil ölçüsüne göre seçilecek. Aşağıdaki bağlantılar ürün sayfasıdır; yalnız proje kutusu açıkça kategori olarak işaretlidir.

## 1. Ana parçalar

| Malzeme ve ürün bağlantısı | Alınacak miktar | Not |
|---|---:|---|
| [DFRobot DFR0300 K1 TAM EC kiti](https://www.emesrobotik.com/urun/dfrobot-gravity-elektriksel-iletkenlik-ec-sensoru-kiti-k-1-dfr0300) | 1 | AL. 1.950 TL görüldü. Prob+kart+BNC/PH2.0 kabloları ve iki standardın dahil olup olmadığı teyit edilecek. |
| [ESP32 ESP-32S 30 pin](https://www.robotistan.com/esp32-esp-32s-wifi-bluetooth-dual-mode-developement-board) | 1 | AL. 415,65 TL; gerçek kart/pin kontrolü. |
| [Suya uygun DS18B20 sıcaklık probu](https://www.robotistan.com/su-gecirmez-ds18b20-dijital-isi-sensoru) | 1 | AL. 75,52 TL. |
| [600 darbe NPN optik encoder](https://www.robotistan.com/doner-encoder-600d) | 1 | AL. 608,31 TL; 5 V besleme/3,3 V pull-up tasarımı. |
| [microSD 16 GB](https://www.robotistan.com/micro-sd-kart-16gb) | 1 | AL veya mevcut uygun kart; 374,02 TL. |
| [SPI microSD modülü — Robotistan adayı](https://www.robotistan.com/mikro-sd-kart-modulu-1) | 1 | KOŞULLU. Satıcı 3,3/5 V sistem kullanımını belirtir; kart beslemesi ve SPI hatları yapacak kişi tarafından doğrulanacak. Önceki [Robodükkan adayı](https://www.robodukkan.com/micro-sd-kart-modulu-644) alternatif; **iki modül alınmayacak**. |
| [Micro-USB kablo 1,5 m](https://www.robotistan.com/mikro-usb-kablo-1) | 1 | Veri aktarımı için; mevcut veri kablosu varsa almayın. |
| [USB SD/microSD kart okuyucu](https://ugreen.com.tr/urun/ugreen-usb-c-usb-3-0-sd-tf-otg-kart-okuyucu/) | 1 | Yalnız bilgisayarda okuyucu yoksa; cihaz içi SPI modülünün yerine geçmez. |

İlk beş ana parçanın görülen toplamı **3.423,50 TL**. SD modülü/kablo/sarf/mekanik/kargo dahil değildir. Tüm cihaz toplamı gibi kullanılmaz. USB gücü ilk aşamada mevcut bilgisayardan; ayrıca powerbank satın almak zorunlu değil.

## 2. Küçük elektronik ve montaj

| Malzeme ve ürün bağlantısı | Miktar | Not |
|---|---:|---|
| [830 nokta breadboard](https://www.robodukkan.com/buyuk-boy-breadboard-830-pin-delikli-yapiskanli-model-42) | 1 | Kartın iki yanına erişim yetersizse ikinci küçük breadboard; atölyede varsa almayın. |
| [10×10 cm delikli plaket](https://www.robotistan.com/10x10-cm-delikli-pertinaks-tek-yuzlu) | 1 | Sağlam son montaj. |
| [Erkek–erkek 40 pin jumper](https://www.robotistan.com/40-pin-ayrilabilen-erkek-erkek-m-m-jumper-kablo-200-mm) | 1 paket | Yaklaşık 20 hat yeterli başlangıç, kalan yedek. |
| [Dişi–erkek 40 pin jumper](https://www.robotistan.com/40-pin-ayrilabilen-disi-erkek-m-f-jumper-kablo-200-mm) | 1 paket | Aynı. |
| [4,7 kΩ 1/4 W direnç, 10 adet](https://www.robocombo.com/47K-14W-Direnc-10-Adet%2CPR-279.html) | 1 paket | 4,7 kΩ; URL görünümündeki yazı nedeniyle 47 kΩ ile karıştırmayın, ürün başlığını kontrol edin. |
| [10 kΩ, 1/4 W, %1 metal film](https://trudyo.com/magaza/10k-1-4w-metal-film-direnc/) | 4 | Bölücü ve yedek; özellik satırında %1 aranır. |
| [20 kΩ, 1/4 W, %1 metal film](https://www.fevaris.com/urun/20k-ohm-20k-1-4w-1-metal-film-direnc) | 4 | Bölücü ve yedek. |
| [100 nF seramik, 10 adet](https://www.robotistan.com/100nf-seramik-kondansator-paketi-10-adet) | 1 paket | Montaj/gürültü stoğu. |
| [100 µF 16 V kondansatör](https://www.robotistan.com/16v-100uf-kondansator-paketi-10-adet) | 2 adet | URL paket dese de adet/paket içeriği ödeme öncesi kontrol edilmeli. |
| [Dişi header 1×40](https://www.robotistan.com/1x40-180-disi) | 2 | Sökülebilir kart bağlantısı için. |
| [Pin header seti](https://www.robotistan.com/pin-header-seti) | Gereken kadar | KOŞULLU; set büyük ve stok belirsiz. Elinizde erkek header varsa seti almayın. |
| [2 pin 5,08 mm vidalı klemens](https://www.robotistan.com/kf128v-508-2p) | 3–4 | KOŞULLU; stok teyidi. Yerleşimle eşleşmeli. |
| [17 g tüp lehim teli](https://www.robotistan.com/prolink-tup-lehim-teli-60-40-17gr-1mm) | 1 | Atölyede varsa almayın. |
| [Lehim pastası/flux](https://www.robotistan.com/pinax-lehim-pastasi) | 1 küçük kutu | Elektronik montaja uygun ürün içeriğini usta seçsin; elde varsa almayın. |
| [Isıyla daralan makaron seti](https://www.robotistan.com/renkli-makaron-seti-530-parca-isiyla-daralan-kablo) | 1 küçük set yeter | Linkteki 530 parça ihtiyaçtan fazla; mevcut atölye stoğu tercih. |
| [150 mm kablo bağı, 100 adet](https://www.robotistan.com/kucuk-kablo-bagi-paketi-100-adet-150mm) | 1 paket | Bir kısmı kullanılacak. |
| [M3 plastik yükseltici](https://www.robotistan.com/erkek-disi-m3-plastik-yukseltme-parcasi-ps-1333) | Yaklaşık 8 | ÖLÇÜYLE. Sayfa fiyatı/stok net değil; uyumlu eşdeğer alınabilir. |
| [Montaj kablosu, 24 AWG set — tedarik örneği](https://www.robotistan.com/tek-damar-montaj-kablosu-paketi-24-awg-5x20-metre) | Gerçek ihtiyaç 3–5 m | Linkte **100 m tek damarlı set** var, bizim için fazla. Kuru sabit plaket bağlantısına örnek; hareket eden sensör kablosu yerine kullanılmaz. Ustadan birkaç metre uygun kablo temin etmek daha uygun. |

Yalıtım bandı ve küçük el aletleri ustanın sarfından kullanılabilir. EC BNC prob kablosunu kesip bu kablolarla uzatmayın. Bu listede devre değerleri önceki tasarımdandır; yapılmış elektriksel doğrulama yok.

## 3. Mekanik — ölçüyü yapacak kişi eşleştirsin

| Malzeme ve ürün bağlantısı | Miktar | Not |
|---|---:|---|
| [2 mm Dyneema ip](https://www.seawolfdive.com/200-mm-dyneema-palamut-ipi) | 3–5 m | Sayfada metre seçenekleri; uygun 5 m seçilebilir. |
| [608ZZ rulman, 8×22×7](https://www.robodukkan.com/urun/608zz-rulman) | 2 | Ayrı kılavuz/baskı tekeri tasarımı için. |
| [8 mm krom mil, 250 mm](https://www.robolinkmarket.com/8mm-krom-kapli-induksiyonlu-mil-250mm) | 1 | Kılavuz tasarımına göre kesilecek. **Encoder miliyle aynı olduğu varsayılmaz.** Usta omuzlu cıvata seçerse bunu almayın. |
| [M3/M4/M5 vida–somun–pul seti](https://www.trendyol.com/acar-civata/770-adet-m3-m4-m5-vida-somun-pul-seti-p-746212988) | 20–30 bağlantılık yeter | Linkte 770 parçalık büyük set; yerel nalburdan gereken boy/adet daha ekonomik olabilir. |
| [PG7 kablo rakoru, somunlu](https://www.endustriyelmarket.com/ortac-orb01-pg-7-standart-etanj-tip-kablo-rakoru-somunlu-siyah) | 3–4 | Yalnız 3–6,5 mm kablo çapına uyarsa. BNC/konnektör geçişi ayrıca çözülür. |
| [Mandal tipi küçük işkence](https://www.hirdavatcesitleri.com/urun/troy-25054-mandal-tipi-iskence-100mm) | 2 | Yardımcı tutma; ana yük taşıyan stand bağlantısının yerine otomatik geçmez. |
| [O-ring/kauçuk conta seti](https://www.trendyol.com/oring/382-parca-o-ring-seti-hidrolik-ve-pnomatik-kaucuk-conta-seti-orkit-5a-p-1156647071) | Uygun ölçüde 1–2 yeter | Büyük set örneği; teker çapını görmeden set almak şart değil. Kılavuzda ayarlı sabit baskı seçilirse ayrıca yay alınmaz. |
| [PETG 1,75 mm filament](https://www.robotistan.com/fibromast-3d-175-mm-petg-filament-beyaz) | Eldeki yoksa 1 makara | Yazıcının filament çapı/uyumu kontrol edilir. Tasarım için yaklaşık 250–500 g ayırma önerisi vardı; CAD yapılmadan tüketim kesin değil. |
| [Proje kutuları — KATEGORİ](https://www.robotistan.com/proje-kutusu) | Baskı yerine hazır seçilirse 1 | Kutuyu basabiliyoruz; bu ek satın alma şartı değil. Gerçek kart yerleşimiyle ölçü seçilir. |

**Satın alınmayıp üretilecekler:** açık sensör başlığı, encoder braketi/göbeği, ölçüm tekeri, kılavuz/baskı braketi, kuru kutu/iç tablası. Bunların hazır üretim STL dosyaları henüz yok. Usta gerçek parçalara göre çizecek. Taşıyıcı göz/halkası ve gerekiyorsa ağırlık mevcut vida/hardware ile tasarıma göre çözülür. Sağlam destek/stand atölye imalatı veya mevcut laboratuvar standı; tek bir evrensel ürün linkiyle ölçü uyumu garanti edilemez.

## 4. İlk sensör kurulumu — kitte yoksa

| Malzeme ve ürün bağlantısı | Miktar | Not |
|---|---:|---|
| [1413 µS/cm APERA kalibrasyon çözeltisi](https://www.novatekanalitik.com.tr/1413-%ce%bcs-cm-iletkenlik-standart-kalibrasyon-cozeltisi-apera/) | 1 | Kitin içindeyse almayın; şişe hacmi/son kullanım teyidi. |
| [12,88 mS/cm APERA kalibrasyon çözeltisi](https://www.novatekanalitik.com.tr/1288-ms-cm-12880-%c2%b5s-cm-iletkenlik-standart-kalibrasyon-cozeltisi-apera/) | 1 | Aynı; pH standardıyla değiştirilmez. |
| [İki EC standardı birlikte — 2 L + 2 L alternatif](https://e-olcer.com/urun/iletkenlik-kalibrasyon-seti-2000ml-1413%c2%b5s-12-88ms/) | Yalnız alternatif | Bu hacim PoC için fazla. Üsttekilerle birlikte alınmaz; önce kit içeriği. |
| [Saf su 5 L — satıcı tedarik adayı](https://www.balmumcukimya.com/teknik-kalite-saf-su-5litre) | 1 | Sayfa teknik kalite saf su diye geçiyor; üreticinin distile durulama şartına uygunluğu/kalitesi teyit edilmeli. Laboratuvarın distile suyu varsa alınmaz. |
| [500 mL piset](https://www.oksilab.com/urun/piset-orta-boyunlu-baskili-distile-su-500-ml) | 1 | Yıkama şişesi; içine su dahil olduğu varsayılmaz. |

Kalibrasyon için temiz küçük kaplar, etiket/kalem/kağıt havlu mevcut laboratuvar sarfından kullanılabilir. Bunlar cihazın kalıcı parçaları değildir. Bağımsız EC metre ve termometre ödünç öncelikli; bu listeye pahalı yeni referans cihaz satın alma şartı eklenmedi.

## 5. Ustanın elinde yoksa araçlar

- [Multimetre örneği](https://www.robotistan.com/unit-ut-33b-dijital-multimetre) — 1; gerilim/direnç ölçebilen mevcut cihaz kullanılabilir.
- [Havya istasyonu örneği](https://www.robotistan.com/class-936-isi-ayarli-analog-havya) — 1; mevcut havya/stand yeterliyse satın alınmaz.
- Kumpas, cetvel, yan keski, kablo soyucu, pense, tornavida/alyan, gerekirse matkap/eğe: atölyenin mevcut araçları. Bu tur bunlara tek tek ürün seçilmedi; cihaz alışverişinin zorunlu yeni kalemleri değildir.
- Bilgisayar ve USB güç: mevcut bilgisayar; ayrı bilgisayar/powerbank satın alma önerilmiyor.

Detaylı kolon/stand deney kurulumu ve su/tuz/terazi/hortum malzemeleri önceki tam dosyada korunur; kullanıcı önce cihazın kendisini istediği için bu acil cihaz sepetine otomatik eklenmedi. Fiziksel temel kontrol için uygun mevcut su kabı kullanılabilir.

## Sipariş önceliği

Önce EC tam kitin elde bulunması ve gönderimi; sonra ESP32, sıcaklık probu, encoder, SD/kablo ve küçük devre malzemeleri. Mekanik ölçüye bağlı alımları yapacak kişi eşleştirir. Fiyatlar/ambalaj adetleri değişebilir; bağlantılar fiyat veya teslim garantisi değildir. Yazılım/donanım testi bu araştırmada yapılmadı.
