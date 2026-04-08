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
