from pydantic import BaseModel, Field
from typing import List, Any, Optional

class PredictionRequest(BaseModel):
    features: List[Any] = Field(..., description="Input features for prediction: [N, P, K, ph, temperature, humidity]")
    farm_id: Optional[str] = Field(None, description="When set, ML service persists a soil health test with this farm_id")
    lat: Optional[float] = Field(None, description="Optional latitude; forwarded to ML /predict and stored in pending cache")
    lng: Optional[float] = Field(None, description="Optional longitude; forwarded to ML /predict and stored in pending cache")


class FertilizerPredictRequest(BaseModel):
    nitrogen: float = Field(..., description="Soil nitrogen (N)")
    phosphorus: float = Field(..., description="Soil phosphorus (P)")
    potassium: float = Field(..., description="Soil potassium (K)")
    ph: float = Field(..., description="Soil pH")
    crop: str = Field(..., description="Crop name; forwarded to ML /predict/fertilizer")
    farm_id: Optional[str] = Field(None, description="Optional farm id (forwarded to ML service)")
    cycle_start_date: Optional[str] = Field(
        None,
        description="ISO YYYY-MM-DD; echoed in ML farming_timeline (e.g. soil reading date)",
    )

class ProbabilityItem(BaseModel):
    crop_class: str = Field(..., description="Predicted crop class")
    probability: float = Field(..., description="Probability score")

class PredictionResponse(BaseModel):
    prediction: Any = Field(..., description="Main prediction result")
    probabilities: Optional[List[ProbabilityItem]] = Field(None, description="Top 3 predictions with probabilities")

class ModelInfoResponse(BaseModel):
    model_path: str
    is_loaded: bool
    model_type: Optional[str] = None
