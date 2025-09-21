"""
Pydantic models for request/response schemas.
"""
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum


class ModelType(str, Enum):
    """Available model types."""
    XGBOOST = "xgboost"
    PYTORCH = "pytorch"
    BOTH = "both"


class PredictionRequest(BaseModel):
    """Request model for predictions."""
    data: Optional[List[List[float]]] = Field(
        None, 
        description="Input data as list of lists (rows x features)",
        example=[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
    )
    model_type: ModelType = Field(
        default=ModelType.BOTH,
        description="Which model(s) to use for prediction"
    )
    study_name: Optional[str] = Field(None, description="Name of the study")
    study_description: Optional[str] = Field(None, description="Description of the study")


class PredictionResult(BaseModel):
    """Individual model prediction result."""
    model_name: str = Field(..., description="Name of the model used")
    prediction: Union[List[float], List[int]] = Field(..., description="Model predictions")
    probability: Optional[List[List[float]]] = Field(None, description="Prediction probabilities (if available)")
    confidence: Optional[float] = Field(None, description="Prediction confidence score")


class PredictionResponse(BaseModel):
    """Response model for predictions."""
    success: bool = Field(..., description="Whether the prediction was successful")
    message: str = Field(..., description="Response message")
    results: List[PredictionResult] = Field(..., description="Prediction results from model(s)")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = Field(False, description="Always false for errors")
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")