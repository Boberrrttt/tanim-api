"""
Machine Learning API Documentation
Separate file for Swagger documentation definitions
"""

from fastapi import Body

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
                    "examples": {
                        "success": {
                            "summary": "Successful prediction",
                            "value": {
                                "prediction": "Good"
                            }
                        }
                    }
                }
            }
        },
        400: {
            "description": "Invalid input features",
            "content": {
                "application/json": {
                    "examples": {
                        "error": {
                            "summary": "Invalid features",
                            "value": {
                                "detail": "Prediction failed: Invalid feature format"
                            }
                        }
                    }
                }
            }
        },
        500: {
            "description": "Model not available or prediction failed",
            "content": {
                "application/json": {
                    "examples": {
                        "error": {
                            "summary": "Model error",
                            "value": {
                                "detail": "Prediction failed: Model not loaded"
                            }
                        }
                    }
                }
            }
        }
    }
}

predict_example = Body(
    ..., 
    description="ML prediction features",
    examples={
        "default": {
            "summary": "Example features",
            "value": {
                "features": [45.5, 28.3, 120.7, 6.8, 0.5, 22.5, 65.2]
            }
        }
    }
)

FERTILIZER_PREDICT_DOCS = {
    "summary": "Fertilizer recommendation (ML)",
    "description": (
        "Proxies to the inference service `POST /predict/fertilizer` with soil NPK, pH, "
        "temperature, EC, and moisture."
    ),
    "responses": {
        200: {
            "description": "Fertilizer prediction successful",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Fertilizer recommendation successful",
                        "data": {
                            "prediction": "Urea",
                            "probabilities": [
                                {
                                    "fertilizer_class": "Urea",
                                    "probability": 0.42,
                                }
                            ],
                        },
                    }
                }
            },
        }
    },
}

fertilizer_predict_example = Body(
    ...,
    description="Soil readings for fertilizer model",
    examples={
        "default": {
            "summary": "Example soil sample",
            "value": {
                "nitrogen": 45.0,
                "phosphorus": 30.0,
                "potassium": 120.0,
                "ph": 6.5,
                "temperature": 28.0,
                "ec": 1.2,
                "moisture": 35.0,
            },
        }
    },
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
                    "examples": {
                        "success": {
                            "summary": "Model info",
                            "value": {
                                "model_path": "C:/Users/User/Dev/tanim/tanim-api/app/models/tanim_model.pkl",
                                "is_loaded": True,
                                "model_type": "RandomForestClassifier"
                            }
                        }
                    }
                }
            }
        },
        500: {
            "description": "Failed to get model information",
            "content": {
                "application/json": {
                    "examples": {
                        "error": {
                            "summary": "Model info error",
                            "value": {
                                "detail": "Failed to get model info: Model file not found"
                            }
                        }
                    }
                }
            }
        }
    }
}
