> U11 güncel bağlam: [FINAL_PRODUCT_CONTRACT](FINAL_PRODUCT_CONTRACT.md), [FUTURE_NORTH_DECISION_MODEL](FUTURE_NORTH_DECISION_MODEL.md) ve [ARCTIC_RESEARCH_PROGRAM](ARCTIC_RESEARCH_PROGRAM.md) geçerlidir. Aşağıdaki bilimsel ayrıntılar korunur; eski UI adları güncel arayüz gereği değildir. Saha araştırması yalnız sıcaklık/arıtma hesabından ibaret değildir: A profil, B numune, C karar bilgisi birlikte planlanır.

# Kuzey su güvenliği — U9

22 Eylül 2026. **Kar, buz ve yağışın varlığı; üretimin gerektiği yerde ve dönemde kullanılabilir, güvenilir su tahsisi demek değildir.** NVE'nin Svalbard özeti, akarsuların genel olarak yılda 2–4 ay aktığını ve göllerin 9–10 ay buzla kaplandığını belirtir. Bu bölgesel bulgu tüm sahaların su kıt olduğunu söylemez; mevsim ve depolama hesabını gerekli kılar. [NVE birincil kurum kaynağı](https://www.nve.no/nytt-fra-nve/nyheter-tilsyn/ny-rapport-om-biodiversitet-i-ferskvann-pa-svalbard/).

## İki ayrı su problemi

**Karasal su güvenliği:** yağış/kar/buzul erimesi → havza akışı → erişilebilir çekim → mevcut kullanım ve çevresel gereksinimler → depolama/kayıp → üretim dönemine güvenilir tahsis. Yağış mm'sini araziyle çarpmak tek başına kullanılabilir su m³ vermez. Kar ve buzul erimesini akıma tekrar eklemek çift sayım yaratabilir.

**Deniz kaynak suyunun kullanılabilirliği:** yer/zaman/derinlikte sıcaklık, tuzluluk ve ilgili kalite → uygun arıtma prosesi → su geri kazanımı, enerji, kimyasal gereksinim ve konsantre atık → üretime verilebilen su. PWN ikinci zincirin gözlem aracıdır. Deniz tatlılaşma sinyali doğrudan sulama suyu değildir.

Bu ayrım ürün tasarım kararı olarak ayrı gruplarda görünür: “Karasal su güvenliği” ve “Su kaynağı portföyü”. Yerel tatlı su kapasitesi, depolanmış su, yeniden kullanım ve arıtılmış deniz suyu ayrı bütçelerdir. Kalite bilinmiyorsa kullanılabilir kabul edilmez.

## Eldeki veri ve gerçek açıklar

| Katman | Bu sürümde gerçek durum | Sonraki somut veri işi |
|---|---|---|
| Gelecek iklim | Mevcut EC_Earth3P_HR uzun dönem verisine ek NASA ACCESS-CM2 SSP245/585 2035 alt kümesi indirildi ve QA geçti. | Çok yıllı/çok model karşılaştırma; ışınım/nem/rüzgâr ile ET0; don/GDD ürün bağlantısı. |
| Toprak/permafrost | ESA CCI v5 kataloğu incelendi: 1997–2023, 1 km aktif katman, permafrost oranı ve yer sıcaklığı ürünleri. **Yerel raster indirilmedi.** | Konuma göre raster, drenaj/toprak, arazi erişimi, altyapı. Çözülen zemin tarıma otomatik uygun değildir. |
| Karasal hidroloji | NVE gözlem ve API yolları belirlendi; **yerel debi/tahsis serisi alınmadı.** | Hidrolojik havza/istasyon, zaman aralığı, kalite kodu, mevcut kullanım ve depo. HydAPI API anahtarı ister; bu tur hesap oluşturulmadı. |
| Deniz profili | Copernicus TOPAZ4 katalog/kalite belgesi incelendi; **sayısal T/S profili alınmadı.** | `cmems_mod_arc_phy_my_topaz4_P1M` 3B aylık T/S alt kümesi; gerçek zaman/derinlik/koordinat ve belirsizlik. |
| CEA enerji | Marul için dış coğrafya referansı mevcut; yerel Arctic enerji aralığı yok. | Saatlik sera ısı kaybı, LED, nem alma, pompalar, atık ısı ve elektrik profili. |
| Arıtma | Mevcut sınırlandırılmış RO sıcaklık ilişkisi literatürden. | Membran/geri kazanım/tuzluluk/ön arıtma eşleştirmesi ve uzman doğrulaması. |

Kaynaklar: [NASA NEX-GDDP](https://www.nccs.nasa.gov/data-collections/nex-gddp-cmip6/), [ESA Permafrost veri kataloğu](https://climate.esa.int/en/projects/permafrost/data/), [NVE HydAPI erişim belgesi](https://hydapi.nve.no/UserDocumentation/), [Copernicus veri erişimi](https://data.marine.copernicus.eu/product/ARCTIC_MULTIYEAR_PHY_002_003/services), [Copernicus QUID](https://catalogue.marine.copernicus.eu/documents/QUID/CMEMS-ARC-QUID-002-003.pdf), [RO sıcaklık deneyi](https://www.sciencedirect.com/science/article/pii/S1944398625001730).

**Önemli profil ayrımı:** incelenen QUID, günlük TOPAZ4 ürününü yüzey 2B, aylık ürünü 3B olarak tanımlar. Yüzey sıcaklığı “su kolonu profili” diye çizilmez. Aylık ortalama da seferin anlık CTD gözlemi değildir. Ürün indirilirken güncel boyutları ayrıca doğrulanmalıdır.

## Hesapta şimdi ne var?

Mevcut motor dönemlik kaynak kapasitelerini ve ürün bazında net su gereğini alır; kuzeyde bu kapasiteler/hidrolojik tahsis **kullanıcı senaryosudur**. Yağış, depo ve mevsimlik akıştan kapasite üreten yerel hidroloji modeli henüz yoktur. U9 NASA yağış alt kümesi bunu değiştirmez. Ön-TASE çıktısı bugün açıklayıcı varsayım hesabı olarak kaydedilebilir; tamamen kaynakla kalibre edilmiş gelecek deseni diye sunulmaz.

Gelecekte aylık bilanço için depo_t+1 = depo_t + gerçekten erişilebilir giriş_t − çekim_t − kayıp_t; depo ve çekim sınırları, çevresel/diğer kullanımlar ve kurak yıl güvenilirliği birlikte uygulanacak. Bu denklem **planlanan yöntemdir**, mevcut motorun çalıştırdığı aylık hidroloji değildir.

## PWN neyi günceller?

Mevcut çalışan bağlantı: geçerli eşleşmiş **deniz suyu sıcaklığı → sınırlandırılmış RO enerji hesabı → aynı optimizasyon motoru**. RO deneyindeki 5–18°C aralığı dışına güvenilir katsayı varsayılmaz. Tuzluluk/EC, basınç/derinlik ve numune kimyası daha sonra doğrulanmış süreç ilişkileriyle eklenir; veri kolonunun bulunması tek başına karar değişkenine bağlamak değildir.

PWN **yıllık karasal tatlı suyu, ürün verimini, gelecek GDD'yi veya permafrost uygunluğunu güncellemez**. Gemi profiliyle kıyısal alım noktası farklıysa arıtma bağlantısı yalnız transfer hipotezidir; yer/zaman/derinlik eşleşmesi ve temsiliyet gerekir. Mevcut model “güven arttı” puanı hesaplamaz. Aynı desen, kaynak tahsisi farkı, enerji farkı, çözümsüzlük veya etkisizlik geçerli sonuçlardır.

## Kaynak ve QA kaydı

[data/north_evidence.json](../data/north_evidence.json) kaynak incelemesini uygulamaya taşır. Yeni iklim indirmeleri ayrı klasördedir: [katalog çözülmüş istekler ve SHA](../data/north/u9_acquisition/catalog_resolved_attempts.json), [QA/özet](../data/north/u9_acquisition/validated_summary.json). İlk NASA dosya yolu sürüm eki nedeniyle 404 verdi; katalogdan `v2.0` yolu çözülerek başarılı indirildi, ilk girişim de saklandı. Altı dosyada toplam 8.760 ham hücre/değişken değeri; nokta çıktısında 730 satır vardır. Veri kaydı saha ölçümü değildir.
