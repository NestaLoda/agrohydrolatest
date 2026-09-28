# TESLİM 023 — Tarım Güvencesi simülasyon sonucuna bağlandı

23 Eylül 2026. Kullanıcının son isteği: gençlere hidroponik/yeni tarımı tanıtmak; ekipman, dönemlik teknik destek, üreticiden ürün alımı ve dağıtım fikrini karar desteğinde göstermek. Kredi/banka hizmeti ve fide geliştirme kapsam dışı. Sağlık sigortası benzetmesindeki sürekli ilişki ve dönemlik hizmet fikri, gerçek poliçe/gelir garantisiyle karıştırılmadan korunuyor.

**Uygulanan:** Üst çubuk adı Tarım Güvencesi oldu. Kuzey'in tamamlanmış üretim sonucuna kısa öneri eklendi. Yıl, planlama alanı, hidroponik/sera payları ve seçilen ürünün yıllık model hasadı aynı sonuçtan gelir. Ayarlar değiştiğinde veya hesap sürerken eski öneriden destek açma kapatılır; tamamlanan yeni sonuçla tekrar açılır. Üretim kurulamıyorsa Kuzey öneri çağrısı da üretilmez.

Yeni Destek planım bölümünde katılım amacı ve eğitim, kurulum, teknik takip, alım/dağıtım, risk kapsamı seçilir. Bu taslak indirilebilir; gerçek üyelik/ödeme/sözleşme oluşturmaz. On iki ay hesap karşılaştırma dönemidir. Seçilen hizmetlerin fiyat etkisi uydurulmaz; bedel ve indirim ayrı girilir.

Kullanıcı önerilmiş ürünü seçince yalnız o ürünün model hasadı destek hesabına aktarılır; karışık ürünlere tek fiyat gizlice uygulanmaz. Fiyat/giderler boş kalır. Sonuç ihracında orijinal model bağlamı/isteği/provenansı, bağlı ürün, seçilen hizmetler ve miktarın elle değiştirilip değiştirilmediği korunur. Miktar 6 ondalıkla aktarılır; 1e-6 toleransında değişim kontrol edilir. Kullanıcı miktarı değiştirince görünür açıklama çıkar. Öğretici örnek yükleme veya temizleme bağlı ürün ve hizmet seçimini hesap kaydından kaldırır.

Türkiye'de çağrı ancak hesaplanmış optimized sonuçtan sonra görünür. Mevcut bölgesel desen hesabından hidroponik uygunluk sonucu çıkarılmaz; genel pilot/üretici desteği açılır. Bilimsel iklim/su/ürün optimizerı değişmedi; program desteği verimi veya iklimi otomatik artırmaz. Yeni bir benimsenme artışı yüzdesi hesaplanmadı; bunun için gerçek katılım/pilot/işletme verisi gerekir.

**Dosyalar:** yeni frontend/src/components/ProducerRecommendation.tsx, ProducerPlan.tsx; değişen ProducerSupport.tsx, producer-support.css, App.tsx, workspaces/NorthConsole.tsx, NorthSimulation.tsx, Simulation.tsx. Yeni docs/TARIM_GUVENCESI_JURI_ANLATIMI.md; mevcut Ferit metni ve program mantığına güncel ek. Backend ve kaynak veri bu tur değişmedi.

**Bu tur doğrulama:** TypeScript/Vite üretim derlemesi başarılı (70 modül). Masaüstü 1280×720: 2050 önerisi → Marul → 47,6 kg/yıl model aktarımı; diğer mali alanlar boş. Açık test varsayımlarıyla hesap 400 TL desteksiz / 360 TL destekli yıllık denge verdi; program bedelinin indirim faydasını aşması gizlenmedi. 2050→2030 seçiminde eski plan çağrısı devre dışı kaldı; yeni hesapla 2030 bağlamı açıldı. Türkiye'de hesap öncesi çağrı yok, hesap sonrası genel destek çağrısı var. Yeni mobil testi yapılmadı. Kanıt: docs/verification/producer-integration/.

**Önceki test:** 548 backend testi 23 Eylül 2026 14:50:39 +03 başlangıçlı TESLİM022 çalıştırmasında geçmişti. Backend değişmediği için bu tur yeniden çalıştırılmadı; yeni test sonucu gibi sunulmaz.

**Jüri cümlesi:** “Gelecekte ne üretilebileceğini hesaplıyoruz; Tarım Güvencesi ile bu önerinin eğitim, ekipman, teknik destek ve alıcı bağlantısıyla uygulanabilmesini planlıyoruz. Model varsayımlarını saha ve pilotla, ekonomik uygulanabilirliği gerçek teklif ve işletme kayıtlarıyla sınayacağız.”

**Dışarıda kalan gerçek işler:** izinli PWN/numune ve laboratuvar, yerel su/enerji/zemin koşulları, kontrollü tarım pilotu, eğitim uygulaması, yazılı ekipman/servis teklifleri, alıcı kalite/fiyat/ödeme koşulları ve yetkili sigorta tarafıyla kapsam. Kredi/banka ürünü kurulmayacak. Sonraki somut adım bu kanıtları gerçek pilot protokolü ve Ferit'in görüşme/teklif çalışmasıyla toplamak.
