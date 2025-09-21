import pandas as pd
import numpy as np
import io
import logging
from typing import Dict, Any, Tuple, Optional
from fastapi import UploadFile
import h5py

#Load selected features
total_mean_SHAP_values = np.loadtxt("Disease_SHAP_Values.txt")
topNFeatures = np.argsort(total_mean_SHAP_values)[-500:][::-1].tolist()
featureIndices = np.array(sorted(topNFeatures))

logger = logging.getLogger(__name__)

class DataService:
    def __init__(self):
        self.supported_formats = ['.csv']
        self.max_file_size = 50 * 1024 * 1024  # 50MB
        self.expected_columns = ['CpG Sites']
    
    def validate_file(self, file: UploadFile) -> Tuple[bool, str]:
        if not file.filename:
            return False, "No filename provided"
        
        if not any(file.filename.lower().endswith(fmt) for fmt in self.supported_formats):
            return False, f"Unsupported file format. Supported formats: {', '.join(self.supported_formats)}"
        
        return True, "File is valid"
    
    async def process_uploaded_file(self, file: UploadFile) -> Tuple[np.ndarray, Dict[str, Any]]:
        try:
            content = await file.read()
            
            if len(content) > self.max_file_size:
                raise ValueError(f"File too large. Maximum size: {self.max_file_size / (1024*1024):.1f}MB")
            
            df = pd.read_csv(io.BytesIO(content), index_col=0)
            
            if df.empty:
                raise ValueError("Empty CSV file")
            
            metadata = {
                "original_filename": file.filename,
                "file_size": len(content),
                "rows": len(df),
                "columns": len(df.columns)
            }

            # Convert back to numpy array
            data_array = df.T.values   # shape will be (1, n_features)

            # Create an HDF5 file and store it
            with h5py.File(io.BytesIO(), "w") as f:
                f.create_dataset("data", data=data_array)
                data = f["data"][0, featureIndices]
                data = data.reshape(1, -1)
            
            return data, metadata
            
        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {e}")
            raise ValueError(f"Error processing file: {str(e)}")
    
    def _preprocess_dataframe(self, df: pd.DataFrame, metadata: Dict[str, Any]) -> np.ndarray:
        try:
            if 'CpG Sites' in df.columns:
                df = df.set_index('CpG Sites').T
                metadata["data_format"] = "CpG sites as rows"
            else:
                metadata["data_format"] = "Samples as rows"
            
            data = df.values.astype(np.float32)
            
            if len(data.shape) == 1:
                data = data.reshape(1, -1)
            
            metadata["features_detected"] = data.shape[1]
            metadata["samples_detected"] = data.shape[0]
            
            self._validate_data_quality(data, metadata)
            
            return data
            
        except Exception as e:
            logger.error(f"Error preprocessing dataframe: {e}")
            raise ValueError(f"Data preprocessing failed: {str(e)}")
    
    def _validate_data_quality(self, data: np.ndarray, metadata: Dict[str, Any]):
        nan_count = np.isnan(data).sum()
        inf_count = np.isinf(data).sum()
        
        if nan_count > 0:
            logger.warning(f"Found {nan_count} NaN values in data")
            metadata["nan_count"] = int(nan_count)
        
        if inf_count > 0:
            logger.warning(f"Found {inf_count} infinite values in data")
            metadata["inf_count"] = int(inf_count)
        
        data_range = (np.min(data), np.max(data))
        metadata["data_range"] = [float(data_range[0]), float(data_range[1])]
        
        if data_range[0] < 0 or data_range[1] > 1:
            logger.warning(f"Data range {data_range} is outside expected methylation range [0, 1]")
            metadata["data_quality_warning"] = "Data outside expected methylation range [0, 1]"
    
    def create_demo_data(self, n_features: int = 500, n_samples: int = 1) -> Tuple[np.ndarray, Dict[str, Any]]:
        np.random.seed(42)
        
        data = np.random.beta(2, 2, size=(n_samples, n_features)).astype(np.float32)
        
        metadata = {
            "demo_data": True,
            "features_detected": n_features,
            "samples_detected": n_samples,
            "data_range": [0.0, 1.0],
            "description": f"Generated demo methylation data with {n_features} CpG sites"
        }
        
        return data, metadata
    
    def process_json_data(self, methylation_data: list, sample_id: str) -> Tuple[np.ndarray, Dict[str, Any]]:
        try:
            data = np.array(methylation_data, dtype=np.float32)
            
            if len(data.shape) == 1:
                data = data.reshape(1, -1)
            
            metadata = {
                "sample_id": sample_id,
                "features_detected": data.shape[1],
                "samples_detected": data.shape[0],
                "data_source": "json_api"
            }
            
            self._validate_data_quality(data, metadata)
            
            return data, metadata
            
        except Exception as e:
            logger.error(f"Error processing JSON data: {e}")
            raise ValueError(f"JSON data processing failed: {str(e)}")
    
    def get_sample_data_info(self) -> Dict[str, Any]:
        return {
            "description": "Sample methylation data for testing",
            "features": 500,
            "samples": 3,
            "format": "CSV with CpG sites as rows, samples as columns",
            "data_range": [0.009, 0.981],
            "file_size": "~33KB"
        }
