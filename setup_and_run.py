import subprocess
import sys
import os
import time

def install_requirements():
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def check_model_file():
    if not os.path.exists("Temp.pkl"):
        print("❌ Model file 'Temp.pkl' not found!")
        print("   Please ensure the trained model file is in the current directory")
        return False
    else:
        print("✅ Model file 'Temp.pkl' found")
        return True

def start_server():
    print("Starting FastAPI server...")
    print("Server will be available at:")
    print("  - Web interface: http://localhost:8000")
    print("  - API docs: http://localhost:8000/docs")
    print("  - Health check: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        subprocess.run([sys.executable, "run_server.py"])
    except KeyboardInterrupt:
        print("\nServer stopped by user")

def main():
    print("🧬 Epigenetic Memory Loss Methylation API Setup")
    print("=" * 50)
    
    # Check if model file exists
    if not check_model_file():
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    print("\n" + "=" * 50)
    print("Setup complete! Starting server...")
    print("=" * 50)
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()

