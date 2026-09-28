# Güncel rebuild kaydı · 22 Eylül 2026

Aynı amaç kuralıyla kaynaklı aday çözümlemesi her koşuda korunur. Kapasite tabanlı su/enerji önceliğinde de normalizasyon kaynak koşuluyla yeniden hesaplanır. Deney deterministik uç nokta taramasıdır; EVSI veya güven yüzdesi değildir. Kimya/salinite bağlantıları eksik; fiziksel panel uzmanla belirlenecek.

Bağlayıcı sözleşme: [REBUILD_CONTRACT.md](REBUILD_CONTRACT.md). Çalışan/eksik ayrımı: [REBUILD_EVIDENCE_AUDIT.md](REBUILD_EVIDENCE_AUDIT.md), [BUILD_STATUS.md](BUILD_STATUS.md).

---

## Önceki ayrıntılı kayıt (tarihsel uygulama durumları kendi tarihleriyle okunur)

# Karar belirsizliği ve saha bilgisinin değeri

22 Eylül 2026 · FINAL_PRODUCT_CONTRACT uygulaması.

Çalışan özellik: POST /api/decision-information aynı üretim motoruyla referans + altı tek-değişken deneyi çalıştırır. Her çalıştırma mevcut provenans altyapısına kaydedilir. Planlama amacı ve diğer girdiler sabittir.

| Değişken | Tarama | Aralık kanıtı | TASE doğrudan ölçebilir mi? |
|---|---|---|---|
| Mevsimsel tatlı su kapasitesi | Mevcut ×0,8 / ×1,2 | Açık stres varsayımı, güven aralığı değil | Hayır; hidroloji/tahsis/depo |
| Enerji bütçesi | Mevcut ×0,8 / ×1,2 | Açık stres varsayımı | Hayır; üretim altyapısı |
| Deniz kaynak sıcaklığı | 5 / 18°C | Bağlı arıtma ilişkisinin literatür alanı; Arktik olası sıcaklık aralığı değil | Evet; eşleşmiş kalibre profil |
| Tuzluluk / EC | Hesaplanmıyor | Sayısal kaynak-kalite/arıtma bağı henüz yok | Evet; sensör ve salinite dönüşümü gereklilikleriyle |
| Kaynak kimyası | Hesaplanmıyor | Tepki modeli ve laboratuvar paneli eksik | Numune/protokol uygunluğuyla |

Sonuçlar: üretim tahsisi, su/enerji, uygulanabilirlik ve bağlayıcı kısıt farkları. Sabit HIGH/MEDIUM etiketleri atanmaz. Desen değişmediyse açıkça değişmedi yazılır. Sadece kaynak tüketimi değişmiş olabilir; ayrıntıda ayrıca görünür. Geçerli referans desen yoksa etki derecesi üretmek yerine önce veri gereksinimi bildirilir.

Bu olasılıksal EVSI/EVPI değildir. Olasılık dağılımı, ekonomik fayda veya güven yüzdesi yoktur. Uç noktalar arasındaki bütün eşikler veya parametre etkileşimleri kapsanmaz. Sefer önceliği belirlemek için aralıkların yerel verilerle, ölçüm hassasiyetinin uzmanla ve operasyonel uygunluğun sefer ekibiyle değerlendirilmesi gerekir.

Kaynaklar: [bağlı parametre kaydı](../data/literature_parameters.json), [motor](../backend/planning.py), [duyarlılık hesabı](../backend/information_value.py), [araştırma sözleşmesi](FINAL_PRODUCT_CONTRACT.md). Gerçek saha sonucu değil; yöntem ve kullanıcı senaryosu.

Kapasite ve dengeli planlarda her denemede tek ürün üst potansiyelleri yeniden hesaplanır. Dolayısıyla aynı planlama kuralı korunur, fakat normalizasyon katsayıları sabit değildir. Sonuç salt sabit amaç katsayılı kaynak marjinali diye yorumlanmaz. Referans uygulanamazken deneme uygulanabilir olursa bu bir uygulanabilirlik farkı olarak raporlanır.
