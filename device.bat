@echo off
where adb >nul 2>&1
if errorlevel 1 (
  echo ADB not found; skipping device setup.
  exit /b 0
)

echo Disconnecting old connections...
adb disconnect >nul 2>&1
echo Setting up connected device...
adb tcpip 5555 >nul 2>&1
timeout /t 3 /nobreak >nul

set ip=
for /f "tokens=2" %%G in ('adb shell ip addr show wlan0 2^>nul ^| find "inet "') do set ipfull=%%G
if defined ipfull (
  for /f "tokens=1 delims=/" %%G in ("%ipfull%") do set ip=%%G
)

if defined ip (
  echo Connecting to device with IP %ip%...
  adb connect %ip% >nul 2>&1
)

exit /b 0
