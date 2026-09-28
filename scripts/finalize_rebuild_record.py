"""Consolidate measured rebuild results into the cumulative handoff."""
from pathlib import Path
import json
import shutil
import zipfile
import difflib
from datetime import datetime, timezone
from xml.etree import ElementTree

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs'
OUT=DOC/'verification/rebuild'
ARCHIVE=DOC/'archive/rebuild-before'
for name in ['BUILD_STATUS.md','ANA_CHAT_TESLIM.txt']:
    if not (ARCHIVE/name).exists():shutil.copy2(DOC/name,ARCHIVE/name)
suite=ElementTree.parse(DOC/'verification/rebuild-tests.xml').getroot().find('testsuite').attrib
qa=json.loads((OUT/'browser-qa.json').read_text(encoding='utf-8'))
assert all(c['passed'] for c in qa['checks'])
tests=f"{suite['tests']} test, {suite['failures']} başarısızlık, {suite['errors']} hata; {suite['time']} s; başlangıç {suite['timestamp']}"
browser=f"{len(qa['checks'])} doğrulanmış kontrol; kayıt {qa['checkedAt']}"

build=f'''# Güncel build durumu · Rebuild / TESLİM 007

22 Eylül 2026. Paket/model sürüm etiketi 0.5.0; bu işin kimliği rebuild ve kaynak kod hash'leridir. Önceki U12/005/006 durumları [arşivde](archive/rebuild-before/BUILD_STATUS.md). Yeni yetkili kapsam [REBUILD_CONTRACT.md](REBUILD_CONTRACT.md); inceleme [REBUILD_EVIDENCE_AUDIT.md](REBUILD_EVIDENCE_AUDIT.md).

## Çalışan ürün ve bu turdaki değişiklikler

- Aynı proje klasöründe veri/bilim korunarak ana simülatör yeniden düzenlendi. .git bulunmadı; yeni depo/reset yok. UI/backend değişim öncesi ZIP ve ağaç/hash envanteri verification/rebuild altında.
- Üstte BUGÜN / TÜRKİYE, GELECEK / KUZEY, SAHA GÜNCELLEMESİ ve minimal bağlam; solda bağımsız Scenario Lab, sağda Decision Canvas. Ölçülen 1367×768 CSS ekranda kontrol genişliği 354 px. Orman/petrol kabuk, sıcak tuval, anlamsal su/üretim/enerji renkleri. Harita veya büyük tablo ana etkileşim değil.
- Türkiye: 5 il kaynağı otomatik yükler ve ilk optimizasyon çalışır. Ürün payı sürgüleri, yüzde/hektar, su −%10/−%20/kuraklık, su bütçesi/randıman, gelişmiş iklim/kısıtlar. Pay artışında toplam alanı aşmamak için gerekirse diğer paylar orantılı azalır. MANUAL OVERRIDE ve eski sonuç uyarısı görünür. Hesap sonrası mevcut/önerilen barları, üretim, su, atanmayan alan ve bağlayıcı kısıtlar birlikte.
- Kuzey: kaynaklı günlük iklim ön taramasının olumsuz sonucu artık **aynı optimizatörün açık tarla adaylarını eler**. Araştırma kataloğu ve yöntem uygunluğu korunur. Özgün/etkin girdiler ayrı; kaynak/motor hash'leri ve SOURCED/MODELED/ASSUMED/UNKNOWN + field_measurable kaydı vardır. Geçen tarama yerel uygunluk/verim onayı değildir.
- Kuzey amaçları: kapasite/dengeli; su ve enerji önceliğinde kg talebinden bağımsız kapasite modu. Önce ortak ulaşılabilir pay, sonra açık %80 üretim tabanı üzerinde kaynak minimizasyonu. %80 değiştirilebilir planlama tercihi, saklı ağırlık değildir. Gerçek talep varsa talep modu korunur. Aynı örnekte su ve enerji önceliği aynı sonucu verdi; farklılık zorlanmadı.
- Üretim çıktısı: ürün kg, ha/m², yöntem, su kaynak payı, ürün sezonu, su/enerji, gerekçe ve kaynak kısıtları. Yerel bilimsel girdiler eksikken varsayılan Kuzey hesabı DATA NEEDED. Açıklayıcı değerler yalnız kapalı hesap deneyi bölümünden açıkça yüklenir.
- Saha A/B/C ve duyarlılık çekmecesi aynı projeye bağlı. PRE kaydı dondurulur; desteklenen sıcaklık ve uygun eşleşme ile aynı motor çalışır. Simülasyon etiketi sonuç kaydındaki kanıt türüne bağlıdır; dropdown değiştirmek sonucu OBSERVED yapmaz. 24 saat uyumsuzluk güncellemeyi engeller; aynı sıcaklıkta değişmeyen desen geçerli sonuçtur.
- Güncel sözleşme, model/kanıt kayıtları, otomasyon açığı, demo ve mülakat anlatımı güncellendi. Fiziksel donanım veya yeni kaynak veri edinimi yapılmadı.

## Korunan gerçek varlıklar

4.380 ERA5; 14.610 EC-Earth; 730 NASA ACCESS-CM2 SSP245/585 2035 günlük satır ve 6 NetCDF; 21 resmî tarım kaydı, 9 ürün kataloğu, 7 Kuzey aday araştırması ve 20 otomatik analiz parametresi. FAO-56, provenance/ham kaynak hash'leri, çok ürün LP, PWN importer, PRE/POST ve eski 144 test korundu.

99 data/hardware dosyası karşılaştırıldı: **98 birebir aynı**. Tek değişen dosya data/metadata/provenance.sqlite; yeni hesapların çalışma kaydı tutuldu. Dosya denetimi [asset-preservation.json](verification/rebuild/asset-preservation.json); SQLite'nın yalnız dosya hash'iyle içerik farkı kanıtlanmaz. Ham dosyalar/kalibrasyon varsayımları gerçek ölçüme çevrilmedi.

## Gerçek hesap / bilimsel sınır

NASA SSP245 2035, açık örnek varsayımlar, dengeli amaç: arpa 5.699,44 kg / yaklaşık 1,90 ha; patates 0 (araştırma sıcaklık elemesi); marul 1.013,23 kg / 337,74 m² hidroponik. Su 3.819,89 m³, enerji yaklaşık 40.000 kWh. Kaynaklar tatlı su 2.000, depolanmış 500 ve arıtılmış deniz suyu yaklaşık 1.319,89 m³. Bunlar **hesaplanmış açıklayıcı senaryo**, kaynakla doğrulanmış yerel Arktik önerisi veya gerçek üretim sonucu değil.

Aynı koşulda kapasite amacı 5.035,98 kg arpa + 1.200 kg marul üretir. Su/enerji önceliği 4.559,55 kg arpa + 810,59 kg marul, 3.055,91 m³ ve 26.802,88 kWh verir. Tam istek/etkin girdi/sonuç ve run_id kayıtları [engine-results.json](verification/rebuild/engine-results.json).

Duyarlılık: bu açık senaryoda tatlı su, enerji ve deniz sıcaklığı uç koşuları deseni etkiliyor. Tatlı su/enerji ±%20 stres; sıcaklık 5–18°C arıtma ilişkisinin destek alanı, Arktik tahmini değil. Salinite/kimya MODEL_LINK_NEEDED; ekonomik/probabilistik bilgi değeri ve otomatik güven artışı hesaplanmaz.

## Son doğrulama

- Tam backend koşusu: **{tests}**. [JUnit](verification/rebuild-tests.xml). Mevcut Starlette/AnyIO deprecation uyarısı; test başarısızlığı yok. Öncesinde 144 testlik başlangıç koşusu ayrıca kayıtlı.
- React/TypeScript/Vite üretim derlemesi geçti; son UI değişiklikleri bu derlemeye dahil. Derleme kaydı verification/rebuild/build.log.
- Tarayıcı: **{browser}**. Konya −%20, ikinci il otomasyonu, kaynaklı Kuzey DATA NEEDED, dengeli/su/enerji hesapları, duyarlılık, PRE/POST/geçersiz/eşit gözlem, sürgü klavye erişimi, masaüstü kontrol/footer ve 390×844 CSS taşma kontrolü. [QA](verification/rebuild/browser-qa.json). Konsol hatası yok; ağ istek sayısı ölçülmedi. 390 px için görüntü yakalama araç sınırı nedeniyle yalnız DOM taşma kontrolü kaydı vardır.
- Görseller: [nihai Konya](verification/rebuild/konya-water20-final.png), [Kuzey eksik veri](verification/rebuild/north-source-needed.png), [dengeli plan](verification/rebuild/north-balanced.png), [su önceliği](verification/rebuild/north-water-priority.png), [duyarlılık](verification/rebuild/tase-sensitivity.png), [PRE/POST](verification/rebuild/pre-post-matched.png), [uyumsuzluk](verification/rebuild/pre-post-rejected.png), [değişmeme](verification/rebuild/pre-post-no-change.png), [Şanlıurfa](verification/rebuild/sanliurfa-baseline.png). Sonraki küçük kaynak sınırı/ondalık/kanıt etiketi düzeltmeleri nihai Konya derlemesinde; eski ekranlar kendi çekim durumunu gösterir.

## Açık bilimsel bağımlılıklar / tamamlanmayan hedef

Tam otomatik **yerel kaynaklarla çözülmüş Kuzey üretim planı henüz tamamlanmadı**. Yerel mevsimsel su tahsisi/erişim/depo/çevresel ve rakip kullanımlar, toprak/permafrost/aktif tabaka, dönemsel ürün verimi ve sulama, sera ısı/ışık enerjisi eksik. Kaynaklı aday elemesi bu boşluğu kapatmaz. Sezon girdileri gösterilir; optimum sezon/depo işletmesi çözülmez. Arıtma kimyası/salinite modeli, gerçek eşlenmiş deniz model profili, CTD/PWN kalibrasyonu ve fiziksel ölçüm yok.

Numune sayısı/derinlikleri/paneli uzman, gemi, izin ve laboratuvar olmadan sabitlenmez. δ18O/δ2H ve arıtma açısından anlamlı sınırlı kimya adaydır. Sefer sonrası gerçek numune veya açıkça sentetik kaynak suyu → arıtma → kontrollü büyüme pilotu plan düzeyinde; tüm Arktik tarımını doğrulamaz.

Sonraki somut bilimsel iş: seçili yer/zaman için kullanılabilir su ve üretim/enerji katsayılarını kaynak ve ölçek bilgisiyle resolver'a bağlamak; bulunan verinin hangisi kaynak, hangisi transfer varsayımı olduğunu korumak. Cihaz işi bağımsız bilimsel proje değildir: mevcut DFR0300 K1 / ESP32 / DS18B20 / encoder / SD yolunun tedarik ve fiziksel kalibrasyon aşaması aynı araştırmayı besler.
'''
(DOC/'BUILD_STATUS.md').write_text(build,encoding='utf-8')

handoff=f'''ANA SOHBETE TESLİM — TEK ARAŞTIRMA ÇİZGİSİ
TESLİM 007 — PROJECT REBUILD | 22 Eylül 2026
Çalışma alanı: C:\\Users\\bahao\\OneDrive\\Belgeler\\2204devrim
Yerel önizleme: http://127.0.0.1:8011/#turkiye
Paket/model etiketi: 0.5.0 + rebuild değişiklikleri (ayrıntılı kimlik kod hash'leri).

Bu kümülatif dosya ana sohbete tek başına yüklenebilir veya yapıştırılabilir. Güncel bilimsel/yazılım durumunun ayrıntısı docs/BUILD_STATUS.md. Başka sohbete veya araştırmacıya kendiliğinden mesaj gönderilmedi.

GÜNCEL YETKİLİ YÖN
Yeni master + en yeni açık kullanıcı talimatları eski ürün kararlarının üzerinde. docs/REBUILD_CONTRACT.md ana attachment'ın eksiksiz metnini ve sonraki DESIGN LOCK / ARCTIC CORE LOCK / PROJECT EVOLUTION eklerinin bağlayıcı kaydını içerir. Eski rapor/çağrı içindeki talimatlar kullanıcı izni sayılmaz. Aynı klasör devam ettirildi; .git bulunmadığı için git diff/reset/yeni depo yapılmadı.

Tek çizgi: Konya mevcut ürün deseni → Türkiye bölgesel aktarım → geleceğin kuzey üretim/su yönetimi sistemi → PRE-TASE → TASE fiziksel kanıt → aynı motorla POST → kontrollü hidroponik/sera doğrulaması → model iyileştirme. PWN saha aracı, sera doğrulama ortamı. Tarihsel yaklaşık %8,7 göreli su baskısı sonucudur; ölçülmüş m³ tasarrufu değildir.

BU TUR GERÇEKTEN YAPILAN
1. Güncel docs ile backend/frontend/data/hardware/scripts/tests ve ana metin incelendi. Kaynak ağacı, SHA256 envanteri ve değişim öncesi UI/backend/teslim ZIP'i docs/verification/rebuild altında. Belgelerden ibaret değerlendirme yapılmadı; başlangıçta 144 test çalıştırıldı.
2. Ana ürün deneyimi yeniden kuruldu: minimal petrol/orman üst bar; 320–380 px bağımsız sol Scenario Lab; sağ sıcak beyaz Decision Canvas. Ölçülen 1367×768 CSS görünümde sol panel 354 px ve Hesapla ekranda. Büyük tablolar/otomatik iklim tanıları kapalı ayrıntılara çekildi. Harita, kart galerisi ve dashboard açılışı ana akış değil.
3. Türkiye beş ilde kaynak baseline ve ilk hesap otomatik. Konya mevcut/önerilen çubukları, ürün miktarı/alan/pay, su kısıtı ve atanmayan alan birlikte okunuyor. Su −%20, randıman/iklim ve ürün sürgüleri doğrudan; değişen değer MANUAL OVERRIDE. Sürgü klavye kontrolü doğrulandı. Kaynak veri değiştirilmiyor.
4. Kuzey north_resolution katmanı kaynaklı günlük iklim olumsuz aday taramasını aynı optimizatöre bağlıyor. Patates açık tarla 2035 araştırma filtresinde eleniyor. Olumlu tarama yerel zemin/verim/uygunluk onayı değil. Özgün ve etkin girdiler, neden, kaynak/motor hash'leri ve SOURCED/MODELED/ASSUMED/UNKNOWN + field_measurable ayrı kayıtlı.
5. Kapasite/dengeli yanı sıra su ve enerji önceliğinde kg talebinden bağımsız hesap: önce ortak üretim potansiyeli, açık varsayılan %80 taban, sonra seçili kaynak minimizasyonu. Gerçek talep modu korunur. Örnek su/enerji planı aynı çıktı; yapay fark üretilmedi. Kullanıcı nihai kg miktarlarını ana girdi olarak vermiyor.
6. Kuzey karar ekranı kg, ha/m², yöntem, su kaynağı, sezon, su/enerji ve kısıtları gösteriyor. Gerçek girdiler eksikse DATA NEEDED. Gizli örnek katsayı otomatik bilimsel baseline yapılmadı; açık hesap deneyi ikincil bölümde.
7. Saha duyarlılığı + A/B/C araştırma akışı aynı kararın devamı. PRE dondurma, eşleşme, aynı motorla POST ve değişmeme korunur. Simüle gözlem sonucu yalnız kanıt türü dropdown'uyla OBSERVED olamaz; etiket kayıtlı sonuca bağlı. 24 saat zaman uyuşmazlığı sonrası hesap engellenir.
8. Ana sözleşme, bilimsel kaynak/kanıt/mimari/model, otomasyon açığı, demo ve mülakat metinleri güncellendi. Önceki ayrıntılı kayıtlar tarihsel diye ayrıldı. Eski teslim bütünü docs/archive/rebuild-before/ANA_CHAT_TESLIM.txt.

KORUNAN VARLIKLAR
4.380 ERA5, 14.610 EC-Earth, 730 NASA ACCESS-CM2 SSP245/585 2035 günlük satır; 6 NetCDF; 21 resmî tarım kaydı; 9 ürün kataloğu; 7 Kuzey aday araştırması; 20 otomatik analiz parametresi. FAO-56, ortak LP, provenance, ham kaynaklar ve PWN importer korunur. 99 data/hardware dosyası karşılaştırıldı; 98 hash aynı, çalışma kayıtları alan provenance.sqlite değişti. Yeni saha ölçümü veya yeni dış veri indirmesi yok.

GERÇEK HESAP ÖRNEĞİ — YEREL ARKTİK ÖNERİSİ DEĞİL
NASA SSP245 2035 + açık mühendislik katsayıları + dengeli amaç: arpa 5699,44 kg / 1,90 ha; patates 0; marul 1013,23 kg / 337,74 m² hidroponik. Su 3819,89 m³; enerji yaklaşık 40000 kWh. Tatlı su 2000, depolanmış su 500, arıtılmış deniz suyu yaklaşık 1319,89 m³. Sayılar LP çıktısıdır; katsayıların yerel doğruluğu veya gerçek üretim kanıtı değildir. Su/enerji önceliği: 4559,55 kg arpa + 810,59 kg marul; 3055,91 m³ ve 26802,88 kWh. Eksiksiz girdiler/sonuçlar/run_id: docs/verification/rebuild/engine-results.json.

SU GÜVENLİĞİ / BİLGİ DEĞERİ / TASE
Fiziksel su → mevsim → erişim/depo → kalite → arıtma/enerji → kullanılabilir üretim suyu. Motor kaynak bütçesi/kalite/enerji/kapasiteyi kullanır; bu bütün hidrolojik zincirin veya optimum sezon/depo işletmesinin çözümü değildir.
Açık senaryoda mevsimsel tatlı su, enerji ve deniz sıcaklığı uç koşuları deseni etkiliyor. Tatlı su/enerji ±%20 stres; sıcaklık 5/18°C arıtma bağıntısının destek alanı, Arktik sıcaklık tahmini değil. Bu deterministik duyarlılık; EVSI, ekonomik fayda veya güven yüzdesi değil. Salinite/kimya için sayısal karar bağlantısı yok.
Karasal yıllık/mevsimsel su hacmi, iklim2050, verim ve permafrost PWN ile doğrudan ölçülmez. PWN hedefleri C/S, T, p/z, UTC, konum ve kalibrasyon/kalite. Model beklentisi fiziksel ölçümden önce dondurulur. Modelin doğru çıkması ve desenin değişmemesi geçerli sonuçlardır.
İzinli numune: arka plan/gradient derinliği aday; sayı/derinlik/panel sabitlenmedi. δ18O/δ2H kaynak karakterizasyonu; yalnız kararı iyileştiren sınırlı kimya arıtma/üretim uyumu için aday. Uzman/laboratuvar, gemi/izin, koruma/taşıma gereksinimleri açık. Sabit derinlik ve gradient seçimi eşit örnek bütçesinde karşılaştırılabilir; AI zorunlu değil.
Sefer sonrası numune veya ölçülen kimyadan açık SYNTHETIC/RECONSTRUCTED su → arıtma/koşullandırma → standart besin çözeltisi → kontrollü test. Su/enerji/EC/büyüme/biokütle/verim vekili ölçülür. Bu tüm Arktik tarımını doğrulamaz. Önerilen sera/hidroponik pilotun gerçek işletme verisi sonraki model iyileştirmesidir.

GERÇEK EKSİKLER — TAMAMLANMIŞ SAYILMADI
Tam otomatik yerel kaynaklı Future North üretim önerisi henüz yok. Varsayılan sonuç DATA NEEDED; tam sözleşmenin bu bilimsel kabulü açık. Yerel su tahsisi/mevsimsellik/depo/erişim/rakip kullanımlar, toprak/permafrost/aktif tabaka, dönemsel yield/sulama, sera ısı/ışık/enerji ve kaynak-temsil bağı eksik. Kaynaklı aday elemesi yalnız kısmi otomasyon. Yıllık Arizona hidroponik verileri kısa Arktik sezona sessizce kopyalanmadı. Gerçek eşlenmiş okyanus modeli/PWN/CTD ve kimyadan arıtma modeli bağlantısı henüz yok.

DOĞRULAMA
{tests}. docs/verification/rebuild-tests.xml. Mevcut Starlette/AnyIO uyarısı; hata yok. Yeni 7 test: kaynak elemesinin motora etkisi, bilinmeyenlerin korunması, su/enerji miktarlarının kg taleplerinden bağımsızlığı, açık tabanın etkisi, tüm yöntemleri kapatma, duyarlılıkta politika/karasal su ayrımı.
Son React/TypeScript/Vite derlemesi geçti (build.log). {browser}. Konsol hatası yok; ağ sayısı ölçülmedi. Dar ekran 390×844 DOM taşma kontrolü geçti; o ölçüde screenshot araç sınırı vardı. Eski 27/7 UI testleri yeni sonuç diye aktarılmadı.
Ekranlar docs/verification/rebuild/: konya-water20-final.png, north-source-needed.png, north-balanced.png, north-water-priority.png, tase-sensitivity.png, pre-post-matched.png, pre-post-rejected.png, pre-post-no-change.png, sanliurfa-baseline.png. Kanıt kayıtları browser-qa.json ve engine-results.json.

ANA DEĞİŞEN DOSYALAR
backend/north_resolution.py; backend/planning.py; backend/planning_contracts.py; tests/test_rebuild.py.
frontend/src/App.tsx; components/ScenarioLab.tsx; components/DecisionCanvas.tsx; components/SimulationResults.tsx; workspaces/Simulation.tsx; workspaces/PatternField.tsx; instrument.css; main.tsx; planning.ts; ui.tsx; frontend/index.html.
docs/REBUILD_CONTRACT.md; REBUILD_EVIDENCE_AUDIT.md; BUILD_STATUS.md; ANA_CHAT_TESLIM.txt; DEMO_PLAN.md; INTERVIEW_STORY.md ve güncel not eklenen kaynak/mimari/model/kanıt belgeleri. scripts/rebuild_inventory.py (ilk envanter; tekrar çalıştırmak başlangıcı ezer), record_rebuild.py (bir kez), rebuild_results.py, finalize_rebuild_record.py. Dosya farkı: docs/verification/rebuild/code-diff.patch.

PWN TEDARİK / FİZİKSEL DURUM — ÖNCEKİ İŞ KORUNUR
DFR0300 K1 EC kit + ESP32 + DS18B20 + encoder + microSD; açık 3D başlık, ayrı taşıyıcı ip, yukarıda mesafe tekeri/kuru kutu. Kullanıcı 3D yazıcı erişimini doğruladı. SD elektriksel uyum, kitte standartlar, gerçek mekanik ölçüler ve stok/teslim teyidi açık. Parça alınmadı, sipariş verilmedi; fiziksel firmware/kalibrasyon/tank/Arktik deneyi bu tur yapılmadı.
docs/PWN_V01_LINKLI_ALISVERIS.md/.txt, PWN_V01_TAM_MALZEME_LISTESI.md, PWN_V01_CIHAZ_TARIFI.md, docs/teslim/PWN_V01_YAPIM_PAKETI_01.zip ve konsept görsel korunur. Önceki fiyatlar kendi tarihli araştırma kaydıdır; bu tur yenilenmedi, kesin tüm cihaz bedeli diye kullanılmaz. Konsept CAD veya ürün fotoğrafı değildir.

KISA TESLİM GEÇMİŞİ
005: ortak çok ürün/yöntem/kaynak motoru, amaçlar ve saha duyarlılığı; tam otomasyon iddiası sonradan daraltıldı.
006/U12: Türkiye otomatik ilk hesap ve Kuzey günlük iklim/ön tarama tanısı; üretim girdisine bağlantı eksikti. Cihaz yapım/alışveriş dokümanları eklendi.
007: ana deneyim rebuild, kaynaklı olumsuz elemenin optimizatöre bağlantısı, kapasite tabanlı kaynak öncelikleri, kanıt/field akışı doğrulaması. Tam yerel Kuzey üretim modelinin eksikleri açık tutuldu.

SONRAKİ SOMUT ADIM
Yeni panel eklemek yerine seçili saha/dönemin hidrolojik arzı ve üretim/enerji katsayılarını kaynak/ölçek/provenansıyla north_resolution'a bağla; otomatik doldurulamayanda UNKNOWN'u koru. Fiziksel cihaz tedarik/kalibrasyon planı aynı projenin saha hazırlığı olarak devam eder. Çalışan akışın dört sorusu: ne biliyoruz, model ne öneriyor, ne belirsiz, hangisini TASE sınayabilir?
'''
(DOC/'ANA_CHAT_TESLIM.txt').write_text(handoff,encoding='utf-8')

diff=[]
with zipfile.ZipFile(OUT/'before-product.zip') as z:
    names=set(n for n in z.namelist() if n.startswith(('frontend/','backend/')) and Path(n).suffix in {'.py','.tsx','.ts','.css','.html','.json'})
    names.update(p.relative_to(ROOT).as_posix() for p in (ROOT/'backend').glob('*.py'))
    names.update(['frontend/src/components/ScenarioLab.tsx','frontend/src/components/DecisionCanvas.tsx','frontend/src/instrument.css','tests/test_rebuild.py'])
    for name in sorted(names):
        before=z.read(name).decode('utf-8-sig').splitlines(True) if name in z.namelist() else []
        after=(ROOT/name).read_text(encoding='utf-8-sig').splitlines(True) if (ROOT/name).exists() else []
        diff.extend(difflib.unified_diff(before,after,fromfile='before/'+name,tofile='after/'+name))
(OUT/'code-diff.patch').write_text(''.join(diff),encoding='utf-8')
print(json.dumps({'tests':tests,'browser':browser,'handoff':str(DOC/'ANA_CHAT_TESLIM.txt')},ensure_ascii=False))
