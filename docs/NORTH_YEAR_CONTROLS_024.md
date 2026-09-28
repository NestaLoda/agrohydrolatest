# TESLİM 024 — Yıl bazlı Kuzey simülasyonu ve kontrol paneli

23 Eylül 2026. Aynı araştırma projesi ve aynı karar motoru korunur.

## Kullanıcı akışı

- Açılış yılı sistemin mevcut yılıdır (bu teslimde 2026). Kullanıcı mevcut yıldan 2100'e kadar tam bir yıl yazar. Şu an, +10 yıl ve +25 yıl hızlı seçimleri vardır. Yıl değişince iklim girdileri otomatik gelir; üretim sonucu “Simülasyonu çalıştır” ile yenilenir.
- Ana seçimde yakın dönem / tarihsel / 2030–2050–2090 karışıklığı kaldırıldı. ERA5 2015–2025 karşılaştırması ve eski çok yıllık dönemler ayrıntıda korunur. Bunlar canlı 2026 havası olarak sunulmaz.
- Yağış/kar toplama alanı, depo hacmi ve tahsisli tatlı su kaydırıcıdır. Bunlar kaynak senaryosunu değiştirir; nihai su kaynak paylarını kullanıcıya yazdırmaz. Kaynak payları optimizasyondan çıkar. Değişiklik MANUAL OVERRIDE olarak işaretlenir.
- Planlama alanı 1–10.000 m² sayı girişidir; 100 m², 1.000 m² ve 1 ha düğmeleri kalır. Alan değişince alan başına tanımlı toplama/depo kapasitesi de ölçeklenir; mutlak yıllık tatlı su tahsisi sabit kalır.
- Geçersiz/boş yıl ve alan, simülasyonu ve eski sonucun destek planına aktarımını engeller.
- Tarım Güvencesi üst menüde Gelecek/Kuzey'in yanında bağlı dal olarak görünür. Tamamlanan sonuçtan açılan destek akışı seçilmiş yıl, alan ve ürün hasadını korur.
- Başlıklar “Önerilen ürün dağılımı” ve “Üretim yöntemi dağılımı” olarak sadeleştirildi. Ana sayfa boyu büyütülmez; panel ve karar alanı ayrı kayar. Telefon testi yapılmaz.

## Yıl hesabının bilimsel kapsamı

NASA NEX-GDDP-CMIP6 ACCESS-CM2, MPI-ESM1-2-HR ve MRI-ESM2-0 modellerinin SSP245/SSP585 günlük verileri kullanılır. 2061–2080 arşiv boşluğu 480 kaynak dosyasıyla tamamlanır. Ayrı yıllık paket 2026–2100 için 150 yıl/senaryo bağlamı, 450 model-yıl günlük dizi ve 1.800 ham kaynak kaydı içerir. Eski dönem paketleri değiştirilmez.

`target_year`, eski `horizon_id` arayüzüne eklenen isteğe bağlı bir alandır. Yıl verilince ilgili takvim yılının doğrulanmış günlük sıcaklık, yağış ve ışınımı seçilir; aday ön elemesi, aylık su toplama, enerji katsayıları ve günlük su sınaması yeniden hesaplanır. Artık yıllarda takvim gün sayısı korunur. Doğrusal yıl interpolasyonu veya sıcaklıkla doğru orantılı ürün payı üretilmez. Ürün × yöntem × mevsim optimizasyonu aynı motorla çözülür.

Ürün verimi hâlâ kaynaklı kontrollü üretim analoğudur. Yerel Arktik verim ölçümü veya bu projeye verilmiş uzman onayı değildir. Ürün payları değişmeyebilir; su, yöntem veya enerji değişebilir. Bu bilimsel olarak geçerli sonuçtur. Kaynak dosyalarının hash kayıtları ve hesap bağlamı PRE kaydına taşınır.

Seçilen yılın CMIP6 dizisi **o yıl gerçekleşecek hava tahmini değildir**; senaryo altında bir model gerçekleşimidir. Tek yıl, uzun vadeli altyapı dayanıklılığını tek başına kanıtlamaz. Çok yıllık karşılaştırma ayrıntıda korunur. Üç model aralığı güven aralığı değildir. Yıllık su taraması sıfır başlangıç karı ve boş depo kabul eder; önceki yıldan kar devri temsil edilmez. Bu koşul arayüzde açılır açıklamada ve kanıt katmanında belirtilir.

## Model anlatımı ve saha

`docs/MODEL_NASIL_CALISIYOR.md`, jüriye bir dakikalık anlatım ve teknik açıklamayı birleştirir. İklim → adaylar → su/enerji → üretim planı → saha/pilot → destek programı zinciri açıklanır. Matematiksel optimizasyon doğal dil üreten yapay zekâ gibi sunulmaz.

Gerçekte yapılması gerekenler: yerel su tahsisi/depolama, enerji ve zemin kanıtı; izinli PWN sıcaklık–tuzluluk–derinlik gözlemi; karar sorusuna göre uzman/laboratuvarla belirlenen numune analizi; uygun arıtma/koşullandırma sonrası kontrollü üretim pilotu. PWN yıllık karasal tatlı suyu veya gelecek verimi doğrudan ölçmez. Aynı motor yalnız gözlemin desteklediği girdilerle güncellenir.

Ana karşılaştırma seçilen yıl ve iki referansı hesaplar (`/api/north/reference`); beş dönemli ayrıntılı analiz kullanıcı açınca yüklenir. Böylece her yıl seçiminde bütün eski gelecek dönemleri gereksiz yere hesaplanmaz.

## Gerçek hesap örneği

Aynı 100 m², SSP245, varsayılan dengeli amaç ve kaynak koşullarıyla, `annual-comparison.json`:

| Hesaplanan büyüklük | 2037 | 2072 |
|---|---:|---:|
| Yıllık yeni su ihtiyacı | 14,132 m³ | 14,251 m³ |
| Depolanan yağış/kar katkısı | 9,685 m³ | 14,251 m³ |
| Arıtılmış deniz suyu | 4,446 m³ | 0 m³ |
| Isı ihtiyacı | 2.258,9 kWh ısı | 1.546,6 kWh ısı |
| Elektrik eşdeğeri | 119.260,5 kWh | 119.700,0 kWh |

Bu örnekte ürün miktarları aynı kalır. Daha sıcak senaryoda ısıtma azalırken toplam enerji otomatik azalmaz; diğer işletme kalemleri de hesaplanır. İki yıl arasındaki fark tek başına iklim trendi veya gerçek gelecek hasadı değildir.

Doğrulama kayıtları: `docs/verification/north-year-controls/`. Sonuçlar teslim sonunda ANA_CHAT_TESLIM ve BUILD_STATUS'a işlenir.
