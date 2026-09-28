# Future North güncel uygulama · 23 Eylül 2026

TASE aynı üretim ve su yönetimi araştırmasının saha aşamasıdır. Karar duyarlılığı fiziksel ölçüm önceliğini belirler. Yeni ekran günümüz su kolonunu günümüz modeliyle test etme ile gözlemi geleceğin koşullu kaynak senaryosuna aktarmayı ayırır. Bir profil gelecek iklimini doğrulamaz; değişmeyen üretim dağılımı geçerli sonuçtur.

Yöntem, kaynak, varsayım ve sınırların güncel ortak kaydı: [FUTURE_NORTH_REBUILD](FUTURE_NORTH_REBUILD.md). Son doğrulama ve teslim: [BUILD_STATUS](BUILD_STATUS.md). Aşağıdaki eski Kuzey uygulama tarifleri kendi tarihleriyle tarihsel kayıttır; bu güncel akışın yerine geçmez. Türkiye ve PWN donanımına ait geçerli kaynak/test kayıtları korunur.

---

# TASE VII ve ulusal kutup araştırmalarıyla uyum

22 Eylül 2026 — FINAL MASTER SYNC ile güncellendi. Bu belge, su yönetimi ve sürdürülebilir üretim karar desteğinin Arktik saha katmanını ve sefer gerçekliğini açıklar. Kullanıcı master promptu kapsamı; resmî belgeler operasyonel koşulları belirler. Kaynak kodları [ana kaynak belgesindedir](PROJECT_SOURCE_OF_TRUTH.md); yeni doğrulama bağlantıları aşağıdadır. Üretim kodu/firmware yazılmadı.

## Arktik sahasının araştırmadaki somut görevi

**Önerilen anlatım:** Konya'da su baskısı altında ürün desenlerini karşılaştıran bir karar destek yaklaşımı geliştirdik. Bunu önce Türkiye'deki farklı koşullara aktararak, gelecekte kuzeye genişleyebilecek üretim potansiyelini su ve enerji açısından değerlendiren ikinci nesil sisteme taşıyoruz. Karar artık ürün, yöntem, su kaynağı ve dönemi birlikte içeriyor. Masa başında iklim senaryolarını ve mevcut model verilerini çalışabiliriz; seferde ise aynı zaman ve konumdaki su kolonunu kendi aracımızla ölçüp modelin temsilini sınamak istiyoruz. Profil ve uygun fiziksel numuneler, belirli kıyısal kaynak-suyu/arıtma senaryolarına girdi sağlayabilir. Mülakata kadar kontrollü kolon prototipi ve gerçek deney grafikleri hazırlamayı hedefliyoruz; seçilirsek Arctic sürümünü ilgili uzmanların görüşleriyle geliştirmek istiyoruz [MASTER §4–16; F2; W1–W6; hedef anlatımıdır, yapılmış deney iddiası değildir].

“Arktik'te hiç veri yok” demeyiz. Model/reanalysis ve geçmiş gözlemler var. İstenen yeni bilgi, **sefer sırasında eşleşen zaman–konum–derinlikte fiziksel gözlem ve fiziksel örnek**. Bu, kaba ölçekli modelin aynı ayrıntıyı zaten doğru verdiğini varsaymadan test etmemizi sağlar [W4,W19; önerilen bilimsel gerekçe].

İki bağlantı ayrı tutulur: **gözlem → ilgili deniz modelinin değerlendirilmesi/kalibrasyonu → belirsizlik ve ilgili karar**; **kaynak suyu → arıtma/şartlandırma → kullanılabilir su → su/enerji maliyeti → üretim sistemi**. PWN profili yıllık karasal su miktarını veya bütün Sustainable Production Frontier'ı tek başına doğrulamaz. Gözlemin kararı değiştirmemesi de geçerli sonuçtur [MASTER §14,32–34; W19].

## Çağrıdan gelen koşullar ve tasarım karşılığı

**Yeniden doğrulama:** [30 Haziran 2026 tarihli TÜBİTAK duyurusunun](https://tubitak.gov.tr/tr/duyuru/kutup-arastirmalari-2027-yili-cagrilari-acildi) doğrudan bağladığı [resmî çağrı PDF'i](https://tubitak.gov.tr/sites/default/files/2026-06/kutup_arastirmalari_cagri_metni_2027_0.pdf), 22 Eylül 2026'da yeniden incelendi. Aşağıdaki sayfalar 1'den başlayan PDF sırasıdır; F5'in ilgili maddeleriyle uyumludur. Bunlar planlanan koşullardır; kesin rota/sefer süresi değildir.

| Resmî belgede ne var? | Yer | Bizim karşılığımız |
|---|---|---|
| Haziran–Eylül 2027 içinde yaklaşık 20–40 gün; Barents Denizi; deniz üstü çalışma | F5 s.6, madde19 | Gemi üzerinden profil ve numune; karada deney zorunluluğu yok |
| Rota/süre lojistik, hava ve deniz buzu koşullarına göre değişebilir | F5 s.6, madde19 | Tek fiyort, çiftlik veya sabit koordinata bağlı araştırma yok |
| Ekipman, bakım, internet ve elektrik garanti edilmiyor | F5 s.5, madde16 | Çevrimdışı kayıt, bağımsız güç, kolay kontrol/onarım |
| Ekipman ve alınacak örneklerin lojistik formda bildirilmesi | F5 s.3, madde6 | Cihaz kütle/boyut/güç ve örnek taşıma planı uzmanlarla hazırlanacak |
| Sefer kısmen/tamamen iptal edilebilir veya değişebilir | F5 s.5, madde18 | Türkiye çalışması ve laboratuvar PoC devam eder; saha katkısı ayrı statüde tutulur |
| Bilimsel çıktı, açık metadata/nihai rapor ve Aperta paylaşımı hükümleri | F5 s.4, madde11 | İzlenebilir kayıt ve paylaşılabilir veri hazırlığı; öğrenci programı gereklilikleri ayrıca teyit |

**Rotadan bağımsız uygulama önerisi:** Sefer ekibinin uygun bulduğu istasyonda UTC/GPS ve profil kimliği → C/T/basınç profili → kalite kontrol → koşullar uygunsa amaçlı numune → yerel iki kopya kayıt. İstasyon sayısı, derinlik, vinç/halat, gemi CTD'si ve numune kapasitesi henüz garanti değildir. Kıyı çiftliği ziyareti veya kara örneklemesi araştırmanın zorunlu adımı olmayacak [MASTER §10,12–16; tasarım önerisi].

**İdari ayrım:** Yüklenen F5, profesyonel KUTUP Araştırmaları çağrısıdır. Kurumsal başvuru, bütçe, asil/yedek ve yayın hükümlerini otomatik olarak bu öğrenci ekibinin şartı gibi yazmıyoruz. Aynı seferin operasyonel çerçevesini anlamak için kullanıyoruz. Çağrıdaki 1.500.000 TL bütçe öğrenci projesine tahsis edilmiş para değildir [F5 s.2–4,10].

F5 Antarktika için TAE-XII/2028'i de içeriyor; TXT'deki öğrenci davetinde TAE-XI/2027 geçiyor. Bunlar farklı program/takvim kapsamlarıdır. Arktik kolunda TASE-VII/2027 uyumlu; bu ayrıntı öğrenci daveti ile çağrının aynı belge olmadığını ayrıca gösterir [F1:14–20; F5 s.7].

## Ulusal Kutup Bilim Stratejisi bağlantısı

| Belgede doğrulanan araştırma yönü | Konum | Projeyle bağ |
|---|---|---|
| Buzulların erimesiyle ilişkili riskleri senaryolarla değerlendirme ve çözüm geliştirme | F6 PDF s.25 / basılı s.23, **TEMA I: Küresel İklim Değişikliği** | Değişen su koşullarını senaryolarla inceleme; projemizin üretim bağlantısı kendi araştırma önerimiz |
| Kutup iklim sisteminin mekânsal/zamansal öngörülebilirliğini iyileştirme | Aynı sayfa ve başlık | Yerel deniz gözlemiyle ilgili model temsilini değerlendirme; bütün iklim modelini doğrulama iddiası yok |
| İklime dayanıklı tarım araştırmaları | Aynı sayfa ve başlık; sonlardan ikinci madde | Belgede açıkça bulunur. Su/enerji kısıtlı üretim değerlendirmesine tematik dayanak; Arktik tarım genişlemesine resmî teşvik anlamına gelmez |
| Yenilikçi saha teknolojileri; modeller/dijital ikizler; uzun dönemli veriler | F6 PDF s.34 / basılı s.32, **Öncelikli Temaların Kesim Noktasında: Destekleyici Yetkinlikler** | PWN ve modelleme yöntemi; tek sefer uzun dönem veri serisi sayılmaz |
| Açık bilim ve FAIR | F6 PDF s.21 / basılı s.19, **Stratejik Çerçeve — Temel Değerler** | İzlenebilir metadata ve paylaşılabilir sonuç |
| Bilim ve toplum ilişkisi | F6 PDF s.38 / basılı s.36, **Stratejik Çerçeve — Stratejik Amaç II**, hedef 1–2 | Gerçek deney ve sınırlarını anlaşılır anlatma |

Bu uyum, projenin resmen desteklendiği veya kabul edildiği anlamına gelmez. Araştırma hedeflerimizin ulusal stratejideki karşılığını gösterir [çıkarım].

## Önceki TASE çalışmalarından ne öğreniyoruz?

Üç araştırma çizgisi de [19 Temmuz 2024 tarihli resmî TÜBİTAK TASE-IV haberinde](https://tubitak.gov.tr/tr/haber/4-ulusal-arktik-bilimsel-arastirma-seferinde-16-projeye-yonelik-calismalar-gerceklestiriliyor) doğrulanıyor [W2].

| Araştırmacı ve geçmiş çalışma | Bizim için somut anlamı | Söylenmeyecek şey |
|---|---|---|
| **Kunter İncili:** Arktik tabakaları, Svalbard termoklin/haloklin ve buzul–akıntı ilişkileri | Hangi fiziksel geçişin anlamlı olduğunu, profil tasarımını ve yorumunu incelemek | “Bizim danışmanımız”; “ilk haloklin çalışmasını biz yapıyoruz” |
| **Aslıhan Nasıf Dondurur:** Svalbard tatlı su girişleri ve akıntılar; DEÜ yaklaşık 90 m su kolonunda veri toplandığını ayrıca bildiriyor | Referans CTD, numune tasarımı ve kaynak suyu yorumuna ilişkin önceki çalışmayı öğrenmek | 90 m'nin bizim hedef derinliğimiz veya sensör dayanımımız olduğu |
| **Çetin Biçer:** Sertifikalı algılayıcılarla WMO standartlarında deniz meteorolojisi gözlemleri | Kendi ölçüm aracımızı referansla karşılaştırmanın ve çevresel bağlamın önemi | PWN'nin WMO sertifikalı veya aynı doğrulukta olduğu |

DEÜ kaydı: [4. Ulusal Arktik Bilimsel Araştırma Seferi, 30.07.2024](https://imst.deu.edu.tr/tr/news/4-ulusal-arktik-bilimsel-arastirma-seferi-30-07-2024/) [W3]. Kurum haberleri araştırma faaliyetini doğrular; bu projelerdeki bütün bilimsel sonuçları yeniden üretmiş sayılmayız.

**Güncel unvan ile geçmiş faaliyeti ayırma:** [DEÜ güncel personel sayfası](https://imst.deu.edu.tr/tr/akademik-personel/) ve [AVESİS](https://avesis.deu.edu.tr/aslihan.nasif), Aslıhan Nasıf Dondurur'u **Doç. Dr.**, DEÜ Deniz Bilimleri ve Teknolojisi Enstitüsü olarak listeliyor. İncili'nin güncel rütbesi/görevi ve Biçer'in güncel birimi bu taramada doğrulanamadı; 2024 haberindeki unvanlar bugüne taşınmaz.

**Olası geri bildirim eşleşmeleri:** [Resmî Kutup Veri Merkezi](https://polardata.tubitak.gov.tr/members/) indeksinde Göksu Uslular, Erhan Arslan, Atilla Yılmaz ve deniz lojistiği uzmanları listeleniyor. Dinamik sayfanın doğrudan erişimi sınırlı olduğundan kanıt düzeyi, güncel rol ve sorular [RESEARCHER_OUTREACH.md](RESEARCHER_OUTREACH.md) içinde kişi bazında kaydedildi. Bunlar danışman veya destek sözü alınmış kişiler değildir.

**Görüşme planı:** Tek sayfalık proje özeti ve PWN blok şeması üzerinden sensör gereksinimi, referans CTD, örnekleme, analiz ve gemi operasyonu hakkında fikir istemek. Bu görevde kimseyle iletişime geçilmedi; alınmamış görüş mektuplara yazılmayacak [U1].

## Formun istediği kişisel ve bilimsel içerik

F4 boş bir bireysel formdur; yalnız serbest motivasyon yazısı değildir. Ödül/sertifika, sefer motivasyonu ve beklenti, projeyi Arktik'te uygulama, Türkiye'nin kutup çalışmalarını takip, yurtdışı deneyimi/kaygılar, İngilizce yeterliği, iklim değişikliği bilgisi, ek yetkinlikler, akademik çıktı, fiziksel uyum ve önceki kutup başvurusu/katılımını sorar [F4, soru başlıkları; 5 sayfa görsel kontrol].

Üç mektubun ortak omurgası:

- Konya pilotu ve su yönetimi başarısı.
- Türkiye'de geliştirme ve gelecekteki kuzey üretim problemi.
- PWN ile gemide yapılacak somut iş ve geri getirilecek veri.
- Çağrı, ulusal strateji ve önceki araştırmalardan öğrenme.
- Seçilince uzmanlarla geliştirilecek Arctic v1 [U1; Öneri].

Farklılaşacak yerler gerçek kişisel motivasyon, önceki katkı, yetkinlik ve sefer görevidir. Ali Baha için 2204-C ikinciliği kutup ilgisinin önceden geldiğini destekler; 2204-D'nin ilk günden Arktik için tasarlandığı iddiasına dönüştürülmez. Cem/Ferit için bilgi alınmadan rol/sertifika/dil seviyesi atanmaz [U1].

## Takvim ve kısa mülakat akışı

**Mülakat 30 Eylül 2026:** Kullanıcı FINAL MASTER SYNC §35 ile tarihi ve formların 48 saat önce teslimini yeniden teyit etti. TXT daveti stantta 5–10 dakika diyor. Tam saat hâlâ bilinmiyor. **İç teslim hedefi 27 Eylül**; 28 Eylül gece yarısı gibi bir saat türetilmez [MASTER §35; F1:14–27].

Önerilen 5 dakikalık çekirdek anlatım: 30 sn Konya → 30 sn Türkiye aktarımı ve evrim → 60 sn kuzeyde gelecek üretim sorusu → 60 sn su güvenliği/üretim sistemi → 90 sn Arktik, PWN ve gerçek fiziksel iş → 30 sn ekip sürekliliği/vizyon. Deney yapılmışsa gerçek grafik gösterilir; yapılmamışsa çalışma planı diye belirtilir. 10 dakika verilirse demonstrasyon ve sorular açılır [MASTER §26–29,45; öneri].
