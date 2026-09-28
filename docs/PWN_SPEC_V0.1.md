# PWN v0.1 ihtiyaç listesi ve prensip gösterimi

22 Eylül 2026 — U6 durum güncellemesi. **Bilişim ve teknoloji öğretmenlerine verilecek çalışma belgesi.** Donanım envanteri henüz bilinmiyor; aşağıdaki liste sahip olunan parçalar değil ihtiyaçlardır. Yazılım/firmware geliştirmesi onaylandı; ilk PWN CSV/analiz yazılımı mevcut. Fiziksel cihaz, tank deneyi veya Arctic CAD tamamlanmış sayılmıyor. Güncel yazılım durumu [BUILD_STATUS.md](BUILD_STATUS.md), uygulanabilir ilk yapım paketi [PWN_TEACHER_BRIEF_TR.md](PWN_TEACHER_BRIEF_TR.md) içindedir [E17](EVIDENCE_MAP.md).

Bu belgedeki malzeme/kurulum/iş akışı seçimleri mühendislik önerisidir [E16](EVIDENCE_MAP.md). V0.1'in CTD ve tuzluluk iddia sınırları [E13](EVIDENCE_MAP.md), mülakat tarihi ve iç teslim hedefi [E15](EVIDENCE_MAP.md) ile izlenir. Korunan F/W atıflarının ayrıntıları [ana kaynak kaydındadır](PROJECT_SOURCE_OF_TRUTH.md).

## Öğretmenlere anlatılacak iş

Kontrollü bir su kolonunda farklı iletkenliğe sahip tabakaları algılayıp derinliğe göre grafiğe döken küçük bir cihaz yapmak istiyoruz. Sensör başlığı aşağı inerken iletkenlik sinyali, sıcaklık, encoder'dan hareket/derinlik ve zaman kaydedilecek. Kayıt internetsiz saklanacak; bilgisayarda tabaka geçişi görülecek. İlk hedef, bu araştırma prensibinin çalıştığını gerçek tekrarlı deneyle göstermek. Arktik için nihai CTD'yi dokuz günde üretmiyoruz [U1; F1:7611–7635].

İlk kurulumda elektronik ve güç **suyun dışında**, prob başlığı suyun içinde olacak. Sensör kablosu yük taşımayacak; taşıyıcı ip ve mekanik tutucu ayrı olacak. Böylece tank gösterimi için basınç kabı yapmak zorunda kalmayız [F1:2953–2985,3503–3523; önerilen tasarım].

Bu cihazın göstereceği şey, ana karar destek sistemine fiziksel profil kazandıran ölçüm prensibidir. Tank deneyi gelecekteki Arktik su miktarını veya üretim uygunluğunu kanıtlamaz. Arktik bağlantısı model–gözlem farkı; ilgili kıyısal kaynak senaryosunda ayrıca kaynak karakterizasyonu → arıtma → kullanılabilir su → enerji/su koşulu → üretim kararıdır [E06, E13, E19](EVIDENCE_MAP.md).

## Zorunlu malzeme ve araçlar

Adetler bir çalışan prototip için planlama önerisidir. Fiyat/stok teyidi yapılmadı; satın alma emri değildir.

| İhtiyaç | Adet | Ne işe yarayacak / seçim ölçütü |
|---|---:|---|
| ESP32 geliştirme kartı **veya** uygun Deneyap kartı | 1; varsa 1 yedek | Sensör okuma, encoder sayma, zaman ve kayıt. Ekip hangi kartı biliyorsa onu seçsin; kart modeli/pin gerilimleri kesinleşsin [W24]. |
| Suya uygun sıcaklık probu | 1; varsa 1 yedek | DS18B20 paketli prob bir PoC adayı. Satıcının prob sızdırmazlığı, kablo boyu ve tepki süresi kontrol edilmeli; çip belgesi deniz basıncı dayanımı sağlamaz [W22]. |
| DIY iletkenlik hücresi | 1; mümkünse yedek elektrot çifti | Sabit aralık ve sabit açık yüzeyli elektrotlar; temizlenebilir inert taşıyıcı. Elektrot malzemesi ve geometri elektronik öğretmeniyle seçilir. |
| İletkenlik ölçüm ön devresi | 1 | Alternatif kutuplama/AC uyarım, akım sınırlama ve kart girişine uygun sinyal şartlandırma. Salt iki elektrodu doğrudan ADC'ye bağlamak kalibre EC ölçümü sayılmaz [Öneri]. |
| Encoder ve sabit çaplı ölçüm tekeri / kaymayan aktarım | 1 set | İninilen mesafeyi kaydetmek. Çok katlı sarılan makaranın değişen çapı ölçümü bozacağından ölçüm tekeri tercih edilir [Öneri]. |
| microSD ve uygun modül **veya** kartta yeterli dahili kayıt | 1 set | Yerel, bağlantısız kayıt. Seçilen Deneyap modelinde kart yuvası varsa ikinci modül gerekmeyebilir; model belgesi kontrol edilir. |
| Uygun USB/batarya güç kaynağı ve veri kablosu | 1 set | Düşük gerilimli tank deneyi ve kayıt; güç ünitesi kuru tarafta. Süre gerçek tüketimle ölçülür. |
| Breadboard/perfboard, dirençler, bağlantı kabloları, konnektörler | 1 set | İlk ölçüm devresi, düzenli bağlantı ve değiştirilebilir sensörler. |
| Şeffaf dikey kolon veya yeterince derin şeffaf kap | 1 | Öneri: yaklaşık 0,6–1 m çalışma yüksekliği; gerçek malzemeye göre uyarlanır. Cetvel, sağlam taban ve dökülme tepsisi gerekir. Boyut bilimsel standart değil. |
| Prob taşıyıcısı, ip, kılavuz ve elle iniş mekanizması | 1 set | Sensörleri yakın konumda tutmak; tabakayı az bozarak tekrarlanabilir iniş yapmak. |
| Cetvel/mezura ve işaretli derinlik referansı | 1 | Encoder'ı bilinen mesafelerde doğrulamak; yüzey sıfırını kaydetmek. |
| Temiz kaplar, kontrollü su/tuz çözeltisi hazırlama gereçleri | 1 set | Homojen kontrol ve tabakalı kolon oluşturmak. Tuz miktarı tek başına sertifikalı EC standardı sayılmaz. |
| Multimetre, lehim ve temel el aletleri | Ortak kullanım | Besleme, bağlantı ve devre kontrolü. |
| Dizüstü bilgisayar | 1 | Kayıt alma, dosya kontrolü ve profil gösterimi. |

**İletkenlik devresi için öncelikli destek:** Ölçüm aralığına uygun analog tasarım, giriş koruması, gürültü ve kalibrasyon. ESP32 ADC'sinin gürültü/kalibrasyon sınırlılıkları üretici belgesinde bulunuyor; gerekirse harici ADC eklenebilir, fakat harici ADC tek başına elektrot/ön devre sorununu çözmez [W23].

## Okuldan veya laboratuvardan ödünç istenecekler

| Öncelik | Araç | Neden |
|---|---|---|
| Çok yararlı | Ölçüm aralığı bilinen referans EC metre ve taze EC standartları | “Sinyal değişiyor”dan kalibre iletkenliğe geçmek ve bağımsız kontrol yapmak |
| Çok yararlı | Referans termometre | Sıcaklık probu sapması ve farklı sıcaklıklarda davranış |
| Yararlı | Osiloskop | AC/polarite uyarımının ve ADC sinyalinin çalıştığını görmek |
| Yararlı | Hassas terazi, ölçülü kap/pipet | Tekrarlanabilir çözelti hazırlama; bunlar EC metre yerine geçmez |
| Varsa | 3D yazıcı/atölye | Prob tutucusu ve ölçüm tekeri; el yapımı tutucu da yeterli |

Referans EC cihazı bulunamazsa PoC yapılabilir; çıktı **ham/bağıl iletkenlik sinyali** diye adlandırılır. “Şu doğrulukta salinity ölçtük” denmez. Kalibrasyon ve bağımsız doğruluk değerlendirmesi ayrı şeylerdir [U1; W15,W18; Öneri].

## Alternatif yol ve şimdi alınmayacaklar

DIY iletkenlik devresi ilk birkaç günde tekrarlanabilir sinyal üretmezse, mevcut/ödünç bir EC modülüyle aynı gösterim yapılabilir. Modülün aralığı deney çözeltisine uygun olmalı. Düşük aralıklı TDS sensörü deniz suyu sensörü diye kullanılmaz; TDS, EC ve pratik tuzluluk aynı çıktı değildir [W18; Öneri].

Dokuz gün için zorunlu değil: pahalı deniz EC hücresi, basınç sensörü, turbidity, pH, çözünmüş oksijen, GPS modülü, otomatik numune, motorlu vinç, sualtı kablosuz iletişim, özel PCB ve basınca dayanıklı gövde. Bunlar ek özellik yarışı yüzünden çekirdek deneyi geciktirmemeli [U1; F1:3257–3268,3751–3796,4198–4203].

## Görev paylaşımı

| Ekip | İstenen katkı | Çıktı |
|---|---|---|
| Elektronik/teknoloji | İletkenlik hücresi ve analog devre; sıcaklık probu; kararlı güç | Tekrarlanabilir ham sinyal ve devre bağlantı şeması |
| Mekanik/atölye | Kolon, tutucu, ölçüm tekeri, elle iniş | Kaymayan, derinliği kontrol edilebilir deney düzeneği |
| Bilişim | Onaydan sonra firmware, kayıt formatı ve grafik | C/T/encoder/zamanı ilişkilendiren dosya ve profil |
| Öğrenciler | Çözelti hazırlama, kontrol/tekrar, kayıt ve anlatım | Kendi yaptıkları deneylerin grafiği, fotoğrafı ve kısa açıklaması |

Kişisel roller henüz isimlere atanmadı. Yardım alınan kısımlar da dürüstçe belirtilir; öğrenciler her bileşenin amacını ve kendi katkılarını açıklayabilmelidir [U1; Öneri].

## Veri ve çalışma akışı

1. Cihaza cast/deney kimliği ver; sensörleri kontrol et, encoder yüzey sıfırını kaydet.
2. Probun aşağı inişini elle ve yavaş yürüt; gerçek iniş süresi ve yöntemi kaydedilsin.
3. Zaman, ham iletkenlik, sıcaklık ve encoder aynı dosyada saklansın. Başlangıç hedefi yaklaşık 1 kayıt/s olabilir; gerçek hız ve prob tepki süresi ölçülür. Sensörler aynı anda okunmamışsa ayrı zaman damgası tutulur.
4. İniş ve çıkış ayrı işaretlensin; çıkış kaydı yeni bağımsız deney gibi sayılmasın.
5. Dosya bilgisayara alınsın; sıcaklık ve iletkenlik derinliğe karşı ayrı eksenlerde gösterilsin.
6. İlk geçiş tespiti yumuşatma + iletkenlik gradienti/eşik yöntemiyle yapılsın. Eşik açık olsun; AI gerekmez.

Bu akış tasarımdır, yazılmış firmware değildir. Kayıt hızı gerçek dikey çözünürlük demek değildir; prob gecikmesi, iniş hızı ve karışma birlikte belirler [U1; F1:3076–3088; mühendislik çıkarımı].

## En küçük anlamlı deney paketi

| Deney | Gösterdiği şey | Başlangıç tekrar hedefi |
|---|---|---:|
| Tek sıcaklıkta homojen su | Sahte tabaka alarmı oluşuyor mu? | 3 |
| Aynı sıcaklığa yakın, güçlü iletkenlik farkı olan kolon | Prensip çalışıyor mu? | 3 |
| Daha zayıf iletkenlik farkı | Algılanabilir sınır nereye yaklaşıyor? | 3; süre kalırsa |
| Benzer çözeltide sıcaklık farkı | Sıcaklık etkisi tabaka gibi yorumlanıyor mu? | 3; süre kalırsa |

Tekrar sayıları istatistiksel yeterlilik garantisi değil, dokuz günlük PoC önerisidir. Kolon her profilde bozulabileceğinden profil sırası/süre ve yeniden hazırlama kaydedilir. “Gerçek sınır” yalnız gözle görülen boya çizgisiyle kabul edilmez; mümkünse ayrı derinliklerden EC referansı alınır. Referans yoksa bilinen fiziksel tabaka düzeniyle nitel karşılaştırma yapılır [Öneri].

İlk tabakalı deney için benzer sıcaklıktaki yüksek tuzlu/yoğun çözelti alta, seyreltilmiş çözelti üste yerleştirilir. Üst katman karıştırmadan yavaş eklenir; profil almadan önce referans noktaları ve yüzey sıfırı kaydedilir [Öneri: basit deney hazırlığı].

## Başarıyı nasıl yazacağız?

PoC'nin minimum başarısı: gerçek sensör verisinin derinlikle kaydedilmesi, homojen ve tabakalı düzeneklerin ayırt edilebilmesi, sonucun tekrar grafikleriyle gösterilmesi ve kayıtların geri açılabilmesi. Sayısal doğruluk eşiği donanım/referans görülmeden icat edilmez [U1; Öneri].

Ölçülebilirse raporlanacaklar: referansa göre EC/sıcaklık sapması, tekrarlar arası fark, geçiş derinliği hatası, homojen kontrolde yanlış alarm, kayıp kayıt ve gecikme. Kullanılacak ifade: “Kontrollü düzende iletkenlik geçişini gösteren çalışan araştırma prensibi prototipi.” Kullanılmayacak ifade: “Arktik için doğrulanmış CTD” [U1].

## Mülakatta masaya konacak paket

- Çalışan prob ve şeffaf kolon.
- Kendi deneyinizden bir homojen ve bir tabakalı profil.
- Tekrar grafiği ve kısa hata/sınır notu.
- Sensör → kayıt → profil → hedefli numune fikri → karar sistemi bağlantısını gösteren tek şema.
- Yanında ayrı etiketli Arctic v1 tasarımı [U1; F1:8024–8032].

Bu liste hedef pakettir; her parçaya o günkü gerçek durum yazılır. Kendi tank verisi `ölçüm`, dış kaynaktan alınan profil `dış gözlem/model`, yapay profil `simülasyon` olarak görünür. Gerçek deneyin yerini doldurmak için örnek sayı üretilmez [E17–E18](EVIDENCE_MAP.md).

## Kritik parça çalışmazsa

| Sorun | Devam yolu | Dürüstçe belirtilecek sınır |
|---|---|---|
| DIY iletkenlik kararsız/ölçüm aralığı dışında | Öğretmenle ön devre kontrolü; uygun aralıklı ödünç/hazır EC modülü | EC kanalı çalışmıyorsa tabaka algılama gösterildi denmez |
| Mutlak EC referansı yok | Ham/bağıl sinyal ve aynı koşuldaki tekrarları göster | EC doğruluğu veya mutlak salinity sonucu yok |
| Sıcaklık probu çalışmıyor | Yedek prob; geçici olarak dış termometreyle kayıtlı sabit sıcaklık deneyi | Entegre sıcaklık kanalı ve sıcaklık düzeltmesi tamamlanmadı |
| Encoder kayıyor/gelmedi | Cetvelle işaretli konumlarda durarak ölçüm; manuel derinlik kaydı | Encoder tabanlı tam profil henüz yok; derinlik kaynağı `manuel` |
| microSD kayıt sorunu | Kartta yeterli bellek varsa yerel dosya; geçici USB ile bilgisayara kayıt | USB kaydı cihazın bağımsız yerel kayıt özelliğinin tamamlandığı anlamına gelmez |
| Kart/güç/bağlantı arızası | Mevcut yedek kart, kablo veya kararlı kuru taraftaki güç; modülleri ayrı kontrol et | Bütünleşik çalışan cihaz yerine tamamlanan alt iş gösterilir |
| Kolon/tutucu gecikmesi veya tabakanın karışması | Sağlam basit tutucu; yeniden hazırlanmış kolon; gerekirse ayrı kaplarda sensör kontrolü | Ayrı kap deneyi dikey profil/haloklin gösterimi değildir |
| Canlı demo çalışmıyor | Daha önce kaydedilmiş kendi ham verisi ve deney videosu | Ekranda `önceden kaydedilmiş gerçek deney`; kayıt yoksa yalnız konsept |

Bu yedekler hedef kapsamı gizlice değiştirmez; hangi işin tamamlandığını korur. Ayrıntılı test ve veri kaydı [PWN_VALIDATION_PLAN.md](PWN_VALIDATION_PLAN.md), jüri gösterimi [DEMO_PLAN.md](DEMO_PLAN.md) içindedir [E16–E17](EVIDENCE_MAP.md).
