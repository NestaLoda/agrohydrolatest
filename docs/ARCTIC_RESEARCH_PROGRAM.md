# Arktik araştırma programı

22 Eylül 2026 · U11. [Nihai sözleşme](FINAL_PRODUCT_CONTRACT.md) kapsamında araştırma tasarımıdır; sefer/laboratuvar onayı veya yapılmış saha sonucu değildir. Amaç **üretim kararını etkileyen belirsiz su sistemi bilgisini sahada sınamak**. TASE kapsamı yalnız arıtma sıcaklığına indirgenmez. Bugün çalışan sıcaklık–arıtma bağlantısı bunun dar bir yazılım gösterimidir.

## Araştırma soruları

| Soru | Test ve çıktı | TASE katkısı |
|---|---|---|
| RQ1: İklimce mümkün seçeneklerden hangileri su, zemin ve enerji kısıtları sonrası kalır? | Filtre öncesi/sonrası uygun seçenekler ve eleme gerekçesi. | Karasal iklim/hidroloji/zemin verisinin yerine geçmez. |
| RQ2: Açık planlama amacına hangi ürün–yöntem–kaynak deseni karşılık gelir? | Aynı kısıtlarla amaç alternatifleri, kapasite ve kaynak tahsisi. | Yalnız ilgili girdilere fiziksel kanıt ekler. |
| RQ3: Hangi belirsizlik kararı değiştirebilir? | Kaynaklı veya açık senaryo aralığında duyarlılık; desen, fizibilite ve kaynak değişimi. | Ölçülebilen değişkenleri önceliklendirmeye yardım eder. |
| RQ4: Gerçek gözlem model hatasını ve/veya kararı ne kadar değiştirir? | Eşlenmiş model–profil hatası; sabit hedef/kısıtlarla PRE/POST çözümü. | Programın doğrudan saha sorusu. |
| RQ5: Kontrollü üretimde gerçek su/enerji/verim modelle uyuşur mu? | Sefer sonrası pilotta öngörü–gerçekleşme farkı. | Numune karakterizasyonu başlangıç sağlar; gemide ürün deseni yetiştirilmez. |

Sorular hipotez/plan sınıfındadır. Karar duyarlılığı olasılıklı ekonomik bilgi değeri olarak adlandırılmaz; olasılık ve maliyet modeli yoksa “en değerli ölçüm” yerine “incelenen aralıkta kararı değiştiren ölçüm” denir.

## A — Su kolonu ve model karşılaştırması

İzinli her indirme öncesinde model sürümü, indirme zamanı, hücre/derinlik/zaman desteği ve değişken tanımı kaydedilir. Sonradan gözlemi asimile etmiş model sürümü bağımsız ön-tahmin diye kullanılmaz. PWN ile iletkenlik, sıcaklık, basınç/derinlik, UTC, konum, cihaz/kalibrasyon ve kalite kaydı hedeflenir. Referans CTD erişimi varsa aynı operasyonda karşılaştırılır; henüz erişim garantisi yoktur.

İlk çıktı profil eşleşmesi, sıcaklık/tuzluluk artıklarının işareti ve büyüklüğü, tabakalaşma/gradient konumu farkıdır. Sensör gecikmesi, iniş–çıkış farkı, model çözünürlüğü ve interpolasyon kaydedilir. Her profil noktası bağımsız tekrar sayılmaz. Hata/MAE/RMSE eşlenmiş geçerli çiftler üzerinde raporlanır; belirsizlik kalibrasyonu için çoklu bağımsız profil gerekir. **Modelle uyum da sonuçtur.**

[TEOS-10 GSW](https://teos-10.org/pubs/gsw/html/gsw_SP_from_C.html) C/T/p'den pratik tuzluluk dönüşümünün kapsamını tanımlar. Düşük maliyetli v0.1'in tank iletkenliği bilimsel CTD doğruluğu sayılmaz. [TOPAZ4 QUID](https://catalogue.marine.copernicus.eu/documents/QUID/CMEMS-ARC-QUID-002-003.pdf) günlük yüzey ve aylık 3B ürün farkını gösterir; aylık ortalama anlık profil değildir.

## B — Fiziksel numune ve kaynak karakterizasyonu

Önceden sabit metre listesi yerine operasyonun izin verdiği **standart derinlik + belirgin geçiş + arka plan** mantığı önerilir. Şişe örneği profil kimliği/UTC/konum/derinlikle bağlanır. Gerçek numune alma cihazı, gemi desteği, hacim ve taşıma zinciri KARE/TASE/laboratuvarla kesinleşir.

| Analiz adayı | Cevaplayacağı soru | Sınır |
|---|---|---|
| δ18O; ek değer varsa δ2H | Su kaynağı/karışım hipotezleri ayrılabiliyor mu? | Yerel uç bileşenler ve karışım modeli gerekir; iki izotop ölçmek tek başına kaynak yüzdesi vermez. |
| EC/tuzluluk, Na/Cl | Tuz yükü ve olası arıtma ihtiyacı nedir? | Ham deniz suyu sulama suyu kabul edilmez. |
| Ca/Mg/alkalinite; gerekliyse bor | Koşullandırma/besin hazırlığı veya proses için hangi kalite sınırlayıcı? | Her parametre yalnız belirlenmiş karar sorusuna hizmet ederse panele girer. |

[Yamamoto-Kawai vd. 2005](https://doi.org/10.1029/2004JC002793) izotop/alkaliniteyle Arktik freshwater araştırması için emsaldir; bizim panelimizin onayı değildir. [FAO su kalitesi rehberi](https://www.fao.org/4/T0234e/T0234E01.htm) tuzluluk ve özel iyon etkilerini ayırır. Laboratuvarın izotop, iyon ve büyüme deneyi için istediği numune hazırlıkları farklı olabilir: aynı korunmuş şişe tüm amaçlarda kullanılmaz. [IAEA örnekleme bölümü](https://gnssn.iaea.org/main/ncp/Tunisia/lrae/documents/tracers/Volume_I.pdf) analiz edecek laboratuvarın talimatını izlemeyi ve buharlaşma/izotop değişimini önlemeyi vurgular. Bu belge şişe hacmi, koruyucu veya sevkiyat protokolünü kilitlemez.

## C — Karara sağlanan bilgi

PRE-TASE çalışması girdileri, amacı, kısıtları ve sonuç kimliğiyle dondurulur. Gözlem doğrulandıktan sonra yalnız temsil ettiği değişken güncellenir ve **aynı motor** çalışır. Ürün miktarı/payları, yöntem, kaynak tahsisi, enerji, fizibilite ve bağlayıcı kısıt farkı gösterilir. Fark çıkması zorunlu değildir. Güven aralığı hesabı yoksa otomatik “güven arttı” denmez.

Bugünkü uygulama yolunda deniz sıcaklığı ilgili arıtma hesabına bağlanabilir. Tuzluluk ve kimya için yeni, doğrulanmış proses bağlantısı gerekir. Deniz profili yıllık karasal tahsisi, geleceğin havasını, ürün verimini veya toprağı güncellemez. Örnekleme yeri kıyısal alım noktasını temsil etmiyorsa arıtma senaryosuna aktarma **hipotezdir**. A paketi model karşılaştırması bu durumda da bilimsel çıktı üretebilir; karar bağlantısı varmış gibi zorlanmaz.

## İsteğe bağlı — gradient bilgisiyle örnekleme

A/B/C'yi aksatmıyorsa eşit küçük numune bütçesinde önceden belirlenmiş derinlikler ile gradient destekli seçim karşılaştırılır. Sınama çıktısı, referans profil/numunede geçişi yakalama veya yeniden kurma hatasıdır; yalnız daha ilginç görünen örneği seçmek başarı değildir. Aynı profil üzerinde çevrimdışı karşılaştırma ilk adım olabilir. Klasik gradient eşik yöntemi yeterlidir; öğrenilmiş yöntem ve bağımsız doğrulama yoksa AI üstünlüğü söylenmez.

## İlk fiziksel adım

Parçalar → tezgâh kontrolü → homojen su → tabakalı tank → UTC/derinlik/ham sinyalli gerçek CSV → importer → gerçek profil. Tank kaydı **KENDİ ÖLÇÜMÜMÜZ — KONTROLLÜ TANK DENEYİ** olur. Seçilme sonrası Arctic v1 için sensör hassasiyeti, soğuk/deniz dayanımı, gerçek basınç ve reference CTD planı uzmanla geliştirilir. Sefer sayısı/istasyon/derinlik/analiz paneli henüz onaylanmış değildir.
