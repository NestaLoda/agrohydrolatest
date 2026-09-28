# AgroHydro · Desenden Dengeye

GitHub deposu: https://github.com/NestaLoda/agrohydrolatest

Vercel kurulumu ve çevrimiçi/yerel kayıt sınırı: [Dağıtım notları](docs/DEPLOYMENT.md).
Güncel teslim ve doğrulama sonuçları: [Ana sohbet teslimi](docs/ANA_CHAT_TESLIM.txt).

# Önceki sürüm özeti: 0.5.0 · TESLİM 005

Bilimsel simülatör: doğrudan Scenario Lab kontrolleri, beş açık Kuzey planlama amacı, karar duyarlılığı ve saha araştırması çekmecesi. Güncel [ürün sözleşmesi](docs/FINAL_PRODUCT_CONTRACT.md), [build durumu](docs/BUILD_STATUS.md), [ana sohbet teslimi](docs/ANA_CHAT_TESLIM.txt). Aşağıdaki önceki sürüm bağlamı yeni UX için esas alınmaz.

# Sustainable Production Frontier · 0.4

Konya pilotundan Türkiye karşılaştırmasına, gelecekteki kuzey üretim sorusuna ve Polar Water Node gözlem katmanına uzanan yeni uygulama. Eski Konya kodu kullanılmadı. Güncel kapsam ve gerçek tamamlanma kaydı: [docs/BUILD_STATUS.md](docs/BUILD_STATUS.md).

## Çalıştırma

Bu bilgisayarda kurulum ve veri paketi hazır. PowerShell'de proje klasöründen:

```powershell
.\scripts\start.ps1
```

Tarayıcı: http://127.0.0.1:8000. Uygulama ve harita dış sunucu gerektirmez. Kaynak bağlantılarını açmak ve ilk paket kurulumu internet gerektirir. Kapatmak için terminalde Ctrl+C.

Başka bilgisayarda Python 3.12 ve Node.js 22.12+ ile:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.lock.txt
.venv\Scripts\python.exe scripts/ingest_data.py
cd frontend
npm ci
npm run build
cd ..
.\scripts\start.ps1
```

Ham iklim dosyaları bu paketle birlikte taşınırsa ingest önbellekten çevrimdışı çalışır. `--refresh` bilinçli yeni veri erişimidir. Eski rapor uygulamada `data/references/konya_original_report.pdf` üzerinden yerel açılır. Raporun yeniden paylaşımını ekip belirler.

## Karar çalışma alanları

1. **BUGÜN / TÜRKİYE:** kalıcı sol Scenario Lab, AUTO/MANUAL, tek girdi kilidi, su/stres kısayolları, ürün alan/pay kontrolleri. Sağda mevcut → önerilen desen ve tablo/grafik denetimi.
2. **GELECEK / KUZEY:** aynı kontrol/hızlı hesap deneyimi; kaynaklı dönem/model bağlamı, su/enerji/altyapı ve ürün hedefleri. Yerel doğrulanmamış çıktı açıkça açıklayıcı simülasyon.
3. **SAHA / PWN:** PRE-TASE snapshot ve aynı motorla desteklenen girdinin gözlem sonrası hesabı; mevcut CSV/profil modülü.
4. **KANIT / VERİ:** kaynak/provenans; her alandan kanıt çekmecesi.

[Senaryo laboratuvarı](docs/SIMULATOR_UX.md), [Arktik karar mantığı](docs/ARCTIC_DECISION_LOGIC.md), [su güvenliği](docs/NORTH_WATER_SECURITY.md). Kullanım sadeleşti; motor ve veri/grafik incelemesi korunup güçlendirildi.

Beş ilde 21 resmî alan/üretim kaydı ve dokuz ürünlük FAO örnek bilgi tabanı eklendi. Ortak motor açık tarlayı ha, sera/hidroponiği m² yetiştirme yüzeyiyle çözer. Amaç ürün bazlı hedef karşılama, sonra su ve bilinen enerji gereğidir. [Motor](docs/CROP_PATTERN_ENGINE.md), [Türkiye kaynakları](docs/TURKIYE_REGIONAL_SIMULATOR.md), [Kuzey senaryosu](docs/FUTURE_NORTH_SIMULATOR.md).

6 noktada 4.380 günlük ERA5 reanalizi; ayrı kuzey paketinde tek modelden 1995–2014 / 2030–2049 toplam 14.610 günlük kayıt bulunur. Yerel model SSP seçenekli ensemble değildir; sıcaklık/yağış göstergeleri ürün veya deniz suyu ölçümü değildir. [Ürün denetimi ve mimari](docs/PRODUCT_REFOCUS.md), [Türkiye seçimi](docs/TURKIYE_BENCHMARKS.md), [kuzey veri planı](docs/NORTH_DATA_PLAN.md).

Ek kaynaklı bağlam: NASA ACCESS-CM2 SSP245/SSP585,2035,730 günlük nokta kaydı ve aylık grafikler. Tek model yılı; üretim katsayılarına otomatik uygulanmaz.

Bu sürümde yerel Arktik verim/enerji kalibrasyonu, gerçek tank deneyi veya eğitimli AI yok. Soğuk kaynak suyunda kullanılan literatür aralığının dışında sayı uydurulmaz. Arayüzün kanıt etiketleri her adımda görünür.

## Yapı

```text
backend/         FastAPI, fiziksel hesaplar, HiGHS, PWN analizi, kaynak kayıtları
frontend/        React + TypeScript + Vite, yerel MapLibre haritası, SVG grafikler
data/            değiştirilmez ham kayıtlar, metadata, CSV/Parquet, literatür
scripts/         veri alma ve başlatma
tests/           fiziksel denge, sınırlar, kaynak bütünlüğü, API/PWN testleri
hardware/        v0.1 öğretmen/yapım paketi ve Arctic v1 mühendislik konsepti
docs/            kaynak metni, bilimsel mimari, kanıtlar ve güncel durum
```

## Geliştirme ve kontrol

```powershell
.venv\Scripts\python.exe -m pytest
```

Arayüz geliştirme: backend çalışırken `frontend` içinde `npm run dev`; `/api` yerel backend'e yönlenir. API sözleşmesi `/docs` adresindedir. Yazılım testleri fiziksel PWN doğrulaması değildir. Kaynaklar ve hesap varsayımları [MODEL_METHODS.md](docs/MODEL_METHODS.md), [DATA_ACCESS_LOG.md](docs/DATA_ACCESS_LOG.md) ve [EVIDENCE_MAP.md](docs/EVIDENCE_MAP.md) içinde.
