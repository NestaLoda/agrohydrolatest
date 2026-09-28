# PWN CSV ve metadata sözleşmesi — 1.0

22 Eylül 2026. Ana uygulama parser'ı ile paylaşılmış veri tasarımıdır. Burada gerçek veya hayalî gözlem satırı yoktur. Ham dosya değişmez; kalibrasyon/filtre/derinlik/gradient ayrı türetilmiş çıktı olur. Kaynak ayrımı [E18](../../docs/EVIDENCE_MAP.md), bilimsel sınır [E13](../../docs/EVIDENCE_MAP.md).

## CSV başlığı

UTF-8, virgül ayırıcı, nokta ondalık; boş değer eksiktir, `0` değildir. Bir dosya bir cihaz/deney/cast ve tek raw sinyal birimi taşır. Sayı alanına NaN/Inf metni yazılmaz.

```csv
schema_version,source_kind,device_id,experiment_id,cast_id,sample_index,timestamp_utc,elapsed_ms,raw_conductivity_signal,temperature_C,encoder_count,cable_out_m,pressure_dbar,latitude,longitude,calibration_id,quality_flag
```

| Alan | Tür/birim | Kural |
|---|---|---|
| schema_version | metin | `1.0` |
| source_kind | enum | Aşağıdaki doğruluk etiketi |
| device_id | metin | Fiziksel cihaz veya sentetik üretici kimliği; boş olamaz |
| experiment_id / cast_id | metin | Hazırlanan deney ve tek profil kimliği; tekrar cast ayrı ID |
| sample_index | integer | Cast içinde sıfırdan artan; yinelenmez |
| timestamp_utc | ISO8601 | Biliniyorsa UTC `Z`; yerel saati Z ekleyerek sahteleştirme |
| elapsed_ms | integer ms | Biliniyorsa cast başlangıcından geçen süre; geriye gitmez |
| raw_conductivity_signal | sayı | Birim manifestte zorunlu; değer yoksa boş + flag |
| temperature_C | °C | Ölçülen değer; bağlantı/hata kodu ölçüm olarak yazılmaz |
| encoder_count | signed integer | Sıfır/yön tanımı manifestte; mevcut değilse boş |
| cable_out_m | m | Aşağı pozitif verilen mesafe; türetme parametresi manifestte |
| pressure_dbar | dbar | Yalnız gerçek ölçüm; v0.1'de boş |
| latitude / longitude | derece | Tankta boş; varsa kaynak/konum yöntemi manifestte |
| calibration_id | metin | Uygulanmış/kayıtlı kalibrasyon kimliği; yoksa boş |
| quality_flag | metin | `OK` veya noktalı virgülle ayrılmış açık sorun kodları |

timestamp_utc veya elapsed_ms'den en az biri bulunur. Sıcaklık örnekleme anı belirgin farklıysa gelecekte ek `temperature_elapsed_ms` alanı kullanılabilir; aynı an iddiası yaratma. İlk sürümde gecikme/örnekleme yöntemi manifestte kayıtlıdır. Süre sayacı taşması veya yeniden başlama yeni cast/segmenttir.

## Kaynak etiketleri

- `OUR_NEW_MEASUREMENT_TANK`: gerçekten ekibin cihazıyla alınmış tank kaydı.
- `EXTERNAL_OBSERVATION`: başka kaynaktan gerçek profil; provider/URL/kullanım bilgisi gerekir.
- `SIMULATION_EXPLANATORY`: sentetik veri; cihaz ve Arktik ölçümü sanılamaz.
- `PLANNED_ARCTIC_OBSERVATION`: yalnız plan metadata'sı. Henüz gözlem yoksa sıfır veri satırı; parser'a gerçek profil yerine verilmez.

Model/reanalysis veya gelecek iklim verisi PWN gözlemine dönüştürülmez; ana veri sisteminde kendi etiketiyle tutulur. Kaynak türü satırlar arasında değişmez.

## Sidecar manifest: `<cast_id>.metadata.json`

CSV tek başına raw sinyalin ne olduğunu açıklamaz. İçe alma paketi şu alanları sağlar (bunlar şema gereksinimleridir; aşağıda ölçüm değeri uydurulmuyor):

| Alan | İçerik |
|---|---|
| schema_version, source_kind, device_id, experiment_id, cast_id | CSV ile aynı |
| raw_conductivity_unit | `adc_count_12bit`, `mV`, `V` veya `arbitrary_unit`; zorunlu |
| raw_signal_definition | Hangi devre/modül çıkışı, ortalama/faz/frekans ve ADC ayarı |
| firmware_version, board_model, sensor_ids | Gerçek sürüm/model ve kurulan sensörler |
| timestamp_basis | `utc_synchronized`, `elapsed_only` veya dış kaynak yöntemi |
| depth_method | `encoder_vertical_tank`, `manual_reference`, `pressure_derived` veya `unavailable` |
| encoder_counts_per_meter, encoder_zero_count, encoder_positive_direction | Kalibre edildiğinde gerçek değerler; yapılmadıysa null |
| depth_reference | Su yüzeyi ve EC ölçüm merkezi/offset tanımı; düşeylik durumu |
| raw_direction | Sinyalin EC ile `increases`, `decreases` veya `unknown` ilişkisi; doğrulanmadan seçme |
| calibration_id, calibration_method, reference_ids | Yapıldıysa; yapılmadıysa null/açık durum |
| experiment_condition, preparation_notes, cast_direction | Homojen/tabakalı/sıcaklık kontrolü, hazırlama ve iniş/çıkış |
| location_method | Tank, gemi/deck GPS veya dış kaynağın yöntemi |
| provider, source_url, access_date, license_or_permission | Dış veride kaynak; kendi ölçümde ekip ve yerel kayıt |
| raw_file_sha256 | Dosya kapandıktan sonra uygulamanın hesapladığı özet; cihaz sayı uydurmaz |

İlk uygulama bu alanların bir alt kümesini doğrulasa bile ham birim, kaynak etiketi, zaman ve derinlik yöntemi kaybedilmeyecek. Parser'ın kesin desteklediği alanlar testleriyle izlenir; bu belge alanı çizdi diye yazılım hazır sayılmaz.

## Mesafe ve türetilmiş değişkenler

Encoder yolu: `(encoder_count - encoder_zero_count) / encoder_counts_per_meter`. Counts tanımı x1/x2/x4 sayım biçimini içerir; katalog pulse sayısını otomatik kullanma. `cable_out_m` ölçüm tekeriyle izlenen harekettir. `depth_m` yalnız düşey kontrollü tank ve tanımlı yüzey/prob referansı geçerliyse ayrı türetilir. Gerçek denizde aynı eşitlik kullanılamaz.

Türetilmiş dosya adayları: `ec_mS_cm`, `ec_reference_temperature_mS_cm`, `practical_salinity`, `depth_m`, `conductivity_gradient_per_m`, `layer_candidate`. EC dönüşümünün katsayısı ve birimi, sıcaklık modeli ve referans sıcaklığı kaydedilir. Raw ADC gradienti, EC gradientiyle aynı birim değildir. Practical salinity yalnız geçerli deniz C/T/p ve [GSW dönüşüm şartları](https://teos-10.org/pubs/gsw/html/gsw_SP_from_C.html) sağlanınca. Eksik parametreye varsayılan sıfır yok.

Önerilen flag'ler: `MISSING_CONDUCTIVITY`, `MISSING_TEMPERATURE`, `ENCODER_UNCALIBRATED`, `MANUAL_DEPTH`, `TIME_UNSYNCED`, `ADC_SATURATED`, `LOGGING_FALLBACK`, `SENSOR_NOT_VALIDATED`. `OK` ile hata flag'i aynı hücreye yazılmaz. Bunlar kalite durumudur, otomatik silme emri değildir.

CSV + manifest değişmez `raw` kopyada saklanır. Analiz kendi sürümü, girdi dosya özeti, dönüşüm ve parametre kaydıyla yeni dosya üretir. Yeniden kalibrasyon raw dosyayı geriye dönük değiştirmez.
