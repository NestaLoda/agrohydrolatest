# PWN Arctic v1 — ayrı mühendislik konsepti

Bu altı dosya Arctic sürümünün tasarım ve uzman görüşü paketidir. V0.1 tank PoC'siyle aynı dayanım/ölçüm sınıfında olduğu varsayılmaz. Maksimum derinlik, basınç rating, salinity doğruluğu, pil süresi ve malzeme rating'i henüz belirlenmedi. Fiziksel Arctic cihazı/CAD/deniz testi yapılmış değildir [E13/E16/E17](../../docs/EVIDENCE_MAP.md).

| Dosya | Kullanım |
|---|---|
| [ARCTIC_CAD_BRIEF.md](ARCTIC_CAD_BRIEF.md) | Çerçeve, sensör/güç/logger ve yük yolu için CAD görevi |
| [SENSOR_REQUIREMENTS.md](SENSOR_REQUIREMENTS.md) | Uzmanla seçilecek sensör gereksinimleri |
| [MARINE_OPERATION.md](MARINE_OPERATION.md) | İzinli gemi operasyonu ve veri/numune |
| [VALIDATION_REQUIREMENTS.md](VALIDATION_REQUIREMENTS.md) | Referans, soğuk/basınç ve model karşılaştırması |
| [OPEN_ENGINEERING_DECISIONS.md](OPEN_ENGINEERING_DECISIONS.md) | Kilitlenmemiş seçimler ve karar sahipleri |

**Amaç:** Modelin verdiği su kolonu ile aynı zaman/konumdaki fiziksel gözlemi karşılaştırmak; uygun kaynak senaryosunda arıtma/üretim kararına etkisini incelemek. PWN ana projenin saha katmanıdır; karasal yıllık su arzını ölçmez [bilimsel mimari](../../docs/SCIENTIFIC_ARCHITECTURE.md).

| V0.1 | Arctic v1 |
|---|---|
| Kontrollü tank; encoder mesafesi | Deniz; gerçek basınç/derinlik |
| Kuru elektronik, düşük maliyetli EC prensibi | Gemiye uygun mimari, hedef sinyale göre sensör |
| Referans bulunursa tank karşılaştırması | Profesyonel/reference CTD karşılaştırması planı |
| Kolon kontrol/tekrar | Uzmanla saha, numune ve kalibrasyon protokolü |

Sefer bağlamı tamamen deniz üstü, rota değişebilir; profesyonel çağrı öğrenci kabul şartıyla eşitlenmez [TASE_ALIGNMENT.md](../../docs/TASE_ALIGNMENT.md). Danışman, CTD, gemi ekipmanı veya laboratuvar erişimi sağlanmış değildir. [Ana Arctic konsept/BOM planı](../../docs/PWN_ARCTIC_V1_CONCEPT.md).
