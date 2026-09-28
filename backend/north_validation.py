"""Field readiness and bounded sample/pilot review. Never updates the optimizer.

Accepted evidence is a submitter declaration, not independent lab verification.
Only north_field's restricted PRE/POST path can update source-water model inputs.
"""
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Literal
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field, model_validator

from .provenance import ROOT, canonical, digest, immutable_write

router = APIRouter(prefix='/api/north/validation', tags=['north-validation'])
RECORD_DIR = ROOT / 'data/north/validation_records'
TEMPLATE_DIR = ROOT / 'data/north/validation_templates'


class StrictRecord(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False, str_strip_whitespace=True)


def utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset().total_seconds() != 0:
        raise ValueError('Zaman UTC ve saat dilimiyle kaydedilmeli.')
    return value


class Evidence(StrictRecord):
    record_id: str = Field(min_length=3, max_length=200)
    content_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')
    reviewer: str = Field(min_length=3, max_length=200)
    quality: Literal['accepted']
    classification: Literal['observed']


class Measurement(StrictRecord):
    parameter: str = Field(min_length=2, max_length=100)
    value: float
    unit: str = Field(min_length=1, max_length=50)
    uncertainty: float = Field(ge=0)
    method: str = Field(min_length=3, max_length=500)
    instrument_id: str = Field(min_length=2, max_length=100)
    calibration_record: str = Field(min_length=3, max_length=500)
    evidence: Evidence


class ReviewCriterion(StrictRecord):
    parameter: str = Field(min_length=2, max_length=100)
    unit: str = Field(min_length=1, max_length=50)
    minimum: float | None = None
    maximum: float | None = None
    decision_link: str = Field(min_length=10, max_length=1000)
    source: str = Field(min_length=10, max_length=1000)

    @model_validator(mode='after')
    def valid_range(self):
        if self.minimum is None and self.maximum is None:
            raise ValueError('En az bir kaynaklı değerlendirme sınırı gerekli.')
        if self.minimum is not None and self.maximum is not None and self.minimum > self.maximum:
            raise ValueError('Alt sınır üst sınırı aşamaz.')
        return self


class SampleReview(StrictRecord):
    sample_id: str = Field(min_length=3, max_length=100)
    source_kind: Literal['seawater', 'freshwater', 'rainwater', 'snowmelt', 'reconstructed']
    source_connection: str = Field(min_length=10, max_length=2000)
    collected_at_utc: datetime
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    depth_m: float | None = Field(None, ge=0, le=10000)
    permit_record: str = Field(min_length=3, max_length=1000)
    custody_record: str = Field(min_length=3, max_length=1000)
    protocol_record: str = Field(min_length=3, max_length=1000)
    expert_reviewer: str = Field(min_length=3, max_length=200)
    intended_use: str = Field(min_length=10, max_length=1000)
    reconstruction_record: str | None = Field(None, min_length=10, max_length=2000)
    measurements: list[Measurement] = Field(default_factory=list, max_length=30)
    criteria: list[ReviewCriterion] = Field(min_length=1, max_length=30)

    @model_validator(mode='after')
    def sample_identity(self):
        if utc(self.collected_at_utc) > datetime.now(timezone.utc):
            raise ValueError('Gelecekteki numune gerçek ölçüm olarak girilemez.')
        if self.source_kind == 'reconstructed' and not self.reconstruction_record:
            raise ValueError('Yeniden oluşturulmuş suyun reçetesi ve kaynak kimya kaydı gerekli.')
        for rows in (self.measurements, self.criteria):
            keys = [row.parameter for row in rows]
            if len(keys) != len(set(keys)):
                raise ValueError('Aynı parametre iki kez girilemez; tekrarlar ayrı örnek kaydı olmalı.')
        return self


def assess_sample(request: SampleReview) -> dict:
    measured = {item.parameter: item for item in request.measurements}
    rows = []
    for criterion in request.criteria:
        item = measured.get(criterion.parameter)
        row = {**criterion.model_dump(), 'measurement': item.model_dump() if item else None}
        if item is None:
            row['status'] = 'measurement_needed'
        elif item.unit != criterion.unit:
            row['status'] = 'unit_mismatch'
        else:
            low, high = item.value - item.uncertainty, item.value + item.uncertainty
            outside = (criterion.minimum is not None and high < criterion.minimum) or (criterion.maximum is not None and low > criterion.maximum)
            contained = (criterion.minimum is None or low >= criterion.minimum) and (criterion.maximum is None or high <= criterion.maximum)
            row['status'] = 'outside_selected_range' if outside else ('within_selected_range' if contained else 'uncertainty_crosses_limit')
        rows.append(row)
    statuses = {row['status'] for row in rows}
    status = 'selected_checks_met' if statuses == {'within_selected_range'} else ('treatment_or_use_review_needed' if 'outside_selected_range' in statuses else 'further_evidence_needed')
    payload = request.model_dump(mode='json')
    return {'classification': 'SUBMITTED_SAMPLE_SCOPE_REVIEW', 'sample_id': request.sample_id,
            'source_kind': request.source_kind, 'status': status, 'checks': rows,
            'unassessed_parameters': sorted(set(measured) - {c.parameter for c in request.criteria}),
            'request_sha256': digest(canonical(payload).encode()), 'updated_model_inputs': [],
            'limits': ['Yalnız uzman tarafından verilen kullanım amacı ve sınırlar değerlendirildi; genel tarımsal uygunluk veya içilebilirlik belgesi değildir.',
                       'Kalite kabulü ve belge özeti gönderenin beyanıdır; yazılım laboratuvarı veya belge içeriğini bağımsız doğrulamaz.',
                       'EC, pratik tuzluluk ve g/kg birbirinin yerine kullanılmaz; otomatik birim dönüşümü yapılmaz.',
                       'Deniz numunesi kar/yağış suyunu temsil etmez; numune yıllık su hacmini veya gelecek iklimini doğrulamaz.']}


class PilotTotals(StrictRecord):
    new_water_m3: float = Field(ge=0, le=1e9)
    electricity_kwh: float = Field(ge=0, le=1e12)
    heat_kwh_th: float = Field(ge=0, le=1e12)
    harvested_fresh_mass_kg: float = Field(ge=0, le=1e9)


class PilotDesign(StrictRecord):
    crop_id: str = Field(min_length=2, max_length=100)
    production_method: Literal['greenhouse', 'hydroponics', 'controlled_environment']
    water_origin: Literal['arctic_sample', 'reconstructed', 'local_control']
    source_water_record: str = Field(min_length=10, max_length=1000)
    treatment_record: str = Field(min_length=10, max_length=1000)
    protocol_record: str = Field(min_length=10, max_length=1000)
    model_run_record: str = Field(min_length=10, max_length=1000)
    area_m2: float = Field(gt=0, le=10000)
    duration_days: float = Field(gt=0, le=1000)
    measurement_boundary: Literal['whole_pilot_including_water_treatment']
    expected: PilotTotals


class PilotObservation(StrictRecord):
    freeze_id: str = Field(pattern=r'^[0-9a-f]{32}$')
    started_at_utc: datetime
    ended_at_utc: datetime
    area_m2: float = Field(gt=0, le=10000)
    measurement_boundary: Literal['whole_pilot_including_water_treatment']
    protocol_record: str = Field(min_length=10, max_length=1000)
    calibration_record: str = Field(min_length=10, max_length=1000)
    source_water_record: str = Field(min_length=10, max_length=1000)
    treatment_record: str = Field(min_length=10, max_length=1000)
    evidence: Evidence
    measured: PilotTotals
    deviations: str = Field(min_length=3, max_length=4000)


def freeze_pilot(request: PilotDesign, directory: Path = RECORD_DIR) -> dict:
    record = {'id': uuid4().hex, 'created_at_utc': datetime.now(timezone.utc).isoformat(),
              'classification': 'PILOT_PRE_MEASUREMENT_EXPECTATION', 'design': request.model_dump(mode='json')}
    raw = canonical(record).encode()
    immutable_write(Path(directory) / (record['id'] + '.json'), raw)
    immutable_write(Path(directory) / (record['id'] + '.sha256'), digest(raw).encode())
    return {**record, 'sha256': digest(raw), 'freeze_id': record['id']}


def compare_pilot(request: PilotObservation, directory: Path = RECORD_DIR) -> dict:
    path = Path(directory) / (request.freeze_id + '.json')
    if not path.exists() or not path.with_suffix('.sha256').exists():
        raise ValueError('Ölçümden önce dondurulmuş pilot beklentisi bulunamadı.')
    raw = path.read_bytes()
    if digest(raw) != path.with_suffix('.sha256').read_text().strip():
        raise ValueError('Dondurulmuş pilot beklentisinin özeti uyuşmuyor.')
    record = json.loads(raw)
    if record.get('classification') != 'PILOT_PRE_MEASUREMENT_EXPECTATION':
        raise ValueError('Kayıt bir pilot beklentisi değil.')
    design = PilotDesign.model_validate(record['design'])
    start, end = utc(request.started_at_utc), utc(request.ended_at_utc)
    if start <= datetime.fromisoformat(record['created_at_utc']) or end <= start or end > datetime.now(timezone.utc):
        raise ValueError('Gerçek pilot ölçümü dondurmadan sonra başlamalı ve bugün itibarıyla tamamlanmış olmalı.')
    duration = (end - start).total_seconds() / 86400
    if abs(duration - design.duration_days) > 1e-6 or abs(request.area_m2 - design.area_m2) > 1e-6:
        raise ValueError('Süre ve alan dondurulmuş pilotla eşleşmeli; yıllık model toplamı kısa deneye doğrudan karşılaştırılmaz.')
    for key in ('measurement_boundary', 'protocol_record', 'source_water_record', 'treatment_record'):
        if getattr(request, key) != getattr(design, key):
            raise ValueError(f'Pilot kayıt kapsamı değişmiş: {key}. Ayrı tasarım veya belgeli yeni çalışma gerekli.')
    measured, expected = request.measured.model_dump(), design.expected.model_dump()
    units = {'new_water_m3': 'm³', 'electricity_kwh': 'kWh', 'heat_kwh_th': 'kWh_th', 'harvested_fresh_mass_kg': 'kg'}
    comparisons = [{'metric': key, 'unit': units[key], 'expected': expected[key], 'observed': value,
                    'delta': value - expected[key], 'delta_percent': 100 * (value - expected[key]) / expected[key] if expected[key] else None}
                   for key, value in measured.items()]
    def intensities(totals):
        mass = totals['harvested_fresh_mass_kg']
        return {key: totals[key] / mass if mass else None for key in ('new_water_m3', 'electricity_kwh', 'heat_kwh_th')}
    result = {'classification': 'SUBMITTED_PILOT_MODEL_OBSERVATION_COMPARISON', 'pre_id': record['id'],
              'water_origin': design.water_origin, 'comparisons': comparisons,
              'per_kg_fresh_mass': {'expected': intensities(expected), 'observed': intensities(measured)},
              'updated_model_inputs': [], 'evidence': request.evidence.model_dump(), 'deviations': request.deviations,
              'limits': ['Bu çalışma kaynak suyu → arıtma → kontrollü üretim uyumunu sınar; gelecekteki Arktik tarımın tamamını doğrulamaz.',
                         'Tek pilot karşılaştırması istatistiksel doğrulama değildir; tekrar, kontrol ve belirsizlik uzman protokolünde tasarlanmalı.',
                         'Yeni su dışarıdan eklenen sudur; devridaim akışı yeniden yeni su diye sayılmaz. Elektrik ve ısı ayrı tutulur.',
                         'Kayıt ve kalite kabulü gönderenin beyanıdır; ölçümler yazılım tarafından bağımsız teyit edilmedi.']}
    post = {'id': uuid4().hex, 'created_at_utc': datetime.now(timezone.utc).isoformat(),
            'request': request.model_dump(mode='json'), 'result': result}
    encoded = canonical(post).encode()
    immutable_write(Path(directory) / (post['id'] + '.json'), encoded)
    immutable_write(Path(directory) / (post['id'] + '.sha256'), digest(encoded).encode())
    return {**result, 'post_id': post['id'], 'sha256': digest(encoded)}


@router.get('/readiness')
def readiness():
    return json.loads((TEMPLATE_DIR / 'readiness.json').read_text(encoding='utf-8'))


@router.get('/templates')
def templates():
    return {'classification': 'BLANK_PROTOCOL_TEMPLATES_NOT_OBSERVATIONS',
            'sample_review_json_schema': SampleReview.model_json_schema(),
            'pilot_design_json_schema': PilotDesign.model_json_schema(),
            'pilot_observation_json_schema': PilotObservation.model_json_schema(),
            'csv_templates': {path.name: path.read_text(encoding='utf-8') for path in sorted(TEMPLATE_DIR.glob('*.csv'))}}


@router.post('/sample-review')
def sample_endpoint(request: SampleReview):
    return assess_sample(request)


@router.post('/pilot/freeze')
def freeze_endpoint(request: PilotDesign):
    return freeze_pilot(request)


@router.post('/pilot/compare')
def compare_endpoint(request: PilotObservation):
    try:
        return compare_pilot(request)
    except (ValueError, FileNotFoundError) as exc:
        raise HTTPException(422, str(exc)) from exc
