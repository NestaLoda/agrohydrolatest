# Üretimin Sınırı — yerel araştırma arayüzü

React, TypeScript, Vite ve MapLibre ile geliştirilen beş çalışma alanlı karar dashboard'u (v0.2). Varsayılan çalışma alanı kuzey üretim kararıdır; sıralı sunum ekranları yerine aynı girdileri paylaşan kalıcı çalışma alanları vardır. Bilimsel değerler `/api` üzerinden gelir; hizmet kapalıysa sayılar örnek değerlerle doldurulmaz.

## Çalışma alanları

- `#north`: düzenlenebilir üretim/kaynak koşulları, sekiz filtre, seçenekler, bağlayıcı kısıtlar, sabitlenen hesapla karşılaştırma. Alt sekmeler: açık simülasyonla saha eşleştirme etkisi ve kaynaklı yerel iklim bağlamı.
- `#turkiye`: beş benchmark bölge, ortak su bütçesi karşılaştırması, harita, karşılaştırma matrisi ve aylık yağış/ET₀ grafiği.
- `#pwn`: ham CSV, kaynak/derinlik/sıcaklık tanımı, kalite kontrolü, sinyal ve sıcaklık profili, klasik geçiş adayları.
- `#evidence`: `/api/sources` üzerinden kayıtlı tüm veri kaynakları. Aynı kayıt global kanıt çekmecesinde de açılır.
- `#pilot`: orijinal Konya sonucunun kompakt karşılaştırması.

Ziyaret edilmiş çalışma alanları navigasyonda korunur; PWN analizi ve sabitlenen karar kaybolmaz. Haritalar yeniden görünür olduğunda boyutlarını yeniler. Sayfa yenilenmesi bir kalıcı oturum deposu değildir; hesaplar JSON olarak indirilebilir.

## Çalıştırma

Node.js 22.15 veya Vite'ın desteklediği daha yeni bir sürüm gerekir.

```powershell
npm.cmd install
npm.cmd run dev
```

Geliştirme adresi: `http://127.0.0.1:5173`. Vite `/api` isteklerini `http://127.0.0.1:8000` adresine aktarır. Üretim çıktısı `npm.cmd run build` ile `dist/` altında oluşur; backend aynı origin'de bu dosyaları sunmalıdır. `vite preview` yalnız statik çıktıyı önizler, backend ile birleşik dağıtım değildir.

## Veri ve doğruluk etiketleri

- Konya sayıları API'deki tarihsel rapor kaydından gelir; göreli endeks m³ tasarruf değildir.
- Türkiye ekranı gerçek iklim verisiyle transfer gösterimini bağımsız validasyondan ayırır.
- Kuzey senaryo sayıları dış literatür sonucu olarak görünür; SSP değişimi yerel CMIP6 hesabı yapılmış gibi üretim parametrelerine uygulanmaz.
- Üretim ve kaynak suyu kontrolleri açıkça simülasyon/varsayım etiketlidir.
- PWN örnek profili matematiksel bir simülasyondur; açılması isteğe bağlıdır ve fiziksel ölçüm diye kaydedilmez.
- CSV yüklemesi için veri türü açık seçilir. Ham sinyal kalibrasyonsuz EC/tuzluluk olarak gösterilmez.
- Hesap sonrası girdiler değiştirilirse sonuç eski olarak işaretlenir. Karar kaydı girdi ve çıktısıyla indirilebilir.

## Çevrimdışı harita

`public/land.geojson`: Natural Earth `ne_110m_land.geojson`, kamu malı. Kaynak: https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_110m_land.geojson (22 Eylül 2026 tarihinde alınmıştır). Harita MapLibre ile yerel vektörden çizilir; harita tile/glyph servisi, web fontu veya CDN gerekmez. Noktalar API metadata'sından gelir. Harita hesaplanmış frontier veya sefer rotası değildir.

## API sözleşmesi

`src/api.ts` typed taşıma katmanıdır: overview, sources, benchmarks, benchmark-comparison, north-context, decision, field-comparison ve PWN uçları. Bilimsel hesaplar frontend'e kopyalanmaz. PWN simülasyonu backend'in açıkça etiketli örnek CSV'sinden analiz edilir; `/api/pwn/example.csv` bağlantısından indirilebilir.

PWN yüklemesinde kaynak türü, ham sinyal birimi ve derinlik yöntemi kullanıcı tarafından bildirilir. Dış gözlem ayrıca sağlayıcı, kaynak URL ve lisans/izin ister. Doğrulanmamış derinlikler grafikte sıfır olarak gösterilmez. Kablo mesafesi, yalnız dikey tank yöntemi açık seçildiğinde derinlik olarak yorumlanır.

22 Eylül 2026 v0.2 kontrolü: TypeScript ve Vite üretim derlemesi başarılı. Yeni sözleşmeler backend kaynakları ve kuzey veri kaydıyla eşleştirildi. Ana görev tarayıcıdaki etkileşim ve responsive kontrollerini ayrıca kaydeder; v0.1 testleri bu refaktörün yeni test sonucu olarak aktarılmaz.

Kuzey iklimi tek EC_Earth3P_HR modelinin yanlılık düzeltmesi kapalı 1995–2014 / 2030–2049 karşılaştırmasıdır. Üstteki SSP seçimi ayrı Xu yayın bağlamını değiştirir; kara iklim çıktısı deniz kaynak sıcaklığına çevrilmez. Saha eşleştirme paneli görünür `SIMULATION_EXPLANATORY` kullanır; zaman/konum/derinlik uyuşmazlığında karar karşılaştırması yapılmaz. Enerji eşiği örneği 25.110 kWh'dir.

Paket sürümleri npm kayıtlarından kontrol edilip sabitlenmiştir; tekrarlanabilir kurulum için `package-lock.json` korunur. Test/derleme durumu gerçek çalıştırma sonuçlarıyla ana build kaydında tutulmalıdır.
