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
        "Proxies to the inference service `POST /predict/fertilizer` with soil N, P, K, pH, and crop."
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
                            "crop": "Corn",
                            "soil_ph": 6.5,
                            "nitrogen": "High",
                            "phosphorus": "High",
                            "potassium": "Medium",
                            "fertilizer_recommendation_rate": "60 - 20 - 45",
                            "organic_fertilizer": "10 bags/ha",
                            "option_1": {
                                "first_application": [],
                                "second_application": [],
                            },
                            "option_2": {
                                "first_application": [],
                                "second_application": [],
                            },
                            "mode_of_application": {
                                "first_application": "",
                                "second_application": "",
                                "organic_fertilizer": "",
                            },
                            "farming_timeline": {
                                "template_id": "CEREAL",
                                "total_days": 105,
                                "cycle_start_date": "2026-04-07",
                                "planting_window_note": "",
                                "phases": [],
                            },
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
                "crop": "Corn",
                "cycle_start_date": "2026-04-07",
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
