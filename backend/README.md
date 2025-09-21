# Backend API Documentation

## Architecture Overview

The backend follows a clean architecture pattern with separation of concerns:

```
backend/
├── main.py              # FastAPI application entry point
├── models/
│   └── schemas.py       # Pydantic models for request/response validation
├── routes/
│   ├── prediction.py    # Prediction endpoints
│   └── health.py        # Health check endpoints
├── services/
│   ├── model_service.py # Model loading and prediction logic
│   └── data_service.py  # Data processing and validation
└── utils/               # Utility functions (future use)
```

## Key Features

### 🎯 **Enhanced Risk Assessment**
- **Clear Risk Percentage**: Shows exact risk percentage (e.g., "82% risk")
- **Risk Level Classification**: Low/Moderate/High risk with color coding
- **Confidence Intervals**: Model reliability indicators

### 📊 **Advanced Visualization**
- **Probability Bars**: Visual representation of class probabilities
- **Calibration Scores**: Model reliability and calibration metrics
- **Confidence Visualization**: Clear confidence indicators

### 🚀 **Demo Data Integration**
- **One-Click Demo**: Instant testing with sample data
- **Sample Data Info**: Detailed information about demo datasets
- **Judge-Friendly**: No need to scramble for test data

### 🔧 **Robust Architecture**
- **Service Layer**: Clean separation of business logic
- **Error Handling**: Comprehensive error management
- **Validation**: Input validation and data quality checks
- **Logging**: Detailed logging for debugging

## API Endpoints

### Core Prediction Endpoints

#### `POST /api/v1/predict`
Upload CSV file for prediction analysis.

**Request**: Multipart form data with CSV file
**Response**: `PredictionResponse` with detailed results

#### `POST /api/v1/predict-json`
Send methylation data as JSON.

**Request**: 
```json
{
  "methylation_data": [[0.8, 0.7, 0.9, ...]],
  "sample_id": "sample_001"
}
```

#### `POST /api/v1/predict-demo`
Use demo data for instant testing.

**Response**: Same as other prediction endpoints

### Information Endpoints

#### `GET /api/v1/health`
Health check and system status.

#### `GET /api/v1/model-info`
Detailed model information and performance metrics.

#### `GET /api/v1/sample-data-info`
Information about available demo datasets.

## Response Format

```json
{
  "sample_id": "filename.csv",
  "prediction": "Alzheimer's",
  "confidence": 0.85,
  "probabilities": {
    "Control": 0.10,
    "MCI": 0.05,
    "Alzheimer's": 0.85
  },
  "feature_importance": {...},
  "model_insights": {
    "model_type": "sklearn/xgboost",
    "total_features": 1000,
    "model_accuracy": 0.85,
    "timestamp": "2024-01-01T12:00:00"
  },
  "risk_level": "High Risk",
  "risk_percentage": 85.0,
  "calibration_score": 0.78
}
```

## Service Architecture

### ModelService
- **Purpose**: Handles model loading and prediction logic
- **Features**: 
  - Automatic model type detection (PyTorch/sklearn)
  - Risk assessment and classification
  - Feature importance extraction
  - Model performance metrics

### DataService
- **Purpose**: Data processing and validation
- **Features**:
  - File validation and preprocessing
  - Demo data generation
  - Data quality assessment
  - Format conversion

## Error Handling

The API provides comprehensive error handling:

- **400 Bad Request**: Invalid input data or file format
- **500 Internal Server Error**: Model or processing errors
- **503 Service Unavailable**: Model not loaded

## Performance Features

- **Async Processing**: Non-blocking file uploads
- **Data Validation**: Pre-processing validation
- **Caching**: Model loading optimization
- **Logging**: Detailed performance monitoring

## Development

### Running the Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python run_backend.py
```

### Testing

```bash
# Run comprehensive tests
python test_backend.py
```

### API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Configuration

The backend can be configured through environment variables:

- `MODEL_PATH`: Path to the model file (default: "Temp.pkl")
- `LOG_LEVEL`: Logging level (default: "INFO")
- `MAX_FILE_SIZE`: Maximum upload size (default: 50MB)

## Security Features

- **File Validation**: Strict file type checking
- **Size Limits**: Upload size restrictions
- **Input Sanitization**: Data validation and cleaning
- **CORS**: Configurable cross-origin policies

