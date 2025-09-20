# epigenetic-memory-loss-methylation

Epigenetic Markers of Memory Loss: Using DNA Methylation Profiles to Predict Cognitive Impairment and Dementia

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Abstract

Epigenetics involves the changes in gene expression without altering the DNA sequence and can be passed down through generations. It is regulated by chemical modifications which alter the DNA molecule to inhibit or express a gene. One such mechanism is called DNA methylation which adds a methyl group to the CpG dinucleotide of the DNA molecule. Both environmental factors and genetics can shape DNA methylation patterns and whether or not a gene is expressed. Alzheimer’s disease, a neurodegenerative condition affected by both genetic factors and environment, may therefore be studied through these epigenetic signatures. By analyzing DNA methylation profiles, we aim to monitor cognitive decline, identify disease-associated genes and CpG sites, and predict Alzheimer’s risk using machine learning. In this project, DNA methylation profiles extracted from blood samples of individuals with Alzheimer’s disease, those experiencing cognitive impairment, and healthy controls will be used to create a dataset for training the machine learning model. This model will predict the likelihood of Alzheimer’s as well as monitor cognitive decline based on methylation patterns. Furthermore, by analyzing feature importance scores from the trained model, we can identify the specific methylation sites and genes most strongly associated with Alzheimer’s, offering valuable insights into disease mechanisms, potential biomarkers, and cognitive impairment.

## Installation

Install the required dependencies for the project:

```bash
# Install Python dependencies
pip install -r requirements.txt
```

## Quick Start

### 1. Start the FastAPI Server

```bash
# Run the new backend server
python run_backend.py
```

The server will start at `http://localhost:8000` with:
- **Web interface**: `http://localhost:8000` (Enhanced UI with demo data)
- **API documentation**: `http://localhost:8000/docs`
- **Health check**: `http://localhost:8000/api/v1/health`
- **Demo prediction**: `http://localhost:8000/api/v1/predict-demo`

### 2. Upload DNA Methylation Data

You can upload DNA methylation data in two ways:

#### Web Interface
1. Open `http://localhost:8000` in your browser
2. **Upload a CSV file** with methylation data OR **click "Use Demo Data"** for instant testing
3. View enhanced prediction results with:
   - Clear risk percentage (e.g., "82% risk")
   - Risk level classification (Low/Moderate/High)
   - Confidence and calibration scores
   - Visual probability bars
   - Model reliability indicators

#### API Endpoints
```python
import requests

# Upload file via API
with open('sample_methylation_data.csv', 'rb') as f:
    response = requests.post('http://localhost:8000/api/v1/predict', files={'file': f})
    result = response.json()
    print(f"Prediction: {result['prediction']}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Risk Percentage: {result['risk_percentage']:.1f}%")
    print(f"Confidence: {result['confidence']:.2%}")

# Use demo data for instant testing
response = requests.post('http://localhost:8000/api/v1/predict-demo')
result = response.json()
print(f"Demo Prediction: {result['prediction']}")
```

## Usage

### Data Format

The API expects CSV files with DNA methylation data where:
- **Rows**: CpG sites (methylation markers)
- **Columns**: Samples
- **Values**: Methylation beta values (0-1 range)

Example format:
```csv
CpG Sites,Sample_1,Sample_2,Sample_3
cg00000029,0.8,0.7,0.9
cg00000108,0.6,0.5,0.8
...
```

### API Endpoints

#### POST `/api/v1/predict`
Upload a CSV file for prediction analysis.

#### POST `/api/v1/predict-json`
Send methylation data as JSON for prediction.

#### POST `/api/v1/predict-demo`
Use demo data for instant testing (judge-friendly).

#### GET `/api/v1/model-info`
Get detailed information about the loaded model.

#### GET `/api/v1/health`
Check server and model status.

#### GET `/api/v1/sample-data-info`
Get information about available demo datasets.

**Enhanced Response Format:**
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

### Model Outputs

The system provides three prediction classes:
- **Control**: Healthy individuals
- **MCI**: Mild Cognitive Impairment
- **Alzheimer's**: Alzheimer's Disease

Each prediction includes:
- **Clear Risk Percentage**: Exact risk percentage (e.g., "82% risk")
- **Risk Level Classification**: Low/Moderate/High risk with color coding
- **Confidence Score**: Model's certainty (0-1)
- **Class Probabilities**: Visual probability bars for each class
- **Feature Importance**: Most influential CpG sites
- **Model Calibration**: Reliability and calibration scores
- **Clinical Assessment**: Risk interpretation and recommendations

## 🎯 Key Features for Judges

### **Demo Data Button**
- **One-click testing**: No need to scramble for test data
- **Instant results**: Immediate prediction with sample data
- **Consistent testing**: Same demo data for all evaluations

### **Enhanced Risk Display**
- **Clear percentages**: "82% Alzheimer's risk" instead of just "High risk"
- **Visual indicators**: Color-coded risk levels and probability bars
- **Confidence metrics**: Model reliability and calibration scores

### **Professional Interface**
- **Drag & drop upload**: Easy file handling
- **Real-time feedback**: Loading states and progress indicators
- **Comprehensive results**: All metrics in one view

## Contribute

Contributions are welcome! If you'd like to contribute, please open an issue or submit a pull request. See the [contribution guidelines](CONTRIBUTING.md) for more information.

## Support

If you have any issues or need help, please open an [issue](https://github.com/hackbio-ca/demo-project/issues) or contact the project maintainers.

## License

This project is licensed under the [MIT License](LICENSE).
