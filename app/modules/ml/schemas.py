from pydantic import BaseModel, Field
from typing import List, Any, Optional

class PredictionRequest(BaseModel):
    features: List[Any] = Field(..., description="Input features for prediction: [N, P, K, ph, temperature, humidity]")
    farm_id: Optional[str] = Field(None, description="When set, ML service persists a soil health test with this farm_id")


class FertilizerPredictRequest(BaseModel):
    nitrogen: float = Field(..., description="Soil nitrogen (N)")
    phosphorus: float = Field(..., description="Soil phosphorus (P)")
    potassium: float = Field(..., description="Soil potassium (K)")
    ph: float = Field(..., description="Soil pH")
    temperature: float = Field(..., description="Temperature (°C)")
    ec: float = Field(..., description="Electrical conductivity")
    moisture: float = Field(..., description="Soil moisture (%)")
    farm_id: Optional[str] = Field(None, description="Optional farm id (forwarded to ML service)")

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
