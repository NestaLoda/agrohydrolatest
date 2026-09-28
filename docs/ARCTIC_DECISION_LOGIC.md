> U11 güncel bağlam: [FINAL_PRODUCT_CONTRACT](FINAL_PRODUCT_CONTRACT.md), [FUTURE_NORTH_DECISION_MODEL](FUTURE_NORTH_DECISION_MODEL.md) ve [ARCTIC_RESEARCH_PROGRAM](ARCTIC_RESEARCH_PROGRAM.md) geçerlidir. Aşağıdaki bilimsel ayrıntılar korunur; eski UI adları güncel arayüz gereği değildir. Saha araştırması yalnız sıcaklık/arıtma hesabından ibaret değildir: A profil, B numune, C karar bilgisi birlikte planlanır.

# Arktik karar mantığı — TESLİM 004

22 Eylül 2026. Kullanıcının FINAL UX + ARCTIC LOGIC CORRECTION talimatı (U9) ürün ve deney çerçevesidir. Aşağıdaki “çalışıyor” ifadeleri mevcut kodu; “plan” ifadeleri henüz doğrulanmamış araştırma bağlantılarını anlatır.

## Asıl karar

Gelecek iklim altında **hangi ürün + yöntem + su kaynağı + dönem** seçilmeli? Çalışan çekirdek eğitilmiş AI modeli değil, `backend/planning.py` içindeki matematiksel optimizasyondur. Türkiye ve Kuzey aynı hesap motorunu kullanır.

Fiziksel kar/buz/yağış varlığı, üretim yerinde ve döneminde güvenilir kullanılabilir su kapasitesiyle eşit değildir. Üretim için suyun zamanı, erişimi, depolanması, kalitesi, arıtılması ve enerjisi ayrı girdilerdir. Bugünkü motor kaynak bazında dönemlik kapasite bütçesi kullanır; aylık kar erimesi–akış–depolama işletmesi modeli henüz yoktur. Kapasite alanına sayı yazılması bu hidrolojinin doğrulandığı anlamına gelmez.

## Ayrı tutulacak iki su problemi

| Problem | Gerekli kanıt | PWN rolü |
|---|---|---|
| Karasal üretim suyu miktarı ve güvenilirliği | Havza hidrolojisi, erime/akış mevsimselliği, mevcut kullanım, erişim ve depolama | Yıllık miktarı ölçmez |
| Deniz kaynak suyunun yerel fiziksel durumu | Aynı zaman/konum/derinlikte model ve gözlem, kalite/kalibrasyon metaverisi | Sıcaklık, iletkenlik/tuzluluk ve derinlik profili planlanır |
| Arıtma kullanılabilirliği | Besleme kimyası, arıtma tasarımı, verim ve enerji | Uygun numunelerle kaynak karakterizasyonuna katkı planlanır |

Bir sefer istasyonunun besleme suyunu bir üretim sahasına bağlamak ayrıca fiziksel temsil gerekçesi ister. Eşleştirme kontrolünün geçmesi tek başına uzun dönem/farklı konum aktarımını doğrulamaz.

## Çalışan saha–karar bağlantısı

`frontend/src/workspaces/PatternField.tsx` PRE-TASE senaryosunu ve hesap sonucunu kaydeder. `/api/pattern-field-update`, aynı `recorded_simulation` işlevini iki kez çağırır. Geçerli eşleştirme halinde **yalnız `seawater_temperature_c`** değişir. Bu değişken mevcut arıtma enerji senaryosuna girer; kapasite, ürün hedefleri, verim, alan, enerji bütçesi ve karasal kaynak miktarı değişmez.

Bugünkü örnek model suyu 10 °C, gözlem senaryosu 5 °C değerleri **varsayımdır**. Otomatik indirilmiş Arktik okyanus profili veya gerçek PWN ölçümü değildir. Sıcaklık–arıtma hesabının uygulama sınırları `backend/science.py` ve mevcut kaynak kayıtlarıyla değerlendirilmelidir; bu deney tuzluluk/kimya etkisini çözmez.

## PRE-TASE çıktısının etiketi

Arpa + patates + hidroponik marul örneği: **AÇIKLAYICI / VARSAYIMA DAYALI SİMÜLASYON**. Üç ürünlü optimizasyonun çalıştığını gösterir; Longyearbyen için doğrulanmış gelecek üretim önerisi değildir. Varsayımsal saha uygunluğu, manuel sulama ihtiyacı, aktarılan verim ve enerji katsayıları otomatik kaynak veri görünümünde sunulmamalıdır.

Gelecek iklim veri özeti, toprak/permafrost, karasal hidroloji ve okyanus kaynağı ayrı kanıt katmanlarıdır. Tam yerel PRE-TASE üretim önerisi için bu girdiler ve temsil sınırları tamamlanmalıdır. Belirsiz parametreler “bilinmiyor / varsayım / saha gözlemi gerekli” kalır; boşluklar ölçüm gibi doldurulmaz.

## PWN'nin konumu

MODEL / VARSAYIM → PWN + izinli fiziksel numune → desteklenen girdinin güncellenmesi → AYNI KARAR MOTORU → üretim deseni karşılaştırması.

Bu zincir, PWN'yi ana ürün yapmaz. Ana ürün su ve sürdürülebilir üretim karar desteğidir. Türkiye simülatörü için ikinci bir PWN kampanyası gerekmiyor; resmî tarım verisi, meteoroloji/reanalysis, hidrolojik kayıt ve açık senaryo varsayımları kullanılır (U9 kullanıcı kararı).

## Kaynak ve uygulama izi

- Ürün kapsamı ve seferin rolü: U9 kullanıcı talimatı; `PROJECT_SOURCE_OF_TRUTH.md`, `TASE_ALIGNMENT.md`.
- Mevcut hesap ve doğrulama davranışı: `backend/planning.py`, `backend/field.py`, `backend/app.py` `/api/pattern-field-update`; `tests/test_planning.py`.
- İklim, ürün ve veri eksikleri: `FUTURE_NORTH_CROP_SET.md`, `NORTH_WATER_SECURITY.md`, `DATA_REQUIREMENTS.md`.
- Deney protokolü: `PRE_POST_TASE_EXPERIMENT.md`.

Bu belge yeni dış kaynaklı ölçüm sonucu veya akademik doğrulama iddiası içermez; mevcut uygulama ve kullanıcı kapsam kararlarının kaydıdır.

