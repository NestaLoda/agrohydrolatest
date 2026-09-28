# Rebuild denetimi · 22 Eylül 2026

## İnceleme ve korunmuş varlıklar

Aynı çalışma klasöründe devam edildi. Bu kopyada .git bulunmadı; depo başlatma/reset veya yeni proje oluşturma yapılmadı. Kaynak ağacı ve SHA256 envanteri [before-inventory.json](verification/rebuild/before-inventory.json); üretilmiş bağımlılık klasörleri hariç ağaç [repository-tree.txt](verification/rebuild/repository-tree.txt). Değişim öncesi frontend/backend ve teslim [before-product.zip](verification/rebuild/before-product.zip). Güncel ve tarihsel docs, data, hardware, backend, frontend, scripts ve tests incelendi. Belgeler kod ve gerçek dosyalarla karşılaştırıldı.

Kaynak PDF metinleri yerel pypdf ile, motivasyon formu python-docx ile okundu; kaynak dosyaları değiştirilmedi. Çıkarılan metinler verification/rebuild/source-0..3.txt ve motivation.txt. Bu tur PDF sayfa düzeni/fotoğraf doğrulaması veya yeni dış kaynak araştırması iddia edilmez.

| Varlık | Gerçek durum / korunma |
|---|---|
| Konya özgün rapor | Göreli su baskısı ve etkileşimli ürün payı modeli; yaklaşık %8,7 tarihsel model sonucu |
| Türkiye başlangıcı | 5 il için 21 resmî alan/üretim kaydı, kaynak ve birim dönüşümleri |
| Günlük iklim | 4.380 ERA5, 14.610 EC-Earth, 730 NASA ACCESS-CM2 SSP245/585 2035 nokta satırı; 6 NetCDF |
| Tarım literatürü | 9 ürün kataloğu, 7 kuzey aday araştırması, 20 kaynaklı otomatik analiz parametresi |
| Hesaplar | FAO-56, günlük su hesapları, çok ürün/yöntem/kaynak LP, provenance/hash, PWN importer, PRE/POST |
| PWN | Sentetik profil fixture; gerçek tank/Arktik ölçümü yok. Hazır DFR0300 kitli cihaz dokümanları korunur |

## Önce / şimdi

Önceki U12 analizinde kaynaklı Kuzey iklimi ürün ön taraması üretiyor fakat optimizasyon adaylarını değiştirmiyordu. Yeni north_resolution katmanı aynı günlük kaynağa dayalı olumsuz tarama sonucunu açık tarla seçeneğinin elenmesine taşır; gerçek motor yeniden çalışır. Geçen tarama zemin/verim/yerel uygunluk onayı değildir. Özgün kullanıcı girdisi korunur; etkin girdiler, değişiklik gerekçesi, kanıt sınıfı ve kaynak/motor hash'leri sonuç kaydına eklenir.

Eski büyük editör ve tablo ağırlıklı açılış yerine ScenarioLab + DecisionCanvas kullanılır. Büyük tablolar ve iklim tanıları ikincil açılır alanlarda; veri/grafik, il kıyası ve özgün pilot görünümü korunur. Eski bileşen dosyalarının bulunması ana rota olarak kullanıldıkları anlamına gelmez.

## Amaçların gerçek anlamı

Kapasite/dengeli amaçlar kg talebinden bağımsız tek ürün kaynak potansiyellerine göre çalışır. Dengeli önce uygun ürünlerin ortak potansiyel payını, sonra toplam karşılamayı artırır, sonra su/enerjiyi azaltır. Kaynak öncelikli amaçlarda ortak optimum payın varsayılan %80'i açık tabandır; bunun üzerinde su→enerji veya enerji→su minimize edilir. Bu taban keyfî kg hedefi değildir, görünür planlama tercihidir; 0,01–1 değiştirilebilir. Amaçlar ekonomik/besinsel optimum iddiası taşımaz. Duyarlılık sırasında aynı amaç kuralı korunur; kaynak değişince normalizasyon potansiyeli değişebilir.

## Su yönetimi ve mevsim kapsamı

Motor kaynak kapasitesi, kalite uygunluğu, kaynak/üretim enerjisi, üretim yüzeyi ve ürün dönemini birlikte kullanır. Sezon tarihleri girdiden gelir; sezonlar arası optimum takvim veya dinamik kar erimesi/depo işletmesi çözülmez. Depolanmış su bütçesi yazılması yağıştan kullanılabilir su türetildiğini göstermez. Su güvenliği zinciri ekranda açıktır; tüm fiziksel zincir henüz hesaplanmış değildir.

## Saha ve doğrulama

Mevcut deterministik tarama tatlı su/enerji ±%20 ve sıcaklık 5/18°C uçlarıyla aynı motoru çalıştırır. Bu sıcaklıklar Arktik tahmini değil bağlı arıtma ilişkisinin destek alanıdır. Salinite ve kimyada MODEL_LINK_NEEDED; ekonomik EVSI veya güven yüzdesi yok. PRE/POST desteklenen tek sıcaklık girdisini günceller, eşleşmeyen konum/UTC/derinlik/temperature_kind ve uygunsuz kayıtları engeller. Gerçek ölçüm yolu kayıtlı kaynak ve kalite kontrolü gerektirir. Simüle yol OBSERVED sayılmaz.

Numune paneli, derinliği, sayısı, koruma/taşıma ve laboratuvar henüz kesinleşmedi. Kontrollü pilot ve kaynak suyu deneyi ileri araştırma aşaması; fiziksel doğrulama tamamlanmadı.

## Gerçek açıklar

Tam otomatik, yerel olarak kaynakla çözülmüş Future North üretim önerisi henüz yok. Varsayılan hesap DATA NEEDED verir. Sayısal ekranlar açık mühendislik senaryosunda gerçek LP hesaplarıdır; yerel Arktik önerisi veya gerçek ölçüm değildir. Eksik yerel hidroloji/tahsis/erişim/depo, zemin/permafrost/aktif tabaka, dönemsel verim/sulama ve sera ısı/ışık enerjisi otomatik örneklerle doldurulmadı. Kaynaklı yıllık Arizona hidroponik değerleri kısa Arktik sezona sessizce aktarılmadı.

Bu teslim ana ürün akışı ve motor bağlantısı iş paketidir. Veri eksikken tüm rebuild/bilimsel araştırma hedefleri tamamlandı denmez.
