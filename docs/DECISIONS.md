# Kararlar ve geçmiş fikirlerin durumu

22 Eylül 2026. Kaynak kodları [ana kaynak belgesinde](PROJECT_SOURCE_OF_TRUTH.md) tanımlıdır. “Kabul” kullanıcı yönünü, “Öneri” henüz uygulamaya alınmamış tasarımı ifade eder. Günlükteki eski emirler uygulanmaz.

## Güncel karar kaydı

| ID | Durum | Karar | Dayanak |
|---|---|---|---|
| D01 | Kabul | Konya gerçek pilot ve bilimsel predecessor. Geçmişi yeniden yazma. | U1; F1:5253–5268; F2 |
| D02 | Kabul | Yeni platform sıfırdan kurulacak; eski kod refactor edilmeyecek. | U1; F1:7994–8006, 8094–8096 |
| D03 | Kabul | Ana hedef su/enerji altında sürdürülebilir üretim sınırı; karar birimi üretim sistemi deseni. | U1; F1:6111–6164, 8421–8651 |
| D04 | Kabul | Önce Türkiye, birkaç benchmark ile transfer testi; haritanın tamamı validasyon sayılmaz. | U1; F1:7277–7349, 8619 |
| D05 | Kabul | PWN ana proje değil, saha gözlem katmanı. | U1; F1:4763–4774, 6150–6164 |
| D06 | Kabul | Arktik tasarımı kara çalışmasına bağımlı olmayacak. | U1; F5 s.6 madde19 |
| D07 | Kabul | V0.1 tank PoC; Arctic v1 uzmanlarla geliştirilecek ayrı konsept. | U1; F1:5915–5947, 7611–7635, 8024–8032 |
| D08 | Kabul | Analiz paneli, hassasiyet, istasyon ve derinlik sayısı henüz kilitlenmeyecek. | U1 |
| D09 | Kabul | AI klasik yöntemle karşılaştırılacak; yarar sağlamazsa klasik yöntem tercih edilecek. | U1 |
| D10 | Kabul | Üç mektup aynı proje, farklı gerçek kişisel katkılar. | U1; F1:7659–7672, 8403–8409 |
| D11 | Kabul | Görüşülmeyen araştırmacı danışman gibi yazılmayacak. | U1; F1:8035–8043 |
| D12 | Tarihsel; U6 ile aşıldı | İlk görev yalnız dokümantasyondu; beklenen açık kodlama onayı 22 Eylül 2026'da U6 ile verildi. | U1, U2, U6 |
| D13 | Kabul | Mülakat için anlaşılır amaç ve somut gösterim öncelikli; ayrıntılar süreci felç etmeyecek. | U3 |
| D14 | Öneri | İlk uçtan uca örnek, uygun kıyısal üretim senaryosunda kaynak suyu özelliği → arıtma/enerji → seçenek karşılaştırması olsun. | U1; F1:6150–6164, 7497–7534; W6 |
| D15 | Öneri | İlk yazılım sürümü modüler tek backend + tek arayüz; karmaşık dağıtık altyapı sonra gerekirse. | Dokuz günlük hedefe yönelik mimari kararı |
| D16 | Kabul; öncelik U6 ile güncellendi | FINAL MASTER SYNC bilimsel kapsamı korunur; ayrı enerji/kaynak katmanıyla toplam dokuz katman. Kodlama izni U6 ile verildi; güncel motor kapsamı U8 ile belirlenir. | U5 §0,9; U6 |
| D17 | Kabul | PWN'nin model güvenilirliği ve kaynak suyu/arıtma bağlantıları ayrı açıklanacak; deniz ölçümü kara su bütçesi sayılmayacak. | U5 §14,34; E13 |
| D18 | Kabul | Ali Baha'nın 2204-C kutup sürekliliği kişisel anlatının temel parçası; doğrulanmamış ayrıntılar eklenmez. | U5 §22; E14 |
| D19 | Kabul | Mülakat 30 Eylül 2026, formlar 48 saat önce; exact saat açık, iç hedef 27 Eylül. | U5 §35; E15 |
| D20 | Kabul | Şerif Efe Dartar'ın aktarılan tavsiyeleri deneyim/strateji girdisi, bilimsel kaynak veya resmî seçim ölçütü değildir. | U5 §25 |
| D21 | Kabul | Anlatıda doğrudan götürülme talebi yerine araştırma sorusu, fiziksel iş ve verinin karar katkısı anlaşılacak. | U5 §11,24,44 |
| D22 | Öneri | H2 aynı koşullardaki optimumu tekrar puanlayarak değil, ayrı yıl/model/koşullarda kararın kısıtları sağlamasıyla sınanacak. | E19; FUTURE_PRODUCTION_MODEL |
| D23 | Tarihsel; U6 ile aşıldı | Audit sonundaki production code/firmware bekleme kararı, U6 açık onayıyla kaldırıldı. | U5 §47–48; U6 |
| D24 | Kabul — 22 Eylül 2026 | Greenfield yazılım/firmware/veri geliştirmesi başladı; öğretmen ve hardware iletişim belgeleri ilk teslimdir. Eski kod LEGACY_REFERENCE_ONLY kalır. | [U6](C:/Users/bahao/.codex/attachments/1cc580a8-6bcb-4076-a685-cf64fe1a2c75/pasted-text.txt) |
| D25 | Uygulama kaydı — 22 Eylül 2026 | İlk çalışan yazılım kesiti, gerçek kaynaklı reanaliz paketi ve yazılım testleri BUILD_STATUS/DATA_ACCESS_LOG üzerinden izlenir. Bunlar fiziksel PWN veya bilimsel saha doğrulaması değildir. | [BUILD_STATUS](BUILD_STATUS.md), [DATA_ACCESS_LOG](DATA_ACCESS_LOG.md) |
| D26 | Tarihsel; gezinme D30 ile güncellendi — U7 | 8 adımlı anlatı ürünü beş çalışma alanlı araştırma/karar dashboard'una dönüşür. Kuzey ana ekran; Konya kısa predecessor, PWN destek modülü. Çalışan bilim ve kaynak akışları korunur. | [PRODUCT_REFOCUS](PRODUCT_REFOCUS.md) |
| D27 | Uygulandı | Türkiye seti Konya, Seyhan–Adana, Gediz–Manisa, GAP–Harran, Trakya–Edirne. Aynı dönem/ürün/depo altında karşılaştırma; tüm Türkiye validasyonu sayılmaz. | [TURKIYE_BENCHMARKS](TURKIYE_BENCHMARKS.md) |
| D28 | Uygulandı | Kuzeyde aynı EC_Earth3P_HR modeli, düzeltme kapalı, 1995–2014 / 2030–2049. Eksik 2050 ve ters Tmin/Tmax cevapları saklanıp sonuçtan çıkarıldı. SSP seçilebilir ensemble değil. | [NORTH_DATA_PLAN](NORTH_DATA_PLAN.md) |
| D29 | Uygulandı | Saha farkı zaman/konum/derinlik ve sıcaklık tanımı eşleşmesiyle sınırlandırılır. İlk UI örneği simülasyon; gerçek profil yolu kaynaklı dış kayıt ister. Tek çift otomatik kalibrasyon veya güven puanı üretmez. | backend/field.py; [PRODUCT_REFOCUS](PRODUCT_REFOCUS.md) |

E kodlarının dayanakları [EVIDENCE_MAP.md](EVIDENCE_MAP.md) içindedir. 22 Eylül master revizyonu önceki Konya sonuçlarını değiştirmedi; bilimsel kimliği, enerji katmanını, saha bağlantılarını ve mülakat teslimlerini senkronize etti.

## U8 uygulama kararları — 22 Eylül 2026

| Kod | Durum | Karar | Dayanak |
|---|---|---|---|
| D30 | Uygulandı | Ana akış bölge → mevcut desen → senaryo → önerilen desendir. Dört alan: Planlama/Simülasyon, Ürün Deseni/Karar, Saha/PWN, Kanıt/Veri. U7 dashboard ilkesi korunur. | U8; frontend/src/App.tsx |
| D31 | Uygulandı | Türkiye ve Kuzey aynı native ha/m² LP motorunu kullanır; tek marul hesabı eski API uyumluluğu için kalır. | backend/planning.py; CROP_PATTERN_ENGINE.md |
| D32 | Uygulandı | Beş ilde 21 ürün kaydı; Konya2023, diğerleri2024. İl verisini havza ortalaması, seçili ekiliş toplamını tekil arazi diye sunma. | data/agriculture/region_baselines.json |
| D33 | Uygulandı | Ürüne özel FAO örnek aşama/Kc + günlük ERA5 + depo → net sulama → randımanla brüt çekim. Çeltik ek suyu eksikse çözüme zorla sokma. | planning.crop_water; PATTERN_CONSTRAINTS.md |
| D34 | Uygulandı | Amaç önce ürün bazlı hedef karşılama oranlarının ağırlıklı toplamı; sonra su, enerji biliniyorsa enerji. Minimum üretim/pay/kapasiteler korunur. Kilogramlar beslenme puanı gibi toplanmaz. | CROP_PATTERN_ENGINE.md |
| D35 | Uygulandı | Arpa+patates+marul kuzey portföyü. Varsayılan bilinmeyen iklim/zemin açık tarlayı engeller; ayrı açık varsayım örneği hesabı gösterir. | FUTURE_NORTH_CROP_SET.md |
| D36 | Uygulandı | Eşleşen saha girdisi aynı portföyün kaynak sıcaklığını değiştirir; hedef ve kısıtlar sabit. Uyumsuz gözlem yeniden hesap üretmez. | FIELD_TO_PATTERN_UPDATE.md |
| D37 | Plan | Sera işletim geri beslemesi, başka coğrafyalara aktarım ve risk hizmeti sonraki aşamadır. Aktüeryal/sigorta ürünü veya eğitilmiş AI tamamlandı iddiası yok. | PROJECT_CONTINUITY.md |

## TXT ile güncel çerçeve arasındaki çatışmalar

| Eski fikir / ifade | Günlükte yeri | Güncel çözüm |
|---|---|---|
| Konya'nın pilot olarak adlandırılmasına itiraz | 5119–5123, 5164 | Kullanıcı 5253'te gerçek pilot olduğunu açıklıyor; itiraz geçersiz. |
| Eski Konya kodunun refactor edilmesi | 7735–7737, 7906 | 7994'te kullanıcı iptal ediyor; yeni codebase. |
| PWN'nin proje başlığı/ana amacı olması, tarımın çok sonraya bırakılması | 3404–3409, 4274–4276, 5187–5247 | Üretim sistemi kararı merkezde; PWN alt katman. |
| Model C yalnız gözlem önceliği veya model güvenilirliği üretsin | 4451–4494 | Bunlar PWN modülünde yararlı, ana platformun nihai üretim kararının yerine geçmez. |
| Konya'dan doğrudan Arktik'e geçmek | 3394–3400, 4776–4800 | Türkiye transfer aşaması eklendi. |
| Dere, göl, kara toprağı veya çiftlik deneyine bağımlı sefer | 283–294, 539–542, 609–649 | Deniz üstü profil ve uygun numune protokolü; kara verisi dış kaynaklardan. |
| Denizde düşük tuzluluk = tarımsal kullanılabilir su | 1005–1010, 1106–1117 gibi erken zincirlerde çıkarım riski | 1150–1160, 1466–1471 ve güncel kaynak düzeltir; arıtma, erişim ve hacim ayrı. |
| Mikroplastik ya da kutup suyunu Konya'ya çözüm yapma | 1505–1553 | Ana konudan sapma; proje kapsamına alınmadı. |
| Pahalı K10 EC/D300 sensörlerini hemen alma | 3446–3491 | Kullanıcı 3751–3762'de maliyeti reddediyor; v0.1 DIY iletkenlik + encoder. Eski fiyatlar geçersiz tedarik kaydı. |
| V0.1 içine tam basınç sistemi, turbidity, Arctic-ready iddiası | 2503–2558 | Tank PoC ve Arctic konsept ayrıldı. |
| Minimum 9 istasyon, sabit numune sayısı, izotopları zorunlu panel olarak kilitleme | 4282–4302, 4319–4354, 4410–4417 | Örnek eski tasarımlar; güncel karar uzmanla belirleme. |
| Sualtı canlı telemetri şartı | 1087–1100 | İlk tercih yerel kayıt ve profil sonrası hızlı analiz; iki geçişli örnekleme koşullara bağlı aday [F1:1417–1425]. |
| AUV, motorlu makara, gemide bitki deneyi | 5628–5697, 7151–7170 | Dokuz günlük çekirdekte yok. |
| Örnek %87 AI skoru veya 42/43 cm sonuçlarını gerçek başarı gibi kullanma | 5514–5516; 4015–4038 | Bunlar hayalî örnekler; gerçek deney yapılmadan sonuç yok. |
| “Bilimsel boşluk kalmadı” | 4635–4636, 7686–7688 | Önceki asistan kanaati; doğrulanmış sonuç değil. Tek somut karar bağlantısı gösterilecek. |
| Stratejide “iklime dayanıklı tarım” atfını geri çekme | 8626–8634 | PDF s.25, basılı s.23'te ifade gerçekten var; dosyanın kendisi üstün [F6]. |

Bu tablonun amacı fikir üretimini cezalandırmak değil, yanlış sürümün yeniden projeye girmesini önlemektir. Tarihçenin son yönü ve kullanıcının güncel özeti, üretim geleceği + gerçek Arktik verisi + somut araç birleşiminde tutarlıdır [U1, U3].

## Eski rapor ve sunum arasındaki farklar

- Raporun standart senaryo çarpanları 1,00 / 1,10 / 1,20; sunumun 12. slaytı 1,00 / 1,22 / 1,45 gösteriyor. İki farklı senaryo seti gibi saklanmalı [F2 s.8,16; F3 slayt12].
- Rapor s.10'daki yardımcı formül ile s.8'deki sabit senaryo tablosu aynı sayısal eşlemeyi vermiyor: yağış değişimi oran olarak alınırsa +1°C ve −%10 için 1,15 çıkar; tabloda 1,10 yazıyor. Bu, eski modelin sürüm/parametre kaydı sorusudur; yeni sistemde senaryo parametreleri tek kaynaktan üretilecek [F2; bu cümle matematiksel kontrolümüz].
- Görsel kontrol de ayrımı doğruluyor: rapor s.14 Şekil12 uygulaması +2°C/−%20 için 1,300 gösteriyor; s.13 ısı haritası aynı sonucu destekliyor. S.8 standart senaryo tablosu ise 1,20 diyor. Bu eski kayıtlar korunur, şimdi refactor veya rapor düzeltme çalışmasına dönüşmez [F2].
- Rapordaki göreli ağırlık ile FAO'nun dönemsel Kc katsayısı aynı şey olarak kullanılmayacak. Sunumda Kc adı verilmesi bu ayrımı kaldırmıyor [F2 s.8; F3 slayt11; W5].
- Rapor ekonomik değişkenleri modele katmadığını söylüyor; sunum ekonomik yorum ve AI raporu gösteriyor. Tamamlanmış kodu görmeden ikisinin aynı sürüm olduğu söylenmez [F2 s.19; F3 slayt22,28,30].
- Sunum slayt25'teki havuz/insan eşdeğerleri yeni anlatıda kullanılmayacak; %8,7 göreli endeks sonucu kullanılabilir [F2 s.17; F3 slayt25].

## Değişiklik kaydı kuralı

Yeni bir karar alınırsa tarih, karar, gerekçe, önceki karara etkisi ve kaynağı birlikte kaydedilir. Sonuçlar `planlandı`, `prototipte gösterildi`, `referansla karşılaştırıldı`, `sahada doğrulandı` statülerinden uygun olanıyla yazılır. Tasarım görseli çalışan donanım; tank sonucu Arktik sonucu; bir istasyon sonucu bütün bölgenin sonucu gibi gösterilmez [U1; Öneri: kayıt biçimi].

## U9 — 22 Eylül 2026

- **D38 / Uygulandı:** Kalıcı sol kontrol, sağ desen/veri/grafik alanı; AUTO/MANUAL, tek-parametre override, tekrarlanabilir hızlı stres. D30'un ayrı karar sayfası gezinmesi bu tek ekranla aşıldı; motor korunuyor.
- **D39 / Uygulandı:** PRE-TASE snapshot, aynı çalıştırma kimliğiyle tekrar üretim kontrolü; gözlem yalnız desteklenen deniz sıcaklığı girdisini değiştirir. Sonradan senaryo değişirse yeniden kayıt gerekir.
- **D40 / Kaynaklı veri edinildi:** NASA ACCESS-CM2 SSP245/585 2035,730 günlük nokta kaydı. Tek model/yıl bağlamı; ürün uygunluğu, tarla ET₀ veya karasal kullanılabilir hacim olarak uygulanmaz. Seçim ve hash provenansta.
- **D41 / Araştırma kararı:** İlk kuzey adayları arpa/patates/marul; alternatif ıspanak/roka/fesleğen kaynaklı yedekler, mikro filiz katsayıları eksik. Hiçbiri yerel doğrulanmış Longyearbyen önerisi sayılmaz.
- **D42 / Ürün ilkesi:** Sadeleşen etkileşim, analitik kapsamın azaltılması değildir. Su, üretim, kaynak tahsisi, kısıtlar ve iklim bağlamı tablo/grafikle incelenebilir.

Dayanak: U9 açık kullanıcı talimatı; SIMULATOR_UX, PRE_POST_TASE_EXPERIMENT, FUTURE_NORTH_CROP_SET, NORTH_WATER_SECURITY; ilgili kaynak URL/hash kayıtları.


D43 — U10: tek bilimsel simülatör. Mode/region üst çubuğu, doğrudan ürün sürgüleri, ilk açılışta LP olmadan baseline analizi, aynı motoru kullanan saha çekmecesi. Motor, provenans ve analitik tablolar korunur.


D44 — U11 / TESLİM 005: FINAL_PRODUCT_CONTRACT yetkili uygulama sözleşmesi. Normal girdiler doğrudan düzenlenir; baseline ayrı kalır. Kuzey kapasite/dengeli amaçları talep kg'den ayrılır. Aynı motorla deterministik duyarlılık ve A/B/C saha araştırması birlikte sunulur. Belirsizliklere sahte sayısal etki atanmaz.


D45 — U12: Kullanıcı kontrolü bilimsel verileri kullanıcının üretmesi demek değildir. Türkiye başlangıç hesabı otomatik; Kuzey gerçek iklimden otomatik analiz. 005 tamamlanma sınırı düzeltildi: tam otomatik Kuzey üretim motoru henüz eksik. Manuel örnekle bu açık kapatılmış sayılmaz.
