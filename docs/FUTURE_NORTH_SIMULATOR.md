# Gelecek kuzey üretim sistemi simülatörü

22 Eylül 2026 · U8 / TESLİM 003. Türkiye ile aynı [ürün deseni motoru](CROP_PATTERN_ENGINE.md) çalışır; mevcut tarım deseni bulunmayan kuzey bağlamında başlangıç, aday ürünler ve dönemsel kapasitelerdir.

## Ne hesaplanıyor?

İlk portföy **arpa + patates + marul**; seçimin birincil kaynakları ve coğrafi sınırları [FUTURE_NORTH_CROP_SET.md](FUTURE_NORTH_CROP_SET.md) içindedir. Arpa/patates açık tarla, marul hidroponik ilk örnektir. Uygun katalog ve açık katsayılarla sera da motorun ayrı kapasite seçeneğidir. Otlar, mikro filizler ve dikey kat sayıları hazırmış gibi eklenmedi.

Kullanıcı aday ürünleri, üretim hedef/minimumlarını, tarla alanını, sera/hidroponik yüzeyini, su kaynaklarını ve kullanılabilir hacimlerini, enerji bütçesini, net sulamayı, verim/kaynak katsayılarını, uygunluk varsayımlarını ve dönem etiketini düzenleyebilir. Çıktı dört katmandır: **ürün katkıları → yöntem/kapasite → kaynak suyu tahsisi → dönem**. Hektar ve hidroponik m² ortak sahte yüzdeye toplanmaz.

## Veri ile varsayım ayrımı

Longyearbyen bağlamında mevcut dış model paketi tek EC_Earth3P_HR modelinin **1995–2014 ve 2030–2049** dönemleridir. GDD5, don olmayan dönem ve yağış göstergesi verir; seçilebilir SSP ensemble'ı, gelecek ET₀ veya deniz suyu sıcaklığı sağlamaz. Dönem etiketini değiştirmek yeni iklim verisi indirmez. [NORTH_DATA_PLAN.md](NORTH_DATA_PLAN.md)

Güvenli başlangıçta açık tarla iklim/zemin uygunluğu **bilinmiyor**dur; pozitif arpa/patates minimumlarıyla geçerli plan çıkmaz. “Uygun saha varsayımı” örneği bunu açıkça `USER_SCENARIO` olarak değiştirir. Bu ayrım Longyearbyen'de tarla uygunluğu kanıtlamadan hesap mantığını göstermeyi sağlar.

## Hesaplanmış örnek — ölçüm değil

22 Eylül 2026'da `planning_context('longyearbyen')['illustrative_scenario']` aynı motorla çalıştırıldı. Örnek tek üretim dönemidir; başlangıç **1 Mayıs 2035**, aşama süreleri başka bölgeler için verilen FAO örneğinden gelir. Arpa 135, patates 130, marul 75 gün takvim etiketi yerel fenoloji kanıtı değildir; özellikle hidroponik döngü ayrıca doğrulanacaktır.

| Girdi | Açık kullanıcı senaryosu |
|---|---|
| Açık alan / hidroponik yüzey sınırı | 3 ha / 400 m² |
| Üretim minimumu = hedef | Arpa 3.000 kg; patates 10.000 kg; marul 1.000 kg |
| Verim | Arpa 3.000 kg/ha; patates 20.000 kg/ha; marul 3 kg/m²/dönem |
| Su | Arpa 150, patates 250 mm net; randıman %75; marul 0,02 m³/kg |
| Enerji | Açık alan 500 kWh/ha; marul 25 kWh/kg; toplam bütçe 40.000 kWh |
| Kullanılabilir kaynak kapasitesi | Tatlı su 2.000; depolanmış su 500; arıtılmış deniz suyu 2.000 m³ |
| Kaynak suyu sıcaklığı | 10°C; arıtma ilişkisi kaynak aralığında |

**Hesaplanan desen:** arpa **1 ha / 3.000 kg**, patates **0,5 ha / 10.000 kg**, hidroponik marul **333,33 m² / 1.000 kg**. Toplam kullanım **3.686,67 m³**, enerji **38.084,49 kWh**. Kaynak tahsisi: tatlı su **2.000 m³ (%54,25)**, depolanmış su **500 m³ (%13,56)**, arıtılmış deniz suyu **1.186,67 m³ (%32,19)**. Yeniden kullanım kapalıdır; açık arazinin **1,5 ha** kısmı tahsis edilmez. Su yüzdelerinin paydası kullanılan toplam m³'tür.

Buradaki arıtılmış kaynak hacmi kullanıma sunulan ürün suyu kapasitesidir; gerçek deniz çekimi veya konsantre yönetimi hesabı değildir. Arıtma enerji ilişkisi ve coğrafi aktarım sınırı mevcut [MODEL_METHODS.md](MODEL_METHODS.md) kaydında korunur. Yerel tatlı su ve depo enerji katsayısının sıfır girilmesi ölçülmüş sıfır pompaj demek değildir.

Aynı hedefler ve 40.000 kWh bütçesi korunarak yalnız kaynak sıcaklığı **5°C** yapılınca bu örnek **uygulanamaz** olur. Bu, seçilmiş katsayıların duyarlılık sonucudur; TASE'den alınmış veri veya kesin Arktik üretim önerisi değildir. Güncelleme yolu [FIELD_TO_PATTERN_UPDATE.md](FIELD_TO_PATTERN_UPDATE.md).

## Sonraki gerçek veri işi

Yerel çeşit/takvim ve verim, gelecek ET₀/kar-akış/depo, fiziksel arazi/permafrost, gerçek enerji arzı ve sera ısıtma/aydınlatma bütçesi gerekir. Mevcut çıktı bu açıkları görünür kılan çalışır koşullu planlama hesabıdır; hesaplanmış coğrafi sürdürülebilir üretim sınırı haritası değildir.
