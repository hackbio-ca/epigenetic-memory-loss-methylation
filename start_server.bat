@echo off
echo Starting Epigenetic Memory Loss Methylation API...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if model file exists
if not exist "Temp.pkl" (
    echo Error: Model file 'Temp.pkl' not found
    echo Please ensure the trained model file is in this directory
    pause
    exit /b 1
)

REM Install requirements if needed
echo Installing/updating requirements...
pip install -r requirements.txt

REM Start the server
echo.
echo Starting server...
echo Server will be available at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
python run_server.py

pause

