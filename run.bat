@echo off
:: CreepyPasta AI - Windows Batch Runner
:: Quick launcher for the CreepyPasta AI application

echo ================================
echo    CreepyPasta AI Launcher
echo ================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

:: Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install/update dependencies
if not exist "venv\pyvenv.cfg" (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

:: Check if .env file exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and add your Reddit API credentials
    echo.
    echo Instructions:
    echo 1. Go to https://www.reddit.com/prefs/apps
    echo 2. Create a new script application
    echo 3. Copy your client ID and secret to .env file
    echo.
    pause
    exit /b 1
)

:: Create necessary directories
if not exist "logs" mkdir logs
if not exist "assets\output" mkdir assets\output

:: Ask user for number of stories
echo.
set /p num_stories="How many stories do you want to process? (default: 5): "
if "%num_stories%"=="" set num_stories=5

:: Run the application
echo.
echo Starting CreepyPasta AI...
echo Processing %num_stories% stories...
echo.

python main.py %num_stories%

:: Keep window open to see results
echo.
echo ================================
echo        Process Complete
echo ================================
echo.
echo Check the assets\output directory for generated audio files.
echo.
pause
