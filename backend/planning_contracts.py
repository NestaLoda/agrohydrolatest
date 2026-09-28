"""Shared crop-pattern planning inputs. Every editable quantity is a scenario."""
from datetime import date
from typing import Literal
from pydantic import Field, model_validator
from .contracts import ScientificInput, FieldComparisonRequest

Method = Literal['open_field', 'greenhouse', 'hydroponics']
Source = Literal['freshwater', 'stored_water', 'reuse', 'desalinated_seawater']

class WaterSourceInput(ScientificInput):
    source_id: Source
    capacity_m3: float = Field(ge=0, le=1e12)
    enabled: bool = True
    quality_suitable: bool | None = None
    energy_kwh_m3: float | None = Field(default=None, ge=0, le=1000)

class CropPlanInput(ScientificInput):
    crop_id: str = Field(min_length=1, max_length=60)
    enabled: bool = True
    current_area_ha: float = Field(default=0, ge=0, le=1e8)
    yield_kg_ha: float | None = Field(default=None, gt=0, le=1e7)
    season_start: date = date(2023, 4, 1)
    stage_days: list[int] | None = Field(default=None, min_length=4, max_length=4)
    min_share: float = Field(default=0, ge=0, le=1)
    max_share: float = Field(default=1, ge=0, le=1)
    min_production_kg: float = Field(default=0, ge=0, le=1e13)
    target_production_kg: float = Field(gt=0, le=1e13)
    priority: float = Field(default=1, gt=0, le=100)
    climate_suitable: bool | None = None
    soil_suitable: bool | None = None
    methods: list[Method] = Field(default_factory=lambda:['open_field'], max_length=3)
    field_energy_kwh_ha: float | None = Field(default=None, ge=0, le=1e8)
    controlled_yield_kg_m2: float | None = Field(default=None, gt=0, le=1000)
    controlled_water_m3_kg: float | None = Field(default=None, ge=0, le=100)
    controlled_energy_kwh_kg: float | None = Field(default=None, ge=0, le=1e5)
    manual_net_irrigation_mm: float | None = Field(default=None, ge=0, le=1e5)

    @model_validator(mode='after')
    def valid_crop(self):
        if self.min_share > self.max_share: raise ValueError('Minimum ürün payı maksimumu aşamaz.')
        if len(set(self.methods)) != len(self.methods): raise ValueError('Yöntem yinelenemez.')
        if self.stage_days is not None and (min(self.stage_days)<1 or sum(self.stage_days)>366):
            raise ValueError('Dört aşama pozitif ve toplamı en fazla 366 gün olmalı.')
        return self

class SimulationRequest(ScientificInput):
    north_input_policy: Literal['explicit_scenario', 'source_resolved'] = 'explicit_scenario'
    quantity_basis: Literal['demand', 'capacity'] = 'demand'
    resource_priority_fraction: float = Field(default=.8, gt=0, le=1)
    planning_objective: Literal['capacity','demand','balanced','water_priority','energy_priority','regional_water'] = 'demand'
    mode: Literal['turkiye','north']
    region_id: str
    period_label: str = Field(default='2022–2023 referans sezonu', max_length=120)
    climate_basis: Literal['era5_2022_2023','era5_2024_2025','user_scenario'] = 'era5_2022_2023'
    climate_context_id: Literal['ec_earth_2030_2049', 'nasa_ssp245_2035', 'nasa_ssp585_2035'] | None = None
    climate_scenario_label: str = Field(default='Referans hava serisi', max_length=240)
    rainfall_factor: float = Field(default=1, ge=0, le=3)
    temperature_delta_c: float = Field(default=0, ge=-3, le=6)
    et0_factor: float = Field(default=1, ge=0, le=3)
    land_area_ha: float = Field(ge=0, le=1e8)
    min_cultivated_fraction: float = Field(default=0, ge=0, le=1)
    soil_capacity_mm: float = Field(default=60, gt=0, le=500)
    initial_storage_mm: float = Field(default=30, ge=0, le=500)
    irrigation_efficiency: float = Field(default=.75, gt=0, le=1)
    energy_budget_kwh: float | None = Field(default=None, ge=0, le=1e14)
    greenhouse_capacity_m2: float = Field(default=0, ge=0, le=1e9)
    hydroponics_capacity_m2: float = Field(default=0, ge=0, le=1e9)
    seawater_temperature_c: float = Field(default=10, ge=-2, le=45)
    water_sources: list[WaterSourceInput] = Field(min_length=1,max_length=4)
    crops: list[CropPlanInput] = Field(min_length=1,max_length=20)
    overrides: list[str] = Field(default_factory=list,max_length=100)

    @model_validator(mode='after')
    def valid_scenario(self):
        if self.mode=='north' and self.temperature_delta_c!=0:
            raise ValueError('Sıcaklık farkı senaryosu bu sürümde yalnız Türkiye içindir; Kuzey için desteklenmiyor.')
        if self.planning_objective=='regional_water' and (self.mode!='turkiye' or any(c.methods!=['open_field'] for c in self.crops if c.enabled)):
            raise ValueError('Bölgesel su amacı Türkiye açık tarla deseni içindir.')
        if self.initial_storage_mm>self.soil_capacity_mm: raise ValueError('Başlangıç nemi depo kapasitesini aşamaz.')
        if len({c.crop_id for c in self.crops})!=len(self.crops):raise ValueError('Ürünler yinelenemez.')
        if len({s.source_id for s in self.water_sources})!=len(self.water_sources):raise ValueError('Su kaynakları yinelenemez.')
        if sum(c.current_area_ha for c in self.crops)>self.land_area_ha+max(1e-6,self.land_area_ha*1e-8):
            raise ValueError('Mevcut ürün alanları toplamı toplam açık tarla alanını aşamaz.')
        if self.mode=='north' and self.region_id!='longyearbyen':raise ValueError('Bu sürümde kuzey veri bağlamı Longyearbyen.')
        if self.mode=='turkiye' and self.region_id=='longyearbyen':raise ValueError('Türkiye bölgesi seçin.')
        return self

class PatternFieldUpdate(ScientificInput):
    simulation: SimulationRequest
    observation: FieldComparisonRequest = Field(default_factory=FieldComparisonRequest)
