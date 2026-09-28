# CAD hazırlayacak kişiye: PWN v0.1 tank düzeneği

**İş:** seçilmiş gerçek prob ve kolon ölçülerine göre basit, sökülebilir bir tutucu ve encoder ölçüm düzeni. Estetik kapalı kapsül değil, çalışan tank düzeneği öncelikli. Bu dosya CAD talimatıdır; CAD dosyası/imalat çizimi değildir. [E16](../../docs/EVIDENCE_MAP.md).

## Çizilecek parçalar

- **Sensör başlığı:** EC elektrot çifti sabit aralık/açık yüzeyde; sıcaklık ucu yakın fakat hücreyi perdelemeyen yerde. Tutucu suyu kapalı haznede hapsetmez; kabarcık birikimi ve duvar teması azaltılır.
- **Ayrı yük yolu:** üst taşıma gözü ile ip başlığı taşır. Sensör kablosu için ayrı kelepçe/strain relief; kablo çekme kuvveti elektrota/lehime ulaşmaz.
- **Denge/ağırlık:** gerektiğinde sökülebilir merkezî bağlantı. Kütle ve malzeme gerçek yüzdürme/iniş testinde seçilir; bu belge değer atamaz.
- **İp/kılavuz:** kolonda düşeye yakın, tekrarlanabilir hareket; sürtünme düşük. Başlıkla cetvel/ölçüm merkezi ilişkisi görülebilir.
- **Encoder tekeri:** tek sabit çapta ip teması, kaymayı azaltan karşı baskı ve encoder mil adaptörü. İp sarma makarası ölçüm tekerinden ayrı; çok kat sarım çapını sabit saymayın.
- **Kuru kutu:** kart, analog ön devre, SD, güç ve konnektörler erişilebilir. Kolondan ayrı montaj; kablo damla yolu; kutu altında su birikmesine izin vermeyen yerleşim.
- **Kolon standı:** mevcut şeffaf kap, sağlam taban, dış cetvel, sıçrama tepsisi ve boşaltma düzeni. Kolon ölçüsüne göre başlık boşluğu bırakılır.

## CAD başlamadan ölçülecek liste

Prob/elektrot çap ve boyları; kablo çapları; kolonun gerçek iç ölçüleri; encoder mil çapı ve sabitleme delikleri; kullanılan ip; kart/kutu montaj noktaları. Elektrot aralığı ve açık yüzey öğretmen EC tasarımıyla birlikte sabitlenir. Uydurma hassas tolerans veya varsayılan kolon çapı kullanılmaz.

## İstenen teslim

Bir montaj görünüşü, bir patlatılmış görünüş, yük/kablo yolları işaretli yan görünüş ve ölçüm tekeri yakın planı. Gerçek ölçüler geldiyse üretilebilir STEP + gerekiyorsa STL; gelmediyse açıkça `ölçüsüz konsept`. Geometri ve parça sürümü test kaydına bağlanacak. Boya/vernik/metal çözeltinin ölçümünü etkileyebileceğinden ıslak malzeme seçimi öğretmence kontrol edilir.

## İlk mekanik kabul

Elektronik kuru; kablo yük taşımıyor; elektrot aralığı değişmiyor; inişte takılma yok; teker kayması ve sıfıra dönüş cetvelle kontrol edilebiliyor. Bunlar üretim ekibinin yapacağı testlerdir; çizimin güzel görünmesi test yerine geçmez. [MECHANICAL_BRIEF.md](MECHANICAL_BRIEF.md), [TEST_PROCEDURE.md](TEST_PROCEDURE.md).
