# Ürün denetimi ve dashboard dönüşümü

**22 Eylül 2026 / U9 güncel ek:** Etkileşim artık kalıcı Scenario Lab + sağ desen/veri/grafik alanıdır. [SIMULATOR_UX](SIMULATOR_UX.md). NASA SSP245/5852035 kaynak bağlamı eklendi; yerel hidroloji/uygunluk yerine geçmez. [Güncel durum](BUILD_STATUS.md), [su güvenliği](NORTH_WATER_SECURITY.md). Önceki aşama anlatıları bu güncel kayıtla birlikte okunur.
22 Eylül 2026 · U7 dashboard dönüşümü, U8 çekirdek motor düzeltmesiyle güncellendi. Bilimsel kapsam ve dashboard dili korunur. **Ana ürün artık mevcut desen → kullanıcı senaryosu → önerilen desen simülatörüdür.** Tamamlanma bilgisi BUILD_STATUS, ana sohbete aktarım ANA_CHAT_TESLIM içindedir.

## A. Mevcut ürün denetimi

İlk sürümde sekiz adımlı gezinme, büyük başlıklar ve “sonraki adım” düğmeleri bir sunum sırası oluşturuyordu. Konya kökeni, gelecek bulgusu, kaynak koşulları ve karar ekranları ayrı tam sayfalardı. Kullanıcı bir parametrenin sonucunu izlemek için sayfalar arasında gidip geliyordu. Harita çoğunlukla bağlam görseliydi; beş bölgenin yan yana sorgulanacağı çalışma yüzeyi değildi. Kaynak kanıtları mevcuttu, fakat kararın yanında hangi kısıtın dolduğu ve hangi seçeneğin neden elendiği yeterince görünür değildi.

Yazılımda optimizasyon ve veri altyapısı çalışıyordu; sorun bu işlevlerin ürün hiyerarşisinde geri planda kalmasıydı. Önceki 8 ekranın görsel kaydı docs/verification ve önceki uygulama kodu incelemesi bu denetimin yerel dayanağıdır. Bu kullanıcı testinden çıkarılmış istatistiksel bir bulgu değil, kullanıcının değerlendirmesiyle uyumlu ürün denetimidir.

U8 denetimi ikinci sorunu ortaya koydu: dashboard görünümü düzelmişti, fakat ana kuzey hesabı tek marul hedefinde yöntem/kaynak seçimiyle sınırlıydı. Türkiye de esasen beş noktalı iklim karşılaştırmasıydı. Özgün 2204-D'nin **hangi üründen ne kadar?** kararı geri planda kalmıştı. Düzeltme görsel süs eklemek yerine ortak ürün alanı/kapasite motorunu ve manuel senaryoyu merkeze aldı.

## B. Yeni ürün mimarisi

Dört ana çalışma alanı; Konya tarihsel pilot referansı bunların içindeki kısa bağlamdır:

| Alan | Görev | Ana içerik |
|---|---|---|
| Türkiye planlama / simülasyon | Bölgeyi seç, mevcut deseni düzenle ve önerilen desenle karşılaştır | Resmî baseline, kullanıcı pay/alan/su/üretim girdileri, hesap, ürün bazında gerekçe; benchmark karşılaştırması ikincil |
| Gelecek kuzey planlama / simülasyon | Aynı motorla geleceğin çok ürünlü üretim desenini hesapla | Aday portföy, açık/kapalı kapasite, su kaynakları, enerji, dönem, yöntem/kaynak tahsisi ve saha öncesi/sonrası |
| PWN / saha gözlemi | Profil verisini incele ve saha katkısını sınırlarıyla göster | Mevcut CSV yükleme, kalite/derinlik, profil, klasik gradient; Arctic v1 konsepti ayrı |
| Kanıt / yöntem | Sonucun dayanağına ulaş | Kaynak kayıtları, kanıt sınıfları, varsayımlar, bilimsel açıklar |

Konya pilot referansı eski dört ürün deseni ve yaklaşık %8,7 göreli model sonucunu gösterir; yeni kaynaklı Konya simülasyonundan ayrıdır ve bağımsız ana ürün olmaz.

Kalıcı uygulama çerçevesi, kaynak çekmecesi, kanıt etiketleri ve PWN yükleme korunur. Planlama iki modu aynı motorla açar; karar/desen sonucu girdilerin yanında yer alır. Harita bağlamdır, ana çıktı mevcut/önerilen ürün tablosudur. Kuzey dönem/senaryo etiketi kullanıcı girdisi olabilir; değiştirmek yeni SSP verisi indirmez. Yerel dış modelin gerçek dönemi ayrıca gösterilir.

Etkileşim modeli: girdi düzenle → hesabı çalıştır → kısıt/sonuç incele → önceki hesabı karşılaştırma için tut → değişen girdinin etkisini gör. Girdi değişip hesap yenilenmediyse eski sonuç açıkça işaretlenir. Türkiye'de seçilen bölgeler aynı hesap koşuluyla yan yana gelir. Kanıt ayrıntıları ana iş akışını terk etmeden açılır. Dosya yükleme ve kaynak koruma akışı devam eder.

## C. Türkiye kapsamı

Seçilen küçük set: **Konya, Seyhan–Adana, Gediz–Manisa, GAP–Harran ve Trakya–Edirne**. Amaç beş farklı gerçek çalışma bağlamında yöntemin nasıl davrandığını görmek; beş istasyonla tüm Türkiye'yi doğruladığını iddia etmek değil. Nokta reanalizi havza ortalaması değildir.

Beş ilin 21 gerçek ürün/alan/üretim kaydı ve bölgeye özgü portföyleri eklendi: [TURKIYE_REGIONAL_SIMULATOR.md](TURKIYE_REGIONAL_SIMULATOR.md). Ana iş akışı tek bölgeyi seçip kaynaklı deseni yüklemek, varsayımları değiştirmek ve yeniden hesaplamaktır. İl deseni ile tek iklim hücresi aynı ölçek değildir; Konya 2023, diğer iller 2024 deseni 2022–2023 hava referansında koşulur. Yerel takvim ve su tahsisi ayrıca doğrulanacaktır.

İkincil benchmark panelinin seçilme gerekçeleri [TURKIYE_BENCHMARKS.md](TURKIYE_BENCHMARKS.md) içindedir. Orada ortak ürün/takvim/depo ile karşılaştırma korunur; bölgesel ürün optimizasyonuyla aynı çıktı diye gösterilmez.

Ortak net ek su bütçesi, sulamasız referans ET açığıyla karşılaştırılır. `gap=max(referans açık−net bütçe,0)`. Bu ikincil karşılaştırma sulama programını simüle etmez, randımanı veya gerçek tahsisi ölçmez; üretim/verim garantisi değildir. “Hangi bölgede aynı varsayımlar altında daha büyük açık kalıyor?” sorusunu yanıtlar. Her bölgeye kanıtsız farklı yerel su tahsisi atanmaz.

## D. Kuzey için minimum veri/model zinciri

1. Geniş coğrafi kuzeye kayma: Xu vd. dış literatür sonucu; iklim potansiyeli için bağlam.
2. Yerel model dönemi karşılaştırması: tek adı belirtilmiş iklim modelinden aynı noktada tarihsel/gelecek dönem GDD5, don olmayan pencere ve yağış. Kalite kontrolü ve gerçek kullanılan dönem/model ayarları [NORTH_DATA_PLAN.md](NORTH_DATA_PLAN.md) içinde. Bir model, ensemble belirsizliği veya yerel tarım doğrulaması değildir.
3. Toprak/permafrost/alan filtresi: eksikse açık tarla otomatik uygun sayılmaz. Kullanıcı varsayımı ayrıca etiketlenir.
4. Karasal su güvenliği: yağış tek başına çekilebilir arz değildir; depolama/akım/çekim/tahsis/ekolojik gereksinim verileri açık kalır. UI'daki su bütçesi senaryodur.
5. Kaynak kullanılabilirliği: kalite ve arıtma koşulu; mevcut sıcaklık hesabının kaynak aralığı korunur.
6. Yöntem ve enerji: arpa/patates/marul portföyü, yöntem kapasitesi ve kaynak suyu aynı LP'de çözülür. Eksik yerel su/verim/enerji katsayıları kullanıcı senaryosu olarak görünür. Arktik ısıtma/ışık kalibrasyonu yoktur.
7. Desen ve sonuç: ürün bazında üretim; açık tarla ha ve kontrollü üretim m²; kaynaklara m³; enerji ve kısıtlar. Birimlere ayrı paydalar uygulanır. [Çalışan kuzey simülatörü](FUTURE_NORTH_SIMULATOR.md). Coğrafi sürdürülebilir üretim sınırı haritası henüz hesaplanmaz.

Kuzey modelinin sıcaklığı kara üzeri hava sıcaklığıdır; deniz kaynak suyu sıcaklığına çevrilmez. PWN'nin yerel su kolonu rolü tam da bu ayrı veri ihtiyacında görünür olur.

## E. Saha gerekliliği ve PWN'nin ürün rolü

Beklenen deniz modeli değeri → aynı zaman/konum/derinlikte gözlem → eşleşme kontrolü → kaynak sıcaklığı güncellemesi → **aynı çok ürünlü motor, aynı hedefler ve kısıtlarla** saha sonrası desen. Uygulama eşleşme başarısızsa ikinci hesabı açmaz. [FIELD_TO_PATTERN_UPDATE.md](FIELD_TO_PATTERN_UPDATE.md)

İlk etkileşimli örnek açık simülasyondur. Gerçek dış profil yolu; kayıtlı kaynak kimliği, kalite OK, UTC, GPS ve basınçtan derinlik ister. Tank veya simülasyon kaydı gerçek deniz gözlemi olarak kabul edilmez. Model beklentisi manuel verilirse kaynak URL'si ve kullanıcı beyanı etiketi tutulur; deniz modeli dosyası otomatik alınmış gibi sunulmaz.

Eşleşme toleransları tasarım senaryosudur; KARE/TASE örnekleme protokolü sayılmaz. Bir çift otomatik model kalibrasyonu veya güven yüzdesi üretmez. Enerji değişip optimum üretim payı aynı kalabilir; bu da açıkça gösterilir. Sefer ölçümünün varsayımsal kıyısal su alma noktasını temsil ettiği ayrıca kanıtlanmalıdır.

PWN ana navigasyonda destek modülüdür. Ana ürün kimliği su/üretim karar desteği olarak kalır. Cihazın yapım belgeleri ve Arctic konsepti erişilebilir, fakat karar alanının yerini tutmaz.

## F. Uygulama değişiklikleri

Mevcut FastAPI ve veri/provenans yapısı korunarak benchmark karşılaştırması, kuzey bağlamı ve saha eşleştirme uçları eklendi. Mevcut optimizer'a kapasite kullanımı, kalan kapasite, bağlayıcı kısıt, tercih gerekçesi ve hedef yetişmiyorsa desteklenebilen maksimum üretim hesabı eklendi. Desteklenmeyen arıtma sıcaklığında enerji değeri sıfır yerine eksik gösterilir. PWN parser ve değiştirilemez ham kayıt akışı korunur.

U7'de frontend beş çalışma alanına ayrılmış, 22 Eylül 2026'da 99 test ve 9 tarayıcı etkileşimi geçmişti; bunlar **TESLİM 002'nin tarihsel sonuçlarıdır**. U8 bunların üzerine `planning.py` / `planning_contracts.py`, `/api/planning-context`, `/api/simulate`, `/api/pattern-field-update` uçlarını ve ürün kataloğu/resmî desen veri katmanını ekledi. Ana Türkiye ve kuzey arayüzleri ortak simülasyon sözleşmesine bağlandı. Ürün ekleme, alan/verim/pay/minimum/hedef, dört aşamalı takvim, kaynak bütçesi ve %20 su düğmesi çalışıyor. 22 Eylül 2026 16:51 TSİ'de 13 tarayıcı kontrolü geçti; Konya/Şanlıurfa, kuzey bilinmeyen/örnek portföy, saha güncellemesi/eşleşmeme, PWN CSV ve kanıt çekmecesi denetlendi. Dört çalışma alanı masaüstü/mobilde yatay taşma olmadan kontrol edildi. Kayıt [simulator-smoke.json](verification/simulator-smoke.json); bütün güncel test ve derleme durumu [BUILD_STATUS.md](BUILD_STATUS.md) içindedir.

## G. Korunan sınırlar

Bu dönüşüm gerçek veri ve karar etkileşimini güçlendirir. Fiziksel PWN, Arktik saha verisi, yeni eğitilmiş AI, bağımsız Türkiye validasyonu, yerel toprak/çekilebilir su tahsisi veya kesin coğrafi üretim sınırı üretilmiş sayılmaz. Öncelik yeni ölçümü doğru yere bağlayan, kullanıcı tarafından incelenebilir çalışan bir karar aracıdır.
