"""
Model service for loading and running predictions with pickle models.
"""
import pickle
import logging
import numpy as np
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from threading import Lock

from ..config import get_settings
from ..models.schemas import ModelType

logger = logging.getLogger(__name__)


class ModelService:
    """Service for managing and running machine learning models."""
    
    def __init__(self):
        """Initialize the model service."""
        self.settings = get_settings()
        self._models: Dict[str, Any] = {}
        self._model_metadata: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()
        self._load_models()
    
    def _load_models(self) -> None:
        """Load all available models."""
        logger.info("Loading models...")
        
        # Load XGBoost model
        try:
            xgb_path = Path(self.settings.xgboost_model_path)
            if xgb_path.exists():
                with open(xgb_path, 'rb') as f:
                    self._models[ModelType.XGBOOST] = pickle.load(f)
                    self._model_metadata[ModelType.XGBOOST] = {
                        "path": str(xgb_path),
                        "loaded": True,
                        "type": "XGBoost",
                        "size": xgb_path.stat().st_size
                    }
                logger.info(f"XGBoost model loaded from {xgb_path}")
            else:
                logger.warning(f"XGBoost model not found at {xgb_path}")
                self._model_metadata[ModelType.XGBOOST] = {"loaded": False, "error": "File not found"}
        except Exception as e:
            logger.error(f"Failed to load XGBoost model: {e}")
            self._model_metadata[ModelType.XGBOOST] = {"loaded": False, "error": str(e)}
        
        # Load PyTorch model
        try:
            pytorch_path = Path(self.settings.pytorch_model_path)
            if pytorch_path.exists():
                with open(pytorch_path, 'rb') as f:
                    self._models[ModelType.PYTORCH] = pickle.load(f)
                    self._model_metadata[ModelType.PYTORCH] = {
                        "path": str(pytorch_path),
                        "loaded": True,
                        "type": "PyTorch",
                        "size": pytorch_path.stat().st_size
                    }
                logger.info(f"PyTorch model loaded from {pytorch_path}")
            else:
                logger.warning(f"PyTorch model not found at {pytorch_path}")
                self._model_metadata[ModelType.PYTORCH] = {"loaded": False, "error": "File not found"}
        except Exception as e:
            logger.error(f"Failed to load PyTorch model: {e}")
            self._model_metadata[ModelType.PYTORCH] = {"loaded": False, "error": str(e)}
    
    def is_model_loaded(self, model_type: ModelType) -> bool:
        """Check if a specific model is loaded."""
        return model_type in self._models and self._model_metadata.get(model_type, {}).get("loaded", False)
    
    def get_loaded_models(self) -> Dict[str, bool]:
        """Get the status of all models."""
        return {
            model_type.value: self._model_metadata.get(model_type, {}).get("loaded", False)
            for model_type in ModelType if model_type != ModelType.BOTH
        }
    
    def get_model_metadata(self) -> Dict[str, Dict[str, Any]]:
        """Get metadata for all models."""
        return self._model_metadata.copy()
    
    def predict(self, data: List[List[float]], model_type: ModelType) -> Dict[str, Any]:
        """
        Make predictions using the specified model(s).
        
        Args:
            data: Input data as list of lists
            model_type: Which model to use
            
        Returns:
            Dictionary with prediction results
        """
        with self._lock:
            if model_type == ModelType.BOTH:
                return self._predict_both(data)
            else:
                return self._predict_single(data, model_type)
    
    def _predict_single(self, data: List[List[float]], model_type: ModelType) -> Dict[str, Any]:
        """Make prediction with a single model."""
        if not self.is_model_loaded(model_type):
            raise ValueError(f"Model {model_type.value} is not loaded")
        
        model = self._models[model_type]
        input_array = np.array(data)
        
        try:
            # Make prediction
            prediction = model.predict(input_array)
            
            # Try to get prediction probabilities if available
            probabilities = None
            confidence = None
            
            if hasattr(model, 'predict_proba'):
                try:
                    probabilities = model.predict_proba(input_array)
                    # Calculate confidence as max probability
                    if probabilities is not None:
                        confidence = float(np.max(probabilities, axis=1).mean())
                except Exception as e:
                    logger.warning(f"Could not get probabilities for {model_type.value}: {e}")
            
            return {
                "model_name": model_type.value,
                "prediction": prediction.tolist() if hasattr(prediction, 'tolist') else prediction,
                "probability": probabilities.tolist() if probabilities is not None else None,
                "confidence": confidence,
                "input_shape": input_array.shape,
                "output_shape": prediction.shape if hasattr(prediction, 'shape') else None
            }
            
        except Exception as e:
            logger.error(f"Prediction failed for {model_type.value}: {e}")
            raise RuntimeError(f"Prediction failed for {model_type.value}: {str(e)}")
    
    def _predict_both(self, data: List[List[float]]) -> Dict[str, Any]:
        """Make predictions with both models."""
        results = {}
        errors = []
        
        for model_type in [ModelType.XGBOOST, ModelType.PYTORCH]:
            try:
                if self.is_model_loaded(model_type):
                    result = self._predict_single(data, model_type)
                    results[model_type.value] = result
                else:
                    errors.append(f"Model {model_type.value} is not loaded")
            except Exception as e:
                errors.append(f"Error with {model_type.value}: {str(e)}")
        
        if not results:
            raise RuntimeError(f"No models available for prediction. Errors: {'; '.join(errors)}")
        
        return {
            "results": results,
            "errors": errors if errors else None,
            "models_used": list(results.keys())
        }
    
    def reload_models(self) -> None:
        """Reload all models."""
        logger.info("Reloading models...")
        with self._lock:
            self._models.clear()
            self._model_metadata.clear()
            self._load_models()


# Global model service instance
_model_service: Optional[ModelService] = None


def get_model_service() -> ModelService:
    """Get the global model service instance."""
    global _model_service
    if _model_service is None:
        _model_service = ModelService()
    return _model_service