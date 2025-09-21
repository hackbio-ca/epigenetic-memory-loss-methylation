"""Test script to check model loading and prediction capabilities."""

import numpy as np
import sys
import os

# Add the backend path to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from backend.app.models.loader import load_xgboost_model, load_pytorch_model
    
    print("Testing model loading...")
    
    # Test XGBoost model
    print("\n=== Testing XGBoost Model ===")
    try:
        xgb_model = load_xgboost_model()
        print(f"XGBoost model loaded successfully: {type(xgb_model)}")
        
        # Create dummy data for testing (5000 features to match the model expectation)
        dummy_data = np.random.rand(5, 5000)  # 5 samples, 5000 features
        print(f"Dummy data shape: {dummy_data.shape}")
        
        # Test prediction
        xgb_predictions = xgb_model.predict(dummy_data)
        print(f"XGBoost predictions: {xgb_predictions}")
        print(f"XGBoost prediction shape: {xgb_predictions.shape}")
        
    except Exception as e:
        print(f"XGBoost model test failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test PyTorch model
    print("\n=== Testing PyTorch Model ===")
    try:
        pytorch_model = load_pytorch_model()
        print(f"PyTorch model loaded successfully: {type(pytorch_model)}")
        
        # Create dummy data for testing
        dummy_data = np.random.rand(5, 5000)  # 5 samples, 5000 features
        print(f"Dummy data shape: {dummy_data.shape}")
        
        # Test prediction
        pytorch_predictions = pytorch_model.predict(dummy_data)
        print(f"PyTorch predictions: {pytorch_predictions}")
        print(f"PyTorch prediction shape: {pytorch_predictions.shape}")
        
    except Exception as e:
        print(f"PyTorch model test failed: {e}")
        import traceback
        traceback.print_exc()

except ImportError as e:
    print(f"Import error: {e}")
    print("Please make sure all dependencies are installed and the path is correct.")
except Exception as e:
    print(f"Unexpected error: {e}")
    import traceback
    traceback.print_exc()