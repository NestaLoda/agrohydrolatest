# AgroHydro · 17 ayrı PNG slayt · Güncel teslim 032

28 Eylül 2026. Son kullanıcı master promptu esas alındı. 17 slaydın tamamı sırayla üretildi; her biri 1920×1080 PNG. Bu görevde PPTX, PDF veya birleşik sunum dosyası hazırlanmadı. Önceki 031’deki 2560×1440, tek tek onay ve 3 yedek slayt kararı artık geçerli değildir.

## Kullanılacak dosyalar

`slides/slide_01.png`–`slides/slide_17.png`. `AgroHydro_17_Slayt_PNG.zip` yalnız bu 17 PNG’yi içerir. PNG’ler bağımsız kullanılabilir. SVG/HTML dosyaları iç üretim kaynaklarıdır. Önceki teslimin `editable/slide_01.pptx`, eski layout JSON ve eski build scripti tarihsel çalışma kaynaklarıdır; bu PNG paketinin parçası değildir ve bu tur üretilmedi.

## Akış

Süreler konuşma planlama tahminidir; otomatik video/oynatıcı oluşturulmadı. Toplam 510 saniye / yaklaşık 8 dakika 30 saniye.

| PNG | Ana mesaj | Anlatım |
|---|---|---|
| slide_01.png | Desenden Dengeye | 20 sn |
| slide_02.png | Bugünün su problemi | 30 sn |
| slide_03.png | Konya pilotu ve %8,7 | 35 sn |
| slide_04.png | Türkiye’ye transfer | 25 sn |
| slide_05.png | İklimsel kuzeye kayış | 35 sn |
| slide_06.png | İklim uygunluğu yeterli değil | 25 sn |
| slide_07.png | Kuzeyde su yönetimi | 35 sn |
| slide_08.png | Yeni araştırma sorusu | 20 sn |
| slide_09.png | Gerçek karar destek sistemi | 30 sn |
| slide_10.png | 2051 gerçek motor örneği | 45 sn |
| slide_11.png | Model ve saha | 25 sn |
| slide_12.png | PWN prototip şeması | 40 sn |
| slide_13.png | PWN ve ayrı numune | 30 sn |
| slide_14.png | Kontrollü hidroponik deney | 40 sn |
| slide_15.png | Araştırma zinciri | 25 sn |
| slide_16.png | Ekip | 30 sn |
| slide_17.png | Kapanış | 20 sn |

## Kaynak ve kanıt sınırları

- Slayt 02: Konya yeraltı suyu/obruk bağlamı, Konya AFAD IRAP ve obruk araştırmaları. [AFAD proje kaydı](https://konya.afad.gov.tr/obruk-alanlarinin-tespit-edilmesi-projesi-calismalari), [Konya IRAP](https://konya.afad.gov.tr/kurumlar/konya.afad/E-Kutuphane/Il-IRAP-Planlari/KONYA-Il-IRAP-Plani-.pdf). Fotoğraf önceki kullanıcı sunumundan çıkarıldı; özgün fotoğrafçı/konum doğrulanamadığından Konya’da çekilmiş saha fotoğrafı olarak sunulmadı, temsili kuraklık etiketi var.
- Slayt 03: `data/references/konya_original_report.pdf`, tarihsel pilot. Mevcut alan payları 47 / 30,3 / 14,6 / 8; önerilen 47 / 45 / 5 / 3. Rapordaki yuvarlatılmış değerler korundu. Göreli baskı 15.702.550 → 14.338.276; yaklaşık %8,7, ölçülmüş m³ tasarrufu değil.
- Slayt 04: [Natural Earth resmi vektör deposu](https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_110m_admin_0_countries.geojson), yerel kopya `assets/turkey_naturalearth.geojson`; bölge koordinatları mevcut proje bağlamıyla eşleşiyor. Noktalar havza sınırı veya tam hizmet kapsamı iddiası değil.
- Slayt 05: [Xu vd. (2026)](https://www.nature.com/articles/s43247-026-03702-w), DOI 10.1038/s43247-026-03702-w. 7 ürün, 5 iklim modeli; 1980–2010’a göre 2071–2100 kuzey iklimsel uygunluk sınırı ortalama kayması: SSP1–2.6 ≈331 km, SSP5–8.5 ≈739 km. Gerçek ekili alan kayması veya kesin gelecek üretimi değildir; uygulamanın 3 modeliyle bu literatürün 5 modeli karıştırılmaz.
- Slayt 09: `docs/verification/north-final-030/north-no-desal-2051.png` gerçek uygulama görüntüsü, 25 Eylül 2026 kaydı. Tarihi slaytta görünür. Yeni ekran testi yapılmış gibi sunulmadı.
- Slayt 10: `assets/slide_10_request.json` ve `slide_10_result.json`. 28 Eylül 2026’da mevcut `plan_north` + `summarize_decision` yeniden çalıştırıldı. İstek 2051, SSP245, Longyearbyen, dengeli/taze ürün, 100 m², 100 m² toplama yüzeyi, %80 toplama, 10 m³ seçili depo, tatlı su tahsisi 0, arıtma seçeneği açık, enerji üst sınırı yok, asgari ürün alan payı %5. Deniz kaynak koşulları 35 g/kg, 2°C, geri kazanım 0,45; bu planda arıtılmış deniz suyu tahsisi 0. Yeni su 14,2049931299 m³/yıl, tümü aylık planda depolanan yağış/kar; ürün alanı alabaş %75, beş diğer ürün %5. Hidroponik %94,5857 / sera %5,4143. Hasat analoğu 4204,3675 kg/yıl. Elektrik 117605,4455 kWh/yıl, ısı 1625,816 kWh_th/yıl; COP=1 ile 119231,2615 kWh/yıl elektrik eşdeğeri. Elektrik eşdeğeri doğrudan yalnız elektrik ölçümü değildir. Günlük çatı/depo tekrar hesabındaki kritik Mayıs 1,168259 m³ yedek su ihtiyacıdır (MRI-ESM2-0), nihai karşılanmayan su veya en yüksek su talebi değildir. Boş depo başlangıcının etkisi slaytta korunur. Yıllık kaynak kapanışı, günlük güvenilirlik garantisi sayılmaz. 100 m² normalize plan; yerel tesis/arsa/tahsis veya ölçülmüş hasat iddiası yok.
- Slayt 12–14: PWN ve hidroponik çizimleri açıkça şematik. Gerçek prototip/Arktik/pilot fotoğrafı veya ölçümü bulunmadığı için uydurulmadı. v0.1 prensibi ile Arktik C/T/basınç hedefi ayrı. Numune ayrı örnekleme; panel uzman/laboratuvar/izinlere bağlı. Deney sütununda sıfır yerine “Henüz ölçülmedi”. Yeniden oluşturulmuş su, gerçek Arktik numunesi değil. Deney bütün Arktik tarımını doğrulamaz.
- Slayt 16: isimler, başarılar ve roller kullanıcı/ekip beyanı. Sertifika veya portre üretilmedi.
- Slayt 01/17 çevre arka planı önceki image_gen varlığı; temsili montaj, gerçek konum/saha görüntüsü değil.

## Üretim ve doğrulama

PNG-only builder `.build/build_slides_png.mjs`; her sayfayı sırasıyla Chrome/Playwright ile işler. Kaynak ve hesap hazırlığı `.build/calculate_slide_scenario.py`. Paket kontrolü `.build/validate_package.py`. Son kayıt `.build/final_verification.json`; metin geometrisi `.build/png_qa.json`.

17/17 boyut, dosya adı, PNG decode, UTF-8, SVG metin taşma/örtüşme, su kaynak kapanışı, ürün/yöntem alan kapanışı, kritik dönem anlamı, ölçüm yok etiketi ve ZIP içeriği kontrolleri geçti. Her slayt görsel olarak incelendi. Türkçe metin görsel modeline yazdırılmadı. Son uygulama testi 25 Eylül 2026 teslim 030’dur; backend test paketi/üretim build’i bu sunum görevinde yeniden çalıştırılmadı.
