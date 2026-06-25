$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

$venvPython = Join-Path $root "envJarvis\Scripts\python.exe"
if (Test-Path $venvPython) {
    & $venvPython run.py
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    python run.py
} else {
    Write-Host "Python was not found. Run setup.bat first."
    Read-Host "Press Enter to exit"
}
