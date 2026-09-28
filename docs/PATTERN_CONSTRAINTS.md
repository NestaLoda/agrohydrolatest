# Desen kısıtları ve optimizasyon sözleşmesi

22 Eylül 2026 · U8. Kod dayanağı [planning_contracts.py](../backend/planning_contracts.py) ve [planning.py](../backend/planning.py).

Her seçenek `i = ürün × yöntem × su kaynağı` ve kapasitesi `x_i ≥ 0` olsun. Açık tarla için x hektar; kontrollü üretim için m² yetiştirme yüzeyidir. Verim y, su gereksinimi w ve enerji e bu kapasite birimine göre tanımlıdır.

| Kısıt | Uygulanan ilişki | Anlamı |
|---|---|---|
| Açık tarla kapasitesi | Σ açık tarla x ≤ alan_ha | Aynı dönem senaryosunda alan üst sınırı |
| En az ekili alan | Σ açık tarla x ≥ alan_ha × minimum oran | Varsayılan 0; boş alan raporlanır |
| Ürün alan payı | min_pay × alan ≤ Σ ürünün açık alanı ≤ max_pay × alan | Paydanın tamamı açık alan kapasitesi; hidroponik karışmaz |
| Sera / hidroponik | Σ ilgili yöntem x ≤ yöntem_m² | Yöntem kapasiteleri ayrı |
| Kaynak suyu | Σ kaynak için w_i x_i ≤ kaynak_m³ | Kalite ve erişilebilirlik açık senaryo |
| Ürün minimumu | Σ ürün için y_i x_i ≥ minimum_kg | İmkânsızsa sessiz gevşetilmez |
| Enerji | Σ e_i x_i ≤ bütçe_kWh | Bütçe açıksa katsayısı eksik seçenek elenir |

İklim/zemin uygunluğu açık tarla seçeneğinde `True` olmalı. Kaynak kapalı, kalitesi bilinmiyor veya hacmi sıfırsa seçenek kullanılamaz. Ürün/yöntem katalogla uyuşmalı. Kontrollü üretim için kg/m² ve m³/kg girdisi; enerji bütçesi varsa kWh/kg ve kaynak enerjisi gerekir. Çeltik ve gelecek kuzey sulaması özel eksik-veri kapılarını korur.

## Amaç ve açıklama

Her ürün için `0 ≤ z_c ≤ 1`, `z_c ≤ üretim_c / hedef_c`. Önce `Σ öncelik_c × z_c` en yüksek yapılır; sonra aynı başarı düzeyinde brüt su, tüm enerji verileri tam ise enerji azaltılır. Hedefler ticari veya besinsel eşdeğerlik değildir. Varsayılan eşit öncelik ve Türkiye %50 minimum üretim birer tasarım tercihidir; kullanıcı düzenleyebilir.

Çıktıda kapasite, kullanım, kalan pay ve sayısal tolerans içinde bağlayıcılık verilir. Sıfır kapasiteli kapalı kaynak matematiksel olarak bağlayıcı görünebilir; bunun gerçek bir kaynak kıtlığına duyarlılık kanıtı olduğu söylenmez. Ürün açıklaması kendi alan değişimini, minimumunu ve hedef su maliyetini gösterir. “Bu ürün neden azaldı?” cevabı bu amaç ve kısıtlarla sınırlıdır.

## Bilinçli sınırlar

Bu ilk motor tek dönem kapasite tahsisi yapar; parselde birden çok ürün ardışıklığı, münavebe ve rekabet eden takvimleri çözmez. Resmî ekiliş toplamı benzersiz arazi değildir. Sulama kaynağı hacmi ürünlere kullanılabilir su olarak verilir; rezervuar işletmesi veya bütün havza hidrolojisi değildir. Azot, fiyat, beslenme ve karbon amaçları bu sürümde sayısal olarak çözülmez. Etiket/uyarı yerine gerçek hesap kapısı gereken yerde eksik veri seçenekleri kapatır; herhangi bir minimum yüzünden çözüm yoksa sonuç `infeasible`, hiç uygun seçenek yoksa `insufficient_data` olur.
