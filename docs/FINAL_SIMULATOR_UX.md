> U12 düzeltmesi: Türkiye ilk optimizasyonu otomatik çalışır. Kuzeyde önce sistemin kaynaklı bölge analizi görünür; örnek senaryo kapalı mühendislik deneyi altındadır. Tam Kuzey üretim otomasyonu henüz bitmemiştir: [AUTOMATION_GAP](AUTOMATION_GAP.md).

# Son simülatör etkileşimi · v0.5

Yetkili ürün sözleşmesi: [FINAL_PRODUCT_CONTRACT](FINAL_PRODUCT_CONTRACT.md). Bilimsel kaynak gerçekleri korunur.

Tek çalışma alanı: küçük üst bağlam çubuğu, 355 px bağımsız kaydırılan Scenario Lab, sağda desen/karar tuvali. Türkiye ve Kuzey aynı yapıdır; saha araştırması üçüncü bilimsel durum olarak çekmecede açılır.

## Başlangıç ve kontrol

Konya açılınca resmî seçili ürün alanları, kaynaklı üretim ve LP çalıştırılmadan modellenen su hesabı yüklenir. Beş sürgü laptop ekranında görünür. Her normal kontrol doğrudan düzenlenir; AUTO/MANUAL dünyaları ve tek tek Düzenle kilitleri kaldırıldı. Değişen değer MANUEL SENARYO etiketi alır; kaynak baseline korunur. Yüzde/hektar seçimi, su −%10/−%20, yağış/ET0 stresi, randıman ve gelişmiş kısıtlar vardır. Sıcaklık değişimini verim/ET0'a bağlayan doğrulanmış model yokken işlevsiz sıcaklık sürgüsü eklenmedi.

Hesapla sabit altlıktadır. İlk sonuç mevcut desen; çalıştırma sonrası mevcut → önerilen. Üretim, su, boş alan, kısıtlar ve çözücü nedenleri birlikte gösterilir. Senaryoyu kaydet kullanıcı girdisini JSON indirir. Girdi değişmişse eski sonuç uyarısı görünür.

## Kuzey

Araştırılmış ilk adaylar otomatik filtrelenir; yerel uygunluk bilinmeyeni ayrı kalır. Amaçlar: kaynak kapasitesini keşfet, talebi karşıla, dengeli, su öncelikli, enerji öncelikli. Kg hedefleri keşif/dengeli modun ana kontrolü değildir. Bu modlar tek ürünün kaynaklar altında hesaplanan potansiyelini kullanır; hedef/minimum kg'yi kullanmadığını belirtir. Talepli modlar için gelişmiş hedefler erişilebilir.

Bilinmeyen yerel parametrelerle sahte üretim önerisi yok. Açıklayıcı senaryo kullanıcı seçimiyle yüklenir ve seçilen amaç korunur. Sonuç ürün + yöntem + kaynak + dönem/kaynak kullanımını verir; tarla ha ve kontrollü yüzey m² ayrıdır. Tek bir sürdürülebilirlik skoru yok.

## Araştırma çekmecesi

SAHA ARAŞTIRMASI: son hesaplanan koşullarda aynı motorla tek-değişken duyarlılığı. Model etkisi, ölçülebilirlik, araç/numune ve eksik model bağlantısı birlikte görünür. Araştırma paketleri A profil, B fiziksel numune, C karar bilgisi; PRE/POST ve teknik PWN/CSV ikincil sekmelerdir. Sadece desteklenen sıcaklık girdisi bugün otomatik güncellenir. Gerçek fiziksel gözlem henüz yoktur.

## Görsel ve erişim

Orman/petrol yeşili bağlam, sıcak açık tuval, sınırlı su/enerji/saha renkleri. Desen geçişi hareket azaltma tercihine uyar. Üst çubuk yüksekliği değiştiğinde panel yüksekliği ölçülerek ayarlanır; hesapla ekranda kalır. Çekmecelerde Escape ve odak döngüsü; mobilde üst üste panel/sonuç.

## Kabul kanıtı

[Tarayıcı raporu](verification/contract-smoke.json), [başlangıç](verification/contract-konya-baseline.png), [stres](verification/contract-konya-stress.png), [ikinci il](verification/contract-second-region.png), [Kuzey](verification/contract-north-pattern.png), [araştırma](verification/contract-research.png), [PRE/POST](verification/contract-pre-post.png).
