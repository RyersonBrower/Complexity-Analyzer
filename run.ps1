# -------------------------------------
# Algorithm Analyzer - Auto Startup Script
# -------------------------------------

Write-Host "🚀 Starting Algorithm Analyzer containers..." -ForegroundColor Cyan

Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Definition)

docker compose up -d --build

Write-Host "⏳ Waiting 10 seconds for containers to start..."
Start-Sleep -Seconds 10

Write-Host "🔍 Checking running containers..." -ForegroundColor Yellow
docker ps

Write-Host "📤 Sending test request to presentation service..." -ForegroundColor Green
$response = Invoke-RestMethod -Uri "http://localhost:5002/present" `
  -Method Post `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"code":"T(n) = 2T(n/2) + n"}'

Write-Host "✅ Response received:" -ForegroundColor Cyan
$response | ConvertTo-Json -Depth 10 | Write-Output

Write-Host "`n🎯 Done! Use 'docker compose down' to stop the containers." -ForegroundColor Yellow
