from typing import Literal
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field, field_validator


class NorthRequest(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)
    site_id: Literal['longyearbyen'] = 'longyearbyen'
    horizon_id: Literal['historical', 'recent', 'near', 'mid', 'late'] = 'mid'
    target_year: int | None = Field(None, ge=2026, le=2100, description='Exact source climate-model year; overrides horizon_id. Not a forecast of the weather on that date.')

    @field_validator('target_year')
    @classmethod
    def current_or_future_year(cls, value):
        if value is not None and value < datetime.now(timezone.utc).year:
            raise ValueError('Planlama yılı mevcut yıldan önce olamaz.')
        return value

    scenario_id: Literal['ssp245', 'ssp585'] = 'ssp245'
    objective: Literal['balanced', 'water', 'energy'] = 'balanced'
    production_purpose: Literal['fresh_mass', 'protein', 'food_energy'] = Field('fresh_mass', description='Explicit output metric: fresh edible kg, grams of crude protein, or food kcal. Nutritional modes are composition-table scenarios, not a balanced diet, local demand, profit or verified polar harvest.')
    production_retention: float = Field(1., ge=.5, le=1., description='Water/energy modes retain this fraction of each crop amount in the newly calculated balanced plan; not a yield forecast.')
    minimum_crop_share: float = Field(.05, ge=0., le=.2, description='Minimum area fraction for each active candidate crop. This is a declared diversity policy, not equal shares or measured suitability. Shares summed over active crops may not exceed one.')
    area_m2: float = Field(100., ge=1., le=10000.)
    roof_ratio: float = Field(1., ge=0., le=5.)
    storage_m3_per_m2: float = Field(.1, ge=0., le=2.)
    collection_efficiency: float = Field(.8, ge=0., le=1.)
    desalination: bool = True
    freshwater_m3: float = Field(0., ge=0., le=100000.)
    heat_cop: float = Field(1., ge=1., le=5.)
    energy_limit_kwh: float | None = Field(None, ge=0., le=1e9)
    available_power_kw: float | None = Field(None, ge=0., le=1e6, description='Optional site electrical capacity for conservative operation-peak screening; separate from annual kWh optimizer constraint.')
    salinity_g_kg: float = Field(35., ge=1., le=50.)
    source_temperature_c: float = Field(2., ge=-2., le=30.)
    recovery: float = Field(.45, ge=.1, le=.6)
    disabled_crops: list[str] = Field(default_factory=list, max_length=30)
    disabled_methods: list[Literal['open_field','greenhouse','hydroponics']] = Field(default_factory=list, max_length=3)


class WaterPoint(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)
    depth_m: float = Field(ge=0., le=10000.)
    temperature_c: float = Field(ge=-3., le=40.)
    salinity_g_kg: float = Field(ge=1., le=50.)


class ModelExpectation(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)
    model_id: str = Field(min_length=2, max_length=200)
    version: str = Field(min_length=1, max_length=100)
    source_url: str = Field(min_length=8, max_length=1000)
    generated_at_utc: str
    valid_from_utc: str
    valid_to_utc: str
    latitude: float = Field(ge=-90., le=90.)
    longitude: float = Field(ge=-180., le=180.)
    temperature_kind: Literal['in_situ']
    salinity_kind: Literal['absolute_mass_g_kg']
    temporal_support: Literal['instantaneous', 'daily_mean', 'monthly_mean']
    points: list[WaterPoint] = Field(min_length=2, max_length=1000)


class FreezeRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    scenario: NorthRequest
    expectation: ModelExpectation | None = None
    intake_depth_m: float | None = Field(None, ge=0., le=10000.)


class Observation(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)
    measured_at_utc: str
    latitude: float = Field(ge=-90., le=90.)
    longitude: float = Field(ge=-180., le=180.)
    temperature_kind: Literal['in_situ']
    salinity_kind: Literal['absolute_mass_g_kg']
    calibration_record: str = Field(min_length=5, max_length=2000)
    quality: Literal['accepted']
    instrument_id: str = Field(min_length=2, max_length=100)
    evidence_record: str = Field(min_length=5, max_length=2000)
    points: list[WaterPoint] = Field(min_length=2, max_length=1000)


class ObserveRequest(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)
    freeze_id: str = Field(pattern=r'^[0-9a-f]{32}$')
    observation: Observation
    intake_depth_m: float = Field(ge=0., le=10000.)
    connection_evidence: str = Field(min_length=20, max_length=4000)
    interpretation: Literal['present_source_scenario_transfer']
