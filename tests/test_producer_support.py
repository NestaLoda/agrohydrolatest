import math

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError
import pytest

from backend.producer_support import ProducerScenario, calculate_scenario, router


def inputs(**changes):
    values = dict(currency='TRY', production_kg=1000., loss_pct=10., buyer_capacity_kg=800.,
                  price_per_kg=20., operating_cost=10000., capital_cost=10000.,
                  equipment_discount_pct=20., annualization_years=5., annual_program_fee=200.)
    values.update(changes)
    return values


def result(**changes):
    return calculate_scenario(ProducerScenario(**inputs(**changes)))


def test_annual_arithmetic_and_discount_not_double_counted():
    r = result()
    s = r['supported']
    assert s['lost_kg'] == 100
    assert s['marketable_kg'] == 900
    assert s['saleable_kg'] == 800
    assert s['unsold_kg'] == 100
    assert s['revenue'] == 16000
    assert s['operating_balance'] == 5800
    assert s['annualized_capital'] == 1600
    assert s['scenario_balance'] == 4200
    assert r['baseline']['scenario_balance'] == 4000
    assert r['support_effect']['one_time_equipment_discount'] == 2000
    assert r['support_effect']['annualized_discount'] == 400
    assert r['support_effect']['annual_balance_change'] == 200
    assert s['break_even_price'] == 14.75
    assert s['break_even_sales_kg'] == 590
    assert s['break_even_feasible']
    assert not r['contracts_verified'] and not r['investment_recommendation'] and not r['optimizer_output']
    assert r['classification'] == 'USER_SCENARIO'


@pytest.mark.parametrize('changes', [dict(production_kg=0), dict(buyer_capacity_kg=0), dict(loss_pct=100)])
def test_no_sales_never_invents_break_even_price(changes):
    s = result(**changes)['supported']
    assert s['saleable_kg'] == s['revenue'] == 0
    assert s['break_even_price'] is None
    assert not s['break_even_feasible']
    assert s['break_even_status'] == 'NO_SALES'


def test_zero_price_and_zero_cost():
    s = result(price_per_kg=0)['supported']
    assert s['break_even_sales_kg'] is None
    assert not s['break_even_feasible']
    assert s['break_even_status'] == 'ZERO_PRICE'
    free = result(price_per_kg=0, operating_cost=0, capital_cost=0, annual_program_fee=0)['supported']
    assert free['break_even_sales_kg'] == 0 and free['break_even_feasible']
    assert free['break_even_status'] == 'NO_COST_TO_RECOVER'


def test_stress_holds_buyer_capacity_and_changes_only_named_inputs():
    r = result()
    variants = {v['id']: v['result'] for v in r['stress_scenarios']}
    assert variants['production_down_20']['saleable_kg'] == 720
    assert variants['production_down_20']['price_per_kg'] == 20
    assert variants['price_down_20']['saleable_kg'] == 800
    assert variants['price_down_20']['revenue'] == 12800
    assert variants['operating_cost_up_20']['operating_cost'] == 12000
    assert variants['combined']['revenue'] == 11520
    assert variants['combined']['scenario_balance'] == -2280
    assert 'STRESS_VULNERABILITY' in {a['code'] for a in r['actions']}


def test_negative_margin_requires_revision_and_capacity_gap_is_explicit():
    r = result(buyer_capacity_kg=100)
    assert r['supported']['scenario_balance'] < 0
    assert not r['supported']['break_even_feasible']
    assert r['supported']['break_even_status'] == 'EXCEEDS_SCENARIO_CAPACITY'
    codes = {a['code'] for a in r['actions']}
    assert {'MATCH_BUYER_CAPACITY', 'REVISE_NEGATIVE_BALANCE'} <= codes


def test_fee_can_exceed_discount_and_no_support_throughput_claim():
    r = result(annual_program_fee=1000)
    assert r['support_effect']['annual_balance_change'] == -600
    assert 'REVIEW_PROGRAM_FEE' in {a['code'] for a in r['actions']}
    for key in ('production_kg', 'marketable_kg', 'saleable_kg', 'unsold_kg', 'revenue'):
        assert r['baseline'][key] == r['supported'][key]


@pytest.mark.parametrize('field', [k for k in inputs() if k != 'currency'])
@pytest.mark.parametrize('bad', ['', None, True, '1', math.nan, math.inf, -math.inf, -1])
def test_invalid_numeric_values_rejected(field, bad):
    with pytest.raises(ValidationError):
        ProducerScenario(**inputs(**{field: bad}))


@pytest.mark.parametrize('changes', [dict(loss_pct=101), dict(equipment_discount_pct=101),
                                  dict(annualization_years=0), dict(annualization_years=101),
                                  dict(currency='USD'), dict(period='month'), dict(unit='tonnes')])
def test_invalid_scopes_and_limits_rejected(changes):
    with pytest.raises(ValidationError):
        ProducerScenario(**inputs(**changes))


def test_omitted_fields_are_not_zero_or_example_defaults():
    with pytest.raises(ValidationError):
        ProducerScenario(currency='TRY')


def test_router_strict_payload_and_success():
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)
    assert client.post('/api/producer-support/scenario', json={}).status_code == 422
    assert client.post('/api/producer-support/scenario', json=inputs(price_per_kg='')).status_code == 422
    response = client.post('/api/producer-support/scenario', json=inputs())
    assert response.status_code == 200
    assert response.json()['supported']['scenario_balance'] == 4200


def test_currency_only_labels_and_no_exchange_rate():
    a, b = result(currency='TRY'), result(currency='EUR')
    assert a['supported'] == b['supported']
    assert b['input']['currency'] == 'EUR'
