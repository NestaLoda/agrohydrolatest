$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$pythonPath = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) { throw 'Python ortami bulunamadi. README kurulumunu tamamlayin.' }
if (-not (Test-Path -LiteralPath (Join-Path $projectRoot 'frontend\dist\index.html'))) { throw 'Arayuz derlenmemis. frontend klasorunde npm ci ve npm run build calistirin.' }
Write-Host 'Uygulama: http://127.0.0.1:8000  |  Durdurmak: Ctrl+C'
& $pythonPath -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
exit $LASTEXITCODE

