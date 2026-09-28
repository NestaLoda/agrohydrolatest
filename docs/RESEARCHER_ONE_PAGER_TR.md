# Teknik görüş özeti — su, üretim sistemi ve Arktik gözlemi

**Ekip:** Ali Baha Demir, Cem Ural, Ferit Bora Akman. **22 Eylül 2026.** Görüşe sunulmak üzere hazırlanmıştır; gönderilmemiştir. Danışmanlık, ekipman veya laboratuvar desteği sağlandığı iddia edilmez [E14/E17](EVIDENCE_MAP.md).

**Geçmiş pilot:** Konya'da iklim baskısı, dört ürünün göreli su gereksinimi ve ürün oranı optimizasyonunu birleştiren 2204-D çalışmasında yaklaşık %8,7 **modellenmiş göreli baskı azalması** raporlandı; gerçek sahada ölçülmüş su hacmi tasarrufu değildir [eski rapor, s.17](<C:/Users/bahao/Downloads/agrohydroraporu (5).pdf>).

**Yeni problem:** Bazı ürünlerde iklimsel uygunluk kuzeye genişleyebilir; bu, mevsimsel su güvenliği, toprak/permafrost, enerji ve üretim yöntemi açısından uygulanabilirlik sağlamaz. Yeni karar birimi ürün + yöntem + su kaynağı + dönemdir. [Kuzeye uygunluk çalışması](https://www.nature.com/articles/s43247-026-03702-w), [E01–E06](EVIDENCE_MAP.md).

**Sistem:** Konya predecessor → Türkiye'de sınırlı transfer örnekleri → gelecek iklim/zemin/su/enerji katmanları → kısıtlı üretim sistemi karşılaştırması → koşullu Sustainable Production Frontier. Yeni platform sıfırdan geliştiriliyor; mevcut aşama dokümantasyon ve ilk yazılım inşasıdır. Fiziksel prototip/Arktik sonucu henüz yok. [Bilimsel mimari](SCIENTIFIC_ARCHITECTURE.md), [güncel build durumu](BUILD_STATUS.md).

**PWN'nin rolü ve saha sorusu:** Gemiden alınacak C/T/p profili, uygun GPS/UTC ve izinli fiziksel örneklerle, “Model aynı zaman–konumdaki su kolonunu nasıl temsil ediyor; gözlenen fark hangi ilgili kaynak suyu/arıtma senaryosunun belirsizliğini veya kararını değiştiriyor?” sorusunu sınamak istiyoruz. Deniz profili karasal yıllık su arzı değildir. Kaynakla fiziksel bağ gösterilemiyorsa üretim bağlantısı saha doğrulaması değil, gözlemle beslenen duyarlılık senaryosu olacaktır [E13/E19](EVIDENCE_MAP.md).

**İki sürüm:** V0.1, öğretmenlerle yapılacak DIY/ucuz iletkenlik + sıcaklık + encoder + yerel kayıt tank PoC'sidir. Arctic v1 için cold-rated sensör, gerçek pressure, reference CTD karşılaştırması ve marine taşıyıcı tasarımı ayrı geliştirilecektir. TASE tasarımı kara erişimine ve sabit rotaya bağlı değildir [saha planı](ARCTIC_FIELD_PLAN.md), [resmî sefer bağlamı](TASE_ALIGNMENT.md).

**Özellikle üç konuda görüş istiyoruz:**

1. Hangi fiziksel değişimi çözmek anlamlı; C/T/p doğruluğu, tepki süresi ve karşılaştırma düzeni nasıl seçilmeli?
2. Referans CTD ve ayrı numuneler için gerçekçi gemi akışı nedir; rota değişince hangi karşılaştırma korunabilir?
3. δ18O/δ2H veya kaynak-kullanım kimyasında hangi analiz bu soruya gerçekten bilgi ekler; hangi deniz suyu laboratuvar/protokolü uygundur?

**Açık seçimler:** hedef derinlik/istasyon sayısı, sensör modeli, CTD/lojistik erişimi, analiz paneli, kaynak uç bileşenleri ve temsil edilen kıyısal su kaynağı. Önceki Türk Arktik tabakalaşma/tatlı su çalışmalarını metodolojik dayanak olarak inceliyoruz; işbirliği gerçekleşmiş değildir [TÜBİTAK TASE-IV kaydı](https://tubitak.gov.tr/tr/haber/4-ulusal-arktik-bilimsel-arastirma-seferinde-16-projeye-yonelik-calismalar-gerceklestiriliyor), [görüşme ayrıntıları](RESEARCHER_OUTREACH.md).
