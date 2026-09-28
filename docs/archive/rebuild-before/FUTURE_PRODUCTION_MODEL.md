# Gelecek üretim modeli ve hipotez denetimi

22 Eylül 2026 — U8 durum güncellemesi. **Bu belge uzun vadeli bilimsel tasarımı tanımlar.** Çalışan ortak çekirdek [CROP_PATTERN_ENGINE.md](CROP_PATTERN_ENGINE.md), çok ürünlü kuzey hesabı [FUTURE_NORTH_SIMULATOR.md](FUTURE_NORTH_SIMULATOR.md), tamamlanma kaydı [BUILD_STATUS.md](BUILD_STATUS.md) içindedir. Aşağıdaki araştırma hipotezleri henüz doğrulanmadı. Kanıt kodları [EVIDENCE_MAP.md](EVIDENCE_MAP.md); ana katmanlar [SCIENTIFIC_ARCHITECTURE.md](SCIENTIFIC_ARCHITECTURE.md).

## U8'de uygulanan minimum model

Türkiye ve kuzey aynı bölge/ürün/yöntem/kaynak/kapasite sözleşmesiyle çözülür. Kuzeyde ilk portföy arpa, patates ve maruldur; kaynak gerekçeleri [FUTURE_NORTH_CROP_SET.md](FUTURE_NORTH_CROP_SET.md). Başlangıçta iklim/zemin bilinmediğinden açık tarla uygun ilan edilmez. Kullanıcının açık uygun-saha senaryosunda 1 ha arpa, 0,5 ha patates, 333,33 m² hidroponik marul ve üç kaynağa su tahsisi hesaplanır; bu yerel tarım tahmini değildir.

Mevcut iklim kanıtı 2030–2049 tek model bağlamıdır; örnek üretim hesabı 2035'te tek döngüdür. Gelecek ET₀, yerel verim/enerji ve çekilebilir su ölçümü eksikleri kullanıcı girdisi olarak görünür. Optimize edilen miktar ürün kapasitesidir; amaç önce ürün bazında hedef başarısı, sonra su ve yeterli enerji verisi varsa enerjidir. Aşağıdaki Pareto/risk/belirsizlik araştırması tam uygulanmış sayılmaz.

## Tam karar sorusu

Seçilen gelecek iklim senaryosunda **nerede, ne, hangi üretim yöntemiyle, hangi su kaynağından, ne zaman ve hangi kaynak kısıtları altında** üretilebilir? Çıktı, tanımlı su/enerji/çevre koşullarına göre **Sustainable Production Frontier**: tek bir enlem çizgisi değil; hücre/bölge × ürün × yöntem × kaynak × dönem için koşullu uygulanabilir seçenekler kümesi [U5 §8; E19].

Bu terim bir proje hedefidir; bütün ekonomik, sosyal ve ekolojik sürdürülebilirliğin kanıtlandığı evrensel sertifika değildir. Kapsama alınmayan boyutlar görünür tutulur.

## Bilimsel olarak desteklenen ile bizim sınayacağımız

| Desteklenen dış başlangıç | Bizim henüz sınanmamış sorumuz |
|---|---|
| İklimsel uygunluk bazı ürünler için kuzeye genişleyebilir; permafrost bunu sınırlayabilir [E01–E02]. | Su/enerji ve yöntem eklendiğinde seçtiğimiz bölgede uygulanabilir seçenek ne kadar değişiyor? |
| Svalbard'da tarihsel kontrollü üretim girişimi ve kaynak/enerji fizibilitesi vardır [E03]. | Seçtiğimiz gelecek dönem ve yerel kaynaklarda hangi üretim deseni mümkün? |
| Üretim yöntemleri su ve enerji açısından farklı bedeller doğurabilir [E04–E05]. | Aynı üretim hedefini karşılayan hangi seçenek ayrı koşullarda daha dayanıklı? |
| Arıtma performansı kaynak suyu koşullarına bağlı olabilir [E06]. | PWN'nin temsil ettiği kaynağın gözlenen T/S/kimya farkı ilgili kararı değiştiriyor mu? |

Svalbard örneği bütün Arktik'i temsil etmez; denizde ölçüm yapılan yer tarla alanı değildir. Karasal üretim coğrafyası ve deniz saha istasyonu iki ayrı veri nesnesidir; aralarında ancak tanımlı fiziksel/altyapısal ilişki kurulursa yerel karar güncellenir [E13].

## Hesaplanacak birim ve kararlar

**İndeks:** bölge r, ürün c, yöntem m, kaynak s, dönem t, iklim/parametre senaryosu ω.

**Kararlar:** üretim alanı veya kapasitesi x; bundan türeyen ürün oranı; kaynak çekimi q; yöntem/kaynak seçimi; ekim/üretim dönemi; gerekiyorsa depolama kullanımı. Yöntemler açık tarla, sera, hidroponik ve yalnız gerekçelendirilirse dikey/kapalı sistemdir. Aynı x birimi bütün yöntemlere zorla uygulanmaz: taban alanı, yetiştirme alanı, kurulu kapasite ayrıca belirtilir [U5; tasarım önerisi].

**Girdiler:** iklim, ürün gereksinimi, toprak/permafrost, ET ve su dengesi, güvenilir kaynak kapasitesi/kalitesi, yöntem verimi ve su girdisi, arıtma geri kazanımı/enerjisi, enerji arzı, çevresel/altyapısal sınırlar. Veri sözleşmesi: birim, dönem, kaynak, sürüm, gözlem/model/varsayım ayrımı [E18].

**Kısıtlar:**

- Ürün bazında üretim alt sınırı veya açık besin hedefi; bir kilogram buğday bir kilogram marulla eşitlenmez.
- Aynı fiziksel alan/kapasitenin iki kez kullanılamaması; üretim dönemlerinin uyumu.
- Dönemsel su dengesi, çekim/arıtma/depolama kapasitesi, kalite ve korunacak diğer kullanımlar.
- Isı/elektrik arzı ve kesinti/enerji bütçesi; elektrik ile ısının aynı birim adıyla gelişigüzel birleştirilmemesi.
- Arazi, permafrost, altyapı ve seçilmiş çevresel sınırlar; açık tarla filtresi kapalı üretime aynen kopyalanmaz.

**Amaç:** Üretim hedefini koruyan planlar içinde su açığı, enerji, iklim riski ve çevresel baskının anlaşılır ödünleşimleri. İlk modelde iki–üç seçenek/Pareto karşılaştırması yeterli; tek ağırlıklı skor kullanılacaksa ölçek ve ağırlık açıklanır. Uygulanabilir çözüm yoksa sistem bunu söyler [U5; E19 önerisi].

## RQ1 ve H1 — iklimsel uygunluktan koşullu üretim uygunluğuna

**RQ1 (refine):** Belirli bölge, ürün/yöntem, dönem ve iklim senaryosunda iklimsel uygun seçeneklerin ne kadarı toprak/permafrost, mevsimsel su, enerji ve tanımlı çevresel kısıtlar eklendiğinde uygulanabilir kalır?

**H1 (test edilebilir öneri):** Seçilen çalışma alanında iklimsel uygunlukla önerilen seçeneklerin ölçülebilir bir kısmı, bağımsız kaynak verileriyle tanımlanmış su/enerji/fiziksel kısıtlardan en az birini ihlal eder.

**Test:** Aynı alan/ürün/yöntem tabanını tut; filtrelerin her birinin elenen alan, karşılanamayan üretim veya kapasite üzerindeki marjinal katkısını raporla. Uygunluk eşiği ve veri kaynağını sonucu görmeden kaydet. Alan oranı veriliyorsa payda ve raster alan ağırlığı belli olsun; ürünler arası örtüşme iki kez toplanmasın.

**Audit:** Filtre ekleyince seçenek sayısının artmaması matematiksel olarak beklenir; tek başına bilimsel keşif sayılmaz. Bilgi değeri *ne kadar, nerede ve hangi bağımsız kısıt nedeniyle* değiştiğidir. İncelenen kapsamda hiçbir seçenek elenmezse H1 desteklenmemiş olabilir. “Veri eksik” hücreler “uygun değil” diye sayılmaz [E01–E02,E18–E19].

## RQ2 ve H2 — üretim deseni dayanıklılığı

**RQ2 (refine):** Aynı üretim hedefi ve bütçeler altında, ürün–yöntem–kaynak–zamanı birlikte seçmek, daha basit planlara göre görülmemiş yıl/model/kuraklık koşullarında kaynak kısıtlarını daha sık sağlayan seçenekler üretir mi?

**Karşılaştırmalar:** B0 iklimsel uygunlukla önerilen plan; B1 su kısıtlı yalnız ürün deseni; B2 ürün+yöntem+kaynak+dönem ortak planı. Hepsi bağımsız değerlendirme sırasında aynı fiziksel su/enerji hesapları ve aynı üretim hedefiyle puanlanır.

**H2:** B2, ayrı tutulan koşullarda üretim hedefi korunurken su açığını/kısıt ihlalini azaltır veya aynı güvenilirlikte kaynak bedelini düşürür. Önceden tanımlı ölçütlerde avantaj yoksa H2 desteklenmez.

**Ölçütler:** üretim hedefinin karşılandığı dönem/senaryo oranı, su açığı m³, enerji kWh ve tanımlı emisyon/çevre metriği; birden çok hedefin ödünleşimi ayrı gösterilir. İklim ensemble'ındaki oran fiziksel olay olasılığı diye otomatik sunulmaz.

**Audit:** Daha çok karar seçeneği verilen çözücünün eğitim probleminde daha iyi hedef değeri bulması beklenebilir. Bunu genellenebilirlik başarısı diye sunmamak için tüm bir yıl/bölge/model üyesini testte ayır; aynı modelin çıktısını kendisine doğrulama olarak gösterme [E04–E05,E19; önerilen yöntem].

## RQ3 ve H3 — yerinde gözlemin bilgi ve karar değeri

**RQ3 (refine):** Kalite kontrollü ve referansla karşılaştırılmış Arktik profilleri, örneklenen koşullarda modelin T/S/p temsil hatasını nasıl değiştirir; bu değişim fiziksel olarak bağlı kaynak suyu/arıtma senaryosunda karar veya karar belirsizliğine ne ölçüde yansır?

**H3a:** Basit veya AI destekli düzeltme, eğitimde kullanılmayan cast/istasyonlarda temel modele göre hata veya kalibrasyonu iyileştirir.

**H3b:** Gözlem güncellemesi, ilgili kaynak senaryosunda en az bazı koşullarda uygulanabilirlik, seçenek sırası veya kararın güvenilirliği üzerinde ölçülebilir fark yaratır.

H3a ve H3b ayrı sınanır. Model iyileşmesi kararın değişmesini gerektirmez; sensör belirsizliği içindeki fark düzeltme başarısı sayılmaz. Gözlem modelle uyuşursa o koşulda modelin temsilini destekleyen sonuç elde edilir; bütün Arktik için genellenmez.

**Test:** Gözlemden önce model snapshot'ını sakla. Zaman/konum/derinlik eşlemesini kaydet. Düzeltmesiz model → basit bias/regresyon → ancak veri yeterliyse residual AI. Tüm cast'leri ayrı tutarak test et; aynı cast'in komşu satırları bağımsız örnek gibi bölünmesin. Model ürünü gözlemi asimile etmişse bağımsız doğrulama etiketi kullanma.

**Ölçütler:** T/S için birimleriyle bias/MAE/RMSE, bağımsız referans belirsizliği, aralık kapsaması ve genişliği; ardından aynı üretim hedefi altında enerji aralığı, su açığı, seçenek sırası/uygulanabilirlik farkı. Daralan fakat gerçek değeri daha az kapsayan aralık iyileşme değildir. Üç–beş profil gibi keyfî sayılarla bölgesel AI başarısı vaat edilmez [E13,E19].

## PWN'nin iki yolu ve temsil koşulu

**A — model değerlendirme:** PWN → modelin örneklenen su kolonunu temsil gücü → ilgili deniz suyu alt modelinin güveni. Karasal su bütçesi ayrı veri ve modelden gelir.

**B — kullanılabilir su:** Kaynak T/S/kimya → seçilmiş arıtma teknolojisi → ürün suyu kalite/miktarı → enerji → üretim planı. RO için q_ürün = geri_kazanım × q_besleme; özgül enerji yalnız doğru teknoloji ve geçerli koşul aralığında kullanılabilir [E06].

TASE istasyonu hedef su alma noktası değilse B çıktısı **gözlemle beslenen duyarlılık senaryosu** olur; gerçek tesis/yerleşim saha doğrulaması olmaz. Seferde belirli bir kaynağa erişim garanti değildir; tasarım route-independent kalır. Buna rağmen A'nın yerel model sınaması ve örneklerin fiziksel karakterizasyonu geçerli araştırma çıktısı olabilir [E07,E13].

## Mülakat demosunun dar kapsamı

1. Konya geçmiş sonucunu doğru birim ve statüyle göster [E12].
2. Konya'da mevcut/önerilen deseni ve %20 su senaryosunu göster; Şanlıurfa'ya geçip aynı motorun farklı resmî desenle çalıştığını göster. Bu transfer demonstrasyonudur; bağımsız agronomik validasyon değildir [TURKIYE_REGIONAL_SIMULATOR.md](TURKIYE_REGIONAL_SIMULATOR.md).
3. Kuzeye uygunluk konusunda kaynaklı örnek → yöntem ve su/enerji kısıtlarının nasıl devreye gireceği. Literatür haritası ile kendi hesabını ayır [E01].
4. Kendi tank kaydı ancak gerçekten alındıysa göster; bugün hazır örnek sentetik profildir ve açık simülasyon etiketiyle kullanılır [E16].
5. Arktik kaynak suyu modelinin hangi girdisinin gelecekte güncelleneceğini açıkla. Henüz sahadan gelmemiş veriyle gerçek kalibrasyon yaptık deme [E17].

## Belirsizlik ve açıklama

Sensör/kalibrasyon, istasyon temsil ölçeği, iklim modelleri, su arzı, üretim/arıtma parametreleri ve karar ağırlıkları ayrı gösterilir. Sonuç durumları: **uygun / koşullu / uygun değil / veri yetersiz**. LLM bu hesaplardan açıklama çıkarabilir; eksik parametreyi güvenli görünen sayı ile dolduramaz. AI'nın bilimsel değeri baseline'a karşı bağımsız katkıdır [U5 §17; E19].

**Bugünkü durum:** U8 ile düzenlenebilir Türkiye ürün deseni ve çok ürünlü kuzey kapasite hesabı aynı motorda çalışır; eşleşmiş saha girdisiyle aynı hedef/kısıtların yeniden koşulması eklenmiştir. [Saha güncelleme sözleşmesi](FIELD_TO_PATTERN_UPDATE.md). Bağımsız bilimsel doğrulama, PWN deneyi ve özgün sürdürülebilir üretim haritası henüz yok. Çalışan hesap hipotez doğrulaması veya yerel Arktik uygunluğu kanıtı değildir [E17].
