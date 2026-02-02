import joblib
import os

# Load your current model to check its size
model_path = 'app/models/tanim_model.pkl'
if os.path.exists(model_path):
    size_mb = os.path.getsize(model_path) / (1024 * 1024)
    print(f"Current model size: {size_mb:.2f} MB")
    
    # Load and re-save with higher compression
    model = joblib.load(model_path)
    
    # Save with maximum compression
    optimized_path = 'app/models/tanim_model_optimized.pkl'
    joblib.dump(model, optimized_path, compress=9)
    
    # Check new size
    new_size_mb = os.path.getsize(optimized_path) / (1024 * 1024)
    print(f"Optimized model size: {new_size_mb:.2f} MB")
    print(f"Size reduction: {((size_mb - new_size_mb) / size_mb * 100):.1f}%")
else:
    print("Model file not found!")
