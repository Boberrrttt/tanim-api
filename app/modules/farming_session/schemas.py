from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field


class CropProbabilityItem(BaseModel):
    crop_class: str
    probability: float


class StartFarmingSessionBody(BaseModel):
    farm_id: str = Field(..., description="Farm this session belongs to")
    farmer_id: str = Field(..., description="Must match farm.farmer_id")
    selected_crop: str = Field(
        ...,
        description="Crop the farmer committed to (stored in column selected_crops)",
    )
    soil_snapshot: dict = Field(
        ...,
        description="N, P, K, pH, salinity, temperature, moisture, etc.",
    )
    features: Optional[List[float]] = Field(
        None,
        description="Optional ML feature vector [N,P,K,pH,temp,moisture,EC]; preferred source for soil_health_test row",
    )
    fertilizer_recommendation: dict = Field(
        ...,
        description="Full successful ML /predict/fertilizer data object",
    )
    top_crop_probabilities: Optional[List[CropProbabilityItem]] = Field(
        None,
        description="Top crop suggestions at start time",
    )
    cycle_start_date: Optional[str] = Field(
        None,
        description="ISO YYYY-MM-DD echoed from fertilizer request",
    )
    started_at: Optional[datetime] = Field(
        None,
        description="Optional client clock; maps to DB created_at when set",
    )
    latitude: Optional[float] = Field(
        None,
        description="When both latitude and longitude are set, updates farm.latitude for this farm_id",
    )
    longitude: Optional[float] = Field(
        None,
        description="When both latitude and longitude are set, updates farm.longitude for this farm_id",
    )
