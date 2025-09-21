"""
Controllers for handling API requests and responses.
"""
import logging
from datetime import datetime
from typing import List
from fastapi import HTTPException

from ..models.schemas import (
    PredictionRequest, 
    PredictionResponse, 
    PredictionResult,
    ModelType
)
from ..services import get_model_service
from ..config import get_settings

logger = logging.getLogger(__name__)


class PredictionController:
    """Controller for handling prediction requests."""
    
    def __init__(self):
        """Initialize the prediction controller."""
        self.model_service = get_model_service()
        self.settings = get_settings()
    
    async def predict(self, request: PredictionRequest) -> PredictionResponse:
        """
        Handle prediction requests.
        
        Args:
            request: Prediction request with data and model type
            
        Returns:
            Prediction response with results
        """
        try:
            logger.info(f"Processing prediction request with {len(request.data)} samples using {request.model_type}")
            
            # Validate input data
            self._validate_input_data(request.data)
            
            # Make prediction using model service
            prediction_results = self.model_service.predict(request.data, request.model_type)
            
            # Format response based on model type
            if request.model_type == ModelType.BOTH:
                results = self._format_multiple_results(prediction_results)
            else:
                results = [self._format_single_result(prediction_results)]
            
            return PredictionResponse(
                success=True,
                message=f"Prediction completed successfully using {request.model_type.value} model(s)",
                results=results,
                metadata={
                    "timestamp": datetime.utcnow().isoformat(),
                    "model_type": request.model_type.value,
                    "input_samples": len(request.data),
                    "features": len(request.data[0]) if request.data else 0
                }
            )
            
        except ValueError as e:
            logger.error(f"Validation error in prediction: {e}")
            raise HTTPException(status_code=400, detail=str(e))
        except RuntimeError as e:
            logger.error(f"Runtime error in prediction: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            logger.error(f"Unexpected error in prediction: {e}")
            raise HTTPException(status_code=500, detail="Internal server error during prediction")
    
    def _validate_input_data(self, data: List[List[float]]) -> None:
        """Validate input data format and content."""
        if not data:
            raise ValueError("Input data cannot be empty")
        
        if not all(isinstance(row, list) for row in data):
            raise ValueError("Input data must be a list of lists")
        
        if not data[0]:
            raise ValueError("Input data rows cannot be empty")
        
        # Check that all rows have the same number of features
        feature_count = len(data[0])
        for i, row in enumerate(data):
            if len(row) != feature_count:
                raise ValueError(f"All rows must have the same number of features. Row {i} has {len(row)}, expected {feature_count}")
            
            # Check that all values are numeric
            for j, value in enumerate(row):
                if not isinstance(value, (int, float)):
                    raise ValueError(f"All values must be numeric. Found {type(value)} at row {i}, column {j}")
    
    def _format_single_result(self, result: dict) -> PredictionResult:
        """Format a single model prediction result."""
        return PredictionResult(
            model_name=result["model_name"],
            prediction=result["prediction"],
            probability=result.get("probability"),
            confidence=result.get("confidence")
        )
    
    def _format_multiple_results(self, results: dict) -> List[PredictionResult]:
        """Format results from multiple models."""
        formatted_results = []
        
        for model_name, result in results["results"].items():
            formatted_results.append(PredictionResult(
                model_name=model_name,
                prediction=result["prediction"],
                probability=result.get("probability"),
                confidence=result.get("confidence")
            ))
        
        return formatted_results

# Global controller instances
prediction_controller = PredictionController()