from pathlib import Path
import json,shutil,hashlib,xml.etree.ElementTree as ET
root=Path.cwd();doc=root/'docs';out=doc/'verification/turkey-reference';archive=doc/'archive/before-teslim008';archive.mkdir(exist_ok=True)
for name in ['BUILD_STATUS.md','ANA_CHAT_TESLIM.txt','PROJECT_SOURCE_OF_TRUTH.md','EVIDENCE_MAP.md','SCIENTIFIC_ARCHITECTURE.md','DATA_REQUIREMENTS.md']:
 if not (archive/name).exists():shutil.copy2(doc/name,archive/name)
old=(archive/'ANA_CHAT_TESLIM.txt').read_text(encoding='utf-8');north=old[old.index('GERÇEK HESAP ÖRNEĞİ'):old.index('DOĞRULAMA\n')];hardware=old[old.index('PWN TEDARİK /'):old.index('KISA TESLİM GEÇMİŞİ')]
t=ET.parse(out/'tests.xml').getroot()[0].attrib;qa=json.loads((out/'browser-qa.json').read_text());assert all(c['pass'] for c in qa['checks']);runs=json.loads((out/'engine-results.json').read_text())['runs']
rows=[]
for run in runs:
 if run['preset']!='reference':continue
 r=run['result'];crops=r['optimized']['crops'];pattern='; '.join(c['name_tr']+' %'+f"{c['area_share_pct']:.2f}" for c in crops);tot=r['optimized']['totals'];base=r['current']['totals'];w=tot.get('known_water_m3',tot['water_m3']);bw=base.get('known_water_m3',base['water_m3']);rows.append(f"| {run['region']} | {pattern} | {(bw-w)/bw*100:.2f}% |")
table='| Bölge | Hesaplanan paylar | Modellenmiş su gereği farkı |\n|---|---|---|\n'+'\n'.join(rows)
science='''Referans, il düzeyinde yayımlanmış seçili ürün alanları/üretimdir; bütün havzanın veya canlı 2026 ekilişinin sayımı değildir. Öneri mevcut üretime %100 tavan koymaz. Amaç sıralıdır: önce kullanılabilir ekili alanı en yükseğe çıkar, aynı alanı sağlayan çözümler içinde su gereğini en aza indir. Ürün başına varsayılan minimum mevcut üretimin %50’sidir; bu açık ve değiştirilebilir planlama tercihidir. Evrensel ekonomik/gıda güvenliği optimumu veya resmî tavsiye değildir. Farklı ürün kg’ları besin eşdeğeri sayılmaz.

Su gereği günlük ERA5 + FAO-56 Kc/örnek takvim + depo hesabı / sulama randımanı ile türetilir. Başlangıç bütçesi mevcut desenin modellenmiş gereksinimidir, gerçek havza su tahsisi değildir. Sabit il ortalama verimi su-stres verim modeli değildir. Bütün seçili alanların tamamlama sulaması hesabı, gerçek sulu/kuru alan ayrımının yerine geçmez. Bölgesel yerel takvim, toprak, su tahsisi, sulu/kuru ekiliş, münavebe ve ekonomik/üretim gereksinimleri sağlandıkça öneri güçlendirilebilir. Su farkı ölçülmüş tasarruf değil, aynı senaryodaki iki desenin model farkıdır.

Trakya çeltik ET dışı tava/sızma suyu eksik. Çeltik mevcut senaryo alanında tutulur; yalnız bilinen su gereği bulunan ürünler optimize edilir. Toplam su None/DATA NEEDED; bilinen alt toplam ayrı. Çeltik için gerekli su girdisi açıkça sağlanırsa tam hesaba katılır. Çelişen minimumlar sessizce gevşetilmez.
'''
changes='''- Konya, Seyhan/Adana, Gediz/Manisa, GAP/Şanlıurfa ve Trakya/Edirne aynı bölgesel amaçla ayrı hesaplanıyor. Bölge açılışı kaynaklı mevcut desen + ayrı otomatik öneri; Referans düğmesi kaynak başlangıcını geri getirip eski öneriyi temizler. Hızlı bölge değişiminde tamamlanan ilk hesap ilgili bölgede korunur; kullanıcı düzenlemesi/Referans resetini geç gelen hesap ezmez.
- Sekiz ikonlu senaryo: Referans, Su −%10, −%20, −%30, Kuraklık, Az yağış, Verimli sulama, Su +%10. Hepsi referanstan türetilir. Kuraklık su/yağış −%20, ET0 +%10; verimli sulama +10 yüzde puan randıman. Kullanıcı değişimleri MANUAL OVERRIDE; sonucu görmek için Hesapla.
- Konya 2023 başlangıcı yeni resmî 2026 yayınının 2024 alan/üretim tablosuyla yenilendi. Manisa 2025 faaliyet raporu 2024 tablosuyla doğrulandı. Diğer üç ilin mevcut kaynakları 2024 verisi; daha güncel tam uyumlu tablo doğrulanmadı. Şanlıurfa 2026 haberindeki yuvarlak tek ürün/rekolte tahmini tüm desene karıştırılmadı.
- Konya 2026 yayınının buğday/arpada hazır verim sütunu alan×üretimle tutarsız. Kaynak alan/üretim korunarak verim = ton×1000/ha türetildi; uyuşmazlık kaynak kaydında. 3,8 milyar m³ il su ifadesi seçili ürünler için tahsis olmadığı için otomatik bütçe yapılmadı.
- Beş bölgeye 3.655 günlük 2024–2025 ERA5 satırı eklendi; sezonlar 2024 sonbahar/2025 üretim dönemi. Önceki 4.380 günlük 2022–2023 paket ve Kuzey kaynakları aynen ayrı durur. Yeni paket de her okumada ham SHA256 ve satır/değer/tarih üzerinden doğrulanır.
- Güncel sıcaklık Open-Meteo model hava bilgisinden ayrı alınır; zaman damgası TSİ ve kaynak bağlantısı görünür. İstasyon ölçümü değildir; optimizasyona girmez. On dakikalık sunucu önbelleği, iki saatten eski sağlayıcı verisini reddetme, ağ yoksa veri alınamadı durumu; sezonluk çevrimdışı hesap devam eder. Ham yanıt ve kaynak anlık kaydı saklanır.
'''
validation=f"""- Backend: {t['tests']} test, 0 hata/başarısızlık, {t['time']} s; başlangıç {t['timestamp']}. JUnit: verification/turkey-reference/tests.xml. Mevcut Starlette/AnyIO deprecation uyarısı sürüyor.
- Son TypeScript/Vite derlemesi geçti: verification/turkey-reference/build.log. Son UI bölge geçişi ve TSİ düzeltmesi dahil.
- Tarayıcı: {len(qa['checks'])} başarılı kontrol; {qa['recorded_at']}. Beş bölge, Referans, senaryo değerleri, kuraklık/randıman, kısmi çeltik, hızlı bölge geçişi; konsol hatası yok. Bu tur dar ekran yeniden ölçülmedi.
- Beş bölge × sekiz senaryo: 40 gerçek API/LP koşusu, girdiler/çıktılar/run_id kayıtlı. Ayrıca bu varsayılan açık-tarla alt problemleri için ürün minimumları + kalan alanı en düşük su/ha ürününe tahsis eden bağımsız kapalı hesapla 40 optimum çapraz kontrol edildi. Maksimum alan farkı 0,012525 ha; LP’nin sıralı amaç sayısal toleransı. İlgili kayıtlar engine-results.json ve independent-optimum-check.json.
"""
files='''backend/planning.py, planning_contracts.py, regional_scope.py, repository.py, current_weather.py, app.py;
frontend/src/App.tsx, planning.ts, turkeyPresets.ts, ui.tsx, instrument.css, components/ScenarioLab.tsx, DecisionCanvas.tsx, SimulationResults.tsx, CurrentWeather.tsx;
scripts/ingest_data.py, ingest_turkey_recent.py, refresh_turkey_baselines.py, record_turkey_reference.py;
tests/test_turkey_reference.py, test_recent_turkey_data.py ve güncel veri/amaç beklentileri uyarlanan test_agriculture.py, test_data.py, test_lab_decisions.py, test_planning.py.
Yeni kaynaklar: data/manifest_turkey_recent.json, data/processed/climate_turkey_recent.csv, 5 yeni ham ERA5/metadata, 2 yeni resmî PDF; data/agriculture/region_baselines.json ve manifest.json güncellendi. Eski tarım JSON/manifest data/agriculture/snapshots altında. Geçiş scripti yeniden çalıştırılıp arşivi ezmesin diye korumalı.
'''
body=f'''# Güncel build durumu · Türkiye referans / TESLİM 008

22 Eylül 2026. Aynı proje; .git yok. Model etiketi 0.5.0, çalıştırma kimliği kod/kaynak hash’leri. Bu tur kullanıcının önceliği Türkiye; Kuzey ürün hedefi genişletilmedi. Önceki durum [arşivde](archive/before-teslim008/BUILD_STATUS.md).

## Çalışan değişiklikler

{changes}
## Bilimsel hesap sınırı

{science}
## Beş bölgenin başlangıç hesabı

2024 resmî seçili ürün deseni, ERA5 2024–2025, varsayılan %50 ürün tabanı / %75 randıman. Her sonuç aynı açık amaçla hesaplandı; bunlar gözlemlenmiş veya koşulsuz uygulanabilir en iyi desenler değildir. Trakya farkı yalnız bilinen ürün suyu içindir.

{table}

Tam girdi/çıktı: [engine-results.json](verification/turkey-reference/engine-results.json).

## Son doğrulama

{validation}
## Dosyalar

{files}
## Korunan Kuzey/PWN durumu ve açık bağımlılıklar

TESLİM007'nin kaynaklı Kuzey iklim elemesi, ortak motor, PRE/POST, 14.610 EC-Earth / 730 NASA günlük satır ve 6 NetCDF, 9 ürün kataloğu / 7 Kuzey araştırma adayı korunur. Tam kaynaklı yerel Future North önerisi henüz yok: yerel su/zemin/verim/enerji eksik, varsayılan DATA NEEDED. PWN gerçek ölçümü, kalibrasyon, kimya paneli ve pilot henüz yapılmadı. Kuzey tarayıcı senaryoları son 007 turunda doğrulanmıştı; bu tur 167 backend testinin içindeler fakat yeni Kuzey UI doğrulaması iddia edilmez.

Türkiye kapsamı uygulamadaki beş veri bölgesidir; 81 ilin tamamı uygulanmış sayılmaz. Her biri havza adının yanında kaynak ilini gösterir. Yeni bölgeler aynı akışa kaynaklı tablo ve iklim paketiyle katılabilir. Sıradaki Türkiye bilimsel adımı yerel sulu/kuru ekiliş ve gerçek mevsimsel tahsis/kısıtları bağlamak; Kuzey'e dönüş kullanıcının sonraki önceliğine bağlı.
'''
(doc/'BUILD_STATUS.md').write_text(body,encoding='utf-8')
header='''ANA SOHBETE TESLİM — TEK ARAŞTIRMA ÇİZGİSİ
TESLİM 008 — TÜRKİYE: MEVCUT REFERANS → HESAPLANAN ÖNERİ | 22 Eylül 2026
Çalışma alanı: C:\\Users\\bahao\\OneDrive\\Belgeler\\2204devrim
Önizleme: http://127.0.0.1:8011/#turkiye

Bu dosya ana sohbete tek başına yüklenebilir veya içeriği yapıştırılabilir. Ayrıntı docs/BUILD_STATUS.md. Başka sohbete kendiliğinden mesaj gönderilmedi. Aynı proje/repo, .git yok; sıfırlama/yeni depo yok.

YETKİLİ YÖN
Yeni master + en yeni açık kullanıcı talimatları eskiden üstündür. Güncel istek kutuptan önce Türkiye'deki mevcut beş bölgeyi düzeltmek: referans gerçek kaynak başlangıcı, öneri bağımsız hesap. Tek çizgi Konya → Türkiye → Future North → PRE-TASE → TASE → aynı motorla POST → kontrollü pilot. PWN araçtır; ayrı ana proje değildir. Yaklaşık %8,7 tarihsel sonuç göreli su baskısıdır, ölçülmüş m³ tasarrufu değil.

BU TUR TAMAMLANAN
'''
hand=header+changes+'\nBİLİMSEL ANLAM / SINIR\n'+science+'\nBÖLGE BAŞINA HESAP\n'+table+'\n\nDOĞRULAMA — SON GERÇEK KOŞULAR\n'+validation+'\nDEĞİŞEN DOSYALAR\n'+files+'\nKORUNAN KUZEY DURUMU — ÖNCEKİ 007 KAYDI\n'+north+'\n'+hardware+'''\nKAPSAM / SONRAKİ SOMUT ADIM
Uygulamadaki beş veri bölgesi tamamlandı; 81 ilin tamamı veya bütün havza envanteri tamamlandı denmez. Türkiye'de resmî kaynak yılı 2024, sezon hava referansı 2024–2025. Canlı 2026 ekiliş sayımı doğrulanmadı. Yayımlanan veri, varsayım, hesap ve güncel model hava bilgisi ayrı etiketli.
Yerel sulu/kuru ekiliş, mevsimlik gerçek su tahsisi, toprak/takvim ve üretim/münavebe ihtiyaçlarını kaynaklarıyla eklemek bir sonraki bilimsel iyileştirmedir. Kullanıcı Türkiye kontrolünü bitirdikten sonra Kuzey'e dönülecek.

KISA TESLİM GEÇMİŞİ
005: ortak çok ürün/yöntem/kaynak motoru, amaçlar, saha duyarlılığı.
006/U12: Türkiye ilk hesap, Kuzey günlük iklim tanısı, cihaz yapım/alışveriş belgeleri.
007: bilimsel simülatör UI rebuild; kaynaklı Kuzey elemesi; kapasite kaynak öncelikleri; PRE/POST kanıt sınırı. O tur 151 test ve 15 UI kontrolü.
008: beş Türkiye bölgesinde mevcut referans/bağımsız öneri; sekiz senaryo; yeni resmî tablo ve ERA5 paketi; güncel hava bağlamı; 167 test, 22 UI kontrolü, 40 hesap + bağımsız optimum kontrolü.
'''
(doc/'ANA_CHAT_TESLIM.txt').write_text(hand,encoding='utf-8')
notes={'PROJECT_SOURCE_OF_TRUTH.md':'Türkiye: referans kaynaklı mevcut desen, öneri mevcut üretimle sınırlandırılmayan sıralı bölgesel optimum. Önce ekili alan, sonra su; açık %50 üretim tabanı. Beş il için 2024 resmî başlangıç; ERA5 2024–2025. Canlı 2026 ekiliş sayımı veya 81 il kapsaması değildir.',
'EVIDENCE_MAP.md':'Yeni kanıt: Konya Ocak2026 yayını / 2024 tablo, Manisa2025 yayını / 2024 tablo, beş noktada 3.655 günlük ERA5 2024–2025. Eski paketler korunur. Güncel hava MODEL_NOWCAST; optimizatör girdisi değil. Çeltik toplam suyu UNKNOWN kalır. Konya hazır verim sütunu uyuşmazlığı kayıtlıdır.',
'SCIENTIFIC_ARCHITECTURE.md':'Yeni regional_water amacı max ekili alan → min su; ürün hedefi artık üst sınır değil. Kısmi Trakya problemi regional_scope.py ile bilinen su ürünlerini optimize eder; çeltik alanı sabit ve toplam su None. recent iklim seçimi kaynak doğrulaması/provenansa bağlı, eski 2022–2023 hesapları ayrı desteklenir.',
'DATA_REQUIREMENTS.md':'Türkiye yeni varsayılan: 2024 il ekiliş/üretim + 2024–2025 ERA5 günlük seri. Anlık sıcaklık ayrı zaman damgalı model hava bağlamı. Eksikler: gerçek tahsis, sulu/kuru ayrımı, yerel fenoloji/toprak, münavebe/üretim zorunlulukları, çeltik ek suyu. 81 il veri paketi yok.'}
for name,note in notes.items():
 original=(archive/name).read_text(encoding='utf-8');(doc/name).write_text('# Güncel Türkiye düzeltmesi · TESLİM 008\n\n'+note+'\n\nDetay ve son doğrulama: [BUILD_STATUS.md](BUILD_STATUS.md). Aşağıdaki 007 ve daha eski kayıtlar kendi tarihleriyle tarihsel durumdur.\n\n---\n\n'+original,encoding='utf-8')
(doc/'TURKIYE_REFERENCE_UPDATE.md').write_text(body,encoding='utf-8')
manifest={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['backend','frontend/src','tests','scripts'] for p in (root/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
(out/'final-code-hashes.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('TESLIM008 documented; tests',t['tests'],'UI',len(qa['checks']))
