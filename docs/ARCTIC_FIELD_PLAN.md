# Güncel ek · TESLİM021 · 23 Eylül 2026

Beş PC geliştirmesi uygulandı:2015–2025 ERA5 yakın dönem karşılaştırması,kaynaklı taze ürün/protein/besin enerjisi hedefleri,günlük sabit plan için döngüsel depo ve toplama stresleri,ayrıntılı enerji ve işletim güç taraması,numune/pilot kayıt ve karşılaştırma akışı. Güncel hesap,kaynak,sınır ve saha işleri [NORTH_PC_COMPLETION_021](NORTH_PC_COMPLETION_021.md) içinde; [doğrulama iş akışı](NORTH_VALIDATION_WORKFLOW.md) uygulanmıştır.

Önceki “güncel referans yok”,“yalnız kg amacı var” ve“hiç minimum depo hesaplanmıyor” ifadeleri eski sürüme aittir. Yeni depo hesabı ilk dolum hariç sabit üretimin döngüsel taramasıdır;LP'de depo yatırımı veya güç optimize edildiği anlamına gelmez. Yıllık enerji kısıtı LP'de,yeni kW beyanı ayrı taramadadır. Yakın ERA5/gelecek NASA farkı veri seti/hücre etkisini de içerir;aynı NASA tarihsel karşılaştırma korunur. Kaynaklı besin bileşimi dengeli diyet/kâr/talep değildir. Gerçek Arktik ölçümü veya pilot yapılmış sayılmaz.

Sunum gerekçesi:bilgisayarda planı ve test edilecek belirsizliği belirle;gerçek sefer zaman/konumundaki suyu modelle kıyaslamak ve kaynak suyunun kullanım/arıtma özelliklerini sınamak için izinli saha gözlemi ve numune topla;desteklenen girdiyi aynı motorda güncelle. Kara suyu,zemin ve enerji tahsisi ayrıca doğrulanır. Tek sefer tüm gelecek tarımını doğrulamaz.

---

Önceki geliştirme kayıtları aşağıdadır;021ekinin değiştirdiği ifadeler tarihsel kalır.

# Future North güncel uygulama · 23 Eylül 2026

Yeni north_field yolu ölçümden önce model beklentisi, su alma derinliği, üretim planı ve kod/veri özetlerini dondurur. POST eşleşmiş kaynak sıcaklığı/tuzluluğunu ve bunlardan türeyen RO elektrik/ısı/basınç uygulanabilirliğini günceller. Kara suyu, gelecek iklimi, ürün verimi veya zemin değişmez. Fiziksel bağlantı kaynaklı beyan ve uzman kontrolü ister; numune panel/sayı/derinliği henüz kesin değildir.

Yöntem, kaynak, varsayım ve sınırların güncel ortak kaydı: [FUTURE_NORTH_REBUILD](FUTURE_NORTH_REBUILD.md). Son doğrulama ve teslim: [BUILD_STATUS](BUILD_STATUS.md). Aşağıdaki eski Kuzey uygulama tarifleri kendi tarihleriyle tarihsel kayıttır; bu güncel akışın yerine geçmez. Türkiye ve PWN donanımına ait geçerli kaynak/test kayıtları korunur.

---

# Arktik saha planı — gemiden profil, numune ve model karşılaştırması

22 Eylül 2026 — FINAL MASTER SYNC. **Seçilme sonrası geliştirilip sefer ekibiyle kesinleştirilecek tasarım.** İstasyon, ekipman, CTD, analiz laboratuvarı veya danışman desteği sağlanmış değildir [E17](EVIDENCE_MAP.md).

## Araştırmanın sahadaki işi

İzinli istasyon fırsatlarında Arctic v1 ile iletkenlik, sıcaklık ve basınç profili; gemi/deck GPS ve UTC; uygun görülürse fiziksel numune alınması hedeflenir. İlk soru, modelin o zaman–konum–derinlikte verdiği su özellikleri ile gözlemin ne kadar örtüştüğüdür. İkinci soru, gözlenen farkın ilgili kaynak suyu/arıtma senaryosundaki belirsizliği veya seçeneği değiştirip değiştirmediğidir. Bu, ana üretim karar sisteminin saha katmanıdır [E13, E18–E19](EVIDENCE_MAP.md).

Seferin planlanan bağlamı Barents Denizi, Haziran–Eylül 2027 penceresinde yaklaşık 20–40 gün ve deniz üstü çalışmadır. Hava, deniz buzu ve lojistik rota/süreyi değiştirebilir. Profesyonel proje çağrısı bu operasyon bağlamı için kullanılır; tüm hükümleri öğrenci seçimine aktarılmaz [E07](EVIDENCE_MAP.md).

## Rota değişse de uygulanabilen tasarım

Sabit bir fiyort, kıyı tesisi veya kara erişimine bağlı değiliz. Sefer ekibinin uygun bulduğu mevcut çalışma fırsatları kullanılır; öğrenciler rota veya gemi operasyonunu belirlemez. Gözlenebilirse farklı su kolonu yapılarını karşılaştırmak isteriz: görece homojen su, belirgin geçiş/tabakalaşma ve bağlamın desteklediği freshwater etkisi adayları. Her türün bulunacağı garanti değildir; sınıflar profiller ve çevresel bağlamla kaydedilir [E07, E08, E16](EVIDENCE_MAP.md).

Kesin istasyon sayısı, maksimum derinlik, cast süresi, tekrar ve numune sayısı yoktur. Bunlar anlamlı bilimsel fark, kullanılabilir cihaz/örnekleyici ve sefer imkanlarıyla belirlenir. Deniz üzerinde erişilebilir bir istasyon tek başına kara su temini noktasını temsil etmez [E16, E19](EVIDENCE_MAP.md).

## Sefer öncesi hazırlanacak paket

| Paket | Somut hazırlık | Açık kalan seçim |
|---|---|---|
| Ölçüm | C/T/p sensör kimlikleri, kalibrasyon ve referans karşılaştırması; logger/saat kontrolü | Hata hedefi, cold-rating, çalışma derinliği |
| Gemi | Boyut, ağırlık, yük alma/geri alma bağlantısı, güç/bakım ihtiyacı | Sefer ekibinin uygun bulduğu operasyon |
| Veri | Kaynak/sürüm/indirme zamanı belli deniz modeli; çevrimdışı bağlam dosyaları | 2027'de erişilebilir analiz/tahmin ürününün kapsamı |
| Numune | Amaç–analiz–şişe–saklama–taşıma eşleşmesi ve örnek kimlikleri | Laboratuvar, panel, hacim, yöntem ve lojistik izin |
| Yedek | Yerel kayıt, güç, uygun servis parçaları, ikinci veri kopyası | Gerçek tüketim ve bakım yapılabilirliği |

Bu paket bir tasarım önerisidir; kaynak dayanakları [E07, E10, E13, E16, E18](EVIDENCE_MAP.md). Önceki Türk su kolonu/haloklin çalışmaları protokol sorularına yön verir; kendi hedef derinliğimizi onların yaptığı derinlikten kopyalamayız [E08](EVIDENCE_MAP.md).

## İzinli bir istasyonun çalışma akışı

1. **Fırsatı ve amacı kaydet:** istasyon kimliği, planlanan iş, gemi ekibinin uygun bulduğu derinlik/operasyon; mevcut hava/deniz bağlamı.
2. **Model kaydını ayır:** mevcutsa ölçümden önce erişilen analiz/tahmin dosyasını ürün/sürüm, üretim zamanı, geçerli zaman, indirme zamanı ve koordinatla sakla. Sonradan alınan reanalysis ayrı karşılaştırmadır; gelecekteki ölçüm anının tahminiymiş gibi sunulmaz.
3. **Cihazı kontrol et:** cihaz/kalibrasyon kimliği, C/T/p kanalları, yüzey basıncı, hafıza, güç, saat–UTC eşlemesi ve yük bağlantısı. Saat kontrolü için sefer öncesi/sonrası sapma notu tut.
4. **Profil al:** izinli cast boyunca yerel kayıt; iniş/çıkış ve operasyon duraklamaları işaretlenir. Gemi/deck konumu sualtı sensörünün kesin yatay konumu sayılmaz; bilinen farklar/notlar saklanır.
5. **Referansla eşleştir:** profesyonel CTD erişimi varsa uygun zaman/konum ve derinlik eşleşmesini kaydet. “Yakındaki CTD” otomatik aynı su paketi değildir; gecikme ve yatay ayrım görünür kalır.
6. **Geri al ve incele:** ham dosyayı değiştirmeden iki kopya sakla; eksik/sıfıra takılı/sıçrayan kanalları işaretle. Önce klasik gradient ve kalite kontrolüyle profil yorumla.
7. **İzinli fiziksel örnek:** geminin uygun gördüğü ayrı örnekleyiciyle, protokole göre standart ve gerekirse hedefli derinlikten al. Önerilen ile fiilen alınan derinlik ayrı kaydedilir; ikinci geçişte zaman/konum değişimi not edilir.
8. **İlişkiyi tamamla:** sample_id → cast_id → model_snapshot_id bağını kur; şişe/işlem/saklama ve laboratuvar zincirini kaydet. Sonucu henüz analiz yapılmadan kaynak kökeni veya kullanım uygunluğu diye yazma.

Bu operasyon adımları, çağrı bağlamında geliştirdiğimiz yöntem önerisidir [E07, E10, E13, E16, E18](EVIDENCE_MAP.md). Canlı internet, canlı sualtı haberleşmesi veya sürekli gemi elektriği şartı koymaz. Yalnız veri çekebilmiş olmak baseline'ın bağımsız olduğu anlamına gelmez; ürüne hangi gözlemlerin asimile edilmiş olabileceği değerlendirilir.

## Fiziksel numunenin iki ayrı amacı

**Kaynak karakterizasyonu:** δ18O ve δ2H güçlü adaylardır; analiz sonuçları uygun uç bileşen ve belirsizlik bağlamında değerlendirilir. Düşük tuzluluk ya da tek izotop sonucu “kesin buzul suyu” anlamına gelmez [E10](EVIDENCE_MAP.md).

**Kullanım/arıtma sorusu:** EC/tuzluluk, Na, Cl, Ca, Mg, bor ve alkalinite aday havuzudur. Yalnız incelenen üretim ve arıtma sorusuna değer katan analiz seçilir. Aynı şişe/koruma yöntemi bütün analizlere uygulanmaz; laboratuvarın deniz suyu kabulü ve protokolü kesinleştirilir [E06, E16](EVIDENCE_MAP.md).

## Bir şey çalışmazsa

| Durum | Gerçekçi devam yolu | İddia sınırı |
|---|---|---|
| Rota/istasyon uygun değil | Başka izinli fırsat; yoksa saha işi yapılmadı diye kayıt | Planlanan istasyonlar alınmış sayılmaz |
| PWN kanalı arızalı | Kalite işareti; ekipçe uygun görülen tamir/yedek; varsa izinli referans veri | Eksik C/T/p ile tam salinity/derinlik çıktısı üretilmez |
| Basınç kanalı yok | Profil durdurulur veya geçerli alternatif referansla sınırlı kayıt | Kablo uzunluğu gerçek deniz derinliği diye yazılmaz |
| Logger/güç sorunu | Kurtarılan ham veri ayrı korunur; uygun yedekle yeni cast | Veri boşluğu interpolasyonla gerçek gözlem gibi doldurulmaz |
| Referans CTD yok | Türkiye ön karşılaştırması ve saha kalite notları; mevcut profile sınırlı analiz | Arktik'te bağımsız CTD doğrulaması yapıldı denmez |
| Numune/laboratuvar mümkün değil | Fiziksel profil–model karşılaştırması devam edebilir | İzotop kaynak ayrımı/eksik kimyasal uygunluk sonucu yok |
| GPS/UTC eşlemesi eksik | Gemi kayıtlarıyla belgeli geri eşleme mümkünse yap; yoksa eşleşme sınırlı | Kesin eşzamanlı/eşkonumlu model karşılaştırması iddiası yok |
| İnternet veya güncel tahmin yok | Önceden arşivlenmiş bağlam; sonra erişilen model ayrı etiketlenir | Eski snapshot ölçüm anına geçerli tahmin diye gösterilmez |
| Sefer/deployment gerçekleşmez | Türkiye transferi ve tank deneyleri sürer | Arktik saha doğrulaması tamamlanmadı |

Yedekler araştırmayı mümkün olduğunca sürdürme planıdır; garanti değildir [E07, E16–E18](EVIDENCE_MAP.md).

## Dönüşte elimizde ne olacak?

Hedef: ham ve kalite işaretli profiller; cihaz/kalibrasyon ve GPS/UTC kayıtları; erişilebilmiş referans karşılaştırmaları; izinli fiziksel örnekler ve laboratuvar sonuçları; model snapshot'ları; model farkı ve ilgili karar senaryosundaki etkisi. Bunların henüz hiçbiri 2027 saha sonucu değildir [E17–E19](EVIDENCE_MAP.md).

PWN → model–gözlem değerlendirmesi → ilgili modelin güvenilirliği ve belirsizliği → karar desteği zinciri korunur. Uygun kıyısal kaynak için ayrıca PWN/numune → kaynak özellikleri → arıtma/koşullandırma → kullanılabilir su → enerji/su bütçesi → üretim seçeneği değerlendirilir. Kara hidrolojisi, ET, toprak ve mevsimsel su miktarı ayrı verilerden gelir. Kararın değişmemesi de geçerli bulgudur [E06, E18–E19](EVIDENCE_MAP.md).

İlgili belgeler: [Arctic v1 konsepti](PWN_ARCTIC_V1_CONCEPT.md), [doğrulama planı](PWN_VALIDATION_PLAN.md), [TASE uyumu](TASE_ALIGNMENT.md), [uzman görüşü gündemi](RESEARCHER_OUTREACH.md).
