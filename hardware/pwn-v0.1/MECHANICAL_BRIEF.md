# Tank mekaniği — atölyeye kısa iş tarifi

Bir sensör başlığını şeffaf kolonda elle ve tekrarlanabilir biçimde indirip çıkaracağız. Başlık sabit geometrili EC elektrotları ve sıcaklık probunu taşır. Elektronik, ADC/ön devre, SD ve güç kuru kutudadır. Bu bir tank düzeneğidir; denize basınçlı indirme tasarımı değildir [onaylı kapsam](../../docs/PWN_SPEC_V0.1.md), [E16](../../docs/EVIDENCE_MAP.md).

## Yapılacak parçalar

1. **Prob tutucusu:** elektrotları sabit tutan, sıcaklık probunu yakın yerleştiren, su akışını kapatmayan açık bir taşıyıcı. Elektrotlar birbirine/metal ağırlığa temas etmez. Elektrot geometrisi söküp takınca tekrarlanmalı.
2. **Yük yolu:** üst taşıma gözü → taşıyıcı ip → başlık. Sensör kabloları taşıma ipi değildir. Kablosu başlığa ve kuru kutuya girmeden önce strain relief ile sabitlenir.
3. **Denge:** gerekirse merkezde sabitlenmiş ağırlık; serbest salınımı azaltır. Ağırlığın malzemesi çözeltiyi kirletmeyecek biçimde seçilir/yalıtılır. Kesin kütle, kaldırma ve hareket gözleminden sonra.
4. **Kılavuz:** kolonun içinde başlığı duvara sürtmeden yönlendiren düzen; elektrot önündeki akışı boğmasın.
5. **Encoder tekeri:** taşıyıcı ip sabit çap ölçüm tekerini kaymadan döndürür. Gerekirse karşı baskı tekeri. İp depolama makarası ayrı olabilir; çok kat sarılan makaranın değişken çapı ölçüm hesabına girmez.
6. **Kolon standı:** devrilmeyen taban, dış cetvel, su toplama tepsisi, kolay boşaltma. Kap genişliği gerçek başlığın rahat geçmesine göre seçilir.
7. **Kuru kutu:** kolon sıçrama alanından uzak ve kablodan su yürümeyecek düzende; bağlantılara erişilebilir. Tankta su altı elektronik gövde yok.

## Derinlik referansı

Probun EC ölçüm merkezini yüzey sıfırında işaretle. Encoder sayımını sıfırla, aşağı yönü pozitif seç. Cetvelle bilinen mesafelerde sayım kontrolü yap. Teker çapından hesap yalnız başlangıçtır; ölçülen counts_per_meter ve sıfır konumu manifestte saklanır. Tank düşeyliği korunmuyorsa cable_out_m gerçek dikey derinlik sayılmaz [DATA_SCHEMA.md](DATA_SCHEMA.md).

## İmalat için ölçülecekler

Eldeki prob çapı/uzunluğu, kablo kalınlığı, kolon iç ölçüsü, encoder mili ve bağlantı biçimi, mevcut ipin kalınlığı, ölçüm tekerinin gerçek çapı, kuru kart/kutu montaj aralığı. Bu bilgiler alınmadan basılacak kesin CAD ölçüsü uydurulmaz. Yalnız şematik yerleşim daha önce çizilebilir.

## Teslim kontrolü

Elle birkaç tam iniş/çıkışta kablo yük taşımıyor, prob duvara çarpmıyor, teker kaymıyor, sıfıra dönüş kaydedilebiliyor ve kuru kutuya su ulaşmıyorsa deney kurulumuna geçilir. Ölçülen sorunlar kısa foto/notla kaydedilir; geçmeyen kontrol gizlenmez. Ayrı kaplarda sensör çalışması, dikey kolonun tamamlandığı anlamına gelmez.
