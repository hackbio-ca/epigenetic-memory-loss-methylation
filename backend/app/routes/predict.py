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
                xgb_model = load_xgboost_model()
                print("XGBoost model loaded")
                
                # Make predictions
                xgb_predictions = xgb_model.predict(data)
                print(f"XGBoost predictions: {xgb_predictions[:5]}...")  # Show first 5
                
                # Create predictions with sample IDs
                predictions_with_ids = []
                for i, (sample_id, prediction) in enumerate(zip(sample_ids, xgb_predictions)):
                    predictions_with_ids.append({
                        "sample_id": sample_id,
                        "prediction": int(prediction) if hasattr(prediction, 'item') else prediction
                    })
                
                return {
                    "success": True,
                    "message": "Prediction completed successfully",
                    "results": [
                        {
                            "model_name": "xgboost",
                            "prediction": xgb_predictions.tolist() if hasattr(xgb_predictions, 'tolist') else list(xgb_predictions),
                            "predictions_with_ids": predictions_with_ids
                        }
                    ],
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