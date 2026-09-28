# TESLİM 025 — Küçük haritadan bölge seçimi

23 Eylül 2026. Bu değişiklik yalnız coğrafya seçiminin arayüzünü düzenler; Türkiye desen hesabı ve Kuzey iklim/üretim motoru değiştirilmedi.

Üst bağlam çubuğundaki uzun bölge açılır listesi, dünya simgeli kısa bir düğmeye taşındı. Harita yalnız düğmeye basılınca açılır; ana simülasyon alanını büyütmez. Açılır haritadaki **Dünya / Bölge** düğmeleri gerçek MapLibre küre görünümü ile yakın bölge haritası arasında geçiş yapar. Türkiye görünümünde Konya, Seyhan/Adana, Gediz/Manisa, GAP/Harran–Şanlıurfa ve Trakya/Edirne noktaları, `data/sites.json` koordinatlarından gelir. Harita işaretine veya altındaki kısa bölge adına basınca uygulamanın mevcut `selectRegion` akışı çalışır. Dolayısıyla seçilen bölgenin gerçek mevcut deseni, iklim bağlamı ve simülasyonu açılır. Harita yalnız temsil noktalarını gösterir; havza veya idari sınır çizmez.

Kuzey görünümünde Longyearbyen araştırma noktası (78,22°K; 15,65°D) ve NASA kaynak iklim hücresinin merkezi (78,125°K; 15,625°D) ayrı işaretlenir. Yaklaşık 0,25° hücre ayak izi, bu veri katmanının coğrafi kapsamını anlatır. Taranan işaret tarım yapılabilir alan, fiziksel su kaynağı, PWN ölçümü veya TASE rotası olarak yorumlanmaz. Kuzey optimizerı yalnız bu mevcut Longyearbyen bağlamını destekler; haritada veri üretilemeyen başka bir konumu seçilebilir göstermedik.

Harita, projedeki mevcut çevrimdışı Natural Earth `land.geojson` temelini ve MapLibre bileşenini kullanır. Yeni harita/iklim verisi indirilmedi. Görseli olmayan ortamda Türkiye noktaları metin düğmeleriyle seçilebilir. Pencere dışına tıklama ve Escape kapatır; işaretler klavyeden erişilebilir düğmelerdir.

Doğrulama: TypeScript/Vite üretim derlemesi geçti. Masaüstü 1280×720 tarayıcı sınamasında beş Türkiye noktası görünür; Gediz harita işaretine basılması Gediz/Manisa planlama bağlamını, GAP adı ise Harran/Şanlıurfa bağlamını açtı. Kuzey işareti ve veri hücresi görüldü. Dünya görünümü her iki modda açıldı, bölge görünümüne geri dönüldü; Seyhan harita işareti Adana planlama bağlamını açtı. Yatay taşma ve tarayıcı konsol hatası yok. Mobil test yapılmadı. Kanıt: `docs/verification/region-globe-025/` (Türkiye/Kuzey bölge ve dünya görselleri, `browser-qa.json`, derleme kaydı).

Önceki backend 574 testinin son çalışması TESLİM 024'te, 23 Eylül 2026 16:11:33 +03 tarihindedir. Bu arayüz değişikliğinde backend ve veri değişmediğinden testler yeniden çalıştırılmadı.
