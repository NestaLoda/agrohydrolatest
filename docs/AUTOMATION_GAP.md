# Güncel rebuild kaydı · 22 Eylül 2026

U12 production_input_applied=false ifadesi bağımsız iklim analizinin tarihsel kapsamını anlatır. Yeni simulate.input_resolution.production_input_applied=true yalnız olumsuz açık tarla aday elemesi kapsamında geçerlidir. Otomatik iklim API analizi kendi başına tam üretim girdisi uygulamaz. Yerel verim/su/zemin/sera enerjisi hâlâ eksik; tam otomasyon tamamlandı denmez.

Bağlayıcı sözleşme: [REBUILD_CONTRACT.md](REBUILD_CONTRACT.md). Çalışan/eksik ayrımı: [REBUILD_EVIDENCE_AUDIT.md](REBUILD_EVIDENCE_AUDIT.md), [BUILD_STATUS.md](BUILD_STATUS.md).

---

## Önceki ayrıntılı kayıt (tarihsel uygulama durumları kendi tarihleriyle okunur)

# Otomasyon açığı ve kullanıcı düzeltmesi · U12

22 Eylül 2026. Kullanıcı referansı: ChatGPT “2204D TO KUUTP”, conversationId 6aae8ac9-0564-83eb-b424-f79823c603df. İlgili son kullanıcı mesajları ve önceki ürün düzeltmeleri okundu. Eski asistan önerileri yeni talimat sayılmadı.

## Asıl beklenti

Bölge/dönem seçilir → sistem kaynakları birleştirir → bilimsel girdileri türetir → üretim desenini hesaplar. Kullanıcı isterse koşulları değiştirir. Kullanıcıdan modelin bilimsel cevaplarını doldurması beklenmez.

## Önceki teslimin eksikliği

0.5'te beş amaç ve duyarlılık çalışıyor olsa da Kuzeyde iklim seçimi çoğunlukla provenans/ekran bağlamıydı. planning_context kuzey yield/su/enerji katsayılarını null bırakıyor, crop_water manuel olmayan Kuzey sulamasını reddediyordu. Kaynaklı veri otomatik çözümlenmeden kullanıcı örnek senaryo veya elle veri girişine yöneliyordu. Arayüz/test başarısı tam otomatik gelecek tarım modeli anlamına gelmiyordu. Kullanıcının itirazı yalnız renk/yerleşim değil, bu hesap akışı eksikliğidir.

## Bu düzeltmede çalışanlar

- Türkiye bölgesi yüklenince mevcut kaynak başlangıcı ve ilk optimizasyon otomatik çalışır. Kullanıcı bir alan doldurmak zorunda değildir; sonraki senaryo değişikliği Hesapla ile değerlendirilir.
- Kuzey seçilen EC-Earth veya NASA günlük serisinden otomatik yeniden analiz edilir. Aylık/yıllık iklim, GDD5, tarihli donsuz pencere, kaynak sıcaklık zarfıyla araştırma ön taraması ve Hargreaves ET0 vekili türetilir. Dönem/SSP değişimi yalnız etiketi değiştirmez, bu hesapları değiştirir.
- Kuzey adayları kaynak durumu ile gösterilir; bilimsel elle girişler gelişmişte. Açıklayıcı veri seti otomatik kaynakmış gibi yüklenmez; mühendislik deneyi altında kalır.
- Tam üretim deseni hesaplanamıyorsa boş formu zorunlu veri girişi gibi öne koymak yerine nedenini sistem açıklar.

## Henüz bitmeyen gerçek iş

Yeni otomatik analiz doğrudan tam Kuzey üretim optimizasyonuna dönüşmüş değildir. production_input_applied=false bunu API'de de belirtir. Su arzı, zemin, yerel yield, kar-su dengesi ve kontrollü ortam enerjisi bağlantıları hâlâ eksiktir. Bunların yerine resmî gibi görünen bütçe veya onay kutusu doldurulmayacaktır.

Sonraki veri/model işi: uygun saha ve zaman ölçeğinde yerel üretim katsayılarını ve hidrololojik/altyapısal arzı kaynaklardan çözümlemek; analiz çıktısını alan bazında kanıt taşıyan motor girdisine çevirmek. Kaynak bulunamayan parametre için koşullu kaynak gereksinimi hesaplanabilir; tam yerel öneri denemez. Bu yazı tamamlanma vaadi veya otomatik veri indirme yapıldı iddiası değildir.

Kaynaklar: [sayısal yöntem/parametre incelemesi](AUTO_BASELINE_EVIDENCE.md), [parametreler](../data/auto_baseline_parameters.json), [otomatik analiz](../backend/automatic_baseline.py), [ana sözleşme](FINAL_PRODUCT_CONTRACT.md).
