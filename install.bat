@echo off
REM ZPI-WARPAI Setup Script - Run with .\install.bat in PowerShell/CMD
echo ZPI-WARPAI Setup - Local WarpAI Agent
echo.

:: Check if Ollama is installed
ollama --version >nul 2>&1
if errorlevel 1 (
    echo Ollama not found. Download from https://ollama.com/download
    pause
    exit /b 1
)

:: Create venv
python -m venv .venv
if errorlevel 1 (
    echo Python not found. Install from python.org
    pause
    exit /b 1
)

call .venv/Scripts/activate.bat
pip install --upgrade pip
pip install -r requirements.txt

:: Pull default model
ollama pull llama3.2:3b

echo Setup complete! Run 'call .venv/Scripts/activate.bat' then 'warpai --help'
echo Start Ollama service: ollama serve
pause

