from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class CropProbabilityItem(BaseModel):
    crop_class: str
    probability: float


class CreateCropRecommendation(BaseModel):
    farm_id: str
    probabilities: List[CropProbabilityItem] = Field(
        ...,
        description="Per-crop model scores, stored as JSONB",
    )
    created_at: Optional[datetime] = None


class UpdateCropRecommendation(BaseModel):
    farm_id: str
    probabilities: List[CropProbabilityItem] = Field(
        ...,
        description="Per-crop model scores, stored as JSONB",
    )
    created_at: Optional[datetime] = None
