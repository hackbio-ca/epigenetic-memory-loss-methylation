import uvicorn
import os
import sys

if __name__ == "__main__":
    if not os.path.exists("Temp.pkl"):
        print("Warning: Temp.pkl model file not found in current directory")
        print("Please ensure the model file is present before starting the server")
        sys.exit(1)
    
    print("Starting Epigenetic Memory Loss Methylation API Server...")
    print("Server will be available at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    print("Web interface at: http://localhost:8000")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

