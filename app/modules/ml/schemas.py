from pydantic import BaseModel, Field
from typing import List, Any, Optional

class PredictionRequest(BaseModel):
    features: List[Any] = Field(..., description="Input features for prediction: [N, P, K, ph, temperature, humidity]")

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
