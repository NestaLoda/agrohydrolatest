# Jüri soruları — kısa ve savunulabilir yanıtlar

22 Eylül 2026 · U11. Kaynak: [nihai sözleşme](FINAL_PRODUCT_CONTRACT.md), [kanıt haritası](EVIDENCE_MAP.md), [saha programı](ARCTIC_RESEARCH_PROGRAM.md). Canlı test sayıları burada tekrarlanmaz; [BUILD_STATUS.md](BUILD_STATUS.md) güncel kayıttır.

**Projeniz nedir?** Değişen iklim ve su koşullarında nerede, hangi üründen ne kadar, hangi yöntem ve kaynakla üretileceğini hesaplayan bir karar destek simülatörü.

**Konya'yla Arktik'in bağlantısı ne?** Konya'da ürün deseni–su baskısı kararını araştırdık. Aynı karar mantığı Türkiye'ye aktarılıyor; geleceğin kuzeyinde yöntem, su kaynağı, toprak ve enerji değişkenleri ekleniyor. Konya projesini baştan Arktik için yaptığımızı söylemiyoruz.

**Bu AI mı?** Çekirdek matematiksel optimizasyon. Öğrenilmiş bir model gibi sunmuyoruz. İleride anomali/kalibrasyon/örnekleme için AI faydası klasik yöntem karşısında gösterilirse kullanılır.

**Kullanıcı cevabı zaten girmiyor mu?** Türkiye'de mevcut üretim doğal başlangıçtır. Kuzeyde kullanıcı açık planlama amacını ve kaynak koşullarını seçer; motor dağılımı hesaplar. Tanımlı talep sepetini karşılamak ayrı bir amaçtır. Normalizasyon ve öncelikler gizli puan değildir.

**Gerçek veri var mı?** Beş ilin resmî tarım kayıtları, tarihsel reanaliz ve dış gelecek iklim serileri var. NASA 2035 SSP245/585 örneği tek model/tek yıldır. Yerel kuzey tarım katsayılarının ve su tahsisinin tamamı doğrulanmış değil. Kaynaklı, hesaplanmış ve kullanıcı varsayımı ayrılır.

**Arpa/patates/marul neden?** Tahıl, yumru ve kontrollü yapraklı yöntemi temsil eden araştırılmış ilk adaylar. Kuzey çeşit/deney emsalleri var; Longyearbyen'e yerel uygunluk onayı yok. Ispanak/roka/fesleğen yedek kanıt havuzunda; eksik katsayıyla motora zorlanmıyor. [Portföy](FUTURE_NORTH_CROP_SET.md).

**Arktik'te çok su yok mu?** Su fiziksel olarak bulunabilir; gereken mevsim/konumda erişilebilir, depolanabilir ve uygun kalitede olması ayrı sorudur. Her Arktik bölgesi susuz demiyoruz. Karasal miktar, kaynak kalitesi ve arıtma enerjisi ayrı katmanlardır.

**Neden uzaktan çalışmıyorsunuz?** Uzaktan model başlangıcı gerekli. TASE, aynı yer/zamandaki fiziksel profil ve gerçek numuneyle modeli sınama olanağı verir. Bu gözlemi yeni bir veri tabanı satırı gibi önceden var sayamayız. Elde edilen bilginin kararı etkileyip etkilemediğini de test ederiz.

**TASE'de tam olarak ne yapacaksınız?** A: izinli C/T/p profili ve varsa reference CTD ile model karşılaştırması. B: anlamlı derinliklerden izinli, hedefli numune. C: bilimsel olarak desteklenen girdileri güncelleyip aynı optimizerle PRE/POST karşılaştırması. Gradient destekli örnekleme ancak operasyon uygunsa ikincil çalışmadır.

**PWN yıllık sulama suyunu bulacak mı?** Hayır; yerel deniz suyu kolonu bilgisini sağlar. Yıllık karasal tahsis hidroloji, erişim, depo ve diğer kullanımlar üzerinden hesaplanır. Bu ayrımı yazılımda da koruyoruz.

**PWN'nin özgünlüğü nedir; CTD zaten var?** CTD'nin yerine yeni bir bilimsel standart icat ettiğimizi söylemiyoruz. Öğrenci düzeyindeki fiziksel prototipi, kalite/eşleştirme kaydı ve karar güncelleme deneyine bağlayan bir araştırma iş akışı geliştiriyoruz. Arctic v1 referansla doğrulanmalı.

**Prototip hazır mı?** Güncel gerçek durum BUILD_STATUS'tadır. Yazılım simülasyonu fiziksel üretim değildir. İlk fiziksel hedef homojen ve tabakalı tanktan gerçek CSV; tank ölçümü Arktik ölçümü diye etiketlenmez.

**Hangi kimyasal analizler kesin?** Henüz panel kilitli değil. Kaynak sorusu için izotoplar; kullanım/arıtma için tuzluluk ve gerekçeli iyon/alkalinite adayları var. Her analiz karar sorusuna bağlanacak; laboratuvar/taşıma protokolü uzmanla kesinleşecek.

**Bugün yalnız sıcaklık–arıtma mı bağlanıyor?** Önceki çalışan dar gösterim bu. Araştırma programı bundan geniş: model-profil doğrulaması ve numune karakterizasyonu da çıktı. Tuzluluk veya kimya ölçülünce doğrulanmış bağıntı olmadan tüm motoru etkiliyormuş gibi yapmayacağız.

**Desen hiç değişmezse başarısızlık mı?** Değil. Model doğru temsil etmiş olabilir veya o girdi kararı sınırlamıyor olabilir. Model hatası, karar farkı ve belirsizlik ayrı raporlanır. Tek ölçümle “güven arttı” sonucu garanti edilmez.

**Bilgi değeri nasıl hesaplanıyor?** İncelenen açık aralıklarda aynı motor yeniden çalıştırılır; desen/fizibilite/kaynak farkı gösterilir. Olasılık ve ekonomik kayıp modeli olmadan parasal veya olasılıklı VOI iddiası yoktur. TASE'nin ölçemediği yüksek etkili bilinmeyenler de görünür kalır.

**Gemide sebze mi yetiştireceksiniz?** Hayır. İzinli numune dönüşü ve laboratuvar koşulları sağlanırsa sefer sonrası kaynak suyu–arıtma–kontrollü büyüme deneyi planlıyoruz. Numune taşınamazsa ölçülen kimyaya göre yeniden oluşturulmuş su kullanılabilir ve böyle etiketlenir.

**Bu deney neyi doğrular?** Belirli kaynak/işlem koşulunun seçili kontrollü üretimle uyumunu ve su/enerji/verim varsayımını. Bütün kuzey ürün desenini veya 2050 tarımını doğrulamaz. [Deney taslağı](SOURCE_WATER_TO_GROWTH_VALIDATION.md).

**%8,7 gerçek su tasarrufu mu?** Orijinal raporun modellenmiş göreli su baskısı azalması. Sahada ölçülmüş m³ tasarruf değil. Yeni motorun su bütçesi sonuçları da model kapsamıyla ayrı sunulur.

**Seferden sonra?** Kontrollü üretim önerisi çıkarsa küçük sera/hidroponik pilotta gerçek su, enerji, çözeltinin durumu, verim ve arızaları kaydederiz; model–gerçek farkını azaltırız. Kamu/çiftçi planlaması ve sigorta araştırması daha sonraki bağımsız doğrulama gerektiren uygulamalardır.

**Kim danışmanınız?** Görüşülmüş ve anlaşılmış kişi varsa gerçek rolüyle söylenir. Önceki çalışmalarını okuduğumuz araştırmacılar danışmanımız diye yazılmaz. KARE/TASE uzmanlarından sensör, örnekleme, gemi ve laboratuvar metodolojisi için geri bildirim hedefliyoruz.
