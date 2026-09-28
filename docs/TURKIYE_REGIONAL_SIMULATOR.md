# Türkiye bölgesel ürün deseni simülatörü

22 Eylül 2026 — TESLİM 003 veri paketi. Ürün seçimi → mevcut alan deseni → kullanıcı senaryosu → hesap → önerilen alan deseni akışı için **beş ilin gerçek istatistiklerinden 21 ürün kaydı** edinildi. Sayısal sözleşme `data/agriculture/region_baselines.json`; dört özgün PDF ve bir özgün DOCX `data/agriculture/raw/` altında SHA256 içeren adlarla korundu.

## Veri ölçeği ve yılı

| Arayüzdeki bölge bağlamı | İstatistiğin gerçek coğrafyası | Veri yılı | Seçilen ürünler | Seçilmiş ekiliş alanı toplamı, ha |
|---|---|---:|---|---:|
| Konya | Konya ili | 2023 | Buğday, arpa, dane mısır, şeker pancarı, patates | 1.280.141,4 |
| Seyhan / Adana | Adana ili | 2024 | Buğday, dane mısır, ayçiçeği, pamuk | 294.433,3 |
| Gediz / Manisa | Manisa ili | 2024 | Buğday, arpa, dane mısır, kütlü pamuk | 150.966,5 |
| Harran / Şanlıurfa | Şanlıurfa ili | 2024 | Buğday, arpa, pamuk, dane mısır | 790.896,0 |
| Trakya / Edirne | Edirne ili | 2024 | Buğday, yağlık ayçiçeği, çeltik, arpa | 323.327,6 |

Bu alan toplamları **seçilmiş ürünlerin ekiliş alanı paydasıdır**. Havza/ilçe istatistiği, bütün ilin tarım alanı veya aynı anda tahsis edilebilir benzersiz fiziksel arazi değildir. İkinci ürün ekimleri aynı parseli bir yılda yeniden sayabilir. Simülatörde fiziksel kapasite ayrıca kullanıcı senaryosu olarak tanımlanmalı; örtüşen takvimler veya ikinci ürün sıra planı çözülmeden il toplamları tek bir arazi kısıtına dönüştürülmemelidir.

## Kaynaklar ve dar kapsamları

- **Konya:** [Konya Tarımı, Haziran 2024](https://konya.tarimorman.gov.tr/Belgeler/kitap/%C4%B0l_Tar%C4%B1m_ve_Orman_haziran_24_v3_2024.pdf), PDF s.12–13 / basılı s.3–4, Tablo4'ün **2023** sütunları. Alan dekar, üretim ton. Buğday durum+diğer; arpa biralık+diğer olarak toplandı. Yeşil ot ve silaj ayrı tutuldu. Kaynağın 2024 baskısı verinin 2024 olduğu anlamına gelmez.
- **Adana:** [2025 Faaliyet Raporu](https://adana.tarimorman.gov.tr/Belgeler/Strateji_Adana_2025_Yili_Faaliyet_Raporu.pdf), PDF/basılı s.21, Tablo7. Dipnot açıkça **2024 resmî verileri** der. Kaynak yuvarlanmış kg/da verim de verir; uygulamanın tutarlı üretim hesabı için üretim/alan oranı ayrıca hesaplandı. Pamuk alt tipi ve ayçiçeği alt tipi tabloda açık yazılmadığından kesinleştirilmedi.
- **Manisa:** [2024 Brifingi](https://manisa.tarimorman.gov.tr/Belgeler/Brifing%202024/Brifing2024.pdf), PDF s.7 / basılı s.6, **TÜİK 2024** önemli tarla bitkileri. Buğday iki alt kategorinin toplamıdır; PDF s.10/basılı s.9 toplamı ile eşleşir. Bağ, zeytinlik ve diğer çok yıllık alanlar bir sezonda dönüşebilir varsayılmadığı için bu ilk yıllık ürün motorundan dışarıdadır; Manisa'nın tüm tarımı temsil edilmez.
- **Şanlıurfa:** [2025 Faaliyet Raporu DOCX](https://sanliurfa.tarimorman.gov.tr/Lists/SolMenu/Attachments/85/2025%20YILI%20%C5%9EANLIURFA%20%C4%B0L%20TARIM%20VE%20ORMAN%20M%C3%9CD%C3%9CRL%C3%9C%C4%9E%C3%9C%20FAAL%C4%B0YET%20RAPORU.docx), “Bitkisel Üretim ve Bitki Sağlığı / Şanlıurfa İli Tarla Bitkileri Verileri” tablosunun **2024** sütunları. Kaynak alan birimi **hektar**; tekrar 10'a bölünmedi. DOCX için sabit PDF sayfa numarası uydurulmadı. Pamuk alt tipi tabloda yazmıyor. 2025 sütunları bu başlangıç veri setine alınmadı.
- **Edirne:** [2025 Faaliyet Raporu](https://edirne.tarimorman.gov.tr/Belgeler/Edirne%20%C4%B0l%20Tar%C4%B1m%20ve%20Orman%20M%C3%BCd%C3%BCrl%C3%BC%C4%9F%C3%BC%202025%20Y%C4%B1l%C4%B1%20Faaliyet%20Raporu.pdf), PDF s.21/basılı s.15, Tablo8'in **2024** sütunları. Çeltik, işlenmiş pirinç değildir. Arpa küçük olsa da kaynakta bulunan ortak tahıl adayıdır.

Resmî dosyalardaki rakamlar elle satır/sütun kontrolüyle aktarıldı. Bunlar `OFFICIAL_STATISTICS` olarak etiketlenir; kendi saha ölçümümüz veya yeni model çıktımız değildir. Resmî istatistiklerin çoğaltma lisansı ayrıca doğrulanmadı; özgün belgeler kaynak denetimi ve atıf için saklanır.

## Başlangıç alanı ve üretim

| İl / yıl | Ürün | Alan, ha | Üretim, ton |
|---|---|---:|---:|
| Konya 2023 | Buğday | 596.686,6 | 2.239.936 |
| Konya 2023 | Arpa | 385.201,1 | 1.393.244 |
| Konya 2023 | Dane mısır | 185.505,4 | 2.043.903 |
| Konya 2023 | Şeker pancarı | 101.947,3 | 7.659.563 |
| Konya 2023 | Patates | 10.801,0 | 462.545 |
| Adana 2024 | Buğday | 127.427,6 | 452.219 |
| Adana 2024 | Dane mısır | 79.785,1 | 917.877 |
| Adana 2024 | Ayçiçeği | 73.869,2 | 203.446 |
| Adana 2024 | Pamuk | 13.351,4 | 63.173 |
| Manisa 2024 | Buğday | 87.142,4 | 216.089 |
| Manisa 2024 | Arpa | 35.547,9 | 74.365 |
| Manisa 2024 | Dane mısır | 13.597,1 | 151.830 |
| Manisa 2024 | Kütlü pamuk | 14.679,1 | 81.684 |
| Şanlıurfa 2024 | Buğday | 339.117,0 | 1.505.887 |
| Şanlıurfa 2024 | Arpa | 149.747,0 | 410.361 |
| Şanlıurfa 2024 | Pamuk | 196.080,0 | 922.012 |
| Şanlıurfa 2024 | Dane mısır | 105.952,0 | 898.766 |
| Edirne 2024 | Buğday | 141.242,0 | 547.866 |
| Edirne 2024 | Yağlık ayçiçeği | 126.606,0 | 173.878 |
| Edirne 2024 | Çeltik | 48.630,6 | 391.101 |
| Edirne 2024 | Arpa | 6.849,0 | 26.956 |

Her kaydın verimi `üretim_ton × 1000 / alan_ha` olarak hesaplandı ve `DERIVED_FROM_OFFICIAL_STATISTICS` etiketini taşır. Resmî tablonun yuvarlanmış verim sütunu veya potansiyel/verim hedefi gibi gösterilmez. İl ortalama verimi, senaryoda sabit taşınan bir katsayı olabilir; su stresi veya sıcaklık değiştiğinde verimin sabit kalacağı bilimsel olarak kanıtlanmış değildir.

## Kullanıcı akışı ve motorla bağlantı

1. Bölge seçildiğinde ürün alanı ve üretim tablosu, gerçek **il adı ve veri yılıyla** yüklenir.
2. Kullanıcı kendi çalışma alanını, başlangıç paylarını, su bütçesini, sulama randımanını, iklim varsayımını ve ürün bazındaki minimum üretim/pay kısıtlarını düzenleyebilir. Değişiklikler `USER SCENARIO` olur; resmî başlangıç kaydı değiştirilmez.
3. Aynı ürünlere ait takvim/Kc ve gerçek yeniden analiz girdileriyle dönemsel su hesabı yapılır. İl istatistiği ile tek iklim hücresi eşleştirmesi açık **transfer varsayımıdır**.
4. Karar değişkeni ürün alanıdır. Mevcut desen ve önerilen desen yan yana gösterilir; su dengesi, ürün bazında üretim ve gerçekten bağlayan kısıtlar açıklanır.
5. Beş bölgeli karşılaştırma, tek bölge simülasyonunun ikincil değerlendirmesidir. Buğday beş ilin tamamında; arpa Konya/Manisa/Şanlıurfa/Edirne'de gerçek kayıtlara dayanır.

Bu belge veri bağlantısını ve kabul sınırını tanımlar; çalışan optimizasyonun yöntem ve test durumu `CROP_PATTERN_ENGINE.md`, `PATTERN_CONSTRAINTS.md` ve `BUILD_STATUS.md` içinde tutulur. Eski Konya proje raporu ayrı tarihsel araştırma sonucudur; bu yeni resmî baseline ile karıştırılmaz.

## Çalışan motorun mevcut sözleşmesi

`backend/planning.py` il baseline'ını okurken özgün kaynak yolunun veri dizini içinde olmasını ve dosya hash'ini doğrular. Resmî desen, düzenlenebilir kullanıcı deseni ve optimize desen ayrı çıktılardır. Türkiye başlangıç senaryosunda toplam alan, seçilmiş ürünlerin ekiliş toplamından başlatılır; **bu bir senaryo kapasitesidir**, doğrulanmış benzersiz il arazi yüzölçümü değildir. Motor henüz parsel bazında ürün ardışıklığını çözmez.

Başlangıç su bütçesi, su hesabı tamamlanabilen mevcut ürünlerin modellenmiş brüt gereksiniminden oluşturulur; DSİ su tahsisi veya gözlenmiş çekim değildir. Eksik ürün gereksinimi varsa tüm mevcut desenin su toplamı eksik kalır. Kullanıcı su kaynağı hacmini, alanı, ürün paylarını, hedefleri ve takvimleri değiştirebilir. Başlangıç %50 ürün üretim tabanı ve eşit hedef ağırlıkları **tasarım senaryolarıdır**. Varsayılan en az ekilen alan oranı sıfırdır (`min_cultivated_fraction=0`); boş kalan alan ayrıca raporlanır. Kullanıcı alanın tamamını kullanmayı seçerse bu ilave kısıtın uygulanamazlık yaratabileceği açıkça gösterilir.

Su yolu `ETc=Kc×ET₀` → yağış/toprak deposu sonrası açık → zamanında tamamlayıcı sulama varsayımıyla net gereksinim → randımanla brüt m³/ha hesabıdır. Manuel net sulama girildiğinde kaynak `USER_SCENARIO` olur. Bu yol su stresinden gerçekleşen verimi hesaplamaz.

**Çeltik veri kapısı:** `rice` için manuel dönemsel net gereksinim yoksa motor `insufficient_data` döndürür; ETc'yi toplam tava sulaması gibi kullanmaz. Çeltik mevcut desende kalır, fakat aday su hesabı eksik olduğu için otomatik açık tarla seçeneği açılamaz. Pozitif minimum üretimi korunursa optimizasyon uygulanamaz olabilir; minimum sessizce kaldırılmaz. Kullanıcı kaynaklı toplam net gereksinim senaryosu verebilir veya çeltik adayını ve ilgili minimumunu açıkça değiştirebilir. Bunun su/perkolasyon doğrulaması ayrıca gerekir.

Optimizasyon, ürünlerin kilogramlarını toplayarak en ağır ürünü seçmez: önce ürün başına hedefin en çok %100 karşılanma oranlarının ağırlıklı toplamını en yükseğe çıkarır; sonra aynı hedef başarısında brüt su çekimini azaltır. Açık tarla hektarı ile sera/hidroponik yetiştirme yüzeyi m² ayrı kapasitelerdir. Model bütünlük kontrolleri ayrı, saha doğrulaması ayrıdır.

## Bilimsel ve operasyonel açıklar

- 2022–2023 tek hücre ERA5 ile 2024 il deseni birlikte kullanılıyorsa sonuç **seçilmiş iklim altında tarihsel deseni çalıştırma senaryosudur**; aynı yıl saha doğrulaması değildir.
- Ürün bazında kuru/sulu alan ayrımı, çeşitler, yerel ekim/hasat ve çoklu ekim takvimi bu tablolardan çıkmaz. Kaynaklı genel takvimler yerel ölçüm gibi sunulmaz.
- Fiilî su hakkı, sezonluk tahsis, güvenilir kaynak hacmi, toprak deposu ve sulama randımanı istatistik tablolarında yoktur; kullanıcı senaryosu/ayrı kaynak gerekir.
- Tahıl, yaş yumru, kök ve pamuk tonları ortak besin veya ekonomik değer değildir. Salt toplam ton maksimize etmek yüksek yaş kütleli ürüne yapay avantaj verebilir; ürün bazında üretim korunması veya açık hedef gerekir.
- Çeltikte ETc, su altında yetiştirmenin toplam tarla giriş suyunu tek başına açıklamaz. Göllendirme, sızma ve perkolasyon ayrıca ele alınmadan tam sulama talebi iddiası kurulmaz.
- Pamuk Adana/Şanlıurfa tablosunda alt tip açık değildir. Verimler kütlü ölçeğiyle uyumlu olsa da bu çıkarım, doğrulanmış lif/kütlü tanımı yerine geçmez.
- Seçilen ürün listeleri eksiksiz il desenleri değildir. Bir sonraki veri işi fiziksel parsel/ilçe ölçeğinde takvim, sulama ve verim doğrulamasıdır.

## Bu paketin kontrolü

22 Eylül 2026'da beş özgün belgenin SHA256 kayıtları doğrulandı; 21 kaydın alan/üretim/verim birimleri ve hesap eşitliği kontrol edildi. Konya buğday ve arpa alt kategori toplamları; Manisa buğday toplamı ayrı kaynak tablosuyla karşılaştırıldı. Eksik sayısal veri uydurulmadı. Bu kontroller kaynak aktarımının tutarlılığıdır; modelin agronomik doğruluğunun testi değildir.
