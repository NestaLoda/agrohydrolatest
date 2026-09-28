# Risk göstergeleri ve yeni bölgelere yaygınlaşma

22 Eylül 2026 · U8 uzun vadeli devam hattı. **Şimdiki çekirdek iş ürün deseni simülasyonudur.** Sigorta primi, poliçe, hasar tazmini veya aktüeryal fiyatlama modülü yapılmış değildir.

## Önce mevcut hesaptan çıkarılabilecek göstergeler

| Gösterge | Ne anlatır? | Ne anlatmaz? |
|---|---|---|
| Senaryo su açığı / su bütçesi boşluğu | Seçilen ürün deseninin tanımlı su koşulunu sağlaması | Gerçek kuraklık zarar olasılığı |
| Ürün başına minimum üretim açığı | Hangi ürün hedefinin hangi kısıt yüzünden karşılanamadığı | Gerçek hasat kaybı; doğrulanmış verim modeli olmadan tahmin değil |
| Enerji/su kaynağına bağımlılık | Seçeneklerin kaynak kesintisine veya bütçe değişimine duyarlılığı | Enerji kesintisinin olasılığı |
| Senaryolar arasında desen değişimi | Aynı hedefler altında planın ne kadar değiştiği | Senaryoların eşit olasılıklı olduğu varsayımı |
| Don/ısı ve veri eksikliği işaretleri | Belirlenen eşiklerin aşılması veya karar dayanağının eksikliği | Çeşitten bağımsız evrensel zarar katsayısı |

Bunlar ürün tasarımıdır; yalnız gerçekten hesaplanan göstergeler arayüze girer. Tek yıllık reanalizden veya tek iklim modelinden yüzde zarar/güven üretmeyiz. Daha sonra bağımsız yıl/işletme verisiyle gerçekleşen sonuç karşılaştırılır.

## Sigortayla olası bağ

TARSİM'in resmî **Köy Bazlı Verim Sigortası** açıklaması, belirli ürünlerde köy eşik verimi ile gerçekleşen verim üzerinden kurulan ayrı bir sistem tarif eder. Projemizin mevcut su açığı hesabı bu veri ve kuralların yerine geçmez; TARSİM ortaklığı veya onayı yoktur. [Resmî açıklama](https://www.tarsim.gov.tr/subPage/koy-bazli-verim-sigortasi)

Uzun vadeli araştırma sorusu: iklim/su göstergeleri, gerçek ürün kaybını açıklamada ve uyum seçeneklerini seçmede değer katıyor mu? Bunun için geçmiş verim ve hasar, yönetim/alan bilgisi, risk tanımı, bağımsız dönem ve aktüerya uzmanlığı gerekir. Bir bölgesel gösterge bireysel kayıpla örtüşmeyebilir; FAO'nun sigorta çerçevesi de tarihsel veri ve bu eşleşme sorununu ele alır. [FAO sigorta planlaması](https://www.fao.org/4/y5996e/y5996e05.htm), [indeks–kayıp farkı](https://www.fao.org/4/y5996e/y5996e03.htm)

İlk olası ürün, **risk azaltıcı üretim planı karşılaştırmasıdır**; prim önerisi değildir. Sigorta bağlantısı veri/uzman işbirliği gerçekleşirse ayrıca araştırılır.

## Kim kullanabilir, nasıl genişler?

Çiftçi/danışman mevcut deseni ve alternatif su koşulunu karşılaştırabilir; belediye veya kamu birimi farklı üretim hedeflerinin kaynak gereksinimini görebilir; araştırmacı aynı motoru yeni veriyle sınayabilir. Bunlar hedef kullanıcı gruplarıdır, edinilmiş müşteri listesi değildir.

Yeni bölge ekleme sırası: sınır ve yıl → gerçek ürün alanı/verimi → ürün/takvim → iklim ve su kaynağı → mevcut desenin yeniden hesabı → açık kullanıcı senaryosu → ayrı yıl/sahada kontrol. İl tablosu havza tablosu diye yeniden adlandırılmaz; çok yıllık bahçe alanı tek dönemde boş tarla gibi dönüştürülmez. Mevcut beş Türkiye bölgesi bu aktarım yolunun ilk örnekleridir; ülke çapında doğrulama değildir. [Veri gereksinimleri](DATA_REQUIREMENTS.md), [ürün bilgisi](../data/agriculture/crops.json)
