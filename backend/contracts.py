from enum import Enum
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator
from datetime import datetime, timezone

MODEL_VERSION = "0.5.0"

class TruthLabel(str, Enum):
    historical = "OUR HISTORICAL RESULT"
    tank = "OUR NEW MEASUREMENT — TANK"
    external = "EXTERNAL OBSERVATION"
    model = "MODEL / REANALYSIS"
    future = "FUTURE SCENARIO"
    simulation = "SIMULATION / EXPLANATORY"
    planned = "PLANNED ARCTIC OBSERVATION"
    engineering = "ENGINEERING CONCEPT"

class ScientificInput(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

class ProductionSystemPattern(ScientificInput):
    """One allocation in the first single-crop, aggregate-period implementation."""
    crop: Literal["lettuce"] = "lettuce"
    production_method: Literal["open_field", "hydroponics"]
    water_source: Literal["freshwater", "desalinated_seawater"]
    production_kg: float = Field(ge=0)
    production_share_fraction: float = Field(ge=0, le=1)
    timing: Literal["aggregate_period_unspecified"] = "aggregate_period_unspecified"
    water_m3: float = Field(ge=0)
    energy_kwh: float = Field(ge=0)
    classification: Literal["SIMULATION / EXPLANATORY"] = "SIMULATION / EXPLANATORY"

class DecisionRequest(ScientificInput):
    region_id: Literal["longyearbyen"] = "longyearbyen"
    scenario_id: Literal["ssp126", "ssp585"] = "ssp126"
    output_target_kg: float = Field(default=1000, gt=0, le=1_000_000)
    freshwater_capacity_m3: float = Field(default=10, ge=0, le=1_000_000)
    energy_budget_kwh: float = Field(default=26000, ge=0, le=1_000_000_000)
    seawater_salinity_psu: float = Field(default=35, ge=0, le=50)
    seawater_temperature_c: float = Field(default=5, ge=-2, le=45)
    open_field_climate_suitable: bool | None = None
    soil_suitable: bool | None = None
    desalination_capacity_m3: float = Field(default=30, ge=0, le=1_000_000)
    production_capacity_kg: float = Field(default=2000, gt=0, le=1_000_000)
    recovery_fraction: float = Field(default=0.4, gt=0, le=0.8)
    energy_margin_fraction: float = Field(default=0.15, ge=0, le=0.5)

class SensitivityRequest(ScientificInput):
    temperature_C: float = Field(default=5, ge=-2, le=45)
    salinity_sp: float = Field(default=35, ge=0, le=50)
    reference_temperature_C: float = Field(default=10, ge=-2, le=45)
    reference_salinity_sp: float = Field(default=35, ge=0, le=50)
    source_kind: Literal["SIMULATION_EXPLANATORY", "EXTERNAL_OBSERVATION", "OUR_NEW_MEASUREMENT_TANK"] = "SIMULATION_EXPLANATORY"
    product_water_m3: float = Field(default=20, gt=0, le=1_000_000)

class BenchmarkRequest(ScientificInput):
    site_ids: list[str] = Field(default_factory=lambda:["konya","seyhan_adana","gediz_manisa","gap_sanliurfa","trakya_edirne"],min_length=1,max_length=5)
    soil_capacity_mm: float = Field(default=60,gt=0,le=500)
    initial_storage_mm: float = Field(default=30,ge=0,le=500)
    net_irrigation_budget_mm: float = Field(default=100,ge=0,le=2000)

    @model_validator(mode="after")
    def check_storage(self):
        if self.initial_storage_mm>self.soil_capacity_mm:raise ValueError("İlk stok depo kapasitesini aşamaz.")
        if len(set(self.site_ids))!=len(self.site_ids):raise ValueError("Bölgeler yinelenemez.")
        return self

class FieldPoint(ScientificInput):
    temperature_C: float = Field(default=10,ge=-2,le=45)
    temperature_kind: Literal["in_situ","potential","conservative"] = "in_situ"
    latitude: float = Field(default=78.22,ge=-90,le=90)
    longitude: float = Field(default=15.65,ge=-180,le=180)
    depth_m: float = Field(default=5,ge=0,le=12000)
    timestamp_utc: datetime = datetime(2026,9,22,12,tzinfo=timezone.utc)

    @model_validator(mode="after")
    def utc_required(self):
        if self.timestamp_utc.utcoffset() is None or self.timestamp_utc.utcoffset().total_seconds()!=0:
            raise ValueError("Saha karşılaştırmasında UTC zaman gerekli.")
        return self

class FieldComparisonRequest(ScientificInput):
    expected: FieldPoint = Field(default_factory=FieldPoint)
    observed: FieldPoint = Field(default_factory=lambda:FieldPoint(temperature_C=5))
    evidence_kind: Literal["SIMULATION_EXPLANATORY","EXTERNAL_OBSERVATION"] = "SIMULATION_EXPLANATORY"
    observed_dataset_id: str | None = None
    observed_sample_index: int | None = Field(default=None,ge=0)
    model_source_url: str | None = None
    max_distance_km: float = Field(default=5,ge=0,le=100)
    max_time_hours: float = Field(default=3,ge=0,le=48)
    max_depth_difference_m: float = Field(default=1,ge=0,le=100)
    decision: DecisionRequest = Field(default_factory=DecisionRequest)
