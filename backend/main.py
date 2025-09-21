from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import logging

from backend.routes import prediction, health
from backend.services.model_service import ModelService

import pandas as pd
import joblib
model = joblib.load("Temp.pkl")
import h5py
import numpy as np
import io


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Load selected features
total_mean_SHAP_values = np.loadtxt("Disease_SHAP_Values.txt")
topNFeatures = np.argsort(total_mean_SHAP_values)[-500:][::-1].tolist()
featureIndices = np.array(sorted(topNFeatures))

# Global model service instance
model_service_instance = None

app = FastAPI(
    title="Epigenetic Memory Loss Methylation API",
    description="API for predicting cognitive impairment and dementia using DNA methylation profiles",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prediction.router)
app.include_router(health.router)

@app.on_event("startup")
async def startup_event():
    global model_service_instance
    try:
        model_service_instance = ModelService()
        model_service_instance.load_model()
        logger.info("Model loaded successfully on startup")
    except Exception as e:
        logger.error(f"Failed to load model on startup: {e}")

def get_model_service() -> ModelService:
    global model_service_instance
    if model_service_instance is None:
        model_service_instance = ModelService()
        try:
            model_service_instance.load_model()
        except Exception as e:
            logger.error(f"Failed to load model in dependency: {e}")
    return model_service_instance

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Epigenetic Memory Loss Methylation Analysis</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                padding: 20px;
            }
            .header {
                text-align: center;
                color: white;
                margin-bottom: 40px;
            }
            .header h1 {
                font-size: 2.5rem;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .header p {
                font-size: 1.2rem;
                opacity: 0.9;
            }
            .main-content {
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                margin-bottom: 30px;
            }
            .upload-section {
                text-align: center;
                margin-bottom: 40px;
            }
            .upload-area { 
                border: 3px dashed #667eea; 
                padding: 60px 40px; 
                text-align: center; 
                margin: 30px 0; 
                border-radius: 15px;
                background: #f8f9ff;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            .upload-area:hover { 
                background: #e8f0ff; 
                border-color: #5a6fd8;
                transform: translateY(-2px);
            }
            .upload-area.dragover {
                background: #e0e7ff;
                border-color: #4f46e5;
            }
            .upload-icon {
                font-size: 3rem;
                color: #667eea;
                margin-bottom: 20px;
            }
            .demo-section {
                background: #f0f9ff;
                border: 2px solid #0ea5e9;
                border-radius: 15px;
                padding: 30px;
                margin: 30px 0;
                text-align: center;
            }
            .demo-button {
                background: linear-gradient(135deg, #0ea5e9, #0284c7);
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 10px;
                font-size: 1.1rem;
                cursor: pointer;
                transition: all 0.3s ease;
                margin: 10px;
            }
            .demo-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(14, 165, 233, 0.3);
            }
            input[type="file"] { 
                margin: 20px 0; 
                padding: 10px;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                width: 100%;
                max-width: 400px;
            }
            .upload-button { 
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white; 
                padding: 15px 30px; 
                border: none; 
                border-radius: 10px; 
                cursor: pointer; 
                font-size: 1.1rem;
                transition: all 0.3s ease;
                margin: 10px;
            }
            .upload-button:hover { 
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            }
            .upload-button:disabled {
                background: #9ca3af;
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
            }
            .results { 
                margin-top: 40px; 
                padding: 30px; 
                background: linear-gradient(135deg, #f0fdf4, #ecfdf5);
                border-radius: 15px;
                border-left: 5px solid #10b981;
                display: none;
            }
            .prediction-card {
                background: white;
                border-radius: 15px;
                padding: 30px;
                margin: 20px 0;
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            }
            .prediction { 
                font-size: 2rem; 
                font-weight: bold; 
                margin: 15px 0;
                color: #1f2937;
            }
            .confidence { 
                font-size: 1.5rem; 
                color: #059669;
                margin: 10px 0;
            }
            .risk-percentage {
                font-size: 3rem;
                font-weight: bold;
                color: #dc2626;
                text-align: center;
                margin: 20px 0;
            }
            .risk-level {
                font-size: 1.3rem;
                font-weight: bold;
                text-align: center;
                padding: 10px;
                border-radius: 8px;
                margin: 15px 0;
            }
            .risk-low { background: #dcfce7; color: #166534; }
            .risk-moderate { background: #fef3c7; color: #92400e; }
            .risk-high { background: #fee2e2; color: #991b1b; }
            .probabilities { 
                margin: 20px 0; 
                background: #f9fafb;
                padding: 20px;
                border-radius: 10px;
            }
            .prob-bar {
                background: #e5e7eb;
                height: 25px;
                border-radius: 12px;
                margin: 10px 0;
                overflow: hidden;
                position: relative;
            }
            .prob-fill {
                height: 100%;
                border-radius: 12px;
                transition: width 0.5s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
            }
            .prob-control { background: #10b981; }
            .prob-mci { background: #f59e0b; }
            .prob-alz { background: #ef4444; }
            .calibration-section {
                background: #fef7ff;
                border: 2px solid #a855f7;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
            }
            .calibration-bar {
                background: #e5e7eb;
                height: 20px;
                border-radius: 10px;
                overflow: hidden;
                margin: 10px 0;
            }
            .calibration-fill {
                height: 100%;
                background: linear-gradient(90deg, #ef4444, #f59e0b, #10b981);
                border-radius: 10px;
                transition: width 0.5s ease;
            }
            .loading {
                display: none;
                text-align: center;
                padding: 20px;
            }
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 20px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .error {
                background: #fee2e2;
                color: #991b1b;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
                border-left: 4px solid #ef4444;
            }
            .info-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }
            .info-card {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .info-card h4 {
                color: #667eea;
                margin-bottom: 10px;
            }
            @media (max-width: 768px) {
                .container { padding: 10px; }
                .main-content { padding: 20px; }
                .header h1 { font-size: 2rem; }
                .upload-area { padding: 40px 20px; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧬 Epigenetic Memory Loss Methylation Analysis</h1>
                <p>Advanced AI-powered prediction of cognitive impairment and dementia risk</p>
            </div>
            
            <div class="main-content">
                <div class="upload-section">
                    <h2>Upload DNA Methylation Data</h2>
                    <p>Upload a CSV file with methylation data (CpG sites as columns, samples as rows)</p>
                    
                    <div class="upload-area" id="uploadArea">
                        <div class="upload-icon">📁</div>
                        <h3>Drag & Drop or Click to Upload</h3>
                        <p>Supported format: CSV files only</p>
                        <input type="file" id="fileInput" accept=".csv" style="display: none;" />
                        <button class="upload-button" onclick="document.getElementById('fileInput').click()">
                            Choose File
                        </button>
                    </div>
                    
                    <button class="upload-button" id="analyzeBtn" onclick="uploadFile()" disabled>
                        🔬 Analyze Data
                    </button>
                </div>
                
                <div class="demo-section">
                    <h3>🎯 Try with Demo Data</h3>
                    <p>Test the system with sample methylation data</p>
                    <button class="demo-button" onclick="useDemoData()">
                        Use Demo Data
                    </button>
                </div>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Analyzing methylation data...</p>
                </div>
                
                <div id="results" class="results">
                    <h3>📊 Analysis Results</h3>
                    <div id="predictionResult"></div>
                </div>
            </div>
        </div>

        <script>
            const uploadArea = document.getElementById('uploadArea');
            const fileInput = document.getElementById('fileInput');
            const analyzeBtn = document.getElementById('analyzeBtn');
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            const predictionResult = document.getElementById('predictionResult');

            // File upload handling
            fileInput.addEventListener('change', function(e) {
                if (e.target.files.length > 0) {
                    analyzeBtn.disabled = false;
                    analyzeBtn.textContent = `🔬 Analyze ${e.target.files[0].name}`;
                }
            });

            // Drag and drop functionality
            uploadArea.addEventListener('dragover', function(e) {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });

            uploadArea.addEventListener('dragleave', function(e) {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
            });

            uploadArea.addEventListener('drop', function(e) {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    fileInput.files = files;
                    analyzeBtn.disabled = false;
                    analyzeBtn.textContent = `🔬 Analyze ${files[0].name}`;
                }
            });

            uploadArea.addEventListener('click', function() {
                fileInput.click();
            });

            async function uploadFile() {
                const file = fileInput.files[0];
                if (!file) {
                    showError('Please select a file first');
                    return;
                }
                
                await performAnalysis(file);
            }

            async function useDemoData() {
                showLoading();
                try {
                    const response = await fetch('/api/v1/predict-demo');
                    if (!response.ok) {
                        throw new Error('Demo analysis failed');
                    }
                    const result = await response.json();
                    displayResults(result);
                } catch (error) {
                    showError('Error: ' + error.message);
                }
            }

            async function performAnalysis(file) {
                showLoading();
                const formData = new FormData();
                formData.append('file', file);
                
                try {
                    const response = await fetch('/api/v1/predict', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.detail || 'Analysis failed');
                    }
                    
                    const result = await response.json();
                    displayResults(result);
                } catch (error) {
                    showError('Error: ' + error.message);
                }
            }

            function showLoading() {
                loading.style.display = 'block';
                results.style.display = 'none';
            }

            function showError(message) {
                loading.style.display = 'none';
                results.style.display = 'block';
                predictionResult.innerHTML = `<div class="error">${message}</div>`;
            }

            function displayResults(result) {
                loading.style.display = 'none';
                results.style.display = 'block';
                
                const riskClass = result.risk_level.toLowerCase().replace(' ', '-');
                const riskColor = result.risk_level === 'High Risk' ? '#ef4444' : 
                                result.risk_level === 'Moderate Risk' ? '#f59e0b' : '#10b981';
                
                predictionResult.innerHTML = `
                    <div class="prediction-card">
                        <div class="prediction">Prediction: ${result.prediction}</div>
                        <div class="confidence">Confidence: ${(result.confidence * 100).toFixed(1)}%</div>
                        
                        <div class="risk-percentage" style="color: ${riskColor}">
                            ${result.risk_percentage.toFixed(1)}%
                        </div>
                        <div class="risk-level risk-${riskClass}">
                            ${result.risk_level}
                        </div>
                    </div>
                    
                    <div class="probabilities">
                        <h4>Class Probabilities:</h4>
                        <div class="prob-bar">
                            <div class="prob-fill prob-control" style="width: ${result.probabilities.Control * 100}%">
                                Control: ${(result.probabilities.Control * 100).toFixed(1)}%
                            </div>
                        </div>
                        <div class="prob-bar">
                            <div class="prob-fill prob-mci" style="width: ${result.probabilities.MCI * 100}%">
                                MCI: ${(result.probabilities.MCI * 100).toFixed(1)}%
                            </div>
                        </div>
                        <div class="prob-bar">
                            <div class="prob-fill prob-alz" style="width: ${result.probabilities["Alzheimer's"] * 100}%">
                                Alzheimer's: ${(result.probabilities["Alzheimer's"] * 100).toFixed(1)}%
                            </div>
                        </div>
                    </div>
                    
                    ${result.calibration_score ? `
                    <div class="calibration-section">
                        <h4>Model Reliability & Calibration</h4>
                        <div class="calibration-bar">
                            <div class="calibration-fill" style="width: ${result.calibration_score * 100}%"></div>
                        </div>
                        <p>Model Reliability: ${(result.calibration_score * 100).toFixed(1)}%</p>
                        <p><small>This indicates how well-calibrated the model's confidence scores are</small></p>
                    </div>
                    ` : ''}
                    
                    <div class="info-grid">
                        <div class="info-card">
                            <h4>📋 Sample Information</h4>
                            <p><strong>Sample ID:</strong> ${result.sample_id}</p>
                            <p><strong>Features Analyzed:</strong> ${result.model_insights.total_features}</p>
                            <p><strong>Model Type:</strong> ${result.model_insights.model_type}</p>
                        </div>
                        <div class="info-card">
                            <h4>🎯 Model Performance</h4>
                            <p><strong>Model Accuracy:</strong> ${result.model_insights.model_accuracy ? (result.model_insights.model_accuracy * 100).toFixed(1) + '%' : 'N/A'}</p>
                            <p><strong>Analysis Time:</strong> ${new Date(result.model_insights.timestamp).toLocaleString()}</p>
                        </div>
                    </div>
                `;
            }
        </script>
    </body>
    </html>
    """

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Read uploaded CSV
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")), index_col=0)

    # Convert to numpy array (1 sample, n_features)
    data_array = df.T.values  # shape (1, n_features)

    # Ensure we have enough columns for featureIndices
    max_index = featureIndices.max()
    if data_array.shape[1] <= max_index:
        # pad missing features with 0
        padded = np.zeros((1, max_index + 1))
        padded[:, :data_array.shape[1]] = data_array
        data_array = padded

    # Create an **in-memory HDF5 file**
    with h5py.File(io.BytesIO(), "w") as h5f:
        h5f.create_dataset("data", data=data_array)
        # Select the top features inside HDF5
        data = h5f["data"][:, featureIndices]
        prediction = model.predict(data)

    return {"prediction": prediction.tolist()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
