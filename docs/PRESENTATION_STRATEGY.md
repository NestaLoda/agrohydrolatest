# Kısa mülakatın sunum ve gösterim planı

22 Eylül 2026 — U6 durum güncellemesi. FINAL MASTER SYNC §24–30,35–37,45–46 doğrultusunda öneri. Eski 36 slaytlık sunum geçmiş referans olarak kalır; bu mülakat için kısa anlatı ve az sayıda güçlü görsel kullanılacak. **İlk yeni yazılım kesiti ve kaynaklı veri paketi artık mevcut;** çalışmış fiziksel PWN, tank grafiği ve Arctic CAD henüz yok. Gösterilebilecek güncel yazılım kapsamı [BUILD_STATUS.md](BUILD_STATUS.md) üzerinden seçilir; aşağıdaki tam paket hâlâ teslim hedefidir.

## Beş dakikada aktarılacak resim

Konya'daki başarı, ekibin karar destek yaklaşımının başlangıç kanıtı. Türkiye aşaması aktarılabilirliğin sınanacağı köprü. Ana gelecek sorusu, kuzeye genişleyebilecek iklimsel uygunluğun su ve enerji koşullarında ne kadar uygulanabilir kaldığı. PWN, bu sistemin ilgili kaynak suyu bilgisini gerçek Arktik gözlemiyle sınama yolu. Kapanış Sustainable Production Frontier: hangi koşulda, neyin, nasıl üretilebileceği. [Master §4–14,26]

| Süre | Ağırlık | Bölüm | Jürinin anlaması gereken |
|---:|---:|---|---|
| 30 sn | %10 | Konya pilotu / geçmiş başarı | Daha önce karar destek yaklaşımıyla gerçek bir araştırma yapıldı |
| 30 sn | %10 | Türkiye transferi / yeni nesil | Yeni sistem sıfırdan kurulacak, tek bölgeye bağlılığı test edilecek |
| 60 sn | %20 | Kuzeye genişleyebilecek üretim | İklimsel uygunluk ile su/enerji açısından uygunluk aynı değil |
| 60 sn | %20 | Üretim sistemi deseni | Ürün + yöntem + kaynak + dönem birlikte seçiliyor |
| 90 sn | %30 | TASE-VII / PWN / fiziksel iş | Ne ölçülecek, nasıl karşılaştırılacak, hangi hesaba girecek |
| 30 sn | %10 | Kişisel süreklilik ve hedef | Ekibin gerçek katkıları, Ali Baha'nın kutup geçmişi, gelecek soru |

Toplam beş dakika. Bunlar konuşma kotası değil prova başlangıcı. Jüri araya girerse sıralamayı korumaya çalışmak yerine soruya cevap verin. On dakika verilirse ikinci beş dakikayı yeni slaytlarla doldurmak yerine soru ve gösterime bırakın. Kısa cevaplar [JURY_QA.md](JURY_QA.md), doğal metinler [INTERVIEW_STORY.md](INTERVIEW_STORY.md) içinde.

## Ana görseller ve işlevleri

**1. Tek geçiş görseli:** [PROJECT_EVOLUTION.svg](visuals/PROJECT_EVOLUTION.svg). Konya → Türkiye → kuzeye genişleyen uygunluk → su güvenliği → üretim sistemi deseni → Arktik gözlemi → kalibrasyon/AI → sürdürülebilir üretim sınırı. İlk bakışta üç büyük durak görünsün: geçmiş pilot, transfer, gelecek/saha. Alt katmanlar oklarla izlenebilsin. Bu, araştırmanın kavramsal akışıdır; bütün aşamaların tamamlandığı anlamına gelmez. Konya `tamamlanan pilot`, diğer uygulama aşamaları `planlanan` olarak ayrılmalı. [Master §27]

**2. Katman/filtre görseli:** [FRONTIER_FILTERS.svg](visuals/FRONTIER_FILTERS.svg). İklimsel uygunluk üzerine zemin, su, enerji ve üretim yöntemi koşulları gelir. Büyük mesaj: **“Yetişebilmesi, sürdürülebilir olduğu anlamına gelmez.”** Veriyle hesaplanmamışsa mutlaka `kavramsal şema — hesaplanmış harita değildir` yazılmalı. Rastgele çizilmiş kuzey alanları gerçek 2050 sonucu gibi sunulmaz. [Master §28; W1]

Bu iki görsel sync sırasında üretildi ve görsel olarak kontrol edildi. Slayta doğrudan eklemek için [evrim PNG](visuals/PROJECT_EVOLUTION.png) ve [filtre PNG](visuals/FRONTIER_FILTERS.png) hazır; SVG dosyaları düzenlenebilir sürümlerdir. Her biri 1920×1080; ana mesaj ve tamamlanma durumu görselin içinde yazılıdır.

Filtreler bütün yöntemlerde aynı davranmaz. Açık tarlada zemin veya don sınırı bir seçenek elerken kontrollü üretimde enerji/altyapı koşuluna dönüşebilir. Görsel bu nedenle “her katmanda her yerde aynı yüzdede alan kaybı” iddiası kurmaz. Gerçek model geldiğinde ürün, yöntem, senaryo ve dönem açık yazılır. [SCIENTIFIC_ARCHITECTURE; tasarım yorumu]

**3. Ölçümden karara bağlantı:** Bir model profili ve bir gerçek gözlem profili; ardından yalnız ilgili kaynak suyu girdisinin arıtma/enerji hesabına gidişi. Kendi PWN verisi henüz yoksa `planlanan karşılaştırma` şeması kullanılır. Gerçek tank verisi geldiğinde `kontrollü kolon — Arktik verisi değil` etiketi konur. Deniz profili ile karasal yıllık su bütçesi arasında doğrudan ok çizilmez. [Master §12–14,34]

**4. İki cihaz sürümü:** V0.1 fiziksel prototip/deney düzeneği ve Arctic v1 mühendislik konsepti yan yana. İlki gerçekten çalıştıktan sonra `çalışan PoC`; ikincisi `seçim sonrası geliştirilecek konsept`. Soğuk/basınç dayanımı, doğruluk veya derinlik denenmediyse görsele sayı olarak eklenmez. [Master §15–16,29]

## Masadaki gösterim sırası

1. Geçiş görselinde bugünkü araştırma sorusunu bir cümlede kurun.
2. Varsa çalışan tank prototipini ve kendi homojen/tabakalı profilini gösterin.
3. Grafikte eksen, birim veya bağıl sinyal, deney kimliği ve tekrarları işaretleyin. Referans yoksa doğruluk sayısı vermeyin.
4. Aynı prensibin deniz sürümünde neden gerçek basınç, soğuğa uygun sensör ve referans CTD gerektirdiğini konseptten anlatın.
5. Platform demosu gerçekten hazırsa, yalnız tek karar örneğinde hangi kaynak girdisinin hangi sonucu değiştirdiğini gösterin.

Canlı su kolonunun mülakat alanında kullanılabilirliği önceden ekip/organizasyonla teyit edilmeli. İzin veya fiziksel koşul uygun değilse kuru düzenek, kendi deney videosu ve ham kayıt kullanılabilir. Video yoksa varmış gibi vaat edilmez. [Öneri; PWN_SPEC_V0.1, DEMO_PLAN]

## Bugünkü durum ve mülakat hedefi

| Öğe | Bugün | Mülakata kadar hedef | Yetişmezse |
|---|---|---|---|
| Bilimsel mimari | Belgelenmiş tasarım | Tek soru ve açık ölçüm–karar bağı | Mevcut tasarım açıkça sunulur |
| Yeni platform | İlk çalışan yazılım kesiti ve kaynaklı veri mevcut; BUILD_STATUS kapsamıyla | Prova edilmiş dar karar gösterimi | Çalışan bölüm + etiketli kalan akış; bütün platform hazır denmez |
| Türkiye transferi | Yapılmış test yok | En az bir karşılaştırılabilir, kaynaklı aktarım örneği | Veri/benchmark planı; validasyon tamamlandı denmez |
| Kuzey analizi | Kaynaklı gerekçe var | Bir kaynaklandırılmış senaryo/uygunluk örneği | Yayının bulgusu kaynakla; ekibin hesapladığı harita gibi değil |
| PWN v0.1 | Donanım ve firmware yok | Çalışan düzenek, kontrol, tekrar, gerçek profil | Gerçek ilerleme ve eksik parça; sahte veri yok |
| Arctic v1 | Gereksinim belgesi var | CAD/BOM/operasyon konsepti | Blok şema ve gereksinimler; imalat tamamlandı denmez |
| Uzman görüşü | Görüşme yapılmadı | Gündem ve doğru araştırmacı eşleşmesi | Alınmamış görüş yazılmaz |
| Üç form | Hikâye çerçevesi | Gerçek kişisel bilgilerle bireysel cevaplar | Eksik kişisel bilgi ekipten alınır; deneyim uydurulmaz |

Bu tablo son prova ve form gönderimi öncesinde gerçek duruma göre güncellenir. Mülakat 30 Eylül 2026; formlar için 27 Eylül iç hedefi korunur. 48 saat önceki resmî son saatin kesin karşılığı teyit edilmeden saat uydurulmaz. [Master §35–37]

## Görsel tasarım dili

Sade açık zemin, koyu okunabilir metin ve az sayıda vurgu rengi yeterli. Harita veya grafikte aynı renk aynı anlamı taşısın; durum ayrımı yalnız renge dayanmasın. `Geçmiş sonuç`, `gözlem`, `model`, `gelecek senaryosu`, `konsept` yazılı etiketleri kullanılsın. Ölçülmemiş haritada parlak yeşil alanlar ve kesin sürdürülebilirlik yüzdeleri kullanılmasın. [Öneri; Master §30–31]

Her ekranda bir soru ve bir ana sonuç olsun. Uzun sensör listesi yerine çekirdek C/T/derinlik ve bunların ne işe yaradığı gösterilsin. Kaynak başlığı/yıl ve kısa dipnot ekranda okunabilsin; tam linkler [EVIDENCE_MAP.md](EVIDENCE_MAP.md) içinde kalsın. Eski 36 slayt gerektiğinde arşiv/ek kaynak; beş dakikalık anlatının ana akışı değil. [Master §26,45]

## Ekip ve anlatıcı geçişleri

Geçmiş rol dağılımı bilinmediği için “Cem donanımcı, Ferit veri uzmanı” gibi atamalar yapılmayacak. Her bölüm, o işi gerçekten yapan ve açıklayabilen öğrenciye verilir. Hepimiz aynı büyük resmi bilmeliyiz; özel soruyu bilen kişi devralır. Ali Baha'nın 2204-C geçmişi kendi ağzından kısa kişisel süreklilik olarak kullanılır. Derecenin ayrıntıları kullanıcı beyanını aşmaz. [Master §22–23; THREE_LETTERS_STORY]

Araştırmacı isimleri tek bir anlamlı cümlede geçsin: hangi çalışma, bize hangi soruyu düşündürdü? İncili/Dondurur/Biçer isimlerini sıralamak yerine profil, numune ve referans disiplinine bağlayın. Güncel görevler [RESEARCHER_OUTREACH.md](RESEARCHER_OUTREACH.md) üzerinden kontrol edilir; danışmanlık ilişkisi iddia edilmez. [W2,W3; Master §18–19]

## Kamuya dönük dürüst ifade

**Tek cümle:** Türkiye birincisi su yönetimi ekibi, gelecekte kuzeye genişleyebilecek üretim seçeneklerini su ve enerji koşullarıyla değerlendiren yeni sistemini, Arktik'te planladığı saha gözlemleriyle geliştirmeye hazırlanıyor.

**Bugün için olası haber çerçevesi:** “Lise öğrencileri, su yönetimi projelerinin Arktik saha gözlem modülünü tasarlıyor.” Çalışan cihaz ve gerçek deney tamamlanınca başlık buna göre güncellenebilir. Bugün “Arktik'in tarım haritasını çıkardılar” veya “kutup cihazını geliştirdiler” denmez. Haber değeri araştırmanın anlaşılabilirliğinden gelsin; yeni özellik ekleme gerekçesi olmasın. [Master §46; U1 başarı beyanı]

## Son prova

Bir kez süre tutarak, bir kez de jüri araya giriyormuş gibi prova yapın. Üç kişi şu dört soruyu aynı biçimde cevaplayabilsin: **Bugün ne hazır? Arktik'te hangi fiziksel veri alınacak? Bu veri hangi alt hesabı etkileyebilir? Model doğru çıkarsa veya cihaz çalışmazsa ne yapacağız?** Sonuçları önceden garanti etmeden somut bir iş tarif edebilmek, anlatının en güçlü tarafıdır.
