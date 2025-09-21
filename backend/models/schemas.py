from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class DiseaseClass(str, Enum):
    CONTROL = "Control"
    MCI = "MCI"
    ALZHEIMERS = "Alzheimer's"

class RiskLevel(str, Enum):
    LOW = "Low Risk"
    MODERATE = "Moderate Risk"
    HIGH = "High Risk"

class PredictionRequest(BaseModel):
    methylation_data: List[List[float]] = Field(..., description="Methylation data as 2D array")
    sample_id: str = Field(..., description="Unique identifier for the sample")

class PredictionResponse(BaseModel):
    prediction: str
    '''sample_id: str
    prediction: DiseaseClass
    confidence: float = Field(..., ge=0, le=1, description="Confidence score between 0 and 1")
    probabilities: Dict[str, float] = Field(..., description="Probability for each disease class")
    feature_importance: Dict[str, float] = Field(default_factory=dict, description="Feature importance scores")
    model_insights: Dict[str, Any] = Field(..., description="Additional model insights")
    risk_level: RiskLevel = Field(..., description="Clinical risk assessment")
    risk_percentage: float = Field(..., ge=0, le=100, description="Risk percentage for primary prediction")
    calibration_score: Optional[float] = Field(None, ge=0, le=1, description="Model calibration score")
'''
class ModelInfo(BaseModel):
    model_loaded: bool
    model_type: Optional[str]
    class_names: Dict[int, str]
    supported_formats: List[str]
    description: str
    total_features: Optional[int]
    model_accuracy: Optional[float]

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    timestamp: str
    version: str = "1.0.0"

class UploadResponse(BaseModel):
    message: str
    sample_id: str
    file_size: int
    features_detected: int

