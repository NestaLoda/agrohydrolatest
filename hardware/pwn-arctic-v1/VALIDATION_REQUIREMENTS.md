# Arctic v1 doğrulama yolu

**Plan, sonuç değil.** V0.1'in tankta çalışması Arctic ölçüm niteliğini kanıtlamaz [E13/E16](../../docs/EVIDENCE_MAP.md).

| Aşama | Yapılacak kontrol | Saklanacak kanıt |
|---|---|---|
| Laboratuvar | C/T/p uygun referans; tepki, tekrar, drift | Ham veri, referans kimliği/kalibrasyonu, karşılaştırma |
| Gövde/güç | Uzman kontrollü soğuk, sızdırmazlık ve hedefe uygun basınç testi | Gerçek test koşulu, süre, sonuç; test edilmeyen rating yok |
| Yerel deniz | İzinli indirme/geri alma, GPS/UTC, veri kaydı | Cast metadata, arızalar, tekrar ve CTD varsa eşleme |
| Arktik | İmkan varsa CTD ile zaman/yer/derinlik karşılaştırması | Hata ve temsil farkı; erişilemediyse açık sınır |
| Model | Baseline vs düzeltme; ayrı cast/istasyon | Bias/RMSE ve aralık kapsaması; aynı profile fit/test yok |

Derinlik, accuracy, batarya süresi ve kabul eşikleri hedef sinyalle uzmanlar tarafından belirlenir; bu belge sayısal sertifika üretmez. Profesyonel CTD'nin de referans kaydı ve zaman/konum farkı görünür olur. [Ayrıntılı PWN doğrulaması](../../docs/PWN_VALIDATION_PLAN.md).

Model hatası, belirsizlik aralığı ve üretim kararının değişmesi farklı sonuçlardır. Gözlem güncellemesi fayda sağlamayabilir; aynı seçeneği destekleyebilir. Kıyısal su kaynağıyla fiziksel bağ yoksa üretim hesabı gözlemle beslenen senaryo olarak kalır. [RQ3/H3](../../docs/FUTURE_PRODUCTION_MODEL.md).

Adaptif örnekleme üstünlüğü iddiası için eşit numune bütçesi ve bağımsız referans gerekir; imkan yoksa yalnız öneri akışı gösterilir. Kimyasal/izotop analizi olmadan kaynak veya kullanım sonucunu sensör grafiğinden tamamlamayız [E10/E11](../../docs/EVIDENCE_MAP.md).
