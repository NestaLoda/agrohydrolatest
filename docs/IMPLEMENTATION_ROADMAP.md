# Dokuz günlük kritik yol ve sonraki geliştirme

22 Eylül 2026. **U6 ile yazılım/firmware geliştirmesi onaylandı; ilk yazılım kesiti tamamlandı.** API/arayüz, kaynaklı veriye dayanan dar hesap akışı ve PWN profil analizi mevcut; güncel doğrulama ve açıklar [BUILD_STATUS.md](BUILD_STATUS.md) içindedir. Konya, Seyhan–Adana, Gediz–Manisa, GAP–Harran, Trakya–Edirne ve Longyearbyen için 2022–2023 ERA5 reanalizinden 4.380 günlük satır indirildi; istasyon gözlemi veya geleceğe ait projeksiyon değildir [DATA_ACCESS_LOG.md](DATA_ACCESS_LOG.md). U7 ile beş çalışma alanlı dashboard ve ayrı kuzey tek modelinden 14.610 günlük veri paketi eklendi; ayrıntılar PRODUCT_REFOCUS ve NORTH_DATA_PLAN içinde. Fiziksel PWN envanteri, imalat ve deney tamamlanmış değil. Kaynak kodları [ana belgede](PROJECT_SOURCE_OF_TRUTH.md).

## Hedef paket

Mülakatta görülebilir dört çıktı öneriyoruz:

1. Çalışan PWN v0.1 ve kendi ölçümlerimizden profil/tekrar grafiği.
2. Yeni platformun dar kapsamlı, sıfırdan yapılmış karar gösterimi: Türkiye başlangıcı → kuzey senaryosu → kaynak suyu bilgisinin karara etkisi.
3. PWN Arctic v1 CAD/operasyon konsepti; çalışan donanımdan ayrı etiketli.
4. Aynı bilimsel hikâyeyi tamamlayan üç bireysel motivasyon formu ve 5 dakikalık takım anlatımı [U1; F1:7611–7635,8024–8032; önerilen paket].

Bütün Türkiye'yi doğrulayan, tüm yöntemleri ve AI modüllerini içeren platform dokuz günlük hedef değildir. Önce tek ölçüm–karar zincirini görünür yapacağız [U3].

## Kritik yol

**Öğretmenlerle malzeme/devre değerlendirmesi → çalışan iletkenlik + sıcaklık + encoder kaydı → homojen/tabakalı deney → gerçek grafiğin gösterimi → Arktik v1 bağlantısı → prova.**

Buna paralel: **tek proje hikâyesi → üç kişisel bilgi seti → bireysel formlar → 27 Eylül iç teslimi.** Mektuplar donanımın son gün bitmesini beklemeyecek; yalnız o tarihte gerçekten tamamlanan şeyler tamamlanmış diye yazılacak [F1:14–27; U1; Öneri].

## 22–30 Eylül çalışma takvimi

Bu, iki uç tarih dahil **9 takvim günlük** plandır; dokuz tam 24 saatlik çalışma süresi değildir. **30 Eylül 2026 tarihi ve 48 saat kuralı master metinle teyit edildi; kesin saat bilinmiyor.** İç teslim 27 Eylül. U6 ile uygulama izni verildi; yazılımda tamamlanan ilk işler aşağıdaki takvimden öne çekildi. Günler fiziksel iş ve prova hedefidir [U5 §35; U6; E15].

| Gün | Tarih | Kritik iş | Paralel iş | Gün sonunda elde olacak |
|---|---|---|---|---|
| 1 | 22 Eylül | Master sync; öğretmen/hardware paketi; U6 sonrası ilk yazılım kesiti | Kaynaklı veri indirme, hesap/API/arayüz ve PWN yazılım testleri | Belgeler ve çalışan dar yazılım kesiti; fiziksel deney henüz yok |
| 2 | 23 Eylül | Kart, sıcaklık, encoder ve kayıt bağlantıları; iletkenlik ön devresi | Mevcut veri sözleşmesi/arayüzle gerçek kayıt entegrasyonu; form cevap iskeletleri | İlk gerçek ham kayıt hedefi; eksik parça kararı |
| 3 | 24 Eylül | Bilinen çözeltilerde tekrarlanabilir sinyal, encoder mesafe kontrolü | Türkiye/kuzey demo için küçük kaynaklı veri paketi; Arctic v1 blok taslağı | Sensör → dosya → grafik zinciri |
| 4 | 25 Eylül | Homojen kontrol ve güçlü tabakalı kolonun tekrarları | Mevcut karar karşılaştırmasının prova/iyileştirmesi; üç formun ilk tam metni | Gerçek profil ve kontrol grafikleri hedefi |
| 5 | 26 Eylül | Kayıt/derinlik/tekrar sorunlarını düzeltme; mümkünse zayıf geçiş/sıcaklık kontrolü | Arctic v1 CAD konsepti; üretim–kaynak suyu bağı görseli | Gösterilebilir PoC, hata/sınır notu, konsept |
| 6 | 27 Eylül | Başarılı deneyi video ve çevrimdışı dosyayla yedekleme | Üç formu kişisel doğruluk ve ortak hikâye açısından bitirme | Formlar takımın göndermesine hazır; demo yedeği |
| 7 | 28 Eylül | Davetteki gerçek son saate göre form tesliminin ekipçe tamamlanması | Yeni özellik eklemeyi durdurma; canlı demo ve 5 dakikalık prova | Teslim durumu teyitli; taşınabilir demo |
| 8 | 29 Eylül | Taşıma, güç, bağlantı ve çevrimdışı prova | Jüri soruları, rol değişimi/yedek anlatım | Hazır cihaz, grafik, konsept, ekip anlatımı |
| 9 | 30 Eylül | Kısa son kontrol ve mülakat | Son dakika kapsam genişletme yok | Somut araştırma prensibi ve sefer amacı |

Yazılım/firmware için U6 onayı geçerlidir; takvimdeki fiziksel teslimler gerçekleştiğinde kayda geçirilir. E-posta gönderimi bu görev kapsamında yetkilendirilmedi; formları ekip gönderir veya ayrıca açık talimat verir [U6; genel iletişim sınırı].

## Üçüncü gün çalışmayan parçaya yaklaşım

- **DIY EC kararsızsa:** öğretmenle devreyi değerlendirme; mevcut/ödünç uygun aralıklı EC modülüne geçme. Sahte veri üretme veya hazır veriyi kendi ölçümü diye sunma yok.
- **Mutlak EC kalibrasyonu yoksa:** ham/bağıl iletkenlik PoC'sini dürüstçe göster; araştırma sınıfı tuzluluk iddiası ekleme.
- **Encoder gecikirse:** geçici elle işaretlenmiş derinliklerle sensör deneyini sürdür; encoder tamamlanmadıysa v0.1 kapsam açığını açık bırak. Nihai çekirdeğin encoder hedefi korunur.
- **Sıcaklık/iletkenlik yalnız ayrı kaydedilebiliyorsa:** zaman ilişkilendirmesi ve entegrasyonu önceliklendir; yeni sensör ekleme.
- **Uygulama yetişmezse:** kaynaklı senaryo çizimi ve gerçek profil görüntüleyicisiyle araştırma akışını göster; tamamlanmamış platformu hazır ürün diye anlatma.
- **Canlı demo aksarsa:** önceden kaydedilmiş kendi deney videosu ve ham kayıtla devam et [Öneri].

## İşlerin ayrımı

| İş alanı | Yapılacak işler | Bu görevdeki durum |
|---|---|---|
| **Web research / belge araştırması** | Kuzeye kayan uygunluk, veri katalogları, çağrı/strateji, önceki TASE çalışmaları; yöntem/arıtma parametreleri | İlk gerçek reanaliz paketi ve kaynaklı yöntem parametreleri mevcut; yerel kalibrasyon/bağımsız doğrulama eksikleri DATA_ACCESS_LOG'da |
| **Coding** | Yeni backend/frontend/veri sözleşmeleri, fiziksel hesap, optimizer, PWN firmware, profil analizi, gerektiğinde AI | U6 ile onaylı; ilk yazılım kesiti ve testler mevcut. Firmware/donanımın durumu ayrı; BUILD_STATUS'a bakılır |
| **Fiziksel PWN** | İletkenlik devresi, sıcaklık, encoder mekaniği, kolon, kalibrasyon, tekrar deneyleri, yerel kayıt entegrasyonu | İhtiyaç/deney planı hazır; parça ve imalat teyidi yok |
| **Mühendislik konsepti** | Arctic v1 çerçeve/sensör/güç/halat CAD'i ve gemi operasyonu | Gereksinimleri hazır; CAD üretilmedi |
| **Mülakat ve formlar** | Aynı proje, farklı kişisel katkı; gerçek prototip ve sahada yapılacak iş | Çerçeve hazır; üç form bu görevde doldurulmadı |
| **Uzman/lojistik görüşü** | Sensör hedefi, CTD, numune/laboratuvar, gemi uygunluğu | Görüşme gündemi hazır; iletişime geçilmedi |

## Mülakat öncesi ile seçilme sonrası ayrımı

| Teslim | Mülakat öncesi hedef | Seçilme sonrası kapsam |
|---|---|---|
| Bilimsel mimari | Dokuz katman, üç RQ, açık sınırlar ve kanıt haritası | Uygulamalı test sonuçlarıyla revizyon |
| Yeni platform | İlk çalışan kesitin veri/etiket/prova kontrolleriyle mülakat demosuna tamamlanması | Kapsamlı veri entegrasyonu ve üretim sınırı analizi |
| Türkiye | Konya + veri bulunan bir karşılaştırma bölgesinde inandırıcı transfer örneği | Birkaç benchmark/bağımsız yıl ile doğrulama |
| Kuzey üretim | Kaynaklı geleceğe dönük uygunluk örneği; iklim/koşullu üretim farkı | Çoklu iklim modeli ve yerel su/enerji kısıtları |
| PWN v0.1 | Mümkünse çalışan düzenek, kontrol/tekrar, gerçek profil ve hata/sınır notu | Arctic v1'e girdi olan deney tecrübesi |
| Arctic v1 | CAD/engineering concept, işlevsel BOM, doğrulama planı; henüz CAD yapılmadı | Soğuk/basınç/sensör tasarımı, reference CTD ve deniz testi |
| Sefer/numune | Rotaya bağımlı olmayan protokol ve uzman soruları | İzinli saha, kesin derinlik/panel, gerçek numune ve analiz |
| Takım/mülakat | Üç bireysel form, 5–10 dakika anlatım, Q&A, dürüst demo yedeği | Fiilî görev ve veri paylaşımı |

Bu tablo uzun vadeli hedefleri de içerir. İlk audit'in yalnız dokümantasyon durumu U6 sonrası yazılım geliştirmesiyle aşıldı; güncel tamamlanma [BUILD_STATUS.md](BUILD_STATUS.md) üzerinden izlenir [E17]. Detaylı demo kararları [DEMO_PLAN.md](DEMO_PLAN.md), saha planı [ARCTIC_FIELD_PLAN.md](ARCTIC_FIELD_PLAN.md).

### Kritik arıza ve yedekler

| Bağımlılık | Başarısızlık | Yedek ve doğru etiket |
|---|---|---|
| DIY EC | Tekrarlanabilir sinyal yok | Uygun aralıklı ödünç EC çözümü; o da yoksa çalışan PoC iddiasını çıkar, tamamlanan parçaları ve test planını göster |
| Kalibrasyon/reference | Doğruluk bilinmiyor | Ham/bağıl sinyal ve tekrarlar; mutlak tuzluluk/hata iddiası yok |
| Encoder | Mesafe kaydı aksıyor | İşaretli elle derinlik; encoder entegrasyonu eksik diye belirtilir |
| Yerel logger | Dosya eksik/bozuk | Kontrollü laboratuvarda zamanlı bilgisayar kaydı; self-contained logger hedefi tamamlanmadı |
| Türkiye verisi | Bağımsız gözlem yok | Kaynaklı transfer demonstrasyonu; bilimsel validation etiketi yok |
| Kuzey hesap | Yeni analiz yetişmiyor | Kaynaklı literatür örneği; özgün model sonucu diye sunulmaz |
| UI/hesap | Uçtan uca demo yetişmiyor | Gerçek çalışan bölüm + açık tasarım akışı; ürünün tamamı çalışıyor denmez |
| Arktik CAD | Ayrıntılı model yetişmiyor | Boyutsuz yerleşim/operasyon şeması; mühendislik üretim onayı değildir |
| Canlı gösterim | Mülakatta cihaz/bağlantı aksıyor | Önceden kaydedilmiş kendi gerçek deney videosu + ham dosya |
| Kişisel form bilgisi | Rol/deneyim eksik | Ortak bilim metni hazır; kişisel boşluklar öğrenci tarafından doldurulur, tahmin edilmez |

## Onaylanan ilk uygulama akışı

U6 ile açılan ilk kesit aşağıdaki akışı esas alır; gerçek tank kaydının eklenmesi fiziksel çalışmayı bekler:

1. Kaynak ve sürümü belli küçük veri paketi.
2. Bir üretim hedefi, az sayıda ürün/yöntem/kaynak seçeneği.
3. Su ve enerji hesabını gösteren karşılaştırma; eksik katsayılar açık senaryo varsayımı.
4. PWN ham dosyasını yükleyip profil ve geçişi gösterme.
5. İlgili kaynak suyu girdisi değişince sonuç aralığı/seçenek farkını gösterme.

Tam ülke haritası, kullanıcı hesabı, bulut dağıtımı, otomatik AI eğitimi, çok sayıda sensör ve her üretim yöntemi bu ilk akıştan sonra gelir [Öneri; U1,U3].

## Dokuz gün sonrasındaki yol

| Aşama | Üretilecek gerçek kanıt | Bir sonraki adım için yeterli ilerleme |
|---|---|---|
| Türkiye modeli | Birkaç benchmark bölge/yılda karşılaştırma; su/üretim çıktısı | Yöntemin nerede işe yarayıp nerede parametre istediği biliniyor |
| Kuzey frontier | Ürün/yönteme özgü iklim, zemin, su ve enerji katmanları | İklimsel uygunlukla koşullu üretim uygunluğu arasındaki fark açık |
| Arctic v1 geliştirme | Uzman görüşü, sensör/CTD testleri, örnekleme ve deniz donanımı | Sefer ekibiyle uygulanabilir operasyon tanımlı |
| Sefer | Profiller, referans eşleşmeleri, metadata, uygun fiziksel örnekler | Kaynak suyu/model farkını değerlendirecek kayıt elde edilmiş |
| Sefer sonrası | Kalibrasyon, kaynak izleme, arıtma/üretim etkisi, belirsizlik | Saha bilgisinin karar katkısı veya katkı sınırı ölçülmüş |
| Paylaşım | Açıklanabilir karar çıktısı, rapor, uygun izinle veri | Yeni araştırmacının sonucu izleyebilmesi |

Bu uzun vadeli planın tarih ve bütçesi seçilme, veri erişimi ve uzman desteğiyle netleşir. Şimdi en değerli ilerleme, “neden gidiyoruz, ne ölçeceğiz, bu ölçüm neyi değiştirecek?” üçlüsünü çalışan ilk düzenekle anlatabilmektir [U1,U3].
