# Modelimiz nasıl çalışıyor?

23 Eylül 2026 · Mevcut kaynak koduna dayanan anlatım. Hesap kapsamı ve sınırlar birlikte okunmalıdır.

## Bir dakikalık anlatım

**Biz geleceğin iklim koşullarında hangi üretim sisteminin, hangi su yönetimiyle kurulabileceğini simüle ediyoruz.** Konya'da mevcut ürün dağılımını iyileştirmekle başladık. Gelecek Kuzey'de aynı karar sorusunu genişlettik: hangi ürün, ne kadar alan, hangi üretim yöntemi, hangi mevsim ve hangi su kaynağı?

Kullanıcı yılını, iklim senaryosunu, planlama alanını ve kaynak koşullarını seçiyor. Sistem yayımlanmış iklim modeli verilerini; ürünlerin yetişme koşulları, kontrollü üretim araştırmaları ve su–enerji hesaplarıyla birleştiriyor. Önce adayları belirliyor, ardından kaynak sınırları içinde üretim dağılımını hesaplıyor. Önerinin yanında **hangi kaynağa ihtiyaç olduğunu, kararı neyin sınırladığını ve hangi bilgi değişirse planın değişebileceğini** gösteriyor.

Burada temel ayrımımız şu: **İklimin bir ürün için elverişli hale gelmesi, sürdürülebilir üretimin mümkün olduğu anlamına gelmez.** Su doğru mevsimde toplanabilmeli, depolanabilmeli ve üretime uygun kaliteye getirilebilmelidir. Kapalı üretimde ışık, sıcaklık, nem ve enerji de sağlanmalıdır. Topraksız üretim susuz üretim değildir.

TASE aşamasında izinli ölçüm ve numunelerle kaynak suyunu incelemek istiyoruz. Bu gözlemlerle yalnız desteklenen girdileri güncelleyip **aynı karar motorunu tekrar çalıştıracağız.** Sonra kontrollü üretim pilotunda gerçek su, enerji ve hasadı ölçeceğiz. Tarım Güvencesi ise önerinin eğitim, ekipman ve alıcı bağlantısıyla uygulanmasına yönelik devam modelimizdir.

## Girilen yılı nasıl hesaplıyoruz?

Yıl, bir katsayı değildir. Örneğin 2043 girildiğinde 2030 ile 2050 sonuçları arasında düz bir çizgi çekerek ürün payı üretmek bilimsel yöntemimiz değildir. Yıl seçimi, o yılın kaynak dosyalarına bağlanır; sıcaklık, yağış ve güneşlenmeyle ilgili günlük girdilerden yetişme koşulları, su toplama ve enerji gereksinimi tekrar hesaplanır. Ardından optimizer yeniden çözülür. Her seçilebilir yıl için bütün gerekli kaynak dosyaları doğrulanmalıdır; eksik yıl sessizce yakın bir döneme veya doğrusal interpolasyona dönüştürülmez.

Kuzey hesabı NASA NEX-GDDP-CMIP6'dan üç model kullanır: ACCESS-CM2, MPI-ESM1-2-HR ve MRI-ESM2-0. Seçilen SSP, emisyonlar ve toplumsal gelişim için bir senaryo yoludur. Veri, günlük ve 0,25° çözünürlükteki model projeksiyonudur; parselde ölçülmüş hava değildir. [NASA veri tanımı](https://www.nccs.nasa.gov/data-collections/nex-gddp-cmip6/)

**“2043 senaryosu” demek, “2043'ün havasını şimdiden biliyoruz” demek değildir.** İklim projeksiyonu belirli bir emisyon senaryosuna verilen model tepkisidir. Tek yılın sonuçlarında modellerin yıllar arası değişkenliği de bulunur. Bu nedenle tek yıllık hesap bir yıllık senaryo denemesidir; uzun ömürlü tesis yatırımı için komşu yıllar ve çok yıllık dönemlerle dayanıklılık ayrıca incelenmelidir. Üç modelin aralığı da otomatik olarak %95 güven aralığı değildir. [IPCC projeksiyon ve değişkenlik tanımları](https://www.ipcc.ch/report/ar6/wg2/chapter/annex-ii/)

“Neden 2050?” sorusuna cevabımız: **2050 zorunlu bir yıl değil; karar vericinin seçtiği planlama ufuklarından biridir. Sistem, seçilen yılı kaynak veriye bağlayarak sınar.** Tarih seçmek gelecekteki verimi, fiyatı veya su tahsisini bildiğimiz anlamına gelmez.

Bugüne yakın karşılaştırmanın veri temeli **2015–2025 ERA5 yeniden analizidir**. Bu, bugünün canlı hava ölçümü veya 2026 yılının tamamı değildir. NASA gelecek projeksiyonu ile ERA5 karşılaştırması farklı veri ürünlerini de karşılaştırır; görülen farkın tamamı iklim değişikliğine yüklenemez. Eski 1995–2014 NASA dönemi, aynı veri ailesiyle ek karşılaştırma için saklanır.

## Hesabın içindeki karar zinciri

| Aşama | Gerçekte yapılan hesap | Karar vericiye karşılığı |
|---|---|---|
| İklim | Günlük sıcaklık, yağış ve kısa dalga ışınımı; yetişme dönemi ve soğuk/ısı koşulları | Seçilen yılın hangi koşulları değiştirdiği |
| Ürün adayları | Kaynaklı yetişme süresi, sıcaklık ve yöntem uygunluğu taraması | İklim açısından araştırılabilecek ürünler |
| Yerel uygulanabilirlik | Zemin/permafrost kanıtı ve yöntem başına nicel üretim kanıtı ayrı kontrol edilir | İklim adayı ile gerçekten hesaplanan üretim seçeneğinin ayrılması |
| Üretim kapasitesi | Yetiştirme alanı × tamamlanabilen çevrim × kaynaklı çevrim verimi | Yöntem ve mevsime göre koşullu hasat |
| Su yönetimi | Kar birikimi/erimesi, toplama alanı, depolama, yeni su gereksinimi ve varsa arıtma | Depodan karşılanacak su, yedek kaynak ve açıklar |
| Enerji | Işık, pompa, fan, nem alma, soğutma, ısıtma ve su arıtma | Yıllık tüketim ve altyapı ihtiyacı |
| Optimizasyon | Aynı su, alan ve enerji sınırları altında ürün × yöntem × mevsim dağılımı | Ürün oranları, alanları, kaynak dağılımı ve sınırlayıcı koşullar |
| Belirsizlik | Kaynak ve mühendislik aralıkları değiştirilerek aynı motor tekrar çözülür | Hangi bilginin kararı etkilediği ve neyin araştırılması gerektiği |

### Ürün payları nereden geliyor?

Motor, SciPy/HiGHS ile çözülen **doğrusal programlama** modelidir. Doğal dil üreten yapay zekâ ürün oranlarını seçmez. Günlük fiziksel hesaplar doğrusal olmayan ilişkiler içerebilir; optimizer bu aşamadan gelen kaynak katsayılarıyla çalışır.

Varsayılan dengeli planda önce seçilen üretim çıktısının ulaşılabilir en yüksek değeri bulunur. Çıktı taze yenilebilir ürün kütlesi, protein veya gıda enerjisi olabilir. Bu en yüksek değerin en az **%95'i korunurken** su ve enerji açısından ayrı ayrı en iyi çözümlerden uzaklaşmanın en büyüğü küçültülür. Varsayılan olarak her etkin ürün için toplam alanın en az **%5'i** ayrılır. Kalan alanı eşit bölmek zorunda değildir.

%95 koruma ve %5 çeşitlilik, **açık planlama tercihidir**; uzmanların bütün bölgeler için ölçtüğü doğal sabitler değildir. Bunlar açıklanmadan “bilimsel olarak tek en iyi desen” denemez. Su ve enerji önceliği modları yeni hesaplanan dengeli planın ürün miktarlarının seçilen bölümünü koruyarak ilgili kaynak gereksinimini azaltır. Hiçbir mod kendi başına kârı, dengeli beslenmeyi veya gerçek talebi en iyi hale getirdiğini iddia etmez.

### Su ve enerji neden birlikte hesaplanıyor?

Yağış ve karın varlığı yeterli değildir. Model karı sıcaklığa bağlı bir erime hesabıyla sıvı suya geçirir, toplama verimini uygular ve tankın sınırlı hacmini izler. Üretimin yeni su ihtiyacı geri kazanımlar düşüldükten sonra hesaplanır. Yeniden kullanılan su ikinci kez bağımsız bir kaynak olarak sayılmaz. Açık kalırsa, izin verilen senaryoda karasal tahsis veya arıtılmış deniz suyu devreye girebilir. Tuzluluk ve kaynak sıcaklığı arıtma gereksinimini etkiler.

Aylık kaynak dengesi optimizerın içindedir; seçilen plan ayrıca günlük sırayla denenir. Aylık toplamın yetmesi her gün su bulunduğu anlamına gelmez. Günlük açıklar, yedek su ve depolama sonuçları bu nedenle birlikte okunur. Başlangıçta kar ve tankın boş kabul edildiği hesaplarda bu bir başlangıç varsayımıdır; önceki yıldan devreden gerçek stok ölçülmüş değildir.

Enerjide **kWh tüketim**, **kW güç kapasitesi** demektir. Bir tesisin yıl boyunca ne kadar enerji kullanacağı ile aynı anda ne kadar güç isteyebileceği farklıdır. Model ısıyı ayrıca hesaplar; elektrik eşdeğerine geçerken seçilen ısıtma verimini kullanır. Bu sonuç, yerel şebekenin o kapasiteyi verebildiğini veya maliyetin karşılanabildiğini kanıtlamaz.

## Ne kaynaklı, ne hesap, ne hâlâ doğrulanacak?

| Bilgi | Durum | Yorum |
|---|---|---|
| NASA günlük iklim serileri | Kaynaklı model verisi | Gerçek yayımlanmış veri; geleceğin gerçekleşmiş gözlemi değil |
| ERA5 2015–2025 | Kaynaklı yeniden analiz | Yakın dönem karşılaştırması; canlı sensör ölçümü değil |
| Kontrollü ürün verimi ve çevrim | Yayımlanmış deneyden aktarılan değer | EDEN ISS 2018 Antarktika çalışması, Svalbard'da ölçülen hasat değil |
| Ürün alanları ve yöntem payları | Hesap/simülasyon | Seçilen hedef, aday kütüphanesi ve kaynak koşullarına bağlı |
| Yapı, toplama verimi, geri kazanım ve başlangıç stokları | Açık mühendislik varsayımları | Yerel kurulum/pilotla sınanmalı |
| %95 üretim koruma, %5 çeşitlilik | Planlama tercihi | Uzman onayı veya ölçüm gibi sunulmaz |
| Yerel toprak, elektrik, su tahsisi ve işletme koşulları | Yerel doğrulama gerekli | Senaryoda girilen sayı tahsis belgesi yerine geçmez |
| Deniz suyu T/S profili | Sahada ölçülebilir | PWN kalibrasyon, UTC, konum ve kalite kaydıyla katkı sağlar |
| Kimya ve üretim uyumluluğu | Numune ve kontrollü pilot gerekli | Panel ve kabul ölçütleri uzman/laboratuvarla belirlenir |

Uzman görüşü, yayımlanmış kaynakla aynı şey değildir. Sistemdeki kaynaklı parametreler literatür ve kurumsal belgelerden gelir. Projeye özel bir uzman onayı ancak kişi, tarih, kapsam ve kayıt bulunduğunda söylenebilir. Özellikle numune paneli, membran seçimi ve üretim deneyi için henüz alınmamış onay varmış gibi gösterilmez.

## Saha, pilot ve Tarım Güvencesi bağlantısı

PRE aşamasında plan ve ilgili model beklentisi kaydedilir. TASE'de toplanan uygun konum/zaman ve kaliteye sahip su gözlemiyle yalnız desteklenen su girdileri güncellenir. POST aşamasında aynı optimizer çalışır. Ürün veya su stratejisi değişebilir; **değişmemesi de geçerli sonuçtur**. Bugünkü deniz ölçümü 2050'nin yıllık karasal suyunu veya gelecekteki deniz tuzluluğunu doğrudan ölçmüş olmaz.

İzinli numuneler kaynak suyu ve arıtma sorularını sınayabilir. Doğrudan kullanılamıyorsa ölçülen kimyaya dayalı, açıkça etiketlenmiş yeniden oluşturulmuş su koşuluyla pilot tasarlanabilir. Kontrollü tarım testi gerçek su ve enerji kullanımı ile bitki tepkisini üretir. Bu test bütün Arktik tarımını değil, denenen kaynak suyu → arıtma → üretim koşulunu doğrular.

Tarım Güvencesi sonucun uygulanmasına yönelik ayrı destek katmanıdır. Modeldeki ürün ve miktar, açık fiyat/gider ve alıcı koşullarıyla destekli/desteksiz hesaba taşınabilir. Eğitim ve destek seçmek fiziksel ürün verimini otomatik artırmaz; model kilogramı otomatik satılmış kabul edilmez. Sistem mevcut aşamada destek planı taslağı oluşturur; gerçek üyelik, poliçe veya alım garantisi oluşturmaz.

## Teknik iz sürme ve araştırma sınırı

Bu anlatımın kod karşılıkları: `backend/north_climate.py`, `north_candidates.py`, `north_resources.py`, `north_planning.py`, `north_optimizer.py`, `north_infrastructure.py`, `north_field.py`, `north_validation.py`, `producer_support.py`. Parametre kökenleri `data/north/crop_evidence_v2.json`, `resource_evidence.json`, `ground_evidence.json`, `food_composition.json` ve iklim manifestlerindedir.

Mevcut nicel kuzey uygulaması Longyearbyen bağlamındadır. Açık tarla ürünleri iklim araştırma adayı olarak gösterilebilir; yerel zemin ve yöntem verimi doğrulanmadığı için mevcut nicel plana otomatik alan verilmez. Sera ve kapalı topraksız seçeneklerin hasat katsayıları, karşılaştırılabilir ortamın sağlandığı kabulüyle kontrollü üretim analoğundan gelir. İklim ısındı diye verimi veya ürün payını otomatik artıran bir gelecek katsayısı yoktur. Gelecekte teknoloji, fiyat, yeni çeşit veya yerel pilot kanıtı eklenirse bunlar ayrı, izlenebilir girdiler olmalıdır.

Mühendislik hesabı ayrıntılı ve yerelde doğrulanmış bir bina/bitki büyüme simülatörü değildir. Saatlik dış koşullar günlük veriden yeniden kurulur; kışın boş tesisin don koruması, tüm arıtma kimyası ve her işletme kaybı kapsanmamaktadır. Koşullu bir planın gerçek uygulamaya geçmesi için su, zemin, enerji ve pilot doğrulaması gereklidir.

Kaynaklı kontrollü verimin araştırma dayanağı: [Zabel ve arkadaşları, EDEN ISS 2018 deney sonuçları](https://doi.org/10.3389/fpls.2020.00656). Çalışmada ölçülen koşullardan başka bir tesise aktarım, yerel doğrulama yerine geçmez.
