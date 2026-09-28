# Jüri modu · rehberli canlı önizleme

25 Eylül 2026 güncellemesi. Mevcut uygulamanın üstündeki **JÜRİ MODU** düğmesiyle açılır. Ayrı site veya ayrı karar motoru değildir. Akışın otomatik bekleme süreleri toplamı **99 saniyedir**; ilk API hazırlığı cihaz hızına göre buna eklenebilir. `Başlat`, `Önceki`, `Sonraki`, `Otomatik oynat / durdur`, `Jüri modundan çık` ve ←/→/Escape çalışır.

| Adım | Süre | Gerçek uygulama işlemi | Görsel kanıt |
|---|---:|---|---|
| 1 · Konya ilk pilot | 9 sn | Konya'nın kaynaklı mevcut ürünü ve başlangıç senaryosu yüklenir; öneri hesaplanmış gibi gösterilmez. | [01](verification/jury-demo-029/01-konya-baseline.png) |
| 2 · Su koşulu değişiyor | 12 sn | Mevcut `water20` hazır senaryosu, `POST /api/simulate`; mevcut→önerilen desen, model su gereği ve kısıt. | [02](verification/jury-demo-029/02-konya-water20.png) |
| 3 · Türkiye aktarımı | 11 sn | Gediz/Manisa kaynaklı varsayılan senaryosu, aynı Türkiye optimizerı. | [03](verification/jury-demo-029/03-gediz-transfer.png) |
| 4 · 2026 model yılı→gelecek | 13 sn | Kuzey 2026 model referansı ve seçilen 2051 yılı, aynı SSP/planlama ayarlarıyla `POST /api/north/reference`; iklim ve karar farkları API'den. | [04](verification/jury-demo-029/04-future-change.png) |
| 5 · Geleceğin üretim/su planı | 19 sn | Longyearbyen 2051, SSP245, 100 m² planlama birimi, dengeli amaç; `POST /api/north/plan`. Ürün, yöntem, su, enerji ve kritik ay gerçek plan sonucundan. | [05](verification/jury-demo-029/05-north-decision.png) |
| 6 · Saha girdileri | 14 sn | Aynı Kuzey planı üzerinde PWN, izinli numune, karasal su/zemin/enerji araştırması ve PRE→TASE→POST. Gözlem üretilmez. | [06](verification/jury-demo-029/06-field.png) |
| 7 · Kontrollü üretim | 11 sn | Mevcut plan üzerinde hazırlanan deneyin yeni su, elektrik, ayrı ısı ve hasat ölçümünü küçük devam kartı olarak açıklar. Pilot sonucu uydurulmaz. | [07](verification/jury-demo-029/07-controlled-pilot.png) |
| 8 · Tek araştırma hattı | 10 sn | Konya→Türkiye→Kuzey→TASE→pilot ve “Modelle → ölç → yeniden hesapla → doğrula.” | [08](verification/jury-demo-029/08-continuity.png) |

Tüm demo parametreleri [juryDemoPreset.ts](../frontend/src/juryDemoPreset.ts) içinde: Konya `konya`; su kısıntısı `water20`; ikinci bölge `gediz_manisa`; Kuzey `longyearbyen`, `ssp245`, `balanced`, `fresh_mass`, 100 m². Seçili yıl 2051; hızlı yıl düğmeleri 2026, 2036, 2051, 2076. Yıl düğmeleri mevcut Kuzey API hesabını yeniden çalıştırır. Paylar veya yöntem değişmiyorsa arayüz bunu olduğu gibi gösterir. 2026 gözlenmiş bugünkü hava değil, üç modelin koşullu model yılıdır. 100 m² gerçek tesis hakkı değil, normalize planlama birimidir.

**Sunumda sözlü söyle:** Türkiye'de su yüzdeleri hesaplanan senaryonun su gereğidir, ölçülmüş tasarruf ya da kâr değildir. PWN v0.1 kayıt/analiz yazılımı var; depodaki örnek sentetiktir ve fiziksel tank deneyi doğrulanmış kayıt yoktur. Arktik sürümü, laboratuvar paneli, numune derinliği ve izinler uzman/sefer görüşü gerektirir. PWN karasal tatlı suyu veya gelecekteki hasadı doğrudan ölçmez. PRE sonucu dondurulup desteklenen saha girdileri geldikten sonra aynı Kuzey motoru yeniden koşulacak; kararın değişmemesi de geçerli sonuçtur. Kontrollü üretim pilotu henüz Arktik tarımı doğrulamış değildir.

Demo API başarısızlığında kısa hata ve yeniden dene görünür, sonraki adıma geçilmez; çıkış her an mümkündür. Normal uygulama demo sırasında çalışır halde saklanır; önceki mod, bölge, yıl, amaç, elle ayar ve hesap sonucu kapanışta korunur. Demo `freeze`, `observe` veya saha güncelleme API'lerini çağırmaz. Tarayıcı testi ve çevrimdışı çağrı kaydı: [browser-qa.json](verification/jury-demo-029/browser-qa.json).
