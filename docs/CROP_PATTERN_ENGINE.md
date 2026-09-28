# Ortak ürün deseni simülasyon motoru

22 Eylül 2026 · U8 / TESLİM 003. Çalışan hesap: [planning.py](../backend/planning.py), girdi sözleşmesi: [planning_contracts.py](../backend/planning_contracts.py). Bu belge kodun mevcut davranışını anlatır; saha validasyonu iddiası değildir.

## Ürünün merkezi

**Bölge + mevcut desen veya aday ürünler + kullanıcı koşulları → su hesabı → ortak optimizasyon → önerilen desen + gerekçe.** Türkiye ve kuzey ayrı hesap motorları kullanmaz. `GET /api/planning-context` kaynaklı başlangıcı yükler; `POST /api/simulate` aynı `SimulationRequest` sözleşmesiyle iki modu çözer. Resmî başlangıç, düzenlenen mevcut desen ve öneri ayrı tutulur. Her hesap kaynak/kod hash'leri, girdileri ve run_id ile kaydedilir.

Önceki tek marul hedefi üzerinden yöntem/su kaynağı seçimi, özgün ürün deseni kararını temsil etmiyordu. Dar arıtma duyarlılığı örneği olarak korunabilir; ana motor artık birden çok ürünün gerçek alan/kapasite miktarını seçer.

## Veri ve su yolu

- Beş ilin 21 kaynaklı ekiliş/üretim kaydı: [Türkiye veri belgesi](TURKIYE_REGIONAL_SIMULATOR.md). Dokuz ürünün FAO kaynaklı Kc/aşama kataloğu: `data/agriculture/crops.json`. Evrensel GDD/don/zemin eşikleri uydurulmaz; eksikler boş kalır.
- Türkiye'de dört gelişme aşamasının günlük Kc eğrisi × ERA5 ET₀ = ETc. Yağış ve kök bölgesi deposu sonrası karşılanmayan ET, zamanında tamamlayıcı sulama varsayımıyla net gereksinimdir. `brüt m³/ha = net mm × 10 / randıman`.
- Başlangıç 60 mm depo, 30 mm başlangıç suyu, %75 randıman ve genel ekim takvimi senaryo girdileridir. Kullanıcı yağış/ET₀ çarpanı, takvim, alan, verim, minimum/azami pay, üretim hedefi ve su bütçesini değiştirebilir.
- Çeltikte ETc toplam tava suyu sayılmaz; ek gereksinim bilinmiyorsa açık manuel net sulama girdisi gerekir. Kuzey gelecek paketinde ET₀ yoktur; gelecek tarla sulaması da açık kullanıcı girdisidir.

FAO dayanağı: [FAO-56 Bölüm 6, Tablo 11–12](https://www.fao.org/4/X0490E/x0490e0b.htm). Yerel takvim ve sulama validasyonu yapılmadı. Sabit verim katsayısı su stresi altında gerçekleşecek verimi hesaplamaz.

## Karar ve amaç

Her uygun ürün × yöntem × su kaynağı seçeneğine bir kapasite değişkeni atanır. Açık tarla değişkeni **ha**; sera/hidroponik değişkeni **m² yetiştirme yüzeyi**dir. Üretim bunların yöntem verimiyle çarpımından çıkar. Alan, ayrı yöntem kapasiteleri, kaynak hacimleri, ürün alt sınırları ve varsa enerji bütçesi birlikte uygulanır. Ayrıntı: [PATTERN_CONSTRAINTS.md](PATTERN_CONSTRAINTS.md).

SciPy HiGHS önce her ürünün hedefini en fazla %100'e kadar karşılayan oranların ağırlıklı toplamını yükseltir. Aynı başarı düzeyinde su çekimini, tüm seçeneklerin enerji katsayıları biliniyorsa üçüncü aşamada enerjiyi azaltır. Hedef ve öncelik kullanıcı tercihidir. Farklı ürünlerin tonları ortak beslenme/değer puanına çevrilmez.

Bu amaç “hektarda en az su isteyen ürünü her zaman artır” demek değildir. Ürün grubunun bütün hedefini karşılamak için gereken su ve hedef ağırlığı önemlidir. Açıklamalar hesaplanan m³/ha, tam hedefin su maliyeti, gerçek alan değişimi ve bağlayan minimum/bütçelerden üretilir; LLM gerekçesi değildir. Bağlayıcı kısıt tek başına nedensel duyarlılık katsayısı sayılmaz.

## Çalıştırılmış Konya örneği

22 Eylül 2026'da `planning_context('konya')` başlangıcının tatlı su bütçesi %20 azaltılıp aynı `simulate` çağrısıyla hesaplandı. %50 ürün minimumları, eşit hedef ağırlıkları ve en az ekilen alan oranı 0 korundu.

| Ürün | Kaynaklı başlangıç, ha | Öneri, ha |
|---|---:|---:|
| Buğday | 596.686,60 | 298.343,30 |
| Arpa | 385.201,10 | 355.914,78 |
| Dane mısır | 185.505,40 | 185.505,40 |
| Şeker pancarı | 101.947,30 | 101.947,30 |
| Patates | 10.801,00 | 10.801,00 |

Modellenmiş mevcut brüt gereksinim **6.057,39 milyon m³**; senaryo bütçesi **4.845,91 milyon m³**; öneri bu bütçeyi sayısal tolerans içinde kullanır. **327.629,62 ha senaryo kapasitesi tahsis edilmez.** Buğdayın %50 üretim tabanı ve tatlı su bütçesi bağlayıcıdır. Buğdayın hektar başına suyu düşük olmasına rağmen bütün buğday hedefinin su maliyeti büyük olduğundan bu amaç altında alanı azalır. Ağırlık/minimum değişince öneri de değişebilir.

Bu sonuç su tasarrufu ölçümü, DSİ tahsisi veya çiftçiye doğrulanmış öneri değildir. İl ekiliş toplamı fiziksel benzersiz arazi ölçümü değildir; burada kapasite senaryosuna başlangıç verir. Eski Konya raporunun yaklaşık %8,7 göreli sonucu bu yeni m³ hesabından ayrıdır.

## Sınırlar ve doğrulama

Motor bütçe/alan/üretim tutarlılığını denetler; imkânsız minimumları sessizce kaldırmaz. Eksik enerji sıfır sayılmaz. Kuru/sulu alan ayrımı, ürün ardışıklığı, yerel fenoloji, gerçek su tahsisi ve verim-su tepkisi sonraki veri işleridir. Güncel test sonucu [BUILD_STATUS.md](BUILD_STATUS.md) içinde tutulur; burada sayısal örneğin çalıştırıldığı tarih yukarıdadır.
