# PWN doğrulama planı — prensipten Arktik ölçümüne

22 Eylül 2026 — U6 durum güncellemesi. **Bu belge fiziksel test planıdır; tank/saha sonucu içermez.** V0.1 kontrollü kolon PoC'si, Arctic v1 ayrı mühendislik ve saha geliştirmesidir. Yazılım/firmware geliştirmesi U6 ile onaylandı; parser/gradient yazılım testleri fiziksel doğrulama sayılmaz. Güncel iş ve test durumu [BUILD_STATUS.md](BUILD_STATUS.md) içindedir [E13, E16–E17](EVIDENCE_MAP.md).

## Mülakat öncesindeki basit hedef

Gerçek sinyalin derinlikle kaydedildiğini, homojen su ile tabakalı kolonun ayırt edilebildiğini ve tekrar profillerinin nasıl davrandığını gösterelim. Baştan uydurulmuş hassasiyet eşiği yerine ne ölçtüğümüzü ve referansın ne olduğunu yazalım. Sensörün aynı sonucu tekrarlaması, sonucun doğru olduğunun tek başına kanıtı değildir [E13, E16](EVIDENCE_MAP.md).

## İlk kurulum ve referanslar

| Kanal | Basit kontrol | Kayda yazılacak |
|---|---|---|
| İletkenlik | Farklı çözeltilerde kararlı sinyal; varsa bilinen standartlar ve bağımsız EC metre | Ham sinyal birimi, standart/cihaz kimliği, çözelti sıcaklığı, kullanılan dönüşüm |
| Sıcaklık | Varsa referans termometreyle aynı kaptaki değerler; dengeye ulaşma süresi | Prob/referans kimliği ve sapma; tepki gecikmesi |
| Encoder/derinlik | Cetvelle bilinen birkaç konumda ölçüm; sıfır ve iniş/çıkış kontrolü | Sayım–mesafe ilişkisi, kayma, yüzey/prob offset'i |
| Kayıt | Deneme kaydı aç/kapat, dosyayı geri aç; güç/kablo bağlantısını kontrol et | Beklenen/gerçek kayıt, zaman, eksik veri, yeniden başlama |
| Mekanik | Kuru elektronik, ayrı taşıyıcı ip, sabit sensör geometrisi | Montaj fotoğrafı, iniş yöntemi, kolon boyutu |

Bu kontroller [PWN_SPEC_V0.1.md](PWN_SPEC_V0.1.md) ihtiyaç listesiyle yapılır. Referans EC yoksa `ham/bağıl iletkenlik sinyali` raporlanır; EC veya salinity doğruluğu yazılmaz. Kalibrasyonda kullanılan noktalar tek başına bağımsız doğruluk testi sayılmaz [E13, E16](EVIDENCE_MAP.md).

## Kontrollü su kolonu deneyi

İlk tabakalı deneyde benzer sıcaklıkta daha yoğun/tuzlu çözelti altta, seyreltilmiş çözelti üstte olacak. Üst çözelti karıştırmadan yavaş eklenir. Sensör/EC modülünün aralığına uygun çözeltiler seçilir; tatlı su–deniz suyu uçlarını kullanmak zorunlu değildir. Her cast tabakayı bozabileceğinden hazırlama, bekleme, profil sırası ve yeniden kurulum kaydedilir [E16](EVIDENCE_MAP.md).

| Deney | Soru | Gösterilecek çıktı | Öncelik |
|---|---|---|---|
| Homojen, benzer sıcaklıklı su | Sistem olmayan bir tabakaya alarm veriyor mu? | Gerçek profil; yanlış alarm var/yok ve sayısı | Çekirdek |
| Güçlü iletkenlik tabakalaşması | Belirgin geçişi yakalıyor mu? | Ham ve işlenmiş profil; bulunan geçiş aralığı | Çekirdek |
| Daha zayıf tabakalaşma | Fark küçülünce ne değişiyor? | Yakalanan/kaçırılan geçiş; sinyal kararlılığı | Çekirdek çalışınca |
| Aynı çözelti, farklı sıcaklık | Sıcaklık etkisi iletkenlik katmanı diye yanlış yorumlanıyor mu? | C/T profilleri birlikte; sıcaklığa bağlı alarm yorumu | Çekirdek çalışınca |
| Tekrar cast'leri | Sonuç ne kadar tekrarlanıyor; düzenek bozuluyor mu? | Aynı eksende tekrarlar; geçiş konumu dağılımı | Çekirdek deneylerle |

Başlangıçta çekirdek koşulları üçer kez denemek pratik bir öneridir, istatistiksel yeterlilik şartı değildir. Sıcaklık kontrolü tabakası konveksiyonla değişebileceğinden gerçekten oluşan T profili gösterilir; “başlangıçta aynı tuz” bilgisi sonradan sabit fiziksel koşul varsayımına dönüştürülmez. Negatif kontrol başarısızsa sonuç saklanmaz, sıcaklık ayrıştırması sınırlı denir [E16](EVIDENCE_MAP.md).

## Hangi sayıyı ne zaman yazabiliriz?

| Sonuç | Gerekli dayanak | Dayanak yoksa |
|---|---|---|
| Encoder derinlik hatası | Bağımsız cetvel konumu ve aynı referans noktası | Yalnız sayım/mesafe ve kontrol durumu |
| Geçiş sınırı hatası | Aynı zamana yakın bağımsız EC derinlik profili veya belgeli referans geçiş aralığı | “Bulunan geçiş konumu”; hata veya santimetre doğruluk iddiası yok |
| Tekrarlanabilirlik | Aynı koşul/yeniden hazırlama kaydı ve tekrarlı cast | Tek cast için tekrarlanabilirlik iddiası yok |
| EC/sıcaklık sapması | Uygun referans cihaz/standart ve ayrı kontrol noktaları | Ham sinyal veya gösterge değer |
| Yanlış alarm | Homojen kontrol ve önceden tanımlı alarm kuralı | Sadece seçilmiş güzel grafikten false-positive sonucu yok |
| Algılama oranı | Hangi gerçek deneylerin geçiş içerdiği, kural ve deney sayısı açık | Az sayıda deney için tek tek yakaladı/kaçırdı kaydı |

Bağımsız sınır `z_ref` ile tespit `z_detected` karşılaştırılabiliyorsa mutlak fark raporlanabilir; referansın belirsizliği de yazılır. Boya çizgisi veya doldurulan su yüksekliği, dinamik iletkenlik geçişinin otomatik doğruluk referansı değildir. Tekrarların birbirine yakınlığı **repeatability** olarak ayrı verilir; bağımsız doğruluk yerine konulmaz [E13, E16](EVIDENCE_MAP.md).

## Analiz ve veri kaydı

Önce basit gradient/eşik yöntemi kullanılır. Ham veriyi sakla; yumuşatma ve eşik seçimini yaz; yalnız başarılı denemeleri ayıklama. Kalibrasyon ve son testler aynı veriyle karıştırılmasın. AI ancak yeterli veri ve klasik yöntemle anlamlı karşılaştırma olursa eklenir [E11, E16, E19](EVIDENCE_MAP.md).

Asgari kayıt: deney/cast kimliği, tarih ve geçen süre, sensör/kalibrasyon kimliği, ham iletkenlik, sıcaklık, encoder/manuel derinlik kaynağı, iniş/çıkış, çözelti hazırlığı, referans, kalite notu ve uygulanan analiz. Türetilmiş EC/derinlik ayrı sütunlarda tutulur. Tank verisine Arktik koordinatı atanmaz [E16, E18](EVIDENCE_MAP.md).

Her deneyden ham dosya, bir profil grafiği, kısa kurulum fotoğrafı ve bir sonuç cümlesi yeterli başlangıç paketidir. Örnek sonuç şablonu: “Bu koşulda geçiş [bulundu/bulunmadı]; [sayı] tekrarın grafikleri ektedir; bağımsız sınır referansı [var/yok].” Köşeli alanlar yalnız gerçek kayıttan doldurulur [E17](EVIDENCE_MAP.md).

## Seçilme sonrası Arctic v1 doğrulaması

1. Uzmanla hedef anlamlı değişimi, soğuk aralığı, çalışma derinliği ve operasyon biçimini belirle.
2. C/T/p kanallarını uygun standartlar ve profesyonel/reference CTD ile karşılaştır; bias, hata, tepki süresi ve drift'i gerçek veriden çıkar.
3. Uygun atölye/laboratuvar düzeninde sızdırmazlık, soğuk, basınç, güç ve kayıt testleri yap; test edilmemiş derinliğe dayanım ilan etme.
4. İzinli yerel deniz denemesinde tekrar profil, GPS/UTC, yük/halat ve geri alma akışını sınayarak sefer protokolünü iyileştir.
5. Seferde erişilebilirse referans CTD eşleşmesini tekrar et; erişilemiyorsa Türkiye doğrulaması ile Arktik referans eksikliğini ayrı raporla [E07, E13, E16](EVIDENCE_MAP.md).

Model katkısı, gözlemden önce saklanan baseline ile sonradan düzeltme yapılan modelin **ayrı profil/istasyonlarda** karşılaştırılmasıyla değerlendirilecek. Model hatası, tahmin aralığı ve üretim kararındaki fark ayrı sonuçlardır; daha dar aralık tek başına daha doğru model değildir. Eşleşme zamanı/mesafesi ve sensör hatası açıklanır [E18–E19](EVIDENCE_MAP.md).

Adaptif örnekleme sınanırsa sabit derinlik, gradient önerisi ve varsa AI aynı numune bütçesinde karşılaştırılır; değerlendirme için PWN seçiminden bağımsız yeterli referans gerekir. Bu imkân yoksa adaptif öneri yöntemi gösterilir, verimlilik üstünlüğü kanıtlandı denmez [E11, E16](EVIDENCE_MAP.md).

Arıza durumunda [v0.1 yedek akışları](PWN_SPEC_V0.1.md) ve [saha yedek akışları](ARCTIC_FIELD_PLAN.md) uygulanır. Amaç her şeyi mülakattan önce bitirmek değil; küçük gerçek deney ile sonraki doğrulama yolunu birlikte göstermektir [E15–E17](EVIDENCE_MAP.md).
