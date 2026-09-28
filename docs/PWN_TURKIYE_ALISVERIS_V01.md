# Türkiye'den teminle sunumda gösterilecek PWN v0.1

**Güncel tam liste:** [PWN_V01_TAM_MALZEME_LISTESI.md](PWN_V01_TAM_MALZEME_LISTESI.md). Aşağıdaki liste ilk fiyat/çekirdek araştırmasıdır; tam montaj sepeti değildir. Tam listede kalibrasyon, küçük elektronik, mekanik bağlantılar ve araçlar ayrı sayılmıştır. Kullanıcı 3D yazıcı erişimini doğruladı. Yaklaşık 10 cm kolon önerisi yerine tam listede daha rahat 15–20 cm başlangıç genişliği önerilir; gerçek başlık görülmeden ölçü kesinleşmez. 5–6 bin TL tüm malzemelerin sıfırdan satın alma toplamı değildir.

22 Eylül 2026. **Önerilen yapım ve alışveriş listesi.** Hedef, okulda kontrollü tankta çalışan kendi kayıt/derinlik/profil sistemimizi kurmak. Hazır EC probu ve ölçüm elektroniği kullanacağız; mekanik taşıyıcı, logger firmware'i, veri akışı, deney ve analiz bizim sistemimiz olacak. Bu öneri kullanıcıya sunuldu; sipariş verilmedi, donanım henüz kurulmadı.

## Tek önerilen çekirdek

**DFRobot DFR0300 K1 EC kiti + ESP32 30pin + suya uygun DS18B20 + optik encoder + microSD.**

| Parça | Adet | Görev | Türkiye sayfasındaki fiyat |
|---|---:|---|---:|
| [DFRobot DFR0300 K1 tam kit — Emes Robotik](https://www.emesrobotik.com/urun/dfrobot-gravity-elektriksel-iletkenlik-ec-sensoru-kiti-k-1-dfr0300) | 1 | İletkenlik probu ve hazır AC ölçüm kartı | 1.950,00 TL |
| [ESP32 ESP-32S 30pin — Robotistan](https://www.robotistan.com/esp32-esp-32s-wifi-bluetooth-dual-mode-developement-board) | 1 | Sensörler, sayım, CSV kayıt | 415,65 TL |
| [Suya uygun paket DS18B20 — Robotistan](https://www.robotistan.com/su-gecirmez-ds18b20-dijital-isi-sensoru) | 1 | Sıcaklık | 75,52 TL |
| [600 darbeli NPN optik encoder — Robotistan](https://www.robotistan.com/doner-encoder-600d) | 1 | Ölçüm tekeri dönüşü / tankta mesafe | 608,31 TL |
| [16GB microSD — Robotistan](https://www.robotistan.com/micro-sd-kart-16gb) | 1 | Yerel dosya | 374,02 TL |
| [microSD modülü — Robodükkan](https://www.robodukkan.com/micro-sd-kart-modulu-644) | 1 | Kart ile bellek arasında SPI | 31,23 TL |
| **Listelenen çekirdek toplamı** | | | **3.454,73 TL** |

Fiyatlar sayfalarda görülen KDV dahil değerlerdir, 22 Eylül erişimi; sipariş anında değişebilir. Arama indeksindeki fiyatlar son ürün sayfası okumalarıyla güncellendi; ESP32 için415,65TL kullanılır. Kart/ADC/SD elektriksel uyumu gerçek ürünle kurulacak; bu liste test edilmiş paket değildir.

**EC kitinin yerli kaydı:** Sayfada1.625TL+KDV=1.950TL ve Sepete Ekle bulunuyor. Stok adedi, fiziksel raf mevcudu, kargoya veriliş tarihi ve orijinal tam kit kutu içeriği teyit edilmedi. Dolar dönüşümündeki fiyatı bu yerel listeye eklemiyoruz. Satıcıyla teyit edilecek: DFR0300 K1 prob+kart+kablo birlikte mi;1413µS/cm ve12,88mS/cm standartlar dahil ve kullanılabilir mi; elden teslim/çıkış zamanı nedir? Satıcıya mesaj gönderilmedi.

[Farnell Türkiye DFR0300](https://tr.farnell.com/dfrobot/dfr0300/electric-sensor-meter-brd-dfrduino/dp/2946108) alternatif kayıt:60,28EUR KDV hariç; listede118stok ve13hafta üretici standart teslimi birlikte görünüyor. Türkiye içinde hazır stok veya mülakat öncesi teslim sayılmadı. Bu nedenle hızlı yerli temin yerine otomatik ikame yapılmamalı.

## Atölyede tamamlayacağımız diğer malzemeler

Aşağıdaki miktar/boyutlar mühendislik önerisidir; marka fiyatı değildir. Mevcut okul malzemeleri kullanılabilir.

| Malzeme | Başlangıç miktarı | Özellik / neden |
|---|---|---|
| Şeffaf akrilik kolon veya uzun şeffaf kap | 1 | Yaklaşık50–70cm su yüksekliği; prob rahat geçecek, başlangıçta yaklaşık10cm iç genişlik. Prob boyutu görülünce kesinleştir. Bir metrelik prob kabloları nedeniyle ilk tankı gereksiz uzatma. |
| Sağlam taban/stand ve kolon sabitleme | 1 set | Dolu kolon devrilmeden durmalı; mevcut laboratuvar standı kullanılabilir. |
| Dökülme tepsisi | 1 | Tankı ve çevresini düzenler. |
| Prob tutucu / açık kafes | 1 | EC ve sıcaklık uçlarını yakın taşır; akışı kapatmaz. 3D baskı veya atölye imalatı. |
| Sabit çaplı ölçüm tekeri, encoder bağlantısı, kılavuz/baskı | 1 set | İp kaymadan ölçüm tekerini döndürür. Mesafeyi çok kat sarılan makaradan hesaplamıyoruz. |
| Esnemesi düşük ip ve mekanik bağlar | 2–3m ip | Yükü ip taşır; prob kablosu taşımaz. |
| Küçük denge ağırlığı | Gerektiğinde1 | Kontrollü dikey iniş; iletken yüzey EC ölçüm alanını etkilemeyecek yerde. |
| Cetvel / mezura | 1 | Sıfır ve encoder mesafesini kontrol. |
| Kuru elektronik kutusu | 1 | Kart, EC kartı ve SD suyun dışında. |
| Micro-USB veri kablosu ve mevcut USB güç/powerbank | 1'er | Kartı tek güç yolundan çalıştır; USB kablosu veri taşımalı. |
| Breadboard, delikli plaket, jumper, bağlantı kablosu | 1 set | İlk kurulum ve daha sonra sağlamlaştırma. |
| Direnç seti | 1 set | DS18B20 için4,7kΩ; encoder pull-up ve EC çıkış uyarlama dirençleri gerçek devreye göre. |
| Lehim, makaron, kablo bağı, konektör, vida | 1 küçük set | Kuru bağlantı sabitleme. |
| Temiz su, sofra tuzu, karıştırma kapları | 1 set | Deney çözeltileri. Hazırlanan NaCl çözeltileri sertifikalı EC standardı değildir. |
| Terazi, ölçülü kap, şırınga+hortum | 1'er | Tekrarlanabilir hazırlık, alt/üst tabakayı yavaş doldurma. |
| Standartlar ve referans cihazlar | Ödünç öncelikli | Kalibrasyon çözeltileri kutuda yoksa ayrıca temin; EC metre ve termometre bağımsız kontrol için. |

Kutu/kolon/mekanik/güç/sarf için **1.000–2.000TL geçici bütçe payı** ayırmak önerimizdir; satıcı teklifi veya doğrulanmış toplam değildir. Bunlar hazır bulunuyorsa düşer, özel kolon imalatıyla artabilir. Çekirdek+bu pay yaklaşık4.455–5.455TL eder; kargo/eksik standart/referans cihaz hariç. Sunum hazırlığı için yaklaşık5–6binTL hedef bütçe, eksik parçalara ayrılan planlama payıdır; kesin fiyat taahhüdü değil.

## Kart uyumu ve ölçüm sınırları

- [DFRobot üretici sayfası](https://www.dfrobot.com/product-1123.html): K1 için önerilen1–15mS/cm ve0–40°C. Deney çözeltilerini bu aralıkta hazırlayacağız. Saf su/sıfıra yakın EC veya normal deniz suyu için bu kitin uygunluğu varsayılmaz. Güçlü iki katman prensip gösterimidir; deniz profili/araştırma CTD doğruluğu değildir.
- Üretici EC çıkışı0–3,4V belirtir. **ESP32 analog girişine kontrolsüz doğrudan bağlanmayacak:** öğretmen çıkışı ölçüp gerilim bölme/uyarlama ve yazılım ölçeklemesini kuracak. ESP32 ADC'nin seçilen aralığı [Espressif belgesinden](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/adc.html) kontrol edilir.
- Seçilen600darbeli encoder5–24V beslemeli NPN açık kolektördür; eski pasif encoder tablosunun beslemesini aynen kullanmayın. A/B hatları3,3V mantığa uygun pull-up ile kurulmalı;5V sinyal ESP32'ye verilmez. Teker çevresi ve sayım modu cetvelle kalibre edilir.
- SD modülünün besleme/lojik düzeni ayrıca kontrol edilir. Kartın30pin sürümü eski WROOM-32E/DevKitC örneğiyle fiziksel aynı kart sayılmaz; GPIO etiketleri yeniden eşleştirilir.
- [ADS1115 modülü](https://www.direnc.net/ads1115-16-bit-i2c-4-kanal-modul)309,77TL, **isteğe bağlı**. İç ADC ile kararlılık yetersizse düşünülebilir; alımı zorunlu değil ve ADC eklemek giriş gerilimi uyarlamasını ortadan kaldırmaz. Kalibrasyonla toplam ölçüm doğruluğu ayrıca sınanır.
- Basınç sensörü ve GPS ilk tank demosunun şartı değil; tank derinliği encoder+referans cetveldir. Deniz v1'de gerçek basınç/depth ve saha metadata'sı ayrıca gerekir.

## Sunumda elde etmek istediğimiz çıktı

1. Kuru masada sıcaklık, encoder ve yerel CSV'yi doğrula.
2. EC kitini kendi standartlarıyla kalibre et; farklı çözeltilerde ayırt edici, kararlı sinyali kontrol et. Ham sinyali de sakla.
3. Homojen kolonda profil al; sonra benzer sıcaklıktaki altta daha yoğun/üstte daha seyreltilmiş iki çözeltiyle kontrollü kolon kur. İnişin tabakayı bozmasını kayıt altına al.
4. Probu yavaş veya duraklayarak indir; EC ve sıcaklık yerleşmesini gözle, hızlı CTD tepki süresi varsayma. Mümkünse3tekrar.
5. Gerçek tankCSV'sini mevcut platforma al; derinlik–sinyal/sıcaklık grafiği ve geçiş adayını göster. Firmware ve sensör entegrasyonu henüz yapılacak; mevcut yazılım importer/profil tarafı hazır.

Jüriye doğru ifade: **“Hazır ölçüm sensörlerini kendi derinlik takipli kayıt ve profil analiz düzeneğimize entegre ettik; kontrollü su kolonunda sınadık.”** Bu cümle ancak fiziksel deney tamamlandıktan sonra geçmiş zamanla kullanılacak. Sensörü ürettiğimizi veya Arktik dayanımını kanıtladığımızı söylemiyoruz.

Güncel durum: Alışveriş önerisi hazır; sipariş, öğretmen bağlantı testi, firmware derleme ve fiziksel deney henüz yok. Mevcut proje kaynak belgeleri ve veri etiketleri korunuyor.
