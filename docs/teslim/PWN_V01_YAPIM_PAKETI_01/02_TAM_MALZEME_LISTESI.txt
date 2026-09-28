# PWN v0.1 — eksiksiz tedarik ve atölye kontrol listesi

22 Eylül 2026. Kapsam: okulda, kontrollü su kolonunda EC/sıcaklık/encoder mesafesi kaydeden ve gerçek profilini uygulamada gösteren ilk prototip. Bu belge güncel tedarik ana listesidir; eski 24 kalem `hardware/pwn-v0.1/BOM.csv` içindeki DIY elektrot/ön devre önceliğinin yerini alır. Cihaz kurulmuş veya test edilmiş değildir. Satın alma yapılmadı.

**Tek önerilen yol: DFR0300 K1 hazır EC kiti + ESP32 + DS18B20 + encoder + microSD + kendi basacağımız mekanik.** Sensör satın alınır; taşıyıcı, derinlik takibi, kayıt, deney ve analiz bizim entegrasyonumuzdur. Kullanıcı beyanı: 3D yazıcı mevcut. Diğer malzemelerin envanteri bilinmiyor.

Adetler, boyutlar ve sarf miktarları atölye için mühendislik önerisidir; üretici şartı veya gerçekleşmiş ölçüm değildir. Önce okulda bulunanlar ayrılır, yalnız eksikler alınır. “Gerekli” bir işlevi ifade eder; örneğin mevcut sağlam laboratuvar standı yeni bir stand satın alma ihtiyacını karşılar.

## A. Ana elektronik — gerekli

Fiyat sütunu 22 Eylül 2026 önceki yerel sayfa okumalarının kaydıdır; bu belgede tüm fiyatlar yeniden sorgulanmadı. KDV dahil; stok/teslim/kutu içeriği satıcıyla teyit edilmedi. Linkler [önceki fiyat araştırmasında](PWN_TURKIYE_ALISVERIS_V01.md) da kayıtlıdır.

| No | Malzeme | Miktar | Seçim ve kontrol | Kayıtlı fiyat |
|---|---|---:|---|---:|
| A1 | [DFRobot DFR0300 K1 tam EC kiti](https://www.emesrobotik.com/urun/dfrobot-gravity-elektriksel-iletkenlik-ec-sensoru-kiti-k-1-dfr0300) | 1 | Prob + V2 ölçüm kartı + BNC prob kablosu + PH2.0 üç pin sinyal kablosu. Sadece prob alınmaz. İki standart ayrıca B1/B2'de. | 1.950,00 TL |
| A2 | [ESP32 ESP-32S 30 pin geliştirme kartı](https://www.robotistan.com/esp32-esp-32s-wifi-bluetooth-dual-mode-developement-board) | 1 | Lehimli pinli tercih; gerçek GPIO etiketi ve USB konnektörü kontrol edilir. | 415,65 TL |
| A3 | [Suya uygun paketli DS18B20](https://www.robotistan.com/su-gecirmez-ds18b20-dijital-isi-sensoru) | 1 | Üç telli harici besleme; yaklaşık 1 m veya daha uzun kablo. Çip datasheet'i paket basınç dayanımı değildir. | 75,52 TL |
| A4 | [600 darbe optik encoder](https://www.robotistan.com/doner-encoder-600d) | 1 | E38S6G5-600BG24N, 5–24 V besleme, NPN açık kolektör. Mekanik boyutlar elde ölçülecek. | 608,31 TL |
| A5 | [microSD kart, 16 GB](https://www.robotistan.com/micro-sd-kart-16gb) | 1 | Yerel CSV; başka yeterli kapasiteli uyumlu kart varsa kullanılabilir. | 374,02 TL |
| A6 | [SPI microSD modülü — aday](https://www.robodukkan.com/micro-sd-kart-modulu-644) | 1 | **Kesinleşmemiş model:** besleme ve MISO/MOSI/SCK/CS seviyeleri ESP32 ile uyumlu olmalı. Ucuz adayın elektriksel uyumu henüz doğrulanmadı; uygun eşdeğerle değişebilir. | 31,23 TL |
| A7 | Micro-USB **veri** kablosu | 1 + mümkünse 1 yedek | Kartın gerçek soketine uygun; yalnız şarj kablosu olmaz. | Teklif yok |
| A8 | 5 V USB güç erişimi | 1 | İlk testte bilgisayar USB'si; bağımsız gösterimde mevcut uygun powerbank. Güç bütçesi/kayıt sırasında reset kontrolü yapılır. Kart tek güç yolundan beslenir. | Mevcutsa alım yok |
| A9 | USB microSD okuyucu veya uygun SD adaptörü | 1 | Bilgisayarda uygun okuyucu yoksa. Kartı çıkarıp dosyayı alabilmek için. | Teklif yok |

**A1–A6 kayıtlı toplam: 3.454,73 TL. Bu tüm cihazın toplamı değildir.** SD adayının değişmesi bu toplamı da değiştirir.

## B. Kalibrasyon, temizlik ve bağımsız kontrol

| No | Malzeme | Miktar | Durum / neden |
|---|---|---:|---|
| B1 | EC standardı **1413 µS/cm = 1,413 mS/cm** | 1 kullanılabilir şişe | Gerekli. Üreticinin standart kit içeriğinde bulunuyor; yerli satıcı paketinde dahilse tekrar alınmaz. Referans sıcaklığı/son kullanım ve probu örtecek hacim kontrol edilir. |
| B2 | EC standardı **12,88 mS/cm = 12880 µS/cm** | 1 kullanılabilir şişe | Gerekli; aynı kutu kontrolü. pH tamponu veya TDS ppm sıvısıyla değiştirilmez. |
| B3 | Distile su | İlk etap 2–5 L | Gerekli, durulama için planlama miktarı. Deney çözeltisini hazırlamak için ayrılan sudan ayrı. |
| B4 | Sıkılabilir yıkama şişesi | 1, yaklaşık 500 mL | Distile suyla prob durulama. |
| B5 | Temiz, ayrı etiketli kalibrasyon kapları | 3–4 | İki standardı ve durulamayı ayırır; hacim prob ucunu örtecek. Kullanılmış sıvı stok şişeye dökülmez. |
| B6 | Kağıt havlu, etiket, kalıcı kalem | 1'er paket/adet | Dış yüzeydeki damla ve çalışma alanı; EC'nin aktif kaplaması silinmez/ovulmaz. |
| B7 | Bağımsız EC metre | 1, ödünç öncelikli | **Doğruluk kontrolü için güçlü öneri.** Deney aralığında mS/cm göstermeli, kendi kalibrasyonu bilinmeli. Yokluğu prensip demosunu engellemez; bağımsız doğrulama yapıldı denmez. |
| B8 | Bağımsız termometre | 1, ödünç öncelikli | Sıcaklık karşılaştırması; referans belirsizliği bilinmiyorsa profesyonel kalibrasyon diye sunulmaz. |

DFRobot iki noktalı kalibrasyonu, sıcaklık sensörü kullanımını, distile suyla durulamayı ve aktif kaplamaya dokunmamayı tarif eder. Arduino örnek kodu ESP32'ye olduğu gibi kopyalanmaz: ADC ölçeği, gerilim bölücü düzeltmesi ve kalıcı kalibrasyon kaydı uyarlanacak. [Üretici kurulum/kalibrasyon belgesi](https://wiki.dfrobot.com/dfr0300/docs/20349).

## C. Küçük elektronik ve sağlam bağlantı — gerekli set

| No | Malzeme | Başlangıç miktarı | Kullanım / sınır |
|---|---|---:|---|
| C1 | Breadboard | 1 büyük veya 2 küçük | 30 pin kartın iki yanına bağlantı yapılabilmeli. |
| C2 | Delikli plaket | 1 | Masa testi sonrası gevşemeyen gösterim montajı; breadboard'da kalıcı gösterime mecbur değiliz. |
| C3 | Erkek–erkek ve erkek–dişi jumper | Her türden 20 | Kuru bağlantılar; ihtiyaç olursa dişi–dişi 10. |
| C4 | Çok damarlı ince bağlantı kablosu | Toplam 3–5 m, farklı renkler | Kutu içi dağıtım ve kuru uzatmalar. EC probunun BNC kablosu kesilmez/uzatılmaz. |
| C5 | 4,7 kΩ direnç | 10 | Bir adet DS18B20, iki adet encoder A/B pull-up için başlangıç; kalanlar yedek. Encoder pull-up'ları 3,3 V'a. |
| C6 | %1 toleranslı 10 kΩ ve 20 kΩ direnç | Her değerden 4 | EC çıkışı için gerilim bölücü ve yedek. Örnek: OUT–10k–ADC–20k–GND; 3,4 V → yaklaşık 2,27 V **hesabı**, yapılmış devre testi değil. Ölçülen direnç/gerilimle ölçek doğrulanır. |
| C7 | 100 nF seramik kondansatör | 5–10 | Besleme/ADC gürültü önlemleri için montaj stoğu; tümü rastgele paralel bağlanmaz. |
| C8 | 100 µF, en az 10 V elektrolitik kondansatör | 2 | Gerekirse besleme yerel tamponu; kutup ve gerçek gereksinim kontrol edilir. |
| C9 | Pin header / dişi soket / küçük vidalı klemens | 1 küçük set | Modül bacakları, sensör ve besleme bağlantılarının sökülebilir sabitlenmesi. |
| C10 | Lehim teli ve uygun flux | 1'er küçük paket | Atölyede varsa alınmaz. |
| C11 | Isı makaronu, elektrik bandı, kablo bağı | 1'er paket | Kuru ek ve gerilimden kurtarma; sualtı sızdırmazlık kanıtı değildir. |
| C12 | Kuru elektronik kutusu + kart yükselticileri | 1 kutu + yaklaşık 8 yükseltici/vida | ESP32, EC kartı ve SD'yi birlikte almalı; yerleşim görülerek ölçü seçilir. 3D basılabilir, suya batırılmaz. |
| C13 | Kablo geçiş lastiği veya uygun rakor | 3–4 | Kutu kenarında kabloyu koruma; gerçek kablo çapıyla eşleşmeli. |

EC modülü çıkışı 0–3,4 V, beslemesi 3–5 V'tur [DFRobot teknik belge](https://wiki.dfrobot.com/dfr0300/). Örnek bölücü bir mühendislik çözümüdür; ESP32 ADC aralığı/kalibrasyonu [Espressif ADC dokümanına](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/adc.html) göre kurulacak. Encoder beslemesi 5 V seçilir; A/B açık kolektör hatları 3,3 V pull-up ile okunur ve gerçek ürün multimetreyle kontrol edilir. Bu tablo fiziksel bağlantı doğrulaması değildir.

## D. Kolon ve 3D baskılı mekanik — gerekli

**Önerilen tank hedefi:** yaklaşık 50–60 cm su yüksekliği, yaklaşık 15–20 cm iç genişlik. Bu boyutlar üretici şartı değildir; ilk listedeki yaklaşık 10 cm dar kolon önerisi yerine montaj/akış için daha rahat başlangıçtır. Başlık ve kablo hareketi denenmeden özel ölçü kolon siparişi verilmez. Ölçüm ucunun duvara, tabana ve metal ağırlığa yaklaşmasının etkisi homojen suda kontrol edilir.

| No | Malzeme | Miktar | Açıklama |
|---|---|---:|---|
| D1 | Şeffaf, su tutan dikey kap/kolon | 1 | Hazır tabanlı kap tercih. Sadece açık akrilik boru alınırsa taban ve uygun sızdırmaz birleştirme ayrıca gerekecek. Yaklaşık 1 m EC kablosuyla kuru kart erişimi korunur. |
| D2 | Taban, dik destek ve kolon sabitleme kelepçeleri | 1 set | Mevcut laboratuvar standı veya atölye imalatı. Dolu ağırlıkla denenecek; taşıyıcı taban yalnız küçük 3D parçaya bırakılmaz. |
| D3 | Dökülme tepsisi ve kaymaz taban | 1'er | Kolonun altında. |
| D4 | Açık sensör tutucu/başlık | 1 baskı | EC ucu açıkta; kabarcık tutmayan ve akışı kapatmayan yapı. Sıcaklık ucunun ölçüm alanını bozmadığı kontrol edilir. |
| D5 | Sabit çaplı, oluklu ölçüm tekeri | 1 baskı | İpin hareketini sayar. Biriken ip çapıyla derinlik hesaplanmaz. |
| D6 | Encoder braketi ve teker bağlantı göbeği | 1'er baskı | Gerçek mil ve montaj delikleri ölçülerek CAD. Hazır uyumlu göbek de kullanılabilir. |
| D7 | İp baskı/kılavuz tekeri ve braketi | 1 set | Kaymayı ve ip çıkmasını azaltır; kauçuk/O-ring temas yüzeyi ve ayarlanabilir baskı. |
| D8 | Kılavuz için mil/omuzlu cıvata + rulman | 1 mil + 2 rulman | Tasarıma uygun eşleşmiş set; örneğin 608 rulman seçilirse iç çap 8 mm'ye uygun mil. Encoder miliyle aynı çapta olduğu varsayılmaz. |
| D9 | Ayar yayı veya elastik baskı elemanı, O-ring/kauçuk bant | 1 küçük set | Kılavuz basıncı ve teker tutuşu; tasarıma göre yay yerine ayarlı sabit baskı kullanılabilir. |
| D10 | Esnemesi düşük örgü ip | 3 m | Başlığı taşıyan bağımsız yük yolu; sensör kabloları yük taşımaz. |
| D11 | Başlık bağlantı halkası ve küçük ayarlanabilir ağırlık | 1'er | Ağırlık yalnız gerekiyorsa; ölçüm hücresinden uzakta sabitlenir. |
| D12 | M3/M4 vida, somun ve pul seti | Yaklaşık 20–30 bağlantılık | Farklı uygun boylar; encoder gövdesinin satıcıda belirtilen M3/5 mm delik derinliği aşılmaz. Gövde vidası boyu braket kalınlığına göre hesaplanır. |
| D13 | Cetvel/mezura ve su seviyesi işareti | 1'er | En az deney yüksekliğini kapsayan cetvel; başlangıç referansı EC ölçüm merkezidir. |
| D14 | Filament | Yaklaşık 250–500 g ayır | **3D yazıcı mevcut — kullanıcı beyanı.** Miktar CAD/slicer olmadan tahmindir; mevcut uygun filament kullanılabilir. Baskıdan basınç kabı yapılmıyor. |
| D15 | Küçük sıkıştırma kelepçesi | 2 | Encoder düzeneğini stand/masa üzerine sabitler; mevcut eşdeğer kullanılabilir. |

3D baskı teslimleri: sensör başlığı, encoder braketi/göbeği, ölçüm tekeri, kılavuz/baskı düzeneği ve kuru kutu/bağlantı düzeni. Gerçek parçalar ölçülmeden dosyalar tamamlanmış sayılmaz. Encoder ürün bilgisi: [Robotistan](https://www.robotistan.com/doner-encoder-600d).

## E. Deney hazırlığı — gerekli

| No | Malzeme | Başlangıç miktarı | Kullanım |
|---|---|---:|---|
| E1 | Aynı kaynaktan temiz deney suyu | Tank hacminin yaklaşık 2–3 katı | Homojen kontrol, iki katman ve yenileme için. Yuvarlak 15 cm çap × 50 cm su yaklaşık 8,8 L; 20 cm × 60 cm yaklaşık 18,8 L **geometri hesabıdır**. Gerçek kap şekline göre hacim ölçülür. |
| E2 | Sofra tuzu / NaCl | 250–500 g stok yeterli başlangıç | Bu miktarın tümü tanka dökülmez. İletkenlik ölçülerek kitin önerilen 1–15 mS/cm aralığında iki ayrışan çözelti hazırlanır; tuz kütlesi EC kalibrasyonunun yerine geçmez. |
| E3 | Temiz hazırlama kovası/kap | 2 | Her biri ilgili katman hacmini almalı; düşük/yüksek EC ayrı. |
| E4 | Dijital terazi | 1 | Çözelti hazırlama kaydı için; mevcut mutfak/laboratuvar terazisi kullanılabilir, çözünürlüğü kayda yazılır. |
| E5 | Ölçülü sürahi/silindir ve karıştırma çubuğu | 1'er | Hacim ve homojen hazırlık. |
| E6 | Şırınga, ince hortum ve akışı kısma mandalı | 1 büyük şırınga + yaklaşık 1–2 m hortum + 1 mandal | Küçük akışlı doldurma; büyük hacimde ölçülü kaptan kontrollü hortum akışı. |
| E7 | Huni ve boşaltma/atık kabı | 1'er | Temizleme ve tankı toplama. |
| E8 | Deney defteri veya çıktı formu | 1 | Çözelti hazırlığı, kalibrasyon, cast kimliği, yüzey sıfırı, bekleme süresi ve tekrarlar. |

Gıda boyası şart değil; ölçüm kolonu yerine ayrı görsel gösterimde kullanılabilir. Boya eklenirse bileşim değişikliği deney notuna yazılır. İlk hedef benzer sıcaklıkta homojen kontrol ve güçlü iletkenlik katmanı; daha sonra mümkünse üç tekrar. Cihazın yerleşme süresi test edilmeden hızlı/santimetre hassasiyetinde profil sözü verilmez.

## F. Okuldan/atölyeden kullanılacak araçlar

| Araç | Miktar | Gereklilik |
|---|---:|---|
| Bilgisayar + USB portu | 1 | Firmware yükleme, kayıt kontrolü, uygulama ve gösterim. |
| Multimetre | 1 | Gerilim, direnç, süreklilik ve bağlantı kontrolü için gerekli. |
| Havya/istasyon ve sehpası | 1 | Plaket ve sağlam montaj için. |
| Yan keski, kablo soyucu, pense, tornavida/alyan | 1 set | Montaj. |
| Kumpas | 1 | Prob/encoder mili/braket için CAD ölçüleri; okuldan kullan. |
| Matkap/uçlar, küçük eğe/zımpara | 1 set, gerekirse | Kutu/stand ve baskı son işlemleri. |
| Telefon + sabit destek | 1 | Gösterim videosu ve deney düzeni kaydı; mevcut cihaz. |

Osiloskop hazır EC kitli v0.1'in satın alma şartı değildir; sinyal sorunu çıkarsa atölyeden kullanılabilir. Bağımsız EC metre ve termometre B7/B8'de; bu araçların hepsini satın almak gerekmiyor.

## G. Bu sürümde satın almaya gerek olmayanlar

- Basınç sensörü, GPS, uydu iletişimi, LoRa/GSM, sualtı bataryası veya basınç gövdesi.
- pH, çözünmüş oksijen, bulanıklık sensörleri; özel ihtiyaç olmadan eklenmez.
- Ayrı Arduino/Deneyap/ikinci ESP32; seçilen tek kart yeterli tasarım hedefidir.
- DC motor, motor sürücü, otomatik vinç; v0.1 elle/duraklayarak indirilir.
- Kendimiz yapacağımız EC elektrotları ve AC sürücü devresi; seçilen kit bu işlevi sağlar.
- Harici ADC: ancak ölçüm testi ihtiyacı gösterirse. ADS1115 kendiliğinden gerilim uyumu sağlamaz.
- RTC/saat modülü: tank CSV sözleşmesi `elapsed_ms` ile çalışabilir; gerçek UTC yoksa üretilmez. Bilgisayardan saat eşitleme ayrı seçenektir.
- Dahili LCD/ekran: ilk gösterim bilgisayardaki profildir; ekrana bütçe ayırmak şart değil.

## H. Bütçenin dürüst sınırı ve sipariş kontrolü

3.454,73 TL yalnız fiyatı kayıtlı altı ana bileşenin toplamı. Önceki 5–6 bin TL ifadesi okulda araç/kap/güç bulunduğu ve mekanik maliyetinin düşük kaldığı koşullu hedef bütçeydi. **Buradaki her şeyi sıfırdan satın almanın kesin toplamı değildir.** Kolon/stand, standartlar kutuda yoksa standartlar, küçük sarflar ve kargo fiyatlandırılmadan “tam maliyet” verilemez. 3D yazıcı erişiminin olması yalnız yazıcı edinme ihtiyacını kaldırır; filament, rulman ve bağlantı malzemeleri ayrıca kontrol edilir.

Sipariş öncesi ürün düzeyinde açık kalanlar:

1. DFR0300 K1 tam kit + iki standardın kullanılabilir şekilde dahil olması, gerçek stok ve teslim tarihi.
2. Seçilecek SPI SD modülünün **besleme ve dört sinyal hattı** açısından ESP32 uyumu.
3. Gerçek prob/encoder ölçülerine göre baskı ve kolon boşlukları; teker ve kılavuz için eşleşmiş mil/rulman.

Bu üçü belirsizken “tam olarak bu ürün sepeti tak-çalıştırdır” denmez. Başka araştırma yönü açılmıyor; aynı tasarımın parça uyumu tamamlanıyor.

## I. Malzeme tamamlandıktan sonra çalışır kabul edeceğimiz çıktı

1. Kuru masada sıcaklık + encoder + SD kayıt/geri okuma ve gerilim kontrolü.
2. Kalibrasyonun kaydedilmesi ve güç kesip açınca korunması; iki çözeltinin kararlı biçimde ayrılması.
3. Cetvel ile encoder mesafe/sıfır kontrolü; kayma ve başlık ofseti kaydı.
4. Homojen kontrol, tabakalı kolon, mümkünse tekrar profilleri; ölçüm yerleşmesini bekleyen iniş.
5. Gerçek CSV + metadata'nın mevcut PWN içe alma akışına verilmesi. Ham mV/ADC ile kalibre EC ayrı tutulur; deniz tuzluluğu veya Arktik ölçümü gibi etiketlenmez.

Firmware derlemesi, kalibrasyonun ESP32'ye uyarlanması, baskı CAD'i ve fiziksel deney henüz tamamlanmadı. Bu iş paketi tedarik/montaj hazırlığıdır; yazılım testleri bu tur yeniden çalıştırılmadı.
