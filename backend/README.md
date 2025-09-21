# Backend API Documentation

## Architecture Overview

The backend follows a clean architecture pattern with separation of concerns:

```
backend/
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── start.sh / start.bat      # Setup and start scripts
├── run.sh                    # Quick run script
├── .env.example              # Environment variables template
├── app/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py       # Application configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py        # Pydantic models for request/response validation
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── prediction.py     # Prediction endpoints
│   │   └── health.py         # Health check endpoints
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── prediction_controller.py  # Business logic controllers
│   ├── services/
│   │   ├── __init__.py
│   │   └── model_service.py  # Model loading and prediction logic
│   └── utils/
│       ├── __init__.py
│       └── helpers.py        # Utility functions
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)
- Required model files in `../model/models/` directory

### Installation & Setup

#### Windows
```bash
# Clone and navigate to backend directory
cd backend

# Run the setup script (creates venv, installs deps, starts server)
start.bat
```

#### Linux/macOS
```bash
# Clone and navigate to backend directory
cd backend

# Make scripts executable
chmod +x start.sh run.sh

# Run the setup script (creates venv, installs deps, starts server)
./start.sh
```

#### Manual Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python main.py
```

## 📡 API Endpoints

### Base URL
- Local: `http://localhost:8000`
- API Prefix: `/api/v1`

### Core Endpoints

#### 🎯 Make Predictions
```http
POST /api/v1/predict
```

**Request Body:**
```json
{
  "data": [
    [1.0, 2.0, 3.0, 4.0],
    [5.0, 6.0, 7.0, 8.0]
  ],
  "model_type": "both"
}
```

**Parameters:**
- `data`: List of lists containing feature values (required)
- `model_type`: Choose from `"xgboost"`, `"pytorch"`, or `"both"` (default: `"both"`)

**Response:**
```json
{
  "success": true,
  "message": "Prediction completed successfully using both model(s)",
  "results": [
    {
      "model_name": "xgboost",
      "prediction": [0, 1],
      "probability": [[0.8, 0.2], [0.3, 0.7]],
      "confidence": 0.75
    },
    {
      "model_name": "pytorch", 
      "prediction": [0, 1],
      "probability": [[0.85, 0.15], [0.25, 0.75]],
      "confidence": 0.8
    }
  ],
  "metadata": {
    "timestamp": "2025-09-21T10:30:00.000Z",
    "model_type": "both",
    "input_samples": 2,
    "features": 4
  }
}
```

#### 🏥 Health Check
```http
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "models_loaded": {
    "xgboost": true,
    "pytorch": true
  },
  "timestamp": "2025-09-21T10:30:00.000Z"
}
```

#### 📚 API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🏗️ Architecture Details

### Service Layer Pattern
- **Controllers**: Handle HTTP requests/responses and validation
- **Services**: Contain business logic and model management
- **Models**: Define data schemas and validation rules
- **Routes**: Define API endpoints and route handlers
- **Config**: Manage application settings and environment variables

### Key Features

#### 🎯 **Dual Model Support**
- **XGBoost Model**: Gradient boosting classifier from `.pkl` file
- **PyTorch Model**: Neural network classifier from `.pkl` file
- **Flexible Selection**: Use either model individually or both together

#### 📊 **Rich Predictions**
- **Multiple Outputs**: Get predictions from one or both models
- **Confidence Scores**: Model reliability indicators
- **Probability Distributions**: Class probabilities when available
- **Metadata**: Input/output shape information and timestamps

#### 🔧 **Robust Architecture**
- **Error Handling**: Comprehensive validation and error management
- **Logging**: Detailed application and request logging
- **Health Monitoring**: Model status and system health checks
- **CORS Support**: Cross-origin resource sharing enabled

#### 🚀 **Production Ready**
- **Environment Configuration**: Flexible settings via environment variables
- **Validation**: Input data validation with detailed error messages
- **Documentation**: Auto-generated API documentation
- **Monitoring**: Health checks and logging for monitoring

## ⚙️ Configuration

### Environment Variables
Copy `.env.example` to `.env` and modify as needed:

```bash
# Application settings
APP_NAME=Epigenetic Memory Loss Prediction API
DEBUG=false

# Server settings  
HOST=0.0.0.0
PORT=8000

# Model paths
XGBOOST_MODEL_PATH=../model/models/xgboost/xgboost_model.pkl
PYTORCH_MODEL_PATH=../model/models/pytorch/model.pkl

# Logging
LOG_LEVEL=INFO
```

### Model Requirements
Ensure your `.pkl` model files are located at:
- XGBoost: `../model/models/xgboost/xgboost_model.pkl`
- PyTorch: `../model/models/pytorch/model.pkl`

The models should have a `predict()` method and optionally `predict_proba()` for probability outputs.

## � Troubleshooting

### Common Issues

#### Model Loading Errors
```bash
# Check if model files exist
ls -la ../model/models/xgboost/xgboost_model.pkl
ls -la ../model/models/pytorch/model.pkl

# Check file permissions
chmod 644 ../model/models/*/*.pkl
```

#### Port Already in Use
```bash
# Change port in .env file or environment variable
PORT=8001 python main.py
```

#### Module Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### Development

#### Running in Development Mode
```bash
# Enable debug mode for auto-reload
DEBUG=true python main.py
```

#### Adding New Endpoints
1. Create route in `app/routes/`
2. Add business logic in `app/controllers/`
3. Register router in `main.py`

#### Testing the API
```bash
# Test health endpoint
curl http://localhost:8000/api/v1/health

# Test prediction endpoint
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [[1.0, 2.0, 3.0]], "model_type": "both"}'
```

## 📝 API Examples

### Using cURL
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Single model prediction
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "data": [[0.5, 1.2, -0.3, 2.1]],
    "model_type": "xgboost"
  }'

# Both models prediction
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      [0.5, 1.2, -0.3, 2.1],
      [1.1, -0.5, 0.8, 1.9]
    ],
    "model_type": "both"
  }'
```

### Using Python requests
```python
import requests
import json

# Health check
response = requests.get("http://localhost:8000/api/v1/health")
print(response.json())

# Make prediction
data = {
    "data": [[0.5, 1.2, -0.3, 2.1], [1.1, -0.5, 0.8, 1.9]],
    "model_type": "both"
}

response = requests.post(
    "http://localhost:8000/api/v1/predict",
    json=data
)
print(json.dumps(response.json(), indent=2))
```

## 🔄 Deployment

### Production Considerations
1. Set `DEBUG=false` in environment
2. Configure proper CORS origins in `ALLOWED_ORIGINS`
3. Use a production WSGI server like Gunicorn
4. Set up proper logging and monitoring
5. Secure model file access and API endpoints

### Docker Deployment (Optional)
Create a `Dockerfile` for containerized deployment:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

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

