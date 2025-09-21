"""
Application configuration settings.
"""
import os
from pathlib import Path
from typing import Optional
try:
    from pydantic_settings import BaseSettings
except ImportError:
    # Fallback for older pydantic versions
    from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application settings
    app_name: str = "Epigenetic Memory Loss Prediction API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Model paths
    base_dir: Path = Path(__file__).parent.parent.parent.parent
    xgboost_model_path: str = str(base_dir / "model" / "models" / "xgboost" / "xgboost_model.pkl")
    pytorch_model_path: str = str(base_dir / "model" / "models" / "pytorch" / "model.pkl")
    
    # API settings
    api_v1_prefix: str = "/api/v1"
    allowed_origins: list = ["http://localhost:3000", "http://127.0.0.1:3000", "*"]  # Configure this properly for production
    
    # Logging
    log_level: str = "INFO"
    
    # File upload settings
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: list = [".csv", ".txt"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings