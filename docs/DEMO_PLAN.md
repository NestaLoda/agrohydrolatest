# 23 Eylül 2026 — TESLİM 024 güncellemesi

Kuzey ana ekranı artık mevcut yıldan 2100’e girilebilir tek yıl hesabı kullanır; 20 yıllık dönem seçimi ana akış değildir. Kaynak NASA CMIP6 model-yıl günlük dizileri yeniden hesaplanır, interpolasyon yapılmaz. Açılış 2026 senaryosu canlı hava değildir; ERA5 referansı 2015–2025 kalır. Su kaynakları kaydırıcı, alan girilebilir ve Tarım Güvencesi Kuzey başlığının yan dalıdır. Ayrıntı ve sınırlamalar: `NORTH_YEAR_CONTROLS_024.md`; jüri/model anlatımı: `MODEL_NASIL_CALISIYOR.md`. Önceki dönem anlatımları aşağıda tarihsel bağlamdır.

# Güncel yön — 23 Eylül 2026 / TESLİM 023

Özellik adı **Tarım Güvencesi**: gençlere eğitim, modüler kurulum, dönemlik teknik destek ve ürün alımı/dağıtım fikri simülasyon sonucuna bağlandı. Kredi/banka ve fide geliştirme kapsam dışı. Gerçek üyelik veya poliçe değil, destek planı taslağı. Güncel anlatım ve demo: [TARIM_GUVENCESI_JURI_ANLATIMI.md](TARIM_GUVENCESI_JURI_ANLATIMI.md). Uygulama/test kapsamı: [TARIM_GUVENCESI_INTEGRATION_023.md](TARIM_GUVENCESI_INTEGRATION_023.md). Aşağıdaki önceki kısa adlar ve giriş yolu yerine bu güncel ad/akış kullanılır; kaynak ve hesap sınırları korunur.

---

# Güncel ek — 23 Eylül 2026 / TESLİM 022

Ana bilimsel demodan sonra bağlam çubuğunda Üreticiye geçiş → Nasıl işler? açılır. İstenirse Destek simülasyonu → Varsayımsal örneği yükle → çalıştır. Örneğin öğretici olduğu söylenir; indirimin tek başına kazanç sağlamadığı, alıcı kapasitesi ve stresler gösterilir. Sonunda Yaygınlaştırma planı ile gerçek pilot ve ticari teyit gereği açıklanır.

Uygulama, sınırlar ve doğrulama: [PRODUCER_SUPPORT_COMPLETION_022.md](PRODUCER_SUPPORT_COMPLETION_022.md).

---

# Güncel ek · TESLİM021 · 23 Eylül 2026

Beş PC geliştirmesi uygulandı:2015–2025 ERA5 yakın dönem karşılaştırması,kaynaklı taze ürün/protein/besin enerjisi hedefleri,günlük sabit plan için döngüsel depo ve toplama stresleri,ayrıntılı enerji ve işletim güç taraması,numune/pilot kayıt ve karşılaştırma akışı. Güncel hesap,kaynak,sınır ve saha işleri [NORTH_PC_COMPLETION_021](NORTH_PC_COMPLETION_021.md) içinde; [doğrulama iş akışı](NORTH_VALIDATION_WORKFLOW.md) uygulanmıştır.

Önceki “güncel referans yok”,“yalnız kg amacı var” ve“hiç minimum depo hesaplanmıyor” ifadeleri eski sürüme aittir. Yeni depo hesabı ilk dolum hariç sabit üretimin döngüsel taramasıdır;LP'de depo yatırımı veya güç optimize edildiği anlamına gelmez. Yıllık enerji kısıtı LP'de,yeni kW beyanı ayrı taramadadır. Yakın ERA5/gelecek NASA farkı veri seti/hücre etkisini de içerir;aynı NASA tarihsel karşılaştırma korunur. Kaynaklı besin bileşimi dengeli diyet/kâr/talep değildir. Gerçek Arktik ölçümü veya pilot yapılmış sayılmaz.

Sunum gerekçesi:bilgisayarda planı ve test edilecek belirsizliği belirle;gerçek sefer zaman/konumundaki suyu modelle kıyaslamak ve kaynak suyunun kullanım/arıtma özelliklerini sınamak için izinli saha gözlemi ve numune topla;desteklenen girdiyi aynı motorda güncelle. Kara suyu,zemin ve enerji tahsisi ayrıca doğrulanır. Tek sefer tüm gelecek tarımını doğrulamaz.

---

Önceki geliştirme kayıtları aşağıdadır;021ekinin değiştirdiği ifadeler tarihsel kalır.

# Sabit referans, su numunesi ve enerji · TESLİM020 · 23 Eylül 2026

Ana kıyas önceki çalıştırma yerine aynı koşullardaki1995–2014 model iklimine sabitlenmiştir. Bu, bugünkü gözlenmiş üretim değildir;2025 etiketi kullanılmaz. Tam güncel üretim referansı için yeni eksiksiz hava paketi ve veri aileleri arasında karşılaştırılabilirlik gerekir. Önceki “son simülasyona göre” akışı artık geçerli değildir.

Enerji açıklaması: üretim elektriği + arıtma elektriği + ısı/COP; ihtiyaç kWh/yıl, fatura veya kurulu güç değil. Su tasarrufu yanında üretim ortamının enerji ihtiyacı değerlendirilir. Yağış/karın mevsimsel miktarı modelden; numunenin tuzluluk/kullanılabilirliği izinli saha ve laboratuvardan gelir. Deniz örneği kar suyunu temsil etmez. Planlanan örnek/üretim deneyi yapılmış ölçüm değildir. Sunum metni: [Su ve enerji notu](SUNUM_SU_VE_ENERJI_NOTU.md).

---

# Su yönetimiyle geleceğin tarımını şekillendirme · TESLİM019 · 23 Eylül 2026

Gelecek iklimi kaynaklı otomatik veri katmanıdır; ürünün ana çıktısı su yönetimine bağlı üretim sistemi önerisidir. Soldan gelecek/amaç/koşullar seçilir, “Simülasyonu çalıştır” ile uygulanır. Ana karar zinciri: su kaynakları ve payları → üretime uygun kalite/koşullandırma → depolama/aylık yedek/devridaim → ürün oranları ve üretim yöntemleri. Üretim ve su birlikte aynı motorla hesaplanır; çizim sırası tek yönlü yeni solver anlamına gelmez. Kimya ve saha doğrulamaları yapılmış gibi gösterilmez.

Kısa demo: 2050/orta emisyon varsayılanında su stratejisini ve ürün/yöntem paylarını göster. Aday ürünler/yöntemlerden topraksızı kapatıp simülasyonu çalıştır: arıtma payı%0,9→%28,9 olur (kaynak payı, tasarruf yüzdesi değil). Yöntemin su yönetimini değiştirdiğini anlat. Başlangıç koşullarına dön, simülasyonu çalıştır. 2030/2050/2090 şeridinde sera ve depolanan su paylarını karşılaştır. Saha satırından yalnız ölçülebilir su girdilerinin güncellenmesini ve kontrollü üretim pilotunu göster.

---

Önceki geliştirme ve bilimsel temel kayıtları:

# Kuzey karar anlatımı güncellemesi · TESLİM017 · 23 Eylül 2026

Güncel motor ürünleri eşit altı paya ayırmaz: açık çeşitlilik tabanı (%5/ürün), en yüksek taze hasadın %95'ini koruma ve su–enerji normalize uzaklık dengesi kullanır. Aynı koşullarla tarihsel/2030/2050/2090 karşılaştırması, ayrı iklim ön elemesi ve somut üretim/su/altyapı eylemleri eklendi. Tür iklim penceresi yerel tarım uygunluğu değildir; depo hacmi hâlâ tasarım girdisidir. Güncel denklemler ve sınırlar [FUTURE_NORTH_REBUILD](FUTURE_NORTH_REBUILD.md), son doğrulama [BUILD_STATUS](BUILD_STATUS.md). Aşağıdaki TESLİM016 eşit göreli pay amacı ve örnek sonuçlar önceki sürüme aittir.

---

# Future North güncel uygulama · 23 Eylül 2026

Güncel Kuzey demosu: Gelecek/Kuzey → 2050/SSP2-4.5 → altı ürünün alan/hasat/yöntemi → aylık ve günlük su dengesi → aynı miktarlı sera karşılaştırması/enerji → 2090/SSP5-8.5 → duyarlılık → Saha doğrulaması → açıkça sentetik PRE/POST örnek. Gerçek ölçüm ve yeni Arktik hasat iddia edilmez. Türkiye demosunda mevcut desen/iklim → düğmeyle hesap akışı korunur.

Yöntem, kaynak, varsayım ve sınırların güncel ortak kaydı: [FUTURE_NORTH_REBUILD](FUTURE_NORTH_REBUILD.md). Son doğrulama ve teslim: [BUILD_STATUS](BUILD_STATUS.md). Aşağıdaki eski Kuzey uygulama tarifleri kendi tarihleriyle tarihsel kayıttır; bu güncel akışın yerine geçmez. Türkiye ve PWN donanımına ait geçerli kaynak/test kayıtları korunur.

---

# Jüri için kısa Türkiye akışı · TESLİM 015

22 Eylül 2026. Masaüstü: http://127.0.0.1:8011/#turkiye. Aşağıdaki eski otomatik ilk-öneri akışı artık uygulanmaz. Açılışta mevcut desen gösterilir; öneri düğmeye basınca hesaplanır.

1. Konya'yı aç: “Bu, kaynaklı mevcut ürün desenimiz.” Kaynak dönemi 2024 il ürün deseni ve 2024–2025 hava koşullarıdır; 2026 canlı ekiliş sayımı diye sunma.
2. “Sıcak ve kurak”ı seç: “Sıcaklık 2 derece artar, yağış yüzde 20 azalırsa aynı ürünlerle ne olur?” Bu bir varsayımsal senaryodur; bu değişikliklerin gerçekleştiği iddia edilmez. Ürün oranlarına dokunma.
3. Kırmızı kadranı göster: “Mevcut deseni sürdürürsek senaryodaki su sınırını aşıyoruz.” Ekrandaki yüzdeyi oku; ezberlenmiş başarı/risk oranı söyleme. Sulama suyu sınırı senaryoda belirlenen miktardır, resmî tahsis ölçümü değildir.
4. “Deseni optimize et” veya “En uygun deseni hesapla”ya bas. Tarladaki dağılım değişsin. “Model, belirlenen en az üretim miktarlarını koruyarak su sınırına uygun ürün paylarını hesaplıyor.”
5. Eylem panelini oku: hangi ürün azalıyor/artıyor, neden ve hangi üretim sınırı korunuyor. Ekilemeyen alan varsa yüzdesini de söyle. Ana su yüzdesi kaynak başlangıcına göre toplam etkidir; ürün değişiminin ek etkisi aynı iklim/sulama koşulundaki hesap öncesi seçime göre ayrıca verilir. Kâr veya ölçülmüş su tasarrufu garantisi değildir.
6. “Serin ve yağışlı”yı seçip yeniden hesapla: olumlu bir koşulda aynı sistemin nasıl değiştiğini göster. İyi koşullar önceden yazılmış bir optimum değildir.
7. Başka bölgeyi seç ve aynı akışı göster. Beş kaynaklı il bağlamında aktarılabilirlik örneğidir. Trakya'da “Çeltik alanı korunuyor, su karşılaştırması diğer ürünleri kapsıyor” denir; tüm bölgenin toplam su yeterliliği diye sunulmaz.
8. İstenirse alttaki grafik/hesapları aç. Hektar, m³, kg ve kaynakları burada incele. Ekonomi için gerçek veya açıkça belirtilmiş işletme fiyat/maliyetleri gir; boş fiyatı sıfır veya kâr sayma.

Verimli sulama örneği: “Aynı ürünlerle sulama verimini %75’ten %85’e çıkarırsak su ihtiyacı 100’den 88,2’ye iner. Deseni optimize edince 81’e iner. Toplam %19 daha az; ikinci aşama kalan miktarın üzerinden ayrıca %8,2’dir.” Bunlar bu gerçek koşunun model sonuçlarıdır, sabit başarı oranı değildir. Sulama verimi bitkinin ihtiyacını karşılayan su payıdır; ürün verimiyle karıştırma.

Mobil test yapılmaz. Sonraki araştırma aşaması Future North'tur; bu sunum için yapay saha verisi veya garantili başarı/kâr üretilmez.

---

# Güncel canlı demo · Rebuild / TESLİM 007

22 Eylül 2026. Başlangıç: uygulamadaki BUGÜN / TÜRKİYE. Her sayıyı ekrandaki koşuluyla anlat; ezberlenmiş başarı oranı kullanma.

1. Konya kendiliğinden kaynak başlangıcını ve ilk hesabı yükler. Solda beş ürün; sağda mevcut → önerilen. Su -20% → ÜRÜN DESENİNİ HESAPLA. Değişen alanı, üretimi, su kısıtını ve atanmayan alanı birlikte göster. Bu modellenmiş su hesabıdır; sahada ölçülmüş tasarruf değildir.
2. Çalışma bölgesinden Şanlıurfa seç. Yeni resmî baseline ve aynı motoru göster. Bu beş il kapsamında aktarım örneği; Türkiye'nin tamamında saha validasyonu değildir.
3. GELECEK / KUZEY → 2035 NASA → SSP2-4.5 → hesapla. Kaynaklı iklimin patates tarla seçeneğini elemesini ve eksik yerel girdileri göster. DATA NEEDED, sıfır üretim önerisi anlamına gelmez.
4. Hesap deneyi · açık varsayımlar bölümünden açıklayıcı senaryoyu yükle → Dengeli plan → hesapla. Hesaplanmış ürün kg, ha/m², yöntem, sezon, kaynak ve kısıtları göster. Bu araştırma hesabı yerel doğrulanmış Arktik planı değildir. Örnek senaryo artık kaynaklı eleme uyguladığı için her zaman üç ürün üretmez.
5. Su/enerji önceliğine geç. Açık %80 ortak üretim tabanını anlat; kullanıcı nihai ürün kilogramlarını girmedi. Amaç değişikliğinin sonucu değiştirmemesi de mümkündür.
6. TASE neyi test edebilir? → karar duyarlılığı. Karasal tatlı su/enerji altyapısı doğrudan PWN ölçümü değil; deniz sıcaklığı ve salinite aday ölçüm, kimya izinli numune/lab. Salinite/kimya sayısal bağlantısı bugün eksik.
7. PRE-TASE / gözlem sonrası: mevcut senaryoyu dondur, açık simülasyon sıcaklığıyla eşleştir ve aynı motoru çalıştır. 24 saat uyumsuzluk güncellemeyi engeller; eşit sıcaklıkta değişmeme geçerli sonuçtur. Gerçek ölçüm yapılmış gibi anlatma.

Sefer sonrası fiziksel numune veya açıkça yeniden oluşturulmuş kaynak suyu → arıtma → kontrollü büyüme testi sonraki aşamadır. Ana ekran dışında ileri tablolar, CSV ve kaynaklar yalnız gerektiğinde açılır. Ekran kayıtları ve güncel doğrulama BUILD_STATUS.md'dedir.
