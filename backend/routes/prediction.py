from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from typing import Dict, Any
import logging

from backend.models.schemas import (
    PredictionRequest, 
    PredictionResponse, 
    UploadResponse,
    ModelInfo
)
from backend.services.model_service import ModelService
from backend.services.data_service import DataService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["prediction"])

def get_model_service() -> ModelService:
    from backend.main import get_model_service as get_global_model_service
    return get_global_model_service()

def get_data_service() -> DataService:
    return DataService()

@router.post("/predict", response_model=PredictionResponse)
async def predict_from_file(
    file: UploadFile = File(...),
    model_service: ModelService = Depends(get_model_service),
    data_service: DataService = Depends(get_data_service)
):
    try:
        if not model_service.is_loaded():
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        is_valid, error_msg = data_service.validate_file(file)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        data, metadata = await data_service.process_uploaded_file(file)
        result = model_service.predict(data)
        print(result)
        return {"prediction":str(result)}
        '''return PredictionResponse(
            sample_id=metadata.get("original_filename", "unknown"),
            prediction=result["prediction"],
            confidence=result["confidence"],
            probabilities=result["probabilities"],
            feature_importance=result["feature_importance"],
            model_insights=result["model_insights"],
            risk_level=result["risk_level"],
            risk_percentage=result["risk_percentage"],
            calibration_score=result["calibration_score"]
        )'''
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in predict_from_file: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.post("/predict-json", response_model=PredictionResponse)
async def predict_from_json(
    request: PredictionRequest,
    model_service: ModelService = Depends(get_model_service),
    data_service: DataService = Depends(get_data_service)
):
    try:
        if not model_service.is_loaded():
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        data, metadata = data_service.process_json_data(
            request.methylation_data, 
            request.sample_id
        )
        result = model_service.predict(data)
        
        return PredictionResponse(
            sample_id=request.sample_id,
            prediction=result["prediction"],
            confidence=result["confidence"],
            probabilities=result["probabilities"],
            feature_importance=result["feature_importance"],
            model_insights=result["model_insights"],
            risk_level=result["risk_level"],
            risk_percentage=result["risk_percentage"],
            calibration_score=result["calibration_score"]
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in predict_from_json: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.post("/predict-demo", response_model=PredictionResponse)
async def predict_demo_data(
    model_service: ModelService = Depends(get_model_service),
    data_service: DataService = Depends(get_data_service)
):
    try:
        if not model_service.is_loaded():
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        data, metadata = data_service.create_demo_data()
        result = model_service.predict(data)
        
        return PredictionResponse(
            sample_id="demo_sample",
            prediction=result["prediction"],
            confidence=result["confidence"],
            probabilities=result["probabilities"],
            feature_importance=result["feature_importance"],
            model_insights=result["model_insights"],
            risk_level=result["risk_level"],
            risk_percentage=result["risk_percentage"],
            calibration_score=result["calibration_score"]
        )
        
    except Exception as e:
        logger.error(f"Error in predict_demo_data: {e}")
        raise HTTPException(status_code=500, detail=f"Demo prediction failed: {str(e)}")

@router.get("/model-info", response_model=ModelInfo)
async def get_model_info(
    model_service: ModelService = Depends(get_model_service)
):
    try:
        return model_service.get_model_info()
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get model info: {str(e)}")

@router.get("/sample-data-info")
async def get_sample_data_info(
    data_service: DataService = Depends(get_data_service)
):
    try:
        return data_service.get_sample_data_info()
    except Exception as e:
        logger.error(f"Error getting sample data info: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get sample data info: {str(e)}")
