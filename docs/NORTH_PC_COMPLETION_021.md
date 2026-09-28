# Bilgisayar tarafındaki beş geliştirme

23 Eylül 2026 · TESLİM021. Bu dosya uygulanmış yazılımı, kaynaklı veriyi, koşullu hesabı ve henüz yapılmamış fiziksel işleri ayırır.

## 1. Yakın dönem ve gelecek

2015–2025 için 4.018 eksiksiz ERA5 günlük Tmin/Tmax/yağış/kısa dalga radyasyonu kaydı edinildi. Open-Meteo üzerinden kaynak URL, UTC, ham dosya ve SHA-256 arşivlendi; 1995–2025'in 11.323 günü aynı sağlayıcıyla tarihsel kontrol için tutuldu. ERA5 yeniden analizdir; kendi istasyonumuz veya gerçek ekiliş değildir. On bir yıllık yakın dönem, 30 yıllık iklim normali diye adlandırılmaz.

Aynı ürün–yöntem–sezon motorunda yeni `recent` dönemi çalışır. Ana kıyas yakın dönem → seçilen gelecektir. Tarihsel NASA 1995–2014 seçeneği aynı model ailesinde kıyas için korunur. Alan, amaç, üretim analoğu ve altyapı eşit tutulur.

Kritik sınır: NASA ve ERA5 aynı tarihsel dönemde bile farklıdır. NASA tarihsel hücresi ERA5'e göre yaklaşık 1,65°C daha soğuk ve yıllık kısa dalga radyasyonu yaklaşık 1.274 MJ/m² daha yüksektir. Yakın ERA5 → gelecek NASA farkı yalnız ısınmaya atfedilemez; veri ailesi/hücre etkisini de taşır. Arayüz bunu söyler. Otomatik, doğrulanmamış bir bias düzeltmesi uygulanmadı. Bu ayrım seferin iklim projeksiyonunu bütünüyle doğrulayabileceği anlamına gelmez.

Kaynak: [Open-Meteo tarihsel hava API](https://open-meteo.com/en/docs/historical-weather-api). Tam kayıt `data/north/rebuild_climate/recent_reference/README.md` ve manifesttedir.

## 2. Ürün seçiminin açık amacı

Kullanıcı artık taze ürün miktarı, bitkisel protein veya besin enerjisi hedefi seçebilir. Altı ürünün ham yenebilir besin bileşimi Norveç Matvaretabellen resmî API'sinden kaynak kimlikleriyle arşivlendi. Bir kg yenebilir ürün için 100 g katsayısı onla çarpılır; protein gramı/kg dönüşümü ayrı açıktır. Yenebilir kısım ikinci kez düşülmez.

Aynı LP önce seçilen çıktının en yüksek değerini bulur; %95'ini koruyarak su–enerji uçları arasındaki en büyük normalize kaybı azaltır. Varsayılan her etkin ürüne %5 alan politikası korunur ve ayarlanabilir. Gizli besin ağırlıkları, keyfî fiyat/talep veya önceden verilen ürün miktarları yoktur. Kaynak önceliği modları seçilen amaçla bulunan dengeli planın ürün miktarlarını korur.

Gerçek varsayılan 2050/SSP245/100 m² hesabında taze ürün hedefi alabaşa %75 alan, protein ve besin enerjisi hedefleri rokaya %75 alan verir; diğer beş ürün %5'er tabandadır. Bu, hedefin kararı gerçekten değiştirdiğini gösterir; bir ürünün evrensel üstünlüğünü kanıtlamaz. Ham protein, sindirilebilir protein değildir; besin enerjisi kcal, tesis elektriği kWh değildir. Bu bir dengeli diyet, yerel pazar talebi veya kâr optimizasyonu değildir. Ekonomi için yerel güvenilir fiyat/işletme maliyeti/talep hâlâ gerekir.

Kaynak: [Matvaretabellen API](https://www.matvaretabellen.no/en/api/). `data/north/food_composition.json`, ham API ve üretim betiği yeniden üretilebilir kayıt olarak tutulur. Besin dosyası ve yeni motor modülü PRE sürüm hash'ine dahil edildi; eski PRE yeni motorla sessizce çalıştırılmaz.

## 3. Günlük su, depo ve yedek hesabı

Mevcut yağış/kar erimesi–çatı toplama hesabının gerçek günlük sırası kullanılır. Hesaplanmış ürün/yöntem planı sabitken, sınanan kaydın döngüsel işletiminde yağış/kar ile talebi karşılayacak en küçük depo sequent-peak kümülatif açık hesabıyla bulunur. Dönem sonu/başı birlikte işlenir. Toplam toplama talebi karşılamıyorsa sonuç `None`: hiçbir sonlu depo su yaratmaz.

Bu depo hesabı ilk doldurmayı dışlar; ilk dönem boş depo sonucu eski günlük güvenlik analizinde ayrıca kalır. Belediye suyunun yıllık toplamı keyfî günlere dağıtılmaz. Mevcut depo için %100, %75 ve %50 toplama stresleri; ortalama/en yüksek yıllık yedek, yoğun gün ve aralıksız yedek gün sayısı hesaplanır. Yüzdeler gerçekleşme olasılığı değildir. Arıtma debisi veya yerel su tahsisi doğrulanmış sayılmaz.

Varsayılan 2050 taze ürün planında seçilen depo 10 m³, üç kaydın tamamı için hesaplanan döngüsel depo yaklaşık 10,865 m³; seçilen depoyla en yoğun gündeki yedek 46,6 L/gündür. Sonuç değişen üretim hedefi/koşulla tekrar hesaplanır. Çatı, kar birikimi, don, toplama verimi, kalite kayıpları ve parsel erişimi yerel ölçüm/uzmanlık gerektirir. Bu sonuç bir tesis uygulama projesi veya garanti değildir.

## 4. Enerji tüketimi ve güç

Üretim elektriği artık ışık, pompa, fan, nem alma ve soğutma olarak aynı fiziksel hesaptan ayrılır. Isı/COP ve arıtma elektriğiyle toplam kapanışı denetlenir. Varsayılan plan: ışık 70.232; pompa157; fan1.602; nem alma22.303; soğutma23.179; ısı elektrik karşılığı1.896; arıtma0,375 kWh/yıl. Yuvarlanmamış toplam119.368,894 kWh/yıl.

Aylık işletim grafiği ve en yoğun ay eklenmiştir. Günlük hava verisinden yeniden kurulan saatlik ısı/elektrik azamileri hesaplanır; seçili seçeneklerin ayrı azamileri toplanarak ihtiyatlı işletim güç taraması verilir. Varsayılan yaklaşık25,8 kW. Bu gerçek eşzamanlı pik ölçümü değildir. Arıtma çalışma debisi/saatleri, başlangıç akımı, yedekleme, boş tesis don koruması ve bağlantı koşulları ayrıca tasarlanmalıdır. Aylık grafik RO ön ısıtmasının dağılımını içermez; yıllık toplam içerir.

Yıllık enerji sınırı LP'de sert kısıttır. Yeni beyan edilen elektrik gücü alanı ayrıca tarama yapar; gücü aşabilecek tasarım için uyarı üretir, henüz LP güç kısıtı değildir. Yerel sağlayıcı kapasitesi otomatik keşfedilmiş veya onaylanmış sayılmaz.

## 5. Numune ve kontrollü pilot

`Saha + üretim testi → Ölçüm kayıtları` alanında karar bağlantılı saha listesi ve boş CSV/JSON şemaları indirilebilir. Numune girişi kaynak türü, zaman/konum, izin/teslim zinciri, kalibrasyon, yöntem, ölçüm belirsizliği ve uzman tarafından kaynaklı kullanım sınırlarını içerir. Birim uyuşmazlığı, eksik ölçüm ve sınırı kesen belirsizlik ayrı sonuç verir. Kontrolleri geçmek tüm tarımsal uygunluk/içilebilirlik onayı değildir.

Pilot beklentisi ölçümden önce değişmez hash'li kayıtla dondurulur. Gerçek gözlem aynı alan/süre/protokol/su kaynağı/arıtma kapsamıyla karşılaştırılır. Yeni su, elektrik, ayrı ısı ve taze hasat farkları ve kg başına yoğunluklar hesaplanır. Eksik/gelecekte/sentetik gözlem reddedilir. Yeniden oluşturulmuş kaynak suyu gerçek fiziksel pilotta kullanılabilir; Arktik'ten alınmış su diye sunulmaz. Kalite kabulü gönderenin belge beyanıdır; yazılım bağımsız laboratuvar değildir.

Numune/pilot incelemesi otomatik katsayı değiştirmez. Mevcut PWN PRE/POST yolu yalnız eşleşmiş kaynak T/S ve desteklenen arıtma girdilerini aynı motorda günceller. Gelecek iklim, karasal su, zemin ve verim buradan değişmez. Numune paneli, adet/derinlik/hacim ve kontrol/tekrar sayısı uzmanlarca belirlenir.

## Sunumda söyleyeceğimiz

“Bilgisayarda geleceğin iklim ve kaynak koşullarını simüle ederek hangi üretim sistemini ve su stratejisini kurmamız gerektiğini hesaplıyoruz. Sonra bu kararı etkileyen belirsizlikleri belirliyoruz. Seferin gerçek zaman ve konumundaki suyu modelin ne kadar doğru temsil ettiğini ve o kaynak suyunun kullanım/arıtma özelliklerini sınamak için sahada ölçüm yapıp izinli numune almamız gerekiyor. Bu kanıtları destekledikleri girdilere işleyip aynı motoru tekrar çalıştıracağız. Desenin değişmemesi de geçerli bir sonuçtur.”

Yerel zemin, bütün yıl karasal su ve enerji tahsisi ayrıca araştırılacaktır; deniz profili bunların yerine geçmez. Longyearbyen bir araştırma/hesap bağlamıdır, teyit edilmiş sefer istasyonu değildir. Sefer rotası ve gözlemin üretim senaryosundaki kaynakla bağı belgelenmeden doğrudan aktarım yapılmaz. Pilotun kendisi sefer sonrası başka uygun kontrollü ortamda yapılabilir; bütün gelecek tarımı seferde yetiştirme vaadi yoktur.

## Sahada / fiziksel çalışmada kalanlar

1. Gerçek sefer istasyonu/rota/izin ve numune laboratuvar protokolünü kesinleştirmek.
2. Uygun aralıkta kalibre C/T/p cihazıyla UTC/konum/QC içeren gerçek profil; bağımsız referansla kontrol. Mevcut düşük aralıklı TDS PoC deniz CTD'si değildir.
3. Kaynağı ayrı kayıtlı izinli su örneklerini analiz etmek; tuzluluk ve karar sorusuyla gerekçeli kimya. Deniz örneği kar/yağış suyunu temsil etmez.
4. Ayrı yerel çalışma ile toplama/depo/erişim/tahsis, zemin ve enerji kapasitesini doğrulamak.
5. Arıtılmış/koşullandırılmış örnek veya açıkça yeniden oluşturulmuş suyla kontrollü üretim pilotu; gerçek su, enerji, bitki ve arıza kayıtları.

Yazılım hazırlığı bu fiziksel işleri yapılmış saymaz. Test ve API kayıtları `docs/verification/north-completion/`, ayrıntılı saha protokolü `docs/NORTH_VALIDATION_WORKFLOW.md` içindedir.
