# PWN: hazır sensör veya hazır profil cihazı seçenekleri

22 Eylül 2026. Kullanıcı hazır cihaz alıp kendi sistemini üzerine kurma seçeneğini sordu. Bu belge üretici kaynaklarına dayalı ön karşılaştırmadır; satın alma, stok rezervasyonu veya kesin tasarım kararı değildir. Mevcut DIY v0.1 planı iptal edilmedi. Fiyatlar erişimde görülen üretici liste değerleridir; Türkiye teslim toplamı değildir.

## Sonuç ve önerimiz

Hazır ölçüm donanımı kullanmak mümkün. Projedeki özgün katkıyı sensörün kendisini imal etmek şartına bağlamıyoruz: araştırma sorusu, ölçüm protokolü, profil kalite kontrolü, model–gözlem karşılaştırması, örnekleme önerisi ve karar sistemine bağlantı bizim geliştireceğimiz işler olabilir. Bu araştırma tasarımı önerisidir; yarışma jürisinin kabul garantisi değildir.

İki ayrı yol var: (1) sensör+ölçüm kartını alıp PWN logger/mekanik/analiz sistemini kurmak; (2) tam CTD profil cihazını alıp veya erişim sağlanırsa ödünç kullanıp verisini platforma bağlamak. Tam cihaz başka, yalnız sensör modülü başkadır.

## Kaynaklı ürün karşılaştırması

| Aday | Üreticinin sunduğu | Görülen fiyat | Bizim bağlamımız |
|---|---|---|---|
| DFRobot Gravity DFR0300-H, K=10 | İletkenlik probu, sinyal kartı, standart çözelti. 10–100 mS/cm, 0–40°C, belirtilen doğruluk ±%5 tam ölçek. | 79,90 USD | Uygun aralıkta tuzlu tank deneyi için EC alt sistemi adayı. Tatlı su tarafında 10 mS/cm altı bu ürünün belirtilmiş aralığı dışında. Sıcaklık/derinlik/logger ve mekanik ayrıca gerekir; Arktik CTD değil. |
| Atlas Scientific Conductivity K10 Kit | K10 prob ve EZO iletkenlik elektronik kiti; üretici 70–500.000+ µS/cm aralığı belirtir. | 242,99 USD | Daha geniş iletkenlik aralığı isteyen entegrasyon adayı. Tam CTD değil; sıcaklık, derinlik, kayıt ve paketleme ayrıca tasarlanır. Daha önce bütçe nedeniyle tercih edilmemiş seçenek yeniden zorunlu yapılmıyor. |
| SonTek CastAway-CTD | İletkenlik/sıcaklık/basınç ölçümü; derinlik/tuzluluk türetimi, 100m profil, GPS, dahili kayıt, CSV dışa aktarma. | YSI ABD görünümünde 7.800 USD (US Only); Türkiye için teklif. | “Hazır al, profil topla, yazılıma aktar” sorusuna en doğrudan örnek. Satın alma yerine kurumsal erişim/ödünç olasılığını araştırmak önerimiz. |
| Valeport SWiFT CTD | C/T/D profili, 500m derinlik sınıfı, dahili GNSS, şarjlı batarya ve veri indirme yazılımı. | İncelenen sayfada açık fiyat yok. | Tam deniz profil cihazı alternatifi. Sefer ihtiyacına göre model/kalibrasyon/deployment seçimi gerekir; bu derinlik sınıfına ihtiyacımız olduğu kararlaştırılmadı. |

Kaynaklar:
- [DFRobot üretici sayfası](https://www.dfrobot.com/product-1797.html).
- [Atlas Scientific K10 kit](https://atlas-scientific.com/kits/conductivity-k-10-kit/).
- [YSI/SonTek CastAway ürün sayfası](https://www.ysi.com/castaway-ctd).
- [CastAway üretici teknik föyü: CSV, 100m, GPS ve ölçüm tanımları](https://www.xylem.com/siteassets/brand/sontek/resources/specification/sontek-castaway-ctd-spec-sheet-2018.pdf).
- [Xylem Türkiye ürün sayfası](https://www.xylem.com/tr-tr/products--services/analytical-instruments-and-equipment/data-collection-mapping-profiling-survey-systems/ctds/castaway-ctd/).
- [Valeport SWiFT CTD](https://www.valeport.co.uk/products/swift-ctd/).

CastAway sayfasının ilk web görünümünde Request Pricing görülürken, devam kontrolünde üretici sayfasının Jina Reader çıktısında **Price $7,800.00 (US Only)** doğrudan okundu. Bu ABD liste fiyatıdır; Türkiye satış/teslim teklifi değildir. Türkiye sayfasının varlığı yerel stok veya teslim süresi kanıtı değildir. Vergi/kargo/gümrük, kalibrasyon ve ödünç erişimi teyit edilmedi. Modül fiyatı bütün PWN maliyeti değildir.

## Dokuz günlük hedef için tercih sırası — öneri

1. Okul/üniversite/KARE bağlantıları üzerinden erişilebilen uygun CTD veya EC referans cihazı olup olmadığını öğrenmek. Herhangi bir kurumda cihaz var, ödünç verilecek veya sponsor olacak denmiyor; kimseye mesaj gönderilmedi.
2. Hızlı erişim varsa hazır EC kiti + mevcut kart + sıcaklık + encoder + kayıtla tank PoC'sini kurmak. Kitin aralığı hazırlanacak çözeltilere göre seçilir; K10 her deney için otomatik tercih değildir.
3. Tam CTD'ye erişim sağlanırsa kendi su kolonu/profil iş akışımızı ve verinin karar motoruna bağlantısını göstermek. Sensörü bizim yaptığımız iddia edilmez. Arctic kullanım koşulları sefer ekibiyle ayrıca belirlenir.

Yalnız ekranda sayı gösteren ve kayıt/dışa aktarma sağlamayan bir el ölçeri, otomatik derinlik profili cihazıyla eşdeğer saymıyoruz. Bir cihazın suya girebilmesi basınç dayanımını veya soğuk deniz şartlarında doğruluğunu kanıtlamaz. Bu ayrım satın alma seçiminde somut işlev farkıdır.

## Biz ne geliştireceğiz?

Hazır sensör/CTD → zaman/konum/derinlik ve kaynak metadata'sı → profil kalite kontrolü → geçiş/anomali değerlendirmesi → model–gözlem eşleştirmesi → ilgili kaynak suyu hesabının güncellenmesi → aynı ürün deseni motorunun yeniden çalışması.

Mevcut uygulama kendi CSV sözleşmemizi okuyor. CastAway veya başka marka CSV'si doğrudan denenmedi; gerçek örnek dosya gelince sütun/birim, sıcaklık türü, kalibrasyon, UTC/konum ve basınç/derinlik eşlemesi için adaptör eklenmeli. “Hazır ürün var” ile “bu marka şu an bizim yazılımla doğrulandı” ayrıdır.

Gemi CTD'sinin zaten toplayacağı veriyle ek çalışmamızın farkı erişim sağlandığında belirlenmeli: tamamlayıcı profil/örnekleme, eşleştirme veya karar etkisi analizi. Sırf kendi sensörümüz olsun diye mükerrer ölçüm gerekçesi üretilmez.

## Şerif Efe ekibinin örneği

[Kabataş Erkek Lisesinin resmî duyurusu](https://kabataserkeklisesi.meb.k12.tr/icerikler/istanbulvalimizsndavutgulunkabulu_15898011.html) İnsansız Kutup Hava Aracı ve Milli Kutup Veri Analiz Programını birlikte anlatıyor. Bu, donanım+veri analizi bağlantısı açısından ilgili örnektir. Kullanıcının “hazır drone üzerine sistem taktılar” açıklaması ayrı kullanıcı aktarımıdır; incelenen duyuru drone'nun hangi parçalarının hazır satın alındığını kesinleştirmiyor. Buradan öğrenciler için aynı satın alma modelinin resmen onaylı olduğu sonucu çıkarılmadı.

## Bu tur tamamlanan / tamamlanmayan

Tamamlanan: üretici kaynaklı ön tarama, iki EC kitinin fiyat/aralık ayrımı, iki tam CTD alternatifi ve entegrasyon yolu. Kod/donanım değiştirilmedi; testler yeniden çalıştırılmadı. Fiziksel PWN hâlâ yapılmış değil. Bütçe, yerel stok/teslim, kurumdan ödünç ve exact cihaz modeli açık. Karar kilitlenmedi.

## Kullanıcının fiyatları birlikte istemesi üzerine ek karşılaştırma

22 Eylül 2026 erişimi. Yaklaşık TL hesabı için [USD/TRY](https://www.investing.com/currencies/usd-try?obOrigUrl=true) sayfasındaki48,8201 yuvarlanarak **48,82TL/USD** kullanıldı. Bu kur dönüşümü Türkiye satış fiyatı değildir; ithal ürünlerde vergi/kargo/gümrük dahil değildir.

| Seçenek | Liste | Yaklaşık TL |
|---|---:|---:|
| [DFRobot K1 DFR0300](https://www.dfrobot.com/product-1123.html) EC kit | 69,90USD | 3.413TL |
| DFRobot K10 DFR0300-H EC kit | 79,90USD | 3.901TL |
| Atlas K10 EC kit | 242,99USD | 11.863TL |
| CastAway tam CTD | 7.800USD / ABD liste | 380.796TL |
| Valeport SWiFT CTD | Teklif; açık fiyat doğrulanmadı | — |
| [RBRconcerto CTD](https://rbr-global.com/how-to-select-the-right-ctd/) | Model/konfigürasyona göre teklif; güncel açık fiyat doğrulanmadı | — |

K1 düşük iletkenlikteki tank deneyleri için incelenebilecek ayrı adaydır; tam deniz iletkenliği için otomatik uygun sayılmaz. Uygun deney aralığı üretici şartlarıyla seçilmeli. Eski RBR satın alma belgeleri ve ikinci el/özel konfigürasyon fiyatları yeni cihaz fiyatı diye kullanılmadı.

EC kitine ek, Türkiye perakende fiyat örnekleri:
- [ESP32 30pin katalog kaydı](https://www.robotistan.com/nodemcu-esp):415,48TL.
- [Suya uygun paket DS18B20](https://www.robotistan.com/su-gecirmez-ds18b20-dijital-isi-sensoru):75,01TL KDV dahil.
- [600 darbeli optik encoder](https://www.robotistan.com/doner-encoder-600d):604,24TL KDV dahil.
- [16GB microSD](https://www.robotistan.com/micro-sd-kart-16gb):371,52TL KDV dahil.
- [microSD modülü](https://www.robodukkan.com/micro-sd-kart-modulu-644):29,98TL KDV dahil.

Bu beş parça toplamı **1.496,23TL**. Kart/modül pin/gerilim uyumu nihai devrede kontrol edilecek; bunlar test edilmiş kit eşleşmesi değil fiyatlandırma adaylarıdır. Kablo, direnç/seviye uyarlama, güç, kutu, kolon, ölçüm tekeri/tutucu, ek kalibrasyon ve işçilik dahil değildir. Standalone kayıt hedefi korunur.

Yalnız listelenen elektroniklerin aritmetik alt toplamı: K1'li4.908,75TL; K10'lu5.396,95TL; Atlas'lı13.359,00TL. Bunlar çalışır cihaz için nihai bütçe veya Türkiye'ye teslim toplamı değildir. Okulda bulunan parçalar maliyeti azaltabilir. Şeffaf kolon ve mekanik boyutları seçilmeden gerçek fiyat uydurulmadı.
