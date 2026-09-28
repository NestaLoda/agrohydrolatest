# Çalışan ilk modelin yöntem ve sınırları

22 Eylül 2026 · model 0.2.0. Bu belge uygulamada gerçekten çalışan hesapları açıklar. Uzun vadeli mimari için SCIENTIFIC_ARCHITECTURE; güncel çıktı durumu için BUILD_STATUS. Beş Türkiye noktası ve bölgesel kuzey modeli U7 ile eklendi; ilk sürümün fiziksel hesap çekirdeği korunur.

## Kaynak → hesap → karar

**Geçmiş:** Orijinal rapordaki 15.702.550 → 14.338.276 göreli endeks, yaklaşık %8,688 azalıştır [F2 s.17]. Uygulama bunu m³ olarak göstermez.

**Türkiye transferi:** Open-Meteo üzerinden açıkça ERA5 seçilerek Konya, Seyhan–Adana, Gediz–Manisa, GAP–Harran ve Trakya–Edirne için 2022–2023 günlük Tmin/Tmax/yağış/ET0 alındı. Bunlar nokta grid serileri; havza ortalaması veya gözlem istasyonu değildir. Kaynak URL, gerçek grid koordinatı, birim, tarih, lisans, SHA256 ham kayıtta korunur. [Veri erişim günlüğü](DATA_ACCESS_LOG.md); [Open-Meteo belgesi](https://open-meteo.com/en/docs/historical-weather-api).

**Su hesabı:** 1 Kasım 2022'den başlayan 240 günlük Akdeniz kış buğdayı örnek takvimi: 30/140/40/30 gün; Kc başlangıç 0,4 ve 0,7 duyarlılığı, orta 1,15, son 0,25. Kc değerleri [FAO56 Tablo 11–12](https://www.fao.org/4/X0490E/x0490e0b.htm) kaynaklıdır; yerel fenolojiyle kalibre edilmedi. Eski göreli ürün ağırlıkları kullanılmaz.

Her gün `ETc_pot = ET0 × Kc`; `taşma=max(0,S+P−kapasite)`; `ET_gerçek=min(min(kapasite,S+P),ETc_pot)`; `S_yeni=min(kapasite,S+P)−ET_gerçek`; `açık=ETc_pot−ET_gerçek`. Kapasite 60 mm, ilk depo 30 mm açık varsayımlardır. 1 mm × 1 ha = 10 m³. Bu, sulamasız tek depolu karşılaştırma; irrigasyon programı veya yıllık güvenilir su arzı modeli değildir. Toplam yağış karın su eşdeğerini içerir ve bu sürümde aynı gün depoya girer; kar birikimi/erimesi ayrıca yoktur. Kuzey için bu bucket su arzı hesaplanmaz.

**İklim göstergeleri:** GDD5 = Σmax((Tmin+Tmax)/2−5,0). Don olmayan pencere, Tmin>0 günlerinin en uzun ardışık dizisi. 60 günlük pencere marul için ihtiyatlı tasarım taramasıdır; zorunlu biyolojik eşik değildir. [FAO Ecocrop](https://ecocrop.apps.fao.org/ecocrop/srv/en/cropView?id=1313) baş marul için 60–85 gün ve yetişkinde −1°C öldürücü sıcaklık bildirir. GDD5 burada betimleyici göstergedir; verim modeli değildir.

**Gelecek:** [Xu vd. 2026](https://www.nature.com/articles/s43247-026-03702-w) 2071–2100 yedi ürün ortalaması için SSP1-2.6/SSP5-8.5 altında 331/739 km kuzeye iklim uygunluğu sınır kayması bildirir. `EXTERNAL LITERATURE RESULT`; kendi CMIP6 hesabımız veya Longyearbyen tahmini değildir. SSP seçimi yerel optimumu yapay biçimde değiştirmez. Longyearbyen seçimi kıyısal kontrollü üretim sorusunu anlatır; bu noktada tarımın gelecekte uygun olduğunu ilan etmez.

## Üretim deseni

İlk ürün **marul**; yöntemler açık tarla ve hidroponik; kaynaklar tatlı su ve arıtılmış deniz suyu. [Barbosa vd. 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4483736/) Arizona karşılaştırmasından açık tarla 250 L/kg ve 1.100 kJ/kg; hidroponik 20 L/kg ve 90.000 kJ/kg merkez değerleri aktarılır. 90.000 kJ/kg = 25 kWh/kg. Bunlar aynı üründe yöntem farkını göstermek içindir. Makaledeki belirsizlikler kaynak JSON'da tutulur; optimizer bu ilk sürümde merkez değerleri kullanır. Arktik ısıtma/ışık sisteminin doğru enerji hesabı oldukları varsayılmaz; bu transfer açık model sınırlamasıdır.

Karar `x_yöntem,kaynak ≥0` üretim kg'sıdır. Toplam kg hedefe eşit; tatlı su, arıtılmış ürün suyu, toplam enerji ve üretim kapasitesi üst sınırları kullanıcı senaryosudur. Enerji en aza indirilir. Ayrıca tatlı suyu en aza indiren ikinci uç çözüm gösterilir; bu iki nokta tam Pareto eğrisi değildir. Alan, besin eşdeğeri, ekonomik maliyet veya çok dönemli depolama ilk çözüme dahil değil. Açık tarlada iklim/zemin bilinmiyorsa seçenek optimizasyona alınmaz. Sınır kartları koşullu seçeneklerdir; bir coğrafi sürdürülebilirlik haritası henüz üretilmedi.

**Arıtma:** [2025 RO sıcaklık deneyi](https://doi.org/10.1016/j.dwt.2025.101157) tek sistemde 5°C'de 10,5; 18°C'de 6,7 kWh/m³ bildirir. İlk duyarlılık modeli yalnız bu iki uç arasında doğrusal interpolasyon yapar; ±%15 varsayımsal pay kullanır. Bu pay istatistiksel güven aralığı değildir. Optimizer üst enerji ucunu kullanır. 5°C altı/18°C üstü için `insufficient_data`; sahte Arctic extrapolasyonu yok. Tuzluluk kaydedilir, fakat kaynakla kalibre edilmiş fonksiyon bulunmadığı için enerji hesabına sokulmaz. Geri kazanım varsayımı `deniz besleme hacmi = ürün suyu / recovery` hesabında kullanılır; SEC-recovery bağlantısı henüz kalibre değil. Ürün suyunun hedef kaliteyi karşılaması bir senaryo koşuludur; kimya paneli henüz kilitlenmedi.

PWN deniz gözleminin bu noktadaki hedefi kaynak suyu durumunu sınamaktır; ham tank verisi deniz suyu veya sulama arzı diye kullanılamaz. Mevcut duyarlılık ekranı ayrı açıklayıcı deniz senaryosudur. Gözlemle kalibre edilmiş bir model iddiası taşımaz.

## PWN ve AI

Kaynak türü + birim + derinlik yöntemi olmadan profil anlamlandırılmaz. Ham iletkenlik sinyali EC/tuzluluk değildir. Dikey tank mesafesinde yüzey sıfırı/prob ofseti önceden düzeltilmiş olmalıdır; gemide kablo uzunluğu derinlik sayılamaz. Gerçek deniz basıncı ve enlem sağlanırsa [TEOS-10 GSW z_from_p](https://teos-10.org/pubs/gsw/html/gsw_z_from_p.html) kullanılabilir; v0.1 bu basınç sensörüne sahipmiş gibi sunulmaz.

Klasik analiz: 3 nokta median; derinliğe göre gradient; eşik `max(median(|g|)+6×1,4826×MAD, 0,25×max(|g|), 1e−9)`. Bu parametreler mühendislik başlangıcıdır, öğrenilmiş eşikler değildir. Kalite OK olmayan satırlar analize girmez. Aynı cast'te ileri/geri veya tekrarlanan derinlik varsa gradient yapılmaz. Sonuç ham sinyal geçiş adayıdır; sıcaklık etkisi ayrıştırılmadan haloklin, kaynak kökeni veya mutlak tuzluluk kanıtı değildir. Önerilen ek örnekleme derinlikleri basit gradient baseline'dır; eğitimli AI yok.

## Tekrarlanabilirlik

Ham SHA256 ve metadata SQLite'a değiştirilemez sürümle kaydedilir. Karar kaydı girdileri, model sürümünü, hesap kodu hash'ini, literatür parametre dosyası hash'ini ve bağlam veri kimliklerini tutar. Aynı girdi/kod/sonuç aynı run_id verir. Ham veri, CSV ve Parquet birbirinden izlenir. Birim hatası, NaN/Inf, yanlış zaman, eksik provenans ve negatif fiziksel girdiler test edilir. Yazılım testinin geçmesi saha validasyonu anlamına gelmez.


## 0.2 dashboard ve saha eşleştirme eki

Bölgesel kuzey iklim modeli ayrıca indirildi: EC_Earth3P_HR, 1995–2014 / 2030–2049, düzeltme kapalı. GDD5/don olmayan pencere/yağış göstergelerinin işlenmesi kendi hesabımız; dış iklim modelini biz çalıştırmış sayılmayız. SSP literatür seçimi bu tek model paketini değiştirmez. Kaynak, dönem değişimi ve veri kalite kararları [NORTH_DATA_PLAN](NORTH_DATA_PLAN.md) içindedir. Hava sıcaklığı deniz sıcaklığına dönüştürülmez.

Türkiye dashboard ortak depo ve net ek su bütçesini düzenler. Referans sulamasız ET açığı eksi bütçe, sıfırdan küçükse sıfır alınır; bu ikinci ekran sulama programı/verim modeli değil, net bütçe farkıdır. Aynı hesap beş bölgeye uygulanır.

Optimizer optimumdaki kaynak kullanımı, kalan kapasite ve bağlayıcı kısıtları gösterir. Bağlayıcılık, kalan kapasitenin sayısal tolerans içinde sıfır olmasıdır; tek başına gölge fiyat veya kaynak artışı faydası değildir. Ek LP hedef eşitliğini kaldırıp aynı kaynak kısıtları altında maksimum kg bulur; hedef mümkün değilse açık miktarı böyle hesaplanır.

Saha karşılaştırmasında Haversine konum farkı, UTC saat farkı, derinlik farkı ve aynı yerinde sıcaklık tanımı denetlenir. Varsayılan 5 km/3 saat/1 m toleranslar kullanıcı senaryosudur. Uyuşmayan çiftte residual veya karar güncellemesi üretilmez. Gerçek dış profil için kaynak kaydı/ham SHA, kalite OK, UTC/GPS, basınçtan derinlik ve açık in_situ sıcaklık metadata beyanı gerekir. Potansiyel/korunumlu sıcaklık otomatik çıkarılmaz. Gerçek profil seçilirse manuel gözlem alanları değil, kayıtlı örnek satırı kullanılır; beklenen model sıcaklığı kaynak URL ile kullanıcı beyanıdır.

UI ilk saha deneyi açık simülasyondur. Beklenen su 10°C, gözlem senaryosu 5°C ve enerji bütçesi 25.110 kWh iken mevcut varsayımlarla önceden mümkün olan plan daha soğuk kaynakta kısıtı aşar. Bu kaynak ve kısıt mekanizmasının örneğidir; gerçek Arktik ölçümü veya kalibrasyon değildir. Üretim payı/statü aynı kalıp yalnız enerji değişirse changed_decision false olur. Güven puanı üretilmez.
