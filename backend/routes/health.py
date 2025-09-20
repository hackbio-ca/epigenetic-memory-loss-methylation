from fastapi import APIRouter, Depends
from datetime import datetime
import logging

from backend.models.schemas import HealthResponse
from backend.services.model_service import ModelService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["health"])

def get_model_service() -> ModelService:
    from backend.main import get_model_service as get_global_model_service
    return get_global_model_service()

@router.get("/health", response_model=HealthResponse)
async def health_check(
    model_service: ModelService = Depends(get_model_service)
):
    try:
        return HealthResponse(
            status="healthy" if model_service.is_loaded() else "degraded",
            model_loaded=model_service.is_loaded(),
            timestamp=datetime.now().isoformat(),
            version="1.0.0"
        )
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return HealthResponse(
            status="unhealthy",
            model_loaded=False,
            timestamp=datetime.now().isoformat(),
            version="1.0.0"
        )
