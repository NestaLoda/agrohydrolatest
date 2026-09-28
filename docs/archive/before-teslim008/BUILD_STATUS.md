# Güncel build durumu · Rebuild / TESLİM 007

22 Eylül 2026. Paket/model sürüm etiketi 0.5.0; bu işin kimliği rebuild ve kaynak kod hash'leridir. Önceki U12/005/006 durumları [arşivde](archive/rebuild-before/BUILD_STATUS.md). Yeni yetkili kapsam [REBUILD_CONTRACT.md](REBUILD_CONTRACT.md); inceleme [REBUILD_EVIDENCE_AUDIT.md](REBUILD_EVIDENCE_AUDIT.md).

## Çalışan ürün ve bu turdaki değişiklikler

- Aynı proje klasöründe veri/bilim korunarak ana simülatör yeniden düzenlendi. .git bulunmadı; yeni depo/reset yok. UI/backend değişim öncesi ZIP ve ağaç/hash envanteri verification/rebuild altında.
- Üstte BUGÜN / TÜRKİYE, GELECEK / KUZEY, SAHA GÜNCELLEMESİ ve minimal bağlam; solda bağımsız Scenario Lab, sağda Decision Canvas. Ölçülen 1367×768 CSS ekranda kontrol genişliği 354 px. Orman/petrol kabuk, sıcak tuval, anlamsal su/üretim/enerji renkleri. Harita veya büyük tablo ana etkileşim değil.
- Türkiye: 5 il kaynağı otomatik yükler ve ilk optimizasyon çalışır. Ürün payı sürgüleri, yüzde/hektar, su −%10/−%20/kuraklık, su bütçesi/randıman, gelişmiş iklim/kısıtlar. Pay artışında toplam alanı aşmamak için gerekirse diğer paylar orantılı azalır. MANUAL OVERRIDE ve eski sonuç uyarısı görünür. Hesap sonrası mevcut/önerilen barları, üretim, su, atanmayan alan ve bağlayıcı kısıtlar birlikte.
- Kuzey: kaynaklı günlük iklim ön taramasının olumsuz sonucu artık **aynı optimizatörün açık tarla adaylarını eler**. Araştırma kataloğu ve yöntem uygunluğu korunur. Özgün/etkin girdiler ayrı; kaynak/motor hash'leri ve SOURCED/MODELED/ASSUMED/UNKNOWN + field_measurable kaydı vardır. Geçen tarama yerel uygunluk/verim onayı değildir.
- Kuzey amaçları: kapasite/dengeli; su ve enerji önceliğinde kg talebinden bağımsız kapasite modu. Önce ortak ulaşılabilir pay, sonra açık %80 üretim tabanı üzerinde kaynak minimizasyonu. %80 değiştirilebilir planlama tercihi, saklı ağırlık değildir. Gerçek talep varsa talep modu korunur. Aynı örnekte su ve enerji önceliği aynı sonucu verdi; farklılık zorlanmadı.
- Üretim çıktısı: ürün kg, ha/m², yöntem, su kaynak payı, ürün sezonu, su/enerji, gerekçe ve kaynak kısıtları. Yerel bilimsel girdiler eksikken varsayılan Kuzey hesabı DATA NEEDED. Açıklayıcı değerler yalnız kapalı hesap deneyi bölümünden açıkça yüklenir.
- Saha A/B/C ve duyarlılık çekmecesi aynı projeye bağlı. PRE kaydı dondurulur; desteklenen sıcaklık ve uygun eşleşme ile aynı motor çalışır. Simülasyon etiketi sonuç kaydındaki kanıt türüne bağlıdır; dropdown değiştirmek sonucu OBSERVED yapmaz. 24 saat uyumsuzluk güncellemeyi engeller; aynı sıcaklıkta değişmeyen desen geçerli sonuçtur.
- Güncel sözleşme, model/kanıt kayıtları, otomasyon açığı, demo ve mülakat anlatımı güncellendi. Fiziksel donanım veya yeni kaynak veri edinimi yapılmadı.

## Korunan gerçek varlıklar

4.380 ERA5; 14.610 EC-Earth; 730 NASA ACCESS-CM2 SSP245/585 2035 günlük satır ve 6 NetCDF; 21 resmî tarım kaydı, 9 ürün kataloğu, 7 Kuzey aday araştırması ve 20 otomatik analiz parametresi. FAO-56, provenance/ham kaynak hash'leri, çok ürün LP, PWN importer, PRE/POST ve eski 144 test korundu.

99 data/hardware dosyası karşılaştırıldı: **98 birebir aynı**. Tek değişen dosya data/metadata/provenance.sqlite; yeni hesapların çalışma kaydı tutuldu. Dosya denetimi [asset-preservation.json](verification/rebuild/asset-preservation.json); SQLite'nın yalnız dosya hash'iyle içerik farkı kanıtlanmaz. Ham dosyalar/kalibrasyon varsayımları gerçek ölçüme çevrilmedi.

## Gerçek hesap / bilimsel sınır

NASA SSP245 2035, açık örnek varsayımlar, dengeli amaç: arpa 5.699,44 kg / yaklaşık 1,90 ha; patates 0 (araştırma sıcaklık elemesi); marul 1.013,23 kg / 337,74 m² hidroponik. Su 3.819,89 m³, enerji yaklaşık 40.000 kWh. Kaynaklar tatlı su 2.000, depolanmış 500 ve arıtılmış deniz suyu yaklaşık 1.319,89 m³. Bunlar **hesaplanmış açıklayıcı senaryo**, kaynakla doğrulanmış yerel Arktik önerisi veya gerçek üretim sonucu değil.

Aynı koşulda kapasite amacı 5.035,98 kg arpa + 1.200 kg marul üretir. Su/enerji önceliği 4.559,55 kg arpa + 810,59 kg marul, 3.055,91 m³ ve 26.802,88 kWh verir. Tam istek/etkin girdi/sonuç ve run_id kayıtları [engine-results.json](verification/rebuild/engine-results.json).

Duyarlılık: bu açık senaryoda tatlı su, enerji ve deniz sıcaklığı uç koşuları deseni etkiliyor. Tatlı su/enerji ±%20 stres; sıcaklık 5–18°C arıtma ilişkisinin destek alanı, Arktik tahmini değil. Salinite/kimya MODEL_LINK_NEEDED; ekonomik/probabilistik bilgi değeri ve otomatik güven artışı hesaplanmaz.

## Son doğrulama

- Tam backend koşusu: **151 test, 0 başarısızlık, 0 hata; 16.924 s; başlangıç 2026-09-22T20:12:18.008593+03:00**. [JUnit](verification/rebuild-tests.xml). Mevcut Starlette/AnyIO deprecation uyarısı; test başarısızlığı yok. Öncesinde 144 testlik başlangıç koşusu ayrıca kayıtlı.
- React/TypeScript/Vite üretim derlemesi geçti; son UI değişiklikleri bu derlemeye dahil. Derleme kaydı verification/rebuild/build.log.
- Tarayıcı: **15 doğrulanmış kontrol; kayıt 2026-09-22T17:23:28.370Z**. Konya −%20, ikinci il otomasyonu, kaynaklı Kuzey DATA NEEDED, dengeli/su/enerji hesapları, duyarlılık, PRE/POST/geçersiz/eşit gözlem, sürgü klavye erişimi, masaüstü kontrol/footer ve 390×844 CSS taşma kontrolü. [QA](verification/rebuild/browser-qa.json). Konsol hatası yok; ağ istek sayısı ölçülmedi. 390 px için görüntü yakalama araç sınırı nedeniyle yalnız DOM taşma kontrolü kaydı vardır.
- Görseller: [nihai Konya](verification/rebuild/konya-water20-final.png), [Kuzey eksik veri](verification/rebuild/north-source-needed.png), [dengeli plan](verification/rebuild/north-balanced.png), [su önceliği](verification/rebuild/north-water-priority.png), [duyarlılık](verification/rebuild/tase-sensitivity.png), [PRE/POST](verification/rebuild/pre-post-matched.png), [uyumsuzluk](verification/rebuild/pre-post-rejected.png), [değişmeme](verification/rebuild/pre-post-no-change.png), [Şanlıurfa](verification/rebuild/sanliurfa-baseline.png). Sonraki küçük kaynak sınırı/ondalık/kanıt etiketi düzeltmeleri nihai Konya derlemesinde; eski ekranlar kendi çekim durumunu gösterir.

## Açık bilimsel bağımlılıklar / tamamlanmayan hedef

Tam otomatik **yerel kaynaklarla çözülmüş Kuzey üretim planı henüz tamamlanmadı**. Yerel mevsimsel su tahsisi/erişim/depo/çevresel ve rakip kullanımlar, toprak/permafrost/aktif tabaka, dönemsel ürün verimi ve sulama, sera ısı/ışık enerjisi eksik. Kaynaklı aday elemesi bu boşluğu kapatmaz. Sezon girdileri gösterilir; optimum sezon/depo işletmesi çözülmez. Arıtma kimyası/salinite modeli, gerçek eşlenmiş deniz model profili, CTD/PWN kalibrasyonu ve fiziksel ölçüm yok.

Numune sayısı/derinlikleri/paneli uzman, gemi, izin ve laboratuvar olmadan sabitlenmez. δ18O/δ2H ve arıtma açısından anlamlı sınırlı kimya adaydır. Sefer sonrası gerçek numune veya açıkça sentetik kaynak suyu → arıtma → kontrollü büyüme pilotu plan düzeyinde; tüm Arktik tarımını doğrulamaz.

Sonraki somut bilimsel iş: seçili yer/zaman için kullanılabilir su ve üretim/enerji katsayılarını kaynak ve ölçek bilgisiyle resolver'a bağlamak; bulunan verinin hangisi kaynak, hangisi transfer varsayımı olduğunu korumak. Cihaz işi bağımsız bilimsel proje değildir: mevcut DFR0300 K1 / ESP32 / DS18B20 / encoder / SD yolunun tedarik ve fiziksel kalibrasyon aşaması aynı araştırmayı besler.
