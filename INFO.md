## Setup

From the project directory, first set up the virtual environment by running:

```
python -m venv venv
pip3 install -r requirements.txt
```

After, make sure that your front-end is set up. To do so simply run,

```
cd frontend
npm install
```

You can simply run the front-end via `npm run dev`. Make sure to user port 3000 as CORS middleware in backend is allowed only for that port in dev mode.

As for the model training, you can call the files in the fashion of `python -m model.data.loaders.loader_xgboost`, or `python -m model._dir1_._dir2_.target_file` in a more general format.

## Appendix: Project Structure

This section provides a detailed breakdown of the project's directory structure and the purpose of each component.

### 📁 Root Directory

```
epigenetic-memory-loss-methylation/
├── backend/                    # FastAPI backend server
├── frontend/                   # Next.js React frontend application  
├── model/                      # Machine learning models and training pipeline
├── Temporary/                  # Experimental scripts and utilities
├── dump/                       # Output files and temporary data storage
├── media/                      # Generated plots and visualization assets
├── venv/                       # Python virtual environment
├── requirements.txt            # Python dependencies for root project
├── README.md                   # Project documentation
├── INFO.md                     # Setup and Appendix
├── LICENSE                     # MIT license file
├── CODE_OF_CONDUCT.md          # Community guidelines
├── CONTRIBUTING.md             # Contribution guidelines
└── .gitignore                  # Git ignore patterns
```

### 🔬 Backend (`/backend/`)

**Purpose**: FastAPI-based REST API server that handles prediction requests, model inference, and SHAP analysis.

```
backend/
├── app/                        # Main application package
│   ├── config/                 # Configuration management
│   ├── controllers/            # Business logic controllers
│   ├── models/                 # Pydantic schemas and model loaders
│   ├── routes/                 # API endpoint definitions
│   ├── services/               # Core business services
│   ├── utils/                  # Utility functions and helpers
│   └── __init__.py             # Package initialization
├── data/                       # Static data files
│   ├── annotation_filtered.csv # CpG site genomic annotations
│   └── disease_CpG_sites.txt   # Disease-associated CpG site identifiers
├── main.py                     # FastAPI application entry point
├── requirements.txt            # Backend Python dependencies
├── test_setup.py               # Backend testing utilities
├── README.md                   # Backend-specific documentation
├── .env.example                # Environment variables template
└── app.log                     # Application logs
```

**Key Features**:
- RESTful API endpoints for methylation data analysis
- XGBoost and PyTorch model inference
- SHAP (SHapley Additive exPlanations) feature importance analysis
- CpG site genomic annotation integration
- CSV file processing and validation
- CORS middleware for frontend integration

### 🎨 Frontend (`/frontend/`)

**Purpose**: Next.js React application providing a user-friendly web interface for uploading methylation data and viewing analysis results.

```
frontend/
├── app/                        # Next.js app directory structure
│   ├── api/                    # API route handlers
│   ├── dashboard/              # Dashboard pages
│   ├── results/                # Results visualization pages
│   ├── layout.tsx              # Root layout component
│   ├── page.tsx                # Home page component
│   └── globals.css             # Global styles
├── components/                 # Reusable React components
│   ├── ui/                     # shadcn/ui components
│   ├── file-upload-section.tsx # File upload interface
│   ├── shap-visualization.tsx  # SHAP plots and charts
│   ├── analysis-loading-dialog.tsx # Progress indicators
│   └── ...                     # Additional UI components
├── hooks/                      # Custom React hooks
├── lib/                        # Utility libraries and API clients
├── public/                     # Static assets
├── styles/                     # CSS and styling files
├── package.json                # Node.js dependencies and scripts
├── tsconfig.json               # TypeScript configuration
├── next.config.js              # Next.js configuration
└── components.json             # UI component configuration
```

**Key Features**:
- Drag-and-drop CSV file upload
- Real-time analysis progress tracking
- Interactive SHAP feature importance visualizations
- Hover tooltips for CpG site genomic annotations
- Responsive design with Tailwind CSS
- TypeScript for type safety

### 🤖 Model (`/model/`)

**Purpose**: Machine learning pipeline for training and managing XGBoost and PyTorch models on DNA methylation data.

```
model/
├── data/                       # Training and testing datasets
│   ├── loaders/                # Data loading utilities
│   ├── train/                  # Training dataset files
│   ├── test/                   # Testing dataset files
│   ├── train.zip               # Compressed training data
│   └── test.zip                # Compressed testing data
├── models/                     # Trained model storage
│   ├── pytorch/                # PyTorch model files
│   └── xgboost/                # XGBoost model files
├── notebooks/                  # Jupyter notebooks for analysis
│   ├── pcc.ipynb               # Pearson correlation analysis
│   ├── umap.ipynb              # UMAP dimensionality reduction
│   ├── selected_feature_indices.npy # Feature selection results
│   └── umap_embedding.npy      # UMAP embeddings
├── train/                      # Training scripts
│   ├── pytorch/                # PyTorch training pipeline
│   └── xgboost/                # XGBoost training pipeline
├── utils/                      # Model utilities
│   ├── pytorch/                # PyTorch helper functions
│   └── xgboost/                # XGBoost helper functions
└── __init__.py                 # Package initialization
```

**Key Features**:
- Multi-class classification (Control, MCI, Alzheimer's)
- Feature selection and dimensionality reduction
- Model evaluation and validation
- SHAP explainability integration
- Cross-validation and hyperparameter tuning

### 🧪 Temporary (`/Temporary/`)

**Purpose**: Experimental scripts and utility functions for data preprocessing and analysis exploration.

```
Temporary/
├── ConvertCSVForModel.py       # Data format conversion utilities
├── ewas.py                     # Epigenome-wide association study tools
├── ewasFeatureSelection.py     # EWAS-based feature selection
└── newAnnotation.py            # Annotation processing scripts
```

### 📊 Media (`/media/`)

**Purpose**: Generated visualization assets and plots from model analysis.

```
media/
├── confusion_matrix.png        # Model performance confusion matrix
├── manhattan_plot.png          # GWAS-style Manhattan plot
├── roc_curve.png              # ROC curve analysis
├── shap_summary.png           # SHAP feature importance summary
└── volcano_plot.png           # Differential methylation volcano plot
```

### 🗄️ Dump (`/dump/`)

**Purpose**: Temporary output files and intermediate data storage.

```
dump/
├── out.csv                     # Processed output data
└── Temp.pkl                    # Serialized temporary objects
```

### 🔧 Configuration Files

- **`requirements.txt`**: Python dependencies for the entire project
- **`venv/`**: Python virtual environment containing all dependencies
- **`.gitignore`**: Specifies files and directories to exclude from version control
- **`LICENSE`**: MIT license governing project usage and distribution
- **`CODE_OF_CONDUCT.md`**: Community guidelines and expected behavior
- **`CONTRIBUTING.md`**: Guidelines for contributing to the project

### 🚀 Getting Started

1. **Backend Setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python main.py
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Model Training**:
   ```bash
   python -m model.train.xgboost.train_model
   python -m model.train.pytorch.train_model
   ```

This modular structure separates concerns between data processing, model training, API services, and user interface, enabling scalable development and deployment of the epigenetic analysis platform.


