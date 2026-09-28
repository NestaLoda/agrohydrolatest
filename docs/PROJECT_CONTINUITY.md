# Projenin sürekliliği

22 Eylül 2026 · U11 / [nihai ürün sözleşmesi](FINAL_PRODUCT_CONTRACT.md). Ana ürün, değişen iklim/su koşullarında **nerede, hangi üründen ne kadar, hangi yöntem ve kaynakla üretileceğini** hesaplayan karar destek simülatörüdür. Motor matematiksel optimizasyondur; eğitilmiş AI modeli değildir.

| Aşama | Somut soru/çıktı | Durum ve sonraki bağlantı |
|---|---|---|
| Konya pilotu | Mevcut ürün deseninin göreli su baskısını azaltabilir miyiz? | Orijinal raporda yaklaşık %8,7 modellenmiş göreli azalma; gerçek m³ tasarrufu değil. |
| Türkiye | Resmî bölgesel ürün deseni ve seçilen su koşullarında hangi alanlar değişmeli? | Beş il/21 ürün kaydı ve ortak motor; senaryo bütçesi gerçek tahsis gibi sunulmaz. |
| Gelecek kuzey | Kaynak kapasitesi ve açık amaç altında hangi ürün–yöntem–kaynak deseni mümkün? | Araştırılmış adaylar, iklim verisi ve eksik yerel parametreleri görünür açıklayıcı hesap. |
| Kritik belirsizlik | Hangi girdi seçilen kararı değiştirebilir? | Kaynaklı/açık senaryo aralığıyla duyarlılık; etkisi hesaplanmayan değişkene sahte önem skoru yok. |
| TASE | Model su kolonunu temsil ediyor mu; numune hangi kaynak bilgisini ekliyor? | A: profil/model; B: hedefli numune; C: aynı motorla karar karşılaştırması. Fiziksel saha henüz yapılmadı. |
| Sefer sonrası kontrollü deney | Kaynak/arıtma koşulu kontrollü üretimle uyumlu mu? | Gerçek veya açıkça yeniden oluşturulmuş suyla küçük deney; onaylanmış laboratuvar protokolü değil. |
| Sera/hidroponik pilot | Gerçek su/enerji/verim modelle ne kadar uyuşuyor? | RQ5 devam hattı; yerel parametre ve bağımsız test verisi. |
| Yaygınlaşma | Bölgesel/kamusal/çiftçi planlamasında aynı yaklaşım çalışır mı? | Yeni veri ve bağımsız doğrulama gerekir; sigorta olası araştırma hattı, mevcut aktüeryal ürün değil. |

Kaynaklar: [kanıt haritası E12/E20–E26](EVIDENCE_MAP.md), [aday portföyü](FUTURE_NORTH_CROP_SET.md), [Arktik programı](ARCTIC_RESEARCH_PROGRAM.md), [kontrollü deney](SOURCE_WATER_TO_GROWTH_VALIDATION.md). Güncel yazılım/test tamamlanması [BUILD_STATUS.md](BUILD_STATUS.md) ile izlenir; bu yaşam döngüsü tablosu her aşamanın tamamlandığı anlamına gelmez.

## Tek ürün, üç bilimsel durum

Türkiye'de kaynak başlangıcı mevcut ürün desenidir. Kuzeyde başlangıç araştırılmış adaylar, mevcut kaynak bilgisi ve **açık planlama amacıdır**; kullanıcıdan cevabı oluşturacak keyfî kg hedeflerini doldurması beklenmez. Tanımlı talebi karşılama ayrı bir amaç olabilir. Saha güncellemesinde aynı amaç/kısıtlar korunur ve yalnız gözlemin desteklediği girdi değiştirilir.

Etkileşimde kaynak verisi otomatik gelir; değiştirilen değer MANUEL SENARYO olur. Ayrı AUTO/MANUAL dünyaları ve her sıradan kontrol için kilit açma gereksinimi U11 ile kaldırılan eski yaklaşımdır. Sol kontrol/sağ desen akışı ve tek hesaplama düğmesi korunur. Destekleyici kanıt ve saha araştırması ikincil ayrıntılardır.

## Ölçüm geri beslemesi

PWN ve fiziksel numune deniz suyu sistemine yeni kanıt ekler. Karasal yıllık su tahsisi ayrı hidroloji işidir. Model ile gözlemin uyuşması, kararın değişmemesi veya ilgili kaynak senaryosunun uygulanamaması da sonuçtur. Gözlem sayısı ve yöntem desteklemiyorsa “belirsizlik azaldı” otomatik çıkarımı yapılmaz.

Kontrollü üretim önerildiğinde pilotta su, elektrik/ısı, sıcaklık/nem, besin çözeltisi, verim ve arıza kaydı tutulur. Aynı hasat verisiyle hem katsayı ayarlayıp hem bağımsız doğrulama iddia edilmez. Sera bütün projenin yerini almaz; önerilen bir yöntemin gerçek işletme testi olur.

İlk fiziksel iş sefer değildir: homojen ve tabakalı tankta PWN v0.1, gerçek CSV ve referans karşılaştırması. Tank verisi Arktik verisi olarak etiketlenmez. Arctic v1 hassasiyet/CTD/gemi/numune tasarımı KARE/TASE ve uygun uzman görüşü gerektirir; görüşülmemiş kimse danışman değildir.
