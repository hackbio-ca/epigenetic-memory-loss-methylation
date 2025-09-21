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
    return joblib.load(str(model_path))


def load_pytorch_model():
    """Load and return the PyTorch model."""
    model_path = MODEL_DIR / 'convnet.pkl'
    return torch.load(str(model_path))