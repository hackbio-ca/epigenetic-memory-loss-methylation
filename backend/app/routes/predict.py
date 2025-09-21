"""
API routes for predictions.
"""
from fastapi import APIRouter, Form, Request
from typing import Optional
import pprint
import pandas as pd
import io

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
        for file in files:
            print(f"Processing file: {file.filename}")
            if file.filename and file.filename.endswith('.csv'):
                contents = await file.read()
                df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
                print(f"CSV shape: {df.shape}")
                print(f"CSV columns: {list(df.columns)}")
                # Convert to numeric data
                numeric_data = df.select_dtypes(include=['number']).values.tolist()
                data.extend(numeric_data)
                print(f"Extracted {len(numeric_data)} rows of numeric data")
        
        print(f"Total data rows: {len(data)}")
        if data:
            print(f"Sample data (first row): {data[0][:5]}...")  # Show first 5 values
        
        # Now add model predictions
        if data:
            try:
                # Load models and make predictions
                from ..models.loader import load_xgboost_model, load_pytorch_model
                
                print("Loading models...")
                xgb_model = load_xgboost_model()
                print("XGBoost model loaded")
                
                # Make predictions
                xgb_predictions = xgb_model.predict(data)
                print(f"XGBoost predictions: {xgb_predictions[:5]}...")  # Show first 5
                
                return {
                    "success": True,
                    "message": "Prediction completed successfully",
                    "results": [
                        {
                            "model_name": "xgboost",
                            "prediction": xgb_predictions.tolist() if hasattr(xgb_predictions, 'tolist') else list(xgb_predictions)
                        }
                    ],
                    "metadata": {
                        "studyName": studyName,
                        "studyDescription": studyDescription,
                        "files_processed": len(files),
                        "total_rows": len(data)
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