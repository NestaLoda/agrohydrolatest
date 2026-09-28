# PWN v0.1 — öğretmen ve atölye paketi

**22 Eylül güncel tedarik yönü:** [Tam malzeme listesi](../../docs/PWN_V01_TAM_MALZEME_LISTESI.md) esas alınır: DFR0300 K1 hazır EC kitli entegrasyon. Aşağıdaki eski DIY elektrot/ön devre anlatımı ve `BOM.csv` tarihsel alternatif hazırlığıdır; güncel satın alma listesi değildir. Sıfırdan elektrot ve AC sürücü alınmayacak. Kullanıcı 3D yazıcı erişimini doğruladı; diğer donanım envanteri bilinmiyor. Gerçek kart/SD/encoder uyumu ve fiziksel test henüz tamamlanmadı.

22 Eylül 2026. Uygulamaya geçiş kullanıcı tarafından onaylandı. Bu klasör **donanım iletişim ve yapım hazırlığıdır**; yapılmış cihaz, test edilmiş analog devre veya çalıştırılmış firmware değildir. Fiziksel kurulum okul/öğretmen/öğrenci ekibince yapılacak.

Amaç: kontrollü dikey su kolonunda bağıl iletkenlik, sıcaklık ve encoder mesafesini kaydedip tabaka geçişini göstermek. Nihai Arktik CTD değildir. Proje içindeki rol ve iddia sınırı: [E13/E16](../../docs/EVIDENCE_MAP.md), [onaylı PoC kapsamı](../../docs/PWN_SPEC_V0.1.md).

## Bugün kurulacak üç parça

1. **Kuru kayıt ünitesi:** ESP32/uygun Deneyap, sıcaklık ve encoder bağlantısı, microSD veya yerel bellek, USB/batarya.
2. **Islak başlık:** sabit geometrili iletkenlik elektrotları ve suya uygun sıcaklık probu; ayrı taşıyıcı ip.
3. **Deney düzeneği:** şeffaf kolon, cetvel, sabit çap ölçüm tekeri ve elle iniş.

## Okuma sırası

- [Öğretmen özeti](../../docs/PWN_TEACHER_BRIEF_TR.md): tek başına okunabilir 22 kısa bölüm.
- [BOM.csv](BOM.csv): envanter kontrolü ve yalnız eksik parça alımı; fiyat/stok yok.
- [WIRING.md](WIRING.md): seçilmiş örnek ESP32 kartı için pin planı ve bağlantı sırası.
- [CONDUCTIVITY_CELL.md](CONDUCTIVITY_CELL.md): öğretmenin tamamlayacağı analog ölçüm zinciri; açık sınır.
- [MECHANICAL_BRIEF.md](MECHANICAL_BRIEF.md), [CAD_BRIEF.md](CAD_BRIEF.md): tutucu, yük yolu ve CAD teslimi.
- [TEST_PROCEDURE.md](TEST_PROCEDURE.md): sırayla yapılacak kısa testler.
- [DATA_SCHEMA.md](DATA_SCHEMA.md): uygulamayla ortak CSV/metadata sözleşmesi.
- [FIRMWARE_PLAN.md](FIRMWARE_PLAN.md): ilk firmware durum makinesi ve kayıt şartları.

**Varsayılan kart kararı:** bağlantı örneği ESP32-DevKitC V4 üzerinde ESP32-WROOM-32E modülü içindir. Bu bir mühendislik seçimidir; ekipte bu kart var demiyoruz. Deneyap/ESP32-S3 veya başka kart varsa aynı pin numaraları kullanılmaz. [Espressif kart belgesi](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html).

## İlk günün tamamlanma noktası

Kart modeli ve eldeki parçalar not edildi; sıcaklık ve encoder kuru masada okunabiliyor; kayıt tekrar açılıyor; öğretmen EC ön devresinin hangi yoldan kurulacağını seçti. Bu durumda mekanik iş paralel ilerleyebilir. Analog devre hazır değilken GPIO'dan suya doğrudan gerilim verilmez; EC dosyasındaki sınırlar geçerlidir.

## Durumun doğru adı

`Dokümantasyon hazır` ile `donanımda çalıştı` farklıdır. Gerçek cast alınmadan örnek CSV satırı kendi ölçümümüz diye oluşturulmaz. Tank kayıtları `OUR_NEW_MEASUREMENT_TANK`; açıklayıcı yapay veri `SIMULATION_EXPLANATORY` olarak etiketlenir. Ana hazır olma kaydı [BUILD_STATUS.md](../../docs/BUILD_STATUS.md).
