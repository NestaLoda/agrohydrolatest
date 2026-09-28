# Arctic v1 CAD görevi

**Konsept çizimi; imalat veya basınç onayı değil.** Boyutlar gerçek sensör ve gemi şartlarıyla belirlenecek [E16](../../docs/EVIDENCE_MAP.md).

Çizimde şu parçalar ve ilişkiler ayrı gösterilsin:

1. Üst yük alma/geri alma bağlantısı ve marine taşıyıcı çerçeve; yük sensör konnektöründen geçmez.
2. Akışa açık conductivity/sıcaklık uçları; mekanik koruma onları kapalı su haznesine hapsetmez.
3. Gerçek deniz basıncını gören port/sensör. Kapalı gövde içindeki havayı ölçmek derinlik ölçümü değildir.
4. Logger, saat, batarya ve yerel kayıt için hacimler; erişim ve veri boşaltma akışı.
5. Gövde, contalar, kablo geçişleri ve strain relief; seçilmemiş malzemeye rating yazılmaz.
6. Denge/ağırlık ve halat güzergahı; gemide elde veya izinli sistemle indirme/geri alma.
7. Deck GPS/UTC eşleme ve bilgisayarla çevrimdışı inceleme.
8. Ayrı numune örnekleyicisi; PWN içine otomatik şişe mekanizması varsayılmaz.

**İstenen görünüşler:** tam montaj; patlatılmış yerleşim; yük yolu; sensör akış bölgesi; deck→profil→geri alma→numune operasyon şeması. Seçilmemiş parçalar isim ve gereksinim kutusuyla, gerçek seçilmiş olanlar katalog boyutuyla çizilir. Tasarım etiketi `ENGINEERING CONCEPT` olacak.

Başlangıç BOM grupları: C/T, pressure, logger/clock/memory, batarya, gövde/conta/konnektör, çerçeve/halat/ağırlık, deck arayüzü, numune/etiket/taşıma. Marka, adet, ölçü ve maliyet uzman geri bildirimi/tedarikten sonra. [Ana BOM planı](../../docs/PWN_ARCTIC_V1_CONCEPT.md), [operasyon](MARINE_OPERATION.md).

V0.1'i yalnız kalınlaştırılmış kapsüle çevirmek Arctic v1 doğrulaması değildir. Üretim dosyası gerçek gereksinimler gelmeden yayımlanmaz; mülakat için şematik konsept yeterli dürüst statüdür.
