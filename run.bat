@echo off
cd /d "%~dp0"

if exist "envJarvis\Scripts\python.exe" (
  "envJarvis\Scripts\python.exe" run.py
) else (
  python run.py
)

if errorlevel 1 pause
