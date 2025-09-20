from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import numpy as np
import joblib
import torch
import os
import io
from typing import List, Dict, Any
import json
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Epigenetic Memory Loss Methylation API",
    description="API for predicting cognitive impairment and dementia using DNA methylation profiles",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionRequest(BaseModel):
    methylation_data: List[List[float]]
    sample_id: str

class PredictionResponse(BaseModel):
    sample_id: str
    prediction: str
    confidence: float
    probabilities: Dict[str, float]
    feature_importance: Dict[str, float]
    model_insights: Dict[str, Any]

class ModelManager:
    def __init__(self):
        self.model = None
        self.model_type = None
        self.feature_names = None
        self.class_names = {0: "Control", 1: "MCI", 2: "Alzheimer's"}
        
    def load_model(self, model_path: str = "Temp.pkl"):
        try:
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file {model_path} not found")
            
            logger.info(f"Loading model from {model_path}")
            
            if model_path.endswith('.pkl'):
                try:
                    self.model = joblib.load(model_path)
                    self.model_type = "sklearn/xgboost"
                    logger.info("Loaded scikit-learn/XGBoost model")
                except Exception as e:
                    logger.error(f"Failed to load as scikit-learn model: {e}")
                    try:
                        self.model = torch.load(model_path, map_location='cpu')
                        self.model_type = "pytorch"
                        logger.info("Loaded PyTorch model")
                    except Exception as e2:
                        logger.error(f"Failed to load as PyTorch model: {e2}")
                        raise Exception("Could not load model with any supported format")
            
            logger.info("Model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")
    
    def predict(self, data: np.ndarray) -> Dict[str, Any]:
        if self.model is None:
            raise HTTPException(status_code=500, detail="Model not loaded")
        
        try:
            if self.model_type == "sklearn/xgboost":
                if hasattr(self.model, 'predict_proba'):
                    probabilities = self.model.predict_proba(data)
                    prediction_idx = np.argmax(probabilities[0])
                    confidence = float(np.max(probabilities[0]))
                else:
                    prediction_idx = self.model.predict(data)[0]
                    confidence = 1.0
                    probabilities = np.array([[0.33, 0.33, 0.34]])
                
                feature_importance = {}
                if hasattr(self.model, 'feature_importances_'):
                    if hasattr(self.model, 'named_steps'):
                        classifier = self.model.named_steps['classifier']
                        if hasattr(classifier, 'feature_importances_'):
                            feature_importance = dict(zip(
                                range(len(classifier.feature_importances_)),
                                classifier.feature_importances_
                            ))
                    else:
                        feature_importance = dict(zip(
                            range(len(self.model.feature_importances_)),
                            self.model.feature_importances_
                        ))
            
            elif self.model_type == "pytorch":
                self.model.eval()
                with torch.no_grad():
                    if isinstance(data, np.ndarray):
                        data = torch.tensor(data, dtype=torch.float32)
                    probabilities = self.model(data)
                    prediction_idx = torch.argmax(probabilities, dim=1).item()
                    confidence = float(torch.max(probabilities).item())
                    probabilities = probabilities.numpy()[0]
                
                feature_importance = {}
            
            prediction = self.class_names.get(prediction_idx, "Unknown")
            prob_dict = {
                self.class_names[i]: float(prob) 
                for i, prob in enumerate(probabilities)
            }
            
            model_insights = {
                "model_type": self.model_type,
                "total_features": len(data[0]) if len(data.shape) > 1 else len(data),
                "prediction_confidence": confidence,
                "risk_assessment": self._assess_risk(prediction, confidence)
            }
            
            return {
                "prediction": prediction,
                "confidence": confidence,
                "probabilities": prob_dict,
                "feature_importance": feature_importance,
                "model_insights": model_insights
            }
            
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    
    def _assess_risk(self, prediction: str, confidence: float) -> str:
        if prediction == "Alzheimer's" and confidence > 0.7:
            return "High Risk - Immediate clinical evaluation recommended"
        elif prediction == "MCI" and confidence > 0.6:
            return "Moderate Risk - Regular monitoring advised"
        elif prediction == "Alzheimer's" and confidence > 0.5:
            return "Moderate Risk - Further testing recommended"
        else:
            return "Low Risk - Continue routine monitoring"

model_manager = ModelManager()

@app.on_event("startup")
async def startup_event():
    model_manager.load_model()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Epigenetic Memory Loss Methylation Analysis</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .upload-area { border: 2px dashed #3498db; padding: 40px; text-align: center; margin: 20px 0; border-radius: 10px; }
            .upload-area:hover { background-color: #f8f9fa; }
            input[type="file"] { margin: 10px 0; }
            button { background-color: #3498db; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            button:hover { background-color: #2980b9; }
            .results { margin-top: 30px; padding: 20px; background-color: #ecf0f1; border-radius: 5px; }
            .prediction { font-size: 24px; font-weight: bold; margin: 10px 0; }
            .confidence { font-size: 18px; color: #27ae60; }
            .probabilities { margin: 15px 0; }
            .risk-assessment { padding: 15px; background-color: #fff3cd; border-left: 4px solid #ffc107; margin: 15px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧬 Epigenetic Memory Loss Methylation Analysis</h1>
            <p>Upload DNA methylation data to predict cognitive impairment and dementia risk.</p>
            
            <div class="upload-area">
                <h3>Upload Methylation Data</h3>
                <p>Please upload a CSV file with methylation data (CpG sites as columns, samples as rows)</p>
                <input type="file" id="fileInput" accept=".csv" />
                <br>
                <button onclick="uploadFile()">Analyze Data</button>
            </div>
            
            <div id="results" class="results" style="display: none;">
                <h3>Analysis Results</h3>
                <div id="predictionResult"></div>
            </div>
        </div>

        <script>
            async function uploadFile() {
                const fileInput = document.getElementById('fileInput');
                const file = fileInput.files[0];
                
                if (!file) {
                    alert('Please select a file first');
                    return;
                }
                
                const formData = new FormData();
                formData.append('file', file);
                
                try {
                    const response = await fetch('/predict', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (!response.ok) {
                        throw new Error('Analysis failed');
                    }
                    
                    const result = await response.json();
                    displayResults(result);
                } catch (error) {
                    alert('Error: ' + error.message);
                }
            }
            
            function displayResults(result) {
                const resultsDiv = document.getElementById('results');
                const predictionDiv = document.getElementById('predictionResult');
                
                predictionDiv.innerHTML = `
                    <div class="prediction">Prediction: ${result.prediction}</div>
                    <div class="confidence">Confidence: ${(result.confidence * 100).toFixed(1)}%</div>
                    
                    <div class="probabilities">
                        <h4>Class Probabilities:</h4>
                        <ul>
                            <li>Control: ${(result.probabilities.Control * 100).toFixed(1)}%</li>
                            <li>MCI: ${(result.probabilities.MCI * 100).toFixed(1)}%</li>
                            <li>Alzheimer's: ${(result.probabilities["Alzheimer's"] * 100).toFixed(1)}%</li>
                        </ul>
                    </div>
                    
                    <div class="risk-assessment">
                        <strong>Risk Assessment:</strong> ${result.model_insights.risk_assessment}
                    </div>
                    
                    <div>
                        <h4>Model Insights:</h4>
                        <ul>
                            <li>Model Type: ${result.model_insights.model_type}</li>
                            <li>Features Analyzed: ${result.model_insights.total_features}</li>
                        </ul>
                    </div>
                `;
                
                resultsDiv.style.display = 'block';
            }
        </script>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model_manager.model is not None}

@app.post("/predict", response_model=PredictionResponse)
async def predict_from_file(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")
        
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))
        
        if df.empty:
            raise HTTPException(status_code=400, detail="Empty CSV file")
        
        if 'CpG Sites' in df.columns:
            df = df.set_index('CpG Sites').T
        
        data = df.values.astype(np.float32)
        
        if len(data.shape) == 1:
            data = data.reshape(1, -1)
        
        result = model_manager.predict(data)
        
        return PredictionResponse(
            sample_id=file.filename,
            prediction=result["prediction"],
            confidence=result["confidence"],
            probabilities=result["probabilities"],
            feature_importance=result["feature_importance"],
            model_insights=result["model_insights"]
        )
        
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/predict-json", response_model=PredictionResponse)
async def predict_from_json(request: PredictionRequest):
    try:
        data = np.array(request.methylation_data, dtype=np.float32)
        
        if len(data.shape) == 1:
            data = data.reshape(1, -1)
        
        result = model_manager.predict(data)
        
        return PredictionResponse(
            sample_id=request.sample_id,
            prediction=result["prediction"],
            confidence=result["confidence"],
            probabilities=result["probabilities"],
            feature_importance=result["feature_importance"],
            model_insights=result["model_insights"]
        )
        
    except Exception as e:
        logger.error(f"Error processing JSON data: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing data: {str(e)}")

@app.get("/model-info")
async def get_model_info():
    return {
        "model_loaded": model_manager.model is not None,
        "model_type": model_manager.model_type,
        "class_names": model_manager.class_names,
        "supported_formats": ["CSV"],
        "description": "Epigenetic Memory Loss Methylation Prediction Model"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
