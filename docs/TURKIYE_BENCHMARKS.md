# Türkiye benchmark kümesi — beş nokta

22 Eylül 2026. **MODEL / REANALYSIS + açık varsayımlı transfer demonstrasyonu.** Türkiye genelinde bilimsel validasyon değildir. Konya pilotunun üzerine yeni yazılım kurmak yerine, aynı yeni fiziksel hesabın farklı bölgesel iklim girdileriyle çalışmasını sınar. Makine tarafından okunabilir seçim gerekçeleri, kaynak tarihleri ve sınırlar `data/benchmark_context.json` içindedir.

## Seçim gerekçesi

Ortak ürün buğdaydır. Resmî kaynaklar bölgelerde ürünün ve su yönetimi probleminin varlığını destekler. Bunlar yerel 2022–2023 sulama/verim ölçümlerinin yerine geçmez.

| Nokta | Karşılaştırmaya katkısı | Kaynak ve desteklediği dar iddia |
|---|---|---|
| Konya | Geçmiş pilotla süreklilik; iç havzada yeraltı suyu bağlamı | Kullanıcının eski final raporu pilotun kaynağıdır. [Bakanlık, 23.03.2020](https://www.tarimorman.gov.tr/Haber/4437/Konya-Kapali-Havzasinda-Yeralti-SuyunaYakin-Takip), yeraltı suyunun tarımsal önemini ve izlenmesini açıklar. Haberdeki rakamlar güncel tahsis sayılmaz. |
| Seyhan / Adana | Konya dışındaki ilk transfer; Aşağı Seyhan üretimi ve sektörel kullanım | [İl Müdürlüğü, 23.06.2020](https://adana.tarimorman.gov.tr/Haber/697/Seyhan-Ilce-Tarim-Ve-Orman-Mudurlugu-Bugday-Cesit-Verim-Demonstrasyonu-Kurdu) buğday denemesi/hasadını doğrular. [2019 kuraklık planı](https://www.tarimorman.gov.tr/SYGM/Belgeler/KURAKLIK%20Y%C3%96NET%C4%B0M%20PLANLARI%2009.01.2023/SEYHAN%20HAVZASI%20KYP%20Y%C3%96NET%C4%B0C%C4%B0%20%C3%96ZET%C4%B0.pdf), PDF s.45/basılı4-8, tarihsel sektörel kullanım bağlamını verir. |
| Gediz / Manisa | Batı Türkiye; tahıl üretimi ve kuraklık koşullarında sektörler arası paylaşım | [İl Müdürlüğü, 25.06.2021](https://manisa.tarimorman.gov.tr/Sayfalar/Detay.aspx?TermId=d59be594-0585-4d66-8a17-00217dd913d6&TermSetId=51c21c3c-cdd9-4e02-8fb2-bd268f69bdcc&TermStoreId=368e785b-af33-487d-a98d-c11d5495130b&UrlSuffix=748%2FManisada-Hububat-Hasadi-Devam-Ediyor), buğday/arpa hasadını bildirir. [Gediz sektörel tahsis planı](https://www.tarimorman.gov.tr/SYGM/Belgeler/Gediz-K%C3%BC%C3%A7%C3%BCk%20Menderes%20Havzas%C4%B1%20SSTP%20Eylem%20Plan%C4%B1_18.12.2020/Gediz%20Havzas%C4%B1%20SSTP%20Eylem%20Plan%C4%B1_18.12.2020.pdf), 2019 plan/31.12.2020 genelge/2021–2025 eylem dönemi; güncel tahsis değildir. |
| GAP / Harran–Şanlıurfa | Güneydoğuda sulama ve drenaj altyapısı; farklı yağış ve atmosferik talep girdileri | [GAPTAEM araştırma kataloğu](https://arastirma.tarimorman.gov.tr/gaptaem/Menu/34/Sonuclanan-Projeler), 1987/1996/1998 tarihli buğday-su/sulu üretim çalışmalarını listeler. [DSİ inşa listesi](https://bolge15.dsi.gov.tr/Sayfa/Detay/809), Harran sulama/tahliye işlerini içerir; tamamlanmış tesis veya garantili su miktarı göstermez. |
| Trakya / Edirne | Kuzeybatı Türkiye'de kışlık tahıl üretimi; ortak modelin farklı sıcaklık ve yağış serisine tepkisi | [İl Müdürlüğü, 17.05.2024](https://edirne.tarimorman.gov.tr/Haber/491/Hububat-Ve-Aycicegi-Ekimi-Yapilan-Arazilerde-Fenolojik-Gozlem-Yapildi), kışlık buğdayın fenolojisini gözler. [İl Su Kurulu, 09.04.2025](https://edirne.tarimorman.gov.tr/Sayfalar/GormeEngellilerDetay.aspx?Liste=Haber&OgeId=531), su kaynaklarının korunması ve sulama verimliliğini ele alır. |

Bu seçim **araştırma tasarımı kararıdır**: beş nokta ülkenin istatistiksel örneklemi veya beş havzanın tam temsili değildir. Edirne ve Harran seçimleri resmî buğday kayıtları ve belirgin su yönetimi bağlamını birlikte sağlar. İl, havza ve proje adları yerel bağlam etiketidir; geometrik havza sınırı işlenmiş değildir.

## Gerçek veri ve adil karşılaştırma

Her noktada 01.01.2022–31.12.2023 için **730 günlük** Tmin, Tmax, yağış ve ET₀ vardır. Aynı sağlayıcı, model (`era5`), UTC günlük toplama, °C/mm birimleri ve yükselti düzeltmesi kapalı ayar kullanılır. Türkiye toplamı 3.650 satırdır; ayrı kuzey bağlamı Longyearbyen ile bütün dosya **4.380 satırdır**. Dört değişkende eksik kayıt yoktur. İndirilmiş ham JSON'lar, SHA256, gerçek grid koordinatı ve erişim tarihi `data/manifest.json` ile izlenir. [Sağlayıcı yöntem belgesi](https://open-meteo.com/en/docs/historical-weather-api)

Aşağıdaki sayılar yalnız **2023 günlük kaynak değerlerinin toplamıdır**; iklim normali, ürün su ihtiyacı veya sulama açığı değildir. Yağış karın su eşdeğerini de içerir; ET₀ referans bitki evapotranspirasyonudur.

| Nokta | İstenen koordinat | Gerçek ERA5 grid koordinatı; yükselti | 2023 yağış, mm | 2023 ET₀, mm |
|---|---|---|---:|---:|
| Konya | 37,87 / 32,49 | 37,75 / 32,50; 1.189 m | 368,70 | 1.342,66 |
| Seyhan / Adana | 37,00 / 35,32 | 37,00 / 35,25; 95 m | 668,90 | 1.449,40 |
| Gediz / Manisa | 38,61 / 27,43 | 38,50 / 27,50; 323 m | 988,60 | 1.273,79 |
| GAP / Harran–Şanlıurfa | 36,87 / 39,03 | 36,75 / 39,00; 369 m | 332,80 | 1.842,57 |
| Trakya / Edirne | 41,68 / 26,56 | 41,75 / 26,50; 125 m | 473,70 | 1.237,75 |

Tüm bölgelerde 1 hektar, 1 Kasım 2022 başlangıcı, 240 günlük aynı FAO-56 örnek takvimi ve aynı Kc duyarlılık senaryoları kullanılır. Toprak deposu 60 mm, başlangıç suyu 30 mm **ortak tasarım varsayımıdır**. Yerel ölçüm veya fit edilmiş katsayı yoktur. Takvimin her bölgede gerçek ekim/hasat tarihiyle eşleştiği iddia edilmez. Böylece farklar farklı gizli parametre atamalarından değil, aynı hesap altındaki iklim girdilerinden doğar. [FAO-56, Bölüm 6, Tablolar 11–12](https://www.fao.org/4/X0490E/x0490e0b.htm)

## Çıktının sınırı ve sonraki doğrulama

Bir sonraki veri isteği bölgeye göre daraltılacak; aşağıdakiler **gereksinimdir**, elde edilmiş veri değildir:

| Bölge | Öncelikli yerel veri | Neyi sınayacak? |
|---|---|---|
| Konya | Kuyu çekimi/seviye zaman serisi, parsel sulaması, buğday fenolojisi ve toprak nemi | Meteorolojik açığın gerçek çekim baskısı ve üretimle ilişkisi |
| Seyhan–Adana | Sulama birliği teslim/tahsis takvimi, drenaj, yerel ekim/hasat ve toprak su kapasitesi | Yağışla aynı toplam suya sahip görünmenin mevsimsel erişim anlamına gelmediği |
| Gediz–Manisa | Güncel sektör/alt havza tahsisi, sezon içi akım/depolama, kaynak kalitesi ve yerel ürün takvimi | Sektörler arası rekabet ve kalite sınırının ortak iklim hesabına etkisi |
| GAP–Harran | Gerçek kanal teslimleri, uygulama randımanı, drenaj/tuzluluk ve buğday verim kayıtları | Altyapı varlığı ile tarlada kullanılabilir su/kalite arasındaki fark |
| Trakya–Edirne | Kışlık buğday fenolojisi, sezonluk toprak nemi ve sulanan/sulanmayan parsellerin bağımsız verimi | Ortak takvim varsayımının ve ek sulama ihtiyacının yerel geçerliliği |

Bu veriler aynı sezon/parsel referansına bağlanmadan yeni bölgesel parametreler “kalibre edildi” diye işaretlenmeyecek. İlk adım, her bölgeden mümkün olan bir bağımsız sezonu doğrulama için ayırmaktır; mevcut iki yıllık reanalizden bunu üretmiş saymıyoruz.

Şimdiki çıktı, varsayımsal ortak buğday sistemi için yağış–ET₀ kaynaklı su dengesi ve parametre duyarlılığıdır. Gerçek sulama önerisi için yerel ürün takvimi/çeşidi, toprak su tutma kapasitesi, başlangıç nemi, sulama uygulaması, randıman, su hakkı/arzı, kalite ve bağımsız verim gözlemi gerekir. Noktasal yeniden analizden havzanın kullanılabilir suyunu çıkaramayız. Havza/yıl verisini eğitim ve değerlendirme arasında ayırarak bağımsız doğrulama yapılmadan “transferability kanıtlandı” denmez.

Longyearbyen bu beşli buğday karşılaştırmasına eklenmez; kuzeyde üretim yöntemi ve su/enerji koşulları için ayrı bağlamdır. Veri lisansı ve sürümleme ayrıntıları `docs/DATA_ACCESS_LOG.md` içinde kayıtlıdır.
