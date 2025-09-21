import uvicorn
import os
import sys

if __name__ == "__main__":
    if not os.path.exists("Temp.pkl"):
        print("Warning: Temp.pkl model file not found in current directory")
        print("Please ensure the model file is present before starting the server")
        sys.exit(1)
    
    print("Starting Epigenetic Memory Loss Methylation API Server...")
    print("Server will be available at:")
    print("  - Web interface: http://localhost:8000")
    print("  - API documentation: http://localhost:8000/docs")
    print("  - Health check: http://localhost:8000/api/v1/health")
    print("  - Demo prediction: http://localhost:8000/api/v1/predict-demo")
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

