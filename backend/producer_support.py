"""Annual producer-support scenarios, separate from agronomic optimization.

Every price, quantity and cost is a user's scenario input. No sale, yield,
partner, insurance cover or investment return is verified by this calculator.
"""
from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field


router = APIRouter(prefix='/api/producer-support', tags=['producer-support'])


class ProducerScenario(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True, allow_inf_nan=False)

    currency: Literal['TRY', 'EUR']
    production_kg: float = Field(ge=0, le=1e12)
    loss_pct: float = Field(ge=0, le=100)
    buyer_capacity_kg: float = Field(ge=0, le=1e12)
    price_per_kg: float = Field(ge=0, le=1e12)
    operating_cost: float = Field(ge=0, le=1e12)
    capital_cost: float = Field(ge=0, le=1e12)
    equipment_discount_pct: float = Field(ge=0, le=100)
    annualization_years: float = Field(ge=1, le=100)
    annual_program_fee: float = Field(ge=0, le=1e12)


def _calculate(data: ProducerScenario, *, supported: bool,
               production_factor: float = 1., price_factor: float = 1.,
               operating_cost_factor: float = 1.) -> dict:
    production = data.production_kg * production_factor
    lost = production * data.loss_pct / 100
    marketable = production - lost
    sold = min(marketable, data.buyer_capacity_kg)
    price = data.price_per_kg * price_factor
    operating_cost = data.operating_cost * operating_cost_factor
    discount = data.capital_cost * data.equipment_discount_pct / 100 if supported else 0.
    annualized_capital = (data.capital_cost - discount) / data.annualization_years
    fee = data.annual_program_fee if supported else 0.
    revenue = sold * price
    total_cost = operating_cost + fee + annualized_capital
    break_even_price = total_cost / sold if sold > 0 else None
    # Zero price can cover only a zero cost. Avoid undefined division/Infinity.
    break_even_sales = total_cost / price if price > 0 else (0. if total_cost == 0 else None)
    feasible = break_even_sales is not None and break_even_sales <= sold + 1e-9
    if total_cost == 0:
        break_even_status = 'NO_COST_TO_RECOVER'
    elif sold == 0:
        break_even_status = 'NO_SALES'
    elif price == 0:
        break_even_status = 'ZERO_PRICE'
    else:
        break_even_status = 'WITHIN_SCENARIO_CAPACITY' if feasible else 'EXCEEDS_SCENARIO_CAPACITY'
    return dict(
        production_kg=production, lost_kg=lost, marketable_kg=marketable,
        saleable_kg=sold, unsold_kg=max(0., marketable - sold),
        price_per_kg=price, operating_cost=operating_cost, annual_program_fee=fee,
        equipment_discount=discount, net_capital_cost=data.capital_cost - discount,
        revenue=revenue, operating_balance=revenue - operating_cost - fee,
        annualized_capital=annualized_capital, annual_total_cost=total_cost,
        scenario_balance=revenue - total_cost,
        break_even_price=break_even_price, break_even_sales_kg=break_even_sales,
        break_even_feasible=feasible, break_even_status=break_even_status,
    )


def calculate_scenario(data: ProducerScenario) -> dict:
    baseline = _calculate(data, supported=False)
    supported = _calculate(data, supported=True)
    discount = data.capital_cost * data.equipment_discount_pct / 100
    effects = dict(
        one_time_equipment_discount=discount,
        annualized_discount=discount / data.annualization_years,
        annual_fee=data.annual_program_fee,
        annual_balance_change=supported['scenario_balance'] - baseline['scenario_balance'],
        comparison_basis='Aynı üretim, kayıp, alıcı kapasitesi ve fiyat; yalnız indirim ve program bedeli değişir.',
    )
    stress_definitions = [
        ('production_down_20', 'Üretim %20 azalırsa', .8, 1., 1.),
        ('price_down_20', 'Satış fiyatı %20 azalırsa', 1., .8, 1.),
        ('operating_cost_up_20', 'İşletme gideri %20 artarsa', 1., 1., 1.2),
        ('combined', 'Üç olumsuz koşul birlikte', .8, .8, 1.2),
    ]
    stress = [dict(
        id=key, label=label,
        changes=dict(production_pct=round((production - 1) * 100),
                     price_pct=round((price - 1) * 100),
                     operating_cost_pct=round((cost - 1) * 100)),
        result=_calculate(data, supported=True, production_factor=production,
                          price_factor=price, operating_cost_factor=cost),
    ) for key, label, production, price, cost in stress_definitions]
    actions = []
    if supported['unsold_kg'] > 0:
        actions.append(dict(code='MATCH_BUYER_CAPACITY', severity='warning',
                            title='Üretimi alıcı kapasitesiyle eşleştir.',
                            detail='Bu senaryoda pazarlanabilir ürünün tamamı alıcı kapasitesine sığmıyor. '
                                   'Ek alıcı ve saklama olanağını doğrula; doğrulanmayan ürünü satılmış sayma.'))
    if supported['lost_kg'] > 0:
        actions.append(dict(code='VERIFY_LOSSES', severity='info',
                            title='Kayıpları pilotta ölç.',
                            detail='Hasat, kalite reddi ve depolama kayıplarını ayrı kaydet; '
                                   'girilen kayıp oranını gerçek üretim verisiyle güncelle.'))
    if supported['scenario_balance'] < 0:
        actions.append(dict(code='REVISE_NEGATIVE_BALANCE', severity='danger',
                            title='Bu koşullarda ölçeği büyütmeden planı düzelt.',
                            detail='Hesaplanan gelir, yıllık gider ve ekipmanın yıllara yayılan bedelini karşılamıyor. '
                                   'Fiyatı, alıcı kapasitesini, işletme giderini ve ekipman teklifini doğrula.'))
    else:
        actions.append(dict(code='VALIDATE_POSITIVE_BALANCE', severity='info',
                            title='Olumlu hesabı pilot ve yazılı koşullarla doğrula.',
                            detail='Sıfır veya pozitif senaryo bakiyesi yatırım onayı değildir. '
                                   'Üretim miktarı, ödeme vadesi, kalite kabulü ve giderleri doğrulamadan büyütme.'))
    if effects['annual_balance_change'] < 0:
        actions.append(dict(code='REVIEW_PROGRAM_FEE', severity='warning',
                            title='Program bedelini ve sağlanan hizmeti gözden geçir.',
                            detail='Yıllık program bedeli, ekipman indiriminin bu yıla düşen faydasını aşıyor. '
                                   'Teknik desteğin veya pazara erişimin ek kazancı bu hesapta varsayılmadı.'))
    if stress[-1]['result']['scenario_balance'] < 0 <= supported['scenario_balance']:
        actions.append(dict(code='STRESS_VULNERABILITY', severity='warning',
                            title='Olumsuz koşullara karşı dayanıklılığı test et.',
                            detail='Birleşik stres denemesinde bakiye negatife dönüyor. '
                                   'Bu deneme bir olasılık veya gelecek tahmini değildir.'))
    return dict(
        input=data.model_dump(), period='year', period_label='Bir yıllık senaryo',
        classification='USER_SCENARIO', contracts_verified=False,
        investment_recommendation=False, optimizer_output=False,
        baseline=baseline, supported=supported, support_effect=effects,
        stress_scenarios=stress, actions=actions,
        labels=dict(saleable_kg='Alıcı kapasitesi içinde satılabileceği varsayılan ürün',
                    marketable_kg='Kayıp sonrası ürün', unsold_kg='Alıcı kapasitesini aşan ürün',
                    scenario_balance='Yıllık senaryo bakiyesi', operating_balance='İşletme bakiyesi',
                    annualized_capital='Ekipman bedelinin bu yıla düşen payı',
                    break_even_price='Giderleri karşılayan satış fiyatı',
                    break_even_sales_kg='Giderleri karşılayan satış miktarı'),
        scope='Bir ürün veya aynı fiyatla değerlendirilen tek parti için yıllık hesap. '
              'Gerçek satış, kâr, sigorta veya gelir garantisi değildir.',
        limitations=[
            'Bütün miktarlar, fiyatlar ve maliyetler kullanıcı senaryosudur; alıcı veya destek taahhüdü doğrulanmaz.',
            'Aynı para birimi ve bir yıllık kapsam kullanılır. Vergi, kredi faizi, enflasyon, ödeme gecikmesi ve artık değer modellenmez.',
            'Ekipman bedeli seçilen yıllara eşit bölünür; bu muhasebe amortismanı veya nakit akışı değildir.',
            'İşletme gideri toplam yıllık tutardır. Başabaş miktarı hesaplanırken ek üretimin marjinal maliyeti modellenmez.',
            'Destek karşılaştırması yalnız indirim ve program bedelini değiştirir; destek sayesinde daha fazla ürün satıldığı varsayılmaz.',
            'Stres denemeleri duyarlılık hesabıdır; olasılık, iklim tahmini veya sigorta teminatı değildir.',
            'Alıcı kapasitesi bir üst sınırdır; senaryoda bu sınıra kadar satış varsayılması alım sözleşmesi değildir.',
        ],
    )


@router.post('/scenario')
def scenario(data: ProducerScenario):
    return calculate_scenario(data)
