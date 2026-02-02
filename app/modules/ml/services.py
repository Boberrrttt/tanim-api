import joblib
import os
import numpy as np
import pandas as pd
from typing import List, Any, Dict
from ...helpers.responses import success_response, error_response

_model = None
_label_encoder = None
_model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models", "tanim_model.pkl"))

async def load_model():
    global _model, _label_encoder
    try:
        if os.path.exists(_model_path):
            loaded_data = joblib.load(_model_path)
            
            if isinstance(loaded_data, dict):
                _model = loaded_data.get('model')
                _label_encoder = loaded_data.get('le')
            else:
                _model = loaded_data
                _label_encoder = getattr(_model, 'label_encoder', None)
            
            print(f"Model loaded from: {_model_path}")
            print(f"Label encoder found: {_label_encoder is not None}")
            return success_response(message="Model loaded successfully")
        else:
            raise FileNotFoundError(f"Model not found at {_model_path}")
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return error_response(message=f"Failed to load model: {str(e)}")

async def predict(features: List[Any]):
    global _model, _label_encoder
    try:
        if _model is None:
            load_result = await load_model()
            if load_result["status"] == "error":
                return load_result
        
        if _model is None:
            return error_response(message="Model not available")
        
        soil_sample = pd.DataFrame([{
            "N": features[0],
            "P": features[1], 
            "K": features[2],
            "ph": features[3],
            "temperature": features[4],
            "humidity": features[5]
        }])
        
        prediction = _model.predict(soil_sample)[0]
        
        if hasattr(prediction, 'item'):
            prediction = prediction.item()
        
        if hasattr(_model, 'predict_proba'):
            probs = _model.predict_proba(soil_sample)[0]
            
            if _label_encoder is not None:
                crops = _label_encoder.classes_
            elif hasattr(_model, 'classes_'):
                crops = _model.classes_
            else:
                crops = [str(prediction)]
                probs = [1.0]
            
            crops = [str(c) for c in crops]
            probs = [float(p) for p in probs]
            
            crop_probs = list(zip(crops, probs))
            top_3 = sorted(crop_probs, key=lambda x: x[1], reverse=True)[:3]
            
            if _label_encoder is not None:
                prediction_name = _label_encoder.inverse_transform([prediction])[0]
            else:
                prediction_name = str(prediction)
            
            return success_response(
                message="Prediction successful",
                data={
                    "prediction": str(prediction_name),
                    "probabilities": [
                        {"crop_class": crop, "probability": float(prob)} 
                        for crop, prob in top_3
                    ]
                }
            )
        else:
            if _label_encoder is not None:
                prediction_name = _label_encoder.inverse_transform([prediction])[0]
            else:
                prediction_name = str(prediction)
                
            return success_response(
                message="Prediction successful",
                data={"prediction": str(prediction_name)}
            )
            
    except Exception as e:
        return error_response(message=f"Prediction failed: {str(e)}")

async def get_model_info():
    global _model
    if _model is None:
        await load_model()
    
    return success_response(
        message="Model info retrieved",
        data={
            "model_path": _model_path,
            "is_loaded": _model is not None,
            "model_type": type(_model).__name__ if _model else None
        }
    )