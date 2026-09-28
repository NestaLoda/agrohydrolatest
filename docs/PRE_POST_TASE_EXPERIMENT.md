> U11 güncel bağlam: [FINAL_PRODUCT_CONTRACT](FINAL_PRODUCT_CONTRACT.md), [FUTURE_NORTH_DECISION_MODEL](FUTURE_NORTH_DECISION_MODEL.md) ve [ARCTIC_RESEARCH_PROGRAM](ARCTIC_RESEARCH_PROGRAM.md) geçerlidir. Aşağıdaki bilimsel ayrıntılar korunur; eski UI adları güncel arayüz gereği değildir. Saha araştırması yalnız sıcaklık/arıtma hesabından ibaret değildir: A profil, B numune, C karar bilgisi birlikte planlanır.

# PRE-TASE / gözlem sonrası deney — TESLİM 004

22 Eylül 2026. Amaç: gözlemin desteklediği bir girdiyi değiştirip **aynı optimizasyon motoruyla** üretim desenine etkisini göstermek. Desenin değişmesi deneyin başarı koşulu değildir.

## Çalışan arayüz protokolü

1. GELECEK / KUZEY laboratuvarında ürünler, yöntemler, hedefler, kapasiteler ve bütçeler seçilir. Varsayıma dayalı örnek portföy açıkça etiketlenir.
2. SAHA / PWN panelinde model/varsayım su sıcaklığı ve eşleştirme noktası tanımlanır. Kaynak URL'si gerçek dış gözlem yolu için gerekir. Otomatik okyanus profili henüz yüklü değildir.
3. **PRE-TASE desenini kaydet**: `/api/simulate` ile hesaplanır. Tam senaryo, model noktası, model URL'si, UTC kayıt tarihi, sonuç ve deterministik `run_id` birlikte saklanır. JSON indirme vardır.
4. Senaryo/model noktası sonradan değişirse eski kayıt kendiliğinden değişmez. Uyarı gösterilir ve karşılaştırmadan önce yeniden kayıt gerekir.
5. Açıklayıcı gözlem senaryosu veya kayıtlı dış gözlem seçilir. Dış gözlemde sıcaklık/metaveri sunucudaki kayıtlı kaynaktan gelir; arayüzde yazılan sıcaklık gerçek gözlem yerine geçirilmez.
6. **Eşleştir ve deseni yeniden hesapla**: dondurulan senaryo gönderilir. Sunucu aynı motorla önceki hesabı tekrar üretir. Arayüz önceki `run_id` ile kaydedilen kimlik eşleşmezse sonucu kabul etmez; yeni kayıt ister.
7. Uygun eşleştirmede yalnız deniz kaynak suyu sıcaklığı değişir. Eşleştirme geçmezse `after = null`; saha sonrası optimizasyon yapılmaz.
8. Ürün alan/pay/üretim, yöntem–kaynak tahsisi, su, enerji, uygulanabilirlik ve bağlayıcı kısıtlar karşılaştırılır. Ha ve kontrollü yetiştirme m² birleştirilmez.

PRE-TASE kayıt kopyası tarayıcı `sessionStorage` içinde çalışma alanı geçişlerinde korunur. Bu bir çok kullanıcılı/sunucuda adlandırılmış proje kayıt sistemi değildir. Kalıcı taşınabilir teslim için JSON indirilmelidir. Motor çalışmaları mevcut SQLite provenance kaydında tutulur. Tarayıcı kapanması veya depolamanın temizlenmesi arayüzdeki snapshot'ı silebilir.

## Değiştirilen ve sabit tutulanlar

| Sınıf | Girdiler |
|---|---|
| Bugün gözlemle güncellenebilir | `seawater_temperature_c` → mevcut arıtma enerji senaryosu |
| Sabit | Ürün listesi, hedef/minimum üretim, öncelik, yöntem seçenekleri, alan, sera/hidroponik kapasite, verim, sulama parametreleri, su kaynağı kapasiteleri, enerji bütçesi |
| Henüz bağlı değil | Tuzluluk/EC, iyonlar, bor, alkalinite, izotoplar, gerçek basınç profili üzerinden yeni arıtma veya üretim hesabı |
| Bu gözlemin ölçmediği | Karasal yıllık tatlı su hacmi, depolama kapasitesi, yerel tarımsal su tahsisi |

Ölçüm kalitesi, zaman/konum/derinlik eşleşmesi ve kaynak temsil bağı gereklidir. Noktasal eşleşme, örneğin gelecek on yılların besleme suyu dağılımını doğruladığı anlamına gelmez.

## Geçerli sonuçlar

- Aynı ürün ve tahsis: anlamlı karar etkisi yok.
- Aynı ürün, farklı kaynak/yöntem tahsisi.
- Farklı alan veya üretim.
- Enerji sınırı nedeniyle önceki çözüm uygulanamaz.
- Eşleşmeyen gözlem: güncelleme yapılmaz.

“Aynı desen, daha yüksek güven” kavramsal olarak ileride mümkündür; bugünkü arayüz sayısal güven artışı hesaplamaz. Eşleşmiş tek bir gözlem otomatik kalibrasyon veya doğrulama değildir. Arayüz bu nedenle önceki ve sonraki kanıt türlerini bildirir; sahte güven puanı üretmez.

## Bir dakikalık açıklayıcı gösterim

Varsayımsal uygun saha portföyünü yükle → PRE-TASE sıcaklığını 10 °C ile kaydet → örnek gözlemi 5 °C yap → aynı motoru çalıştır. Mevcut örnek bütçede sıcaklığa bağlı enerji değişimi çözümü uygulanamaz hale getirebilir. Bu bir **simülasyon etkisi**dir; gerçek Arktik öneri veya gerçekleşmiş TASE sonucu değildir. Ardından 24 saat zaman kaydırmasını etkinleştir: eşleştirme geçmeyince saha sonrası sonuç üretilemediğini göster.

## Test izi ve kapsam

Mevcut `tests/test_planning.py` aynı motorun iki kez çalışmasını, yalnız sıcaklık güncellemesini ve geçersiz eşleştirmede `after = null` davranışını kapsar. Snapshot kaydı, kaydın korunması, girdi değişim uyarısı ve kimlik kontrolü yeni arayüz davranışıdır. Bu belgenin yazılması testlerin yeniden geçtiği iddiası değildir; son doğrulama zamanı ve sonuçları `BUILD_STATUS.md` ile `docs/verification/` altında kaydedilir.

Kaynaklar: U9 kullanıcı talimatı; `frontend/src/workspaces/PatternField.tsx`, `backend/app.py` (`recorded_simulation`, `pattern_field_update`), `backend/planning.py`, `tests/test_planning.py`. Dış bilimsel kaynakların envanteri `ARCTIC_DECISION_LOGIC.md` ve ilgili veri belgeleriyle birlikte değerlendirilir.
