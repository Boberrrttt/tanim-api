"""
Machine Learning API Documentation
Separate file for Swagger documentation definitions
"""

from fastapi import Body
from ..modules.ml.schemas import PredictionRequest

# Prediction Documentation
PREDICT_DOCS = {
    "summary": "Make ML Prediction",
    "description": """
    Make a prediction using the trained Tanim machine learning model.
    
    **Process:**
    1. Validate input features
    2. Load ML model if not already loaded
    3. Make prediction using the model
    4. Return prediction result
    
    **Requirements:**
    - features must be a list of values matching model's expected input
    - Model file (tanim_model.pkl) must exist in app/models/
    
    **Features:**
    - Provide feature values in the same order as training data
    - Ensure all features are numeric and properly scaled
    """,
    "responses": {
        200: {
            "description": "Prediction successful",
            "content": {
                "application/json": {
                    "example": {
                        "prediction": "Good"
                    }
                }
            }
        },
        400: {
            "description": "Invalid input features",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Prediction failed: Invalid feature format"
                    }
                }
            }
        },
        500: {
            "description": "Model not available or prediction failed",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Prediction failed: Model not loaded"
                    }
                }
            }
        }
    }
}

predict_example = Body(
    ..., 
    description="ML prediction features",
    example={
        "features": [45.5, 28.3, 120.7, 6.8, 0.5, 22.5, 65.2]
    }
)

# Get Model Info Documentation
GET_MODEL_INFO_DOCS = {
    "summary": "Get ML Model Information",
    "description": """
    Retrieve information about the loaded machine learning model.
    
    **Process:**
    1. Check model status
    2. Return model information including:
       - Model file path
       - Load status
       - Model type
    
    **Returns:**
    - Current model status and metadata
    - Useful for debugging and monitoring
    """,
    "responses": {
        200: {
            "description": "Model information retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "model_path": "C:/Users/User/Dev/tanim/tanim-api/app/models/tanim_model.pkl",
                        "is_loaded": True,
                        "model_type": "RandomForestClassifier"
                    }
                }
            }
        },
        500: {
            "description": "Failed to get model information",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Failed to get model info: Model file not found"
                    }
                }
            }
        }
    }
}
