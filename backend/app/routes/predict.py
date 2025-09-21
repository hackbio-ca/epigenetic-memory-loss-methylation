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

def load_cpg_annotations():
    """Load CpG site annotations from the annotation_filtered.csv file"""
    try:
        annotation_path = "./data/annotation_filtered.csv"  # Fixed path - backend runs from backend/ directory
        df = pd.read_csv(annotation_path)
        print(f"Loaded {len(df)} CpG annotations from {annotation_path}")
        print(f"Columns in annotation file: {list(df.columns)}")
        
        # Create a dictionary with IlmnID as key and annotation data as value
        annotations = {}
        for _, row in df.iterrows():
            cpg_id = row['IlmnID']
            annotations[cpg_id] = {
                'name': row['Name'] if pd.notna(row['Name']) else cpg_id,
                'chromosome': str(row['CHR']) if pd.notna(row['CHR']) else 'Unknown',
                'genomic_position': str(int(row['MAPINFO'])) if pd.notna(row['MAPINFO']) else 'Unknown',
                'gene_names': row['UCSC_RefGene_Name'] if pd.notna(row['UCSC_RefGene_Name']) else 'Unknown',
                'gene_regions': row['UCSC_RefGene_Group'] if pd.notna(row['UCSC_RefGene_Group']) else 'Unknown'
            }
        
        print(f"Created annotations dictionary with {len(annotations)} CpG sites")
        # Print a few sample annotations for debugging
        sample_keys = list(annotations.keys())[:3]
        for key in sample_keys:
            print(f"Sample annotation for {key}: {annotations[key]}")
        
        return annotations
        
    except Exception as e:
        print(f"Failed to load CpG annotations: {e}")
        import traceback
        traceback.print_exc()
        return {}

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
        csv_feature_names = []  # Store column names from CSV
        
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
                    
                    # Get numeric columns and their names
                    numeric_df = df.select_dtypes(include=['number'])
                    numeric_data = numeric_df.values.tolist()
                    data.extend(numeric_data)
                    
                    # Store the column names (CpG sites) for feature labels
                    if not csv_feature_names:  # Only set once from first file
                        csv_feature_names = list(numeric_df.columns)
                        print(f"Extracted {len(csv_feature_names)} feature names from CSV: {csv_feature_names[:5]}...")
                    
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

                # SHAP Analysis for XGBoost model
                print("Computing SHAP values...")
                try:
                    # Convert data to numpy array for SHAP
                    data_array = np.array(data)
                    print(f"Data array shape: {data_array.shape}")
                    print(f"Data array type: {type(data_array)}")
                    print(f"Data array dtype: {data_array.dtype}")
                    print(f"Sample IDs count: {len(sample_ids)}")
                    print(f"XGBoost model type: {type(xgb_model)}")
                    
                    # Test if model works with the data
                    test_pred = xgb_model.predict(data_array[:1])  # Test with first sample
                    print(f"Test prediction successful: {test_pred}")
                    
                    # Create SHAP explainer for XGBoost model
                    print("Creating SHAP explainer...")
                    
                    # Check if it's a pipeline and extract the final estimator
                    if hasattr(xgb_model, 'named_steps'):
                        print("Model is a pipeline, extracting final estimator...")
                        final_estimator = None
                        for step_name, step in xgb_model.named_steps.items():
                            print(f"Pipeline step: {step_name} -> {type(step)}")
                            final_estimator = step  # Get the last step
                        
                        if final_estimator is not None:
                            print(f"Using final estimator: {type(final_estimator)}")
                            # Transform data through the pipeline up to the final step
                            transformed_data = data_array
                            for step_name, step in list(xgb_model.named_steps.items())[:-1]:  # All steps except last
                                print(f"Applying transformation: {step_name}")
                                transformed_data = step.transform(transformed_data)
                            
                            print(f"Transformed data shape: {transformed_data.shape}")
                            explainer = shap.Explainer(final_estimator, transformed_data)
                        else:
                            print("Could not extract final estimator, using full pipeline")
                            explainer = shap.Explainer(xgb_model, data_array)
                    else:
                        print("Model is not a pipeline, using directly")
                        explainer = shap.Explainer(xgb_model, data_array)
                    
                    print("SHAP explainer created successfully")
                    
                    print("Computing SHAP values...")
                    if hasattr(xgb_model, 'named_steps') and 'transformed_data' in locals():
                        # Use transformed data for SHAP computation
                        shap_values = explainer(transformed_data)
                        data_for_shap = transformed_data
                    else:
                        # Use original data
                        shap_values = explainer(data_array)
                        data_for_shap = data_array
                    print("SHAP values computed successfully")
                    
                    print(f"SHAP values type: {type(shap_values)}")
                    print(f"SHAP values shape: {shap_values.values.shape}")
                    print(f"SHAP base values type: {type(shap_values.base_values)}")
                    print(f"SHAP base values shape: {shap_values.base_values.shape if hasattr(shap_values.base_values, 'shape') else 'scalar'}")
                    
                    # Get feature names - prioritize CSV column names
                    try:
                        if csv_feature_names and len(csv_feature_names) == data_for_shap.shape[1]:
                            feature_names = csv_feature_names
                            print(f"Using {len(feature_names)} feature names from CSV columns")
                        else:
                            # Fallback to disease CpG sites file
                            with open("./backend/data/disease_CpG_sites.txt", "r") as f:
                                feature_names = f.read().strip().splitlines()
                            print(f"Using {len(feature_names)} feature names from disease_CpG_sites.txt")
                    except Exception as fname_error:
                        print(f"Feature names loading failed: {fname_error}")
                        # Final fallback to generic names
                        feature_names = [f"Feature_{i}" for i in range(data_for_shap.shape[1])]
                        print(f"Generated {len(feature_names)} default feature names")
                    
                    # Ensure feature names match data dimensions
                    if len(feature_names) != data_for_shap.shape[1]:
                        print(f"Warning: Feature names count ({len(feature_names)}) doesn't match data features ({data_for_shap.shape[1]})")
                        feature_names = [f"Feature_{i}" for i in range(data_for_shap.shape[1])]
                        print(f"Using generic feature names instead")
                    
                    # Prepare SHAP data for frontend
                    shap_data = []
                    print(f"Processing {len(sample_ids)} samples for SHAP data...")
                    print(f"Base values type: {type(shap_values.base_values)}")
                    print(f"Base values shape/value: {shap_values.base_values.shape if hasattr(shap_values.base_values, 'shape') else shap_values.base_values}")
                    
                    for i, sample_id in enumerate(sample_ids):
                        try:
                            # Handle base values for multi-class
                            if hasattr(shap_values.base_values, 'shape') and len(shap_values.base_values.shape) > 0:
                                if len(shap_values.base_values.shape) == 2:
                                    # Multi-class base values: shape (samples, classes)
                                    predicted_class = int(xgb_predictions[i])
                                    base_val = float(shap_values.base_values[i, predicted_class])
                                else:
                                    # Single dimension base values
                                    base_val = float(shap_values.base_values[i])
                            else:
                                # Scalar base value
                                base_val = float(shap_values.base_values)
                            
                            # Handle multi-class SHAP values
                            if len(shap_values.values.shape) == 3:
                                # For multi-class, we'll use the SHAP values for the predicted class
                                predicted_class = int(xgb_predictions[i])
                                sample_shap_values = shap_values.values[i, :, predicted_class]
                                print(f"Sample {i}: Using class {predicted_class} SHAP values")
                            else:
                                # Single class case
                                sample_shap_values = shap_values.values[i]
                            
                            sample_shap = {
                                "sample_id": sample_id,
                                "base_value": base_val,
                                "shap_values": sample_shap_values.tolist(),
                                "data_values": data_for_shap[i].tolist(),
                                "predicted_class": int(xgb_predictions[i])
                            }
                            shap_data.append(sample_shap)
                            
                            if i == 0:  # Debug first sample
                                print(f"First sample SHAP data: sample_id={sample_id}, base_value={base_val}, shap_values_len={len(sample_shap_values)}, predicted_class={int(xgb_predictions[i])}")
                                print(f"First few SHAP values: {sample_shap_values[:5]}")
                                
                        except Exception as sample_error:
                            print(f"Error processing sample {i} ({sample_id}): {sample_error}")
                            import traceback
                            traceback.print_exc()
                            # Continue with next sample instead of failing completely
                    
                    print(f"Processed {len(shap_data)} samples successfully")
                    
                    # Get top features by absolute SHAP value for summary
                    print("Computing top features...")
                    
                    # Handle multi-class SHAP values (shape: samples x features x classes)
                    if len(shap_values.values.shape) == 3:
                        print(f"Multi-class SHAP detected: {shap_values.values.shape}")
                        # Take mean across classes and samples to get feature importance
                        mean_abs_shap = np.mean(np.mean(np.abs(shap_values.values), axis=2), axis=0)
                    else:
                        print(f"Single-class SHAP detected: {shap_values.values.shape}")
                        # Standard case: mean across samples
                        mean_abs_shap = np.mean(np.abs(shap_values.values), axis=0)
                        
                    print(f"Mean absolute SHAP values shape: {mean_abs_shap.shape}")
                    print(f"Mean absolute SHAP values range: {np.min(mean_abs_shap):.6f} to {np.max(mean_abs_shap):.6f}")
                    
                    # Get top 20 features
                    top_features_idx = np.argsort(mean_abs_shap)[-20:][::-1]  # Top 20 features
                    print(f"Top feature indices shape: {top_features_idx.shape}")
                    print(f"Top feature indices: {top_features_idx[:5]}...")  # Show first 5
                    
                    top_features = []
                    for idx in top_features_idx:
                        feature_name = feature_names[int(idx)] if int(idx) < len(feature_names) else f"Feature_{int(idx)}"
                        top_features.append({
                            "feature_name": feature_name,
                            "feature_index": int(idx),
                            "mean_abs_shap": float(mean_abs_shap[idx])
                        })
                    
                    print(f"Created {len(top_features)} top features")
                    print(f"Top 3 features: {[f['feature_name'] for f in top_features[:3]]}")
                    
                    print(f"SHAP computation completed successfully!")
                    print(f"Final counts - shap_data: {len(shap_data)}, top_features: {len(top_features)}, feature_names: {len(feature_names)}")
                    
                except Exception as shap_error:
                    print(f"SHAP computation failed: {shap_error}")
                    import traceback
                    traceback.print_exc()
                    shap_data = []
                    top_features = []
                    feature_names = []

                # Load feature names if not already loaded
                if 'feature_names' not in locals():
                    if csv_feature_names:
                        feature_names = csv_feature_names
                        print(f"Using {len(feature_names)} feature names from CSV")
                    else:
                        try:
                            with open("./backend/data/disease_CpG_sites.txt", "r") as f:
                                feature_names = f.read().strip().splitlines()
                            print(f"Using {len(feature_names)} feature names from file")
                        except:
                            feature_names = []
                            print("No feature names available")

                # Load CpG site annotations
                print("Loading CpG site annotations...")
                cpg_annotations = load_cpg_annotations()
                
                # Create annotations object for the features we're analyzing
                feature_annotations = {}
                for feature_name in feature_names:
                    if feature_name in cpg_annotations:
                        feature_annotations[feature_name] = cpg_annotations[feature_name]
                    else:
                        # If not found in annotations, create a placeholder
                        feature_annotations[feature_name] = {
                            'name': feature_name,
                            'chromosome': 'Unknown',
                            'genomic_position': 'Unknown',
                            'gene_names': 'Unknown',
                            'gene_regions': 'Unknown'
                        }
                
                print(f"Created feature annotations for {len(feature_annotations)} features")
                print(f"Found annotations for {sum(1 for v in feature_annotations.values() if v['chromosome'] != 'Unknown')} CpG sites")

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
                    "shap_analysis": {
                        "shap_data": shap_data,
                        "top_features": top_features,
                        "feature_names": feature_names,
                        "cpg_annotations": feature_annotations
                    },
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