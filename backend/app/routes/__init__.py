"""
Initialize routes module.
"""

from .predict import router as prediction_router

__all__ = ["prediction_router", "health_router"]