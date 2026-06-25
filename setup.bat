@echo off
cd /d "%~dp0"

echo Creating virtual environment...
python -m venv envJarvis
if errorlevel 1 (
  echo Failed to create virtual environment.
  pause
  exit /b 1
)

echo Installing dependencies...
"envJarvis\Scripts\python.exe" -m pip install --upgrade pip
"envJarvis\Scripts\python.exe" -m pip install -r requirements.txt

echo.
echo Setup complete. Run Jarvis with run.bat
pause
