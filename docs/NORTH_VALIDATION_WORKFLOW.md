# Bilgisayardaki hazırlık → gerçek saha ve pilot doğrulaması

23 Eylül 2026. Bu belge uygulanmış yazılım akışını ve henüz yapılmamış fiziksel işleri ayırır. Gerçek TASE/PWN numunesi veya hidroponik pilot sonucu içermez.

## Sunumda söyleyeceğimiz

“Gelecek iklim koşullarında hangi ürünleri, hangi yöntemle ve hangi su yönetimiyle üretmemiz gerektiğini bilgisayarda hesaplıyoruz. Su bulunması, o suyun üretimde kullanılabilmesi demek değil. Kar/yağışın hangi ayda depolanabildiğini modelle; kaynak suyunun sıcaklık, tuzluluk ve kullanım/arıtma özelliklerini ise uygun gözlem ve numuneyle araştırıyoruz. Seferin gerçek zaman ve konumundaki suyu modelin ne kadar iyi temsil ettiğini sınamak için Arktik saha kanıtına ihtiyacımız var. Ölçümün desteklediği girdileri güncelleyip aynı motoru yeniden çalıştıracağız. Sonucun değişmemesi de bilimsel sonuçtur.”

Tek sefer geleceğin iklimini, yıllık kara suyu miktarını, yerel zemin uygunluğunu veya bütün tarımsal sistemi doğrulamaz. Kara hidrolojisi ve enerji kapasitesi için ayrı araştırma gerekir. Gemi rotası kar/yağış/tatlı su numunesine erişimi garanti etmez; deniz örneği bunları temsil etmez.

## Çalışan bilgisayar araçları

`backend/north_validation.py` ayrı router içerir. Mevcut `north_field` PRE/POST güvenlik sınırları korunur.

| API | Gerçek işlev |
|---|---|
| `GET /api/north/validation/readiness` | Değişken → mevcut kanıt → karar bağlantısı → TASE ölçebilir mi → yöntem → sahada kalan iş listesi |
| `GET /api/north/validation/templates` | Boş CSV formları ve tam JSON şemaları; gerçek ölçüm içermez |
| `POST /api/north/validation/sample-review` | Uzmanın verdiği kullanım amacı/parametre/birim/sınırı gerçek numune kaydıyla değerlendirir |
| `POST /api/north/validation/pilot/freeze` | Pilotun ürün, yöntem, su kökeni, süre, alan, ölçüm kapsamı ve model beklentisini içerik özetiyle değişmez saklar |
| `POST /api/north/validation/pilot/compare` | Ölçümden önce dondurulmuş aynı alan/süre/kapsamla gerçek pilot toplamlarını karşılaştırır; değişmez POST kaydı üretir |

CSV dosyaları kayıt/form hazırlığı içindir; otomatik CSV içe aktarma iddiası yoktur. API JSON şemasına uygun kayıt girilir. Şablonlar `data/north/validation_templates/`; yeni pilot kayıtları `data/north/validation_records/` altında tutulur. OpenAPI `/docs` üzerinden şemalar ve işlem ekranları kullanılabilir.

## Su numunesi incelemesi

1. Numuneye ayrı kimlik, kaynak türü, UTC/konum, varsa derinlik verilir. İzin, protokol ve teslim/saklama zinciri kayıtları ilişkilendirilir.
2. Uzman belirli bir kullanım sorusu tanımlar: örneğin belirli arıtma veya kontrollü üretim yolunu değerlendirmek. Her parametrenin karar bağlantısı ve sınır kaynağı girilir. Hazır dev kimya paneli veya evrensel uygunluk sınırı yoktur.
3. Laboratuvar/saha değeri; birim, raporlanmış belirsizlik, yöntem, cihaz, kalibrasyon, kabul eden kişi ve belge SHA-256 özetiyle girilir. Yazılım bu beyanı laboratuvarın bağımsız teyidi saymaz.
4. Eksik ölçüm `measurement_needed`; birim farkı `unit_mismatch`; belirsizlik aralığının sınırı kesmesi `uncertainty_crosses_limit` üretir. Birimler gizlice çevrilmez. EC, pratik tuzluluk ve g/kg birbirinin yerine geçmez.
5. Bütün seçilmiş kontroller geçse bile çıktı yalnız `selected_checks_met` olur. Bu, genel tarımsal uygunluk veya içilebilirlik belgesi değildir. Eksik kimya/mikrobiyoloji/arıtma gereksinimlerini otomatik onaylamaz.

İzotop, iyon veya başka analiz yalnız gerçek kaynak/arıtma sorusunu yanıtlıyorsa seçilir; panel, sayı, derinlik, şişe, hacim, koruma ve taşıma uzman/laboratuvarla belirlenir. Yeniden oluşturulmuş su ayrı etiket ve reçete/kaynak kimya bağlantısı gerektirir.

## Kontrollü üretim pilotu

Önce ölçüm süresi ve alanına uygun bir beklenti oluşturulur. Yıllık plan toplamını kısa bir deneye doğrudan kıyaslamak yasaktır; pilot dönemi ve kontrol koşulları için ayrı model beklentisi hesaplanmalı ve kaynak/model kaydı belirtilmelidir. Beklenti **pilot başlamadan önce** dondurulur. Sonra aynı protokol, kaynak suyu, arıtma, alan, süre ve bütün pilotu kapsayan ölçüm sınırıyla sonuç girilir.

Karşılaştırılan toplamlar: dışarıdan eklenen yeni su (m³), elektrik (kWh), ayrı ısı enerjisi (kWh_th), hasat edilen taze kütle (kg). Devridaim debisi yeni su toplamına yeniden eklenmez. Isı ve elektrik karıştırılmaz. Her ölçü için mutlak fark ve başlangıç sıfır değilse yüzde fark; hasat sıfır değilse kg başına su/elektrik/ısı yoğunluğu hesaplanır. Sıfıra bölme “başarı” diye gösterilmez.

Gerçek deneyde yeniden oluşturulmuş su kullanılabilir; bu fiziksel deneyin sonucu gerçektir fakat **Arktik'ten alınmış su deneyi** diye etiketlenmez. Sentetik/simülasyon ölçüm kaydı kabul edilmez. Yazılım biçim, zaman, kapsam ve bütünlük denetimi yapar; belge içeriği ve cihazın gerçekten kullanılması insan kalite incelemesi ister. Tek deney istatistiksel doğrulama sağlamaz; kontrol, tekrar, hata hedefi ve çalışma büyüklüğü uzman protokolünde ayrıca belirlenir.

Bu uçlar optimizer katsayılarını otomatik değiştirmez. Profil için mevcut kısıtlı `north_field` yolu; pilot katsayıları için uzman değerlendirmesi, ayrı sürüm ve yeniden test gerekir.

## Fiziksel olarak kalan işler

- İzin, rota/istasyon fırsatı ve gemi operasyonunu sefer ekibiyle kesinleştirmek.
- PWN C/T/p donanımını kalibre etmek, referansla karşılaştırmak ve gerçek UTC/konum bağlı profilleri almak.
- Laboratuvarla yalnız karar sorusuna gerekli analizleri seçmek; izinli fiziksel su numunesi almak, saklamak, taşımak ve analiz ettirmek.
- Kara suyu miktarı/tahsisi, zemin ve yerel enerji altyapısı için ilgili yerel kurum/uzman verisini edinmek; PWN bunları ölçmez.
- Karakterize edilmiş su veya açıkça etiketli yeniden oluşturulmuş suyla kontrollü pilotu kurmak; gerçek su/enerji/bitki/arıza kayıtları almak.

Bu işler bilgisayar başında yapılmış gibi tamamlanamaz. Yazılımın şema ve testlerinin geçmesi fiziksel veri veya bilimsel saha doğrulaması üretmez.
