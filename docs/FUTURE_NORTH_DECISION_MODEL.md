# Güncel rebuild kaydı · 22 Eylül 2026

Güncel amaç kuralı REBUILD_EVIDENCE_AUDIT içinde. source_resolved politikasında patatesin açık tarla elemesi açıklayıcı senaryoda da uygulanır. Tarihsel üç ürünlü örnek sonuçlar bu yeni koşulun sonucu sayılmaz. Açık kg hedefi gerektirmeyen su/enerji öncelikli kapasite modu eklendi.

Bağlayıcı sözleşme: [REBUILD_CONTRACT.md](REBUILD_CONTRACT.md). Çalışan/eksik ayrımı: [REBUILD_EVIDENCE_AUDIT.md](REBUILD_EVIDENCE_AUDIT.md), [BUILD_STATUS.md](BUILD_STATUS.md).

---

## Önceki ayrıntılı kayıt (tarihsel uygulama durumları kendi tarihleriyle okunur)

# Future North karar modeli — beş açık planlama amacı

22 Eylül 2026 · U11 / TESLİM 005 · uygulama sürümü 0.5.0.

Bu belge `FINAL_PRODUCT_CONTRACT.md` §12 ve §15'in **çalışan uygulamasını** açıklar. Kod kaynakları: `backend/planning.py`, `backend/planning_contracts.py`; doğrulama: `tests/test_planning_objectives.py`. Buradaki sayılar 22 Eylül 2026 tarihinde mevcut açıklayıcı senaryo yeniden çalıştırılarak üretildi. Yerel Arktik ölçümü veya doğrulanmış tarımsal öneri değildir.

## Aynı motor, açık amaç seçimi

Karar değişkeni ürün × yöntem × su kaynağı için kapasitedir. Açık tarla değişkeni ha; sera/hidroponik değişkeni yetiştirme yüzeyi m²'dir. Üretim kg, su m³ ve enerji kWh kendi katsayılarıyla hesaplanır. Farklı ürün kg'ları gıda, besin değeri veya ekonomik değer eşdeğeri olarak toplanmaz. Bu çekirdek eğitilmiş AI değil matematiksel optimizasyondur.

Notasyon:

- `p_i`: ürün i'nin hesaplanan toplam üretimi, kg.
- `D_i`: kullanıcı talep hedefi, kg.
- `M_i`: beyan edilen minimum üretim, kg.
- `w_i`: açık kullanıcı önceliği; varsayılan 1. Gizli katsayı yoktur.
- `P_i`: aynı kaynak üst sınırları altında yalnız ürün i yetiştirilse ulaşılabilecek hesaplanmış üretim potansiyeli, kg.
- `z_i`: hedef veya potansiyelin en fazla %100'e kadar karşılanan oranı.

Alan, yöntem kapasitesi, uygun kaynak suyu, enerji bütçesi ve ürün alan payı kısıtları birlikte uygulanır. Uygunluk veya gerekli katsayı eksikse seçenek dışlanır. Kaynak kalitesi bilinmiyorsa kaynak kullanılamaz. Enerji bütçesi veya enerji önceliği uygulanırken eksik enerji katsayısı sıfır kabul edilmez.

## 1. Kaynak kapasitesini keşfet — `capacity`

Kullanıcının önceden cevap olarak kg miktarı yazması gerekmez. Motor her ürün için ayrı küçük bir optimizasyonla `P_i` hesaplar:

`P_i = max p_i`, yalnız i ürününe ait yöntem/kaynak değişkenleri açıkken.

Bu tek ürün hesabında açık alan, kontrollü kapasite, su kaynağı ve varsa enerji üst sınırları ile ürünün maksimum açık alan payı korunur. Portföyün minimum ekilen alan, minimum ürün alanı ve minimum üretim yükümlülükleri **normalizasyon hesabına dahil edilmez**. Bu nedenle `P_i`, bütün portföy yükümlülüklerini yerine getiren bir plan değil, kaynaklarla sınırlı tek ürün üst potansiyelidir. Ürünlerin `P_i` değerleri birlikte üretilebilecek toplam değildir.

Asıl ortak portföy çözümünde:

1. `z_i ≤ p_i / P_i`, `0 ≤ z_i ≤ 1` koşuluyla `Σ w_i z_i` maksimize edilir.
2. Aynı başarı düzeyi korunarak toplam brüt su çekimi minimize edilir.
3. Enerji katsayıları tam ise önceki aşamalar korunarak enerji minimize edilir.

**Bu modda beyan edilen kg hedefleri ve kg minimumları etkisizdir.** Motor bir kopyada `M_i = 0` yapar, hedef normalizasyonunu `P_i` ile değiştirir. Kullanıcının alan payı minimum/maksimumları ve minimum toplam ekilen alan tercihi asıl çözümde korunur. Hangi değişikliğin yapıldığı `objective.minima_policy` ve `effective_request` içinde görünür; özgün `request` değiştirilmez.

`P_i = 0` olan ürünün amaç ağırlığı hesapta sıfırdır; veri veya uygunluk eksikliğiyle üretim uydurulmaz. Hiç uygun seçenek yoksa sonuç `insufficient_data`, `optimized = null` olur. Mod çeşitliliği zorunlu kılmaz; bazı ürünlere sıfır üretim ayırması mümkündür.

## 2. Talebi karşıla — `demand`

Önceki motor davranışını koruyan varsayılan API amacıdır; Türkiye'nin mevcut üretimi doğal talep bağlamıdır.

1. `z_i ≤ p_i / D_i`, `0 ≤ z_i ≤ 1` altında `Σ w_i z_i` maksimize edilir.
2. Başarı düzeyi korunarak su minimize edilir.
3. Enerji katsayıları tam ise enerji minimize edilir.

`p_i ≥ M_i` korunur. `D_i`'nin tamamı zorunlu değildir; kaynak yetersizliğinde minimumun üstünde kısmi talep karşılanabilir. “Talebi karşıla” etiketi her talebin kesin karşılandığı anlamına gelmez. Kullanıcı tam talep istiyorsa minimumu hedefe eşitleyebilir veya aşağıdaki sıkı kaynak öncelikli modu seçebilir.

## 3. Dengeli plan — `balanced`

Kapasite moduyla aynı `P_i` normalizasyonu ve kg hedef/minimumlarını kullanmama kuralı geçerlidir.

1. Pozitif `P_i` olan adaylarda `z_i ≥ q` koşuluyla ortak `q` maksimize edilir: en az karşılanan potansiyel oranı olabildiğince artırılır.
2. Bu taban oran korunarak `Σ w_i z_i` maksimize edilir.
3. Önceki sonuçlar korunarak su, ardından katsayılar tam ise enerji minimize edilir.

İlk aşamadaki denge ürünlerin eşit kg üretimi değil, kendi kaynak potansiyellerinin ortak oranıdır. Kullanıcı öncelikleri ikinci aşamada açık ağırlık olarak kullanılır. `balanced_floor` sayısal sonucu raporlar. Veri eksikliğiyle potansiyeli sıfır kalan ürünler denge grubuna zorla eklenmez.

## 4. Su öncelikli — `water_priority`

Etkin ürünlerde `p_i ≥ max(M_i, D_i)` zorunlu kılınır. Aynı tam talebi sağlayan çözümler arasında önce su, sonra enerji minimize edilir. Tam talep sağlanamıyorsa uygulanamaz sonuç döner; sıfır üretim “en az su” cevabı yapılmaz. Kapalı ürünün önceden beyan edilmiş minimumu sessizce silinmez.

## 5. Enerji öncelikli — `energy_priority`

Aynı tam talep zorunluluğu uygulanır. Önce enerji, sonra su minimize edilir. Enerjisi bilinmeyen seçenekler kullanılmaz; eksik enerji sıfır kabul edilerek ucuz seçenek yaratılmaz.

Su ve enerji öncelikleri aynı sonucu verebilir. Farklı sonuç üretmek bir başarı koşulu değildir. Testte aynı marul talebi için açık tarla ve hidroponik yöntem seçenekleri birlikte verildiğinde su önceliği daha az su tüketen, enerji önceliği daha az enerji isteyen yöntemi seçmektedir. Bu davranış senaryo katsayılarının sonucudur; yöntemlerin evrensel sıralaması değildir.

## Sıralı çözüm ve tolerans

Amaçlar tek bir gizli bileşik puana çevrilmez. Her aşamada önceki optimum küçük sayısal toleransla korunur. Çözücü satırları sayısal ölçek için normalize edilir; son plan fiziksel kısıt toleransından geçirilir. `objective.stages`, gerçekten yürütülen amaç aşamalarını açıklar. Su/enerji/ürün sonuçlarının gösterim yuvarlaması çözümün dahili hassasiyeti değildir.

## Veriyle aday seçimi

Kuzey listesi sabit UI listesi değildir. `data/north_evidence.json` incelemesi SHA doğrulamalı `load_north_evidence` yolundan yüklenir. Bir ürünün ilk aday listesinde kalması için:

1. İnceleme kaydında `default_candidate = true` olmalı.
2. Ortak tarımsal ürün kataloğunda bulunmalı.
3. İncelenen yöntemler ile kataloğun desteklediği yöntemler kesişmeli.
4. İnceleme kaynak kimlikleri kaynak sözlüğünde bulunmalı.

Her adayda `retained`, `compatible_methods`, `verified_source_ids`, `readiness`, `exclusion_reasons` döner. Mevcut sonuç arpa, patates ve maruldur. Ispanak, roka, fesleğen ve mikro filizler araştırma kaydında görünür; parametre/yöntem/readiness eksikleri nedeniyle zorla optimizasyona eklenmez.

**Bu bir yerel iklim uygunluk sınıflandırıcısı değildir.** Mevcut adayların yerel parametre yeterliliği `DATA_NEEDED` durumundadır. Araştırma kanıtı Kuzeyde bir çalışma yapılmış olmasını gösterebilir; Longyearbyen'de aynı verimin veya su/enerji katsayısının geçerli olduğunu göstermez. NASA gelecek bağlamını seçmek bu eksikliği otomatik kapatmaz.

Varsayılan Kuzey bağlamı `capacity` açar; yerel verim, net sulama ve tarla/CEA enerji katsayıları `null` kalır. Açıklayıcı örnek ayrıca yüklenir; eski arpa/patates/marul katsayıları açık varsayım olarak kullanılabilir. Kullanıcı amaç seçimini örnek yüklerken korumak UI sorumluluğudur.

## Yeniden hesaplanan örnek — kesin öneri değildir

**AÇIKLAYICI / VARSAYIMA DAYALI SİMÜLASYON.** Ortak koşullar: 3 ha açık alan, 400 m² hidroponik kapasite, 40.000 kWh enerji, 2.000 m³ yerel tatlı su + 500 m³ depolanmış su + 2.000 m³ arıtılmış deniz suyu kapasitesi; 10 °C kaynak sıcaklığı. Açık alan uygunluğu ve ürün katsayıları örnek varsayımlardır. Öncelikler 1/1/1. Talep modunun sepeti 3.000 kg arpa + 10.000 kg patates + 1.000 kg maruldur; kapasite/dengeli mod bu sepetten bağımsızdır.

Tek ürün kaynak potansiyelleri: arpa 6.750 kg, patates 27.000 kg, marul 1.200 kg.

| Amaç | Arpa kg | Patates kg | Marul kg | Açık alan ha | Hidroponik m² | Su m³ | Enerji kWh |
|---|---:|---:|---:|---:|---:|---:|---:|
| Kapasite | 0 | 20.334,98 | 1.200 | 1,01675 | 400 | 3.413,16 | 40.000,00 |
| Dengeli | 3.366,02 | 13.464,10 | 598,41 | 1,79521 | 199,47 | 4.500,00 | 36.646,29 |
| Talep | 3.000 | 10.000 | 1.000 | 1,5 | 333,33 | 3.686,67 | 38.084,49 |

Dengeli çözüm ortak potansiyelin yaklaşık %49,867'sini karşılar. Kapasite çözümünde arpanın sıfır olması hata değildir; çeşitlilik garantisi istenirse dengeli amaç veya açık kısıt gerekir. Kontrollü m² ile açık tarla ha tek yüzdeye toplanmaz.

## Duyarlılık incelemesiyle ilişki

`backend/information_value.py` tek değişkenli iki uç nokta taraması yapar; olasılıksal bilgi değeri değildir. Kapasite/dengeli modda kaynak değişince `P_i` değerleri de yeniden hesaplanır. Dolayısıyla sonuç farkı, değişen kaynağın ve buna bağlı normalizasyonun birlikte etkisidir; sabit amaç katsayılı marjinal etki diye yorumlanmamalıdır. Diğer ham girdiler ve amaç modu sabittir.

Tuzluluk/kimya için sayısal model bağlantısı yoksa etki “bilinmiyor” kalır. Karasal su miktarı PWN tarafından ölçülmez. Deniz sıcaklığına bağlı mevcut arıtma alt hesabı saha araştırmasının tamamı değildir.

## Doğrulama

22 Eylül 2026: `tests/test_planning_objectives.py` içindeki altı test geçti. Testler talep miktarı değişse de kapasite sonucunun aynı kalmasını, dengeli tabanı, su/enerji amaçlarının anlamlı yöntem farkını, araştırma kaydına bağlı filtreyi, kapalı adayın sıfır kapasitesini ve hiçbir uygun seçeneği olmayan varsayılan Kuzeyin sahte geçerli plan üretmemesini kapsar. Genel entegrasyon ve son test sayısı için `BUILD_STATUS.md` esas alınır.
