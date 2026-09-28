> U11 güncel bağlam: [FINAL_PRODUCT_CONTRACT](FINAL_PRODUCT_CONTRACT.md), [FUTURE_NORTH_DECISION_MODEL](FUTURE_NORTH_DECISION_MODEL.md) ve [ARCTIC_RESEARCH_PROGRAM](ARCTIC_RESEARCH_PROGRAM.md) geçerlidir. Aşağıdaki bilimsel ayrıntılar korunur; eski UI adları güncel arayüz gereği değildir. Saha araştırması yalnız sıcaklık/arıtma hesabından ibaret değildir: A profil, B numune, C karar bilgisi birlikte planlanır.

# Kuzey için ilk ürün portföyü — U9

22 Eylül 2026. İlk araştırma portföyü **arpa + patates + marul** olarak kalır. Bu defa seçim, alternatifleri karşılaştıran kaynak matrisiyle desteklenmiştir. **Longyearbyen için doğrulanmış varsayılan üretim önerisi yoktur.** Adaylar otomatik gösterilebilir; eksik yerel parametreler “bilinmiyor” kalır. U8'in 1 ha arpa + 0,5 ha patates + 333,333 m² marul hesabı **AÇIKLAYICI / VARSAYIMA DAYALI SİMÜLASYON** olmaya devam eder.

Makinece okunabilir inceleme: [north_evidence.json](../data/north_evidence.json). Asıl hesap kataloğu bu incelemede değiştirilmedi; dış araştırma bulguları sessizce model katsayısı yapılmadı.

## Birinci portföy

| Ürün / yöntem | Kuzey kanıtı ve dönem | Verim, su ve enerji dayanağı | Varsayım olmadan henüz söylenemeyen |
|---|---|---|---|
| **Arpa — açık tarla adayı** | NORA çok yer/çeşit denemesi: Alta 2014 98 gün; Holt 2015 124 gün, Saana 131 gün. | Alta Tiril 2,42 t kuru madde/ha. Bu değer yaş tane kg/ha değildir. FAO Kc başlangıcı mevcut; yerel ET0 yok. Islak hasatta kurutma enerjisi gerekir. | Longyearbyen çeşidi, GDD/don eşiği, olgunlaşma, sulama ve enerji. |
| **Patates — açık tarla adayı** | Tromsø 69,7°K; Gullauge/Mandel, 24 saat doğal fotoperiyot, kontrollü 9–21°C. 86 günlük deney. | Yaklaşık 15°C yumru verimi optimumu bu deneyin sonucudur; 12 L saksı verimi tarla kg/ha olmaz. FAO Kc başlangıcı var. | Yerel tarla verimi, don eşiği, aktif katman/drenaj, depolama ve enerji. |
| **Marul — hidroponik/sera adayı** | Alaska NFT araştırması yöntem dayanağıdır; seçilen kuzey tesisinin validasyonu değildir. | Arizona karşılaştırmasındaki 20 L/kg ve 25 kWh/kg dış referanstır. U8 3 kg/m²/çevrim değeri kullanıcı senaryosudur. | Yerel çevrim verimi, ısı/LED/nem bütçesi, su geri kazanımı ve mevsim. |

Kaynaklar: [NORA 2016, Tablo 3-2 ve 3-3, PDF s.18/21](https://www.nibio.no/prosjekter/northern-cereals--new-markets-for-a-changing-environment/_/attachment/inline/9b22f769-3666-463e-bcca-4c058231fc5d:1167bdffe36f245bedb4dcfa9c70a4a87315e953/NORA%20Northern%20Cereals%20Final%20Report.pdf), [Mølmann ve Johansen 2025](https://doi.org/10.1007/s11540-025-09854-0), [UAF 2007, s.24–25](https://www.uaf.edu/afes/publications/database/variety-trials/files/pdfs/AES-2007.pdf), [Barbosa vd. 2015](https://doi.org/10.3390/ijerph120606879), [FAO-56 Tablo 11–12](https://www.fao.org/4/X0490E/x0490e0b.htm).

Bu üçlü; tahıl, yumru ve kontrollü yapraklı üretimi aynı su/enerji kısıtında karşılaştırmaya yeter. Ürünlerin kg'larını eşit beslenme değeri saymayız. Hedefler ürün bazındadır. Seçim bir ürün kararıdır; en iyi Arktik ürünleri ispatlayan sıralama değildir.

## İncelenen ek adaylar

| Aday | Birincil kanıt | Karar |
|---|---|---|
| Ispanak | Fairbanks 2003 denemesinde 30 Mayıs–7 Temmuz; Melody 1,90 lb/sıra-ft. Uzun günde çeşit seçimi önemli. | **Yedek.** Sıra aralığı doğrulanmadan kg/m² dönüşümü; su/enerji olmadan optimizere varsayılan yapılmaz. |
| Roka | EDEN ISS yüksek ışık: ortalama 29 gün, 5,49±0,40 kg/m²/çevrim; 8 çevrim. | **Yedek CEA.** Su/enerji yoğunluğu eksik. |
| Fesleğen | EDEN ISS 121 gün çoklu hasat, 7,30±0,93 kg/m²; 2 değerlendirilen çevrim. | **Yedek ot.** Kısa marul çevrimiyle eşitlenmez. |
| Mikro filizler | Tür, hasat evresi ve ortak su/enerji/verim paneli bu odak taramada doğrulanmadı. | **Seçilmedi.** “Mikro filiz” tek ürün katsayısı değildir. |

Kaynaklar: [UAF Vegetable Variety Trials 2003](https://www.uaf.edu/afes/publications/database/circulars/files/pdfs/C127.pdf), [Zabel vd. 2020, EDEN ISS, Tablo 6–7](https://doi.org/10.3389/fpls.2020.00656). EDEN ISS **Antarktika** deneyidir; Arktik yerel tarla kanıtı değildir. Kontrollü ortam 21/19°C gündüz/gece ve 17 saat ışık set noktalarıyla işletilmiştir. Bunlar ürünlerin evrensel optimum/don sınırları değildir. Çalışmada bu adaylar için yerel Arctic kWh/kg aralığı verilmediği için türetmedik.

## Otomatik seçim için gereken eşik

Şu anda uygulama “araştırma adaylarını” önerebilir; gerçek otomatik uygunluk elemesi için **yer + çeşit + dönem** düzeyinde fenoloji/GDD/don sınırı, toprak/drenaj, sulama ve verim gerekir. Uygunluk bilinmiyorsa açık tarla kapısı kapalı kalır. Kullanıcının uygunluk varsayımıyla açması mümkündür ve görünür etiketlenir. Hidroponik sistemler için açık tarla Kc kullanılarak tüketim hesaplanmaz.

FAO katalog süreleri arpa 135, patates 130, marul 75 gündür; bunlar belirli başka iklim örnekleridir. NORA'nın gözlenen 98–131 günlük takvimleri bu sürelerin evrensel olmadığını gösterir; yerel validasyon yapılmadan motorun dört aşamalı takvimi değiştirilmedi.

## Yeni gerçek iklim alt kümesi

NASA'nın belgelenmiş THREDDS yolundan ACCESS-CM2 v2.0, **SSP245 ve SSP585 / 2035**, Tmin/Tmax/toplam yağış indirildi. Alt küme 2×2 hücre; en yakın nokta 78,125°K / 15,625°D. Altı NetCDF ve SHA256 kayıtları, 730 günlük nokta satırı, tekrar üretim betiği var. [İndirme/QA özeti](../data/north/u9_acquisition/validated_summary.json), [betik](../scripts/research_north_u9.py), [NASA kaynak ve erişim yöntemi](https://www.nccs.nasa.gov/data-collections/nex-gddp-cmip6/).

**Tek modelin tek yılı**, 2030–2049 klimatolojisi veya SSP'ler arasında güvenilir etki sıralaması değildir. Bu veriler kanıt panelinde incelenebilir; ürün uygunluğu veya yıllık kullanılabilir tatlı su olarak bağlanmaz. Çok yıl, çok model, ET0 ve yerel ürün/zemin kalibrasyonu sonraki veri adımıdır.
