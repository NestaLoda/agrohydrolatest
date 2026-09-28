# Açık sorular ve ne zaman çözülecekleri

22 Eylül 2026. Bu liste projeye başlamayı engelleyen bir akademik kontrol listesi değildir. Yalnız doğru sırada cevaplanması gereken soruları tutar [U3]. Kaynaklar: [kaynak kaydı](PROJECT_SOURCE_OF_TRUTH.md).

## Mülakat öncesinde netleşmesi en çok işe yarayacak beş soru

| Soru | Neyi değiştirir? | Bugünkü çalışma varsayımı | Cevap sahibi |
|---|---|---|---|
| Mülakatın ve 48 saat önceki form tesliminin kesin saati nedir? | Son teslim takvimi | 30 Eylül 2026 tarihi master metinle teyitli; saat hâlâ açık; iç hedef 27 Eylül [U5 §35; E15] | Ekip/davetin güncel kopyası |
| Elimizde hangi kart, sıcaklık probu, encoder, ölçüm aleti ve tank malzemesi var; ne zaman erişebiliriz? | İlk çalışan PWN tarihi | Donanım envanteri bilinmiyor. Satın alındığı varsayılmıyor [U1; F1:7994,8101–8105] | Ekip |
| İlk karar gösteriminin yerel katsayıları nasıl geliştirilecek? | Hikâyenin son halkası | İlk kesitte marul/açık tarla–hidroponik/tatlı su–arıtılmış deniz suyu; kaynaklı fakat yerel Arktik kalibrasyonu olmayan gösterim. Türkiye transferinde buğday kullanılıyor [MODEL_METHODS.md](MODEL_METHODS.md) | Ekip, sonra uzman geri bildirimi |
| Cem ve Ferit'in gerçek güçlü yönleri ve geçmiş görevleri neler? | Üç mektubun farklılığı | Model/veri, PWN/deney, saha/iletişim iş paketleri var; kişilere henüz atanmıyor [U1; F3 slayt1] | Üç öğrenci |
| İlk gerçek PWN kaydını mevcut yazılım kesitine ne zaman bağlayabiliriz? | Fiziksel ölçüm–grafik zinciri | Kodlama U6 ile onaylandı; parser/analiz var, gerçek tank kaydı ve fiziksel envanter bekleniyor [BUILD_STATUS.md](BUILD_STATUS.md) | Ekip ve öğretmenler |

## Bilimsel köprüde kalan gerçek sorular

**Denizdeki gözlem hangi kararı güncelleyecek?** En somut aday, belirli kıyısal kaynak suyunun tuzluluk/sıcaklık/kimya belirsizliğinin arıtma ve enerji gereksinimine etkisi. TASE rotası ile varsayımsal üretim lokasyonu aynı sistemde değilse sonuç yalnız yöntem/senaryo testi olur; yerel su temini kanıtı olmaz [U1; W4, W6; Öneri].

**Su miktarı ve sürekliliği nereden gelecek?** Bir CTD profili yıllık debi veya çekilebilir hacim vermez. Türkiye için akım/yeraltı suyu/depolama ve kullanım kayıtları; kuzey üretim senaryoları için ilgili kara hidrolojisi ve altyapı gerekir. Bunları PWN verisinden türetmeye çalışmayacağız [W12–W13; mimari çıkarım].

**İlk ürün ve yöntem seti ne kadar küçük?** Konya'nın dört ürünü geçmiş karşılaştırma içindir; hepsini hidroponik/dikey üretime taşımak zorunlu değil. İki farklı yöntem yalnız aynı üretim/beslenme hedefi ve uygun ürün grubu üzerinden karşılaştırılır [U1; F2 s.7; Öneri].

**Sürdürülebilirlik nasıl ölçülecek?** Su açığı, üretim/beslenme alt sınırı, enerji, emisyon ve çevresel baskı için ölçülebilir göstergeler seçilmeli. İlk sürüm “su ve enerji açısından koşullu uygunluk” gösterebilir; bütün sosyal/ekolojik sürdürülebilirliği kanıtladığını iddia etmez [U1; Öneri].

**Saha bilgisi işe yaradı mı?** Model hata azalması ile üretim kararındaki fark ayrı gösterilmeli. Model düzelip karar değişmeyebilir; bu da anlamlı sonuçtur. Aynı profilin satırlarını eğitim ve test diye bölmek yerine ayrı profil/istasyonlar kullanılmalı [F1:2753–2774; Öneri].

## Seçilince uzmanlarla netleşecekler

Yeni sync'te açık kalan kanıt konuları: Ali Baha'nın 2204-C proje adı/yılı/alanı ve ödül belgesi; Cem/Ferit'in gerçek katkıları; seçilen kıyısal üretim lokasyonu ile sefer istasyonları arasındaki temsil ilişkisi; bağımsız Türkiye doğrulama verisi; soğuk su arıtma modelinin geçerli aralığı; belirlenen bilimsel sinyali çözebilecek sensör hata bütçesi. Kunter İncili/Çetin Biçer'in güncel unvan/kurumu doğrulanmadan 2024 bilgisi bugünkü görev gibi yazılmaz. Svalbard'daki tarihsel üretim girişiminin bugün faal olduğu iddia edilmeyecek [E03,E06,E08,E14,E18–E19; ayrıntı: EVIDENCE_MAP ve RESEARCHER_OUTREACH].

Hipotez sonuçları da açıktır: su/enerji filtresinin etkisi sıfır çıkabilir, ortak optimizasyon bağımsız koşullarda avantaj vermeyebilir, PWN modeli doğrulayıp kararı değiştirmeyebilir. Bu sonuçların hiçbirinde başarı yüzdesi üretmeyiz [E19].

| Konu | Sorulacak somut soru | Şimdiden iddia edilmeyen |
|---|---|---|
| Oceanography | Hangi en küçük fiziksel sinyal anlamlı; T/S/p hata ve tepki süresi hedefleri ne olmalı? | Research-grade hassasiyet |
| Sefer | İzinli istasyon/depth aralığı, cast süresi, taşıyıcı/halat, gemi GPS, ekipman erişimi? | CTD, vinç veya sabit rota garantisi |
| Referans | Ön testte ve seferde hangi CTD/EC referansına erişilebilir? | Sağlanmış laboratuvar/kurum desteği |
| Numune | Yüzey/geçiş/arka plan örneği hangi koşullarda anlamlı? | Sabit istasyon ve numune sayısı |
| İzotop | δ18O/δ2H için deniz suyu matrisi kabulü, kaynak uç bileşenleri, hacim ve saklama? | Her kaynağın kesin ayrıştırılması |
| Kimya | Kullanım/arıtma modeline hangi analiz gerçekten bilgi katar? | Na, Cl, Ca, Mg, bor, alkalinitenin zorunlu tam panel olması |
| Arıtma | Besleme suyu → geri kazanım/ürün suyu kalitesi/enerji ilişkisi hangi modelle? | Hazır evrensel kWh/m³ katsayısı |
| Veri | Geçmiş TASE verileri, kullanım izni, zaman/koordinat ve referans kalibrasyon kayıtları var mı? | Açık erişim veya paylaşım izni |

Bu sorular, KARE/TASE/oşinografi araştırmacılarından görüş alma planının gündemidir; kimseye mesaj gönderilmedi [U1].

## Veri bulunmasına göre netleşecekler

- Türkiye benchmark adayları: Konya + farklı bir sulamalı havza + farklı mevsimsellikte bir üçüncü bölge. Gediz ve Çukurova/Seyhan yalnız aday; gözlem ve ürün örtüşmesi görülmeden kesin seçim yok [Öneri].
- Baz dönem, gelecek dönem ve senaryo seti. Başlangıç adayı: 1991–2020 geçmiş karşılaştırması ve 2041–2060 gelecek penceresi; verilerin ortak kapsamına göre kesinleşir [Öneri; W7–W9].
- İklim modeli sayısı, yanlılık düzeltmesi, ürün parametrelerinin aktarımı ve belirsizlik sunumu [Öneri].
- CARRA2/TOPAZ'ın sefer gününe erişimi. Reanalysis yayın gecikmesi olabileceği için sefer öncesi tahmin/analyse çıktısı ayrı arşivlenecek [W4, W9; Öneri].
- Soğukta sera/hidroponik su-enerji katsayıları: literatür ve üretici/deney verisiyle desteklenmeden hazır sayılar yazılmayacak [U1].

## Şimdilik cevaplamak zorunda olmadıklarımız

Marka adı, bütün Arktik haritası, ticari gelir modeli, tam otomatik numune sistemi, motorlu makara, tüm AI modülleri ve tüm kimya analizleri dokuz günlük kritik yol değildir. Çalışan PoC, gerçek ölçüm, anlaşılır karar bağlantısı ve ikna edici sefer planı önceliklidir [U1, U3; F1:7611–7635].
