from io import BytesIO
from copy import deepcopy

from pypdf import PdfReader

from backend.decision_pdf import turkey_pdf, north_pdf, _fmt
from backend.planning import planning_context, simulate
from backend.planning_contracts import SimulationRequest
from backend.north_api import calculate
from backend.north_contracts import NorthRequest


def pdf_text(content):
    assert content.startswith(b'%PDF-')
    reader = PdfReader(BytesIO(content))
    assert 1 <= len(reader.pages) <= 4
    return '\n'.join(page.extract_text() for page in reader.pages)


def test_turkey_report_matches_optimizer_and_labels_modelled_water():
    context = planning_context('konya')
    result = simulate(SimulationRequest.model_validate(context['default_scenario']))
    text = pdf_text(turkey_pdf(context, result))
    expected = result['optimized']['totals']['water_m3']/1e6
    assert _fmt(expected, 1) in text
    assert 'Mevcut desen' in text and 'önerilen desen' in text
    assert 'ölçülmüş tasarruf' in text
    assert result['optimized']['crops'][0]['name_tr'] in text


def test_partial_turkey_report_limits_water_claim_to_known_subset():
    context = planning_context('trakya_edirne')
    result = simulate(SimulationRequest.model_validate(context['default_scenario']))
    assert result['status'] == 'partial_conditional'
    text = ' '.join(pdf_text(turkey_pdf(context, result)).split())
    assert 'KAPSAM SINIRI' in text
    assert 'bölgenin toplam su gereği veya tasarrufu değildir' in text


def test_north_report_matches_water_allocation_and_field_boundary():
    result = calculate(NorthRequest(target_year=2026))
    text = pdf_text(north_pdf(result))
    assert _fmt(result['plan']['totals']['water_m3']) in text
    assert _fmt(result['plan']['totals']['stored_water_m3']) in text
    normalized = ' '.join(text.split())
    assert 'PWN yıllık karasal tatlı su miktarını ölçmez' in normalized
    assert 'model yılına dayalı koşullu simülasyondur' in normalized
    assert 'Geleceğin üretim ve su yönetimi planı' in normalized
    assert 'fiziksel tank veya Arktik ölçümü doğrulanmış değildir' in normalized


def test_north_report_does_not_prescribe_unused_desalination_or_fake_critical_month():
    result = calculate(NorthRequest(target_year=2051))
    assert result['plan']['totals']['desalinated_m3'] == 0
    text = ' '.join(pdf_text(north_pdf(result)).split())
    assert 'açığı arıtılmış deniz suyuyla tamamla' not in text
    assert 'Arıtılmış deniz suyu:' not in text
    missing = deepcopy(result)
    missing['decision_story']['water_security']['critical_month'] = None
    text = ' '.join(pdf_text(north_pdf(missing)).split())
    assert 'Sınanan koşulda bulunmadı' in text
