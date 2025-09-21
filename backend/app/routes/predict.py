"""
API routes for predictions.
"""
from fastapi import APIRouter, Form, Request
from typing import Optional
import pprint
import pandas as pd
import io, numpy as np
import shap

router = APIRouter(prefix="/predict", tags=["predictions"])

@router.post("/")
async def predict_endpoint(
    request: Request,
    studyName: Optional[str] = Form(None),
    studyDescription: Optional[str] = Form(None)
):
    """Prediction endpoint with CSV processing"""
    
    print("=== ENDPOINT HIT ===")
    print(f"studyName: {studyName}")
    print(f"studyDescription: {studyDescription}")
    
    try:
        form_data = await request.form()
        print(f"Form keys: {list(form_data.keys())}")
        
        # Extract files
        files = []
        for key, value in form_data.items():
            if key.startswith('file_') and hasattr(value, 'filename'):
                files.append(value)
        
        print(f"Found {len(files)} files")
        
        # Process CSV files
        data = []
        sample_ids = []
        for file in files:
            print(f"Processing file: {file.filename}")
            if file.filename and file.filename.endswith('.csv'):
                contents = await file.read()
                df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
                print(f"CSV shape: {df.shape}")
                print(f"CSV columns: {list(df.columns)}")
                
                # Extract sample IDs (first column) and numeric data
                if len(df.columns) > 0:
                    # Get sample IDs from first column
                    ids_from_file = df.iloc[:, 0].astype(str).tolist()
                    sample_ids.extend(ids_from_file)
                    print(f"Extracted {len(ids_from_file)} sample IDs: {ids_from_file[:3]}...")
                    
                    # Convert numeric data (excluding first column if it's non-numeric)
                    numeric_data = df.select_dtypes(include=['number']).values.tolist()
                    data.extend(numeric_data)
                    print(f"Extracted {len(numeric_data)} rows of numeric data")
        
        print(f"Total data rows: {len(data)}")
        print(f"Total sample IDs: {len(sample_ids)}")
        if data:
            print(f"Sample data (first row): {data[0][:5]}...")  # Show first 5 values
        if sample_ids:
            print(f"Sample IDs: {sample_ids[:5]}...")  # Show first 5 IDs
        
        # Now add model predictions
        if data:
            try:
                # Load models and make predictions
                from ..models.loader import load_xgboost_model, load_pytorch_model
                
                print("Loading models...")
                try:
                    xgb_model = load_xgboost_model()
                    print("XGBoost model loaded successfully")
                except Exception as xgb_error:
                    print(f"XGBoost model loading failed: {xgb_error}")
                    raise Exception(f"Failed to load XGBoost model: {xgb_error}")
                
                try:
                    pytorch_model = load_pytorch_model()
                    print("PyTorch model loaded successfully")
                except Exception as pytorch_error:
                    print(f"PyTorch model loading failed: {pytorch_error}")
                    raise Exception(f"Failed to load PyTorch model: {pytorch_error}")
                
                # Make predictions
                print("Making XGBoost predictions...")
                xgb_predictions = xgb_model.predict(data)
                print(f"XGBoost predictions: {xgb_predictions[:5]}...")  # Show first 5
                
                print("Making PyTorch predictions...")
                pytorch_predictions = pytorch_model.predict(data)
                print(f"PyTorch predictions: {pytorch_predictions[:5]}...")  # Show first 5

                # Create predictions with sample IDs for both models
                xgb_predictions_with_ids = []
                pytorch_predictions_with_ids = []
                
                for i, sample_id in enumerate(sample_ids):
                    xgb_pred = int(xgb_predictions[i]) if hasattr(xgb_predictions[i], 'item') else xgb_predictions[i]
                    pytorch_pred = int(pytorch_predictions[i]) if hasattr(pytorch_predictions[i], 'item') else pytorch_predictions[i]
                    
                    xgb_predictions_with_ids.append({
                        "sample_id": sample_id,
                        "prediction": xgb_pred
                    })
                    
                    pytorch_predictions_with_ids.append({
                        "sample_id": sample_id,
                        "prediction": pytorch_pred
                    })

                # # MARK: Shap Analysis
                # explainer = shap.Explainer(xgb_model, data)
                # shap_values = explainer(data) 

                # Load feature names if available
                try:
                    with open("./disease_CpG_sites.txt", "r") as f:
                        feature_names = f.read().strip().splitlines()
                except:
                    feature_names = []

                return {
                    "success": True,
                    "message": "Prediction completed successfully",
                    "results": [
                        {
                            "model_name": "xgboost",
                            "prediction": xgb_predictions.tolist() if hasattr(xgb_predictions, 'tolist') else list(xgb_predictions),
                            "predictions_with_ids": xgb_predictions_with_ids
                        },
                        {
                            "model_name": "pytorch", 
                            "prediction": pytorch_predictions.tolist() if hasattr(pytorch_predictions, 'tolist') else list(pytorch_predictions),
                            "predictions_with_ids": pytorch_predictions_with_ids
                        }
                    ],
                    "feature_names": feature_names,
                    "metadata": {
                        "studyName": studyName,
                        "studyDescription": studyDescription,
                        "files_processed": len(files),
                        "total_rows": len(data),
                        "total_samples": len(sample_ids)
                    }
                }
                
            except Exception as model_error:
                print(f"Model error: {model_error}")
                import traceback
                traceback.print_exc()
                return {
                    "success": False,
                    "error": f"Model prediction failed: {str(model_error)}",
                    "data_processed": True
                }
        
        return {
            "success": True,
            "message": "CSV processed successfully",
            "data": {
                "studyName": studyName,
                "studyDescription": studyDescription,
                "files_processed": len(files),
                "total_rows": len(data),
                "sample_data": data[0][:3] if data else None
            }
        }
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}