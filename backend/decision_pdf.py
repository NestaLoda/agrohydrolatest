"""Decision-maker PDFs rendered from the same calculated result as the UI."""
from __future__ import annotations

from io import BytesIO
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

FOREST = colors.HexColor('#173f36')
GREEN = colors.HexColor('#3c8760')
BLUE = colors.HexColor('#3886a2')
AMBER = colors.HexColor('#b68b43')
PAPER = colors.HexColor('#f7f7f1')
INK = colors.HexColor('#203d35')
MUTED = colors.HexColor('#5c7067')
LINE = colors.HexColor('#d9e4dc')
RED = colors.HexColor('#a85b48')


def _fonts():
    if 'Decision' in pdfmetrics.getRegisteredFontNames():
        return
    root = Path(__file__).resolve().parent / 'fonts'
    regular = root / 'NotoSans-Regular.ttf'
    bold = root / 'NotoSans-Bold.ttf'
    if not regular.exists():
        raise RuntimeError('Bundled Noto Sans fonts are required for decision PDFs.')
    pdfmetrics.registerFont(TTFont('Decision', str(regular)))
    pdfmetrics.registerFont(TTFont('Decision-Bold', str(bold)))
    pdfmetrics.registerFontFamily('Decision', normal='Decision', bold='Decision-Bold')


def _fmt(v, digits=1):
    if v is None:
        return 'Hesaplanmadı'
    s = f'{float(v):,.{digits}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


class Report:
    def __init__(self, kind, title, subtitle):
        _fonts()
        self.buffer = BytesIO()
        self.c = Canvas(self.buffer, pagesize=A4, pageCompression=1)
        self.c.setTitle(title)
        self.c.setAuthor('Desenden Dengeye · karar destek simülasyonu')
        self.w, self.h = A4
        self.margin = 42
        self.y = self.h - 42
        self.page = 1
        self.kind = kind
        self.title = title
        self.subtitle = subtitle
        self._header()

    def _header(self):
        c = self.c
        c.setFillColor(FOREST); c.rect(0, self.h-114, self.w, 114, fill=1, stroke=0)
        c.setFillColor(colors.HexColor('#9bd0b6')); c.setFont('Decision-Bold', 9)
        c.drawString(self.margin, self.h-36, 'DESENDEN DENGEYE  /  KARAR DESTEK SİSTEMİ')
        c.setFillColor(colors.white); c.setFont('Decision-Bold', 21)
        c.drawString(self.margin, self.h-68, self.title)
        c.setFillColor(colors.HexColor('#d8e9dc')); c.setFont('Decision', 9)
        c.drawString(self.margin, self.h-90, self.subtitle)
        self.y = self.h-135

    def _footer(self):
        c = self.c
        c.setStrokeColor(LINE); c.line(self.margin, 40, self.w-self.margin, 40)
        c.setFont('Decision', 7.5); c.setFillColor(MUTED)
        c.drawString(self.margin, 27, 'Kaynaklı veri + açık varsayımlar + koşullu simülasyon')
        c.drawRightString(self.w-self.margin, 27, f'Sayfa {self.page}  /  Simülasyon raporu')

    def space(self, h=9):
        self.y -= h

    def ensure(self, h):
        if self.y-h < 62:
            self._footer(); self.c.showPage(); self.page += 1; self._header()

    def section(self, title, color=GREEN):
        self.ensure(35)
        self.space(9)
        self.c.setFillColor(color); self.c.roundRect(self.margin, self.y-2, 4, 17, 2, fill=1, stroke=0)
        self.c.setFillColor(INK); self.c.setFont('Decision-Bold', 12)
        self.c.drawString(self.margin+13, self.y+1, title)
        self.y -= 26

    def text(self, value, size=9, color=INK, gap=7):
        style = ParagraphStyle('body', fontName='Decision', fontSize=size, leading=size*1.42,
                               textColor=color, alignment=TA_LEFT)
        p = Paragraph(str(value).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'), style)
        _, h = p.wrap(self.w-2*self.margin, self.h)
        self.ensure(h+gap)
        p.drawOn(self.c, self.margin, self.y-h)
        self.y -= h+gap

    def metrics(self, items):
        self.ensure(74)
        gap = 8; card_w = (self.w-2*self.margin-gap*(len(items)-1))/len(items)
        for i,(label,val,accent) in enumerate(items):
            x = self.margin+i*(card_w+gap)
            self.c.setFillColor(PAPER); self.c.roundRect(x,self.y-64,card_w,64,7,fill=1,stroke=0)
            self.c.setFillColor(accent); self.c.setFont('Decision-Bold', 15)
            self.c.drawString(x+10,self.y-30,str(val))
            self.c.setFillColor(MUTED); self.c.setFont('Decision', 7)
            self.c.drawString(x+10,self.y-48,str(label))
        self.y -= 73

    def row(self, label, before, after, color=GREEN):
        self.ensure(33)
        self.c.setFont('Decision-Bold',8.5); self.c.setFillColor(INK)
        self.c.drawString(self.margin,self.y,label[:42])
        self.c.setFont('Decision',8); self.c.setFillColor(MUTED)
        self.c.drawRightString(self.w-self.margin,self.y,f'{before}  →  {after}')
        self.c.setStrokeColor(LINE); self.c.line(self.margin,self.y-8,self.w-self.margin,self.y-8)
        self.y -= 24

    def bar(self, label, pct, color=GREEN, suffix=None):
        self.ensure(30)
        self.c.setFont('Decision',8.5); self.c.setFillColor(INK)
        self.c.drawString(self.margin,self.y,label[:37])
        self.c.setFillColor(LINE); self.c.roundRect(self.margin+165,self.y-2,235,8,4,fill=1,stroke=0)
        self.c.setFillColor(color); self.c.roundRect(self.margin+165,self.y-2,max(1,min(235,235*max(0,pct)/100)),8,4,fill=1,stroke=0)
        self.c.setFont('Decision-Bold',8); self.c.setFillColor(color)
        self.c.drawRightString(self.w-self.margin,self.y,suffix or f'%{_fmt(pct,1)}')
        self.y -= 25

    def callout(self, title, body, color=BLUE):
        style = ParagraphStyle('callout',fontName='Decision',fontSize=8.5,leading=12,textColor=INK)
        p=Paragraph(body.replace('&','&amp;'),style)
        _,h=p.wrap(self.w-2*self.margin-30,self.h)
        total=h+31
        self.ensure(total)
        self.c.setFillColor(PAPER); self.c.roundRect(self.margin,self.y-total+3,self.w-2*self.margin,total,6,fill=1,stroke=0)
        self.c.setFillColor(color); self.c.rect(self.margin,self.y-total+3,3,total,fill=1,stroke=0)
        self.c.setFont('Decision-Bold',9); self.c.drawString(self.margin+13,self.y-16,title)
        p.drawOn(self.c,self.margin+13,self.y-23-h)
        self.y -= total+6

    def monthly(self, rows, critical_month, critical_basis=None):
        if not rows:return
        self.ensure(95)
        self.c.setFillColor(INK); self.c.setFont('Decision-Bold',9)
        self.c.drawString(self.margin,self.y,'AYLIK YENİ SU GEREĞİ')
        peak=max(0.01,*(float(row.get('demand_m3',0) or 0) for row in rows))
        names=['Oca','Şub','Mar','Nis','May','Haz','Tem','Ağu','Eyl','Eki','Kas','Ara']
        slot=(self.w-2*self.margin)/12
        for row in rows:
            month=int(row.get('month',0) or 0)
            if not 1<=month<=12:continue
            x=self.margin+(month-1)*slot+5
            demand=float(row.get('demand_m3',0) or 0)
            height=32*demand/peak
            self.c.setFillColor(AMBER if month==critical_month else BLUE)
            self.c.roundRect(x,self.y-53,slot-10,max(1,height),2,fill=1,stroke=0)
            self.c.setFillColor(MUTED);self.c.setFont('Decision',7)
            self.c.drawCentredString(x+(slot-10)/2,self.y-65,names[month-1])
        self.c.setFillColor(MUTED);self.c.setFont('Decision',7.5)
        basis='günlük tekrarda' if critical_basis=='MAX_MODEL_CLIMATOLOGICAL_MONTH_FROM_DAILY_REPLAY' else 'aylık ortalama planda'
        self.c.drawString(self.margin,self.y-79,f'Sarı: {basis} en yüksek yedek gereği. Sütunlar aylık plan talebidir.')
        self.y-=95

    def finish(self):
        self._footer(); self.c.save(); return self.buffer.getvalue()


def turkey_pdf(context, result):
    region=context['region']; request=result['request']; optimized=result.get('optimized')
    if not optimized:
        raise ValueError('PDF için uygulanabilir öneri bulunamadı.')
    name=region['name']; year=region['year']
    r=Report('turkiye',f'{name} | karar raporu',f'{year} mevcut ürün deseni  →  seçili koşullarda önerilen desen')
    partial=result['status']=='partial_conditional'
    water_key='known_water_m3' if partial else 'water_m3'
    base=result['baseline']['totals'].get(water_key); current=result['current']['totals'].get(water_key); new=optimized['totals'].get(water_key)
    saving=(current-new)/current*100 if current and new is not None else None
    r.metrics([('MEVCUT EKİLİ ALAN',f'{_fmt(request["land_area_ha"],0)} ha',GREEN),
               ('KAPSAMDAKİ MODEL SUYU' if partial else 'MODEL SU GEREĞİ',f'{_fmt(new/1e6,1)} milyon m³' if new is not None else '—',BLUE),
               ('KAPSAMDAKİ EK ETKİ' if partial else 'DESENİN EK ETKİSİ',f'%{_fmt(saving,1)} daha az' if saving is not None else '—',GREEN if saving is not None and saving>=0 else RED)])
    r.callout('KARAR',f'Seçili iklim ve sulama koşullarında kaynaklı {year} desenini önerilen ürün paylarına dönüştür. Su farkı modelin hesapladığı sulama gereksinimidir; ölçülmüş tasarruf veya resmî tahsis değildir.',GREEN)
    if partial:
        held=', '.join(result.get('regional_scope',{}).get('held_crop_ids',[]))
        r.callout('KAPSAM SINIRI',f'Su katsayısı eksik {held} mevcut alanda sabit tutuldu. Verilen su miktarı ve yüzde yalnız suyu hesaplanan ürünlerin alt kapsamıdır; bölgenin toplam su gereği veya tasarrufu değildir.',AMBER)
    r.section('1  /  Mevcut desen → önerilen desen')
    old={c['crop_id']:c for c in result['baseline']['crops']}
    crops=sorted(optimized['crops'],key=lambda c:abs(c['delta_area_ha']),reverse=True)
    for c in crops:
        old_area=old.get(c['crop_id'],{}).get('area_ha',c['current_area_ha'])
        old_pct=100*old_area/request['land_area_ha'] if request['land_area_ha'] else 0
        r.row(c['name_tr'],f'%{_fmt(old_pct)}',f'%{_fmt(c["area_share_pct"])}  ({"+" if c["delta_area_ha"]>0 else ""}{_fmt(c["delta_area_ha"],0)} ha)',GREEN if c['delta_area_ha']>=0 else AMBER)
    r.section('2  /  Su yönetimi',BLUE)
    if base is not None and current is not None and new is not None:
        r.bar('Kaynak başlangıcına göre seçili koşul',current/base*100 if base else 0,BLUE,f'{_fmt(current/1e6,1)} milyon m³')
        r.bar('Önerilen desenin gereği',new/base*100 if base else 0,GREEN,f'{_fmt(new/1e6,1)} milyon m³')
        r.text(f'Senaryo koşulları: sıcaklık {request.get("temperature_delta_c",0):+.1f} °C, yağış çarpanı {_fmt(request["rainfall_factor"]*100,0)}%, sulama verimi {_fmt(request["irrigation_efficiency"]*100,0)}%. Ürün deseninin ek etkisi, seçili koşullardaki mevcut desen ile karşılaştırılır; yüzdeler toplanmaz.')
    else:
        r.text('Su katsayısı eksik ürünler bulunduğu için toplam su farkı verilmez. Eksik değer sıfır kabul edilmedi.')
    r.section('3  /  Karar verici için eylemler')
    for c in crops[:4]:
        delta=c['delta_area_ha']; verb='Artır' if delta>1e-4 else 'Azalt' if delta< -1e-4 else 'Koru'
        r.text(f'{verb}: {c["name_tr"]} alanı {abs(delta):,.0f} ha ({_fmt(c["area_share_pct"])}% önerilen pay).')
    r.callout('UYGULAMA EŞİĞİ','Yerel tahsis, gerçek parsel koşulları, ürün alım piyasası ve çiftçi maliyetleri doğrulanmadan nihai ekiliş kararı verme. Bu rapor ekonomik kâr garantisi üretmez.',AMBER)
    r.ensure(250)
    r.section('4  /  Kısıtlar ve kanıt')
    for constraint in result.get('constraints',[]):
        if constraint.get('binding'):
            r.text(f'Bağlayıcı: {constraint.get("label",constraint["id"])} · kullanılan {_fmt(constraint.get("used"))} / sınır {_fmt(constraint.get("capacity"))}.',8)
    sources=region.get('sources',[])
    r.text(f'Ürün alanı / üretim kaynağı: {year} resmî bölge verisi ({len(sources)} kaynak kaydı). İklim ve ürün su hesabı: rapordaki model sürümü ve kaynaklı veri katmanları. Simülasyon sınıfı: {result["classification"]}.',8,MUTED)
    r.section('5  /  Kaynak ve hesap zinciri',BLUE)
    for source in sources[:4]:
        r.text(f'{source.get("publisher","Resmî veri")}: {source.get("title",source.get("id","Kaynak"))} · {source.get("year",year)}. {source.get("url","")}',7.7,MUTED)
    r.text('Ekili alan payı resmî ürün alanından türetilir. İklim seçimi ET₀ / ürün su gereği hesabına aktarılır. Aynı alan ve açık üretim kısıtları altında çözücü önerilen alanları hesaplar; bu öneri saha ölçümü değildir.',8)
    r.section('6  /  Doğrulama gereksinimi',AMBER)
    r.text('Karar öncesi su tahsisi, sulama şebekesi/verimi, parsel verimi ve çiftçi maliyetleri yerel kurumlarla doğrulanmalı. Özellikle fiyat ve satış verisi bu motorun amaç fonksiyonunda olmadığı için gelir/kâr sonucu çıkarılamaz.',8)
    for limit in result.get('limitations',[])[:4]:r.text('Sınır: '+str(limit),7.8,MUTED)
    return r.finish()


def north_pdf(result):
    req=result['request']; year=req.get('target_year') or result['climate'].get('period')
    story=result['decision_story']; water=story['water_security']; production=story['production']; totals=result['plan']['totals']
    r=Report('north',f'{year} | Geleceğin üretim ve su yönetimi planı','Longyearbyen · koşullu gelecek simülasyonu · SSP ve planlama ölçeği rapor girdilerindedir')
    r.metrics([('ÜRETİM ALANI',f'{_fmt(req["area_m2"],0)} m²',GREEN),
               ('YILLIK YENİ SU',f'{_fmt(totals["water_m3"])} m³',BLUE),
               ('MODEL HASADI',f'{_fmt(totals["production_kg"],0)} kg',GREEN)])
    sources=water['sources']; used=[s for s in sources if (s.get('m3') or 0)>1e-7]
    source_line='; '.join(f'{s["label"]}: {_fmt(s["m3"])} m³/yıl' for s in used) or 'Pozitif kaynak tahsisi hesaplanmadı'
    r.callout('SU YÖNETİMİ PLANI',source_line+'. Bunlar seçilen toplama, depo ve tahsis koşullarında model sonucudur; doğrulanmış yerel su hakkı değildir.',BLUE)
    r.section('1  /  Su kaynakları ve mevsimsel güvenlik',BLUE)
    for src in sources:
        if src.get('m3',0)>0:r.bar(src['label'],src['share_pct'],BLUE if src['id']=='desalinated_seawater' else GREEN,f'{_fmt(src["m3"])} m³ · %{_fmt(src["share_pct"])}')
    critical=water['critical_month'] or {}; storage=water['storage']; backup=water['backup']
    r.row('En yüksek yedek gereği',critical.get('label','Yok'),f'{_fmt(critical.get("backup_m3"))} m³, çatı/depo sonrası' if critical else 'Sınanan koşulda bulunmadı',BLUE)
    r.row('Senaryo depo kapasitesi',f'{_fmt(storage.get("configured_m3"))} m³','Asgari boyut hesaplanmadı',BLUE)
    r.text('Kar/yağışın fiziksel varlığı üretimde kullanılabilir su demek değildir. Toplama, mevsim, depo, erişim, kalite, arıtma ve enerji zinciri ayrı doğrulanır. İlk model yılı boş depo ile başlar; bu kurak yıl kanıtı değildir.')
    r.section('2  /  Ürün ve üretim yöntemi')
    area=req['area_m2']
    for c in production['crops']:
        pct=100*c['area_m2']/area if area else 0
        r.bar(c['name'],pct,GREEN,f'%{_fmt(pct)} · {_fmt(c["production_kg"],0)} kg')
    method_names={'hydroponics':'Topraksız kontrollü üretim','greenhouse':'Güneş alan sera','open_field':'Açık tarla'}
    for m in production['methods']:
        if m['area_m2']>0:r.text(f'{method_names.get(m["id"],m["id"])}: {_fmt(m["area_m2"])} m² ({_fmt(100*m["area_m2"]/area)}% alan).',8)
    r.space(10)
    r.monthly(result['plan'].get('monthly',[]),critical.get('month'),critical.get('basis'))
    r.ensure(155)
    r.section('3  /  Enerji ve uygulanabilirlik',AMBER)
    r.metrics([('ELEKTRİK EŞDEĞERİ',f'{_fmt(totals["equivalent_electricity_kwh"],0)} kWh/y',AMBER),
               ('ARITMA ELEKTRİĞİ',f'{_fmt(totals["treatment_electricity_kwh"],0)} kWh/y',BLUE)])
    r.text('Elektrik eşdeğeri, ısıtma ve diğer enerji gereğini karşılaştırılabilir yıllık elektrik yüküne dönüştürür; saha şebeke kapasitesi veya maliyet hesabı değildir. Güç, süreklilik ve yerel enerji kaynağı ayrıca doğrulanır.')
    r.section('4  /  Saha ve kontrollü tarım testleri',BLUE)
    r.callout('SAHADA SINANACAK GİRDİLER','Bilgisayarda gelecek iklimi, seçili su/depo/arıtma senaryoları ve ürün dağılımı hesaplanabilir. Kaynak suyunun sefer zamanındaki sıcaklığı, tuzluluğu ve kimyası; yerel toplama/erişim ve üretim performansı ayrıca doğrulanır.',BLUE)
    r.text('Polar Water Node (PWN), farklı derinliklerdeki su özelliklerini ölçüp kaydetmek için geliştirdiğimiz taşınabilir ölçüm cihazıdır. v0.1 kayıt/analiz yazılımı mevcut; fiziksel tank veya Arktik ölçümü doğrulanmış değildir.')
    r.text('Arktik sürümü hedefi: eşleşmiş konum/zamanda sıcaklık, iletkenlik, basınç, uygun tuzluluk/derinlik hesabı, UTC/konum ve kalite kaydı. Son deniz mühendisliği uzman/sefer görüşüyle belirlenecek.')
    r.text('Ayrı fiziksel su numunesi: Kaynak kullanılabilirliği ve seçilmiş arıtma kimyası izinli uzman/laboratuvar protokolüyle test edilecek; panel ve numune sayısı henüz kesin değildir.')
    r.text('Kar/yağış ve karasal su: Mevsimsel toplama, depo, erişim ve tahsisi ayrı hidroloji/altyapı çalışmasıyla doğrula. PWN yıllık karasal tatlı su miktarını ölçmez.')
    r.text('Kontrollü üretim deneyi: Mevcut topraksız düzenek seçilen ürün/koşula uyarlanacak. Uygun işlem görmüş numune veya açıkça etiketli yeniden oluşturulmuş suyla yeni su, elektrik, ayrı ısı ve hasat ölçülecek; henüz deney ölçümü yoktur. Tek pilot tüm Arktik tarımını doğrulamaz.')
    r.section('5  /  Karar ve kanıt sınırı')
    r.text('Sefer öncesi planı ve model beklentisini dondur; yalnız eşleşmiş gözlemin desteklediği girdiyi güncelle; aynı optimizasyon motorunu yeniden çalıştır. Ürün payının değişmemesi de geçerli sonuçtur.')
    r.text(f'{year} çıktısı üç CMIP6 modelinin tekil model yılına dayalı koşullu simülasyondur; ölçülmüş {year} havası veya gelecekteki kesin hasat değildir. Depo, enerji, verim ve su kaynağı katsayıları açık senaryo/analoglardır.',8,MUTED)
    for limit in story.get('limitations',[])[:4]:r.text('Sınır: '+str(limit),7.8,MUTED)
    return r.finish()
