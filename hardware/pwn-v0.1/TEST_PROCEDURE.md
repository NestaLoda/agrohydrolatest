# PWN v0.1 test sırası

Bu protokol [onaylı doğrulama planının](../../docs/PWN_VALIDATION_PLAN.md) öğretmenle uygulanacak kısa sürümüdür. Henüz deney sonucu değildir. Yapılan her iş gerçek kayıtla tamamlandı sayılır; önerilen tekrar sayıları hassasiyet garantisi değildir [E13/E16/E17](../../docs/EVIDENCE_MAP.md).

## 1. Kuru masa

- Kart/firmware/pin ve cihaz kimliğini yaz. UTC senkron değilse elapsed_ms kullan; saat uydurma.
- Sıcaklık, encoder, SD/yerel dosya ve seri görünümü tek tek dene.
- Encoder'ı cetvelle bilinen birkaç mesafede kontrol et; iniş yönü ve yüzey sıfırını kaydet.
- EC ön devresini öğretmen kontrol etsin; ADC uca yapışıyorsa su deneyiyle devam etme.
- Kaydı kapat, dosyayı yeniden aç; header ve eksik değerlerin boş kaldığını doğrula.

## 2. Çözelti ve referans

Aynı sıcaklığa yakın en az iki farklı çözelti hazırla; tarif, su/tuz türü, zaman ve sıcaklığı kaydet. Sensör aralığını aşma. Varsa EC metre/standart kimliğini ve bağımsız termometreyi kaydet. Tuz kütlesi EC standardı değildir. Kalibrasyona kullanılan çözeltilerden ayrı kontrol çözeltileriyle sınama yapılabiliyorsa ekle; yapılamadıysa bunu yaz.

## 3. Kolon deneyleri

| ID | Hazırlık | İşlem | Kaydedilecek sonuç |
|---|---|---|---|
| H | Homojen çözelti, benzer sıcaklık | Yüzeyden yavaş iniş; çıkış ayrı işaretli | Ham C/T, mesafe; sahte alarm |
| S | Daha yoğun çözelti alt, seyreltilmiş üst; üstü yavaş ekle | Hazırlama/başlangıç zamanı; aynı iniş düzeni | Belirgin geçiş yakalandı/kaçtı |
| W | Daha küçük iletkenlik farkı | S çalışınca aynı akış | Geçiş ve gürültü; farkın referansı varsa yaz |
| T | Aynı ana çözeltiden alınan iki bölüm, farklı sıcaklık | Gerçek T profilini kaydet; karışma/konveksiyonu izle | Sıcaklık farkının yanlış tabaka yorumuna etkisi |
| R | H/S tekrarları | Başlangıç için üçer kayıt; yeniden hazırlama durumunu yaz | Aynı eksende tekrarlar; geçiş dağılımı |

Her cast sonrası kolonun bozulduğunu düşün; sıralı geçişleri bağımsız yeni hazırlanmış deney gibi sayma. İniş ve çıkış aynı deneyin parçalarıdır. H/S ve gerçek dosya ilk öncelik; W/T çekirdek çalıştıktan sonra. [Mekanik düzen](MECHANICAL_BRIEF.md).

## 4. Hata ve tekrar

Encoder mesafe hatası için bağımsız cetvel kullanılabilir. **Tabaka sınırı hatası** için aynı zaman/kolona ait bağımsız EC derinlik referansı veya belgelenmiş referans aralığı gerekir. Yalnız boya çizgisi, doldurma yüksekliği veya algoritmanın kendi sonucu referans değildir. Referans yoksa bulunan sınır ve tekrarlar raporlanır; “±X cm doğruluk” yazılmaz.

EC/temperature RMSE veya bias yalnız uygun bağımsız referans varsa; repeatability yalnız tekrar varsa; yanlış alarm yalnız homojen kontrol varsa verilir. Bütün grafiklerin altında gerçek deney kimliği bulunur. Ham veri üzerine düzeltme yazılmaz; analiz ayrı çıktıdır [DATA_SCHEMA.md](DATA_SCHEMA.md).

## 5. Son küçük paket

Bir H profili + bir S profili + tekrar grafiği + ham CSV/manifest + kısa video/fotoğraf + “ne gösterdik/ne henüz ölçülmedi” notu. Başarısız denemeleri silme. Canlı demo olmazsa bu gerçek kayıtlar kullanılır; kayıt yoksa sadece tasarım gösterilir. Seri bilgisayar kaydı kullanıldıysa bağımsız SD logger tamamlandı denmez.
