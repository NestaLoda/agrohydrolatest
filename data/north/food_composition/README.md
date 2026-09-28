# Kaynaklı üretim amacı katsayıları

23 Eylül 2026'da Norveç Gıda Güvenliği Kurumu'nun Matvaretabellen API'sinden
`foods.json`, `nutrients.json`, `sources.json` indirildi. API sürümsüz olduğu için
ham dosyalar saklandı; SHA-256 değerleri `../food_composition.json` içindedir.
Belgeleme: https://www.matvaretabellen.no/en/api/

`scripts/build_north_food_composition.py` altı uygun ürünün açık eşlemesini ve
protein/besin enerjisi katsayılarını ham kaynaklardan tekrar üretir. Bu dosyalar
saha ölçümü değildir. Kaynağın her besin değeri için verdiği sourceId, ham kaynak
tablosunda izlenebilir; veri doğrudan analiz veya başka tablodan aktarım olabilir.

## Hesap

- Taze ürün amacı: modelin yenebilir taze hasadı, kg.
- Protein amacı: yenebilir kg × g/100 g × 10; hedef birimi g protein.
- Besin enerjisi amacı: yenebilir kg × kcal/100 g × 10; hedef birimi kcal.
- Raporlanan protein kg = protein g / 1000.
- Elektrik kWh ve gıdanın kcal değeri ayrı büyüklüklerdir.
- Mevcut ürün verimi zaten yenebilir biyokütledir; kaynak tablonun yenebilir kısım
  yüzdesi ikinci kez çarpılmaz. Kaynak yüzde bilgisi denetim için saklanır.

Üç amaçta da aynı su, alan, enerji ve çeşitlilik koşulları kullanılır. Seçilen tek
üretim çıktısı önce ençoklanır; bunun %95'i korunarak su ve enerji için normalize
en büyük sapma küçültülür. Bu %95 bir açık planlama tercihi, agronomik sabit
değildir. Varsayılan taze ürün amacı önceki çalışmayla karşılaştırılabilir kalır.
Besin amaçlarında katsayısı olmayan ürüne sıfır atanmaz; hesap açık hata verir.

## Yorum sınırı

Besin bileşimi, aynı türün çiğ yenebilir ürününe ait bir aktarım katsayısıdır;
kutup yetiştiriciliğinde aynı bileşimin oluştuğunu doğrulamaz. Çeşit, yetiştirme,
depolama/pişirme kaybı ve sindirilebilirlik ayrıca sınanmalıdır. Amaçlar tam
beslenme, yerel tüketim talebi veya kâr optimizasyonu değildir. Talep/maliyet
verisi olmadan bunlara “en iyi beslenme” veya “en kârlı desen” denmemelidir.
