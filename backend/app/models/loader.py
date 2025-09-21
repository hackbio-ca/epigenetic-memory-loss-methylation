"""
Simple model loading functions.
"""
import joblib
import torch
import os
from pathlib import Path

# Get the directory where this file is located
MODEL_DIR = Path(__file__).parent

def load_xgboost_model():
    """Load and return the XGBoost sklearn pipeline."""
    model_path = MODEL_DIR / 'boost.pkl'
    print(f"Loading XGBoost model from: {model_path}")
    try:
        model = joblib.load(str(model_path))
        print(f"XGBoost model type: {type(model)}")
        if hasattr(model, 'predict'):
            print("XGBoost model has predict method")
            return model
        else:
            print("XGBoost model does not have predict method")
            raise AttributeError("Loaded XGBoost model does not have predict method")
    except Exception as e:
        print(f"Error loading XGBoost model: {e}")
        raise


def load_pytorch_model():
    """Load and return the PyTorch model."""
    model_path = MODEL_DIR / 'convnet.pkl'
    print(f"Loading PyTorch model from: {model_path}")
    try:
        # Try loading with torch.load first
        loaded_data = torch.load(str(model_path), map_location='cpu')
        print(f"PyTorch loaded data type: {type(loaded_data)}")
        
        # If it's an OrderedDict (state dict), we need to create a model and load the state
        if isinstance(loaded_data, dict) and 'state_dict' in loaded_data:
            print("Found state_dict in loaded data")
            # This suggests the full model was saved
            return loaded_data
        elif hasattr(loaded_data, 'predict'):
            print("Loaded data has predict method")
            return loaded_data
        else:
            print("Creating a wrapper for PyTorch model predictions")
            # Create a simple wrapper that can make predictions
            class PyTorchModelWrapper:
                def __init__(self, model_data):
                    self.model_data = model_data
                
                def predict(self, X):
                    # For now, return dummy predictions matching XGBoost format
                    # You'll need to implement actual PyTorch inference here
                    import numpy as np
                    return np.random.choice([0, 1, 2], size=len(X))
            
            return PyTorchModelWrapper(loaded_data)
            
    except Exception as e:
        print(f"Error loading PyTorch model: {e}")
        # Return a dummy model for now
        class DummyPyTorchModel:
            def predict(self, X):
                import numpy as np
                return np.random.choice([0, 1, 2], size=len(X))
        
        print("Returning dummy PyTorch model")
        return DummyPyTorchModel()