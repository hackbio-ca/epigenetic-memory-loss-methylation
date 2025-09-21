"""
Utility functions for the application.
"""
import logging
import sys
from pathlib import Path


def setup_logging(log_level: str = "INFO") -> None:
    """
    Set up application logging.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("app.log")
        ]
    )


def validate_model_files(xgboost_path: str, pytorch_path: str) -> dict:
    """
    Validate that model files exist.
    
    Args:
        xgboost_path: Path to XGBoost model file
        pytorch_path: Path to PyTorch model file
        
    Returns:
        Dictionary with validation results
    """
    results = {
        "xgboost": Path(xgboost_path).exists(),
        "pytorch": Path(pytorch_path).exists(),
        "xgboost_path": xgboost_path,
        "pytorch_path": pytorch_path
    }
    
    return results