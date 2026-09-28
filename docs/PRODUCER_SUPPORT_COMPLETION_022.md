# Üreticiye geçiş — uygulanan devam modeli

23 Eylül 2026 · TESLİM 022

Ferit Bora'nın kullanıcı tarafından iletilen fikri, **Desenden Dengeye Üretici Destek ve Pazara Erişim Programı** olarak araştırıldı ve projeye eklendi. Sürekli teknik destek, karşılaştırılabilir ekipman teklifleri/indirim, alıcı bağlantısı ve uygun sigorta kapsamına erişim ayrı sorumluluklardır. Mevcut bir sigorta, gelir garantisi, ortaklık veya alım taahhüdü oluşturulmadı. Fikrin katkı sahibi ve tarihi araştırma notunda korunur.

## Uygulanan yazılım

Türkiye ve Kuzey ekranlarının bağlam çubuğunda **Üreticiye geçiş** düğmesi var. Ana bilimsel simülasyon uzatılmadan açılan panelde üç bölüm bulunuyor: nasıl işler, destek simülasyonu, yaygınlaştırma planı. Hesap formu ve sonuç ayrı kayar; masaüstü kullanım doğrulandı, telefon testi yapılmadı.

Yeni `POST /api/producer-support/scenario` yıllık tek ürün/aynı fiyatlı ürün grubu için kullanıcı girdileriyle hesap yapar. Kayıp sonrası ürün alıcı kapasitesiyle sınırlanır; fazlası satılmış sayılmaz. Yıllık gelir, işletme gideri, kurulum bedelinin yıllık payı, ekipman indirimi ve hizmet bedeli ayrıdır. Destekli/desteksiz karşılaştırmada aynı miktar, fiyat ve alıcı kapasitesi korunur. Desteğin verimi yükselttiği veya yeni müşteri yarattığı varsayılmaz.

Başabaş fiyatı/miktarı, alıcısı planlanmamış ürün, dört stres durumu ve somut eylemler hesaplanır. Üretim −%20, fiyat −%20, işletme gideri +%20 ve birleşik stres olasılık değildir. Negatif denge kırmızı, pozitif denge yeşil; olumlu sonuç yatırım onayı değildir. Vergi, kredi/finansman, enflasyon, tahsilat zamanı ve paranın zaman değeri modellenmez. Kurulum tutarını yıllara yaymak ilk yatırım nakdini ortadan kaldırmaz.

Form başlangıçta boştur. Açıkça yüklenen öğretici örnek varsayımsal olarak etiketlenir. Boş, negatif, geçersiz ve sonlu olmayan girdiler reddedilir. Girdi değişince eski sonuç işaretlenir ve güncel sonuç indirme kapatılır. Girdiler, kaynak notu ve sonuç JSON indirilebilir; panel kapatıldığında geçici form sıfırlanır. Belge inceleme, imzalı sözleşme doğrulama, üretici hesabı veya kalıcı ticari kayıt sistemi henüz uygulanmadı. Tüm sonuçlarda USER_SCENARIO, contracts_verified=false, investment_recommendation=false vardır.

Bilimsel optimizer ve üretim desenleri bu katmandan bağımsızdır. Kuzey modelindeki kg, satış geliri olarak otomatik aktarılmadı. Su/enerji/ürün hesabı, PRE–POST sınırları ve kaynaklı veriler korundu.

## Araştırma ve metinler

- `docs/URETICI_DESTEK_MODELI.md`: resmî kaynaklı kapsam, program ve para akışı, alım/dağıtımın finansman ve stok yükü, üretici hakları, pilot ölçütleri.
- `docs/FERIT_SUNUM_VE_CALISMA_METINLERI.md`: 30 ve 90 saniyelik anlatım, beş slayt ve konuşma notları, proje paragrafı, kısa uygulama metinleri, Ferit'in çalışma çıktıları, tedarikçi/alıcı/sigortacı soruları, jüri yanıtları.
- `data/producer_support/research/manifest.json`: 23 Eylül 2026'da indirilen dört resmî kaynak, URL, UTC, yerel ham dosya ve SHA-256. TARSİM 2026 sera şartları, gelir koruma sayfası, Bakanlık tip sözleşme sayfası ve SEDDK kuruluş listesi arşivlendi. Bunlar gerçek ortaklık/uygunluk kanıtı değildir.

TARSİM sera şartlarında teminatlı risk → teknik donanım hasarı → ürün kaybı bağlantısı ile genel arıza/iş durması istisnaları ayrıdır. Mevcut gelir koruma sayfası buğday, arpa ve çavdarı tanımlar. Türkiye mevzuatı Arktik tesise otomatik uygulanmaz. İşbirliği ve teminat ancak yetkili tarafların yazılı değerlendirmesiyle somutlaşabilir. Araştırma notlarında doğrudan resmî bağlantılar vardır.

## Doğrulama — 23 Eylül 2026

Tam backend paketi: **548 test, 0 hata, 0 başarısız, 0 atlanan**; 65,353 saniye, başlangıç 14:50:39 +03. Bunun 90 testi yeni hesap/validasyon/stres paketi. TypeScript ve Vite üretim derlemesi başarılı. Mevcut Starlette/AnyIO deprecated-alias uyarısı test hatası değildir.

Canlı API öğretici örneğinde 1.000 kg hasat, %10 kayıp, 800 kg alıcı kapasitesi, 50 TL/kg, 30.000 TL işletme, 40.000 TL kurulum, %15 indirim, 5 yıl ve 1.000 TL/yıl hizmet ile destek olmadan 2.000 TL, destekle 2.200 TL yıllık denge; 100 kg alıcısı planlanmamış ürün; birleşik streste −15.000 TL bulundu. Bunlar tamamen varsayımsal yazılım kontrol sayılarıdır. Hizmet 10.000 TL olunca denge −6.800 TL ve program bedeli uyarısı görüldü. Boş API kaydı 422 ile reddedildi.

Masaüstü 1280×720: Kuzey/Türkiye girişleri, panel sekmeleri, örnek hesabı, negatif sonuç, stres grafikleri, değişen girdide eski sonuç uyarısı ve Escape ile kapatma denetlendi. Kanıtlar: `docs/verification/producer-support/` içindeki test XML/log, build log, API JSON, ekran görüntüleri ve browser-qa.json. Gerçek ölçüm/teklif/kontrat oluşturulmadı; dışarıya mesaj gönderilmedi.

## Fiziksel ve dış bağımlılıklar

PWN kalibrasyonu ve izinli TASE ölçümü/numunesi; kullanım amacına uygun uzman laboratuvar paneli; yerel yağış/kar toplama, su erişimi, zemin ve enerji koşulları; kontrollü üretimde gerçek su/enerji/satılabilir hasat. Bunlar saha/pilot kanıtı gerektirir. Sefer tek başına 2050 iklimini, yıllık karasal suyu veya üretici kazancını doğrulamaz.

Yaygınlaştırma için ayrıca yazılı ekipman teklifleri, gerçek alıcı ihtiyacı, ödeme ve kalite şartları, yetkili sigorta yanıtı ve işletme finansmanı gerekir. İlk somut adım: Ferit'in metin dosyasındaki teklif–alıcı–sigorta çalışma paketini gerçek bilgilerle doldurmak; üretim pilotunun kapsamını ölçümden önce kesinleştirmek. Sonuçlar uygunsa küçük ölçekli uygulama, ardından kanıta dayalı yaygınlaştırma.
